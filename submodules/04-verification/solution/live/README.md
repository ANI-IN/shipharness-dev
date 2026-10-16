# live

Live evidence of the reference solution, in the layout every submission uses (brief:
`../../assignment/README.md`, "Live step"). The captured files replace the marker below. Until
then the grader accepts the marker for this folder only (`pending_only` in
`assignment/visible_tests/a4_live.py`); for any other folder a missing file fails the
`live-evidence` criterion. So the reference solution's 10 live-evidence points are not yet earned
on real evidence. The integrator records the run and then removes that special case.

| File | What goes in it |
|---|---|
| `testgen.txt` | `$ <testgen command>`, then everything the command printed, `Cost:` line included |
| `testgen-report.json` | `.shipharness/a4/testgen/testgen-report.json` after `apply_filter --update-report` |
| `ab.txt` | `$ <ab command>`, then everything the command printed, `Cost:` line included |
| `scores/<run_id>.json` | The two ScoreRecords of that A/B, copied from `exports/scores/` |

Commands (from the repository root; keys in `.env`; Docker running for the A/B):

```
L=submodules/04-verification/solution/live
export PYTHONPATH=submodules/04-verification/solution
mkdir -p $L/scores
echo '$ uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 --out .shipharness/a4/testgen' > $L/testgen.txt
uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 \
    --out .shipharness/a4/testgen 2>&1 | tee -a $L/testgen.txt
uv run python -m a4_verification.apply_filter --repo teamtrack --kept .shipharness/a4/testgen \
    --existing tests/visible/test_tenant_isolation.py --existing tests/visible/test_issues.py \
    --existing tests/visible/test_legacy_and_schema.py --update-report
cp .shipharness/a4/testgen/testgen-report.json $L/
echo '$ uv run shipharness ab --section demo-4 --feature F4 --no-preview' > $L/ab.txt
uv run shipharness ab --section demo-4 --feature F4 --no-preview 2>&1 | tee -a $L/ab.txt
AB=$(grep -o 'ab-[0-9]\{8\}-[0-9]\{6\}-[0-9a-f]\{6\}' $L/ab.txt | head -1)
grep -l "\"ab_id\": \"$AB\"" exports/scores/*.json | xargs -I{} cp {} $L/scores/
uv run python submodules/04-verification/solution/grader/grade.py
```

Then remove the marker, fill the `[[PENDING]]` sections of `../portfolio/` from these files, and
recapture `../captured/grade-solution.txt`.

[[PENDING: captured live run of the reference solution (testgen with filter 6, then the F4 A/B) | source: M6 pilot | how: uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 --out .shipharness/a4/testgen; apply_filter --update-report as above; uv run shipharness ab --section demo-4 --feature F4 --no-preview; files to live/testgen.txt, live/testgen-report.json, live/ab.txt, live/scores/<run_id>.json]]
