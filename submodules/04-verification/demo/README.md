# S4 demo: harness in action (`make show-4`), and the launch of the final A/B

Runbook for the S4 block in class. It covers the poll, the two launches (`make show-4` and `make
final`), what runs while the concepts and the code walkthrough are on screen, and the 15-minute demo
block: the harness arm at work on F4, a real run replayed, a constructed example, and the honest
results. Concepts: [../concepts.md](../concepts.md).

Every captured block in this file is labelled "captured on <date>, run <id>; your output will
differ". Source IDs such as (A3, F-a-110) resolve in [REFERENCES.md](../../../REFERENCES.md).

---

## 1. What this section shows, and why

**The problem.** F4 (`teamtrack/docs/features/f4.md`) adds optimistic concurrency and issue history
from checkpoint `m1-s4-start`. The `If-Match` header is optional, so every existing test keeps
passing whether or not concurrency works. An agent can test the happy path, call
`finish(claim="done")`, and ship a board where two people editing one issue overwrite each other.
The referee judges every run on two counts the agent never sees: hidden tests passed (of 69) and
referee-set mutants killed by the shipped tests (of 4).

**Why no live A/B in S4.** The class plan (course design) keeps a live bare-against-harness A/B
only where the course's pilot data shows a gap. On F4 it does not: both arms failed the primary
measure in 3 of 3 A/Bs of pilot run 3 and in the one A/B of the class-profile round (section 12).
That is "no measurable difference on this task with this model". So S4 shows the verification layer
doing its job instead, in three labelled parts, and leaves the measurement lesson to the final:

| Part | Command | Label on screen | Model calls |
|---|---|---|---|
| Harness in action: the harness arm alone on F4, live (handoffs between sessions, the test phase, the five test filters) | `make show-4` | `▶ HARNESS IN ACTION — one arm, not an A/B` | yes |
| Real run, replayed: the class-profile round's F4 A/B, where the bare arm claimed done with 68 of 69 hidden tests passing and the referee failed it | `make replay RUN=ab-20261017-090903-926c02` | `● RECORDING` | no |
| Constructed example: a scripted done claim with a failing test, refused by the gate, then accepted after the fix | `make example-4` | `CONSTRUCTED EXAMPLE` | no |
| The final: one live A/B on the feature the room picks, launched in S4 and read in the final block | `make final FEATURES=<poll winner>` | none (a live A/B) | yes |

The verification layer's assumption, in the course's words: the agent's "done" and its own tests
cannot be trusted (after A3, F-a-124; cause 4: A3, F-a-15; A4, F-a-17). The three parts show what
the layer does about that; the results slide shows what the pilot measured, wins and "no measurable
difference" alike.

## 2. Before class

Run everything inside WSL2 from the repository root (`~/shipharness`).

| Step | Command | What you should see | If it fails |
|---|---|---|---|
| 1. Keys, Docker, versions | `make doctor` | every line ok (it lists OpenAI models and one LangSmith project; no tokens) | fix the line it names; `SANDBOX_MODE=docker` must be set in `.env` |
| 2. Class date | set `SHIPHARNESS_CLASS_DATE=<YYYY-MM-DD>` in `.env` | class commands start | without it every class command stops with `x SHIPHARNESS_CLASS_DATE is not set: ...` and exit 2 |
| 3. Warm the host | `make warm` | one line per step with its time; a second run finds everything in place | read the step it names; rerunning is safe (no model calls) |
| 4. Console | `make console` (terminal A) | the console at `http://localhost:8765/` | `CONSOLE_PORT=8766 make console` if the port is taken |
| 5. The recorded A/B is on the host | `ls .shipharness/runs/ab-20261017-090903-926c02` | `ab.json`, `events.jsonl`, `bare/`, `harness/`, `screenshots/` | copy the run folder from the build host, or use another recorded F4 A/B (section 15) |

`make warm` was measured on the class host before the class-profile round (2026-10-17): the first
run took 407 s (images rebuilt in 145 s, 7 referee baselines and 4 gate baselines), the second 1.2
s. Without it the first launch pays that cost.

## 3. Commands

