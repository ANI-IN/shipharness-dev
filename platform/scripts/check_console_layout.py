"""Check the console's layout on recorded runs in a real browser at the three class screen sizes.

At 1366x768, 1440x900, and 1920x1080, for every screen of every run: nothing scrolls sideways, no
element clips its content, every panel is inside the window, the page scrolls to its last panel,
and "All runs" goes back to the list
(`shipharness.console.layout_check`, the same checks as the browser tests). No model calls.

    uv run python platform/scripts/check_console_layout.py RUN_ID [RUN_ID ...] \
        [--label show-1=ab-...] [--shots DIR]

`--shots DIR` saves a full-page screenshot per screen as `<run>-screen<N>-<width>.png` (the run's
label when given). Exit 1 on any problem.
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
from pathlib import Path

from shipharness.console.app import create_console_app
from shipharness.console.layout_check import SIZES, screen_problems


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", nargs="*", help="run ids (A/B ids) under --runs-dir")
    parser.add_argument("--label", action="append", default=[], help="name=run id")
    parser.add_argument("--runs-dir", type=Path, default=Path(".shipharness/runs"))
    parser.add_argument("--exports", type=Path, default=Path("exports"))
    parser.add_argument("--shots", type=Path, default=None)
    args = parser.parse_args(argv)
    labelled = dict(item.split("=", 1) for item in args.label)
    runs = {**{rid: rid for rid in args.runs}, **{v: k for k, v in labelled.items()}}
    if not runs:
        parser.error("name at least one run")

    import uvicorn
    from playwright.sync_api import sync_playwright

    port = _free_port()
    app = create_console_app(args.runs_dir, args.exports)
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    deadline = time.monotonic() + 15
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    base = f"http://127.0.0.1:{port}"
    if args.shots:
        args.shots.mkdir(parents=True, exist_ok=True)
    failures = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for rid, name in runs.items():
            for width, height in SIZES:
                context = browser.new_context(
                    viewport={"width": width, "height": height}, device_scale_factor=1
                )
                page = context.new_page()
                page.goto(f"{base}/run/{rid}")
                page.wait_for_timeout(1500)
                for key in "12345":
                    problems = screen_problems(page, key)
                    status = "ok" if not problems else "; ".join(problems[:5])
                    print(f"{name} screen {key} {width}x{height}: {status}")
                    failures += bool(problems)
                    if args.shots:
                        shot = args.shots / f"{name}-screen{key}-{width}.png"
                        page.screenshot(path=str(shot), full_page=True)
                page.locator("a.all-runs").click()
                page.wait_for_url(f"{base}/")
                context.close()
        browser.close()
    server.should_exit = True
    print(f"{failures} screen(s) with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
