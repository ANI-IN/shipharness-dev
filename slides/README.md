# Module 1: Harness Engineering for Coding Agents - Slides

The slides for the 240-minute class: 72 slides. The PDF and the PowerPoint file in this folder are
ready to present. The rest of this page is for anyone who changes a slide and builds them again.

| File | What it is |
|---|---|
| `deck.pdf`, `deck.pptx` | The slides, ready to present; the PowerPoint file has the speaker notes |
| `deck.md` | The source of every slide, one block per slide. Edit this file |
| `outline.md` | The block table and the class plan per section |
| `img/` | Console screenshots from timed runs of the class commands |
| `dist/` | Build output (`deck.html`, `deck.pdf`, `deck.pptx`, cached diagram pictures); not tracked |

## Build

```bash
make slides
uv run python platform/scripts/build_slides.py --check
make slides SLIDES_OPTS=--strict
cp slides/dist/deck.pdf slides/dist/deck.pptx slides/
```

The first command checks the deck, then writes `dist/deck.html`, `dist/deck.pdf`, and
`dist/deck.pptx`. The second only checks the deck and lists open items; it needs no browser. The
third is the release check: it fails while any open item remains. After a clean strict build, the
fourth copies the two files into this folder.

The build needs Playwright's Chromium (`uv run playwright install chromium`). The first time each
diagram is drawn, it also needs network access to load Mermaid 11.4.1 from cdn.jsdelivr.net. Diagram
pictures are cached in `dist/diagrams/` by content, so later builds work offline until a diagram
changes.

### If the build fails

| What you see | Cause | Fix |
|---|---|---|
| `x Chromium did not start ...` or `x playwright is not installed: ...`, exit 3 | Chromium is missing | `uv run playwright install chromium`, then `make slides` |
| `x browser step failed: ...`, exit 3, while a new diagram is drawn | Mermaid cannot load from the network | Connect and rerun; cached diagrams need no network |
| `x slide N (line L): ...`, then `nothing built`, exit 2 | A slide breaks a rule listed below | Fix that slide; `--check` repeats the check |
| `! slide N: text still overflows ...` | Too much text for one slide | Shorten the bullets, or move detail to the notes |
| `x --strict: open items remain`, exit 1 | A marker or an empty result slot is left | The report above that line lists each one |

The HTML page is the layout engine. Each slide is a 1280 x 720 page, and text that does not fit is
shrunk step by step. The PDF is printed from that page. The PowerPoint file has text boxes with the
same font sizes, diagrams as pictures, and the speaker notes. Each note starts with "Slide N of 72",
the section, and the minutes. The build warns about any slide whose text had to shrink below 22 px.

The build stops (exit 2) unless: there are exactly 72 slides, numbered 1 to 72 in order; every slide
has a section; no slide has more than 6 bullets or 12 code lines; every image path exists; and every
code reference resolves to a walkthrough anchor.

## Block format

The comment at the top of `deck.md` has the full reference. One slide looks like this:

```markdown
## 19. Demo block: what to watch
section: S1 Instructions
minutes: 8
image: img/s1-watch.png
live: `make show-1`: the primary verdict

- Screen 1: build turns, test phase, the verdict
- Screen 3: files read by category

notes:
Speaker notes until the next slide.
```

The first line is the number, a dot, and the title. `section:` is required and shows in the header.
`minutes:` is the speaker timing. `image:` is a path relative to this folder. `live:` is a value
produced in class; it shows as a grey "Filled in live" box. Bullets start with `- `; use 3 to 6.

Other fields: `layout:` (`default`, `title`, or `statement`), `subtitle:`, `slot:` (a result slot),
`code:` (lines of a walkthrough anchor, for example `code: S4:filters 20-23,30-36`; left-out lines
show as `...`), `diagram: architecture now=L1,L2` (the architecture diagram defined once at the top
of `deck.md`, with the named parts drawn thick and marked "now"), and inline Mermaid blocks.

## Open items

An open item is a marker that a slide is not finished: either a missing piece, or output still to
be copied in from a real run. Each is written inside double square brackets; the comment at the top
of `deck.md` shows the form. The strict build fails while any open item or empty result slot
remains. The released slides have none.

If code inside a walkthrough anchor changes, check the code slides: the line numbers in `code:` count
from the first line inside the anchor.
