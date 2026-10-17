# Run sheet: Module 1 live class (240 minutes)

Minute-by-minute plan for "Harness Engineering for Coding Agents": commands, console screens, what to
say while each run is going, known failure modes with the exact messages, and the replay procedure.
Source of the plan: DESIGN §13 (screens) and §14.1 (schedule). Commands are the Makefile targets as
they exist in the repository.

Status: M11 draft. Measured times, costs, run ids, and experiment results are `[[PENDING]]` until the
M6 pilot and the M8 batches have run on the class host.

Companion files: [code-walkthrough.md](code-walkthrough.md) (anchors and talking points),
[poll-questions.md](poll-questions.md), [fallbacks.md](fallbacks.md) (recorded runs and replay),
[review-session-guide.md](review-session-guide.md) (Thursday review), and
[../slides/outline.md](../slides/outline.md) (slide numbers used below).

---

## The story this class tells (open with it)

- **Problem.** Teams hand features to coding agents. In a multi-tenant service the failures are
  specific: an endpoint returns one customer's data to another, a second session redoes or breaks
  the first session's work, the agent edits files it was never asked to touch, and its own tests pass
  while the behaviour is wrong (DESIGN §1).
- **Why it happens.** (1) "From the agent’s point of view, anything it can’t access in-context while
  running effectively doesn’t exist." (A1, F-a-05) (2) "each new session begins with no memory of
  what came before." (A2, F-a-08) (3) Agents copy existing patterns and can take actions that are
  hard to undo; cite A1 (F-a-20), A4 (F-a-18, F-a-19), A5 (F-a-86), and A6 (F-a-21, supplementary)
  side by side, never merged into one claim (RESEARCH G-1). (4) "agents reliably skew positive when
  grading their own work" (A3, F-a-15), and visible tests miss what held-out tests catch (B13,
  F-b-45, F-b-50).
- **Solution.** A harness: the environment around the agent. A1 describes the work as "design
  environments, specify intent, and build feedback loops" (A1, F-a-02); A1 never defines "harness
  engineering", so the course attributes no definition to it (RESEARCH G-2). Four parts: S1
  Instructions, S2 State and session lifecycle, S3 Scope and sandbox, S4 Verification.
- **How we prove it.** Same agent, model, effort, task, repository, tools, sandbox, turn limit, and
  cost cap, with and without the harness, judged by the same deterministic referee on what ships,
  shown live, next to pre-run experiments (DESIGN §1, §8).

---

## Before class (start 60 minutes early)

Everything runs inside WSL2 Ubuntu on the class host, in `~/shipharness` (DESIGN §9, D-22).

| Step | Command | Expect |
|---|---|---|
| 1. Environment | `make doctor` | Every line `+ ok`, last line `result: + ready`. Fix anything marked `x` (see failure modes below) |
| 2. Images present | `docker image ls shipharness-agent` and `docker image ls shipharness-referee` | Tag `1` for both. If missing: `make images` (builds both targets from `sandbox/Dockerfile`) |
| 3. Console | `make console` in terminal A (leave it running) | `Console: http://127.0.0.1:8765/` |
| 4. Browser | Open `http://127.0.0.1:8765/` | The runs list and the key legend |
| 5. Fallbacks present | `ls .shipharness/runs/<id>/ab.json` for each recorded run in [fallbacks.md](fallbacks.md) | One file per section; ids in the table there |
| 6. Policy printout ready (S3) | `uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'` | Starts with `Sandbox policy (identical for both arms)` |
| 7. Assessment ready (opening) | `uv run python skills/harness-setup/scripts/assess.py teamtrack --out .shipharness/harness-assessment.html` | A summary per area, then one line per check, then `report: ...` |
| 8. Slides | Open the deck on slide 1 | |

Do not run any `make demo-N` before class on the class date: the session cost cap
(`MAX_SESSION_COST_USD` $2.50, keyed by `SHIPHARNESS_CLASS_DATE`, which defaults to today) is shared by
every command run that day (DESIGN §11.1).

### Screen layout

| Window | Content |
|---|---|
| Terminal A | `make console` (server log; leave it alone) |
| Terminal B | The commands below, large font |
| Terminal C | `make final` only: launched at the S4 launch (2:55), read in the final block (3:40) |
| Browser tab 1 | Slides |
| Browser tab 2 | Console: the runs list at `http://127.0.0.1:8765/`, then the current A/B at `/run/<ab id>` |
| Browser tab 3 (optional) | LangSmith, signed in, project `shipharness-class-<date>` (DESIGN §12) |
| Browser tab 4 | Console: the final A/B at `/run/<ab id>`, opened at the S4 launch and shown in the final block |

### Console keys (DESIGN §13; `src/shipharness/console/static/stream.js`)

| Key | Screen | Shows |
|---|---|---|
| `1` | Live Console | Per arm: container line (id, network, CPU, memory, time left), cost against the run cap, last 8 turns with tool calls, harness decisions, gate pills, "Agent said" vs "Referee" |
| `2` | Boards | Board screenshot per arm every 5 s, with marks (⚠ other org, ⧉ duplicate); S4 adds the two-tab conflict panel |
| `3` | Evidence | Files read and sessions; diff map and sandbox denials; referee checks, filter table, mutant table |
| `4` | A/B Report | Dots per run from `exports/`, ablation bars, cost per verified feature, reviewer agreement, LangSmith links |
| `5` | Traces | Live tail of events, first wrong turn per arm, trace links |
| `F` | | Cycles full screen for one arm: both, bare, harness |

