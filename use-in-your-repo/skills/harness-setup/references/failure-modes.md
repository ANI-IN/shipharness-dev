# Common failure modes and the harness part that addresses each

Each row is a failure the sources report, in our words, with the finding ids listed in
`REFERENCES.md` at the repository root. The last column names the part of the harness
and the template from this skill that address it.

| Failure | What you see | Source | Harness part |
|---|---|---|---|
| The agent cannot follow a rule it cannot see | A rule from the team wiki is broken in every session | A1, F-a-05, F-a-06 | Instructions: AGENTS.md map and docs/ |
| One giant instruction file | The file is long, stale, and partly contradictory; the agent follows some of it | A1, F-a-23, F-a-24, F-a-25 | Instructions: short map, one doc per topic |
| Copying the nearest pattern, including bad ones | New code repeats a legacy handler's mistakes | A1, F-a-20 | Instructions: ARCHITECTURE.md "patterns to copy" and "legacy" tables; a house rule with a check |
| Trying to do everything at once | The session runs out of context mid-feature and leaves it half-done and undocumented | A2, F-a-11, F-a-12 | Scope: feature_list.json, one feature per session |
| Declaring the job done early | A later session sees progress and stops | A2, F-a-13 | Scope: every feature starts with `passes: false`; Verification: a gate before done |
| Marking a feature done without testing it end to end | Unit tests pass, the feature does not work for a user | A2, F-a-16, F-a-104 | Verification: end-to-end check, clean-state checklist |
| Time spent working out how to run the app | Each session rediscovers the start command | A2, F-a-64 | State: init.sh |
| The next session guesses what happened | Work is redone or undone | A2, F-a-12, F-a-53 | State: progress.md and git history; Lifecycle: session-handoff.md |
| Self-evaluation skews positive | The agent praises mediocre work | A3, F-a-14, F-a-15 | Verification: a separate evaluator with grading criteria |
| Visible tests pass, the job is not done | Held-out tests that combine features fail | A4, F-a-17; B13, F-b-45, F-b-50 | Verification: held-out tests, mutant-guided tests (assured-tests skill) |
| Hard-to-undo actions | An agent kills its own process or deletes files | A4, F-a-18, F-a-19; A6, F-a-21 | Scope: container, no network, allowlisted commands |
| Context window pollution | Test runs print thousands of lines and push the task out of context | A4, F-a-131 | Verification: short, grep-friendly output; logs in files (init.sh template) |
| Time blindness | The agent runs the full slow suite again and again | A4, F-a-133 | Verification: a fast sample mode |
| Docs drift from the code | The map points to files that moved | A1, F-a-25, F-a-26, F-a-37 | Instructions: mechanical checks on docs (assessment check I3 is a small version) |

## How to use this table

When an agent run goes wrong, find the row that matches what you saw, then check the harness part
in the last column first. A1's advice for every such case: ask "what capability is missing, and how
do we make it both legible and enforceable for the agent?" (F-a-04).
