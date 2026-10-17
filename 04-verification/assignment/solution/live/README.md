# live

Live evidence of the reference solution, in the layout every submission uses (brief:
`../../assignment/README.md`, "Live step"). Two runs, both captured on 2026-10-17: the testgen run
`r-20261017-093940-52dde8` with filter 6 applied to its report, and the F4 A/B
`ab-20261017-094339-3b29e3`. The grader validates these files the same way as a learner's
(`assignment/visible_tests/a4_live.py`) and re-runs nothing; `../portfolio/` reports what they show.

| File | What it holds |
|---|---|
| `testgen.txt` | captured on 2026-10-17, run `r-20261017-093940-52dde8`: `$ <testgen command>`, then everything the command printed, ending with `Cost: $0.003287 (testgen, model gpt-6-luna)`; "kept 1 of 5 proposed tests" |
| `testgen-report.json` | captured on 2026-10-17, run `r-20261017-093940-52dde8`: `.shipharness/a4/testgen/testgen-report.json` after `apply_filter --update-report`; 17 rows of filters 1-5, one filter-6 row, and `filter6` (1 kept test, 23 existing tests) |
| `ab.txt` | captured on 2026-10-17, run `ab-20261017-094339-3b29e3`: `$ <ab command>`, then everything the command printed (the A/B line, one line per arm, the `Cost:` line) |
| `scores/r-20261017-094339-1abebd.json` | captured on 2026-10-17, run `ab-20261017-094339-3b29e3`: the bare arm's ScoreRecord, copied from `exports/scores/` |
| `scores/r-20261017-094339-f5e6af.json` | captured on 2026-10-17, run `ab-20261017-094339-3b29e3`: the harness arm's ScoreRecord, copied from `exports/scores/` |

The commands that produced them (from the repository root; keys in `.env`; Docker running for the
A/B). The testgen command runs without `--image`, so its tests ran on the host and it printed an
UNSANDBOXED warning (first lines of `testgen.txt`).

```
L=04-verification/assignment/solution/live
export PYTHONPATH=04-verification/assignment/solution
mkdir -p $L/scores
echo '$ uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 --out .shipharness/a4/testgen' > $L/testgen.txt
uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 \
    --out .shipharness/a4/testgen 2>&1 | tee -a $L/testgen.txt
uv run python -m a4_verification.apply_filter --repo platform/teamtrack --kept .shipharness/a4/testgen \
    --existing tests/visible/test_tenant_isolation.py --existing tests/visible/test_issues.py \
    --existing tests/visible/test_legacy_and_schema.py --update-report
cp .shipharness/a4/testgen/testgen-report.json $L/
echo '$ uv run shipharness ab --section demo-4 --feature F4 --purpose assignment --no-preview' > $L/ab.txt
uv run shipharness ab --section demo-4 --feature F4 --purpose assignment --no-preview 2>&1 | tee -a $L/ab.txt
AB=$(grep -o 'ab-[0-9]\{8\}-[0-9]\{6\}-[0-9a-f]\{6\}' $L/ab.txt | head -1)
grep -l "\"ab_id\": \"$AB\"" exports/scores/*.json | xargs -I{} cp {} $L/scores/
make grade-assignment-4 SUBMISSION=04-verification/assignment/solution   # instructor only
```

What `apply_filter` printed is not kept here; its result is in the report (the filter-6 row and
`filter6`). A new capture replaces all five files at once, then the run sections of
`../portfolio/` and `../captured/grade-solution.txt` are updated from them.
