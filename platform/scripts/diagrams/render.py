"""Render .excalidraw files to SVG (fonts embedded) and PNG (2x) with Excalidraw's own export.

Usage: uv run --with playwright python render.py FILE_OR_DIR [...]

It loads @excalidraw/excalidraw (pinned) from esm.sh in headless Chromium and calls exportToSvg
and exportToBlob. Each `name.excalidraw` gets `name.svg` and `name.png` beside it, cropped to the
diagram's light panel (transparent outside its rounded corners).
"""

from __future__ import annotations

import asyncio
import base64
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright
from style import PNG_SCALE

EXCALIDRAW = "0.18.0"
REACT = "18.3.1"
PADDING = 0  # the panel is the canvas: crop tight to it
SCALE = PNG_SCALE

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<script>window.EXCALIDRAW_ASSET_PATH =
  "https://unpkg.com/@excalidraw/excalidraw@{EXCALIDRAW}/dist/prod/";</script>
<script type="module">
import * as EX from "https://esm.sh/@excalidraw/excalidraw@{EXCALIDRAW}?deps=react@{REACT},react-dom@{REACT}";
const appState = {{ exportBackground: false, viewBackgroundColor: "#ffffff",
                    exportWithDarkMode: false }};
window.renderScene = async (scene) => {{
  const elements = scene.elements;
  const svg = await EX.exportToSvg({{ elements, appState, files: {{}}, exportPadding: {PADDING} }});
  svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  const blob = await EX.exportToBlob({{
    elements, appState, files: {{}}, exportPadding: {PADDING}, mimeType: "image/png",
    getDimensions: (w, h) => ({{ width: w * {SCALE}, height: h * {SCALE}, scale: {SCALE} }}),
  }});
  const buf = new Uint8Array(await blob.arrayBuffer());
  let bin = "";
  for (let i = 0; i < buf.length; i += 0x8000)
    bin += String.fromCharCode(...buf.subarray(i, i + 0x8000));
  return {{ svg: svg.outerHTML, png: btoa(bin) }};
}};
window.ready = true;
</script></head><body></body></html>"""


def targets(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        out += sorted(p.glob("*.excalidraw")) if p.is_dir() else [p]
    return out


async def main(args: list[str]) -> int:
    files = targets(args)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        page.on("pageerror", lambda e: print("pageerror:", e, file=sys.stderr))
        await page.route(
            "http://render.local/", lambda r: r.fulfill(body=HTML, content_type="text/html")
        )
        await page.goto("http://render.local/")
        await page.wait_for_function("window.ready === true", timeout=180_000)
        for f in files:
            scene = json.loads(f.read_text(encoding="utf-8"))
            out = await page.evaluate("s => window.renderScene(s)", scene)
            svg = out["svg"]
            if "@font-face" not in svg or "Excalifont" not in svg:
                print(f"WARNING {f.name}: no embedded Excalifont in the SVG", file=sys.stderr)
            f.with_suffix(".svg").write_text(svg + "\n", encoding="utf-8")
            f.with_suffix(".png").write_bytes(base64.b64decode(out["png"]))
            print(f"rendered {f}")
        await browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1:])))
