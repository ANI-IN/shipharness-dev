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
| Browser tab 1 | Slides |
| Browser tab 2 | Console: the runs list at `http://127.0.0.1:8765/`, then the current A/B at `/run/<ab id>` |
| Browser tab 3 (optional) | LangSmith, signed in, project `shipharness-class-<date>` (DESIGN §12) |

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
stamp). The runs list does not refresh by itself.

---

## Minute-by-minute

Times are elapsed from the start of class. Slide numbers refer to
[../slides/outline.md](../slides/outline.md).

| Time | Block | What happens | Command or screen | Slides |
|---|---|---|---|---|
| 0:00-0:03 | Opening: problem | Title; four failures; one real failure on the board, from a recorded run, labelled as recorded | Slide 2 image | 1-2 |
| 0:03-0:05 | Opening: why | Four causes, cited | | 3 |
| 0:05-0:07 | Opening: solution | The harness: four parts plus the sandbox | Architecture diagram | 4 |
| 0:07-0:10 | Opening: tour | shipharness, TeamTrack, console tour (keys 1-5); `Opening:two_arms` and `Opening:publish` briefly; how we prove it; `make doctor`; `harness-setup` assessment | Terminal B, console tab | 5-7 |
| 0:10-0:25 | S1 concepts | Problem, cause, harness piece | | 8-13 |
| 0:25-0:35 | S1 walkthrough | `S1:agents_md`, `S1:progressive`, `S1:prefix` | Editor | 14-16 |
| 0:35-0:37 | S1 live | Feature F1, rule R1 at risk; glance at control C1 | | 17 |
| 0:37-0:39 | S1 live | Poll S1 | | 18 |
| 0:39-0:50 | S1 live | `make demo-1`; screens 1, 2, 3 | Console | 19 |
| 0:50-0:57 | S1 results | Screen 4; `make swap-1` | Console, terminal B | 20 |
| 0:57-1:00 | S1 results | Discussion; transition | | 21 |
| 1:00-1:15 | S2 concepts | | | 22-26 |
| 1:15-1:25 | S2 walkthrough | `S2:init`, `S2:stop_resume`, `S2:write` | Editor | 27-29 |
| 1:25-1:27 | S2 live | Feature F2, R7 and continuity at risk; glance at control C2 | | 30 |
| 1:27-1:29 | S2 live | Poll S2 | | 31 |
| 1:29-1:40 | S2 live | `make demo-2`; screens 1, 2, 3 (and 5) | Console | 32 |
| 1:40-1:47 | S2 results | Screen 4; `make swap-2` | Console, terminal B | 33 |
| 1:47-1:50 | S2 results | Discussion; optional layer switch started (rules below) | | 34 |
| 1:50-2:00 | Break | Return time on screen | | 35 |
| 2:00-2:15 | S3 concepts | Includes two sandbox slides | | 36-41 |
| 2:15-2:25 | S3 walkthrough | `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile` | Editor | 42-43 |
| 2:25-2:27 | S3 live | Feature F3, scope at risk; glance at control C3 | | 44 |
| 2:27-2:29 | S3 live | Poll S3 | | 45 |
| 2:29-2:40 | S3 live | `make demo-3`; screens 1, 2, 3 | Console | 46 |
| 2:40-2:47 | S3 results | Sandbox moment; screen 4; `make swap-3` | Console, terminal B | 47 |
| 2:47-2:50 | S3 results | Discussion; transition | | 48 |
| 2:50-3:05 | S4 concepts | | | 49-54 |
| 3:05-3:15 | S4 walkthrough | `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate` | Editor | 55-57 |
| 3:15-3:17 | S4 live | Feature F4, hidden tests and mutants; glance at control C4 | | 58 |
| 3:17-3:19 | S4 live | Poll S4 | | 59 |
| 3:19-3:30 | S4 live | `make demo-4`; screens 1, 2, 3 | Console | 60 |
| 3:30-3:37 | S4 results | Screen 4; `make swap-4` | Console, terminal B | 61 |
| 3:37-3:40 | S4 results | Discussion; transition | | 62 |
| 3:40-3:41 | Final | Feature poll | | 63 |
| 3:41-3:45 | Final | `make final FEATURES=<poll winner>` | Terminal B | 64 |
| 3:45-3:48 | Final | All screens | Console | 65 |
| 3:48-3:50 | Final | Both boards | Console screen 2 | 66 |
| 3:50-3:53 | Final | Report and LangSmith comparison; `Final:dots` | `make report`, LangSmith tab | 67 |
| 3:53-3:56 | Wrap-up | Assignments | | 68-69 |
| 3:56-3:58 | Wrap-up | Skills and templates to take home; `Final:skill_template` | | 70 |
| 3:58-4:00 | Wrap-up | References | | 71-72 |

