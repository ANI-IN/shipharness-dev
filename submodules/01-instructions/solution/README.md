# solution

The reference solution for assignment A1 and its grader. Learners do not need anything here to do
the assignment; the brief is [../assignment/README.md](../assignment/README.md).

| Path | What it is |
|---|---|
| `work/` | a finished work folder: `instructions/` (map, docs, the `add-list-endpoint` skill), `checker/` (the reference checker and the visible tests), `ab-report.md` (structure complete, A/B values as pending markers) |
| `grader/grade.py` | the grader: the self-check's visible checks plus hidden checks; prints the score out of 100 |
| `grader/hidden/checker_cases.py` | the eleven hidden checker cases |
| `grader/tests/` | tests for the self-check, the grader, and `ab_summary.py` |
| `captured/` | the output of the self-check and the grader on the starter and on this solution |
| `SOLUTION_NOTES.md` | approach, design choices, alternatives, trade-offs, known limits |

Commands (repository root):

```bash
uv run python submodules/01-instructions/solution/grader/grade.py --work submodules/01-instructions/solution/work --allow-pending
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/work/checker
```

`--allow-pending` accepts a well-formed `[[PENDING: ...]]` marker in place of the A/B values, because
the reference A/B has not been run. Without it the reference scores 92: the eight points for the A/B
values are not awarded. Learners are graded without the flag.
