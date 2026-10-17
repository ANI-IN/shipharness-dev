# solution

The reference solution for assignment A1. Learners do not need anything here to do the
assignment: try it first, then compare. The brief is [../README.md](../README.md). The grader, its
hidden cases, and its tests stay private (instructor only).

| Path | What it is |
|---|---|
| `work/` | a finished work folder: `instructions/` (map, docs, the `add-list-endpoint` skill), `checker/` (the reference checker and the visible tests), `ab-report.md` (structure complete; each A/B value says the reference live run was not captured), `live/` (no evidence; its `README.md` says why and keeps the exact commands) |
| `captured/` | the output of the self-check and the grader on the starter and on this solution, each file labelled with its capture date |
| `SOLUTION_NOTES.md` | approach, design choices, alternatives, trade-offs, known limits |

Commands (repository root):

```bash
make check-assignment-1 A1_WORK=01-instructions/assignment/solution/work
uv run python -m pytest -q -p no:cacheprovider 01-instructions/assignment/solution/work/checker
make grade-assignment-1 SUBMISSION=01-instructions/assignment/solution/work   # instructor only
```

Grading a submission: `make grade-assignment-1 SUBMISSION=<folder or git URL>` (instructor only;
the grader is private). The submission is the learner's work folder, or a checkout of their
repository (the grader then uses `01-instructions/assignment/starter` inside it). A git URL is
cloned shallow first (`platform/scripts/grade_assignment.py`).

The reference scores 83.0/100 (`captured/grade-solution.txt`): the five points for the A/B values
(criterion E) and the twelve points of criterion F (live run evidence) are not awarded, because the
reference live run was not captured. The owner's FOCUS instructions of 2026-10-17 required a real
captured live run for A3 and A4 only, so the A1 reference A/B was left out of scope. That is not a
defect of the solution. The reference holds no pending markers, so grading it with
`--allow-pending` also gives 83.0; learners are graded without the flag. A learner's submission
with real live evidence can reach 100: the grader's own tests grade a SYNTHETIC one that does. The
commands that would capture the reference run are in [work/live/README.md](work/live/README.md).
