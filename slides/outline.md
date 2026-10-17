# Slide outline: Module 1: Harness Engineering for Coding Agents (72 slides)

[deck.md](deck.md) is the single source of the slide content: titles, bullets, code excerpts,
diagrams, timings, speaker notes, and the "Filled in live" boxes. This page keeps only the block
table and the class plan per section, so the two files cannot drift apart. Build and format:
[README.md](README.md). Instructor plan with the class-day cheat sheet:
[../docs/instructor-guide.md](../docs/instructor-guide.md).

| Block | Slides | Minutes |
|---|---|---|
| Opening | 1-7 (7) | 10 |
| S1 Instructions | 8-21 (poll and launch 2, concepts and code 9, demo block and discussion 3) | 50 |
| S2 State and session lifecycle | 22-34 (poll and launch 2, concepts and code 8, demo block and discussion 3) | 50 |
| Break | 35 (1) | 10 |
| S3 Scope and sandbox | 36-48 (poll and launch 2, concepts and code 8, demo block and discussion 3) | 50 |
| S4 Verification | 49-63 (S4 poll, final feature poll, and launch 3; concepts and code 9; demo block and discussion 3) | 50 |
| Final results | 64-68 (final A/B 4, what we measured 1) | 13 |
| Wrap-up | 69-72 (assignments, skills and starter kit, references 2) | 7 |
| **Total** | **72** | **240** |

## Class plan per section

The rule: a live A/B only where the runs before class showed a real gap; otherwise harness in action.
S1, S2, and S4 showed no gap on their own tasks, so each shows its layer at work, live: harness in
action (`make show-N`, the harness arm alone, live checks, live console). S3 runs a live A/B,
`make demo-3 FEATURE=F4`: a confirmation registered before its runs found a gap on scope (bare 0 of
3 passing, harness 3 of 3). The final keeps one live A/B (`make final`), launched in S4, as the
measurement lesson. Recorded showcases and constructed examples are optional extras in
`docs/extras.md`, not part of any demo block. Slide 68 shows every section's result, the harness
lead and "no measurable difference" alike.

| Position | Content | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| Opens the section | Poll: predict a result from before class (answer on the results slide) | 8 | 22 | 36 | 49 |
| S4 only | Final feature poll | | | | 50 |
| Right after the poll | Launch the live run (S4: also `make final`), with the section's Mermaid diagram | 9 | 23 | 37 | 51 |
| Demo block 1 | What to watch on the console, with real screenshots | 19 | 32 | 46 | 61 |
| Demo block 2 | Reading the result: tonight's verdict and what was measured before class | 20 | 33 | 47 | 62 |
| Closes the section | Runbook link, discussion, transition | 21 | 34 | 48 | 63 |

| Section | Live run |
|---|---|
| S1 | `make show-1`: the map in context, then the documents the ticket needs |
| S2 | `make show-2 SESSION_BUDGET=12,38`: the handoff at the end of session 1, the resume in session 2 |
| S3 | `make demo-3 FEATURE=F4`: live A/B; the bare arm's out-of-scope edit, the harness arm's blocked edit with its reason |
| S4 | `make show-4`: handoffs, the test phase, the filters, the gate |

The screenshots on the demo-block slides (19, 20, 32, 33, 46, 47, 61, 62) and on the final results
slides (65, 66) come from timed runs of the class commands on 2026-10-17: the show runs and the
final run one command at a time, and, for S3, the S3 confirmation A/B that ran alone. S1, S2, S4, and
the final were timed with the earlier 300 s agent time limit; S3 with the class limit of 420 s.
Which run each picture shows is listed in [../docs/evidence.md](../docs/evidence.md) under Captures.
The concept and code slides sit between the launch and the demo block; the live run proceeds in
terminal B while they are shown. "Filled in live" boxes mark values produced in class: slide 7
(doctor and assessment), the polls (8, 22, 36, 49, 50), the live runs (19, 32, 46, 61), the break
(35), and the final A/B (64-67).
