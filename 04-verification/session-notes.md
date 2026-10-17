# S4 session notes: Verification

For learners, after class. Reading time: about 7 minutes. Concepts in full:
[concepts.md](concepts.md). Instructor runbook: [demo/README.md](demo/README.md).

"S4 Verification" and "house rules" are course labels. Source IDs such as (A3, F-a-110) resolve in
[REFERENCES.md](../../REFERENCES.md); quotes are verbatim.

## What was shown

1. **Poll.** Building F4 (ETag, If-Match, issue history), which arm passes more of the 69 hidden
   tests and kills more of the 4 referee mutants? Then the final feature poll (F5, F6, or F7).
2. **Two launches.** `make show-4` (harness in action: the harness arm alone, with all four layers,
   on F4 from checkpoint `m1-s4-start`; not an A/B) and, a minute later, `make final
   FEATURES=<poll winner>`, the course's one live A/B. Both ran while the concepts and the code
   were on screen. S4 has no live bare-against-harness A/B because the course's pilot data shows no
   gap on F4 (below).
3. **Concepts.** The problem (F4's `If-Match` header is optional, so every existing test keeps
   passing whether or not concurrency works), the cause (the agent judges its own work; visible
   tests miss what held-out tests catch), and the harness piece: the verify gate, R1-R7 checks,
   clean state, five test filters, targeted mutants in two disjoint sets, and the blinded reviewer
   ("blinded" is the course's A/B design, not a source term).
4. **Code walkthrough.** Four anchors, each printed by `uv run python scripts/anchors.py extract
   <id>`: `S4:filters` (`src/shipharness/filters/pipeline.py`), `S4:probe`
   (`src/shipharness/checks/r1_tenant.py`), `S4:blind` (`src/shipharness/reviewer/blind.py`),
   `S4:gate` (`src/shipharness/harness/verify/gate.py`).
5. **Demo block.** Two parts:
   - harness in action: the `make show-4` run on screen 1 (session handoffs, the gate pills if the
     agent claimed done, the primary verdict pill), screen 3 (the test filter table with discard
     reasons), and screen 2 (the two-tab edit conflict);
   - the results slide and screen 4: every section's result, "no measurable difference" included.

To read the same evidence on a run of your own: the live step of assignment A4 runs one F4 A/B
(`--purpose assignment`), and each score record it writes carries the arm's `trace_url`. Open the
harness arm's trace, find the test phase, and note which tests the agent proposed and which filter
stopped each discarded one.

## Key ideas, with sources

- **Each piece encodes an assumption about the model.** "every component in a harness encodes an
  assumption about what the model can't do on its own, and those assumptions are worth stress
  testing" (A3, F-a-124). The verification layer's, in the course's words: the agent's "done" and
  its own tests cannot be trusted.
- **The agent should not grade its own work.** "agents reliably skew positive when grading their
  own work." (A3, F-a-15). "Separating the agent doing the work from the agent judging it proves to
  be a strong lever to address this issue." (A3, F-a-110). In shipharness the verify gate decides
  whether a "done" claim stands, and only the harness sets `passes` (course design).
- **Visible tests miss what held-out tests catch.** "while every frontier agent saturates the
  visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout
  suites." (B13, F-b-45). Most of the gap is features that work alone and fail together (B13,
  F-b-50). F4's 69 hidden tests include two files that combine F4 with earlier features.
- **The verifier must be strict.** "it’s important that the task verifier is nearly perfect,
  otherwise Claude will solve the wrong problem." (A4, F-a-127). Clean state means code "that would
  be appropriate for merging to a main branch" (A2, F-a-84).
- **House rules become checks.** "House rules" is the course label for A1's "golden principles"
  encoded in the repository (A1, F-a-99) and taste invariants enforced "with custom lints" (A1,
  F-a-96).
