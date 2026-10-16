# Instructor guide

Stage by stage, from the day before class to the Thursday review. Each stage lists the command, what
to check, the pass criteria, the expected time and cost, and what to do if it fails. Everything runs
inside the Ubuntu terminal of the class host (WSL2), in `~/shipharness`. Source ids such as
(A1, F-a-05) point to [REFERENCES.md](../REFERENCES.md). Messages quoted here are copied from the
code; the full list of failure messages is in [troubleshooting.md](troubleshooting.md).

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
- **How we prove it.** Same agent, model, effort, task, repository, tools, sandbox, turn limit, and
  cost cap, with and without the harness, judged by the same referee on what ships, shown live,
  next to pre-run experiments.

The labels S1 to S4, R1 to R7, "layer", "house rules", filters 4 and 5, and "trap" are course
labels. Introduce each one as such: "house rules" is the course's label for what A1 calls "golden
principles" and "taste invariants" (A1, F-a-96, F-a-99); filters 4 and 5 are course filters with no
direct source; the forced session stop is a session turn budget that produces A3's "context reset"
(A3, F-a-65).

### Schedule (240 minutes)

| Block | Minutes | Content |
|---|---|---|
| Opening | 10 | Problem with a real failure on the board (3), why it happens (2), the harness: four parts and the sandbox (2), shipharness, TeamTrack, console tour, `harness-setup` assessment (3) |
| S1 Instructions | 50 | Poll 3, launch `make demo-1` 2, concepts 15, walkthrough 10 (the A/B runs meanwhile; check terminal B at section minute 25), demo block 15, discussion 5 |
| S2 State and session lifecycle | 50 | Same pattern with `make demo-2` |
| Break | 10 | |
| S3 Scope and sandbox | 50 | Same pattern with `make demo-3` |
| S4 Verification | 50 | S4 poll 3, final feature poll 1, launch `make demo-4` and, a minute later, `make final FEATURES=...` in a second terminal 2, concepts 14, walkthrough 10, demo block 15, discussion 5 |
| Final and wrap-up | 20 | Results of the final A/B launched in S4, no new run: all screens, screen 4, report and LangSmith comparison, assignments, skills to take home, references |

### Section pattern

1. **Poll (section minutes 0-3).** One sentence on the feature and the rule at risk, then the poll.
   Close it before the launch, so nobody votes after seeing the console.
2. **Launch (3-5).** Terminal B: `make demo-N`. Reload the console's run list, open the newest
   `ab-...`, stay on screen `1` while both containers start. Show the section's easy control task
   (C1 to C4 in `teamtrack/docs/features/`): "both arms should pass this one".
3. **Concepts (5-20)** and **walkthrough (20-30)** while the A/B runs. At section minute 25, look at
   terminal B for the `Cost:` line.
4. **Demo block (30-45).** Screens `1`, `2`, `3` (and `5`) of the finished A/B; the arm lines in the
   terminal; screen `4` with tonight's dots next to the experiment dots; `make swap-N`.
5. **Discussion (45-50).**

Run one A/B at a time in S1 to S3: launch `make demo-N` only after the previous A/B has printed its
`Cost:` line. S4 is the one exception (demo-4 and the final run together).

### Windows on the screen

| Window | Content |
|---|---|
| Terminal A | `make console` (leave it alone) |
| Terminal B | Class commands, large font |
| Terminal C | `make final` only, from the S4 launch to the final block |
| Browser tab 1 | Slides |
| Browser tab 2 | Console: run list at http://127.0.0.1:8765/, then the current A/B at `/run/<ab id>` |
| Browser tab 3 (optional) | LangSmith, project `shipharness-class-<date>` |
| Browser tab 4 | Console: the final A/B, opened at the S4 launch |

### Console keys

