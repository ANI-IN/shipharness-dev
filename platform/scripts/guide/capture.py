"""HD screenshots of the shipharness console for the demo guide, with numbered callouts.

Playwright Chromium, headless (the console page only, no browser chrome), viewport 1920x1080 at
device pixel ratio 2. For each screen 1-5 of a run: the viewport (`screen-N-final.png`), a
full-page image when the screen is taller (`screen-N-full.png`), and crops of the key panels
(`screen-1-harness.png`, `screen-3-referee.png`, ...). Callout targets are DOM selectors or text
matches, resolved to bounding boxes in the page and scaled by the pixel ratio. Before an image is
saved, the page text (every screen, tooltips, the title) is checked: a host path, an email
address, or key-like text stops the capture.

Subcommands (each writes PNGs and merges entries into <out>/images.json):

    run    --base URL --run-id AB --demo s1 --out DIR --kind recorded|live   screens 1-5 + run list
    list   --base URL --out DIR --name runlist-empty --demo setup --kind ...  the run list only
    cut    --base URL --runs-dir DIR --src RUN_DIR --demo s2 --out DIR ...    moments, from the
           run's log cut at the moment's event (served by a console on --runs-dir)
    terms  --src terminal.txt --demo s1 --out DIR --kind ...                  terminal renders
    watch  --demos s1,s2,... --base URL --runs DIR --status DIR --images DIR  live moments, then
           everything once the live runner writes DONE

Run with the dev repo's environment: `uv run python platform/scripts/guide/capture.py ...`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from callouts import Target, annotate
from guidelib import (
    Box,
    box_in_crop,
    find_secrets,
    image_entry,
    load_entries,
    merge_entries,
    personal_hits,
    save_entries,
    scale_box,
)
from PIL import Image

WIDTH, HEIGHT, DPR = 1920, 1080, 2
SCREENS = {1: "Live Console", 2: "Boards", 3: "Evidence", 4: "A/B Report", 5: "Traces"}
DEMOS = {
    "s1": "Section 1 show-1",
    "s2": "Section 2 show-2",
    "s3": "Section 3 demo-3",
    "s4": "Section 4 show-4",
    "final": "Final A/B",
    "replay": "replay",
    "setup": "setup",
}
MAX_CALLOUTS = 7


class PrivacyError(RuntimeError):
    """Personal or secret text on the page: nothing is saved."""


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# Targets --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Spec:
    """A callout target: a CSS selector and/or a text match, inside the shown screen (root
    "screen"), the header bar ("bar"), or the whole page ("page"); `arm` keeps matches inside
    that arm's blocks; `nth` picks among matches (document order, deepest elements)."""

    label: str
    sel: str | None = None
    text: str | None = None
    arm: str | None = None
    root: str = "screen"
    nth: int = 0


RESOLVE_JS = r"""
(args) => {
  const {specs, screen} = args;
  const vis = e => {
    if (!e || !e.getBoundingClientRect) return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden' &&
      (e.offsetParent !== null || getComputedStyle(e).position === 'fixed');
  };
  const out = [];
  for (const s of specs) {
    let root = s.root === 'bar' ? document.querySelector('.bar') :
      s.root === 'page' ? document.body : document.querySelector('#screen-' + screen);
    if (!root) { out.push(null); continue; }
    let cands = Array.from(root.querySelectorAll(s.sel || '*')).filter(vis);
    if (s.arm) cands = cands.filter(e => {
      const a = e.closest('[data-arm]'); return a && a.getAttribute('data-arm') === s.arm; });
    if (s.text) {
      cands = cands.filter(e => (e.textContent || '').includes(s.text));
      cands = cands.filter(e => !cands.some(o => o !== e && e.contains(o)));
    }
    const e = cands[s.nth || 0];
    if (!e) { out.push(null); continue; }
    const list = e.closest('[data-scroll]');
    let r = e.getBoundingClientRect();
    if (list && list !== e) {
      const lr = list.getBoundingClientRect();
      if (r.top < lr.top || r.bottom > lr.bottom) {
        list.scrollTop += r.top - lr.top - Math.min(lr.height / 3, 80);
      }
      r = e.getBoundingClientRect();
      const l2 = list.getBoundingClientRect();
      const top = Math.max(r.top, l2.top), bottom = Math.min(r.bottom, l2.bottom);
      if (bottom <= top) { out.push(null); continue; }
      r = {left: r.left, top: top, width: r.width, height: bottom - top};
    }
    out.push({x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height});
  }
  return out;
}
"""

PRIVACY_JS = r"""
() => {
  const parts = [document.title, document.body ? document.body.textContent : ''];
  document.querySelectorAll('[title],[alt],[aria-label]').forEach(e => {
    ['title', 'alt', 'aria-label'].forEach(a => {
      if (e.getAttribute(a)) parts.push(e.getAttribute(a));
    });
  });
  return parts.join('\n');
}
"""

FACTS_JS = r"""
(screen) => {
  const root = document.querySelector('#screen-' + screen) || document.body;
  const txt = e => e ? e.textContent.replace(/\s+/g, ' ').trim() : '';
  const arms = {};
  for (const arm of ['bare', 'harness']) {
    const panel = root.querySelector('[data-arm="' + arm + '"]');
    if (!panel) continue;
    const notRun = panel.querySelector('.not-run');
    const pill = panel.querySelector('.referee .ref-line');
    const end = Array.from(panel.querySelectorAll('.sandbox-line')).map(txt).join(' ');
    arms[arm] = {notRun: txt(notRun), pill: txt(pill), end: end};
  }
  return {
    feature: txt(root.querySelector('.badge.feature')),
    recording: !!root.querySelector('.badge.recording'),
    single: !!root.querySelector('.badge.single-arm'),
    refusals: txt(root.querySelector('.gate-refusals')),
    arms: arms,
    height: document.documentElement.scrollHeight,
    conn: txt(document.querySelector('#conn')),
  };
}
"""


def arm_specs(single: bool) -> list[Spec]:
    if single:
        return [Spec("Bare arm: Not run (harness in action)", sel=".not-run", arm="bare")]
    return [Spec("Bare arm line: no layers", sel=".arm-head h2, h2", arm="bare")]


