# VERIFICATION

Record of what was run, what it cost, and what it showed. Every number in course material that is not
cited to a source points to an entry here. Status: in progress (milestones M3 to M5). The full
verification (M9) adds per-command costs, demo times, pilot and experiment results.

## Running totals

| Item | Used so far | Budget |
|---|---|---|
| OpenAI spend (instructor, all milestones) | about $0.0022 (M3: $0.000838 for 3 live loop smoke runs; M4: about $0.0014 for the blinded-reviewer live test, from the builder report) | experiments ≤ $25; class ≤ $2.50 |
| LangSmith traces (instructor, October 2026) | about 18 (M3: 5 probe, 3 loop smoke runs, 4 trace-link checks, 4 retention re-check; M4: about 2) | experiments ≤ 1,500; month ≤ 2,500 |

## M3 core (2026-10-16)

Branch `m3-core`. Machine: Windows 11 Pro, Python 3.12.10, uv 0.13.0; no Docker, no WSL, no make.

| Check | Command | Result |
|---|---|---|
| Unit + TeamTrack visible tests | `uv run pytest` | 347 passed, 1 skipped (symlink test: Windows lacks symlink privilege), 5 deselected (Docker) |
| Live tests | `uv run pytest -m live tests/live` | 2 passed: both keys accepted (zero model tokens); two-turn loop smoke run (below) |
| Lint | `uv run ruff check .`, `uv run ruff format --check .` | clean |
| Prose lint | `uv run python scripts/lint_prose.py` | 0 problems |
| Walkthrough anchors | `uv run python scripts/anchors.py check` | 5 anchors, 0 problems |
| Import contract (R6) | `cd teamtrack && uv run lint-imports --config .importlinter` | 2 contracts kept, 0 broken (from M4 the layers contract is named "Layers: web -> api -> services -> repositories -> db") |
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


## M5 features, datasets, checkpoints (2026-10-16)

Machine: the class host. Windows 11 Pro with WSL2 Ubuntu 26.04.1 (systemd), Docker Engine 29.9.1 inside
Ubuntu (DESIGN D-22), repository at `~/shipharness`, Python 3.12.15 (pinned by `.python-version`), uv
0.13.1.

