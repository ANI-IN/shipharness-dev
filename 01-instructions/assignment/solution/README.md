# solution

The reference solution for assignment A1 and its grader. Learners do not need anything here to do
the assignment, and this folder stays in the build repository until the review session; the brief
is [../assignment/README.md](../assignment/README.md).

| Path | What it is |
|---|---|
| `work/` | a finished work folder: `instructions/` (map, docs, the `add-list-endpoint` skill), `checker/` (the reference checker and the visible tests), `ab-report.md` (structure complete; each A/B value says the reference live run was not captured), `live/` (no evidence; its `README.md` says why and keeps the exact commands) |
| `grader/grade.py` | the grader: the self-check's visible checks (live evidence included) plus hidden checks; prints the score out of 100 |
| `grader/hidden/checker_cases.py` | the eleven hidden checker cases |
| `grader/tests/` | tests for the self-check, the grader, the live evidence, and `ab_summary.py`; `synthetic_live.py` builds the SYNTHETIC live evidence they use (invented values, batch `a1-synthetic`, never a real run) |
| `captured/` | the output of the self-check and the grader on the starter and on this solution, each file labelled with its capture date |
| `SOLUTION_NOTES.md` | approach, design choices, alternatives, trade-offs, known limits |

Commands (repository root):

```bash
make grade-assignment-1 SUBMISSION=submodules/01-instructions/solution/work
make check-assignment-1 A1_WORK=submodules/01-instructions/solution/work
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/work/checker
```

Grading a submission: `make grade-assignment-1 SUBMISSION=<folder or git URL>` (instructor only).
It runs `grader/grade.py --work <submission>`; the submission is the learner's work folder, or a
checkout of their repository (the grader then uses `submodules/01-instructions/assignment/starter`
inside it). A git URL is cloned shallow first (`scripts/grade_assignment.py`).

The reference scores 83.0/100 (`captured/grade-solution.txt`): the five points for the A/B values
(criterion E) and the twelve points of criterion F (live run evidence) are not awarded, because the
reference live run was not captured. The owner's FOCUS instructions of 2026-10-17 required a real
captured live run for A3 and A4 only, so the A1 reference A/B was left out of scope. That is not a
defect of the solution. The reference holds no pending markers, so `grade.py --allow-pending` also
gives it 83.0 (`captured/grade-solution-allow-pending.txt`); learners are graded without the flag. A
learner's submission with real live evidence can reach 100: the grader tests grade a SYNTHETIC one
that does. The commands that would capture the reference run are in
[work/live/README.md](work/live/README.md).
