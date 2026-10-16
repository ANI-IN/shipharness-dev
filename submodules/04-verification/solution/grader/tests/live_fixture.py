"""SYNTHETIC live evidence for the grader's own tests. Not a real run: no model was called.

Every value here is made up and marked as such: run ids carry the date 2000-01-01, trace links
point at `https://smith.langchain.com/synthetic-fixture/...`, every cost is invented, and each
transcript starts with a `# SYNTHETIC FIXTURE` line. Only `checkpoint_sha` is real: it is the
commit this repository's `m1-s4-start` tag names, passed in by the caller, so the fixture can
pass the commit check. Never copy these files into a submission or a portfolio.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

LABEL = "# SYNTHETIC FIXTURE: made-up values for the grader's own tests, not a real run"
TG_RUN = "r-20000101-000000-00000a"
AB_ID = "ab-20000101-000000-00000b"
RUN_IDS = {"bare": "r-20000101-000000-00000c", "harness": "r-20000101-000000-00000d"}
HARNESS_LAYERS = ["instructions", "scope", "state", "verify"]
GEN = "tests/test_issues_generated.py"
KEPT = [f"{GEN}::test_list_hides_deleted", f"{GEN}::test_list_hides_deleted_again"]
DROPPED = f"{GEN}::test_adds_nothing"

TESTGEN_COMMAND = (
    "uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 "
    "--out .shipharness/a4/testgen"
)
AB_COMMAND = "uv run shipharness ab --section demo-4 --feature F4 --no-preview"


def checkpoint_sha(repo: Path, tag: str = "m1-s4-start") -> str:
    run = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", f"{tag}^{{commit}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return run.stdout.strip()


def _row(test_id: str, number: int, passed: bool, reason: str) -> dict[str, Any]:
    return {"test_id": test_id, "filter": number, "passed": passed, "reason": reason}


def testgen_report() -> dict[str, Any]:
    """A testgen report after `apply_filter --update-report` (synthetic)."""
    rows = [_row(tid, n, True, f"filter {n}: synthetic pass") for tid in KEPT for n in range(1, 6)]
    rows += [
        _row(DROPPED, 1, True, "filter 1: synthetic pass"),
        _row(DROPPED, 2, True, "filter 2: synthetic pass"),
        _row(DROPPED, 3, False, "filter 3: synthetic: no new coverage and no mutant killed"),
        _row(KEPT[0], 6, True, "filter 6: no duplicate among 3 existing tests"),
        _row(KEPT[1], 6, False, f"filter 6: duplicate of earlier candidate {KEPT[0]}"),
    ]
    return {
        "run_id": TG_RUN,
        "status": "completed",
        "unsandboxed": True,
        "baseline_includes_doctests": False,
        "kept": list(KEPT),
        "not_evaluated": [],
        "results": rows,
        "filter6": {"kept": [KEPT[0]], "existing_tests": 3},
    }


def testgen_transcript() -> str:
    return "\n".join(
        [
            LABEL,
            f"$ {TESTGEN_COMMAND}",
            "target TG-teamtrack-app-repositories-issues: app/repositories/issues.py in teamtrack",
            "! UNSANDBOXED — results not official: generated tests run on this machine",
            "Baseline: existing suite without doctests",
            f"testgen {TG_RUN}: completed; kept 2 of 3 proposed tests",
            *[f"+ {tid}" for tid in KEPT],
            f"- {DROPPED}: filter 3: synthetic: no new coverage and no mutant killed",
            "Kept tests and report: .shipharness/a4/testgen",
            "Cost: $0.012345 (testgen, model gpt-6-luna)",
            "",
        ]
    )


def score_record(arm: str, sha: str) -> dict[str, Any]:
    """One synthetic ScoreRecord (every field of `shipharness.ab.score.ScoreRecord`)."""
    harness = arm == "harness"
    return {
        "run_id": RUN_IDS[arm],
        "ab_id": AB_ID,
        "arm": arm,
        "feature_id": "F4",
        "variant": "canonical",
        "checkpoint": "m1-s4-start",
        "checkpoint_sha": sha,
        "layers": HARNESS_LAYERS if harness else [],
        "status": "completed",
        "claim": "done",
        "r1_new_violations": 0,
        "r1_leaks": 0,
        "r2_new_violations": 0,
        "r3_new_failures": 0,
        "r4_duplicates": 0,
        "r5_audit_missing": 0,
        "r6_ok": True,
        "r7_ok": True,
        "regression_passed": 10,
        "regression_total": 10,
        "hidden_passed": 70 if harness else 40,
        "hidden_total": 70,
        "mutants_killed": 8 if harness else 2,
        "mutants_total": 8,
        "shipped_tests": 5,
        "flaky_tests": 0,
        "out_of_scope_files": 0,
        "test_phase_source_edits": 0,
        "continuity_failure": None,
        "redone_lines_pct": None,
        "board_ok": True,
        "reviewer_verdict": "accept" if harness else "reject",
        "reviewer_agrees": True,
        "primary": {"hidden_passed": 70 if harness else 40, "mutants_killed": 8 if harness else 2},
        "passed_primary": harness,
        "cost_usd": 0.06 if harness else 0.05,
        "review_cost_usd": 0.005,
        "turns_total": 20,
        "wall_s": 100.0,
        "trace_url": f"https://smith.langchain.com/synthetic-fixture/{RUN_IDS[arm]}",
        "referee_trace_url": None,
        "sandboxed": True,
        "recorded": False,
        "captured_at": "2000-01-01T00:00:00+00:00",
    }


def _record_line(record: dict[str, Any]) -> str:
    """The line `shipharness ab` prints per arm (`_print_record` in ab/commands.py)."""
    return (
        f"  {record['arm']:<8} {record['status']:<17} claim={record['claim']:<8} "
        f"primary={json.dumps(record['primary'])} passed={record['passed_primary']} "
        f"hidden {record['hidden_passed']}/{record['hidden_total']} "
        f"mutants {record['mutants_killed']}/{record['mutants_total']} "
        f"reviewer={record['reviewer_verdict']} cost=${record['cost_usd']:.4f}"
    )


def ab_transcript(records: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            LABEL,
            f"$ {AB_COMMAND}",
            f"A/B {AB_ID} (F4, layers={HARNESS_LAYERS})",
            *[_record_line(r) for r in records],
            "Cost: $0.120000 (this command: gpt-5.6-luna $0.010000, gpt-6-luna $0.110000; "
            "session $0.120000 of $2.50)",
            "",
        ]
    )


def write_live(root: Path, sha: str) -> Path:
    """Write the synthetic `live/` folder under `root`; return `root`."""
    live = root / "live"
    (live / "scores").mkdir(parents=True, exist_ok=True)
    (live / "testgen.txt").write_text(testgen_transcript(), encoding="utf-8")
    (live / "testgen-report.json").write_text(json.dumps(testgen_report(), indent=2), "utf-8")
    records = [score_record(arm, sha) for arm in ("bare", "harness")]
    for record in records:
        path = live / "scores" / f"{record['run_id']}.json"
        path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    (live / "ab.txt").write_text(ab_transcript(records), encoding="utf-8")
    return root