- **Filter generated tests, cheapest first.** TestGen-LLM keeps tests through "a series of
  progressively demanding semantic filters" (B11, F-b-16): builds, passes five runs (F-b-19), adds
  coverage (F-b-20). Filter 3's mutant branch comes from ACH (B12, F-b-32). Filters 4 (real
  assertions, no mocking) and 5 (no source change in the test phase) are course filters: no
  source states them. The filters judge only tests proposed in the test phase; tests written in
  the build phase ship without them.
- **Mutants that target the fault you fear.** ACH writes faults "relevant to the issue of concern"
  that no existing test catches (B12, F-b-29); 49% of its mutant-killing tests added no line
  coverage (B12, F-b-40). The course keeps a filter set and a referee set that share no mutation
  (course design), so the referee never judges a test by the mutant it was written against.
- **A separate reviewer is useful but lenient.** "the evaluator is still an LLM that is inclined to
  be generous towards LLM-generated outputs." (A3, F-a-112). Its verdict is a secondary measure;
  the primary counts come from code the referee runs.

## What the A/B showed

### Pilot run 2

Measured in the course pilot, run 2, 2026-10-16: three F4 A/Bs, gpt-6-luna at effort medium. Both
arms failed the primary measure in all three A/Bs. The measure needs all 69 hidden tests and all 4
referee mutants.

| Count per A/B (A/Bs 1, 2, 3 of pilot run 2) | Bare arm | Harness arm |
|---|---|---|
| Hidden tests passed, of 69 | 69, 66, 69 | 69, 61, 69 |
| Referee mutants killed, of 4 | 3, 4, 3 | 0, 0, 2 |
| Tests shipped (score records) | 30, 33, 8 | 0, 0, 3 |

The three values in each cell come from A/Bs ab-20261016-182828-c81fc0, ab-20261016-185422-8a8c2a,
and ab-20261016-191626-6100f6, in that order.

- The bare arm came close: its tests killed most mutants, but each A/B missed either hidden tests
  or one mutant.
- The harness arm shipped 0, 0, and 3 tests, so it killed 0, 0, and 2 mutants. None came from the
  12-turn test phase: in A/Bs 1 and 2 the test phase proposed no test, and in A/B 3 the three
  shipped tests were written in build session 1 while the test phase's one proposed test failed
  filter 2 ("kept 0, discarded 1"). Its sessions spent turns re-reading 3 to 7 instruction
  documents and about 15 product files and updating state files mid-session.
- No arm claimed done, so the verify gate never ran on F4 in this pilot run.
- The reviewer rejected all six arms and agreed with the referee each time (`reviewer_agrees` in
  the score records).
- Run ids, per-arm costs, and wall times: [demo/README.md](demo/README.md), part 7 and section 11.

### Changes before run 3

- **A harness change after run 2, turn cost** (harness arm only): the handoff's agent notes come before
  any document, state files are updated only in the wrap-up turns, and a test-phase session starts
  with the feature's tests. This targets the harness arm's test phases, which kept no test.
- **Two referee changes after run 2** (measurement changes, both arms, no outcome change): each arm is judged as
  soon as it finishes, and the unmutated-pass step before the referee mutants runs all shipped
  tests in one batch. The batch gave the same pass or fail outcome as one-at-a-time runs on all 181
  shipped tests of run 2.

### Pilot run 3

Measured in the course pilot, run 3, 2026-10-16: three F4 A/Bs, effort medium, with change 9 in
place. Both arms failed the primary measure in all three A/Bs.

| Count per A/B (A/Bs 1, 2, 3 of pilot run 3) | Bare arm | Harness arm |
|---|---|---|
| Hidden tests passed, of 69 | 66, 66, 69 | 27, 69, 69 |
| Referee mutants killed, of 4 | 4, 0, 3 | 0, 0, 0 |
| Tests shipped (score records) | 23, 0, 5 | 0, 0, 0 |

The three values in each cell come from A/Bs ab-20261016-212252-aa1644,
ab-20261016-214151-ca9841, and ab-20261016-220010-c5b4bf, in that order.

- The harness arm shipped no tests in any A/B, so it killed 0 of 4 mutants each time. Its test
  phase proposed no test in any A/B, and no harness arm claimed done, so the gate never ran.
