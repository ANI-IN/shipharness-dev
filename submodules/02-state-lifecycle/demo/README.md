# S2 demo: the state layer across a 12-turn session stop

Runbook for the S2 class block (50 minutes). It covers what the demo shows and why, the commands,
the order in class, the console screens, what to watch, the real run that is replayed, the
constructed example, the results to show, time and cost, troubleshooting, and the fallback. Source ids
(A1-A7, F-a-NN) point to [REFERENCES.md](../../../REFERENCES.md).

Captured output is labelled "captured on <date>, run <id>; your output will differ". Everything
quoted comes from recorded pilot runs on the class host (`.shipharness/runs/<ab id>/events.jsonl` and
`exports/scores/<run id>.json`).

---

## 1. What this demo shows, and why

**The task.** F2, comments on issues ([teamtrack/docs/features/f2.md](../../../teamtrack/docs/features/f2.md)),
from checkpoint `m1-s2-start` (base + F1). The task file sets a session turn budget of `[20, 30]`
([teamtrack/reference/f2/task.toml](../../../teamtrack/reference/f2/task.toml)); the class runs it with
`--session-budget 12,38`: the first session stops after 12 turns and a 38-turn session starts with an
empty context. The session turn budget is the course's mechanism, not a source term; it produces A3's
context reset at a fixed point (A3, F-a-65).

