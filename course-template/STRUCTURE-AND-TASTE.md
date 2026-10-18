# Structure and taste: how a course module looks and feels

This guide sets the structure and the taste of a hands-on technical course module: one with live
demos, a results console or dashboard, assignments with graders, and a public release built from
a private development repository. The rules hold for any project and any topic. Read it with its
checklist, [STRUCTURE-AND-TASTE-CHECKLIST.md](STRUCTURE-AND-TASTE-CHECKLIST.md), and generate the
empty skeleton with [scripts/new_module.py](scripts/new_module.py) ([README](README.md)).

The rules come from building and teaching a full module: the style guide and its checker, the
finished pages, the course owner's instructions over the build, the slide reviews, and what broke
in rehearsal and in class. Where a rule changed during the build, the later rule is the one
written here. The examples are illustrative; replace them with your module's own.

The kit around this guide:

| Folder | What it gives you |
|---|---|
| [skeleton/](skeleton/) | The empty module the generator renders, with its checker, prose lint, and CI |
| [skills/](skills/) | Agent Skills for building a course: a section, a demo guide, a slide outline |
| [playbooks/](playbooks/) | The shared brief, prompt templates for agent teams, and report formats |
| [slides/](slides/) | The slide template, the outline template, speaker-note rules, the slide review |
| [tools/](tools/) | The guide PDF builder, screenshot and callout tools, the layout sweep, the release build, the secret scan |

---

## 1. Structure

### 1.1 The course-first layout

The top level holds the course, in the order a learner meets it, and one folder for the code.
Decide it before the first page; every later move costs a rewrite of every link.

| Folder | What it holds |
|---|---|
| `README.md` | The module's front page: problem, why, approach, class plan, results, quick start |
| `setup/` | `README.md` (index), `windows.md`, `macos.md`, `linux.md`, `pre-class.md` |
| `section-N-<slug>/` | One folder per section, in class order (below) |
| `final-project/` | `README.md`, `run.sh`, `walkthrough.md`, `expected/`, `CHECKLIST.md` |
| `guide/` | The Live Demo Guide: README, Part 0, one chapter per section, appendix, one PDF, build sources |
| `slides/` | The class deck (one file) and a short `README.md` |
| `use-in-your-repo/` | The kit, the skills, and the step-by-step guide for a learner's own repository |
| `docs/` | Start here, glossary, FAQ, costs, reference, evidence, instructor guide, troubleshooting, architecture, `STYLE.md`, `diagrams/`, `images/` |
| `platform/` | All code: the tool, the project the module works on, config, scripts, tests, before-class records |

Root files besides the README: `Makefile`, `pyproject.toml`, the lock file, `.python-version`,
`.env.example`, `LICENSE`, `SECURITY.md`, `.gitignore`, `.github/workflows/`. Nothing else.

Every section folder has the same parts, and the checker enforces them:

```text
section-N-<slug>/
  README.md              the section's front page
  concepts.md            the idea, taught in 15 minutes
  session-notes.md       what class showed, questions, what to try next
  demo/
    README.md            the page learners follow
    run.sh               the one command that runs the live demo
    walkthrough.md       the 30 to 40 lines of code that matter, explained
    <files>/             the real files the demo uses
    expected/            real output and screenshots from a real run
  assignment/
    README.md            story, what you build, steps, grading, solution walkthrough
    SPEC.md              the detailed, testable requirements
    starter/             the learner's working files
    solution/            the complete reference solution, side by side, with SOLUTION.md
  post-class-reading/    README.md index and one file per reading
  diagrams/              README.md, and per diagram .excalidraw + .png + .svg
```

Files in `platform/config/` fix the decisions in files from the first commit:

| File | What it fixes |
|---|---|
| `course.toml` | The module title, section names, named kinds, codes, id patterns, sources |
| `measures.toml` | Each section's headline measure, secondary measures, and demo time bar, written before the first comparison run |
| `release.toml` | The paths the public release includes and excludes, and the folders the checkers scan |

