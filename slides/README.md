# Slides

The Module 1 slides: 72 slides for the 240-minute class.

| File | What it is |
|---|---|
| `deck.md` | The deck source and the single source of the slide content, one block per slide. Edit this file |
| `outline.md` | The block table and the class plan per section; it points to `deck.md` for every slide's content |
| `deck.pdf`, `deck.pptx` | The released build: copies of `dist/deck.pdf` and `dist/deck.pptx`, committed |
| `img/` | Console screenshots from the quiet runs of the class commands (2026-10-17), cut to the harness panel and joined with the board view; each slide that shows one names its run id |
| `dist/` | Build output (`deck.html`, `deck.pdf`, `deck.pptx`, cached diagram PNGs); not tracked |

`outline.md` used to repeat every slide's content as a table. Keeping two copies of 72 slides in
step was not practical, so the slide content now lives only in `deck.md`.

## Build

```bash
make slides                                   # validate, then write dist/deck.html, deck.pdf, deck.pptx
uv run python platform/scripts/build_slides.py --check   # validate and list open items only (no browser)
make slides SLIDES_OPTS=--strict              # release check: fails while any open item remains
cp slides/dist/deck.pdf slides/dist/deck.pptx slides/   # after a clean strict build: the released copies
```

The build needs Playwright's Chromium (`uv run playwright install chromium`) and, the first time each
diagram is drawn, network access to load Mermaid 11.4.1 from cdn.jsdelivr.net. Diagram PNGs are cached
in `dist/diagrams/` by content hash, so later builds work offline until a diagram changes.

### If the build fails

| What you see (exact text) | Cause | Fix |
|---|---|---|
| `x Chromium did not start (uv run playwright install chromium): ...` or `x playwright is not installed: ...`, exit code 3 | Playwright's Chromium is missing | `uv run playwright install chromium`, then `make slides` again |
| `x browser step failed: <error type>: ...`, exit code 3, while a new or changed diagram is drawn | The first render of that diagram cannot load Mermaid from cdn.jsdelivr.net | Connect to the network and rerun; diagrams already cached in `dist/diagrams/` need no network |
| `x slide N (line L): ...` lines, then `<n> validation errors; nothing built`, exit code 2 | A slide breaks a rule in the list of checks below (count, bullets, image path, code reference) | Fix that slide in `deck.md`; `uv run python platform/scripts/build_slides.py --check` repeats the check without a browser |
| `! slide N: text still overflows at <px>px; shorten it` or `! slide N: body text shrunk to <px>px to fit` | Too much text for one slide | Shorten that slide's bullets, or move detail to its notes |
| `x --strict: open items remain`, exit code 1 | A PENDING or CAPTURE marker or an empty result slot is left | The report above that line lists each one with its slide; fill or remove it |

The HTML page is the layout engine: each slide is a 1280 x 720 page, and text that does not fit is
shrunk step by step. The PDF is printed from that page. The PPTX has native text boxes with the same
font sizes, diagrams as pictures, and the speaker notes (each starting with "Slide N of 72 | section |
minutes"). The build prints a warning for any slide whose text had to shrink below 22 px or still
overflows; shorten that slide.

Checks that stop the build (exit code 2): exactly 72 slides numbered 1 to 72 in order, a section on
every slide, at most 6 bullets and 12 code lines per slide, every image path present, every code
reference resolving to a walkthrough anchor. At the end the build lists every PENDING marker, every
CAPTURE marker, and every empty result slot with their counts; exit code 0, or 1 with `--strict`
while any remain.

## Block format

The comment at the top of `deck.md` has the full reference. In short:

```text
## 19. Demo block: what to watch       number, a dot, the title
section: S1 Instructions                required, shown in the header
minutes: 8                              speaker timing
image: img/s1-watch.png                 a picture, path relative to this folder
live: `make show-1`: the primary verdict   shown as "Filled in live: ..."

- `make show-1`, finished: screen 1      3 to 6 bullets; `code` in backticks
- Screen 3: files read by category

notes:
Speaker notes until the next slide, with the run sheet section and the source.
```

Other fields: `layout:` (`default`, `title`, or `statement`), `subtitle:`, `image:` (path relative to
this folder), `slot:` (a result slot: `slot: name` while empty, `slot: name = value` or an image path
once filled), `code: <anchor id> <lines>` (lines of a walkthrough anchor from
`uv run python platform/scripts/anchors.py extract <id>`, for example `S4:filters 20-23,30-36`; left-out lines
show as `...`), `diagram: architecture now=L1,L2` (the recurring architecture diagram defined once at
the top of `deck.md`, with the named nodes drawn with a thick border and the word "now"), and inline
` ```mermaid ` blocks.

## Markers and live values

- A PENDING marker, written `PENDING: what | source: ... | how: ...` inside double square brackets:
  an open item; on a slide it shows as an amber box.
- A CAPTURE marker, written `CAPTURE: what | how: command` inside double square brackets: output, a
  time, or a cost that comes from a real run of the command named after `how:`. Replace the whole
  line with the captured text, labelled "captured on <date>, run <id>; your output will differ", and
  rebuild.
- `live: ...`: a value produced in class (a poll result, a show run's verdict, the final A/B). It shows
  as a grey "Filled in live" box and is never an open item.

The release build must report `open items: 0 PENDING markers ..., 0 CAPTURE markers, 0 empty result
slots`. Then copy `dist/deck.pdf` and `dist/deck.pptx` to this folder and commit them.

If code inside a walkthrough anchor changes, check the code slides: line numbers in `code:` count from
the first line inside the anchor.