def screen_specs(screen: int, single: bool) -> list[Spec]:
    """What matters on each screen, in callout order (missing targets are skipped)."""
    nav = [
        Spec("← All runs: back to the run list", sel=".all-runs", root="bar"),
        Spec("Screen tabs 1 to 5", sel="nav.tabs", root="bar"),
    ]
    if screen == 1:
        specs = (
            nav
            + arm_specs(single)
            + [
                Spec("Harness arm line: its layers", sel=".arm-head h2", arm="harness"),
                Spec("Gate list", sel=".pills", arm="harness"),
                Spec("Gate refused 'done', then passed", sel=".gate-refusals", arm="harness"),
                Spec("Referee pill (harness)", sel=".referee .ref-line", arm="harness"),
            ]
        )
        if not single:
            specs.append(Spec("Referee pill (bare)", sel=".referee .ref-line", arm="bare"))
        return specs
    if screen == 2:
        return nav[:1] + [
            Spec("Harness board, signed in as one user", sel="h2", arm="harness"),
            Spec("Board marks", sel=".marks", arm="harness"),
            Spec("Bare board marks", sel=".marks", arm="bare"),
            Spec("Bare arm: Not run (harness in action)", sel=".not-run", arm="bare"),
            Spec("Two-tab edit conflict", sel=".conflict-panel h2"),
        ]
    if screen == 3:
        return [
            Spec("Sessions, including the test phase", sel=".sessions", arm="harness"),
            Spec("Diff map (harness)", sel=".diffmap", arm="harness"),
            Spec("Diff map (bare)", sel=".diffmap", arm="bare"),
            Spec(
                "Files outside the allowed paths (diff_scope)",
                sel=".check-row",
                text="Files outside the allowed paths",
                arm="harness",
            ),
            Spec(
                "Files outside the allowed paths (bare)",
                sel=".check-row",
                text="Files outside the allowed paths",
                arm="bare",
            ),
            Spec("Filter table: may be a real bug", sel=".maybe-bug"),
            Spec("Blinded reviewer's reason", sel=".reviewer-line", arm="harness"),
            Spec("Bare arm: Not run (harness in action)", sel=".not-run", arm="bare"),
        ]
    if screen == 4:
        return [
            Spec("This run", sel=".this-run"),
            Spec("Measured before class", sel="h2", text="Measured before class"),
            Spec("Dots per run", sel=".dot-row"),
            Spec("Cost per verified feature", sel=".costs"),
            Spec("Reviewer agreement", sel=".agreement"),
        ]
    return [
        Spec("Live tail", sel=".tail-panel h2"),
        Spec("First wrong turn", sel="h2", text="First wrong turn"),
        Spec("LangSmith links", sel="h2", text="LangSmith"),
    ]


@dataclass(frozen=True)
class Crop:
    name: str
    sel: str
    specs: tuple[Spec, ...]
    nth: int = 0
    arm: str | None = None


def crops_for(screen: int, single: bool) -> list[Crop]:
    if screen == 1:
        out = [
            Crop(
                "screen-1-harness",
                ".arm-panel",
                (
                    Spec("Harness arm line: its layers", sel=".arm-head h2", arm="harness"),
                    Spec("Turns list", sel=".list-head", arm="harness"),
                    Spec("Harness decisions", sel=".decisions", arm="harness"),
                    Spec("Gate list", sel=".pills", arm="harness"),
                    Spec("Referee pill", sel=".referee .ref-line", arm="harness"),
                ),
                arm="harness",
            )
        ]
        if not single:
            out.append(
                Crop(
                    "screen-1-bare",
                    ".arm-panel",
                    (
                        Spec("Bare arm line: no layers", sel=".arm-head h2", arm="bare"),
                        Spec("Turns list", sel=".list-head", arm="bare"),
                        Spec("Referee pill", sel=".referee .ref-line", arm="bare"),
                    ),
                    arm="bare",
                )
            )
        return out
    if screen == 3:
        return [
            Crop(
                "screen-3-sessions",
                ".evidence > article",
                (
                    Spec("Files read", sel=".files", arm="harness"),
                    Spec("Sessions", sel=".sessions", arm="harness"),
                ),
                nth=0,
            ),
            Crop(
                "screen-3-diff-map",
                ".evidence > article",
                (
                    Spec("Diff map (bare)", sel=".diffmap", arm="bare"),
                    Spec("Diff map (harness)", sel=".diffmap", arm="harness"),
                    Spec("Sandbox denials", sel=".denials", arm="harness"),
                ),
                nth=1,
            ),
            Crop(
                "screen-3-referee",
                ".evidence > article",
                (
                    Spec(
                        "Files outside the allowed paths (diff_scope)",
                        sel=".check-row",
                        text="Files outside the allowed paths",
                        arm="bare",
                    ),
                    Spec(
                        "Files outside the allowed paths (diff_scope)",
                        sel=".check-row",
                        text="Files outside the allowed paths",
                        arm="harness",
                    ),
                    Spec("hidden tests", sel=".check-row", text="hidden tests", arm="harness"),
                    Spec("Blinded reviewer's reason", sel=".reviewer-line", arm="harness"),
                    Spec("Filter table: may be a real bug", sel=".maybe-bug"),
                ),
                nth=2,
            ),
            Crop(
                "screen-3-filters",
                "table.filters",
                (
                    Spec("A test kept by the filters", sel="tr", text="kept"),
                    Spec("fails on the current code; this may be a real bug", sel=".maybe-bug"),
                ),
            ),
            Crop(
                "screen-3-mutants",
                "table.mutants",
                (Spec("Mutants: filter set and referee set", sel="thead"),),
                arm="harness",
            ),
        ]
    if screen == 4:
        return [
            Crop(
                "screen-4-report",
                ".grid.three > article",
                (
                    Spec("Measured before class", sel="h2", text="Measured before class"),
                    Spec("Dots per run", sel=".dot-row"),
                    Spec("Legend", sel=".legend"),
                ),
                nth=0,
            ),
            Crop("screen-4-this-run", ".this-run", (Spec("This run", sel=".this-run-head"),)),
        ]
    return []


# Browser --------------------------------------------------------------------------------------


