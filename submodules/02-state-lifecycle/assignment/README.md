# Assignment A2: three forced stops, one consistent history

Build a state layer that lets a three-step feature finish across three forced session stops, with
no duplicated migration, no redone work, and a progress log and exec plan that agree with the git
history. The graded scenarios run offline: a test stand-in agent (a deterministic program, not a
model) drives the real `shipharness` runner loop on a small repository, so the self-check and the
grader need no API key, network, or Docker, and the scores repeat. Then you run your layer once,
live, with the course model (gpt-6-luna) through three forced stops, and submit that run's records.

Planned effort: 3 to 6 hours for a strong engineer (brief §5.1), plus one live run.

## Objective

Write `ResumableStateLayer`, a harness layer (CONTRACTS §5) that writes, at every session stop,
the state the next session needs, derived from evidence in the repository rather than from what
the agent says it did. Then show that it works: `make check-assignment-2` passes on the visible
scenarios, and one live run with gpt-6-luna (the required live step) goes through four sessions
with your layer as the state layer. The instructor's grader adds hidden scenarios and checks the
live run's records; the score is out of 100.

## Problem statement

In class (S2) the harness arm got a progress file, an exec plan, and a structured handoff, and the
feature finished across one forced stop. Here the ticket has three steps and the session turn
budget stops the run three times before the agent can finish. The test stand-in agent starts every
session with an empty context and believes only what it reads. When the state it reads is missing
or wrong, it does what a resumed agent does: it starts the work again. You will see it create a
second migration for a table that already exists, rewrite files it already wrote, and run out of
turns before the last step.

The class's S2 layer (`shipharness.harness.state.layer.StateLayer`) is not enough. It never tells
the next session which steps are done, so step 1 is redone in every session.

The pilot showed the same gap from the other side. In pilot run 2 the class layer's harness arm on F2
re-read 3 to 7 instruction documents and about 15 product files in every session, because nothing in
its state said what was already known or done, and made 0 to 1 product patches in 50 build turns
(VERIFICATION.md, M6 pilot run 2; the harness change that followed is change 9). A state layer that
says exactly which steps are done, and which files are already written, saves the next session
those turns.

## Background

- A2 keeps the state of a long task in files and git: "the claude-progress.txt file alongside the
  git history" (A2, F-a-53), and each session ends the same way: "End the session by writing a git
  commit and progress update." (A2, F-a-63). This course calls the file progress.md (CONTRACTS
  §15.2).
- A3's context reset clears the context and starts a fresh agent, "combined with a structured
  handoff that carries the previous agent's state and the next steps" (A3, F-a-65). The course
  produces the reset with a session turn budget smaller than the feature; "forced stop" is the
  course's name for that mechanism, not a source term (RESEARCH G-5). A3 treats resets as
  model-dependent and later dropped them for Opus 4.5 (A3, F-a-69).
- Exec plans are "execution plans with progress and decision logs that are checked into the
  repository" (A1, F-a-34). A7 asks that "it should always be possible to restart from _only_ the
  ExecPlan and no other work." (A7, F-a-47) and requires living `Progress`, `Surprises &
  Discoveries`, `Decision Log`, and `Outcomes & Retrospective` sections (A7, F-a-48).
- A2 found that the model "is less likely to inappropriately change or overwrite JSON files
  compared to Markdown files" (A2, F-a-81). progress.md and the exec plan are Markdown, so in this
  assignment the harness, not the agent, owns the parts the next session depends on.
- The S2 primary measure (DESIGN §8.2): a run fails continuity if R7 fails (heads ≠ 1 or a fresh
  upgrade fails), a second migration creates the same table, or at least 30% of the lines session 1
  added are removed in session 2 (`REDONE_THRESHOLD_PCT` in `src/shipharness/checks/continuity.py`).

Course design (not from a source): the step ledger, the rule that it is rebuilt from git at every
stop, the test stand-in agent itself, and the four-session live task.

The S2 code to read first, by walkthrough anchor (`uv run python scripts/anchors.py list`):
`S2:init` (init.sh), `S2:stop_resume` (session stop and resume), `S2:write` (session-log entry).

## The test stand-in agent

`a2_scenario/literal_agent.py` is a test stand-in agent: a deterministic program that follows
fixed rules, not a model. It exists for grading only, so that every learner's layer meets the same
agent and the scenario scores repeat. It is not a recording: each call decides the next tool call
from the current session's transcript only, so it reacts to whatever your layer wrote. Its rules
are the contract between your layer and the next session.

1. Every session starts with three reads, one turn each: `progress.md`, `session-handoff.md`, and
   `docs/exec-plans/active/<feature>.md`.
2. It learns only from those reads and from the resume message (your `on_session_start` text),
   line by line:
   - a line with `[x]` and a step id (`S2`) means that step is done;
   - otherwise, a line with a step id and the word `written` names files of that step that are
     already on disk; it will not write them again;
   - a line `Migration heads: 1 (<rev>)` gives the head for a new migration's `down_revision`
     (without one it uses the ticket's base revision, `0001`).

   It never infers progress from commit lines, file listings, or the ticket's step list.
3. It does the steps in order: one turn per file, then one turn for the step commit, with a subject
   that starts with the step id (`S1: Comments table`). When every step is done it runs the visible
   tests and calls `finish(claim="done")`.
4. It ignores the wrap-up message and keeps working, unless the scenario gives it a behaviour for
   that session: write a note in session-handoff.md, rewrite progress.md, or tick the next step in
   the exec plan before doing it.
5. Work it does not know about is done again as a fresh attempt: a new migration file with a new
   revision id, and files rewritten with a different `# draft <n>` marker on every line.

