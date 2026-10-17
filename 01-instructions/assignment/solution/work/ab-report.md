# A1 A/B report: the instructions layer on section-1 (reference tree)

This is the reference solution's report. Its structure is what a learner's report must have. The
reference live run was not captured: the owner's FOCUS instructions of 2026-10-17 required a real
captured live run for assignments A3 and A4 only, so the A1 reference A/B was left out of scope.
Every value below that needs the run says so instead of giving a number.

## Setup

- Command: `uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference`
- Runs per arm: 24 (8 section-1 tasks, k=3; DESIGN §11.5)
- Model and reasoning effort: `OPENAI_MODEL` and `OPENAI_REASONING_EFFORT` from the settings
  (CONTRACTS §1), recorded in each experiment's metadata

Instructions tree commit: none, because the reference live run was not captured (owner scope,
2026-10-17).

## Results

| Measure | Bare arm (runs failing of N) | Harness arm (runs failing of N) |
|---|---|---|
| R1: runs with at least one new R1 violation | not captured | not captured |
| R3: runs with at least one new R3 failure | not captured | not captured |

No counts: the reference live run was not captured (owner scope, 2026-10-17).

## Links

No LangSmith experiment links: the reference live run was not captured (owner scope, 2026-10-17).

## Cost and traces

Budget for this command: at most $2.50 and 150 traces (DESIGN §11.5); the run stops cleanly at
`MAX_BATCH_COST_USD`. No measured cost or trace count: the reference live run was not captured
(owner scope, 2026-10-17).

## Reading the result

The primary measure for section 1 is registered in DESIGN §8.2: a run fails when it has at least one
new R1 violation, and results are counts of failing runs out of k per task, summed over the eight
tasks. R3 is the secondary measure this assignment adds: runs with at least one new R3 failure. With
counts from a captured run, compare the arms on R1 first, then on R3, and look task by task at F1-trap
(the legacy handler next to the right pattern) and at the control task C1, where both arms should
pass. Check in the run logs that harness runs opened the map's targets and the skill; a harness run
that never read `docs/SECURITY.md` or the skill did not test the restructuring.

## Limits

Three runs per task is a small sample, so a difference of one or two runs between the arms is not
evidence on its own. One model and one effort level are used. The referee counts only what the R1
and R3 probes cover, and both arms read the same facts, so the comparison measures organisation, not
content.
