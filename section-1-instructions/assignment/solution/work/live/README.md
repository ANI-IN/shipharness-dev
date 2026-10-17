# Module 1: Harness Engineering for Coding Agents - Live evidence of the reference A/B

This folder holds the live evidence of the reference solution's A/B, in the layout that
`assignment/live_evidence.py` collects and that the self-check and the grader check:

| Path | What it is |
|---|---|
| `output.txt` | the command line (`$ ...`) and everything it printed, ending with its `Cost: $...` line |
| `experiments/<name>.json` | the two experiment exports of batch `a1-reference` (bare and harness) |
| `scores/<run_id>.json` | the score record (`platform/src/shipharness/ab/score.py`) of every run in them |
| `runs/<run_id>/events.jsonl` | the run log of every harness-arm run |

The reference live run is being re-run; its first attempt was interrupted on 2026-10-17. Until it
is captured, this folder holds no evidence, and the grader gives the reference 0 of the 12
points of criterion F, with or without `--allow-pending` (`captured/grade-solution.txt`).

If the run is captured later, these are the commands (repository root; needs keys and Docker;
within the Assignment 1 budget of $2.50):

```bash
git switch -c a1-reference-run                     # throwaway branch: never merge it
rm -rf platform/teamtrack/harness/instructions
cp -r section-1-instructions/assignment/solution/work/instructions platform/teamtrack/harness/instructions
git add platform/teamtrack/harness/instructions && git commit -m "Assignment 1: reference tree for the live A/B"
git log -1 --format=%h                             # the "Instructions tree commit"
CMD="uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference"
echo "\$ $CMD" > ~/a1-reference-output.txt
$CMD | tee -a ~/a1-reference-output.txt
git switch -                                       # back to your branch
uv run python section-1-instructions/assignment/live_evidence.py --batch a1-reference --output ~/a1-reference-output.txt --work section-1-instructions/assignment/solution/work
uv run python section-1-instructions/assignment/ab_summary.py --batch a1-reference --exports section-1-instructions/assignment/solution/work/live
```

After such a capture, fill `../ab-report.md` from the `ab_summary.py` output, replace the
paragraph above with the capture date, and check that the grader gives the reference 100 without
`--allow-pending`.
