"""Hidden grader tests: the reference solution scores 100 with live evidence, the starter and the
class's S2 layer do not, and the self-check and grader commands report what they should.

The live evidence in these tests is a SYNTHETIC TEST FIXTURE (assignment/tests/a2_live_fixture.py),
never a real run; the captured live run of the reference solution is recorded separately.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType

import pytest

GRADER = Path(__file__).resolve().parents[1]
SOLUTION = GRADER.parent
ASSIGNMENT = SOLUTION.parent  # solution/ sits inside assignment/
sys.path.insert(0, str(ASSIGNMENT))
sys.path.insert(0, str(GRADER))


def load(name: str, path: Path) -> ModuleType:
    """Import a script under a unique name (other assignments also have check.py and grade.py)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


grade = load("a2_grade", GRADER / "grade.py")
check = load("a2_check", ASSIGNMENT / "check.py")
fixture = load("a2_live_fixture", ASSIGNMENT / "tests" / "a2_live_fixture.py")

from a2_hidden import HIDDEN  # noqa: E402
from a2_scenario.scenarios import VISIBLE  # noqa: E402

from shipharness.harness.state.layer import StateLayer  # noqa: E402


def test_hidden_scenarios_force_three_stops_and_differ_from_the_visible_ones() -> None:
    assert len(HIDDEN) == 4
    assert all(len(s.budgets) == 4 for s in (*VISIBLE, *HIDDEN))
    assert {s.budgets for s in HIDDEN}.isdisjoint({s.budgets for s in VISIBLE})
    assert {s.feature.id for s in HIDDEN} == {"comments", "labels"}


def _submission(tmp_path: Path) -> Path:
    """The reference layer plus SYNTHETIC live evidence, as a learner's submission folder."""
    folder = tmp_path / "submission"
    shutil.copytree(SOLUTION / "a2_state", folder / "a2_state")
    fixture.write_evidence(folder, tmp_path / "work")
    return folder


def test_the_solution_scores_100_with_valid_live_evidence(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_json = tmp_path / "grade.json"
    folder = _submission(tmp_path)
    code = grade.main(["--impl", str(folder), "--json", str(out_json), "--fail-under", "100"])
    printed = capsys.readouterr().out
    assert code == 0, printed
    assert "Score: 100.0/100" in printed
    assert "test stand-in agent" in printed
    assert "Live run evidence: valid" in printed and fixture.AB_ID in printed
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["score"] == 100.0
    assert data["points"]["live_run"] == 10
    assert data["live"] == {"valid": True, "problems": []}
    assert [s["name"] for s in data["scenarios"]] == [s.name for s in (*VISIBLE, *HIDDEN)]
    assert all(s["passed"] for s in data["scenarios"])


def test_missing_live_evidence_fails_the_live_criterion(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = grade.main(["--impl", str(SOLUTION), "--fail-under", "100"])
    printed = capsys.readouterr().out
    assert code == 1
    assert "Score: 90.0/100" in printed
    assert "Live run evidence: not valid" in printed and "live/: missing task.jsonl" in printed


def test_live_evidence_of_another_layer_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    folder = _submission(tmp_path)
    ledger = folder / "a2_state" / "ledger.py"
    ledger.write_text(ledger.read_text(encoding="utf-8") + "\n# edited after the run\n", "utf-8")
    grade.main(["--impl", str(folder), "--visible-only"])
    printed = capsys.readouterr().out
    assert "the run's layer differs from the submitted a2_state/" in printed


def test_the_grader_finds_the_submission_in_a_cloned_repo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    folder = _submission(tmp_path)
    repo = tmp_path / "repo"
    shutil.copytree(
        ASSIGNMENT / "starter", repo / "section-2-state-lifecycle" / "assignment" / "starter"
    )
    shutil.copytree(folder, repo / "my-a2")
    assert grade.main(["--impl", str(repo), "--visible-only"]) == 0
    printed = capsys.readouterr().out
    assert "against my-a2" in printed
    assert "Live run evidence: valid" in printed


def test_the_starter_runs_and_scores_low(tmp_path: Path) -> None:
    factory = grade.load_layer(ASSIGNMENT / "starter")
    report = grade.grade(factory, (*VISIBLE, *HIDDEN), tmp_path)
    assert not any(r.error for r in report.results)  # it runs without errors
    assert report.score < 15
    assert report.points["one_head"] == 0
    assert report.points["no_duplicate_table"] == 0
    assert report.points["no_redone_lines"] < 3


def test_the_class_s2_layer_is_not_enough(tmp_path: Path) -> None:
    report = grade.grade(lambda **kw: StateLayer(**kw), (*VISIBLE, *HIDDEN), tmp_path)
    assert report.score < 60
    assert report.points["no_duplicate_table"] == 0  # it redoes S1: no step ledger
    # it logs every session, but loses the log when the agent rewrites progress.md (H3)
    assert 0 < report.points["session_log"] < 8
    h3 = next(r for r in report.results if r.scenario.name.startswith("H3"))
    assert next(o for o in h3.outcomes if o.key == "session_log").fraction == 0


def test_fail_under_sets_the_exit_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = grade.main(
        ["--impl", str(ASSIGNMENT / "starter"), "--visible-only", "--fail-under", "50"]
    )
    assert code == 1
    assert "Score:" in capsys.readouterr().out


def test_the_self_check_fails_on_the_starter_and_passes_on_the_solution(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert check.main(["--impl", str(ASSIGNMENT / "starter")]) == 1
    starter_out = capsys.readouterr().out
    assert "FAIL no_duplicate_table" in starter_out and "[REDO: S1" in starter_out
    assert "hint:" in starter_out
    assert "test stand-in agent" in starter_out and "not a model" in starter_out
    assert "Live evidence (graded, 10 points): not found" in starter_out
    assert check.main(["--impl", str(SOLUTION)]) == 0
    assert "Self-check: 28 of 28 checks pass." in capsys.readouterr().out
