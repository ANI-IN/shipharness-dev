# Structure and taste: how a module of this program looks and feels

This guide captures the structure and the taste of Module 1, so every later module (the next one is
"Loop Engineering for Coding Agents") looks and feels the same. The rules are project-agnostic.
Module 1's project and topic appear only in the quoted examples, each marked with the file it comes
from. Read it with its checklist, [STRUCTURE-AND-TASTE-CHECKLIST.md](STRUCTURE-AND-TASTE-CHECKLIST.md),
and generate the empty skeleton with `scripts/new_module.py` ([README](README.md)).

The rules come from four places: the style guide and its checker (`docs/STYLE.md`,
`platform/scripts/check_style.py`), the finished pages, the owner's instructions over the build
(`instructor/engineering-notes/focus-2026-10-17.md`, `overnight-final-2026-10-18.md`), and the
slide rules (scratchpad `slides-md/NAMING-FINAL.md`, `ROUND3.md`, `SPEC.md`, and
`tpl/template-analysis.md`). Where the owner changed a rule during the build, the later rule is the
one written here.

---

## 1. Structure

### 1.1 The course-first layout

The top level holds the course, in the order a learner meets it, and one folder for the code. The
owner asked for exactly this after an earlier, cluttered layout:

> Restructure the public layout to: README.md, setup/, 01-instructions/, 02-state-lifecycle/,
> 03-scope-sandbox/, 04-verification/, final-project/, slides/, use-in-your-repo/ (kit + 4 skills +
> guide), docs/ (...), platform/ (...), plus Makefile, pyproject.toml, uv.lock, LICENSE, .env.example.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 12)

The section folders were later named `section-N-<slug>/`, which is the form to use.

| Folder | What it holds |
|---|---|
| `README.md` | The module's front page: problem, why, approach, class plan, results, quick start |
| `setup/` | `README.md` (index), `windows.md`, `macos.md`, `linux.md`, `pre-class.md` |
| `section-N-<slug>/` | One folder per section, in class order (below) |
| `final-project/` | `README.md`, `run.sh`, `walkthrough.md`, `expected/`, `CHECKLIST.md` |
| `slides/` | The class deck (one PowerPoint file) and a short `README.md` |
| `use-in-your-repo/` | The kit, the skills, and the step-by-step guide for a learner's own repository |
| `docs/` | Start here, glossary, FAQ, costs, reference, evidence, instructor guide, troubleshooting, architecture, `STYLE.md`, `diagrams/`, `images/` |
| `platform/` | All code: the tool, the project the module works on, config, scripts, tests |

Root files besides the README: `Makefile`, `pyproject.toml`, `uv.lock`, `.python-version`,
`.env.example`, `LICENSE`, `SECURITY.md`, `.gitignore`, `.github/workflows/`. Nothing else.

Every section folder has the same parts. The checker enforces them (SC19):

```text
section-N-<slug>/
  README.md              the section's front page
  concepts.md            the idea, taught in 15 minutes
  session-notes.md       what class showed, questions, what to try next
  demo/
    README.md            the page learners follow
    run.sh               the one command that runs the live demo
    walkthrough.md       the 30 to 40 lines of code that matter, explained
    <files>/             the real files the demo uses (Module 1: harness/)
    expected/            real output and screenshots from a real run
  assignment/
    README.md            story, what you build, steps, grading, solution walkthrough
    SPEC.md              the detailed, testable requirements
    starter/             the learner's working files
    solution/            the complete reference solution, side by side, with SOLUTION.md
  post-class-reading/    README.md index and one file per reading
  diagrams/              README.md, and per diagram .excalidraw + .png + .svg
```

Example of the folder rule as the checker states it:

```python
# platform/scripts/check_style.py (lines 424-438)
SECTION_ITEMS = (
    "README.md",
    "concepts.md",
    "session-notes.md",
    "demo/README.md",
    "demo/run.sh",
    "demo/walkthrough.md",
    "demo/harness/",
    "demo/expected/",
    "assignment/README.md",
    "assignment/SPEC.md",
    "assignment/starter/",
    "assignment/solution/SOLUTION.md",
    "post-class-reading/",
)
```

What each `docs/` page is for:

