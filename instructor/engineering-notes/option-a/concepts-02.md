# Option A: changes to submodules/02-state-lifecycle/concepts.md

Draft, not applied. Line numbers refer to the file at 67cfb3c. Each change gives what changes, the
proposed text between `proposed` markers (public wording, ready to paste), and what stays. Word count:
3,416 now; 3,092 after these changes (counted by applying them to a copy).

What stays: §1 up to the `git status` capture (its reading shortened) and the M6 pilot marker (line
71); §2 unchanged (§2.3 already says resets are model-dependent, A3 F-a-69); §3 except its last
paragraph, shortened; §4.1 with `init.sh`, §4.2, §4.3's wrap-up and session-log text, §4.4's text;
§5's measure and its two limits. Shortened: the `progress.md` paragraph, the `session_stop` excerpt
(replaced by a pointer to the anchor), the machine-summary paragraph, the score-record paragraph.
Deleted: two diagrams. §6 is rewritten around the claim.

## Change 0. Section 1, the reading of the capture (lines 57-61): replace

Shorter; the A3 link moves to §6.

<!-- proposed replace 57-61 -->
It then read the migration and carried on. A6, about Claude models: "Claude's latest models are
extremely effective at discovering state from the local filesystem." (A6, F-a-76; a living page,
accessed 2026-10-16). The pilot model is not a Claude model: one observation that fits A6, not a test.
<!-- /proposed -->

## Change 1. Section 1, after the capture (lines 63-69): replace

The run 2 bug and the run 3 numbers move to §6; the run 3 A/B stays here because the M6 pilot marker
on line 71 refers to it.

<!-- proposed replace 63-69 -->
In run 3 the bare arm passed again with a 12-turn first session (A/B `ab-20261016-213317-9a0ec1`, run
`r-20261016-213317-97004c`: 3 sessions, `continuity_failure` false, 56 of 56 hidden tests). Section 6
has every pilot run on F2 and what the results say about the state files.
<!-- /proposed -->

## Change 0b. Section 3, last paragraph (lines 143-147): replace

<!-- proposed replace 143-147 -->
A2's initializer is a model session with its own first prompt (A2, F-a-52). The course writes the
initial files with deterministic harness code instead, because one ticket fixes them (course design).
The state layer never calls the model.
<!-- /proposed -->

## Change 0c. Section 4.1, the `progress.md` paragraph (lines 164-166): replace

