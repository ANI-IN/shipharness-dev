# S2 demo: F2 across a forced session stop

Runbook for the S2 live A/B (`make demo-2`). It follows the brief's demo checklist: purpose,
commands, screen sequence and anchors, poll, what to watch, captured output, experiment results, time
and cost, troubleshooting and replay. In the 50-minute S2 block the demo takes the "live A/B" (15 min)
and "results" (10 min) slots, after concepts and the code walkthrough (DESIGN §14.1).

Everything marked PENDING needs real run output and is filled from the pilot, the
experiment batches, or the class itself. Captured output is labelled "captured on <date>, run <id>;
your output will differ".

---

## 1. Purpose and the problem this demo shows

Both arms build F2, comments on issues ([teamtrack/docs/features/f2.md](../../../teamtrack/docs/features/f2.md)),
from checkpoint `m1-s2-start` (base + F1). The task's session turn budget is `[20, 30]`
([teamtrack/reference/f2/task.toml](../../../teamtrack/reference/f2/task.toml)): if an arm has not
called `finish` after 20 turns, the session stops, and a second session of 30 turns starts with an
empty context. This is the course's way of producing A3's context reset at a fixed point in both arms
(A3, F-a-65; RESEARCH G-5).

The problem: a session that "begins with no memory of what came before" (A2, F-a-08) has to work out
what the first session did. On F2 the cost of guessing wrong is visible: a second Alembic migration
from the old head (two heads, house rule R7), a second `create_table("comments")`, or session 2
removing and rewriting what session 1 wrote.

| Arm | Layers | What it gets at the stop |
|---|---|---|
| bare | none | "This session is ending soon. Turns left in this session: 3." then, in session 2, "A previous session worked on this ticket and was stopped." |
| harness | instructions, state (DESIGN §6.6) | The same two sentences, plus the wrap-up steps (progress, exec plan, handoff notes, commit), a harness-written machine summary in `session-handoff.md`, a session-log entry in `progress.md`, and the Getting up to speed routine in every session |

Everything else is identical: model, effort, tools, ticket, sandbox, turn budgets, wrap-up turns, cost
cap (DESIGN §6.1). The bare arm has the same R7 rule in `docs/HANDBOOK.md`.

Primary measure (registered in DESIGN §8.2): `continuity_failure`, true if (a) R7 fails, (b) two
migrations create the same table, or (c) 30% or more of session 1's added lines are removed in
session 2. See [concepts.md](../concepts.md) §5.

---

## 2. Commands

Run everything inside WSL2 from the repository root (`~/shipharness`). Before class: `make doctor`
passes and `make setup` has built the two images.

| Step | Command | What it does |
|---|---|---|
| Console | `make console` (separate terminal) | Starts the console on port 8765 (`CONSOLE_PORT`); open `http://127.0.0.1:8765/`, then the new A/B under its id |
| Demo | `make demo-2` | `shipharness ab --section demo-2 --feature F2`: F2 canonical, bare vs instructions + state, both arms in parallel, referee on both, blinded reviewer on both diffs |
| Swap test | `make swap-2` | `shipharness ab --swap latest --section demo-2`: re-judges each arm's shipped diff under the other arm's label with the recorded seed and pinned checkpoint commit; no model calls. Prints `Swap test on <ab_id>: judged measures identical` (exit 0) or `DIFFERENT` with the fields that changed (exit 1). `AB=<ab or run id>` picks another A/B |
| Layer switch | `make demo-2 LAYERS=-state` | The same demo with the state layer removed from the section stack: the harness arm runs with `instructions` only (`ab/demo.py`, `section_layers`). A new live A/B: it costs as much as `make demo-2` |
| Replay fallback | `make replay RUN=<ab or run id>` | Only if the live run fails on stage; see §9 |

At the end `make demo-2` prints one header line and one line per arm (`ab/commands.py`,
`_print_record`):

```text
A/B <ab_id> (F2, layers=['instructions', 'state'])
  <arm>  <status>  claim=<claim>  primary={"continuity_failure": ...} passed=<bool> hidden <x>/<N> mutants <k>/<M> reviewer=<verdict> cost=$<usd>
Cost: $<usd> (this command: <model> $<usd>, ...; session $<usd> of $2.50)
```

The line format comes from the code; the values do not exist until the run. Exit code: 0 when both
arms completed, 2 when an arm ended `ABORTED` (cap or timeout), 1 on `ERROR`.

