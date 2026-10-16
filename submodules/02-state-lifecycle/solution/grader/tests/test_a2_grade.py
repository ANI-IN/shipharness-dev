"""Hidden grader tests: the reference solution scores 100, the starter and the class's S2 layer do
not, and the self-check and grader commands report what they should."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

GRADER = Path(__file__).resolve().parents[1]
SOLUTION = GRADER.parent
ASSIGNMENT = SOLUTION.parent / "assignment"
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

from a2_hidden import HIDDEN  # noqa: E402
from a2_scenario.scenarios import VISIBLE  # noqa: E402

from shipharness.harness.state.layer import StateLayer  # noqa: E402


def test_hidden_scenarios_force_three_stops_and_differ_from_the_visible_ones() -> None:
    assert len(HIDDEN) == 4
    assert all(len(s.budgets) == 4 for s in (*VISIBLE, *HIDDEN))
    assert {s.budgets for s in HIDDEN}.isdisjoint({s.budgets for s in VISIBLE})
    assert {s.feature.id for s in HIDDEN} == {"comments", "labels"}


def test_the_solution_scores_100_on_visible_and_hidden_scenarios(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_json = tmp_path / "grade.json"
    code = grade.main(["--impl", str(SOLUTION), "--json", str(out_json), "--fail-under", "100"])
    printed = capsys.readouterr().out
    assert code == 0, printed
    assert "Score: 100.0/100" in printed
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["score"] == 100.0
    assert [s["name"] for s in data["scenarios"]] == [s.name for s in (*VISIBLE, *HIDDEN)]
    assert all(s["passed"] for s in data["scenarios"])


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
    assert 0 < report.points["session_log"] < 10
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
    assert check.main(["--impl", str(SOLUTION)]) == 0
    assert "Self-check: 28 of 28 checks pass." in capsys.readouterr().out
