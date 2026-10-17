"""Tests for the live step tool (assignment/live.py) on a SYNTHETIC A/B (synthetic_live.py).

The synthetic A/B is written by hand; it is never presented as a real run. Run (repository root):
    uv run python -m pytest -q -p no:cacheprovider \
        section-3-scope-sandbox/assignment/solution/grader/tests/test_a3_live.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import synthetic_live as synth

SUBMODULE = Path(__file__).resolve().parents[4]
REPO = SUBMODULE.parent
LIVE = SUBMODULE / "assignment" / "live.py"
SOLUTION = SUBMODULE / "assignment" / "solution"
STARTER = SUBMODULE / "assignment" / "starter"


def live(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LIVE), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )


def copy_impl(source: Path, dest: Path) -> Path:
    shutil.copytree(source / "a3scope", dest / "a3scope")
    shutil.copytree(source / "tests", dest / "tests")
    return dest


def collect(impl: Path, raw: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return live(
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
        synth.COMMAND,
        "--replay-logs",
        str(raw / "replay"),
        *extra,
    )


def verify(impl: Path, tmp_path: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    out = tmp_path / "verify.json"
    done = live("verify", "--impl", str(impl), "--json", str(out))
    return done, json.loads(out.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def collected(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The reference solution with live/ collected from the synthetic A/B."""
    root = tmp_path_factory.mktemp("collected")
    raw = synth.build(root / "raw")
    impl = copy_impl(SOLUTION, root / "impl")
    done = collect(impl, raw)
    assert done.returncode == 0, done.stdout + done.stderr
    return impl


@pytest.fixture
def impl(collected: Path, tmp_path: Path) -> Path:
    """A fresh copy of the collected submission that a test may change."""
    dest = tmp_path / "impl"
    shutil.copytree(collected, dest, ignore=shutil.ignore_patterns("__pycache__"))
    return dest


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_the_fixture_is_labelled_synthetic() -> None:
    assert synth.AB_ID.startswith("synthetic-")
    assert all(run_id.startswith("synthetic-") for run_id in synth.RUN_IDS.values())
    assert synth.ab_output().startswith("SYNTHETIC FIXTURE")


def test_collect_writes_the_evidence_layout(collected: Path) -> None:
    folder = collected / "live"
    expected = {
        "command.txt",
        "ab-output.txt",
        "ab-summary.json",
        f"scores/{synth.RUN_IDS['bare']}.json",
        f"scores/{synth.RUN_IDS['harness']}.json",
        "bare/diff.patch",
        "harness/diff.patch",
        "bare/sandbox-log.json",
        "harness/sandbox-log.json",
        "verdict-bare.json",
        "verdict-harness.json",
    }
    found = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
    assert found == expected
    assert (folder / "command.txt").read_text(encoding="utf-8").strip() == synth.COMMAND
    summary = read(folder / "ab-summary.json")
    assert summary["ab_id"] == synth.AB_ID
    assert summary["checkpoint_sha"] == synth.CHECKPOINT_SHA
    assert summary["arms"]["harness"]["model"] == "gpt-6-luna"
    assert summary["arms"]["bare"]["test_phase_files"] == synth.TEST_PHASE_FILES["bare"]


def test_bare_verdict_applies_the_policy_to_the_recorded_diff(collected: Path) -> None:
    verdict = read(collected / "live" / "verdict-bare.json")
    assert verdict["schema"] == "a3-live-verdict/1"
    assert (verdict["arm"], verdict["run_id"], verdict["feature_id"]) == (
        "bare",
        synth.RUN_IDS["bare"],
        "F3",
    )
    assert verdict["policy"] == {"allowed_paths": synth.F3_ALLOWED, "state_layer": False}
    build = verdict["scope"]["build"]
    assert build["accepted"] is False
    assert build["refusals"] == [
        {"path": "app/middleware/idempotency.py", "code": "outside_allowed_paths"}
    ]
    test = verdict["scope"]["test"]
    assert test["files"] == synth.TEST_PHASE_FILES["bare"]
    assert test["refusals"] == [{"path": "app/api/issues.py", "code": "test_phase_source_edit"}]
    status = verdict["status"]
    assert status["kind"] == "status_set"
    assert status["evidence"]["visible"] == "4/4"
    assert status["evidence"]["commit"] == "b" * 40
    assert status["commands"] == [synth.VISIBLE_TESTS_COMMAND]
    assert verdict["referee"]["out_of_scope_files"] == 1
    assert verdict["referee"]["test_phase_source_edits"] == 1


def test_harness_verdict_flags_the_feature_list_and_keeps_passes_false(collected: Path) -> None:
    verdict = read(collected / "live" / "verdict-harness.json")
    assert verdict["policy"]["state_layer"] is True
    assert verdict["scope"]["build"]["refusals"] == [
        {"path": "feature_list.json", "code": "harness_only"}
    ]
    assert verdict["scope"]["test"]["accepted"] is True
    assert verdict["status"]["kind"] == "note"
    assert verdict["status"]["evidence"] is None


