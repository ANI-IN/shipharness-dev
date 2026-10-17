"""Shared layouts for the round-2 diagrams: a numbered story strip, a Socratic build-up, a
timeline, a four-idea cheat sheet, and the small icons the cheat sheets use.

All sizes are canvas units of a "wide" canvas (1920x1080); text sizes come from style.py.
"""

from __future__ import annotations

from exlib import Scene, metrics
from style import (
    AMBER,
    BLUE,
    FONT_BODY,
    FONT_SMALL,
    FONT_TITLE,
    GREY,
    INK,
    RED,
    STROKE_WIDTH_BOLD,
    tint,
)

LEFT, RIGHT = 60, 1860
CENTRE = 960


def title(s: Scene, text: str, y: float = 50) -> None:
    s.text(CENTRE, y, text, FONT_TITLE, INK, "center")


def footnote(s: Scene, text: str, y: float = 985) -> None:
    s.text(RIGHT, y, text, FONT_SMALL, INK, "right")


# -- story strip ---------------------------------------------------------------------------------


def story_strip(
    s: Scene,
    heading: str,
    rows: list[tuple[str | None, list[str]]],
    note: str | None = None,
) -> None:
    """Numbered steps, left to right, row by row. The last step is the failure (red)."""
    title(s, heading)
    total = sum(len(r[1]) for r in rows)
    n = 0
    prev = None
    top = 190
    row_gap = 340
    for r, (row_label, steps) in enumerate(rows):
        y = top + r * row_gap
        if row_label:
            s.text(RIGHT, y - 4, row_label, FONT_BODY, INK, "right")
            y += 40
        k = len(steps)
        gap = 90
        w = (RIGHT - LEFT - (k - 1) * gap) / k
        for i, label in enumerate(steps):
            n += 1
            x = LEFT + i * (w + gap)
            last = n == total
            b = s.box(
                x,
                y,
                w,
                190,
                f"{n}\n{label}",
                role="fail" if last else "plain",
                stroke_width=STROKE_WIDTH_BOLD if last else 2,
            )
            if prev is not None:
                if i == 0:
                    py = prev["y"] + prev["height"] + 8
                    mid = py + 24
                    s.arrow(
                        prev,
                        b,
                        start="bottom",
                        end="top",
                        via=[(prev["x"] + prev["width"] / 2, mid), (x + w / 2, mid)],
                    )
                else:
                    s.arrow(prev, b, start="right", end="left")
            prev = b
    if note:
        footnote(s, note)


# -- Socratic build-up ---------------------------------------------------------------------------


def socratic(
    s: Scene,
    question: str,
    answer: str,
    reasons: list[str],
    closing: str,
    frames: int,
) -> None:
    """Frame 1: the question. Then the answer, then the reasons (with the closing question).
    With frames=2 the answer and the reasons come together in frame 2."""
    s.stage = 1
    q = s.box(360, 60, 1200, 190, question, role="accent", size=FONT_TITLE, stroke_width=3)
    s.stage = 2
    a = s.box(560, 360, 800, 130, answer, role="fail", size=FONT_TITLE, stroke_width=3)
    s.arrow(q, a, start="bottom", end="top")
    s.stage = 3 if frames == 3 else 2
    k = len(reasons)
    gap = 80
    w = (RIGHT - LEFT - (k - 1) * gap) / k
    for i, label in enumerate(reasons):
        x = LEFT + i * (w + gap)
        r = s.box(x, 620, w, 190, label, role="neutral")
        s.arrow(a, r, start="bottom", end="top")
        s.text(x + 24, 632, f"{i + 1}", FONT_BODY, INK)
    s.box(610, 880, 700, 100, closing, role="ghost", dashed=True)


# -- timeline -------------------------------------------------------------------------------------


def _fmt(t: float) -> str:
    return f"{int(t) // 60}:{int(t) % 60:02d}"


