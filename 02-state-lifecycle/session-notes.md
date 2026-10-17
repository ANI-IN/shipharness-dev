# S2 session notes: state and session lifecycle

Notes for learners after the S2 block. They summarise what was shown, the key ideas with their
sources, what the pilot measured (every run, not only tonight's), the questions that usually come up,
and what to try next. Source ids (A1-A7) and finding ids (F-a-NN) point to
[REFERENCES.md](../../REFERENCES.md). The full material is in [concepts.md](concepts.md) and the
[demo runbook](demo/README.md).

## What was shown

1. **Poll**, before anything ran: in the course pilot, with a first session stopped after 12 turns,
   which arm had more continuity failures over six A/Bs? (Answer: neither had any; see below.)
2. **Harness in action**, launched right after the poll: the harness arm alone (instructions and
   state) building F2, comments on issues, with a 12-turn first session and a 38-turn second one
   (`make show-2 SESSION_BUDGET=12,38`, which runs `shipharness ab --section demo-2 --feature F2
   --arms harness --session-budget=12,38`). It was not
   an A/B: the pilot had found no gap between the arms on this task, so the class watched the state
   layer do its job instead.
3. **Concepts** while it ran: why a fresh session has no memory, why compaction is not the fix, A3's
   context reset, and the files that carry state across it.
4. **Code walkthrough**: the anchors `S2:init` (`init.sh`), `S2:stop_resume` (`session_stop` and
   `resume_text`), and `S2:write` (the session-log line). Print any of them with
   `uv run python scripts/anchors.py extract S2:stop_resume`.
5. **Demo block**: the finished live run (screens 1, 3, 5): the initializer step, the wrap-up,
   "Session 1 stopped", the handoff written, "Session 2 resumed", and the referee's primary verdict.
6. **Every result** on one slide and console screen 4, wins and "no measurable difference" alike.

For your own notes from the live run, take from screens 1 and 3: the run id, how session 1 ended
(`ended_by`), whether session 2 read the handoff before writing code, whether it ran `alembic heads`
before writing a migration, and the primary verdict.

## Key ideas

- **Each session starts with no memory.** "each new session begins with no memory of what came
  before." (A2, F-a-08). A fresh agent also pays to orient itself: it "will spend significant time
  orienting itself, especially on large projects." (A4, F-a-10).
- **Compaction is not enough.** "However, compaction isn’t sufficient." (A2, F-a-54).
- **A context reset needs a structured handoff.** A3's reset is a fresh agent "combined with a
  structured handoff that carries the previous agent's state and the next steps" (A3, F-a-65). The
  course produces the reset with a **session turn budget**, the same for both arms; that mechanism is
  the course's, not a source term.
- **State lives in files and git.** A2 keeps it in "the claude-progress.txt file alongside the git
  history." (A2, F-a-53); the course calls the file `progress.md`. Plans are "checked into the
  repository" (A1, F-a-34), and A7 asks that "it should always be possible to restart from _only_ the
  ExecPlan and no other work." (A7, F-a-47; A7 is archived, accessed 2026-10-16).
- **Two routines bracket every session.** Getting up to speed: "Read the git logs and progress files
  to get up to speed on what was recently worked on." (A2, F-a-59). The end: "End the session by
  writing a git commit and progress update." (A2, F-a-63).
- **The harness writes part of the handoff itself.** At every stop `shipharness` writes a machine
  summary (commits, files changed, visible tests, TODO markers, migration heads, documents read) and
  a session-log line, even if the agent wrote nothing (course design).
- **Each piece encodes an assumption about the model.** A3: "every component in a harness encodes an
  assumption about what the model can't do on its own, and those assumptions are worth stress
  testing" (A3, F-a-124). The state files assume, in the course's words, that a fresh session cannot
  pick up the work from the repository alone. A3 dropped its resets once the model no longer needed
  them: "Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from
  this harness entirely." (A3, F-a-69).

## What the pilot measured

The course pilot ran F2 in four rounds before the class (gpt-6-luna). Primary measure:
`continuity_failure`, runs passing out of k per arm.

| Round | Session budget, effort | A/Bs | Bare passed | Harness passed | Hidden tests 56 of 56, bare / harness |
|---|---|---|---|---|---|
| Run 2, 2026-10-16 | 20/30, medium | `ab-20261016-181736-08a9c4`, `-184318-636e90`, `-190548-ae9abe` | 3/3 | 0/3 (measurement bug) | 1 of 3 / 0 of 3 |
| Run 3, 2026-10-16 | 12/38, medium | `ab-20261016-211419-dfe06f`, `-213317-9a0ec1`, `-214959-de790f` | 3/3 | 3/3 | 3 of 3 / 1 of 3 |
| Run 4, 2026-10-16/17 | 12/38, low | `ab-20261016-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9` | 3/3 | 3/3 | 0 of 3 / 2 of 3 |
| Class-profile round, 2026-10-17 | 12/38, low, Fast tier | `ab-20261017-085139-7c0661` | 1/1 | 1/1 | 1 of 1 / 1 of 1 |

On the primary measure: no measurable difference on this task with this model (course pilot, runs 3
and 4 and the class-profile round). What stands behind that:

- **Run 2's 0 of 3 was the course's own bug.** The continuity check read session patches that
  included the harness's `progress.md`, `session-handoff.md`, and exec plan, and scored their rewrite
  in session 2 as 50-84% redone work. The fix strips the harness's files before the check, for both
  arms. The same run showed the turn cost: harness sessions re-read 3 to 7 instruction documents and
  about 15 product files, with 0 to 1 product patches in 50 build turns.
- **The bare arm found its own state.** In `ab-20261016-181736-08a9c4` its session 2 ran
  `git status`, saw session 1's uncommitted `migrations/versions/0002_comments.py`, read it, and
  carried on. A6 says Claude models are "extremely effective at discovering state from the local
  filesystem." (A6, F-a-76; a living page, accessed 2026-10-16); the pilot model, which is not a
  Claude model, behaved that way here.
- **The measure has a blind spot.** Six arms in runs 3 and 4 built nothing (3 of 56 hidden tests) and
  still passed: the measure cannot fail when session 1 leaves no product lines to redo.
- **The runner had a bug, in both arms.** Those six arms called `finish(claim="not_done")` after 9 to
  12 turns of the first session, and the runner ended the build phase, so the 38-turn session never
  ran: two harness arms in run 3; all three bare arms and one harness arm in run 4. The fix: before
  the last build session, `finish(claim="not_done")` ends only that session. In the class-profile
  round, run after the fix, both arms built the feature (56 of 56).
- **Post hoc** (chosen after the results; descriptive; 9 runs per arm, runs 2 to 4): harness arms hit
  the agent time limit in 4 runs, bare arms in 0; median arm wall time 361 s against 232 s; median
  tests shipped 0 against 8.

The course's planned experiment batches (10 runs per arm per section, and a leave-one-layer-out
ablation) were not run, because the pre-registered pilot gate did not pass; the runs above are the
data. Run ids per arm are in the [demo runbook](demo/README.md) §11.

