# Structure and taste: reviewer checklist

Use this list to confirm that a module matches [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md).
Each item is a yes or no. The items marked (checker) are checked by
`platform/scripts/check_style.py --strict`, (lint) by `platform/scripts/lint_prose.py`, and (test)
by the module's own tests; read or run the rest yourself, as a first-time engineer.

## Structure

- [ ] The top level holds only `README.md`, `setup/`, the section folders, `final-project/`,
      `guide/`, `slides/`, `use-in-your-repo/`, `docs/`, `platform/`, and the root config files.
- [ ] Section folders are named `section-N-<slug>/`, in class order.
- [ ] Every section has `README.md`, `concepts.md`, `session-notes.md`, `demo/`, `assignment/`,
      `post-class-reading/`, and `diagrams/` with their required files (checker).
- [ ] `final-project/` has `README.md`, `run.sh`, `walkthrough.md`, `expected/`, `CHECKLIST.md`
      (checker).
- [ ] `docs/` has start-here, glossary, FAQ, costs, reference, evidence (index and one page per
      section), instructor guide, troubleshooting, architecture, and `STYLE.md`.
- [ ] `setup/` has an index, one page per system (Windows, macOS, Linux), and a pre-class list.
- [ ] `platform/config/` holds `course.toml`, `measures.toml`, and `release.toml`;
      `platform/before-class/` holds the before-class records.

## Pages

- [ ] Every page has the H2 headings of its template, in order (checker).
- [ ] Every README and setup page starts with "# Module N: <name>" (checker).
- [ ] Every teaching page opens with "**Illustrative scenario.**", a story with no numbers, then
      why it happens (cited), what the module does, and the how-to (checker for the label).
- [ ] One glossary box per page, with the same wording as the glossary (checker for one box).
- [ ] No template guidance comment is left on any page (checker).
- [ ] Sentences are short and plain; every less common term is spelled out on first use.
- [ ] Every claim has an example, a command, real output, or a linked source.
- [ ] Names follow "<Kind> N: <name>" on first mention; no bare codes (checker).
- [ ] Sources are cited by linked title and listed, numbered, at the end of the page (checker).
- [ ] Every link resolves and points at the right place (checker for relative links; open the
      external ones).
- [ ] Every diagram is an Excalidraw source with PNG and SVG renders, in the shared palette, labels
      at least 20 px when placed, with alt text and a caption (checker for source and alt text).
- [ ] No dated words: "today", "in class", "this session", or "this run" only (lint).

## Demos

- [ ] Each demo folder holds `run.sh`, the real files the demo uses, `walkthrough.md`, and real
      captured output in `expected/`, not images alone.
- [ ] Every class demo is a live run; any recording is labelled as recorded and used only as a
      fallback.
- [ ] `run.sh` states what it runs, the most it costs, and its measured time; it uses
      `set -euo pipefail`, works from any folder, and prints one readable line per step.
- [ ] Each demo was run three times against its time bar before class, and the times are on the
      evidence page.
- [ ] "If it fails" lists the three to five likely problems with exact fixes.

## Assignments

- [ ] "Try it yourself first..." sits right under the H1 (checker).
- [ ] `starter/` and `solution/` sit side by side; the solution is complete and works.
- [ ] `SOLUTION.md` walks through the approach, choices, alternatives, and common mistakes.
- [ ] The solution holds captured self-check output, one real live run, and the grade.
- [ ] Grading criteria add up to 100 points, each with how it is checked.
- [ ] Grader code and hidden tests are not in the public files.

## Slides

- [ ] Made from the program template; at most 80 slides; the class fits its time.
- [ ] Exactly one poll in the whole class.
- [ ] One DEMO slide per section, badge and title only, no screenshot.
- [ ] No "What just happened" slides.
- [ ] Text sits in styled boxes and cards with even spacing; titles are "lead: rest", at most 10
      words.
- [ ] Speaker notes let an instructor deliver each slide from the notes alone.
- [ ] The repository holds one deck, the owner's final file.

## Live console and dashboard

- [ ] The layout uses auto-fit grids, wrapping header and tab rows, `min-width: 0` on grid and
      flex children, rem fonts, and no fixed pixel widths or device-tuned media queries.
- [ ] The automated width sweep passed (for example 320 to 2560 CSS px in 40 px steps, two
      heights, pixel ratios 1 and 2, zoom 150% to 175%, a phone width): no horizontal overflow,
      nothing past the right edge or clipped, pills on one line, no mid-word breaks, the page
      scrolls to the bottom, back navigation works.
- [ ] A lighter sweep runs in CI.
- [ ] Someone looked at screenshots at the presenter's real display scaling.
- [ ] No fixed-height panel clips; long inner lists have a visible scrollbar, a minimum height, an
      expand toggle, and keyboard and wheel scrolling.
- [ ] Static assets carry a content hash in their URL and are served no-cache.
- [ ] A visible "back to all runs" control and keyboard shortcuts exist.
- [ ] The run list shows section, item, type, status, and start time, newest first, and lists a
      run from the moment it starts.
