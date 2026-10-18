"""The one place for diagram style. Every course diagram takes its look from here.

Change a value here, run build.py and render.py, and every diagram follows.

Placement rule: each diagram is drawn on a fixed canvas (a light rounded panel) and is meant to
sit on a 1920x1080 slide at a fixed size (PLACED_WIDTH). On the slide the canvas shrinks by
PLACED_WIDTH / canvas width (0.8 for both canvas types), so a label drawn at MIN_FONT (25) shows
at 20 px at 1080p. build.py refuses a diagram with a smaller label.
"""

from __future__ import annotations

# -- palette (the slide template's colours) ------------------------------------------------------

GREY = "#78909C"  # the bare arm
BLUE = "#3896D2"  # the harness arm, harness pieces
AMBER = "#FFAB40"  # attention
RED = "#E46962"  # a "no", a failure
INK = "#212121"  # every label, neutral strokes
PANEL = "#F0F3F6"  # the light rounded panel under each diagram
SLIDE = "#324158"  # the template's navy slide background (QA composites only)
WHITE = "#ffffff"

# Soft fills: the same colour, mostly transparent (8-digit hex).
FILL_ALPHA = "33"


def tint(color: str, alpha: str = FILL_ALPHA) -> str:
    """A soft fill of a palette colour."""
    return color + alpha


ROLES: dict[str, tuple[str, str | None]] = {
    # role: (stroke, fill)
    "plain": (INK, WHITE),
    "neutral": (INK, tint(INK, "12")),
    "bare": (GREY, tint(GREY)),
    "harness": (BLUE, tint(BLUE)),
    "accent": (AMBER, tint(AMBER, "40")),
    "fail": (RED, tint(RED)),
    "ghost": (INK, None),
}

# -- strokes, shapes, arrows ----------------------------------------------------------------------

ROUGHNESS = 1  # hand-drawn, the same everywhere
STROKE_WIDTH = 2
STROKE_WIDTH_BOLD = 3  # the one element a frame points at
ARROWHEAD = "arrow"
ROUNDNESS_RECT = {"type": 3}  # rounded corners
ROUNDNESS_CURVED = {"type": 2}  # ellipses, diamonds
PANEL_RADIUS = {"type": 3, "value": 48}

# -- text --------------------------------------------------------------------------------

FONT_FAMILY = 5  # Excalifont in @excalidraw/excalidraw 0.18
LINE_HEIGHT = 1.25
TEXT_COLOR = INK
FONT_TITLE = 36
FONT_BODY = 28
FONT_SMALL = 26  # footnotes such as "captured 2026-10-17" (20.8 px on the slide)
MIN_SLIDE_PX = 20  # at 1080p, on the slide, at the placed size
MAX_WORDS = 5  # every label: no sentences inside a diagram
MAX_WORDS_TITLE = 8  # the one title line
MAX_WORDS_FOOTNOTE = 8  # one small footnote line, such as the capture date
# No bare course codes (feature, house rule, section, assignment, source ids) in any label: write
# "<Kind> N: <name>" or the short form "Feature 4", "House rule 1" (the naming standard).
COURSE_CODE = r"\b(?:[FRSA][1-8]|B1[0-4]|B[1-9])\b"
# "<Kind> N: <name>" in a label must carry the exact name (exlib checks it against
# shipharness.datasets.names).
NAMED_KINDS = ("Feature", "House rule", "Section", "Assignment", "Filter")

# -- canvases -----------------------------------------------------------------------------
# name: (width, height, placed width on a 1920x1080 slide). Both place at 864 px high.

CANVAS: dict[str, tuple[int, int, int]] = {
    "wide": (1920, 1080, 1536),  # 16:9, 80% of the slide width
    "std": (1440, 1080, 1152),  # 4:3, 60% of the slide width
}
MARGIN = 64  # empty panel around the content, the same on the tighter axis
MAX_FIT = 1.5  # a small drawing grows to fill the panel, up to this factor
SLIDE_W, SLIDE_H = 1920, 1080
PNG_SCALE = 2


def placed_scale(canvas: str) -> float:
    w, _, placed = CANVAS[canvas]
    return placed / w


MIN_FONT = MIN_SLIDE_PX / min(placed_scale(c) for c in CANVAS)  # 25.0
