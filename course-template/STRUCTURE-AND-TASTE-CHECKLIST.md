# Structure and taste: reviewer checklist

Use this list to confirm that a module matches [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md).
Each item is a yes or no. The items marked (checker) are checked by
`platform/scripts/check_style.py --strict` in the module's repository; read the rest as a
first-time engineer.

## Structure

- [ ] The top level holds only `README.md`, `setup/`, the section folders, `final-project/`,
      `slides/`, `use-in-your-repo/`, `docs/`, `platform/`, and the root config files.
- [ ] Section folders are named `section-N-<slug>/`, in class order.
- [ ] Every section has `README.md`, `concepts.md`, `session-notes.md`, `demo/`, `assignment/`,
      `post-class-reading/`, and `diagrams/` with their required files (checker).
- [ ] `final-project/` has `README.md`, `run.sh`, `walkthrough.md`, `expected/`, `CHECKLIST.md`
      (checker).
- [ ] `docs/` has start-here, glossary, FAQ, costs, reference, evidence (index and one page per
      section), instructor guide, troubleshooting, architecture, and `STYLE.md`.
- [ ] `setup/` has an index, one page per system (Windows, macOS, Linux), and a pre-class list.

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

## Demos

- [ ] Each demo folder holds `run.sh`, the real files the demo uses, `walkthrough.md`, and real
      captured output in `expected/`, not images alone.
- [ ] Every class demo is a live run; any recording is labelled as recorded and used only as a
      fallback.
- [ ] `run.sh` states what it runs, the most it costs, and its dated measured time; it uses
      `set -euo pipefail` and works from any folder.
- [ ] Each demo was run three times against its time bar before class, and the times are on the
      evidence page with the date.
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

## Honesty

- [ ] Every number names its file or its run; nothing is estimated (checker for placeholders).
- [ ] Results are counts, never percentages.
- [ ] "No measurable difference" is said plainly wherever it is the result.
- [ ] The cost of the approach and the known limitations are stated.
- [ ] Any setting change is disclosed with its date and reason; both arms of a comparison use the
      same settings.
- [ ] Run ids, finding ids, and hashes appear only in the evidence pages (checker).

## Repo hygiene

- [ ] No empty placeholders, blank links, broken images, or empty code blocks (checker).
- [ ] No internal words, no dated words such as "tonight" (checker), no old or duplicate versions.
- [ ] Prose lint and `check-style --strict` report 0 errors and 0 warnings.
- [ ] The secret scan passed on the working tree and the full history before the push.
- [ ] The public repository has a single commit by the owner's identity, with no attribution lines.
- [ ] CI is green on the pushed commit.
- [ ] The release was verified from a fresh clone, following the tester checklist exactly.