| Command | Terminal | When | What it runs (`make -n`, checked on 2026-10-17, except `make example-4`) |
|---|---|---|---|
| `make show-4` | B | section minute 4 | `uv run shipharness ab --section demo-4 --feature F4 --arms harness --purpose class --profile class` |
| `make final FEATURES=<poll winner>` | C | section minute 5 | for each feature: `uv run shipharness ab --section final --feature <f> --purpose class --profile class` |
| `make replay RUN=ab-20261017-090903-926c02` | B | minute 25, after `make show-4` has printed its `Cost:` line | `uv run shipharness replay ab-20261017-090903-926c02 --purpose class` |
| `make example-4` | B | demo block | `shipharness example --section demo-4`: scripted steps, no model |
| `make swap-4 AB=ab-20261017-090903-926c02` | B | optional, demo block | `uv run shipharness ab --swap ab-20261017-090903-926c02 --section demo-4 --purpose class` |

`uv run shipharness ab --help` lists the two options the class runs add: `--profile` ("standard
(settings as loaded) or class (live class runs: low effort, Fast, 2 CPUs)") and `--arms` ("both
(A/B, default) or harness (the harness arm alone: harness in action)"). The class profile is the
same for every arm: reasoning effort low, 2 CPUs per arm and referee container, and OpenAI's Fast
tier for the agent; the reviewer keeps its own settings.

What each command prints when it ends (formats from `src/shipharness/ab/commands.py`):

```text
A/B <ab_id> (<feature>, layers=[...], profile=class, harness in action)
  <arm> <status> claim=<claim> primary=<values> passed=<bool> hidden <x>/<n> mutants <y>/<m> reviewer=<verdict> cost=$<usd>
Cost: $<this command> (this command: <model> $<usd>, ...; session $<spent> of $2.50; build $<spent> of $15.00 ($<left> left))
```

`, harness in action` appears only for `make show-4`, which prints one record line (the harness
arm); `make final` prints two record lines per feature;
`make replay` starts with `RECORDING: replay <new id> of ab-20261017-090903-926c02 (<n> events)`.
Exit codes: 0 when every arm completed, 2 when an arm was aborted (agent time limit or cost cap), 1
on an error.

Captured output of `make show-4`:

[[CAPTURE: terminal output of make show-4 (A/B line, the harness record line, the Cost line) with its date and ab id | how: make show-4]]

The swap test works on an A/B only: on the `make show-4` id it stops with `x <id> is a single-arm
run (harness in action): the swap test needs both arms; pass the id of an A/B`. On
ab-20261017-090903-926c02 it re-judges both recorded diffs with the labels swapped, with no model
calls, and prints `Swap test on <ab_id>: judged measures identical` (exit 0) or each difference
(exit 1). The layer switch (`make demo-4 LAYERS=-verify`) would be a new A/B and is not part of the
class plan.

## 4. The section, minute by minute

| Section minutes | Block | Terminals and console |
|---|---|---|
| 0-3 | S4 poll (section 5) | |
| 3-4 | Final feature poll (F5, F6, or F7) | Close it before the launch |
| 4-6 | Launch | Minute 4: `make show-4` in terminal B, open its run on the console (screen `1`). Minute 5: `make final FEATURES=<winner>` in terminal C, open its run in a second browser tab and leave it for the final block |
| 6-20 | Concepts ([../concepts.md](../concepts.md)) | Both runs proceed |
| 20-30 | Code walkthrough (section 11) | Minute 25: check terminal B for the `Cost:` line of `make show-4` and terminal C for the final's; then start `make replay RUN=ab-20261017-090903-926c02` in terminal B |
| 30-45 | Demo block | `make show-4` on screens 1, 3, 2 (section 6); the replay on screens 1 and 3 (section 7); `make example-4` (section 8); the results slide and screen 4 (section 9) |
| 45-50 | Discussion and transition | The final A/B is read in the final block (section 10) |

The console's runs list shows ids only, newest first. Open the `make show-4` run right after the
launch, before `make final` starts, so the two do not get mixed up; after a run,
`http://localhost:8765/run/<ab_id>` opens it directly. Keys `1` to `5` switch screens; `F` shows
one arm full screen.

**Will it be ready by minute 25?** In the class-profile round (one A/B at a time, 2026-10-17) the
F4 harness arm reached its primary verdict 811 s and its full verdict 927 s after the launch
(ab-20261017-090903-926c02). Its harness time was 433 s against 311 s of agent time, mostly the test
filters running each of its 6 test-phase tests up to 5 times. Every A/B of that round finished
within 15.5 minutes of its launch. A launch at minute 4 that takes as long ends near minute 20.
The time of `make show-4` itself, with `make final` running beside it:

[[CAPTURE: launch to primary verdict and launch to full verdict of make show-4 (class profile), with its ab id | how: make show-4]]

If `make show-4` has no full verdict at minute 30, open the demo block on the running arm (screen
1 and the filter table fill in as it goes) and show the replay first (section 7).

## 5. Poll question and answer pattern

Ask before the launch; the final feature poll follows it (S4, slide 49):

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

Answer pattern from the course's seven F4 A/Bs (hidden of 69 and mutants of 4, bare against
harness; A/B ids in section 12):

