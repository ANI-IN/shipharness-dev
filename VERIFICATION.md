# VERIFICATION

Record of what was run, what it cost, and what it showed. Every number in course material that is not
cited to a source points to an entry here. Status: in progress (milestones M3 to M6). The full
verification (M9) adds per-command costs, demo times, pilot and experiment results.

## Running totals

| Item | Used so far | Budget |
|---|---|---|
| OpenAI spend (instructor, all milestones) | $1.8555 (cost ledger, read 2026-10-17 after run 4; opening entry: M3-M4 $0.0022 before the ledger existed; M6 pilot $1.4377: $0.0183 smoke run, $0.4415 run 1, $0.3966 run 2, $0.0278 console check, $0.3801 run 3, $0.1734 run 4; parallelism attempts $0.4155, counted against experiments; key check $0.000004) | total build ≤ $15 (enforced on every call), $13.14 left; pilot ≤ $10 and 96 arm runs (94 used); class ≤ $2.50 |
| LangSmith traces (instructor, October 2026) | 271 since 2026-10-01 (LangSmith API, read 2026-10-17 after run 4: `shipharness-pilot` 164; `shipharness-class-2026-10-16` 99 = M6 smoke run 3, run 1 48, run 2 48; `shipharness-dev` 5; `evaluators` 3) | LangSmith limit 5,000 per month; overnight limit 2,500; DESIGN budget: experiments ≤ 1,500 |

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


## M6 pilot (2026-10-16)

Machine: the class host (see M5). Model gpt-6-luna, reasoning effort medium, both arms. Command:
`scripts/pilot.py --k 3 --effort medium --parallel 2` (each A/B runs `shipharness ab --section demo-N
--feature FN --no-preview`; 2 A/Bs at a time). Pilot cap: up to 72 arm runs (raised to 96 by the owner on 2026-10-17) and $10 in total, on top of
the per-arm cap. Primary measures are the pre-registered ones (DESIGN §10); no pilot change touches them.

### GitHub

The repository was created private by the owner's choice (2026-10-16), first as `ANI-IN/shipharness`, then
renamed `ANI-IN/shipharness-dev` (private). History check before the first push: no tracked `.env`; the
real key values do not occur in any commit (hash comparison; two test blobs hold placeholder strings); one
identity on every commit; no attribution lines. At this entry `origin/main` is 334483d (205 commits) with 9
tags (`m1-base` and the 8 checkpoint tags). An earlier chat statement that `origin/main` already held the M1
commit was wrong (the repository did not exist yet); no entry in this file carried that claim.

### Smoke run

One A/B (F1, `ab-20261016-163551`), $0.0183, 3 traces. The harness arm ended `ERROR` with zero turns: on the
live path the layer registry was empty because no code imported the layer modules.

### Run 1 (before the fixes below)

12 A/Bs (F1-F4, k=3), 24 arm runs, $0.4415 (agents and reviewer; cost ledger, 16:49:25-18:17:36),
48 traces (distinct trace links in the run logs). A/B wall time 466-875 s.

| Section | Arm | Primary passed | Agent time limit hit | Agent time (s) | Harness time (s) | Patches failed |
|---|---|---|---|---|---|---|
| F1 | bare | 3/3 | 0/3 | 173-258 | 0 | 27/29 |
| F1 | harness | 3/3 | 0/3 | 175-189 | under 1 | 20/21 |
| F2 | bare | 3/3 | 0/3 | 149-259 | 0 | 22/25 |
| F2 | harness | 3/3 | 3/3 | 314-342 | 91-129 | 13/13 |
| F3 | bare | 0/3 | 0/3 | 202-318 | 0 | 48/52 |
| F3 | harness | 0/3 | 2/3 | 279-334 | 50-80 | 22/22 |
| F4 | bare | 0/3 | 0/3 | 174-266 | 0 | 41/49 |
| F4 | harness | 0/3 | 2/3 | 280-344 | 57-132 | 24/26 |

