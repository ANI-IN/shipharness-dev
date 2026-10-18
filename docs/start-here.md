# Start here

This page is the learning path through Module 1: Harness Engineering for Coding Agents, in order.
Follow it top to bottom: set up once, then work through Section 1: Instructions to Section 4:
Verification, then the final project, then your own repository. New words are in the
[glossary](glossary.md); money questions are on the [costs page](costs.md); common questions are in
the [FAQ](faq.md).

## How the times were set

Each step gives a time, so you can plan your week. Two kinds of number are mixed here, and each row
says which:

- **Measured**: a reading time printed at the top of a page, or a run time on the
  [evidence page](evidence/general.md#timings).
- **Estimate**: a planning guess for work the course has not timed, such as a first install or an
  assignment. Yours may be shorter or longer.

A live run's time is mostly waiting. Read the next page while it runs.

## The path at a glance

| Step | What you do | Time |
|---|---|---|
| 1. Setup | Accounts, tools, keys, `make doctor`, a first live run | 1 to 2 hours (estimate) |
| 2. Section 1: Instructions | README, concepts, demo, assignment, reading | About 6 hours |
| 3. Section 2: State and sessions | README, concepts, demo, assignment, reading | About 5 hours |
| 4. Section 3: Scope and sandbox | README, concepts, demo, assignment, reading | About 6 hours |
| 5. Section 4: Verification | README, concepts, demo, assignment, reading | About 9 hours |
| 6. Final project | One A/B on a new feature, then read the result | About 1 hour |
| 7. Use it in your repo | Copy the kit, write a map, add checks | 2 to 4 hours (estimate) |

The section totals add up the rows in the section tables below. Most of each is the assignment.

## Step 1: Setup

Start at [setup](../setup/README.md). It takes a machine with nothing installed to a first live run,
on Windows (through WSL2), Linux, or macOS.

| Part | Page | Time |
|---|---|---|
| Accounts, tools, clone, `.env` | [setup](../setup/README.md) and your system's page | 1 to 2 hours (estimate) |
| Build both images | `make setup` | 145 s on the course machine (measured) |
| First live run | `make show-1` | About 10 minutes (measured) |
| Before a live class | [pre-class checklist](../setup/pre-class.md) | 15 minutes (estimate) |

`make doctor` must end with `result: + ready` before you go on.

## Steps 2 to 5: the four sections

Every section has the same parts, in the same order. Work through them in this order:

1. The section README: the problem, why it happens, and how the layer fixes it.
2. `concepts.md`: the idea, how it works, and what the course measured.
3. The demo: run it, watch the console, then read the demo page and the code walkthrough.
4. The assignment: build the layer yourself, run its self-check, then its one live step.
5. The post-class reading and the session notes.

### Section 1: Instructions

| Part | Page | Time |
|---|---|---|
| README | [Section 1](../section-1-instructions/README.md) | 5 minutes (estimate) |
| Concepts | [concepts.md](../section-1-instructions/concepts.md) | 15 minutes (measured) |
| Demo run | `make show-1` | 10 min 14 s (measured) |
| Demo page and walkthrough | [demo](../section-1-instructions/demo/README.md) | 30 minutes (estimate) |
| Assignment 1: Instructions | [assignment](../section-1-instructions/assignment/README.md) | 3 to 4 hours (estimate) |
| Reading | [three readings](../section-1-instructions/post-class-reading/README.md) | 100 minutes (measured) |

Assignment 1 has eight steps; its live step runs 8 tasks with 3 runs per arm, so start it early.

### Section 2: State and sessions

| Part | Page | Time |
|---|---|---|
| README | [Section 2](../section-2-state-lifecycle/README.md) | 5 minutes (estimate) |
| Concepts | [concepts.md](../section-2-state-lifecycle/concepts.md) | 15 minutes (measured) |
| Demo run | `make show-2 SESSION_BUDGET=12,38` | 10 min 7 s (measured) |
| Demo page and walkthrough | [demo](../section-2-state-lifecycle/demo/README.md) | 30 minutes (estimate) |
| Assignment 2: State and sessions | [assignment](../section-2-state-lifecycle/assignment/README.md) | 3 to 4 hours (estimate) |
| Reading | [three readings](../section-2-state-lifecycle/post-class-reading/README.md) | 50 minutes (measured) |

### Section 3: Scope and sandbox

| Part | Page | Time |
|---|---|---|
| README | [Section 3](../section-3-scope-sandbox/README.md) | 5 minutes (estimate) |
| Concepts | [concepts.md](../section-3-scope-sandbox/concepts.md) | 15 minutes (measured) |
| Demo run | `make demo-3 FEATURE=version-checks` | 11 to 16 minutes (measured) |
| Demo page and walkthrough | [demo](../section-3-scope-sandbox/demo/README.md) | 30 minutes (estimate) |
| Assignment 3: Scope and sandbox | [assignment](../section-3-scope-sandbox/assignment/README.md) | 4 hours (estimate) |
| Reading | [three readings](../section-3-scope-sandbox/post-class-reading/README.md) | 45 minutes (measured) |

### Section 4: Verification

| Part | Page | Time |
|---|---|---|
| README | [Section 4](../section-4-verification/README.md) | 5 minutes (estimate) |
| Concepts | [concepts.md](../section-4-verification/concepts.md) | 15 minutes (measured) |
| Demo run | `make show-4` | 11 min 6 s (measured) |
| Demo page and walkthrough | [demo](../section-4-verification/demo/README.md) | 30 minutes (estimate) |
| Assignment 4: Verification | [assignment](../section-4-verification/assignment/README.md) | 4 to 5 hours (estimate) |
| Reading | [four readings](../section-4-verification/post-class-reading/README.md) | 190 minutes (measured) |

Assignment 4 has ten steps, two of them live (a test-generation run and one A/B), plus a portfolio.

## Step 6: Final project

The [final project](../final-project/README.md) runs the whole harness on a new feature, one of
Feature 5: Bulk close, Feature 6: Watchers, or Feature 7: Labels, as one A/B. The course's own bulk
close run took 12 min 9 s from launch to its cost line (measured). Reading the result field by field
takes about 30 minutes (estimate). Its [checklist](../final-project/CHECKLIST.md) lists what to hand
in.

## Step 7: Use it in your repo

[Use it in your repo](../use-in-your-repo/README.md) has the starter kit, four skills, and a
step-by-step guide. Copying the kit makes no model calls:

```bash
uv run shipharness init --target ~/my-repo
```

Here `~/my-repo` stands for the path to a repository of yours. Plan 2 to 4 hours (estimate) for a
first map, the house-rule checks, and one A/B on a ticket of your own.

## After class

[After class](after-class.md) covers the days up to the review session: keep your runs and trace
links, re-run a demo, and do the assignments. Bring your self-check output and one question per
assignment to the review session.
