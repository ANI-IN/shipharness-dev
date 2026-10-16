# A2 solution notes

Reference solution: `a2_state/` (layer.py, ledger.py, progress_log.py). Grader:
`grader/grade.py` with the hidden scenarios in `grader/a2_hidden.py`. Hidden grader tests:
`grader/tests/`. Unit tests of the solution's helpers: `tests/`.

## Results (captured)

The full outputs are in `captured/`, captured on 2026-10-17 at commit e7287f4 with the make
targets on each file's first command line (offline: the test stand-in agent, no model calls, so no
run id; commit hashes in the output change on every run).

| Layer | Self-check (visible), `make check-assignment-2 A2_IMPL=<folder>` | Grade (visible and hidden), `make grade-assignment-2 SUBMISSION=<folder>` | File |
|---|---|---|---|
| Reference solution (`submodules/02-state-lifecycle/solution`) | 28 of 28 checks, exit 0 | 90.0/100 (scenarios 90 of 90; `live_run` 0 of 10) | `check-solution.txt`, `grade-solution.txt` |
| Starter (`submodules/02-state-lifecycle/assignment/starter`, the default) | 2 of 28 checks; `check.py` exits 1, make exits 2 | 4.3/100 | `check-starter.txt`, `grade-starter.txt` |
| Class S2 layer (`submodules/02-state-lifecycle/solution/class_s2_layer`) | not run | 27.6/100 | `grade-class-s2-layer.txt` |

The reference solution loses exactly the 10 `live_run` points, and that is expected: its live run is
not captured yet (`live/README.md` holds the PENDING marker). Every scenario criterion earns full
points.

The scenarios are deterministic (the test stand-in agent and the scripted token counts never
vary), so the scores repeat; only commit hashes and timestamps differ between runs. The test
stand-in agent is a program that follows fixed rules, not a model; it is used for grading only.

The `live_run` criterion (10 points) needs the captured live run of the reference solution in
`live/` (see `live/README.md` for the command and the PENDING marker). The grader's tests give the
reference layer 100/100 with a synthetic, labelled evidence fixture
(`assignment/tests/a2_live_fixture.py`), never presented as a real run.

## Approach

At every session end the layer asks the repository what happened, and writes that where the next
session reads it:

1. Evidence (`_evidence`): `git log --reverse --format=%H%x09%s <setup>..HEAD` and
   `git status --porcelain -uall`, both through the sandbox. A step is done when a commit subject
   starts with its id and a colon; the first such commit is the one that did it. The first step
   that is not done is in progress if the working tree has uncommitted product files, which are
   listed as written.
2. The ledger is rendered as A7-style checkbox lines (`- [x] S1 ...: done in commit <sha7>`,
   `- [ ] S2 ...: in progress; written but not committed: <files>`, `- [ ] S3 ...: not started`).
   The same lines go into the exec plan's Progress section, the handoff's machine summary, and the
   resume message, so every place the next session looks agrees.
3. The exec plan's Progress section is rebuilt on every stop: the ledger, then one line per session
   (`Session <n> (<phase>) ended by <reason> after <turns> turns at commit <sha7> (<UTC time>)`).
4. session-handoff.md: the S2 `MachineSummary` (files changed, visible tests, last commits, TODO
   markers, migration heads) plus the ledger, merged with `handoff.merge`, which keeps the agent's
   `## Notes from the agent` section as written.
5. progress.md: the layer keeps its own list of session-log entries (in the
   `progress.session_entry` format) and rebuilds the file with `normalise_progress`: the
   CONTRACTS §15.2 sections in order, the agent's text kept where it wrote any, missing sections from
   the template, and the session log from the layer's list.
6. One harness commit per stop (`commit_paths` on the handoff, progress.md, and the plan).
7. The resume message: the ledger, the next step (and that its listed files exist), and
   `Migration heads: <handoff.migration_heads>`.
8. `on_phase_end`: if the last claim is done and a fresh ledger shows every step done, the Progress
   section is rebuilt, the outcome replaces "Not finished yet.", the plan moves to
   `docs/exec-plans/completed/`, and `docs/exec-plans` is committed. It runs once.

Everything else comes from the S2 package: templates, safe file writes, the session-log format, the
machine summary, migration heads read as text, and sandboxed commits.

## Design choices

- Evidence over claims. The ledger comes from commits and the working tree, never from the files
  the agent edits. This is why the early tick in hidden scenario H4 does no harm: the next stop
  rebuilds Progress from git. It follows A2's pairing of the progress file with git history
  (A2, F-a-53); deriving the status only from git is course design.
- The harness owns the plan's Progress section. A7 describes Progress as a living section; here the
  harness writes it and the agent's narrative goes to Surprises & Discoveries and the Decision Log
  (the wrap-up message says so).
- Uncommitted work is recorded, not committed. At a stop between "files written" and "commit", the
  ledger lists the files as written and the next session commits them, so the step's commit is the
  agent's own `S<n>:` commit and `steps_once` holds.