`platform/before-class/` holds the results recorded before class, which the console shows next to
every new run.

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
them. The checker compares every page with its template. The generated skeleton holds these
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
- Where next: Section 1, setup, use-in-your-repo, the Live Demo Guide, and "Getting help".

**Section README** (at most 120 lines): The problem, Why it happens, How this section fixes it, How
to work through this section, Where next. The last-but-one part is a table of the parts in order
(concepts, demo, walkthrough, assignment, reading, session notes) with what each gives and when.

**Concepts** (fits 15 minutes live, at most about 1,800 words): The problem, The idea in one
sentence, How it works, How <project> does it, What we measured, When it helps and when it does
not, Key takeaways (exactly 3), Check your understanding (3 to 5 questions, answers in details
blocks), Further reading.

**Demo README** (at most 250 lines): The problem, What you'll see, Run it, What to watch, What the
result means, If it fails. "Run it" ends with a "Files and links" list: `run.sh`, `walkthrough.md`,
the files folder, `expected/` (the fallback), the section's evidence page, the guide's chapter.

**Walkthrough**: What this code does, The code, explained (one H3 per excerpt, "<file>, lines
a-b"), If you copy this into your repo. 30 to 40 code lines in total.

**`run.sh`**: a comment block (what it runs, the most it costs, how long it takes, from measured
runs that ran alone), `set -euo pipefail`, works from any folder, one readable line per step,
clear `x` error lines, non-zero exit on failure.

**Assignment README** (at most 250 lines): the line "Try it yourself first. The full solution is
in ./solution/ with a step-by-step walkthrough." right under the H1, then The problem, What you'll
build (one diagram, one paragraph), Step by step (each step: what to do, the command, "Check:"),
Grading criteria (100 points) (criterion, what earns the points, points, checked by), Solution
walkthrough.

**SPEC.md**: Inputs, Files you must produce, Requirements (numbered, testable), Self-check, Evidence
to hand in, Limits.

**SOLUTION.md**: The approach step by step, Design choices and why, Alternatives considered,
Common mistakes this avoids, Run and verify it, Evidence.

**Post-class reading index**: Readings (reading, reading time, why read it), How to use these.
**Each reading**: "Reading time: about N minutes." and a "Source:" line under the H1, then Why it
matters, Three key ideas (exactly 3, 2 to 4 sentences each), Apply it to your repo.

**Session notes** (at most 150 lines): What we showed, Key ideas, What the result showed, Questions
from class, What to try next.

**Setup index**: What you will install, Pick your system, Get help. **Setup per system**: Before
you start, Steps, Common errors, You're ready. Each step is "### Step N: <what you do>" with five
parts in order: **Why.**, **Do this.**, **You should see.**, **Check it worked.**, **If it fails.**

**Instructor guide**: Class-day cheat sheet (at most 60 lines: timeline, console keys, three
commands if a demo stalls, who to call), The day before, Thirty minutes before, Section by section,
If something breaks, After class.

**Reference**: Make targets, Settings and variables, Caps and limits, Folders. **Evidence page**:
How to use this page, Results, Captures, Sources and findings, Commits and tags. **Final project
README**: the demo README headings plus "Use it on your own repository".

**Live Demo Guide**: the README, the chapters, and the appendix have their own templates
(section 7).

Every page that teaches also carries one glossary box at the end of "The problem", and the first
paragraph of "The problem" starts with **Illustrative scenario.**

Example of a scenario (illustrative):

> **Illustrative scenario.** You ask a coding agent to add a search across every customer's
> records. The rule that keeps customers apart is written down, deep in a long handbook. The agent
> finds an old handler that predates the rule, and copies it.

---

## 2. Taste: what the owner liked (do this)

### 2.1 Problem first

Open every teaching page with a concrete situation an engineer recognises, then why it happens
(cited), then what the module does about it, then exactly how. The scenario is a story with no
numbers.

### 2.2 Detailed, specific writing for software engineers

Show the mechanism: the real file, the real command, the real output, the trade-off. Plain words,
short sentences (25 words or fewer), "you", active voice, paragraphs of at most 5 lines. Every claim
has an example, a command, real output, or a cited source.

### 2.3 Excalidraw whiteboard diagrams

One style for every diagram: an Excalidraw source, a 2x PNG for slides, an SVG for pages, a fixed
1920 by 1080 canvas on a light panel, one palette with fixed meanings (for example grey for the
control arm, blue for the approach under test, amber for what to notice, red for a block or a
failure), labels of at least 20 px when placed on a slide, step frames of the same size for
build-ups, alt text and a caption, and never colour alone. The checker requires the `.excalidraw`
source next to every render.

### 2.4 Demo folders with the working piece, and live demos only

A demo folder holds the files that do the work, the one command, the code explained, and the real
captured output; not pictures alone. Every class demo is a live run. A recording exists only as a
labelled fallback (section 7.5).

### 2.5 Assignments with starter and full solution side by side

`starter/` and `solution/` sit next to each other; the solution is complete and working, with a
step-by-step `SOLUTION.md`, captured self-check output, one real captured live run, and the grade.
The grader code and hidden tests stay private.

### 2.6 Naming, sources, glossary

Everything a learner can see is named "<Kind> <number>: <name>" on first mention, then "<Kind>
<number>": in pages, slides, speaker notes, console labels, and command output. Never a bare code.
Sources are numbered per page, cited by linked title in prose, and listed at the end. Every term
is in the glossary, with the same wording in every page's glossary box.

### 2.7 First-time setup, start-here, FAQ, costs, limitations

Setup assumes nothing is installed: one page per system, every step with why, the command, the
expected output, a check, and a fix. A start-here page gives the path with times; a FAQ answers the
real questions; a costs page gives both the cap and the measured cost; the README lists known
limitations.

### 2.8 Slides

Use the program's slide template ([slides/](slides/)). At most 80 slides for a 240-minute class.
Exactly one poll in the whole class. One live DEMO slide per section, with the badge and title
only. Text sits in styled containers (key-idea box, quote cards, step cards, two-column cards,
icon rows) with even, content-based spacing. Speaker notes let an instructor deliver from the notes
alone. The owner makes the final deck from the reviewed slide outline; the repository holds that
one deck.

Template rules: titles "lead: rest" of at most 10 words; 5 to 30 words on a content slide; a
numbered series of one idea per slide closed by a cheat-sheet slide; build-ups of 2 to 3 steps on a
fixed frame; fixed wording for DEMO, Q&A, Break, and Poll slides. A DEMO slide's notes give the
exact files, which screen to show when, what to say for a pass and for a fail, and the fallback.

---

## 3. Taste: what the owner rejected (never do this)

### 3.1 AI slop and audit-log pages

No vague, generic, or filler text. No page that reads like a log of what was done. No ids or codes
in learner text, no unexplained abbreviations, no internal jargon ("owner scope", "build
repository", "this release", milestone codes, `PENDING` markers, "generated when released"). The
prose lint bans a list of filler words and emoji.

Not this:

> A1 reports that agents copy patterns (A1, F-a-12); see the run in the log. In S1 you hand in A1.

### 3.2 Picture-only demos, fake live demos, extra polls, recap slides

No demo folder with only images. No recorded or scripted run presented as live. No poll per
section. No "What just happened" slides. No screenshots on DEMO slides.

### 3.3 Empty placeholders, broken things, dated words, stale copies

No blank values, empty links, broken images, empty code blocks, or code blocks with only a
comment. No words that only make sense on the day they were written: write "today", "in class",
"this session", or "this run", never "tonight"; the prose lint enforces the list. No old or <!-- lint-prose: allow -->
duplicate versions left in the repository: one deck, one PDF.

### 3.4 Clutter, silent waits, late changes

No cluttered top level. No long waits without a word: run independent work in parallel and report
when a stage ends. No changing a settled decision late: decide layout, naming, measures, and
formats at the start. Each late move of a folder or a name costs a rewrite of every page, slide,
and link.

---

## 4. Live console and dashboard

The results console is on the projector for most of the class. Build it for every screen, and
check it the way the class will see it.

### 4.1 A fluid layout that fits every screen

- Fit any width, resolution, display scaling, and browser zoom: auto-fit grids, header and tab
  rows that wrap, `min-width: 0` on every grid and flex child, no fixed pixel widths.
- Fonts in rem, readable on a projector. No media queries tuned to particular devices.
- The page scrolls naturally. No fixed-height panel that clips. A long inner list keeps a visible
  scrollbar, a minimum height, and an expand toggle, and scrolls by keyboard and wheel.
- Long identifiers get their own full-width row in tables and break only at separators, never
  mid-word.
- Version static assets (a content hash in the URL, served no-cache), so a browser never mixes an
  old stylesheet with new pages.

### 4.2 Verify with a sweep, then with your eyes

- Run an automated continuous width sweep ([tools/](tools/)): for example 320 to 2560 CSS px in
  40 px steps, two heights, device pixel ratios 1 and 2, browser zoom 150% to 175%, and a phone
  width.
- At every size: no horizontal overflow, nothing past the right edge, nothing clipped, status
  pills on one line, no mid-word breaks in identifiers, the page scrolls to the bottom, and back
  navigation works.
- Run a lighter sweep in CI.
- A person looks at screenshots at the presenter's real display scaling too. An automated sweep
  once passed while the real laptop at 150% overflowed.

### 4.3 Plain words on screen

- A visible "back to all runs" control and keyboard shortcuts.
- Plain status words ("finished", not "event 12").
- Plain labels, with the internal code in brackets where people must connect them to logs:
  "Files outside the allowed paths (`diff_scope`)". No bare codes in prose.
- Empty states in plain words, with no internal type names or paths.
- Never show results for something that did not run: "Not run (single-arm demo)", not "pending"
  or "none".
- Where a process has several phases, report the outcome per phase, in the same words in every
  view, console and terminal alike: "done (build) · not done (test phase)". Two views that
  summarise differently confuse instructors.

### 4.4 The run list and before-class records

- The run list shows section, item, type, status, and start time, newest first.
- A run is listed from the moment it starts: write its start metadata before work begins, not
  only at the end.
- Show the before-class records always, labelled, with new runs next to them.
- Server logs are quiet by default (warnings and errors only), with a verbose flag.

---

## 5. Terminal and commands

- Terminal summaries are plain words, not `key={...}` dumps.
- Make targets echo readable names. Hide shell loops (`@` recipes) and print one clear line per
  step.
- When human-readable output changes, every parser of it (graders, checkers, scripts) accepts both
  the old and the new form, with a test for each. A changed summary line once broke two assignment
  checkers.
- A page that quotes a tool-reported line number (such as `make: *** [Makefile:N: target]`) has a
  test that checks the number against the file.

---

## 6. Honest results and measures

### 6.1 Measures are fixed before the runs

- Pre-register the headline measure of each section in `platform/config/measures.toml`, before the
  first comparison run.
- The demo's headline is that measure. Every other result is labelled secondary.
- If a measure was applied wrongly, you may re-judge from stored data with no new model calls.
  Disclose it on the evidence page.

### 6.2 Report what happened

- Results are counts ("0 of 3"), never percentages.
- Say "no measurable difference" plainly when that is the result; show what the approach costs;
  list known limitations.
- Never re-run to get a nicer result, never pick or drop runs, never edit captured output, and
  never change settings mid-comparison. Both arms of a comparison use the same settings.
- Record surprises, such as the control arm behaving well, and write the guide around what
  actually happened, with an "If your run differs" step.
- Disclose any setting change on the evidence page, with the reason.

Example of a results table (illustrative):

> | Measure | Control | With the approach | Verdict |
> |---|---|---|---|
> | No new rule violation (headline) | 7 of 7 | 7 of 7 | No measurable difference |
> | Every hidden test passes (secondary) | 0 of 4 | 0 of 4 | Both fail |

### 6.3 Timings

- Take timings only from runs that ran alone; paired runs slow each other.
- Give ranges over at least two runs.
- State the clock basis (from launch, or from the first event) and use one basis everywhere.
- Measure every demo three times against its time bar before class; fix until all three pass.

### 6.4 Never invent a number

Every number names its file or its run; a missing number is captured, never estimated.

---

## 7. Demo guide

The Live Demo Guide is a step-by-step PDF that an instructor runs the class from, and a learner
repeats the demos with. Build it with the guide builder from [tools/](tools/); the
[skills/](skills/) folder has a skill for writing a chapter.

### 7.1 The folder

`guide/` is its own top-level folder:

- `README.md`: Who it is for, What you need first, How to follow it, Time and cost, The slides
  (a pointer to the deck), Build the PDF.
- `part0.md` (Before you start), `chapters/` (one per section), `appendix.md` (command cheat
  sheet, troubleshooting, glossary, fallback).
- One copy of the PDF, at a print-friendly size, and the build sources in `source/`, with
  `source/CONVENTIONS.md`.

### 7.2 The step template

Every step has the same fields and boxes, in this order:

| Field | What it holds |
|---|---|
| Where | Which terminal or screen, and which folder |
| Type | The copy-ready command, with no prompt sign, or the key or click |
| You should see | The real output or a screenshot from the recorded run |
| Look at | The one line or element to read |
| What it means | What it tells you, in plain words |
| Checkpoint | One thing to confirm before going on |
| If it looks different | One to three lines, each "cause → fix" |
| Instructor note | What to point at and what to say |

Each chapter ends with a result summary table, the time and cost, and "What to say in class".
The skeleton's checker reports a step with a missing or misplaced field.

### 7.3 Every command run, every number recorded

- Every command in the guide was actually run.
- Every number comes from the recorded live runs.
- No placeholders in commands, except a value the reader supplies. Never another machine's run id
  in a copy-ready command.

### 7.4 Screenshots and callouts

- Capture at a narrower CSS viewport (about 1024 px at 2x scale), so console text prints at 8 pt
  or more on a printed page.
- Prefer focused crops that include their headings over full windows or tall strips.
- Place callouts in reading order, never crossing. Verify in code that each points at the element
  holding its named text. Numbered lists match the circles.
- Alt text and captions describe only what is visible in the frame. Check each against the image;
  claims about a part that is cut off are the most common error.
- The screenshot and callout tools are in [tools/](tools/).

### 7.5 Live first, a labelled replay as the fallback

When a later moment depends on a live event, capture it live. If it cannot be captured, replay the
recorded log at the same viewport, labelled as recorded.

### 7.6 Redact, then scan

- Redact host paths, user names, and account or workspace ids. Mask dashboard URLs before capture
  and scan the page text before saving.
- Scan the PDF's text for keys, paths, account links, and placeholders before publishing.

### 7.7 A fresh reviewer, live

A reviewer with no context follows the guide on a clean copy, live: first as a learner, then as an
instructor. Fix every finding in one pass, then rebuild once.

---

## 8. Release and repository hygiene

### 8.1 The learner's copy stays clean

- Git-ignore every folder the tool writes in a learner's copy, with a test that lists them.

### 8.2 The release is an allow-list

- The public release is built from the private repository by an allow-list (`release.toml`; the
  release-build pattern is in [tools/](tools/)).
- Each new public folder joins the allow-list, with a test. The style checker and the prose lint
  scan it too: a moved folder once fell out of the checks silently.
- Private tooling and its tests stay out of the release. Test helpers name private paths as string
  literals, so the release build's excluded-test detection sees them.

### 8.3 Secrets and recorded evidence

- Build fake keys in tests at runtime, so secret scanners do not flag them.
- Run the secret scan ([tools/](tools/)) over the tree and the full history before every push.
- Before redacting anything in graded reference answers or recorded evidence, check which graders
  read it. A redaction that changes a reference grade is a results change: decide it explicitly.

### 8.4 The public repository

- One fresh commit, only the owner's identity, no attribution lines.
- CI green on the pushed commit is the bar, not a local pass. Reproduce CI conditions locally
  first (no colour, fixed terminal width).
- Every link works, and the release is verified from a fresh clone: clone, sync, run the fast
  suite, and walk the tester checklist exactly as written.

---

## 9. Process: building with agents

### 9.1 Decide at the start

Write these down before the first page and do not reopen them without the owner:

| Decision | Write down |
|---|---|
| Layout | Course first, as in section 1.1, including `guide/` |
| Naming | "<Kind> N: <name>", the exact names in `course.toml` and the glossary |
| Measures | The headline and secondary measures per section, and each demo's time bar, in `measures.toml` |
| Solutions policy | Public, side by side with the starter; graders and hidden tests private |
| Demo format | Live only, one command per demo, a captured run in `expected/` and a labelled replay as the fallback |
| Release | The allow-list in `release.toml` |
| Slide process | Slide outline from the template rules, owner review, owner makes the deck |

`scripts/new_module.py` writes the layout, the templates, `course.toml`, `measures.toml`, and
`release.toml`, so these decisions are fixed in files from the first commit.

### 9.2 Stop points

Stop and wait for the owner only at these points:

1. **Project and sections approval**: the project the module builds on, the section list, and each
   section's failure story.
2. **Design approval**: the measures, the demo per section, and the time bar for each demo.
3. **Slide outline review**: the full slide outline with notes, before any deck is built.
4. **Publish**: the release candidate, tested from a fresh clone, before the public push.

Also stop before deleting or renaming repositories, spending beyond the budget, or anything that
would change a headline measure. Between stop points, answer your own questions with the existing
rules, record the decision and the reason, and continue.

### 9.3 Parallel agents

- Split work into agents with disjoint write scopes, each in its own git worktree and branch.
- Write one shared brief file first ([playbooks/](playbooks/)): environment, rules, the folder
  contract, and conventions fixed up front. Every agent reads it before starting.
- The lead merges, runs the full suite once, and pushes.
- After merging branches, run the full suite: combined branches break tests that passed
  separately.
- Verify agents' claims: re-run the checks they report and look at the images they made. Stale
  reports happen.

### 9.4 Heavy jobs on one machine

- Run at most a fixed number of heavy jobs (live runs, containers, full test suites) at once on a
  laptop, and give each heavy slot one owner.
- Use the fast test suite while iterating; run the full suite and the container tests once at the
  end.
- Pilot every demo live as soon as it exists, not in the last session before class.

### 9.5 Reports

- A status report is a few lines: done, running, left, ETA, health.
- Every report has a budget line: build spend and what is left, pilot runs and their cost.
- Reports go in chat unless a page is asked for.
- When time is short, give agents hard deadlines with the priority order.

### 9.6 Working habits

1. **A golden sample first.** Finish one section completely, have it reviewed, then apply the same
   shape to the others in parallel.
2. **Write the style checker on day one** and run the strict check and the prose lint before every
   commit, so pages never drift into the defects in section 3.
3. **Fresh reviewers.** A reviewer that wrote none of the pages reads every page as a first-time
   engineer before the release candidate.
4. **Keep the kit current.** When a build teaches a new rule, add it here, to the checklist, and to
   the skeleton, with a test.
