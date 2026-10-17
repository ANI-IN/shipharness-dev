# S4 demo: `make demo-4` (F4, all layers)

Runbook for the S4 live A/B. Class plan (course design): poll (3 min), then the final feature poll
(1 min); `make demo-4` launched right after them and `make final FEATURES=<poll winner(s)>` one
minute later in terminal C, with a glance at an easy control task (2 min); concepts (14 min) and
code walkthrough (10 min) while both A/Bs run in the background; demo block (15 min): screens 1, 2,
3, the A/B verdicts, screen 4, the swap test or the layer switch; discussion (5 min). Concepts:
[../concepts.md](../concepts.md).

Every captured output in this file is labelled "captured on <date>, run <id>; your output will
differ". Items that need a real run carry a PENDING marker until the pilot (M6), batch 1 (M8), or
the live class fills them. Source IDs such as (A3, F-a-110) resolve in
[REFERENCES.md](../../../REFERENCES.md).

---

## 1. Purpose and the problem this demo shows

Both arms build F4, optimistic concurrency and issue history (`teamtrack/docs/features/f4.md`), from
checkpoint `m1-s4-start`, with the same ticket, model, tools, sandbox, turn budget, and cost cap. The
bare arm runs with no layers; the harness arm runs all four (`SECTION_STACKS` in
`src/shipharness/ab/demo.py`).

The problem: the `If-Match` header is optional, so every existing test keeps passing whether or not
concurrency works. An agent can test the happy path, call `finish(claim="done")`, and ship a board
where two people editing one issue silently overwrite each other. In the bare arm nothing checks
the claim. In the harness arm the verify gate runs before "done" is accepted, the five filters
decide which test-phase tests are kept, and the referee judges both arms on two counts neither arm
can see: hidden tests passed (of 69) and referee-set mutants killed by the shipped tests (of 4).

This runbook is written for the canonical F4 task, which pilot run 3 also uses (pre-registered: F4
canonical, no lever; the harness turn-cost change applies). The class task follows the pilot
decision recorded after run 3:

[[PENDING: final F4 task for the class (canonical or another variant) after pilot run 3 | source: M6 pilot | how: course pilot (build repository)]]

The pilot gate did not pass (course pilot, 2026-10-17), so the class task is the instructor's decision.

## 2. Commands

Run everything inside WSL2 from the repository root (`~/shipharness`).

Before class:

```sh
make doctor          # keys, Docker, versions; fix anything that is not ok
make console         # second terminal: console at http://localhost:8765
```

In class:

```sh
make demo-4                     # A/B on F4: bare vs all layers, then the referee and reviewer
make final FEATURES=<ids>       # terminal C, one minute after make demo-4
make swap-4                     # swap test on the latest demo-4 A/B (no model calls)
make demo-4 LAYERS=-verify      # layer switch: harness arm without the verify layer
make replay RUN=<ab or run id>  # fallback only: replays a recorded A/B, referee runs live
```

What each one runs, as `make -n <target>` prints it (run on 2026-10-17; `make -n` only prints the
commands, it starts nothing):

| Target | Command |
|---|---|
| `make demo-4` | `uv run shipharness ab --section demo-4 --feature F4 --purpose class` |
| `make final FEATURES=<ids>` | `uv run shipharness ab --section final --feature <id> --purpose class` for each id, one after another |
| `make swap-4` | `uv run shipharness ab --swap latest --section demo-4 --purpose class` (`AB=<id>` replaces `latest`) |
| `make demo-4 LAYERS=-verify` | `uv run shipharness ab --section demo-4 --feature F4 --layers=-verify --purpose class` (harness arm: instructions, state, scope) |
| `make replay RUN=<id>` | `uv run shipharness replay <id>` |
| `make console` | `uv run shipharness console --port 8765` |

None of these were run for this runbook: they call OpenAI or start containers (`make doctor` also
calls OpenAI to check the key, `client.models.list()` in `src/shipharness/doctor.py`). The
integrator verifies them live. The live console check ran `make demo-1 PURPOSE=pilot` with previews
(A/B ab-20261016-210339-909651, 2026-10-16); no F4 A/B has run with previews yet. The captured
output in section 6 comes from pilot run 2.

`make demo-4` prints `A/B <ab_id> (F4, layers=[...])` when it finishes. At the launch the id is not
printed yet, so pick the newest run on `http://localhost:8765/` (reload the list); after the run,
`http://localhost:8765/run/<ab_id>` opens it directly. Keys `1` to `5` switch screens; `F` shows one
arm full screen. In S4 two A/Bs start a minute apart: open demo-4's A/B right after `make demo-4`,
before `make final` starts, because the runs list shows only ids, newest first; open the final's
A/B in a second browser tab and leave it for the closing block.

