"""Run filter 6 over the tests a `shipharness testgen` run kept.

    uv run python -m a4_verification.apply_filter --repo <repo> --kept <testgen out dir> \\
        --existing <test file or folder> [--existing ...]

`--kept` is the folder testgen printed as "Kept tests and report" (it holds `testgen-report.json`
and the kept test files). `--existing` names the repo's existing tests, relative to `--repo`. The
filter compares each kept test with the existing tests and with the kept tests before it. Nothing
is executed: filter 6 only reads source. Exit 0 after a report, 1 on bad input.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from a4_verification.dedup_filter import NoDuplicateTest
from shipharness.filters import CoverageMap, FilterContext, collect_candidates, run_pipeline


def _test_files(repo: Path, targets: list[str]) -> list[str]:
    files: list[str] = []
    for target in targets:
        path = (repo / target).resolve()
        if path.is_dir():
            found = sorted(path.rglob("test_*.py")) + sorted(path.rglob("*_test.py"))
            files.extend(p.relative_to(repo.resolve()).as_posix() for p in found)
        elif path.is_file():
            files.append(path.relative_to(repo.resolve()).as_posix())
        else:
            raise ValueError(f"existing test path not found: {target}")
    return list(dict.fromkeys(files))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m a4_verification.apply_filter")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--kept", type=Path, required=True)
    parser.add_argument("--existing", action="append", default=[], required=True)
    args = parser.parse_args(argv)
    report_path = args.kept / "testgen-report.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        existing = collect_candidates(args.repo, _test_files(args.repo, args.existing))
    except (OSError, ValueError) as exc:
        print(f"ERROR {exc}")
        return 1
    kept_ids = [str(t) for t in report.get("kept", [])]
    files = list(dict.fromkeys(tid.split("::", 1)[0] for tid in kept_ids))
    by_id = {c.test_id: c for c in collect_candidates(args.kept, files)}
    cands = [by_id[tid] for tid in kept_ids if tid in by_id]
    ctx = FilterContext(
        workspace=args.kept,
        sandbox=None,
        baseline_coverage=CoverageMap(),
        filter_mutants=[],
        source_shas_at_phase_start={},
    )
    flt = NoDuplicateTest(existing)
    results = run_pipeline(cands, ctx, None, filters=[flt])
    for result in results:
        sign = "+" if result.passed else "-"
        print(f"{sign} {result.test_id}: filter {result.filter}: {result.reason}")
    kept = sum(1 for r in results if r.passed)
    missing = len(kept_ids) - len(cands)
    print(
        f"filter 6 kept {kept} of {len(cands)} kept tests "
        f"({len(existing)} existing tests compared; {missing} kept ids not found)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