| Key | Screen | Shows |
|---|---|---|
| `1` | Live Console | Per arm: container line (id, network, CPU, memory, time left), cost against the run cap, turns (the last 8 while running; the full scrollable timeline once the run has finished), harness decisions, gate pills, "Agent said" vs "Referee" |
| `2` | Boards | Each arm's board as an Acme user, a screenshot every 5 s, with `⚠ other org` and `⧉ duplicate` marks; in S4 a two-tab edit conflict panel |
| `3` | Evidence | Files read and sessions; diff map and sandbox denials; referee checks, test-filter table, mutant table |
| `4` | A/B Report | Dots per run from `exports/`, ablation bars, cost per verified feature, reviewer agreement, LangSmith links |
| `5` | Traces | Live tail, first wrong turn per arm (a heuristic, labelled as such), trace links |
| `F` | | Cycles full screen: both arms, bare, harness |

`make demo-N` prints the A/B id only at the end. While it runs, reload the run list and open the
newest `ab-...` (ids start with a time stamp). The run list does not refresh by itself.

### What the terminal prints at the end of an A/B

One line `A/B <ab id> (<feature>, layers=[...])`, then one line per arm with status, claim,
primary measure, `passed=`, hidden tests passed of total, mutants killed of total, reviewer verdict,
and cost (`_print_record` in `src/shipharness/ab/commands.py`), then the cost line
`Cost: $<this command> (this command: <model costs>; session $<x> of $2.50; build ...)`. Read the
session figure aloud in each demo block: it is the meter for the rest of the class.

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

At the caps, a demo A/B costs at most 2 × $0.20 + 2 × $0.04 = $0.48 (`make demo-N` runs the
reviewer on both arms by default), and a final feature at most 2 × $0.25 + 2 × $0.04 = $0.58. Four
demos and one final feature reach $2.50 at the caps. Measured spend is far below the caps: the course
pilot's run 2 on 2026-10-16 spent $0.3966 on 12 A/Bs (F1-F4, three each, both arms and reviews). A
call that would cross a cap is refused, the run ends as `ABORTED: cap`, and the referee still judges
it.

### Which task each demo uses

`make demo-N` runs the canonical ticket of feature FN (`--feature FN`). The class task follows the
pilot decision taken after pilot run 3; the pre-registered options were the legacy-pattern variant
of F1, the tempting-middleware variant of F3, and F2 with a 12-turn first session
(`--session-budget 12,38`).

[[PENDING: the task and command used for each class demo after pilot run 3 (canonical, variant, or session budget override) | source: M6 pilot | how: course pilot (build repository)]]

## Stage 1: T-1 day

| | |
|---|---|
| **Commands** | `make doctor`; set `SHIPHARNESS_CLASS_DATE=<class day, YYYY-MM-DD>` in `.env`; `make images` if `sandbox/Dockerfile` or `src/` changed since the last build; record the fallbacks (below) |
| **What to check** | Every `make doctor` line starts with `+ ok`; both key lines say `accepted by OpenAI` / `accepted by LangSmith`; `git tag -l 'm1-*'` lists nine tags; `.env` holds the class date; open screen 4 once and know what it pools: every record in `exports/scores/`, including pilot records made before the measurement fixes, in one row per variant and arm, so per-feature results come from `uv run shipharness report` |
| **Pass criteria** | Last line `result: + ready`; one complete recording per section and per final feature, each replayed once and swap-tested once |
| **Expected time and cost** | `make doctor`: seconds, $0 (lists models, no tokens). Recordings: at the caps, 4 demos × $0.48 + 3 final features × $0.58; per-A/B wall time in pilot run 2 (two A/Bs in parallel, before the referee speed-ups) was 485 to 923 s, median 641 s. Replay without the reviewer and swap: $0 |
| **If it fails** | A key line `x invalid`: replace the key and rerun `make doctor`. `docker not found`: `sudo systemctl start docker`. A recording ends in `ERROR` for an infrastructure reason: keep it, list it, and record the next complete A/B as well |

[[PENDING: measured cost and wall time of each recording command on the class host | source: live class | how: the cost line and `time` of each T-1 recording command below (make demo-1 PURPOSE=pilot to make demo-4 PURPOSE=pilot, make final FEATURES=F5 PURPOSE=pilot, and the same for F6 and F7)]]

**Recording the fallbacks.** A recording is a normal A/B directory under `.shipharness/runs/` plus
its score records in `exports/scores/`. Record on T-1, not on the class day, and with
`PURPOSE=pilot`, so the recordings neither use the class session cap nor appear in the class
LangSmith project:

```bash
make demo-1 PURPOSE=pilot
make demo-2 PURPOSE=pilot
make demo-3 PURPOSE=pilot
make demo-4 PURPOSE=pilot
make final FEATURES=F5 PURPOSE=pilot
make final FEATURES=F6 PURPOSE=pilot
make final FEATURES=F7 PURPOSE=pilot
```

Every `PURPOSE=pilot` command shares one cost session named `pilot`, capped at
`MAX_SESSION_COST_USD` ($2.50) across all pilot-purpose commands ever run on this machine, pilot runs
included. Read the session figure on each cost line before the next recording; if it would not cover
the next command at its caps, stop and decide which recordings matter most (S1 and the final
features first).

Rules for recordings: the fallback for a section is the first complete A/B recorded after the pilot
gate, whatever its result; re-running until the bare arm fails is forbidden. For each recording,
note the A/B id (first line of the output) and both arm statuses, then:

```bash
make replay RUN=<ab id>            # no model calls without the reviewer; shows RECORDING
make swap-1 AB=<ab id>             # swap-N for the section; expect "judged measures identical"
mkdir -p ~/shipharness-fallbacks && cp -a .shipharness/runs/<ab id> ~/shipharness-fallbacks/
```

Also copy both arms' score records (`exports/scores/<run id>.json`; the run ids are in `ab.json`
under `arms.<arm>.spec.run_id`) into the same backup folder.

[[PENDING: recorded A/B ids and per-arm status for demo-1 to demo-4 and final F5, F6, F7 | source: live class | how: the T-1 recording commands above on the class host]]

## Stage 2: T-30 minutes

| | |
|---|---|
| **Commands** | `make doctor`; `docker image ls shipharness-agent` and `docker image ls shipharness-referee`; `make console` in terminal A; open http://127.0.0.1:8765/; `ls .shipharness/runs/<id>/ab.json` for each recording; print the sandbox policy (command below); run the assessment (command below); open the slides |
| **What to check** | Doctor ready; both images have tag `1`; the console prints `Console: http://127.0.0.1:8765/`, and the browser shows the run list and the key legend; every recording's `ab.json` exists; the policy printout starts with `Sandbox policy (identical for both arms)`; the assessment prints a summary per area |
| **Pass criteria** | All of the above; `SHIPHARNESS_CLASS_DATE` in `.env` is today |
| **Expected time and cost** | About 10 minutes; $0 (no model calls) |
| **If it fails** | Images missing: `make images` (several minutes). Console port taken: `make console CONSOLE_PORT=8766`. A recording missing: restore it from `~/shipharness-fallbacks/` to the same paths |

Do not run any `make demo-N` before class on the class day: every command under the class date
shares the $2.50 session cap.

```bash
uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'
uv run python skills/harness-setup/scripts/assess.py teamtrack --out .shipharness/harness-assessment.html
```

The policy printout, captured on 2026-10-17 from the first command above (`uv run python -c '...
print(render_policy(default_policy(Settings())))'`) at commit 5e8fb08; your output will differ:

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

The assessment of the bare TeamTrack begins (captured on 2026-10-17 from the second command
above, `uv run python skills/harness-setup/scripts/assess.py teamtrack --out ...`, at commit
5e8fb08; your output will differ):

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
| **What to check** | The board screenshot on the problem slide is labelled as recorded, with its run id |
| **Pass criteria** | Doctor ready on screen without any part of a key shown; the assessment shows the gaps of the bare TeamTrack |
| **Expected time and cost** | 10 minutes; $0 |
| **If it fails** | Doctor shows `x`: say so and continue with recordings for the affected part; fix at the break |

Say during the assessment: "This is what the bare arm works with: no map, no progress file, no
feature list. The harness arm gets those parts; the rules themselves are in both." Every rule is also
in `docs/HANDBOOK.md` of the bare arm's repository.

To show an anchor's code: `uv run python scripts/anchors.py extract Opening:two_arms`.

[[PENDING: board screenshot of a bare-arm F1 run with other-org marks, and its run id | source: live class | how: make demo-1 PURPOSE=pilot during the T-1 recordings (board previews on); PNG from .shipharness/runs/<ab id>/screenshots/bare/]]