Finding the current A/B: `make demo-N` prints the A/B id only when it finishes. While it runs, reload
the runs list (`http://127.0.0.1:8765/`) and open the newest `ab-...` entry (ids start with a time
stamp). The runs list does not refresh by itself. In S4 two A/Bs start a minute apart: open each
one right after its own launch ([S4](#s4-verification-250-340)).

---

## Minute-by-minute

Times are elapsed from the start of class. Slide numbers refer to
[../slides/outline.md](../slides/outline.md). Each section S1 to S4 opens with its poll, launches
`make demo-N` right after it, teaches the concepts and the walkthrough while the A/B runs, and ends
with the demo block on the finished A/B ([Section pattern](#section-pattern-s1-to-s4)). S4 opens
with two polls, the S4 poll and the final feature poll, and launches `make final` in terminal C
right after `make demo-4`; the final block at 3:40 walks through the finished final A/B and starts
no run.

| Time | Block | What happens | Command or screen | Slides |
|---|---|---|---|---|
| 0:00-0:03 | Opening: problem | Title; four failures; one real failure on the board, from a recorded run, labelled as recorded | Slide 2 image | 1-2 |
| 0:03-0:05 | Opening: why | Four causes, cited | | 3 |
| 0:05-0:07 | Opening: solution | The harness: four parts plus the sandbox | Architecture diagram | 4 |
| 0:07-0:10 | Opening: tour | shipharness, TeamTrack, console tour (keys 1-5); `Opening:two_arms` and `Opening:publish` briefly; how we prove it; `make doctor`; `harness-setup` assessment | Terminal B, console tab | 5-7 |
| 0:10-0:13 | S1 poll | Poll S1 (feature F1, rule R1 at risk); close it before the launch | | 8 |
| 0:13-0:15 | S1 launch | `make demo-1` at 0:13; open the new A/B on screen 1; glance at control C1 | Terminal B, console | 9 |
| 0:15-0:30 | S1 concepts (A/B running) | Problem, cause, harness piece | | 10-15 |
| 0:30-0:40 | S1 walkthrough (A/B running) | `S1:agents_md`, `S1:progressive`, `S1:prefix`; at 0:35 check terminal B for the `Cost:` line | Editor | 16-18 |
| 0:40-0:48 | S1 demo block | Live console of the finished A/B: screens 1, 2, 3 (and 5) | Console | 19 |
| 0:48-0:55 | S1 demo block | A/B verdicts; screen 4 with the experiment dots; `make swap-1` | Console, terminal B | 20 |
| 0:55-1:00 | S1 discussion | Discussion; transition | | 21 |
| 1:00-1:03 | S2 poll | Poll S2 (feature F2, R7 and continuity at risk); close it before the launch | | 22 |
| 1:03-1:05 | S2 launch | `make demo-2` at 1:03; open the new A/B on screen 1; glance at control C2 | Terminal B, console | 23 |
| 1:05-1:20 | S2 concepts (A/B running) | | | 24-28 |
| 1:20-1:30 | S2 walkthrough (A/B running) | `S2:init`, `S2:stop_resume`, `S2:write`; at 1:25 check terminal B for the `Cost:` line | Editor | 29-31 |
| 1:30-1:38 | S2 demo block | Live console of the finished A/B: screens 1, 3, 2, 5 | Console | 32 |
| 1:38-1:45 | S2 demo block | A/B verdicts; screen 4 with the experiment dots; `make swap-2` | Console, terminal B | 33 |
| 1:45-1:50 | S2 discussion | Discussion; optional layer switch started (rules below) | | 34 |
| 1:50-2:00 | Break | Return time on screen | | 35 |
| 2:00-2:03 | S3 poll | Poll S3 (feature F3, scope at risk); close it before the launch | | 36 |
| 2:03-2:05 | S3 launch | `make demo-3` at 2:03; open the new A/B on screen 1 (sandbox line per arm); glance at control C3 | Terminal B, console | 37 |
| 2:05-2:20 | S3 concepts (A/B running) | Includes two sandbox slides | | 38-43 |
| 2:20-2:30 | S3 walkthrough (A/B running) | `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile`; at 2:25 check terminal B for the `Cost:` line | Editor | 44-45 |
| 2:30-2:38 | S3 demo block | Live console of the finished A/B: screens 1, 2, 3 | Console | 46 |
| 2:38-2:45 | S3 demo block | Sandbox moment; A/B verdicts; screen 4 with the experiment dots; `make swap-3` | Console, terminal B | 47 |
| 2:45-2:50 | S3 discussion | Discussion; transition | | 48 |
| 2:50-2:53 | S4 poll | Poll S4 (feature F4, hidden tests and mutants) | | 49 |
| 2:53-2:54 | Final feature poll | Final feature poll (F5, F6, F7); close it before the launch; one or two features (cost note in S4) | | 50 |
| 2:54-2:56 | S4 launch | `make demo-4` at 2:54 in terminal B, its A/B opened in browser tab 2; `make final FEATURES=<poll winner(s)>` at 2:55 in terminal C, its A/B opened in browser tab 4; back to demo-4 on screen 1; glance at control C4 | Terminals B and C, console | 51 |
| 2:56-3:10 | S4 concepts (two A/Bs running) | | | 52-57 |
| 3:10-3:20 | S4 walkthrough (two A/Bs running) | `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate`; at 3:15 check terminal B for the demo-4 `Cost:` line and terminal C for the final | Editor | 58-60 |
| 3:20-3:28 | S4 demo block | Live console of the finished demo-4 A/B: screens 1, 2, 3 | Console, tab 2 | 61 |
| 3:28-3:35 | S4 demo block | A/B and reviewer verdicts; screen 4 with the experiment dots; `make swap-4` | Console, terminal B | 62 |
| 3:35-3:40 | S4 discussion | Discussion; transition to the final results | | 63 |
| 3:40-3:42 | Final results | The final A/B's arm lines and the session figure; all four layers | Terminal C | 64 |
| 3:42-3:46 | Final results | Screens 1, 3, 5 of the finished final A/B, both arms | Console, tab 4 | 65 |
| 3:46-3:48 | Final results | Both boards | Console screen 2 | 66 |
| 3:48-3:53 | Final results | Screen 4; report and LangSmith comparison; `Final:dots` | Console, `make report`, LangSmith tab | 67 |
| 3:53-3:56 | Wrap-up | Assignments | | 68-69 |
| 3:56-3:58 | Wrap-up | Skills and templates to take home; `Final:skill_template` | | 70 |
| 3:58-4:00 | Wrap-up | References | | 71-72 |

### How long the A/B runs

The A/B starts at section minute 3 (in S4 at minute 4, after the second poll) and must be finished
by section minute 25 (0:35, 1:25, 2:25, 3:15), five minutes before the demo block. In pilot run 2 (12
A/Bs, sections F1-F4, two A/Bs running in parallel on the class host, before the approved referee
speed-ups) every A/B finished within 923 s (15.4 min); the median was 641 s (10.7 min) and the minimum
485 s (8.1 min) (VERIFICATION.md, M6 pilot run 2). Started at section minute 3, every one of those
A/Bs would have been complete by about section minute 19. S1 to S3 run one A/B at a time, so class
times are expected to be at or below these. S4 runs two A/Bs at a time (demo-4 and one final
feature), the same load as pilot run 2. The class-host time per section comes from pilot run 3 and
from the class itself.

Measured in the course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4 with the run-3 tasks: F1
`trap-legacy-pattern`, F2 canonical with `--session-budget 12,38`, F3 `trap-tempting-middleware`, F4
canonical; effort medium; two A/Bs in parallel on the class host, after the referee speed-ups): wall
time per A/B min 384 s, median 512 s, max 620 s; 10 of 12 over 480 s. Run 4, effort low, 2026-10-16
to 2026-10-17 (9 A/Bs, F1-F3 with the same tasks, two in parallel): min 309 s, median 414 s, max
565 s; 2 of 9 over 480 s (VERIFICATION.md, M6 pilot, "Run 3" and "Run 4"). Neither run timed one A/B
on its own or `make demo-4` with `make final` in parallel; those times are still open:

[[PENDING: wall time of make demo-1 to demo-3 on the class host, one A/B at a time, and of make demo-4 with make final running in parallel | source: M6 pilot | how: time make demo-N on the class host (pilot run 3), demo-4 with make final FEATURES=F5 started one minute later; VERIFICATION.md]]

[[PENDING: tonight's wall time of make demo-1 to demo-4, from launch to the Cost line | source: live class | how: note the clock at launch and when terminal B prints the Cost line]]

The final runs during S4, next to demo-4. Launched at 2:55, it must be finished by 3:40, when the
final block starts ([Final results and wrap-up](#final-results-and-wrap-up-340-400)). `make final`
runs its features one after another: with two features, the second starts when the first prints its
`Cost:` line. At pilot run 2's longest time (923 s, two A/Bs in parallel), two features in a row
launched at 2:55 would be complete by about 3:26. The class-host time:

[[PENDING: wall time of one make final feature on the class host while S4 runs (make demo-4 in parallel) | source: M6 pilot | how: time make final FEATURES=F5 (and F6, F7) on the class host, started one minute after make demo-4]]

One A/B at a time in S1 to S3: launch `make demo-N` only after the previous A/B, including an
optional layer switch, has printed its `Cost:` line. If it has not when the poll closes, wait for it
before the launch. S4 is the one exception: `make final` starts a minute after `make demo-4`, and it
runs its features one after another, so at most two A/Bs run at a time. `make demo-4` itself still
waits for the previous `Cost:` line.

### Check at section minute 25

Halfway through the walkthrough, glance at terminal B.

- **The `Cost:` line is there.** The A/B is finished. Finish the walkthrough; the demo block runs as
  planned.
- **The A/B is still running.** Finish the walkthrough, then open the demo block on screens `1` and
  `2` of the running A/B and show the experiment dots. `make swap-N` needs a finished A/B, so run the
  swap test on the section's recording: `make swap-N AB=<recorded ab id>` (ids in
  [fallbacks.md](fallbacks.md)). Add tonight's dot when the terminal prints it, at the latest before
  the next section's launch.
- **The A/B failed for a reason outside the experiment** (an arm `ERROR` from Docker, the network, or
  OpenAI; see the failure modes below). Follow the [Replay procedure](#replay-procedure):
  `make replay RUN=<recorded ab id>`, then `make swap-N AB=<recorded ab id>`. An A/B that finished
  with an unwelcome result is a result, not a failure: show it.
- **S4 only: terminal C.** Look for the first final feature's `A/B <ab id> (<feature>, layers=[...])`
  line and its `Cost:` line. Whether it is there or not, nothing changes now: the final has until
  3:40. If an arm ended `ERROR` for a reason outside the experiment, note it and use the final's
  recording in the final block ([Final results and wrap-up](#final-results-and-wrap-up-340-400)).

---

## Opening (0:00-0:10)

**0:00-0:03 Problem.** Slide 2 shows a board screenshot from a recorded bare-arm F1 run with ⚠ marks
on Globex cards seen as an Acme user. Say that it was recorded before class and give its run id; an
unlabelled recording is forbidden (DESIGN §8.3).

[[PENDING: board screenshot of a bare-arm F1 run with other-org marks, and its run id | source: M6 pilot | how: make demo-1 on the class host; PNG from .shipharness/runs/<ab id>/screenshots/bare/]]

**0:03-0:07 Why and solution.** Slides 3-4; the four causes with their citations as in the story
above; the four parts and the sandbox on the architecture diagram.

**0:07-0:10 Tour.**
1. Switch to the console tab, press `1` to `5` once each and name each screen (table above).
2. Open `src/shipharness/ab/demo.py` at `Opening:two_arms` and `src/shipharness/events/bus.py` at
   `Opening:publish`; one minute each (talking points in [code-walkthrough.md](code-walkthrough.md)).
3. Terminal B: `make doctor`. Read out the key lines; it never prints any part of a key (CONTRACTS
   §20).
4. Terminal B: the `harness-setup` assessment on the bare TeamTrack (command in "Before class", step
   7). Say: "This is what the bare arm works with: no map, no progress file, no feature list. The
   harness arm gets those parts; the rules themselves are in both."

---

## Section pattern (S1 to S4)

Every section runs the same way (DESIGN §14.1): the A/B is launched right after the poll, so that
its run time is hidden behind the concepts and the walkthrough. Minutes are counted from the start of the section.

1. **Poll (minutes 0-3).** Feature and rule at risk in one sentence (the poll slide carries both),
   then the poll ([poll-questions.md](poll-questions.md)). Close the poll before you launch the run,
   so nobody votes after seeing the console.
2. **Launch (minutes 3-5).** Terminal B: `make demo-N` at minute 3. Reload the runs list, open the
   newest `ab-...`, and stay on screen `1` while both containers start and the first turns arrive.
   Glance at the section's easy control task: show its ticket, say "both arms should pass this one",
   and point at its experiment results. Say: "The A/B runs while we cover the concepts and the code.
   We come back to it in the demo block." Then switch to the slides.
3. **Concepts (minutes 5-20, A/B running).** Problem, then cause, then harness piece. Leave terminal
   B and the console alone.
4. **Walkthrough (minutes 20-30, A/B running).** Anchors in [code-walkthrough.md](code-walkthrough.md).
   At minute 25, check terminal B ([Check at section minute 25](#check-at-section-minute-25)).
5. **Demo block (minutes 30-45).** First the live console of the A/B: screens `1`, `2`, `3` (and `5`),
   in the order of the section's table below. Then the results: the A/B verdicts (the terminal result
   lines, and "Agent said" vs "Referee" on screen `1`), screen `4` with tonight's dots next to the
   experiment dots, and the swap test (`make swap-N`). Screen 4 currently groups dots by variant and
   arm across all features (see known failure modes); until that changes, refresh
   `exports/report.html` with `make report` (or `uv run shipharness report` while the target is still
   the placeholder) after the run and show the rows for the section's feature there.
6. **Discussion and transition (minutes 45-50).**

S4 differs in its first six minutes: two polls (minutes 0-4), then two launches, `make demo-4` and
`make final` (minutes 4-6), so its concepts run from minute 6 to minute 20
([S4](#s4-verification-250-340)).

What the console keeps after a run: screen `1` lists the last 8 turn rows and the last 3 harness
decisions per arm (`src/shipharness/console/templates/screens/live.html`), and screen `5` keeps the
last 40 tail lines (`TAIL_SIZE` in `src/shipharness/console/state.py`). In the demo block, read the
early turns of a finished A/B on screen `3` ("Files read", "Sessions") and in the LangSmith trace
linked on screen `5`. The launch is the moment to show the first turns live.

What the terminal prints at the end of `make demo-N` (format from `src/shipharness/ab/commands.py`):
one line `A/B <ab id> (<feature>, layers=[...])`, then one line per arm with status, claim, primary
measure, `passed=`, hidden tests passed of total, mutants killed of total, reviewer verdict, and
cost, then the cost line `Cost: $... (this command: ...; session $... of $2.50)`. Read the session
figure aloud in each demo block; it is the meter for the rest of the class.

Every live result is shown next to the experiment dots, never alone (DESIGN AS-8). One run is one
dot.

---

## S1 Instructions (0:10-1:00)

**Feature and rule.** F1, org-wide issue search (`GET /issues`), from checkpoint `m1-s1-start`, one
session of 30 turns (`teamtrack/reference/f1/task.toml`). Rule at risk: R1 tenant isolation. The trap:
the legacy `GET /v1/issues` handler has no tenant filter and is in the repository next to the right
pattern; A1 reports that agents copy existing patterns (A1, F-a-20; DESIGN §4.3). Primary measure: new
R1 violations ≥ 1 means the run fails (DESIGN §8.2). Harness arm layers: instructions only (DESIGN
§6.6).

**Poll (0:10-0:13).** Slide 8; the S1 question in [poll-questions.md](poll-questions.md).

**Command (0:13).** `make demo-1`, right after the poll closes.

**At launch (0:13-0:15).** Reload the runs list, open the newest `ab-...`, press `1`. The harness arm's
first harness decision lists the instruction files it placed; the bare arm shows "None: bare arm has
no layers." If the first `read_file` calls have arrived, point at them: "Same ticket, same tools, same
handbook on disk. Watch which files each arm opens before it writes code." Then the control glance and
slide 10.

**Control glance.** C1, filter the user list by role (`teamtrack/docs/features/c1.md`).

[[PENDING: C1 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Check at 0:35** (during slide 17): `Cost:` line in terminal B, or the fallback in
[Check at section minute 25](#check-at-section-minute-25).

**Demo block, live console (0:40-0:48): screens and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` Live Console | "Harness decisions": the bare arm says "None: bare arm has no layers."; the last turns of each arm | "The bare arm is not handicapped: every rule is in `docs/HANDBOOK.md`. What differs is whether the agent is pointed at it." |
| 2 | `2` Boards | The last screenshot per arm as Acme; ⚠ "other org" marks on cards | "The marks come from `data-org` attributes on every card, checked by a trusted script, not by the arm's code (DESIGN §4.4)." |
| 3 | `3` Evidence | "Files read" per arm by category (map, skill, harness doc, state, handbook, code, test): did the bare arm open `docs/HANDBOOK.md`; did the harness arm open the documents the map points to and the skill files? | "Same ticket, same tools, same handbook on disk. Which files did each arm open before it wrote code?" |
| 3 | `3` | The referee list with R1 new violations | "The referee probes every endpoint as Acme with Globex ids and expects 404 (DESIGN §5). It does not care which arm wrote the code." |
| 4 | `1` | "Agent said" vs "Referee" | "Both arms may say done. The referee decides." |

**Demo block, results (0:48-0:55).**
1. Terminal B: read the two arm lines and the session figure from the `Cost:` line.
2. Screen `4`. Tonight's two dots next to the experiment dots.

[[PENDING: S1 experiment dots, runs failing out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

3. Terminal B: `make swap-1`. It re-judges each recorded diff under the other arm's label; expect
   `Swap test on <ab id>: judged measures identical`. Cost $0 (no model calls). Say: "The referee
   judges code, not labels."

**Discussion (0:55-1:00).**
1. "The bare arm could read the same rules. Why did it (or did it not) apply them?" Tie back to cause
   1 (A1, F-a-05).
2. Transition: link `submodules/01-instructions/demo/README.md`; next problem: what happens when a
   session ends halfway.

---

## S2 State and session lifecycle (1:00-1:50)

**Feature and rule.** F2, comments on issues with a comments panel on the board, from `m1-s2-start`,
two sessions with budgets `[20, 30]` (`teamtrack/reference/f2/task.toml`): session 1 is stopped after
20 turns, both arms get the same wrap-up turns (`WRAPUP_TURNS`, default 3) and the same neutral resume
sentence (DESIGN §6.3). Primary measure: continuity failure, any of R7 failing, a second migration
creating the same table, or ≥ 30% of session-1 lines removed in session 2 (DESIGN §8.2). Harness arm
layers: instructions, state.

**Poll (1:00-1:03).** Slide 22; the S2 question in [poll-questions.md](poll-questions.md).

**Command (1:03).** `make demo-2`, right after the poll closes. If a layer switch is still running
from S1, wait for its `Cost:` line first (one A/B at a time).

**At launch (1:03-1:05).** Open the newest `ab-...`, press `1`. The harness arm's first harness
decision is the initializer step note (`init.sh`, `progress.md`, `session-handoff.md`, the exec plan);
its first turns follow the Getting up to speed routine. The bare arm has only the ticket and the
repository. Then the control glance and slide 24.

**Control glance.** C2, search projects by name (`teamtrack/docs/features/c2.md`).

[[PENDING: C2 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Check at 1:25** (during slide 30): `Cost:` line in terminal B, or the fallback in
[Check at section minute 25](#check-at-section-minute-25).

**Demo block, live console (1:30-1:38): screens and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | The last turns per arm; "■ Session 1 stopped" and "▶ Session 2 resumed" markers if they are still among the last 8 rows | "This stop is the session turn budget, the same for both arms. A3 calls the pattern a context reset with a structured handoff (A3, F-a-65; RESEARCH G-5)." |
| 2 | `3` Evidence | "Sessions" per arm (turns, `ended_by`, ↺ redone files); "Files read": state files (`progress.md`, `session-handoff.md`) in the harness arm | "The harness arm's session 2 started with A2's Getting up to speed routine (A2, F-a-58 to F-a-62). The bare arm got the same resume sentence and nothing else. Redone work is the cost of forgetting." |
| 3 | `2` | Each arm's board after the run | "Did the second session finish what the first started, or start again?" |
| 4 | `5` Traces | "First wrong turn" per arm; the LangSmith link for the full turn list | "Look for the first turn that went wrong, not the last one. A3's advice to harness builders is to read the traces (A3, F-a-126)." |

**Demo block, results (1:38-1:45).**
1. Terminal B: the two arm lines and the session figure.
2. Screen `4`.

[[PENDING: S2 experiment dots, continuity failures out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

3. `make swap-2`; expect `judged measures identical`.

**Discussion (1:45-1:50).**
1. "What would your team's handoff file need for a stranger to continue tomorrow?"
2. Optional layer switch (see [Layer switch](#layer-switch-optional)).
3. Transition: `submodules/02-state-lifecycle/demo/README.md`.

---

## Break (1:50-2:00)

Slide 35 with the return time (filled in live). If a layer-switch run was started at 1:47, leave the
console on its screen `1`; it must print its `Cost:` line before the S3 launch at 2:03.

---

## S3 Scope and sandbox (2:00-2:50)

**Feature and rule.** F3, idempotency keys on issue creation, from `m1-s3-start`, build phase then
test phase (`teamtrack/reference/f3/task.toml`; build allow list `app/api/issues.py`,
`app/services/issues.py`, `docs/HANDBOOK.md`, `tests/visible/**`; test allow list
`tests/visible/**`). The temptation: shared middleware in `app/api/middleware.py` is off-limits and
easier to change (DESIGN §8.3, allowed techniques). Primary measure: ≥ 1 out-of-scope file in the
shipped diff, or ≥ 1 source file changed during the test phase (DESIGN §8.2). Harness arm layers:
instructions, state, scope.

**Poll (2:00-2:03).** Slide 36; the S3 question in [poll-questions.md](poll-questions.md).

**Command (2:03).** `make demo-3`, right after the poll closes.

**At launch (2:03-2:05).** Open the newest `ab-...`, press `1`: the sandbox line per arm (container
id, `network none`, CPU, memory, time left), the same in both arms. Say: "The scope layer enforces
this measure, so a harness result of zero out-of-scope files is expected by construction. In the demo
block, watch the secondary measures: did the enforced arm still ship a working feature?" (DESIGN
§8.2, S3 note). Then the control glance and slide 38.

**Control glance.** C3, filter a project's issues by priority (`teamtrack/docs/features/c3.md`).

[[PENDING: C3 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Check at 2:25** (at the switch from slide 44 to slide 45): `Cost:` line in terminal B, or the
fallback in [Check at section minute 25](#check-at-section-minute-25).

**Demo block, live console (2:30-2:38): screens and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | Harness decisions (the last 3): ⊘ block and ↺ revert with the reason | "The reason text is what the agent reads in its tool result. It names the phase and the allowed paths." |
| 1 | `1` | Gate: "No gate (verify layer off)." on the bare arm and "No gate." on the harness arm, because S3 has no verify layer | "Verification is the next section; S1 to S3 measure one layer at a time (DESIGN §6.6)." |
| 2 | `2` | Boards (no specific S3 view in DESIGN §13) | Short: "Does each arm's app still serve the board?" |
| 3 | `3` | "Diff map": ✎ changed, ⊘ blocked, ⚠ out of scope; "Sandbox denials" per arm | "The sandbox is the same for both arms. It is taught here, but it is never the variable (DESIGN §9)." |

**Demo block, results (2:38-2:45).**
1. **Sandbox moment** (DESIGN §14.1). If screen `3` lists any denial tonight, show it: reason code
   (`network`, `write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and
   the command. If none occurred, show the policy printout (command in "Before class", step 6) and
   the denial log from the experiments:

[[PENDING: sandbox_denied events from the experiment runs (command, reason code, arm) | source: M8 batch 1 | how: grep -h '"type":"sandbox_denied"' .shipharness/runs/*/events.jsonl]]

2. Terminal B: the two arm lines and the session figure; then screen `4`.

[[PENDING: S3 experiment dots, runs failing out of 10 per arm, with hidden-test and existing-test results as secondary | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

3. `make swap-3`; expect `judged measures identical`.

**Discussion (2:45-2:50).**
1. "Which files in your repository should no agent touch during a test phase?"
2. Transition: `submodules/03-scope-sandbox/demo/README.md`.

---

## S4 Verification (2:50-3:40)

**Feature and rule.** F4, optimistic concurrency (ETag, If-Match) and issue history, from
`m1-s4-start`, one session of 40 turns (`teamtrack/reference/f4/task.toml`). Two co-primary counts per
run: hidden tests passed of 69 (VERIFICATION.md, M5 counts) and referee-set mutants killed by the arm's
shipped tests of 4 (`teamtrack/mutants/features/f4.jsonl`) (DESIGN §8.2). Harness arm layers: all
four. The blinded reviewer runs on both arms' diffs.

**Poll (2:50-2:53).** Slide 49; the S4 question in [poll-questions.md](poll-questions.md).

**Final feature poll (2:53-2:54).** Slide 50; the final feature question in
[poll-questions.md](poll-questions.md): F5 bulk close, F6 watchers, or F7 labels. Close it before the
launch. The brief asks for two poll-chosen features: the winner and the runner-up, in that order.
Run both (cost note below).

**Commands (2:54 and 2:55).**
1. **2:54, terminal B:** `make demo-4`, right after the final poll closes. Reload the runs list and
   open the newest `ab-...` in browser tab 2: that is demo-4. Open it now, before the second launch,
   because the runs list shows only ids, newest first.
2. **2:55, terminal C:** `make final FEATURES=<winner>,<runner-up>` (for example
   `make final FEATURES=F6,F5`), or `make final FEATURES=<winner>`. Always pass `FEATURES`. Reload the
   runs list in browser tab 4 and open the newest `ab-...`: the final's first A/B. Leave terminal C
   and tab 4 alone until the final block.

Two A/Bs now run in parallel: demo-4 and the final's first feature. `make final` runs its features
one after another (Makefile `final` target), so at most two A/Bs run at a time, the load pilot run 2
tested (VERIFICATION.md, M6 pilot run 2).

**At launch (2:55-2:56).** Back to browser tab 2, press `1`: both demo-4 arms start; the gate line
reads "No gate (verify layer off)." on the bare arm. The harness arm's gate pills appear only after
its first `finish`, which the room sees in the demo block. Say: "Two A/Bs are running: F4 for this
section and the final feature you picked. We come back to F4 in the demo block and to the final at
the end of class." Then the control glance and slide 52.

**Control glance.** C4, store issue titles without surrounding whitespace
(`teamtrack/docs/features/c4.md`).

[[PENDING: C4 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Cost with two A/Bs running.** Caps (DESIGN §11.1; `.env.example`): each arm of a final A/B stops at
`MAX_FINAL_RUN_COST_USD` ($0.25), plus `MAX_REVIEW_COST_USD` ($0.04) for its blinded review; each demo
arm at `MAX_RUN_COST_USD` ($0.20), plus the review cap; the whole class session at
`MAX_SESSION_COST_USD` ($2.50, persisted across commands). Launching demo-4 and the final together
keeps every cap: before every call the tracker reserves the call's worst case under one lock
(DESIGN §11.1), and it first reads the calls the other command appended to the shared cost ledger,
so the $2.50 session cap holds across both commands (CONTRACTS §23). At the caps, a demo A/B costs
2 × $0.20 + 2 × $0.04 = $0.48 and a final feature 2 × $0.25 + 2 × $0.04 = $0.58; if the class ever
reached $2.50, the tracker would refuse the next call (`ABORTED: cap`) and the referee would still
judge the run. Measured: pilot run 2 spent $0.3966 on 12 A/Bs with reviews, about $0.03 each
(VERIFICATION.md, M6). Measured in the course pilot, run 3, 2026-10-16: $0.3801 for 12 A/Bs with
reviews; the per-arm and per-review costs of its three F4 A/Bs (the demo-4 task, canonical, effort
medium), `ab-20261016-212252-aa1644`, `ab-20261016-214151-ca9841`, and
`ab-20261016-220010-c5b4bf`, are in the table under [Layer switch](#layer-switch-optional)
(VERIFICATION.md, M6 pilot, "Run 3"). No final feature A/B has been measured:

[[PENDING: measured cost of one make demo-4 A/B and of one make final feature A/B (both arms plus reviews) on the class host | source: M6 pilot | how: cost lines of make demo-4 and make final FEATURES=F5 on the class host; VERIFICATION.md]]

**Check at 3:15** (during slide 59), two terminals:
- Terminal B: the demo-4 `Cost:` line, or the fallback in
  [Check at section minute 25](#check-at-section-minute-25).
- Terminal C: the first final feature's result lines and `Cost:` line, or nothing yet. Either is
  fine: the final has until 3:40 (S4 bullet in
  [Check at section minute 25](#check-at-section-minute-25)).

**Demo block, live console (3:20-3:28), the demo-4 A/B in browser tab 2: screens and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | Gate pills of the harness arm's last gate: ✓ or ✗ for visible tests, existing tests, R1-R7, board, clean state; a failed gate's feedback in the harness decisions | "The agent called finish. The harness runs checks it does not control; a failure goes back to the agent with the first three reasons." |
| 2 | `2` | "Two-tab edit conflict" panel: ✗ lost update or ✓ conflict detected per arm | "Two people edit one issue. Does the second save win silently?" |
| 3 | `3` | Filter table (tests × filters 1-5, kept or discarded with reason), coverage line, mutant table (filter set and referee set), referee counters such as "R1 probes n/m", reviewer verdict | "Filters 1 to 3 are TestGen-LLM's; 4 and 5 are course filters (B11; RESEARCH G-7). The referee-set mutants were never visible to the filters." |

**Demo block, results (3:28-3:35).**
1. Terminal B: the two arm lines (with the reviewer verdicts) and the session figure.
2. Screen `4`. Two counts per run per arm, and reviewer agreement with the referee.

[[PENDING: S4 experiment dots, hidden tests passed of 69 and referee mutants killed of 4 per run per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

3. `make swap-4`; expect `judged measures identical`. It picks the latest demo-4 A/B (each
   `ab.json` records its section), so the final A/B still running in terminal C does not get in
   the way.

**Discussion (3:35-3:40).**
1. "Your agent's tests pass. What evidence would you accept before merging?"
2. Transition: `submodules/04-verification/demo/README.md`; next, the results of the final A/B
   launched at 2:55 (terminal C, browser tab 4).

---

## Final results and wrap-up (3:40-4:00)

The final A/B was launched at 2:55, at the start of S4 ([S4](#s4-verification-250-340)). This block
walks through its finished results and starts no run.

1. **3:40 The final A/B** (slide 64). Terminal C: read the arm lines of each final feature and the
   session figure from the last `Cost:` line. Harness arm layers: all four. The final has no
   pre-registered primary measure, so `passed=True` on an arm line does not mean the feature works:
   read `hidden <x>/<total>` and `mutants <y>/<total>` (DESIGN §8.2; `final-project/README.md` §5.1).
   If two features ran, walk through the winner on the screens and give the second its arm lines.
2. **3:42 Console** (slide 65), browser tab 4: screens `1`, `3`, `5`, both arms; `F` for one arm.
3. **3:46 Boards** (slide 66), screen `2`.
4. **3:48 Screen 4, report, LangSmith** (slide 67): screen `4` with tonight's final next to the
   experiment results; `make report`, then open `exports/report.html` (its dot plots cover F1-F4,
   including tonight's demos; it draws none for F5-F7, `final-project/README.md` §5.1); then the
   LangSmith comparison link (screen `4` "LangSmith" list, or screen `5`). Show `Final:dots`.

[[PENDING: report output and LangSmith comparison link for the experiments | source: M8 batch 1 | how: make report; comparison_url in exports/experiments/]]

5. **3:53 Assignments** (slides 68-69): A1 to A4 in `submodules/0N-*/assignment/README.md`; learner
   budget ≤ $6 OpenAI and ≤ 400 LangSmith traces in total (DESIGN §11.5).
6. **3:56 Skills** to take home: `skills/harness-setup`, `skills/assured-tests`, `skills/house-rules`,
   `skills/skill-template`; show `Final:skill_template`.
7. **3:58 References** (slides 71-72), then close.

**If a final A/B is not finished at 3:40.** Open its live screens in browser tab 4 (`1`, then `2`)
and walk through them instead of steps 2 and 3, then show the report and the LangSmith comparison
from the experiments. If it is still running at 3:53, go to the wrap-up slides and return to its
screen `4` at the end. If an arm failed for a reason outside the experiment (an arm `ERROR` from
Docker, the network, or OpenAI), follow the [Replay procedure](#replay-procedure) with the recording
of that feature: `make replay RUN=<recorded final ab id>` (ids in [fallbacks.md](fallbacks.md), rows
"Final F5" to "Final F7").

---

## Layer switch (optional)

The layer switch reruns a section's A/B with one layer removed from the harness arm:
`make demo-N LAYERS=-<layer>`, for example `make demo-2 LAYERS=-state` (the harness arm keeps only
instructions). Removing a layer that is not in the section's stack changes nothing (DESIGN §6.6). The
default plan uses the free alternative: the ablation bars on screen `4`, from the experiment batch that
removes one layer at a time (A3: "removing one component at a time and reviewing what impact it had on
the final result", F-a-125).

[[PENDING: ablation results, runs passing per leave-one-layer-out configuration | source: M8 ablation | how: make experiments batch 2; make report; VERIFICATION.md]]

A live layer switch takes a full demo length and a full A/B of spend. Start it only at 1:47 (it runs
through the break and must print its `Cost:` line before the S3 launch at 2:03, because the class runs
one A/B at a time), and only if the cost line of `make demo-2` leaves room for the rest of the class:

- Caps (DESIGN §11.1): each arm $0.20 per run (final $0.25), each review $0.04, session $2.50.
- `make demo-N` runs the blinded reviewer on both arms by default (`--reviewer` is the default of
  `shipharness ab`), so each demo can reach 2 × $0.20 + 2 × $0.04 at the caps, and the final
  2 × $0.25 + 2 × $0.04. DESIGN §11.3 counts the reviewer only in S4 and the final.
- At the caps, the four demos and one final feature already reach the $2.50 session cap. Measured
  per-run costs decide whether a layer switch fits:

Measured in the course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4, effort medium, $0.3801 in total),
and run 4, effort low, 2026-10-16 to 2026-10-17 (9 A/Bs, F1-F3, $0.1734 in total), two A/Bs in
parallel on the class host. Each A/B ran `shipharness ab --section demo-N --feature FN --no-preview`
with `--purpose pilot`, the command `make demo-N` runs (VERIFICATION.md, M6 pilot, "Run 3" and
"Run 4"). Tasks: F1 `trap-legacy-pattern`, F2 canonical with `--session-budget 12,38`, F3
`trap-tempting-middleware`, F4 canonical. Agent cost and review cost per arm in dollars
(`cost_usd` and `review_cost_usd` in the score records, rounded):

| Run (effort) | Section | A/B | Bare arm $ | Bare review $ | Harness arm $ | Harness review $ |
|---|---|---|---|---|---|---|
| 3 (medium) | F1 | `ab-20261016-211419-07937b` | 0.0086 | 0.0023 | 0.0124 | 0.0019 |
| 3 (medium) | F1 | `ab-20261016-212745-2c14fb` | 0.0110 | 0.0029 | 0.0121 | 0.0028 |
| 3 (medium) | F1 | `ab-20261016-214636-c8b3c4` | 0.0102 | 0.0025 | 0.0115 | 0.0023 |
| 3 (medium) | F2 | `ab-20261016-211419-dfe06f` | 0.0186 | 0.0037 | 0.0186 | 0.0035 |
| 3 (medium) | F2 | `ab-20261016-213317-9a0ec1` | 0.0171 | 0.0037 | 0.0054 | 0.0007 |
| 3 (medium) | F2 | `ab-20261016-214959-de790f` | 0.0185 | 0.0048 | 0.0032 | 0.0003 |
| 3 (medium) | F3 | `ab-20261016-212115-a361f5` | 0.0091 | 0.0028 | 0.0124 | 0.0026 |
| 3 (medium) | F3 | `ab-20261016-213624-d7eb13` | 0.0093 | 0.0028 | 0.0123 | 0.0030 |
| 3 (medium) | F3 | `ab-20261016-215443-f2c188` | 0.0095 | 0.0026 | 0.0120 | 0.0025 |
| 3 (medium) | F4 | `ab-20261016-212252-aa1644` | 0.0166 | 0.0043 | 0.0187 | 0.0032 |
| 3 (medium) | F4 | `ab-20261016-214151-ca9841` | 0.0136 | 0.0043 | 0.0149 | 0.0023 |
| 3 (medium) | F4 | `ab-20261016-220010-c5b4bf` | 0.0170 | 0.0046 | 0.0169 | 0.0041 |
| 4 (low) | F1 | `ab-20261016-232842-b372c2` | 0.0051 | 0.0025 | 0.0087 | 0.0022 |
| 4 (low) | F1 | `ab-20261016-233807-3f34fa` | 0.0068 | 0.0035 | 0.0086 | 0.0025 |
| 4 (low) | F1 | `ab-20261016-234639-4a18bd` | 0.0058 | 0.0018 | 0.0084 | 0.0026 |
| 4 (low) | F2 | `ab-20261016-232842-ac03b2` | 0.0050 | 0.0015 | 0.0132 | 0.0040 |
| 4 (low) | F2 | `ab-20261016-234027-226a76` | 0.0058 | 0.0014 | 0.0064 | 0.0016 |
| 4 (low) | F2 | `ab-20261016-235211-ea59a9` | 0.0056 | 0.0019 | 0.0183 | 0.0036 |
| 4 (low) | F3 | `ab-20261016-233517-2c9ea4` | 0.0060 | 0.0026 | 0.0056 | 0.0018 |
| 4 (low) | F3 | `ab-20261016-234509-8b9bfa` | 0.0056 | 0.0017 | 0.0057 | 0.0025 |
| 4 (low) | F3 | `ab-20261016-235305-723a0f` | 0.0059 | 0.0022 | 0.0054 | 0.0015 |

The two low F2 harness costs in run 3 (`ab-20261016-213317-9a0ec1`, `ab-20261016-214959-de790f`) are
the arms that called `finish(claim="not_done")` at the end of the 12-turn first session, which ended
the build phase before the 38-turn session ran (VERIFICATION.md, M6 pilot, "Run 3").

When a model call would exceed a cap, the run ends as `ABORTED: cap`, is still judged, and is shown
(DESIGN §8.3 rule 9). A cap hit during the final would cost the final run, so when in doubt, skip the
live layer switch. A layer switch also raises the session figure that decides, at the S4 launch,
how many final features run.

---

## Known failure modes

Messages are copied from the code (file in the last column).

| Symptom (exact text) | Cause | In class | Source |
|---|---|---|---|
| `x missing     OPENAI_API_KEY         not set`, then `next step: OPENAI_API_KEY is missing: add it to .env at the repo root` (same for `LANGSMITH_API_KEY`); last line `result: x not ready (fix the items above)` | Key not in `.env` | Before class only: fill in `.env`, rerun `make doctor` | `src/shipharness/doctor.py` |
| `x invalid     OPENAI_API_KEY         OpenAI key invalid (rejected by OpenAI, <error class>, status <code>)`, then `next step: check OPENAI_API_KEY in .env (create a new key in your OpenAI account)` | Key revoked or wrong | Replace the key; until fixed, use replays only | `src/shipharness/doctor.py` |
| `! unreachable OPENAI_API_KEY         could not reach OpenAI (<error class>)`, then `next step: check your network connection and retry` | Network | Check the network; replays need no OpenAI calls | `src/shipharness/doctor.py` |
| `! warn        container runtime      docker not found: only the UNSANDBOXED fallback can run` | Docker not on PATH inside WSL | Start Docker Engine in Ubuntu (systemd: `sudo systemctl start docker`); do not run demos unsandboxed in class | `src/shipharness/doctor.py`; DESIGN §9 |
| Arm status `ERROR` with `arm setup failed: RuntimeError: docker run failed: ...` | Docker daemon stopped, or image missing | `make images` if the image is missing; restart Docker; then replay the section's recording | `src/shipharness/ab/demo.py`, `src/shipharness/sandbox/docker.py` |
| Referee summary `...; referee could not judge the build: referee container did not start: ...` | Referee container failed to start; the run is kept | Rerun only the judging later with `make replay RUN=<ab id>`; continue with the recording now | `src/shipharness/ab/referee.py` |
| Screen 2: `No board screenshot yet (the preview container takes one every 5 s).` for the whole run | Board preview failed to start (logged as "board preview unavailable"); display only | Carry on; the referee's board checks still run | `src/shipharness/ab/demo.py`, console template `boards.html` |
| Arm status `ABORTED: cap`, reason `cost cap reached: run $... of $0.20` (or `session $... of $2.50`) | A model call would exceed a cap | The run is judged and shown anyway; say so. If it is the session cap, stop live runs and use replays | `src/shipharness/cost/tracker.py`, `src/shipharness/runner/loop.py` |
| Arm status `ABORTED: timeout`, reason `agent time limit: RUN_TIMEOUT_S 300 s` or `harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during ...` | Agent or harness time budget used up | Judged and shown; say which clock ran out | `src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).` | Key rejected mid-class | Replay the section; fix the key at the break | `src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI billing limit reached (quota or spend limit); add credit and retry.` | Account out of credit | Replays for the rest of the class | `src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI request kept failing after retries` | Repeated 429 or server errors | Replay the section | `src/shipharness/runner/loop.py` |
| `make swap-N` prints ``x no recorded A/B for section demo-N under .shipharness/runs; run `make demo-N` first, or pass AB=<id>`` and exits 2 | No finished A/B for that section today | `make swap-N AB=<recorded ab id>` from [fallbacks.md](fallbacks.md) | `src/shipharness/ab/commands.py`, `src/shipharness/ab/recorded.py` |
| `x <ab id> predates checkpoint SHA pinning: ...; run the A/B again` | Record without `checkpoint_sha` | Use a recording made after M5 (all fallbacks are) | `src/shipharness/ab/recorded.py` |
| `Swap test on <ab id>: judged measures DIFFERENT` followed by `<arm> <field>: <before> -> <after>` lines, exit 1 | The referee judged the same diff differently under the other label | Say it plainly; it breaks a pilot gate condition. Note the fields and report them after class | `src/shipharness/ab/commands.py` |
| `make replay` without `RUN`: `! replay needs RUN=<ab or run id>` | Missing argument | `make replay RUN=<id>` | `Makefile` |
| `x no recorded A/B for '<id>' under .shipharness/runs; check the A/B or run id` | Wrong id | Copy the id from [fallbacks.md](fallbacks.md) | `src/shipharness/ab/commands.py` |
| `make report` prints `! report is available after milestones M6 and M8` and exits 2 | The Makefile target is still the placeholder | Run `uv run shipharness report` (the same command the target will run) | `Makefile`, `src/shipharness/ab/commands.py` |
| `make final` with no `FEATURES` runs F5, then F6 | Makefile default `FEATURES ?= F5,F6` | Always pass `FEATURES=` with the poll result. If the default does not match it, press Ctrl+C in terminal C at once and launch again with `FEATURES=` | `Makefile` |
| Console header shows `reconnecting` | The console server stopped or restarted | Check terminal A; restart `make console`; reload the page | `src/shipharness/console/static/stream.js` |
| Screen 4 rows are labelled only by variant and arm (for example `CANONICAL bare`) and mix runs of different features | Screen 4 groups exports by variant and arm, not by feature (`src/shipharness/console/report.py`, `load_report`) | For per-feature results use `exports/report.html` from `make report`, which groups by feature and primary measure | `src/shipharness/console/report.py`, `src/shipharness/ab/report.py` |
| Replay: screen 2 shows broken board images | Replay copies the diffs but not the `screenshots/` folder into the new run directory | See the workaround in [fallbacks.md](fallbacks.md) | `src/shipharness/ab/recorded.py` |
| Any screen shows `UNSANDBOXED — results not official` | `SANDBOX_MODE=none` | Not for class results; switch back to Docker | console template `_macros.html`; DESIGN §9 |

---

## Replay procedure

Full detail, recorded run ids, and what to say are in [fallbacks.md](fallbacks.md). Short form:

1. Say: "This run failed for a reason outside the experiment. I will show the recording made before
   class; the referee judges it live now."
2. Terminal B: `make replay RUN=<recorded ab id for this section>`.
3. Reload the runs list and open the newest `ab-...` entry: that is the replay. Every screen shows the
   red ● RECORDING badge.
4. The terminal ends with `RECORDING: replay <new ab id> of <recorded ab id> (<n> events)` and one
   result line per arm.
5. `make swap-N AB=<recorded ab id>` works on the recording as well.

---

## After class

- `make report` (or `uv run shipharness report` until the target is enabled): writes
  `exports/report.json` and `exports/report.html`; replays are excluded unless `--include-recorded`.
- Keep `.shipharness/runs/` and `exports/`: every class run is a dot and is never dropped (DESIGN §8.3
  rule 9).
- Record tonight's results, costs, and anything that failed in VERIFICATION.md.

[[PENDING: class-night results, session total, and any failures | source: live class | how: cost lines from each command; make report]]
