# Evidence report: generated tests for TeamTrack's issue repository, and R8

Reference version. Sections that need a model run hold a `[[PENDING]]` marker until the
instructor's run fills them; everything under "R8 on TeamTrack" is real output (no model call).

## Target

- Dataset target `TG-teamtrack-app-repositories-issues` from `datasets/testgen-targets-v1.jsonl`:
  module `app/repositories/issues.py` in `teamtrack/` (pin `m1-base`).
- Existing tests (from the target line): `tests/visible/test_tenant_isolation.py`,
  `tests/visible/test_issues.py`, `tests/visible/test_legacy_and_schema.py`.
- Filter mutants: `teamtrack/mutants/app.repositories.issues.jsonl#filter` (2 of the file's 4
  mutants). One of them, `app.repositories.issues-m3`, is "soft-deleted issues still listed": the
  same fault R8 looks for, at the unit level.
- Why this module: it holds the live-issue lookups (`get`, `list_for_project`) that every R8
  finding in this assignment traces back to.

## Commands

```
uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 \
    --out .shipharness/a4/testgen
export PYTHONPATH=submodules/04-verification/solution
uv run python -m a4_verification.apply_filter --repo teamtrack --kept .shipharness/a4/testgen \
    --existing tests/visible/test_tenant_isolation.py --existing tests/visible/test_issues.py \
    --existing tests/visible/test_legacy_and_schema.py --update-report
python submodules/04-verification/solution/skill/testgen-evidence/scripts/summarize_report.py \
    .shipharness/a4/testgen/testgen-report.json
uv run python -m a4_verification.run_r8 --build teamtrack --checkpoint m1-base --feature A4
```

The testgen command runs without `--image`, so generated tests run on the host and the command
prints an UNSANDBOXED warning. The other three commands make no model calls. `--update-report`
writes the filter-6 rows into `testgen-report.json`, so the summary table counts filter 6 too;
the command's transcript and the report are the live evidence in `../live/`.

## Results

[[PENDING: summary table of the testgen run (proposed, kept, discarded per filter) and its discard reasons | source: M8 batch 1 | how: uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 --out .shipharness/a4/testgen; then summarize_report.py .shipharness/a4/testgen/testgen-report.json]]

[[PENDING: cost line printed by the testgen command | source: M8 batch 1 | how: last line of the testgen command above]]

## Filter 6 on the kept tests

[[PENDING: output of filter 6 over the kept tests (kept N of M, each duplicate with the test it copies) | source: M8 batch 1 | how: uv run python -m a4_verification.apply_filter --repo teamtrack --kept .shipharness/a4/testgen --existing <the three files above> --update-report]]

## R8 on TeamTrack

Real output of the last command above on `teamtrack/`; the full JSON document is in
`../captured/r8-teamtrack.json`.

| Field | Value |
|---|---|
| `check` | `r8_soft_delete` |
| `passed` | `false` |
| `new_violations` | 1 |
| `total_probes` | 15 |
| Finding | `R8`, `leak`, `GET /v1/issues`, `detail_key` `deleted_list` |
| `detail` | GET /v1/issues -> 200 lists soft-deleted issue(s) [1, 11]; add `deleted_at IS NULL` to the query (HANDBOOK: deleted issues are hidden from lists) |

The one finding is the legacy `/v1/issues` handler, which reads every row through
`list_all_legacy` with no `deleted_at` filter. It exists at the checkpoint, so it belongs in the
baseline: rerunning with `--baseline` set to this output gives no new violations, like the legacy
R1 leak in DESIGN §5. Every other endpoint in the OpenAPI schema answers 404 for a deleted issue or
leaves it out of its list.

## Limits

- Filters 1-3 show that a kept test builds, passed five runs, and added line coverage or killed a
  filter-set mutant (B11, F-b-17 to F-b-20; B12, F-b-32). They do not show that the test checks the
  behaviour a reviewer cares about.
- Filter 6 compares syntax trees. Two tests that check the same thing with different calls both
  stay; it removes copies, not overlap.
- R8 probes one deleted issue per endpoint with the home org's admin token. A list endpoint whose
  required query parameters filter the deleted row out by accident would hide a leak; so would a
  list longer than one page if the deleted rows were not the first ones.
- The run used one target and one model run; one run is an example, not a rate.
