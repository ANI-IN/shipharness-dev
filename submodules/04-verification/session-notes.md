# S4 session notes: Verification

For learners, after class. Reading time: about 7 minutes. Concepts in full:
[concepts.md](concepts.md). Instructor runbook: [demo/README.md](demo/README.md).

"S4 Verification" and "house rules" are course labels. Source IDs such as (A3, F-a-110) point to
[RESEARCH.md](../../RESEARCH.md); quotes are copied from it.

## What was shown

1. **Poll.** Building F4 (ETag, If-Match, issue history), which arm passes more of the 69 hidden
   tests and kills more of the 4 referee mutants? Then the final feature poll (F5, F6, or F7).
2. **Two launches.** `make demo-4` (F4 from checkpoint `m1-s4-start`, bare arm vs the harness arm
   with all four layers) and, a minute later, `make final FEATURES=<poll winner(s)>`. Both ran
   while the concepts and the code were on screen.
3. **Concepts.** The problem (F4's `If-Match` header is optional, so every existing test keeps
   passing whether or not concurrency works), the cause (the agent judges its own work; visible
   tests miss what held-out tests catch), and the harness piece: the verify gate, R1-R7 checks,
   clean state, five test filters, targeted mutants in two disjoint sets, and the blinded reviewer.
4. **Code walkthrough.** Four anchors, each printed by `uv run python scripts/anchors.py extract
   <id>`: `S4:filters` (`src/shipharness/filters/pipeline.py`), `S4:probe`
   (`src/shipharness/checks/r1_tenant.py`), `S4:blind` (`src/shipharness/reviewer/blind.py`),
   `S4:gate` (`src/shipharness/harness/verify/gate.py`).
5. **Demo block.** Screen 1 (gate pills and "Agent said" vs "Referee"), screen 2 (the two-tab edit
   conflict), screen 3 (filter table, mutant matrix, referee counters), the terminal verdicts,
   screen 4 (dots per run), and `make swap-4`.

Tonight's run:

[[PENDING: tonight's demo-4 A/B id, both arms' hidden of 69 and referee mutants of 4, claims, two-tab marks, reviewer verdicts, and the swap-test line | source: live class | how: make demo-4, then make swap-4]]

## Key ideas, with sources

- **The agent should not grade its own work.** "agents reliably skew positive when grading their
  own work." (A3, F-a-15). "Separating the agent doing the work from the agent judging it proves to
  be a strong lever to address this issue." (A3, F-a-110). In shipharness the verify gate decides
  whether a "done" claim stands, and only the harness sets `passes` (course design, RESEARCH G-6).
- **Visible tests miss what held-out tests catch.** "while every frontier agent saturates the
  visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout
  suites." (B13, F-b-45). Most of the gap is features that work alone and fail together (B13,
  F-b-50). F4's 69 hidden tests include two files that combine F4 with earlier features.
- **The verifier must be strict.** "it’s important that the task verifier is nearly perfect,
  otherwise Claude will solve the wrong problem." (A4, F-a-127). Clean state means code "that would
  be appropriate for merging to a main branch" (A2, F-a-84).
- **House rules become checks.** "House rules" is the course label for A1's "golden principles"
  encoded in the repository (A1, F-a-99) and taste invariants enforced "with custom lints" (A1,
  F-a-96; RESEARCH G-9).
- **Filter generated tests, cheapest first.** TestGen-LLM keeps tests through "a series of
  progressively demanding semantic filters" (B11, F-b-16): builds, passes five runs (F-b-19), adds
  coverage (F-b-20). Filter 3's mutant branch comes from ACH (B12, F-b-32). Filters 4 (real
  assertions, no mocking) and 5 (no source change in the test phase) are course filters (RESEARCH
  G-7).
- **Mutants that target the fault you fear.** ACH writes faults "relevant to the issue of concern"
  that no existing test catches (B12, F-b-29); 49% of its mutant-killing tests added no line
  coverage (B12, F-b-40). The course keeps a filter set and a referee set that share no mutation
  (DESIGN D-4), so the referee never judges a test by the mutant it was written against.
- **A separate reviewer is useful but lenient.** "the evaluator is still an LLM that is inclined to
  be generous towards LLM-generated outputs." (A3, F-a-112). Its verdict is a secondary measure;
  the primary counts come from code the referee runs.

## What the A/B showed

### Pilot run 2 (VERIFICATION.md, M6 pilot run 2)

Three F4 A/Bs on 2026-10-16, gpt-6-luna at effort medium, k=3. Both arms failed the primary measure
in all three runs. The measure needs all 69 hidden tests and all 4 referee mutants.

