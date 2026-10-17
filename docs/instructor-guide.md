# Instructor guide

Stage by stage, from the day before class to the Thursday review. Each stage lists the command, what
to check, the pass criteria, the expected time and cost, and what to do if it fails. Everything runs
inside the Ubuntu terminal of the class host (WSL2), in `~/shipharness`. Source ids such as
(A1, F-a-05) point to the References section of the [README](../README.md#17-references) (the
release also carries them as `REFERENCES.md`). Messages quoted here are copied from the code; the
full list of failure messages is in [troubleshooting.md](troubleshooting.md). Optional extras that
are not part of any demo section (replays of the pilot's real-mistake showcases, constructed
examples) are in [extras.md](extras.md).

Expected times and costs come from two sources, both on 2026-10-17 with the class profile after
`make warm`: the quiet runs of the class commands themselves (`make show-1` to `make show-4` and
`make final FEATURES=F5`, one command at a time on a quiet machine, `PURPOSE=pilot`), and the
class-profile round (one A/B per section, one at a time). Run ids are in the tables below.

Contents:

- [Before you start: the plan in one page](#before-you-start-the-plan-in-one-page)
- [Stage 1: T-1 day](#stage-1-t-1-day)
- [Stage 2: T-30 minutes](#stage-2-t-30-minutes)
- [Stage 3: Opening (0:00-0:10)](#stage-3-opening-000-010)
- [Stage 4: S1 Instructions (0:10-1:00)](#stage-4-s1-instructions-010-100)
- [Stage 5: S2 State and session lifecycle (1:00-1:50)](#stage-5-s2-state-and-session-lifecycle-100-150)
- [Stage 6: S3 Scope and sandbox (2:00-2:50)](#stage-6-s3-scope-and-sandbox-200-250)
- [Stage 7: S4 Verification, with the final launched (2:50-3:40)](#stage-7-s4-verification-with-the-final-launched-250-340)
- [Stage 8: Final block and wrap-up (3:40-4:00)](#stage-8-final-block-and-wrap-up-340-400)
- [Stage 9: After class](#stage-9-after-class)
- [Stage 10: Thursday review](#stage-10-thursday-review)
- [Replay procedure](#replay-procedure)

## Before you start: the plan in one page

### The story

- **Problem.** Teams hand features to coding agents. In a multi-tenant service the failures are
  specific: an endpoint returns one customer's data to another, a second session redoes or breaks
  the first session's work, the agent edits files it was never asked to touch, and its own tests
  pass while the behaviour is wrong.
- **Why it happens.** (1) "From the agent’s point of view, anything it can’t access in-context while
  running effectively doesn’t exist." (A1, F-a-05) (2) "each new session begins with no memory of
  what came before." (A2, F-a-08) (3) Agents copy existing patterns and can take actions that are
  hard to undo; no single source says this, so cite side by side: A1 on pattern copying (F-a-20), A4
  running the agent "in a container, not your actual machine" and the `pkill -9 bash` incident
  (F-a-18, F-a-19), A5's file operations "restricted to the project directory only" (F-a-86), and
  A6 as supplementary (F-a-21). (4) "agents reliably skew positive when grading their own work"
  (A3, F-a-15), and visible tests miss what held-out tests catch (B13, F-b-45, F-b-50).
- **Solution.** A harness, the environment around the agent. A1 describes the work as "design
  environments, specify intent, and build feedback loops" (A1, F-a-02); A1 does not define
  "harness engineering", so no definition is attributed to it. Four parts, taught as course
  sections S1 to S4, plus the sandbox.
- **The claim.** A harness encodes assumptions about the model; measure each piece, keep what earns
  its place. A3: "every component in a harness encodes an assumption about what the model can't do
  on its own, and those assumptions are worth stress testing" (A3, F-a-124); A3's method is
  "removing one component at a time and reviewing what impact it had on the final result." (A3,
  F-a-125). "Keep what earns its place" is course framing.
- **How we measure it.** Same agent, model, effort, task, repository, tools, sandbox, turn limit,
  and cost cap, with and without the harness, judged by the same referee on what ships. One primary
  measure per section, registered before any run.
- **What the course pilot found.** In pilot runs 3 (effort medium) and 4 (effort low) and in the
  class-profile round, no section showed the harness arm ahead on its primary measure: "no
  measurable difference on this task with this model" for S1 to S4 (S4: both arms fail). The
  pre-registered gate for the larger experiment batches therefore did not pass, and those batches
  were not run. The class shows this result in every section; the harness does not have to win.

The labels S1 to S4, R1 to R7, "layer", "house rules", filters 4 and 5, and "trap" are course
labels. Introduce each one as such: "house rules" is the course's label for what A1 calls "golden
principles" and "taste invariants" (A1, F-a-96, F-a-99); filters 4 and 5 are course filters with no
direct source; the forced session stop is a session turn budget that produces A3's "context reset"
(A3, F-a-65).

### The class plan per section

Every demo section is live. S1 to S4 run **harness in action** (`make show-N`: the harness arm
alone, live, with the live referee checks and the live console; not an A/B). No section has a
measured gap, so none runs a live A/B (`make demo-N`). The final runs `make final`, the class's one
live A/B and its measurement lesson. Recorded showcases and constructed examples are optional extras
([extras.md](extras.md)), never part of a demo block; a replay of a recording is the emergency
fallback only ([Replay procedure](#replay-procedure)). Every section ends on one slide and one
console view (screen `4`) that show every result.

| Section | Live command | Layers in the harness arm |
|---|---|---|
| S1 | `make show-1` | instructions (F1) |
| S2 | `make show-2 SESSION_BUDGET=12,38` | instructions and state (F2, sessions of 12 and 38 turns) |
| S3 | `make show-3` | instructions, state, scope (F3) |
| S4 | `make show-4` | all four (F4) |
| Final | `make final FEATURES=<poll winners>` | both arms, all four layers in the harness arm (one live A/B per feature) |

The fallback recordings need their run directories under `.shipharness/runs/` on the class host.
They are not part of the repository: record them on T-1 or copy them from the machine that made them
(stage 1).

### All results: the slide and screen 4

Primary measure passed, bare / harness:

| Section | Pilot run 3, effort medium (k=3) | Pilot run 4, effort low (k=3) | Class-profile round (k=1) |
|---|---|---|---|
| S1 F1, legacy-pattern ticket | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-084558-0356a0`) |
| S2 F2, session budget 12 then 38 turns | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-085139-7c0661`) |
| S3 F3, tempting-middleware ticket | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-090051-91f837`) |
| S4 F4, canonical ticket | 0/3, 0/3 | not run | 0/1, 0/1 (`ab-20261017-090903-926c02`) |

Run 3 A/Bs: F1 `ab-20261016-211419-07937b`, `-212745-2c14fb`, `-214636-c8b3c4`; F2 `-211419-dfe06f`,
`-213317-9a0ec1`, `-214959-de790f`; F3 `-212115-a361f5`, `-213624-d7eb13`, `-215443-f2c188`; F4
`-212252-aa1644`, `-214151-ca9841`, `-220010-c5b4bf`. Run 4 A/Bs: F1 `ab-20261016-232842-b372c2`,
`-233807-3f34fa`, `-234639-4a18bd`; F2 `-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9`; F3
`-233517-2c9ea4`, `-234509-8b9bfa`, `-235305-723a0f`. F4 had no run 4: the pilot's run cap was
reached.

Post hoc (chosen after the results; descriptive; 34 arm runs per arm over pilot runs 2-4 and the live
console check `ab-20261016-210339-909651`): files changed outside the allowed paths in 9 bare runs
(F4 6 of 6, F2 3 of 9) and 0 harness runs; done claimed in 19 bare and 10 harness runs, none with
failing hidden tests; tests shipped, median 7.5 bare and 2.5 harness; arm wall time, median 190 s and
302 s; agent time limit hit in 4 and 9 runs; cost per arm, median $0.0103 and $0.0123. The scope
layer runs only in the F3 and F4 stacks, so F2's 0 of 9 is not its doing. Label this table "post hoc"
whenever you show it.

### Schedule (240 minutes)

| Block | Minutes | Content |
|---|---|---|
| Opening | 10 | The four failures (3), why it happens (2), the harness and the claim (2), shipharness, TeamTrack, console tour, what the pilot found, `harness-setup` assessment (3) |
| S1 Instructions | 50 | Poll 3, launch `make show-1` 2, concepts 15, walkthrough 10 (the run goes on meanwhile; at section minute 25 check terminal B for the `Cost:` line), demo block 15 (harness in action 10, reading the result 3, all results 2), discussion 5 |
| S2 State and session lifecycle | 50 | Same pattern with `make show-2 SESSION_BUDGET=12,38` |
| Break | 10 | |
| S3 Scope and sandbox | 50 | Same pattern with `make show-3` |
| S4 Verification | 50 | S4 poll 3, final feature poll 1, launch `make show-4` and, a minute later, `make final FEATURES=...` in a second terminal 2, concepts 14, walkthrough 10, demo block 15, discussion 5 |
| Final and wrap-up | 20 | Results of the final A/B launched in S4, no new run: all screens, screen 4 next to the pilot's dots, the all-results slide, assignments, skills and the starter kit, references |

### Section pattern

1. **Poll (section minutes 0-3).** One sentence on the feature and the rule at risk, then the poll:
   the room predicts the pilot's result for the section. Close it before the launch.
2. **Launch (3-5).** Terminal B: `make show-N`. Reload the console's run list, open the newest
   `ab-...`, stay on screen `1` while the container starts. Say: "This is the harness arm alone. It is
   not an A/B; the A/B results come at the end of the section."
3. **Concepts (5-20)** and **walkthrough (20-30)** while the run goes on. At section minute 25, look
   at terminal B for the `Cost:` line.
4. **Demo block (30-45).** Harness in action (10 minutes): screens `1`, `3`, `2`, and `5` of the
   finished show-N run. Reading the result (3): show-N's verdict on screen `1` and the session figure
   on the `Cost:` line. All results (2): the slide row and screen `4`.
5. **Discussion (45-50).**

At most two runs at a time: in S4, show-4 and the final run together.

### Windows on the screen

| Window | Content |
|---|---|
| Terminal A | `make console` (leave it alone) |
| Terminal B | `make show-N`, large font (`make replay` only as the emergency fallback) |
| Terminal C | `make final` only, from the S4 launch to the final block |
| Browser tab 1 | Slides |
| Browser tab 2 | Console: run list at http://127.0.0.1:8765/, then the current run at `/run/<id>` |
| Browser tab 3 (optional) | LangSmith, project `shipharness-class-<date>` |
| Browser tab 4 | Console: the final A/B, opened at the S4 launch |

### Console keys

| Key | Screen | Shows |
|---|---|---|
| `1` | Live Console | Per arm: container line (id, network, CPU, memory, time left), cost against the run cap, turns (the last 8 while running; the full scrollable timeline once the run has finished), harness decisions, gate pills, "Agent said" vs "Referee", and the `primary verdict ready` pill with the time from launch to the primary verdict |
| `2` | Boards | Each arm's board as an Acme user, a screenshot every 5 s, with `⚠ other org` and `⧉ duplicate` marks; in S4 a two-tab edit conflict panel |
| `3` | Evidence | Files read and sessions; diff map and sandbox denials; referee checks, test-filter table, mutant table |
| `4` | A/B Report | One row per feature, variant, and arm, one dot per run from `exports/scores/`; records made by an older referee version and harness-in-action runs are counted and left out |
| `5` | Traces | Live tail, first wrong turn per arm (a heuristic, labelled as such), trace links |
| `F` | | Cycles full screen: both arms, bare, harness |

`make show-N` prints the run id only at the end. While it runs, reload the run list and open the
newest `ab-...` (ids start with a time stamp). The run list does not refresh by itself.

### What the terminal prints at the end of a run

One line `A/B <id> (<feature>, layers=[...], profile=class)`, with `, harness in action` added for
`make show-N`; then one line per arm with status, claim, primary measure, `passed=`, hidden tests
passed of total, mutants killed of total, reviewer verdict, and cost (`_print_record` in
`src/shipharness/ab/commands.py`); then the cost line
`Cost: $<this command> (this command: <model costs>; session $<x> of $2.50; build ...)`. Read the
session figure aloud in each demo block. The exit code is 0 when every arm completed, 2 when an arm
was aborted (cost cap or time limit), 1 when an arm ended in `ERROR`.

### Caps and the class budget

From `.env.example` and `src/shipharness/config/settings.py`:

| Cap | Value |
|---|---|
| Per arm per run, build and test phases together (`MAX_RUN_COST_USD`) | $0.20 |
| Per arm per final run (`MAX_FINAL_RUN_COST_USD`) | $0.25 |
| Per blinded review (`MAX_REVIEW_COST_USD`) | $0.04 |
| Per command (`MAX_BATCH_COST_USD`) | $2.50 |
| Per class session, every command under one `SHIPHARNESS_CLASS_DATE` (`MAX_SESSION_COST_USD`) | $2.50 |
| Agent time per arm per run (`RUN_TIMEOUT_S`) | 300 s |
| Harness work per arm per run (`HARNESS_TIMEOUT_S`) | 120 s |

At the caps, one `make show-N` costs at most $0.20 + $0.04 = $0.24 and one final feature at most
2 × $0.25 + 2 × $0.04 = $0.58. Four show-N runs and two final features reach at most $2.12, under the
$2.50 session cap. `make warm` makes no model calls.

The class profile (`PROFILE=class`, the default of `make show-N`, `make demo-N`, and `make final`)
runs both arms identically at reasoning effort `low`, with 2 CPUs per arm and referee container, and
sends the agent's model calls at OpenAI's Fast tier. Fast costs twice the Standard rate per token for
gpt-6-luna (`config/prices.toml`: $0.20 input, $0.02 cached input, $0.25 cache write, $1.00 output
per 1M tokens, against $0.10, $0.01, $0.125, $0.50). Each call is charged by the tier the response
reports, so a Fast request that comes back at the Standard tier costs the Standard rate. The reviewer
keeps its own settings and the Standard tier. The caps are unchanged.

Measured in the class-profile round (agents at the Fast tier, every call reported `fast`; review
costs from the score records, field `review_cost_usd`):

| Section | A/B | Bare arm $ | Harness arm $ | Review $ (bare, harness) |
|---|---|---|---|---|
| S1 F1 | `ab-20261017-084558-0356a0` | 0.0122 | 0.0151 | 0.0028, 0.0028 |
| S2 F2 | `ab-20261017-085139-7c0661` | 0.0329 | 0.0357 | 0.0036, 0.0041 |
| S3 F3 | `ab-20261017-090051-91f837` | 0.0120 | 0.0135 | 0.0021, 0.0031 |
| S4 F4 | `ab-20261017-090903-926c02` | 0.0217 | 0.0257 | 0.0038, 0.0040 |

The four A/Bs cost $0.1953 in total (agents $0.1689, reviews $0.0263). A call that would cross a cap
is refused, the run ends as `ABORTED: cap`, and the referee still judges it.

## Stage 1: T-1 day

| | |
|---|---|
| **Commands** | `make doctor`; set `SHIPHARNESS_CLASS_DATE=<class day, YYYY-MM-DD>` in `.env`; `make warm`; record the fallbacks (below) |
| **What to check** | Every `make doctor` line starts with `+ ok`; both key lines say `accepted by OpenAI` / `accepted by LangSmith`; `git tag -l 'm1-*'` lists nine tags; `.env` holds the class date; `make warm` ends with `warm: done (<s> s)`; `ls .shipharness/runs/<id>/ab.json` for each fallback recording |
| **Pass criteria** | Last doctor line `result: + ready`; `warm: done`; one fallback recording per section and per final feature, each replayed once |
| **Expected time and cost** | `make doctor`: seconds, $0 (lists models, no tokens). `make warm`: 407 s on the first run in the class-profile round (images rebuilt 145 s, 7 referee and 4 gate baselines), 1.2 s on the second run; $0. Recordings: at most $0.24 per show-N and $0.58 per final feature at the caps; class-round costs in the table above. Replays without the reviewer: $0 |
| **If it fails** | A key line `x invalid`: replace the key and rerun `make doctor`. `docker not found`: `sudo systemctl start docker`. `warm: incomplete` or a line starting `x`: `make images`, then `make warm` again. A recording ends in `ERROR` for an infrastructure reason: keep it, list it, and record the next complete run as well |

**What `make warm` does.** It runs `uv run shipharness warm --profile class`: it rebuilds the images
through `make images` only if their source changed, starts and removes one container per image so
the images are paged in, and computes and caches the referee baseline of every class task and the
gate baseline of every task with the verify layer. It prints one line per step with its time and
ends with `warm: done (<s> s)` or `warm: incomplete (<s> s)` (`src/shipharness/ab/warm.py`). It
makes no model calls and is safe to rerun. Run it after any change to `sandbox/Dockerfile` or
`src/`, and again on the class day.

**Recording the fallbacks.** A fallback is a normal run directory under `.shipharness/runs/` plus its
score records in `exports/scores/`. Record on T-1, not on the class day, and with `PURPOSE=pilot`, so
the recordings neither use the class session cap nor appear in the class LangSmith project:

```bash
make show-1 PURPOSE=pilot
make show-2 SESSION_BUDGET=12,38 PURPOSE=pilot
make show-3 PURPOSE=pilot
make show-4 PURPOSE=pilot
make final FEATURES=F5 PURPOSE=pilot
make final FEATURES=F6 PURPOSE=pilot
make final FEATURES=F7 PURPOSE=pilot
```

Every `PURPOSE=pilot` command shares one cost session named `pilot`, capped at
`MAX_SESSION_COST_USD` ($2.50) across all pilot-purpose commands ever run on this machine. Read the
session figure on each cost line before the next recording; if it would not cover the next command
at its caps, record the final features first.

The course's own runs of these commands on a quiet machine, with the class profile (2026-10-17;
your ids will differ):

GUIDE_QUIET

Rules for recordings: the fallback for a section is the first complete run recorded, whatever its
result; re-running until a result looks better is forbidden. For each recording, note the id (first
line of the result output) and the arm statuses, then:

```bash
make replay RUN=<id> PURPOSE=pilot   # no model calls without the reviewer; shows RECORDING
mkdir -p ~/shipharness-fallbacks && cp -a .shipharness/runs/<id> ~/shipharness-fallbacks/
```

Also copy the score records (`exports/scores/<run id>.json`; the run ids are in `ab.json` under
`arms.<arm>.spec.run_id`) into the same backup folder.

## Stage 2: T-30 minutes

| | |
|---|---|
| **Commands** | `make doctor`; `make warm`; `make console` in terminal A; open http://127.0.0.1:8765/; `ls .shipharness/runs/<id>/ab.json` for each recording; print the sandbox policy (command below); run the assessment (command below); open the slides |
| **What to check** | Doctor ready; `warm: done`; the console prints `Console: http://127.0.0.1:8765/`, and the browser shows the run list and the key legend; every `ab.json` exists; the policy printout starts with `Sandbox policy (identical for both arms)`; the assessment prints a summary per area |
| **Pass criteria** | All of the above; `SHIPHARNESS_CLASS_DATE` in `.env` is today |
| **Expected time and cost** | About 10 minutes; `make warm` 1.2 s when nothing changed since T-1 (class-profile round); $0 (no model calls) |
| **If it fails** | `warm: incomplete`: `make images`, then `make warm`. Console port taken: `make console CONSOLE_PORT=8766`. A recording missing: restore it from `~/shipharness-fallbacks/` to the same paths |

Do not run any `make show-N` or `make final` before class on the class day: every command under the
class date shares the $2.50 session cap.

```bash
uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'
uv run python skills/harness-setup/scripts/assess.py teamtrack --out .shipharness/harness-assessment.html
```

The policy printout, captured on 2026-10-17 from the first command above at commit 5e8fb08; your
output will differ. It shows the settings as loaded (`SANDBOX_CPUS=1.0` in `.env.example`); the class
profile raises the CPU limit to 2 for class runs:

```
Sandbox policy (identical for both arms)
  network: none
  cpus: 1.0
  memory: 1024 MB (swap: 0 MB)
  pids: 256
  user: 1000:1000
  read-only root: yes
  writable: /work, /tmp
  capabilities dropped: ALL
  tool timeout: 120 s; run timeout: 300 s
  refused commands: 6 rules (network access)
```

The assessment of the bare TeamTrack begins (captured on 2026-10-17 from the second command above at
commit 5e8fb08; your output will differ):

```
Instructions       pass 0  partial 1  fail 5
State              pass 0  partial 0  fail 4
Scope              pass 1  partial 1  fail 3
Verification       pass 1  partial 1  fail 3
Session lifecycle  pass 0  partial 0  fail 5
```

## Stage 3: Opening (0:00-0:10)

| | |
|---|---|
| **Commands** | Console tab: press `1` to `5` once each; editor: `Opening:two_arms` (`src/shipharness/ab/demo.py`) and `Opening:publish` (`src/shipharness/events/bus.py`), one minute each; terminal B: `make doctor`; terminal B: the assessment from stage 2 |
| **What to check** | The problem slide names the four failures and that the referee checks every run for them; the "how we measure it" slide states the pre-registered outcome rule |
| **Pass criteria** | Doctor ready on screen without any part of a key shown; the assessment shows the gaps of the bare TeamTrack |
| **Expected time and cost** | 10 minutes; $0 |
| **If it fails** | Doctor shows `x`: say so, fix it at the break, and use the fallback replays for the affected part ([Replay procedure](#replay-procedure)) |

There is no recorded board with leaked cards to show: in pilot runs 2, 3, and 4 and the live console
check, no bare F1 arm shipped a new tenant-isolation violation, and in the class-profile round no arm
leaked another org's cards. Say so. No real run produced ⚠ marks; an optional constructed example
that shows them is in [extras.md](extras.md), outside the class flow.

Say during the assessment: "This is what the bare arm works with: no map, no progress file, no
feature list. The harness arm gets those parts; the rules themselves are in both." Every rule is also
in `docs/HANDBOOK.md` of the bare arm's repository.

To show an anchor's code: `uv run python scripts/anchors.py extract Opening:two_arms`.

## Stage 4: S1 Instructions (0:10-1:00)

`make show-1` runs feature F1, org-wide issue search (`GET /issues`), canonical ticket, from
checkpoint `m1-s1-start`, one session of 30 turns (`teamtrack/reference/f1/task.toml`), with the
instructions layer. Rule at risk: R1 tenant isolation. The legacy `GET /v1/issues` handler has no
tenant filter and sits next to the right pattern; A1 reports that agents copy existing patterns (A1,
F-a-20). Primary measure: one or more new R1 violations fails the run. The assumption the map
encodes: the model will not apply a rule it has not been pointed to (course wording).

| | |
|---|---|
| **Commands** | 0:13 `make show-1`; 0:30-0:40 anchors `S1:agents_md`, `S1:progressive`, `S1:prefix`; 0:35 check terminal B for the `Cost:` line; 0:40-0:53 demo block on the finished run |
| **What to check** | At launch: the first harness decision lists the placed instruction files. Demo block: screen `1` timeline (the map and the documents it points to read before the code); screen `3` "Files read" by category and the R1 line; screen `2` the board ("✓ only own-org cards"); screen `5` the trace links |
| **Pass criteria** | show-1 prints its arm line and a `Cost:` line before 0:35 |
| **Expected time and cost** | Quiet run of `make show-1` (2026-10-17, run `ab-20261017-112101-c5d839`): primary verdict 4:11 and full verdict 10:00 after launch, 10 min 14 s for the whole command; $0.0179 for the arm plus $0.0019 for the review. Class-profile round, harness arm of `ab-20261017-084558-0356a0`: 114 s and 324 s; $0.0151 plus $0.0028. At most $0.24 at the caps |
| **If it fails** | Still running at 0:35: finish the walkthrough, then open the demo block on screens `1` and `3` of the running show-1; screen `1` shows `primary verdict ready` as soon as it is known. An arm `ERROR` from Docker, the network, or OpenAI: [Replay procedure](#replay-procedure) with the S1 fallback recording. An unwelcome result is a result: show it |

Say at the result: "This is one harness arm on one run. It tells us the layer ran; it cannot tell us
the layer helped." At the results: S1 row, "no measurable difference on this task with this model".
Discussion: "The bare arm could read the same rules, and applied them. What would have to be true of
a model or a ticket for the map to earn its place?" (A1, F-a-05).

## Stage 5: S2 State and session lifecycle (1:00-1:50)

`make show-2 SESSION_BUDGET=12,38` runs feature F2, comments on issues, from `m1-s2-start`, with the
instructions and state layers, in two sessions of 12 and 38 turns (the pilot's lever; the task's own
budget is 20 and 30, `teamtrack/reference/f2/task.toml`): session 1 stops after 12 turns, the arm
gets the wrap-up turns (`WRAPUP_TURNS`, default 3) and the resume sentence. Primary measure: continuity failure (R7 fails, a second migration creates the same table,
or at least 30% of session 1's added lines are removed in session 2). The assumption the state files
encode: a fresh session cannot pick up the work from the repository alone (A2, F-a-08; one-line form
is the course's). Since 2026-10-17 the runner rule for both arms is: before the last build session,
`finish(claim="not_done")` ends only that session.

| | |
|---|---|
| **Commands** | 1:03 `make show-2 SESSION_BUDGET=12,38`; 1:20-1:30 anchors `S2:init`, `S2:stop_resume`, `S2:write`; 1:25 check terminal B for the `Cost:` line; 1:30-1:43 demo block on the finished run |
| **What to check** | At launch: the first decision is the initializer step (`init.sh`, `progress.md`, `session-handoff.md`, the exec plan). Demo block: screen `1` `■ Session 1 stopped` and `▶ Session 2 resumed`; screen `3` "Sessions" (turns, how each ended, `↺ redone` files) and the state files in "Files read"; screen `2` the board ("✓ only own-org cards, no duplicates"); screen `5` the first wrong turn |
| **Pass criteria** | `Cost:` line before 1:25 |
| **Expected time and cost** | Quiet run of `make show-2 SESSION_BUDGET=12,38` (2026-10-17, run `ab-20261017-113213-fe89a3`): primary verdict 6:46 and full verdict 9:52 after launch, 10 min 7 s for the whole command, exit 2 (session 2 hit the agent time limit); $0.0268 for the arm plus $0.0027 for the review. Class-profile round, harness arm of `ab-20261017-085139-7c0661`: 358 s and 533 s; $0.0357 plus $0.0041. At most $0.24 at the caps |
| **If it fails** | As S1, with the S2 fallback recording |

Say at the result: "Before change 14, a `finish(not_done)` at the end of session 1 ended the build
phase; now it ends only that session, in both arms." At the results:
"No measurable difference on this task with this model; the measure cannot fail when session 1
leaves nothing to redo: 6 of the 12 F2 arms of runs 3 and 4 built nothing." Discussion: "Which state
file would you keep for this model, and how would you measure it?"


## Stage 6: S3 Scope and sandbox (2:00-2:50)

`make show-3` runs feature F3, idempotency keys on issue creation, from `m1-s3-start`, a build phase
then a test phase (`teamtrack/reference/f3/task.toml`), with the instructions, state, and scope
layers. The shared middleware in `app/api/middleware.py` is off-limits and easier to change. Primary
measure: one or more out-of-scope files in the shipped diff, or one or more source files changed
during the test phase. The scope layer enforces this measure, so the harness arm's zero is expected by
construction.

| | |
|---|---|
| **Commands** | 2:03 `make show-3`; 2:20-2:30 anchors `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile`; 2:25 check terminal B for the `Cost:` line; 2:30-2:43 demo block on the finished run, with the sandbox moment |
| **What to check** | At launch: the sandbox line (container id, `network none`, CPU, memory, time left). Demo block: screen `1` harness decisions `⊘ block` / `↺ revert` with the reason the agent read, if any; screen `3` diff map and "Sandbox denials" |
| **Pass criteria** | `Cost:` line before 2:25 |
| **Expected time and cost** | Quiet run of `make show-3` (2026-10-17, run `ab-20261017-114259-b64f54`): primary verdict 4:25 and full verdict 7:31 after launch, 7 min 43 s for the whole command; $0.0142 for the arm plus $0.0030 for the review; no blocked edit and no sandbox denial. Class-profile round, harness arm of `ab-20261017-090051-91f837`: 317 s and 481 s; $0.0135 plus $0.0031. At most $0.24 at the caps |
| **If it fails** | As S1, with the S3 fallback recording |

Sandbox moment: if screen `3` lists a denial, show its reason code (`network`,
`write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and the command. If
none occurred, show the policy printout from stage 2 and say that no A/B in pilot runs 3 and 4 or the
class-profile round had a sandbox denial. Say: "The sandbox is the same for both arms. It is taught
here, but it is never the variable." At the results: "The clearest post hoc difference was on F4,
where scope was not the primary measure: bare arms left scope in 6 of 6 runs, harness arms in 0 of 6
(descriptive, not tested)."

## Stage 7: S4 Verification, with the final launched (2:50-3:40)

`make show-4` runs feature F4, optimistic concurrency (ETag, If-Match) and issue history, from
`m1-s4-start`, one session of 40 turns (`teamtrack/reference/f4/task.toml`), with all four layers.
Two co-primary counts per run: hidden tests passed (of 69) and referee-set mutants killed by the
arm's shipped tests (of 4, `teamtrack/mutants/features/f4.jsonl`). The blinded reviewer runs on the
diff.

| | |
|---|---|
| **Commands** | 2:50 S4 poll; 2:53 final feature poll (F5 bulk close, F6 watchers, F7 labels); 2:54 terminal B `make show-4`, opened in browser tab 2; 2:55 terminal C `make final FEATURES=<winner>,<runner-up>`, opened in browser tab 4; 3:10-3:20 anchors `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate`; 3:15 check terminals B and C for their `Cost:` lines; 3:20-3:33 demo block on the finished show-4 |
| **What to check** | Always pass `FEATURES`: the Makefile default is `F5,F6`. At 3:15: show-4's `Cost:` line in terminal B; in terminal C the first final feature's lines, or nothing yet (both are fine). Demo block: screen `1` gate pills or the test phase, and the `primary verdict ready` pill; screen `3` filter table, mutant table, referee counters, reviewer verdict; screen `2` the board and the two-tab conflict panel |
| **Pass criteria** | show-4 finished before 3:20; at most two runs at once (show-4 and the final) |
| **Expected time and cost** | S4_TIME |
| **If it fails** | show-4 as S1, with the S4 fallback recording. If show-4 is not finished at 3:15, open the demo block on its live screens. Wrong `FEATURES` started: Ctrl+C in terminal C at once and launch again. A final arm `ERROR` for an infrastructure reason: note it and use the final's fallback recording in stage 8 |

**Both final features fit.** `make final` runs its features one after another, so a second feature
starts only when the first prints its `Cost:` line. At the caps, show-1 to show-4 and two final
features need at most $2.12, under the $2.50 session cap. Check the session figure on show-3's cost
line: two features fit while it is at most $1.10 (show-4 $0.24 plus two features $1.16, at the caps);
otherwise run the winner only.

Launching show-4 and the final together keeps every cap: before each call the tracker reserves the
call's worst case under one lock and reads the calls the other command added to the shared ledger.

Say at the filter table: "Filters 1 to 3 are TestGen-LLM's (B11, F-b-16 to F-b-22); 4 and 5 are
course filters. Filter 2 re-runs each test five times, TestGen-LLM's 'every one of five executions'
(B11, F-b-19)." At the results: "In pilot runs 2 to 4 no done claim came with failing hidden tests
(0 of 19 bare, 0 of 10 harness, post hoc); the class-profile round's bare arm on F4 was the first, at
68 of 69." Discussion: "What would a gate need to catch to earn its turns on this
model?" (A4, F-a-17).

## Stage 8: Final block and wrap-up (3:40-4:00)

The final A/B was launched at 2:55. This block walks through its results and starts no run. It is
the class's one live A/B: one A/B is one dot, read against the pilot's results, never alone.

| | |
|---|---|
| **Commands** | 3:40 terminal C: read the arm lines and the session figure; 3:42 browser tab 4: screens `1`, `3`, `5`, `F` for one arm; 3:46 screen `2`; 3:48 screen `4`, then the all-results slide; show `Final:dots`; 3:53 assignments; 3:56 skills, the starter kit, and `Final:skill_template`; 3:58 references |
| **What to check** | F5-F7 have no primary measure, so `passed=True` on a final arm line does not mean the feature works: read `hidden <x>/<total>` and `mutants <y>/<total>` |
| **Pass criteria** | Both arms of at least one final feature judged and shown |
| **Expected time and cost** | 20 minutes; no new model calls. The final's own time and cost, measured with the class profile, are below the table |
| **If it fails** | Final not finished at 3:40: walk through its live screens `1` and `2` (screen 1 shows `primary verdict ready` per arm as soon as it is known), then the all-results slide; return to its screen `4` at the end. An arm `ERROR` outside the experiment: [Replay procedure](#replay-procedure) with the recorded final |

GUIDE_FINAL

`make report` is a placeholder target in this release (it prints
`! report is available after milestones M6 and M8`); use `uv run shipharness report` after class. Its
dot plots cover F1-F4 (features with a primary measure); it draws none for F5-F7.

Close the results with A1's caveat about its own results, which applies to the pilot as well: they
should "not be assumed to generalize without similar investment" (A1, F-a-143). The pilot measured
one model, one task per section, and three runs per arm per run.

Assignments: four briefs in `submodules/0N-*/assignment/README.md`; the learner budget is at most $6
of OpenAI usage and 400 LangSmith traces in total. Skills to take home: `skills/harness-setup`,
`skills/house-rules`, `skills/assured-tests`, `skills/skill-template`. The starter kit copies them,
with the AGENTS.md map and the session files, into a learner's repository:
`uv run shipharness init --target <repo>` ([apply-to-your-repo.md](apply-to-your-repo.md)).

## Stage 9: After class

| | |
|---|---|
| **Commands** | `uv run shipharness report`; back up `.shipharness/runs/` and `exports/`; note the session total from the last cost line |
| **What to check** | `exports/report.html` includes tonight's final; show-N runs are single-arm and stay out of the A/B report; every class run is kept, including aborted ones |
| **Pass criteria** | Tonight's results written down: each command's run id, `Cost:` line, the launch-to-primary-verdict times from screen 1, the session total, and any failure with its exact message |
| **Expected time and cost** | 15 minutes; $0 |
| **If it fails** | A run is missing from the report: check that `exports/scores/` holds its records; replays are left out unless `--include-recorded` |

## Stage 10: Thursday review

Two hours: about 25 minutes per assignment (expected approach 5, solution walkthrough 8, common
mistakes 5, discussion 7), then 20 minutes of open questions. The hidden scripted diffs of
assignment 3 are revealed in its block.

| | |
|---|---|
| **Commands** | Before the session, in the private build repository (the graders are not in the learner repository, where the target stops with `no grader for assignment N: graders are private (build repository only)`): `make grade-assignment-N SUBMISSION=<folder or git URL>` for each submission and each N; collect the score per criterion |
| **What to check** | Each grader also runs on the reference solution before the session, so the expected scores are known |
| **Pass criteria** | A score per submission and per criterion, used as counts in the "common mistakes" part |
| **Expected time and cost** | Grading makes no model calls; the session is 2 hours |
| **If it fails** | `! grade-assignment-N needs SUBMISSION=<folder or git URL>`: pass the folder or URL |

| Time | Item |
|---|---|
| 0:00-0:25 | Assignment 1, Instructions |
| 0:25-0:50 | Assignment 2, State and session lifecycle |
| 0:50-1:15 | Assignment 3, Scope and sandbox, with the hidden-diff reveal |
| 1:15-1:40 | Assignment 4, Verification and portfolio |
| 1:40-2:00 | Open questions |

Before the session, tally the grader output: for each criterion, how many submissions lost points,
and the most common message. Use those counts, not impressions, in each "common mistakes" slot.

Reveal for assignment 3: show one hidden diff at a time with the phase it was replayed in; ask
"reject or accept, and why?"; take two or three answers before the expected verdict; show how many
submissions got it wrong, as a count; pair a rejected diff with the closest legitimate one to show
where a false positive comes from.

The solutions are not in the repository before the review. They are released as a tagged release
after the review session.

## Replay procedure

Use a replay only when a live run failed for a reason outside the experiment (Docker, the network,
OpenAI errors, time). A live run that the harness arm "lost" is a result, not a failure. The replay
is never part of a demo block.

1. For a failed live run, say: "This run failed for a reason outside the experiment. I will show the
   recording made before class; the referee judges it live now."
2. Terminal B: `make replay RUN=<recorded id>` (an A/B id or a run id; single-arm show-N recordings
   replay the same way).
3. Reload the run list and open the newest `ab-...`: that is the replay, under a new id. Every screen
   shows the red `● RECORDING` badge. The recorded events arrive at once; the referee then judges the
   recorded diffs live.
4. The terminal ends with `RECORDING: replay <new ab id> of <recorded ab id> (<n> events)`, one line
   per arm, and the cost line.

Screen `2` of a replay shows broken images, because the replay copies the diffs but not the
screenshots. Fix it once the replay's directory exists, then reload the page:

```bash
cp -a .shipharness/runs/<recorded ab id>/screenshots .shipharness/runs/<replay ab id>/
```

If Docker itself is down, a replay cannot run (the referee needs a container). Last resort: open the
recording directly at `http://127.0.0.1:8765/run/<recorded ab id>`. These are the original events, so
there is **no** RECORDING badge: put up the "recorded before class" slide and say it before switching
screens. Never switch to `SANDBOX_MODE=none` for class results.
