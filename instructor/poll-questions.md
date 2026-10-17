# Poll questions

One prediction poll per section, plus the final feature poll. Each section S1 to S4 opens with its
poll (3 minutes; the poll slide states the feature and the rule at risk), and `make show-N` is
launched right after it. The room predicts the course pilot's result for the section; the answer is
revealed on the all-results slide at the end of the section's demo block. S4 opens with two polls
back to back, the S4 poll and then the final feature poll, and `make show-4` and `make final` are
launched right after the second. Close each poll before the launch. Slide numbers refer to
[../slides/outline.md](../slides/outline.md); timing is in [run-sheet.md](run-sheet.md).

The answers come from pilot runs 3 and 4 and the class-profile round (VERIFICATION.md, "Run 3", "Run
4", "Gate decision", "Class-profile round"). The k=10 experiment batches (M8) were not run, because
the pre-registered gate did not pass; every answer below is the pilot's, with its A/B ids in
[run-sheet.md](run-sheet.md#every-result-on-one-slide-and-one-console-view).

How to use the result: put the room's majority next to the pilot's result on the all-results slide.
A prediction that turns out wrong is the best opening for the discussion; say so before the launch.
In class, note the vote counts of each poll and add them to the after-class record in VERIFICATION.md.

---

## S1 Instructions (slide 8, 3 minutes)

**Question.** Both arms can read every house rule in `docs/HANDBOOK.md`. Only the harness arm gets the
AGENTS.md map and the skill catalogue in its context. The ticket sits next to a legacy handler without
the tenant filter. In the course pilot, 3 A/Bs per run: in how many of 3 runs did each arm add at
least one new tenant-isolation (R1) violation while building F1, org-wide issue search?

| Option | Bare arm | Harness arm (instructions layer) |
|---|---|---|
| A | 0 of 3 | 0 of 3 |
| B | 1-3 of 3 | 0 of 3 |
| C | 0 of 3 | 1-3 of 3 |
| D | 1-3 of 3 | 1-3 of 3 |

**What each answer says.** A: the rule was applied wherever it lived. B: where a rule lives decides
whether the agent applies it (cause 1: A1, F-a-05). C or D: the map does not stop the leak.

**Measure behind it.** S1 primary measure, new R1 violations ≥ 1 per run, reported as runs failing out
of k per arm (DESIGN §8.2).

**The pilot's answer: A.** Run 3 (effort medium, legacy-pattern ticket): 0 of 3 failing in each arm;
run 4 (effort low): 0 of 3 in each; class-profile round: 0 of 1 in each (`ab-20261017-084558-0356a0`).
No measurable difference on this task with this model. No arm copied the legacy handler into a leak.

**Follow-up for the discussion.** "If the bare arm had a 900-line instruction file instead of a
150-line handbook, would it do better or worse?" (A1: "Too much guidance becomes non-guidance.",
F-a-23 to F-a-26; assignment A1).

---

## S2 State and session lifecycle (slide 22, 3 minutes)

**Question.** Building F2 (comments), both arms are stopped after 12 turns of session 1 and resumed in
a fresh session of 38 turns with the same resume sentence. In the course pilot's runs 3 and 4 (6 A/Bs),
which arm showed a continuity failure: R7 fails, a second migration creates the same table, or at
least 30% of the lines added in session 1 are removed in session 2?

| Option | Answer |
|---|---|
| A | Neither arm |
| B | Bare arm only |
| C | Harness arm only |
| D | Both arms |

**What each answer says.** B: the progress file, exec plan, handoff, and Getting up to speed routine
carry state across the reset (A2, F-a-58 to F-a-62; A3, F-a-65). D: the handoff does not prevent the
failure. C would point at the harness's own files getting in the way.

**Measure behind it.** S2 primary measure, continuity failure per run (DESIGN §8.2).

**The pilot's answer: A.** 0 of 3 continuity failures per arm in run 3 and in run 4, and 0 of 1 in
the class-profile round (`ab-20261017-085139-7c0661`). No measurable difference on this task with
this model. Then the catch: the measure cannot fail when session 1 leaves nothing to redo, and 6 of
the 12 arms of runs 3 and 4 built nothing (hidden 3 of 56): two harness arms in run 3, which called
`finish(claim="not_done")` after session 1, and all three bare arms and one harness arm in run 4.
Change 14 (both arms) now lets only that session end; in the class-profile round both arms built the
feature (hidden 56 of 56).

**Follow-up.** "Would a summary of the conversation (compaction) have done the same job?" A2:
"However, compaction isn’t sufficient." (A2, F-a-54)

---

## S3 Scope and sandbox (slide 36, 3 minutes)

**Question.** The scope layer rejects or reverts any change outside the allowed paths, so the harness
arm cannot ship an out-of-scope file. Building F3 (idempotency keys on issue creation, with tempting
shared middleware next to it), what happened to the harness arm's feature in the course pilot?

| Option | Answer |
|---|---|
| A | It shipped a working feature: hidden tests pass, existing tests keep passing |
| B | It shipped a partial feature: some hidden tests fail |
| C | It got stuck on blocked edits and shipped little or nothing |
| D | It did worse than the bare arm on the hidden tests |

**Why this question and not "who has fewer out-of-scope files".** The harness arm's zero is expected
by construction (DESIGN §8.2, S3 note). The interesting result is the secondary measures: did the
enforced arm still ship a working feature?

**Measure behind it.** S3 primary measure (≥ 1 out-of-scope file in the shipped diff, or ≥ 1 source
file changed during the test phase); hidden tests and existing tests as secondary measures for both
arms (DESIGN §8.2).

**The pilot's answer: A, and the bare arm did the same.** Primary measure: 0 of 3 failing per arm in
run 3 and in run 4, 0 of 1 in the class-profile round (`ab-20261017-090051-91f837`); no shipped diff
touched `app/api/middleware.py`. Hidden tests 49 of 49 in every run 4 arm and in both class-round arms.
Post hoc over runs 2-4 (9 runs per arm): every hidden test passed in 9 of 9 runs of each arm, and
existing tests kept passing in 9 of 9; the harness arms shipped a median of 0 tests against 6.

**Follow-up.** "The sandbox is identical for both arms. Why is it in this section at all?" (DESIGN §9:
taught here, never an A/B variable; A4 runs agents in a container, F-a-88.)

---

## S4 Verification (slide 49, 3 minutes)

**Question.** Building F4 (ETag, If-Match, issue history), the referee runs 69 hidden tests
(VERIFICATION.md, M5 counts) and 4 referee-set mutants (`teamtrack/mutants/features/f4.jsonl`) against
the tests each arm shipped. In the course pilot, which arm passed more hidden tests and killed more
mutants?

| Option | Answer |
|---|---|
| A | Harness arm on both counts |
| B | Harness arm on hidden tests only |
| C | Bare arm on mutants |
| D | No clear difference |

**What each answer says.** A: verification the agent does not control (filters, gate, separate
evaluator) changes what ships (A3, F-a-110; B11; B12). C: the arm that shipped more tests killed more
mutants. Remind the room of A4: "it is easy to see tests pass and assume the job is done, when this is
rarely the case." (A4, F-a-17)

**Measure behind it.** S4 co-primary counts per run: hidden tests passed (of 69) and referee-set
mutants killed by shipped tests (of 4); a run passes only with all of both (DESIGN §8.2).

**The pilot's answer: C, and both arms fail the primary measure.** Run 3 (effort medium): bare hidden
66, 66, 69 of 69 with mutants killed 4, 0, 3 of 4; the harness arm shipped no tests in any run, so 0 of
4 mutants each, and one harness arm built a broken change (hidden 27 of 69). Class-profile round
(`ab-20261017-090903-926c02`): hidden 68 of 69 in both arms; mutants bare 4 of 4, harness 1 of 4.
Primary measure: 0 of 3 per arm in run 3, 0 of 1 in the class round. No measurable difference on this
task with this model. Post hoc over runs 2-3 (6 runs per arm): every hidden test passed in 3 of 6 bare
runs and 4 of 6 harness runs.

**Follow-up.** "No done claim in pilot runs 2-4 came with failing hidden tests. What would a gate need
to catch to earn its turns on this model?" (A3, F-a-123: an evaluator is "worth the cost when the task
sits beyond what the current model does reliably solo.")

---

## Final feature poll (slide 50, start of S4, 1 minute)

Ask it right after the S4 poll (2:53, run sheet S4) and close it before the launch. The final A/B
runs during S4; the room sees its results in the final block (3:40).

**Question.** Which feature should both arms build for the final run, with all four layers on? The
winner runs first; the runner-up runs after it.

| Option | Feature | Spec | Sessions | What it stresses |
|---|---|---|---|---|
| A | F5 Bulk close: close all finished issues of a project in one request | `teamtrack/docs/features/f5.md` | One, budget 30 (`teamtrack/reference/f5/task.toml`) | Atomic 404 for any foreign or deleted id (R1), viewers get 403 (R2), one audit row per request (R5) |
| B | F6 Watchers: follow issues and list the ones you watch | `teamtrack/docs/features/f6.md` | Two, budgets 20 and 30 | A session stop in the middle (S2), one new migration (R7), no-op writes add no audit row (R5) |
| C | F7 Labels: tag issues and filter lists by label | `teamtrack/docs/features/f7.md` | Two, budgets 25 and 35 | A session stop (S2), idempotent label creation per org (R4) |

**After the vote.** Terminal C, one minute after `make show-4` (2:55):
`make final FEATURES=<winner>,<runner-up>` when the session figure on show-3's `Cost:` line is at most
$1.10; otherwise `make final FEATURES=<winner>` (run sheet, S4 cost note). `make final` runs the
features one after another. The final has no pre-registered primary measure; every score is shown
(DESIGN §8.2).

**What to compare it with.** The pilot ran no F5-F7 A/B, and the experiment batch that would have
covered them (M8) was not run because the pre-registered gate did not pass. Tonight's final is one dot
per arm: read its hidden-test and mutant counts against the section results on the all-results slide,
never as a verdict on its own. The course's one earlier F5 A/B is the class-profile recording listed in
[fallbacks.md](fallbacks.md).
