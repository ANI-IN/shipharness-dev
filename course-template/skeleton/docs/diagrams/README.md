# {{MODULE_TITLE}} - Diagrams

Every diagram has three files with the same name:

| File | What it is for |
|---|---|
| `.excalidraw` | The source. Open it at excalidraw.com to edit it |
| `.png` | A render at 2x scale, for slides |
| `.svg` | A render with the font embedded, for pages on GitHub |

A diagram built up on slides one step at a time also has step frames, named `-step-1`, `-step-2`,
and so on. Each frame adds one element, and every frame has the same size, so the picture does
not jump between slides. The file without a step number is the full diagram.

The colours mean the same thing in every diagram:

| Colour | Meaning |
|---|---|
| Grey `#78909C` | The baseline: the run without the module's piece |
| Blue `#3896D2` | The module's piece, and the parts of it |
| Amber `#FFAB40` | What to notice: a claim, a question |
| Red `#E46962` | A "no": a block, a revert, a failure |
| Dark `#212121` | Every label, and everything else |

Every diagram sits on a light rounded panel (`#F0F3F6`), so it reads on the navy slide
background (`#324158`) and on GitHub in light or dark mode. Each panel is a fixed canvas: 1920 by
1080, placed at 80% of the slide width, so every label shows at 20 px or more on a 1080p slide.
Colour is never the only signal: each diagram names its parts in words, and its alt text and
caption say what it shows.

## The diagrams

<!-- guide: one H3 per shared diagram: the SVG with alt text and an italic caption, then four bullets (what it teaches, slide topic, files, source in the code). -->
