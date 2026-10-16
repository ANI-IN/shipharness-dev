# solution

Reference solution and hidden grader for assignment A4 (brief: `../assignment/README.md`).

| Path | What it is |
|---|---|
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, captured output |
| `a4_verification/` | Reference R8 check, soft-delete adapter, filter 6, and the two CLIs |
| `tests/` | The reference solution's own tests (27 collected test cases) |
| `skill/testgen-evidence/` | Example learner skill with a report-summary script |
| `portfolio/` | Example evidence report, LangSmith page, and case study (model-run output is `[[PENDING]]`) |
| `live/` | Live evidence of the reference solution: exact commands and `[[PENDING]]` markers until M8 batch 1 |
| `grader/grade.py` | `make grade-assignment-4`: visible + hidden tests, score out of 100 |
| `grader/hidden_tests/` | Hidden seeded violations and hidden candidate tests (never in the starter) |
| `grader/tests/` | Tests for the grader, the self-check, and the live-evidence checks (synthetic fixture in `live_fixture.py`, never a real run) |
| `captured/` | Real output of the self-check, the grader, and R8 on TeamTrack |

Run the grader on this folder: `uv run python submodules/04-verification/solution/grader/grade.py`.
Grade a submission: `uv run python submodules/04-verification/solution/grader/grade.py --impl
<submission folder>` (the implementation folder with its `live/`, or a checkout of the course repo).
When `--impl` is this folder, `[[PENDING]]` markers in `portfolio/` and `live/` are accepted in
place of run output; for any other folder they fail the portfolio and live-evidence criteria.
