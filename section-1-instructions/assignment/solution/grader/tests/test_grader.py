"""Tests for the A1 grader (solution/grader/grade.py) and its hidden checker cases.

Run:
    uv run python -m pytest -q -p no:cacheprovider \\
        section-1-instructions/assignment/solution/grader/tests
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import synthetic_live as syn
from helpers import A1, GRADER, SOLUTION_WORK, STARTER, load

grade = load("a1_grade", GRADER / "grade.py")
REFERENCE = SOLUTION_WORK / "checker" / "check_docs.py"
STARTER_CHECKER = STARTER / "checker" / "check_docs.py"


def points(items: list, criterion: str | None = None) -> float:
    return round(sum(i.earned for i in items if criterion is None or i.criterion == criterion), 6)


# -- hidden checker cases -------------------------------------------------------------------------


@pytest.mark.parametrize("case", grade.CASES, ids=lambda c: c.name)
def test_every_hidden_case_passes_on_the_reference_checker(case, tmp_path: Path) -> None:
    outcome = grade.run_case(REFERENCE, case, tmp_path)
    assert outcome.passed, outcome.detail


@pytest.mark.parametrize("case", [c for c in grade.CASES if c.exit_code == 1], ids=lambda c: c.name)
def test_every_problem_case_fails_on_the_starter_checker(case, tmp_path: Path) -> None:
    assert not grade.run_case(STARTER_CHECKER, case, tmp_path).passed


# -- whole grades ---------------------------------------------------------------------------------


def test_the_criteria_total_100_points() -> None:
    assert sum(grade.CRITERIA.values()) == 100
    items = grade.grade(SOLUTION_WORK, allow_pending=True)
    for criterion, total in grade.CRITERIA.items():
        assert sum(i.points for i in items if i.criterion == criterion) == pytest.approx(total)


@pytest.mark.parametrize("allow_pending", [False, True])
def test_the_captured_reference_scores_100(allow_pending: bool) -> None:
    # The reference holds the real live evidence of batch a1-reference (captured 2026-10-17) and
    # no pending markers, so --allow-pending changes nothing.
    items = grade.grade(SOLUTION_WORK, allow_pending=allow_pending)
    assert {i.name for i in items if i.earned < i.points} == set()
    assert points(items, "F Live run evidence") == 12
    assert points(items) == 100


def test_the_starter_scores_low_without_crashing() -> None:
    items = grade.grade(STARTER)
    assert points(items) < 10
    assert points(items, "D Docs checker") < 5


def test_a_modified_original_zeroes_rule_coverage(tmp_path: Path) -> None:
    original = tmp_path / "AGENTS.md"
    text = grade.ORIGINAL.read_text(encoding="utf-8")
    original.write_text(text.replace("[CV-12]", "[CV-12] (retired 2026-01)"), encoding="utf-8")
    items = grade.grade(SOLUTION_WORK, allow_pending=True, original=original)
    assert points(items, "B Rule coverage") == 0
    assert any("modified" in i.note for i in items if i.name == "original-unchanged")


def test_an_untagged_rule_costs_coverage_and_the_checker_must_say_so(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(SOLUTION_WORK, work)
    doc = work / "instructions" / "docs" / "RELIABILITY.md"
    doc.write_text(doc.read_text(encoding="utf-8").replace("[R4.3]", "R4.3"), encoding="utf-8")
    items = {i.name: i for i in grade.grade(work, allow_pending=True)}
    assert items["coverage"].earned == pytest.approx(12 * 65 / 66)
    assert items["checker-clean"].earned == 0


def test_a_checker_that_reports_nothing_earns_no_reference_tree_points(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(SOLUTION_WORK, work)
    shutil.copy(STARTER_CHECKER, work / "checker" / "check_docs.py")
    items = {i.name: i for i in grade.grade(work, allow_pending=True)}
    assert items["reference-tree"].earned == 0
    assert items["hidden-cases"].earned < 2
    assert items["pristine-visible-tests"].earned < 2


def test_main_prints_each_criterion_and_the_score(capsys: pytest.CaptureFixture[str]) -> None:
    assert grade.main(["--work", str(SOLUTION_WORK), "--allow-pending"]) == 0
    out = capsys.readouterr().out
    for criterion in grade.CRITERIA:
        assert criterion in out
    assert out.strip().splitlines()[-1] == "Score: 100.0/100"


def test_min_score_turns_a_low_score_into_exit_1() -> None:
    assert grade.main(["--work", str(STARTER), "--min-score", "50"]) == 1


# -- the live step --------------------------------------------------------------------------------

live = load("a1_live", A1 / "assignment" / "live_evidence.py")


def synthetic_submission(root: Path) -> Path:
    """The reference work folder plus SYNTHETIC live evidence (never a real run) and a report
    whose values match it."""
    work = root / "work"
    shutil.copytree(SOLUTION_WORK, work, ignore=shutil.ignore_patterns("__pycache__", "live"))
    placed = live.tree_files(work / "instructions")
    summary = syn.write_live(work, sorted(live.section_tasks()), placed, r1_fail={"bare": 3})
    text = syn.report(summary, r1=("3/24", "0/24"), r3=("0/24", "0/24"), runs=24)
    (work / "ab-report.md").write_text(text, encoding="utf-8")
    return work


def test_live_evidence_is_its_own_criterion_of_12_points() -> None:
    assert grade.CRITERIA["F Live run evidence"] == 12


def test_a_submission_with_valid_live_evidence_scores_100_without_pending(tmp_path: Path) -> None:
    items = grade.grade(synthetic_submission(tmp_path))
    assert [(i.name, i.note) for i in items if i.earned < i.points] == []
    assert points(items) == 100


def test_missing_live_evidence_fails_the_live_criterion_by_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    work = synthetic_submission(tmp_path)
    shutil.rmtree(work / "live")
    items = grade.grade(work)
    assert points(items, "F Live run evidence") == 0
    assert points(items) == 88
    grade.main(["--work", str(work)])
    out = capsys.readouterr().out
    assert any(
        line.startswith("F Live run evidence") and "0.0/12" in line for line in out.splitlines()
    )


def test_a_repository_checkout_is_accepted_as_the_submission(tmp_path: Path) -> None:
    work = synthetic_submission(tmp_path)
    checkout = tmp_path / "learner-repo"
    starter = checkout / "section-1-instructions" / "assignment" / "starter"
    shutil.copytree(work, starter)
    assert grade.resolve_work(checkout) == starter
    assert grade.resolve_work(work) == work
    assert grade.main(["--work", str(checkout), "--min-score", "100"]) == 0
