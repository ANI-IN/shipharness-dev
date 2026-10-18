# Slides: the template and how a deck is built

One deck per class, in PowerPoint, with the speaker notes inside it. This folder holds what you
need to build one the same way:

| File | What it is |
|---|---|
| `template.pptx` | The design (masters, layouts, theme, fonts) and seven example slides with notes. |
| `outline-template.md` | The outline a writer fills in, per section, before building slides. |
| `slide-review.md` | How to produce a read-only change list for a deck after the repo changes. |
| `scripts/extract_deck.py` | Extracts the text and notes of any .pptx to Markdown. |
| `scripts/make_template.py` | Rebuilds `template.pptx` from a copy of a finished deck. |

## Use the template

1. Copy `template.pptx` to `slides/<COURSE>.pptx` in the course repo.
2. Fill in `outline-template.md` first; a slide exists only when the outline has a row for it.
3. Duplicate the example slide that matches each outline row (title, section divider, concept,
   diagram, demo, result table) and replace every `<PLACEHOLDER>`. Keep the layouts; do not
   restyle a slide by hand.
4. Delete the seven examples when the deck is done. `extract_deck.py` on the finished deck must
   show no `<...>` placeholder left.

## Slide structure per section

Each section of the class follows the same arc, in this order:

1. **Agenda** with the section highlighted.
2. **Failure story:** one illustrative ticket, told in three to five beats, ending in the harm.
3. **The question:** the tempting fix as a yes/no question to the room, then the verdict in a
   "KEY IDEA" box.
4. **Concepts, numbered 1) to 4):** one slide each: a title "N) name: what it does", a
   one-sentence subtitle, a diagram or bullets, and a "Key idea:" line at the bottom.
5. **Cheat sheet:** the section's four moves on one slide, to refer back to.
6. **Demo:** "Section N: <name> - Implementation Notes: <demo title>", with the console screens to
   walk, in order.
7. **Questions**, then a **break** or a **poll** where the timing needs one.

The class opens with the title, the instructor, how the class runs, setup checks, a recap, and
the problem statement (what is built, why it matters, how it is measured, a glossary). It closes
with the final demo, all results on one slide, "which piece when", how to use it in your own
repo, the final project, a one-picture summary, takeaways, references, and questions.

## Speaker-note conventions

- **Line 1 is always the timing:** `Time: <minutes> min (<start>-<end>)`, clock times from the
  class start (0:00). The times of all slides add up to the class length.
- **Then what to say, in order.** Quotes carry their source number and link:
  `Source 2: <title> (<link>): "<quote>"`.
- **Point at:** what the room should look at, and in which order (a box on the slide, a screen
  number and callout on the console).
- **Demo slides** list the files for the demo, which browser tab and terminal to use, when the
  run was launched, the screens to walk in order, and the fallback (the captured run).
- **Likely questions** with one-line answers and where in the repo the answer lives.
- **Transition:** the sentence that leads to the next slide.
- **"Re-check after live runs:"** on every slide that states a number or a result a live run can
  change. Before each class, walk these lines against the evidence pages.

## Naming rules on slides

- Plain names first: "Section 2: State and sessions", "Assignment 1: Instructions". Internal
  codes (S2, A1) appear only in brackets, and only where a reader needs them to find a file.
- The first mention of a named kind on a slide uses the full "<Kind> N: <name>" form.
- File paths are written as they are in the repo, in monospace, so a learner can open them.
- No people's names, run ids, or dates on slides; examples are labelled "illustrative".

## Slides never contradict the repo

The repository is the source of truth: the code, the docs, the evidence pages. A slide that
disagrees with the repo is wrong, even if the repo changed after the slide was written. After
any change to the repo that a slide mentions (a file name, a count, a command, a result), run
the review in `slide-review.md` and update the deck. Never edit a deck someone else is editing:
hand them the change list instead.

## The template file

`template.pptx` was made with `scripts/make_template.py` from a copy of a finished deck: all
slides removed, masters, layouts, theme, and embedded fonts kept, layout texts blanked, the
thumbnail and comment authors dropped, and seven example slides added (title, section divider,
concept, diagram placeholder, demo with a "console screen N" placeholder, result table, and a
"what to say" notes example). To use your organization's design, run the script on a copy of
one of your decks.