| Page | What it holds |
|---|---|
| `start-here.md` | The learning path in order, with a reading and run time per step |
| `glossary.md` | Every term and abbreviation, one plain line each; the "<Kind> N: <name>" names first |
| `faq.md` | Ten to fifteen real questions, answered from the repository |
| `costs.md` | Each command and assignment: most at the caps, and measured cost |
| `reference.md` | Make targets, variables, caps, folders, each with the file it comes from |
| `evidence.md`, `evidence/` | The only pages with run ids, finding ids, hashes, and capture details |
| `instructor-guide.md` | A one-page class-day cheat sheet first, then the details |
| `troubleshooting.md` | Exact error lines, cause, fix, per area |
| `architecture.md` | The big picture, one run step by step, packages, files on disk |
| `STYLE.md` | The rules and templates in this guide, for the module's own repository |

### 1.2 Page templates

Each page type has a fixed list of H2 headings, in order; a closing `## Sources` may follow any of
them. The checker compares every page with its template (SC16). The generated skeleton holds these
headings with a guide comment under each.

**Root README** (at most 250 lines): The problem, Why it happens, The approach, The class plan,
What we measured, Quick start, Where next.

- The problem: one story that covers the whole module, one failure per section, then what each
  costs. No "Illustrative scenario" label on this page only.
- Why it happens: one numbered cause per failure, each with a quoted, linked source.
- The approach: one diagram, two sentences per section.
- The class plan: a table of section, what you see, time; the breaks.
- What we measured: one small table of counts, the plain verdict, the cost, a "Known limitations"
  list, a link to the evidence index.
- Quick start: exactly five commands, then a link to `setup/`.
- Where next: Section 1, setup, use-in-your-repo, and "Getting help".

Example (`README.md`, The problem):

> Your team gives a week of tickets on a multi-tenant issue tracker to a coding agent. On Monday the
> agent copies an old handler that has no tenant filter. The tests pass, and one customer can now
> read another customer's issues. On Tuesday a session stops halfway through a database migration.

**Section README** (at most 120 lines): The problem, Why it happens, How this section fixes it, How
to work through this section, Where next. The last-but-one part is a table of the parts in order
(concepts, demo, walkthrough, assignment, reading, session notes) with what each gives and when.

Example (`section-1-instructions/README.md`, How to work through this section):

> | [concepts.md](concepts.md) | The idea, how it works, what the course measured | Minutes 2-20 |
> | [demo/](demo/README.md) | The live run of the harness arm, and how to read it | Launch at minute 1; review at 30-46 |

**Concepts** (fits 15 minutes live, at most about 1,800 words): The problem, The idea in one
sentence, How it works, How <project> does it, What we measured, When it helps and when it does
not, Key takeaways (exactly 3), Check your understanding (3 to 5 questions, answers in details
blocks), Further reading.

Example (`section-1-instructions/concepts.md`, The idea in one sentence):

> Give the agent a short map that is always in its context and points to focused documents and
> skills, which it opens only when the task needs them.

**Demo README** (at most 250 lines): The problem, What you'll see, Run it, What to watch, What the
result means, If it fails. "Run it" ends with a "Files and links" list: `run.sh`, `walkthrough.md`,
the files folder, `expected/` (the fallback), the section's evidence page.