**The problem.** A session that "begins with no memory of what came before." (A2, F-a-08) has to work
out what the first session did. On F2 a wrong guess is visible: a second Alembic migration from the
old head (two heads, breaking house rule R7; "house rules" is the course's label for A1's "golden
principles", A1, F-a-99), a second `create_table("comments")`, or session 2 removing and rewriting
what session 1 wrote. The primary measure, `continuity_failure`, fails a run on any of the three
([concepts.md](../concepts.md) §5).

**Why the class does not run a live A/B here.** The pilot found no gap between the arms on this task
(section 8): with the 12-turn first session, no arm of either kind had a continuity failure in run 3
(effort medium, 3 A/Bs), run 4 (effort low, 3 A/Bs), or the class-profile round (1 A/B). The course's
rule is a live A/B only where the pilot shows a real gap; otherwise the section shows the harness
piece doing its job, one real mistake, and one constructed example. So the S2 block has three parts:

| Part | Label on screen and in speech | What it shows |
|---|---|---|
| `show` (section 3) | "harness in action" (console badge "▶ HARNESS IN ACTION — one arm, not an A/B") | The harness arm alone, live: the initializer step, the wrap-up, the handoff written at the stop, session 2 resuming from it |
| `make replay RUN=ab-20261016-213317-9a0ec1` | "real run, replayed" (console badge "● RECORDING") | Pilot run 3: the harness arm gave up the build phase with `finish(claim="not_done")` after the 12-turn first session; the runner fix that followed is the lesson |
| `make example-2` | "constructed example" (console badge "CONSTRUCTED EXAMPLE") | A scripted two-session run with no model: the handoff written at the turn budget, session 2 resuming from it |

The harness arm runs the demo-2 stack, instructions and state (`SECTION_STACKS` in
`src/shipharness/ab/demo.py`). The bare arm, in the pilot's A/Bs, got the same ticket, the same
sentences at the stop ("This session is ending soon. Turns left in this session: 3." and "A previous
session worked on this ticket and was stopped."), and the R7 rule in `docs/HANDBOOK.md`, with none of
the state files.

---

## 2. Before class

Run these from the repository root (`~/shipharness`) inside WSL2.

1. `make doctor` reports both keys and Docker ready, and `.env` sets `SHIPHARNESS_CLASS_DATE` to the
   class day (`--purpose class` needs it).
2. `make warm` builds the images if their source changed, starts the containers, and computes the
   referee and gate baselines, with no model calls (it runs `uv run shipharness warm --profile class
   --images-command "make images RUNTIME=docker"`).
   Measured on the class host on 2026-10-17 before the class-profile round: first run 407 s (images
   rebuilt 145 s, 7 referee and 4 gate baselines), second run 1.2 s.
3. Check that the two recorded runs this block needs are on the host:

   ```sh
   ls .shipharness/runs/ab-20261016-213317-9a0ec1 .shipharness/runs/ab-20261017-085139-7c0661
   ```

   Each folder has `ab.json`, `events.jsonl`, `bare/`, and `harness/`. The first is the showcase
   (section 6); the second is the fallback for the live run (section 11).
4. Run `make replay RUN=ab-20261016-213317-9a0ec1 PURPOSE=pilot` once and note how long it takes on
   this host (the referee judges both arms), so you know when to launch it in class (section 4).

---

## 3. Commands

| Step | Command | What it runs |
|---|---|---|
| Console | `make console` (terminal A) | `uv run shipharness console --port 8765`; open `http://127.0.0.1:8765/` |
| Harness in action | `uv run shipharness ab --section demo-2 --feature F2 --arms harness --session-budget 12,38 --purpose class --profile class` (terminal B) | The harness arm alone (instructions + state) on F2 with a 12-turn first session, the class profile (effort low, OpenAI's Fast tier, 2 CPUs per container), the referee, and the reviewer. Not an A/B: its record stays out of the bare-vs-harness comparison and the swap test |
| Real run, replayed | `make replay RUN=ab-20261016-213317-9a0ec1` | `uv run shipharness replay ab-20261016-213317-9a0ec1 --purpose class`: re-emits the recorded events (RECORDING on every screen), applies the recorded diffs to a fresh export of the pinned checkpoint commit, and runs the referee live. No agent model calls; the reviewer is off unless you pass `--reviewer` |
| Constructed example | `make example-2` | `shipharness example --section demo-2`: scripted steps, no model, "CONSTRUCTED EXAMPLE" on every console screen |
| Fallback for the live run | `make replay RUN=ab-20261017-085139-7c0661` | The class-profile round's F2 A/B, replayed (section 11) |

**Why not `make show-2`.** `make show-2` runs `uv run shipharness ab --section demo-2 --feature F2
--arms harness --purpose class --profile class`, and at this commit it does not pass
`SESSION_BUDGET`: `make -n show-2 SESSION_BUDGET=12,38` prints the same line with no
`--session-budget`, so the first session would be 20 turns. `make demo-2 SESSION_BUDGET=12,38` does
pass it (`--session-budget=12,38`), but that is the two-arm A/B. Use the full command above.

Checked on 2026-10-17 at commit d132507, with commands that make no model calls: `make -n show-2
SESSION_BUDGET=12,38`, `make -n demo-2 SESSION_BUDGET=12,38`, `make -n replay
RUN=ab-20261016-213317-9a0ec1`, `make -n console`, `uv run shipharness ab --help` (lists `--arms`,
`--session-budget`, `--profile`), and `uv run shipharness replay --help`. The live commands and
`make example-2` were not run for this runbook.

At the end the live command prints a header, one line for the harness arm, and the cost line
(format from `src/shipharness/ab/commands.py`, `_print_record`, and `ab/runtime.py`, `cost_line`):

```text
A/B <ab_id> (F2, layers=['instructions', 'state'], profile=class, harness in action)
  harness  <status>  claim=<claim>  primary={"continuity_failure": ...} passed=<bool> hidden <x>/56 mutants <k>/4 reviewer=<verdict> cost=$<usd>
Cost: $<usd> (this command: <model> $<usd>, ...; session $<usd> of $2.50; build $<usd> of $15.00 ($<usd> left))
```

Exit code: 0 when the arm completed, 2 when it ended `ABORTED` (cap or timeout), 1 on `ERROR`.

[[CAPTURE: terminal output of the S2 harness-in-action run (header, harness line, Cost line), its wall time from launch to the Cost line, and its cost | how: uv run shipharness ab --section demo-2 --feature F2 --arms harness --session-budget 12,38 --purpose class --profile class]]

---

## 4. Order in class

The block follows the class's section pattern ([instructor guide, "Section
pattern"](../../../docs/instructor-guide.md#section-pattern)), with the live run in place of the A/B.

| Section minutes | Block | Terminal and console |
|---|---|---|
| 0-3 | Poll (section 5) | Close the poll before the launch |
| 3-5 | Launch | Terminal B: the harness-in-action command. Open the newest run on screen `1`: the badges and the initializer step |
| 5-20 | Concepts ([../concepts.md](../concepts.md)) | The run goes on in the background |
| 20-30 | Code walkthrough (anchors below) | At minute 20, if terminal B shows the `Cost:` line, launch `make replay RUN=ab-20261016-213317-9a0ec1` so its referee runs during the walkthrough; otherwise launch it at minute 25 |
| 30-36 | Demo block 1: harness in action | The finished run: screens `1`, `3`, `5` (section 6) |
| 36-41 | Demo block 2: real run, replayed | The replay: screens `1` and `3`, then the runner code (section 7) |
| 41-45 | Demo block 3: constructed example, and every result | `make example-2` (section 8); then screen `4` and the results slide (section 9) |
| 45-50 | Discussion | Poll answer, follow-up question |

Timing: in the class-profile round (2026-10-17, A/B `ab-20261017-085139-7c0661`), the F2 harness arm
reached its primary verdict 358 s after launch and its full verdict 533 s after launch. A run started
at section minute 3 at that pace finishes around minute 12. Run one live command at a time: the
replay waits for the live run's `Cost:` line.

### Code walkthrough (minutes 20-30)

Print each anchor with `uv run python scripts/anchors.py extract <id>`:

| Anchor | File | Show |
|---|---|---|
| `S2:init` | `src/shipharness/harness/state/assets/init.sh` (lines 2-29) | Scratch database, `alembic heads` then `upgrade head`, one end-to-end test file with `-x` |
| `S2:stop_resume` | `src/shipharness/harness/state/lifecycle.py` (lines 95-134) | `session_stop`: machine summary, handoff merge, progress entry, commit; `resume_text` |
| `S2:write` | `src/shipharness/harness/state/progress.py` (lines 11-37) | `session_entry` and `append_session_entry` (restores the heading) |

Also worth a glance: `getting_up_to_speed` and `wrapup_text` at the top of `lifecycle.py`, and
`NEUTRAL_RESUME` in `src/shipharness/runner/prompts.py` (the sentence both arms get).

---

## 5. Poll question

Ask before the launch:

> In the course pilot both agents built F2 with a first session stopped after 12 turns and a fresh
> 38-turn session after it. The bare agent had no progress file, no handoff, and no exec plan. Over
> six A/Bs, which arm had more continuity failures (two migration heads, a second `comments` table,
> or 30% of session 1's lines redone)?
>
> A. The bare arm. B. The harness arm. C. Neither arm had any. D. Both had several.

Answer, after the demo block: C. `continuity_failure` was false in all 12 arms of runs 3 and 4, and
in both arms of the class-profile round (section 9). Then say what the pass does not show: six of
those arms built nothing (3 of 56 hidden tests), and the measure cannot fail when session 1 leaves no
product lines to redo.

Follow-up for the discussion: "The bare arm found session 1's work with `git status`. Which state
file would you keep for this model, and how would you measure it?"

---

## 6. Harness in action: what to watch

**Screens.** Every screen shows the badges "▶ HARNESS IN ACTION — one arm, not an A/B" and
"profile: class". On screen `1` the bare panel reads "Not run: harness in action shows the harness
arm alone. The bare-vs-harness comparison comes from the A/B runs (make demo-N)."
(`src/shipharness/console/templates/screens/`). There are no BLOCKED lines and no gate pills: the
scope layer starts in demo-3 and the verification gate in demo-4.

| Key | Screen | Point at |
|---|---|---|
| `1` | Live Console | The initializer step (decision "initializer step: init.sh, progress.md, session-handoff.md, docs/exec-plans/active/F2.md"), the Getting up to speed calls, the wrap-up at turn 10, the marker "■ Session 1 stopped", the decision "session 1 handoff written to session-handoff.md", the marker "▶ Session 2 resumed", and the first calls of session 2. Then the referee line: "primary verdict ready: PASS" (or FAIL) with `continuity_failure`, and the time from launch to the primary and full verdicts |
| `3` | Evidence | The "Sessions" list: turns and `ended_by` per session, "↺ redone" hints; the referee rows `continuity` and `r7_migrations` |
| `5` | Traces | The LangSmith trace link; in session 2, the first five tool calls: does the agent read what session 1 left before writing code? |
| `2` | Boards | One frame of `/board`. The comments panel is on the issue page, which the preview does not open; the hidden board tests judge it |

**What it looked like in the class-profile round** (captured on 2026-10-17, run
`r-20261017-085139-9dfb9d` in `ab-20261017-085139-7c0661`, the harness arm's events, cut where `...`
stands; your output will differ):

```text
[decision] note state: initializer step: init.sh, progress.md, session-handoff.md, docs/exec-plans/active/F2.md
s1 t 1 run pwd; cat progress.md; git log --oneline -20; cat session-handoff.md; cat docs/exec-pl ...
s1 t 3 read_file docs/features/f2.md
s1 t 4 read_file docs/HANDBOOK.md
...
s1 t10 apply_patch progress.md
s1 t11 apply_patch docs/exec-plans/active/F2.md
s1 t12 apply_patch session-handoff.md
[decision] session_stop state: session 1 handoff written to session-handoff.md
[session_stop] {"session_index": 1, "ended_by": "turn_budget", "end_sha": "61d2480...", "handoff_path": "session-handoff.md"}
[session_resume] {"session_index": 2, "start_sha": "e5de4b0...", "prefix_blocks": ["core", "instructions", "state"]}
s2 t 1 run pwd && cat progress.md && git log --oneline -20 && cat session-handoff.md && cat docs ...
...
s2 t16 list_dir migrations/versions
...
s2 t22 run alembic heads && cat migrations/versions/0001_initial.py | head -30; cat app/api/deps ...
s2 t23 apply_patch migrations/versions/0002_comments.py
```

Things to point at, in that order:

- **Session 1 spent its 12 turns reading and on the wrap-up.** Nine turns of orientation, then the
  three wrap-up turns on `progress.md`, the exec plan, and the handoff. No product code yet. That is
  the cost A3 names for resets, "orchestration complexity, token overhead, and latency" (A3, F-a-68).
- **The stop.** `ended_by` is `turn_budget`, and the harness wrote its machine summary and session-log
  line whatever the agent did (`session_stop`, anchor `S2:stop_resume`).
- **The resume.** `prefix_blocks` lists `core, instructions, state`; the first call of session 2 reads
  `progress.md`, the git log, the handoff, and the exec plan, A2's Getting up to speed (A2, F-a-59).
- **The migration.** Before writing `0002_comments.py` the agent ran `alembic heads`: one head, so no
  second migration. That is what parts (a) and (b) of the measure check.
- **If the agent calls `finish(claim="not_done")` in session 1.** Since the runner fix (section 7),
  session 2 still starts; the stop marker then shows `ended_by` `claim_not_done`. Say that this is the
  fix working live. After `finish(claim="done")` in session 1 there is no stop: say so, and let the
  constructed example show the stop instead.

The class-profile round's harness arm then built the feature in session 2 (56 of 56 hidden tests,
`continuity_failure` false; section 9).

---

## 7. Real run, replayed: the early finish in pilot run 3

`make replay RUN=ab-20261016-213317-9a0ec1` replays A/B `ab-20261016-213317-9a0ec1` (pilot run 3,
2026-10-16, F2 canonical with `--session-budget 12,38`, effort medium). Say "real run, replayed"; every
screen shows "● RECORDING". The recorded events arrive at once; the referee then judges the recorded
diffs again, live. Screen `2` stays empty: the pilot ran without board previews.

The harness arm's events (captured on 2026-10-16, run `r-20261016-213317-a33b07`, cut where `...`
stands; your output will differ):

```text
s1 t 1 run pwd && cat progress.md && printf '\n--- GIT LOG ---\n' && git log --oneline -20
...
s1 t 5 run bash init.sh
s1 t 6 run_visible_tests
s1 t 7 read_file docs/features/f2.md
s1 t 8 read_file docs/HANDBOOK.md
s1 t 9 read_file .agents/skills/add-endpoint/SKILL.md
s1 t10 apply_patch progress.md, docs/exec-plans/active/F2.md, session-handoff.md
s1 t11 run git add progress.md docs/exec-plans/active/F2.md session-handoff.md && git commit -m  ...
s1 t12 finish not_done
[claim] {"phase": "build", "claim": "not_done", "summary": "Completed initial F2 orientation and recorded the next steps and implementation rules in progress.md, the execution plan, and session-handoff.md. ... No feature implementation has started; the handoff describes remaining work.", ...}
[decision] session_stop state: session 1 handoff written to session-handoff.md
s2 t 1 run pwd && git log --oneline -20 && ls
...
[verdict] {"primary": {"continuity_failure": false}, "passed_primary": true, "summary": "agent said not_done; referee: passes the primary measure; hidden tests 3/56, mutants killed 0/4, R1 new 0"}
```

What to say:

1. **What happened.** On its last turn of session 1 the agent called `finish(claim="not_done")`. Under
   the runner's rule at the time, any `finish` ended the build phase, so the 38-turn session never
   ran. The `s2` lines are the test phase, not a second build session. The arm built nothing: 3 of 56
   hidden tests (the 3 that pass on the checkpoint).
2. **What the measure said.** `continuity_failure` false: a pass. Session 1 left no product lines,
   so nothing could be redone. A pass says nothing was broken or redone, not that the feature was
   built.
3. **It was not only the harness arm.** The same early finish ended the build phase in the harness arm
   of `ab-20261016-214959-de790f` (run 3), and in run 4 (effort low) in all three bare arms
   (`ab-20261016-232842-ac03b2`, `ab-20261016-234027-226a76`, `ab-20261016-235211-ea59a9`) and the
   harness arm of `ab-20261016-234027-226a76`, after 9 to 12 turns. In this A/B the bare arm ran its
   first session to the turn budget and built the feature in the second (56 of 56 hidden tests).
4. **The fix, for both arms.** Before the last build session, `finish(claim="not_done")` ends only
   that session; the next one starts as after a spent turn budget. The last build session and the
   test phase keep the old rule. From `src/shipharness/runner/loop.py`, lines 99-104:

   ```python
   def _next_session_runs(phase: Phase, ended_by: str) -> bool:
       """Whether the phase goes on to its next session (if it has one). A spent turn budget always
       does. In the build phase, a finish(claim="not_done") ends only that session: before the last
       build session it means "out of turns here", not "give up" (pilot runs 3 and 4, F2, both arms).
       Every other ending (done, timeout, cap, error, no tool call) ends the phase."""
       return ended_by == "turn_budget" or (phase == "build" and ended_by == "claim_not_done")
   ```

   Its tests are in `tests/unit/test_loop.py` (`test_not_done_before_the_last_build_session_ends_only_that_session`
   and the two tests after it). The replay shows the recorded run, so it still shows the old rule.
5. **The lesson.** The harness was not the only code with an assumption about the model: the runner
   assumed `finish` means "stop the phase". Reading the run, not only the verdict, found it.

---

## 8. Constructed example: `make example-2`

Say "constructed example": a scripted two-session run with no model. The first session ends at its
turn budget, the state layer writes the handoff, and session 2 resumes from it. Every console screen
shows "CONSTRUCTED EXAMPLE". Use it to show the stop and the resume step by step, or when the live
run had no stop.

[[CAPTURE: terminal output and wall time of the S2 constructed example, and the console screen 1 view of its stop and resume | how: make example-2]]

Point at the handoff written at the stop (the decision "session 1 handoff written to
session-handoff.md"), the "▶ Session 2 resumed" marker, and the first call of session 2 reading the
handoff.

---

## 9. Every result, as measured

Show these on screen `4` and the results slide, wins and "no measurable difference" alike. Screen 4
lists the harness-in-action run under "single-arm run (harness in action) not compared: no bare run".

| Round | Budget, effort | A/Bs | Bare: no continuity failure | Harness: no continuity failure | Hidden tests 56 of 56, bare / harness |
|---|---|---|---|---|---|
| Run 2, 2026-10-16 | 20/30, medium | 3 | 3/3 | 0/3 (measurement bug, fixed since) | 1 of 3 / 0 of 3 |
| Run 3, 2026-10-16 | 12/38, medium | 3 | 3/3 | 3/3 | 3 of 3 / 1 of 3 |
| Run 4, 2026-10-16/17 | 12/38, low | 3 | 3/3 | 3/3 | 0 of 3 / 2 of 3 |
| Class-profile round, 2026-10-17 | 12/38, low, Fast tier | 1 | 1/1 | 1/1 | 1 of 1 / 1 of 1 |

On the primary measure: no measurable difference on this task with this model (course pilot, runs 3
and 4 and the class-profile round). The course's planned experiment batches (10 runs per arm, and a
leave-one-layer-out ablation) were not run, because the pre-registered pilot gate did not pass; these
runs are the data.

Post hoc (chosen after the results; descriptive, 9 runs per arm, runs 2 to 4): harness arms hit the
agent time limit in 4 runs, bare arms in 0; median arm wall time 361 s against 232 s; median tests
shipped 0 against 8; median cost per arm $0.0132 against $0.0171.

### Per-run dots, runs 3 and 4 and the class-profile round

From the A/B records and score records (captured on 2026-10-16 and 2026-10-17, runs as listed; your
output will differ). Sessions and turns count every session of the arm, the test phase included.

| Round | A/B | Arm | Run id | Status | `continuity_failure` | `redone_lines_pct` | Hidden (of 56) | Sessions | Turns | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | `ab-20261016-211419-dfe06f` | bare | `r-20261016-211419-22afc9` | completed | false | 0.0 | 56 | 3 | 62 | 0.0186 |
| 3 | `ab-20261016-211419-dfe06f` | harness | `r-20261016-211419-3f4a1c` | ABORTED: timeout | false | 0.0 | 56 | 3 | 58 | 0.0186 |
| 3 | `ab-20261016-213317-9a0ec1` | bare | `r-20261016-213317-97004c` | completed | false | 5.3 | 56 | 3 | 62 | 0.0171 |
| 3 | `ab-20261016-213317-9a0ec1` | harness | `r-20261016-213317-a33b07` | completed | false | 0.0 | 3 | 2 | 24 | 0.0054 |
| 3 | `ab-20261016-214959-de790f` | bare | `r-20261016-214959-c2f640` | completed | false | 0.0 | 56 | 3 | 62 | 0.0185 |
| 3 | `ab-20261016-214959-de790f` | harness | `r-20261016-214959-1deb1e` | ABORTED: timeout | false | 0.0 | 3 | 2 | 22 | 0.0032 |
| 4 | `ab-20261016-232842-ac03b2` | bare | `r-20261016-232842-16089d` | completed | false | 0.0 | 3 | 2 | 20 | 0.0050 |
| 4 | `ab-20261016-232842-ac03b2` | harness | `r-20261016-232842-ee62c3` | ABORTED: timeout | false | 0.0 | 56 | 3 | 44 | 0.0132 |
| 4 | `ab-20261016-234027-226a76` | bare | `r-20261016-234027-e3c2b2` | completed | false | 0.0 | 3 | 2 | 21 | 0.0058 |
| 4 | `ab-20261016-234027-226a76` | harness | `r-20261016-234027-92eb41` | completed | false | 0.0 | 3 | 2 | 24 | 0.0064 |
| 4 | `ab-20261016-235211-ea59a9` | bare | `r-20261016-235211-d597c7` | completed | false | 0.0 | 3 | 2 | 24 | 0.0056 |
| 4 | `ab-20261016-235211-ea59a9` | harness | `r-20261016-235211-0b643c` | completed | false | 0.0 | 56 | 3 | 62 | 0.0183 |
| class | `ab-20261017-085139-7c0661` | bare | `r-20261017-085139-93cdec` | completed | false | 0.0 | 56 | 3 | 57 | 0.0329 |
| class | `ab-20261017-085139-7c0661` | harness | `r-20261017-085139-9dfb9d` | completed | false | 0.0 | 56 | 3 | 62 | 0.0357 |

In the class-profile round the bare arm's build sessions ran 12 turns (turn budget) and 33 (claimed
done); the harness arm's 12 and 38, both ended by the turn budget. The bare arm changed one file
outside the allowed paths, the harness arm none (a secondary count; the demo-2 stack has no scope
layer). Mutants killed: bare 2 of 4, harness 0 of 4.

### Run 2 dots (before the continuity fix)

Captured on 2026-10-16, runs as listed; your output will differ. The harness arm's
`continuity_failure` and `redone_lines_pct` were scored before the fix and count the harness's own
files; they are the measurement bug ([post-class reading 03](../post-class-reading/03-the-continuity-measure.md)),
not a result.

| A/B | Arm | Run id | `continuity_failure` | `redone_lines_pct` | Hidden (of 56) | Build sessions, ended by | Cost (USD) |
|---|---|---|---|---|---|---|---|
| `ab-20261016-181736-08a9c4` | bare | `r-20261016-181736-a05ddb` | false | 2.1 | 55 | 20 turn_budget, 30 claim_not_done | 0.018463 |
| `ab-20261016-181736-08a9c4` | harness | `r-20261016-181736-260803` | true (bug) | 84.0 | 3 | 20 turn_budget, 30 turn_budget; ABORTED: timeout in the test phase | 0.016612 |
| `ab-20261016-184318-636e90` | bare | `r-20261016-184318-a7c11c` | false | 0.0 | 56 | 20 turn_budget, 30 turn_budget | 0.016186 |
| `ab-20261016-184318-636e90` | harness | `r-20261016-184318-fdee0c` | true (bug) | 76.5 | 3 | 20 claim_not_done (no stop) | 0.009195 |
| `ab-20261016-190548-ae9abe` | bare | `r-20261016-190548-3c5d9d` | false | 0.0 | 55 | 20 turn_budget, 30 turn_budget | 0.017546 |
| `ab-20261016-190548-ae9abe` | harness | `r-20261016-190548-9352c4` | true (bug) | 50.0 | 3 | 20 turn_budget, 30 turn_budget | 0.015149 |

---

## 10. Time and cost

Limits for every arm (`src/shipharness/config/settings.py`): `MAX_RUN_COST_USD` $0.20 per arm per
run; `RUN_TIMEOUT_S` 300 s of agent time; `HARNESS_TIMEOUT_S` 120 s of harness work; `TOOL_TIMEOUT_S`
120 s per tool command; `MAX_REVIEW_COST_USD` $0.04 per review; `MAX_SESSION_COST_USD` $2.50 for the
class. The worst case for the harness-in-action run at the caps is $0.20 + $0.04 = $0.24. The
replay and the constructed example make no model calls.

Nearest measurement: the class-profile round's F2 harness arm (2026-10-17, A/B
`ab-20261017-085139-7c0661`): 254 s of agent time, primary verdict 358 s and full verdict 533 s after
launch, arm cost $0.0357 plus $0.0041 for the review. Harness work runs on its own clock after the
agent's turns: each session-end handoff runs the visible suite, about 31-34 s on this host. Tonight's
time and cost come from the capture in section 3.

