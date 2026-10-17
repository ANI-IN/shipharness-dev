# Module 1: Harness Engineering for Coding Agents - Section 2 diagrams

The diagrams for Section 2, the state and lifecycle layer. Each one has an `.excalidraw` source, a
`.png` at 2x for slides, and an `.svg` with the font embedded for pages. Colours, step frames,
editing, and licences are explained once, in [the course diagrams guide](../../docs/diagrams/README.md).

> **Terms on this page**
>
> - **Bare arm**: An agent run with the ticket and the repository, and no harness.
> - **Harness arm**: The same run with the harness turned on.
> - **Session turn budget**: The fixed number of turns a session gets before the runner stops it.
> - **Structured handoff**: A file that carries the last session's state and the next steps to the next session.
> - **R7**: House rule 7, migrations: exactly one Alembic head, and a fresh upgrade works.

## The diagrams

### Session lifecycle and handoff

![Session 1 stops at its turn budget, the harness writes the handoff, session 2 reads it first](./session-lifecycle.svg)

*Session 2 starts with an empty context; what it knows comes from the handoff, progress.md, and git.*

- **What it teaches**: a context reset with a structured handoff, from one session to the next.
- **Slide topic**: one task, two sessions.
- **Files**: `session-lifecycle`, with step frames `session-lifecycle-step-1` to
  `session-lifecycle-step-4`.
- **Source**: `platform/src/shipharness/harness/state/lifecycle.py` and the 12-turn first session in
  [the Section 2 evidence](../../docs/evidence/s2.md).

### What the handoff holds

![session-handoff.md with a machine summary from the harness and notes from the agent](./handoff-contents.svg)

*The harness writes the facts from the repository; the agent writes its notes, which stay as written.*

- **What it teaches**: the two owners of `session-handoff.md` and what each part holds.
- **Slide topic**: the handoff file.
- **Files**: `handoff-contents`.
- **Source**: `MachineSummary` and `merge` in `platform/src/shipharness/harness/state/handoff.py`.

### One head or two heads

![A migration chain with one head, next to a fork where two migrations share one parent](./alembic-heads.svg)

*Two migrations with the same down_revision make two heads, and house rule R7 needs exactly one.*

- **What it teaches**: what a redone migration does to the Alembic history.
- **Slide topic**: the cost of a forgotten session.
- **Files**: `alembic-heads`.
- **Source**: `platform/teamtrack/migrations/versions/0001_initial.py` and `migration_heads` in
  `platform/src/shipharness/harness/state/handoff.py`.

### Section 2 results

![Dot chart for the comments ticket: every run of both arms passed](./results-s2.svg)

*All 7 runs of each arm passed: no measurable difference on this task with this model.*

- **What it teaches**: the measured result for the state layer, one dot per run.
- **Slide topic**: what we measured in Section 2.
- **Files**: `results-s2`.
- **Source**: [the Section 2 evidence](../../docs/evidence/s2.md). One earlier round is not shown:
  the evidence page reports it as a measurement bug.