**Walkthrough**: What this code does, The code, explained (one H3 per excerpt, "<file>, lines
a-b"), If you copy this into your repo. 30 to 40 code lines in total.

Example (`section-1-instructions/demo/walkthrough.md`, What this code does):

> The instructions layer talks to the runner through three hooks. Before the run, it copies the map,
> the docs, and the skill into the workspace. At the start of each session, it hands over the context
> prefix: the map and the skills catalogue. After each tool call, it reports which of its files the
> agent opened.

**`run.sh`**: a comment block (what it runs, the most it costs, how long it takes, from dated
measured runs), `set -euo pipefail`, works from any folder, clear `x` error lines, non-zero exit on
failure.

Example (`section-1-instructions/demo/run.sh`, lines 12-16):

```bash
# Cost: at most $0.24, the per-arm cap ($0.20) plus the per-review cap ($0.04); the caps are set in
# platform/src/shipharness/config/settings.py and .env.example. Three runs, measured 2026-10-18
# with the class profile, cost $0.021 to $0.023 each.
# Time: in those runs the primary verdict came 2:57 to 6:18 after launch and the full verdict 7:23 to
# 10:58; the command ends a few seconds after the full verdict
```

**Assignment README** (at most 250 lines): the line "Try it yourself first. The full solution is
in ./solution/ with a step-by-step walkthrough." right under the H1, then The problem, What you'll
build (one diagram, one paragraph), Step by step (each step: what to do, the command, "Check:"),
Grading criteria (100 points) (criterion, what earns the points, points, checked by), Solution
walkthrough.

**SPEC.md**: Inputs, Files you must produce, Requirements (numbered, testable), Self-check, Evidence
to hand in, Limits.

**SOLUTION.md**: The approach step by step, Design choices and why, Alternatives considered,
Common mistakes this avoids, Run and verify it, Evidence.

Example (`section-1-instructions/assignment/solution/SOLUTION.md`, The approach):

> 2. **Write the checker first, test first.** The visible tests failed against the starter stubs (12 of
>    15). The checker was then written until they passed, and it ran after every document of the split.
>    A split without a check is a guess.

**Post-class reading index**: Readings (reading, reading time, why read it), How to use these.
**Each reading**: "Reading time: about N minutes." and a "Source:" line under the H1, then Why it
matters, Three key ideas (exactly 3, 2 to 4 sentences each), Apply it to your repo.

Example (`section-1-instructions/post-class-reading/01-map-not-manual.md`):

> 1. **On disk is not in context.** "From the agent’s point of view, anything it can’t access in-context
>    while running effectively doesn’t exist." A rule works only if it is in the repository and also
>    reaches the agent's context while it works.

**Session notes** (at most 150 lines): What we showed, Key ideas, What the result showed, Questions
from class, What to try next.

**Setup index**: What you will install, Pick your system, Get help. **Setup per system**: Before
you start, Steps, Common errors, You're ready. Each step is "### Step N: <what you do>" with five
parts in order: **Why.**, **Do this.**, **You should see.**, **Check it worked.**, **If it fails.**

Example (`setup/windows.md`, Step 7):

> **Check it worked.** In the new terminal, `uv --version` prints the version:
>
> ```text
> uv 0.13.1 (x86_64-unknown-linux-gnu)
> ```
>
> **If it fails.** `uv: command not found` means the terminal started before the install: open a new
> one. If it persists, check that `~/.local/bin/uv` exists.

**Instructor guide**: Class-day cheat sheet (at most 60 lines: timeline, console keys, three
commands if a demo stalls, who to call), The day before, Thirty minutes before, Section by section,
If something breaks, After class.

Example (`docs/instructor-guide.md`, cheat sheet):

> | Time | Terminal | Command | What you should see |
> |---|---|---|---|
> | T-30 min | B | `make doctor` | Last line `result: + ready` |
> | 0:11 | B | `make show-1` | Section 1: Instructions, harness in action |

**Reference**: Make targets, Settings and variables, Caps and limits, Folders. **Evidence page**:
How to use this page, Results, Captures, Sources and findings, Commits and tags. **Final project
README**: the demo README headings plus "Use it on your own repository".

Every page that teaches also carries one glossary box at the end of "The problem", and the first
paragraph of "The problem" starts with **Illustrative scenario.** (SC17, SC18).

---

## 2. Taste: what the owner liked (do this)

### 2.1 Problem first

Open every teaching page with a concrete situation an engineer recognises, then why it happens
(cited), then what the module does about it, then exactly how. The scenario is a story with no
numbers.

> Every README starts with the problem, not the lesson: (1) The problem: a concrete situation an
> engineer recognises, what goes wrong, what it costs; (2) Why it happens (cited); (3) What we do
> about it (the harness piece); (4) Then the detailed how-to
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 10)

Example (`section-1-instructions/README.md`):

> **Illustrative scenario.** You ask a coding agent to add an org-wide issue search to a multi-tenant
> tracker. The tenant rule is written down, deep in a long handbook. The agent finds a legacy list
> handler that predates the rule.

### 2.2 Detailed, specific writing for software engineers

Show the mechanism: the real file, the real command, the real output, the trade-off. Plain words,
short sentences (25 words or fewer), "you", active voice, paragraphs of at most 5 lines. Every claim
has an example, a command, real output, or a cited source.

> Concrete over general: every claim has an example, a command, real output, or a cited source.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 4)

Example (`section-1-instructions/demo/README.md`):

