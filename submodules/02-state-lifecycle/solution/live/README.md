# live

Evidence of the required live step for the reference solution: one A/B on the four-session F2 task
(`F2-a2-four-sessions`, session budget [10, 10, 10, 20]) with the reference `ResumableStateLayer`
as the harness arm's state layer and gpt-6-luna as the agent model. The wrapper writes these files
next to this README: `task.jsonl`, `command.txt`, `output.txt`, `summary.json`, and
`scores/<run_id>.json` (one ScoreRecord per arm). The grader checks them with
`assignment/a2_scenario/live_evidence.py`; until they are here, the grader gives the reference
solution 90/100 (the live criterion fails with "live/: missing ...").

Command (from the repository root, with keys, Docker, and the checkpoints; `make doctor` passes):

```
uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops
```

[[PENDING: captured live run of the reference solution | source: M8 batch 1 | how: uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl submodules/02-state-lifecycle/solution --forced-stops]]

After recording it, re-capture the grader output:
`uv run python submodules/02-state-lifecycle/solution/grader/grade.py --impl submodules/02-state-lifecycle/solution`.

[[PENDING: grader output on the reference solution with its captured live run (100/100 expected if the evidence is valid) | source: M8 batch 1 | how: uv run python submodules/02-state-lifecycle/solution/grader/grade.py --impl submodules/02-state-lifecycle/solution > submodules/02-state-lifecycle/solution/captured/grade-solution.txt]]
