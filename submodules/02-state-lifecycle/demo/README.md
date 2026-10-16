# S2 demo: F2 across a forced session stop

Runbook for the S2 live A/B (`make demo-2`): purpose, commands, screen sequence and anchors, poll,
what to watch, what the harness arm does differently, captured output, pilot and experiment results,
time and cost, troubleshooting and replay. The 50-minute S2 block follows the class's section pattern
([instructor guide, "Section pattern"](../../../docs/instructor-guide.md#section-pattern)): poll
(3 min), launch of `make demo-2` (2 min), concepts (15 min) and code walkthrough (10 min) while the
A/B runs in the background, then the demo block (15 min) on the finished A/B and discussion (5 min).
Source ids (A1-A7, F-a-NN) point to [REFERENCES.md](../../../REFERENCES.md).

Everything marked PENDING needs real run output and is filled from pilot run 3, the experiment
batches, or the class itself. Captured output is labelled "captured on <date>, run <id>; your output
will differ". The captured blocks below come from pilot run 2 (2026-10-16), before the fixes that
followed it; where a fix since then changes what you will see, the text says so.

---

## 1. Purpose and the problem this demo shows

Both arms build F2, comments on issues
([teamtrack/docs/features/f2.md](../../../teamtrack/docs/features/f2.md)), from checkpoint
`m1-s2-start` (base + F1). The task's session turn budget is `[20, 30]`
([teamtrack/reference/f2/task.toml](../../../teamtrack/reference/f2/task.toml)): if an arm has not
called `finish` after 20 turns, the session stops, and a second session of 30 turns starts with an
empty context. The session turn budget is the course's mechanism, not a source term; it produces
A3's context reset at a fixed point in both arms (A3, F-a-65).

The problem: a session that "begins with no memory of what came before." (A2, F-a-08) has to work
out what the first session did. On F2 a wrong guess is visible: a second Alembic migration from the
old head (two heads, breaking house rule R7; "house rules" is the course's label for what A1 calls
"golden principles", A1, F-a-99), a second `create_table("comments")`, or session 2 removing and
rewriting what session 1 wrote.

| Arm | Layers | What it gets at the stop |
|---|---|---|
| bare | none | "This session is ending soon. Turns left in this session: 3." then, in session 2, "A previous session worked on this ticket and was stopped." |
| harness | instructions, state (`src/shipharness/ab/demo.py`, `SECTION_STACKS`) | The same two sentences, plus the wrap-up steps (progress, exec plan, handoff notes with the rules and files that matter, commit), a harness-written machine summary in `session-handoff.md`, a session-log entry in `progress.md`, and the Getting up to speed routine in every session |

Everything else is identical: model, effort, tools, ticket, sandbox, turn budgets, wrap-up turns, cost
cap. The bare arm has the same R7 rule in `docs/HANDBOOK.md`.

Primary measure (registered before any run): `continuity_failure`, true if (a) R7 fails, (b) two
migrations create the same table, or (c) 30% or more of session 1's added lines are removed in
session 2. See [concepts.md](../concepts.md) §5.

**Which task the class runs.** This runbook is written for F2 canonical. Pilot run 2 showed no gap on
it (section 7), so pilot run 3 tests the registered lever: the same task with a 12-turn first session
and 38 turns after it (`--session-budget 12,38`). The class task follows the pilot's decision after
run 3.

[[PENDING: final S2 class task (F2 canonical [20, 30] or F2 canonical with --session-budget 12,38) and the exact class command | source: M6 pilot | how: course pilot (build repository)]]

---

## 2. Commands

Run everything inside WSL2 from the repository root (`~/shipharness`). Before class: `make doctor`
passes and `make setup` has built the two images.

| Step | Command | What it runs (`make -n`) |
|---|---|---|
| Console | `make console` (separate terminal) | `uv run shipharness console --port 8765`; open `http://127.0.0.1:8765/`, then the new A/B under its id |
| Demo | `make demo-2` | `uv run shipharness ab --section demo-2 --feature F2 --purpose class`: F2 canonical, bare vs instructions + state, both arms in parallel, referee on both, the reviewer on both diffs (it does not see the arm labels) |
| Demo with the run-3 lever | `uv run shipharness ab --section demo-2 --feature F2 --session-budget 12,38 --purpose class` | The same A/B with a 12-turn first session; only if the pilot decision picks it (section 1). `make demo-2` has no variable for the budget |
| Swap test | `make swap-2` | `uv run shipharness ab --swap latest --section demo-2 --purpose class`: re-judges each arm's shipped diff under the other arm's label with the recorded seed and pinned checkpoint commit; no model calls. Prints `Swap test on <ab_id>: judged measures identical` (exit 0) or `DIFFERENT` with the fields that changed (exit 1). `AB=<ab or run id>` picks another A/B |
| Layer switch | `make demo-2 LAYERS=-state` | `uv run shipharness ab --section demo-2 --feature F2 --layers=-state --purpose class`: the harness arm runs with `instructions` only (`ab/demo.py`, `section_layers`). A new live A/B under the same caps as `make demo-2` (at most $0.48) |
| Replay fallback | `make replay RUN=<ab or run id>` | `uv run shipharness replay <id>`. Only if the live run fails on stage; see §9 |

The expansions in the third column were captured on 2026-10-17 from `make -n <target>` at commit
5e8fb08 (offline command; your output will differ only if the Makefile changes). The
`--session-budget` option is listed by `uv run shipharness ab --help`. `make demo-2`, `make swap-2`,
`make replay`, and `make console` were not run for this runbook (they start containers or call
OpenAI); the integrator verifies them live.

At the end `make demo-2` prints one header line and one line per arm (`ab/commands.py`,
`_print_record`):

```text
A/B <ab_id> (F2, layers=['instructions', 'state'])
  <arm>  <status>  claim=<claim>  primary={"continuity_failure": ...} passed=<bool> hidden <x>/<N> mutants <k>/<M> reviewer=<verdict> cost=$<usd>
Cost: $<usd> (this command: <model> $<usd>, ...; session $<usd> of $2.50)
```

The line format comes from the code; the values do not exist until the run. Exit code: 0 when both
arms completed, 2 when an arm ended `ABORTED` (cap or timeout), 1 on `ERROR`.

Start the layer switch only if the session figure on the `Cost:` line leaves room for the rest of the
class; `MAX_SESSION_COST_USD` ($2.50) blocks it otherwise. If it does not fit, show the ablation dots
instead (§7).

---

## 3. Screen sequence and code anchors

### Order in class

| Section minutes | Block | Terminal B and console |
|---|---|---|
| 0-3 | Poll (section 4) | Close the poll before the launch |
| 3-5 | Launch | `make demo-2` at minute 3; open the new A/B on screen `1`; control glance |
| 5-20 | Concepts ([../concepts.md](../concepts.md)) | The A/B runs in the background |
| 20-30 | Code walkthrough | The A/B runs; at minute 25 check terminal B for the `Cost:` line |
| 30-45 | Demo block | The finished A/B: screens, verdicts, pilot and experiment dots, swap test |
| 45-50 | Discussion and transition | |

The A/B must be finished by section minute 25. In pilot run 2 (12 A/Bs, F1-F4, two A/Bs in parallel
on the class host, before the referee speed-ups) every A/B finished within 923 s (15.4 min); median
641 s (10.7 min), minimum 485 s (8.1 min) (measured in the course pilot, run 2, 2026-10-16). The class
runs one A/B at a time. If the A/B is still running at minute 25, open the demo block on the running
A/B and run the swap test on the recorded fallback (`make swap-2 AB=<recorded ab id>`); if it failed
on stage, use the replay (section 9). The instructor guide's "If it fails" rows cover both cases.

While a run is live, screen `1` shows the last 8 turn rows and the last 3 harness decisions per arm;
once the run has finished it lists every turn row and every harness decision in scrollable lists
(`src/shipharness/console/templates/screens/live.html`). Show the first turns live at the launch; in
the demo block, scroll the finished timeline on screen `1` or read screen `3`.

### Poll and launch (5 min, before the concepts)

| When | Key | Screen | Point at |
|---|---|---|---|
| Section minutes 0-3 | | | Poll (§4); close it before the launch |
| Minute 3 | | | `make demo-2`. If a layer switch from S1 is still running, wait for its `Cost:` line first |
| First turns | `1` | Live Console | Harness arm: the `note` decision "initializer step: init.sh, progress.md, session-handoff.md, docs/exec-plans/active/F2.md"; its prompt asks for Getting up to speed before any change (`pwd`, `progress.md`, `git log`, the handoff's agent notes, `bash init.sh`). Bare arm: only the ticket and the repository |
| Minutes 4-5 | | | Glance at the easy control task, C2 "Search projects by name" (`teamtrack/docs/features/c2.md`); then the concept slides |

### Code walkthrough (10 min, while the A/B runs)

Open the three S2 anchors (`uv run python scripts/anchors.py extract <id>`):

| Anchor | File | Show |
|---|---|---|
| `S2:init` | `src/shipharness/harness/state/assets/init.sh` (lines 2-29) | Scratch database, `alembic heads` then `upgrade head`, one end-to-end test file (`tests/visible/test_issues.py`) with `-x`; the A2 sentence in the header comment |
| `S2:stop_resume` | `src/shipharness/harness/state/lifecycle.py` (lines 95-134) | `session_stop`: machine summary, handoff merge, progress entry, commit, `session_stop` decision; `resume_text` |
| `S2:write` | `src/shipharness/harness/state/progress.py` (lines 11-37) | `session_entry` (index, commits, `ended_by`, turns, files, tests) and `append_session_entry` (restores the heading) |

Also worth a glance: `getting_up_to_speed` and `wrapup_text` at the top of `lifecycle.py` (the agent
notes first, bookkeeping only in the wrap-up: the harness change after pilot run 2);
`StateLayer.prepare_workspace` in `src/shipharness/harness/state/layer.py` (the initializer step as
deterministic code, course design); and `NEUTRAL_RESUME` in `src/shipharness/runner/prompts.py` (the
sentence both arms get).

### Demo block (15 min, after the walkthrough)

The wrap-up and the start of session 2 happen while the concepts are on screen. In the demo block
they are read from the finished A/B, in this order (screens 1, 3, 2, 5, then the verdicts and
screen 4):

| Key | Screen | Point at |
|---|---|---|
| `1` | Live Console | The full timeline per arm: the markers "■ Session 1 stopped" and "▶ Session 2 resumed", the first tool calls of each session, the harness arm's decisions |
| `3` | Evidence | "Sessions" list per arm: turns and `ended_by` per session, and "↺ redone" lines for files changed again in a later session; then the referee list: `continuity` and `r7_migrations` results per arm |
| `2` | Boards | Each arm's `/board` page as Acme, the last capture from the preview container |
| `5` | Traces | First wrong turn per arm (a heuristic: the earliest turn that edited a file a failing check names) and the LangSmith trace link. In the trace, compare each arm's first five tool calls in session 2: does it read what session 1 left, and does it run `alembic heads` or look at `migrations/versions/` before writing a migration? |
| | Terminal B | The A/B verdicts (one line per arm) and the session figure from the `Cost:` line |
| `4` | A/B Report | S2 dots: tonight's run next to the pilot and batch-1 dots (§7). Every run is a dot; read counts, not percentages |
| | | Then `make swap-2`, or `make demo-2 LAYERS=-state` if the session figure leaves room |

Screen 4 note: in the live console check (A/B `ab-20261016-210339-909651`, 2026-10-16) screen 4
pooled all features and pre-fix records into one row per arm; it groups by feature from tonight's fix.

---

## 4. Poll question

Ask before `make demo-2`:

> Both agents stop after 20 turns, before F2 is finished, and start again with an empty context. The
> bare agent has the same house rules in its docs, including "exactly one migration head". After the
> second session, which arm ships a migration history with one head and one `comments` table, and
> keeps most of what session 1 wrote?
>
> A. Both arms. B. Only the harness arm. C. Only the bare arm. D. Neither.

If the class runs the 12-turn lever, say "after 12 turns" instead.

What the pilot showed so far: in run 2 the bare arm passed in 3 of 3 runs; the harness arm's 0 of 3
is not a valid measurement, because the continuity check counted the harness's own files, a bug fixed
since (section 7). Answer pattern from the experiments:

[[PENDING: S2 poll answer pattern: continuity_failure counts per arm out of k=10, split by component (a) R7, (b) duplicate table, (c) redone >= 30%, with run ids | source: M8 batch 1 | how: uv run shipharness experiments --split section-2 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

After the run, ask one follow-up: "Which file did each arm's session 2 read first, and did it change
what that session did next?"

---

## 5. What to watch

The initializer step and the first turns can be shown live at the launch. The rest is read in the
demo block from the finished timeline on screen 1, screens 3 and 5, and the trace.

- **No BLOCKED lines and no gate pills in demo-2.** The harness arm runs instructions and state only.
  Only the scope layer rejects patches (`src/shipharness/harness/scope/layer.py`), and it starts in
  demo-3; the verification gate starts in demo-4, so screen 1 shows "No gate" for both arms. The
  three F2 A/Bs of pilot run 2 had 0 `blocked` events (their `events.jsonl`).
- **The initializer step** (screen 1, harness decisions): one `note` listing the four files, and the
  commit `harness: initializer step for F2`. Nothing like it in the bare arm.
- **Getting up to speed** (screen 1, tool calls): `run pwd`, `read_file progress.md`, `run git log
  --oneline -20`, `read_file session-handoff.md` (the agent notes first), `read_file
  docs/exec-plans/active/F2.md`, `run bash init.sh`, and in session 1 only, `run_visible_tests`. The
  prompt asks for this order; whether the agent follows it is the thing to watch.
- **Documents read after that.** In pilot run 2 every harness session re-read 3 to 7 instruction
  documents (section 6). Since the change that followed, the prompt says to open a document from the
  AGENTS.md map only for a detail the handoff notes do not cover. Count the `read_file` calls on
  documents before the first `apply_patch` in each session.
- **`init.sh` output in session 2**: the line `== migrations (house rule R7: exactly one head)`
  followed by the heads. If session 1 already added the comments migration, its revision is listed
  here.
- **Wrap-up**: both arms get "This session is ending soon. Turns left in this session: 3." Only the
  harness arm's message continues with four numbered steps.
- **The stop**: the marker "■ Session 1 stopped" (event `session_stop`, with `ended_by` and the end
  commit); for the harness arm a `session_stop` decision "session 1 handoff written to
  session-handoff.md" and the commit `harness: session 1 handoff for F2`.
- **The handoff's machine summary**: the line `- Migration heads: ...`. With more than one head it
  ends with "house rule R7 needs exactly one". The last line lists the harness documents read so
  far.
- **The resume**: "▶ Session 2 resumed" (event `session_resume`, with `prefix_blocks`: `core` for the
  bare arm, `core, instructions, state` for the harness arm).
- **The bare arm's session 2**: in pilot run 2 it found session 1's uncommitted work with `git status`
  and read the migration before writing code (section 6). Watch for that call; it is the bare arm's
  own way of getting up to speed.
- **`migrations/versions/` in session 2**: a second new migration file in either arm is the moment to
  point at; it is what parts (a) and (b) catch.
- **Screen 3 "↺ redone"**: a file-level hint (a file changed in session 1 changed again later).
  Working on the same file in session 2 is normal; the judged number is `redone_lines_pct` from the
  referee (post-class reading 03).
- **No stop at all**: an arm that calls `finish` in session 1, even on its last turn, has no stop
  markers. Say so; parts (a) and (b) still judge its migrations.
- **Exec plan**: in demo-2 the plan stays in `docs/exec-plans/active/`. It moves to `completed/` only
  after the scope layer sets `passes`, which starts in demo-3.
- **Screen 2**: the preview captures the `/board` page. The comments panel is on the issue page
  (`/board/issues/{issue_id}`), which the preview's board view does not open; the referee's hidden
  board tests for F2 (`tests/hidden/f2/test_f2_board.py`, 8 tests) judge the panel.

---

## 6. What the harness arm does differently, and why

The harness arm's answer to the problem is state written where the next session looks, by two
writers:

- **The agent**, in the wrap-up turns: what it was doing, what is left, what to watch out for, and the
  house rules and file locations it already looked up, so session 2 does not look them up again.
- **The harness**, at the stop, whatever the agent did: the machine summary (commits, files changed,
  visible tests, TODO markers, migration heads, documents read) and one session-log line in
  `progress.md`, committed.

Session 2 then starts from those files instead of from a search of the repository. That is A2's
"Getting up to speed" (F-a-59) with A3's structured handoff (F-a-65). The bare arm has to rebuild the
same picture with its own tool calls.

What pilot run 2 showed, before the turn-cost change: the harness arm followed the routine and wrote
good notes, but spent most of its turns reading. In `ab-20261016-181736-08a9c4` the harness arm's
session 1 was `pwd`/`git log`, the three state files, `init.sh`, the visible tests, the feature spec,
the HANDBOOK, a skill, four instruction documents, two product files, and then the bookkeeping in
turns 18-20; its first product patch came at turn 27 of session 2. The bare arm wrote its first
product patch at turn 18 of session 1. The change after run 2 (a harness change, harness arm only)
moved the bookkeeping to the wrap-up turns and put the agent's notes ahead of any document. Tonight's
run is the first class-host run with that change; compare the first-patch turn per session with the
run 2 timeline below.

---

## 7. Captured output, screenshots, and results

### Captured output from pilot run 2

The harness arm's tool calls in sessions 1 and 2 (captured on 2026-10-16, run
`r-20261016-181736-260803` in `ab-20261016-181736-08a9c4`; the `name` and `target` fields of the
`tool_call` events in `events.jsonl`, with the session and turn of the preceding `turn` event, cut
where `...` stands; your output will differ):

```text
s1 t 1 run pwd && git status --short && git log --oneline -20
...
s1 t 3 read_file progress.md
s1 t 4 read_file session-handoff.md
s1 t 5 read_file docs/exec-plans/active/F2.md
s1 t 6 run bash init.sh
s1 t 7 run_visible_tests
s1 t 8 read_file docs/features/f2.md
s1 t 9 read_file docs/HANDBOOK.md
s1 t10 read_file .agents/skills/add-endpoint/SKILL.md
s1 t11 read_file ARCHITECTURE.md
...
s1 t19 apply_patch progress.md, docs/exec-plans/active/F2.md, session-handoff.md
s1 t20 run git add progress.md docs/exec-plans/active/F2.md session-handoff.md && git commit -m "docs ...
s2 t 1 run pwd && cat progress.md && git log --oneline -20
s2 t 2 read_file session-handoff.md
...
s2 t 7 read_file docs/HANDBOOK.md
...
s2 t26 read_file app/repositories/projects.py
s2 t27 apply_patch app/db/models.py
s2 t28 apply_patch progress.md, docs/exec-plans/active/F2.md, session-handoff.md
```

The agent's handoff notes after session 1 (captured on 2026-10-16, run `r-20261016-181736-260803`,
`harness/sessions/session-1.patch`, added lines, cut; your output will differ):

```text
+- What I was doing: Started F2 comments-on-issues work. Read the feature specification and handbook,
+  plus the add-endpoint skill and architecture/security/API/reliability guidance. No implementation
+  edits have been made yet.
...
+- What to watch out for: The baseline is good (`bash init.sh`, 162 visible tests pass; current migration
+  head is `0001_initial`). Follow the exact requirements in `docs/features/f2.md`, particularly the
...
```

The harness's session-log line in `progress.md` (captured on 2026-10-16, run
`r-20261016-181736-260803`, a context line of `harness/sessions/session-2.patch`; your output will
differ):

```text
- Session 1 (build): start ba50736, end 09c49c7, ended by turn_budget after 20 turns. 3 files changed; visible tests passed=162 failed=0 errors=0.
```

The bare arm's session-2 look at the working tree is in [concepts.md](../concepts.md) §1 (same A/B,
run `r-20261016-181736-a05ddb`).

### Pilot run 2 dots for F2

Every run of F2 canonical in pilot run 2, from the A/B records (`.shipharness/runs/<ab id>/ab.json`)
and the score records (`exports/scores/<run id>.json`) (captured on 2026-10-16, runs as listed; your
output will differ). The harness arm's `continuity_failure` and `redone_lines_pct` were scored before
the continuity fix and count the harness's own files; they are the measurement bug, not a result.

| A/B | Arm | Run id | `continuity_failure` | `redone_lines_pct` | Hidden tests passed (of 56) | Build sessions, ended by | Cost (USD) |
|---|---|---|---|---|---|---|---|
| `ab-20261016-181736-08a9c4` | bare | `r-20261016-181736-a05ddb` | false | 2.1 | 55 | 20 turn_budget, 30 claim_not_done | 0.018463 |
| `ab-20261016-181736-08a9c4` | harness | `r-20261016-181736-260803` | true (bug) | 84.0 | 3 | 20 turn_budget, 30 turn_budget; ABORTED: timeout in the test phase | 0.016612 |
| `ab-20261016-184318-636e90` | bare | `r-20261016-184318-a7c11c` | false | 0.0 | 56 | 20 turn_budget, 30 turn_budget | 0.016186 |
| `ab-20261016-184318-636e90` | harness | `r-20261016-184318-fdee0c` | true (bug) | 76.5 | 3 | 20 claim_not_done (no stop) | 0.009195 |
| `ab-20261016-190548-ae9abe` | bare | `r-20261016-190548-3c5d9d` | false | 0.0 | 55 | 20 turn_budget, 30 turn_budget | 0.017546 |
| `ab-20261016-190548-ae9abe` | harness | `r-20261016-190548-9352c4` | true (bug) | 50.0 | 3 | 20 turn_budget, 30 turn_budget | 0.015149 |

Hidden tests are secondary for S2; the gap in them (55-56 against 3) is the turn cost described in
section 6, not a continuity failure. Every bare arm wrote `migrations/versions/0002_comments.py` in
session 1 and none wrote a second migration (session patches in the same A/B folders).

[[PENDING: pilot run 3 F2 dots (12-turn first session, k=3): continuity_failure, redone_lines_pct, hidden passed, sessions per arm, with run ids | source: M6 pilot | how: course pilot (build repository)]]

### Class-host screenshots and live output

[[PENDING: terminal output of the S2 class command (header, two arm lines, cost line), labelled captured on <date>, run <id> | source: live class | how: make demo-2]]

[[PENDING: screen 1 Live Console screenshot of a finished A/B showing the Session 1 stopped and Session 2 resumed markers for both arms | source: live class | how: make console, then make demo-2, key 1]]

[[PENDING: screen 2 Boards screenshot of both arms' /board pages | source: live class | how: make console, then make demo-2, key 2]]

[[PENDING: screen 3 Evidence screenshot with the Sessions list per arm (turns, ended_by, redone lines) and the continuity and r7_migrations referee rows | source: live class | how: make console, then make demo-2, key 3]]

[[PENDING: screen 4 A/B Report screenshot with the S2 dots and this run highlighted | source: live class | how: make console after make demo-2, then key 4]]

[[PENDING: screen 5 Traces screenshot with the first wrong turn per arm and the LangSmith link | source: live class | how: make console, then make demo-2, key 5]]

[[PENDING: terminal output of make swap-2 | source: live class | how: make swap-2]]

[[PENDING: terminal output of make demo-2 LAYERS=-state | source: live class | how: make demo-2 LAYERS=-state]]

### Experiment results for this section

Batch 1 of the course's experiment plan runs F1-F4 canonical, two arms, k=10 each, reviewer on; for
S2 that is 10 runs per arm of F2 canonical with the demo-2 stack.

[[PENDING: S2 dots from batch 1: continuity_failure per run per arm (k=10), components (a)/(b)/(c), redone_lines_pct, sessions, hidden tests passed of 56, run ids, LangSmith comparison link | source: M8 batch 1 | how: uv run shipharness experiments --split section-2 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

The ablation batch removes one layer at a time from the full stack (an ablation in A3's sense: remove
one component and see what changes, F-a-125). The state row is the result to show if the live layer
switch does not fit the budget:

[[PENDING: ablation dots for the stack without the state layer on the S2 tasks (k=2), with run ids | source: M8 ablation | how: uv run shipharness experiments --split section-2 --k 2 --layers=-state --batch ablation, then uv run shipharness report]]

---

## 8. Measured time and cost

Limits that apply to every arm (from `src/shipharness/config/settings.py`): `MAX_RUN_COST_USD` $0.20
per arm per run, build and test phases together; `RUN_TIMEOUT_S` 300 s of agent time per arm;
`HARNESS_TIMEOUT_S` 120 s of harness work per arm; `TOOL_TIMEOUT_S` 120 s per tool command;
`MAX_REVIEW_COST_USD` $0.04 per review. The worst case for one `make demo-2` at the caps is
2 × $0.20 + 2 × $0.04 = $0.48. The course accepts up to 8 minutes (480 s) of wall time for a live
demo; that is a limit, not a measurement, and all 12 A/Bs of pilot run 2 were over it.

Pilot run 2, F2 (measured in the course pilot, run 2, 2026-10-16; per-run costs in the table in §7):
agent time 215-242 s (bare) and 265-303 s (harness); harness time 54-64 s; arm cost $0.009195 to
$0.018463. Pilot run 2 as a whole: 24 arm runs for $0.3966, A/B wall time 485-923 s with two A/Bs in
parallel, before two referee speed-ups (each arm judged as soon as it ends; one pytest process for
the unmutated pass step).

The nearest measurement of one A/B alone with board previews is the live console check: `make demo-1
PURPOSE=pilot` (F1, not F2) took 9 min 10 s and cost $0.027821 (A/B `ab-20261016-210339-909651`,
2026-10-16).

[[PENDING: measured wall time and cost per arm for F2 across batch 1 (worst case seen), from exports/scores | source: M8 batch 1 | how: uv run shipharness experiments --split section-2 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

[[PENDING: tonight's wall time (launch to Cost line) and cost for make demo-2 on the class host | source: live class | how: make demo-2]]

---

## 9. Troubleshooting and the replay fallback

| Symptom | Cause in the code | What to do |
|---|---|---|
| `make doctor` reports a key as `missing`, `invalid`, or `unreachable` | `shipharness doctor` checks each key separately (`src/shipharness/doctor.py`) | Fix `.env` at the repo root as the message says; never paste keys on screen |
| `make demo-2` exits 2 before any arm starts | `shipharness ab` refuses a missing or rejected `OPENAI_API_KEY` or a stand-in model client; there is no fallback to a recording (tests in `tests/unit/ab/test_commands.py`) | Fix the key with `make doctor`; if it cannot be fixed on stage, use the replay (below) and say it is a recording |
| `! docker not found: images not built` during `make setup` | No container runtime | Install Docker Engine in WSL2 ([docs/setup-windows.md](../../../docs/setup-windows.md)). `SANDBOX_MODE=none` runs the UNSANDBOXED fallback; every screen then shows "UNSANDBOXED — results not official", so do not use it for the class result |
| An arm line shows `ABORTED: cap` or `ABORTED: timeout` and the command exits 2 | The run hit `MAX_RUN_COST_USD`, `RUN_TIMEOUT_S`, or `HARNESS_TIMEOUT_S` | The referee still judged the run; it is a dot and stays in the results. Say so and go on. Pilot run 2 had one such F2 harness arm (`r-20261016-181736-260803`, timeout in the test phase) |
| The layer switch refuses to start | The session cap (`MAX_SESSION_COST_USD` 2.50, counted from the shared cost ledger `.shipharness/ledger.jsonl`) has no room | Show the ablation dots (§7) instead |
| An arm has no "Session 1 stopped" marker | It called `finish` in session 1; the loop starts a second session only after one that ended by its turn budget (`runner/loop.py`) | Point out that this arm never faced the reset; its migrations are still judged. Pilot run 2 had one (`r-20261016-184318-fdee0c`, `finish(claim="not_done")` on turn 20, the last turn of the budget) |
| Screen 2 says "No board screenshot yet" | The preview container failed to start; this is logged and skipped | Carry on with screens 1 and 3; the referee does not depend on the preview |
| A verdict reads "referee could not judge the build" | The referee container did not start | Check `docker ps` and disk space; rerun the referee with `make replay RUN=<ab_id>`, which judges the recorded diffs again |
| `make swap-2` prints ``x no recorded A/B for section demo-2 under .shipharness/runs; run `make demo-2` first, or pass AB=<id>`` | No demo-2 A/B is recorded on this machine | Run `make demo-2` first, or pass `AB=<id>` |
| `make swap-2` or `make replay` stops with an unpinned-record message | The A/B record has no `checkpoint_sha` | Use a record made after SHA pinning |

### Replay fallback

Use it only when the live run fails on stage:

```sh
ls .shipharness/runs/            # A/B ids start with a sortable time stamp
make replay RUN=<ab or run id>
```

`shipharness replay` re-emits the recorded events with `recorded=True`, so every console screen
shows a red "● RECORDING" badge; applies the recorded diffs to a fresh export of the pinned
checkpoint commit; and runs the referee live with the recorded seed
(`src/shipharness/ab/recorded.py`). No agent model calls are made; the reviewer is off unless you
pass `--reviewer` to `uv run shipharness replay` (listed by `uv run shipharness replay --help`). The
terminal prints `RECORDING: replay <new ab_id> of <source ab_id> (<n> events)` and one line per arm.
Say out loud that it is a recording.

The pilot run 2 A/Bs above predate the continuity fix, so a replay re-judges them with the fixed
check; they are not the class fallback until the integrator picks one. The recorded S2 run to replay
in class:

[[PENDING: run id of the recorded S2 fallback A/B (the class task, demo-2 stack) and the date it was captured | source: M6 pilot | how: course pilot (build repository)]]
