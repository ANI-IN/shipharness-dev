# Module 1: Harness Engineering for Coding Agents - Section 2 reading list

Three short readings that go past the 50 minutes of class. Each one sums up a primary source in plain
words and shows how to apply it to your own repository.

> **Terms on this page**
>
> - **Session**: One run of the agent with one context window, from its first turn to its stop.
> - **Context reset**: Clearing the context and starting a fresh session, with a handoff.
> - **Structured handoff**: A file that carries the last session's state and the next steps to the next session.
> - **Exec plan**: A plan checked into the repository, with its progress and its decisions.

## Readings

| Reading | Reading time | Why read it |
|---|---|---|
| [01 Effective harnesses for long-running agents](01-effective-harnesses-for-long-running-agents.md) | 5 minutes | The files and routines that carry work from one session to the next |
| [02 Harness design: context resets](02-harness-design-context-resets.md) | 5 minutes | Resets against compaction, and why the choice depends on the model |
| [03 Using PLANS.md](03-exec-plans.md) | 5 minutes | A plan the next session can restart from |

## How to use these

- Read them in order. The first sets up the files; the second asks when you need a reset at all; the
  third makes the plan good enough to restart from.
- After each reading, do the first step of its "Apply it to your repo" list on a repository you work
  on. It takes a few minutes and makes the idea stick.
- Then read the primary sources. Start with the "Getting up to speed" part of
  [Anthropic, Effective harnesses](../../docs/evidence/s1.md#src-anthropic-long-running), then the
  context reset part of [Anthropic, Harness design](../../docs/evidence/s1.md#src-anthropic-harness-design).
- The class recap is in [session-notes.md](../session-notes.md).
