# solution

Reference solution and hidden grader for assignment A4 (brief: `../assignment/README.md`).

| Path | What it is |
|---|---|
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, captured output |
| `a4_verification/` | Reference R8 check, soft-delete adapter, filter 6, and the two CLIs |
| `tests/` | The reference solution's own tests (27 collected test cases) |
| `skill/testgen-evidence/` | Example learner skill with a report-summary script |
| `portfolio/` | Example evidence report, LangSmith page, and case study (model-run output is `[[PENDING]]`) |
| `live/` | Live evidence of the reference solution: exact commands and one `[[PENDING]]` marker until the integrator captures the run (M6 pilot) |
| `grader/grade.py` | `make grade-assignment-4`: visible + hidden tests, score out of 100 |
| `grader/hidden_tests/` | Hidden seeded violations and hidden candidate tests (never in the starter) |
| `grader/tests/` | Tests for the grader, the self-check, and the live-evidence checks (synthetic fixture in `live_fixture.py`, never a real run) |
| `captured/` | Real output of the self-check, the grader, and R8 on TeamTrack (each file starts with its capture date, command, and commit) |

Run the grader on this folder: `make grade-assignment-4 SUBMISSION=submodules/04-verification/solution`
(or `uv run python submodules/04-verification/solution/grader/grade.py`). Its 100/100 includes 20
points that pass on `[[PENDING]]` markers, not on a real run: live-evidence (10) on the `live/`
marker, and portfolio-evidence (5), portfolio-langsmith (2), and portfolio-case-study (3) on the
portfolio markers (SOLUTION_NOTES.md, "Known limits").
Grade a submission: `uv run python submodules/04-verification/solution/grader/grade.py --impl
<submission folder>` (the implementation folder with its `live/`, or a checkout of the course repo).
When `--impl` is this folder, `[[PENDING]]` markers in `portfolio/` and `live/` are accepted in
place of run output; for any other folder they fail the portfolio and live-evidence criteria.
