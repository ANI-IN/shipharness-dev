# Module 1: Harness Engineering for Coding Agents - Live Demo Guide

This folder holds the sources of the Live Demo Guide, a PDF that walks through the five live
demos of the class one command and one screen at a time. The finished PDF is
[Harness-Engineering-Demo-Guide.pdf](Harness-Engineering-Demo-Guide.pdf).

## What is here

| Path | What it holds |
|---|---|
| `source/intro.md` | The short introduction after the contents |
| `part0.md` | Part 0: Before you start (terminals, checks, the console) |
| `chapters/` | One chapter per demo, Sections 1 to 4 and the final |
| `appendix.md` | Cheat sheet, troubleshooting, glossary, and the replay fallback |
| `images/` | Screenshots and terminal images, copied in by the build |
| `source/` | The build script, the page template, the styles, and the Markdown conventions |

The Markdown conventions (steps, boxes, screenshots with numbered callouts) are in
[source/CONVENTIONS.md](source/CONVENTIONS.md).

## Build the PDF

From the repository root, in the Ubuntu terminal:

```bash
uv run python docs/walkthrough/source/build_pdf.py --images
```

`--images` first copies the screenshots from `~/guide-work/images/` into `images/`; leave it out to
build from the images already here. `--desktop-copy` followed by a folder also copies the PDF
there. The build makes no model calls and starts no container. It needs only the packages of
`uv sync`: `markdown-it-py` for the Markdown and Playwright's Chromium for printing (install the
browser once with `uv run playwright install chromium`). The page size is 210 by 297 mm, and the fonts are
DejaVu Sans and DejaVu Sans Mono.

The build prints the page count, then one line for each missing chapter, missing image, or unknown
box. A missing image prints as a placeholder box in the PDF.