> In it, `F1` is the org-wide issue search, and `r1_new_violations` counts new violations
> of the tenant isolation rule. The run id and the running totals are cut where marked; the full
> capture is in [expected/terminal.txt](expected/terminal.txt):

### 2.3 Excalidraw whiteboard diagrams

One style for every diagram: an Excalidraw source, a 2x PNG for slides, an SVG for pages, a fixed
1920 by 1080 canvas on a light panel, one palette with fixed meanings, labels of at least 20 px when
placed on a slide, step frames for build-ups, alt text and a caption, and never colour alone. The
checker requires the `.excalidraw` source next to every render (SC20).

Example (`docs/diagrams/README.md`):

> | Grey `#78909C` | The bare arm |
> | Blue `#3896D2` | The harness arm, and the parts of the harness |
> | Amber `#FFAB40` | What to notice: a done claim, a question |
> | Red `#E46962` | A "no": a block, a revert, a failure |
>
> Each panel is a fixed canvas: 1920 by 1080 for the 16:9 diagrams, placed at 80% of the slide width
> (...). At that size every label shows at 20 px or more on a 1080p slide.

Build-up frames: "Each frame adds one element, and every frame has the same size, so the picture
does not jump between slides" (same file).

### 2.4 Demo folders with the working piece, and live demos only

A demo folder holds the files that do the work, the one command, the code explained, and the real
captured output; not pictures alone. Every class demo is a live run. A recording exists only as a
labelled emergency fallback.

> Every demo section in the class uses only live model runs (...). Scripted constructed examples
> (`make example-N`) and recorded showcases/replays are NOT part of any demo section.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 7)

Example (`docs/STYLE.md`, demo folder): "`harness/`: exact copies of the files the agent receives in
this section, with no course text added. A check keeps them identical to the files the harness
really places."

### 2.5 Assignments with starter and full solution side by side

`starter/` and `solution/` sit next to each other; the solution is complete and working, with a
step-by-step `SOLUTION.md`, captured self-check output, one real captured live run, and the grade.
The grader code and hidden tests stay private.

> Structure per assignment: `0N-*/assignment/starter/` (learner work) and `0N-*/assignment/solution/`
> (complete reference solution), side by side.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 14)

### 2.6 Naming, sources, glossary

Everything a learner can see is named "<Kind> <number>: <name>" on first mention, then "<Kind>
<number>". Sources are numbered per page, cited by linked title in prose, and listed at the end.
Every term is in the glossary, with the same wording in every page's glossary box.

> Format everywhere (repo, slides, speaker notes, console labels, CLI messages, kit, skills, harness
> files): "<Kind> <number>: <name>". Full form on first use per page/slide; "Feature 4", "House rule 1",
> "Source 2" after that. Never bare F4, R1, S1, A1, B11.
>
> (scratchpad `slides-md/NAMING-FINAL.md`)

Example (`section-1-instructions/README.md`, Sources):

> - Source 1: Harness engineering: leveraging Codex in an agent-first world, <https://openai.com/index/harness-engineering/>, Ryan Lopopolo (OpenAI), 2026-02-11

### 2.7 Honest results

Results are counts ("0 of 3"), never percentages. Say "no measurable difference" plainly when that
is the result, show what the approach costs, list known limitations, and never pick runs, edit
captured output, or change a measure after the fact.

> The harness doesn't have to win; every result is reported as measured.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 4)

Example (`README.md`, What we measured):

> | 1: no new tenant leak | 7 of 7 | 7 of 7 | No measurable difference |
> | 3, confirmation on a second ticket | 0 of 3 | 3 of 3 | Harness ahead |
> | 4: every hidden test and mutant | 0 of 4 | 0 of 4 | Both fail |

### 2.8 First-time setup, start-here, FAQ, costs, limitations

Setup assumes nothing is installed: one page per system, every step with why, the command, the
expected output, a check, and a fix. A start-here page gives the path with times; a FAQ answers the
real questions; a costs page gives both the cap and the measured cost; the README lists known
limitations.

> First-time install, very detailed: setup/ assumes nothing is installed. Separate pages for Windows
> (WSL2 + Ubuntu + Docker Engine), macOS, Linux. (...) Each step: why, the exact command or click
> path, what you should see, how to check it worked, the common errors and fixes.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 12)

Example (`docs/costs.md`):

> | Command | At most, at the caps | Measured on the course machine |
> |---|---|---|
> | `make show-1` | $0.24 | $0.021 to $0.023 |

