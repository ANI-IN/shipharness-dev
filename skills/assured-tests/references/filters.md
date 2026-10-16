# Why each filter exists

Finding ids refer to the shipharness research register (research/notes/R-b.md and R-a.md). B11 is
TestGen-LLM, B12 is ACH, A2 is Anthropic's long-running harness article. Filters 1-3 come from the
papers; filters 4 and 5 are the course's own (RESEARCH G-7) and are presented as such.

## Filter 1: imports and runs

- Rule: pytest collects the test and runs it without a collection or import error.
- Source: B11's first filter "simply checks that the candidate code is fully buildable within the
  existing infrastructure of the app under test" (F-b-17). Python has no build step, so the course
  reads "buildable" as "collected and run by pytest".
- Catches: hallucinated imports, wrong fixture names, syntax errors.
- Misses: everything about what the test checks.

## Filter 2: passes on every one of five runs

- Rule: the test passes on its first run and on each of five runs.
- Source: B11 discards "any test case that does not pass on first execution", because without an
  automated oracle a failing test cannot tell a bug from a wrong test, and "a test that does not
  pass on every one of five executions is deemed flaky" (F-b-18, F-b-19).
- Catches: tests that fail on correct code, and most flaky tests.
- Misses: flakiness that shows up less often than one run in five; tests that pass by checking
  nothing.
- Note: the number five is TestGen-LLM's. ACH asks for tests that "pass and do so consistently"
  without restating a count (F-b-31), so do not attribute "five runs" to ACH.

## Filter 3: adds line coverage, or kills a mutant nothing else kills

- Rule: the test covers at least one line the existing suite does not, or it kills a filter-set
  mutant that no existing test kills.
- Source, coverage branch: B11 discards "Any test that does not improve coverage" (F-b-20). B11
  measures line coverage only.
- Source, mutant branch: B12 builds mutants "that denote faults that are both relevant to the issue
  of concern and also currently not caught (unkilled) by any existing test case", and keeps tests
  that catch them: "Hardening: The new tests catch faults that no existing test can catch" (F-b-29,
  F-b-32).
- Why both: in B12, 49% of the tests that uniquely kill a mutant add no line coverage (F-b-40). A
  coverage-only filter would throw those tests away.
- Course detail: mutants are split into a filter set, which this filter uses, and a referee set kept
  apart for judging. A test is never judged by the same mutants that selected it.
- Misses: faults that no mutant simulates, in lines that are already covered.

## Filter 4: real assertions, no mocking of the unit under test

- Rule: the test contains at least one assertion that can fail, and it does not replace the
  function or class it tests with a mock. Checked on the test's syntax tree.
- Source: none in B11 or B12. This is a course filter (RESEARCH G-7). It exists because a test
  with `assert True`, or one that mocks the code it claims to test, can pass filters 1-3: it runs,
  passes reliably, and executes new lines.
- Misses: weak assertions that are technically able to fail.

## Filter 5: no source file changed during the test phase

- Rule: the hash of every source file at the end of the test phase equals its hash at the start.
- Source: a composite of two statements (RESEARCH G-7). B11 keeps every existing test and only adds,
  "guaranteeing there will be no regression, by construction" (F-b-22). A2 tells agents "It is
  unacceptable to remove or edit tests because this could lead to missing or buggy functionality"
  (F-a-80). The course applies the same protection in the other direction: in the test phase the
  code under test is fixed.
- Catches: an agent that edits the code to make its own test pass.

## What "assured" means here

B11 calls its approach Assured LLM-based Software Engineering: a kept test comes with guarantees
that were checked, not claimed (F-b-21). In this skill the guarantees are exactly the five filters
above, no more. A kept test still needs a human review of whether it tests the right behaviour; B11
describes TestGen-LLM as a recommender "that leaves the software engineer in ultimate control"
(F-b-28).
