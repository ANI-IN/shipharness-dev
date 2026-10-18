# Course style guide

This page is for anyone who writes or edits a page of {{MODULE_TITLE}}. Every public page follows
it. It has two parts: the rules that apply to every page, and one template per document type.

Two scripts check what a machine can check. Run both before you commit:

```bash
make check-style
uv run python platform/scripts/lint_prose.py
```

`make check-style` runs `platform/scripts/check_style.py`; `--list-checks` lists every check.
Errors fail the check. Length limits, template headings, the scenario label, the glossary box,
and template guidance left on a page are warnings; they fail with `make check-style-strict`, which
must pass before anything is published. Everything specific to this module (the title, the
section names, the named kinds, the codes, the id patterns, the source register) is in
`platform/config/course.toml`.

If a line must break a rule, for example to quote real output, end it with an allow marker: the
check id, then the reason. A marker on its own line, right before a fenced block, covers the whole
block:

```markdown
A quoted output line <!-- check-style: allow SC08 quoted terminal output -->
```

Public course files are `README.md`, `setup/`, the section folders, `final-project/`,
`slides/README.md`, `use-in-your-repo/`, `guide/`, and `docs/`. Agent files (the real files a demo gives an
agent, in each `demo/{{DEMO_FILES}}/` folder; skills; kit templates) follow their own format; only
the image rules and the id rules apply to them.

Folder rules (checked on a full run): every section folder has `README.md`, `concepts.md`,
`session-notes.md`, `demo/` (`README.md`, `run.sh`, `walkthrough.md`, `{{DEMO_FILES}}/`,
`expected/`), `assignment/` (`README.md`, `SPEC.md`, `starter/`, `solution/SOLUTION.md`),
`post-class-reading/README.md`, and `diagrams/README.md` once it has a `diagrams/` folder.
`final-project/` has `README.md`, `run.sh`, `walkthrough.md`, `expected/`, and `CHECKLIST.md`.
Every `.png` or `.svg` in a `diagrams/` folder has an `.excalidraw` source with the same name.

---

## Rules for every page

### 1. Title line

Every `README.md` and every setup page starts with the module title as its only H1. The root
README uses exactly `# {{MODULE_TITLE}}`. Other READMEs and setup pages add the page name after a
spaced hyphen, such as `# {{MODULE_TITLE}} - Setup on Windows`. Other pages have one H1 with their
own name.

### 2. Problem first

Pages that teach (section READMEs, concepts, demo READMEs, assignment READMEs, the final project)
open with `## The problem`. Its first paragraph starts with the label **Illustrative scenario.**
and tells a short work story an engineer recognises. The root README tells its story without the
label. Each section uses its own failure. The scenario holds no numbers: it is a story, not a
measurement. After it come why it happens (cited), what the module does about it (and that the
course measures whether it helps), and then the how-to.

### 3. Plain short sentences

- One idea per sentence. Aim for 25 words or fewer.
- Write to the reader as "you". Use the active voice and the present tense.
- Say what happens, not what something "allows" or "enables".
- Use the source's own words for its ideas.
- Report results as counts ("0 of 3 runs"), never as percentages.
- Short paragraphs: at most 5 lines.
- Standard terms (API, CI, HTTP, JSON, SQL) need no explanation. Spell out any less common term on
  first use on each page, in a few plain words. Every such term is in the
  [glossary](glossary.md), one line each, in alphabetical order.

### 4. One glossary box per page

Each page defines the course terms it uses once, in one box at the end of `## The problem` (or
right after the H1 on pages without that section). Use the same wording for a term on every page.
Do not write sentences about labels.

```markdown
> **Terms on this page**
>
> - **Term**: one plain sentence, the same on every page.
```

### 5. Evidence stays in the evidence pages, and names follow one format

Run ids, finding ids, source ids, and commit hashes appear only in the evidence pages:
`docs/evidence.md` (the index) and the files under `docs/evidence/`.

Sections, assignments, and any other named kind are written "<Kind> N: <name>". The first mention
on a page is the full form; later mentions use the short form "Section 2". Plurals such as
"Sections 1 to 4" are not mentions. The exact names are in `platform/config/course.toml`.

- Never a bare code such as `S1` or `A2` in prose, headings, link text, tables, or HTML comments.
  Code spans, fenced code, and commands are identifiers and are not read.