The layer switch fits only if the session meter has room: the class budget leaves room for one
optional rerun at $0.20 (DESIGN §11.3), and `MAX_SESSION_COST_USD` (2.50) blocks it otherwise. If it
does not fit, show the ablation dots instead (§7).

---

## 3. Screen sequence and code anchors

### Code walkthrough (10 min, before the demo)

Open the three S2 anchors (`uv run python scripts/anchors.py extract <id>`):

| Anchor | File | Show |
|---|---|---|
| `S2:init` | `src/shipharness/harness/state/assets/init.sh` (lines 2-29) | Scratch database, `alembic heads` then `upgrade head`, the visible suite with `-x`; the A2 sentence in the header comment |
| `S2:stop_resume` | `src/shipharness/harness/state/lifecycle.py` (lines 80-117) | `session_stop`: machine summary, handoff merge, progress entry, commit, `session_stop` decision; `resume_text` |
| `S2:write` | `src/shipharness/harness/state/progress.py` (lines 11-37) | `session_entry` (index, commits, `ended_by`, turns, files, tests) and `append_session_entry` (restores the heading) |

Also worth a glance: `StateLayer.prepare_workspace` in `src/shipharness/harness/state/layer.py` (the
deterministic initializer step, DESIGN D-11) and `NEUTRAL_RESUME` in `src/shipharness/runner/prompts.py`
(the sentence both arms get).

### Live A/B (15 min)

| When | Key | Screen | Point at |
|---|---|---|---|
| Before the run | | | Poll (§4), then start `make demo-2` |
| First turns | `1` | Live Console | Harness arm: the `note` decision "initializer step: init.sh, progress.md, session-handoff.md, docs/exec-plans/active/F2.md"; its prompt asks for Getting up to speed before any change (`pwd`, `progress.md`, `git log`, `bash init.sh`). Bare arm: only the ticket and the repository |
| Turns 18-20 | `1` | Live Console | Wrap-up at three turns left; harness arm editing `progress.md`, the exec plan, and `session-handoff.md`, then committing. The marker row "■ Session 1 stopped" in each arm's turn list |
| Session 2 starts | `1` | Live Console | "▶ Session 2 resumed". Compare each arm's first five tool calls in session 2: does it read what session 1 left, and does it run `alembic heads` before touching `migrations/versions/`? |
| While session 2 runs | `2` | Boards | Each arm's `/board` page as Acme, refreshed every 5 s from the preview container |
| After the run | `3` | Evidence | "Sessions" list per arm: turns and `ended_by` per session, and "↺ redone" lines for files changed again in a later session |

### Results (10 min)

| Key | Screen | Point at |
|---|---|---|
| `3` | Evidence | Referee list: `continuity` and `r7_migrations` results per arm |
| `4` | A/B Report | S2 dots: tonight's run next to the batch-1 dots (§7). Every run is a dot; read counts, not percentages (DESIGN §8.3) |
| `5` | Traces | First wrong turn per arm (a heuristic: the earliest turn that edited a file a failing check names) and the LangSmith trace link |
| | | Then `make swap-2`, or `make demo-2 LAYERS=-state` if the session meter has room |

---

## 4. Poll question

Ask before `make demo-2`:

> Both agents stop after 20 turns, before F2 is finished, and start again with an empty context. The
> bare agent has the same house rules in its docs, including "exactly one migration head". After the
> second session, which arm ships a migration history with one head and one `comments` table, and
> keeps most of what session 1 wrote?
>
> A. Both arms. B. Only the harness arm. C. Only the bare arm. D. Neither.

Answer pattern from the experiments:

[[PENDING: S2 poll answer pattern: continuity_failure counts per arm out of k=10, split by component (a) R7, (b) duplicate table, (c) redone >= 30%, with run ids | source: M8 batch 1 | how: make experiments BATCH=1 && make report]]

After the run, ask one follow-up: "Which file did the harness arm's session 2 read first, and did it
change what that session did next?"

---

## 5. What to watch

- **The initializer step** (screen 1, harness decisions): one `note` listing the four files, and the
  commit `harness: initializer step for F2`. Nothing like it in the bare arm.
- **Getting up to speed in session 1 and session 2** (screen 1, tool calls): `run pwd`, `read_file
  progress.md`, `run git log --oneline -20`, `read_file session-handoff.md`, `read_file
  docs/exec-plans/active/F2.md`, `run bash init.sh`, `run_visible_tests`. The prompt asks for this
  order; whether the agent follows it is the thing to watch.