| Check | Command | Result |
|---|---|---|
| Full suite (Linux) | `make test-all` (`pytest -n auto -m "not live and not docker"`) | 1625 passed, 0 skipped, 0 failed, 15 min |
| Real-container tests | `pytest -m docker` (images rebuilt from the final source) | 11 passed |
| Datasets | `shipharness datasets validate` (schema plus checkpoints, hidden ids, mutant sets applied at each line's checkpoint, primary measures, counts, splits) | features 60 valid, testgen 40 valid |
| Upload | `make datasets` | teamtrack-features-v1: 60 examples; testgen-targets-v1: 40 examples; a second upload is refused |
| Checkpoint tags | `scripts/build_checkpoints.py` | 8 tags on commits whose parent is the final main commit; dry run reports no recorded results |
| Mutant sets | `shipharness.filters.mutant_sets.overlaps` | no mutation in both sets: TeamTrack module and feature files, boltons, WTForms |
| Lint | ruff check, ruff format --check, prose lint, anchors (19) | clean |

Real-container results: network denial (`--network none`: no name resolution, only `lo`), read-only root,
non-root user (uid 1000), command timeout, writable arm workspace, read-only board preview mount (writes to
`/work` fail, `/tmp` works, host files unchanged), harness commands longer than the 1 s tool cap, read-only
hidden-test mount inside `/work`, image dependencies importable from container commands, board preview
reload after the arm changes `app/` plus a real board screenshot (PNG), and the referee check runner
judging TeamTrack in the referee image (R6, R7, existing tests: all pass, 21 s).

Three bugs were found only by real containers and a Linux browser, each fixed with a failing test first:
container commands ran in a login shell (`bash -lc`) whose `/etc/profile` dropped the image's venv, so
pytest, FastAPI, and the check runner were missing in every arm, gate, and referee container; the board
preview never started (`nohup HOME=/tmp ...` ran `HOME=/tmp` as the command); a long LangSmith link
overflowed its console panel with Linux fonts.

Counts: hidden tests 441 (F1 54, F2 56, F3 49, F4 69, F5 46, F6 54, F7 64; C1-C8 49). Every
(task, checkpoint) pair: 91-96% of hidden tests fail before the reference (the rest are guards), all pass
with it (independent audit, 23 pairs). Mutants: TeamTrack module files 20 (41 filter, 40 referee), feature
files 7 (14 filter, 25 referee), boltons 10 modules (22 filter, 27 referee), WTForms 10 modules (21 filter,
24 referee). Every referee mutant applies by exact text at every checkpoint it is used with and is killed by
the reference's visible tests (features, controls) or the base suite (modules); every library mutant is
killed by its recorded upstream test.

### M5 reviews

Two fresh reviewers. Code review (8074eaf..1b6eb00): ready with fixes, no critical findings. Audit of hidden
tests and mutants: no critical findings. One fix pass, each fix test-first:

| Finding | Resolution |
|---|---|
| Feature referee mutants matched by line number in files arms edit; F4 m401 failed at `m1-alt-b` | Mutants are located by their exact original text (one match per file); validation re-checks every referee mutant at every checkpoint it is used with; 10 library and 2 TeamTrack records moved to unique lines |
| Filter and referee sets shared exact and equivalent mutations across files (D-4) | Filter-side records replaced; `mutant_sets.overlaps` fails on any overlap (repository test) |
| Swap and replay re-judged against a moved tag | `ab.json` and score records pin `checkpoint_sha`; swap, replay, and referee mutants use it; `--force` refuses to move tags once results exist unless `--owner-approved-move` |
| F4 spec required test edits that the rules forbid | Owner decision: If-Match optional (412 when stale or malformed); the reference no longer edits existing tests |
| Tool calls after the harness time limit ran unchecked | Refused with a "Refused, not run" result |
| Hidden board tests over-specified markup; id allocation, 422 vs 404, hex case asserted beyond the spec | Tests relaxed or the spec states the rule (F5, F7) |
| Minors | Reviewer reserves cost; `make swap-N` hint instead of a traceback; replay continuity counts; file-level dataset checks at any line count; upload checks existing examples; gate input write cannot crash the run; tool caches excluded from working-tree exports; `testgen --target`; HANDBOOK R4 and harness docs no longer stale after F3; F7 combined test renamed; a mutant killed only by fixture errors replaced |

## M4 harness layers and tooling (2026-10-16)

Seven builders in separate worktrees from `d25df1e`, merged into `main` in the order checks, filters,
instructions, state-scope, verify, console, skills, with the full suite after each merge; no merge
conflicts. Same machine as M3 (no Docker, no WSL, no make).

| Check | Command | Result |
|---|---|---|
| Unit + TeamTrack visible tests | `uv run pytest -q -p no:cacheprovider -n 6` | 1094 passed, 6 skipped (Docker, symlink privilege, browser where Chromium is absent), 469 s |
| Lint | `uv run ruff check .`, `uv run ruff format --check .` | clean |
| Prose lint | `uv run python scripts/lint_prose.py` | 0 problems |
| Walkthrough anchors | `uv run python scripts/anchors.py check` | 19 anchors, 0 problems |
| Course skills | `uv run shipharness skills validate skills` | 4 skills, 0 errors, 0 warnings (also in `make lint`) |
| Checks against TeamTrack base | `uv run shipharness check --app teamtrack --rules R1,R2,R4,R5,R6,R7` | one R1 leak on `/v1/issues` (the documented legacy endpoint); nothing else |
| Line endings | `tests/unit/test_line_endings.py` | 0 tracked files with CRLF (69 normalized in M4) |

Integration findings fixed with a failing test first: check parameter names differed between the
referee, the gate, and the checks (`checks/params.py` plus a contract test); the verify test phase did
not reach the real filter pipeline (`test_filters_wiring.py`); referee mutants and board previews were not
wired into `run_ab` (`test_preview_and_mutants_wiring.py`); failing counts dropped when findings were
capped at 200 (`test_scores.py`).

### M4 final review

A fresh reviewer (most capable model, read-only) reviewed d25df1e..1e26849. Verdict: "not ready". It
found two critical and eight important findings. Each was reproduced by a failing test before its fix,
in one fix pass:

| Finding | Fix | Test |
|---|---|---|
| Every sandbox command was capped at the 120 s tool timeout, so the referee (asks 1,200 s) and the gate (600 s) were cut short; the visible suite alone took 120 s on this host | The cap applies to agent tool calls only (`runner/tools.py`); harness commands keep their own limits | `test_local_exec_honours_a_harness_timeout_above_the_tool_cap`, `test_docker_exec_honours_a_harness_timeout_above_the_tool_cap` |
| The gate sent `exemptions: {}` while its baseline used the adapter's exemptions, so documented legacy endpoints became new violations at every gate | Exemptions only when given; the baseline gets the gate's params | `test_gate_params_report_no_new_violations_on_the_untouched_checkpoint` (real R4 run) and two more |
| The referee ran the runner with the arm's build as working directory, so a shipped `shipharness/` package replaced it; an atexit print could forge results | `python -P`; per-run nonce in the results document | `test_a_runner_package_in_the_working_directory_is_never_imported`, `test_parse_takes_only_the_results_document_with_the_nonce` |
| Shipped tests that fail on the clean build counted as mutant kills | Only tests that pass unmutated judge mutants | `test_shipped_tests_failing_on_the_unmutated_build_never_kill_mutants` |
| The arm controlled pytest configuration and could delete existing tests unnoticed | Judge configuration restored; `regression_expected` | `test_arm_changes_to_test_configuration_are_reverted_before_judging`, `test_regression_reports_an_existing_test_the_arm_removed` |
| Swap test, replay, and experiments ignored the mutant set | One `referee_mutants` for every referee path | `test_swap_and_replay_referee_loads_the_task_mutant_set`, `test_experiment_referee_loads_the_task_mutant_set` |
| A failing preview or referee container aborted the A/B and could leave containers running | Previews skipped on failure and stopped on every path; referee start failures give a verdict | four tests in `test_preview_and_mutants_wiring.py` |
| The board preview never reloaded the arm's code | uvicorn reload on `app/` | `test_preview_server_reloads_when_the_arm_changes_its_code` |
| Diff headers with spaces (unquoted by git) broke artifact stripping | Paths from `---`/`+++`/rename lines, header split as fallback | `test_paths_with_spaces_from_real_git_diffs`, `test_renames_and_binary_files_with_spaces` |
| Removing a class's last test left an empty class and crashed the harness run | The emptied class body becomes `pass` | `test_removing_the_last_method_of_a_class_keeps_the_file_valid` |

After the fix pass: `uv run pytest -q -p no:cacheprovider -n 6` gives 1124 passed, 6 skipped; lint, prose
lint, anchors (19), and the import contracts are clean.

Not verified on this machine (no Docker): the longer referee and gate limits in a real container and
the preview reload. The M6 pilot on the class host checks both.
