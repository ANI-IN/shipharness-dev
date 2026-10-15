# shipharness

Module 1 — Harness Engineering for Coding Agents: instructions, state, scope, and verification that
make agent-written code safe to merge.

> Status: under construction (milestone M3). The design is in [DESIGN.md](DESIGN.md), interfaces in
> [CONTRACTS.md](CONTRACTS.md), sources in [RESEARCH.md](RESEARCH.md). This README is completed in M9.

## The problem

Teams now hand features to coding agents. The agent writes code that looks right and reports "done."
In a multi-tenant service the failures are specific and expensive:

- a new endpoint returns one customer's data to another customer;
- a second session does not know what the first session did, and redoes or breaks it;
- the agent changes files it was never asked to touch, and older features stop working;
- the agent's own tests pass while the behaviour is wrong, and "the agent said it passed" is the only
  evidence a reviewer gets.

## Why it happens

1. The agent cannot follow rules it cannot see in its context.
2. Each new session starts without memory of the previous one.
3. Agents copy existing patterns, including bad ones, and can take actions that are hard to undo.
4. The agent judges its own work, and its visible tests miss what held-out tests catch.

Each cause is cited to its primary source in [DESIGN.md §1](DESIGN.md#1-storyline).

## The solution: a harness

The environment around the agent, not a better prompt.

| Part | What it gives the agent |
|---|---|
| S1 Instructions: what the agent knows | Instructions it can find |
| S2 State and session lifecycle: what the agent remembers | State that survives sessions |
| S3 Scope and sandbox: what the agent is allowed to change and reach | Scope enforced by code and by the sandbox |
| S4 Verification: what proves the work is done | Verification the agent does not control |

## How we prove it

Same agent, model, and task, with and without the harness, judged by the same referee, shown live,
backed by pre-run experiments.

## Quick start (development)

```bash
uv sync
cp .env.example .env   # fill in OPENAI_API_KEY and LANGSMITH_API_KEY
uv run shipharness --version
uv run pytest
```

## License

MIT, see [LICENSE](LICENSE).