@dataclass
class Shot:
    """One full-page screenshot plus the resolved boxes (image pixels)."""

    path: Path
    width: int
    height: int
    facts: dict[str, Any] = field(default_factory=dict)


_BROWSER: list[Any] = []  # [playwright, browser], shared by every Console of the process


class Console:
    def __init__(self, base: str) -> None:
        if not _BROWSER:
            from playwright.sync_api import sync_playwright

            pw = sync_playwright().start()
            _BROWSER.extend([pw, pw.chromium.launch(headless=True)])
        self.base = base.rstrip("/")
        self._ctx = _BROWSER[1].new_context(
            viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=DPR
        )
        self.page = self._ctx.new_page()
        self.tmp = Path(tempfile.mkdtemp(prefix="guide-capture-"))

    def close(self) -> None:
        self._ctx.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    @staticmethod
    def shutdown() -> None:
        if _BROWSER:
            pw, browser = _BROWSER
            browser.close()
            pw.stop()
            _BROWSER.clear()

    def goto(self, path: str) -> None:
        self.page.goto(self.base + path, wait_until="domcontentloaded")
        self.page.wait_for_load_state("load")

    def open_run(self, run_id: str) -> None:
        self.goto(f"/run/{run_id}#1")
        try:  # the first SSE message replaces "connecting"
            self.page.wait_for_function(
                "() => { const c = document.querySelector('#conn');"
                " return c && c.textContent.trim() !== 'connecting'; }",
                timeout=15000,
            )
        except Exception:  # noqa: BLE001 - the server-rendered page is still complete
            log("! the console did not say live or finished within 15 s")
        self.page.wait_for_timeout(1200)

    def show(self, screen: int) -> None:
        self.page.keyboard.press(str(screen))
        self.page.wait_for_timeout(400)

    def expand(self, ids: Iterable[str]) -> None:
        for i in ids:
            button = self.page.locator(f'.expand-toggle[data-expand="{i}"]')
            if button.count() and button.first.is_visible():
                button.first.click()
                self.page.wait_for_timeout(300)

    def check_private(self) -> None:
        text = self.page.evaluate(PRIVACY_JS)
        hits = personal_hits(text)
        if hits or find_secrets(text):
            kinds = sorted({"host path" if "/" in h or "\\" in h else "email" for h in hits})
            raise PrivacyError(
                f"personal or secret text on {self.page.url}: {', '.join(kinds) or 'key-like text'}"
            )

    def boxes(self, specs: Iterable[Spec], screen: int | None) -> list[Box | None]:
        raw = self.page.evaluate(
            RESOLVE_JS, {"specs": [s.__dict__ for s in specs], "screen": screen or 0}
        )
        return [
            None if r is None else scale_box((r["x"], r["y"], r["w"], r["h"]), DPR) for r in raw
        ]

    def full_shot(self, name: str, screen: int | None) -> Shot:
        self.page.evaluate("() => window.scrollTo(0, 0)")
        facts = self.page.evaluate(FACTS_JS, screen or 1)
        self.check_private()
        path = self.tmp / f"{name}.png"
        self.page.screenshot(path=str(path), full_page=True)
        w, h = Image.open(path).size
        return Shot(path, w, h, facts)


# Output ---------------------------------------------------------------------------------------


@dataclass
class Out:
    folder: Path
    demo: str
    kind: str
    run_id: str | None
    entries: list[dict[str, Any]] = field(default_factory=list)

    def add(
        self,
        file: str,
        screen: int | str | None,
        moment: str,
        alt: str,
        callouts: list[dict[str, Any]],
    ) -> None:
        self.entries.append(
            image_entry(
                file=file,
                screen=screen,
                moment=moment,
                alt=alt,
                callouts=callouts,
                source_run_id=self.run_id,
                recorded_or_live=self.kind,
            )
        )

    def save(self) -> None:
        path = self.folder / "images.json"
        save_entries(path, merge_entries(load_entries(path), self.entries))
        log(f"{self.folder.name}/images.json: {len(self.entries)} entries written or replaced")


def _targets(specs: list[Spec], boxes: list[Box | None], crop: Box | None) -> list[Target]:
    out: list[Target] = []
    seen: set[tuple[int, int, int, int]] = set()
    for spec, box in zip(specs, boxes, strict=True):
        if box is None:
            continue
        if crop is not None:
            box = box_in_crop(box, crop)
            if box is None:
                continue
        key = (round(box.x), round(box.y), round(box.w), round(box.h))
        if key in seen:
            continue
        seen.add(key)
        out.append(Target(box, spec.label))
    return out[:MAX_CALLOUTS]


def save_image(
    shot: Shot,
    out: Out,
    name: str,
    crop: Box | None,
    specs: list[Spec],
    boxes: list[Box | None],
    screen: int | str | None,
    moment: str,
    alt: str,
) -> None:
    img = Image.open(shot.path)
    region = crop or Box(0, 0, shot.width, shot.height)
    region = Box(
        max(0, region.x),
        max(0, region.y),
        min(region.w, shot.width - max(0, region.x)),
        min(region.h, shot.height - max(0, region.y)),
    )
    cut = img.crop((int(region.x), int(region.y), int(region.right), int(region.bottom)))
    raw = shot.path.parent / f"{name}-raw.png"
    cut.save(raw)
    file = f"{name}.png"
    callouts = annotate(raw, out.folder / file, _targets(specs, boxes, region))
    out.add(file, screen, moment, alt, callouts)
    log(f"  {out.folder.name}/{file} ({cut.size[0]}x{cut.size[1]}, {len(callouts)} callouts)")


# Alt text -------------------------------------------------------------------------------------


def _arm_words(arm: str, a: dict[str, str]) -> str:
    if a.get("notRun"):
        return f'the {arm} arm reads "{a["notRun"].split(":")[0]}"'
    bits = []
    m = re.search(r"run (\w+) · (\d+) turns", a.get("end", ""))
    if m:
        bits.append(f"run {m.group(1)} after {m.group(2)} turns")
    if a.get("pill"):
        bits.append(f'referee pill "{a["pill"]}"')
    return f"the {arm} arm shows " + (", ".join(bits) if bits else "its turns so far")