def test_verify_accepts_the_collected_evidence(impl: Path, tmp_path: Path) -> None:
    done, result = verify(impl, tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    assert result["present"] is True
    assert result["evidence_problems"] == []
    assert result["verdict_problems"] == []
    assert result["evidence_ok"] is True and result["verdicts_ok"] is True


def test_verify_accepts_the_assignment_purpose(impl: Path, tmp_path: Path) -> None:
    """The README's live command traces to shipharness-assignments with --purpose assignment."""
    command = synth.COMMAND + " --purpose assignment"
    assert command.endswith("--feature F3 --no-preview --purpose assignment")
    (impl / "live" / "command.txt").write_text(command + "\n", encoding="utf-8")
    done, result = verify(impl, tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    assert result["evidence_problems"] == [], result


def test_verify_reports_missing_evidence(tmp_path: Path) -> None:
    bare_impl = copy_impl(SOLUTION, tmp_path / "impl")
    done, result = verify(bare_impl, tmp_path)
    assert done.returncode == 2
    assert result["present"] is False
    assert result["evidence_ok"] is False


def _summary(edit: Callable[[dict[str, Any]], None]) -> Callable[[Path], None]:
    def apply(folder: Path) -> None:
        data = read(folder / "ab-summary.json")
        edit(data)
        write(folder / "ab-summary.json", data)

    return apply


def _score(arm: str, edit: Callable[[dict[str, Any]], None]) -> Callable[[Path], None]:
    def apply(folder: Path) -> None:
        path = folder / "scores" / f"{synth.RUN_IDS[arm]}.json"
        data = read(path)
        edit(data)
        write(path, data)

    return apply


def _text(name: str, old: str, new: str) -> Callable[[Path], None]:
    def apply(folder: Path) -> None:
        path = folder / name
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    return apply


def _remove(name: str) -> Callable[[Path], None]:
    return lambda folder: (folder / name).unlink()


MALFORMED: dict[str, tuple[Callable[[Path], None], str]] = {
    "other-model": (
        _summary(lambda d: d["arms"]["harness"].update(model="gpt-5.6-luna")),
        "gpt-6-luna",
    ),
    "recorded-run": (_score("bare", lambda d: d.update(recorded=True)), "recorded"),
    "not-sandboxed": (_score("bare", lambda d: d.update(sandboxed=False)), "sandboxed"),
    "arm-over-cap": (_score("harness", lambda d: d.update(cost_usd=0.31)), "cap"),
    "raised-cap": (
        _summary(lambda d: d["arms"]["bare"].update(cost_limit_usd=1.0)),
        "MAX_RUN_COST_USD",
    ),
    "no-checkpoint-sha": (
        _score("bare", lambda d: d.update(checkpoint_sha=None)),
        "checkpoint_sha",
    ),
    "missing-score": (_remove(f"scores/{synth.RUN_IDS['harness']}.json"), "score record"),
    "schema": (_score("bare", lambda d: d.update(model="gpt-6-luna")), "ScoreRecord"),
    "run-id-mismatch": (_score("bare", lambda d: d.update(run_id="other-run")), "run_id"),
    "other-section": (_summary(lambda d: d.update(section="demo-2")), "demo-3"),
    "other-feature": (_summary(lambda d: d.update(feature_id="F1")), "F3"),
    "one-arm": (_summary(lambda d: d["arms"].pop("bare")), "both arms"),
    "command": (_text("command.txt", "demo-3", "demo-2"), "command"),
    "command-over-cap": (_text("ab-output.txt", "Cost: $0.192", "Cost: $2.892"), "2.50"),
    "ab-id-not-in-output": (_text("ab-output.txt", synth.AB_ID, "other-ab"), "A/B"),
}


@pytest.mark.parametrize("case", sorted(MALFORMED))
def test_verify_rejects_malformed_evidence(case: str, impl: Path, tmp_path: Path) -> None:
    edit, expected = MALFORMED[case]
    edit(impl / "live")
    done, result = verify(impl, tmp_path)
    assert done.returncode == 1
    assert result["evidence_ok"] is False
    assert any(expected in problem for problem in result["evidence_problems"]), result


def test_verify_rejects_a_verdict_that_your_policy_does_not_reproduce(
    impl: Path, tmp_path: Path
) -> None:
    path = impl / "live" / "verdict-harness.json"
    data = read(path)
    data["status"]["kind"] = "status_set"
    write(path, data)
    done, result = verify(impl, tmp_path)
    assert done.returncode == 1
    assert result["evidence_ok"] is True
    assert result["verdicts_ok"] is False
    assert any("verdict-harness.json" in p for p in result["verdict_problems"])


def test_verify_rejects_a_diff_changed_after_collect(impl: Path, tmp_path: Path) -> None:
    path = impl / "live" / "bare" / "diff.patch"
    path.write_text(path.read_text(encoding="utf-8").replace("middleware", "services"), "utf-8")
    _, result = verify(impl, tmp_path)
    assert result["verdicts_ok"] is False
    assert any("sha256" in p for p in result["verdict_problems"])


def test_verify_rejects_an_unused_sandbox_result(impl: Path, tmp_path: Path) -> None:
    """A recorded test run the gate never asked for is not evidence the policy used."""
    path = impl / "live" / "harness" / "sandbox-log.json"
    data = read(path)
    write(path, data + data)
    _, result = verify(impl, tmp_path)
    assert result["verdicts_ok"] is False
    assert any("sandbox-log.json" in p for p in result["verdict_problems"])


def test_starter_code_errors_are_recorded_not_raised(tmp_path: Path) -> None:
    raw = synth.build(tmp_path / "raw")
    impl = copy_impl(STARTER, tmp_path / "impl")
    done = collect(impl, raw)
    assert done.returncode == 0, done.stdout + done.stderr
    verdict = read(impl / "live" / "verdict-bare.json")
    assert "NotImplementedError" in verdict["scope"]["build"]["error"]
    assert "NotImplementedError" in verdict["status"]["error"]


def test_collect_refuses_to_overwrite_without_force(collected: Path, tmp_path: Path) -> None:
    raw = synth.build(tmp_path / "raw")
    impl = tmp_path / "impl"
    shutil.copytree(collected, impl, ignore=shutil.ignore_patterns("__pycache__"))
    done = collect(impl, raw)
    assert done.returncode == 2
    assert "--force" in done.stdout
    assert collect(impl, raw, "--force").returncode == 0