| A/B | Hidden, bare / harness | Mutants, bare / harness | Which of A-C held |
|---|---|---|---|
| Run 2, A/B 1 | 69 / 69 | 3 / 0 | none |
| Run 2, A/B 2 | 66 / 61 | 4 / 0 | none |
| Run 2, A/B 3 | 69 / 69 | 3 / 2 | none |
| Run 3, A/B 1 | 66 / 27 | 4 / 0 | none |
| Run 3, A/B 2 | 66 / 69 | 0 / 0 | B |
| Run 3, A/B 3 | 69 / 69 | 3 / 0 | none |
| Class-profile round | 68 / 68 | 4 / 1 | none |

A held in none of the seven, B in one, C in none; the harness arm never killed more mutants than
the bare arm. Say it plainly: on this task with this model, the harness arm did not get ahead.

## 6. What to watch: `make show-4` (harness in action)

Every screen shows the badge `▶ HARNESS IN ACTION — one arm, not an A/B` and `profile: class`.
The bare panel on screen 1 reads "Not run: harness in action shows the harness arm alone. The
bare-vs-harness comparison comes from the A/B runs (make demo-N)."

While the run is live, screen `1` keeps the last 8 turn rows and the last 3 harness decisions;
after the run it lists all of them in scrollable lists. Point at these, in order:

| Moment | Where | What appears |
|---|---|---|
| Start | Screen 1, harness decisions | `placed 31 instruction files (AGENTS.md map, docs, skills)`, the initializer step, `feature_list.json written with F4 (passes: false)`, the gate baseline |
| A write outside the ticket | Screen 1 | `BLOCKED reject_patch: <path>`: the scope layer refused the patch (only if the agent tries one) |
| End of a build session | Screen 1, turn list | "Session 1 stopped" with `session 1 handoff written to session-handoff.md`; the next session resumes from it |
| A done claim | Screen 1 | Gate pills `visible tests`, `existing tests`, `R1` to `R7`, `board`, `clean state`: ⏳, then ✓ or ✗. On ✗ the agent gets `Gate <id>: <n> of <m> items failed (<names>).`, up to three failure lines, and `Fix these, commit your work, and call finish again.` (`_feedback` in `src/shipharness/harness/verify/gate.py`) |
| Test phase (12 turns) | Screen 3, Verification panel | One row per proposed test, ✓/✗ per filter 1-5, `kept` or `discarded`, and the reason under the row; then `test filters: kept <n>, discarded <m>` on screen 1 |
| Referee | Screen 1, bottom of the panel | `referee pending`, then `primary verdict ready: PASS` or `FAIL` with the two counts, `secondary checks running`, and "launch to primary verdict mm:ss · launch to full verdict mm:ss" |
| After the run | Screen 2, Boards | The "Two-tab edit conflict" panel: `✓ CONFLICT DETECTED: tab B got HTTP <status>` or `✗ LOST UPDATE: tab B overwrote tab A without a conflict` |

If no gate pills appear, the agent never claimed done; the gate runs only on `finish(claim="done")`.
That happened in every F4 harness arm of the pilot and the class-profile round (section 12). Say so:
the referee still judges the shipped diff, and the constructed example (section 8) shows the gate
refusing a claim.