def alt_text(demo: str, screen: int, facts: dict[str, Any], what: str, moment: str) -> str:
    feature = facts.get("feature") or ""
    label = DEMOS.get(demo, demo)
    head = f"Screen {screen} ({SCREENS[screen]}) of the {label} run"
    if feature:
        head += f" on {feature}"
    head += f", {moment}"
    arms = facts.get("arms") or {}
    if screen == 1 and arms:
        body = "; ".join(_arm_words(arm, a) for arm, a in arms.items())
        if facts.get("refusals"):
            body += "; the gate refusal is listed under the turns"
    else:
        body = what
    if facts.get("recording"):
        body += "; the red RECORDING badge marks a replay"
    return f"{head}: {body}."


SCREEN_WHAT = {
    2: "the board screenshot of each arm with its marks",
    3: "files read, sessions, the diff map, sandbox denials, one row per referee check, the "
    "blinded reviewer's reason, and the test filter table",
    4: "this run's results next to the dots of the runs measured before class",
    5: "the live tail of events, the first wrong turn of each arm, and the LangSmith links",
}


def capture_screen(
    con: Console,
    out: Out,
    screen: int,
    *,
    name: str,
    moment: str,
    specs: list[Spec] | None = None,
    expand: Iterable[str] = (),
    crops: bool = True,
    full: bool = True,
    view: bool = True,
) -> None:
    con.show(screen)
    con.expand(expand)
    shown = con.page.evaluate("() => document.body.getAttribute('data-seq') || '?'")
    moment = moment.replace("{shown}", str(shown))
    single = bool(
        con.page.evaluate(
            "(s) => !!document.querySelector('#screen-' + s + ' .badge.single-arm')", screen
        )
    )
    specs = specs if specs is not None else screen_specs(screen, single)
    if single:  # one arm: the bare arm is only its "Not run" line
        specs = [
            s for s in specs if not s.label.startswith(("Bare arm line", "Referee pill (bare"))
        ]
    boxes = con.boxes(specs, screen)
    shot = con.full_shot(name, screen)
    alt = alt_text(out.demo, screen, shot.facts, SCREEN_WHAT.get(screen, ""), moment)
    viewport = Box(0, 0, WIDTH * DPR, HEIGHT * DPR)
    if view:
        save_image(shot, out, name, viewport, specs, boxes, screen, moment, alt)
    if full and shot.height > HEIGHT * DPR + 40:
        save_image(
            shot,
            out,
            name.replace("-final", "") + "-full",
            None,
            specs,
            boxes,
            screen,
            moment,
            alt.replace(f"Screen {screen} ", f"Screen {screen}, whole page, ", 1),
        )
    if not crops:
        return
    for c in crops_for(screen, single):
        idx = con.page.evaluate(
            "(a) => { const all = Array.from(document.querySelectorAll('#screen-' + a.screen +"
            " ' ' + a.sel)).filter(e => e.getBoundingClientRect().height > 0 && (!a.arm ||"
            " e.getAttribute('data-arm') === a.arm || (e.closest('[data-arm]') &&"
            " e.closest('[data-arm]').getAttribute('data-arm') === a.arm)));"
            " const e = all[a.nth]; if (!e) return null; const r = e.getBoundingClientRect();"
            " return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; }",
            {"screen": screen, "sel": c.sel, "nth": c.nth, "arm": c.arm},
        )
        if not idx:
            continue
        pad = 12
        box = scale_box(
            (idx["x"] - pad, idx["y"] - pad, idx["w"] + 2 * pad, idx["h"] + 2 * pad), DPR
        )
        cspecs = list(c.specs)
        cboxes = con.boxes(cspecs, screen)
        part = c.name.split("-", 2)[-1].replace("-", " ")
        calt = (
            f"Close-up of screen {screen} ({SCREENS[screen]}), the {part} panel of the "
            f"{DEMOS.get(out.demo, out.demo)} run, {moment}."
        )
        save_image(shot, out, prefixed(name, c.name), box, cspecs, cboxes, screen, moment, calt)


def prefixed(name: str, crop_name: str) -> str:
    """Crops of a moment image carry the moment: screen-1-block -> screen-1-block-harness."""
    base = re.sub(r"-final$", "", name)
    screen_prefix = re.match(r"screen-\d", crop_name)
    if base == (screen_prefix.group(0) if screen_prefix else base):
        return crop_name
    return base + crop_name[len(screen_prefix.group(0)) :] if screen_prefix else crop_name


RUNLIST_SPECS_TOP = [
    Spec("Run id: open the run", sel=".run-link", root="page"),
    Spec("Type: harness in action or A/B", sel=".run-meta span:nth-child(3)", root="page"),
    Spec("Status", sel=".run-meta span:nth-child(4)", root="page"),
    Spec("Start time", sel=".run-meta span:nth-child(5)", root="page"),
]


def capture_list(con: Console, out: Out, name: str, moment: str, run_id: str | None) -> None:
    con.goto("/")
    con.page.wait_for_timeout(500)
    nth = 0
    if run_id:
        ids = con.page.evaluate(
            "() => Array.from(document.querySelectorAll('.run-link')).map(a => a.textContent"
            ".replace(/\\s+/g, ''))"
        )
        nth = next((i for i, t in enumerate(ids) if run_id in t), 0)
    has_runs = con.page.locator(".run-link").count() > 0
    if has_runs:
        specs = [
            Spec(s.label, sel=f".runs > li:nth-child({nth + 1}) {s.sel}", root="page")
            for s in RUNLIST_SPECS_TOP
        ]
        if nth:  # bring the card into view
            con.page.locator(".runs > li").nth(nth).scroll_into_view_if_needed()
    else:
        specs = [
            Spec("No runs yet: start one in Terminal 2", sel=".panel p", root="page"),
            Spec("Console keys", sel=".panel:last-child p", root="page"),
        ]
    boxes = con.boxes(specs, None)
    scroll = con.page.evaluate("() => window.scrollY")
    con.check_private()
    path = con.tmp / f"{name}.png"
    con.page.screenshot(path=str(path))
    w, h = Image.open(path).size
    shot = Shot(path, w, h)
    boxes = [None if b is None else Box(b.x, b.y - scroll * DPR, b.w, b.h) for b in boxes]
    count = con.page.locator(".run-link").count()
    if has_runs:
        alt = (
            f"The console's run list at http://127.0.0.1 with {count} run cards, newest first; "
            f"each card shows the run id, section, feature, type, status, and start time"
        )
        if run_id:
            alt += f", with the card of {run_id} marked"
    else:
        alt = (
            'The console\'s empty run list: "No runs yet" with the command to start one, and '
            "the console keys 1 to 5, F, and H or Esc"
        )
    save_image(shot, out, name, None, specs, boxes, "list", moment, alt + ".")


