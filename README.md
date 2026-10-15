# shipharness

Module 1 — Harness Engineering for Coding Agents: instructions, state, scope, and verification that
make agent-written code safe to merge.

> Status: milestone M3 (core) complete; harness layers, referee checks, console screens, datasets,
> experiments, and course content arrive in M4-M11. Design: [DESIGN.md](DESIGN.md). Interfaces:
> [CONTRACTS.md](CONTRACTS.md). Sources: [RESEARCH.md](RESEARCH.md). This README is completed in M9.

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

## Prerequisites

- Python 3.12+, [uv](https://docs.astral.sh/uv/), git.
- A container runtime for sandboxed runs: Docker Desktop (WSL2 backend) on Windows, Docker Engine or
  Podman on Linux, Docker Desktop or Colima on macOS. See [sandbox/README.md](sandbox/README.md).
- A paid OpenAI API account (Build tier or higher, at least $5 of credit) and a free LangSmith
  Developer account with no card on file. See [setup/PRE-CLASS.md](setup/PRE-CLASS.md).

On Windows, clone and run inside WSL2 (for example `~/shipharness`).

## Setup

```bash
git clone https://github.com/ANI-IN/shipharness.git && cd shipharness
make setup            # uv sync, build the sandbox images, create .env from .env.example
# edit .env: fill in OPENAI_API_KEY and LANGSMITH_API_KEY (the file is git-ignored)
make doctor           # names any key that is missing or invalid
make up               # TeamTrack API + board on http://127.0.0.1:8000/board
```

## Commands

Every Make target wraps a `uv run` command, so the right column works without make.

| Make target | Command | What it does |
|---|---|---|
| `make setup` | `uv sync --frozen` (+ image builds) | Install pinned dependencies, build sandbox images |
| `make doctor` | `uv run shipharness doctor` | Check Python, git, uv, container runtime, both keys, prices |
| `make up` | `uv run shipharness up` | Migrate, seed, and serve TeamTrack and its board |
| `make console` | `uv run shipharness console` | Live console on http://127.0.0.1:8765/ |
| `make datasets` | `uv run shipharness datasets upload` | Validate and upload both datasets to LangSmith (M5) |
| `make test` | `uv run pytest` | Unit tests (no network, no keys, no Docker) and TeamTrack visible tests |
| `make test-live` | `uv run pytest -m live tests/live` | Tests that call OpenAI and LangSmith |
| `make test-docker` | `uv run pytest -m docker tests/unit/test_sandbox_docker.py` | Sandbox tests against a real container runtime |
| `make lint` | `uv run ruff check . && uv run ruff format --check .` | Lint, format check, import contract, anchors |
| `make lint-prose` | `uv run python scripts/lint_prose.py` | Banned words and emoji in course documents |

Targets for demos, experiments, reports, assignments, and slides print the milestone that delivers
them.

## Configuration

All settings come from `.env` at the repository root or the environment
(full list in [.env.example](.env.example) and [CONTRACTS.md §1](CONTRACTS.md)).

| Variable | Default | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | (required) | OpenAI key; never printed, logged, traced, or passed into a container |
| `LANGSMITH_API_KEY` | (required) | LangSmith key; same rules |
| `OPENAI_MODEL` | `gpt-6-luna` | Builder and test-writer model (both arms) |
| `OPENAI_EVAL_MODEL` | `gpt-5.6-luna` | Blinded reviewer model |
| `OPENAI_REASONING_EFFORT` | `medium` | Provisional; the M6 pilot sets the final value |
| `MAX_RUN_COST_USD` | `0.20` | Per arm per run, build and test phases together |
| `MAX_SESSION_COST_USD` | `2.50` | Per class session |
| `MAX_BATCH_COST_USD` | `2.50` | Per command |
| `SANDBOX_MODE` | `docker` | `none` runs commands on the host, labelled UNSANDBOXED |

## Repository layout (so far)

```
src/shipharness/   config, cost, events, sandbox, tracing, runner, harness, checks, console, datasets, cli
teamtrack/         demo target: multi-tenant API, web board, migrations, seed, docs, visible tests
sandbox/           Dockerfile (agent and referee images), runtime notes
scripts/           anchors.py (walkthrough anchors), lint_prose.py
research/notes/    M1 research notes (finding IDs cited in RESEARCH.md)
tests/unit, tests/live
```

## License

MIT, see [LICENSE](LICENSE).