What the same harness arm did in the class-profile round, as screen 1 and screen 3 showed it
(events cut to their key fields, "..." marks a cut; captured on 2026-10-17, run
ab-20261017-090903-926c02; your output will differ):

```text
{..."arm":"harness","seq":10,..."type":"harness_decision","data":{"kind":"note","layer":"scope","message":"feature_list.json written with F4 (passes: false)",...
{..."arm":"harness","seq":160,..."type":"harness_decision","data":{"kind":"block","layer":"scope","message":"app/services/errors.py: outside the allowed paths for the build phase (...); patch not applied",...
{..."arm":"harness","seq":324,..."type":"claim","data":{"phase":"build","claim":"not_done","summary":"Committed partial F4 implementation as 39b59d5. ... Work is incomplete: Ruff check reports errors, and feature regression tests have not been added.","gate_id":null},...
{..."arm":"harness","seq":329,..."type":"harness_decision","data":{"kind":"session_stop","layer":"state","message":"session 1 handoff written to session-handoff.md",...
{..."arm":"harness","seq":396,..."type":"test_filter_result","data":{...,"filter":3,"passed":false,"reason":"adds no line coverage over the existing suite and kills no filter-set mutant that the existing tests miss (0 checked)"},...
{..."arm":"harness","seq":400,..."type":"test_filter_result","data":{...,"filter":3,"passed":true,"reason":"adds 3 covered lines: app/api/issues.py:32,34; app/services/issues.py:105"},...
{..."arm":"harness","seq":411,..."type":"test_filter_result","data":{...,"filter":2,"passed":false,"reason":"failed on run 1 of 5: AssertionError: assert 412 == 404"},...
{..."arm":"harness","seq":424,..."type":"harness_decision","data":{"kind":"note","layer":"verify","message":"test filters: kept 4, discarded 2",...
{..."arm":"harness","seq":425,..."type":"run_end","data":{"status":"ABORTED: timeout","claim":"not_done","cost_usd":0.025744,"turns_total":43,"wall_s":744.581},...
```

Read it aloud: the arm stopped its build with `not_done`, so no gate ran; the scope layer refused
one write; the test phase proposed 6 tests, filter 2 caught one that failed on its first run, filter
3 caught one that added nothing, and 4 shipped. "(0 checked)" means the test-phase context has no
filter-set mutant list, so filter 3 decided by coverage alone.

In class: read the `primary verdict ready` pill and the two counts off screen 1, and say which count
failed. Then say the record is not an A/B: screen 4 leaves single-arm runs out of the comparison
("<n> single-arm run (harness in action) not compared: no bare run.").

[[CAPTURE: screen 1 and screen 3 of make show-4 after the referee (gate pills or "No gate", the filter table with a discard reason, the primary verdict pill) | how: make show-4 with make console open, keys 1 and 3]]

## 7. What to watch: the replay (real run, replayed)

`make replay RUN=ab-20261017-090903-926c02` re-emits the recorded events of the class-profile
round's F4 A/B with `recorded=True`, so every screen shows `● RECORDING`, and then re-runs the
referee live on the recorded diffs, one arm after the other (`replay_ab` in
`src/shipharness/ab/recorded.py`). The reviewer is off and no model is called. The recorded
verdicts appear with the events; the live referee adds its own afterwards.

What to point at, on screen 1 and screen 3:

- Bare arm, "Agent said" `done`; "Referee" fail. Its claim: "Verified the complete visible suite
  (191 passing)". The referee: hidden tests 68 of 69, mutants 4 of 4, so it fails the primary
  measure. Nothing in the bare arm checked the claim: it has no layers.
- Screen 1 shows the two counts under each referee pill. The name of the one failing hidden test,
  the same in both arms, is in the run log (`check_result` for `hidden_tests`, below); screen 3's
  `hidden_tests` row counts only new failures against the checkpoint, so do not point at it for this.
- Screen 3, bare arm: `diff_scope: 1 new`. The bare arm changed `app/services/errors.py`, the file
  the harness arm's scope layer refused in section 6.
