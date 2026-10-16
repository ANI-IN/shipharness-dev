# Poll questions

One prediction poll per section, plus the final feature poll. Each section S1 to S4 opens with its
poll (3 minutes; the poll slide states the feature and the rule at risk), and `make demo-N` is
launched right after it, so the A/B runs while the concepts and the walkthrough are taught. Close each
poll before the launch, so nobody votes after seeing the console. Slide numbers refer to
[../slides/outline.md](../slides/outline.md); timing is in [run-sheet.md](run-sheet.md).

Status: M11 draft. The answer patterns come from the experiments and are `[[PENDING]]` until M8 has
run. Do not present an expected answer as a fact before then.

How to use the result: put the room's majority next to tonight's dots and the experiment dots on
screen 4 (or `exports/report.html`) in the section's demo block. A prediction that turns out wrong
is the best opening for the discussion; say so before the launch.

---

## S1 Instructions (slide 8, 3 minutes)

**Question.** Both arms can read every house rule in `docs/HANDBOOK.md`. Only the harness arm gets the
AGENTS.md map and the skill catalogue in its context. In how many of 10 runs does each arm add at
least one new tenant-isolation (R1) violation while building F1, org-wide issue search?

| Option | Bare arm | Harness arm (instructions layer) |
|---|---|---|
| A | 0-2 of 10 | 0-2 of 10 |
| B | 3-6 of 10 | 0-2 of 10 |
| C | 7-10 of 10 | 0-2 of 10 |
| D | About the same for both arms | |

**What each answer says.** A: the rules are easy enough that location does not matter. B or C: where
a rule lives decides whether the agent applies it (cause 1: A1, F-a-05). D: the map adds nothing over
a handbook on disk.

**Measure behind it.** S1 primary measure, new R1 violations ≥ 1 per run, reported as runs failing out
of k per arm (DESIGN §8.2).

**Answer pattern from the experiments.**

