# TestGen-LLM in short (B11)

Alshahwan, Chheda, Finegenova, Gokkaya, Harman, Harper, Marginean, Sengupta, Wang (Meta).
"Automated Unit Test Improvement using Large Language Models at Meta". FSE '24.
arXiv 2402.09171, 2024-02-14. https://arxiv.org/abs/2402.09171

Summary in our own words; quotes are marked and come from the research notes (R-b, finding ids
F-b-16 to F-b-28).

## What it does

TestGen-LLM takes an existing Kotlin test class at Meta, asks a language model for extra test
cases, and keeps only the candidates that survive a series of filters. The surviving tests are
added to the class; existing tests are never changed, so there can be no regression "by
construction" (F-b-22).

## The filters

1. Builds: the candidate compiles in the app's existing build (F-b-17).
2. Passes: it passes on first execution, and on "every one of five executions"; otherwise it is
   discarded as failing or flaky (F-b-18, F-b-19).
3. Improves coverage: it adds line coverage to the class; tests that do not are discarded (F-b-20).

Later versions added a filter that removes test cases seen before (F-b-26). The guarantees were
first per test class and were extended to each test case after engineers asked for them (F-b-27).

## Results reported

| Measure | Value | Where |
|---|---|---|
| Evaluation on 86 test classes (Instagram Reels and Stories) | 75% of classes had a new test that builds, 57% one that also passes reliably, 25% one that also adds line coverage | B11 §3.3 (F-b-23) |
| Deployment | about 10% of the test classes it was applied to were improved (the abstract says 11.5%); 73% of improvements were accepted by engineers | B11 §4 (F-b-24) |
| Success rate per trial | about 4-5%; a trial succeeds only if the test builds, passes, and adds coverage | B11 §4, Table 3 (F-b-25) |

The 75/57/25% figures are per test class, not per generated test (RESEARCH §5, correction 6).

## What the course takes from it

- The filter pipeline: cheap checks first, and a test is kept only when it passes every filter.
- Five runs as the flakiness check.
- Line coverage as the measure of "adds something".
- The word "assured": survivors carry checked guarantees (F-b-21).
- The engineer stays in control; the tool recommends (F-b-28).
