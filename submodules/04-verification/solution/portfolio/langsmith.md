# LangSmith experiment: section-4 split, bare vs harness

Reference version. The link and the numbers come from the instructor's run.

## Experiment link

[[PENDING: LangSmith comparison URL for the bare and harness experiments (the `url` printed per arm by the command below) | source: M6 pilot | how: uv run shipharness experiments --dataset teamtrack-features-v1 --split section-4 --k 1 --batch a4-reference]]

## Command

```
uv run shipharness experiments --dataset teamtrack-features-v1 --split section-4 --k 1 \
    --batch a4-reference
```

The command runs LangSmith `evaluate()` once per arm on the same 8 examples of the `section-4`
split (`datasets/teamtrack-features-v1.jsonl`), with the referee as the evaluator, and writes the
score records to `exports/` (DESIGN §12). It prints one line per arm with the experiment name,
summary statistics, and URL, then the cost line.

## What the comparison shows

[[PENDING: per-arm counts from the comparison view: runs whose hidden tests all pass, existing tests that keep passing, new R1-R7 violations, kept tests and mutant kills | source: M6 pilot | how: open the comparison link; or read exports/experiments/<name>.json]]

[[PENDING: cost line printed by the experiments command | source: M6 pilot | how: last line of the command above]]

What to read in the comparison view: the referee's scores are evaluator feedback on each run, so
the view lines up both arms per example. With k=1 each example has one run per arm; a difference
on one example is a single observation, so the page reports counts, not rates.
