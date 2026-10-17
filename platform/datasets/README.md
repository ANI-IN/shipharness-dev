# Datasets

| File | LangSmith dataset | Examples | Built in |
|---|---|---|---|
| `teamtrack-features-v1.jsonl` | `teamtrack-features-v1` | 60 build tasks | M5 |
| `testgen-targets-v1.jsonl` | `testgen-targets-v1` | 40 test-generation targets | M5 |
| `mutants/` | (not uploaded) | targeted mutants per module, split into filter and referee sets | M5 |

Each line is one dataset example (inputs, outputs, metadata). Subsets are LangSmith splits
(`smoke`, `section-1` to `section-4`, `testgen`).

Library targets need the pinned sources: `uv run python platform/scripts/fetch_testgen_libs.py` (network;
clones into `.shipharness/libs/`). Regenerate with `uv run python the course build repository's dataset builder` and
`uv run python the course build repository's dataset builder` (both have `--check`).

```bash
uv run shipharness datasets validate platform/datasets/teamtrack-features-v1.jsonl --kind features
uv run shipharness datasets upload   # validates both files, checks the counts, uploads
```