A real model does not follow these rules; the required live step shows what your layer does with
one.

## What to build

`starter/a2_state/` holds a layer that runs but writes nothing at a session stop. Complete it:

- `ledger.py`: the steps of the ticket and their status from git evidence (TODO 1a-1c).
- `layer.py`: `on_session_end` (TODO 1-5), `on_session_start` (TODO 6), `on_phase_end` (TODO 7).
- `progress_log.py`: progress.md rebuilt with every section and every session-log entry (TODO 4).

Then run the required live step once and keep its records in your folder (`live/`).

## Concepts tested

- Session lifecycle: initializer step, Getting up to speed, forced stop, resume (A2, A3).
- State from evidence: progress derived from commits and the working tree, not from the agent's
  own claims (course design, building on A2 F-a-53 and A3 F-a-65).
- Migration continuity: one Alembic head and no duplicate table across sessions (house rule R7).
- Progress-file integrity: one log entry per session, sections kept when the agent rewrites the
  file, every harness write committed.
- Exec plan lifecycle: a living Progress section, active to completed (A1, A7).

## Prerequisites

- Section S2 in class (`make demo-2`) and the anchors above.
- Python 3.12, uv, and git; `make setup` (or `uv sync --frozen`) done once.
- Read all of `src/shipharness/harness/state/`, and CONTRACTS §5 and §15.
- For the live step only: both API keys in `.env`, Docker, and the checkpoints (`make doctor`
  passes).

## Expected input and output

Input: a scenario (a feature, four session turn budgets, optional agent behaviours), run by the
real runner loop with your layer as the only harness layer, the test stand-in agent in the model's
place, and LocalSandbox on a fresh mini repository (`a2_scenario/fixture.py`).

Output, in the mini repository after the run:

| File | What it must show |
|---|---|
| `migrations/versions/` | exactly one head; a fresh `alembic upgrade head` works; no table created twice |
| git history | one `S<n>:` commit per step; nothing a session wrote was rewritten later |
| `progress.md` | the six CONTRACTS §15.2 sections in order; one `- Session <n> ...` entry per session |
| `docs/exec-plans/completed/<feature>.md` | Progress: `[x]` per step with its commit, one line per session; an outcome |
| `session-handoff.md` | machine summary of the last session, `Migration heads: 1 (...)`, the agent's notes |
| working tree | clean: every harness write committed |

## Detailed requirements

1. Initializer: keep the provided `prepare_workspace` (templates, one commit). You may add the
   ledger to the plan's Progress section here.
2. Ledger (TODO 1): at every session end, read `git log` since `ctx.state["harness.setup_sha"]`
   and `git status --porcelain -uall` through `ctx.sandbox.exec` (host code never runs git on the
   workspace). A step is done when a commit subject starts with its id and a colon (the first such
   commit counts). The first step that is not done is in progress when there are uncommitted
   product files (anything except progress.md, session-handoff.md, init.sh, the feature_list files,
   and `docs/exec-plans/`), and those files are listed as written.
