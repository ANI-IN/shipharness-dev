# solution

Reference solution and grader for assignment A3 (brief: `../assignment/README.md`). The hidden cases
live here, not in the starter; they are revealed at the Thursday review (brief §5.3).

| Path | What it is |
|---|---|
| `a3scope/` | Reference implementation: `diffparse.py`, `scope.py`, `status.py`, `policy.py` (`sandbox.py` as given) |
| `tests/test_a3_sandbox_rule.py` | Reference denial test (passes with the rule, fails without it) |
| `tests/test_a3_docker_rule.py` | Optional real-container check (`pytest -m docker`) |
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, hidden case list, review notes |
| `grader/grade.py` | `make grade-assignment-3`: visible + hidden tests + live evidence, score out of 100 |
| `grader/hidden/` | Hidden scripted diffs (`diffs/`, `cases.json`, built by `make_hidden.py`) and hidden tests |
| `grader/tests/test_a3_grader.py` | Tests for the self-check and the grader |
| `grader/tests/test_a3_live.py` | Tests for the live step tool (`assignment/live.py`) |
| `grader/tests/synthetic_live.py` | SYNTHETIC A/B for those tests, written by hand: never a real run |
| `live/` | Captured live step of this solution (A/B `ab-20261017-092810-d5d31c`, below) |
| `captured/` | Captured output of the self-check and the grader on the starter and on this solution |

Run (from the repository root):

```bash
make check-assignment-3 A3_IMPL=03-scope-sandbox/assignment/solution    # self-check
make grade-assignment-3 SUBMISSION=03-scope-sandbox/assignment/solution # grader, score out of 100
uv run python -m pytest -q -p no:cacheprovider 03-scope-sandbox/assignment/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider -m docker 03-scope-sandbox/assignment/solution/tests
```

The first two were run again on 2026-10-17 after the live run was captured (output in
`captured/`). The grader tests were run the same day (42 passed, the slow one deselected); the
docker line was not (no containers), and `captured/docker-solution.txt` holds the container check
from 2026-10-16.

Grade a learner submission (a folder, or a git URL that is cloned shallow; `platform/scripts/grade_assignment.py`):

```bash
make grade-assignment-3 SUBMISSION=<folder or git URL>
uv run python 03-scope-sandbox/assignment/solution/grader/grade.py --impl <submission folder>  # the same, without make
```

`--live <dir>` points at live evidence kept elsewhere. The grader reads `<submission>/live/`, validates
it, and re-runs the submission's `a3scope` on the included diffs; it calls no model and needs no keys.

## Captured live run of this solution

The live step of the reference solution, run once with the class settings (`gpt-6-luna`,
`MAX_RUN_COST_USD=0.20`, `MAX_BATCH_COST_USD=2.50`), from the repository root:

```bash
uv run shipharness ab --section demo-3 --feature F3 --no-preview --purpose assignment 2>&1 | tee ab-output.txt
uv run python 03-scope-sandbox/assignment/live.py collect --impl 03-scope-sandbox/assignment/solution --ab-output ab-output.txt --command "uv run shipharness ab --section demo-3 --feature F3 --no-preview --purpose assignment"
uv run python 03-scope-sandbox/assignment/live.py verify --impl 03-scope-sandbox/assignment/solution
```

Captured on 2026-10-17, run `ab-20261017-092810-d5d31c` (both arms' score records:
`r-20261017-092810-03baf8` bare, `r-20261017-092810-1551e0` harness). `live.py collect` wrote the
files in `solution/live/`: `command.txt`, `ab-output.txt` with the cost line, `ab-summary.json`,
`scores/<run_id>.json` for both arms, `<arm>/diff.patch`, `<arm>/sandbox-log.json`, and
`verdict-<arm>.json`. `live.py verify` prints `evidence ok` and `verdicts ok` for them. The cost
line of the A/B (`live/ab-output.txt`):

```
Cost: $0.021708 (this command: gpt-5.6-luna $0.005858, gpt-6-luna $0.015850; session $0.021708 of $2.50; build $2.091206 of $15.00 ($12.908794 left))
```

In that A/B both arms passed the S3 primary measure (0 out-of-scope files, 0 test-phase source
edits) and 49 of 49 hidden tests. The harness arm's status is `ABORTED: timeout` (its build
claimed done) and it killed 0 of 4 referee mutants against the bare arm's 4 of 4. One run per arm
is an example, not a rate.

Grading this folder now scores 100.0 / 100 with `Result: PASS`: criterion 6 is 10 / 10 on the
captured run, graded like any submission's `live/` (`captured/grade-solution.txt`). The grader's
own tests also grade a copy with the synthetic evidence in `grader/tests/synthetic_live.py`, which
is never a real run, and grade this folder as it is
(`test_reference_solution_passes_on_its_captured_live_run`).

Rebuild the hidden diffs after changing a case (the slow grader test checks they are reproducible):

```bash
uv run python 03-scope-sandbox/assignment/solution/grader/hidden/make_hidden.py
```