- In ab-20261016-212252-aa1644 the harness arm built a broken change: hidden 27 of 69, 3 new R1
  violations.
- Every bare arm hit the agent time limit; its shipped tests killed 4, 0, and 3 mutants.
- The reviewer rejected all six arms.
- Pilot run 4 (effort low) ran F1-F3 only, so F4 has no run 4 result.

Result: no measurable difference on this task with this model (course pilot, run 3).

### Class-profile round

Measured in the course's class-profile round, 2026-10-17: one F4 A/B, ab-20261017-090903-926c02,
effort low, OpenAI Fast tier, 2 CPUs per container. Both arms failed the primary measure again.

| One A/B | Bare arm | Harness arm |
|---|---|---|
| Hidden tests passed, of 69 | 68 | 68 |
| Referee mutants killed, of 4 | 4 | 1 |
| Tests shipped | 16 | 4 |
| Claim at the end of the build | `done` | `not_done` |

- The bare arm claimed done ("Verified the complete visible suite (191 passing)") and the referee
  failed it: one hidden test, `test_invalid_body_with_a_stale_version_is_412`, failed in both arms.
- The harness arm's test phase proposed 6 tests; filter 2 discarded one (`failed on run 1 of 5:
  AssertionError: assert 412 == 404`), filter 3 another (it added no coverage), and 4 shipped. Its
  build ended with `not_done`, so the gate did not run.

Over pilot run 3 and this round, F4 shows no measurable difference on this task with this model.
Post hoc (measures chosen after the results; descriptive), over pilot runs 2-4 and the live console
check, 34 runs per arm across all sections: no done claim came with failing hidden tests in either
arm, harness arms shipped a median of 2.5 tests against 7.5, and on F4 no harness arm ever called
`finish(claim="done")`. The course's planned 10-run experiment batch and the leave-one-out ablation
were not run, because the pilot did not pass its pre-registered decision rule.

## Common questions

**The harness did not win. Was it useless?** On F4 the runs did not test the verification parts
much: the gate never ran (no harness arm claimed done), and the filters saw one proposed test in
run 2, none in run 3, and six in the class-profile round. A3's rule applies: an evaluator "is worth
the cost when the task sits beyond what the current model does reliably solo." (A3, F-a-123). On
this task, with this model, the result is "no measurable difference" (the course's pre-registered
decision rule), which is a statement about this model and this task, not about every repository
(A1, F-a-143).

**The bare arm killed more mutants. Does verification not work?** The bare arm shipped more tests:
30, 33, 8 in run 2, 23, 0, 5 in run 3, and 16 in the class-profile round, against the harness arm's
0, 0, 3, then 0, 0, 0, then 4. A test that is never written cannot kill a mutant, and the filters
judge only the tests the test phase proposes.

**Why does a run need all 69 hidden tests and all 4 mutants?** That is the pre-registered primary
measure (course design; `evaluate_primary` in `src/shipharness/ab/score.py`). The report also shows
each count as a dot, so a near miss is visible.

**Why doesn't the gate run the hidden tests or the referee mutants?** They would stop being held
out. The hidden tests are "never shown to the agent" (B13, F-b-43); they are not in `GATE_CHECKS`
and not in the arm's exported repository.

**The gate runs R1-R7, and so does the referee. Is that fair?** It is a disclosed overlap (course
design). The rules are documented for both arms, so a better R1-R7 result for the harness arm
is partly expected by construction. The co-primary counts do not have this overlap.

**Why does a broken test not count as a kill?** The referee counts a kill only with shipped tests
that pass on the arm's unmutated build (`_passing_unmutated` in `src/shipharness/ab/referee.py`). A
test that fails everywhere "kills" every mutant and proves nothing.

**Did the referee changes after run 2 change any result?** No. Both are labelled "measurement
change, both arms, no outcome change"; the batched step was checked on 181 tests.

**Why are filters 4 and 5 not cited to a paper?** No source states them; they are course filters. Filter 5
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