def capture_run(
    con: Console,
    out: Out,
    run_id: str,
    moment: str,
    *,
    runlist: bool = True,
    screens: Iterable[int] = (1, 2, 3, 4, 5),
) -> None:
    if runlist:
        capture_list(con, out, "runlist", moment, run_id)
    con.open_run(run_id)
    for screen in screens:
        capture_screen(con, out, screen, name=f"screen-{screen}-final", moment=moment)
    # Section 3 and the A/B runs: screen 1 with the harness decisions open (the block row).
    con.show(1)
    if con.page.locator('.expand-toggle[data-expand="decisions-harness"]').count():
        capture_screen(
            con,
            out,
            1,
            name="screen-1-decisions-expanded",
            moment=moment + ", with Harness decisions expanded",
            expand=["decisions-harness"],
            crops=False,
            full=True,
        )


# Moments (from a run's log cut at an event) -------------------------------------------------


def read_events(path: Path) -> list[dict[str, Any]]:
    out = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _ts(e: dict[str, Any]) -> float:
    return datetime.fromisoformat(e["ts"].replace("Z", "+00:00")).timestamp()


def _kind(e: dict[str, Any]) -> str | None:
    return e["data"].get("kind") if e.get("type") == "harness_decision" else None


@dataclass(frozen=True)
class Moment:
    name: str  # file name stem
    screen: int
    words: str  # "when the scope layer blocked an edit"
    # (the moment's own event, the event to cut the log after), or None
    find: Callable[[list[dict[str, Any]]], tuple[int, int] | None]
    specs: tuple[Spec, ...]
    expand: tuple[str, ...] = ()


def _first(events, pred, extra: int = 0):
    for i, e in enumerate(events):
        if pred(e):
            j = min(len(events) - 1, i + extra)
            return e["seq"], events[j]["seq"]
    return None


def _early(events):
    if not events:
        return None
    t0 = _ts(events[0])
    last = None
    for e in events:
        if _ts(e) - t0 > 60:
            break
        last = e["seq"]
    return None if last is None else (last, last)


def _both_arms(events):
    turns = {"bare": 0, "harness": 0}
    for e in events:
        if e.get("type") == "turn" and e.get("arm") in turns:
            turns[e["arm"]] += 1
            if min(turns.values()) >= 4:
                return e["seq"], e["seq"]
    return None


def _resumed(events):
    for i, e in enumerate(events):
        if e.get("type") == "session_resume":
            turns = [x for x in events[i + 1 :] if x.get("type") == "turn"][:2]
            return e["seq"], (turns[-1]["seq"] if turns else e["seq"])
    return None


def _gate_done(e, passed: bool) -> bool:
    if e.get("type") != "gate_result":
        return False
    items = e["data"].get("items", [])
    if any(i.get("status") == "pending" for i in items):
        return False
    ok = e["data"].get("passed")
    if ok is None:
        ok = all(i.get("status") == "pass" for i in items)
    return bool(ok) == passed


def _primary(arm: str | None):
    return lambda events: _first(
        events,
        lambda e: e.get("type") == "primary_verdict" and (arm is None or e["arm"] == arm),
        extra=1,
    )


