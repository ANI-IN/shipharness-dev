# Live evidence of the reference A/B

This folder holds the live evidence of the reference solution's A/B, in the layout that
`assignment/live_evidence.py` collects and that the self-check and the grader check:

| Path | What it is |
|---|---|
| `output.txt` | the command line (`$ ...`) and everything it printed, ending with its `Cost: $...` line |
| `experiments/<name>.json` | the two experiment exports of batch `a1-reference` (bare and harness) |
| `scores/<run_id>.json` | the ScoreRecord of every run in them (`src/shipharness/ab/score.py`) |
| `runs/<run_id>/events.jsonl` | the run log of every harness-arm run |

The run has not been captured yet. Until it is, this file's pending marker stands in for the
evidence, and only `--allow-pending` accepts it.

Commands (repository root; needs keys and Docker; within A1's budget of $2.50):

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

After the capture, fill `../ab-report.md` from the `ab_summary.py` output, replace the marker
below with the capture date, and check that the grader gives the reference 100 without
`--allow-pending`.

[[PENDING: captured live run of the reference solution (output.txt, two experiment exports, 48 score records, 24 harness run logs), collected into this folder | source: M6 pilot | how: uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference, then uv run python submodules/01-instructions/assignment/live_evidence.py --batch a1-reference --output ~/a1-reference-output.txt --work submodules/01-instructions/solution/work]]