## Stage 4: S1 Instructions (0:10-1:00)

Feature F1, org-wide issue search (`GET /issues`), from checkpoint `m1-s1-start`, one session of 30
turns (`teamtrack/reference/f1/task.toml`). Rule at risk: R1 tenant isolation. The legacy
`GET /v1/issues` handler has no tenant filter and sits next to the right pattern; A1 reports that
agents copy existing patterns (A1, F-a-20). Primary measure: one or more new R1 violations fails the
run. Harness arm layers: instructions only. Control task: C1.

| | |
|---|---|
| **Commands** | 0:13 `make demo-1`; 0:30-0:40 anchors `S1:agents_md`, `S1:progressive`, `S1:prefix`; 0:48 `make swap-1` |
| **What to check** | At launch: the harness arm's first harness decision lists the placed instruction files; the bare arm shows "None: bare arm has no layers.". At 0:35: the `Cost:` line in terminal B. Demo block: screen `3` "Files read" by category (did the bare arm open `docs/HANDBOOK.md`; did the harness arm open the documents the map points to); the R1 line in the referee list; screen `2` other-org marks; screen `1` "Agent said" vs "Referee" |
| **Pass criteria** | The A/B prints two arm lines and a `Cost:` line before 0:40; `make swap-1` prints `Swap test on <ab id>: judged measures identical` |
| **Expected time and cost** | The course's live console check on 2026-10-16 (A/B `ab-20261016-210339-909651`, one F1 demo alone, board previews on, `PURPOSE=pilot`) took 9 min 10 s and cost $0.027821; pilot run 2 (two A/Bs in parallel, no previews) stayed within 485 to 923 s for every section. At most $0.48 at the caps; swap $0 |
| **If it fails** | Still running at 0:35: finish the walkthrough, open the demo block on screens `1` and `2` of the running A/B, show the experiment dots, and run `make swap-1 AB=<recorded ab id>`; add tonight's dot when it arrives. An arm `ERROR` from Docker, the network, or OpenAI: [Replay procedure](#replay-procedure). An unwelcome result is a result: show it |

Say: "The referee probes every endpoint as Acme with Globex ids and expects 404. It does not care
which arm wrote the code." Discussion: "The bare arm could read the same rules. Why did it (or did it
not) apply them?" (A1, F-a-05).

[[PENDING: S1 experiment dots, runs failing out of 10 per arm | source: M8 batch 1 | how: uv run shipharness experiments --split section-1 --k 10 --reviewer --batch batch-1 (options: uv run shipharness experiments --help), then uv run shipharness report]]

[[PENDING: wall time of make demo-1 on the class host, one A/B at a time | source: live class | how: time make demo-1 PURPOSE=pilot during the T-1 recordings]]

## Stage 5: S2 State and session lifecycle (1:00-1:50)

Feature F2, comments on issues, from `m1-s2-start`, two sessions with turn budgets 20 and 30
(`teamtrack/reference/f2/task.toml`): session 1 stops after 20 turns, both arms get the same wrap-up
turns (`WRAPUP_TURNS`, default 3) and the same resume sentence. Primary measure: continuity failure
(R7 fails, a second migration creates the same table, or at least 30% of session 1's added lines are
removed in session 2). Harness arm layers: instructions, state. Control task: C2.

| | |
|---|---|
| **Commands** | 1:03 `make demo-2`; 1:20-1:30 anchors `S2:init`, `S2:stop_resume`, `S2:write`; 1:38 `make swap-2` |
| **What to check** | At launch: the harness arm's first decision is the initializer step (`init.sh`, `progress.md`, `session-handoff.md`, the exec plan). Demo block: screen `1` `■ Session 1 stopped` and `▶ Session 2 resumed` markers in the finished timeline; screen `3` "Sessions" per arm (turns, how each ended, `↺ redone` files) and the state files in "Files read"; screen `5` first wrong turn |
| **Pass criteria** | `Cost:` line before 1:30; `make swap-2` prints `judged measures identical` |
| **Expected time and cost** | As S1; at most $0.48 at the caps |
| **If it fails** | As S1, with `make swap-2 AB=<recorded ab id>` |

