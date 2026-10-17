# solution

Reference solution and hidden grader for assignment A4 (brief: `../assignment/README.md`).

| Path | What it is |
|---|---|
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, captured output |
| `a4_verification/` | Reference R8 check, soft-delete adapter, filter 6, and the two CLIs |
| `tests/` | The reference solution's own tests (27 collected test cases) |
| `skill/testgen-evidence/` | Example learner skill with a report-summary script |
| `portfolio/` | Example evidence report, LangSmith page, and case study, filled from the live run in `live/` |
| `live/` | Live evidence of the reference solution, captured on 2026-10-17 (testgen run `r-20261017-093940-52dde8`, F4 A/B `ab-20261017-094339-3b29e3`), and the commands that produced it |
| `grader/grade.py` | `make grade-assignment-4`: visible + hidden tests, score out of 100 |
| `grader/hidden_tests/` | Hidden seeded violations and hidden candidate tests (never in the starter) |
| `grader/tests/` | Tests for the grader, the self-check, the live-evidence checks, and the portfolio checks (synthetic fixture in `live_fixture.py`, never a real run; the reference solution's own `live/` and `portfolio/` are graded as they are) |
| `captured/` | Real output of the self-check, the grader, and R8 on TeamTrack (each file starts with its capture date, command, and commit) |

Run the grader on this folder: `make grade-assignment-4 SUBMISSION=04-verification/assignment/solution`
(or `uv run python 04-verification/assignment/solution/grader/grade.py`). It scores 100/100
(`captured/grade-solution.txt`), every criterion on real work: live-evidence (10) on the captured
run in `live/`, and the three portfolio criteria (5 + 2 + 3) on pages filled from that run.
Grade a submission: `uv run python 04-verification/assignment/solution/grader/grade.py --impl
<submission folder>` (the implementation folder with its `live/`, or a checkout of the course repo).
The grader treats this folder like any submission: a PENDING marker in `portfolio/` or a
`live/` without evidence fails the portfolio and live-evidence criteria here too.
