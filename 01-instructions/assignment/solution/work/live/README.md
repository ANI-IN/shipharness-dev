# Live evidence of the reference A/B

This folder holds the live evidence of the reference solution's A/B, in the layout that
`assignment/live_evidence.py` collects and that the self-check and the grader check:

| Path | What it is |
|---|---|
| `output.txt` | the command line (`$ ...`) and everything it printed, ending with its `Cost: $...` line |
| `experiments/<name>.json` | the two experiment exports of batch `a1-reference` (bare and harness) |
| `scores/<run_id>.json` | the ScoreRecord of every run in them (`src/shipharness/ab/score.py`) |
| `runs/<run_id>/events.jsonl` | the run log of every harness-arm run |

The reference live run was not captured. The owner's FOCUS instructions of 2026-10-17 required a
real captured live run for assignments A3 and A4 only, so the A1 reference A/B was left out of
scope. This folder therefore holds no evidence, and the grader gives the reference 0 of the 12
points of criterion F, with or without `--allow-pending` (`captured/grade-solution.txt`).

If the run is captured later, these are the commands (repository root; needs keys and Docker;
within A1's budget of $2.50):

```bash
git switch -c a1-reference-run                     # throwaway branch: never merge it
rm -rf teamtrack/harness/instructions
cp -r submodules/01-instructions/solution/work/instructions teamtrack/harness/instructions
git add teamtrack/harness/instructions && git commit -m "A1: reference tree for the live A/B"
git log -1 --format=%h                             # the "Instructions tree commit"
CMD="uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference"
echo "\$ $CMD" > ~/a1-reference-output.txt
$CMD | tee -a ~/a1-reference-output.txt
git switch -                                       # back to the build branch
uv run python submodules/01-instructions/assignment/live_evidence.py --batch a1-reference --output ~/a1-reference-output.txt --work submodules/01-instructions/solution/work
uv run python submodules/01-instructions/assignment/ab_summary.py --batch a1-reference --exports submodules/01-instructions/solution/work/live
```

After such a capture, fill `../ab-report.md` from the `ab_summary.py` output, replace the
paragraph above with the capture date, and check that the grader gives the reference 100 without
`--allow-pending`.