3. Exec plan (TODO 2): rewrite the active plan's `## Progress` section from the ledger plus one line
   per session so far containing `Session <n>` and `ended by <reason>`. Rebuild it every time; do
   not keep lines the agent added there (it may tick a step it has not done).
4. Handoff (TODO 3): `## Machine summary` from `handoff.MachineSummary` (it states "end of session
   <n>" and the migration heads) plus the ledger lines; `## Notes from the agent` kept exactly as
   the agent left it (`handoff.merge` does this).
5. progress.md (TODO 4): one entry per session in the `progress.session_entry` format
   (`- Session <n> (<phase>): start <sha7>, end <sha7>, ended by <reason> ...`), with the
   SessionResult's values. If the agent rewrote the file, restore the missing sections from the
   template, keep what it wrote, and rebuild the session log from your own list of entries.
6. Commit (TODO 5): one harness commit per stop for every file you wrote (`commit_paths`).
7. Resume (TODO 6): the ledger lines, the next step, and `Migration heads: <output of
   handoff.migration_heads>`.
8. Completion (TODO 7): once, when the last claim is done and the ledger shows every step done,
   rebuild Progress, replace "Not finished yet." under `## Outcomes & Retrospective`, move the plan
   to `docs/exec-plans/completed/`, and commit `docs/exec-plans`.
9. Live step: one run of your final layer with gpt-6-luna through three forced stops, with its
   records in `<your folder>/live/` (section "Required live step").

## Constraints

- Edit only `starter/a2_state/` (or a copy of it, passed with `A2_IMPL` / `--impl`). Do not edit
  `a2_scenario/`, `check.py`, `live/`, or anything under `src/`.
- Keep `context_prefix` byte-stable across sessions (it is part of the cached prompt prefix).
- Run git in the sandbox; write workspace files with `shipharness.harness.state.files`.
- No model calls and no network in the layer. The layer must work for any feature whose steps have
  ids `S1`, `S2`, ...; nothing may depend on the visible feature's file names or step count.
- The live step runs once per submission, with the course model, sandbox, and caps (section
  "Required live step"). Do not edit the files it writes.

## Step-by-step tasks

1. Run `make check-assignment-2` on the starter. Read the session lines and find the first `[REDO`.
2. TODO 1a-1c in `ledger.py`: `parse_steps`, `derive_ledger`, `render_ledger`. Unit-test them.
3. TODO 1 and 5: compute the ledger and the heads in `on_session_end`; commit what you write.
4. TODO 6: the resume text. Run the self-check: V1 now gets past step 1.
5. TODO 2: the exec plan's Progress section with the session lines.
6. TODO 3: the handoff. TODO 4: `normalise_progress` and the session log.
7. TODO 7: completion. Run the self-check until all 28 checks pass. The grader's hidden scenarios
   use other stop points, a four-step feature with two chained migrations, an agent that writes a
   handoff note and later rewrites progress.md, and an agent that ticks a step in the exec plan
   before doing it, so test those cases yourself.
8. With the layer final, run the required live step once. Run the self-check again: its last lines
   report whether `live/` holds valid evidence.
9. Submit your folder (section "Submission").

## Expected project structure

```
assignment/
  README.md                this brief
  check.py                 self-check: visible scenarios, PASS/FAIL per criterion, exit 0 or 1
  a2_scenario/             provided, do not edit
    feature.py             steps, file slots, ticket text
    fixture.py             the mini repository (one Alembic migration, one visible test)
    literal_agent.py       the test stand-in agent (deterministic, not a model)
    runner.py              one scenario through shipharness.runner.loop.run_agent
    measures.py            the grading criteria of the scenarios
    live_evidence.py       the live task, the evidence files, and their checks
    report.py              loading your layer, printing results
    scenarios.py           the visible feature (comments, three steps) and scenarios V1, V2
  starter/a2_state/        your work
    layer.py               ResumableStateLayer (TODO 1-7)
    ledger.py              TODO 1a-1c
    progress_log.py        TODO 4
  tests/                   tests of the provided code (the live evidence tests use a synthetic fixture)
  live/run_live.py         the live wrapper: required live step and optional live variant
```

Your submission folder (a copy of `starter/`, here `my-a2/`):

```
my-a2/
  a2_state/                your layer
  live/                    written by the required live step; do not edit
    task.jsonl             the four-session F2 task the run used
    command.txt            the wrapper command as run, and the shipharness command it ran
    output.txt             everything the A/B printed, with its `Cost: $...` line
    summary.json           run summary: A/B id, run ids, model, sessions and forced stops per arm, layer
    scores/<run_id>.json   the ScoreRecord of each arm, copied from exports/scores/
```

## Setup

```
make setup                      # once: uv sync and the images (the images are for the live step)
make check-assignment-2         # see the starter fail: "Self-check: 2 of 28 checks pass.", make exits 2
```

To keep the starter untouched, copy it and point the commands at the copy:
`cp -r submodules/02-state-lifecycle/assignment/starter my-a2`, then add `A2_IMPL=my-a2`.

## How to run

```
make check-assignment-2 [A2_IMPL=<folder>]   # visible scenarios and the live evidence status
```

Without make: `uv run python submodules/02-state-lifecycle/assignment/check.py --impl <folder>`.
`--keep` keeps the scenario repositories and prints their paths, so you can read the files your
layer wrote. The required live step has its own command (section "Required live step").

## How to test

- The self-check is the visible test: it runs V1 and V2 and prints every criterion.
- Write unit tests for your ledger and progress helpers next to your code and run them with
  `uv run python -m pytest -q -p no:cacheprovider <your test folder>`.
- Tests of the provided code: `uv run python -m pytest -q -p no:cacheprovider
  submodules/02-state-lifecycle/assignment/tests`.

## Expected behaviour

With a correct layer, every scenario finishes in session 4 and the session lines show no `[REDO`:

- V1 (budgets 6, 6, 6, 5): each stop lands right after a step commit.
- V2 (budgets 5, 6, 6, 8): each stop lands after a step's files are written but before its commit;
  the next session commits them without writing them again.

## Example inputs and outputs

The visible feature's ticket (`Feature.ticket()` in `a2_scenario/feature.py`), its step lines:

```
- S1 Comments table: one migration that creates the comments table, and app/comments/models.py
- S2 Comment service: app/comments/service.py and app/comments/validation.py
- S3 Index and tests: one migration that adds an index on comments.issue_id, and tests/visible/test_comments.py
```

Self-check on the starter, scenario V1 and the summary (captured on 2026-10-17 from
`make check-assignment-2` on the starter; offline, so there is no run id; lines cut with `...`; your
commit hashes will differ). The full output is in the reference solution's captured files, which the
instructor keeps:

```
$ make check-assignment-2
uv run python submodules/02-state-lifecycle/assignment/check.py
A2 self-check: 2 visible scenarios against submodules/02-state-lifecycle/assignment/starter
...
  session 2 (6 turns, ended by turn_budget): 3 reads, write S1 migrations/versions/c1a2_comments.py [REDO: S1 was committed in session 1], ...
...
  FAIL one_head: 4 heads: c1a2 (head) | c1a3 (head) | c1a4 (head)
...
  FAIL no_duplicate_table: comments created by c1a1_comments.py, c1a2_comments.py, c1a3_comments.py, c1a4_comments.py
...
Self-check: 2 of 28 checks pass.
...
Fix the FAIL and HALF lines (the hints name the TODOs in a2_state), then run again.
make: *** [Makefile:130: check-assignment-2] Error 1
```

`check.py` exits 1 on any failing check; make reports that as `Error 1` and itself exits 2.

Ledger lines that work with the test stand-in agent:

```
- [x] S1 Comments table: done in commit 615f2d2
- [ ] S2 Comment service: in progress; written but not committed: app/comments/service.py
- [ ] S3 Index and tests: not started
```

## Grading criteria (100 points)

The instructor grades your submission folder. Each scenario criterion is checked in every
scenario (2 visible, 4 hidden), run with the test stand-in agent. Its points are multiplied by the
share of scenarios that pass it; `no_redone_lines` earns half in a scenario where the worst session
redid less than 30% of earlier lines. `live_run` is all or nothing.

| Key | Points | Criterion |
|---|---:|---|
| `finished` | 13 | Three forced stops, the last session ends with `finish(done)`, visible tests pass, every step's files exist |
| `one_head` | 9 | Exactly one Alembic head |
| `fresh_upgrade` | 9 | `alembic upgrade head` works on an empty database |
| `no_duplicate_table` | 5 | No table is created by two migrations |
| `no_redone_lines` | 13 | No session removes lines an earlier session added (0%: full points; under 30%: half) |
| `steps_once` | 5 | Each step is committed exactly once |
| `progress_sections` | 3 | progress.md keeps its CONTRACTS §15.2 sections in order |
| `session_log` | 8 | One session-log entry per session, in order |
| `history_consistent` | 4 | Each entry's start and end commits and end reason match the run |
| `plan_completed` | 5 | Exec plan moved to `completed/`, with an outcome |
| `plan_ledger` | 5 | Progress ticks every step with a commit whose subject starts with its id |
| `plan_sessions` | 5 | Progress has a `Session <n> ... ended by <reason>` line per session |
| `handoff` | 4 | Last session's machine summary, `Migration heads: 1 (`, agent notes kept |
| `clean_tree` | 2 | Clean working tree at the end |
| `live_run` | 10 | `live/` holds valid evidence of the required live step (checks below) |

The `live_run` checks read the files only; the grader never runs a model and needs no keys. It
scores nothing from what the model did beyond these facts:

- the files exist, each `scores/*.json` is a valid ScoreRecord (`src/shipharness/ab/score.py`,
  `checkpoint_sha` set), one per arm, named by its run id;
- the run ids and the A/B id agree across `summary.json`, the score records, and `output.txt`, and
  `command.txt` names the live task (`--example F2-a2-four-sessions --layers instructions,state`);
- both arms ran gpt-6-luna with session budget [10, 10, 10, 20]; the harness arm had four build
  sessions, the first three ended by the turn budget, and three `session_stop` events;
- `recorded` is false and `sandboxed` is true in both records;
- each arm's `cost_usd` is at most the run cap ($0.20, `max_run_cost_usd`), and the command's
  `Cost: $...` line is at most $2.50 (`max_batch_cost_usd`), both in
  `src/shipharness/config/settings.py`;
- the harness record lists the `state` layer, and the layer that ran is your submitted
  `a2_state/`: `summary.json` holds a sha256 of its `.py` files, which must match the folder you
  submit.

## Common mistakes

- Trusting the exec plan or progress.md as written: the agent may tick a step it has not done.
  Rebuild from git every time.
- Listing only committed work: a stop between "files written" and "commit" needs a `written` line,
  or the next session rewrites the files (redone lines).
- Appending the session-log entry to whatever progress.md holds: after the agent rewrites the file,
  the earlier entries are gone. Keep your own list.
- Forgetting to commit the exec plan at each stop, or the move at the end (`clean_tree`).
- Moving the plan on the claim alone: the move needs the claim and every step committed.
- Taking the migration head from the last commit only: call `handoff.migration_heads` on the
  workspace at every stop, so an uncommitted migration counts.
- Hard-coding `S1`-`S3` or the comments file names: the hidden feature has four steps.
- Running git on the host instead of through `ctx.sandbox.exec`.
- Changing `a2_state/` after the live step: the layer hash no longer matches and `live_run` fails.
  Run the live step last.

## Required live step

Course design: one A/B, run once, with your layer as the harness arm's state layer and the course
model as the agent. It uses the real `shipharness` runner, sandbox, referee, and caps of class.

The task is F2-canonical from `teamtrack-features-v1` with one change: four build sessions instead
of two. The dataset's F2 tickets have one forced stop each (session budget [20, 30]); the live
task splits the same 50 build turns into [10, 10, 10, 20] (`LIVE_BUDGETS` in
`a2_scenario/live_evidence.py`), and its ticket says "This task runs over four sessions." instead
of two. Hidden tests, mutants, and the primary measure are unchanged. The runner starts the next
session only when a session ends by its turn budget (`_run_phases` in
`src/shipharness/runner/loop.py`), so a run that reaches session 4 has had three forced stops,
each followed by a `session_stop` event.

From the repository root, with keys, Docker, and the checkpoints (`make doctor` passes):

```
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl my-a2 --forced-stops
```

The wrapper writes `my-a2/live/task.jsonl`, registers your `ResumableStateLayer` as "state", and
runs `shipharness ab --dataset my-a2/live/task.jsonl --example F2-a2-four-sessions --layers
instructions,state --no-reviewer` (both arms; the referee judges both). It prints the A/B output as
it runs, then writes `command.txt`, `output.txt`, `summary.json` (from
`.shipharness/runs/<ab_id>/ab.json` and `events.jsonl`), and copies the two score records from
`exports/scores/`. It ends with `+ live evidence written ...` or a list of what is not valid, and
it never overwrites an existing `live/summary.json`.

The run does not count when the model ends a session before its turn budget (a `finish` call in
sessions 1-3) or the run stops at a cap before session 4: the check reports the build sessions it
found. Move `live/` away and run again; each attempt costs up to $0.40 at the caps.

Score records and runs stay in `exports/` and `.shipharness/runs/` as for any A/B, so
`uv run shipharness replay <ab_id>` and the console work on them. The run's continuity result
(`continuity_failure`, `redone_lines_pct` in the records) is for your report, not for points.

## Submission

Submit your folder (`my-a2/` with `a2_state/` and `live/`), as a folder or as a git repository.
The instructor runs `make grade-assignment-2 SUBMISSION=<folder or git URL>`. In a repository,
the grader uses the folder that holds `a2_state/layer.py` and `live/summary.json`; keep exactly
one such folder.

## Cost and trace budget

The scenarios and the self-check make no model calls: $0 and 0 LangSmith traces. The test stand-in
agent reports fixed token counts to the cost tracker, and nothing is sent anywhere.

The required live step is one A/B: two arms, each capped at $0.20 (`max_run_cost_usd` in
`src/shipharness/config/settings.py`), so at most $0.40, and 4 traces (2 per run: agent root and
referee evaluator, DESIGN §12). The optional variant below adds at most $0.80 and 8 traces, so A2
stays inside its planned $1.50 and 60 traces (DESIGN §11.5).

## Optional live variant (costs money)

Two more F2 tasks of the `section-2` subset, each with one forced stop (session budget [20, 30]),
to see your progress file, plan, and handoff on other tickets. `live/run_live.py` passes
everything after `--` to the `shipharness` CLI:

```
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl my-a2 -- ab --example F2-reworded-pm --layers instructions,state --no-reviewer
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl my-a2 -- ab --example F2-alt-a --layers instructions,state --no-reviewer
```

At the caps each command costs at most $0.40. A LangSmith experiment on the whole `section-2`
split (`shipharness experiments --split section-2 --k 1`) runs 8 tasks in two arms, up to $3.20 at
the caps, above the $2.50 limit per command (brief §5.1), so the variant uses `ab`.

The live tickets have no step ids, so your ledger is empty there (also in the required live step):
the runs show whether your progress file, plan, and handoff hold up with a real model.

### Live report template

Copy this block into your own file and fill in every field from the required live step (and the
variant, if you ran it). Keep the run ids, so the numbers can be checked against
`.shipharness/runs/<ab id>/events.jsonl` and the LangSmith traces.

```
# A2 live report

Layer folder (--impl):            Commit of the layer:
Date and model (OPENAI_MODEL):
Commands run (exactly as typed):

| Example             | Arm     | Run id | Status | Continuity | Redone lines % | Heads | Forced stops | Cost (USD) |
|---------------------|---------|--------|--------|------------|----------------|-------|--------------|------------|
| F2-a2-four-sessions | bare    |        |        |            |                |       |              |            |
| F2-a2-four-sessions | harness |        |        |            |                |       |              |            |
| F2-reworded-pm      | bare    |        |        |            |                |       |              |            |
| F2-reworded-pm      | harness |        |        |            |                |       |              |            |
| F2-alt-a            | bare    |        |        |            |                |       |              |            |
| F2-alt-a            | harness |        |        |            |                |       |              |            |

Total cost (sum of the cost lines the commands printed):

What the layer wrote: for the harness run of F2-a2-four-sessions, the session-handoff.md machine
summary at each forced stop and the exec plan's Progress section at the end. Did each resumed
session use them (its first tool calls in the run log)?

Findings: where the real model differed from the test stand-in agent's rules; what you would
change for tickets without step ids.
```

"Continuity" is the S2 primary measure (DESIGN §8.2): the score record's `continuity_failure` and
`redone_lines_pct` fields (`src/shipharness/ab/score.py`). It compares sessions 1 and 2 only
(`src/shipharness/checks/continuity.py`); for sessions 3 and 4, read the session patches in
`.shipharness/runs/<ab id>/harness/sessions/`.
