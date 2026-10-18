---
name: section-author
description: Write one course section to the structure-and-taste rules - README, concepts, demo (run.sh, walkthrough, expected output), assignment (spec, starter, solution, grader), post-class reading and session notes. Use when filling a generated section folder or rewriting one.
---

# Section author

A section teaches one idea through one failure: a problem an engineer recognises, why it happens,
the fix, a live demo of the fix, and an assignment that builds it. The page templates are in section
1.2 of [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md); the taste rules are in sections 2
and 3.

## When to use

- A generated `section-N-<slug>/` still holds guide comments.
- A finished section must be rewritten after review, or matched to the golden sample.

## Inputs

- The section's failure story, approved by the owner.
- The demo's real files and its one command, and a real captured run (from
  [live-demo-runner](../live-demo-runner/SKILL.md)).
- The assignment's grader and hidden tests (private), and the reference solution.
- The sources the section cites, with titles and links.

## Steps

1. **Problem first.** In every teaching page, "The problem" opens with **Illustrative scenario.**, a
   story with no numbers; then why it happens (cited), what the section does, then the how-to.
2. **README** (at most 120 lines): the template headings, and a table of the parts in order with
   what each gives and when in class.
3. **concepts.md** (15 minutes live, about 1,800 words at most): the idea in one sentence, how it
   works, how `<PROJECT>` does it, what was measured, when it helps and when not, exactly 3 key
   takeaways, 3 to 5 questions with answers in details blocks.
4. **demo/**: `run.sh` (comment block with what it runs, the most it costs at the caps, dated
   measured time; `set -euo pipefail`; works from any folder; clear error lines), the real files the
   demo uses with no course text added, `walkthrough.md` (30 to 40 code lines, one H3 per excerpt,
   "<file>, lines a-b"), `expected/` with the real captured output, and `README.md` ending "Run it"
   with the files-and-links list.
5. **assignment/**: README with "Try it yourself first. The full solution is in ./solution/ with a
   step-by-step walkthrough." under the H1, steps each with "Check:", grading criteria summing to 100
   points; `SPEC.md` with numbered, testable requirements; `starter/` the learner's files;
   `solution/` complete and working with `SOLUTION.md`, captured self-check output, one real live run
   and its grade. Write the grader's visible tests first and watch them fail on the starter. Keep the
   grader code and hidden tests private.
6. **post-class-reading/**: an index (reading, time, why), and per reading "Reading time: about N
   minutes.", a "Source:" line, why it matters, exactly 3 key ideas, apply it to your repo.
7. **session-notes.md** (at most 150 lines): what class showed, key ideas, what the result showed,
   questions from class, what to try next.
8. **diagrams/**: per diagram an Excalidraw source, 2x PNG and SVG, the shared palette, labels of at
   least 20 px when placed, alt text and caption; never colour alone.
9. Apply [style-and-naming](../style-and-naming/SKILL.md) and remove each guide comment as its part
   is written.

## Outputs

A section folder with every required file, no guide comments, every number traced to a run or file,
every link working, and one glossary box per teaching page.

## Checks

- `make check-style-strict` and the prose lint report 0 errors and 0 warnings.
- The assignment's visible tests fail on `starter/` and pass on `solution/`.
- `run.sh` runs from another folder and exits non-zero on failure.
- Every result is a count with its source; see
  [honesty-and-measures.md](../../playbooks/honesty-and-measures.md).
- The section passes its part of the [checklist](../../STRUCTURE-AND-TASTE-CHECKLIST.md) and a
  [fresh-reviewer](../fresh-reviewer/SKILL.md) pass.
