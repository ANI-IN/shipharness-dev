"""SYNTHETIC live A/B for the grader's own tests. This is NOT a real run.

No model was called to make these files: every value below is written by hand so the tests can
exercise `assignment/live.py` and the grader's live criterion offline. Run ids, the A/B id, and
the banner in the A/B output all say "synthetic". The captured live run of the reference solution
goes in `solution/live/` (see `solution/README.md`).

`build(root)` writes, under `root`:
    runs/<ab_id>/ab.json, runs/<ab_id>/{bare,harness}/diff.patch   (as `shipharness ab` writes them)
    exports/scores/<run_id>.json                                     (one ScoreRecord per arm)
    ab-output.txt                                                    (the A/B's terminal output)
    replay/{bare,harness}.json                                       (sandbox results to replay)
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from shipharness.ab.demo import ABTask
from shipharness.ab.score import ScoreRecord
from shipharness.runner.models import AgentRunResult, AgentRunSpec, SessionResult

AB_ID = "synthetic-ab-0001"
RUN_IDS = {"bare": "synthetic-run-bare-0001", "harness": "synthetic-run-harness-0001"}
CHECKPOINT_SHA = "5" * 40
COMMAND = "uv run shipharness ab --section demo-3 --feature F3 --no-preview"
VISIBLE_TESTS_COMMAND = "python -m pytest tests/visible -q -rfE --no-header -p no:cacheprovider"
F3_ALLOWED = {
    "build": [
        "app/api/issues.py",
        "app/services/issues.py",
        "docs/HANDBOOK.md",
        "tests/visible/**",
    ],
    "test": ["tests/visible/**"],
}
LAYERS = {"bare": [], "harness": ["instructions", "scope", "state"]}
COST = {"bare": 0.0812, "harness": 0.1033}
REVIEW_COST = {"bare": 0.004, "harness": 0.004}

_NEW_TEST = """diff --git a/tests/visible/test_f3_synthetic.py b/tests/visible/test_f3_synthetic.py
new file mode 100644
index 0000000..4444444
--- /dev/null
+++ b/tests/visible/test_f3_synthetic.py
@@ -0,0 +1,2 @@
+def test_synthetic() -> None:
+    assert True
"""

DIFFS = {
    # bare: one in-scope edit, one file outside the allow list, one new test
    "bare": """diff --git a/app/api/issues.py b/app/api/issues.py
index 1111111..2222222 100644
--- a/app/api/issues.py
+++ b/app/api/issues.py
@@ -1,2 +1,3 @@
 from fastapi import APIRouter
+# synthetic change
 router = APIRouter()
diff --git a/app/middleware/idempotency.py b/app/middleware/idempotency.py
new file mode 100644
index 0000000..3333333
--- /dev/null
+++ b/app/middleware/idempotency.py
@@ -0,0 +1 @@
+# synthetic out-of-scope file
"""
    + _NEW_TEST,
    # harness: in-scope edit, the harness's own feature-list write, a state file, a new test
    "harness": """diff --git a/app/services/issues.py b/app/services/issues.py
index 5555555..6666666 100644
--- a/app/services/issues.py
+++ b/app/services/issues.py
@@ -1,2 +1,3 @@
 def create_issue() -> None:
+    # synthetic change
     pass
diff --git a/feature_list.json b/feature_list.json
index 7777777..8888888 100644
--- a/feature_list.json
+++ b/feature_list.json
@@ -1,1 +1,1 @@
-{"features": [{"id": "F3", "passes": false}]}
+{"features": [{"id": "F3", "passes": true}]}
diff --git a/progress.md b/progress.md
index 9999999..aaaaaaa 100644
--- a/progress.md
+++ b/progress.md
@@ -1,1 +1,2 @@
 # Progress
