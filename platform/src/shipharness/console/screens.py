"""Render the five console screens from ConsoleState and the exports report.

Screens are server-rendered HTML fragments with Jinja autoescape on: turn excerpts, tool targets,
file paths, and check details come from the agent or its build and are hostile. The browser only
swaps the fragments in, so it never builds markup from agent strings.

Readability rules: text >= 20 px, high contrast, <= 3 panels per screen, symbol +
label on every status (never colour alone), fixed 1920x1080 layout, `F` full screen for one arm.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from shipharness.console.report import Report, safe_url
from shipharness.console.state import ARMS, ConsoleState, measure_values

HERE = Path(__file__).parent

# key -> (symbol, label, tone). Tones map to colours; the symbol and label carry the meaning.
STATUS: dict[str, tuple[str, str, str]] = {
    "pass": ("✓", "pass", "good"),
    "fail": ("✗", "fail", "bad"),
    "pending": ("⏳", "pending", "wait"),
    "skipped": ("–", "skipped", "muted"),
    "done": ("✓", "done", "good"),
    "not_done": ("✗", "not done", "bad"),
    "none": ("–", "no claim", "muted"),
    "killed": ("✓", "killed", "good"),
    "survived": ("✗", "survived", "bad"),
    "timeout": ("◷", "timeout", "warn"),
    "error": ("!", "error", "warn"),
    "changed": ("✎", "changed", "info"),
    "blocked": ("⊘", "blocked", "warn"),
    "reverted": ("↺", "reverted", "warn"),
    "out of scope": ("⚠", "out of scope", "bad"),
    "denied": ("⊘", "denied", "warn"),
    "redone": ("↺", "redone", "bad"),
    "other_org": ("⚠", "other org", "bad"),
    "duplicate": ("⧉", "duplicate", "bad"),
    "lost_update": ("✗", "lost update", "bad"),
    "conflict_detected": ("✓", "conflict detected", "good"),
    "kept": ("✓", "kept", "good"),
    "discarded": ("✗", "discarded", "bad"),
    "accept": ("✓", "accept", "good"),
    "reject": ("✗", "reject", "bad"),
    "supported": ("✓", "claim supported", "good"),
    "unsupported": ("✗", "claim not supported", "bad"),
    "unknown": ("?", "unknown", "muted"),
    "gate_fail": ("✗", "gate fail", "bad"),
    "gate_pass": ("✓", "gate pass", "good"),
    "block": ("⊘", "block", "warn"),
    "revert": ("↺", "revert", "warn"),
    "allow": ("✓", "allow", "good"),
    "note": ("•", "note", "info"),
    "status_set": ("★", "status set", "good"),
    "session_stop": ("■", "session stop", "info"),
    "session_resume": ("▶", "session resume", "info"),
}

SCREENS: tuple[tuple[str, str, str], ...] = (
    ("1", "live", "Live Console"),
    ("2", "boards", "Boards"),
    ("3", "evidence", "Evidence"),
    ("4", "report", "A/B Report"),
    ("5", "traces", "Traces"),
)


def status(key: str, label: str | None = None) -> Markup:
    """A status pill: symbol + label, tone class for colour. Unknown keys render as '?'."""
    symbol, default_label, tone = STATUS.get(key, STATUS["unknown"])
    if label is None:
        label = default_label if key in STATUS else str(key)
    text = label
    return Markup(
        '<span class="status tone-{tone}"><span class="sym" aria-hidden="true">{sym}</span> '
        '<span class="label">{label}</span></span>'
    ).format(tone=tone, sym=symbol, label=text)


def mmss(seconds: float | int | None) -> str:
    if seconds is None:
        return "--:--"
    total = max(0, int(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def usd(value: float | None, places: int = 3) -> str:
    return "–" if value is None else f"${value:.{places}f}"


def width_class(part: int, total: int) -> str:
    """Bar width as a class in 5-point steps (no inline styles under the CSP)."""
    if total <= 0:
        return "w-0"
    return f"w-{round(part / total * 20) * 5}"


def short_test(test_id: str) -> str:
    return test_id.rsplit("::", 1)[-1]


def file_url(run_id: str, path: str) -> str:
    """Screenshot URL. Each capture has its own file name, so no cache buster is needed."""
    return f"/runs/{quote(run_id)}/files/{quote(path)}"


@dataclass
class ScreenContext:
    run_id: str
    state: ConsoleState
    report: Report
    exports_dir: str


class ScreenRenderer:
    def __init__(self, templates_dir: Path | None = None) -> None:
        self.env = Environment(
            loader=FileSystemLoader(templates_dir or HERE / "templates"),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.globals.update(
            status=status,
            mmss=mmss,
            usd=usd,
            width_class=width_class,
            short_test=short_test,
            safe_url=safe_url,
            file_url=file_url,
            arms=ARMS,
            screens=SCREENS,
            escape=escape,
            measure_values=measure_values,
        )

    def render(self, key: str, ctx: ScreenContext) -> str:
        name = dict((k, n) for k, n, _ in SCREENS)[key]
        title = dict((k, t) for k, _, t in SCREENS)[key]
        template = self.env.get_template(f"screens/{name}.html")
        return template.render(
            key=key,
            title=title,
            run_id=ctx.run_id,
            state=ctx.state,
            report=ctx.report,
            exports_dir=ctx.exports_dir,
        )

    def render_all(self, ctx: ScreenContext) -> dict[str, str]:
        return {key: self.render(key, ctx) for key, _, _ in SCREENS}
