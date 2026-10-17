# Worked example: the kit on three boltons modules

This folder is the end state of the worked example in
[docs/apply-to-your-repo.md](../../../docs/apply-to-your-repo.md): the kit installed with
`shipharness init` and filled in for a small real repository, three modules of boltons 26.2.0
(`typeutils`, `listutils`, `queueutils`) with their tests. boltons is BSD-3-Clause; the course
already pins it for `shipharness testgen` (`datasets/sources/testgen.toml`), and
`scripts/fetch_testgen_libs.py` fetches it without a model call.

## Rebuild the starting repository

```bash
uv run python scripts/fetch_testgen_libs.py boltons
bash kit/examples/boltons-queueutils/make_repo.sh /tmp/boltons-queueutils
```

`make_repo.sh` copies the three modules, their tests, `LICENSE`, and `.gitignore` from the pinned
clone into a new git repository and commits them. The boltons code is not stored in this folder.

## What is in `filled/`

Every kit file as it reads after filling, in the same layout as the repository. Compare a file here
with the same path in [`kit/templates/`](../../templates/) to see what changed.

| Decision | Files |
|---|---|
| Rewritten for this repository | `AGENTS.md`, `ARCHITECTURE.md`, `docs/QUALITY_SCORE.md`, `docs/PLANS.md`, `docs/design-docs/`, `docs/product-specs/`, `docs/references/import-linter-llms.txt`, `docs/clean-state-checklist.md`, `docs/house-rules.md`, the state files, `feature_list.json`, `init.sh`, `harness/`, `.github/workflows/shipharness.yml` |
| Kept as copied, marker lines removed | `feature_list.schema.json`, `harness/sandbox-policy.toml` |
| Deleted: they do not apply to a library with no API, tenants, or database | `docs/SECURITY.md`, `docs/RELIABILITY.md`, `docs/design-docs/api-conventions.md`, `docs/design-docs/cursor-pagination.md`, `docs/product-specs/teamtrack-base.md`, `docs/references/alembic-llms.txt` |
| Added | `docs/product-specs/queueutils.md` (replaces `teamtrack-base.md`), `harness/check-baseline.json` (written by `shipharness check --json`) |

The feature in `feature_list.json` is real: the docstrings of `peek` and `pop` say an empty queue
raises `KeyError`, and the code raises `IndexError` (`docs/product-specs/f1.md` in `filled/`).

`tests/unit/kit/test_example.py` keeps this folder honest: no REPLACE marker is left, the files
kept as copied still match the kit, and, when the boltons clone is present, the house-rule check
passes on a rebuilt repository.