def timeline(
    s: Scene,
    heading: str,
    lanes: list[tuple[str | None, str, list[tuple[float, str, str]]]],
    end: float,
    end_label: str,
    note: str,
    bars: list[tuple[float, float, str]] | None = None,
) -> None:
    """lanes: (lane name or None, role, [(seconds, label, role)]). One lane: labels alternate
    above and below the line. Two lanes: lane 1 labels above, lane 2 labels below."""
    title(s, heading)
    m = metrics()
    named = any(name for name, _, _ in lanes)
    x0 = 330 if named else 120
    x1 = 1740

    def xt(t: float) -> float:
        return x0 + (x1 - x0) * t / end

    ys = [520] if len(lanes) == 1 else [400, 590]
    for li, (name, role, ticks) in enumerate(lanes):
        ly = ys[li]
        s.line([(x0, ly), (x1, ly)], color=INK, stroke_width=3)
        if name:
            s.box(LEFT, ly - 40, 230, 80, name, role=role, stroke_width=3)
        placed: dict[tuple[int, int], float] = {}
        for k, (t, label, trole) in enumerate(ticks):
            side = (-1 if k % 2 == 0 else 1) if len(lanes) == 1 else (-1 if li == 0 else 1)
            text = f"{_fmt(t)}  {label}" if "\n" not in label else f"{_fmt(t)}\n{label}"
            tw = m.width(text, FONT_BODY) + 36
            th = m.height(text, FONT_BODY) + 20
            cx = xt(t)
            for tier in (0, 1, 2):
                left = min(max(cx - tw / 2, LEFT), RIGHT - tw)
                key = (side, tier)
                if placed.get(key, -1e9) + 24 <= left:
                    break
            placed[key] = left + tw
            dist = 70 + tier * 125
            by = ly - dist - th if side < 0 else ly + dist
            b = s.box(left, by, tw, th, text, role=trole, pad=18)
            s.box(cx - 9, ly - 9, 18, 18, shape="ellipse", stroke=INK, fill=INK)
            ey = by + th + 6 if side < 0 else by - 6
            ex = min(max(cx, left + 20), left + tw - 20)
            s.line([(cx, ly + 12 * side), (ex, ey)], color=INK)
            _ = b
    for a, b, label in bars or []:
        ly = ys[0]
        s.box(xt(a), ly + 14, xt(b) - xt(a), 44, label, role="harness", size=FONT_SMALL, pad=6)
    for ly in ys:
        s.text(x1 + 18, ly - 16, end_label, FONT_SMALL, INK)
    if len(lanes) == 1:
        s.text(x0 - 18, ys[0] - 16, "0:00", FONT_SMALL, INK, "right")
    else:
        s.text(x0, ys[1] - 56, "0:00", FONT_SMALL, INK, "center")
    footnote(s, note)


# -- icons (drawn in a size x size square at x, y) ---------------------------------------------


