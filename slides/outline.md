# Slide outline: Module 1: Harness Engineering for Coding Agents (80 slides)

[module1-slides.md](module1-slides.md) is the class deck: every slide's text, layout, diagram,
timing, and full speaker notes. This page keeps only the block table and the class plan per
section. Instructor plan with the class-day cheat sheet:
[../docs/instructor-guide.md](../docs/instructor-guide.md).

| Block | Slides | Minutes |
|---|---|---|
| Opening: housekeeping, recap, agenda, the problem | 1-20 (20) | 10 |
| Section 1: Instructions | 21-31 (11) | 50 |
| Break | 32 (1) | 10 |
| Section 2: State and sessions | 33-43 (11) | 50 |
| Section 3: Scope and sandbox | 44-54 (11) | 50 |
| Break | 55 (1) | 5 |
| Section 4: Verification, opening with the poll | 56-67 (12) | 45 |
| Final block | 68-70 (3) | 10.5 |
| Close | 71-80 (10) | 9.5 |
| **Total** | **80** | **240** |

## Class plan per section

The rule: a live A/B only where the runs before class showed a real gap; otherwise harness in
action. Sections 1, 2, and 4 showed no gap on their own tickets, so each shows its layer at work,
live: harness in action (`make show-N`, the harness arm alone, judged by the referee). Section 3:
Scope and sandbox runs a live A/B, `make demo-3 FEATURE=version-checks`: a confirmation registered
before its runs found a gap on scope (bare 0 of 3 passing, harness 3 of 3). The final keeps one live
A/B (`make final`), launched in Section 4 and read in the final block.

Every section has the same shape:

| Position | Content | Slides per section |
|---|---|---|
| Section 4 only | Live Zoom Poll: the final feature, the one poll of the class | 56 |
| Start slide | Agenda marker and the launch of the live run | 21, 33, 44, 57 |
| Story and question | Failure story, then the Socratic question | 22-23, 34-35, 45-46, 58-59 |
| Four ideas | One idea per slide, each with its diagram | 24-27, 36-39, 47-50, 60-63 |
| Cheat sheet | The layer in four moves | 28, 40, 51, 64 |
| DEMO | Implementation notes and the finished run on the console | 29, 41, 52, 65 |
| Results | What we measured, and when the layer earns its place | 30, 42, 53, 66 |
| Q&A | Questions on the section | 31, 43, 54, 67 |

| Section | Live run, launched on the start slide |
|---|---|
| Section 1: Instructions | `make show-1` at 0:11: the map in context, then the documents the ticket needs |
| Section 2: State and sessions | `make show-2 SESSION_BUDGET=12,38` at 1:11: session 1 stops, session 2 resumes |
| Section 3: Scope and sandbox | `make demo-3 FEATURE=version-checks` at 2:01: the bare arm's out-of-scope edit, the harness arm's blocked edit |
| Section 4: Verification | `make show-4` and `make final FEATURES=<winner>,<runner-up>` at 2:57, right after the poll |

Each run is launched at the start of its section, so it has the whole section to finish before
its DEMO slide. The DEMO slides show no screenshots: the instructor walks through the live run, and
the notes say what to point at on each console screen.
