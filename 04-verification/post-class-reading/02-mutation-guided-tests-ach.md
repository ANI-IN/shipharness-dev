# Mutation-guided test generation (ACH) and the course's targeted mutants

Reading time: about 8 minutes.

Source: B12, "Mutation-Guided LLM-based Test Generation at Meta" (Foster et al., Meta, submitted to
FSE 2025 Industry Track), https://arxiv.org/abs/2501.12862. Quotes are verbatim, with finding IDs
that resolve in [REFERENCES.md](../../../REFERENCES.md).

## The idea: start from the fault you fear

Coverage asks "did a test run this line?". ACH asks "would a test notice if this line were wrong in
the way we care about?". It starts from a concern, such as privacy, and works backwards:

1. **Make a fault.** The concern enters as free text, for example "a typical bug that introduces a
   privacy violation similar to {diff}." (F-b-33). The goal is to "construct mutants that denote
   faults that are both relevant to the issue of concern and also currently not caught (unkilled) by
   any existing test case" (F-b-29).
2. **Drop equivalent mutants.** A mutant that behaves exactly like the original can never be killed.
   "This Equivalence Detector agent uses the LLM-as-judge approach [24, 63]." (F-b-36). On its own
   the detector reached precision 0.79 and recall 0.47; with rule-based pre-processing, "an overall
   precision and recall of 0.95 and 0.96 respectively" (F-b-37).
3. **Write tests that kill the mutant.** The prompt asks for "extra test cases that will fail on the
   mutant version of the class, but would pass on the correct version." (F-b-34). The test filter
   is "a slightly modified version of the previously published TestGen-LLM tool [3]." (F-b-35).

## What a kept test promises

ACH states assurances, and "The first three assurances are boolean in nature; they are unequivocal
guarantees made by ACH about the tests it proposes to the engineer." (F-b-30). Two of them map to
the course's filters:

- "Valid Regression Tests: The tests pass and do so consistently, so they are non-flaky [26]
  regression tests" (F-b-31). ACH does not restate a run count; the five-run check is TestGen-LLM's
  (B11, F-b-19).
- "Hardening: The new tests catch faults that no existing test can catch" (F-b-32).

## Scale and results

| Item | Value | Finding |
|---|---|---|
| Classes under test | 10,795 | F-b-38 |
| Mutants generated / that build and pass | 31,677 / 9,095 | F-b-38 |
| Judged non-equivalent | 4,660 | F-b-38 |
| Tests produced | 571 | F-b-38 |
| Engineer acceptance (Messenger and WhatsApp test-a-thons) | 73%; about 36% judged privacy-relevant | F-b-39 |
| Tests that uniquely kill a mutant but add no line coverage | 49% | F-b-40 |

The last row is the reason the course's filter 3 accepts a test that kills a mutant even when it
adds no coverage. The stated limit: "This allows us to protect against future regressions, but it
cannot detect existing faults residing in the code base." (F-b-41). The current code is the oracle.

## How the course applies it

The course keeps ACH's concept (issue-specific faults on risky lines) and changes the machinery.

**Hand-written mutants instead of generated ones.** Each mutant is one record: a file, the exact
original text, a replacement, and a rationale (`Mutant` in `src/shipharness/filters/mutants.py`). A
small targeted runner applies one mutant at a time; mutmut is not used because it cannot target
chosen lines (course design). Because every mutant is written and checked by hand, there is no
equivalence detector: dataset validation (`uv run shipharness datasets validate
datasets/teamtrack-features-v1.jsonl --kind features`) checks that every task's referee set is
non-empty and that each mutant's original text matches exactly one line at the task's checkpoint,
and the course checked that each referee mutant is killed by the reference implementation's
visible tests.

**The concern is TeamTrack's house rules and the feature's risk.** One record from
`teamtrack/mutants/features/f4.jsonl`:

```json
{"id": "app.services.issues-m401", "target": "app.services.issues", "set": "referee", "file": "app/services/issues.py", "line": 54, "original": "    issue.version += 1", "replacement": "    issue.version += 0", "rationale": "writes do not move the version, so stale If-Match values still match (lost update)"}
```

A test that writes twice and checks that the second stale write gets 412 kills it. A test that only
checks one happy-path PATCH does not.

**Two disjoint sets.** Every mutant file is split into a filter set (used by filter 3 while the
agent works) and a referee set (held out; used only by the referee). If the same mutation sat in
both, "a test written to kill the filter mutant also kills the referee mutant, and the referee no
longer measures held-out behaviour" (module docstring of `src/shipharness/filters/mutant_sets.py`).
`overlaps` fails on any shared mutation, and the docstring records the behaviourally equivalent
pairs found by review and how each was resolved (course design).

**Only real kills count.** The referee runs referee-set mutants against shipped tests that pass on
the arm's unmutated build (`_passing_unmutated` in `src/shipharness/ab/referee.py`), so a broken
test does not count as a kill.

Counts of records in the repository (`teamtrack/mutants/*.jsonl`, `teamtrack/mutants/features/`,
`datasets/mutants/`):
TeamTrack module files 41 filter / 40 referee; feature files 14 filter / 25 referee; boltons 22 / 27;
WTForms 21 / 24.

## Why it matters for your own repo

- Coverage tells you a line ran, not that a test would notice it going wrong in the way you fear.
  Almost half of ACH's mutant-killing tests added no line coverage (F-b-40), so a coverage target
  alone would have rejected them.
- A real case from this course: in A/B 1 of the course pilot's run 2 the bare arm shipped 30 tests
  (score record `r-20261016-182828-1daced`), and the lost-update mutant `app.services.issues-m401` still survived
  (captured on 2026-10-16, run ab-20261016-182828-c81fc0, `mutant_result` event; your output will
  differ). Thirty tests, and none of them noticed writes that no longer move the version.
- Start with one record: pick the line whose failure would hurt a customer most, write the mutant
  as `original` and `replacement`, apply it by hand, and run your suite. If nothing fails, you have
  found a test to write.
- If you use mutants to steer an agent, keep a second set it never sees. Otherwise the agent's
  tests are judged by the same mutants they were written against.

## Questions to take away

- Name one fault in your own service that would hurt a customer and that your suite would not
  notice. Write it as a one-line mutant record. Does any existing test kill it?
- ACH generates mutants with a model and filters equivalents with a judge; the course writes them by
  hand. When does each choice make sense for your team?
