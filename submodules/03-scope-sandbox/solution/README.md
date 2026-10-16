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
| `live/` | Captured live step of this solution (pending, below) |
| `captured/` | Captured output of the self-check and the grader on the starter and on this solution |

Run (from the repository root):

```bash
uv run python submodules/03-scope-sandbox/assignment/check.py --impl submodules/03-scope-sandbox/solution
uv run python submodules/03-scope-sandbox/solution/grader/grade.py --impl submodules/03-scope-sandbox/solution
uv run python -m pytest -q -p no:cacheprovider submodules/03-scope-sandbox/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider -m docker submodules/03-scope-sandbox/solution/tests
```

Grade a learner submission (a folder or a clone of the learner's repository holding `a3scope/`,
`tests/`, and `live/`):

```bash
uv run python submodules/03-scope-sandbox/solution/grader/grade.py --impl <submission folder>
```

`--live <dir>` points at live evidence kept elsewhere. The grader reads `<submission>/live/`, validates
it, and re-runs the submission's `a3scope` on the included diffs; it calls no model and needs no keys.

## Captured live run of this solution

The live step of the reference solution, run once with the class settings (`gpt-6-luna`,
`MAX_RUN_COST_USD=0.20`, `MAX_BATCH_COST_USD=2.50`), from the repository root:

```bash
uv run shipharness ab --section demo-3 --feature F3 --no-preview 2>&1 | tee ab-output.txt
uv run python submodules/03-scope-sandbox/assignment/live.py collect --impl submodules/03-scope-sandbox/solution --ab-output ab-output.txt --command "uv run shipharness ab --section demo-3 --feature F3 --no-preview"
uv run python submodules/03-scope-sandbox/assignment/live.py verify --impl submodules/03-scope-sandbox/solution
```

The files go to `solution/live/` (`command.txt`, `ab-output.txt` with the cost line, `ab-summary.json`,
`scores/<run_id>.json` for both arms, `<arm>/diff.patch`, `<arm>/sandbox-log.json`,
`verdict-<arm>.json`):

[[PENDING: captured live run of the reference solution | source: M8 batch 1 | how: uv run shipharness ab --section demo-3 --feature F3 --no-preview, output saved as ab-output.txt; uv run python submodules/03-scope-sandbox/assignment/live.py collect --impl submodules/03-scope-sandbox/solution --ab-output ab-output.txt --command "uv run shipharness ab --section demo-3 --feature F3 --no-preview"]]

Until then, grading this folder directly scores 90.0 / 100 with `Result: FAIL` (no live evidence), as
`captured/grade-solution.txt` shows; the grader's own tests grade a copy with the synthetic evidence.

Rebuild the hidden diffs after changing a case (the slow grader test checks they are reproducible):

```bash
uv run python submodules/03-scope-sandbox/solution/grader/hidden/make_hidden.py
```
