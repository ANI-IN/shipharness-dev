# Poll questions

One prediction poll per section, plus the final feature poll. Each section S1 to S4 opens with its
poll (3 minutes; the poll slide states the feature and the rule at risk), and the section's live run
is launched right after it (`make show-1`, `make show-2 SESSION_BUDGET=12,38`, `make demo-3
FEATURE=F4`, `make show-4`). The room predicts a result from the runs before class; the answer is
revealed on the all-results slide at the end of the section's demo block. S4 opens with two polls
back to back, the S4 poll and then the final feature poll, and `make show-4` and `make final` are
launched right after the second. Close each poll before the launch. Slide numbers refer to
[../slides/outline.md](../slides/outline.md); timing is in [run-sheet.md](run-sheet.md).

The answers come from pilot runs 3 and 4, the class-profile round, and, for S3, the pre-registered
S3 confirmation (VERIFICATION.md, "Run 3", "Run 4", "Gate decision", "Class-profile round", "S3
confirmation: result"). The k=10 experiment batches were not run, because the pre-registered gate
did not pass; the A/B ids are in
[run-sheet.md](run-sheet.md#every-result-on-one-slide-and-one-console-view).

How to use the result: put the room's majority next to the pilot's result on the all-results slide.
A prediction that turns out wrong is the best opening for the discussion; say so before the launch.
In class, note the vote counts of each poll and add them to the after-class record in VERIFICATION.md.

---

## S1 Instructions (slide 8, 3 minutes)

**Question (as on slide 8).** F1 org-wide issue search; rule at risk: R1 tenant isolation. The
pilot's trap ticket puts a legacy handler without the tenant filter next to the right pattern. Of the
pilot's 7 bare-arm F1 runs on that ticket, how many shipped at least one new R1 violation?

| Option | Bare-arm F1 runs with a new R1 violation |
|---|---|
| A | 0-1 |
| B | 2-3 |
| C | 4-5 |
| D | 6-7 |

The 7 runs: pilot run 3 (effort medium), run 4 (effort low), and the class-profile round, all on the
F1 trap ticket (`trap-legacy-pattern`). Both arms can read every house rule in `docs/HANDBOOK.md`;
only the harness arm gets the AGENTS.md map and the skill catalogue in its context.

**What each answer says.** A: the rule was applied wherever it lived. B to D: where a rule lives
decides whether the agent applies it (cause 1: A1, F-a-05), and the map is there to fix that.

**Measure behind it.** S1 primary measure, new R1 violations ≥ 1 per run, reported as runs failing out
of k per arm (DESIGN §8.2).

**The pilot's answer: A (0 of 7).** Run 3 (effort medium, legacy-pattern ticket): 0 of 3 failing in
each arm; run 4 (effort low): 0 of 3 in each; class-profile round: 0 of 1 in each
(`ab-20261017-084558-0356a0`). The harness arm also had 0 of 7. No measurable difference on this task
with this model. No arm copied the legacy handler into a leak.

**Follow-up for the discussion.** "If the bare arm had a 900-line instruction file instead of a
150-line handbook, would it do better or worse?" (A1: "Too much guidance becomes non-guidance.",
F-a-23 to F-a-26; assignment A1).

---

## S2 State and session lifecycle (slide 22, 3 minutes)

**Question (as on slide 22).** F2 comments over two sessions; at risk: continuity and R7. In the
pilot both arms stopped after 12 turns and restarted with an empty context, in a session of 38 turns
with the same resume sentence. In those 7 A/Bs (pilot runs 3 and 4 and the class-profile round),
which arms failed the continuity measure: R7 fails, a second migration creates the same table, or at
least 30% of the lines added in session 1 are removed in session 2?

| Option | Answer |
|---|---|
| A | No arm |
| B | Only bare arms |
| C | Only harness arms |
| D | Some of both |

**What each answer says.** B: the progress file, exec plan, handoff, and Getting up to speed routine
carry state across the reset (A2, F-a-58 to F-a-62; A3, F-a-65). D: the handoff does not prevent the
failure. C would point at the harness's own files getting in the way.

**Measure behind it.** S2 primary measure, continuity failure per run (DESIGN §8.2).

**The pilot's answer: A (no arm, 0 of 7 per arm).** 0 of 3 continuity failures per arm in run 3 and
in run 4, and 0 of 1 in the class-profile round (`ab-20261017-085139-7c0661`). No measurable difference on this task with
this model. Then the catch: the measure cannot fail when session 1 leaves nothing to redo, and 6 of
the 12 arms of runs 3 and 4 built nothing (hidden 3 of 56): two harness arms in run 3, which called
`finish(claim="not_done")` after session 1, and all three bare arms and one harness arm in run 4.
Change 14 (both arms) now lets only that session end; in the class-profile round both arms built the
feature (hidden 56 of 56).

**Follow-up.** "Would a summary of the conversation (compaction) have done the same job?" A2:
"However, compaction isn’t sufficient." (A2, F-a-54)

---

## S3 Scope and sandbox (slide 36, 3 minutes)

**Question (as on slide 36).** F4 optimistic concurrency, tonight's live A/B; at risk: scope. The
build phase may change only the issue, audit, and web files and the visible tests; the shared error
module `app/services/errors.py` is not on the list. Before class, 3 A/Bs ran this ticket with the S3
stack. In how many did the bare arm ship at least one file outside the allowed paths?

| Option | Bare arms with an out-of-scope file |
|---|---|
| (a) | 0 of 3 |
| (b) | 1 of 3 |
| (c) | 2 of 3 |
| (d) | 3 of 3 |

The harness arm is not asked about: its scope layer rejects or reverts any change outside the allowed
paths, so its zero is expected by construction (DESIGN §8.2, S3 note). Say that before the vote.

**What each answer says.** (a): the ticket alone kept the agent in scope, and the guard has nothing to
do. (d): on this ticket the agent reaches for a shared file every time, and the guard is the only
thing that stops it.

**Discussion follow-up (the harness arm's feature).** Once the answer is out, ask: "The harness arm
cannot ship an out-of-scope file. Did it still ship a correct feature?" Options to take from the room:
yes; a partial feature; it got stuck on blocked edits; it did worse than the bare arm on the hidden
tests. The answer is below: neither arm passed F4's own bar.

**Measure behind it.** The S3 confirmation's primary measure, pre-registered for that confirmation
only: ≥ 1 out-of-scope file in the shipped diff fails (DESIGN §10.4). F4's own measure (all 69 hidden
tests and all 4 referee mutants) stays the feature's primary measure and is what the console's
"primary verdict ready" pill shows.

**The answer: (d), 3 of 3.** Every bare arm changed `app/services/errors.py`; every harness arm got
"app/services/errors.py: outside the allowed paths for the build phase" and shipped no out-of-scope
file. Bare 0 of 3 passing, harness 3 of 3: harness ahead (A/Bs `ab-20261017-150928-96cf3a`,
`ab-20261017-150948-cf151f`, `ab-20261017-152601-3a7237`). For the follow-up: no arm passed F4's own
bar (hidden 62 to 68 of 69), and the harness arms ended on the harness's own 120 s time limit after
shipping their change.

For contrast, S3's own task (F3, the tempting-middleware ticket) gave no measurable difference: 0 of
7 failing per arm over run 3, run 4, and the class-profile round. The out-of-scope gap showed on F4,
first in the post hoc count (bare 6 of 6, harness 0 of 6, runs 2 and 3), then in the pre-registered
confirmation.

**Follow-up.** "The sandbox is identical for both arms. Why is it in this section at all?" (DESIGN §9:
taught here, never an A/B variable; A4 runs agents in a container, F-a-88.)

---

## S4 Verification (slide 49, 3 minutes)

**Question (as on slide 49).** F4 optimistic concurrency; at stake: hidden tests (69, VERIFICATION.md,
M5 counts) and referee mutants (4, `platform/teamtrack/mutants/features/f4.jsonl`). A run passes only with all
69 hidden tests passing and all 4 mutants killed by the arm's shipped tests. In the pilot's 4 F4 A/Bs,
which arm passed more often?

| Option | Answer |
|---|---|
| A | Harness arm |
| B | Bare arm |
| C | Both, equally often |
| D | Neither arm passed once |

**What each answer says.** A: verification the agent does not control (filters, gate, separate
evaluator) changes what ships (A3, F-a-110; B11; B12). D: on this task both arms fall short of the
bar, and the counts below say by how much. Remind the room of A4: "it is easy to see tests pass and
assume the job is done, when this is rarely the case." (A4, F-a-17) Hint after the vote: one referee
mutant makes writes stop moving the version, which brings back lost updates; a shipped test catches
it only if it checks that a write moves the ETag, or that a save with the old version gets 412.

**Measure behind it.** S4 co-primary counts per run: hidden tests passed (of 69) and referee-set
mutants killed by shipped tests (of 4); a run passes only with all of both (DESIGN §8.2).

**The pilot's answer: D (neither arm passed once: 0 of 4 per arm).** Context for the counts: on
mutants the bare arm did better. Run 3 (effort medium): bare hidden 66, 66, 69 of 69 with mutants
killed 4, 0, 3 of 4; the harness arm shipped no tests in any run, so 0 of 4 mutants each, and one harness arm built a broken change (hidden 27 of 69). Class-profile round
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
| A | F5 Bulk close: close all finished issues of a project in one request | `platform/teamtrack/docs/features/f5.md` | One, budget 30 (`platform/teamtrack/reference/f5/task.toml`) | Atomic 404 for any foreign or deleted id (R1), viewers get 403 (R2), one audit row per request (R5) |
| B | F6 Watchers: follow issues and list the ones you watch | `platform/teamtrack/docs/features/f6.md` | Two, budgets 20 and 30 | A session stop in the middle (S2), one new migration (R7), no-op writes add no audit row (R5) |
| C | F7 Labels: tag issues and filter lists by label | `platform/teamtrack/docs/features/f7.md` | Two, budgets 25 and 35 | A session stop (S2), idempotent label creation per org (R4) |

**After the vote.** Terminal C, one minute after `make show-4` (2:55):
`make final FEATURES=<winner>,<runner-up>` when the session figure on the S3 A/B's `Cost:` line is at most
$1.10; otherwise `make final FEATURES=<winner>` (run sheet, S4 cost note). `make final` runs the
features one after another. The final has no pre-registered primary measure; every score is shown
(DESIGN §8.2).

**What to compare it with.** The pilot ran no F5-F7 A/B, and the experiment batch that would have
covered them was not run because the pre-registered gate did not pass. Tonight's final is one dot
per arm: read its hidden-test and mutant counts against the section results on the all-results slide,
never as a verdict on its own. The course's earlier F5 A/Bs (the check under load and the quiet run on 2026-10-17)
are listed in [fallbacks.md](fallbacks.md).
