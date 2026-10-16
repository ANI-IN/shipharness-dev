# S2 session notes: state and session lifecycle

Notes for learners after the S2 block. They summarise what was shown, the key ideas with their
sources, what the A/B showed (the pilot and experiment dots, not only tonight's run), the questions
that usually come up, and what to try next. Source ids (A1-A7) and finding ids (F-a-NN) point to
[RESEARCH.md](../../RESEARCH.md). The full material is in [concepts.md](concepts.md) and the
[demo runbook](demo/README.md).

## What was shown

1. **Poll**, before anything ran: both agents stop after the first session's turn budget and start
   again with an empty context; which arm ships one migration head, one `comments` table, and most of
   session 1's work?
2. **The live A/B**, launched right after the poll: F2, comments on issues, in two arms (bare, and
   instructions + state), each in its own container, judged by the same referee. The class task
   follows the pilot decision recorded in VERIFICATION.md (F2 canonical with a [20, 30] session turn
   budget, or the run-3 lever [12, 38]).
3. **Concepts** while the A/B ran: why a fresh session has no memory, why compaction is not the fix,
   A3's context reset, and the files that carry state across it.
4. **Code walkthrough**: the anchors `S2:init` (`init.sh`), `S2:stop_resume` (`session_stop` and
   `resume_text`), and `S2:write` (the session-log line). Print any of them with
   `uv run python scripts/anchors.py extract S2:stop_resume`.
5. **Demo block** on the finished A/B: screen 1 (the session stop and resume markers, the first tool
   calls of each session), screen 3 (sessions per arm and the referee's `continuity` and
   `r7_migrations` rows), screen 2 (the boards), screen 5 (first wrong turn and trace), the verdicts,
   screen 4 (the dots), and `make swap-2`.

[[PENDING: tonight's S2 A/B id, both arms' status, continuity_failure, redone_lines_pct, hidden tests passed, cost, and the poll result | source: live class | how: make demo-2 (or the class command recorded in VERIFICATION.md)]]

## Key ideas

- **Each session starts with no memory.** "each new session begins with no memory of what came
  before." (A2, F-a-08). A fresh agent also pays to orient itself: it "will spend significant time
  orienting itself, especially on large projects." (A4, F-a-10).
- **Compaction is not enough.** "However, compaction isn’t sufficient." (A2, F-a-54).
- **A context reset needs a structured handoff.** A3's reset is a fresh agent "combined with a
  structured handoff that carries the previous agent's state and the next steps" (A3, F-a-65). The
  course produces the reset with a **session turn budget**, the same for both arms; that mechanism is
  the course's, not a source term (RESEARCH G-5).
- **State lives in files and git.** A2 keeps it in "the claude-progress.txt file alongside the git
  history." (A2, F-a-53); the course calls the file `progress.md`. Plans are "checked into the
  repository" (A1, F-a-34), and A7 asks that "it should always be possible to restart from _only_ the
  ExecPlan and no other work." (A7, F-a-47).
- **Two routines bracket every session.** Getting up to speed: "Read the git logs and progress files
  to get up to speed on what was recently worked on." (A2, F-a-59). The end: "End the session by
  writing a git commit and progress update." (A2, F-a-63).
- **The harness writes part of the handoff itself.** At every stop `shipharness` writes a machine
  summary (commits, files changed, visible tests, TODO markers, migration heads, documents read) and
  a session-log line, even if the agent wrote nothing (course design, DESIGN §6.3).
- **Resets are model-dependent.** A3 dropped them for a later model: "Opus 4.5 largely removed that
  behavior on its own, so I was able to drop context resets from this harness entirely." (A3,
  F-a-69). The course teaches the part that holds for any model: if a session can end before the work
  is done, the next one must be able to pick up from files.

## What the A/B showed

### Pilot run 2

The M6 pilot ran each section's A/B three times before the class (gpt-6-luna, effort medium). Run 2's
per-section results (VERIFICATION.md, M6 pilot run 2):

| Section | Bare: primary passed | Harness: primary passed | Why the harness arm failed |
|---|---|---|---|
| F1 | 3/3 | 3/3 | (passed) |
| F2 (this section) | 3/3 | 0/3 | continuity failure measured on harness files only (change 7) |
| F3 | 3/3 | 3/3 | (passed) |
| F4 | 0/3 | 0/3 | shipped 0, 0, 3 tests in the 12-turn test phase |

For F2, two findings, both described in [concepts.md](concepts.md) §6:

- **The bare arm did not forget.** It passed continuity in 3 of 3 runs. In
  `ab-20261016-181736-08a9c4` its session 2 ran `git status`, saw session 1's uncommitted
  `migrations/versions/0002_comments.py`, read it, and carried on. A6 says Claude models are
  "extremely effective at discovering state from the local filesystem." (A6, F-a-76); the pilot model
  behaved that way on this task too.
- **The harness arm's 0 of 3 was the course's own problem.** The continuity check read session
  patches that included the harness's `progress.md`, `session-handoff.md`, and exec plan, and scored
  their rewrite in session 2 as 50-84% redone work. Fixed by change 7 (harness artifacts stripped
  before the check; "bug fix, applies to both arms"). Separately, the harness arms spent their turns
  re-reading 3 to 7 instruction documents and about 15 product files per session and updating their
  state files mid-session, with 0 to 1 product patches in 50 build turns; change 9 moved the
  bookkeeping to the wrap-up and puts the handoff's agent notes ahead of any document.

The dots per run, with run ids and per-run costs, are in the [demo runbook](demo/README.md) §7.

### Pilot run 3 and the experiments

With the bug fixed, F2 still had no gap in run 2, so the pre-registered lever for run 3 is a tighter
session turn budget: a 12-turn first session (`shipharness ab --session-budget 12,38`, DESIGN §10.4).

[[PENDING: pilot run 3 F2 results with the 12-turn first session (continuity_failure per arm out of k=3, components, redone_lines_pct, run ids) and the class task decision | source: M6 pilot | how: scripts/pilot.py --budgets F2=12/38 (pilot run 3); VERIFICATION.md]]

[[PENDING: M8 batch 1 S2 dots: continuity_failure per arm out of k=10, components (a)/(b)/(c), redone_lines_pct, run ids | source: M8 batch 1 | how: make experiments BATCH=1 && make report]]

[[PENDING: M8 ablation, leaving the state layer out (-state), S2 tasks, with run ids | source: M8 ablation | how: make experiments BATCH=2 && make report]]

If a section still shows no gap after the pre-registered steps, the course reports it as "no
measurable difference on this task with this model" and shows it that way (DESIGN §10.4).

## Common questions

**The bare arm passed. Does that mean state files are useless?**
No. It means that on this model, at this effort, with a 20-turn first session, the agent rebuilt the
picture from `git status` and the files on disk. A3 reports the same kind of result for a later model
(F-a-69). The A/B tells you about one model and one task; the run-3 lever and the batch dots test
other conditions.

**Why did the harness arm lose if the files help?**
On the primary measure it lost because of a measurement bug, now fixed (change 7). On the work itself
it built little in run 2 because the routine and the documents cost turns. State files are not free:
A3 lists "orchestration complexity, token overhead, and latency" for resets (F-a-68).

**Is changing the measure after a run allowed?**
The measure's definition did not change; the input was corrected so the check reads product work
only, for both arms. Every pilot-driven change is logged in VERIFICATION.md with its label, reason,
the run that revealed it, and its commit, before the next run (DESIGN §10.4, pilot rules).

**Why does the harness write a machine summary when the agent writes notes anyway?**
An agent that runs out of turns mid-edit may write nothing. Facts like commits, test status, and
migration heads can be collected by a script, so the next session always gets them (course design,
DESIGN §6.3).

**Why is the initializer harness code and not a model session, as in A2?**
For one ticket the initial files are fixed by the ticket text. A2 itself says its two agents differ
only in their first prompt (A2, F-a-52); the course writes the files deterministically (DESIGN §15
D-11).

**What does the screen 3 "↺ redone" marker mean?**
A file changed in session 1 changed again later. It is a hint, not the measure; the judged number is
`redone_lines_pct` from the referee ([post-class reading 03](post-class-reading/03-the-continuity-measure.md)).

## What to try next

- Read the [post-class reading](post-class-reading/README.md), especially 03 on the measurement bug.
- Start assignment A2 ([assignment/README.md](assignment/README.md)): a state layer that carries a
  three-step feature across three forced stops. Run `make check-assignment-2` first; on the starter it
  reports "Self-check: 2 of 28 checks pass."
- In your own repository, stop your coding agent mid-task and start a fresh session. Count the tool
  calls it spends before its first change, then add a handoff file and count again.
- Write down, for your own tickets, which facts a script could put in a handoff (git state, test
  status, schema heads) and which only the agent knows (decisions, dead ends).
