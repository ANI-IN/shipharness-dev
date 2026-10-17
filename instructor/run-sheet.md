# Run sheet: Module 1 live class (240 minutes)

Minute-by-minute plan for "Harness Engineering for Coding Agents": commands, console screens, what to
say while each run is going, and, in the two sections marked "Fallback" at the end, the known failure
modes with their exact messages and the replay procedure. Sources: DESIGN §13 (screens) and §14.1
(schedule); the per-section class plan in VERIFICATION.md, "Class plan per section", as revised on
2026-10-17 (owner message 7: every demo section is live); measured times and costs from the quiet
runs of the class commands on 2026-10-17 (one command at a time on a quiet machine, class profile,
`PURPOSE=pilot`) and from VERIFICATION.md, "Class-profile round". Commands are the Makefile targets as
they exist in the repository.

Status: final for the class plan. Every demo step launches or shows a live run;
`tests/unit/test_run_sheet_live.py` fails if a replay or a constructed example enters a demo step.

Companion files: [code-walkthrough.md](code-walkthrough.md) (anchors and talking points),
[poll-questions.md](poll-questions.md), [fallbacks.md](fallbacks.md) (fallback recordings, replay,
and the optional extras),
[review-session-guide.md](review-session-guide.md) (Thursday review), and
[../slides/outline.md](../slides/outline.md) (slide numbers used below). The stage-by-stage version
with pass criteria is [../docs/instructor-guide.md](../docs/instructor-guide.md).

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
- **The claim.** A harness encodes assumptions about the model; measure each piece, keep what earns
  its place. The first half is A3's: "every component in a harness encodes an assumption about what
  the model can't do on its own, and those assumptions are worth stress testing" (A3, F-a-124). The
  method is A3's too: "removing one component at a time and reviewing what impact it had on the final
  result." (A3, F-a-125). "Keep what earns its place" is course framing; say so.
- **How we measure it.** Same agent, model, effort, task, repository, tools, sandbox, turn limit, and
  cost cap, with and without the harness, judged by the same deterministic referee on what ships. One
  primary measure per section, registered before any run; a section without a gap is reported as "no
  measurable difference on this task with this model" (DESIGN §8, §10.4).
- **What the course pilot found.** The pre-registered gate did not pass: in runs 3 (effort medium)
  and 4 (effort low) every section showed no measurable difference on this task with this model, and
  the class-profile round (one A/B per section) agreed (VERIFICATION.md, "Gate decision",
  "Class-profile round"). Say it in the opening and show it in every section. The harness does not
  have to win; every result is reported as measured.

---

## The class plan per section

