# Instructor materials

Everything the instructor needs to run "Module 1: Harness Engineering for Coding Agents" live and to
run the Thursday review. The class plan per section: S1, S2, and S4 run harness in action, live
(`make show-1`, `make show-2 SESSION_BUDGET=12,38`, `make show-4`); S3 runs a live A/B,
`make demo-3 FEATURE=version-checks`, because the pre-registered S3 confirmation came out "harness ahead"; the
final runs one live A/B, `make final` (VERIFICATION.md, "Class plan per section" and "S3
confirmation: result"). Measured times and costs come from the demo runs measured 2026-10-18, three
per class command (docs/evidence/general.md, "Demo runs after the speed-up"). The class date (`SHIPHARNESS_CLASS_DATE`) is set at T-30 on
the class day, in step 1 of the run sheet's "Before class".

| File | Use it for |
|---|---|
| [run-sheet.md](run-sheet.md) | The 240-minute class, minute by minute: commands, console screens and keys, what to say during each run, the all-results table, and, in the sections marked "Fallback", the known failure modes with exact messages and the replay procedure |
| [code-walkthrough.md](code-walkthrough.md) | Every walkthrough anchor (`platform/scripts/anchors.py list`) with its file, lines, the code pulled from the repository, and talking points with source citations |
| [poll-questions.md](poll-questions.md) | The one poll of the class: the final feature poll at the start of Section 4 (2:55-2:57) |
| [fallbacks.md](fallbacks.md) | The fallback recordings per class command (how to record them, where they live, how to replay them with the RECORDING badge, what to say), and the optional extras (the showcases and the constructed examples; not in the demo flow) |
| [review-session-guide.md](review-session-guide.md) | The 2-hour Thursday review: 25 minutes per assignment, the files to open, the A3 hidden-diff reveal, open questions |
| [engineering-notes/](engineering-notes/) | Provenance records from building the repository, the owner's instructions, and the option A story drafts; not course material |

Related: the public guide with the one-page class-day cheat sheet is
[../docs/instructor-guide.md](../docs/instructor-guide.md); the slide outline is
[../slides/outline.md](../slides/outline.md); section demo pages are in `section-N-*/demo/README.md`; design
and contracts are [../DESIGN.md](../DESIGN.md) (§13 console, §14 class plan) and
[../CONTRACTS.md](../CONTRACTS.md).
