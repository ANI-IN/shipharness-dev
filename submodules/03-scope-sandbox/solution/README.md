# solution

Reference solution and grader for assignment A3 (brief: `../assignment/README.md`). The hidden cases
live here, not in the starter; they are revealed at the Thursday review (brief §5.3).

| Path | What it is |
|---|---|
| `a3scope/` | Reference implementation: `diffparse.py`, `scope.py`, `status.py`, `policy.py` (`sandbox.py` as given) |
| `tests/test_a3_sandbox_rule.py` | Reference denial test (passes with the rule, fails without it) |
| `tests/test_a3_docker_rule.py` | Optional real-container check (`pytest -m docker`) |
| `SOLUTION_NOTES.md` | Approach, design choices, alternatives, trade-offs, known limits, hidden case list, review notes |
| `grader/grade.py` | `make grade-assignment-3`: visible + hidden tests, score out of 100 |
| `grader/hidden/` | Hidden scripted diffs (`diffs/`, `cases.json`, built by `make_hidden.py`) and hidden tests |
| `grader/tests/test_a3_grader.py` | Tests for the self-check and the grader |
| `captured/` | Captured output of the self-check and the grader on the starter and on this solution |

Run (from the repository root):

```bash
uv run python submodules/03-scope-sandbox/assignment/check.py --impl submodules/03-scope-sandbox/solution
uv run python submodules/03-scope-sandbox/solution/grader/grade.py --impl submodules/03-scope-sandbox/solution
uv run python -m pytest -q -p no:cacheprovider submodules/03-scope-sandbox/solution/grader/tests
uv run python -m pytest -q -p no:cacheprovider -m docker submodules/03-scope-sandbox/solution/tests
```

Rebuild the hidden diffs after changing a case (the slow grader test checks they are reproducible):

```bash
uv run python submodules/03-scope-sandbox/solution/grader/hidden/make_hidden.py
```
