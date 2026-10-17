# solution

Reference solution and hidden grader for assignment A2 (brief: `../assignment/README.md`).

| Path | What it is |
|---|---|
| `a2_state/` | The reference `ResumableStateLayer` (layer.py, ledger.py, progress_log.py) |
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits |
| `grader/grade.py` | Grader: visible and hidden scenarios, score out of 100 |
| `grader/a2_hidden.py` | The four hidden scenarios and the hidden four-step feature (labels) |
| `grader/tests/` | Hidden grader tests: the solution scores 100, the starter and the class layer do not |
| `tests/` | Unit tests of the solution's ledger and progress-file helpers |
| `class_s2_layer/` | The class's S2 layer under the name the grader loads (a baseline) |
| `captured/` | Captured output of the self-check and the grader |
| `live/` | The command that records the reference solution's live run; that run is not captured (owner scope, 2026-10-17) |

```
make check-assignment-2 A2_IMPL=submodules/02-state-lifecycle/solution
make grade-assignment-2 SUBMISSION=submodules/02-state-lifecycle/solution
uv run python -m pytest -q -p no:cacheprovider submodules/02-state-lifecycle
```

The first two are what produced `captured/` (2026-10-17). Without make they run
`assignment/check.py --impl <folder>` and `scripts/grade_assignment.py 2 <folder>`.

Grading a learner's submission (the folder with `a2_state/` and `live/`, or a cloned repository
with exactly one such folder):

```
uv run python submodules/02-state-lifecycle/solution/grader/grade.py --impl <submission> [--json <file>]
```

The scenarios run the test stand-in agent (not a model). The `live_run` criterion checks the files
in `<submission>/live/` and never runs a model. The reference solution's live run is not being
captured: the owner listed only the A3 and A4 reference live runs for capture (owner scope,
2026-10-17). So the reference solution scores 90.0/100 (`captured/grade-solution.txt`), and that
stays its recorded score.

Recording the reference solution's live run (keys, Docker, checkpoints; `make doctor` passes):

```
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops
```

Keep this folder out of the learners' copy until the Thursday review.