---

## 11. Troubleshooting and fallback

| Symptom | Cause | What to do |
|---|---|---|
| The live command exits 2 before the arm starts | `shipharness ab` refuses a missing or rejected `OPENAI_API_KEY` or a stand-in model client; there is no fallback to a recording (`tests/unit/ab/test_commands.py`) | Fix the key with `make doctor`; if that cannot be done on stage, use the fallback below and say it is a recording |
| It refuses to start with a message about the class date | `--purpose class` needs `SHIPHARNESS_CLASS_DATE` in `.env` | Set it to today's date, or run with `--purpose pilot` and say the trace goes to the pilot project |
| The first session runs 20 turns, not 12 | The run was started with `make show-2`, which does not pass `SESSION_BUDGET` | Let it run (the stop still happens at turn 20), and use the full command next time |
| No "Session 1 stopped" marker | The agent called `finish(claim="done")` in session 1, or the run hit a cap or the time limit | Say the arm never faced the reset; show the stop in the constructed example |
| The arm line shows `ABORTED: timeout` or `ABORTED: cap` and the command exits 2 | `RUN_TIMEOUT_S`, `HARNESS_TIMEOUT_S`, or `MAX_RUN_COST_USD` | The referee still judges the run. In run 3 two of three F2 harness arms hit the agent time limit (section 9). Say so and go on |
| `make replay` says it cannot find the run | The recorded folder is not under `.shipharness/runs/` on this host | Check with the `ls` in section 2; copy the folder from the machine that recorded it |
| `make replay` stops with an unpinned-record message | The record has no `checkpoint_sha` | Both runs named here are pinned; check the id |
| `make example-2` is not found | The Makefile on this host predates the target | Skip the constructed example; show screen `1` of the live run's stop instead |
| Screen 2 says "No board screenshot yet" | The preview did not start, or the run had no previews (the replayed pilot run) | Carry on with screens `1` and `3`; the referee does not use the preview |
| The session cap blocks a command | `MAX_SESSION_COST_USD` counted from `.shipharness/ledger.jsonl` | The replay and the constructed example need no budget; use them |

**Fallback when the live run fails on stage.** Say "this run failed for a reason outside the
experiment; here is the recorded run from the class-profile round", then:

```sh
make replay RUN=ab-20261017-085139-7c0661
```

It replays both arms of that A/B (RECORDING on every screen): the harness arm's sessions of 12 and
38 turns, the stop and resume shown in section 6, and the bare arm next to it. If Docker is down, the
replay cannot run (the referee needs a container): open `http://127.0.0.1:8765/run/ab-20261017-085139-7c0661`
instead. Those are the original events, so there is no RECORDING badge; say it before you switch.
The instructor guide's [replay procedure](../../../docs/instructor-guide.md#replay-procedure) has the
full steps.