Example (`README.md`, Known limitations): "**One model.** Every run used gpt-6-luna for the agent
and gpt-5.6-luna for the reviewer. Another model may behave differently."

### 2.9 Slides

Use the program's PowerPoint template. At most 80 slides for a 240-minute class. Exactly one poll
in the whole class. One live DEMO slide per section, with the badge and title only. Text sits in
styled containers (key-idea box, quote cards, step cards, two-column cards, icon rows) with even,
content-based spacing. Speaker notes let an instructor deliver from the notes alone. The owner
makes the final deck from the reviewed slide Markdown; the repository holds that one deck.

> Maximum 80 slides in total. (...) NO "What just happened" slides anywhere. (...) Exactly ONE Live
> Zoom Poll in the whole session (...). Styled containers, not plain bullet lists (...). Spacing based
> on content: distribute boxes evenly in the available space.
>
> (scratchpad `slides-md/ROUND3.md`)

Template rules that carry over (scratchpad `tpl/template-analysis.md`): titles "Blue lead: white
rest" of at most 10 words; 5 to 30 words on a content slide, 127 the ceiling; a numbered series of
one idea per slide closed by a "Cheat Sheet:" slide; build-ups of 2 to 3 steps on a fixed frame;
fixed wording for DEMO, Q&A, Break, and Poll slides.

Example of a DEMO slide (scratchpad `slides-md/module1-slides.md`, slide 29):

> **On the slide:**
> DEMO - 1
> Section 1 - Implementation Notes: The map at work
> **Visual:** Template DEMO layout: "DEMO - 1" badge and the title only; no screenshot. Switch to the console.

Its notes then give the exact files, which screen to show when, what to say for a pass and for a
fail, and the fallback.

### 2.10 A clean public repository

One fresh commit, only the owner's identity, no attribution lines, CI green on the pushed commit,
every link working, and the release checked from a fresh clone.

> Only ANI-IN as contributor, in every repo: Every commit's author and committer is ANI-IN (...).
> No Co-authored-by trailers, no bot commits, no attribution lines anywhere in history or files.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 10)

Example (`VERIFICATION.md`): "Fresh clone: 1 commit, 877 files, `uv sync --frozen` ok".

---

## 3. Taste: what the owner rejected (never do this)

### 3.1 AI slop and audit-log pages

No vague, generic, or filler text. No page that reads like a log of what was done. No ids or codes
in learner text, no unexplained abbreviations, no internal jargon.

> I reviewed the RC: the content is accurate but reads like an audit log, not teaching material.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 14)

The style guide's own "Not this" example (`docs/STYLE.md`, rule 5):

> A1 reports that agents copy patterns (A1, F-a-NN); see run ab-20261016-181736-a07558.
> In S1 you hand in A1. Section 1 checks R1, the tenant rule.

Internal words to avoid (`docs/STYLE.md`, rule 6): "owner scope", "class host", "build repository",
"not a make target in this release", `PENDING` or `CAPTURE` markers, milestone codes, "generated
when released". The prose lint bans a list of filler words and emoji; the list is in
`platform/scripts/lint_prose.py`.

### 3.2 Picture-only demos, fake live demos, extra polls, recap slides

No demo folder with only images. No recorded or scripted run presented as live. No poll per
section. No "What just happened" slides. No screenshots on DEMO slides.

> `make replay` stays emergency fallback only (RECORDING badge).
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 7)

> 2 SLIDES: max 80; ONE poll (final-feature poll in Section 4); no "What just happened"; one live
> DEMO per section, no screenshots
>
> (`instructor/engineering-notes/overnight-final-2026-10-18.md`)

### 3.3 Empty placeholders, broken things, dated words, stale copies

No blank values, empty links, broken images, empty code blocks, or code blocks with only a
comment. No words that only make sense on the day they were written ("tonight", "this release"). No
old or duplicate versions left in the repository.

> Fix the defects I found: blank "captured on , run ;" placeholders; empty output blocks (...); broken
> screen-1 final image; REFERENCES.md "generated when released" contradictions
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 14)

Example of removing duplicates (`slides/README.md`): "It is the only deck for the 240-minute class,
with 75 slides." (commit message: "Slides: the owner's deck is the only deck; remove the earlier
versions and the slide build").

### 3.4 Clutter, silent waits, late changes

