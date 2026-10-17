# Module 1: Harness Engineering for Coding Agents - Section 3 diagrams

The diagrams for Section 3, the scope layer and the sandbox. Each one has an `.excalidraw` source,
a `.png` at 2x for slides, and an `.svg` with the font embedded for pages. Colours, step frames,
editing, and licences are explained once, in [the course diagrams guide](../../docs/diagrams/README.md).
The F4 ticket diagram, `optimistic-concurrency`, is in that folder too, because Section 4 uses it
as well.

> **Terms on this page**
>
> - **Bare arm**: An agent run with the ticket and the repository, and no harness.
> - **Harness arm**: The same run with the harness turned on.
> - **Allowed paths**: The globs a ticket lists for each phase; the files the agent may change then.
> - **Block**: A patch the scope layer refuses before anything is written; the agent sees `BLOCKED`.
> - **Revert**: A command's change outside the allowed paths, undone right after the command runs.
> - **Sandbox**: The container every tool command runs in, the same for both arms.

## The diagrams

### The scope check

![Flowchart: a patch to feature_list.json or outside the allowed paths is blocked; a command's changes outside are reverted](./scope-check-flow.svg)

*A patch is checked before anything is written; a command is checked after it runs.*

- **What it teaches**: the order of the checks and the reason the agent reads after `BLOCKED:`.
- **Slide topic**: how the scope layer decides.
- **Files**: `scope-check-flow`.
- **Source**: `PathRules.reason` in `platform/src/shipharness/harness/scope/guard.py`, and the
  blocked file in [the Section 3 evidence](../../docs/evidence/s3.md).

### The sandbox boundary

![The host holds the agent loop and the keys; the container holds the workspace and has no network](./sandbox-boundary.svg)

*The model calls leave from the host; the container itself has no network and never sees the keys.*

- **What it teaches**: what runs where, and what the container cannot reach.
- **Slide topic**: the sandbox.
- **Files**: `sandbox-boundary`.
- **Source**: `platform/sandbox/README.md` and `platform/src/shipharness/sandbox/policy.py`.

### Least privilege, side by side

![Two columns: what the bare arm and the harness arm may change, with the shared tools and sandbox below](./least-privilege.svg)

*Only the file rights differ; the tools and the sandbox are the same for both arms.*

- **What it teaches**: the scope layer as least privilege for file changes.
- **Slide topic**: bare arm and harness arm permissions.
- **Files**: `least-privilege`.
- **Source**: `platform/src/shipharness/harness/scope/`, the F4 allowed paths in
  `platform/teamtrack/reference/f4/task.toml`, and the seven tools in
  `platform/src/shipharness/runner/prompts.py`.

### Section 3 results

![Dot chart: on F4 the bare arm failed 3 of 3 runs and the harness arm passed 3 of 3; on F3 all runs passed](./results-s3.svg)

*On F4 the bare arm left the allowed paths in 3 of 3 runs and the harness arm in 0 of 3.*

- **What it teaches**: the one measured gap in the course, and the ticket where there was none.
- **Slide topic**: what we measured in Section 3.
- **Files**: `results-s3`.
- **Source**: [the Section 3 evidence](../../docs/evidence/s3.md).

### Failure story: a tidy diff in a shared file

![Six numbered steps from a ticket's file list to a wrong status nobody links](./failure-story-s3.svg)

*In the pilot, every bare arm changed app/services/errors.py.*

- **What it teaches**: how a reasonable edit outside the ticket breaks something later.
- **Slide**: "Problem statement: A tidy diff in a shared file".
- **Files**: `failure-story-s3`.
- **Source**: the slide's notes and [the Section 3 evidence](../../docs/evidence/s3.md).
- **How to edit**: change `failure-story-s3` in `platform/scripts/diagrams/`, then build and render (see [How to edit a diagram](../../docs/diagrams/README.md#how-to-edit-a-diagram)).

### Socratic build-up: is the file list enough?

![The question, the answer no, and three reasons](./socratic-s3.svg)

*Frame 1 asks; frame 2 answers with the reasons.*

- **What it teaches**: why a written file list is only a request.
- **Slide**: "Scope: Is the ticket's file list enough?", frame N on build N.
- **Files**: `socratic-s3`, with step frames `socratic-s3-step-1` to `socratic-s3-step-2`.
- **Source**: [the Section 3 evidence](../../docs/evidence/s3.md) (the bare arm left the allowed paths in 3 of 3 runs).
- **How to edit**: change `socratic-s3` in `platform/scripts/diagrams/`, then build and render (see [How to edit a diagram](../../docs/diagrams/README.md#how-to-edit-a-diagram)).

### One feature at a time: feature_list.json

![The harness writes the entry, the agent claims done, the harness checks and sets passes once](./feature-list-lifecycle.svg)

*Only the harness writes the file; passes is set once.*

- **What it teaches**: the life of one feature entry and who may change it.
- **Slide**: "1) One feature at a time: `feature_list.json`".
- **Files**: `feature-list-lifecycle`.
- **Source**: `features.py`, `status.py`, `guard.py`, and `layer.py` in `platform/src/shipharness/harness/scope/`.
- **How to edit**: change `feature-list-lifecycle` in `platform/scripts/diagrams/`, then build and render (see [How to edit a diagram](../../docs/diagrams/README.md#how-to-edit-a-diagram)).

### Timeline of the captured demo-3 A/B

![Two time lines, bare arm and harness arm, with the ticks of each](./timeline-s3.svg)

*Captured 2026-10-17 (run 3, alone), agent limit 420 s, console clock.*

- **What it teaches**: the same run in two lanes: the bare arm's edit and the harness arm's block.
- **Slide**: "What just happened: Same pull, two arms".
- **Files**: `timeline-s3`.
- **Source**: the captured demo-3 A/B in [the Section 3 evidence](../../docs/evidence/s3.md) and `demo/expected/terminal.txt`.
- **How to edit**: change `timeline-s3` in `platform/scripts/diagrams/`, then build and render (see [How to edit a diagram](../../docs/diagrams/README.md#how-to-edit-a-diagram)).

### Cheat sheet: four boundaries

![Four boxes with icons: feature list, allowed paths, sandbox, least privilege](./cheat-sheet-s3.svg)

*Two boundaries are the harness arm's; two hold for both arms.*

- **What it teaches**: the four boundaries of Section 3 on one page.
- **Slide**: "Cheat Sheet: Four boundaries for one feature".
- **Files**: `cheat-sheet-s3`.
- **Source**: `section-3-scope-sandbox/concepts.md`.
- **How to edit**: change `cheat-sheet-s3` in `platform/scripts/diagrams/`, then build and render (see [How to edit a diagram](../../docs/diagrams/README.md#how-to-edit-a-diagram)).