The layer switch runs both arms again and calls the model. Each arm is capped at `MAX_RUN_COST_USD`
($0.20) and each review at `MAX_REVIEW_COST_USD` ($0.04) (`src/shipharness/config/settings.py`). The
class budget allows one optional layer-switch rerun only if the session meter shows room; the
session cap (`MAX_SESSION_COST_USD`, $2.50) blocks it otherwise. Check the last line `make demo-4`
printed (`Cost: ... session $<spent> of $2.50 ...`) before choosing the layer switch over the swap
test.

## 3. Screen sequence and code anchors

### Order in class

| Section minutes | Block | Terminal B and console |
|---|---|---|
| 0-3 | Poll (section 4) | |
| 3-4 | Final feature poll | Close it before the launch; the winner, plus the runner-up if the session figure allows |
| 4-6 | Launch | `make demo-4` at minute 4 (terminal B); `make final FEATURES=<poll winner(s)>` at minute 5 (terminal C); open each new A/B; screen `1` of demo-4; control glance |
| 6-20 | Concepts ([../concepts.md](../concepts.md)) | Both A/Bs run in the background |
| 20-30 | Code walkthrough | Both A/Bs run; at minute 25 check terminal B for the demo-4 `Cost:` line and terminal C for the final |
| 30-45 | Demo block | The finished demo-4 A/B: screens, verdicts, experiment dots, swap test |
| 45-50 | Discussion and transition | Next: the final A/B's results, in the closing block |

The A/B must be finished by section minute 25. Measured in the course pilot, run 2, 2026-10-16 (12
A/Bs, sections F1-F4, two A/Bs running in parallel on the class host, before the referee speed-ups):
every A/B finished within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s (8.1 min). In S4
two A/Bs run at a time (demo-4 and one final feature; `make final` runs its features one after
another), the same load as pilot run 2; the class-host time for `make demo-4` is in section 8. If
the A/B is still running at minute 25, open the demo block on the running A/B and run the swap test
on the recorded fallback (`make swap-4 AB=<recorded ab id>`); if it failed on stage, use the replay
(section 9).

While a run is live, screen `1` keeps only the last 8 turn rows and the last 3 harness decisions
per arm; once the run has finished, it lists every turn row and every harness decision in
scrollable lists (`src/shipharness/console/templates/screens/live.html`). The launch is the moment
to show the first turns live; in the demo block, scroll the finished arm's lists, or open the
LangSmith trace linked on screen `5`.

Launch (section minutes 4-6) and demo block (section minutes 30-45):

| When | Key | Screen | Show |
|---|---|---|---|
| Launch | `1` | Live Console | Both arms start; bare arm: "No gate (verify layer off)." The harness arm's gate pills appear only after its first `finish(done)`, while the concepts are on screen |
| Launch | — | — | Glance at the easy control task, C4 "Store issue titles without surrounding whitespace" (`teamtrack/docs/features/c4.md`); then the concept slides |
| Demo block | `1` | Live Console | Harness arm: the last gate's pills ✓/✗ and, after a failed gate, its feedback in the harness decisions; if no pills appear, the agent never claimed done (section 5); bare arm: "No gate (verify layer off)." |
| Demo block | `2` | Boards | The "Two-tab edit conflict" panel: ✗ lost update or ✓ conflict detected, per arm |
| Demo block | `3` | Evidence | Verification panel: referee counters, test filter table (1-5) with discard reasons, coverage line, mutant matrix |
| Demo block | — | Terminal B | The A/B and reviewer verdicts (one line per arm) and the session figure from the `Cost:` line |
| Demo block | `4` | A/B Report | S4 dots for both co-primary counts, tonight's run next to the experiment runs |
| Demo block | `1` | Live Console | "Agent said" vs "Referee" for each arm; then `make swap-4` or the layer switch |

Code walkthrough (about 10 minutes, while the A/B runs; `uv run python scripts/anchors.py extract
<id>` prints each one):

| Order | Anchor | File and lines | Point at |
|---|---|---|---|
| 1 | `S4:filters` | `src/shipharness/filters/pipeline.py:34-74` | A test stops at its first failing filter; every result is published with a reason |
| 2 | `S4:probe` | `src/shipharness/checks/r1_tenant.py:65-104` | R1: a foreign id must give 404; a 2xx carrying Globex data is a leak |
| 3 | `S4:blind` | `src/shipharness/reviewer/blind.py:15-39` | What the reviewer never sees: harness artifacts, commit metadata, workspace paths, run ids, the arm label |
| 4 | `S4:gate` | `src/shipharness/harness/verify/gate.py:133-172` | Pending pills first, checks in the arm container, feedback only on failure; `GATE_CHECKS` (lines 31-41) has no hidden tests or mutants |

