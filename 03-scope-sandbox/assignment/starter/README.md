# starter

Your starting files for assignment A3 (task and grading criteria: [`../README.md`](../README.md)).

| File | Status |
|---|---|
| `a3scope/diffparse.py` | Part A1: `parse_diff`, `changed_paths` are `TODO` |
| `a3scope/scope.py` | Part A2: `glob_matches`, `check_diff` are `TODO` |
| `a3scope/status.py` | Part B: `update_status` is `TODO` |
| `a3scope/policy.py` | Part C: `HISTORY_MESSAGE`, `HISTORY_RULES` are `TODO` |
| `a3scope/sandbox.py` | Given: `PolicySandbox` (pre-exec denial, as in `DockerSandbox.exec`) |
| `tests/test_a3_sandbox_rule.py` | Task 6: your denial test is `TODO` |
| `tests/test_a3_docker_rule.py` | Given: optional real-container check (`pytest -m docker`) |
| `live/` | Not here yet: `assignment/live.py collect` writes it after your live A/B (assignment README, "Live step") |

Every `TODO` is marked `TODO(A3 ...)`; `make check-assignment-3` lists the ones left. The package
imports and the self-check runs on these files as they are; it fails until the parts are done.
