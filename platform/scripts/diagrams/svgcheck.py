"""Open SVGs as <img> (as GitHub shows them), with every network request blocked.

Usage: uv run --with playwright python svgcheck.py OUT.png FILE.svg [...]

It prints whether every image decoded and which requests were blocked (none expected: the fonts
are embedded), and saves a screenshot to look at.
"""

from __future__ import annotations

import asyncio
import base64
import sys
from pathlib import Path

from playwright.async_api import Route, async_playwright

PAGE = "http://check.local/"


def page_html(svgs: list[str]) -> str:
    imgs = []
    for s in svgs:
        data = base64.b64encode(Path(s).read_bytes()).decode()
        imgs.append(f'<img style="width:1300px" src="data:image/svg+xml;base64,{data}"><br>')
    return f"<html><body style='background:#0d1117'>{''.join(imgs)}</body></html>"


async def main(out: str, svgs: list[str]) -> int:
    html = page_html(svgs)
    blocked: list[str] = []

    async def route(r: Route) -> None:
        url = r.request.url
        if url == PAGE:
            await r.fulfill(body=html, content_type="text/html")
        elif url.startswith("data:"):
            await r.continue_()
        else:
            blocked.append(url)
            await r.abort()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.route("**/*", route)
        await page.goto(PAGE)
        await page.wait_for_timeout(1500)
        ok = await page.evaluate("[...document.images].every(i => i.complete && i.naturalWidth)")
        await page.screenshot(path=out, full_page=True)
        await browser.close()
    print("all images decoded:", bool(ok), "| blocked requests:", blocked or "none")
    return 0 if ok and not blocked else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1], sys.argv[2:])))
