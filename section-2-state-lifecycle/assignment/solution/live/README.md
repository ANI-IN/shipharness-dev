# live

This folder holds the files of the reference solution's live step: one A/B on the four-session F2
task (`F2-a2-four-sessions`, session budget [10, 10, 10, 20]), with the reference
`ResumableStateLayer` as the harness arm's state layer and gpt-6-luna as the agent model.

Command (from the repository root, with keys, Docker, and the checkpoints; `make doctor` passes):

```
uv run python 02-state-lifecycle/assignment/live/run_live.py --impl 02-state-lifecycle/assignment/solution --forced-stops
```

The script writes these files next to this README: `task.jsonl`, `command.txt`, `output.txt`,
`summary.json`, and `scores/<run_id>.json` (one score record per arm). The grader checks them with
`assignment/a2_scenario/live_evidence.py`.

## This run is not valid evidence

The run in this folder finished, but it does not meet the live step's rule. The rule asks for four
build sessions in the harness arm, the first three ended by their turn budget, and three session
stops. In this run the harness arm reached its agent time limit (300 s) on turn 8 of session 3, so
it had three sessions, two session stops, and no session 4. The script says so at the end of
`output.txt`:

```text
x live evidence in 02-state-lifecycle/assignment/solution/live is not valid:
  - summary: the harness arm needs 4 build sessions, the first 3 ended by turn_budget (found 3: ['turn_budget', 'turn_budget', 'timeout'])
  - summary: the harness arm needs 3 session_stop events (sessions 1-3), found [1, 2]
```

Where the time went, from the harness arm's run log: each session began with start-up calls before
the agent read the ticket. Session 1 ran one long status command (23 s) and the visible test suite
(37 s); sessions 2 and 3 ran `bash init.sh` (20 s and 40 s) and the visible test suite (55 s and
51 s). Those calls took about 225 s of the 300 s, so session 3 ran out of time before its turn
budget. The
bare arm ran all four sessions in 159 s of agent time. The run shared the machine with another
live A/B, which made the tool calls slower.

The grade of this folder is 90/100: every scenario criterion passes, and the live criterion
(10 points) gives 0 because of the two problems above (`../captured/grade-solution.txt`).

To try again, move the files listed above out of this folder (keep this README), then run the
command again. The script refuses to run while `summary.json` is here.