- Session history in two places. progress.md keeps the A2-style session log; the plan keeps one line
  per session as well, so the plan alone is enough to restart from (A7, F-a-47).
- In-memory entries. The session log is rebuilt from the layer's own list, so an agent that rewrites
  progress.md (hidden scenario H3) cannot delete history.

## Alternatives considered

- Harness work-in-progress commits at every stop (commit the agent's uncommitted files). Simpler to
  describe, but it mixes agent work into harness commits and makes the step commit empty or
  missing; the ledger would then need file-to-step mapping.
- Keeping the agent's Progress lines and marking unproven ticks as "claimed, not in git". It keeps
  more of the agent's text but adds a second grammar the next session has to read correctly.
- Parsing the previous session-log entries back out of progress.md instead of keeping a list. It
  survives a harness restart, but not an agent that rewrote the file before the stop.
- A JSON state file (A2's argument for JSON, F-a-81). It would be harder for the agent to damage,
  but CONTRACTS §15 fixes progress.md, the handoff, and the exec plan as the workspace artifacts.

## Trade-offs

- Commit subjects are agent-controlled: an agent can write `S3: ...` without doing step 3. The
  ledger records what git says, not whether the step works. The S3 scope layer's evidence-gated
  status (`harness/scope/status.py`) is the course's answer to that problem.
- Every stop runs the visible tests once, for the machine summary. That costs harness time at each
  stop but tells the next session whether it starts from a working state (A2, F-a-62).
- The ledger needs step ids. Tickets without `S<n>` ids (the real F2 tickets in the required live step and the live variant)
  get an empty ledger; the layer then still writes the session log, the plan's session lines, the
  handoff, and the heads.

## Known limits

- The test stand-in agent imitates a disciplined but forgetful agent; it is not a model. A real
  model may read other files, infer progress from the git log, or ignore the plan; the required
  live step (one four-session A/B with gpt-6-luna) shows that for each learner's layer.
- The layer keeps its session-log list in memory, so it assumes one process per run (true for
  `run_agent`).
- Only Alembic migrations under `migrations/versions/` are counted for heads (as in the S2 layer).
- `uncommitted_paths` strips git's quotes but does not decode C-style escapes in unusual file names.

## How the grader decides

Per scenario, `assignment/a2_scenario/measures.py` evaluates 14 criteria (90 points in total). The
redone-lines measure reuses `redone_pct` from the S2 continuity check, applied to every session:
session j's change runs from the stop of session j-1 to its own stop, so anything a layer changes in
product files between sessions also counts. The working tree is captured at each session start and
at each stop (before the layer writes) with a temporary git index, so uncommitted work is included.
A criterion's points are multiplied by the share of the six scenarios that pass it.

The live criterion (`live_run`, 10 points, `assignment/a2_scenario/live_evidence.py`) is all or
nothing. It reads `<submission>/live/` and checks structure only: one valid ScoreRecord per arm
with `checkpoint_sha`, `recorded` false and `sandboxed` true; run ids and the A/B id consistent
across the records, `summary.json`, and `output.txt`; `command.txt` naming the live task; model
gpt-6-luna and session budget [10, 10, 10, 20] for both arms; four build sessions for the harness
arm with the first three ended by the turn budget and three `session_stop` events; each arm within
the $0.20 run cap and the command's cost line within $2.50; the `state` layer in the harness
record; and the sha256 of the submitted `a2_state/*.py` equal to the one recorded at run time. It
never runs a model and scores nothing else from the model's output.

Why [10, 10, 10, 20]: the dataset's F2 lines all give the build phase 50 turns in two sessions
([20, 30], [13, 37], [25, 25], [38, 12]); the live task keeps 50 and splits it into four sessions.
The runner starts session n+1 only when session n ends by its turn budget, and emits a
`session_stop` event after each such session except the last (`_run_phases` in
`src/shipharness/runner/loop.py`), so reaching session 4 means three forced stops. A model that
calls `finish` in sessions 1-3, or a cap that stops the run before session 4, makes the evidence
invalid; the learner moves `live/` away and runs again.

[[PENDING: share of real gpt-6-luna runs of F2-a2-four-sessions that reach session 4 (three forced stops) and their cost per A/B | source: M8 batch 1 | how: uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops]]

[[PENDING: measured cost per A/B and continuity result per arm for the reference solution layer on the optional variant (F2-reworded-pm, F2-alt-a) | source: M8 batch 1 | how: uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution -- ab --example <id> --layers instructions,state --no-reviewer]]

## Review notes for the Thursday session

- Expected approach: derive the ledger from git; list uncommitted files as written; rebuild plan
  Progress and the session log every stop; commit; move the plan on claim plus evidence.
- Common mistakes seen in the starter and the class layer: no step status for the next session
  (step 1 redone, duplicate `comments` table, several heads); the session log lost when the agent
  rewrites progress.md; the plan never moved because the move waited for the scope layer's
  `passes`.
- Discussion: when should the harness commit the agent's uncommitted work? What evidence would
  make the ledger trustworthy against an agent that writes misleading commit subjects?