## 4. Poll question and answer pattern

Ask before `make demo-4`; the final feature poll follows it. The question (S4, slide 49):

> Building F4 (ETag, If-Match, issue history), both arms' visible tests pass at the end. The referee
> then runs 69 hidden tests (`teamtrack/tests/hidden/f4/`) and 4 referee-set mutants
> (`teamtrack/mutants/features/f4.jsonl`) against the tests each arm shipped. Which arm passes more
> hidden tests and kills more mutants?
>
> A. Harness arm on both counts
> B. Harness arm on hidden tests only
> C. Harness arm on mutants only
> D. No clear difference

Hint for the room after the vote: one referee mutant makes writes stop moving the version
(`issue.version += 1` becomes `+= 0`), which brings back lost updates. A shipped test catches it
only if it checks that a write moves the ETag, or that a save with the old version gets 412.

What pilot run 2 showed (measured in the course pilot, run 2, 2026-10-16): none of A to C held in
any of its three F4 A/Bs. The bare arm killed 3, 4, 3 mutants against the harness arm's 0, 0, 2,
and passed 69, 66, 69 hidden tests against 69, 61, 69. Pilot run 3 added the turn-cost change for
the harness arm (section 5a); measured in the course pilot, run 3, 2026-10-16, none of A to C held
in any of its three F4 A/Bs either: the bare arm killed 4, 0, 3 mutants against the harness arm's
0, 0, 0, and passed 66, 66, 69 hidden tests against 27, 69, 69 (section 7).

Answer pattern from the experiments:

