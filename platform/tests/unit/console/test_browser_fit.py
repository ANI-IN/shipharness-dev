"""The console fits the screen at 100% zoom at 1366x768, 1440x900, and 1920x1080: no horizontal
scrolling, every panel inside the window, and panels stack on a narrow window. Every run page has an
"All runs" link, and H or Esc goes back to the run list (not while typing in a field).

Marked `browser`; skips cleanly when Chromium is not installed.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from shipharness.console.app import create_console_app
from tests.unit.console.fixture_log import AB_ID, build_fixture_exports, build_fixture_run
from tests.unit.console.run_logs import single_arm_run

pytestmark = pytest.mark.browser

SIZES = [(1366, 768), (1440, 900), (1920, 1080)]
SINGLE = "ab-20261018-045459-aaaaaa"

FIT = """(key) => {
  const w = window.innerWidth, h = window.innerHeight;
  const panels = [...document.querySelectorAll('#screen-' + key + ' .panel')]
    .filter(p => p.offsetParent !== null);
  const out = panels.filter(p => {
    const r = p.getBoundingClientRect();
    return r.left < -1 || r.right > w + 1 || r.bottom > h + 1;
  }).map(p => (p.querySelector('h2') || p).textContent.trim().slice(0, 30));
  return {scroll: document.documentElement.scrollWidth, w, panels: panels.length, out};
}"""


@pytest.fixture
def base(tmp_path: Path, live_server: Callable[[Any], Any]) -> str:
    runs = tmp_path / "runs"
    build_fixture_run(runs)
    single_arm_run(runs, SINGLE)
    exports = build_fixture_exports(tmp_path / "exports")
    return str(live_server(create_console_app(runs, exports_dir=exports)).url)


def _page(chromium: Any, width: int, height: int) -> Any:
    context = chromium.new_context(
        viewport={"width": width, "height": height}, device_scale_factor=1, bypass_csp=True
    )
    return context, context.new_page()


@pytest.mark.parametrize(("width", "height"), SIZES)
@pytest.mark.parametrize("run", [AB_ID, SINGLE])
def test_every_screen_fits_the_window(
    chromium: Any, base: str, run: str, width: int, height: int
) -> None:
    context, page = _page(chromium, width, height)
    try:
        page.goto(f"{base}/run/{run}")
        for key in "12345":
            page.keyboard.press(key)
            fit = page.evaluate(FIT, key)
            assert fit["panels"] >= 1, key
            assert fit["scroll"] <= fit["w"], (key, fit)  # no horizontal scrolling
            assert fit["out"] == [], (key, fit)  # no panel cut off at the window edge
    finally:
        context.close()


def test_panels_stack_on_a_narrow_window(chromium: Any, base: str) -> None:
    context, page = _page(chromium, 900, 1000)
    try:
        page.goto(f"{base}/run/{AB_ID}")
        page.keyboard.press("3")
        lefts = page.evaluate(
            "[...document.querySelectorAll('#screen-3 .panel')].map(p => "
            "Math.round(p.getBoundingClientRect().left))"
        )
        assert len(lefts) == 3 and len(set(lefts)) == 1  # one column
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    finally:
        context.close()


def test_body_text_stays_projector_readable_at_1366(chromium: Any, base: str) -> None:
    context, page = _page(chromium, 1366, 768)
    try:
        page.goto(f"{base}/run/{AB_ID}")
        size = page.evaluate("parseFloat(getComputedStyle(document.body).fontSize)")
        assert size >= 20
    finally:
        context.close()


@pytest.mark.parametrize("key", ["h", "H", "Escape"])
def test_h_or_escape_goes_back_to_the_run_list(chromium: Any, base: str, key: str) -> None:
    context, page = _page(chromium, 1440, 900)
    try:
        page.goto(f"{base}/run/{SINGLE}")
        link = page.locator("a.all-runs")
        assert link.is_visible() and link.text_content().strip() == "← All runs"
        box = link.bounding_box()
        assert box["x"] < 100 and box["y"] < 80  # top left
        page.keyboard.press(key)
        page.wait_for_url(f"{base}/")
        assert "Runs" in page.content()
    finally:
        context.close()


def test_h_typed_in_a_field_and_screen_keys_do_not_navigate(chromium: Any, base: str) -> None:
    context, page = _page(chromium, 1440, 900)
    try:
        url = f"{base}/run/{SINGLE}"
        page.goto(url)
        for key in ["1", "2", "3", "4", "5", "f", "F"]:
            page.keyboard.press(key)
        assert page.url.startswith(url)
        page.evaluate(
            "() => { const i = document.createElement('input'); i.id = 'probe';"
            " document.body.appendChild(i); i.focus(); }"
        )
        page.keyboard.press("h")
        page.keyboard.press("Escape")
        assert page.url.startswith(url)
        page.keyboard.press("Control+h")
        assert page.url.startswith(url)
    finally:
        context.close()