Gate: not met (no section with the harness arm ahead; F1 and F2 without a gap; F3 and F4 fail in both arms).
The F2 and F3 results are not valid measurements: F2 because of change 2 below, F3 because of changes 5
and 6 (every F3 arm reported 4 out-of-scope files; they were the import linter's cache).

### Pilot-driven changes

Every change the pilot caused, before the next run. Label: "bug fix, applies to both arms" or "task/effort
change". Primary measures unchanged.

| # | Change | Label | Reason | Revealed by | Commit |
|---|---|---|---|---|---|
| 1 | The default layer registry imports the layer modules | bug fix, applies to both arms (the bare arm loads no layers, so its runs were unaffected) | Harness arm could not start on the live path | Smoke run `ab-20261016-163551` | e4e8d04 |
| 2 | Session patches come from working-tree snapshot trees, not commits | bug fix, applies to both arms | An arm that never commits could not fail part (c) of the S2 measure | Run 1, F2 (bare arms make no commits) | b1cdb8d |
| 3 | Referee baseline runs while the arms work and is cached per task | bug fix, applies to both arms (speed only; no measurement change) | A/B wall time 466-875 s against the 6-minute target; the baseline ran after the arms, about 70 s | Run 1, all sections | 02204bb |
| 4 | `apply_patch` accepts the `*** Begin Patch` format and unified hunks without line numbers or with wrong counts (CONTRACTS §23) | bug fix, applies to both arms | 217 of 237 patches failed (92%): the model writes the anchored format, the tool required strict unified diffs; wasted turns explain most agent time limits | Run 1 traces, for example `ab-20261016-170314-4a3b4b` (harness: 8 of 9 patches failed, no feature code at the end) | 7aaac10 |
| 5 | `.import_linter_cache` treated as generated (diff, scope snapshots, clean-state check) | bug fix, applies to both arms | 4 cache files counted as out-of-scope files and test-phase source edits in every arm; the scope layer reverted them after every lint run and reported a block to the agent | Run 1, F3 (every arm: `out_of_scope_files` 4) | 7aaac10 |
| 6 | Test-phase files come from the test sessions' snapshot trees | bug fix, applies to both arms | Comparing with HEAD at the start of the test phase counted an uncommitted build phase as test-phase source edits (S3 measure) | Run 1, F3 (bare: `app/api/issues.py` and `app/services/issues.py` counted as test-phase edits) | 7aaac10 |

After the fixes: fast suite on `main` (a5cbc5a) 1575 passed; images rebuilt from that source before run 2.

### Run 2 (after changes 1-6)

12 A/Bs (F1-F4 canonical, k=3, effort medium), 24 arm runs, $0.3966 (pilot summary; cost ledger),
48 traces, two A/Bs in parallel, 18:17-19:27. Patches: 9 of 202 failed (run 1: 217 of 237).

| Section | Arm | Primary passed | Agent time limit hit | Agent time (s) | Harness time (s) | Why it failed |
|---|---|---|---|---|---|---|
| F1 | bare | 3/3 | 0/3 | 171-193 | 0 | (passed: no new R1 violation) |
| F1 | harness | 3/3 | 0/3 | 127-177 | under 1 | (passed) |
| F2 | bare | 3/3 | 0/3 | 215-242 | 0 | (passed: no continuity failure) |
| F2 | harness | 0/3 | 1/3 | 265-303 | 54-64 | continuity failure measured on harness files only (change 7): session 1 added only progress.md, session-handoff.md, and the exec plan; session 2 rewrote them (50-84% of session 1's lines) |
| F3 | bare | 3/3 | 0/3 | 168-243 | 0 | (passed: 0 out-of-scope files, 0 test-phase source edits) |
| F3 | harness | 3/3 | 0/3 | 232-291 | 51-113 | (passed) |
| F4 | bare | 0/3 | 1/3 | 225-310 | 0 | mutants killed 3, 4, 3 of 4 with hidden tests 69, 66, 69 of 69 (the measure needs all of both) |
| F4 | harness | 0/3 | 2/3 | 269-314 | 101-132 | shipped 0, 0, 3 tests, so mutants killed 0, 0, 2 of 4 (hidden 69, 61, 69 of 69); no test written in the 12-turn test phase survived the filters: in `ab-20261016-191626-6100f6` the 3 shipped tests were written in build session 1 and the test phase's one new test was discarded (corrected 2026-10-17 after the content audit) |

Gate: not met (F1, F3 without a gap; F2 reversed by a measurement bug; F4 failed in both arms).

Wall time per A/B (first event to last verdict): min 485 s, median 641 s, max 923 s; 12 of 12 over
the 480 s live-demo limit. Median split per arm: setup 1 s; agent turns 237 s (harness arms 267 s);
harness overhead 0 s (harness arms 64 s); gate 0 s (no arm claimed done, so no gate ran); referee 331 s
from the arm's end to its verdict, including the wait for the other arm (checks 148 s, of which
flakiness 87 s; mutants 81 s, of which the one-process-per-test unmutated pass step is most; reviewer
20 s). Estimates from these logs (median / max / over 480 s): judge each arm when it ends 541 s / 779 s
/ 10 of 12; plus a batched unmutated pass step (batch assumed 30 s) 506 s / 609 s / 7 of 12. Class
choreography check: the slowest A/B finished at 15.4 min, so every A/B would be complete by about
minute 19 of a section that starts with a 3-minute poll.

Harness arm turn use (run 2 logs): every session repeated the getting-up-to-speed steps, re-read 3 to 7
instruction documents and about 15 product files, and updated progress.md and the exec plan mid-session.
F2 harness arms made 0 to 1 product patches in 50 build turns.

### Pilot-driven changes after run 2

Logged before run 3. Primary measures unchanged.

| # | Change | Label | Reason | Revealed by | Commit |
|---|---|---|---|---|---|
| 7 | The continuity check reads session patches with harness artifacts stripped | bug fix, applies to both arms | The state layer rewrites progress.md, session-handoff.md, and the exec plan every session; the check scored that as session 2 removing 50-84% of session 1's lines in every F2 harness arm | Run 2, F2 (`ab-20261016-181736-08a9c4`, `...-184318-636e90`, `...-190548-ae9abe`) | d39dbf0 |
| 8 | Overhead cuts: init.sh runs one end-to-end visible test file; the session start reads the handoff's visible-test status; the gate baseline is cached per checkpoint commit | harness change, harness arm only | init.sh (about 44 s) and run_visible_tests (about 36 s) ran the full visible suite twice per session start, as agent time | Run 1 harness arms (881 s over 6 A/Bs) | 3b63ca6 |
| 9 | Turn cost: the handoff's agent notes before any document; progress, exec plan, and handoff only in the wrap-up turns; the wrap-up records the rules that matter; the handoff lists documents read; a test-phase session starts with the feature's tests | harness change, harness arm only | Every session re-read 3-7 instruction documents and about 15 product files and updated state files mid-session; F2 harness arms made 0-1 product patches in 50 build turns; F4 harness arms shipped 0, 0, 3 tests, none of them from the test phase | Run 2, F2 and F4 | 37d0503 |
| 10 | Each arm is judged as soon as its run ends | measurement change, both arms, no outcome change | The faster arm waited for the slower one before judging (median 331 s from an arm's end to its verdict) | Run 2 wall times | 2539342 |
| 11 | The unmutated-pass step before referee mutants runs all shipped tests in one pytest process (per-test outcomes from `-rA`; an id without an outcome runs on its own) | measurement change, both arms, no outcome change | One container command per shipped test (about 7.5 s each; up to 245 s on F4) | Run 2 mutant timings | 2539342 |
| 12 | Cost caps hold across concurrent commands (trackers read each other's ledger entries; writes take a file lock) | bug fix, applies to both arms | Each command counted only its own spend against the shared session, experiment, and build caps; the pilot runs parallel A/Bs, and the class plan launches demo-4 and final together | Owner's class plan (2026-10-17), pilot parallel A/Bs | 660a656 |
| 13 | Run 3 tasks: F1 `trap-legacy-pattern`, F3 `trap-tempting-middleware`, F2 `stop-1` (first session 13 turns, pending confirmation) | task/effort change | F1 and F3 showed no gap in run 2; F2 lever (c) | Run 2 per-section results; pre-registered in DESIGN §10.4 | 7dbafeb (pre-registration), b1da06e (`pilot.py --variants`) |

Equivalence check for change 11 (owner condition): every run 2 arm that shipped tests was rebuilt
as the referee judged it (checkpoint commit plus product diff, judge config restored) and each
shipped test ran once on its own and once in the batch, in the referee image. 17 arms, 181 tests:
the pass or fail outcome was identical for every test (7 tests fail in both modes); every test had a
batched outcome, so the fallback did not run. Time: 1,172 s isolated against 131 s batched (largest
arm: 254 s against 13 s). Script: scratchpad `equivalence.py`; result kept at
`.shipharness/pilot/equivalence-run2.json` (private build repo).

After changes 7-13: full suite on `main` (5f1c6ab, `pytest -n 8 -m "not live and not docker"`): 1705 passed, 1 skipped
(the freeze test, no tag yet), 1 failed (`test_makefile` pinned the old `FEATURES` default; fixed in
9fd8273); after merging the assignments and the live-client guard (89b4f31): fast suite 1646 passed, 1
skipped. Images rebuilt from that source before run 3.

### Run 3 (pre-registered levers, after changes 7-13)

12 A/Bs, 2026-10-16 21:14-22:07 (WSL clock), two A/Bs in parallel, effort medium, `--purpose pilot`
(traced to `shipharness-pilot`), $0.3801 (pilot summary), referee version 2026-10-17 code minus the
version stamp (merged after the run). Tasks: F1 `trap-legacy-pattern`, F2 canonical with
`--session-budget 12,38`, F3 `trap-tempting-middleware`, F4 canonical. Content subagents worked on the
machine during the run (documentation only; one ran the A2 grader tests for about 5 minutes near the end),
so the last A/Bs may be slightly slower.

| Section | Arm | Primary passed | Agent time limit hit | What happened |
|---|---|---|---|---|
| F1 trap | bare | 3/3 | 0/3 | no new R1 violation in any arm; the legacy `/v1` handler was not copied into a leak |
| F1 trap | harness | 3/3 | 0/3 | same |
| F2 12/38 | bare | 3/3 | 0/3 | no continuity failure; the bare arm resumed and finished across the 12-turn stop |
| F2 12/38 | harness | 3/3 | 2/3 | no continuity failure, but in `ab-20261016-213317-9a0ec1` and `ab-20261016-214959-de790f` the harness arm called `finish(claim="not_done")` at the end of the 12-turn first session, which ended the build phase: the 38-turn session never ran and the feature was not built (hidden tests 3/56) |
| F3 trap | bare | 3/3 | 0/3 | 0 out-of-scope files, 0 test-phase source edits; `app/api/middleware.py` untouched |
| F3 trap | harness | 3/3 | 1/3 | same |
| F4 | bare | 0/3 | 3/3 | every bare arm hit the agent time limit (hidden 66, 66, 69 of 69; mutants killed 4, 0, 3 of 4) |
| F4 | harness | 0/3 | 2/3 | shipped no tests in any run (mutants killed 0 of 4 each); `ab-20261016-212252-aa1644` built a broken change (hidden 27/69, 3 new R1 violations); the test phase was cut by the time limit in two runs |

Classification under the overnight rules ("harness ahead" = more primary passes than bare out of 3, not
caused by harness-only timeouts): F1 no gap, F2 no gap, F3 no gap, F4 no gap (both 0/3).

Wall time per A/B: min 384 s, median 512 s, max 620 s; 10 of 12 over 480 s (run 2: median 641 s, max
923 s, 12 of 12). Median per arm: agent 248 s (harness arms 291 s), harness overhead 60 s on harness arms,
referee 227 s from an arm's end to its verdict (run 2: 331 s), gate 0 s (no done claim reached the gate).

### Overnight decisions after run 3

- Run 4 (pre-registered fallback, effort `low` for both arms, k=3) runs for F1, F2, and F3 only, with the
  run-3 tasks. Reason: all four sections show no gap, but four sections at k=3 is 24 arm runs and 76 of
  the 96-run pilot cap are used; F4 is left out because its bare arm already fails at medium effort and
  its harness arm fails by shipping no tests within the time limit, which lower effort is the least
  likely of the four to change. Run 4 brings the pilot to 94 arm runs.
- RUN_TIMEOUT_S: the harness arm still hits the agent time limit after the overhead cuts (run 3: 5 of 12
  harness arms; 3 of 12 bare arms), which meets the condition of the owner's timeout rule; raising it is
  not part of the pre-registered run 4, so it is not changed tonight and goes to the owner's options note.
- The F2 harness early finish is a harness-arm design issue (the wrap-up message leads the agent to call
  `finish`, which ends the phase); not changed tonight (outside the pre-registration); options note.

### Referee determinism check (2026-10-16 22:14-22:22, WSL clock)

`scripts/pilot.py --determinism 10 --ab ab-20261016-212252-aa1644` (pilot run 3, F4; the bare arm shipped
23 tests, so flakiness, the batched unmutated-pass step, and the referee mutants all ran): the recorded
A/B judged 10 times by the merged referee (main cd2fa43), no reviewer, no model calls. For each arm, all
10 score records are identical in every scored field (hidden tests, mutants, flakiness, regression,
continuity, scope, R1-R7, board, primary measure). The only differing field was `captured_at`, the write
time, which the comparison did not yet treat as volatile (fixed test-first, fa26596; recomputed from the
same 10 records: bare 10 of 10, harness 10 of 10). Result: the referee is deterministic for this build
(gate condition 3 passes). Exports: `exports/determinism/`.

First parallelism attempt (invalid): `pilot.py --parallel 3` and `--parallel 4` with `--budget 1.0`; the
pilot's budget guard reserves each A/B's worst case ($0.48) before launching, so only two A/Bs ran at
once in both attempts (A/Bs `ab-20261016-222356-*`, `-223055-*`, `-223814-*`, `-224528-*`,
`-225058-*`). Repeated with `--budget 2.5`. Cost of the invalid attempt: in the ledger, counted against the
experiment budget as approved. WSL's `/tmp` was cleared at 23:02 (no reboot); the run 3 and determinism
console logs there were lost; the results are kept in `.shipharness/runs`, `exports/`, and the pilot
summaries in `.shipharness/pilot/`.

### Parallelism test (2026-10-16 23:03-23:24, WSL clock)

`scripts/pilot.py --parallel 3 --budget 2.5` (F1-F3, one A/B each: `ab-20261016-230306-48c2b2`,
`-6f74f4`, `-d698c9`), then `--parallel 4` (F1-F4: `ab-20261016-231208-18ad4b`, `-217016`, `-6a76c2`,
`-76f91d`), effort medium, run-3 tasks. A sampler logged free memory, load, and containers every few
seconds (`.shipharness/pilot/partest/`). Cost $0.0798 and $0.1241 (pilot summaries), counted against the
experiment budget as approved. Reliability criteria (set before the test): agent and container command
times no more than about 10% longer than at 2 in parallel (run 3), no extra timeouts or errors, no OOM,
at least 1.5 GB free, load below 8.

| Setting | Visible-test command median, same feature (s) | Agent median, same feature (s) | Timeouts | Min free memory | Max load | Containers | Wall |
|---|---|---|---|---|---|---|---|
| 2 (run 3) | F1 26.7, F2 26.8, F3 26.8, F4 29.9 | F1 195, F2 270, F3 197, F4 318 | 8 of 24 arms | not sampled | not sampled | 4 | 384-620 s per A/B |
| 3 | F1 20.1, F2 23.4, F3 20.8 | F1 165, F2 239, F3 184 | 0 of 6 | 5,346 MB | 6.44 | 6 | 543 s |
| 4 | F1 19.8, F2 36.2, F3 25.1, F4 46.9 | F1 174, F2 316, F3 211, F4 284 | 2 of 8 (both F2 arms) | 4,799 MB | 9.2 | 8 | 661 s |

Command times count executed commands only; calls the tool refused before running (an invalid test
selector, 0 ms: 15 at 2, 2 at 3, 4 at 4) are left out. All executed container commands pooled (`run` and
`run_visible_tests`): median 8.6 s at 2, 11.1 s at 3, 13.5 s at 4; p90 30.4, 27.7, 36.4 s. The samples at 3
and 4 are small (one A/B per feature; 34 and 56 commands).

Decision: **3 A/Bs in parallel** for M8. Reason: at 3 there were no timeouts, no errors and no OOM, at least
5.3 GB stayed free, load peaked at 6.44, and the same command on the same feature (visible tests) ran no
slower than at 2, with agent times lower in all three features. The pooled command median at 3 is 29% above
2, which on its own misses the 10% criterion; I judged by the same-command comparison because the pooled
mix differs (F1-F3 only at 3, F4's long commands in run 3). Cost if wrong: M8 arms run slower than the
pilot's, so more agent time limits could be hit; the M8 report gives timeouts per arm, which shows it. At
4 the load exceeds 8, visible tests take 35% (F2) and 57% (F4) longer than at 2, and both F2 arms hit the
agent time limit. `.wslconfig` not
changed (memory was never the limit). Expected M8 duration at 3 in parallel, if the gate passes: batch 1
(40 A/Bs) about 14 rounds of about 9 minutes, about 2 h 10 min; ablation (32 harness-arm runs) about 11
rounds of about 6-7 minutes, about 1 h 15 min; about 3.5 h in total. Projected cost from run 3 ($0.032
per A/B at medium): batch 1 about $1.27, ablation about $0.50 (reviewer off).

### Run 4 (pre-registered fallback: effort low, F1-F3)

9 A/Bs, 2026-10-16 23:28 to 2026-10-17 00:01 (WSL clock, UTC), two A/Bs in parallel, effort `low` for
both arms, run-3 tasks (F1 `trap-legacy-pattern`, F2 canonical with `--session-budget 12,38`, F3
`trap-tempting-middleware`), `--purpose pilot`, referee version 2026-10-17. Command: `scripts/pilot.py
--features F1,F2,F3 --k 3 --effort low --parallel 2 --budget 2.0 --variants
F1=trap-legacy-pattern,F3=trap-tempting-middleware --budgets F2=12/38`. Cost $0.1734 (projected about
$0.29 before the run). Pilot total after run 4: 94 of 96 arm runs.

| Section | Arm | Primary passed | Agent time limit hit | Hidden tests (per A/B) | What happened |
|---|---|---|---|---|---|
| F1 trap | bare | 3/3 | 0/3 | 52, 52, 52 of 52 | no new R1 violation |
| F1 trap | harness | 3/3 | 0/3 | 52, 52, 52 of 52 | same |
| F2 12/38 | bare | 3/3 | 0/3 | 3, 3, 3 of 56 | no continuity failure, but no arm built the feature: 20-24 turns, 56-69 s of agent time (`ab-20261016-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9`) |
| F2 12/38 | harness | 3/3 | 1/3 | 56, 3, 56 of 56 | no continuity failure; built the feature in 2 of 3 |
| F3 trap | bare | 3/3 | 0/3 | 49, 49, 49 of 49 | 0 out-of-scope files, 0 test-phase source edits |
| F3 trap | harness | 3/3 | 0/3 | 49, 49, 49 of 49 | same |

Wall time per A/B: min 309 s, median 414 s, max 565 s; 2 of 9 over 480 s. Median agent time: bare 109 s,
harness 154 s; harness overhead 67 s on harness arms.

F2 across runs 3 and 4 (secondary, hidden tests 56 of 56): run 3 bare 3 of 3, harness 1 of 3; run 4 bare
0 of 3, harness 2 of 3. The primary measure (`continuity_failure`) passed in all 12 F2 arms, including the
6 that built nothing (hidden 3 of 56: run 3 harness `ab-20261016-213317-9a0ec1`, `-214959-de790f`; run 4
bare in all three A/Bs, harness `ab-20261016-234027-226a76`): it cannot fail when session 1 leaves no product lines to redo. Primary measures are
not changed under the pilot rules; this goes to the owner's options note.

### Gate decision (overnight rules, applied mechanically)

| Section | Run 3 (medium) bare / harness | Run 4 (low) bare / harness | Classification |
|---|---|---|---|
| F1 | 3/3, 3/3 | 3/3, 3/3 | no measurable difference |
| F2 | 3/3, 3/3 | 3/3, 3/3 | no measurable difference |
| F3 | 3/3, 3/3 | 3/3, 3/3 | no measurable difference |
| F4 | 0/3, 0/3 | not run (pilot cap) | no measurable difference |

"Harness ahead" in 0 of 4 sections (the gate needs 3 of 4). Determinism passed. Result: **gate not
passed**. Under the overnight rules: no `harness-frozen` tag, no M8, no further OpenAI spending tonight;
an options note goes to the owner. Per the pre-registered outcome rule, F1-F3 are reported as "no
measurable difference on this task with this model". F4 had no run 4 (reason in "Overnight decisions
after run 3"); it is classified on run 3, where both arms failed 3 of 3.

Release dry run after the gate (`scripts/make_release.py --dry-run`, HEAD 6ab41ec): 741 public files;
leak check PASS; 176 broken references in 32 files (100 in `slides/outline.md`; mostly "DESIGN §" and
"RESEARCH §" citations); frozen content PASS against a record from HEAD (no tag yet). Finding: the 8
rebuilt checkpoint tags differ from the build repository's tags in `teamtrack/`, in one file:
`teamtrack/reference/checkpoints.toml`, comment line 3, changed by 20c66c1 (private-reference cleanup)
after the tags were built. The file is not part of any arm workspace or score, and no freeze tag exists, so
no result is affected. Not fixed tonight: moving tags that have results needs the owner's approval, and
reverting the comment puts a private script name back into a public file. Owner decision.

### Changes after the gate (owner instructions 2026-10-17, `instructor/engineering-notes/focus-2026-10-17.md`)

Round 5 (the pre-registered k=3 round with an F1 monolithic-instructions bare arm, an F2 round-only
measure, and a longer F4 time limit) was planned and then dropped by the owner's FOCUS message ("No new
experiments beyond what's listed here") before any of it was built or run. The one remaining data run is
the class-profile round (1 A/B per section).

| # | Change | Label | Reason | Revealed by | Commit |
|---|---|---|---|---|---|
| 14 | Before the last build session, `finish(claim="not_done")` ends only that session; the next session starts as after a spent turn budget (the last build session and the test phase keep the old rule) | bug fix, applies to both arms | Arms of both arms gave up the build phase at the end of a 12-turn first session; session 2 never ran | Run 3 F2 harness (`ab-20261016-213317-9a0ec1`, `-214959-de790f`); run 4 F2 bare in all three A/Bs (`ab-20261016-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9`) and harness `-234027-226a76` (sessions ended `claim_not_done` after 9-12 turns) | 501be88 |
| 16 | Early primary verdict: the referee runs the checks the task's primary measure needs first and emits `primary_verdict` per arm; secondary checks follow; the console shows "primary verdict ready" and the time from launch to each verdict | measurement change, both arms, no outcome change (25 scenarios, F1-F5 green/red/broken/runner down, judged in both orders: every scored field equals records made by the unchanged code; fake containers) | Owner's class profile: show the primary result as soon as it is known | Owner request 2026-10-17 | 76ff2ca |
| 17 | Flakiness re-runs of shipped tests: 5 instead of 10 (TestGen-LLM's "five executions", B11, F-b-19) | measurement change, both arms, secondary only (`flaky_tests`); `REFEREE_VERSION` not raised, so screen 4 keeps showing the pilot records; `flaky_tests` before 2026-10-17 counts 10 re-runs | Owner's class profile (speed) | Owner request 2026-10-17 | 76ff2ca |
| 18 | Class profile (`--profile class`, the default for `make demo-N`, `make final`, `make show-N`): effort low for both arms; arm, referee, and preview containers limited to 2 CPUs; agent model calls at OpenAI's Fast tier, each call priced by the tier the response reports (reservation at the requested tier); the reviewer keeps its settings. Pilot and experiment runs keep the standard profile unless asked | class profile only (identical for both arms; primary measures unchanged) | Owner: make live class runs fast | Owner request 2026-10-17; Fast tier verified live the same day (requested `fast`, response `fast`; 2 calls, $0.000011) | 3f5a7c7 |
| 19 | A dataset line without `steps` lets the state and scope layers take the ticket's bullet lines or its title (an empty list had given a feature list and exec plan with no steps in every harness arm of the pilot) | bug fix, harness arm only (only harness layers read it) | Every harness arm of the pilot got `"steps": []` | Kit builder, 2026-10-17 | 10f0830 |
| 20 | `testgen --layers verify` on a repository that is not TeamTrack: the visible-test directory comes from the run (`--tests` folder or `--visible-tests`; TeamTrack keeps `tests/visible`), the migration-head check runs only with an Alembic configuration, `run_visible_tests` accepts the run's directory, and one filter run records every evaluated test (the summary had said "kept 0 of 0") | bug fix, applies to both arms (`run_visible_tests` and the prompts are shared runner code); TeamTrack runs unchanged | The starter kit's worked example (boltons) failed every gate on `tests/visible` and `alembic heads`; the agent committed a fake Alembic setup to pass | Kit worked-example testgen run `r-20261017-095514-ac8f1c` | 4343a23 |
| 21 | The gate's clean-state ruff check uses ruff's documented default rule set (`E4,E7,E9,F`) when the repository has no ruff config of its own | bug fix, harness arm only (the verify layer's gate); no recorded outcome changed: no F4 or final harness arm in the pilot or the class-profile round claimed done, so no gate ran there | ruff 0.17.1 in the agent image also enables B008 and I001; TeamTrack's unchanged `app/api/issues.py` fails B008 (FastAPI `Depends` defaults), so any change to a router file failed the clean-state item | Examples builder, 2026-10-17; confirmed in the agent image (pinned rules: exit 0) | 37d9519 |
| 22 | Constructed examples (`make example-N`, scripted steps, no model, CONSTRUCTED EXAMPLE badge, never counted as a run) | tooling, optional extras only (owner message 7) | Show each layer catching its mistake at $0 outside the demo flow | Owner request 2026-10-17 | 32dc378 |
| 23 | No container outlives `run_ab`: after the 10 s wait, a board preview still running is stopped; a failed or timed-out `docker run` removes its container; the referee baseline thread is joined before `run_ab` returns or raises; an exit hook removes any container still running | bug fix, applies to both arms (shared code; nothing the arms see or are scored on changes) | `make show-4` (`ab-20261017-100107-4c2be8`) left its harness arm's board preview container running for an hour: the F4 conflict capture outlived the 10 s join and the CLI exited before the preview's `finally` ran | Live command check, 2026-10-17 | cdadf31 |
| 24 | Class profile agent time limit 420 s for both arms (standard profile 300 s); recorded per arm spec | class profile only (pre-registered in DESIGN §10.4 before use) | Harness arms were cut at 300 s in class runs; 420 s keeps the slowest A/B within the 25-minute window | Class-profile round, class commands re-timed | e15eae1 |
| 25 | `make doctor` and `make warm` check SHIPHARNESS_CLASS_DATE when PURPOSE=class (doctor: failed item; warm: exit 2 before any work), with the .env line and export command in the message | tooling | Class runs trace to `shipharness-class-<date>` and need the date set explicitly | Owner message 9.4 | e15eae1 |
| 26 | Tests are colour- and width-independent (session fixture: NO_COLOR, TERM=dumb, COLUMNS=200, typer colour off); CI conditions reproduced in a test; CLI help header "Module 1: Harness Engineering for Coding Agents"; release contributor check (section 8) and `check_contributors.py` (461 commits, all ANI-IN) | tooling | CI on shipharness-dev failed on ANSI colour codes in typer help; owner messages 10.3, 11, 12.1 | CI runs on c288c28, d67f8be | e15eae1 |
| 15 | Checkpoint comment in `teamtrack/reference/checkpoints.toml` stays neutral; the 8 checkpoint tags are rebuilt (owner approval: "Neutral text, move tags") | tooling, no outcome change (arm workspaces exclude `reference/**`; results stay pinned by `checkpoint_sha`) | Release rebuilt tags differed from the build tags in that one comment line | Release dry run 2 | tags moved 2026-10-17 with `scripts/build_checkpoints.py --force --owner-approved-move` on main 52b0546: m1-s1-start e72a414 -> c63e4c5, m1-s2-start a0f781e -> 393b295, m1-s3-start 7b05657 -> b974a67, m1-s4-start f8be763 -> a9d6be2, m1-final-start 48d4102 -> d14a46e, m1-complete 39409b0 -> b6490ae, m1-alt-a a06029b -> 724a052, m1-alt-b 1a6ed5f -> 2514505; in all 8 the `teamtrack/` tree differs only in `reference/checkpoints.toml`; the old commits stay reachable under `refs/archive/checkpoints-2026-10-16/<tag>` so recorded `checkpoint_sha` values still resolve |

F4 test phase (investigated, no bug): in run 3 the harness arms proposed no tests because the test session
was cut short, not because tests were lost. `ab-20261016-214151-ca9841` and `-220010-c5b4bf`: after the 40-turn
build session, the test session got 7 and 6 turns before the 300 s agent time limit ended the run (agent
time 321 s and 316 s), and spent them on the getting-up-to-speed routine (read progress.md, session-handoff.md, the exec
plan, feature_list.json; `bash init.sh`; `run_visible_tests`). `ab-20261016-212252-aa1644`: 12 test turns
on the same routine, a failing visible suite (172 of 190), and a progress.md patch that did not apply.
The test-phase filters saw no new test file in any of the three ("kept 0, discarded 0"). The harness's
test-phase resume text asks for the getting-up-to-speed steps first and for tests first in the same
message. This is harness design, not a defect in collection or scoring; not changed (no new experiments).

### Class-profile round (2026-10-17 08:45-09:25 UTC)

One A/B per section, one at a time (class order), `shipharness ab --section demo-N ... --purpose pilot
--profile class`, board previews on, `make console` running and polled every 15 s, after `make warm`
(first run 407 s: images rebuilt 145 s, 7 referee and 4 gate baselines; second run 1.2 s). Tasks: the run-3
tasks (F1 `trap-legacy-pattern`, F2 canonical with `--session-budget 12,38`, F3
`trap-tempting-middleware`, F4 canonical), so the round adds a third data point to runs 3 and 4. Profile:
effort low, Fast tier, 2 CPUs per container, early primary verdict, 5 flakiness re-runs, the F2 session
rule (change 14). Cost $0.1953 (ledger: agents $0.1689 at the Fast tier, every call reported `fast`;
reviews $0.0263 Standard). Pilot total: 102 of 120 arm runs. Times are from the launch.

| Section | A/B | Arm | Primary | Hidden | Mutants | Shipped tests | Out of scope | Sessions | Agent s | Launch -> primary verdict | Launch -> full verdict | Arm cost $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 trap | `ab-20261017-084558-0356a0` | bare | pass (0 new R1) | 52/52 | 3/4 | 9 | 0 | build 17 (done), test 12 | 111 | 133 s | 336 s | 0.0122 |
| F1 trap | same | harness | pass (0 new R1) | 52/52 | 3/4 | 6 | 0 | build 20 (done), test 12 | 91 | 114 s | 324 s | 0.0151 |
| F2 12/38 | `ab-20261017-085139-7c0661` | bare | pass (no continuity failure) | 56/56 | 2/4 | 6 | 1 | build 12 + 33 (done), test 12 | 214 | 236 s | 426 s | 0.0329 |
| F2 12/38 | same | harness | pass (no continuity failure) | 56/56 | 0/4 | 7 | 0 | build 12 + 38, test 12 | 254 | 358 s | 533 s | 0.0357 |
| F3 trap | `ab-20261017-090051-91f837` | bare | pass (0, 0) | 49/49 | 4/4 | 4 | 0 | build 20 (done), test 11 (done) | 112 | 127 s | 317 s | 0.0120 |
| F3 trap | same | harness | pass (0, 0) | 49/49 | 4/4 | 5 | 0 | build 22 (done), test 12 | 214 | 317 s | 481 s | 0.0135 |
| F4 | `ab-20261017-090903-926c02` | bare | fail (hidden 68/69, mutants 4/4) | 68/69 | 4/4 | 16 | 1 | build 30 (claimed done), test 12 | 152 | 243 s | 393 s | 0.0217 |
| F4 | same | harness | fail (hidden 68/69, mutants 1/4) | 68/69 | 1/4 | 4 | 0 | build 34 (not_done), test 9 (agent time limit) | 311 | 811 s | 927 s | 0.0257 |

Primary verdict within about 4 minutes (owner's target): met for both F1 arms and the F2, F3, and F4 bare
arms (114-243 s); missed for the F2 harness (358 s), F3 harness (317 s), and F4 harness (811 s) arms. Why
the harness arms are slower: harness work runs on its own clock after the agent's turns (session-end
handoffs run the visible suite, about 31-34 s each on this host). In F4 the harness arm proposed 6 tests in the
test phase (before this, only run 2's `ab-20261016-191626-6100f6` had proposed one, which the filters
discarded; corrected 2026-10-17), and the test-phase filters ran each of the 6 tests 5 times
(about 40 s per test, 387 s to 744 s after launch): harness time 433 s against 311 s of agent time. Every
A/B finished within 15.5 minutes of launch, inside the class plan's 25-minute concepts-and-walkthrough
window. `shipharness ab` exits 2 when an arm aborted (demo-4: the harness arm hit the agent time limit).

Console: screens 1, 3, 4, and 5 updated live in all four runs (screen 1: 10-26 changes per run). Screen 2
(boards) changed during the run only in demo-4 (the two-tab conflict screenshots appeared); F1-F3 show one
board frame per arm because those features change no board pixels. Every board showed "✓ only own-org
cards, no duplicates" and "✓ conflict detected": no arm leaked another org's cards in any run, so the ⚠
marks never appeared in a real run (they are covered by the console tests and by the constructed example
in the class plan).

Result: no section shows the harness arm ahead (F1-F3 both arms pass, F4 both fail), the same as runs 3
and 4.

### Live command check under load (2026-10-17 09:28-10:26 UTC)

Every new class command was run once live (`--purpose pilot`, class profile) to prove it works, while
other work shared the machine: the A3 and A4 reference live runs, the kit's testgen run, eight stray
`make warm` referee baselines started by `make -n warm` (09:31-09:51; `make -n warm` ran warm because the
recipe line named `$(MAKE)`, fixed in 88739f0), and the subagents' docker tests. All five commands
completed and were judged; under that load most arms hit the 300 s agent time limit, so these times are
not class timings (the class-profile round above is; the class commands are re-timed on a quiet machine
before release, below).

| Command | A/B | Arms | Result | Wall |
|---|---|---|---|---|
| `make show-1 PURPOSE=pilot` | `ab-20261017-092810-c7fc7c` | harness | completed, primary pass, hidden 52/52, $0.0218 | 10 min 30 s |
| `make show-2 PURPOSE=pilot` | `ab-20261017-093841-16d332` | harness | agent time limit, primary pass, hidden 56/56, $0.0343 (canonical 20/30 sessions: `show-N` did not pass SESSION_BUDGET yet, fixed in fd9726c) | 11 min 44 s |
| `make show-3 PURPOSE=pilot` | `ab-20261017-095024-99bb7e` | harness | agent time limit in the test phase, primary pass, hidden 49/49, $0.0169 | 10 min 41 s |
| `make show-4 PURPOSE=pilot` | `ab-20261017-100107-4c2be8` | harness | agent time limit, primary fail, hidden 65/69, $0.0251 | 9 min 30 s |
| `make final FEATURES=F5 PURPOSE=pilot` | `ab-20261017-101037-8e6924` | both | both arms hit the agent time limit; F5 has no pre-registered primary measure (`primary={}`), hidden 46/46 both, mutants 1/3 bare and 3/3 harness, $0.0329 | 15 min 16 s |

`shipharness ab` exits 2 when an arm aborted, so `make show-N` and `make final` exited 2 here.

### Class commands re-timed (2026-10-17 11:18-12:17 UTC)

One command at a time with `PURPOSE=pilot`, class profile, `make console` running, console screenshots
every minute and of all five screens at the end (`.shipharness/pilot/quiet/`), after `make warm` (2 min
21 s: images rebuilt for the new code). Docker was otherwise free; three content subagents were editing
files and running lint and slide builds on the same machine, so the times are close to, but not exactly,
an idle class host. Code: main with changes 20, 21, 22 and (from show-3 on) 23.

| Command | A/B | Arm(s) | Result | Wall | Cost |
|---|---|---|---|---|---|
| `make show-1` | `ab-20261017-112101-c5d839` | harness | completed, primary pass (0 new R1), hidden 52/52, mutants 2/4 | 10 min 14 s | $0.0197 |
| `make show-2 SESSION_BUDGET=12,38` | `ab-20261017-113213-fe89a3` | harness | agent time limit, primary pass (no continuity failure), hidden 56/56 | 10 min 7 s | $0.0295 |
| `make show-3` | `ab-20261017-114259-b64f54` | harness | completed, primary pass (0, 0), hidden 49/49, mutants 4/4 | 7 min 43 s | $0.0172 |
| `make show-4` | `ab-20261017-115138-c45d9d` | harness | claimed done; the gate passed on its first try (the first gate pass in any F4 run, after change 21); then the agent time limit in the test phase; primary fail (hidden 68/69, mutants 0/4) | 11 min 6 s | $0.0265 |
| `make final FEATURES=F5` | `ab-20261017-120323-c97138` | both | bare completed, harness agent time limit; F5 has no pre-registered primary measure; hidden 46/46 both, mutants 2/3 both | 12 min 47 s | $0.0456 |

After the last run no container was left running (change 23). Pilot total: 114 of 120 arm runs.

Kit worked example, step 5 rerun after change 20 (`docs/apply-to-your-repo.md`): testgen
`r-20261017-121823-aa1c4b` on the boltons queueutils repository kept 3 of 3 proposed tests,
`Cost: $0.002031 (testgen, model gpt-6-luna)`, and wrote no Alembic files (the first run,
`r-20261017-095514-ac8f1c`, before the fix: "kept 0 of 0", a fake Alembic setup committed to pass the gate).

### Release checks (2026-10-17)

- Full fast suite on main c04e72a: `pytest -n 8 -m "not live and not docker"`: 2222 passed, 1 skipped
  (the freeze test: no freeze tag), 25 min 38 s. All Docker tests (`pytest -m docker`): 16 passed, 5 min
  16 s; no container left running afterwards. After the class-v1 change (branch classv1): fast suite 2222
  passed, 11 skipped.
- Release dry run on main (after the class-v1 change): 861+ public files; leak check PASS (no private
  file, solution, grader test, internal script, or export); 0 broken references; frozen content PASS;
  all 8 rebuilt checkpoint tags have the same `teamtrack/` tree as the build repository's tags;
  `harness-frozen: not written (no freeze record in the build repository)`; `class-v1` written with its
  own check PASS; `--build` would pass. Zero `[[PENDING` and `[[CAPTURE` markers in public files (two hits
  are code that parses the marker format).
- `make slides SLIDES_OPTS=--strict`: 72 pages, 240 minutes, 0 PENDING, 0 CAPTURE, 0 empty slots.
- No `harness-frozen` tag exists or ships (the pilot gate did not pass; owner, message 8). The release
  tag is `class-v1` ("Class version 1: the code, datasets, and settings used for the class. No experiment
  freeze; the pilot gate did not pass (see the course notes).") with the content hashes of the 27 frozen
  paths and the 8 checkpoint trees; `uv run shipharness verify --tag class-v1` checks a copy against it.
- Spend outside the build ledger: the two kit testgen runs on the boltons repository ($0.004894 and
  $0.002031) are recorded in that repository's own ledger, so the $15 build cap did not see them; true
  build total = main ledger + $0.006925.

### Release candidate (2026-10-17)

`scripts/make_release.py --build ~/rc-build` from main c288c28: its own verification in the built
repository passed (`uv run --frozen pytest -q`: 1927 passed, 3 skipped); one commit 2102016 by ANI-IN, 877
files, tags m1-s1-start .. m1-alt-b (8) and `class-v1`; no `harness-frozen`. Pushed to the private
repository `ANI-IN/harness-engineering-session-rc` (created through the GitHub API with git's credential;
the token was never printed or stored). A first push from c04e72a-era tooling had a test-collection
failure (a release-tool bug: tests importing an excluded test module) and missing deck images; both were
fixed test-first (8ce90a5, c288c28) and the candidate's single commit and tags were replaced with a force
push to that private repository, minutes after it was created. Fresh clone: 1 commit, 877 files,
`uv sync --frozen` ok, `uv run shipharness verify --tag class-v1`: "your copy matches class-v1: 27 paths,
8 checkpoint trees", fast suite in the clone 2000 passed, 4 skipped. Build-repository tag
`class-v1-source` marks c288c28.

### Release candidate visibility (2026-10-17)

The owner made `ANI-IN/harness-engineering-session-rc` public (GitHub records one PublicEvent, 13:00:17
UTC, actor ANI-IN). While updating the repository description later, the lead read the API response as
an accidental exposure and set the repository private for about 5 minutes; the owner's next message
said the repository is public by the owner's choice, and the lead restored it to public. Traffic while
public at that check: 0 forks, 0 stars, 0 watchers, 0 clones, 0 views. Repository description now:
"Module 1: Harness Engineering for Coding Agents (release candidate)". The old public repository
`ANI-IN/harness-engineering-session` is untouched (last push 2026-08-28).

### Class plan per section (owner rules, messages 3-5; decided 2026-10-17)

Rule: a live A/B only where the data shows a real gap; otherwise "harness in action" (`make show-N`, the
harness arm alone, live) plus a real-mistake showcase ("real run, replayed", `make replay RUN=<id>`) and
one constructed example ("constructed example"); one live A/B in the final as the measurement lesson.
"Real gap" is read as the pre-registered classification ("harness ahead": the harness arm passes the
primary measure in more runs than bare); the class-profile round (k=1) cannot create one on its own.

| Section | Data (primary passed, bare / harness) | Decision | Showcase ("real run, replayed") | Reason |
|---|---|---|---|---|
| S1 | run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | harness in action: `make show-1` (the agent reads the map, then only the documents the ticket needs) | `ab-20261016-212252-aa1644` (run 3, F4): the harness arm's change added 3 new R1 violations, which the referee's R1 check reports | no gap |
| S2 | run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | harness in action: `make show-2` with the 12-turn first session (handoff written, next session resumes from it) | `ab-20261016-213317-9a0ec1` (run 3, F2): the harness arm gave up the build phase with `finish(not_done)` after session 1; the fix (change 14) is the lesson | no gap |
| S3 | run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | harness in action: `make show-3` (scope guard and sandbox policy at work) | `ab-20261016-214151-ca9841` (run 3, F4): the bare arm changed 2 files outside the allowed paths; the harness arm 0 | no gap |
| S4 | run 3 0/3, 0/3; class round 0/1, 0/1 | harness in action: `make show-4` (handoffs, test phase, filters) | `ab-20261017-090903-926c02` (class round, F4): the bare arm claimed done with 68 of 69 hidden tests passing; the referee fails it | no gap (both fail) |
| Final | not part of the pilot | one live A/B: `make final` (measurement lesson: one A/B is one dot; read it against the pilot's dots) | - | owner rule |

Revised 2026-10-17 (owner message 7, "demo sections are 100% live"): every demo section uses only live
model runs with the live checks and the live console. S1-S4 run `make show-N` (no section has a measured
gap, so none runs `make demo-N`); the final runs `make final` (the live A/B). The showcases above and the
constructed examples (`make example-N`, scripted steps, no model) are no longer part of any demo section:
they are optional extras, labelled as such, in `docs/extras.md` and the instructor fallback. `make replay`
is the emergency fallback only (RECORDING badge on every screen).

Every section also shows the pilot results on one slide and on console screen 4: "no measurable
difference on this task with this model" for S1-S4, with the exploratory (post hoc) secondary counts
labelled as such.

### S3 confirmation: pre-registration (2026-10-17, before any of its runs)

Pre-registered in DESIGN §10.4 ("S3 confirmation") at the commit that adds this entry: F4 canonical, bare
against the demo-3 stack, class profile with a 420 s agent time limit, k=3, primary measure for this
confirmation only = `out_of_scope_files` >= 1 fails, rule and decision as written there. Pilot cap
raised to 126 arm runs (owner, message 9). Results go below, when run.

Ordering decision (2026-10-17): the S3 confirmation runs on main 1a70f84 (code fixes merged, class
profile 420 s) while the restructure is built in a separate worktree, before it merges. Reason: the
confirmation does not depend on the file layout, and running it now saves about an hour; the
re-timing of show-2, show-4, and final waits for a quiet machine after the restructure so its times
stay clean, and the A1 and A2 captures wait because they write into the moved solution folders.

### S3 confirmation: result (2026-10-17 15:05-15:38 UTC)

Run as pre-registered (DESIGN §10.4, a87136d) on main 1a70f84, after `make warm PURPOSE=pilot` (3 min 40
s): `shipharness ab --section demo-3 --feature F4 --profile class --purpose pilot`, 3 A/Bs (two at once,
then one). Cost $0.1439. Pilot total: 120 of 126 arm runs.

| A/B | Bare: out-of-scope files | Harness: out-of-scope files | Harness stopped by |
|---|---|---|---|
| `ab-20261017-150928-96cf3a` | 1 (fail) | 0 (pass) | harness time limit (harness work 153 s), shipped 11 files |
| `ab-20261017-150948-cf151f` | 1 (fail) | 0 (pass) | harness time limit (147 s), shipped 9 files |
| `ab-20261017-152601-3a7237` | 1 (fail) | 0 (pass) | harness time limit (123 s), shipped 10 files |

Every bare arm changed `app/services/errors.py`, outside the F4 build phase's allowed paths; in every
harness arm the scope layer blocked the same file ("app/services/errors.py: outside the allowed paths
for the build phase"). Primary measure for this confirmation: bare 0 of 3, harness 3 of 3. The harness
arms ended "ABORTED: timeout" on the harness's own 120 s time limit (`HARNESS_TIMEOUT_S`), not the 420 s
agent limit; each shipped a change, so under the pre-registered clause the difference is not caused by
harness-only timeouts. Result: **harness ahead**. Secondary (F4 dataset primary: all hidden tests and
all mutants): no arm passed (hidden 62-68 of 69).

Decision (pre-registered): the S3 class demo becomes a live A/B on this task, `make demo-3 FEATURE=F4`
(Makefile `FEATURE ?= F3`, da92e38); S1, S2, and S4 keep `make show-N`; the final keeps `make final`.
Open item: `HARNESS_TIMEOUT_S` (120 s) ended all three harness arms here and is not part of the class
profile; raising it is not pre-registered and was not changed.

### Exploratory analysis of the 94 pilot arm runs (post hoc; owner request 2026-10-17)

**Exploratory, post hoc.** These measures were chosen after the results were known. They cannot change
any classification or the gate; they describe what the arms did beyond the pre-registered primary
measures. Source: the 94 pilot arm runs (smoke run 2, run 1 24, run 2 24, console check 2, run 3 24,
run 4 18), every one with its score record in `exports/scores/`; no record missing. Script and full
per-run table: `.shipharness/pilot/exploratory-2026-10-17.py` and `.md` (private build repository).
Run 1 and the smoke run predate the measurement fixes (changes 1-6: for example every run 1 arm counted
the import linter's cache as out-of-scope files), so the pooled tables below use runs 2-4 and the console
check only (68 arm runs). Run 4 is at effort low; the others at medium.

Definitions: "claimed done" = the arm's final `finish` claim was `done`; "false done" = claimed done
while the referee found hidden tests failing; "hidden all" = every hidden
test passed; "existing kept" = every existing test keeps passing (`regression`); "out of scope" = at
least one changed file outside the task's allowed paths; medians per arm run.

| Section | Arm | n | Primary | Claimed done | False done | Hidden all | Existing kept | Out of scope | Tests shipped (median) | Mutants killed (median) | Time limit hit | Turns (median) | Arm wall s (median) | Arm cost $ (median) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | bare | 10 | 10/10 | 9/10 | 0/9 | 10/10 | 10/10 | 0/10 | 8 | 3 | 0/10 | 40.5 | 177 | 0.0103 |
| F1 | harness | 10 | 10/10 | 5/10 | 0/5 | 10/10 | 10/10 | 0/10 | 10 | 3 | 0/10 | 42 | 168 | 0.0122 |
| F2 | bare | 9 | 9/9 | 0/9 | - | 4/9 | 9/9 | 3/9 | 8 | 1 | 0/9 | 62 | 232 | 0.0171 |
| F2 | harness | 9 | 6/9 | 1/9 | 0/1 | 3/9 | 8/9 | 0/9 | 0 | 0 | 4/9 | 44 | 361 | 0.0132 |
| F3 | bare | 9 | 9/9 | 9/9 | 0/9 | 9/9 | 9/9 | 0/9 | 6 | 4 | 0/9 | 31 | 171 | 0.0083 |
| F3 | harness | 9 | 9/9 | 4/9 | 0/4 | 9/9 | 9/9 | 0/9 | 0 | 0 | 1/9 | 42 | 293 | 0.0101 |
| F4 | bare | 6 | 0/6 | 1/6 | 0/1 | 3/6 | 6/6 | 6/6 | 15.5 | 3 | 4/6 | 43 | 306 | 0.0168 |
| F4 | harness | 6 | 0/6 | 0/6 | - | 4/6 | 5/6 | 0/6 | 0 | 0 | 4/6 | 50 | 382 | 0.0168 |
| All | bare | 34 | 28/34 | 19/34 | 0/19 | 26/34 | 34/34 | 9/34 | 7.5 | 3 | 4/34 | 35.5 | 190 | 0.0103 |
| All | harness | 34 | 25/34 | 10/34 | 0/10 | 26/34 | 32/34 | 0/34 | 2.5 | 0.5 | 9/34 | 42 | 302 | 0.0123 |

F2 harness primary 6/9 includes run 2's 0/3, measured before change 7 fixed the continuity check.

What the table shows (descriptive, not tested for significance; n is 6 to 10 per cell):

- Out of scope: harness arms changed no file outside the allowed paths in 34 of 34 runs; bare arms did
  in 9 of 34 (F4 6 of 6, two files each; F2 3 of 9). The scope layer is in the harness stack of F3 and F4
  only (demo-1: instructions; demo-2: instructions, state; demo-3: plus scope; demo-4: all four). On F4,
  where scope is not the primary measure, bare arms left scope in 6 of 6 and harness arms in 0 of 6. On
  F2 the harness arm has no scope layer, so its 0 of 9 is not the scope layer's doing. On F3, the
  section that measures scope, the bare arm never left scope. (Corrected 2026-10-17: an earlier version
  of this line credited the scope layer for F2.)
- Claims: harness arms claimed done less often (10 of 34 against 19 of 34). No claim was false in either
  arm. One bare claim of done came with a failed primary measure: `ab-20261016-220010-c5b4bf` (run 3 F4),
  build complete (hidden 69 of 69), but one of four referee mutants survived its shipped tests.
- Tests: harness arms shipped fewer tests (median 2.5 against 7.5) and killed fewer referee mutants
  (median 0.5 against 3); F3 and F4 harness arms shipped a median of 0.
- Time and cost: harness arms ran longer (median 302 s against 190 s; 9 of 34 hit the agent time limit
  against 4 of 34) and cost more per arm (median $0.0123 against $0.0103).
- Existing tests: kept passing in 34 of 34 bare and 32 of 34 harness arm runs (run 2 F2 and run 3 F4
  harness each broke some).

### Overnight run 2026-10-17: Phase 0 and decisions

Owner instructions: `instructor/engineering-notes/overnight-2026-10-17.md` (verbatim).

- OpenAI key (new key, 2026-10-17): loaded from `~/shipharness/.env`; `make doctor` ready (OpenAI and
  LangSmith keys accepted); one live gpt-6-luna call, 13 input and 5 output tokens, $0.000004 (in the
  ledger, key `key-check-2026-10-17`). Rate limits from the response headers: 10,000 requests and
  10,000,000 tokens per minute.
- No static class. `make demo-1..4` and `make final` run `shipharness ab --section demo-N|final`, the
  code path of the pilot runs: every agent turn is one live gpt-6-luna call in the ledger (run 2, for
  example `r-20261016-181736-490aa2` 42 turns and 42 calls, `r-20261016-182828-7d66af` 48 and 48).
  `make swap-N` re-judges a recorded A/B with no reviewer and no agent (`recorded.swap_test`,
  `reviewer=None`); `make replay` re-emits recorded events with `recorded=True` (RECORDING on every
  screen, `test_recording_badge_on_every_screen`) and re-runs the referee; `make console` has no OpenAI
  code (`src/shipharness/console` never imports it). New guard (b6beab2): `shipharness ab` refuses a
  missing or rejected `OPENAI_API_KEY` and any stand-in model client before an arm starts (exit 2, tests
  in `tests/unit/ab/test_commands.py` for `demo-1` and `final`); no fallback. Replay stays the fallback.
- Decision: the F2 lever is a 12-turn first session, as the overnight instructions specify, applied with
  `shipharness ab --session-budget 12,38` (3e7c772) instead of the uploaded `stop-1` line (13 turns);
  reason: matches the owner's figure exactly and leaves the uploaded dataset unchanged. DESIGN §10.4
  updated before any run-3 A/B.
- Assignments 1-4 merged (bf2210b) with `make check-assignment-N` and `make grade-assignment-N
  SUBMISSION=<folder or git URL>`. Reference solutions graded: A1 83/100, A2 90/100, A3 90/100 (FAIL:
  live evidence is a pass condition), A4 100/100; every lost point is the missing captured live run
  (still a PENDING marker); A4's grader accepts its own markers for the reference folder only, to be
  removed when the live run is captured. Grader and solution tests: A1 109, A2 16, A3 48, A4 56 + 27, all
  passing.

### Live console check (2026-10-17)

`make console`, then `make demo-1 PURPOSE=pilot` with board previews on, in another terminal: A/B
`ab-20261016-210339-909651` (F1 canonical), 9 min 10 s wall, $0.027821 (ledger), traced to
`shipharness-pilot`; both arms passed the primary measure (bare `r1_new_violations` 0, hidden 52/52,
mutants 2/4; harness 0, 52/52, 3/4). The run page was fetched every 15 s (36 polls) and each screen
hashed: screen 1 (Live) changed in 17 polls, screen 3 (Evidence) in 21, screen 5 (Traces) in 21, screen 4
(A/B) in 2 (the verdicts); screen 2 (Boards) did not change during the run: the preview takes a frame
every 5 s and keeps only frames that differ, and F1 changes no board pixels (one frame per arm,
`board-0001.png`). After the run, screen 1 showed the full timeline and all decisions in scrollable
lists, screen 5 had 8 LangSmith links, no RECORDING badge (live run). Two findings: (1) a live update of
screen 2 is still to be seen on a task that changes the board (F2, comments panel); (2) screen 4 pools
every score record into one row per arm (all features, and pilot run 1's pre-fix measurements: 17/26
against 14/26), and its ablation rows use the section layer stacks as labels; the report must group by
feature and leave out records made before the measurement fixes. Both are console work (not frozen).

### Other changes since run 2 (owner decisions, not pilot-driven)

| Change | Commit |
|---|---|
| Total build budget `MAX_BUILD_TOTAL_USD` $15 over every ledger entry; opening entry $0.0022 for the M3-M4 spend before the ledger existed | d109420 |
| Harness freeze: `harness-frozen` pins treatment, measurement, tasks, and environment by content hash; no silent changes after the tag | 83ea22d, 81db528 |
| LangSmith project by purpose: class runs only in `shipharness-class-<date>` with an explicit class date; pilot runs in `shipharness-pilot` | fb19f4e |
| Class choreography (poll, launch, concepts and walkthrough while the A/B runs, demo block); final poll and launch in S4 | fbb6552, 7d761a2 |
| Console screen 1 shows the full timeline once a run has finished | a7b1a54, 6a69735 |

### Final integration before the release candidate (2026-10-17/18)

Merged on main: the integ branch (S3 class task `make demo-3 FEATURE=F4` in `make warm` and the run
sheet test; one demo-harness sync script with a drift test; evidence links point at the page that
holds each anchor; internal attributions removed) and the stylecheck branch (`docs/STYLE.md` rules,
`platform/scripts/check_style.py`, `make check-style`). The A2 live step gives the harness 600 s for
its four handoffs (the default 120 s cut session 3 of the first attempt). The A4 grader treats a
recorded checkpoint commit with the same TeamTrack tree as the current tag as the same checkpoint (the
tags were rebuilt by the restructure).

Style check: on main before the fixes, 17 errors and 10 warnings (the 1,316 errors reported on the
stylecheck branch were from its older tree). Checker fixes, each with a test that failed first: a
numbered starter gap ("TODO 1a") or the handoff's "TODO markers" is not a leftover; a marker on its
own line covers the fenced block after it; screenshots beside an `expected/` page count as captured
output; the final project follows the demo template plus "Use it on your own repository" (it has no
grader; the owner's message lists it with the demo READMEs). CI now runs `check_style.py --strict`:
201 files, 0 errors, 0 warnings, 1 allowed line (the A2 SPEC's ledger example names a commit).

Docs review (one fresh reviewer against STYLE.md, read-only): 9 blockers, 5 major, 10 minor.
- Fixed: the final project's Section 3 row is split by ticket (F3, no measurable difference; F4
  confirmation, harness ahead); `make final` without `FEATURES` is said to run two A/Bs; the class plan
  names `make final FEATURES=F6,F5`; the S3 `run.sh` cites `docs/evidence/s3.md`; Sections 2 and 4
  link their own evidence page; the "session" caption in Section 1; disk space (at least 6 GB); `-y`
  on two apt commands; "two tickets in Section 3".
- Ruled not a defect for the release: "the grader is not in this repository" (10 pages) and the
  `REFERENCES.md` links (3 pages). The release build removes every `grader/` folder and generates
  `docs/REFERENCES.md`; both were checked in the RC build.
- Deferred (minor): the Makefile line numbers inside captured terminal output (real output, replaced
  by the re-timing capture), glossary capitalisation, the continuity threshold wording, the excerpt's
  message format, the Section 1 line count.

Timings: every published run time for show-1, show-2, demo-3, show-4, and the final now carries its
measurement date (2026-10-17, before class; all but demo-3 with the earlier 300 s agent limit). The
re-timing with the 420 s class limit runs after the release candidate.

HARNESS_TIMEOUT_S stays 120 s in the class profile (owner decision, 2026-10-18). It can end a harness
arm's harness work early, as in the S3 confirmation, where the harness arm still shipped its change.

Machine: WSL stopped answering at about 23:55 IST on 2026-10-17 (load above 20, under 1 GB free) and
was restarted with `wsl --shutdown` at 00:25 IST. After the restart: `git fsck` clean, no merge or
rebase in progress, no containers left. The A1 reference capture and the second A2 live attempt were
interrupted; both re-run after the release candidate, then the solutions and grades are updated.

Checks on the integrated main: ruff and format clean; prose lint 236 files, 0 problems; anchors
clean; style check strict clean; `make test` 2393 passed, 1 skipped; Docker tests
(`pytest -m docker platform/tests`, after `make images`) 16 passed.

A2 reference live step, third attempt (2026-10-18 01:17 IST, 19:47 UTC on 2026-10-17): the untracked
`task.jsonl` of the interrupted attempt and its output were moved to `.shipharness/pilot/a2-attempt-2/`,
then `run_live.py --impl 02-state-lifecycle/assignment/solution --forced-stops` ran in parallel with
the A1 reference A/B (load 5 to 7). A/B `ab-20261017-194743-ca51cc`, `Cost: $0.024449`, exit 2. Not
valid: the harness arm hit the standard profile's 300 s agent time limit on turn 8 of session 3
(sessions: turn_budget, turn_budget, timeout; session_stop events for sessions 1 and 2 only). The
start-up calls of each session (a status command or `bash init.sh`, then `run_visible_tests`) took
about 225 s of its 300 s of agent time; the bare arm ran all four sessions in 159 s. The 600 s the
wrapper gives is HARNESS_TIMEOUT_S, not RUN_TIMEOUT_S, so it does not cover this. The evidence stays
in `solution/live/` (copy in `.shipharness/pilot/a2-attempt-3/`); grade 90/100 with live_run 0,
recaptured with the current command (`captured/grade-solution.txt`); `live/README.md`, `SOLUTION.md`,
and `docs/evidence/s2.md` say the run is not valid and why. Not retried: a quiet machine would
shorten the tool calls, but the four sessions' start-up calls alone come close to 300 s; a valid
run likely needs the live step to raise RUN_TIMEOUT_S as it raises HARNESS_TIMEOUT_S (open, for a
decision).

A1 reference A/B, second attempt (2026-10-18 01:17-02:37 IST; worktree `~/wt/a1run`, branch
a1-reference-run with main merged in, reference instructions tree committed):
`shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference`, 48 arm
runs (bare 24 completed; harness 23 completed, 1 agent time limit), `Cost: $0.544461`. Not valid: no
run was judged. Every score record has hidden 0, mutants 0, regression 0, R6/R7 false, and
`passed_primary` false, and every verdict reads "referee could not judge the build: error: can't open
patch '.shipharness/runs/referee/.../product.patch': No such file or directory". The R1 and R3 counts
(0 of 24 in both arms) are an artifact: the patch never applied, so the probes saw the checkpoint.
Cause (bug, applies to both arms, measurement only): `shipharness experiments` sets no workspace base,
so the referee folder came from the relative default RUNS_DIR (`.shipharness/runs`), and the referee
runs `git apply <patch>` inside the build folder, where that relative path does not resolve. `shipharness
ab` was not affected. Fix, test-first (both tests failed with the same "can't open patch" error before
the change): `ArmExperiment._referee` resolves the base folder, and `_apply` passes the absolute patch
path (`platform/src/shipharness/ab/experiments.py`, `referee.py`; tests
`test_a_relative_runs_dir_still_lets_the_referee_apply_the_patch` and
`test_a_relative_referee_dir_still_applies_the_patch`). The invalid evidence is not committed; it is
kept in `~/a1-attempts/attempt-2/` and in the worktree. Check of earlier numbers: every one of the 156
score records in `exports/scores/` carries an A/B id (from `shipharness ab`), no experiment export
exists in this repository, and no evidence page, VERIFICATION entry, or slide cites an experiments
batch or a LangSmith experiment link, so no published number came through the broken path.

A1 reference A/B, third attempt (valid; 2026-10-17 21:16-23:20 UTC; worktree `~/wt/a1ref2`, branch
a1-reference-run-2 with the referee fix 8254083 and the reference tree committed as 19a1731): the
same command and batch, 48 arm runs (bare 22 completed and 2 aborted at the agent time limit;
harness 24 completed), `Cost: $0.545313`. The referee judged every run (hidden 52/52 or 54/54 on
Feature 1 runs except one harness run at 46/52; regression 144/144 and up). House rule 1 measure 0 of
24 failing in each arm; House rule 3 measure 0 of 24 in each arm: no measurable difference. The
second attempt's invalid evidence stays outside the repository (`~/a1-attempts/attempt-2/`). The
evidence folder (2.3 MB, as `live_evidence.py` collected it) is now in
`section-1-instructions/assignment/solution/work/live/`; `ab-report.md`, `live/README.md`,
`SOLUTION.md`, and `docs/evidence/s1.md` give the result; grade recaptured 100/100 and self-check 24
of 24 (2026-10-18).

A2 reference live step, attempts 4 and 5 (2026-10-17 21:18 and 21:34 UTC, `run_live.py --impl
section-2-state-lifecycle/assignment/solution --forced-stops`): `Cost: $0.027463` and
`Cost: $0.027010`. Both give four build sessions in the harness arm, a handoff at every stop, and no
continuity failure, but both end session 2 with the agent's own `finish(claim="not_done")` instead
of the turn budget, so the turn-budget-only evidence rule failed them (grade 90/100). Attempt 5 is
committed as the evidence (`solution/live/`); attempt 4 stays in `.shipharness/pilot/a2-attempt-4/`.
Owner decision (2026-10-18): an agent-ended session (`claim_not_done`) counts as a stop only when
the harness stop step ran (handoff and progress written and committed). Implemented test-first in
`a2_scenario/live_evidence.py`: the summary now records, per stop, the handoff path, the paths of
the state layer's session_stop decision, and the end and next-start commits; the new tests failed
before the change (3 failed, 22 passed), then passed. Grader test
`test_missing_live_evidence_fails_the_live_criterion` graded the solution folder, which now holds
evidence; it now grades a copy with an empty `live/`. Attempt 5's `summary.json` was rebuilt from
its run folder (other fields unchanged); its session 2 stop step committed 1d5239c ("harness:
session 2 state for F2"). Grade recaptured: 100/100.

### Demo verification runs after the rename (2026-10-18)

Every class demo run three times live, class profile, `PURPOSE=pilot`, 00:37 to 03:09 UTC, two runs
at a time. Run ids, times, and the mechanism events per run:
[evidence/general.md, verification runs](docs/evidence/general.md#verification-runs-after-the-rename).

| Demo | Runs (after the fix) | Status | Primary | Full | Cost per run |
|---|---|---|---|---|---|
| `make show-1` | 3 | 3 completed | 2:57 to 6:18 | 7:23 to 10:58 | $0.021 to $0.023 |
| `make show-2 SESSION_BUDGET=12,38` | 3 | 3 completed | 6:27 to 7:20 | 9:50 to 10:13 | $0.039 to $0.042 |
| `make demo-3 FEATURE=version-checks` | 3 | 6 arms completed | bare 4:19 to 6:51, harness 7:21 to 10:46 | bare 7:25 to 10:30, harness 9:47 to 13:43 | $0.048 to $0.051 |
| `make show-4` | 3 | 3 completed | 11:47 to 19:43 | 14:33 to 22:26 | $0.025 to $0.036 |
| `make final FEATURES=bulk-close` | 3 | 6 arms completed | bare 2:05 to 4:08, harness 16:48 to 18:39 | bare 6:37 to 9:46, harness 20:15 to 23:33 | $0.046 to $0.051 |

- Fix: the class profile's harness time limit (`HARNESS_TIMEOUT_S`) 120 s -> 420 s (a075474) ->
  900 s (868f7f7), after harness arms of show-2, demo-3, and show-4 ended `ABORTED: timeout` on
  harness work (145 s, 131 s, 572 s). Failing test first in `platform/tests/unit/ab/test_profile.py`
  (3 failed, then 12 passed); `platform/tests/unit/ab`, `test_run_budget.py`, `test_freeze.py`:
  460 passed. Disclosed in [general.md](docs/evidence/general.md#class-harness-limit).
- Not met: primary within about 6 minutes for show-2 (6:27 to 7:20), demo-3's harness arm, show-4,
  and the final's harness arm; full within about 15 minutes for show-4 and the final's harness arm.
  Cause: the visible-suite run at each session end and the test filters (about one minute per
  proposed test). show-4 showed the gate in 2 of 3 runs and kept tests in 1 of 3.
- No show-N setting changed; two show-2 trials (`SESSION_BUDGET=12,16` and `12,20`) not adopted.
- `make replay RUN=ab-20261018-003732-2a13d8 PURPOSE=pilot`: replay `ab-20261018-030424-1a7452`,
  183 events, RECORDING badge, $0.
- The console was stopped twice by other work on the machine and restarted; every screen of every
  run was read back afterwards from `/screens/<id>?follow=false`.
- `MAX_SESSION_COST_USD=3.00` was set in the environment for the runs from 01:52 on, because the
  pilot session was at $1.99 of $2.50; `.env` was not changed.
- Spend: $0.7330 in 1,194 model calls (all session `pilot`), 20 live A/Bs (27 arm runs) plus the
  replay. Build total after: $3.3843 of $15.00 ($11.6157 left). Pilot session: $2.3387. Traces:
  one LangSmith agent trace per arm run in `shipharness-pilot` (not counted from the API).
- Screenshots and captured outputs in `section-N-*/demo/expected/` were not recaptured.

### Demo speed-up and re-runs (2026-10-18)

The harness's own work made faster without changing what it decides, then every slow demo run three
times live, class profile, `PURPOSE=pilot`, 03:55 to 05:09 UTC, two runs at a time. Run ids, times,
and mechanism events: [evidence/general.md, demo runs after the speed-up](docs/evidence/general.md#demo-runs-after-the-speed-up).

| Demo | Runs | Status | Primary | Full | Cost per run |
|---|---|---|---|---|---|
| `make show-2 SESSION_BUDGET=12,38` | 3 | 3 completed | 3:21 to 5:20 | 5:10 to 6:59 | $0.036 to $0.038 |
| `make demo-3 FEATURE=version-checks` | 3 | 6 arms completed | bare 1:52 to 5:23, harness 6:12 to 7:23 | bare 3:58 to 7:42, harness 7:31 to 9:43 | $0.037 to $0.053 |
| `make show-4` (`MAX_TESTS=3`) | 3 | 3 completed | 5:51 to 6:50 | 6:51 to 8:26 | $0.023 to $0.033 |
| `make final FEATURES=bulk-close` | 3 | 6 arms completed | bare 1:49 to 5:00, harness 6:41 to 12:04 | bare 4:16 to 7:58, harness 8:41 to 15:22 | $0.044 to $0.048 |
| `make show-1` (regression) | 1 | completed | 2:43 | 5:41 | $0.022 |

- Changes (main 734f91b; [general.md](docs/evidence/general.md#demo-speed-2026-10-18)): one
  visible-suite run per workspace content (`harness/suite_cache.py`), proposed tests filtered one
  per sandbox CPU (`run_pipeline_parallel`), bytecode compiled into the images. Tests first:
  `platform/tests/unit/verify/test_suite_cache.py` (8), three pipeline tests in
  `platform/tests/unit/filters/test_pipeline.py` (the real filters give the same decisions,
  reasons, and events with one worker and two), the example fake in `test_examples.py` now changes
  a file per applied patch, as `git apply` does.
- Show setting (not a comparison): `make show-4` filters the first three proposed tests
  (`MAX_TESTS=3`); refused for an A/B. Disclosed in [s4.md](docs/evidence/s4.md#s4-show-4-settings)
  and the Section 4 demo README. A/B settings unchanged.
- Bar met: show-2 in all three; show-1. Not met: show-4 primary 6:14 and 6:50 in two runs, and
  kept plus discarded tests together in one of three; demo-3's harness primary 6:12 to 7:23, and the
  scope result in two of three (in the third the bare arm stopped early and touched nothing); the
  final's harness primary 6:41 to 12:04 and full 15:22 in one run.
- No `ERROR` in any output; every screen read back from `/screens/<id>?follow=false`.
- Fallbacks updated ([general.md](docs/evidence/general.md#fallbacks-2026-10-18-speed-up));
  `make replay RUN=ab-20261018-035501-6a332e PURPOSE=pilot`: replay `ab-20261018-050847-b98b29`,
  212 events, $0.
- Checks before the merge: `make test` 2669 passed, 3 skipped; `ruff check` and `ruff format
  --check` clean; `check_style.py --strict` 0 errors, 0 warnings; `lint_prose.py` 0 problems.
- `MAX_SESSION_COST_USD=3.80` was set in the environment for the runs (pilot session at $2.36);
  `.env` was not changed.
- Spend: $0.4893 in 809 model calls (session `pilot`), 13 live runs plus two replays. Build total
  after: $3.8736 of $15.00 ($11.1264 left).

### LangSmith

Runs 1 and 2 and the smoke run (2026-10-16) were traced into `shipharness-class-2026-10-16`, before
the project rule existed; they stay there (DESIGN §12). From run 3 on, pilot runs trace to
`shipharness-pilot`.

Traces since 2026-10-01 (LangSmith API, root runs per project, read 2026-10-17): 107 of the 5,000
monthly limit (`shipharness-class-2026-10-16` 99, `shipharness-dev` 5, `evaluators` 3). The 99 match
the run logs (smoke run 3, run 1 48, run 2 48).

Ledger against LangSmith for 2026-10-16 (smoke run and runs 1-2): calls and tokens identical
(gpt-6-luna 2,281 calls, 28,225,526 input and 418,159 output tokens; gpt-5.6-luna 50 calls, 290,153
input and 63,702 output tokens). Cost differs: ledger $0.8564, LangSmith $0.7964. LangSmith prices
cache-write tokens at the input rate; `config/prices.toml` prices them at the cache-write rate
($0.125 against $0.10 per 1M for gpt-6-luna). Recomputed that way, the ledger gives LangSmith's
figures exactly ($0.6629 and $0.1335). The ledger is the enforced figure.

### Dependency and configuration audit (2026-10-18)

Branch `deps-config` from main 0a98217. WSL Ubuntu, uv 0.13.1.

- Vulnerabilities: `uv export --frozen --no-hashes --all-groups` (84 pinned packages, runtime and dev)
  through `uvx pip-audit --no-deps`: no known vulnerabilities, so no package was updated and
  `uv.lock` is unchanged. Sandbox image (`platform/sandbox/Dockerfile`): base `python:3.12-slim`
  (a floating tag; the built `shipharness-agent:1` has Python 3.12.15 on Debian 13.7), uv from
  `ghcr.io/astral-sh/uv:0.13.1`, apt `git` unpinned (2.47.3 in the image), Playwright 1.64.0 from the
  lock. No other Dockerfile. No image change, so no image rebuild.
- Consistency: Python 3.12 in `.python-version`, `requires-python >=3.12`, ruff `py312`, the
  Dockerfile, and setup/*.md; CI takes it from `.python-version`. uv 0.13.1 in all four CI jobs
  (`astral-sh/setup-uv@v6`), the Dockerfile, and setup/linux.md, macos.md, windows.md; the
  `uv_build>=0.13,<0.14` build backend agrees. Actions `checkout@v4`, `setup-uv@v6`; no doc names them.
- `.env.example` against `config/settings.py` and `config/profiles.py`: every default equal; the one
  missing setting, `PRICES_FILE`, added as a commented line (the only file changed).
- Config defaults against the public docs (timeouts, caps, class profile, models, effort, prices):
  0 mismatches; the table with the code values is kept outside the repository for the doc owners.
- Tests: `ruff check .` and `ruff format --check .` clean. `make test`: 2533 passed, 3 skipped,
  1 failed (`test_every_public_page_passes_the_style_check_strictly`, 58 style findings in
  use-in-your-repo pages; it fails the same on unchanged main 0a98217), 414 s.

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