- Harness arm: "Agent said" `not_done`, no gate pills, the filter table from section 6.
- Screen 2: both arms show `✓ CONFLICT DETECTED`: the board stops the two-tab lost update in both,
  yet both fail the hidden test.

The recorded lines (captured on 2026-10-17, run ab-20261017-090903-926c02; your output will differ):

```text
{..."arm":"bare","seq":222,..."type":"claim","data":{"phase":"build","claim":"done","summary":"... Added regression coverage for ETags, stale writes, and history. Verified the complete visible suite (191 passing) and committed as e1bb6d4.","gate_id":null},...
{..."arm":"bare","seq":311,..."type":"check_result","data":{"check":"hidden_tests",...,"total_probes":69,"findings":[{"rule":"hidden","severity":"violation",...,"detail":"tests/hidden/f4/test_f4_concurrency.py::test_invalid_body_with_a_stale_version_is_412: failed",...
{..."arm":"bare","seq":328,..."type":"primary_verdict","data":{...,"passed":false,"values":{"hidden_passed":68,"mutants_killed":4},"elapsed_s":79.017},...
{..."arm":"bare","seq":392,..."type":"verdict","data":{...,"summary":"agent said done; referee: fails the primary measure; hidden tests 68/69, mutants killed 4/4, R1 new 0"},...
{..."arm":"harness","seq":459,..."type":"verdict","data":{...,"summary":"agent said not_done; referee: fails the primary measure; hidden tests 68/69, mutants killed 1/4, R1 new 0"},...
```

Why it matters: it is the case the verification layer is built for, a "done" the referee
contradicts (A3, F-a-15; A4, F-a-17). Be exact about what the gate would have done: it runs visible
tests, existing tests, R1-R7, the board check, and clean state, not the hidden tests (`GATE_CHECKS`
in `gate.py`), so it does not run this hidden test. What separates the claim from the verdict here
is the referee's held-out check (B13, F-b-43).

[[CAPTURE: terminal output of make replay RUN=ab-20261017-090903-926c02 (the RECORDING line, both record lines, the Cost line) | how: make replay RUN=ab-20261017-090903-926c02]]

## 8. What to watch: the constructed example

`make example-4` runs `shipharness example --section demo-4`: scripted steps, no model, and a
`CONSTRUCTED EXAMPLE` badge on every console screen. The script makes a done claim while one test
fails; the gate refuses it and sends back its feedback; the script fixes the test and claims done
again; the gate accepts the claim. It is labelled "constructed example" in class, never presented as
a run of the agent.

Point at: the gate pills on screen 1 going ⏳ then ✗ on the first claim; the feedback line `Gate
<id>: <n> of <m> items failed (<names>).` with the failure lines and `Fix these, commit your work,
and call finish again.`; then all pills ✓ on the second claim.

[[CAPTURE: terminal output of make example-4 and screen 1 with the refused claim (gate pills, feedback) and the accepted claim | how: make example-4 with make console open, key 1]]

## 9. The results slide and screen 4

One slide and one console view show every result, wins and "no measurable difference" alike.