| Count per run (runs 1, 2, 3) | Bare arm | Harness arm |
|---|---|---|
| Hidden tests passed, of 69 | 69, 66, 69 | 69, 61, 69 |
| Referee mutants killed, of 4 | 3, 4, 3 | 0, 0, 2 |
| Tests shipped (score records) | 30, 33, 8 | 0, 0, 3 |

- The bare arm came close: its tests killed most mutants, but each run missed either hidden tests
  or one mutant.
- The harness arm shipped 0, 0, and 3 tests in the 12-turn test phase, so it killed 0, 0, and 2
  mutants. Its sessions spent turns re-reading 3 to 7 instruction documents and about 15 product
  files and updating state files mid-session.
- No arm claimed done, so the verify gate never ran on F4 in this run.
- The reviewer rejected all six arms and agreed with the referee each time (`reviewer_agrees` in
  the score records).
- Run ids, per-arm costs, and wall times: [demo/README.md](demo/README.md), sections 7 and 8.

### Changes before run 3

- **Change 9, turn cost** (harness change, harness arm only): the handoff's agent notes come before
  any document, state files are updated only in the wrap-up turns, and a test-phase session starts
  with the feature's tests. This targets the harness arm's 0, 0, 3 shipped tests.
- **Changes 10 and 11** (measurement changes, both arms, no outcome change): each arm is judged as
  soon as it finishes, and the unmutated-pass step before the referee mutants runs all shipped
  tests in one batch. The batch gave the same pass or fail outcome as one-at-a-time runs on all 181
  shipped tests of run 2.

### Still to come

[[PENDING: F4 results of pilot run 3 (hidden of 69 and referee mutants of 4 per run, bare vs harness) with run ids | source: M6 pilot | how: scripts/pilot.py run 3; VERIFICATION.md, M6 pilot run 3]]

[[PENDING: S4 batch 1 dots (hidden of 69 and referee mutants of 4 per run, bare vs harness, k=10) with run ids | source: M8 batch 1 | how: make experiments BATCH=1, then make report]]

[[PENDING: effect of removing the verify layer (leave-one-out) on the F4 task | source: M8 ablation | how: make experiments BATCH=2, then make report]]

## Common questions

**The bare arm killed more mutants in the pilot. Does verification not work?** Pilot run 2 did not
test the verification parts much. The gate never ran (no arm claimed done), and the filters saw one
proposed test in three runs. The harness arm lost on turn cost: it shipped almost no tests. Change
9 is the fix being tested in run 3. If a section still shows no gap after the pre-registered
levers, the course reports "no measurable difference on this task with this model" (DESIGN §10.4).

**Why does a run need all 69 hidden tests and all 4 mutants?** That is the pre-registered primary
measure (DESIGN §8.2; `evaluate_primary` in `src/shipharness/ab/score.py`). The report also shows
each count as a dot, so a near miss is visible.

**Why doesn't the gate run the hidden tests or the referee mutants?** They would stop being held
out. The hidden tests are "never shown to the agent" (B13, F-b-43); they are not in `GATE_CHECKS`
and not in the arm's repository (DESIGN §8.3 rule 6).

**The gate runs R1-R7, and so does the referee. Is that fair?** It is a disclosed overlap (DESIGN
§8.3 rule 8). The rules are documented for both arms, so a better R1-R7 result for the harness arm
is partly expected by construction. The co-primary counts do not have this overlap.

**Why does a broken test not count as a kill?** The referee counts a kill only with shipped tests
that pass on the arm's unmutated build (CONTRACTS §21). A test that fails everywhere "kills" every
mutant and proves nothing.

**Did the referee changes after run 2 change any result?** No. Changes 10 and 11 are labelled
"measurement change, both arms, no outcome change" in VERIFICATION.md; change 11 was checked on 181
tests.

**Why are filters 4 and 5 not cited to a paper?** No source states them (RESEARCH G-7). Filter 5
is a composite of B11's "no regression, by construction" (F-b-22) and A2's "It is unacceptable to
remove or edit tests" (F-a-80).

## What to try next

- Assignment A4 ([assignment/README.md](assignment/README.md)): add house rule R8 (soft delete),
  a sixth test filter (no duplicate test), and one live F4 A/B. Start with `make
  check-assignment-4`; it makes no model calls.
- Read the four anchors again with `uv run python scripts/anchors.py extract S4:gate` (and
  `S4:filters`, `S4:probe`, `S4:blind`).
- Look at the testgen options with `uv run shipharness testgen --help` before you spend a run on
  your own module (each run is capped at $0.20, `MAX_RUN_COST_USD`).
- Write one mutant record for the riskiest line in your own service and check whether any test
  kills it ([post-class reading 02](post-class-reading/02-mutation-guided-tests-ach.md)).
- Post-class reading: [post-class-reading/](post-class-reading/README.md).
