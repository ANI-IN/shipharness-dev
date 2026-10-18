"""Check the console's layout on recorded runs in a real browser, at any size: no model calls.

Runs the checks of `shipharness.console.layout_check` (no sideways scrolling, nothing past the right
edge, nothing clipped or cut by an ellipsis, pills on one line, no mid-word breaks, the page scrolls
to its bottom, "All runs" goes back) on:
- the sweep: every `--step` CSS px from 320 to 2560 at heights 600 and 1000, plus pixel ratios
  1.25, 1.5, and 2 at a few widths; screens 1, 3, and 4 of every run, the run list, and an empty
  run list;
- the named viewports (display scaling, zoom, phone, class sizes): every screen of every run.

    uv run python platform/scripts/check_console_layout.py --label show-1=ab-... [--step 40] \
        [--shots DIR]

`--shots DIR` saves full-page screenshots: `<run>-screen<N>-<viewport>.png` for the named
viewports and the sweep widths 320, 768, 1097, 1280, and 2560, and `runlist-<viewport>.png`.
Exit 1 on any problem.
"""

from __future__ import annotations

import argparse
import socket
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from shipharness.console.app import create_console_app
from shipharness.console.layout_check import VIEWPORTS, runlist_problems, screen_problems, sweep

SHOT_WIDTHS = (320, 768, 1097, 1280, 2560)


def _serve(app: Any) -> str:
    import uvicorn

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    deadline = time.monotonic() + 15
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    return f"http://127.0.0.1:{port}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--label", action="append", default=[], help="name=run id")
    parser.add_argument("--runs-dir", type=Path, default=Path(".shipharness/runs"))
    parser.add_argument("--exports", type=Path, default=Path("exports"))
    parser.add_argument("--step", type=int, default=40, help="sweep step in CSS px")
    parser.add_argument("--shots", type=Path, default=None)
    args = parser.parse_args(argv)
    runs = {v: k for k, v in (item.split("=", 1) for item in args.label)}
    if not runs:
        parser.error("name at least one run with --label name=run id")

    from playwright.sync_api import sync_playwright

    base = _serve(create_console_app(args.runs_dir, args.exports))
    empty = _serve(create_console_app(Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())))
    if args.shots:
        args.shots.mkdir(parents=True, exist_ok=True)
    checked = failed = 0
    plan = [(vp, "12345", True) for vp in VIEWPORTS]
    plan += [
        (vp, "134", vp.dpr == 1 and vp.height == 1000 and vp.width in SHOT_WIDTHS)
        for vp in sweep(args.step)
    ]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for vp, keys, named in plan:
            shoot = bool(args.shots) and named
            context = browser.new_context(
                viewport={"width": vp.width, "height": vp.height}, device_scale_factor=vp.dpr
            )
            page = context.new_page()
            for label, url in (("runlist", f"{base}/"), ("runlist-empty", f"{empty}/")):
                page.goto(url)
                problems = runlist_problems(page)
                checked += 1
                failed += bool(problems)
                if problems:
                    print(f"{label} {vp.name}: {'; '.join(problems[:3])}")
                if shoot:
                    page.screenshot(path=str(args.shots / f"{label}-{vp.name}.png"), full_page=True)
            for rid, name in runs.items():
                page.goto(f"{base}/run/{rid}")
                page.wait_for_function(
                    "/^(live|finished)/.test(document.getElementById('conn').textContent)"
                )
                for key in keys:
                    problems = screen_problems(page, key)
                    checked += 1
                    failed += bool(problems)
                    if problems:
                        print(f"{name} screen {key} {vp.name}: {'; '.join(problems[:3])}")
                    if shoot:
                        shot = args.shots / f"{name}-screen{key}-{vp.name}.png"
                        page.screenshot(path=str(shot), full_page=True)
                page.locator("a.all-runs").click()
                page.wait_for_url(f"{base}/")
            context.close()
        browser.close()
    print(f"{checked - failed} of {checked} page checks passed in {len(plan)} viewports")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
