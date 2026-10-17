---
name: assured-tests
description: >
  Generate unit tests for one Python module with a coding agent and keep only the tests that pass
  five filters: they import and run, pass on every one of five runs, add line coverage or kill a
  mutant no existing test kills, contain real assertions without mocking the unit under test, and
  leave the source code unchanged. Runs `shipharness testgen` and explains every discarded test.
  Use when adding tests to existing code, when generated tests look plausible but may prove
  nothing, or when hardening a module against specific faults with targeted mutants.
license: MIT
compatibility: Python 3.12+, uv, and the shipharness CLI with an OpenAI key; calls a model (costs money).
metadata:
  course: shipharness
  sources: B11 B12 A2 B1
---

# Assured tests

A generated test is easy to write and easy to get wrong: it can fail on correct code, pass by
luck, or pass without checking anything. TestGen-LLM at Meta answers this by running every
candidate through "progressively demanding semantic filters" and keeping only survivors, which "are
thus guaranteed to improve the existing test class, and to provide reliable regression test signal"
(B11, F-b-16, F-b-21). This skill applies the same idea with five filters.

## The five filters

A proposed test is kept only if it passes all five, checked in this order, cheapest first.

| # | Filter | Source |
|---|---|---|
| 1 | Imports and runs: pytest collects it with no errors | B11, "buildable" (F-b-17) |
| 2 | Passes on every one of five runs | B11 (F-b-18, F-b-19) |
| 3 | Adds line coverage over the existing suite, or kills a filter-set mutant that no existing test kills | B11 coverage (F-b-20); B12 hardening (F-b-29, F-b-32) |
| 4 | Has real assertions and does not mock the unit under test | Course filter (no direct source) |
| 5 | No source file changed during the test phase | Course filter, built on B11 F-b-22 and A2 F-a-80 |

Why each filter exists, and what it cannot catch: [filters](references/filters.md). The two papers
in short: [TestGen-LLM](references/testgen-llm.md), [ACH](references/ach.md).

## When to use

- A module has thin coverage and you want tests that are proven to add something.
- You want to protect specific behaviour (tenant isolation, permission checks) against a known kind
  of fault: write mutants for that fault and let filter 3 keep the tests that catch them.
- You want to compare kept tests against what an agent writes with no filters (`--layers none`).

## Steps

1. Run the existing suite first and note any failures. A test that already fails on your machine
   makes filters 1 and 2 meaningless for that file. Configure coverage.py if it is not set up.
2. Preview the command:

   ```
   python scripts/run_testgen.py --repo <repo> --module <path/in/repo.py> --max-tests 8 --dry-run
   ```

3. Run it without `--dry-run`. With no `--sandbox docker --image <image>`, generated tests run on
   your machine with your permissions: the script and shipharness both say UNSANDBOXED. Use a
   container for any repository you do not trust.
4. Read the result table: one row per proposed test, with the first filter it failed and the
   reason. A kept test is committed; a discarded test is never committed.
5. Review the kept tests as code. The filters prove a test runs reliably and adds coverage or
   catches a mutant. They do not prove its name and assertions describe the behaviour you want.
6. If almost everything fails filter 3, the suite already covers the module's lines: add mutants
   for the faults you care about (see the ACH summary) and run again.

## Reading discard reasons

| Filter failed | Usual cause | What to do |
|---|---|---|
| 1 | Wrong import path, missing fixture, syntax error | Check the module path; the agent may need the package layout |
| 2 | Order dependence, time, randomness, network | Expected; do not "fix" by retrying until it passes |
| 3 | The test repeats what existing tests cover | Expected for well-tested modules; add targeted mutants |
| 4 | No assert, `assert True`, or the function under test is mocked | The test proves nothing; it is discarded on purpose |
| 5 | The agent edited source code to make its test pass | Never acceptable in the test phase; the edit is reverted |

## Costs and limits

- Each run calls a model; `shipharness testgen` prints `Cost: $X` at exit and respects the course
  cost cap.
- The current code is the oracle: a kept test asserts what the code does today, so it protects
  against future regressions but "cannot detect existing faults residing in the code base" (B12,
  F-b-41).
- Filter 2's five runs catch most flakiness, not all of it.

## Sources

Ids from the shipharness research register.

- B11: Alshahwan et al., "Automated Unit Test Improvement using Large Language Models at Meta",
  FSE '24, arXiv 2402.09171. https://arxiv.org/abs/2402.09171
- B12: Foster et al., "Mutation-Guided LLM-based Test Generation at Meta", arXiv 2501.12862
  (submitted to FSE 2025 Industry Track). https://arxiv.org/abs/2501.12862
- A2: Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- B1: Agent Skills Specification. https://agentskills.io/specification
