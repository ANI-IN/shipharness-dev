# Module 1: Harness Engineering for Coding Agents - Demo 4 harness files

This folder holds what the verify layer gives the harness arm in the Section 4 demo. The verify layer
places no files in the agent's workspace. It gives the agent text: one block in the first message of
every session, and the result of the gate when the agent claims done. The files here hold that text,
taken from the layer's code in `platform/src/shipharness/harness/verify/`.

> **Terms on this page**
>
> - **Harness layer**: One part of the harness: instructions, state, scope, or verification.
> - **Verify gate**: The checks that run in the agent's container when it claims done; a failure sends the claim back.
> - **Done claim**: The agent's call `finish(claim="done")`, which says the phase's work is complete.
> - **Clean state**: All work committed, ruff clean on changed files, one migration head, no debug output.
> - **Test filters**: Five checks a test from the test phase must pass to be kept.
> - **House rules**: TeamTrack's seven rules for every endpoint, R1 to R7.

Do not edit the files here. A script writes them from the code
(`platform/scripts/sync_demo_harness_s4.py`), and a unit test fails if they differ from what the
layer gives the agent. To change the text, change the code and run the script again.

## What is here

| File | What it holds | How the agent gets it |
|---|---|---|
| `context-prefix.txt` | The verify block: what the gate checks, and that test-phase tests must pass the filters | In the first message of every session |
| `gate-items-build.txt` | The gate's 11 items in a build phase, in order | Named in a refusal, such as "(R1, clean state)" |
| `gate-items-test.txt` | The gate's 2 items in a test phase | Named in a refusal |

The same item names are the gate pills on console screen 1.

When the gate refuses a claim, `finish` returns "Not accepted.", then one line with how many items
failed and their names, then up to three failure lines, then "Fix these, commit your work, and call
finish again." The [walkthrough](../walkthrough.md) shows the code that builds it.

## What is not here

- The list of the five filters. The agent is told only that its test-phase tests must pass "the test
  filters". The filters run after the test phase ends, and their results go to the console, not to
  the agent.
- The hidden tests and the referee mutants. They live outside the agent's workspace and are never
  named in anything the agent receives.
- The prompts both arms get (the core prompt and the phase prompts). They are not part of this
  layer.
- The other three layers. All four run in this demo; their files are in the demo folders of
  Sections 1 to 3.
