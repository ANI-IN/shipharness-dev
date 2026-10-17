"""Tests for the A4 grader and self-check (scoring, criteria coverage, and end-to-end runs)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

GRADER = Path(__file__).resolve().parents[1]
SOLUTION = GRADER.parent
ASSIGNMENT = SOLUTION.parent  # solution/ sits inside assignment/
MODULE = ASSIGNMENT.parent
VISIBLE = ASSIGNMENT / "visible_tests"
HIDDEN = GRADER / "hidden_tests"
sys.path[:0] = [str(GRADER), str(VISIBLE)]

import grade  # noqa: E402
from a4_runner import Outcome  # noqa: E402


def _ids_used() -> set[str]:
    used: set[str] = set()
    for folder in (VISIBLE, HIDDEN):
        for path in folder.glob("test_*.py"):
            used |= set(re.findall(r'criterion\("([^"]+)"\)', path.read_text(encoding="utf-8")))
    return used


def test_criteria_add_up_to_100_points() -> None:
    assert sum(c.points for c in grade.CRITERIA) == 100
    assert len({c.id for c in grade.CRITERIA}) == len(grade.CRITERIA)


def test_every_criterion_has_tests_and_every_test_has_a_criterion() -> None:
    ids = {c.id for c in grade.CRITERIA}
    assert _ids_used() == ids


def test_points_split_evenly_over_a_criterion_tests() -> None:
    criterion = grade.CRITERIA[0]
    outcomes = [
        Outcome(f"t.py::test_{n}", criterion.id, passed)
        for n, passed in enumerate([True, True, False])
    ]
    (first, *rest) = grade.score(outcomes)
    assert first.criterion == criterion
    assert (first.passed, first.total) == (2, 3)
    assert first.earned == pytest.approx(criterion.points * 2 / 3)
    assert all(s.earned == 0 and s.total == 0 for s in rest)


def test_live_evidence_is_a_named_criterion_worth_10_points() -> None:
    points = {c.id: c.points for c in grade.CRITERIA}
    assert points["live-evidence"] == 10


def test_submission_path_may_be_the_impl_folder_or_a_course_repo_root(tmp_path: Path) -> None:
    impl = tmp_path / "04-verification" / "assignment" / "starter"
    (impl / "a4_verification").mkdir(parents=True)
    assert grade.resolve_impl(tmp_path) == impl.resolve()
    assert grade.resolve_impl(impl) == impl.resolve()
    other = tmp_path / "elsewhere"
    other.mkdir()
    assert grade.resolve_impl(other) == other.resolve()


def test_unknown_criterion_is_reported_as_a_grader_error() -> None:
    with pytest.raises(ValueError, match="no-such"):
        grade.score([Outcome("t.py::test_x", "no-such", True)])


def test_report_names_failed_tests_and_the_total() -> None:
    criterion = grade.CRITERIA[0]
    outcomes = [
        Outcome("t.py::test_ok", criterion.id, True),
        Outcome("t.py::test_bad", criterion.id, False, "AssertionError: nope"),
    ]
    text = grade.format_report(grade.score(outcomes), outcomes, Path("impl"))
    assert "FAIL test_bad: AssertionError: nope" in text
    assert re.search(r"Score: \d+(\.\d)?/100", text)


def _run(script: Path, impl: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), "--impl", str(impl)],
        capture_output=True,
        text=True,
        timeout=1800,
    )


def test_grade_reference_solution_scores_100_on_its_captured_run() -> None:
    # No criterion rests on a [[PENDING]] marker: live/ and portfolio/ hold the real run.
    run = _run(GRADER / "grade.py", SOLUTION)
    assert run.returncode == 0, run.stdout[-3000:] + run.stderr[-3000:]
    assert "Score: 100/100" in run.stdout, run.stdout[-3000:]
    assert "FAIL" not in run.stdout, run.stdout[-3000:]


def test_grade_starter_scores_low() -> None:
    run = _run(GRADER / "grade.py", ASSIGNMENT / "starter")
    assert run.returncode == 0, run.stdout[-3000:] + run.stderr[-3000:]
    total = float(re.search(r"Score: ([\d.]+)/100", run.stdout).group(1))  # type: ignore[union-attr]
    assert total < 10, run.stdout[-3000:]


def test_self_check_fails_on_the_starter_and_names_the_todos() -> None:
    run = _run(ASSIGNMENT / "check.py", ASSIGNMENT / "starter")
    assert run.returncode == 1, run.stdout[-3000:]
    assert "FAIL" in run.stdout
    assert "TODO(A4-1)" in run.stdout
    assert "self-check: FAILED" in run.stdout


def test_self_check_passes_on_the_solution() -> None:
    run = _run(ASSIGNMENT / "check.py", SOLUTION)
    assert run.returncode == 0, run.stdout[-3000:] + run.stderr[-3000:]
    assert "self-check: PASSED" in run.stdout
    assert "FAIL" not in run.stdout, run.stdout[-3000:]
