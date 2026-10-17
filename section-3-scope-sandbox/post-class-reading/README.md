# Module 1: Harness Engineering for Coding Agents - Section 3 reading list

Three short readings that go past the 50 minutes of class. Each one sums up a primary source in plain
words and shows how to apply it to your own repository. Each page takes about five minutes; the
reading time in the table is for the full source, at 200 words a minute.

> **Terms on this page**
>
> - **Feature list**: `feature_list.json`, the one feature of the run and its `passes` field.
> - **Sandbox**: The container every tool command runs in, the same for both arms.
> - **Allowed paths**: The globs a ticket lists for each phase; the files the agent may change then.

## Readings

| Reading | Reading time | Why read it |
|---|---|---|
| [01 Effective harnesses for long-running agents](01-effective-harnesses-feature-list.md) | 10 minutes | Where the feature list, one feature at a time, and `passes` come from |
| [02 Building a C compiler with parallel Claudes](02-c-compiler-containers.md) | 15 minutes | Why unattended agents run in a container with no internet |
| [03 Codex: agent approvals and security](03-codex-sandbox-and-approvals.md) | 20 minutes | How another coding agent sets its sandbox, and what it leaves to you |

## How to use these

- Read them in order. The first is about files in scope, the second about what the machine allows,
  the third puts both next to an agent you may already use.
- After each reading, do the first step of its "Apply it to your repo" list on a repository you work
  on. It takes a few minutes and makes the idea stick.
- Then read the primary sources. Start with the "Feature list" part of
  [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), then the
  sections on running agents in parallel in
  [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler).
- The class recap is in [session-notes.md](../session-notes.md).

## Sources

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic, Justin Young, 2025-11-26)
- [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) (Anthropic, Nicholas Carlini, 2026-02-05)
