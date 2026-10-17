# Module 1: Harness Engineering for Coding Agents - Section 4 reading list

Four short readings that go past the 50 minutes of class. Each one sums up a primary source in plain
words and shows how to apply it to your own repository.

> **Terms on this page**
>
> - **Test filters**: Five checks a test from the test phase must pass to be kept.
> - **Mutant**: A copy of the code with one small planted fault; a test that fails on it catches it.
> - **Hidden tests**: Tests the agent never sees; the referee runs them after the agent stops.

## Readings

| Reading | Reading time | Why read it |
|---|---|---|
| [01 TestGen-LLM's filters](01-testgen-llm-filters.md) | 5 minutes | Why most generated tests fail a filter, and what a kept test guarantees |
| [02 Mutation-guided tests (ACH)](02-mutation-guided-tests-ach.md) | 5 minutes | How to test for the fault you fear, not for coverage |
| [03 Separate evaluators](03-separate-evaluator.md) | 5 minutes | Why the agent should not judge its own work, and the limits of a model judge |
| [04 Held-out tests (SpecBench)](04-held-out-tests-specbench.md) | 5 minutes | How far a green visible suite can mislead you |

## How to use these

- Read 01 and 02 together: the filters, then the planted faults that filter 3 and the referee use.
- Read 03 and 04 together: who judges the work, and with which tests.
- After each reading, do the first step of its "Apply it to your repo" list on a repository you work
  on. It takes a few minutes and makes the idea stick.
- Then read the primary sources. Start with the section on the evaluator in
  [Anthropic, Harness design](../../docs/evidence/s1.md#src-anthropic-harness-design), then the filter
  pipeline in [Meta, TestGen-LLM](../../docs/evidence/s4.md#src-testgen-llm).
- The class recap is in [session-notes.md](../session-notes.md).