- Commands use readable aliases, not codes.
- Other codes a learner can see go in a code span with a plain-words explanation, or are left out.
- Cite a source by its linked title. Every mention of a source's title is a link to it; after the
  first citation you may write "Source 2". A page that cites a source ends with a `## Sources`
  list, numbered in the order the page first cites each source, one entry per source:

  ```markdown
  ## Sources

  - Source 1: Full title of the article, <https://example.org/article>, Author (Publisher), 2026-01-01
  ```

  URLs, titles, authors, and dates come from the source register, never from memory.
- A link always has text and a target. Every relative link resolves.
- Captured terminal output is real output: it is not edited.

### 6. No internal language

Words from how the course was built mean nothing to learners: "owner scope", "the owner's",
"class host", "build repository", "this release", "brief", "lead" (as a role), milestone codes,
`PENDING` or `CAPTURE` markers, "generated when released", "(private)", and the dated words of
rule 15. Say who does it ("you", "the instructor"), give the command to run, or cut the sentence.

### 7. No invented numbers

Every number comes from a file in this repository (name the file) or a real run listed in an
evidence page. Do not estimate times or costs. Caps are stated as caps, with their variable name in
`.env.example`. If a number is missing, run the command and capture it. Never commit a placeholder.

### 8. One "your output will differ" note per page

A page with captured output or screenshots has exactly one note, right before the first captured
block or image:

```markdown
> Your output will differ: run times, ids, and wording change on every run.
```

### 9. Consistent headings

One H1 per page. H2 headings are exactly the ones in the page's template, in that order, plus an
optional last `## Sources`. H3 headings are free; never deeper than H3. Sentence case, no numbers
in headings, except setup steps ("Step 3: Install git").

### 10. Tables

At most 4 columns, short cells, no ids. Split a wider table or use a list.

### 11. Images with captions

Screenshots are real, from real runs, stored in the repository: section screenshots in
`section-N-*/demo/expected/`, shared ones in `docs/images/`. File names are lowercase with hyphens.
Each image stands on its own line with alt text, then a blank line, then an italic caption that
says what to notice. Alt text says what the image shows, never a file name or one word such as
"image". Colour never carries meaning alone. The one remote image allowed is the CI status badge.

### 12. Code blocks

Commands go in `bash` blocks, captured output in `text` blocks. A diagram is a small labelled
`mermaid` block or an Excalidraw SVG from a `diagrams/` folder. Code excerpts come from real files;
the first line is a comment with the path and line numbers; at most 40 lines. Never leave a block
empty or holding only a comment.

### 13. Links

Use relative links between course pages. Clone commands use the real repository URL.

### 14. Template guidance

Pages generated from the module skeleton hold HTML comments that start with `guide:` and say what
goes in each part. They never show on GitHub, and the checker reports each one as a warning until
the part is written and the comment deleted.

### 15. No dated words

Write "today", "in class", "this session", or "this run". Words that only make sense on the day
they were written fail the prose lint: "tonight", "tomorrow", "yesterday", "last night". <!-- lint-prose: allow -->

### 16. Plain labels, in pages and on screen

A result reads in plain words, with the internal code in brackets only where a reader must
connect it to a log: "Files outside the allowed paths (`diff_scope`)". The console, the terminal
summaries, and the pages use the same words for the same outcome, phase by phase. Something that
did not run says so ("Not run"), never "pending" or "none".

### 17. The Live Demo Guide

`guide/` holds the step-by-step guide to every live demo: its README, Part 0, one chapter per
section, and the appendix. Every step has the same fields and boxes, in order (the checker reports
a gap as SC28); `guide/source/CONVENTIONS.md` lists them. Every command was really run and every
number comes from a recorded live run. In `guide/` only, a run id may stand in a command or a
terminal excerpt, never in prose.

---

## Templates

Each skeleton lists the exact H2 headings that `check_style.py` expects.

### Root README (`README.md`), at most 250 lines

```markdown skeleton:root-readme
# {{MODULE_TITLE}}
## The problem
## Why it happens
## The approach
## The class plan
## What we measured
## Quick start
## Where next
```

### Section README (`section-N-*/README.md`), at most 120 lines

```markdown skeleton:section-readme
# {{MODULE_TITLE}} - Section N: Name
## The problem
## Why it happens
## How this section fixes it
## How to work through this section
## Where next
```

### Concepts (`section-N-*/concepts.md`), at most about 1,800 words

```markdown skeleton:concepts
# Section N: Name. Concepts
## The problem
## The idea in one sentence
## How it works
## How {{PROJECT}} does it
## What we measured
## When it helps, and when it does not
## Key takeaways
## Check your understanding
## Further reading
```

Key takeaways holds exactly 3 bullets; each check question has its answer in a details block.

