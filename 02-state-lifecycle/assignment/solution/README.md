# solution

Reference solution for assignment A2 (brief: [../README.md](../README.md)). Try the assignment
first, then compare. The grader, its hidden scenarios, and its tests stay private (instructor
only).

| Path | What it is |
|---|---|
| `a2_state/` | The reference `ResumableStateLayer` (layer.py, ledger.py, progress_log.py) |
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits |
| `tests/` | Unit tests of the solution's ledger and progress-file helpers |
| `class_s2_layer/` | The class's S2 layer under the name the grader loads (a baseline) |
| `captured/` | Captured output of the self-check and the grader |
| `live/` | The command that records the reference solution's live run; that run is not captured (owner scope, 2026-10-17) |

```
make check-assignment-2 A2_IMPL=02-state-lifecycle/assignment/solution
make grade-assignment-2 SUBMISSION=02-state-lifecycle/assignment/solution   # instructor only
uv run python -m pytest -q -p no:cacheprovider 02-state-lifecycle
```

The first two are what produced `captured/` (2026-10-17). Without make they run
`assignment/check.py --impl <folder>` and `platform/scripts/grade_assignment.py 2 <folder>`.

Grading a learner's submission (the folder with `a2_state/` and `live/`, or a cloned repository
with exactly one such folder) is `make grade-assignment-2 SUBMISSION=<submission>` (instructor
only).

The scenarios run the test stand-in agent (not a model). The `live_run` criterion checks the files
in `<submission>/live/` and never runs a model. The reference solution's live run is not being
captured: the owner listed only the A3 and A4 reference live runs for capture (owner scope,
2026-10-17). So the reference solution scores 90.0/100 (`captured/grade-solution.txt`), and that
stays its recorded score.

Recording the reference solution's live run (keys, Docker, checkpoints; `make doctor` passes):

```
uv run python 02-state-lifecycle/assignment/live/run_live.py --impl 02-state-lifecycle/assignment/solution --forced-stops
```
