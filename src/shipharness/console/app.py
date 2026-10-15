"""Live console (FastAPI + Jinja2 + server-sent events). Screens are built on this in M4."""

from __future__ import annotations

import asyncio
import re
from collections.abc import AsyncIterator, Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

from shipharness.events import read_events

HERE = Path(__file__).parent
_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,80}$")


async def sse_events(
    log_path: Path,
    after_seq: int = 0,
    *,
    follow: bool = True,
    poll_s: float = 0.25,
    should_stop: Callable[[], bool] | None = None,
) -> AsyncIterator[dict[str, str]]:
    """Yield SSE messages (id = seq, event = type, data = event JSON) after `after_seq`."""
    last = after_seq
    while True:
        for event in read_events(log_path, after_seq=last):
            last = event.seq
            yield {"id": str(event.seq), "event": event.type, "data": event.model_dump_json()}
        if not follow or (should_stop is not None and should_stop()):
            return
        await asyncio.sleep(poll_s)


def _log_for(runs_dir: Path, run_id: str) -> Path:
    if not _RUN_ID.match(run_id):
        raise HTTPException(status_code=400, detail="invalid run id")
    log = (runs_dir / run_id / "events.jsonl").resolve()
    if runs_dir.resolve() not in log.parents or not log.exists():
        raise HTTPException(status_code=404, detail="run not found")
    return log


def create_console_app(runs_dir: Path) -> FastAPI:
    runs_dir = Path(runs_dir)
    templates = Jinja2Templates(directory=HERE / "templates")
    app = FastAPI(title="shipharness console", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        runs = sorted(
            (p.parent.name for p in runs_dir.glob("*/events.jsonl")),
            reverse=True,
        )
        return templates.TemplateResponse(request, "index.html", {"runs": runs})

    @app.get("/events/{run_id}")
    async def events(request: Request, run_id: str, follow: bool = True) -> EventSourceResponse:
        log = _log_for(runs_dir, run_id)
        last_id = request.headers.get("Last-Event-ID", "0")
        after = int(last_id) if last_id.isdigit() else 0
        # sse-starlette cancels the generator when the client disconnects.
        return EventSourceResponse(sse_events(log, after, follow=follow), ping=15)

    return app