- [ ] Status words and labels are plain, with the internal code in brackets only where it links to
      logs; empty states hold no internal type names or paths.
- [ ] Anything that did not run says "Not run" with the reason, never "pending" or "none".
- [ ] Long identifiers sit on their own full-width row and break only at separators.
- [ ] Before-class records are always shown, labelled, next to new runs.
- [ ] Server logs show only warnings and errors unless the verbose flag is on.
- [ ] Each phase's outcome reads the same in the console and the terminal.

## Terminal and commands

- [ ] Terminal summaries are plain words, with no `key={...}` dumps.
- [ ] Make targets echo readable names; shell loops are hidden and each step prints one line.
- [ ] Every parser of human-readable output accepts the old and the new form, with a test for each
      (test).
- [ ] Every tool-reported line number quoted in a page is checked by a test (test).

## Honest results and measures

- [ ] Each section's headline measure was in `measures.toml` before the first comparison run.
- [ ] The demo's headline is that measure; every other result is labelled secondary.
- [ ] Any re-judging from stored data is disclosed on the evidence page.
- [ ] Every number names its file or its run; nothing is estimated (checker for placeholders).
- [ ] Results are counts, never percentages.
- [ ] "No measurable difference" is said plainly wherever it is the result.
- [ ] The cost of the approach and the known limitations are stated.
- [ ] No run was repeated for a nicer result, no run was picked or dropped, and no setting changed
      mid-comparison; any setting change is disclosed with its reason.
- [ ] Surprises are recorded, and the guide is written around what actually happened.
- [ ] Timings come only from runs that ran alone, as ranges over at least two runs, on one stated
      clock basis.
- [ ] Run ids, finding ids, and hashes appear only in the evidence pages, or in commands and
      terminal excerpts of the guide (checker).

## Demo guide

- [ ] `guide/` has a README (who it is for, what you need first, how to follow it, time and cost,
      the slides, build), Part 0, one chapter per section, the appendix, one PDF at a
      print-friendly size, and `source/` (checker for the README headings).
- [ ] Every step has Where, Type, You should see, Look at, What it means, Checkpoint, If it looks
      different, and Instructor note, in that order (checker).
- [ ] Every chapter ends with a result summary, the time and cost, and "What to say in class", and
      has an "If your run differs" step (checker for the headings).
- [ ] The appendix has a command cheat sheet, troubleshooting, a glossary, and the replay fallback
      (checker).
- [ ] Every command in the guide was run; commands have no prompt signs and no placeholders except
      values the reader supplies; no other machine's run id.
- [ ] Every number comes from the recorded live runs.
- [ ] Screenshots were captured at about 1024 CSS px at 2x scale; console text prints at 8 pt or
      more; crops are focused and include their headings.
- [ ] Callouts are in reading order and never cross; each was verified in code to point at its
      element; the numbered lists match the circles.
- [ ] Every alt text and caption was checked against its image and describes only what is visible.
- [ ] Host paths, user names, and account or workspace ids are masked; the PDF's text was scanned
      for keys, paths, account links, and placeholders.
- [ ] A fresh reviewer followed the guide live on a clean copy, as a learner and as an instructor,
      and every finding was fixed in one pass before the rebuild.
- [ ] Any replayed moment is labelled as recorded and shown at the same viewport as the live
      screenshots.

## Release and repository hygiene

- [ ] Every folder the tool writes in a learner's copy is git-ignored (test).
- [ ] Every public folder is in the release allow-list, and the style checker and the prose lint
      scan it (test).
- [ ] Private tooling and its tests are not in the release; tests name private paths as string
      literals.
- [ ] Fake keys in tests are built at runtime.
- [ ] Any redaction of graded reference answers or recorded evidence was checked against the
      graders that read it, and a grade change was decided explicitly.
- [ ] No empty placeholders, blank links, broken images, or empty code blocks (checker).
- [ ] No internal words, no dated words (checker, lint), no old or duplicate versions.
- [ ] Prose lint and `check-style --strict` report 0 errors and 0 warnings.
- [ ] The secret scan passed on the working tree and the full history before the push.
- [ ] The public repository has a single commit by the owner's identity, with no attribution lines.
- [ ] CI is green on the pushed commit.
- [ ] The release was verified from a fresh clone, following the tester checklist exactly.

## Building with agents

- [ ] The layout, naming, measures, solutions policy, demo format, release list, and slide process
      were written down before the first page.
- [ ] One shared brief file existed before the agents started, and every agent read it.
- [ ] Agents had disjoint write scopes, each in its own worktree and branch.
- [ ] The full suite ran once after all branches were merged, before the push.
- [ ] Every claim an agent reported was re-checked: checks re-run, images looked at.
- [ ] No more than the agreed number of heavy jobs ran at once, each slot with one owner.
- [ ] Every status report gave done, running, left, ETA, health, and a budget line.
