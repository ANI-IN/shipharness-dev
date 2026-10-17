# Slide outline: Module 1 (72 slides)

[deck.md](deck.md) is the single source of the slide content: titles, bullets, code excerpts,
diagrams, timings, speaker notes, and the "Filled in live" boxes. This page keeps only the block
table and the class plan per section, so the two files cannot drift apart. Build and format:
[README.md](README.md). Stage-by-stage instructor plan: [../docs/instructor-guide.md](../docs/instructor-guide.md).

| Block | Slides | Minutes |
|---|---|---|
| Opening | 1-7 (7) | 10 |
| S1 Instructions | 8-21 (poll and launch 2, concepts and code 9, demo block and discussion 3) | 50 |
| S2 State and session lifecycle | 22-34 (poll and launch 2, concepts and code 8, demo block and discussion 3) | 50 |
| Break | 35 (1) | 10 |
| S3 Scope and sandbox | 36-48 (poll and launch 2, concepts and code 8, demo block and discussion 3) | 50 |
| S4 Verification | 49-63 (S4 poll, final feature poll, and launch 3; concepts and code 9; demo block and discussion 3) | 50 |
| Final results | 64-68 (final A/B 4, what the pilot measured 1) | 13 |
| Wrap-up | 69-72 (assignments, skills and starter kit, references 2) | 7 |
| **Total** | **72** | **240** |

## Class plan per section

The course pilot showed no measurable difference on any section's primary measure, so no section
runs a live A/B. Each section shows its layer at work, live: harness in action (`make show-N`, the
harness arm alone, live checks, live console). The final keeps one live A/B (`make final`), launched
in S4, as the measurement lesson. Recorded showcases and constructed examples are optional extras in
`docs/extras.md`, not part of any demo block. Slide 68 shows every section's
result, wins and "no measurable difference" alike.

| Position | Content | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| Opens the section | Poll: predict a pilot result (answer on the results slide) | 8 | 22 | 36 | 49 |
| S4 only | Final feature poll | | | | 50 |
| Right after the poll | Launch `make show-N` (S4: also `make final`), with the section's Mermaid diagram of the demo | 9 | 23 | 37 | 51 |
| Demo block 1 | What to watch: harness in action on the console (screens 1, 3, 5, 2), with real screenshots | 19 | 32 | 46 | 61 |
| Demo block 2 | Reading the result: the show run's verdict and what the pilot measured for the section | 20 | 33 | 47 | 62 |
| Closes the section | Runbook link, discussion, transition | 21 | 34 | 48 | 63 |

| Section | Harness in action (live) |
|---|---|
| S1 | `make show-1`: the map in context, then the documents the ticket needs |
| S2 | `make show-2 SESSION_BUDGET=12,38`: the handoff at the end of session 1, the resume in session 2 |
| S3 | `make show-3`: blocked or reverted edits with reasons, the sandbox policy |
| S4 | `make show-4`: handoffs, the test phase, the filters, the gate |

The screenshots on the demo-block slides (19, 20, 32, 33, 46, 47, 61, 62) and on the final results
slides (65, 66) come from the quiet runs of the class commands on 2026-10-17; each slide names its
run id. The concept and code slides sit between the launch and the demo block; the show run
proceeds in terminal B while they are shown. "Filled in live" boxes mark values produced in class:
slide 7 (doctor and assessment), the polls (8, 22, 36, 49, 50), the show runs (19, 32, 46, 61), the
break (35), and the final A/B (64-67).