H = "harness"
EARLY_SPECS = (
    Spec("HARNESS IN ACTION badge, or the feature", sel=".badge.single-arm, .badge.feature"),
    Spec("Bare arm: Not run (harness in action)", sel=".not-run", arm="bare"),
    Spec("Bare arm line: no layers", sel=".arm-head h2", arm="bare"),
    Spec("Harness arm line: its layers", sel=".arm-head h2", arm=H),
    Spec("Container line", sel=".sandbox-line", arm=H),
    Spec("Last turns", sel=".list-head", arm=H),
    Spec("Harness decisions: the layer notes", sel=".decisions li", arm=H),
)
MOMENTS = [
    Moment("screen-1-early", 1, "about one minute after launch", _early, EARLY_SPECS),
    Moment(
        "screen-1-both-arms",
        1,
        "with both arms working side by side",
        _both_arms,
        (
            Spec("Bare arm line: no layers", sel=".arm-head h2", arm="bare"),
            Spec("Harness arm line: its layers", sel=".arm-head h2", arm=H),
            Spec("Bare turns", sel=".turns", arm="bare"),
            Spec("Harness turns", sel=".turns", arm=H),
            Spec("Harness decisions", sel=".decisions", arm=H),
        ),
    ),
    Moment(
        "screen-1-session-stop",
        1,
        "when session 1 stopped and its handoff was written",
        lambda ev: _first(ev, lambda e: _kind(e) == "session_stop"),
        (
            Spec("Session 1 stopped", sel=".marker", text="stopped", arm=H),
            Spec(
                "Handoff written to session-handoff.md",
                sel=".decisions li",
                text="handoff written",
                arm=H,
            ),
            Spec("Turns list", sel=".list-head", arm=H),
        ),
        ("decisions-harness",),
    ),
    Moment(
        "screen-1-session-resumed",
        1,
        "when session 2 resumed from the handoff",
        _resumed,
        (
            Spec("Session 1 stopped", sel=".marker", text="stopped", arm=H),
            Spec("Session 2 resumed", sel=".marker", text="resumed", arm=H),
            Spec(
                "Handoff written to session-handoff.md",
                sel=".decisions li",
                text="handoff written",
                arm=H,
            ),
        ),
        ("decisions-harness",),
    ),
    Moment(
        "screen-1-block",
        1,
        "when the scope layer blocked an edit outside the allowed paths",
        lambda ev: _first(ev, lambda e: _kind(e) == "block", extra=1),
        (
            Spec(
                "Blocked edit: outside the allowed paths",
                sel=".decisions li",
                text="outside the allowed paths",
                arm=H,
            ),
            Spec("Turns list", sel=".list-head", arm=H),
            Spec("Bare arm line: no layers", sel=".arm-head h2", arm="bare"),
        ),
        ("decisions-harness",),
    ),
    Moment(
        "screen-1-gate-pending",
        1,
        "when the agent claimed done and the gate started",
        lambda ev: _first(ev, lambda e: e.get("type") == "gate_result"),
        (
            Spec("Gate list: checks pending", sel=".pills", arm=H),
            Spec("Agent said", sel=".claims p", arm=H),
        ),
    ),
    Moment(
        "screen-1-gate-refused",
        1,
        "when the gate refused the agent's 'done'",
        lambda ev: _first(ev, lambda e: _gate_done(e, False), extra=1),
        (
            Spec("Gate refused 'done'", sel=".gate-refusals", arm=H),
            Spec("Gate list", sel=".pills", arm=H),
        ),
        ("decisions-harness",),
    ),
    Moment(
        "screen-1-gate-passed",
        1,
        "when the gate passed",
        lambda ev: _first(ev, lambda e: _kind(e) == "gate_pass"),
        (
            Spec("Gate list: every check passed", sel=".pills", arm=H),
            Spec("Gate passed", sel=".decisions li", text="passed", arm=H),
            Spec("Gate refused 'done', then passed", sel=".gate-refusals", arm=H),
        ),
        ("decisions-harness",),
    ),
    Moment(
        "screen-1-bare-verdict",
        1,
        "when the bare arm's verdict was ready",
        _primary("bare"),
        (
            Spec("Bare referee pill", sel=".referee .ref-line", arm="bare"),
            Spec("Secondary checks running", sel=".referee", text="secondary checks", arm="bare"),
            Spec("Harness still working", sel=".list-head", arm=H),
        ),
    ),
    Moment(
        "screen-1-primary",
        1,
        "when the first primary verdict was ready",
        _primary(None),
        (
            Spec("Referee pill (harness)", sel=".referee .ref-line", arm=H),
            Spec("Referee pill (bare)", sel=".referee .ref-line", arm="bare"),
            Spec("Secondary checks running", sel=".referee", text="secondary checks", arm=H),
        ),
    ),
]
DEMO_MOMENTS = {
    "s1": ["screen-1-early"],
    "s2": ["screen-1-early", "screen-1-session-stop", "screen-1-session-resumed"],
    "s3": ["screen-1-early", "screen-1-block", "screen-1-primary"],
    "s4": [
        "screen-1-early",
        "screen-1-block",
        "screen-1-gate-pending",
        "screen-1-gate-refused",
        "screen-1-gate-passed",
        "screen-1-primary",
    ],
    "final": [
        "screen-1-early",
        "screen-1-both-arms",
        "screen-1-gate-passed",
        "screen-1-bare-verdict",
        "screen-1-primary",
    ],
    "replay": [],
}
BY_NAME = {m.name: m for m in MOMENTS}


