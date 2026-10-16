# live

Evidence of the required live step for the reference solution: one A/B on the four-session F2 task
(`F2-a2-four-sessions`, session budget [10, 10, 10, 20]) with the reference `ResumableStateLayer`
as the harness arm's state layer and gpt-6-luna as the agent model. The wrapper writes these files
next to this README: `task.jsonl`, `command.txt`, `output.txt`, `summary.json`, and
`scores/<run_id>.json` (one ScoreRecord per arm). The grader checks them with
`assignment/a2_scenario/live_evidence.py`; until they are here, the grader gives the reference
solution 90/100 (the live criterion fails with "live/: missing ...", `../captured/grade-solution.txt`).

Command (from the repository root, with keys, Docker, and the checkpoints; `make doctor` passes):

```
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops
```

[[PENDING: captured live run of the reference solution (live/ evidence files written by the wrapper) | source: M6 pilot | how: uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops]]

After recording it, capture the grader output again with
`make grade-assignment-2 SUBMISSION=submodules/02-state-lifecycle/solution` and replace
`../captured/grade-solution.txt` with it, labelled with the date; 100/100 is the expected score when
the evidence is valid.
