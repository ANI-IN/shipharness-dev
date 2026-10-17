"""A small builder for Excalidraw scenes: one style for every course diagram.

It writes real Excalidraw element JSON (rectangle, ellipse, diamond, arrow, line, text), with
bound labels (`containerId`) and arrow bindings. Every style value (font, strokes, roughness,
arrowheads, corners, palette, panel, text sizes, canvases) comes from style.py. Text is measured
with the Excalifont glyph widths, so labels sit centred in their shapes and overflow is caught.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

from style import (
    AMBER,
    ARROWHEAD,
    BLUE,
    CANVAS,
    FONT_BODY,
    FONT_FAMILY,
    GREY,
    INK,
    LINE_HEIGHT,
    MARGIN,
    MIN_FONT,
    PANEL,
    PANEL_RADIUS,
    RED,
    ROLES,
    ROUGHNESS,
    ROUNDNESS_CURVED,
    ROUNDNESS_RECT,
    STROKE_WIDTH,
    TEXT_COLOR,
    WHITE,
    tint,
)

__all__ = ["AMBER", "BLUE", "GREY", "INK", "RED", "WHITE", "Scene", "metrics", "tint"]

EXCALIDRAW_VERSION = "0.18.0"
FONT_URL = (
    f"https://unpkg.com/@excalidraw/excalidraw@{EXCALIDRAW_VERSION}"
    "/dist/prod/fonts/Excalifont/Excalifont-Regular-{h}.woff2"
)
FONT_HASHES = (
    "349fac6ca4700ffec595a7150a0d1e1d",
    "3f2c5db56cc93c5a6873b1361d730c16",
    "41b173a47b57366892116a575a43e2b6",
    "623ccf21b21ef6b3a0d87738f77eb071",
    "a88b72a24fb54c9f94e3b5fdaa7481c9",
    "b9dcf9d2e50a1eaf42fc664b50a3fd0d",
    "be310b9bcd4f1a43f571c46df7809174",
)
CACHE = Path.home() / ".cache" / "shipharness-diagrams"


# -- text measurement ---------------------------------------------------------------------------


class Metrics:
    """Advance widths of Excalifont (every subset file merged), in em units."""

    def __init__(self) -> None:
        from fontTools.ttLib import TTFont

        CACHE.mkdir(parents=True, exist_ok=True)
        self.advance: dict[str, float] = {}
        for h in FONT_HASHES:
            path = CACHE / f"Excalifont-{h}.woff2"
            if not path.exists():
                urllib.request.urlretrieve(FONT_URL.format(h=h), path)
            font = TTFont(str(path))
            upem = font["head"].unitsPerEm
            hmtx = font["hmtx"]
            for code, glyph in font.getBestCmap().items():
                self.advance.setdefault(chr(code), hmtx[glyph][0] / upem)
        self.missing: set[str] = set()

    def width(self, text: str, size: float) -> float:
        best = 0.0
        for line in text.split("\n"):
            total = 0.0
            for ch in line:
                if ch not in self.advance:
                    self.missing.add(ch)
                total += self.advance.get(ch, 0.6)
            best = max(best, total * size)
        return round(best, 2)

    @staticmethod
    def height(text: str, size: float) -> float:
        return round(len(text.split("\n")) * size * LINE_HEIGHT, 2)


_METRICS: Metrics | None = None


def metrics() -> Metrics:
    global _METRICS
    if _METRICS is None:
        _METRICS = Metrics()
    return _METRICS


# -- scene --------------------------------------------------------------------------------------

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def fractional_index(i: int) -> str:
    """Valid fractional-indexing keys in order: a0..az, then b00..bzz."""
    if i < 62:
        return "a" + _DIGITS[i]
    i -= 62
    return "b" + _DIGITS[i // 62] + _DIGITS[i % 62]


def _seed(text: str) -> int:
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16) % 2_000_000_000 + 1


class Scene:
    """One diagram. Draw in canvas units (the canvas is CANVAS[canvas] wide and high); call
    finalize() to centre the drawing on its panel (shrinking it only if it does not fit)."""

    def __init__(self, name: str, canvas: str = "wide") -> None:
        self.name = name
        self.canvas = canvas
        self.els: list[dict[str, Any]] = []
        self.stage_of: dict[str, int] = {}
        self.stage = 1
        self._n = 0
        self.problems: list[str] = []
        self.fit_scale = 1.0

    @property
    def W(self) -> int:  # noqa: N802
        return CANVAS[self.canvas][0]

    @property
    def H(self) -> int:  # noqa: N802
        return CANVAS[self.canvas][1]

    # -- low level ------------------------------------------------------------------------------

    def _id(self, kind: str) -> str:
        self._n += 1
        return f"{self.name}-{kind}-{self._n}"

    def _base(self, kind: str, x: float, y: float, w: float, h: float, **kw: Any) -> dict:
        eid = kw.pop("id", None) or self._id(kind)
        el = {
            "id": eid,
            "type": kind,
            "x": round(x, 2),
            "y": round(y, 2),
            "width": round(w, 2),
            "height": round(h, 2),
            "angle": 0,
            "strokeColor": kw.pop("stroke", INK),
            "backgroundColor": kw.pop("fill", None) or "transparent",
            "fillStyle": "solid",
            "strokeWidth": kw.pop("stroke_width", STROKE_WIDTH),
            "strokeStyle": "dashed" if kw.pop("dashed", False) else "solid",
            "roughness": kw.pop("roughness", ROUGHNESS),
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": None,
            "roundness": kw.pop("roundness", None),
            "seed": _seed(eid),
            "version": 1,
            "versionNonce": _seed(eid + "/n"),
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
        }
        el.update(kw)
        self.els.append(el)
        self.stage_of[eid] = self.stage
        return el

    def _text_el(
        self,
        x: float,
        y: float,
        text: str,
        size: float,
        align: str,
        container: str | None = None,
        valign: str = "top",
    ) -> dict:
        m = metrics()
        w, h = m.width(text, size), m.height(text, size)
        return self._base(
            "text",
            x,
            y,
            w,
            h,
            stroke=TEXT_COLOR,
            text=text,
            fontSize=size,
            fontFamily=FONT_FAMILY,
            textAlign=align,
            verticalAlign=valign,
            containerId=container,
            originalText=text,
            autoResize=True,
            lineHeight=LINE_HEIGHT,
        )

    # -- public ---------------------------------------------------------------------------------

    def text(
        self,
        x: float,
        y: float,
        text: str,
        size: float = FONT_BODY,
        color: str = INK,
        align: str = "left",
    ) -> dict:
        """Free text, always in the text colour (colour is carried by shapes, never by text).
        For align='center', x is the centre; for 'right', x is the right edge."""
        _ = color
        m = metrics()
        w = m.width(text, size)
        left = x - w / 2 if align == "center" else x - w if align == "right" else x
        return self._text_el(left, y, text, size, align)

    def box(
        self,
        x: float,
        y: float,
        w: float | None = None,
        h: float | None = None,
        label: str | None = None,
        *,
        role: str | None = None,
        shape: str = "rectangle",
        stroke: str | None = None,
        fill: str | None = None,
        size: float = FONT_BODY,
        text_color: str | None = None,
        dashed: bool = False,
        stroke_width: float = STROKE_WIDTH,
        align: str = "center",
        valign: str = "middle",
        pad: float = 20,
    ) -> dict:
        _ = text_color
        if role is not None:
            rs, rf = ROLES[role]
            stroke = stroke or rs
            fill = fill or rf
        stroke = stroke or INK
        m = metrics()
        tw = m.width(label, size) if label else 0
        th = m.height(label, size) if label else 0
        if w is None:
            w = tw + 2 * pad
        if h is None:
            h = th + 2 * pad * 0.75
        if label:
            # The text area Excalidraw gives a bound label: the inner box of the shape.
            iw, ih = (
                (w / 2, h / 2)
                if shape == "diamond"
                else (w * 0.7071, h * 0.7071)
                if shape == "ellipse"
                else (w, h)
            )
            if tw + 2 * 10 > iw + 0.5 or th + 2 * 6 > ih + 0.5:
                self.problems.append(
                    f"label {label!r} needs {tw + 20:.0f}x{th + 12:.0f}, "
                    f"the {shape} gives {iw:.0f}x{ih:.0f}"
                )
        roundness = ROUNDNESS_RECT if shape == "rectangle" else ROUNDNESS_CURVED
        el = self._base(
            shape,
            x,
            y,
            w,
            h,
            stroke=stroke,
            fill=fill,
            dashed=dashed,
            stroke_width=stroke_width,
            roundness=roundness,
        )
        if label:
            tx = x + pad if align == "left" else x + (w - tw) / 2
            ty = y + pad * 0.75 if valign == "top" else y + (h - th) / 2
            t = self._text_el(tx, ty, label, size, align, container=el["id"], valign=valign)
            el["boundElements"].append({"type": "text", "id": t["id"]})
        return el

    @staticmethod
    def anchor(el: dict, side: str, off: float = 0.0, gap: float = 8.0) -> tuple[float, float]:
        x, y, w, h = el["x"], el["y"], el["width"], el["height"]
        if side == "left":
            return (x - gap, y + h / 2 + off)
        if side == "right":
            return (x + w + gap, y + h / 2 + off)
        if side == "top":
            return (x + w / 2 + off, y - gap)
        return (x + w / 2 + off, y + h + gap)

    def arrow(
        self,
        a: dict,
        b: dict,
        label: str | None = None,
        *,
        start: str | None = None,
        end: str | None = None,
        start_off: float = 0.0,
        end_off: float = 0.0,
        via: list[tuple[float, float]] | None = None,
        color: str = INK,
        dashed: bool = False,
        both: bool = False,
        size: float = FONT_BODY,
        label_color: str | None = None,
        stroke_width: float = STROKE_WIDTH,
        gap: float = 8.0,
    ) -> dict:
        """An arrow bound to shapes a and b, leaving and entering at side midpoints."""
        ca = (a["x"] + a["width"] / 2, a["y"] + a["height"] / 2)
        cb = (b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
        first = via[0] if via else cb
        last = via[-1] if via else ca
        if start is None:
            dx, dy = first[0] - ca[0], first[1] - ca[1]
            start = (
                ("right" if dx > 0 else "left")
                if abs(dx) >= abs(dy)
                else ("bottom" if dy > 0 else "top")
            )
        if end is None:
            dx, dy = cb[0] - last[0], cb[1] - last[1]
            end = (
                ("left" if dx > 0 else "right")
                if abs(dx) >= abs(dy)
                else ("top" if dy > 0 else "bottom")
            )
        p0 = self.anchor(a, start, start_off, gap)
        p1 = self.anchor(b, end, end_off, gap)
        pts = [p0, *(via or []), p1]
        el = self.path(
            pts,
            label=label,
            color=color,
            dashed=dashed,
            both=both,
            size=size,
            label_color=label_color,
            stroke_width=stroke_width,
        )
        el["startBinding"] = {"elementId": a["id"], "focus": 0, "gap": gap}
        el["endBinding"] = {"elementId": b["id"], "focus": 0, "gap": gap}
        a["boundElements"].append({"type": "arrow", "id": el["id"]})
        b["boundElements"].append({"type": "arrow", "id": el["id"]})
        return el

    def path(
        self,
        pts: list[tuple[float, float]],
        label: str | None = None,
        *,
        color: str = INK,
        dashed: bool = False,
        both: bool = False,
        head: bool = True,
        size: float = FONT_BODY,
        label_color: str | None = None,
        stroke_width: float = STROKE_WIDTH,
        kind: str = "arrow",
    ) -> dict:
        """A free arrow (or line, kind='line') through absolute points."""
        _ = label_color
        x0, y0 = pts[0]
        rel = [[round(px - x0, 2), round(py - y0, 2)] for px, py in pts]
        xs = [p[0] for p in rel]
        ys = [p[1] for p in rel]
        extra: dict[str, Any] = {
            "points": rel,
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
        }
        if kind == "arrow":
            extra.update(
                startArrowhead=ARROWHEAD if both else None,
                endArrowhead=ARROWHEAD if head else None,
                elbowed=False,
            )
        else:
            extra.update(startArrowhead=None, endArrowhead=None, polygon=False)
        el = self._base(
            kind,
            x0,
            y0,
            max(xs) - min(xs),
            max(ys) - min(ys),
            stroke=color,
            dashed=dashed,
            stroke_width=stroke_width,
            roundness=None,
            **extra,
        )
        if label:
            # Excalidraw puts an arrow label on the middle point (odd count) or between the two
            # middle points (even count).
            n = len(pts)
            if n % 2:
                mx, my = pts[n // 2]
            else:
                (ax, ay), (bx, by) = pts[n // 2 - 1], pts[n // 2]
                mx, my = (ax + bx) / 2, (ay + by) / 2
            m = metrics()
            tw, th = m.width(label, size), m.height(label, size)
            if n == 2:
                seg = ((pts[1][0] - pts[0][0]) ** 2 + (pts[1][1] - pts[0][1]) ** 2) ** 0.5
                horizontal = abs(pts[1][0] - pts[0][0]) >= abs(pts[1][1] - pts[0][1])
                need = (tw if horizontal else th) + 30
                if seg < need:
                    self.problems.append(
                        f"arrow label {label!r} needs {need:.0f} px, the arrow is {seg:.0f} px"
                    )
            t = self._text_el(
                mx - tw / 2,
                my - th / 2,
                label,
                size,
                "center",
                container=el["id"],
                valign="middle",
            )
            el["boundElements"].append({"type": "text", "id": t["id"]})
        return el

    def line(self, pts: list[tuple[float, float]], **kw: Any) -> dict:
        return self.path(pts, kind="line", **kw)

    # -- output ---------------------------------------------------------------------------------

    def bounds(self) -> tuple[float, float, float, float]:
        xs: list[float] = []
        ys: list[float] = []
        for e in self.els:
            if "points" in e:
                xs += [e["x"] + p[0] for p in e["points"]]
                ys += [e["y"] + p[1] for p in e["points"]]
            else:
                xs += [e["x"], e["x"] + e["width"]]
                ys += [e["y"], e["y"] + e["height"]]
        return min(xs), min(ys), max(xs), max(ys)

    def finalize(self) -> None:
        """Centre the drawing on the canvas (shrink only if it does not fit inside the margin),
        then put the light rounded panel, the full canvas, under it in every frame. Every frame
        of a build-up therefore exports at the same size, with every element in place."""
        x0, y0, x1, y1 = self.bounds()
        aw, ah = self.W - 2 * MARGIN, self.H - 2 * MARGIN
        s = min(1.0, aw / (x1 - x0), ah / (y1 - y0))
        self.fit_scale = s
        ox = (self.W - (x1 - x0) * s) / 2 - x0 * s
        oy = (self.H - (y1 - y0) * s) / 2 - y0 * s
        for e in self.els:
            e["x"] = round(e["x"] * s + ox, 2)
            e["y"] = round(e["y"] * s + oy, 2)
            e["width"] = round(e["width"] * s, 2)
            e["height"] = round(e["height"] * s, 2)
            if "points" in e:
                e["points"] = [[round(px * s, 2), round(py * s, 2)] for px, py in e["points"]]
            if e["type"] == "text":
                e["fontSize"] = round(e["fontSize"] * s, 2)
        stage, self.stage = self.stage, 1
        self._base(
            "rectangle",
            0,
            0,
            self.W,
            self.H,
            id=f"{self.name}-panel",
            stroke="transparent",
            fill=PANEL,
            stroke_width=1,
            roughness=0,
            roundness=PANEL_RADIUS,
            locked=True,
        )
        self.stage = stage
        self.els.insert(0, self.els.pop())
        small = [e for e in self.els if e["type"] == "text" and e["fontSize"] < MIN_FONT - 0.01]
        for e in small:
            self.problems.append(f"text {e['text']!r} is {e['fontSize']:.1f} (< {MIN_FONT:.0f})")

    @property
    def min_font(self) -> float:
        return min((e["fontSize"] for e in self.els if e["type"] == "text"), default=99.0)

    @property
    def stages(self) -> int:
        return max(self.stage_of.values()) if self.stage_of else 1

    def elements(self, upto: int | None = None) -> list[dict]:
        keep = {e["id"] for e in self.els if upto is None or self.stage_of[e["id"]] <= upto}
        out = []
        for e in self.els:
            if e["id"] not in keep:
                continue
            e = json.loads(json.dumps(e))
            e["boundElements"] = [b for b in e["boundElements"] if b["id"] in keep] or None
            e["index"] = fractional_index(len(out))
            out.append(e)
        return out

    def document(self, upto: int | None = None) -> dict:
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements(upto),
            "appState": {"gridSize": 20, "viewBackgroundColor": WHITE},
            "files": {},
        }
