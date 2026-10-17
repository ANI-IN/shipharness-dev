# Option A: changes to submodules/04-verification/concepts.md

Draft, not applied. Line numbers refer to the file at 67cfb3c. Each change gives what changes, the
proposed text between `proposed` markers (public wording, ready to paste), and what stays. Word count:
3,138 now; 3,146 after these changes (counted by applying them to a copy).

What stays: the opening; §1 with the run 2 table, the A/B ids, and the captured verdicts (only its
bullets get shorter); §2 except one shortened paragraph (the bare arm did fail here, as cause 4
predicts); the §3 table, the start of §3.1, §3.3's filter table, and §3.5's first paragraph; §4
except the sequence diagram; §5's co-primary counts, the disclosed overlap (its end shortened), and
the three M8 markers. The run 3 results and the post hoc findings move into a new §6.

## Change 1. Section 1, the three bullets under the run 2 table (lines 55-67): replace

<!-- proposed replace 55-67 -->
- **The bare arm** killed most referee mutants but missed something every time: A/B 2 failed 3
  hidden tests, and A/Bs 1 and 3 each left one mutant alive (in A/B 1, the lost-update mutant
  `app.services.issues-m401`). The measure needs all 69 and all 4.
- **The harness arm** shipped 0, 0, and 3 tests, none of them from the 12-turn test phase, and killed
  0, 0, and 2 mutants. Turns ran out: every session repeated A2's "Getting up to speed" steps (A2,
  F-a-58 to F-a-62) and re-read 3 to 7 instruction documents and about 15 product files.
- **No arm called `finish(claim="done")`.** Every arm used its 40 build turns, so its claim was
  `none` and the verify gate never ran.
<!-- /proposed -->

## Change 1a. Section 2, the A2 paragraph (lines 92-94): replace

<!-- proposed replace 92-94 -->
A2's single agent was told to "Self-verify all features." (A2, F-a-108); the separate evaluator as a
working design comes from A3.
<!-- /proposed -->

## Change 1b. Section 3.1, the course-design paragraph (lines 141-143): replace

S3 explains this rule; S4 keeps one sentence.

<!-- proposed replace 141-143 -->
Only after the gate passes does the scope layer set `passes: true` (course design, explained in S3,
after A3, F-a-110).
<!-- /proposed -->

## Change 1c. Section 3.2, the list of checks (lines 149-154): replace

<!-- proposed replace 149-154 -->
Both arms can read the rules in `docs/HANDBOOK.md`. The checks in `src/shipharness/checks/` cover R1
tenant isolation (foreign IDs get 404), R2 roles, R3 conventions, R4 idempotent creates, R5 one audit
row per write, R6 layering, and R7 migrations, each counting **new** violations against the
checkpoint baseline (`mark_baseline` in `src/shipharness/checks/base.py`).
<!-- /proposed -->

## Change 2. Section 3.3, the paragraph after the filter table notes (lines 173-181): replace

Drops the `testgen` sentence (it is in the post-class reading); keeps the captured discard reason.

<!-- proposed replace 173-181 -->
The filters judge only the tests proposed in the test phase
(`src/shipharness/harness/verify/testphase.py`); tests written in the build phase ship without them.
Every discard carries a reason: in A/B 3 of pilot run 2 the harness arm's one test-phase test stopped
at filter 2 with `failed on run 1 of 5: assert None is not None` (captured on 2026-10-16, run
ab-20261016-191626-6100f6, `test_filter_result` event; your output will differ). In `make demo-4`
the test-phase context has no mutant list and no target module, so filter 3 decides by coverage and
filter 4 checks assertions only.
<!-- /proposed -->

## Change 3. Section 3.4, second paragraph (lines 190-199): replace

<!-- proposed replace 190-199 -->
shipharness uses hand-written mutants applied one at a time (course design: mutmut cannot target
chosen lines), split per file into a **filter set** (visible to filter 3) and a **referee set** (held
out) that never share a mutation (`overlaps` in `src/shipharness/filters/mutant_sets.py`). F4's four
referee mutants (`teamtrack/mutants/features/f4.jsonl`) target the risky lines:
`app.services.issues-m401` turns `issue.version += 1` into `+= 0`, so "stale If-Match values still
match (lost update)". A kill counts only with shipped tests that pass on the arm's unmutated build
(`_passing_unmutated` in `src/shipharness/ab/referee.py`), so a broken test cannot "kill" anything.
<!-- /proposed -->

## Change 3a. Section 3.5, second paragraph (lines 208-213): replace

<!-- proposed replace 208-213 -->
A3 grades against "grading criteria" (A3, F-a-114) with a hard threshold each (A3, F-a-119). The
course reviewer takes its criteria from the harness's `docs/SECURITY.md` and `ARCHITECTURE.md`
(`src/shipharness/reviewer/criteria.py`), the same for both arms. "Blinded" is A/B design, not a
source term: the reviewer sees the ticket and a diff with every arm-identifying trace removed, and
runs on both final diffs, never inside the gate (course design).
<!-- /proposed -->

## Change 4. Section 4, "The flow of a done claim" (lines 239-258): delete

§3.1 describes the same flow in text; the diagram can move to the post-class reading.

<!-- proposed replace 239-258 -->
<!-- /proposed -->

## Change 4a. Section 5, the end of "Disclosed overlap" (lines 298-300): replace

