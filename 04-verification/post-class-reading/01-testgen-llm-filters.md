# TestGen-LLM's filters and the course's five

Reading time: about 8 minutes.

Source: B11, "Automated Unit Test Improvement using Large Language Models at Meta" (Alshahwan et al.,
Meta, FSE '24), https://arxiv.org/abs/2402.09171. Quotes are verbatim, with finding IDs that
resolve in [docs/REFERENCES.md](../../docs/REFERENCES.md).

## What TestGen-LLM does

TestGen-LLM asks language models for new unit tests for an existing test class at Instagram and
Facebook, then throws away every candidate that does not survive "a series of progressively
demanding semantic filters" (F-b-16). The filters run in order of cost:

1. Builds: "The first filter simply checks that the candidate code is fully buildable within the
   existing infrastructure of the app under test." (F-b-17)
2. Passes: "TestGen-LLM discards any test case that does not pass on first execution." (F-b-18)
   Then the flakiness check: "a test that does not pass on every one of five executions is deemed
   flaky." (F-b-19)
3. Improves coverage: "Any test that does not improve coverage is also discarded." (F-b-20). Coverage
   here means line coverage only (F-b-20, footnote 3).

Survivors carry a guarantee: "The candidate test cases that pass through all three filters are thus
guaranteed to improve the existing test class, and to provide reliable regression test signal."
(F-b-21). Existing tests are never touched, "retaining all existing test cases and thereby
guaranteeing there will be no regression, by construction." (F-b-22).

Two later changes matter for anyone building a similar pipeline. A dedup filter was added: "we
doubled down on this observation and included an extra filter to remove previously seen test
cases." (F-b-26). And per-test guarantees came only after reviewers asked: "In the initial MVP, we
had only implemented class-level improvement guarantees." (F-b-27).

The paper counts three filters plus the later dedup filter. "5 runs" is TestGen-LLM's number, not
ACH's.

## The funnel is steep

These numbers come from the paper and are reported per test class, not per test:

| Stage | Result | Finding |
|---|---|---|
| Evaluation, 86 classes (Reels and Stories) | 75% had a test that builds, 57% one that passes reliably, 25% one that also increases line coverage | F-b-23 |
| Deployment | about 10% of test classes improved (the abstract says 11.5%); 73% of the improvements accepted by engineers | F-b-24 |
| Per trial | about 4-5% of trials succeed; "A trial is only considered successful if the generated test case builds, passes, and increases coverage over all existing test cases." | F-b-25 |

The lesson for a harness: most generated tests prove nothing new, and only a mechanical filter
tells you which ones do. The engineer stays in charge: "TestGen-LLM's goal is to provide a
recommender system [1], that leaves the software engineer in ultimate control of the code that lands
into the code base." (F-b-28).

## Side by side with the course's five filters

| # | Course filter | TestGen-LLM | Status |
|---|---|---|---|
| 1 | Imports and runs: pytest collects it with no errors | Filter 1, "fully buildable" (F-b-17) | Direct |
| 2 | Passes 5 consecutive runs | Filter 2, first execution plus five executions (F-b-18, F-b-19) | Direct |
| 3 | Adds line coverage over the existing suite, **or** kills a filter-set mutant that no existing test kills | Filter 3, line coverage (F-b-20); the mutant branch comes from ACH (B12, F-b-29, F-b-32) | Direct, two sources |
| 4 | Real assertions, no mocking of the unit under test | Not in B11 or B12 | Course filter |
| 5 | No source file changed during the test phase | B11 keeps existing tests "by construction" (F-b-22); A2: "It is unacceptable to remove or edit tests" (F-a-80) | Course filter, composite |
| – | Dedup of previously seen tests | Later TestGen-LLM filter (F-b-26) | Not in the course pipeline |

Why the course adds filters 4 and 5. TestGen-LLM works at diff time on code that humans own, so a
generated test cannot change the code under test. A coding agent in a test phase can: it can edit
the source until its own test passes, or write a test that mocks the function it claims to test and
asserts nothing real. Filter 5 compares source fingerprints from the start of the test phase;
filter 4 reads the test's syntax tree. Neither has a source sentence of its own, so the course
labels them course filters.

Why filter 3 has a mutant branch. ACH found that "a large proportion (49%) of test cases that
uniquely additionally kill a mutant, do not also add line coverage." (B12, F-b-40). A coverage-only
filter would discard those tests. Reading 02 covers ACH.

## Where to see it in the repository

- `platform/src/shipharness/filters/filters.py`: the five filter classes; every result has a `reason`, for
  the formats `flaky: passed <n> of 5 runs, then <error>` and `adds no line coverage over the existing
  suite and kills no filter-set mutant that the existing tests miss (<n> checked)`.
- `platform/src/shipharness/filters/pipeline.py` (anchor `S4:filters`): a test stops at its first failing
  filter, so the expensive filters never run on a test that fails a cheap one.
- `use-in-your-repo/skills/assured-tests/`: the course skill that runs `shipharness testgen` and explains every
  discard.

One difference between the two entry points. `shipharness testgen --target <id>` passes the target
module and its filter-set mutants, so filter 3's mutant branch and filter 4's mocking check both
run (`platform/src/shipharness/testgen/run.py`). The verify layer's test phase in an A/B builds the filter
context without a mutant list or target module (`platform/src/shipharness/harness/verify/testphase.py`), so
there filter 3 decides by coverage and filter 4 checks assertions only.

## Why it matters for your own repo

- The tests an agent leaves in your repository guard every later change. A test that asserts
  nothing, mocks the code it claims to test, or fails one run in five costs review time and gives
  no signal. TestGen-LLM's funnel says most candidates fail at least one filter (F-b-23 to F-b-25),
  so expect the same of an agent's tests until a filter shows otherwise.
- Order the checks by cost, as B11 does (F-b-16): run a new test file five times (F-b-19) before
  you measure what it adds, and measure coverage only for tests that already pass.
- A real case from this course: in the course pilot, run 2, the only F4 test a harness arm
  proposed in its test phase failed filter 2 on its first run, reason `failed on run 1 of 5: assert
  None is not None` (captured on 2026-10-16, run ab-20261016-191626-6100f6; your output will
  differ). Without filter 2 it would have shipped as a red test. The same arm still shipped 3
  tests: it wrote them in build session 1, and in shipharness the filters judge only tests
  proposed in the test phase. A filter guards only the path it sits on; tests that reach your
  repository another way need their own check.
- Filters 4 and 5 answer a risk that B11 did not have: an agent can edit the code under test. If
  your agent may touch both source and tests in one task, add a check like filter 5 (a course
  filter, not a source idea).

## Questions to take away

- Your team's generated tests: which of the five filters would discard most of them? Run
  `shipharness testgen` on one module and read the discard reasons before guessing.
- TestGen-LLM's guarantee is "reliable regression test signal" (F-b-21). It does not say the tested
  behaviour is correct. What would you need to add to check correctness?