The measured length of each demo decides how much of the 11-minute run slot is waiting:

[[PENDING: wall time of make demo-1 to demo-4 and of one make final feature on the class host | source: M6 pilot | how: time make demo-N; VERIFICATION.md demo times]]

If a run is still going at the end of its slot, move to the results slide, show the experiment dots,
and add tonight's dot when the terminal prints it. If it fails, follow
[Replay procedure](#replay-procedure).

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

Every section runs the same way (DESIGN §14.1):

1. **Concepts (15 min).** Problem seen live, then cause, then harness piece.
2. **Walkthrough (10 min).** Anchors in [code-walkthrough.md](code-walkthrough.md).
3. **Live A/B (15 min).**
   - Feature, rule at risk, command (slide). Glance at the section's easy control task: show its
     ticket, say "both arms should pass this one", and point at its experiment results.
   - Poll ([poll-questions.md](poll-questions.md)). Close the poll before you start the run.
   - Terminal B: `make demo-N`. Reload the runs list, open the newest `ab-...`, then screens `1`, `2`,
     `3` as below.
4. **Results (10 min).** Screen `4`, the swap test (`make swap-N`), discussion. Screen 4 currently
   groups dots by variant and arm across all features (see known failure modes); until that changes,
   refresh `exports/report.html` with `make report` (or `uv run shipharness report` while the target
   is still the placeholder) after the run and show the rows for the section's feature there.

What the terminal prints at the end of `make demo-N` (format from `src/shipharness/ab/commands.py`):
one line `A/B <ab id> (<feature>, layers=[...])`, then one line per arm with status, claim, primary
measure, `passed=`, hidden tests passed of total, mutants killed of total, reviewer verdict, and
cost, then the cost line `Cost: $... (this command: ...; session $... of $2.50)`. Read the session
figure aloud after each run; it is the meter for the rest of the class.

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

**Control glance.** C1, filter the user list by role (`teamtrack/docs/features/c1.md`).

[[PENDING: C1 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Command.** `make demo-1`

**Screens during the run and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` Live Console | Turn list: `read_file` calls on the documents the map points to, skill files, and state files are highlighted; compare the bare arm's first reads (does it open `docs/HANDBOOK.md`?) | "Same ticket, same tools, same handbook on disk. Watch which files each arm opens before it writes code." |
| 1 | `1` | "Harness decisions": the bare arm says "None: bare arm has no layers." | "The bare arm is not handicapped: every rule is in `docs/HANDBOOK.md`. What differs is whether the agent is pointed at it." |
| 2 | `2` Boards | Screenshots as Acme every 5 s; ⚠ "other org" marks on cards | "The marks come from `data-org` attributes on every card, checked by a trusted script, not by the arm's code (DESIGN §4.4)." |
| 3 | `3` Evidence | "Files read" per arm by category (map, skill, harness doc, state, handbook, code, test); after the run, the referee list with R1 new violations | "The referee probes every endpoint as Acme with Globex ids and expects 404 (DESIGN §5). It does not care which arm wrote the code." |
| 1 | `1` | "Agent said" vs "Referee" at the end | "Both arms may say done. The referee decides." |

**Results (0:50-1:00).**
1. Screen `4`. Tonight's two dots next to the experiment dots.

[[PENDING: S1 experiment dots, runs failing out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

2. Terminal B: `make swap-1`. It re-judges each recorded diff under the other arm's label; expect
   `Swap test on <ab id>: judged measures identical`. Cost $0 (no model calls). Say: "The referee
   judges code, not labels."
3. Discussion: "The bare arm could read the same rules. Why did it (or did it not) apply them?" Tie
   back to cause 1 (A1, F-a-05).
4. Transition: link `submodules/01-instructions/demo/README.md`; next problem: what happens when a
   session ends halfway.

---

## S2 State and session lifecycle (1:00-1:50)

**Feature and rule.** F2, comments on issues with a comments panel on the board, from `m1-s2-start`,
two sessions with budgets `[20, 30]` (`teamtrack/reference/f2/task.toml`): session 1 is stopped after
20 turns, both arms get the same wrap-up turns (`WRAPUP_TURNS`, default 3) and the same neutral resume
sentence (DESIGN §6.3). Primary measure: continuity failure, any of R7 failing, a second migration
creating the same table, or ≥ 30% of session-1 lines removed in session 2 (DESIGN §8.2). Harness arm
layers: instructions, state.

**Control glance.** C2, search projects by name (`teamtrack/docs/features/c2.md`).

[[PENDING: C2 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Command.** `make demo-2`

**Screens during the run and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | "■ Session 1 stopped" and "▶ Session 2 resumed" markers in both arms | "This stop is the session turn budget, the same for both arms. A3 calls the pattern a context reset with a structured handoff (A3, F-a-65; RESEARCH G-5)." |
| 1 | `1` | Harness arm's first turns after resume: `progress.md`, `git log`, `init.sh`, visible tests | "That is A2's Getting up to speed routine (A2, F-a-58 to F-a-62). The bare arm got the same resume sentence and nothing else." |
| 2 | `2` | Comments panel on each board after resume | "Did the second session finish what the first started, or start again?" |
| 3 | `3` | "Sessions" per arm, with ↺ redone files | "Redone work is the cost of forgetting." |
| 4 | `5` Traces | "First wrong turn" per arm | "Look for the first turn that went wrong, not the last one. A3's advice to harness builders is to read the traces (A3, F-a-126)." |

**Results (1:40-1:50).**
1. Screen `4`.

[[PENDING: S2 experiment dots, continuity failures out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

2. `make swap-2`; expect `judged measures identical`.
3. Discussion: "What would your team's handoff file need for a stranger to continue tomorrow?"
4. Optional layer switch (see [Layer switch](#layer-switch-optional)).
5. Transition: `submodules/02-state-lifecycle/demo/README.md`.

---

## Break (1:50-2:00)

Slide 35 with the return time (filled in live). If a layer-switch run was started at 1:48, leave the
console on its screen `1`.

---

## S3 Scope and sandbox (2:00-2:50)

**Feature and rule.** F3, idempotency keys on issue creation, from `m1-s3-start`, build phase then
test phase (`teamtrack/reference/f3/task.toml`; build allow list `app/api/issues.py`,
`app/services/issues.py`, `docs/HANDBOOK.md`, `tests/visible/**`; test allow list
`tests/visible/**`). The temptation: shared middleware in `app/api/middleware.py` is off-limits and
easier to change (DESIGN §8.3, allowed techniques). Primary measure: ≥ 1 out-of-scope file in the
shipped diff, or ≥ 1 source file changed during the test phase (DESIGN §8.2). Harness arm layers:
instructions, state, scope.

Say before the run: "The scope layer enforces this measure, so a harness result of zero out-of-scope
files is expected by construction. Watch the secondary measures: did the enforced arm still ship a
working feature?" (DESIGN §8.2, S3 note)

**Control glance.** C3, filter a project's issues by priority (`teamtrack/docs/features/c3.md`).

[[PENDING: C3 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Command.** `make demo-3`

**Screens during the run and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | Sandbox line per arm: container id, `network none`, CPU, memory, time left; harness decisions ⊘ block and ↺ revert with the reason | "The reason text is what the agent reads in its tool result. It names the phase and the allowed paths." |
| 1 | `1` | Gate: "No gate (verify layer off)." on the bare arm and "No gate." on the harness arm, because S3 has no verify layer | "Verification is the next section; S1 to S3 measure one layer at a time (DESIGN §6.6)." |
| 2 | `2` | Boards (no specific S3 view in DESIGN §13) | Short: "Does each arm's app still serve the board?" |
| 3 | `3` | "Diff map": ✎ changed, ⊘ blocked, ⚠ out of scope; "Sandbox denials" per arm | "The sandbox is the same for both arms. It is taught here, but it is never the variable (DESIGN §9)." |

**Results (2:40-2:50).**
1. **Sandbox moment** (DESIGN §14.1). If screen `3` lists any denial tonight, show it: reason code
   (`network`, `write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and
   the command. If none occurred, show the policy printout (command in "Before class", step 6) and
   the denial log from the experiments:

[[PENDING: sandbox_denied events from the experiment runs (command, reason code, arm) | source: M8 batch 1 | how: grep -h '"type":"sandbox_denied"' .shipharness/runs/*/events.jsonl]]

2. Screen `4`.

[[PENDING: S3 experiment dots, runs failing out of 10 per arm, with hidden-test and existing-test results as secondary | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

3. `make swap-3`; expect `judged measures identical`.
4. Discussion: "Which files in your repository should no agent touch during a test phase?"
5. Transition: `submodules/03-scope-sandbox/demo/README.md`.

---

## S4 Verification (2:50-3:40)

**Feature and rule.** F4, optimistic concurrency (ETag, If-Match) and issue history, from
`m1-s4-start`, one session of 40 turns (`teamtrack/reference/f4/task.toml`). Two co-primary counts per
run: hidden tests passed of 69 (VERIFICATION.md, M5 counts) and referee-set mutants killed by the arm's
shipped tests of 4 (`teamtrack/mutants/features/f4.jsonl`) (DESIGN §8.2). Harness arm layers: all
four. The blinded reviewer runs on both arms' diffs.

**Control glance.** C4, store issue titles without surrounding whitespace
(`teamtrack/docs/features/c4.md`).

[[PENDING: C4 control results for both arms | source: M8 batch 4 | how: make experiments, full dataset; VERIFICATION.md]]

**Command.** `make demo-4`

**Screens during the run and what to say.**

| Order | Screen | Watch | Say |
|---|---|---|---|
| 1 | `1` | Gate pills on the harness arm: ⏳ pending, then ✓ or ✗ for visible tests, existing tests, R1-R7, board, clean state | "The agent called finish. The harness runs checks it does not control; a failure goes back to the agent with the first three reasons." |
| 2 | `2` | "Two-tab edit conflict" panel: ✗ lost update or ✓ conflict detected per arm | "Two people edit one issue. Does the second save win silently?" |
| 3 | `3` | Filter table (tests × filters 1-5, kept or discarded with reason), coverage line, mutant table (filter set and referee set), referee counters such as "R1 probes n/m", reviewer verdict | "Filters 1 to 3 are TestGen-LLM's; 4 and 5 are course filters (B11; RESEARCH G-7). The referee-set mutants were never visible to the filters." |

**Results (3:30-3:40).**
1. Screen `4`. Two counts per run per arm, and reviewer agreement with the referee.

[[PENDING: S4 experiment dots, hidden tests passed of 69 and referee mutants killed of 4 per run per arm | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

2. `make swap-4`; expect `judged measures identical`.
3. Discussion: "Your agent's tests pass. What evidence would you accept before merging?"
4. Transition: `submodules/04-verification/demo/README.md`.

---

## Final run-through and wrap-up (3:40-4:00)

1. **3:40 Poll** (final feature poll in [poll-questions.md](poll-questions.md)): F5 bulk close, F6
   watchers, or F7 labels.
2. **3:41 Run** the winner only: `make final FEATURES=F6` (replace with the winner). Always pass
   `FEATURES`: the Makefile default is `F5,F6,F7`, three A/Bs in a row, which does not fit the time or
   the session cap. A second feature runs only if the session line after the first shows room for
   another final A/B (each arm capped at `MAX_FINAL_RUN_COST_USD` $0.25, plus the review cap).
3. **3:45 All screens**, `1` to `5`, both arms. Harness arm layers: all four.
4. **3:48 Boards**, screen `2`.
5. **3:50 Report**: `make report`, then open `exports/report.html`; then the LangSmith comparison
   link (screen `4` "LangSmith" list, or screen `5`). Show `Final:dots`.

[[PENDING: report output and LangSmith comparison link for the experiments | source: M8 batch 1 | how: make report; comparison_url in exports/experiments/]]

6. **3:53 Assignments** (slides 68-69): A1 to A4 in `submodules/0N-*/assignment/README.md`; learner
   budget ≤ $6 OpenAI and ≤ 400 LangSmith traces in total (DESIGN §11.5).
7. **3:56 Skills** to take home: `skills/harness-setup`, `skills/assured-tests`, `skills/house-rules`,
   `skills/skill-template`; show `Final:skill_template`.
8. **3:58 References** (slides 71-72), then close.

If the final A/B is still running at 3:53, go to the wrap-up slides and return to its screen `4` at
the end.

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
through the break), and only if the cost line after `make swap-2` leaves room for the rest of the
class:

- Caps (DESIGN §11.1): each arm $0.20 per run (final $0.25), each review $0.04, session $2.50.
- `make demo-N` runs the blinded reviewer on both arms by default (`--reviewer` is the default of
  `shipharness ab`), so each demo can reach 2 × $0.20 + 2 × $0.04 at the caps, and the final
  2 × $0.25 + 2 × $0.04. DESIGN §11.3 counts the reviewer only in S4 and the final.
- At the caps, the four demos and one final feature already reach the $2.50 session cap. Measured
  per-run costs decide whether a layer switch fits:

[[PENDING: measured cost per arm per demo and per review | source: M6 pilot | how: make demo-N cost lines; VERIFICATION.md per-command cost]]

When a model call would exceed a cap, the run ends as `ABORTED: cap`, is still judged, and is shown
(DESIGN §8.3 rule 9). A cap hit during the final would cost the final run, so when in doubt, skip the
live layer switch.

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
| `make final` with no `FEATURES` runs F5, F6, and F7 | Makefile default `FEATURES ?= F5,F6,F7` | Press Ctrl+C before the second feature starts; always pass `FEATURES=` | `Makefile` |
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