[[PENDING: S4 poll answer pattern: referee mutants killed per arm across batch 1 runs (how often each of A-D held), plus tonight's result | source: M8 batch 1 | how: uv run shipharness report]]

## 5. What to watch

The gate runs while the concepts are on screen. In the demo block the run has finished, so screen
1 shows the last gate's pills and the full list of harness decisions, including every gate's
feedback; the LangSmith trace linked on screen 5 has the same turns.

Screen 1, Live Console:

- Harness arm, after `finish(claim="done")` in the build phase: pills for `visible tests`,
  `existing tests`, `R1` to `R7`, `board`, and `clean state` appear as ⏳, then turn ✓ or ✗
  (`run_gate` in `gate.py`). Progress labels such as `R1 probes <done>/<total>` show the gate
  working (`probe_all` in `r1_tenant.py`).
- On a failed gate, the harness decision shows the feedback the agent received:
  `Gate <id>: <n> of <m> items failed (<names>).`, up to three failure lines, then `Fix these,
  commit your work, and call finish again.` (`_feedback` in `gate.py`). Watch the next turns: does
  the agent fix the named item, or work around it?
- After the test phase: the decision `test filters: kept <n>, discarded <m>` (`verify/layer.py`).
- `BLOCKED <action>: <paths>` lines appear when the scope layer refuses a write
  (`src/shipharness/console/state.py`). The three F4 A/Bs of pilot run 2 had none: their events
  contain no `blocked` event, so do not promise one.
- Bare arm: "No gate (verify layer off)." and "None: bare arm has no layers." The phase ends on the
  agent's claim.
- Bottom of each panel: "Agent said" next to "Referee", then supported or unsupported. For F4 the
  referee mark is ✓ only when all 69 hidden tests pass and all 4 referee mutants are killed
  (`evaluate_primary` in `src/shipharness/ab/score.py`).

Screen 2, Boards:

- The conflict panel appears once per arm after its run ends (the preview container captures it
  for F4 only; `src/shipharness/ab/runtime.py`). The screenshot banner reads `✗ LOST UPDATE: tab B
  overwrote tab A without a conflict` or `✓ CONFLICT DETECTED: tab B got HTTP <status>`; a line
  starting `!` means the save failed some other way (`capture_conflict` in
  `src/shipharness/console/board_capture.py`).

Screen 3, Evidence, Verification panel:

- Referee rows per rule (`R1: <n> new` and so on) and, after the review, `reviewer accept` or
  `reviewer reject` with the tenant-isolation risk.
- Test filters (1-5): one row per test proposed in the test phase, ✓/✗ per filter, `kept` or
  `discarded`, and the discard reason under the row. Point at one discard and read its reason
  aloud. Tests written in the build phase have no row: they ship without the filters.
- `Coverage (filter 3: adds coverage or kills a mutant): <x> of <y> tests`.
- Mutants: one row per mutant, columns "filter set" and "referee set", outcome `killed` or
  `survived`. In `make demo-4` expect the filter-set column to show `–`: the verify layer's test
  phase builds its filter context without a mutant list (`filters_pipeline` in
  `src/shipharness/harness/verify/testphase.py`), so only the referee's rows appear. Find
  `app.services.issues-m401` (the lost-update mutant) for each arm.

Screen 4, A/B Report: two dot rows for F4, `hidden_passed` (of 69) and `mutants_killed` (of 4), one
dot per run per arm, with counts, never percentages.

Terminal: `make demo-4` ends with one line per arm in this format (`_print_record` in
`src/shipharness/ab/commands.py`), then the cost line (`cost_line` in `src/shipharness/ab/runtime.py`):

```text
  <arm> <status> claim=<claim> primary={"hidden_passed": <x>, "mutants_killed": <y>} passed=<bool> hidden <x>/69 mutants <y>/4 reviewer=<verdict> cost=$<usd>
Cost: $<this command> (this command: <model> $<usd>, ...; session $<spent> of $2.50; build $<spent> of $15.00 ($<left> left))
```

`make swap-4` prints `Swap test on <ab_id>: judged measures identical` and exits 0; any difference
is listed field by field and the exit code is 1 (`src/shipharness/ab/commands.py`).

If the harness arm never calls `finish(claim="done")`, no gate pills appear at all. That is what
happened in all three F4 A/Bs of pilot run 2: every arm used its 40 build turns and its claim was
`none`, so no gate ran. Say so; the referee still judges the shipped diff.

## 5a. What the harness arm does differently, and why

The harness arm differs from the bare arm in four places on F4 (concepts section 3). The bare arm
has none of them:

| Where | Harness arm | Why (concepts) |
|---|---|---|
| Start | 31 instruction files placed (map, docs, skills), the state files written, `feature_list.json` with F4 at `passes: false`, the gate baseline recorded (harness decisions at the start of every pilot run) | The map points to the rules both arms can read in `docs/HANDBOOK.md`; only the harness sets `passes` (course design) |
| `finish(claim="done")` in the build phase | The verify gate runs visible tests, existing tests, R1-R7, the board check, and clean state in the arm's container; a failure goes back as the `finish` result | The agent does not judge its own work (A3, F-a-110) |
| Test phase | Each test proposed in the 12-turn test phase goes through the five filters; only kept ones are committed. Tests written in the build phase ship without the filters | Filters 1-3 from B11 and B12; 4 and 5 are course filters |
| Every session start (after change 9) | The handoff's agent notes come before any document; a test-phase session starts with "write the tests for the feature first" (`TEST_PHASE_FIRST` in `src/shipharness/harness/state/lifecycle.py`) | Turns go to the ticket, not to re-reading (change 9 of the pilot change log) |

What it did in pilot run 2 (measured in the course pilot, run 2, 2026-10-16): it did not get ahead.
Every session repeated A2's "Getting up to speed" steps (A2, F-a-58 to F-a-62), re-read 3 to 7
instruction documents and about 15 product files, and updated progress.md and the exec plan
mid-session. It shipped 0, 0, and 3 tests, against the bare arm's 30, 33, and 8 (score records),
so its shipped tests killed 0, 0, and 2 referee mutants. None of those tests came from the test
phase: in A/Bs 1 and 2 the test phase proposed no test, and in A/B 3 (ab-20261016-191626-6100f6) the
three shipped tests were written in build session 1 while the test phase's one proposed test failed
filter 2. The gate never ran, because no arm claimed done. The fix for run 3 is change 9 above, a
harness change for the harness arm only. The two referee changes since run 2 (judge each arm when it
finishes; run the unmutated-pass step for all shipped tests in one batch) are measurement changes
with no outcome change: the batch step gave the same pass or fail outcome as one-test-at-a-time on
all 181 shipped tests of run 2.

What it did in pilot run 3, measured in the course pilot, run 3, 2026-10-16, A/Bs
ab-20261016-212252-aa1644, ab-20261016-214151-ca9841, and ab-20261016-220010-c5b4bf (from each
A/B's `events.jsonl`): with change 9 in place it still wrote no tests.

| Harness arm, per A/B | aa1644 | ca9841 | c5b4bf |
|---|---|---|---|
| Build session 1: turns used, of 40 | 40 | 40 | 40 |
| Build phase: patches to files under `tests/` | 0 | 0 | 0 |
| Test phase (session 2): turns used, of 12 | 12 | 7 | 6 |
| Test phase: tests proposed (filter decision) | 0 (`kept 0, discarded 0; no new tests to filter`) | 0 (same) | 0 (same) |
| Gate runs (`finish(claim="done")` calls) | 0 | 0 | 0 |
| Arm status | completed | ABORTED: timeout | ABORTED: timeout |

In all three A/Bs the build session spent its 40 turns reading and then patching product files
under `app/`, and never called `finish`, so the claim stayed `none` and the gate never ran. Each
test phase began by reading progress.md, session-handoff.md, and the exec plan and running `bash
init.sh` again; in ca9841 and c5b4bf the agent time limit ended the run during the test phase, and
in aa1644 the test phase's only patch was to progress.md. The filters therefore discarded nothing:
no test reached them. The harness arm shipped 0 tests in each A/B, so its tests killed 0 of 4
referee mutants each time.

## 6. Captured output and screenshots

Each item below is labelled "captured on <date>, run <id>; your output will differ". The excerpts
are lines of `events.jsonl` from the F4 A/Bs of pilot run 2, cut to their key fields ("..." marks a
cut). Pilot A/Bs ran with `--no-preview`, so they have no terminal transcript of `make demo-4` and
no board screenshots; those stay PENDING until the live class.

The harness arm's start, the same in every A/B (captured on 2026-10-16, run
ab-20261016-185422-8a8c2a; your output will differ):

```text
{... "arm":"harness","seq":83, ... "type":"harness_decision","data":{"kind":"note","layer":"instructions","message":"placed 31 instruction files (AGENTS.md map, docs, skills)", ...
{... "arm":"harness","seq":85, ... "type":"harness_decision","data":{"kind":"note","layer":"scope","message":"feature_list.json written with F4 (passes: false)", ...
{... "arm":"harness","seq":86, ... "type":"harness_decision","data":{"kind":"note","layer":"verify","message":"gate baseline recorded", ...
{... "arm":"harness","seq":134, ... "type":"harness_decision","data":{"kind":"note","layer":"instructions","message":"agent read ARCHITECTURE.md", ...
```

The harness arm's test phase in A/B 3 of pilot run 2: one proposed test, discarded at filter 2.
The three tests that arm shipped were written in build session 1 and never reached the filters
(captured on 2026-10-16, run ab-20261016-191626-6100f6; your output will differ):

```text
{... "arm":"harness","seq":435, ... "type":"test_filter_result","data":{"test_id":"tests/visible/test_issue_history_etag.py::test_issue_history_is_oldest_first_and_tenant_scoped","filter":1,"passed":true,"reason":"collected 1 test"}, ...
{... "arm":"harness","seq":436, ... "type":"test_filter_result","data":{"test_id":"tests/visible/test_issue_history_etag.py::test_issue_history_is_oldest_first_and_tenant_scoped","filter":2,"passed":false,"reason":"failed on run 1 of 5: assert None is not None"}, ...
{... "arm":"harness","seq":437, ... "type":"harness_decision","data":{"kind":"note","layer":"verify","message":"test filters: kept 0, discarded 1", ...
```

Referee mutants and verdicts in A/B 1 of pilot run 2: the lost-update mutant survived in both arms
(captured on 2026-10-16, run ab-20261016-182828-c81fc0; your output will differ):

```text
{... "arm":"harness","seq":399, ... "type":"mutant_result","data":{"mutant_id":"app.services.issues-m401","set":"referee","outcome":"survived","killed_by":null}, ...
{... "arm":"harness","seq":404, ... "type":"verdict", ... "summary":"agent said none; referee: fails the primary measure; hidden tests 69/69, mutants killed 0/4, R1 new 0"} ...
{... "arm":"bare","seq":431, ... "type":"mutant_result","data":{"mutant_id":"app.services.issues-m401","set":"referee","outcome":"survived","killed_by":null}, ...
{... "arm":"bare","seq":436, ... "type":"verdict", ... "summary":"agent said none; referee: fails the primary measure; hidden tests 69/69, mutants killed 3/4, R1 new 0"} ...
```

One blinded-reviewer finding on the harness arm of the same A/B, which names the same weakness as
the surviving mutant (captured on 2026-10-16, run ab-20261016-182828-c81fc0, `reviewer_output`;
your output will differ):

```text
{... "arm":"harness","seq":403, ... "type":"reviewer_output","data":{"findings":[{"file":"app/services/issues.py","line":100,"severity":"blocker","criterion":"Stop lost updates and return a new ETag for every successful write","comment":"Writes without If-Match do not increment issue.version. An unconditional edit can therefore leave the same ETag in place, allowing a later conditional edit based on the old version to overwrite it."}, ...
```

[[PENDING: terminal output of make demo-4 (A/B line, both record lines, cost line) | source: live class | how: make demo-4]]

[[PENDING: screenshot, screen 1 Live Console during the harness arm's first gate (pills pending, then results; bare arm "No gate") | source: live class | how: make demo-4 with make console open, key 1]]

[[PENDING: screenshot, screen 1 Live Console after the referee ("Agent said" vs "Referee" for both arms) | source: live class | how: make demo-4, key 1]]

[[PENDING: screenshot, screen 2 Boards with the two-tab edit conflict panel for both arms | source: live class | how: make demo-4, key 2]]

[[PENDING: screenshot, screen 3 Evidence, Verification panel (referee counters, filter table with a discard reason, coverage line, mutant matrix) | source: live class | how: make demo-4, key 3]]

[[PENDING: screenshot, screen 4 A/B Report with the S4 dots | source: live class | how: uv run shipharness report, then make demo-4, key 4]]

[[PENDING: terminal output of make swap-4 | source: live class | how: make swap-4]]

[[PENDING: terminal output and screen 1 of make demo-4 LAYERS=-verify | source: live class | how: make demo-4 LAYERS=-verify]]

## 7. Experiment results for this section

### Pilot run 2 (2026-10-16, F4 canonical, three A/Bs)

One row per arm run, copied from the score records `exports/scores/<run_id>.json` of the course
pilot (captured on 2026-10-16, runs as listed in the table; your output will differ):

| A/B | Arm | Run id | Status | Hidden of 69 | Referee mutants of 4 | Tests shipped | Existing tests | Reviewer |
|---|---|---|---|---|---|---|---|---|
| ab-20261016-182828-c81fc0 | bare | r-20261016-182828-1daced | ABORTED: timeout | 69 | 3 | 30 | 190/190 | reject |
| ab-20261016-182828-c81fc0 | harness | r-20261016-182828-7d66af | ABORTED: timeout | 69 | 0 | 0 | 190/190 | reject |
| ab-20261016-185422-8a8c2a | bare | r-20261016-185422-ce2096 | completed | 66 | 4 | 33 | 190/190 | reject |
| ab-20261016-185422-8a8c2a | harness | r-20261016-185422-618828 | completed | 61 | 0 | 0 | 190/190 | reject |
| ab-20261016-191626-6100f6 | bare | r-20261016-191626-e55f2f | completed | 69 | 3 | 8 | 190/190 | reject |
| ab-20261016-191626-6100f6 | harness | r-20261016-191626-7aebe4 | ABORTED: timeout | 69 | 2 | 3 | 190/190 | reject |

In all six records the claim is `none`, `passed_primary` is false, the new R1-R7 violation counts
are 0, `board_ok` is true, `flaky_tests` is 0, and `reviewer_agrees` is true. Every arm passes all
hidden tests in at least one A/B, so the hidden-test count alone does not separate the arms here;
the mutant count does, in the bare arm's favour.

### Pilot run 3 (2026-10-16, F4 canonical, three A/Bs)

Measured in the course pilot, run 3, 2026-10-16, effort medium, two A/Bs in parallel, after changes
7-13 of the pilot change log (change 9 is the turn-cost change in section 5a). One row per arm run,
from the score records (captured on 2026-10-16, runs as listed in the table; your output will
differ):

| A/B | Arm | Run id | Status | Hidden of 69 | Referee mutants of 4 | Tests shipped | Out-of-scope files | R1 new | Reviewer |
|---|---|---|---|---|---|---|---|---|---|
| ab-20261016-212252-aa1644 | bare | r-20261016-212252-eb2cb4 | ABORTED: timeout | 66 | 4 | 23 | 2 | 0 | reject |
| ab-20261016-212252-aa1644 | harness | r-20261016-212252-1623c9 | completed | 27 | 0 | 0 | 0 | 3 | reject |
| ab-20261016-214151-ca9841 | bare | r-20261016-214151-23531c | ABORTED: timeout | 66 | 0 | 0 | 2 | 0 | reject |
| ab-20261016-214151-ca9841 | harness | r-20261016-214151-c0e492 | ABORTED: timeout | 69 | 0 | 0 | 0 | 0 | reject |
| ab-20261016-220010-c5b4bf | bare | r-20261016-220010-087344 | ABORTED: timeout | 69 | 3 | 5 | 1 | 0 | reject |
| ab-20261016-220010-c5b4bf | harness | r-20261016-220010-aabcbb | ABORTED: timeout | 69 | 0 | 0 | 0 | 0 | reject |

Both arms failed the primary measure in 3 of 3 A/Bs: no measurable difference on this task with
this model (course pilot, run 3). No arm passed all 69 hidden tests and killed all 4 referee
mutants in the same run. Pilot run 4 (effort low) ran F1-F3 only, so F4 has no run 4 result.

### Batch 1

Batch 1 runs F4 canonical, two arms, k=10 (course experiment plan). Each run is a dot for each
co-primary count.

[[PENDING: S4 batch 1 dots (hidden x/69 and referee mutants y/4, per run, bare vs harness) with run ids and the LangSmith comparison link | source: M8 batch 1 | how: uv run shipharness experiments --split section-4 --k 10 --batch batch-1, then uv run shipharness report]]

[[PENDING: S4 secondary measures from batch 1 (existing tests, R1-R7 new violations, flaky tests, reviewer agreement) | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: leave-one-out result with the verify layer removed, on the ablation tasks | source: M8 ablation | how: uv run shipharness experiments --split section-4 --layers=-verify --batch ablation, then uv run shipharness report]]

## 8. Measured time and cost

Limits from the repository (not measurements; `src/shipharness/config/settings.py`): agent time per
arm `RUN_TIMEOUT_S` 300 s, harness work per arm `HARNESS_TIMEOUT_S` 120 s, tool command
`TOOL_TIMEOUT_S` 120 s; cost caps $0.20 per arm (`MAX_RUN_COST_USD`) and $0.04 per review
(`MAX_REVIEW_COST_USD`); F4 session budget 40 turns (`teamtrack/reference/f4/task.toml`). By those
caps the two demo-4 arms and their two reviews cost at most $0.48. The final A/B running beside
demo-4 has its own arm cap, `MAX_FINAL_RUN_COST_USD` ($0.25), and the same review cap; both
commands count against the one session cap of $2.50.

Measured in the course pilot, run 2, 2026-10-16 (F4 rows): agent time 225-310 s for the bare arm and
269-314 s for the harness arm, harness time 101-132 s for the harness arm; the agent time limit was
hit in 1 of 3 bare runs and 2 of 3 harness runs. Across all 12 run-2 A/Bs (two in parallel), wall
time from first event to last verdict was 485 s minimum, 641 s median, 923 s maximum, with the
referee taking a median 331 s from an arm's end to its verdict before changes 10 and 11. All 12
run-2 A/Bs with reviews cost $0.3966.

Per arm, from the score records (captured on 2026-10-16, runs as listed in the table; your output
will differ):

| Run id | Arm | `wall_s` | `cost_usd` | `review_cost_usd` |
|---|---|---|---|---|
| r-20261016-182828-1daced | bare | 310.173 | 0.015296 | 0.004127 |
| r-20261016-182828-7d66af | harness | 422.691 | 0.016684 | 0.004066 |
| r-20261016-185422-ce2096 | bare | 225.33 | 0.016903 | 0.004038 |
| r-20261016-185422-618828 | harness | 369.779 | 0.016342 | 0.003399 |
| r-20261016-191626-e55f2f | bare | 281.933 | 0.019123 | 0.004327 |
| r-20261016-191626-7aebe4 | harness | 409.127 | 0.018463 | 0.004193 |

Every arm stayed below the $0.20 arm cap and every review below the $0.04 review cap.

Measured in the course pilot, run 3, 2026-10-16 (F4 rows, after changes 7-13, two A/Bs in
parallel), from the pilot summary (captured on 2026-10-16, runs as listed in the table; your output
will differ):

| A/B | Run id | Arm | Agent s | Harness s | Cost $ | Review $ | A/B wall s |
|---|---|---|---|---|---|---|---|
| ab-20261016-212252-aa1644 | r-20261016-212252-eb2cb4 | bare | 320 | 0 | 0.0166 | 0.0043 | 623.6 |
| ab-20261016-212252-aa1644 | r-20261016-212252-1623c9 | harness | 270 | 91 | 0.0187 | 0.0032 | 623.6 |
| ab-20261016-214151-ca9841 | r-20261016-214151-23531c | bare | 302 | 0 | 0.0136 | 0.0043 | 486.2 |
| ab-20261016-214151-ca9841 | r-20261016-214151-c0e492 | harness | 321 | 67 | 0.0149 | 0.0023 | 486.2 |
| ab-20261016-220010-c5b4bf | r-20261016-220010-087344 | bare | 328 | 0 | 0.0170 | 0.0046 | 535.6 |
| ab-20261016-220010-c5b4bf | r-20261016-220010-aabcbb | harness | 316 | 61 | 0.0169 | 0.0041 | 535.6 |

The agent time limit was hit in 3 of 3 bare runs and 2 of 3 harness runs. Every arm stayed below
the $0.20 arm cap and every review below the $0.04 review cap. Across all 12 run-3 A/Bs (sections
F1-F4), wall time from first event to last verdict was 384 s minimum, 512 s median, 620 s maximum
(the maximum is ab-20261016-212252-aa1644; the pilot summary column above is a separate
measurement and lists it as 623.6 s). All 12 run-3 A/Bs with reviews
cost $0.3801. F4 was not part of pilot run 4.

[[PENDING: wall time of make demo-4 on the class host with make final running in parallel, launch to Cost line | source: M6 pilot | how: course pilot (build repository)]]

[[PENDING: tonight's time and cost of make demo-4 | source: live class | how: make demo-4]]

## 9. Troubleshooting and the replay fallback

| Symptom | Cause (from the code) | What to do |
|---|---|---|
| Harness arm shows no gate pills by the end of the run | The agent never called `finish(claim="done")`; the gate runs only on a done claim (`run_gate` in `gate.py`). Seen in every F4 arm of pilot run 2 | Nothing to fix: the claim is `none` and the referee judges the shipped diff. Show the test-phase decision and the referee counts instead |
| `make swap-4` prints a line starting `x` that ends "run `make demo-4` first, or pass AB=<id>", and exits 2 | No demo-4 A/B in `RUNS_DIR` (`.shipharness/runs`) | Run `make demo-4`, or pass `AB=<id>` of a recorded A/B |
| `make swap-4` or `make replay` prints `x ...` about an unpinned record and exits 2 | The A/B record has no `checkpoint_sha` (`UnpinnedRecord` in `src/shipharness/ab/recorded.py`) | Use an A/B recorded after SHA pinning |
| Every gate pill ✗ with `could not write the check inputs in the container` or `check runner failed (exit <n>)` | The harness time limit (`HARNESS_TIMEOUT_S`) ran out; every gate command is capped by the harness time left (`GateConfig.limit`) | Keep the run: every run is scored (course design). Say what happened; show the experiment dots |
| A tool result reads `Refused, not run: ...` | A tool call came after the run or session ended (`src/shipharness/runner/loop.py`) | Nothing to fix; the referee still judges the shipped diff |
| Status `ABORTED: cap` or `ABORTED: timeout` | Run cost cap or `RUN_TIMEOUT_S` reached (`runner/loop.py`) | The referee still runs; the run stays a dot |
| No "Two-tab edit conflict" panel; boards say "No board screenshot yet" | The preview container failed to start and was skipped | Use screen 3 (board check) and the hidden board tests counted in `hidden <x>/69` |
| `mutants 0/0` in the record | The mutant set could not be loaded (`src/shipharness/ab/mutants.py`); the run continues and scores 0/0 | Run `uv run shipharness datasets validate datasets/teamtrack-features-v1.jsonl --kind features` (checks that every mutant set exists and applies at its checkpoint); the run still counts |
| `reviewer=None` | The review was incomplete, refused, failed, or hit `MAX_REVIEW_COST_USD` (`reviewer/review.py`) | Primary counts are unaffected; say so |
| Verdict text `referee could not judge the build: ...` | The referee container failed to start (`ab/referee.py`) | Check Docker (`make doctor`), then `make swap-4` re-judges the recorded diffs without model calls |
| Red badge `UNSANDBOXED — results not official` | `SANDBOX_MODE` is not `docker` | Set `SANDBOX_MODE=docker` in `.env`, start Docker Engine in WSL2, `make doctor` |
| Layer-switch arms end at once with `ABORTED: cap` | Session cap reached (`MAX_SESSION_COST_USD`); the tracker reserves each call's worst case first (`src/shipharness/cost/tracker.py`) | Use `make swap-4` (no model calls) and the ablation dots instead |

### Replay fallback

Use only when the live run fails on stage. `make replay RUN=<id>` takes an A/B id or run id. It
re-emits the recorded events with `recorded=True` (red RECORDING badge on every screen), applies the
recorded diffs to a fresh export of the pinned checkpoint commit, and runs the referee live
(`src/shipharness/ab/recorded.py`). The reviewer is off by default for `replay`, so no model is
called. The terminal prints `RECORDING: replay <new id> of <source id> (<n> events)`, the record
lines, and the cost line.

The three F4 A/Bs of pilot run 2 are recorded (section 7), but they predate changes 9-11. The A/B
id to replay in class is chosen after pilot run 3 and goes on the instructor's fallback list:

[[PENDING: run id of the recorded F4 A/B to use for make replay, with its capture date | source: M6 pilot | how: course pilot (build repository)]]
