# Module 1: Harness Engineering for Coding Agents - Section 4 reading list

Four short readings that go past the 50 minutes of class. Each one sums up a primary source in plain
words and shows how to apply it to your own repository. Each page takes about five minutes; the
reading time in the table is for the full source, at 200 words a minute.

> **Terms on this page**
>
> - **Test filters**: Five checks a test from the test phase must pass to be kept.
> - **Mutant**: A copy of the code with one small planted fault; a test that fails on it catches it.
> - **Referee**: The program that scores each run after the agent stops.
> - **Hidden tests**: Held-out tests: the agent never sees them; the referee runs them after the agent stops.

## Readings

| Reading | Reading time | Why read it |
|---|---|---|
| [01 TestGen-LLM's filters](01-testgen-llm-filters.md) | 60 minutes | Why most generated tests fail a filter, and what a kept test guarantees |
| [02 Mutation-guided tests (ACH)](02-mutation-guided-tests-ach.md) | 60 minutes | How to test for the fault you fear, not for coverage |
| [03 Separate evaluators](03-separate-evaluator.md) | 25 minutes | Why the agent should not judge its own work, and the limits of a model judge |
| [04 Held-out tests (SpecBench)](04-held-out-tests-specbench.md) | 45 minutes | How far a green visible suite can mislead you |

## How to use these

- Read 01 and 02 together: the filters, then the planted faults that filter 3 and the referee use.
- Read 03 and 04 together: who judges the work, and with which tests.
- After each reading, do the first step of its "Apply it to your repo" list on a repository you work
  on. It takes a few minutes and makes the idea stick.
- Then read the primary sources. Start with the section on the evaluator in
  [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps),
  then the filter pipeline in [Meta, TestGen-LLM](https://arxiv.org/abs/2402.09171).
- The class recap is in [session-notes.md](../session-notes.md).

## Sources

- [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/abs/2402.09171) (Meta, TestGen-LLM)
- [Mutation-Guided LLM-based Test Generation at Meta](https://arxiv.org/abs/2501.12862) (Meta, ACH)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (Anthropic)
- [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384)
