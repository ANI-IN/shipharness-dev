# solution

The reference solution for assignment A1 and its grader. Learners do not need anything here to do
the assignment, and this folder stays in the build repository until the review session; the brief
is [../assignment/README.md](../assignment/README.md).

| Path | What it is |
|---|---|
| `work/` | a finished work folder: `instructions/` (map, docs, the `add-list-endpoint` skill), `checker/` (the reference checker and the visible tests), `ab-report.md` (structure complete, A/B values as pending markers), `live/` (where the captured live run goes; for now its `README.md` holds the exact commands and a pending marker) |
| `grader/grade.py` | the grader: the self-check's visible checks (live evidence included) plus hidden checks; prints the score out of 100 |
| `grader/hidden/checker_cases.py` | the eleven hidden checker cases |
| `grader/tests/` | tests for the self-check, the grader, the live evidence, and `ab_summary.py`; `synthetic_live.py` builds the SYNTHETIC live evidence they use (invented values, batch `a1-synthetic`, never a real run) |
| `captured/` | the output of the self-check and the grader on the starter and on this solution |
| `SOLUTION_NOTES.md` | approach, design choices, alternatives, trade-offs, known limits |

Commands (repository root):

```bash
uv run python submodules/01-instructions/solution/grader/grade.py --work submodules/01-instructions/solution/work --allow-pending
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/work/checker
```

Grading a submission: `--work` takes the learner's work folder, or a checkout of their repository
(the grader then uses `submodules/01-instructions/assignment/starter` inside it):

```bash
uv run python submodules/01-instructions/solution/grader/grade.py --work <work folder or checkout>
```

`--allow-pending` accepts a well-formed `[[PENDING: ...]]` marker in place of the A/B values and of
the live evidence, because the reference live run has not been captured. Without it the reference
scores 83: the five points for the A/B values and the twelve points of criterion F (live run
evidence) are not awarded. Learners are graded without the flag. The commands that capture the
reference run are in [work/live/README.md](work/live/README.md).
