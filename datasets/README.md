# Datasets

| File | LangSmith dataset | Examples | Built in |
|---|---|---|---|
| `teamtrack-features-v1.jsonl` | `teamtrack-features-v1` | 60 build tasks | M5 |
| `testgen-targets-v1.jsonl` | `testgen-targets-v1` | 40 test-generation targets | M5 |
| `mutants/` | (not uploaded) | targeted mutants per module, split into filter and referee sets | M5 |

Line formats are defined in [CONTRACTS.md §16](../CONTRACTS.md). Subsets are LangSmith splits
(`smoke`, `section-1` to `section-4`, `testgen`).

Library targets need the pinned sources: `uv run python scripts/fetch_testgen_libs.py` (network;
clones into `.shipharness/libs/`). Regenerate with `uv run python scripts/build_features_dataset.py` and
`uv run python scripts/build_testgen_dataset.py` (both have `--check`).

```bash
uv run shipharness datasets validate datasets/teamtrack-features-v1.jsonl --kind features
uv run shipharness datasets upload   # validates both files, checks the counts, uploads
```
