# VERIFICATION

Record of what was run, what it cost, and what it showed. Every number in course material that is not
cited to a source points to an entry here. Status: in progress (milestone M3 entries). The full
verification (M9) adds per-command costs, demo times, pilot and experiment results.

## Running totals

| Item | Used so far | Budget |
|---|---|---|
| OpenAI spend (instructor, all milestones) | $0.000838 (3 live loop smoke runs, M3) | experiments ≤ $25; class ≤ $2.50 |
| LangSmith traces (instructor, October 2026) | about 16 (M3: 5 probe, 3 loop smoke runs, 4 trace-link checks, 4 retention re-check) | experiments ≤ 1,500; month ≤ 2,500 |

## M3 core (2026-10-16)

Branch `m3-core`. Machine: Windows 11 Pro, Python 3.12.10, uv 0.13.0; no Docker, no WSL, no make.

| Check | Command | Result |
|---|---|---|
| Unit + TeamTrack visible tests | `uv run pytest` | 347 passed, 1 skipped (symlink test: Windows lacks symlink privilege), 5 deselected (Docker) |
| Live tests | `uv run pytest -m live tests/live` | 2 passed: both keys accepted (zero model tokens); two-turn loop smoke run (below) |
| Lint | `uv run ruff check .`, `uv run ruff format --check .` | clean |
| Prose lint | `uv run python scripts/lint_prose.py` | 0 problems |
| Walkthrough anchors | `uv run python scripts/anchors.py check` | 5 anchors, 0 problems |
| Import contract (R6) | `cd teamtrack && uv run lint-imports --config .importlinter` | 2 contracts kept, 0 broken |
| Doctor | `uv run shipharness doctor` | ready; container runtime: warning (Docker not installed) |
| TeamTrack size | OpenAPI operations / visible tests | 25 operations; 142 visible tests (design targets ≈ 25 and ≈ 120) |

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
| Retention of an `evaluate()` experiment run | `trace_tier: longlived`; the API reports `ttl_seconds: 34560000` (400 days). This conflicts with the docs (180 days for new extended traces from 2026-09-14); see "Extended retention re-check" below |
| Evaluator calls inside `evaluate()` | One root run per evaluator call in project `evaluators` (2 for 2 examples); `shortlived`, 14 days |
| One evaluator returning several scores | Works (`exact`, `diff` recorded) |
| Dataset splits | `list_examples(splits=["smoke"])` returned 2, `["section-1"]` returned 1, as tagged |
| Comparison link | `ExperimentResults.comparison_url` present |
| Tracing without `LANGSMITH_TRACING` in the environment | Off: nothing is posted. Settings reads `.env` but does not export variables, so `LangSmithTracer` now enables tracing explicitly (`tracing_context(enabled=True)`); unit test added |

### Extended retention re-check (2026-10-16)

Re-run on request because the API value conflicts with the docs. One fresh experiment run (created 2026-10-16 06:06 UTC); probe dataset and projects deleted afterwards; 3 traces.

| Source | Value |
|---|---|
| LangSmith docs, administration overview and billing pages (fetched 2026-10-16) | "Starting September 14, 2026, the maximum long-lived trace retention period for SaaS customers is changing to 180 days." Extended traces: 180 days by default |
| Account retention settings, `GET /api/v1/ttl-settings` | `default_trace_tier: shortlived`, `longlived_ttl_days: null` (no custom value) |
| Experiment run, `GET /api/v1/runs/{id}` | `trace_tier: longlived`, `ttl_seconds: 34560000` (400 days) |
| Experiment project and a new plain project, `GET /api/v1/sessions/{id}` | `trace_tier: shortlived` (project default; experiment runs are upgraded individually) |

Conclusion: the account's API reports a 400-day TTL on new experiment runs while the docs state 180 days. Which one LangSmith enforces cannot be observed until a run expires. Course material and planning use the documented 180 days (the shorter value) and do not claim 400. Reports read `exports/`, so neither value affects them. To re-check: open an experiment run created on or after 2026-10-16 after 2027-04-14 (day 180).

Still open (needs usage-page access or a cap hit): whether experiment (long-lived) traces count against
the 5,000-trace monthly cap differently from base traces, and the exact response when the cap is
reached. Plan: read Settings > Usage after the M6 pilot and record the counts here.

### Live agent-loop smoke test

Command: `uv run pytest -m live tests/live/test_loop_live.py -s` (2026-10-16). Model `gpt-6-luna`,
effort `low`, bare arm, LocalSandbox (UNSANDBOXED; Docker not installed), task: read `app.py` and finish.
Run three times; every run: `status=completed`, `claim=done`, 3 turns, file unchanged, trace link present
on the second and third runs.

| Turn | Input tokens | Cached | Cache write | Output | Reasoning |
|---|---|---|---|---|---|
| 1 | 745 | 0 | 0 | 22 | 0 |
| 2 | 780 | 0 | 0 | 29 | 0 |
| 3 | 852 | 0 | 0 | 32-33 | 0 |

Cost per run: $0.000279-$0.000280 (CostTracker, verified prices). No caching: the prompt is below the
1,024-token minimum. Reasoning tokens are 0 at effort `low` for this task. This confirms function
calling with `strict` schemas, stateless replay (`store=False`), usage field names, cost recording, and
LangSmith tracing of a real run; it does not measure realistic per-run cost, which M6 does.

Finding: the first run returned no trace link (LangSmith's link lookup failed transiently and the tracer
returns None rather than failing the run). The loop now retries the lookup at the end of the run; unit
test `test_trace_link_is_retried_at_the_end_when_unavailable_at_start`.

### M3 final review

Fresh reviewer (most capable model) on 7b616cf..5c3bc92: verdict "with fixes". Three critical findings,
all reproduced by failing tests before the fix and fixed in commit 970698f:

| Finding | Fix | Test |
|---|---|---|
| Host-side git honoured agent-set `.git/config` (`core.fsmonitor`, filters), executing commands outside the sandbox | `files_changed` by hashing files without git; diffs via a temporary git dir with clean config and the workspace objects as alternates | `test_files_changed_snapshot_does_not_run_agent_git_config`, `test_write_diff_does_not_run_agent_git_config` |
| `search` read files through a link out of the workspace; `list_dir` crashed on it | Never follow symlinks or junctions in host-side tools; refuse a linked `.git` | `test_search_does_not_follow_links_out_of_the_workspace` and two more |
| Non-UTF-8 output crashed the Docker path; diffs re-encoded bytes | Bytes in, UTF-8 with replacement for tool output; raw bytes for diffs | `test_docker_exec_decodes_non_utf8_output_without_crashing`, `test_write_diff_keeps_non_utf8_bytes_exactly` |

Seven important findings were fixed the same way (loop exception safety, redaction over-matching, key
masking in tool output and run logs, board validation, discovery of unauthenticated endpoints, tool-log
file names from model-chosen ids, class-date default). Thirteen minor findings are deferred and listed in
the M3 hand-off.