- **`init.sh` output in session 2**: the line `== migrations (house rule R7: exactly one head)` followed
  by the heads. If session 1 already added the comments migration, its revision is listed here.
- **Wrap-up**: both arms get "This session is ending soon. Turns left in this session: 3." Only the
  harness arm's message continues with four numbered steps.
- **The stop**: the marker "■ Session 1 stopped" (event `session_stop`, with `ended_by` and the end
  commit); for the harness arm a `session_stop` decision "session 1 handoff written to
  session-handoff.md" and the commit `harness: session 1 handoff for F2`.
- **The handoff's machine summary**: the line `- Migration heads: ...`. With more than one head it ends
  with "house rule R7 needs exactly one".
- **The resume**: "▶ Session 2 resumed" (event `session_resume`, with `prefix_blocks`: `core` for the
  bare arm, `core, instructions, state` for the harness arm).
- **`migrations/versions/` in session 2**: a second new migration file in either arm is the moment to
  point at; it is what parts (a) and (b) catch.
- **Screen 3 "↺ redone"**: a file-level hint (a file changed in session 1 changed again later). Working
  on the same file in session 2 is normal; the judged number is `redone_lines_pct` from the referee
  (post-class reading 03).
- **No stop at all**: if an arm calls `finish(claim="done")` before turn 20, it has no stop markers.
  Say so; parts (a) and (b) still judge its migrations.
- **Exec plan**: in demo-2 the plan stays in `docs/exec-plans/active/`. It moves to `completed/` only
  after the scope layer sets `passes`, which starts in demo-3.
- **Screen 2**: the preview captures the `/board` page. The comments panel is on the issue page
  (`/board/issues/{issue_id}`), which the preview's board view does not open; the referee's hidden
  board tests for F2 (`tests/hidden/f2/test_f2_board.py`, 8 tests) judge the panel.

---

## 6. Captured output and screenshots

Each item is labelled "captured on <date>, run <id>; your output will differ" when filled.

[[PENDING: terminal output of make demo-2 (header, two arm lines, cost line), labelled captured on <date>, run <id> | source: M6 pilot | how: make demo-2]]

[[PENDING: screen 1 Live Console screenshot showing the Session 1 stopped and Session 2 resumed markers for both arms | source: M6 pilot | how: make console, then make demo-2, key 1]]

