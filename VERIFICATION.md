# VERIFICATION

Record of what was run, what it cost, and what it showed. Every number in course material that is not
cited to a source points to an entry here. Status: in progress (milestone M3 entries). The full
verification (M9) adds per-command costs, demo times, pilot and experiment results.

## Running totals

| Item | Used so far | Budget |
|---|---|---|
| OpenAI spend (instructor, all milestones) | $0.00 (no model calls yet; `doctor` uses `models.list`) | experiments ≤ $25; class ≤ $2.50 |
| LangSmith traces (instructor, October 2026) | 5 (M3 probe) | experiments ≤ 1,500; month ≤ 2,500 |

## M3 core (2026-10-16)

Branch `m3-core`. Machine: Windows 11 Pro, Python 3.12.10, uv 0.13.0; no Docker, no WSL, no make.

| Check | Command | Result |
|---|---|---|
| Unit + TeamTrack visible tests | `uv run pytest` | 326 passed, 1 skipped (symlink test: Windows lacks symlink privilege), 5 deselected (Docker) |
| Live key check | `uv run pytest -m live tests/live` | 1 passed (both keys accepted; zero model tokens) |
| Lint | `uv run ruff check .`, `uv run ruff format --check .` | clean |
| Prose lint | `uv run python scripts/lint_prose.py` | 0 problems |
| Walkthrough anchors | `uv run python scripts/anchors.py check` | 5 anchors, 0 problems |
| Import contract (R6) | `cd teamtrack && uv run lint-imports --config .importlinter` | 2 contracts kept, 0 broken |
| Doctor | `uv run shipharness doctor` | ready; container runtime: warning (Docker not installed) |
| TeamTrack size | OpenAPI operations / visible tests | 25 operations; 139 visible tests (design targets ≈ 25 and ≈ 120) |

Not verified on this machine (needs Docker or Linux): `tests/unit/test_sandbox_docker.py` (network
denial, read-only root, non-root user, timeout in a real container), the symlink-escape test, and the
Makefile itself (each target was run through its `uv` command instead). CI runs these on Ubuntu
(`sandbox` and `unit` jobs); the class host (Docker Desktop on WSL2) repeats them before M6.

### LangSmith live probe (RESEARCH G-13)

Command: `uv run python scripts/probe_langsmith.py` (2026-10-16). SDK `langsmith` 0.14.9. Cost: 5 traces,
no OpenAI calls. The probe dataset was deleted afterwards.

| Question | Observed |
|---|---|
| Plan of the account used | Personal organization, tier `free_10_2026`, no payment method on file |
| Invalid key | HTTP 403 from `/api/v1/sessions`; SDK raises `LangSmithError` (not `LangSmithAuthError`) |
| `@traceable` root with one child | 1 root run, 2 runs in total: one trace |
| Retention of an ordinary trace | `trace_tier: shortlived`, `ttl_seconds: 1209600` (14 days) |
| Retention of an `evaluate()` experiment run | `trace_tier: longlived`, `ttl_seconds: 34560000` (400 days), on the no-card account |
| Evaluator calls inside `evaluate()` | One root run per evaluator call in project `evaluators` (2 for 2 examples); `shortlived`, 14 days |
| One evaluator returning several scores | Works (`exact`, `diff` recorded) |
| Dataset splits | `list_examples(splits=["smoke"])` returned 2, `["section-1"]` returned 1, as tagged |
| Comparison link | `ExperimentResults.comparison_url` present |
| Tracing without `LANGSMITH_TRACING` in the environment | Off: nothing is posted. Settings reads `.env` but does not export variables, so `LangSmithTracer` now enables tracing explicitly (`tracing_context(enabled=True)`); unit test added |

Still open (needs usage-page access or a cap hit): whether experiment (long-lived) traces count against
the 5,000-trace monthly cap differently from base traces, and the exact response when the cap is
reached. Plan: read Settings > Usage after the M6 pilot and record the counts here.
