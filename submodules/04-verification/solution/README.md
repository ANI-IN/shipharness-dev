# solution

Reference solution and hidden grader for assignment A4 (brief: `../assignment/README.md`).

| Path | What it is |
|---|---|
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, captured output |
| `a4_verification/` | Reference R8 check, soft-delete adapter, filter 6, and the two CLIs |
| `tests/` | The reference solution's own tests (24 collected test cases) |
| `skill/testgen-evidence/` | Example learner skill with a report-summary script |
| `portfolio/` | Example evidence report, LangSmith page, and case study (model-run output is `[[PENDING]]`) |
| `grader/grade.py` | `make grade-assignment-4`: visible + hidden tests, score out of 100 |
| `grader/hidden_tests/` | Hidden seeded violations and hidden candidate tests (never in the starter) |
| `grader/tests/` | Tests for the grader and the self-check |
| `captured/` | Real output of the self-check, the grader, and R8 on TeamTrack |

Run the grader on this folder: `uv run python submodules/04-verification/solution/grader/grade.py`.
When `--impl` is this folder, `[[PENDING]]` markers in `portfolio/` are accepted in place of run
output; for any other folder they fail the portfolio criteria.
