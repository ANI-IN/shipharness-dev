# LangSmith traces: F4 A/B, bare vs harness

Reference version. The links and the numbers come from the reference solution's live run, whose
files go in `../live/`.

## Trace links

[[PENDING: trace_url of the bare and the harness arm, each with its run id (from live/scores/<run_id>.json) | source: M6 pilot | how: uv run shipharness ab --section demo-4 --feature F4 --purpose assignment --no-preview]]

## Command

```
uv run shipharness ab --section demo-4 --feature F4 --purpose assignment --no-preview
```

The command runs the F4 ticket (example `F4-canonical` in `datasets/teamtrack-features-v1.jsonl`,
checkpoint `m1-s4-start`) in both arms: bare with no harness layer, harness with the demo-4 stack
(instructions, state, scope, verify; `SECTION_STACKS` in `src/shipharness/ab/demo.py`). The
referee judges both builds the same way and writes one score record per arm to
`exports/scores/<run_id>.json`. `--no-preview` skips the board preview containers. The command
prints the A/B id, one line per arm, and the cost line. `--purpose assignment` traces each run
to the LangSmith project `shipharness-assignments` (agent root and referee) and counts its spend in
the `assignment` cost session (`_trace_target` in `src/shipharness/ab/commands.py`).

## What the comparison shows

[[PENDING: per-arm counts from the two score records: hidden tests passed, mutants killed, existing tests that keep passing, new R1-R7 violations, reviewer verdict | source: M6 pilot | how: read live/scores/<run_id>.json after uv run shipharness ab --section demo-4 --feature F4 --purpose assignment --no-preview]]

[[PENDING: cost line printed by the ab command | source: M6 pilot | how: last line of live/ab.txt]]

How to read it: F4's primary measure has two parts, hidden tests passed and mutants killed, each
against its total (`primary_measure` in the F4 dataset line). One A/B at k=1 is one run per arm,
so a difference between the arms is a single observation; the page reports counts, not rates.
