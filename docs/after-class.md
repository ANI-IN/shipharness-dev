# After class

What to do in the days between the live class and the Thursday review: read the results you saw,
run things yourself, do the four assignments, read further, and point the tools at your own
repository. Source ids such as (A3, F-a-126) point to [REFERENCES.md](../REFERENCES.md).

## 1. Keep what you have

- Your `.shipharness/runs/` and `exports/` folders are git-ignored and only on your machine. Every
  run is a dot in the results, including aborted ones, so do not delete runs you want to report.
- LangSmith keeps an ordinary trace for 14 days ("Base traces have the base retention and are
  short-lived (14 days)", LangSmith billing page, https://docs.langchain.com/langsmith/billing, read
  2026-10-17). Copy the trace links you need into your notes; the score records in
  `exports/scores/` stay on disk and hold the links (`trace_url`, `referee_trace_url`).

## 2. Read the results again, slowly

The live class shows one run per arm per section. One run is one dot: read it next to the
experiment dots, never alone, because model output varies between runs.

```bash
uv run shipharness report
```

This reads only `exports/` and writes `exports/report.json` and `exports/report.html`, with one dot
per run for every feature that has a primary measure (F1-F4). It makes no model calls and prints
`Cost: $0.000000 (no model calls; runs in exports $...)`. Replays are left out unless you pass
`--include-recorded`. (`make report` is still a placeholder target in this release and only prints
a message.)

How to read a single score record, field by field, is in
[final-project/README.md, part 5](../final-project/README.md#5-how-to-read-the-results).

## 3. Run a demo yourself

You can repeat any section's A/B on your own machine. It calls OpenAI live (no fallback) and costs
real money, within these caps per A/B: 2 arms × $0.20 plus 2 blinded reviews × $0.04, so at most
$0.48 (`.env.example`).

Two ways to run it:

```bash
# Option 1: traced to shipharness-assignments, with its own cost session
make demo-1 PURPOSE=assignment

# Option 2: as a class command; needs SHIPHARNESS_CLASS_DATE=<today> in .env
make demo-1
```

Watch it with `make console` in a second terminal (http://127.0.0.1:8765/). The demos' layer
stacks, features, and what to watch are in each section's runbook:
[S1](../submodules/01-instructions/demo/README.md),
[S2](../submodules/02-state-lifecycle/demo/README.md),
[S3](../submodules/03-scope-sandbox/demo/README.md),
[S4](../submodules/04-verification/demo/README.md).

To see what one layer contributes, remove it: `make demo-2 LAYERS=-state` runs the S2 A/B with the
harness arm keeping only the instructions layer. This is A3's method of "removing one component at
a time and reviewing what impact it had on the final result" (A3, F-a-125).

`make swap-N` re-judges your latest demo-N A/B with the labels swapped and costs nothing.

## 4. Do the assignments

Each assignment has a brief with grading criteria (100 points), a starter folder, an offline
self-check, and one required live step. Work in the order of the sections.

| Assignment | Brief | Self-check | Live step, bounded by the caps |
|---|---|---|---|
| 1 Instructions | [README](../submodules/01-instructions/assignment/README.md) | `make check-assignment-1` | An A/B on the `section-1` subset, k=3: at most $2.50 and 150 traces |
| 2 State and session lifecycle | [README](../submodules/02-state-lifecycle/assignment/README.md) | `make check-assignment-2` | One A/B with three forced stops: at most $0.40, 4 traces |
| 3 Scope and sandbox | [README](../submodules/03-scope-sandbox/assignment/README.md) | `make check-assignment-3` | One `demo-3` A/B: 2 × $0.20 + 2 × $0.04, 4 traces |
| 4 Verification and portfolio | [README](../submodules/04-verification/assignment/README.md) | `make check-assignment-4` | One `testgen` run and one F4 A/B: at most $0.68 |

The planned learner budget for all four is at most $6 of OpenAI usage and 400 LangSmith traces;
no single command may spend more than $2.50 (`MAX_BATCH_COST_USD`). The budget figures come from
each assignment's "Cost and trace budget" section; read it before you start a live step.

On a fresh clone every self-check fails with FAIL lines that name the TODOs to fix. That is the
starting point. `make grade-assignment-N` is the instructor's grader and needs private files that
are not in this repository.

The reference solutions are not in this repository. They are published as a tagged release after
the Thursday review session.

## 5. Read further

Start with each section's session notes (what was shown, the key ideas with their sources, what
the A/B showed, common questions):
[S1](../submodules/01-instructions/session-notes.md),
[S2](../submodules/02-state-lifecycle/session-notes.md),
[S3](../submodules/03-scope-sandbox/session-notes.md),
[S4](../submodules/04-verification/session-notes.md).

Each section also has two to four reading notes that go deeper than class time, each with a reading
time and a "why it matters for your own repo" part:

- [S1 Instructions](../submodules/01-instructions/post-class-reading/README.md)
- [S2 State and session lifecycle](../submodules/02-state-lifecycle/post-class-reading/README.md)
- [S3 Scope and sandbox](../submodules/03-scope-sandbox/post-class-reading/README.md)
- [S4 Verification](../submodules/04-verification/post-class-reading/README.md)

The primary sources themselves (A1 to A7, B1 to B13) are listed with links in
[REFERENCES.md](../REFERENCES.md). A3's advice to whoever builds a harness is to "read its traces on
realistic problems" (A3, F-a-126); your LangSmith project from class is a good place to start.

## 6. Apply it to your own repository

The [final project](../final-project/README.md) walks through the whole run and then points the
same tools at your own code:

1. Assess your repository's harness (read-only, no model calls):
   `uv run python skills/harness-setup/scripts/assess.py <your-repo> --out harness-assessment.html`
2. Add the missing parts from the `harness-setup` templates, then assess again.
3. Turn a rule your reviewers keep repeating into a check with the `house-rules` skill.
4. Generate tests that must pass five filters with `shipharness testgen` (the `assured-tests`
   skill; costs money).
5. Write your own skill from `skills/skill-template/` and validate it with
   `uv run shipharness skills validate <your-skill-dir>`.

Installing the skills into Claude Code, Codex, or Cursor is described in each skill's README:
[harness-setup](../skills/harness-setup/README.md), [house-rules](../skills/house-rules/README.md),
[assured-tests](../skills/assured-tests/README.md),
[skill-template](../skills/skill-template/README.md).

To copy TeamTrack's whole harness into your repository in one command and fill it step by step, follow [apply-to-your-repo.md](apply-to-your-repo.md).

## 7. The Thursday review

The review session goes through the four assignments: the expected approach, a walkthrough of the
reference solution, common mistakes, and discussion; the hidden scripted diffs of assignment 3 are
shown there. Bring your self-check output and one question per assignment. The solutions are
released as a tagged release after the session.