[[PENDING: S1 runs failing out of 10 per arm (F1 canonical) | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

**Follow-up for the discussion.** "If the bare arm had a 900-line instruction file instead of a
150-line handbook, would it do better or worse?" (A1: "Too much guidance becomes non-guidance.",
F-a-23 to F-a-26; assignment A1).

---

## S2 State and session lifecycle (slide 22, 3 minutes)

**Question.** Building F2 (comments), both arms are stopped after 20 turns of session 1 and resumed in
a fresh session with the same resume sentence. Which arm shows a continuity failure: R7 fails (more
than one migration head, or a fresh upgrade fails), a second migration creates the same table, or at
least 30% of the lines added in session 1 are removed in session 2?

| Option | Answer |
|---|---|
| A | Neither arm |
| B | Bare arm only |
| C | Harness arm only |
| D | Both arms |

**What each answer says.** B: the progress file, exec plan, handoff, and Getting up to speed routine
carry state across the reset (A2, F-a-58 to F-a-62; A3, F-a-65). D: the handoff does not prevent the
failure. C would point at the harness's own files getting in the way; look at screen 3 "Sessions" for
redone work.

**Measure behind it.** S2 primary measure, continuity failure per run (DESIGN §8.2).

**Answer pattern from the experiments.**

[[PENDING: S2 continuity failures out of 10 per arm (F2 canonical), with the component that failed | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

**Follow-up.** "Would a summary of the conversation (compaction) have done the same job?" A2:
"However, compaction isn’t sufficient." (A2, F-a-54)

---

## S3 Scope and sandbox (slide 36, 3 minutes)

**Question.** The scope layer rejects or reverts any change outside the allowed paths, so the harness
arm cannot ship an out-of-scope file. Building F3 (idempotency keys on issue creation), what happens to
the harness arm's feature?

| Option | Answer |
|---|---|
| A | It ships a working feature: hidden tests pass, existing tests keep passing |
| B | It ships a partial feature: some hidden tests fail |
| C | It gets stuck on blocked edits and ships little or nothing |
| D | Same result as the bare arm on the hidden tests |

**Why this question and not "who has fewer out-of-scope files".** The harness arm's zero is expected
by construction (DESIGN §8.2, S3 note). The interesting result is the secondary measures: did the
enforced arm still ship a working feature?

**Measure behind it.** S3 primary measure (≥ 1 out-of-scope file in the shipped diff, or ≥ 1 source
file changed during the test phase) for the bare arm; hidden tests and existing tests as secondary
measures for both arms (DESIGN §8.2).

**Answer pattern from the experiments.**

[[PENDING: S3 runs failing the primary measure out of 10 per arm, and hidden tests passed per run per arm (F3 canonical) | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

**Follow-up.** "The sandbox is identical for both arms. Why is it in this section at all?" (DESIGN §9:
taught here, never an A/B variable; A4 runs agents in a container, F-a-88.)

---

## S4 Verification (slide 49, 3 minutes)

**Question.** Building F4 (ETag, If-Match, issue history), both arms' visible tests pass at the end.
The referee then runs 69 hidden tests (VERIFICATION.md, M5 counts) and 4 referee-set mutants
(`teamtrack/mutants/features/f4.jsonl`) against the tests each arm shipped. Which arm passes more
hidden tests and kills more mutants?

| Option | Answer |
|---|---|
| A | Harness arm on both counts |
| B | Harness arm on hidden tests only |
| C | Harness arm on mutants only |
| D | No clear difference |

**What each answer says.** A: verification the agent does not control (filters, gate, separate
evaluator) changes what ships (A3, F-a-110; B11; B12). D: passing visible tests was already enough for
this feature. Remind the room of A4: "it is easy to see tests pass and assume the job is done, when
this is rarely the case." (A4, F-a-17)

**Measure behind it.** S4 co-primary counts per run: hidden tests passed (of 69) and referee-set
mutants killed by shipped tests (of 4) (DESIGN §8.2).

**Answer pattern from the experiments.**

[[PENDING: S4 hidden tests passed of 69 and mutants killed of 4, one dot per run per arm (F4 canonical) | source: M8 batch 1 | how: make experiments batch 1; make report; VERIFICATION.md]]

**Follow-up.** "The reviewer is blinded. Did it agree with the referee?" (screen 4, reviewer
agreement; A3, F-a-112 on evaluator leniency)

---

## Final feature poll (slide 63, 1 minute)

**Question.** Which feature should both arms build for the final run, with all four layers on?

| Option | Feature | Spec | Sessions | What it stresses |
|---|---|---|---|---|
| A | F5 Bulk close: close all finished issues of a project in one request | `teamtrack/docs/features/f5.md` | One, budget 30 (`teamtrack/reference/f5/task.toml`) | Atomic 404 for any foreign or deleted id (R1), viewers get 403 (R2), one audit row per request (R5) |
| B | F6 Watchers: follow issues and list the ones you watch | `teamtrack/docs/features/f6.md` | Two, budgets 20 and 30 | A session stop in the middle (S2), one new migration (R7), no-op writes add no audit row (R5) |
| C | F7 Labels: tag issues and filter lists by label | `teamtrack/docs/features/f7.md` | Two, budgets 25 and 35 | A session stop (S2), idempotent label creation per org (R4) |

**After the vote.** Run only the winner: `make final FEATURES=<F5|F6|F7>` (run sheet, final). The
final has no pre-registered primary measure; every score is shown (DESIGN §8.2).

**Answer pattern from the experiments.** F5-F7 run in the full-dataset batch, so there are experiment
results to show next to tonight's run:

[[PENDING: F5, F6, F7 canonical results per arm (all scores) | source: M8 batch 4 | how: make experiments, full dataset; make report; VERIFICATION.md]]

[[PENDING: room vote counts for each poll | source: live class | how: poll tool export]]