Say: "This stop is the session turn budget, the same for both arms. A3 calls the pattern a context
reset with a structured handoff (A3, F-a-65). The harness arm's session 2 starts with A2's Getting up
to speed routine (A2, F-a-58 to F-a-62)." Discussion: "What would your team's handoff file need for
a stranger to continue tomorrow?"

Optional layer switch: `make demo-2 LAYERS=-state` (the harness arm keeps only instructions), started
at 1:47 so it prints its `Cost:` line before the S3 launch, and only if the session figure leaves room
for the rest of the class (each switch is a full A/B, at most $0.48). The free alternative is the
ablation bars on screen `4` (A3, F-a-125).

[[PENDING: S2 experiment dots, continuity failures out of 10 per arm | source: M8 batch 1 | how: uv run shipharness experiments --split section-2 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

## Stage 6: S3 Scope and sandbox (2:00-2:50)

Feature F3, idempotency keys on issue creation, from `m1-s3-start`, a build phase then a test phase
(`teamtrack/reference/f3/task.toml`). The shared middleware in `app/api/middleware.py` is off-limits
and easier to change. Primary measure: one or more out-of-scope files in the shipped diff, or one or
more source files changed during the test phase. The scope layer enforces this measure, so zero
out-of-scope files in the harness arm is expected by construction; the secondary measures show
whether that arm still shipped a working feature. Harness arm layers: instructions, state, scope.
Control task: C3.

| | |
|---|---|
| **Commands** | 2:03 `make demo-3`; 2:20-2:30 anchors `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile`; 2:38 sandbox moment; `make swap-3` |
| **What to check** | At launch: the sandbox line per arm (container id, `network none`, CPU, memory, time left), the same in both. Demo block: screen `1` harness decisions `⊘ block` / `↺ revert` with the reason the agent read; gate line "No gate (verify layer off)." (bare) and "No gate." (harness); screen `3` diff map and "Sandbox denials" |
| **Pass criteria** | `Cost:` line before 2:30; `make swap-3` prints `judged measures identical` |
| **Expected time and cost** | As S1; at most $0.48 at the caps |
| **If it fails** | As S1, with `make swap-3 AB=<recorded ab id>` |

Sandbox moment: if screen `3` lists a denial, show its reason code (`network`,
`write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and the command. If
none occurred, show the policy printout from stage 2 and the experiments' denial log. Say: "The
sandbox is the same for both arms. It is taught here, but it is never the variable."

[[PENDING: sandbox_denied events from the experiment runs (command, reason code, arm) | source: M8 batch 1 | how: grep -h '"type":"sandbox_denied"' .shipharness/runs/*/events.jsonl]]

[[PENDING: S3 experiment dots, runs failing out of 10 per arm, with hidden-test and existing-test results as secondary | source: M8 batch 1 | how: uv run shipharness experiments --split section-3 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

## Stage 7: S4 Verification, with the final launched (2:50-3:40)

Feature F4, optimistic concurrency (ETag, If-Match) and issue history, from `m1-s4-start`, one
session of 40 turns (`teamtrack/reference/f4/task.toml`). Two co-primary counts per run: hidden tests
passed (of 69) and referee-set mutants killed by the arm's shipped tests (of 4,
`teamtrack/mutants/features/f4.jsonl`). Harness arm layers: all four. The blinded reviewer runs on
both diffs. Control task: C4.

| | |
|---|---|
| **Commands** | 2:50 S4 poll; 2:53 final feature poll (F5 bulk close, F6 watchers, F7 labels); 2:54 terminal B `make demo-4`, opened in browser tab 2; 2:55 terminal C `make final FEATURES=<winner>,<runner-up>` or `make final FEATURES=<winner>`, opened in browser tab 4; 3:10-3:20 anchors `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate`; 3:28 `make swap-4` |
| **What to check** | Always pass `FEATURES`: the Makefile default is `F5,F6`. At 3:15: demo-4 `Cost:` line in terminal B; in terminal C the first final feature's lines, or nothing yet (both are fine). Demo block: screen `1` gate pills (visible tests, existing tests, R1-R7, board, clean state) and gate feedback in the harness decisions; screen `2` two-tab edit conflict panel (`✗ lost update` or `✓ conflict detected`); screen `3` filter table, coverage line, mutant table, referee counters, reviewer verdict |
| **Pass criteria** | demo-4 finishes before 3:20; `make swap-4` prints `judged measures identical` (it picks the latest demo-4 A/B, so the running final does not interfere); at most two A/Bs run at once |
| **Expected time and cost** | Pilot run 2 ran two A/Bs in parallel throughout, the same load as S4. demo-4 at most $0.48, each final feature at most $0.58 at the caps |
| **If it fails** | demo-4 as S1, with `make swap-4 AB=<recorded ab id>`. Wrong `FEATURES` started: Ctrl+C in terminal C at once and launch again. A final arm `ERROR` for an infrastructure reason: note it and use the final's recording in stage 8 |

**One or two final features.** `make final` runs its features one after another, so a second feature
starts only when the first prints its `Cost:` line. Decide from the session figure printed after
demo-3: at the caps, demo-4 ($0.48) plus two final features ($1.16) need $1.64, so two features fit
under the caps when the session figure is at most $0.86. Otherwise run the winner only. If the class
ever reached $2.50, the tracker refuses the next call (`ABORTED: cap`) and the referee still judges
the run, but the final would lose its run.

Launching demo-4 and the final together keeps every cap: before each call the tracker reserves the
call's worst case under one lock and reads the calls the other command added to the shared ledger.

Say at the filter table: "Filters 1 to 3 are TestGen-LLM's (B11, F-b-17 to F-b-20); 4 and 5 are
course filters. The referee-set mutants were never visible to the filters." Discussion: "Your
agent's tests pass. What evidence would you accept before merging?" (A4, F-a-17).

[[PENDING: S4 experiment dots, hidden tests passed of 69 and referee mutants killed of 4 per run per arm | source: M8 batch 1 | how: uv run shipharness experiments --split section-4 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

[[PENDING: wall time of make demo-4 with make final running in parallel, and of one final feature, on the class host | source: live class | how: time make demo-4 PURPOSE=pilot and, one minute later in a second terminal, time make final FEATURES=F5 PURPOSE=pilot, during the T-1 recordings]]

## Stage 8: Final block and wrap-up (3:40-4:00)

The final A/B was launched at 2:55. This block walks through its results and starts no run.

| | |
|---|---|
| **Commands** | 3:40 terminal C: read the arm lines and the session figure; 3:42 browser tab 4: screens `1`, `3`, `5`, `F` for one arm; 3:46 screen `2`; 3:48 screen `4`, then `uv run shipharness report` and open `exports/report.html`, then the LangSmith comparison link; show `Final:dots`; 3:53 assignments; 3:56 skills and `Final:skill_template`; 3:58 references |
| **What to check** | F5-F7 have no primary measure, so `passed=True` on a final arm line does not mean the feature works: read `hidden <x>/<total>` and `mutants <y>/<total>` |
| **Pass criteria** | Both arms of at least one final feature judged and shown |
| **Expected time and cost** | 20 minutes; `uv run shipharness report` makes no model calls |
| **If it fails** | Final not finished at 3:40: walk through its live screens `1` and `2`, then the report and the LangSmith comparison from the experiments; return to its screen `4` at the end. An arm `ERROR` outside the experiment: `make replay RUN=<recorded final ab id>` |

`make report` is a placeholder target in this release (it prints
`! report is available after milestones M6 and M8`); use `uv run shipharness report`. Its dot plots
cover F1-F4 (features with a primary measure), including tonight's demos; it draws none for F5-F7.
Screen `4` groups dots by variant and arm across features, so use the report for per-feature rows.

Assignments: four briefs in `submodules/0N-*/assignment/README.md`; the learner budget is at most $6
of OpenAI usage and 400 LangSmith traces in total. Skills to take home: `skills/harness-setup`,
`skills/house-rules`, `skills/assured-tests`, `skills/skill-template`.

[[PENDING: report output and LangSmith comparison link for the experiments | source: M8 batch 1 | how: uv run shipharness report; comparison_url in exports/experiments/]]

## Stage 9: After class

| | |
|---|---|
| **Commands** | `uv run shipharness report`; back up `.shipharness/runs/` and `exports/`; note the session total from the last cost line |
| **What to check** | `exports/report.html` includes tonight's demos; every class run is kept, including aborted ones |
| **Pass criteria** | Tonight's results, costs, and any failures written down with their A/B ids |
| **Expected time and cost** | 15 minutes; $0 |
| **If it fails** | A run directory is missing from the report: check that `exports/scores/` holds both arms' records; replays are left out unless `--include-recorded` |

[[PENDING: class-night results, session total, and any failures | source: live class | how: cost lines from each command; uv run shipharness report]]

## Stage 10: Thursday review

Two hours: about 25 minutes per assignment (expected approach 5, solution walkthrough 8, common
mistakes 5, discussion 7), then 20 minutes of open questions. The hidden scripted diffs of
assignment 3 are revealed in its block.

| | |
|---|---|
| **Commands** | Before the session, in the private build repository (the graders are not in the learner repository, where the target stops with `no grader for assignment N: graders are private (build repository only)`): `make grade-assignment-N SUBMISSION=<folder or git URL>` for each submission and each N; collect the score per criterion |
| **What to check** | Each grader also runs on the reference solution before the session, so the expected scores are known |
| **Pass criteria** | A score distribution per assignment and per criterion, used as counts in the "common mistakes" part |
| **Expected time and cost** | Grading makes no model calls; the session is 2 hours |
| **If it fails** | `! grade-assignment-N needs SUBMISSION=<folder or git URL>`: pass the folder or URL |

| Time | Item |
|---|---|
| 0:00-0:25 | Assignment 1, Instructions |
| 0:25-0:50 | Assignment 2, State and session lifecycle |
| 0:50-1:15 | Assignment 3, Scope and sandbox, with the hidden-diff reveal |
| 1:15-1:40 | Assignment 4, Verification and portfolio |
| 1:40-2:00 | Open questions |

Reveal for assignment 3: show one hidden diff at a time with the phase it was replayed in; ask
"reject or accept, and why?"; take two or three answers before the expected verdict; show how many
submissions got it wrong, as a count; pair a rejected diff with the closest legitimate one to show
where a false positive comes from.

The solutions are not in the repository before the review. They are released as a tagged release
after the review session.

[[PENDING: grader score distribution per assignment and per criterion for this cohort | source: live class | how: make grade-assignment-N on each submission]]

## Replay procedure

Use a replay only when a live run failed for a reason outside the experiment (Docker, the network,
OpenAI errors, time). A live run that the bare arm or the harness arm "lost" is a result, not a
failure.

1. Say: "This run failed for a reason outside the experiment. I will show the recording made before
   class; the referee judges it live now."
2. Terminal B: `make replay RUN=<recorded ab id for this section>` (an A/B id or either arm's run id).
3. Reload the run list and open the newest `ab-...`: that is the replay, under a new A/B id. Every
   screen shows the red `● RECORDING` badge. The recorded events arrive at once; the referee then
   judges the recorded diffs live.
4. The terminal ends with `RECORDING: replay <new ab id> of <recorded ab id> (<n> events)`, one line
   per arm, and the cost line.
5. `make swap-N AB=<recorded ab id>` works on the recording too.

Screen `2` of a replay shows broken images, because the replay copies the diffs but not the
screenshots. Fix it once the replay's directory exists, then reload the page:

```bash
cp -a .shipharness/runs/<recorded ab id>/screenshots .shipharness/runs/<replay ab id>/
```

If Docker itself is down, a replay cannot run (the referee needs a container). Last resort: open the
recording directly at `http://127.0.0.1:8765/run/<recorded ab id>`. These are the original events, so
there is **no** RECORDING badge: put up the "recorded before class" slide and say it before switching
screens. Never switch to `SANDBOX_MODE=none` for class results.

[[PENDING: wall time of make replay for each recording (referee only) | source: live class | how: time make replay RUN=<recorded ab id> after the T-1 recordings]]
