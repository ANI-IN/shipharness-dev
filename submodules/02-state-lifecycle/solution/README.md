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

```
uv run python submodules/02-state-lifecycle/assignment/check.py --impl submodules/02-state-lifecycle/solution
uv run python submodules/02-state-lifecycle/solution/grader/grade.py --impl submodules/02-state-lifecycle/solution
uv run python -m pytest -q -p no:cacheprovider submodules/02-state-lifecycle
```

Keep this folder out of the learners' copy until the Thursday review.