Every demo section is live (VERIFICATION.md, "Class plan per section", revised 2026-10-17 under
owner message 7). S1 to S4 run `make show-N`: the harness arm alone, live, with the live referee
checks and the live console, showing the layer doing its job. No section has a measured gap, so none
runs `make demo-N`. The final runs `make final`, the class's one live A/B and its measurement lesson.
Recorded showcases and constructed examples are optional extras, listed in `docs/extras.md` and in
[fallbacks.md](fallbacks.md); they are never part of a demo block. A replay of a recording is the
emergency fallback only ([Fallback: replay procedure](#fallback-replay-procedure)).

| Section | Harness in action (live) |
|---|---|
| S1 | `make show-1`: F1, instructions layer; watch the agent read the map, then only the documents the ticket needs |
| S2 | `make show-2 SESSION_BUDGET=12,38`: F2, instructions and state; session 1 stops at its 12-turn budget, the handoff is written, session 2 (38 turns) resumes from it |
| S3 | `make show-3`: F3, instructions, state, scope; scope guard and sandbox policy at work |
| S4 | `make show-4`: F4, all four layers; handoffs, test phase, filters |
| Final | One live A/B: `make final FEATURES=<poll winners>`; one A/B is one dot, read against the pilot's dots |

`make show-2 SESSION_BUDGET=12,38` runs the pilot's lever: a 12-turn first session, then 38 turns
(the task's own budget is 20 and 30, `teamtrack/reference/f2/task.toml`). The Makefile passes
`SESSION_BUDGET` to `show-2` since fd9726c (`make -n show-2 SESSION_BUDGET=12,38` prints
`--session-budget=12,38`).

Label, every time: a show-N run is "harness in action, not an A/B: its score stays out of every
bare-vs-harness comparison". The console shows the purple `HARNESS IN ACTION — one arm, not an A/B`
badge on every screen.

### Every result, on one slide and one console view

Each section's demo block ends on the all-results slide and on console screen `4`. Say the result
plainly: "no measurable difference on this task with this model". Primary measure passed, bare /
harness (VERIFICATION.md, "Run 3", "Run 4", "Gate decision", "Class-profile round"):

| Section | Run 3, effort medium (k=3) | Run 4, effort low (k=3) | Class-profile round (k=1) | Classification |
|---|---|---|---|---|
| S1 F1 `trap-legacy-pattern` | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-084558-0356a0`) | no measurable difference |
| S2 F2, session budget 12, 38 | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-085139-7c0661`) | no measurable difference |
| S3 F3 `trap-tempting-middleware` | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-090051-91f837`) | no measurable difference |
| S4 F4 canonical | 0/3, 0/3 | not run (pilot cap) | 0/1, 0/1 (`ab-20261017-090903-926c02`) | no measurable difference (both arms fail) |

Run 3 A/Bs: F1 `ab-20261016-211419-07937b`, `-212745-2c14fb`, `-214636-c8b3c4`; F2
`-211419-dfe06f`, `-213317-9a0ec1`, `-214959-de790f`; F3 `-212115-a361f5`, `-213624-d7eb13`,
`-215443-f2c188`; F4 `-212252-aa1644`, `-214151-ca9841`, `-220010-c5b4bf`. Run 4: F1
`ab-20261016-232842-b372c2`, `-233807-3f34fa`, `-234639-4a18bd`; F2 `-232842-ac03b2`,
`-234027-226a76`, `-235211-ea59a9`; F3 `-233517-2c9ea4`, `-234509-8b9bfa`, `-235305-723a0f`.

Post hoc, and labelled so on the slide: measures chosen after the results were known, descriptive,
not tested, over 34 arm runs per arm from runs 2-4 and the live console check (VERIFICATION.md,
"Exploratory analysis of the 94 pilot arm runs"):

| Measure | Bare | Harness |
|---|---|---|
| Runs with a file changed outside the allowed paths | 9 of 34 (F4 6 of 6, F2 3 of 9) | 0 of 34 |
| Runs that claimed done | 19 of 34 | 10 of 34 |
| Done claims with failing hidden tests | 0 of 19 | 0 of 10 |
| Tests shipped, median | 7.5 | 2.5 |
| Arm wall time, median | 190 s | 302 s |
| Agent time limit hit | 4 of 34 | 9 of 34 |
| Cost per arm, median | $0.0103 | $0.0123 |

The scope layer runs only in F3 and F4 (demo-3 and demo-4 stacks). Never credit it for F2's 0 of 9:
the F2 harness arm has no scope layer. On F3, the section that measures scope, the bare arm never
left scope either.

The pilot's experiment batches (M8: the k=10 headline batch, the leave-one-layer-out ablation, the
control tasks) were not run, because the pre-registered gate did not pass. Wherever an older slide
or note promises "experiment dots", show the pilot results above instead.

---

## Before class (start 60 minutes early)

Everything runs inside WSL2 Ubuntu on the class host, in `~/shipharness` (DESIGN §9, D-22). `make warm`
ran on T-1 (instructor guide, stage 1); run it again here, it takes seconds when nothing changed.

| Step | Command | Expect |
|---|---|---|
| 1. Environment | `make doctor` | Every line `+ ok`, last line `result: + ready`. Fix anything marked `x` (see failure modes below) |
| 2. Warm-up | `make warm` | Last line `warm: done (<seconds> s)`. In the class-profile round the second run took 1.2 s (the first, with an image rebuild, 407 s; VERIFICATION.md, "Class-profile round"); before the quiet runs on 2026-10-17 it ended `warm: done (140.6 s)`, again with an image rebuild. A line starting with `x` is a failed step |
| 3. Console | `make console` in terminal A (leave it running) | `Console: http://127.0.0.1:8765/` |
| 4. Browser | Open `http://127.0.0.1:8765/` | The runs list and the key legend |
| 5. Fallbacks present | `ls .shipharness/runs/<id>/ab.json` for each fallback in [fallbacks.md](fallbacks.md) | One file per id |
| 6. Policy printout ready (S3) | `uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'` | Starts with `Sandbox policy (identical for both arms)` |
| 7. Assessment ready (opening) | `uv run python skills/harness-setup/scripts/assess.py teamtrack --out .shipharness/harness-assessment.html` | A summary per area, then one line per check, then `report: ...` |
| 8. Slides | Open the deck on slide 1 | |

Do not run any `make show-N` or `make final` before class on the class date: the session cost cap
(`MAX_SESSION_COST_USD` $2.50, keyed by `SHIPHARNESS_CLASS_DATE`) is shared by every command run under
that date (DESIGN §11.1). `make warm` makes no model calls.

### Screen layout

| Window | Content |
|---|---|
| Terminal A | `make console` (server log; leave it alone) |
| Terminal B | The section command `make show-N`, large font (a replay only as the emergency fallback) |
| Terminal C | `make final` only: launched at the S4 launch (2:55), read in the final block (3:40) |
| Browser tab 1 | Slides |
| Browser tab 2 | Console: the runs list at `http://127.0.0.1:8765/`, then the current run at `/run/<id>` |
| Browser tab 3 (optional) | LangSmith, signed in, project `shipharness-class-<date>` (DESIGN §12) |
| Browser tab 4 | Console: the final A/B at `/run/<ab id>`, opened at the S4 launch and shown in the final block |

### Console keys (DESIGN §13; `src/shipharness/console/static/stream.js`)

| Key | Screen | Shows |
|---|---|---|
| `1` | Live Console | Per arm: container line (id, network, CPU, memory, time left), cost against the run cap, turns, harness decisions, gate pills, "Agent said" vs "Referee", and the "primary verdict ready" pill with the time from launch |
| `2` | Boards | Board screenshot per arm every 5 s, with marks (⚠ other org, ⧉ duplicate); S4 adds the two-tab conflict panel |
| `3` | Evidence | Files read and sessions; diff map and sandbox denials; referee checks, filter table, mutant table |
| `4` | A/B Report | Dots per run from `exports/`, one row per feature, variant, and arm; records of an older referee version and harness-in-action runs are counted and left out |
| `5` | Traces | Live tail of events, first wrong turn per arm, trace links |
| `F` | | Cycles full screen for one arm: both, bare, harness |

Finding the current run: `make show-N` prints the run id only when it finishes. While it runs,
reload the runs list and open the newest `ab-...` entry (ids start with a time stamp). The runs list
does not refresh by itself. In S4 two runs start a minute apart: open each one right after its own
launch ([S4](#s4-verification-250-340)).

---

## Minute-by-minute

Times are elapsed from the start of class. Slide numbers refer to
[../slides/outline.md](../slides/outline.md). Each section S1 to S4 opens with its poll, launches
`make show-N` right after it, teaches the concepts and the walkthrough while the run proceeds, and
ends with the demo block: harness in action (live) and all results
([Section pattern](#section-pattern-s1-to-s4)). S4 opens with two polls, the S4 poll and the final
feature poll, and launches `make final` in terminal C right after `make show-4`; the final block at
3:40 walks through the finished final A/B and starts no run.

| Time | Block | What happens | Command or screen | Slides |
|---|---|---|---|---|
| 0:00-0:03 | Opening: problem | Title; four failures the referee checks in every run | | 1-2 |
| 0:03-0:05 | Opening: why | Four causes, cited | | 3 |
| 0:05-0:07 | Opening: solution | The harness: four parts plus the sandbox; the claim (A3, F-a-124) | Architecture diagram | 4 |
| 0:07-0:10 | Opening: tour | shipharness, TeamTrack, console tour (keys 1-5); `Opening:two_arms` and `Opening:publish` briefly; how we measure it and what the pilot found; `make doctor`; `harness-setup` assessment | Terminal B, console tab | 5-7 |
| 0:10-0:13 | S1 poll | Poll S1; close it before the launch | | 8 |
| 0:13-0:15 | S1 launch | `make show-1` at 0:13; open the new run on screen 1 | Terminal B, console | 9 |
| 0:15-0:30 | S1 concepts (run going) | Problem, cause, harness piece, the assumption it encodes | | 10-15 |
| 0:30-0:40 | S1 walkthrough (run going) | `S1:agents_md`, `S1:progressive`, `S1:prefix`; at 0:35 check terminal B for the `Cost:` line | Editor, terminal B | 16-18 |
| 0:40-0:50 | S1 demo: harness in action | The finished show-1 run: screens 1, 3, 5, and 2 | Console | 19 |
| 0:50-0:53 | S1 demo: reading the result | show-1's verdict on screen 1; the first wrong turn and the trace links on screen 5 | Console | 20 |
| 0:53-0:55 | S1 demo: all results | All-results slide, S1 row; screen 4 | Slides, console | 20 |
| 0:55-1:00 | S1 discussion | Discussion; transition | | 21 |
| 1:00-1:03 | S2 poll | Poll S2; close it before the launch | | 22 |
| 1:03-1:05 | S2 launch | `make show-2 SESSION_BUDGET=12,38` at 1:03; open the new run on screen 1 | Terminal B, console | 23 |
| 1:05-1:20 | S2 concepts (run going) | | | 24-28 |
| 1:20-1:30 | S2 walkthrough (run going) | `S2:init`, `S2:stop_resume`, `S2:write`; at 1:25 check terminal B for the `Cost:` line | Editor, terminal B | 29-31 |
| 1:30-1:40 | S2 demo: harness in action | Session stop and resume, the handoff: screens 1, 3, 2, and 5 | Console | 32 |
| 1:40-1:43 | S2 demo: reading the result | show-2's verdict on screen 1; screen 3 "Sessions" | Console | 33 |
| 1:43-1:45 | S2 demo: all results | All-results slide, S2 row; screen 4 | Slides, console | 33 |
| 1:45-1:50 | S2 discussion | Discussion; transition | | 34 |
| 1:50-2:00 | Break | Return time on screen | | 35 |
| 2:00-2:03 | S3 poll | Poll S3; close it before the launch | | 36 |
| 2:03-2:05 | S3 launch | `make show-3` at 2:03; open the new run on screen 1 (sandbox line) | Terminal B, console | 37 |
| 2:05-2:20 | S3 concepts (run going) | Includes two sandbox slides | | 38-43 |
| 2:20-2:30 | S3 walkthrough (run going) | `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile`; at 2:25 check terminal B for the `Cost:` line | Editor, terminal B | 44-45 |
| 2:30-2:40 | S3 demo: harness in action | Scope decisions and sandbox on show-3's screens 1, 3, and 5; the sandbox moment | Console | 46 |
| 2:40-2:43 | S3 demo: reading the result | show-3's verdict on screen 1; the diff map on screen 3 | Console | 47 |
| 2:43-2:45 | S3 demo: all results | All-results slide, S3 row; screen 4 | Slides, console | 47 |
| 2:45-2:50 | S3 discussion | Discussion; transition | | 48 |
| 2:50-2:53 | S4 poll | Poll S4 | | 49 |
| 2:53-2:54 | Final feature poll | Final feature poll (F5, F6, F7); close it before the launch | | 50 |
| 2:54-2:56 | S4 launch | `make show-4` at 2:54 in terminal B, opened in browser tab 2; `make final FEATURES=<poll winner(s)>` at 2:55 in terminal C, opened in browser tab 4; back to show-4 on screen 1 | Terminals B and C, console | 51 |
| 2:56-3:10 | S4 concepts (two runs going) | | | 52-57 |
| 3:10-3:20 | S4 walkthrough (two runs going) | `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate`; at 3:15 check terminal B (show-4) and terminal C (final) for their `Cost:` lines | Editor, terminals | 58-60 |
| 3:20-3:30 | S4 demo: harness in action | Test phase, filter table, gate pills, boards: screens 1, 3, 2, and 5 | Console, tab 2 | 61 |
| 3:30-3:33 | S4 demo: reading the result | show-4's "Agent said" against the referee on screen 1; hidden tests and mutants on screen 3 | Console, tab 2 | 62 |
| 3:33-3:35 | S4 demo: all results | All-results slide, S4 row; screen 4 | Slides, console | 62 |
| 3:35-3:40 | S4 discussion | Discussion; transition to the final A/B | | 63 |
| 3:40-3:42 | Final A/B | Terminal C: arm lines and the session figure | Terminal C | final results slides |
| 3:42-3:46 | Final A/B | Screens 1, 3, 5 of the finished final A/B, both arms | Console, tab 4 | final results slides |
| 3:46-3:48 | Final A/B | Both boards | Console screen 2 | final results slides |
| 3:48-3:53 | Final A/B and all results | Screen 4: tonight's final next to the pilot's dots; the all-results slide for all four sections; `Final:dots` | Console, slides | final results, all results |
| 3:53-3:56 | Wrap-up | Assignments | | wrap-up |
| 3:56-3:58 | Wrap-up | Skills, the starter kit (`shipharness init`), `Final:skill_template` | | wrap-up |
| 3:58-4:00 | Wrap-up | References | | wrap-up |

The slide numbers from 64 on (final results, the all-results slide, wrap-up) are in
[../slides/outline.md](../slides/outline.md).

### How long the runs take

Expected times come from the class-profile round, 2026-10-17 (one A/B per section, one at a time,
class profile, after `make warm`; VERIFICATION.md, "Class-profile round"). The harness arm of each
A/B is the closest measured match for `make show-N`, which runs that arm alone:

| Section | Class-round A/B | Harness arm: launch to primary verdict | Harness arm: launch to full verdict | Whole A/B finished within |
|---|---|---|---|---|
| S1 | `ab-20261017-084558-0356a0` | 114 s | 324 s | 336 s |
| S2 | `ab-20261017-085139-7c0661` (session budget 12, 38) | 358 s | 533 s | 533 s |
| S3 | `ab-20261017-090051-91f837` | 317 s | 481 s | 481 s |
| S4 | `ab-20261017-090903-926c02` | 811 s | 927 s | 927 s |

Every class-round A/B finished within 15.5 minutes of launch. A run launched at section minute 3 (S4:
minute 4) is therefore expected to be finished before the check at minute 25. The harness arms are
slower than the bare arms because harness work runs on its own clock after the agent's turns
(session-end handoffs run the visible suite, about 31-34 s each on this host); in F4 the test-phase
filters ran each of the harness arm's 6 tests 5 times.

The class commands themselves were timed on 2026-10-17 on a quiet machine, one command at a time,
after `make warm`, with `PURPOSE=pilot` and the class profile (the quiet runs; `real` is the shell's
`time` of the whole command; the console captured screens 1 and 2 every minute):

| Command | Run | Launch to primary verdict | Launch to full verdict | Whole command (`real`) | Exit | Result | Cost: arm + review |
|---|---|---|---|---|---|---|---|
| `make show-1` | `ab-20261017-112101-c5d839` | 4:11 | 10:00 | 10 min 14 s | 0 | completed, claimed done; primary pass (0 new R1); hidden 52/52, mutants 2/4 | $0.0179 + $0.0019 |
| `make show-2 SESSION_BUDGET=12,38` | `ab-20261017-113213-fe89a3` | 6:46 | 9:52 | 10 min 7 s | 2 | agent time limit in session 2; primary pass (no continuity failure); hidden 56/56, mutants 0/4 | $0.0268 + $0.0027 |
| `make show-3` | `ab-20261017-114259-b64f54` | 4:25 | 7:31 | 7 min 43 s | 0 | completed, claimed done; primary pass (0, 0); hidden 49/49, mutants 4/4 | $0.0142 + $0.0030 |
| `make show-4` | `ab-20261017-115138-c45d9d` | 9:19 | 10:55 | 11 min 6 s | 2 | claimed done, gate passed, then the agent time limit in the test phase; primary fail; hidden 68/69, mutants 0/4 | $0.0233 + $0.0032 |
| `make final FEATURES=F5` | `ab-20261017-120323-c97138` | bare 3:27, harness 9:48 | bare 6:50, harness 12:32 | 12 min 47 s | 2 | bare completed, claimed done; harness agent time limit, no claim; no primary measure; hidden 46/46 and mutants 2/3 in both arms | bare $0.0177, harness $0.0226; reviews $0.0053; command $0.0456 |

Exit 2 means an arm was aborted at a time limit, not that the command broke. Every show run
finished within 11 min 6 s of launch, so a run launched at section minute 3 (S4: minute 4) is
finished before the check at minute 25. The quiet runs were slower than the class-profile round's
harness arms on the same tasks (S1 full verdict 10:00 against 324 s); both are real, so plan for
the slower figure.

The final runs during S4, next to show-4. Launched at 2:55, it must be finished by 3:40, when the
final block starts ([Final results and wrap-up](#final-results-and-wrap-up-340-400)). `make final`
runs its features one after another: with two features, the second starts when the first prints its
`Cost:` line. No F5-F7 A/B ran in the pilot or the class-profile round; the quiet run of
`make final FEATURES=F5` above is the measured time of one feature with the class profile.

At most two runs at a time: in S4, show-4 and the final run together. The class profile limits each
container to 2 CPUs (VERIFICATION.md, change 18) because a class runs at most two A/Bs at once (owner
instructions, 2026-10-17).

### Check at section minute 25

Halfway through the walkthrough, glance at terminal B.

- **The `Cost:` line is there.** Show-N is finished; finish the walkthrough. The demo block runs on
  the finished run.
- **Show-N is still running.** Finish the walkthrough. Open the demo block on screens `1` and `3` of
  the running show-N: screen 1 shows "primary verdict ready" as soon as the primary check is done,
  and the secondary checks fill in while you talk.
- **Show-N failed for a reason outside the experiment** (`ERROR` from Docker, the network, or OpenAI;
  see [Fallback: known failure modes](#fallback-known-failure-modes)). Follow
  [Fallback: replay procedure](#fallback-replay-procedure) with the section's fallback recording from
  [fallbacks.md](fallbacks.md). A run that finished with an unwelcome result is a result, not a
  failure: show it.
- **S4 only: terminal C.** Look for the first final feature's `A/B <ab id> (<feature>, layers=[...],
  profile=class)` line and its `Cost:` line. Whether it is there or not, nothing changes now: the final
  has until 3:40. If an arm ended `ERROR` for a reason outside the experiment, note it; the fallback
  for the final block is in [fallbacks.md](fallbacks.md).

---

## Opening (0:00-0:10)

**0:00-0:03 Problem.** Slide 2: the four failures, and that the referee checks every run for all
four, in both arms. There is no board screenshot: in the course pilot no bare F1 arm shipped a new
tenant-isolation violation (runs 2, 3, and 4, and the live console check), and no arm in the
class-profile round leaked another org's cards (VERIFICATION.md, "Class-profile round"). Say: "We
come back to what that means at the end." No real run produced ⚠ marks; they are covered by the
console tests (VERIFICATION.md, "Class-profile round"). An optional constructed example that shows
them is in `docs/extras.md`, outside the class flow.

**0:03-0:07 Why and solution.** Slides 3-4; the four causes with their citations as in the story
above; the four parts and the sandbox on the architecture diagram; the claim with A3's quote
(F-a-124), and "keep what earns its place" named as course framing.

**0:07-0:10 Tour.**
1. Switch to the console tab, press `1` to `5` once each and name each screen (table above).
2. Open `src/shipharness/ab/demo.py` at `Opening:two_arms` and `src/shipharness/events/bus.py` at
   `Opening:publish`; one minute each (talking points in [code-walkthrough.md](code-walkthrough.md)).
3. Slide 6, how we measure it: one sentence on the pilot ("in runs 3 and 4 the arms tied on every
   section's primary measure; you will see each result in its section").
4. Terminal B: `make doctor`. Read out the key lines; it never prints any part of a key (CONTRACTS
   §20).
5. Terminal B: the `harness-setup` assessment on the bare TeamTrack (command in "Before class", step
   7). Say: "This is what the bare arm works with: no map, no progress file, no feature list. The
   harness arm gets those parts; the rules themselves are in both."

---

## Section pattern (S1 to S4)

Every section runs the same way (DESIGN §14.1): the run is launched right after the poll, so that
its run time is hidden behind the concepts and the walkthrough. Minutes are counted from the start of
the section.

1. **Poll (minutes 0-3).** Feature and rule at risk in one sentence (the poll slide carries both),
   then the poll ([poll-questions.md](poll-questions.md)). The poll asks the room to predict the
   pilot's result for the section. Close the poll before you launch.
2. **Launch (minutes 3-5).** Terminal B: `make show-N` at minute 3. Reload the runs list, open the
   newest `ab-...`, and stay on screen `1` while the container starts and the first turns arrive.
   Say: "This is the harness arm alone, live. It is not an A/B: we watch the layer do its job. The A/B
   results come at the end of the section." Then switch to the slides.
3. **Concepts (minutes 5-20, run going).** Problem, then cause, then harness piece, then the
   assumption the piece encodes. Leave terminal B and the console alone.
4. **Walkthrough (minutes 20-30, run going).** Anchors in [code-walkthrough.md](code-walkthrough.md).
   At minute 25, check terminal B for the `Cost:` line
   ([Check at section minute 25](#check-at-section-minute-25)).
5. **Demo block (minutes 30-45).**
   - **Harness in action (10 min):** the finished show-N run on the section's screens, in the order
     of the "what to watch" slide (screen 1 timeline, screen 3 evidence, screen 2 boards, screen 5
     traces).
   - **Reading the result (3 min):** show-N's verdict on screen 1 ("primary verdict ready", then the
     full verdict), what it means for the section, and the session figure on the `Cost:` line.
   - **All results (2 min):** the all-results slide, this section's row and the post hoc table, then
     screen `4`. "No measurable difference on this task with this model."
6. **Discussion and transition (minutes 45-50).**

S4 differs in its first six minutes: two polls (minutes 0-4), then two launches, `make show-4` and
`make final` (minutes 4-6), so its concepts run from minute 6 to minute 20
([S4](#s4-verification-250-340)).

What the terminal prints at the end of `make show-N` (format from `src/shipharness/ab/commands.py`):
one line `A/B <id> (<feature>, layers=[...], profile=class, harness in action)`, one line for the
harness arm with status, claim, primary measure, `passed=`, hidden tests passed of total, mutants
killed of total, reviewer verdict, and cost, then the cost line `Cost: $... (this command: ...;
session $... of $2.50; ...)`. Read the session figure aloud in each demo block; it is the meter for
the rest of the class. The exit code is 2 when the arm was aborted (for example at the agent time
limit), which is a result, not a failure of the command.

What the console keeps after a run: screen `1` shows the full scrollable timeline once a run has
finished; screen `5` keeps the last 40 tail lines (`TAIL_SIZE` in
`src/shipharness/console/state.py`). The launch is the moment to show the first turns live.

---

## S1 Instructions (0:10-1:00)

**Feature and rule.** `make show-1` runs F1, org-wide issue search (`GET /issues`), canonical ticket,
from checkpoint `m1-s1-start`, one session of 30 turns (`teamtrack/reference/f1/task.toml`). Rule at
risk: R1 tenant isolation. The legacy `GET /v1/issues` handler has no tenant filter and is in the
repository next to the right pattern; A1 reports that agents copy existing patterns (A1, F-a-20).
Primary measure: one or more new R1 violations fails the run (DESIGN §8.2). Harness arm layers:
instructions only (DESIGN §6.6). The assumption the map encodes: the model will not apply a rule it
has not been pointed to (course wording, after A3, F-a-124).

**Poll (0:10-0:13).** Slide 8; the S1 question in [poll-questions.md](poll-questions.md).

**Command (0:13).** `make show-1`, right after the poll closes.

**At launch (0:13-0:15).** Reload the runs list, open the newest `ab-...`, press `1`. The harness
arm's first harness decision lists the instruction files it placed. If the first `read_file` calls
have arrived, point at them: "Watch which files it opens before it writes code."

**Check at 0:35** (during slide 17): the `Cost:` line in terminal B.

**Demo block (0:40-0:55): screens and what to say.**

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` Live Console | The full timeline: the instruction files placed, the map and the documents it points to read, then the code | "The map is about 100 lines and points outward (A1, F-a-27, F-a-28). The bare arm has every rule too, in `docs/HANDBOOK.md`." |
| Harness in action | `3` Evidence | "Files read" by category (map, skill, harness doc, code, test); the referee's R1 line | "The referee probes every endpoint as Acme with Globex ids and expects 404 (DESIGN §5). It does not care which arm wrote the code." |
| Harness in action | `2` Boards, `5` Traces | The harness arm's board as an Acme user: "✓ only own-org cards"; the tail of events and the trace links | "F1 changes no board pixels, so the board shows one frame. Screen 5 is where you look for the first wrong turn." |
| Reading the result | `1` | "primary verdict ready" with the time from launch, then the referee's verdict: new R1 violations, hidden tests, mutants | "This is one harness arm on one run. It tells us the layer ran; it cannot tell us the layer helped. That needs the A/B, next." |
| All results | slide 20, screen `4` | S1 row: run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | "No measurable difference on this task with this model. Here the assumption did not hold: the bare arm applied R1 from the handbook." |

What the quiet run of `make show-1` showed (captured on 2026-10-17, run
`ab-20261017-112101-c5d839`; your output will differ): screen 1 listed 31 instruction files placed
(the AGENTS.md map, docs, skills); the agent's third tool call opened `docs/HANDBOOK.md`, and the
harness decisions recorded `ARCHITECTURE.md` and the add-endpoint skill as read; build session 23
turns, test phase 12; "primary verdict ready: PASS" (new R1 violations 0) 4:11 after launch, the full
verdict 10:00 after launch (hidden tests 52/52, mutants 2/4, reviewer accept); screen 2 "✓ only
own-org cards, no duplicates"; screen 5 "no wrong turn found". Cost: $0.0179 for the arm, $0.0019 for
the review.

Post hoc for S1 (descriptive; VERIFICATION.md, exploratory rows "F1 bare" and "F1 harness", 10 runs
per arm): harness arms claimed done in 5 of 10 runs, bare arms in 9 of 10; median cost per arm
$0.0122 against $0.0103; median arm wall time 168 s against 177 s; no agent time limit hit in either
arm.

**Discussion (0:55-1:00).**
1. "The bare arm could read the same rules, and applied them. What would have to be true of a model
   or a ticket for the map to earn its place?" Tie back to cause 1 (A1, F-a-05).
2. Transition: link `submodules/01-instructions/demo/README.md`; next problem: what happens when a
   session ends halfway.

---

## S2 State and session lifecycle (1:00-1:50)

**Feature and rule.** `make show-2 SESSION_BUDGET=12,38` runs F2, comments on issues with a comments
panel on the board, from `m1-s2-start`, two sessions with the pilot's budgets 12 and 38 (the task's
own budget is 20 and 30, `teamtrack/reference/f2/task.toml`): session 1 stops after 12 turns, the arm
gets the wrap-up turns (`WRAPUP_TURNS`, default 3) and the neutral resume sentence (DESIGN §6.3). Primary measure: continuity failure, any of R7 failing, a
second migration creating the same table, or ≥ 30% of session-1 lines removed in session 2 (DESIGN
§8.2). Harness arm layers: instructions, state. The assumption the state files encode: a fresh
session cannot pick up the work from the repository alone (A2 states the problem, F-a-08; the
one-line form is the course's). The runner rule since change 14 (both arms): before the last build
session, `finish(claim="not_done")` ends only that session.

**Poll (1:00-1:03).** Slide 22; the S2 question in [poll-questions.md](poll-questions.md).

**Command (1:03).** `make show-2 SESSION_BUDGET=12,38`, right after the poll closes.

**At launch (1:03-1:05).** Open the newest `ab-...`, press `1`. The harness arm's first harness
decision is the initializer step note (`init.sh`, `progress.md`, `session-handoff.md`, the exec
plan); its first turns follow the Getting up to speed routine.

**Check at 1:25** (during slide 30): the `Cost:` line in terminal B.

**Demo block (1:30-1:45): screens and what to say.**

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` | "■ Session 1 stopped" and "▶ Session 2 resumed" in the finished timeline | "This stop is the session turn budget. A3 calls the pattern a context reset with a structured handoff (A3, F-a-65; RESEARCH G-5)." |
| Harness in action | `3` Evidence | "Sessions" (turns, `ended_by`, ↺ redone files); "Files read": `progress.md`, `session-handoff.md` | "Session 2 started with A2's Getting up to speed routine (A2, F-a-58 to F-a-62)." |
| Harness in action | `2`, `5` | The board after the run ("✓ only own-org cards, no duplicates"); the first wrong turn and the trace links | "Did the second session finish what the first started? Screen 5 names the first turn that edited a file a failing check names." |
| Reading the result | `1`, `3` | "primary verdict ready", then the continuity verdict; screen 3 "Sessions" | "Before change 14, a `finish(not_done)` at the end of session 1 ended the build phase in 6 of the 12 F2 arms of runs 3 and 4. Now it ends only that session, in both arms." |
| All results | slide 33, screen `4` | S2 row: run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | "No measurable difference on this task with this model. The measure cannot fail when session 1 leaves nothing to redo: 6 of the 12 F2 arms of runs 3 and 4 built nothing (hidden 3 of 56)." |

What the quiet run of `make show-2 SESSION_BUDGET=12,38` showed (captured on 2026-10-17, run
`ab-20261017-113213-fe89a3`; your output will differ): about 2 minutes after launch, turn 1.12 called
`finish not_done` and screen 1 showed "■ Session 1 stopped: ended by claim_not_done; handoff
session-handoff.md", then "▶ Session 2 resumed: prefix: core, instructions, state"; session 2's first
turn ran `pwd; git log --oneline -20; cat progress.md`. Sessions: 12 turns, then 31, when the agent
time limit ended the run (`ABORTED: timeout`, exit 2). "primary verdict ready: PASS" (no continuity
failure) 6:46 after launch, the full verdict 9:52 after launch: hidden tests 56/56, mutants 0/4,
diff scope 1 new (secondary; screen 5's first wrong turn: turn 2.16 edited `app/api/issues.py`),
reviewer reject. Cost: $0.0268 for the arm, $0.0027 for the review.

Post hoc for S2 (VERIFICATION.md, exploratory rows "F2 bare" and "F2 harness", 9 runs per arm):
harness arms hit the agent time limit in 4 of 9, bare arms in 0 of 9; median arm wall time 361 s
against 232 s. The F2 harness primary 6 of 9 there includes run 2's 0 of 3, measured before change 7
fixed the continuity check.

**Discussion (1:45-1:50).**
1. "Which state file would you keep for this model, and how would you measure it?"
2. Transition: `submodules/02-state-lifecycle/demo/README.md`.

---

## Break (1:50-2:00)

Slide 35 with the return time (filled in live). Nothing runs during the break.

---

## S3 Scope and sandbox (2:00-2:50)

**Feature and rule.** `make show-3` runs F3, idempotency keys on issue creation, from `m1-s3-start`,
build phase then test phase (`teamtrack/reference/f3/task.toml`; build allow list
`app/api/issues.py`, `app/services/issues.py`, `docs/HANDBOOK.md`, `tests/visible/**`; test allow
list `tests/visible/**`). Primary measure: ≥ 1 out-of-scope file in the shipped diff, or ≥ 1 source
file changed during the test phase (DESIGN §8.2). Harness arm layers: instructions, state, scope. The
scope layer enforces this measure, so the harness arm's zero is expected by construction. The
assumption it encodes: the agent will change files outside the ticket unless code stops it (course
wording; cause 3's sources stand side by side).

**Poll (2:00-2:03).** Slide 36; the S3 question in [poll-questions.md](poll-questions.md).

**Command (2:03).** `make show-3`, right after the poll closes.

**At launch (2:03-2:05).** Open the newest `ab-...`, press `1`: the sandbox line (container id,
`network none`, CPU, memory, time left). The class profile gives every arm and referee container 2
CPUs (VERIFICATION.md, change 18).

**Check at 2:25** (at the switch from slide 44 to slide 45): the `Cost:` line in terminal B.

**Demo block (2:30-2:45): screens and what to say.**

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` | Harness decisions: ⊘ block and ↺ revert with the reason, if any; gate line "No gate." (S3 has no verify layer) | "The reason text is what the agent reads in its tool result. It names the phase and the allowed paths." |
| Harness in action | `3` | "Diff map": ✎ changed, ⊘ blocked; "Sandbox denials" | "The sandbox is the same for both arms. It is taught here, but it is never the variable (DESIGN §9)." |
| Harness in action | `5` | The tail of events and the trace links | "If the guard blocked an edit, this is where you see what the agent did next." |
| Reading the result | `1`, `3` | "primary verdict ready", then out-of-scope files and test-phase source edits | "The harness arm's zero is expected by construction: the guard enforces this measure. The interesting part is whether it still shipped a working feature: hidden tests on the same line." |
| All results | slide 47, screen `4` | S3 row: run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1 | "No measurable difference on this task with this model: no shipped diff touched `app/api/middleware.py` in either arm. The clearest post hoc difference in out-of-scope files was on F4, where scope was not the primary measure; it is not a measured effect." |

**Sandbox moment.** If screen `3` of show-3 lists a denial tonight, show its reason code (`network`,
`write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and the command.
If none occurred, show the policy printout (command in "Before class", step 6) and say: "No run in
pilot runs 3 and 4 or the class-profile round had a sandbox denial" (`grep -c sandbox_denied` over
those runs' `events.jsonl`, read 2026-10-17: 0 in every A/B).

What the quiet run of `make show-3` showed (captured on 2026-10-17, run `ab-20261017-114259-b64f54`;
your output will differ): the agent began with `pwd; git status --short; git log --oneline`; the
harness decisions were the 31 instruction files, the initializer step, and "feature_list.json
written with F3 (passes: false)"; the agent never tried an edit outside the allow list, so no ⊘
block or ↺ revert appeared, and screen 3 listed no sandbox denial. Sessions: build 18 turns, test 12.
"primary verdict ready: PASS" (out-of-scope files 0, test-phase source edits 0) 4:25 after launch,
the full verdict 7:31 after launch: hidden tests 49/49, mutants 4/4, reviewer reject. Cost: $0.0142
for the arm, $0.0030 for the review. So in a run like this one, the sandbox moment is the policy
printout.

Post hoc for S3 and F4 (VERIFICATION.md, exploratory rows "F3" and "F4"): on F3 harness arms shipped
a median of 0 tests against 6, killed a median of 0 of 4 referee mutants against 4, and claimed done
in 4 of 9 runs against 9 of 9. On F4, bare arms changed files outside the allowed paths in 6 of 6
runs, harness arms in 0 of 6.

**Discussion (2:45-2:50).**
1. "The clearest post hoc difference showed where scope was not the primary measure. How would you
   register that before the next run?"
2. Transition: `submodules/03-scope-sandbox/demo/README.md`.

---

## S4 Verification (2:50-3:40)

**Feature and rule.** `make show-4` runs F4, optimistic concurrency (ETag, If-Match) and issue
history, from `m1-s4-start`, one session of 40 turns (`teamtrack/reference/f4/task.toml`). Two
co-primary counts per run: hidden tests passed of 69 (VERIFICATION.md, M5 counts) and referee-set
mutants killed by the arm's shipped tests of 4 (`teamtrack/mutants/features/f4.jsonl`) (DESIGN
§8.2). Harness arm layers: all four. The assumption the gate and filters encode: the agent's "done"
and its own tests cannot be trusted (A3, F-a-15; A4, F-a-17; the one-line form is the course's).

**Poll (2:50-2:53).** Slide 49; the S4 question in [poll-questions.md](poll-questions.md).

**Final feature poll (2:53-2:54).** Slide 50; the final feature question in
[poll-questions.md](poll-questions.md): F5 bulk close, F6 watchers, or F7 labels. Close it before
the launch. Run the winner and the runner-up, in that order (cost note below).

**Commands (2:54 and 2:55).**
1. **2:54, terminal B:** `make show-4`, right after the final poll closes. Reload the runs list and
   open the newest `ab-...` in browser tab 2. Open it now, before the second launch, because the runs
   list shows only ids, newest first.
2. **2:55, terminal C:** `make final FEATURES=<winner>,<runner-up>` (for example
   `make final FEATURES=F6,F5`). Always pass `FEATURES`: the Makefile default is `F5,F6`. Reload the
   runs list in browser tab 4 and open the newest `ab-...`: the final's first A/B. Leave terminal C
   and tab 4 alone until the final block.

Two runs now go in parallel: show-4 (one arm) and the final's first feature (two arms). `make final`
runs its features one after another (Makefile `final` target).

**At launch (2:55-2:56).** Back to browser tab 2, press `1`. Say: "Two runs are going: the harness
arm alone on F4 for this section, and the final A/B on the feature you picked, both arms. We come
back to F4 in the demo block and to the final at the end of class."

**Cost of the class.** Caps (DESIGN §11.1; `.env.example`): each show-N arm stops at
`MAX_RUN_COST_USD` ($0.20) plus `MAX_REVIEW_COST_USD` ($0.04) for its review, so at most $0.24; each
final arm at `MAX_FINAL_RUN_COST_USD` ($0.25) plus the review cap, so a final feature costs at most
2 × $0.25 + 2 × $0.04 = $0.58; the session at `MAX_SESSION_COST_USD` ($2.50, persisted across
commands). At the caps, four show-N
runs and two final features are 4 × $0.24 + 2 × $0.58 = $2.12, under the session cap, so both final
features fit unless other model commands ran under the class date. Launching show-4 and the final
together keeps every cap: before every call the tracker reserves the call's worst case under one
lock and reads the calls the other command appended to the shared cost ledger (VERIFICATION.md,
change 12). Measured in the class-profile round (agents at the Fast tier, every call reported
`fast`; reviews Standard): harness arm and review per section, F1 $0.0151 + $0.0028, F2 $0.0357 +
$0.0041, F3 $0.0135 + $0.0031, F4 $0.0257 + $0.0040; the round's four A/Bs cost $0.1953 in total.
The final's measured cost: the quiet run of `make final FEATURES=F5` (2026-10-17, run
`ab-20261017-120323-c97138`) cost $0.0456 for the command: bare arm $0.0177, harness arm $0.0226,
both reviews $0.0053.

**Check at 3:15** (during slide 59), two terminals:
- Terminal B: the show-4 `Cost:` line. If show-4 is still running, open the demo block on its live
  screens; screen 1 shows "primary verdict ready" as soon as it is known.
- Terminal C: the first final feature's result lines and `Cost:` line, or nothing yet. Either is
  fine: the final has until 3:40.

**Demo block (3:20-3:35), browser tab 2: screens and what to say.**

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` | Gate pills of the last gate: ✓ or ✗ for visible tests, existing tests, R1-R7, board, clean state, if the arm claimed done; otherwise the test phase and the "primary verdict ready" pill | "The harness runs checks the agent does not control; a failure goes back to the agent with the first three reasons." |
| Harness in action | `3` | Filter table (tests × filters 1-5, kept or discarded with reason), mutant table, referee counters, reviewer verdict | "Filters 1 to 3 are TestGen-LLM's (B11); 4 and 5 are course filters (RESEARCH G-7). Filter 2 now re-runs each test 5 times, TestGen-LLM's 'five executions' (B11, F-b-19)." |
| Harness in action | `2` | The board and the two-tab conflict panel: "✓ conflict detected" | "Two tabs edit the same issue; the second save is refused with 'This issue was changed by someone else'. The board check runs on every arm." |
| Reading the result | `1`, `3` | "Agent said" against the referee: hidden tests of 69, mutants killed of 4 | "A run passes only with all 69 hidden tests and all 4 mutants. The referee-set mutants were never visible to the filters." |
| All results | slide 62, screen `4` | S4 row: run 3 0/3, 0/3; class round 0/1, 0/1 | "No measurable difference on this task with this model: both arms fail. In the class-profile round the bare arm claimed done with 68 of 69 hidden tests, the first such claim in the pilot's records." |

What the quiet run of `make show-4` showed (captured on 2026-10-17, run `ab-20261017-115138-c45d9d`;
your output will differ): minute 1, turn 1.15 tried to patch `app/services/errors.py` and screen 1
showed ⊘ blocked ("outside the allowed paths"); minute 3, turn 1.31 called `finish done` and the gate
ran with every pill ✓ (visible tests, existing tests, R1-R7, board, clean state); the harness set F4
`passes` with its evidence and moved the exec plan to completed; minutes 4-8, the test phase wrote one
test file and the filters ran (4 tests proposed, 1 kept: two discarded by filter 3, one by filter 2,
"failed on run 1 of 5: assert 422 == 412"); minute 9, the agent time limit ended the run
(`ABORTED: timeout`, exit 2) and "primary verdict ready: FAIL" came 9:19 after launch; the full
verdict 10:55 after launch: hidden tests 68/69, mutants 0/4, reviewer reject. Screen 2: "✓ only
own-org cards, no duplicates" and "CONFLICT DETECTED: tab B got HTTP 409". The gate passed while a
hidden test failed: the gate never sees the hidden tests. Cost: $0.0233 for the arm, $0.0032 for the
review.

Post hoc for S4 (VERIFICATION.md, exploratory rows "All bare" and "All harness", 34 runs per arm):
no done claim came with failing hidden tests in either arm (0 of 19 bare, 0 of 10 harness), and
harness arms shipped a median of 2.5 tests against 7.5. In runs 2 and 3 the F4 harness arm never
claimed done (0 of 6), so its verify gate never ran; in run 3 the agent time limit cut its test phase
in two A/Bs.

**Discussion (3:35-3:40).**
1. "What would a gate need to catch to earn its turns on this model?"
2. Transition: `submodules/04-verification/demo/README.md`; next, the final A/B launched at 2:55
   (terminal C, browser tab 4).

---

## Final results and wrap-up (3:40-4:00)

The final A/B was launched at 2:55, at the start of S4. This block walks through its finished results
and starts no run. It is the class's one live A/B and its measurement lesson: one A/B is one dot.

1. **3:40 The final A/B.** Terminal C: read the arm lines of each final feature and the session
   figure from the last `Cost:` line. Harness arm layers: all four. The final has no pre-registered
   primary measure, so `passed=True` on an arm line does not mean the feature works: read `hidden
   <x>/<total>` and `mutants <y>/<total>` (DESIGN §8.2; `final-project/README.md` §5.1). If two
   features ran, walk through the winner on the screens and give the second its arm lines.
2. **3:42 Console**, browser tab 4: screens `1`, `3`, `5`, both arms; `F` for one arm.
3. **3:46 Boards**, screen `2`.
4. **3:48 Screen 4 and all results.** Screen `4`: tonight's final next to the pilot's records. Say:
   "One A/B is one dot. Read it against the pilot's three dots per arm per run, never alone." Then
   the all-results slide for all four sections, wins and ties alike, with the post hoc table labelled
   post hoc. Show `Final:dots`. A1 warns that its own results should "not be assumed to generalize
   without similar investment" (A1, F-a-143); the same holds for this pilot: one model, one task per
   section, three runs per arm per run.
5. **3:53 Assignments**: A1 to A4 in `submodules/0N-*/assignment/README.md`; learner budget ≤ $6
   OpenAI and ≤ 400 LangSmith traces in total (DESIGN §11.5).
6. **3:56 Skills and the starter kit**: `skills/harness-setup`, `skills/assured-tests`,
   `skills/house-rules`, `skills/skill-template`; `uv run shipharness init --target <repo>` copies
   them with the kit (`docs/apply-to-your-repo.md`); show `Final:skill_template`.
7. **3:58 References**, then close.

**If a final A/B is not finished at 3:40.** Open its live screens in browser tab 4 (`1`, then `2`;
screen 1 shows "primary verdict ready" per arm as soon as it is known) and walk through them instead
of steps 2 and 3, then the all-results slide. If it is still running at 3:53, go to the wrap-up
slides and return to its screen `4` at the end. If an arm failed for a reason outside the experiment
(an arm `ERROR` from Docker, the network, or OpenAI), follow [Fallback: replay procedure](#fallback-replay-procedure)
with the recording of that feature from [fallbacks.md](fallbacks.md).

---

## Layer switch (not in the class plan)

`make demo-N LAYERS=-<layer>` reruns a section's A/B with one layer removed from the harness arm, A3's
method ("removing one component at a time", F-a-125). It is a full A/B at up to $0.48 and is not part
of the class plan. The pilot's leave-one-layer-out batch (M8 ablation) was not run, because the
pre-registered gate did not pass, so there are no ablation bars to show on screen `4`. Point to
`docs/after-class.md`, which has the command for learners.

---

## Fallback: known failure modes

Messages are copied from the code (file in the last column).

| Symptom (exact text) | Cause | In class | Source |
|---|---|---|---|
| `x missing     OPENAI_API_KEY         not set`, then `next step: OPENAI_API_KEY is missing: add it to .env at the repo root` (same for `LANGSMITH_API_KEY`); last line `result: x not ready (fix the items above)` | Key not in `.env` | Before class only: fill in `.env`, rerun `make doctor` | `src/shipharness/doctor.py` |
| `x invalid     OPENAI_API_KEY         OpenAI key invalid (rejected by OpenAI, <error class>, status <code>)`, then `next step: check OPENAI_API_KEY in .env (create a new key in your OpenAI account)` | Key revoked or wrong | Replace the key; until fixed, use the fallback recordings ([fallbacks.md](fallbacks.md)) | `src/shipharness/doctor.py` |
| `! unreachable OPENAI_API_KEY         could not reach OpenAI (<error class>)`, then `next step: check your network connection and retry` | Network | Check the network; a replay of a fallback recording needs no OpenAI calls | `src/shipharness/doctor.py` |
| `! warn        container runtime      docker not found: only the UNSANDBOXED fallback can run` | Docker not on PATH inside WSL | Start Docker Engine in Ubuntu (systemd: `sudo systemctl start docker`); do not run class commands unsandboxed | `src/shipharness/doctor.py`; DESIGN §9 |
| `make warm` ends with `warm: incomplete (<n> s)`, or a line starting `x images: build failed` or `x page-in failed` | An image build or a container start failed | `make images`, restart Docker, rerun `make warm` | `src/shipharness/ab/warm.py` |
| Arm status `ERROR` with `arm setup failed: RuntimeError: docker run failed: ...` | Docker daemon stopped, or image missing | `make images` if the image is missing; restart Docker; then replay the section's recording | `src/shipharness/ab/demo.py`, `src/shipharness/sandbox/docker.py` |
| Referee summary `...; referee could not judge the build: referee container did not start: ...` | Referee container failed to start; the run is kept | Rerun only the judging later with `make replay RUN=<id>`; continue with the recording now | `src/shipharness/ab/referee.py` |
| Screen 2: `No board screenshot yet (the preview container takes one every 5 s).` for the whole run | Board preview failed to start; display only | Carry on; the referee's board checks still run | `src/shipharness/ab/demo.py`, console template `boards.html` |
| Arm status `ABORTED: cap`, reason `cost cap reached: run $... of $0.20` (or `session $... of $2.50`) | A model call would exceed a cap | The run is judged and shown anyway; say so. If it is the session cap, stop live runs and use replays | `src/shipharness/cost/tracker.py`, `src/shipharness/runner/loop.py` |
| Arm status `ABORTED: timeout`, reason `agent time limit: RUN_TIMEOUT_S 300 s` or `harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during ...`; the command exits 2 | Agent or harness time budget used up | Judged and shown; say which clock ran out. Exit code 2 means an arm was aborted, not that the command broke (the class-profile round's F4 A/B exited 2 this way) | `src/shipharness/runner/loop.py`, `src/shipharness/ab/commands.py` |
| Arm status `ERROR`, error `OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).` | Key rejected mid-class | Replay the section; fix the key at the break | `src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI billing limit reached (quota or spend limit); add credit and retry.` | Account out of credit | Fallback recordings for the rest of the class | `src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI request kept failing after retries` | Repeated 429 or server errors | Replay the section | `src/shipharness/runner/loop.py` |
| A show-N run is much slower than the times above | A Fast-tier request can come back at the Standard tier; it is then charged Standard rates. `tail -n 20 .shipharness/ledger.jsonl` shows `"service_tier": "default"` instead of `"fast"` on those calls | Nothing to fix in class; the run is valid. Say the time and note it | `src/shipharness/cost/tracker.py`; `config/prices.toml` |
| `x <id> is a single-arm run (harness in action): the swap test needs both arms; pass the id of an A/B` | `make swap-N` on a show-N run | Swap tests apply to A/Bs only; the class plan runs none in S1 to S4 | `src/shipharness/ab/recorded.py` |
| `x <ab id> predates checkpoint SHA pinning: ...; run the A/B again` | Record without `checkpoint_sha` | Use a recording made after M5 (all fallbacks are) | `src/shipharness/ab/recorded.py` |
| `make replay` without `RUN`: `! replay needs RUN=<ab or run id>` | Missing argument | `make replay RUN=<id>` | `Makefile` |
| `x no recorded A/B for '<id>' under .shipharness/runs; check the A/B or run id` | Wrong id | Copy the id from [fallbacks.md](fallbacks.md) | `src/shipharness/ab/commands.py` |
| `make report` prints `! make report is not a make target in this release; use uv run shipharness experiments --help or uv run shipharness report --help` and exits 2 | `report` is not a make target in this release | Run `uv run shipharness report` | `Makefile`, `src/shipharness/ab/commands.py` |
| `make final` with no `FEATURES` runs F5, then F6 | Makefile default `FEATURES ?= F5,F6` | Always pass `FEATURES=` with the poll result. If the default does not match it, press Ctrl+C in terminal C at once and launch again with `FEATURES=` | `Makefile` |
| Console header shows `reconnecting` | The console server stopped or restarted | Check terminal A; restart `make console`; reload the page | `src/shipharness/console/static/stream.js` |
| Replay: screen 2 shows broken board images | Replay copies the diffs but not the `screenshots/` folder into the new run directory | See the workaround in [fallbacks.md](fallbacks.md) | `src/shipharness/ab/recorded.py` |
| Any screen shows `UNSANDBOXED — results not official` | `SANDBOX_MODE=none` | Not for class results; switch back to Docker | console template `_macros.html`; DESIGN §9 |

---

## Fallback: replay procedure

Full detail, recorded run ids, and what to say are in [fallbacks.md](fallbacks.md). Use it only
when a live run failed for a reason outside the experiment. Short form:

1. Say: "This run failed for a reason outside the experiment. I will show the recording made before
   class; the referee judges it live now."
2. Terminal B: `make replay RUN=<recorded id for this section>`.
3. Reload the runs list and open the newest `ab-...` entry: that is the replay. Every screen shows the
   red ● RECORDING badge.
4. The terminal ends with `RECORDING: replay <new ab id> of <recorded ab id> (<n> events)`, one result
   line per arm, and the cost line.

---

## After class

- `uv run shipharness report` (`make report` is still the placeholder): writes `exports/report.json`
  and `exports/report.html`; replays are excluded unless `--include-recorded`.
- Keep `.shipharness/runs/` and `exports/`: every class run is a dot and is never dropped (DESIGN §8.3
  rule 9).
- Write tonight's results into VERIFICATION.md: each command's run id and `Cost:` line, the session
  total from the last cost line, the launch-to-primary-verdict times from screen 1, and anything that
  failed with its exact message.
