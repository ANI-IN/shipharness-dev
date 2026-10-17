# ACH in short (B12)

Foster, Gulati, Harman, Harper, Mao, Ritchey, Robert, Sengupta (Meta). "Mutation-Guided LLM-based
Test Generation at Meta". arXiv 2501.12862, 2025-01-22; submitted to the FSE 2025 Industry Track.
https://arxiv.org/abs/2501.12862

Summary in our own words; quotes are marked, and their finding ids (F-b-29 to F-b-41) are listed
in `docs/REFERENCES.md` in the course repository.

## What it does

ACH starts from a concern written in plain text, for example a kind of privacy fault seen before.
A language model writes mutants: small changes to the code that simulate that fault. A second
model, used as a judge, removes mutants that behave the same as the original (equivalent mutants).
A modified TestGen-LLM then writes tests that pass on the original code and fail on the mutant
(F-b-33, F-b-34, F-b-35, F-b-36).

The target is mutants that are "relevant to the issue of concern and also currently not caught
(unkilled) by any existing test case" (F-b-29). A kept test therefore catches a fault that no
existing test catches: ACH calls this "Hardening" (F-b-32).

## Results reported

| Measure | Value | Where |
|---|---|---|
| Scale | 10,795 classes; 31,677 mutants generated, 9,095 that build and pass; 4,660 judged not equivalent; 571 tests | B12 Table 2 (F-b-38) |
| Acceptance | engineers accepted 73% of the tests | B12 §4.2 (F-b-39) |
| Equivalence judge | precision 0.95 and recall 0.96 with simple rule-based pre-processing; 0.79 and 0.47 for the model alone | B12 §5.3 (F-b-37) |
| Mutation versus coverage | 49% of tests that uniquely kill a mutant add no line coverage | B12 §6 (F-b-40) |

## Limits the authors state

The current code is the regression oracle, so ACH "cannot detect existing faults residing in the
code base" (F-b-41). It protects against future regressions of the concern.

## What the course takes from it

- Filter 3's second branch: a test that kills a mutant no existing test kills is kept even when it
  adds no coverage, because coverage alone would discard about half of such tests (F-b-40).
- Targeted mutants on risky lines, written by hand for the course rather than by a model, and
  validated so each one is killed by at least one existing test.
- Mutants split into a filter set and a referee set, so the tests are never judged with the
  mutants that selected them.