Screen 4 (A/B Report) reads the score records in `exports/scores/` and shows one dot per run for
each feature, variant, and arm: ● passed the primary measure, ○ failed, with the count passed of
runs. It leaves out records scored under an older referee version, and lists replays ("<n> runs
are replays (recorded).") and single-arm runs separately (`src/shipharness/console/report.py`). The
dots on the class host depend on the records it holds.

What to say, from the course's data (section 12): F4 failed the primary measure in both arms in
every A/B of pilot runs 2 and 3 and of the class-profile round, so S4 is "no measurable difference
on this task with this model". S1-S3 passed in both arms in runs 3 and 4 and the class-profile
round: the same verdict. Post hoc (measures chosen after the results; descriptive), over runs 2-4
and the live console check: harness arms changed files outside the allowed paths in 0 of 34 runs,
bare arms in 9 of 34; harness arms shipped a median of 2.5 tests against 7.5; no done claim came
with failing hidden tests in either arm; the class-profile round's bare F4 claim did.

## 10. The final A/B (launched here, read in the final block)

`make final FEATURES=<poll winner>` is the course's one live A/B: both arms with all four layers on
the harness side, from checkpoint `m1-final-start`. F5-F7 have no pre-registered primary measure
(the dataset's `primary_measure` is empty), so the referee reports every score. Each arm is capped at
`MAX_FINAL_RUN_COST_USD` ($0.25) and each review at `MAX_REVIEW_COST_USD` ($0.04)
(`src/shipharness/config/settings.py`). `make final` runs its features one after another, so at most
two runs proceed at once in S4: the final A/B and `make show-4`.

The lesson for the final block: one A/B is one dot. A difference in one A/B is not a result, and
neither is no difference. The F4 rows in section 12 show how far one arm moves between A/Bs of the
same ticket: the bare arm killed 3, 4, 3 referee mutants in run 2 and 4, 0, 3 in run 3.

[[CAPTURE: terminal output of make final FEATURES=F5 (A/B line, both record lines, Cost line), its launch to full verdict time, and its ab id | how: make final FEATURES=F5]]

## 11. Code walkthrough (10 minutes, while the runs proceed)

`uv run python scripts/anchors.py extract <id>` prints each anchor.

| Order | Anchor | File and lines | Point at |
|---|---|---|---|
| 1 | `S4:filters` | `src/shipharness/filters/pipeline.py:34-74` | A test stops at its first failing filter; every result is published with a reason |
| 2 | `S4:probe` | `src/shipharness/checks/r1_tenant.py:65-104` | R1: a foreign id must give 404; a 2xx carrying Globex data is a leak |
| 3 | `S4:blind` | `src/shipharness/reviewer/blind.py:15-39` | What the reviewer never sees: harness artifacts, commit metadata, workspace paths, run ids, the arm label |
| 4 | `S4:gate` | `src/shipharness/harness/verify/gate.py:133-172` | Pending pills first, checks in the arm container, feedback only on failure; `GATE_CHECKS` (lines 31-41) has no hidden tests or mutants |

## 12. Results for this section

Every F4 A/B the course ran, from the score records (captured on 2026-10-16 and 2026-10-17, runs as
listed; your output will differ). Pilot runs 2 and 3 used effort medium; the class-profile round
used the class profile (effort low, Fast tier, 2 CPUs per container, five flakiness re-runs).

| Run | A/B | Arm | Run id | Status | Claim | Hidden of 69 | Referee mutants of 4 | Tests shipped |
|---|---|---|---|---|---|---|---|---|
| Pilot run 2 | ab-20261016-182828-c81fc0 | bare | r-20261016-182828-1daced | ABORTED: timeout | none | 69 | 3 | 30 |
| Pilot run 2 | ab-20261016-182828-c81fc0 | harness | r-20261016-182828-7d66af | ABORTED: timeout | none | 69 | 0 | 0 |
| Pilot run 2 | ab-20261016-185422-8a8c2a | bare | r-20261016-185422-ce2096 | completed | none | 66 | 4 | 33 |
| Pilot run 2 | ab-20261016-185422-8a8c2a | harness | r-20261016-185422-618828 | completed | none | 61 | 0 | 0 |
| Pilot run 2 | ab-20261016-191626-6100f6 | bare | r-20261016-191626-e55f2f | completed | none | 69 | 3 | 8 |
| Pilot run 2 | ab-20261016-191626-6100f6 | harness | r-20261016-191626-7aebe4 | ABORTED: timeout | none | 69 | 2 | 3 |
| Pilot run 3 | ab-20261016-212252-aa1644 | bare | r-20261016-212252-eb2cb4 | ABORTED: timeout | none | 66 | 4 | 23 |
| Pilot run 3 | ab-20261016-212252-aa1644 | harness | r-20261016-212252-1623c9 | completed | none | 27 | 0 | 0 |
| Pilot run 3 | ab-20261016-214151-ca9841 | bare | r-20261016-214151-23531c | ABORTED: timeout | none | 66 | 0 | 0 |
| Pilot run 3 | ab-20261016-214151-ca9841 | harness | r-20261016-214151-c0e492 | ABORTED: timeout | none | 69 | 0 | 0 |
| Pilot run 3 | ab-20261016-220010-c5b4bf | bare | r-20261016-220010-087344 | ABORTED: timeout | done | 69 | 3 | 5 |
| Pilot run 3 | ab-20261016-220010-c5b4bf | harness | r-20261016-220010-aabcbb | ABORTED: timeout | none | 69 | 0 | 0 |
| Class-profile round | ab-20261017-090903-926c02 | bare | r-20261017-090903-ffa6fd | completed | done | 68 | 4 | 16 |
| Class-profile round | ab-20261017-090903-926c02 | harness | r-20261017-090903-3dc7bc | ABORTED: timeout | not_done | 68 | 1 | 4 |

No arm passed all 69 hidden tests and killed all 4 referee mutants in the same run, so both arms
failed the primary measure in every A/B: no measurable difference on this task with this model.
Pilot run 4 (effort low) ran F1-F3 only.

What else the records show:

- **The gate never ran on F4.** No harness arm called `finish(claim="done")`: the claim was `none`
  in runs 2 and 3 (every build used its 40 turns) and `not_done` in the class-profile round.
- **Two bare done claims, both failed by the referee.** In ab-20261016-220010-c5b4bf the build
  passed 69 of 69 hidden tests and one referee mutant survived its shipped tests; in
  ab-20261017-090903-926c02 one hidden test failed.
- **The harness test phase.** In run 2 it kept no test (in ab-20261016-191626-6100f6 the 3 shipped
  tests came from build session 1, and the one test-phase test failed filter 2). In run 3 it
  proposed none: in ab-20261016-214151-ca9841 and ab-20261016-220010-c5b4bf the agent time limit
  ended the test session after 7 and 6 turns, spent on the getting-up-to-speed steps. In the
  class-profile round it proposed 6 and kept 4.
- **A broken change.** In ab-20261016-212252-aa1644 the harness arm passed 27 of 69 hidden tests
  and added 3 new R1 violations.
- **The reviewer** rejected all 14 arms in the table and agreed with the referee each time
  (`reviewer_agrees`).

The course's planned 10-run experiment batch and the leave-one-out ablation (`--layers=-verify`)
were not run: the pilot did not pass its pre-registered decision rule, so the A/Bs above are all the
F4 data the course has.

## 13. Time and cost

Limits (not measurements; `src/shipharness/config/settings.py`): agent time per arm `RUN_TIMEOUT_S`
300 s, harness work per arm `HARNESS_TIMEOUT_S` 120 s, tool command `TOOL_TIMEOUT_S` 120 s; $0.20
per arm (`MAX_RUN_COST_USD`), $0.25 per final arm (`MAX_FINAL_RUN_COST_USD`), $0.04 per review
(`MAX_REVIEW_COST_USD`), $2.50 per session (`MAX_SESSION_COST_USD`); F4 build session 40 turns
(`teamtrack/reference/f4/task.toml`). By those caps `make show-4` costs at most $0.24 and one
`make final` feature at most $0.58. Fast-tier calls cost twice the Standard rate per token; the caps
do not change.

Measured in the class-profile round, 2026-10-17 (ab-20261017-090903-926c02, from the launch):

| Arm | Agent s | Launch to primary verdict | Launch to full verdict | Arm cost $ | Review $ |
|---|---|---|---|---|---|
| bare | 152 | 243 s | 393 s | 0.0217 | 0.0038 |
| harness | 311 | 811 s | 927 s | 0.0257 | 0.0040 |

Measured in pilot run 2, 2026-10-16 (effort medium, two A/Bs in parallel), per arm from the score
records (captured on 2026-10-16, runs as listed; your output will differ):

| Run id | Arm | `wall_s` | `cost_usd` | `review_cost_usd` |
|---|---|---|---|---|
| r-20261016-182828-1daced | bare | 310.173 | 0.015296 | 0.004127 |
| r-20261016-182828-7d66af | harness | 422.691 | 0.016684 | 0.004066 |
| r-20261016-185422-ce2096 | bare | 225.33 | 0.016903 | 0.004038 |
| r-20261016-185422-618828 | harness | 369.779 | 0.016342 | 0.003399 |
| r-20261016-191626-e55f2f | bare | 281.933 | 0.019123 | 0.004327 |
| r-20261016-191626-7aebe4 | harness | 409.127 | 0.018463 | 0.004193 |

Every arm stayed below its cap. Time and cost of tonight's `make show-4` and `make final` run: read
them off the `Cost:` lines and the console's "launch to full verdict" when they finish.

## 14. Troubleshooting

| Symptom | Cause (from the code) | What to do |
|---|---|---|
| `x SHIPHARNESS_CLASS_DATE is not set: ...`, exit 2 | Class purpose without the class day (`_trace_target` in `src/shipharness/ab/commands.py`) | Set it in `.env`; `PURPOSE=pilot` traces to `shipharness-pilot` instead |
| `x OpenAI refused the key: ...; no arm was started` | Live runs refuse a missing or rejected key and any stand-in client; there is no automatic fallback | Fix the key (`make doctor`), or go to the fallback (section 15) |
| `make show-4` exits 2 | The harness arm was aborted (agent time limit or cost cap); it happened in the class-profile round (`ABORTED: timeout`) | Nothing to fix: the referee still judges the shipped diff and the record is complete |
| No gate pills by the end of the run | The agent never claimed done; the gate runs only on `finish(claim="done")` | Show the test-phase filter table and the referee counts; the constructed example shows the gate |
| Every gate pill ✗ with `could not write the check inputs in the container` or `check runner failed (exit <n>)` | The harness time limit (`HARNESS_TIMEOUT_S`) ran out; each gate command is capped by the harness time left | Keep the run (every run is scored); say what happened |
| `make swap-4` on the show-4 id stops with `... is a single-arm run (harness in action) ...` | The swap test needs both arms | Pass an A/B id, for example `AB=ab-20261017-090903-926c02` |
| `make replay` prints `x ...; check the A/B or run id`, exit 2 | The run folder is not in `.shipharness/runs/` on this host | Copy the folder (section 2, step 5) or replay another recorded A/B |
| `make replay` prints `x ...` about an unpinned record, exit 2 | The record has no `checkpoint_sha` (`UnpinnedRecord` in `src/shipharness/ab/recorded.py`) | Use an A/B recorded after SHA pinning; ab-20261017-090903-926c02 is pinned |
| No "Two-tab edit conflict" panel; boards say "No board screenshot yet" | The preview container failed to start and was skipped | Use screen 3 (board check) and the hidden board tests counted in `hidden <x>/69` |
| `mutants 0/0` in the record | The mutant set could not be loaded (`src/shipharness/ab/mutants.py`) | Run `uv run shipharness datasets validate datasets/teamtrack-features-v1.jsonl --kind features`; the run still counts |
| `reviewer=None` | The review was incomplete, refused, failed, or hit `MAX_REVIEW_COST_USD` | Primary counts are unaffected; say so |
| Verdict text `referee could not judge the build: ...` | The referee container failed to start (`src/shipharness/ab/referee.py`) | Check Docker (`make doctor`) |
| Red badge `UNSANDBOXED — results not official` | `SANDBOX_MODE` is not `docker` | Set `SANDBOX_MODE=docker` in `.env`, start Docker Engine in WSL2, `make doctor` |
| `make final` with no `FEATURES` runs F5, then F6 | The Makefile default is `FEATURES ?= F5,F6` | Always pass `FEATURES=` with the poll result; press Ctrl+C at once if the default started |

## 15. Fallback

Class commands call OpenAI live and never fall back on their own. If a live run fails on stage:

- **`make show-4` fails:** replay a recorded `make show-4` run (`make replay RUN=<id>`, id below; the
  RECORDING badge is shown on every screen), or go straight to the replay of
  ab-20261017-090903-926c02, which covers the filter table and the referee.

[[CAPTURE: ab id of the recorded make show-4 run to replay as the fallback, with its capture date | how: make show-4]]

- **`make final` fails:** replay a recorded final A/B (id below) and read it as one dot.

[[CAPTURE: ab id of the recorded make final FEATURES=F5 A/B to replay as the fallback, with its capture date | how: make final FEATURES=F5]]

- **The replay fails** (for example the run folder is missing): read the captured lines in section 7
  and the table in section 12.

A replay makes no model calls; it re-runs the referee in containers, so Docker must be up.
