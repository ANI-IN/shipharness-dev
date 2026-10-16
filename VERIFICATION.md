# VERIFICATION

Record of what was run, what it cost, and what it showed. Every number in course material that is not
cited to a source points to an entry here. Status: in progress (milestones M3 to M6). The full
verification (M9) adds per-command costs, demo times, pilot and experiment results.

## Running totals

| Item | Used so far | Budget |
|---|---|---|
| OpenAI spend (instructor, all milestones) | $0.8586 (cost ledger with the opening entry: M3-M4 $0.0022 before the ledger existed; M6: $0.0183 smoke run, $0.4415 pilot run 1, $0.3966 pilot run 2) | total build ≤ $15 (enforced on every call); experiments ≤ $25; class ≤ $2.50 |
| LangSmith traces (instructor, October 2026) | 107 since 2026-10-01 (LangSmith API, read 2026-10-17: `shipharness-class-2026-10-16` 99 = M6 smoke run 3, run 1 48, run 2 48; `shipharness-dev` 5; `evaluators` 3) | LangSmith limit 5,000 per month; DESIGN budget: experiments ≤ 1,500, instructor month ≤ 2,500 |

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
--feature FN --no-preview`; 2 A/Bs at a time). Pilot cap: up to 72 arm runs and $10 in total, on top of
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