<!-- proposed replace 164-166 -->
`progress.md` has the sections `Current feature`, `Done`, `In progress`, `Next` (the agent's), and
`Session log` (the harness's, one entry per session).
<!-- /proposed -->

## Change 1b. Section 4.3, the `session_stop` excerpt (lines 210-231): replace

The excerpt is shown in the walkthrough; the text keeps what it does and how to print it.

<!-- proposed replace 210-231 -->
When the session ends, `session_stop` (anchor `S2:stop_resume`,
`src/shipharness/harness/state/lifecycle.py`, lines 96-120) writes the harness's part of the handoff
and a progress log entry, whatever the agent did, and commits both. Print it with
`uv run python scripts/anchors.py extract S2:stop_resume`.
<!-- /proposed -->

## Change 1c. Section 4.3, the machine summary paragraph (lines 233-237): replace

<!-- proposed replace 233-237 -->
The machine summary (`handoff.py`) lists commits, files changed, visible-test status, open TODO
markers, migration heads (with "house rule R7 needs exactly one" when there is more than one), and
the documents read. It never touches the agent's notes; writing it when the agent writes nothing is
course design.
<!-- /proposed -->

## Change 2. Section 4.4, the sequence diagram and its caption (lines 251-272): delete

The text of §4.2 to §4.4 already gives the order; the diagram can move to the post-class reading
unchanged.

<!-- proposed replace 251-272 -->
<!-- /proposed -->

## Change 2b. Section 5, score record and session patches (lines 285-292): replace

<!-- proposed replace 285-292 -->
Results are runs failing out of k, per arm, one dot per run; the components and `redone_lines_pct`
(the share of session 1's added lines that session 2 removes) are secondary (`src/shipharness/ab/score.py`).
Session patches come from each session's working-tree snapshots, so an arm that never commits is
measured like one that does; the referee strips the harness's files from them and runs the check in
its own container (`ab/demo.py`, `ab/referee.py`).
<!-- /proposed -->

## Change 3. Section 5, the decision flowchart and its caption (lines 293-305): delete

The three bullets (a), (b), (c) above it give the same decision.

<!-- proposed replace 293-305 -->
<!-- /proposed -->

## Change 4. Section 6 (lines 318-381): replace

<!-- proposed replace 318-381 -->
## 6. What the state files assume, and what the pilot measured

A3: "every component in a harness encodes an assumption about what the model can't do on its own,
and those assumptions are worth stress testing" (A3, F-a-124). The state files' assumption, in the
course's words: a fresh session cannot pick up the work from the repository alone, the problem A2
names (A2, F-a-08). A3 tested its own version of this piece and dropped it when the model changed
(A3, F-a-69, section 2.3).

### 6.1 Run 2: a bug, and a cost

Measured in the course pilot, run 2, 2026-10-16 (F2 canonical, effort medium; A/Bs
`ab-20261016-181736-08a9c4`, `ab-20261016-184318-636e90`, `ab-20261016-190548-ae9abe`): the bare arm
passed in 3 of 3, the harness arm in 0 of 3, because of a measurement bug: the check counted session
2's rewrite of the harness's own state files as removing 50-84% of session 1's lines. The fix, for
both arms, strips those files first; the primary measure is unchanged.

The same run showed the piece's cost. Every harness session re-read 3 to 7 instruction documents and
about 15 product files and updated its state files mid-session; the F2 harness arms made 0 to 1
product patches in 50 build turns. That is A4's orienting cost (A4, F-a-10), caused by the harness.
The change that followed (harness arm only) is in sections 4.2 and 4.3.

### 6.2 Runs 3 and 4: the primary measure

Both runs used a 12-turn first session and 38 turns after it, for both arms
(`--session-budget 12,38`). Measured in the course pilot, run 3, 2026-10-16 (effort medium), A/Bs
`ab-20261016-211419-dfe06f`, `ab-20261016-213317-9a0ec1`, `ab-20261016-214959-de790f`; and run 4,
effort low, 2026-10-16/17, A/Bs `ab-20261016-232842-ac03b2`, `ab-20261016-234027-226a76`,
`ab-20261016-235211-ea59a9`. Values in A/B order:

| Run | Arm | Primary passed | Agent time limit hit | Hidden tests passed (of 56) | `redone_lines_pct` |
|---|---|---|---|---|---|
| 3 | bare | 3/3 | 0/3 | 56, 56, 56 | 0.0, 5.3, 0.0 |
| 3 | harness | 3/3 | 2/3 | 56, 3, 3 | 0.0, 0.0, 0.0 |
| 4, effort low | bare | 3/3 | 0/3 | 3, 3, 3 | 0.0, 0.0, 0.0 |
| 4, effort low | harness | 3/3 | 1/3 | 56, 3, 56 | 0.0, 0.0, 0.0 |

No measurable difference on this task with this model (course pilot, runs 3 and 4):
`continuity_failure` was false in all 12 arms.

### 6.3 What the result says about the piece

- **The bare arm found its own state.** Section 1 shows it starting session 2 with `git status`, and
  in run 3 it passed all three A/Bs with every hidden test. On this task and this model the
  assumption did not hold.
- **The measure has a blind spot.** Six arms built nothing (3 of 56 hidden tests): the harness arms
  of `ab-20261016-213317-9a0ec1` and `ab-20261016-214959-de790f`, and in run 4 all three bare arms and
  the harness arm of `ab-20261016-234027-226a76`. The check cannot fail when session 1 leaves no
  product lines to redo: a pass says nothing was broken or redone, not that the feature was built.
- **A harness piece caused a failure.** In those two run 3 A/Bs the harness arm called
  `finish(claim="not_done")` at the end of the 12-turn first session, which ended the build phase; the
  38-turn session never ran. The course traced it to the harness arm's wrap-up message, which led the
  agent to call `finish`.

### 6.4 Post hoc: what else the arms did

These measures were chosen after the results, so they describe and do not test (9 runs per arm, runs
2 to 4). Harness arms hit the agent time limit in 4 runs, bare arms in 0; median arm wall time was 361
s against 232 s; every hidden test passed in 3 harness runs and 4 bare runs; harness arms shipped a
median of 0 tests against 8.

The lesson for your own harness: state files cost turns, and an A/B can show it, as A3 found for
resets (A3, F-a-68, section 2.3).

### 6.5 What the next round tests

Round 5, the course's next pre-registered pilot round, fixes the harness arm's early finish and, for
that round only, uses a primary measure that an arm which builds nothing cannot pass: no continuity
failure and at least 50% of the hidden tests passed.

[[PENDING: F2 round 5 result after the early-finish fix, runs passing "continuity AND at least 50% of hidden tests" out of k per arm, with A/B ids and run ids | source: M6 pilot | how: course pilot (build repository)]]

[[PENDING: the S2 class task decision | source: M6 pilot | how: course pilot (build repository)]]

The pilot gate did not pass (course pilot, 2026-10-17), so the class task is the instructor's decision.

[[PENDING: S2 primary measure, continuity_failure runs out of k=10 per arm, with components (a), (b), (c) and redone_lines_pct per run, and run ids | source: M8 batch 1 | how: uv run shipharness experiments --split section-2 --k 10 --reviewer --batch batch-1, then uv run shipharness report]]

[[PENDING: ablation result for leaving the state layer out on the S2 tasks | source: M8 ablation | how: uv run shipharness experiments --split section-2 --k 2 --layers=-state --batch ablation, then uv run shipharness report]]
<!-- /proposed -->

## Evidence (private)

| Statement | VERIFICATION.md (main), M6 pilot |
|---|---|
| Run 2 F2 3/3 and 0/3; the bug, 50-84% | "Run 2" table, F2 rows; change 7 |
| 3 to 7 documents, about 15 product files, 0 to 1 product patches in 50 build turns | "Run 2", harness arm turn use; change 9 |
| Runs 3 and 4 table | "Run 3" and "Run 4" tables; values per A/B from the current §6 (score records) |
| Six arms built nothing | "Run 4", "F2 across runs 3 and 4" |
| Early finish; wrap-up message as the cause | "Run 3" F2 harness row; "Overnight decisions after run 3", third bullet |
| Post hoc: 4/9 and 0/9, 361 s and 232 s, 3/9 and 4/9, median 0 and 8 | "Exploratory analysis", rows "F2 bare", "F2 harness" |
| Round 5 design | owner, 2026-10-17 (task brief for this draft) |
