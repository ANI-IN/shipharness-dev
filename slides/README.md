# Slides

The Module 1 slides: 72 slides for the 240-minute class.

| File | What it is |
|---|---|
| `outline.md` | The plan: every slide by section, with timings, sources, and the result slots |
| `deck.md` | The deck source, one block per slide, built from the outline. Edit this file |
| `dist/` | Build output (`deck.html`, `deck.pdf`, `deck.pptx`, cached diagram PNGs); not tracked |

## Build

```bash
make slides                                   # validate, then write dist/deck.html, deck.pdf, deck.pptx
uv run python scripts/build_slides.py --check   # validate and list open items only (no browser)
make slides SLIDES_OPTS=--strict              # release check: fails while any open item remains
```

The build needs Playwright's Chromium (`uv run playwright install chromium`) and, the first time each
diagram is drawn, network access to load Mermaid 11.4.1 from cdn.jsdelivr.net. Diagram PNGs are cached
in `dist/diagrams/` by content hash, so later builds work offline until a diagram changes.

The HTML page is the layout engine: each slide is a 1280 x 720 page, and text that does not fit is
shrunk step by step. The PDF is printed from that page. The PPTX has native text boxes with the same
font sizes, diagrams as pictures, and the speaker notes (each starting with "Slide N of 72 | section |
minutes"). The build prints a warning for any slide whose text had to shrink below 22 px or still
overflows; shorten that slide.

Checks that stop the build (exit code 2): exactly 72 slides numbered 1 to 72 in order, a section on
every slide, at most 6 bullets and 12 code lines per slide, every image path present, every code
reference resolving to a walkthrough anchor. At the end the build lists every PENDING marker and every
empty result slot with its count; exit code 0, or 1 with `--strict` while any remain.

## Block format

The comment at the top of `deck.md` has the full reference. In short:

```text
## 20. Demo block: results           number, a dot, the title
section: S1 Instructions             required, shown in the header
minutes: 7                           speaker timing
slot: s1_experiment_dots             a result slot, empty until filled
live: tonight's two dots             shown as "Filled in live: ..."

- The A/B verdicts                   3 to 6 bullets; `code` in backticks
- Tonight's two dots next to the experiment dots

[[PENDING: S1 experiment dots ... | source: M8 batch 1 | how: make report]]

notes:
Speaker notes until the next slide, with the run sheet section and the source.
```

Other fields: `layout:` (`default`, `title`, or `statement`), `subtitle:`, `image:` (path relative to
this folder), `code: <anchor id> <lines>` (lines of a walkthrough anchor from
`uv run python scripts/anchors.py extract <id>`, for example `S4:filters 20-23,30-36`; left-out lines
show as `...`), `diagram: architecture now=L1,L2` (the recurring architecture diagram defined once at
the top of `deck.md`, with the named nodes drawn with a thick border and the word "now"), and inline
` ```mermaid ` blocks.

## Filling results

1. Put the value after the slot name: `slot: s1_experiment_dots = bare 3 of 10 failed, harness 0 of
   10`, or an image path such as `slot: s1_experiment_dots = images/s1-dots.png` (the picture then
   takes the visual area of the slide).
2. Delete the PENDING line that described it, on the slide or in the notes.
3. Run `make slides` and check the open-items count; `make slides SLIDES_OPTS=--strict` passes once it
   is zero.

If code inside a walkthrough anchor changes, check the code slides: line numbers in `code:` count from
the first line inside the anchor.
