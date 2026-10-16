# starter

Your implementation folder for assignment A4 (instructions: `../README.md`). Work here on your own branch,
or copy the folder and pass the copy as `A4_IMPL=<folder>` to the make targets.

| Path | State | TODO |
|---|---|---|
| `a4_verification/adapter.py` | `soft_delete` raises | A4-1 |
| `a4_verification/r8_soft_delete.py` | check registered; `issue_param`, `plan`, `judge` raise | A4-2, A4-3, A4-4 |
| `a4_verification/dedup_filter.py` | `normalized` and `evaluate` raise | A4-5, A4-6, A4-7 |
| `a4_verification/run_r8.py`, `apply_filter.py` | complete | none |
| `tests/` | two example tests, failing until you implement | A4-8, A4-9 |
| `skill/` | empty: copy `skills/skill-template` here | see `skill/README.md` |
| `portfolio/` | templates | every TODO line |
| `live/` | empty: the files of your two live runs go here | see `live/README.md` |

The starter imports and runs: `make check-assignment-4` executes every visible test, prints FAIL
with the TODO each failure comes from, and exits 1. Start with `issue_param` and its tests.