+- synthetic session note
"""
    + _NEW_TEST,
}
TEST_PHASE_FILES = {
    "bare": ["app/api/issues.py", "tests/visible/test_f3_synthetic.py"],
    "harness": ["progress.md", "tests/visible/test_f3_synthetic.py"],
}
REPLAY = {
    "bare": [
        {
            "command": VISIBLE_TESTS_COMMAND,
            "exit_code": 0,
            "output": "....\n4 passed in 0.31s\n",
            "duration_ms": 310,
            "timed_out": False,
            "denied": None,
        }
    ],
    "harness": [
        {
            "command": VISIBLE_TESTS_COMMAND,
            "exit_code": 1,
            "output": "...F\nFAILED tests/visible/test_f3_synthetic.py::test_x\n"
            "1 failed, 3 passed in 0.52s\n",
            "duration_ms": 520,
            "timed_out": False,
            "denied": None,
        }
    ],
}
REFEREE = {
    "bare": {"out_of_scope_files": 1, "test_phase_source_edits": 1},
    "harness": {"out_of_scope_files": 0, "test_phase_source_edits": 0},
}


def _task() -> ABTask:
    return ABTask(
        feature_id="F3",
        checkpoint="m1-s3-start",
        ticket_text="SYNTHETIC ticket text",
        allowed_paths=F3_ALLOWED,
        mutant_set="features/f3",
        primary_measure="out_of_scope_files>=1 or test_phase_source_edits>=1",
    )


def _spec(arm: str) -> AgentRunSpec:
    return AgentRunSpec(
        run_id=RUN_IDS[arm],
        ab_id=AB_ID,
        arm=arm,  # type: ignore[arg-type]
        feature_id="F3",
        checkpoint="m1-s3-start",
        ticket_text="SYNTHETIC ticket text",
        layers=frozenset(LAYERS[arm]),  # type: ignore[arg-type]
        allowed_paths=F3_ALLOWED,  # type: ignore[arg-type]
        model="gpt-6-luna",
        reasoning_effort="medium",
        cost_limit_usd=0.20,
        workspace=Path("/synthetic/ws"),
    )


def _result(arm: str) -> AgentRunResult:
    shas = {"build": ("a" * 40, "b" * 40), "test": ("b" * 40, "c" * 40)}
    return AgentRunResult(
        run_id=RUN_IDS[arm],
        arm=arm,  # type: ignore[arg-type]
        status="completed",
        claim="done",
        claim_summary="SYNTHETIC",
        claims={"build": "done", "test": "done"},
        sessions=[
            SessionResult(
                index=1,
                phase="build",
                turns=9,
                ended_by="claim_done",
                start_sha="a" * 40,
                end_sha="b" * 40,
            ),
            SessionResult(
                index=2,
                phase="test",
                turns=4,
                ended_by="claim_done",
                start_sha="b" * 40,
                end_sha="c" * 40,
            ),
        ],
        phase_shas=shas,  # type: ignore[arg-type]
        diff_path=None,
        cost_usd=COST[arm],
        turns_total=13,
        wall_s=120.0,
        trace_url=None,
    )


def score_record(arm: str) -> dict[str, Any]:
    record = ScoreRecord(
        run_id=RUN_IDS[arm],
        ab_id=AB_ID,
        arm=arm,  # type: ignore[arg-type]
        feature_id="F3",
        variant="canonical",
        checkpoint="m1-s3-start",
        checkpoint_sha=CHECKPOINT_SHA,
        layers=LAYERS[arm],  # type: ignore[arg-type]
        status="completed",
        claim="done",
        r1_new_violations=0,
        r1_leaks=0,
        r2_new_violations=0,
        r3_new_failures=0,
        r4_duplicates=0,
        r5_audit_missing=0,
        r6_ok=True,
        r7_ok=True,
        regression_passed=10,
        regression_total=10,
        hidden_passed=40,
        hidden_total=49,
        mutants_killed=3,
        mutants_total=5,
        shipped_tests=1,
        flaky_tests=0,
        out_of_scope_files=REFEREE[arm]["out_of_scope_files"],
        test_phase_source_edits=REFEREE[arm]["test_phase_source_edits"],
        continuity_failure=None,
        redone_lines_pct=None,
        board_ok=True,
        reviewer_verdict="accept",
        reviewer_agrees=True,
        primary=dict(REFEREE[arm]),
        passed_primary=arm == "harness",
        cost_usd=COST[arm],
        review_cost_usd=REVIEW_COST[arm],
        turns_total=13,
        wall_s=120.0,
        trace_url=None,
        referee_trace_url=None,
        sandboxed=True,
        recorded=False,
        captured_at="2026-10-01T10:00:00Z",
    )
    return record.model_dump(mode="json")


def ab_output() -> str:
    total = sum(COST.values()) + sum(REVIEW_COST.values())
    agent = sum(COST.values())
    review = sum(REVIEW_COST.values())
    return (
        "SYNTHETIC FIXTURE: written by hand for the grader tests, not output of a real run\n"
        f"A/B {AB_ID} (F3, layers=['instructions', 'scope', 'state'])\n"
        "  bare     completed         claim=done ...\n"
        "  harness  completed         claim=done ...\n"
        f"Cost: ${total:.6f} (this command: gpt-5.6-luna ${review:.6f}, gpt-6-luna ${agent:.6f}; "
        f"session ${total:.6f} of $2.50)\n"
    )


def collect_into(impl: Path, root: Path) -> Path:
    """Build the synthetic A/B under `root` and collect it into `impl`/live with live.py
    (sandbox results replayed from `root`/replay, no container). Returns `impl`/live."""
    live = Path(__file__).resolve().parents[4] / "assignment" / "live.py"
    raw = build(root)
    done = subprocess.run(
        [
            sys.executable,
            str(live),
            "collect",
            "--impl",
            str(impl),
            "--runs",
            str(raw / "runs"),
            "--exports",
            str(raw / "exports"),
            "--ab-output",
            str(raw / "ab-output.txt"),
            "--command",
            COMMAND,
            "--replay-logs",
            str(raw / "replay"),
        ],
        cwd=Path(__file__).resolve().parents[5],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if done.returncode != 0:
        raise RuntimeError(done.stdout + done.stderr)
    return impl / "live"


def build(root: Path) -> Path:
    """Write the synthetic A/B under `root`; return `root`."""
    task = _task()
    ab_dir = root / "runs" / AB_ID
    arms: dict[str, Any] = {}
    for arm in ("bare", "harness"):
        (ab_dir / arm).mkdir(parents=True, exist_ok=True)
        (ab_dir / arm / "diff.patch").write_bytes(DIFFS[arm].encode("utf-8"))
        arms[arm] = {
            "spec": _spec(arm).public_dict(),
            "result": _result(arm).model_dump(mode="json", exclude={"diff_path"}),
            "diff": f"{arm}/diff.patch",
            "test_phase_files": TEST_PHASE_FILES[arm],
            "session_patches": [],
        }
        scores = root / "exports" / "scores"
        scores.mkdir(parents=True, exist_ok=True)
        (scores / f"{RUN_IDS[arm]}.json").write_text(
            json.dumps(score_record(arm), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        replay = root / "replay"
        replay.mkdir(parents=True, exist_ok=True)
        (replay / f"{arm}.json").write_text(json.dumps(REPLAY[arm], indent=2), encoding="utf-8")
    data = {
        "task": asdict(task),
        "seed": 1,
        "section": "demo-3",
        "checkpoint_sha": CHECKPOINT_SHA,
        "from_working_tree": False,
        "arms": arms,
    }
    (ab_dir / "ab.json").write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    (root / "ab-output.txt").write_text(ab_output(), encoding="utf-8")
    return root
