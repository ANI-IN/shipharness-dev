"""Tests for the A3 self-check (assignment/check.py) and grader (solution/grader/grade.py).

Run (from the repository root):
    uv run python -m pytest -q -p no:cacheprovider submodules/03-scope-sandbox/solution/grader/tests
    (the last test is marked slow: add -m slow to run it)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SUBMODULE = Path(__file__).resolve().parents[3]
REPO = SUBMODULE.parents[1]
CHECK = SUBMODULE / "assignment" / "check.py"
GRADE = SUBMODULE / "solution" / "grader" / "grade.py"
STARTER = SUBMODULE / "assignment" / "starter"
SOLUTION = SUBMODULE / "solution"


def run(script: Path, impl: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), "--impl", str(impl), *extra],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )


def grade(impl: Path, tmp_path: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    out = tmp_path / "grade.json"
    done = run(GRADE, impl, "--json", str(out))
    return done, json.loads(out.read_text(encoding="utf-8"))


def copy_solution(tmp_path: Path) -> Path:
    impl = tmp_path / "impl"
    shutil.copytree(SOLUTION / "a3scope", impl / "a3scope")
    shutil.copytree(SOLUTION / "tests", impl / "tests")
    return impl


@pytest.fixture(scope="module")
def solution_grade(tmp_path_factory: pytest.TempPathFactory):  # type: ignore[no-untyped-def]
    return grade(SOLUTION, tmp_path_factory.mktemp("solution"))


def test_solution_scores_100_and_passes(solution_grade) -> None:  # type: ignore[no-untyped-def]
    done, result = solution_grade
    assert done.returncode == 0, done.stdout + done.stderr
    assert result["total"] == 100.0
    assert result["passed"] is True
    assert result["zero_tolerance"] == {"all_bad_rejected": True, "zero_false_positives": True}
    assert "Result: PASS" in done.stdout


def test_solution_grade_counts_hidden_cases(solution_grade) -> None:  # type: ignore[no-untyped-def]
    _, result = solution_grade
    groups = result["groups"]
    assert groups["bad"]["total"] >= 30 and groups["good"]["total"] >= 20
    assert groups["bad"]["passed"] == groups["bad"]["total"]
    assert groups["good"]["passed"] == groups["good"]["total"]


def test_starter_scores_zero_and_fails(tmp_path: Path) -> None:
    done, result = grade(STARTER, tmp_path)
    assert done.returncode == 1
    assert result["total"] == 0.0
    assert result["passed"] is False
    assert "Result: FAIL" in done.stdout


def test_a_denial_test_that_ignores_the_rule_loses_the_mutation_points(tmp_path: Path) -> None:
    impl = copy_solution(tmp_path)
    (impl / "tests" / "test_a3_sandbox_rule.py").write_text(
        "from shipharness.sandbox import check_command\n"
        "from a3scope.policy import policy\n\n\n"
        "def test_status_runs() -> None:\n"
        "    assert check_command(policy(), 'git status') is None\n",
        encoding="utf-8",
    )
    _, result = grade(impl, tmp_path)
    proof = result["criteria"]["proof"]
    assert proof["checks"] == {
        "passes": True,
        "fails_without_rule": False,
        "uses_policy_code": True,
    }
    assert result["total"] == 96.0


def test_rejecting_every_diff_earns_no_scope_points(tmp_path: Path) -> None:
    impl = copy_solution(tmp_path)
    scope = impl / "a3scope" / "scope.py"
    scope.write_text(
        scope.read_text(encoding="utf-8") + "\n\n_real = check_diff\n\n\n"
        "def check_diff(policy, phase, diff):  # noqa: F811\n"
        "    return ScopeVerdict(phase, (Refusal('x', 'outside_allowed_paths', 'x'),))\n",
        encoding="utf-8",
    )
    _, result = grade(impl, tmp_path)
    assert result["groups"]["good"]["passed"] == 0
    assert result["criteria"]["scope"]["points"] == 0.0
    assert result["zero_tolerance"]["zero_false_positives"] is False
    assert result["passed"] is False


def test_importing_the_real_guard_zeroes_parsing_and_scope(tmp_path: Path) -> None:
    impl = copy_solution(tmp_path)
    scope = impl / "a3scope" / "scope.py"
    scope.write_text(
        "from shipharness.harness.scope.guard import glob_matches as _unused  # noqa: F401\n"
        + scope.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    _, result = grade(impl, tmp_path)
    assert result["criteria"]["parse"]["points"] == 0.0
    assert result["criteria"]["scope"]["points"] == 0.0
    assert "shipharness.harness.scope.guard" in " ".join(result["forbidden_imports"])
    assert result["criteria"]["status"]["points"] == 20.0


def test_check_fails_clearly_on_the_starter() -> None:
    done = run(CHECK, STARTER)
    assert done.returncode == 1
    assert "Self-check FAILED" in done.stdout
    assert "TODO(A3 Part A1)" in done.stdout  # the markers left are listed
    assert "a3scope/diffparse.py" in done.stdout


def test_check_passes_on_the_solution() -> None:
    done = run(CHECK, SOLUTION)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "Self-check PASSED" in done.stdout


@pytest.mark.slow
def test_hidden_diffs_are_reproducible(tmp_path: Path) -> None:
    """make_hidden.py regenerates exactly the committed diffs (git output is deterministic)."""
    hidden = SUBMODULE / "solution" / "grader" / "hidden"
    work = tmp_path / "hidden"
    shutil.copytree(hidden, work, ignore=shutil.ignore_patterns("__pycache__"))
    script = work / "make_hidden.py"
    text = script.read_text(encoding="utf-8").replace(
        "HERE.parents[2]", repr(str(SUBMODULE)).join(("Path(", ")"))
    )
    script.write_text(text, encoding="utf-8")
    subprocess.run([sys.executable, str(script)], cwd=REPO, check=True, capture_output=True)
    for diff in sorted((hidden / "diffs").glob("*.diff")):
        assert (work / "diffs" / diff.name).read_bytes() == diff.read_bytes(), diff.name
    assert (work / "cases.json").read_bytes() == (hidden / "cases.json").read_bytes()