## Common questions

**The harness did not win. Was it useless?**
It did not show an effect on this task with this model, which is what the course reports. The state
files encode an assumption, that a fresh session cannot pick up the work from the repository alone,
and here it did not hold: the bare arm found its own state. A3 dropped its resets for the same kind of
reason (F-a-69). Keep a piece where your own measurement shows it earns its turns; the post hoc
numbers show what it costs.

**Why did the harness arm lose in run 2 if the files help?**
On the primary measure it lost because of a measurement bug, now fixed. On the work itself it built
little because the routine and the documents cost turns. State files are not free: A3 lists
"orchestration complexity, token overhead, and latency" for resets (F-a-68).

**Is changing the measure or the runner after a run allowed?**
The measure's definition did not change; its input was corrected so the check reads product work
only, for both arms. The runner fix also applies to both arms. The course's pilot rules require every
pilot-driven change to be logged with its label, reason, the run that revealed it, and its commit,
before the next run.

**Why does the harness write a machine summary when the agent writes notes anyway?**
An agent that runs out of turns mid-edit may write nothing. Facts like commits, test status, and
migration heads can be collected by a script, so the next session always gets them (course design).

**Why is the initializer harness code and not a model session, as in A2?**
For one ticket the initial files are fixed by the ticket text. A2 itself says its two agents differ
only in their first prompt (A2, F-a-52); the course writes the files deterministically (course
design).

**What does the screen 3 "↺ redone" marker mean?**
A file changed in session 1 changed again later. It is a hint, not the measure; the judged number is
`redone_lines_pct` from the referee
([post-class reading 03](post-class-reading/03-the-continuity-measure.md)).

## What to try next

- Read the [post-class reading](post-class-reading/README.md), especially 03 on the measurement bug
  and the measure's blind spot.
- Start assignment A2 ([assignment/README.md](assignment/README.md)): a state layer that carries a
  three-step feature across three forced stops. Run `make check-assignment-2` first; on the starter it
  reports "Self-check: 2 of 28 checks pass."
- In your own repository, stop your coding agent mid-task and start a fresh session. Count the tool
  calls it spends before its first change, then add a handoff file and count again. If the count does
  not drop, the handoff is not earning its turns.
- Write down, for your own tickets, which facts a script could put in a handoff (git state, test
  status, schema heads) and which only the agent knows (decisions, dead ends).