def icon(s: Scene, kind: str, x: float, y: float, size: float = 150, color: str = BLUE) -> None:
    u = size / 10
    fill = tint(color)
    if kind == "map":
        pts = [(0, 1), (3, 0), (7, 1), (10, 0), (10, 9), (7, 10), (3, 9), (0, 10), (0, 1)]
        s.line([(x + px * u, y + py * u) for px, py in pts], color=color, stroke_width=3)
        s.line([(x + 3 * u, y), (x + 3 * u, y + 9 * u)], color=color, dashed=True)
        s.line([(x + 7 * u, y + u), (x + 7 * u, y + 10 * u)], color=color, dashed=True)
    elif kind == "stack":
        for i in range(3):
            s.box(
                x + i * u, y + (2 + i * 2.6) * u, (10 - 2 * i) * u, 2 * u, stroke=color, fill=fill
            )
    elif kind == "lock":
        s.box(x + 2.5 * u, y, 5 * u, 6 * u, shape="ellipse", stroke=color, stroke_width=3)
        s.box(x + u, y + 4 * u, 8 * u, 6 * u, stroke=color, fill=tint(color, "66"))
        s.box(x + 4.4 * u, y + 6 * u, 1.2 * u, 2 * u, stroke=INK, fill=INK)
    elif kind == "check":
        s.box(x, y, 10 * u, 10 * u, stroke=color, fill=fill)
        s.line(
            [(x + 2 * u, y + 5.2 * u), (x + 4.2 * u, y + 7.6 * u), (x + 8.2 * u, y + 2.4 * u)],
            color=INK,
            stroke_width=4,
        )
    elif kind == "terminal":
        s.box(x, y + u, 10 * u, 8 * u, stroke=color, fill=fill)
        s.line(
            [(x + 2 * u, y + 3.5 * u), (x + 4 * u, y + 5 * u), (x + 2 * u, y + 6.5 * u)],
            color=INK,
            stroke_width=3,
        )
        s.line([(x + 5 * u, y + 7 * u), (x + 8 * u, y + 7 * u)], color=INK, stroke_width=3)
    elif kind in ("list", "checklist"):
        s.box(x + u, y, 8 * u, 10 * u, stroke=color, fill=fill)
        for i in range(3):
            yy = y + (2.2 + i * 2.6) * u
            if kind == "checklist":
                s.box(x + 2.2 * u, yy - 0.7 * u, 1.4 * u, 1.4 * u, stroke=INK)
            else:
                s.box(x + 2.4 * u, yy - 0.5 * u, u, u, shape="ellipse", stroke=INK, fill=INK)
            s.line([(x + 4.4 * u, yy), (x + 7.8 * u, yy)], color=INK, stroke_width=3)
        if kind == "checklist":
            s.line(
                [(x + 2.3 * u, y + 2.2 * u), (x + 2.9 * u, y + 2.9 * u), (x + 4 * u, y + 1.2 * u)],
                color=INK,
                stroke_width=3,
            )
    elif kind == "document":
        s.box(x + 1.5 * u, y, 7 * u, 10 * u, stroke=color, fill=fill)
        for i in range(4):
            yy = y + (2 + i * 2) * u
            s.line([(x + 3 * u, yy), (x + 7 * u, yy)], color=INK, stroke_width=2)
    elif kind == "twoband":
        s.box(x + 1.5 * u, y, 7 * u, 10 * u, stroke=color)
        s.box(x + 2.2 * u, y + 0.8 * u, 5.6 * u, 4 * u, stroke=color, fill=tint(color, "66"))
        s.box(x + 2.2 * u, y + 5.4 * u, 5.6 * u, 3.8 * u, stroke=INK, fill=tint(INK, "12"))
    elif kind == "fence":
        s.box(x, y + u, 10 * u, 8 * u, stroke=color, dashed=True, stroke_width=3)
        s.box(x + 2 * u, y + 3 * u, 3.5 * u, 4 * u, stroke=INK, fill=tint(color, "66"))
        s.box(x + 7.4 * u, y + 7.6 * u, 3.6 * u, 2.4 * u, stroke=RED, fill=tint(RED))
    elif kind == "globe":
        s.box(x + u, y + u, 8 * u, 8 * u, shape="ellipse", stroke=color, fill=fill)
        s.line([(x + u, y + 5 * u), (x + 9 * u, y + 5 * u)], color=color)
        s.box(x + 3.2 * u, y + u, 3.6 * u, 8 * u, shape="ellipse", stroke=color)
        s.line([(x, y), (x + 10 * u, y + 10 * u)], color=RED, stroke_width=4)
    elif kind == "gate":
        s.box(x, y + u, 1.6 * u, 9 * u, stroke=color, fill=tint(color, "66"))
        s.box(x + 8.4 * u, y + u, 1.6 * u, 9 * u, stroke=color, fill=tint(color, "66"))
        for i in range(3):
            xx = x + (2.8 + i * 2.2) * u
            s.line([(xx, y + 3 * u), (xx, y + 10 * u)], color=INK, stroke_width=3)
        s.line([(x + 1.6 * u, y + 3 * u), (x + 8.4 * u, y + 3 * u)], color=INK, stroke_width=3)
    elif kind == "funnel":
        pts = [(0, 0), (10, 0), (6, 5), (6, 10), (4, 9), (4, 5), (0, 0)]
        s.line(
            [(x + px * u, y + py * u) for px, py in pts],
            color=color,
            stroke_width=3,
        )
    elif kind == "vault":
        s.box(x, y + u, 10 * u, 9 * u, stroke=color, fill=fill)
        s.box(x + 3 * u, y + 3.5 * u, 4 * u, 4 * u, shape="ellipse", stroke=INK, stroke_width=3)
        s.line([(x + 5 * u, y + 3.5 * u), (x + 5 * u, y + 7.5 * u)], color=INK)
    elif kind == "bug":
        s.box(x + 3 * u, y + 2.5 * u, 4 * u, 6.5 * u, shape="ellipse", stroke=color, fill=fill)
        s.box(x + 3.8 * u, y + 0.6 * u, 2.4 * u, 2.2 * u, shape="ellipse", stroke=color)
        for i in range(3):
            yy = y + (4 + i * 1.8) * u
            s.line([(x + 3 * u, yy), (x + 0.8 * u, yy - 0.8 * u)], color=INK)
            s.line([(x + 7 * u, yy), (x + 9.2 * u, yy - 0.8 * u)], color=INK)
    else:
        raise ValueError(kind)


def cheat_sheet(
    s: Scene,
    heading: str,
    items: list[tuple[str, str, str, str]],
    tags: list[str] | None = None,
    note: str | None = None,
) -> None:
    """Four boxes left to right: (label, sub-label, icon, colour role)."""
    title(s, heading)
    gap = 60
    w = (RIGHT - LEFT - 3 * gap) / 4
    for i, (label, sub, kind, role) in enumerate(items):
        x = LEFT + i * (w + gap)
        color = {"harness": BLUE, "bare": GREY, "accent": AMBER, "fail": RED}.get(role, INK)
        s.box(x, 160, w, 660 if tags else 600, role="plain", stroke=color, stroke_width=3)
        s.text(x + 28, 180, str(i + 1), FONT_TITLE, INK)
        icon(s, kind, x + w / 2 - 80, 240, 160, color)
        s.text(x + w / 2, 460, label, FONT_TITLE, INK, "center")
        s.text(x + w / 2, 560, sub, FONT_BODY, INK, "center")
        if tags:
            s.box(x + 30, 715, w - 60, 70, tags[i], role="neutral", size=FONT_SMALL, pad=8)
    if note:
        s.text(CENTRE, 860 if tags else 810, note, FONT_BODY, INK, "center")