def write_cut(src_run: Path, runs_dir: Path, upto: int) -> Path:
    """A copy of the run with its log cut after event `upto` (no ab.json: not finished)."""
    dst = runs_dir / src_run.name
    if not dst.exists():
        shutil.copytree(src_run, dst, ignore=shutil.ignore_patterns("ab.json", "events.jsonl"))
    lines = []
    for line in (src_run / "events.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            if json.loads(line)["seq"] > upto:
                break
        except (json.JSONDecodeError, KeyError):
            continue
        lines.append(line)
    (dst / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dst


def event_words(events: list[dict[str, Any]], seq: int) -> str:
    """'event 154 (harness_decision block)': the event a moment is about."""
    for e in events:
        if e.get("seq") == seq:
            kind = _kind(e)
            return f"event {seq} ({e.get('type')}{' ' + kind if kind else ''})"
    return f"event {seq}"


def capture_cuts(
    con: Console,
    out: Out,
    src_run: Path,
    runs_dir: Path,
    names: Iterable[str],
    note: str,
    view: bool = True,
) -> list[str]:
    events = read_events(src_run / "events.jsonl")
    done = []
    for name in names:
        m = BY_NAME[name]
        found = m.find(events)
        if found is None:
            log(f"  {name}: no such moment in {src_run.name}")
            continue
        trig, seq = found
        write_cut(src_run, runs_dir, seq)
        con.open_run(src_run.name)
        capture_screen(
            con,
            out,
            m.screen,
            name=name,
            moment=f"{m.words} ({note} {seq}; the moment's event is {event_words(events, trig)})",
            specs=list(m.specs),
            expand=m.expand,
            crops=False,
            full=True,
            view=view,
        )
        done.append(name)
    shutil.rmtree(runs_dir / src_run.name, ignore_errors=True)
    return done


# Terminal renders -----------------------------------------------------------------------------


def _command_of(text: str, meta: dict[str, Any]) -> str | None:
    if meta.get("command"):
        return str(meta["command"])
    for line in text.splitlines()[:4]:
        if line.startswith(("uv run ", "make ")):
            return line.rstrip(" \\")
    return None


def term_facts(text: str) -> str:
    bits = []
    m = re.search(r"^A/B (ab-[0-9a-f-]+)", text, re.MULTILINE)
    if m:
        bits.append(f"the A/B line names {m.group(1)}")
    for arm, status, rest in re.findall(r"^\s+(bare|harness)\s+(\w+)\s+(.*)$", text, re.MULTILINE):
        passed = re.search(r"passed=(\w+)|primary measure (passed|failed)", rest)
        word = None
        if passed:
            word = f"passed={passed.group(1)}" if passed.group(1) else passed.group(0)
        bits.append(f"the {arm} arm line reads {status}" + (f", {word}" if word else ""))
    c = re.search(r"^Cost: (\$[0-9.]+)", text, re.MULTILINE)
    if c:
        bits.append(f"the Cost line totals {c.group(1)}")
    return "; ".join(bits)


def capture_terms(
    src: Path,
    out: Out,
    *,
    label: str,
    title: str = "Terminal 2",
    tail: int = 8,
    head: int = 10,
    command: str | None = None,
    prefix: str = "term",
) -> None:
    from term_render import render

    text = src.read_text(encoding="utf-8", errors="replace")
    meta_path = src.parent / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    lines = text.splitlines()
    if lines and lines[0].startswith("$ "):  # the capture starts with its own prompt line
        command = command or lines[0][2:].strip()
        lines = lines[1:]
        text = "\n".join(lines) + "\n"
    command = command or _command_of(text, meta)
    facts = term_facts(text)
    n = len(lines)
    # Start: through the "A/B ..." line when there is one; end: from the first arm line.
    ab = next((i for i, x in enumerate(lines) if x.startswith("A/B ")), None)
    arm = next((i for i, x in enumerate(lines) if re.match(r"\s+(bare|harness)\s", x)), None)
    start = f"1-{min(n, ab + 1 if ab is not None and ab < 20 else head)}"
    end = f"{arm + 1}-{n}" if arm is not None and n - arm <= 20 else f"-{min(tail, n)}"
    shown = f"`{command}`" if command else "the command"
    jobs = [
        (f"{prefix}-start", start, f"the first lines of {shown} for {label}, right after launch"),
        (f"{prefix}-end", end, f"the final lines of {shown} for {label}"),
    ]
    if n <= 80:  # a long log (make warm) is shown by its first and final lines only
        jobs.insert(0, (f"{prefix}-full", None, f"the whole output of {shown} for {label}"))
    for name, ranges, words in jobs:
        file = f"{name}.png"
        render(text, out.folder / file, command=command, ranges=ranges, title=title)
        alt = (
            f"Terminal output: {words}"
            + (f"; {facts}" if facts and name != f"{prefix}-start" else "")
            + "."
        )
        out.add(file, "terminal", words.replace("`", ""), alt.replace("`", ""), [])
        log(f"  {out.folder.name}/{file}")


# Live watch -----------------------------------------------------------------------------------


def demo_of(run_dir: Path) -> str | None:
    """s1..s4, final, or replay, from the run's run_start events (checkpoint, arms) or its
    recording. Section 3's A/B starts from the Section 4 checkpoint too: it has a bare arm."""
    arms, cp = set(), ""
    events = read_events(run_dir / "events.jsonl")[:60]
    for e in events:
        if e.get("recorded"):
            return "replay"
        if e.get("type") == "run_start":
            arms.add(e.get("arm"))
            cp = cp or str(e["data"].get("spec", {}).get("checkpoint", ""))
    if "final" in cp:
        return "final"
    m = re.search(r"-s(\d)-", cp)
    if not m:
        return None
    if m.group(1) == "4" and "bare" in arms:
        return "s3"
    if m.group(1) == "4" and len(events) < 30:
        return None  # too early to tell Section 3's A/B from show-4
    return f"s{m.group(1)}"


def archive_recorded(folder: Path) -> None:
    """Move the recorded set into recorded/ before the live set replaces it (once)."""
    entries = load_entries(folder / "images.json")
    if not entries or all(e["recorded_or_live"] == "live" for e in entries):
        return
    keep = folder / "recorded"
    keep.mkdir(exist_ok=True)
    rec = [e for e in entries if e["recorded_or_live"] == "recorded"]
    for e in rec:
        if (folder / e["file"]).is_file():
            shutil.move(str(folder / e["file"]), keep / e["file"])
    save_entries(keep / "images.json", merge_entries(load_entries(keep / "images.json"), rec))
    save_entries(folder / "images.json", [e for e in entries if e not in rec])
    log(f"{folder.name}: {len(rec)} recorded images moved to recorded/")


@dataclass
class LiveDemo:
    demo: str
    run_dir: Path | None = None
    seen: set[str] = field(default_factory=set)
    finished: bool = False


def watch(args: argparse.Namespace) -> int:
    demos = args.demos.split(",")
    status, images, runs = Path(args.status), Path(args.images), Path(args.runs)
    state = {d: LiveDemo(d) for d in demos}
    for d, s in state.items():  # a restarted watcher skips the demos it already finished
        if (images / d / ".live-done").exists():
            s.finished = True
    con = Console(args.base)
    cut_con = Console(args.cut_base) if args.cut_base else None
    log(f"watching {', '.join(demos)} (console {args.base}, runs {runs.name})")
    try:
        while not all(s.finished for s in state.values()):
            for d, s in state.items():
                flag = status / d / "STARTED"
                if not flag.exists():
                    flag = status / d / "DONE"
                if s.finished or not flag.exists():
                    continue
                started = flag.stat().st_mtime
                if s.run_dir is None:
                    s.run_dir = _find_run(runs, d, started)
                    if s.run_dir:
                        log(f"{d}: live run {s.run_dir.name}")
                if s.run_dir and d not in ("setup",):
                    _live_moments(con, s, images / d)
                if (status / d / "DONE").exists():
                    meta = status / d / "meta.json"
                    rid = json.loads(meta.read_text()).get("run_id") if meta.is_file() else None
                    if rid and (runs / str(rid)).is_dir():
                        s.run_dir = runs / str(rid)
                    try:
                        _after_done(con, cut_con, s, status / d, images / d, Path(args.cut_runs))
                        (images / d / ".live-done").write_text(time.ctime() + "\n")
                    except Exception as err:  # noqa: BLE001 - keep watching the other demos
                        log(f"! {d}: capture after DONE failed: {err!r}")
                    s.finished = True
            time.sleep(1.0)
    finally:
        con.close()
        if cut_con:
            cut_con.close()
        Console.shutdown()
    log("all demos captured")
    return 0


def _find_run(runs: Path, demo: str, started: float) -> Path | None:
    if demo == "setup":
        return None
    for run in sorted(runs.glob("ab-*"), reverse=True):
        recent = (run / "events.jsonl").is_file() and run.stat().st_mtime >= started - 120
        if recent and demo_of(run) == demo:
            return run
    return None


def _live_moments(con: Console, s: LiveDemo, folder: Path) -> None:
    events = read_events(s.run_dir / "events.jsonl")
    for name in DEMO_MOMENTS.get(s.demo, []):
        if name in s.seen:
            continue
        found = BY_NAME[name].find(events)
        if found is None:
            continue
        trig, seq = found
        # The early moment fires once a minute has passed; the others on their event.
        if name == "screen-1-early" and (not events or _ts(events[-1]) - _ts(events[0]) < 60):
            continue
        s.seen.add(name)
        if events and seq < events[-1]["seq"] - 40:
            log(f"{s.demo}: {name} already passed (event {seq}); the replay cut covers it")
            continue
        time.sleep(1.5)
        m = BY_NAME[name]
        out = Out(folder, s.demo, "live", s.run_dir.name)
        archive_recorded(folder)
        try:
            con.open_run(s.run_dir.name)
            capture_screen(
                con,
                out,
                m.screen,
                name=name,
                moment=(
                    f"{m.words} (captured live; the moment's event is "
                    f"{event_words(events, trig)}; the console showed event {{shown}})"
                ),
                specs=list(m.specs),
                expand=m.expand,
                crops=False,
                full=True,
            )
            out.save()
            s.seen.add(name + ":live")
        except Exception as err:  # noqa: BLE001 - a missed moment is filled from the replay
            log(f"! {s.demo} {name}: live capture failed: {err}")


def _after_done(
    con: Console, cut_con: Console | None, s: LiveDemo, status: Path, folder: Path, cut_runs: Path
) -> None:
    log(f"{s.demo}: DONE")
    archive_recorded(folder)
    out = Out(folder, s.demo, "live", s.run_dir.name if s.run_dir else None)
    term = status / "terminal.txt"
    if s.demo == "setup":
        _setup_terms(status, out)
        capture_list(con, out, "runlist", "after the live runs started", None)
        out.save()
        return
    if s.run_dir:
        capture_run(con, out, s.run_dir.name, "after the run finished")
    if term.is_file():
        capture_terms(term, out, label=DEMOS[s.demo])
    out.save()
    caught = {  # captured live, also by an earlier watcher process
        e["file"][:-4]
        for e in load_entries(folder / "images.json")
        if "captured live" in e["moment"]
    }
    missed = [
        n for n in DEMO_MOMENTS.get(s.demo, []) if n + ":live" not in s.seen and n not in caught
    ]
    if missed and cut_con and s.run_dir:
        cut_runs.mkdir(parents=True, exist_ok=True)
        out2 = Out(folder, s.demo, "live", s.run_dir.name)
        got = capture_cuts(
            cut_con,
            out2,
            s.run_dir,
            cut_runs,
            missed,
            "captured from replay: the run's log replayed to event",
        )
        out2.save()
        log(f"{s.demo}: from replay: {', '.join(got) or 'none'}")


def _setup_terms(status: Path, out: Out) -> None:
    for name, title in (
        ("doctor", "Terminal 1"),
        ("warm", "Terminal 1"),
        ("console", "Terminal 1"),
    ):
        src = status / f"{name}.txt"
        if src.is_file():
            capture_terms(
                src,
                out,
                label=f"make {name}",
                title=title,
                prefix=f"term-{name}",
                command=f"make {name}",
            )
    if (status / "terminal.txt").is_file():
        capture_terms(status / "terminal.txt", out, label="the setup", title="Terminal 1")


# CLI ------------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Console screenshots for the demo guide.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp: argparse.ArgumentParser, base: bool = True) -> None:
        if base:
            sp.add_argument("--base", default="http://127.0.0.1:8771")
        sp.add_argument("--demo", required=True, choices=sorted(DEMOS))
        sp.add_argument("--out", required=True, type=Path)
        sp.add_argument("--kind", default="recorded", choices=["recorded", "live"])
        sp.add_argument("--run-id", default=None)

    sp = sub.add_parser("run")
    common(sp)
    sp.add_argument("--moment", default="after the run finished")
    sp.add_argument("--no-runlist", action="store_true")
    sp = sub.add_parser("list")
    common(sp)
    sp.add_argument("--name", default="runlist")
    sp.add_argument("--moment", default="the run list")
    sp = sub.add_parser("cut")
    common(sp)
    sp.add_argument("--runs-dir", required=True, type=Path)
    sp.add_argument("--src", required=True, type=Path)
    sp.add_argument("--moments", default="")
    sp.add_argument("--note", default="the recorded run's log cut at event")
    sp.add_argument("--only-full", action="store_true", help="save only the whole-page images")
    sp = sub.add_parser("terms")
    common(sp, base=False)
    sp.add_argument("--src", required=True, type=Path)
    sp.add_argument("--title", default="Terminal 2")
    sp.add_argument("--prefix", default="term")
    sp.add_argument("--command", default=None)
    sp = sub.add_parser("watch")
    sp.add_argument("--demos", default="setup,s1,s2,s3,s4,final,replay")
    sp.add_argument("--base", default="http://127.0.0.1:8770")
    sp.add_argument("--cut-base", default="http://127.0.0.1:8772")
    sp.add_argument("--cut-runs", required=True)
    sp.add_argument("--runs", required=True)
    sp.add_argument("--status", required=True)
    sp.add_argument("--images", required=True)
    a = p.parse_args(argv)

    if a.cmd == "watch":
        return watch(a)
    a.out.mkdir(parents=True, exist_ok=True)
    out = Out(a.out, a.demo, a.kind, a.run_id)
    if a.cmd == "terms":
        capture_terms(
            a.src, out, label=DEMOS[a.demo], title=a.title, prefix=a.prefix, command=a.command
        )
        out.save()
        return 0
    con = Console(a.base)
    try:
        if a.cmd == "run":
            capture_run(con, out, a.run_id, a.moment, runlist=not a.no_runlist)
        elif a.cmd == "list":
            capture_list(con, out, a.name, a.moment, a.run_id)
        elif a.cmd == "cut":
            names = [n for n in a.moments.split(",") if n] or DEMO_MOMENTS[a.demo]
            out.run_id = out.run_id or a.src.name
            a.runs_dir.mkdir(parents=True, exist_ok=True)
            capture_cuts(con, out, a.src, a.runs_dir, names, a.note, view=not a.only_full)
    except PrivacyError as err:
        print(f"x {err}", file=sys.stderr)
        return 1
    finally:
        con.close()
        Console.shutdown()
    out.save()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