### Demo folder (`section-N-*/demo/`)

| File | What it holds |
|---|---|
| `run.sh` | The one command that runs the live demo |
| `{{DEMO_FILES}}/` | The real files this demo uses |
| `walkthrough.md` | The 30 to 40 lines of code that matter, explained |
| `expected/` | Real output and screenshots from a real run |
| `README.md` | The page learners follow |

`run.sh` starts with a comment block (what it runs, the most it costs, how long it takes from
measured runs), uses `set -euo pipefail`, works from any folder, and exits non-zero on failure.

```markdown skeleton:walkthrough
# Demo N walkthrough: Name
## What this code does
## The code, explained
## If you copy this into your repo
```

```markdown skeleton:demo-readme
# {{MODULE_TITLE}} - Demo N: Name
## The problem
## What you'll see
## Run it
## What to watch
## What the result means
## If it fails
```

### Final project README (`final-project/README.md`)

```markdown skeleton:final-project
# {{MODULE_TITLE}} - Final project
## The problem
## What you'll see
## Run it
## What to watch
## What the result means
## If it fails
## Use it on your own repository
```

### Assignment folder (`section-N-*/assignment/`)

The README's line right under the H1 is "Try it yourself first. The full solution is in
`./solution/` with a step-by-step walkthrough.", with `./solution/` linked to the folder.

```markdown skeleton:assignment-readme
# {{MODULE_TITLE}} - Assignment N: Name
## The problem
## What you'll build
## Step by step
## Grading criteria (100 points)
## Solution walkthrough
```

```markdown skeleton:spec
# Assignment N: Name. Specification
## Inputs
## Files you must produce
## Requirements
## Self-check
## Evidence to hand in
## Limits
```

`starter/` holds the learner's files and a README that says which to edit. `solution/` holds the
complete working files side by side with it, the captured self-check output, one real captured
live run, and the grader score. Grader code and hidden tests are not in the course files.

```markdown skeleton:solution
# Assignment N: Name. Solution
## The approach, step by step
## Design choices and why
## Alternatives considered
## Common mistakes this avoids
## Run and verify it
## Evidence
```

### Post-class reading (`section-N-*/post-class-reading/`)

```markdown skeleton:reading-index
# {{MODULE_TITLE}} - Reading list for Section N: Name
## Readings
## How to use these
```

Each reading file, `NN-short-name.md`, has "Reading time: about N minutes." and a "Source: " line
under its H1:

```markdown skeleton:reading
# Title of the source
## Why it matters
## Three key ideas
## Apply it to your repo
```

### Session notes (`section-N-*/session-notes.md`), at most 150 lines

```markdown skeleton:session-notes
# Section N: Name. Session notes
## What we showed
## Key ideas
## What the result showed
## Questions from class
## What to try next
```

### Setup pages (`setup/`)

```markdown skeleton:setup-index
# {{MODULE_TITLE}} - Setup
## What you will install
## Pick your system
## Get help
```

```markdown skeleton:setup-os
# {{MODULE_TITLE}} - Setup on System
## Before you start
## Steps
## Common errors
## You're ready
```

Each step is an H3 "Step N: what you do" with five parts in order: **Why.**, **Do this.**, **You
should see.**, **Check it worked.**, **If it fails.**

### Instructor guide (`docs/instructor-guide.md`), cheat sheet at most 60 lines

```markdown skeleton:instructor-guide
# Instructor guide
## Class-day cheat sheet
## The day before
## Thirty minutes before
## Section by section
## If something breaks
## After class
```

### Reference (`docs/reference.md`)

```markdown skeleton:reference
# Reference
## Make targets
## Settings and variables
## Caps and limits
## Folders
```

### Evidence (`docs/evidence/`)

```markdown skeleton:evidence
# Evidence: Part name
## How to use this page
## Results
## Captures
## Sources and findings
## Commits and tags
```

### Live Demo Guide (`guide/`)

```markdown skeleton:guide-readme
# {{MODULE_TITLE}} - Live Demo Guide
## Who it is for
## What you need first
## How to follow it
## Time and cost
## The slides
## Build the PDF
```

Each chapter (`guide/chapters/N-*.md`) is its steps, then:

```markdown skeleton:guide-chapter
# Chapter N: Section N: Name
## Result summary
## Time and cost
## What to say in class
```

```markdown skeleton:guide-appendix
# Appendix: Cheat sheet, troubleshooting, glossary and fallback
## Command cheat sheet
## Troubleshooting
## Glossary
## Fallback: replay a recorded run
```