No cluttered top level. No long waits without a word: run independent work in parallel and report
when a stage ends. No changing a settled decision late: decide layout, naming, and formats at the
start.

> Don't wait between steps; start every independent task as soon as its inputs are ready.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 7)

The cost of late changes in Module 1: the section folders moved twice (into `01-instructions`
in the restructure, then to `section-1-instructions`, scratchpad `slides-md/SPEC.md`), the naming
format was set in the last night (`overnight-final-2026-10-18.md`, item 1), and every page was
rewritten after the release candidate (message 14).

---

## 4. Process: how to build a module efficiently

### 4.1 Decide at the start

Write these down before the first page, in the module's engineering notes, and do not reopen them
without the owner:

| Decision | Module 1's final answer |
|---|---|
| Layout | Course first: `setup/`, `section-N-<slug>/`, `final-project/`, `slides/`, `use-in-your-repo/`, `docs/`, `platform/` |
| Naming | "<Kind> N: <name>", the exact names in the config and the glossary |
| Solutions policy | Public, side by side with the starter; graders and hidden tests private |
| Demo format | Live only, one command per demo, captured run in `expected/` as the fallback |
| Slide process | Slide Markdown from the template rules, owner review, owner makes the deck |

`scripts/new_module.py` writes the layout, the templates, and `platform/config/course.toml` with the
names, so these decisions are fixed in files from the first commit.

### 4.2 Stop points

Stop and wait for the owner only at these points:

1. **Project and sections approval**: the project the module builds on, the section list, and each
   section's failure story.
2. **Design approval**: the measures, the demo per section, and the time bar for each demo.
3. **Slide Markdown review**: the full slide Markdown with notes, before any deck is built.
4. **Publish**: the release candidate, tested from a fresh clone, before the public push.

> Only stop for: publishing, deleting or renaming repos, spending beyond the budget, or anything that
> would change a primary measure.
>
> (`instructor/engineering-notes/focus-2026-10-17.md`, message 5)

Between stop points, answer your own questions with the existing rules, record the decision and
the reason, and continue.

### 4.3 Working rules

- **Pilot the demos early.** Run every demo live as soon as it exists, not in the last night.
- **At most two heavy jobs at once on this laptop** (containers, test suites, renders).
  "Max two heavy jobs. If WSL hangs, restart, verify repo, resume."
  (`overnight-final-2026-10-18.md`)
- **Reports in chat only, each with a budget line**: build spend and what is left, pilot runs and
  money, traces. "Budget line in every report. Reports in chat only." (message 4)
- **Use the fast test suite while iterating**; run the full suite and the container tests once at
  the end (message 7).

### 4.4 Lessons from Module 1

1. **Measure every demo three times against a time bar before class.** "each demo 3x live (...).
   Pass = all 3: no ERROR, primary verdict <= ~6 min, full <= ~15 min" (`overnight-final-2026-10-18.md`,
   item 9). Fix until all three pass, then keep one good run as the recorded fallback.
2. **Keep every timing dated, with its range over the runs.** Example (`docs/start-here.md`): "Run
   times are the range over three runs of each command, measured 2026-10-18 with the class
   profile".
3. **Disclose any setting change** on the evidence page, with the date and the reason, and keep
   both arms of a comparison identical. Example (`docs/evidence/general.md`): "Harness time limit
   raised for the class profile (2026-10-18)".
4. **Run the secret scan before every push**, over the working tree and the full history
   (`overnight-final-2026-10-18.md`, limits).
5. **Verify the release from a fresh clone**: clone it, sync, run the fast suite, and walk the
   tester checklist exactly as written (`VERIFICATION.md`, release candidate).
6. **CI green on the pushed commit is the bar, not a local pass.** Reproduce CI conditions locally
   first (no colour, fixed terminal width). "A local pass is not enough." (message 11)
7. **Never invent a number.** Every number names its file or its run; a missing number is captured,
   never estimated (`docs/STYLE.md`, rule 7).
8. **Write the style checker on day one** and run `check-style --strict` and the prose lint before
   every commit, so pages never drift into the defects listed in section 3.
9. **A golden sample first.** Finish one section completely, have it reviewed, then apply the same
   shape to the others in parallel (message 14).
10. **Fresh reviewers.** Have a reviewer that wrote none of the pages read every page as a
    first-time engineer before the release candidate (message 13).
