# solution

Reference solution for assignment A4 (brief: [../README.md](../README.md)). Try the assignment
first, then compare. The grader, its hidden tests, and its own tests stay private (instructor
only).

| Path | What it is |
|---|---|
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, captured output |
| `a4_verification/` | Reference R8 check, soft-delete adapter, filter 6, and the two CLIs |
| `tests/` | The reference solution's own tests (27 collected test cases) |
| `skill/testgen-evidence/` | Example learner skill with a report-summary script |
| `portfolio/` | Example evidence report, LangSmith page, and case study, filled from the live run in `live/` |
| `live/` | Live evidence of the reference solution, captured on 2026-10-17 (testgen run `r-20261017-093940-52dde8`, F4 A/B `ab-20261017-094339-3b29e3`), and the commands that produced it |
| `captured/` | Real output of the self-check, the grader, and R8 on TeamTrack (each file starts with its capture date, command, and commit) |

The grader (instructor only) on this folder: `make grade-assignment-4
SUBMISSION=04-verification/assignment/solution`. It scores 100/100
(`captured/grade-solution.txt`), every criterion on real work: live-evidence (10) on the captured
run in `live/`, and the three portfolio criteria (5 + 2 + 3) on pages filled from that run.
Grade a submission: `make grade-assignment-4 SUBMISSION=<submission folder>` (the implementation
folder with its `live/`, or a checkout of the course repo).
The grader treats this folder like any submission: a PENDING marker in `portfolio/` or a
`live/` without evidence fails the portfolio and live-evidence criteria here too.
