# Module 1: Harness Engineering for Coding Agents - Slides

The class deck has 80 slides for the 240-minute class. It follows the class plan: each section
launches its live run on its start slide, the one poll opens Section 4: Verification, and the breaks
come after Section 1: Instructions (10 minutes) and Section 3: Scope and sandbox (5 minutes).

| File | What it is |
|---|---|
| `module1-slides.md` | The source: each slide's text, layout, diagram, time, and speaker notes |
| `module1-deck.pptx` | The deck in PowerPoint, built from `module1-slides.md`, with the speaker notes |
| `module1-deck.pdf` | The same deck as a PDF, one page per slide |
| `outline.md` | The block table of the deck: slides and minutes per block |
| `img/` | Console screenshots from the timed runs, listed in the instructor run sheet |

## The source

`module1-slides.md` is the only place the slides are written. Each slide has a heading, then one
line with its block, its time, its diagram, and its layout, then the slide text and the speaker
notes. The Time fields add up to 240 minutes. Diagrams are pictures under `docs/diagrams/` and
`section-N-*/diagrams/`. The notes are written so the class can be taught from them alone.

## How the PowerPoint is built

The PowerPoint file is built from `module1-slides.md` with the course PowerPoint template, outside
this repository: each slide's layout field picks a template layout, the slide text and the diagram
go into it, and the notes become the speaker notes. The PDF is exported from the PowerPoint file.
When `module1-slides.md` changes, the deck is built again and both files here are replaced.

`make slides` prints where the deck is and points to this page; it builds nothing.

## How to view it

- Present: open `module1-deck.pptx` in PowerPoint, Keynote, or Google Slides, and use the
  presenter view to see the speaker notes.
- Read: open `module1-deck.pdf` in any PDF viewer.
- Read the notes in plain text: open `module1-slides.md`; the index at its top lists every slide.
