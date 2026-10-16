"""Live console (FastAPI + Jinja2 + server-sent events): five screens driven by run-log events.

Routes:
- `GET /` lists runs; `GET /run/{run_id}` is the five-screen page (keys 1-5, `F`).
- `GET /events/{run_id}` streams raw events (id = seq, Last-Event-ID resumes; CONTRACTS §8.1).
- `GET /screens/{run_id}` streams the screens: the server tails the same run log, folds the events
  into ConsoleState, renders the screens with autoescape, and sends only the screens that changed.
- `GET /runs/{run_id}/files/{path}` serves board screenshots (PNG only, inside the run dir).

The browser uses the EventSource API (DESIGN D-15); there is no frontend build step and nothing
loads from a CDN.
"""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import AsyncIterator, Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

from shipharness.console.report import Report, exports_signature, load_report
from shipharness.console.screens import ScreenContext, ScreenRenderer
from shipharness.console.state import ConsoleState
from shipharness.events import LogTail, read_events

HERE = Path(__file__).parent
_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,80}$")
CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; "
    "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
)


async def sse_events(
    log_path: Path,
    after_seq: int = 0,
    *,
    follow: bool = True,
    poll_s: float = 0.25,
    should_stop: Callable[[], bool] | None = None,
) -> AsyncIterator[dict[str, str]]:
    """Yield SSE messages (id = seq, event = type, data = event JSON) after `after_seq`.

    The log is tailed by byte offset, so a malformed line is skipped and logged once (not on
    every poll) and a partial last line is held until it is complete."""
    tail = LogTail(log_path)
    last = after_seq
    while True:
        for event in tail.read():
            if event.seq <= last:
                continue
            last = event.seq
            yield {"id": str(event.seq), "event": event.type, "data": event.model_dump_json()}
        if not follow or (should_stop is not None and should_stop()):
            return
        await asyncio.sleep(poll_s)


async def screen_updates(
    log_path: Path,
    exports_dir: Path,
    renderer: ScreenRenderer,
    run_id: str,
    *,
    follow: bool = True,
    poll_s: float = 0.5,
    should_stop: Callable[[], bool] | None = None,
) -> AsyncIterator[dict[str, str]]:
    """First message: every screen. Then, after new events or changed exports, only the screens
    whose HTML changed. Message id = last folded seq."""
    state = ConsoleState()
    tail = LogTail(log_path)
    sent: dict[str, str] = {}
    signature: object = None
    report = Report()
    first = True
    while True:
        new = state.extend(tail.read())
        current = exports_signature(exports_dir)
        exports_changed = current != signature
        if exports_changed:
            signature, report = current, load_report(exports_dir)
        if first or new or exports_changed:
            ctx = ScreenContext(run_id, state, report, str(exports_dir))
            screens = renderer.render_all(ctx)
            delta = {k: html for k, html in screens.items() if sent.get(k) != html}
            if first or delta:
                sent.update(delta)
                payload = {"seq": state.seq, "recorded": state.recorded, "screens": delta}
                yield {"id": str(state.seq), "event": "screens", "data": json.dumps(payload)}
            first = False
        if not follow or (should_stop is not None and should_stop()):
            return
        await asyncio.sleep(poll_s)


def _run_dir(runs_dir: Path, run_id: str) -> Path:
    if not _RUN_ID.match(run_id):
        raise HTTPException(status_code=400, detail="invalid run id")
    run_dir = (runs_dir / run_id).resolve()
    if run_dir.parent != runs_dir.resolve() or not (run_dir / "events.jsonl").exists():
        raise HTTPException(status_code=404, detail="run not found")
    return run_dir


def _log_for(runs_dir: Path, run_id: str) -> Path:
    return _run_dir(runs_dir, run_id) / "events.jsonl"


def create_console_app(runs_dir: Path, exports_dir: Path | None = None) -> FastAPI:
    """The console app. `exports_dir` (screen 4) defaults to the EXPORTS_DIR setting."""
    runs_dir = Path(runs_dir)
    if exports_dir is None:
        from shipharness.config import get_settings

        exports_dir = get_settings().exports_dir
    exports_dir = Path(exports_dir)
    renderer = ScreenRenderer()
    templates = Jinja2Templates(env=renderer.env)
    app = FastAPI(title="shipharness console", docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

    @app.middleware("http")
    async def security_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
        response: Response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", CSP)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        runs = sorted(
            (
                p.parent.name
                for p in runs_dir.glob("*/events.jsonl")
                if _RUN_ID.match(p.parent.name)
            ),
            reverse=True,
        )
        return templates.TemplateResponse(request, "index.html", {"runs": runs})

    @app.get("/run/{run_id}", response_class=HTMLResponse)
    def run_page(request: Request, run_id: str) -> HTMLResponse:
        log = _log_for(runs_dir, run_id)
        state = ConsoleState.from_events(read_events(log))
        ctx = ScreenContext(run_id, state, load_report(exports_dir), str(exports_dir))
        return templates.TemplateResponse(
            request,
            "run.html",
            {"run_id": run_id, "state": state, "rendered": renderer.render_all(ctx)},
        )

    @app.get("/events/{run_id}")
    async def events(request: Request, run_id: str, follow: bool = True) -> EventSourceResponse:
        log = _log_for(runs_dir, run_id)
        last_id = request.headers.get("Last-Event-ID", "0")
        after = int(last_id) if last_id.isdigit() else 0
        # sse-starlette cancels the generator when the client disconnects.
        return EventSourceResponse(sse_events(log, after, follow=follow), ping=15)

    @app.get("/screens/{run_id}")
    async def screens(run_id: str, follow: bool = True) -> EventSourceResponse:
        log = _log_for(runs_dir, run_id)
        # The screens are a fold over the whole log, so a reconnect rebuilds from seq 0 and
        # sends a full snapshot; Last-Event-ID is not needed here.
        return EventSourceResponse(
            screen_updates(log, exports_dir, renderer, run_id, follow=follow), ping=15
        )

    @app.get("/runs/{run_id}/files/{path:path}")
    def run_file(run_id: str, path: str) -> FileResponse:
        run_dir = _run_dir(runs_dir, run_id)
        target = (run_dir / path).resolve()
        if run_dir not in target.parents or target.suffix.lower() != ".png" or not target.is_file():
            raise HTTPException(status_code=404, detail="file not found")
        return FileResponse(target, media_type="image/png")

    return app