The A3 quote moves to S4's new §6 framing; the citation stays.

<!-- proposed replace 298-300 -->
**layer switch** (`make demo-4 LAYERS=-verify`) removes the verify layer, A3's leave-one-out idea
(A3, F-a-125).
<!-- /proposed -->

## Change 5. Section 5, Results (lines 304-327): replace

The change log and the run 3 table move to §6; the three M8 markers stay here.

<!-- proposed replace 304-327 -->
Section 6 gives the pilot results and what they say about the gate and the filters.
<!-- /proposed -->

## Change 6. New section 6, after line 334: insert

<!-- proposed insert 334 -->
---

## 6. What the gate and filters assume, and what the pilot measured

A3: "every component in a harness encodes an assumption about what the model can't do on its own,
and those assumptions are worth stress testing" (A3, F-a-124). The verification layer's assumption,
in the course's words: the agent's "done" and its own tests cannot be trusted. Its basis is cause 4
(A3, F-a-15; A4, F-a-17; B13, F-b-45).

### 6.1 Changes before run 3

After run 2 the course changed the harness arm only: state files are updated only in the wrap-up
turns, and a test-phase session opens with "write the tests for the feature first"
(`TEST_PHASE_FIRST` in `src/shipharness/harness/state/lifecycle.py`; course wording). Two
measurement changes for both arms changed no outcome.

### 6.2 Run 3: the primary measure

Measured in the course pilot, run 3, 2026-10-16 (F4 canonical, effort medium): both arms failed the
primary measure in 3 of 3 A/Bs.

| Count per A/B (A/Bs 1, 2, 3 of pilot run 3) | Bare arm | Harness arm |
|---|---|---|
| Hidden tests passed, of 69 | 66, 66, 69 | 27, 69, 69 |
| Referee mutants killed, of 4 | 4, 0, 3 | 0, 0, 0 |
| Tests shipped (score records) | 23, 0, 5 | 0, 0, 0 |

Values in A/B order: ab-20261016-212252-aa1644, ab-20261016-214151-ca9841, ab-20261016-220010-c5b4bf.
In the first, the harness arm also built a broken change (3 new R1 violations). Run 4 (effort low)
ran F1-F3 only. No measurable difference on this task with this model (course pilot, run 3).

### 6.3 What the result says about the pieces

Unless a run is named, these points use measures chosen after the results: post hoc and descriptive.

- **The arms did not fail by claiming too much.** Over all four sections (34 runs per arm), no done
  claim came with failing hidden tests, in either arm. One bare F4 done claim failed the primary
  measure another way: in ab-20261016-220010-c5b4bf the build passed 69 of 69 hidden tests, and one
  of four referee mutants survived its shipped tests. On F4 the harness arm never called `finish` in
  runs 2 and 3, so its gate never ran.
- **They ran out of time.** In run 3 every bare F4 arm hit the agent time limit, and the limit cut the
  harness arm's test phase in two runs. Over runs 2 and 3, each arm hit it in 4 of 6 F4 runs.
- **The harness arm shipped almost no tests.** On F4 harness arms shipped a median of 0 tests against
  15.5; over all sections, 2.5 against 7.5. The five filters cannot keep a test that is never proposed.

A3 says of its own evaluator that it "is not a fixed yes-or-no decision. It is worth the cost when the
task sits beyond what the current model does reliably solo." (A3, F-a-123). In these runs the case the
gate is built for, a "done" that the referee contradicts, came up once, in the bare arm, and the
harness arm never reached its gate on F4.

### 6.4 What the next round tests

Round 5, the course's next pre-registered pilot round, gives both arms a longer agent time limit (the
same for both) and looks at why the harness arm's test phase ships no tests.

[[PENDING: F4 round 5 result with a longer agent time limit for both arms (hidden x of 69 and referee mutants y of 4 per run per arm), and what the test-phase investigation found, with A/B ids and run ids | source: M6 pilot | how: course pilot (build repository)]]

<!-- /proposed -->

## Evidence (private)

| Statement | VERIFICATION.md (main), M6 pilot |
|---|---|
| Run 2 bullets (unchanged facts) | "Run 2" table, F4 rows; harness arm turn use |
| Change 9, changes 10 and 11, 181 tests from 17 arms | "Pilot-driven changes after run 2" and the equivalence check |
| Run 3 table, broken change, every bare arm at the time limit | "Run 3" table, F4 rows; per-A/B harness hidden values from the current §5 (score records) |
| No done claim with failing hidden tests (0 of 19 bare, 0 of 10 harness) | "Exploratory analysis", rows "All bare", "All harness", column "False done" |
| `ab-20261016-220010-c5b4bf`: 69 of 69, one mutant survived | same section, "Claims" bullet |
| F4 claimed done 0 of 6 harness; time limit 4 of 6 each; shipped median 0 and 15.5 | rows "F4 bare", "F4 harness" |
| Test phase cut by the time limit in two harness runs | "Run 3", F4 harness row |
| "never reached its gate on F4" | run logs (`events.jsonl` of the six F4 A/Bs of runs 2 and 3, read 2026-10-17): no `finish` tool call by the harness arm in any of them; its only verify decisions are the gate baseline and the test-filter summary. The single `finish` call is the bare arm's in `ab-20261016-220010-c5b4bf` |