[[PENDING: screen 2 Boards screenshot of both arms' /board pages during session 2 | source: M6 pilot | how: make console, then make demo-2, key 2]]

[[PENDING: screen 3 Evidence screenshot with the Sessions list per arm (turns, ended_by, redone lines) and the continuity and r7_migrations referee rows | source: M6 pilot | how: make console, then make demo-2, key 3]]

[[PENDING: screen 4 A/B Report screenshot with the S2 dots and this run highlighted | source: M8 batch 1 | how: make console after make experiments BATCH=1, then make demo-2, key 4]]

[[PENDING: screen 5 Traces screenshot with the first wrong turn per arm and the LangSmith link | source: M6 pilot | how: make console, then make demo-2, key 5]]

[[PENDING: harness arm session-handoff.md after session 1 (machine summary and agent notes) and the progress.md session log, from the arm workspace | source: M6 pilot | how: make demo-2, then read .shipharness/runs/<ab_id>/ workspace files]]

[[PENDING: terminal output of make swap-2 | source: M6 pilot | how: make swap-2]]

[[PENDING: terminal output of make demo-2 LAYERS=-state | source: M6 pilot | how: make demo-2 LAYERS=-state]]

---

## 7. Experiment results for this section

Batch 1 runs F1-F4 canonical, two arms, k=10 each, reviewer on (DESIGN §10.4); for S2 that is 10 runs
per arm of F2 canonical with the demo-2 stack.

[[PENDING: S2 dots from batch 1: continuity_failure per run per arm (k=10), components (a)/(b)/(c), redone_lines_pct, sessions, hidden tests passed of 56, run ids, LangSmith comparison link | source: M8 batch 1 | how: make experiments BATCH=1 && make report]]

The ablation batch removes one layer at a time from `all` (A3, F-a-125; DESIGN §10.4). The state row
is the result to show if the live layer switch does not fit the budget:

[[PENDING: ablation dots for -state on the S2 tasks (k=2), with run ids | source: M8 ablation | how: make experiments BATCH=2 && make report]]

---

## 8. Measured time and cost

Limits that apply to every arm (from `src/shipharness/config/settings.py`): `MAX_RUN_COST_USD` $0.20
per arm per run, build and test phases together; `RUN_TIMEOUT_S` 300 s of agent time per arm;
`HARNESS_TIMEOUT_S` 120 s of harness work per arm; `TOOL_TIMEOUT_S` 120 s per tool command;
`MAX_REVIEW_COST_USD` $0.04 per review. The worst case for one `make demo-2` at the caps is
2 × $0.20 + 2 × $0.04 = $0.48. The design target for a demo is 6 minutes or less (DESIGN §16 AS-9);
that is a target, not a measurement.

[[PENDING: measured wall time and cost per arm for make demo-2 (build, test, referee, reviewer), median and worst case seen | source: M6 pilot | how: make pilot]]

[[PENDING: measured wall time and cost per arm for make demo-2 across batch 1 (worst case seen), from exports/scores | source: M8 batch 1 | how: make experiments BATCH=1 && make report]]

[[PENDING: tonight's wall time and cost for make demo-2 | source: live class | how: make demo-2]]

---

## 9. Troubleshooting and the replay fallback

| Symptom | Cause in the code | What to do |
|---|---|---|
| `make doctor` reports a key as `missing`, `invalid`, or `unreachable` | `shipharness doctor` checks each key separately (CONTRACTS §20) | Fix `.env` at the repo root as the message says; never paste keys on screen |
| `! docker not found: images not built` during `make setup` | No container runtime | Install Docker Engine in WSL2 (DESIGN §9). `SANDBOX_MODE=none` runs the UNSANDBOXED fallback; every screen then shows "UNSANDBOXED — results not official", so do not use it for the class result |
| An arm line shows `ABORTED: cap` or `ABORTED: timeout` and the command exits 2 | The run hit `MAX_RUN_COST_USD`, `RUN_TIMEOUT_S`, or `HARNESS_TIMEOUT_S` | The referee still judged the run; it is a dot and stays in the results (DESIGN §8.3 rule 9). Say so and go on |
| The layer switch refuses to start | The session cap (`MAX_SESSION_COST_USD` 2.50, persisted in `.shipharness/session.json`) has no room | Show the ablation dots (§7) instead |
| An arm has no "Session 1 stopped" marker | It called `finish(claim="done")` before turn 20; the loop only stops a session that used its whole budget (`runner/loop.py`) | Point out that this arm never faced the reset; its migrations are still judged |
| Screen 2 says "No board screenshot yet" | The preview container failed to start; this is logged and skipped (CONTRACTS §21) | Carry on with screens 1 and 3; the referee does not depend on the preview |
| A verdict reads "referee could not judge the build" | The referee container did not start (CONTRACTS §21) | Check `docker ps` and disk space; rerun the referee with `make replay RUN=<ab_id>`, which judges the recorded diffs again |
| `make swap-2` prints ``x no recorded A/B for section demo-2 under .shipharness/runs; run `make demo-2` first, or pass AB=<id>`` | No demo-2 A/B is recorded on this machine | Run `make demo-2` first, or pass `AB=<id>` |
| `make swap-2` or `make replay` stops with an unpinned-record message | The A/B record has no `checkpoint_sha` (CONTRACTS §22) | Use a record made after SHA pinning |

### Replay fallback

Use it only when the live run fails on stage (brief §1.1 rule 5):

```sh
ls .shipharness/runs/            # A/B ids start with a sortable time stamp
make replay RUN=<ab or run id>
```

`shipharness replay` re-emits the recorded events with `recorded=True`, so every console screen shows
a red "● RECORDING" badge; applies the recorded diffs to a fresh export of the pinned checkpoint commit;
and runs the referee live with the recorded seed (`src/shipharness/ab/recorded.py`). No agent model
calls are made; the reviewer is off unless you pass `--reviewer` to `uv run shipharness replay`. The
terminal prints `RECORDING: replay <new ab_id> of <source ab_id> (<n> events)` and one line per arm.
Say out loud that it is a recording.

The recorded S2 run to replay in class:

[[PENDING: run id of the recorded S2 fallback A/B (F2 canonical, demo-2 stack) and the date it was captured | source: M6 pilot | how: make demo-2, then note the A/B id printed in the header line]]
