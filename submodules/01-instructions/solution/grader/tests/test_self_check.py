"""Tests for the A1 self-check (submodules/01-instructions/assignment/check.py).

Run: uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/grader/tests
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from helpers import A1, SOLUTION_WORK, STARTER, load, write

check = load("a1_check", A1 / "assignment" / "check.py")

VALID_REPORT = """# A1 A/B report

## Setup

- Command: `uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1`
- Instructions tree commit: 1a2b3c4d
- Runs per arm: 24

## Results

| Measure | Bare arm (runs failing of N) | Harness arm (runs failing of N) |
|---|---|---|
| R1: runs with at least one new R1 violation | 9/24 | 2/24 |
| R3: runs with at least one new R3 failure | 5/24 | 1/24 |

## Links

- Bare experiment: https://smith.langchain.com/o/1/datasets/2/compare?selectedSessions=a
- Harness experiment: https://smith.langchain.com/o/1/datasets/2/compare?selectedSessions=b

## Cost and traces

- Cost: $1.92
- Traces: 96

## Reading the result

The harness arm failed R1 in fewer runs than the bare arm, and R3 in fewer runs as well. The
difference is largest on the trap task, where the legacy handler sits next to the right pattern.
Both arms read the same facts; only the organisation differs, so the drop in R1 failures is the
effect of the map and the skill being in context, not of new information. The control task passed
in both arms.

## Limits

Three runs per task is a small sample, one model and one effort level were used, and the referee
checks only what the house-rule probes cover, so other mistakes are not counted here.
"""

PENDING = (
    "[[PENDING: A/B counts for the reference tree | source: M8 batch 1 | how: uv run shipharness "
    "experiments --split section-1 --k 3 --layers instructions --batch a1-reference]]"
)


def by_name(results: list) -> dict:
    return {r.name: r for r in results}


# -- whole runs -----------------------------------------------------------------------------------


def test_the_starter_fails_with_one_line_per_check(capsys: pytest.CaptureFixture[str]) -> None:
    results = by_name(check.run_checks(STARTER))
    for name in ("layout", "map-length", "skill-valid", "checker-tests", "report-results", "todo"):
        assert not results[name].ok, name
    assert check.main(["--work", str(STARTER)]) == 1
    out = capsys.readouterr().out
    assert "FAIL layout:" in out
    assert out.strip().splitlines()[-1].startswith("self-check: ")


def test_the_reference_solution_passes_every_check_when_pending_markers_are_allowed(
    capsys: pytest.CaptureFixture[str],
) -> None:
    results = check.run_checks(SOLUTION_WORK, allow_pending=True)
    assert [r.name for r in results if not r.ok] == []
    assert check.main(["--work", str(SOLUTION_WORK), "--allow-pending"]) == 0
    assert "FAIL" not in capsys.readouterr().out


def test_the_self_check_lists_the_five_live_items(capsys: pytest.CaptureFixture[str]) -> None:
    names = [r.name for r in check.run_checks(STARTER)]
    for name in ("live-files", "live-command", "live-caps", "live-tree", "live-report"):
        assert name in names
    assert len(names) == 24


def test_learner_facing_files_never_point_into_the_solution_folder() -> None:
    assignment = A1 / "assignment"
    files = [p for p in assignment.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "solution/" not in text, path.relative_to(A1).as_posix()


def test_the_self_check_runs_in_a_learner_repository_without_solution(tmp_path: Path) -> None:
    repo = A1.parents[1]
    copy = tmp_path / "repo"
    shutil.copytree(
        A1 / "assignment",
        copy / "submodules" / "01-instructions" / "assignment",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    for name in ("teamtrack", "datasets", "skills"):
        (copy / name).symlink_to(repo / name, target_is_directory=True)
    script = copy / "submodules" / "01-instructions" / "assignment" / "check.py"
    run = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, timeout=600, cwd=copy
    )
    assert not (copy / "submodules" / "01-instructions" / "solution").exists()
    assert "Traceback" not in run.stderr, run.stderr
    assert run.returncode == 1
    assert run.stdout.strip().splitlines()[-1] == "self-check: 0 of 24 checks pass"


def test_pending_markers_do_not_count_as_results_by_default() -> None:
    results = by_name(check.run_checks(SOLUTION_WORK))
    assert not results["report-results"].ok


# -- the report -----------------------------------------------------------------------------------


def report(tmp_path: Path, text: str, allow_pending: bool = False) -> dict:
    path = tmp_path / "ab-report.md"
    path.write_text(text, encoding="utf-8")
    return by_name(check.check_report(path, allow_pending=allow_pending))


def test_a_complete_report_passes(tmp_path: Path) -> None:
    assert [n for n, r in report(tmp_path, VALID_REPORT).items() if not r.ok] == []


@pytest.mark.parametrize(
    ("change", "failing"),
    [
        (("9/24 | 2/24", "37% | 8%"), "report-results"),
        (("5/24 | 1/24", "5/12 | 1/12"), "report-results"),
        (("9/24 | 2/24", "25/24 | 2/24"), "report-results"),
        (("--k 3", "--k 2"), "report-command"),
        (("--layers instructions", "--layers all"), "report-command"),
        (
            ("Instructions tree commit: 1a2b3c4d", "Instructions tree commit: soon"),
            "report-command",
        ),
        (("Cost: $1.92", "Cost: $3.10"), "report-cost"),
        (("Traces: 96", "Traces: 200"), "report-cost"),
        (("selectedSessions=b", "selectedSessions=a"), "report-links"),
        (("## Limits", "## Caveats"), "report-sections"),
        (("Both arms read", "TODO: Both arms read"), "report-sections"),
        (
            (
                "## Reading the result\n\nThe harness",
                "## Reading the result\n\nShort.\n\n## Notes\n\nThe harness",
            ),
            "report-reading",
        ),
    ],
)
def test_report_problems_are_caught(tmp_path: Path, change: tuple[str, str], failing: str) -> None:
    assert change[0] in VALID_REPORT
    results = report(tmp_path, VALID_REPORT.replace(*change))
    assert not results[failing].ok


def test_a_pending_marker_stands_in_for_values_only_when_allowed(tmp_path: Path) -> None:
    text = (
        VALID_REPORT.replace("| 9/24 | 2/24 |", "| pending | pending |")
        .replace("| 5/24 | 1/24 |", "| pending | pending |")
        .replace("## Links", PENDING + "\n\n## Links")
    )
    assert not report(tmp_path, text)["report-results"].ok
    assert report(tmp_path, text, allow_pending=True)["report-results"].ok
    malformed = text.replace("source: M8 batch 1", "source: soon")
    assert not report(tmp_path, malformed, allow_pending=True)["report-results"].ok


# -- the tree -------------------------------------------------------------------------------------


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    target = tmp_path / "instructions"
    shutil.copytree(SOLUTION_WORK / "instructions", target)
    return target


def tree_checks(tree: Path) -> dict:
    return by_name(check.check_tree(tree, check.PRODUCT, check.ORIGINAL))


def test_the_reference_tree_passes_the_tree_checks(tree: Path) -> None:
    assert [n for n, r in tree_checks(tree).items() if not r.ok] == []


def test_a_document_the_map_cannot_reach_is_an_orphan(tree: Path) -> None:
    write(tree, {"docs/design-docs/orphan.md": "# Nobody links here\n"})
    result = tree_checks(tree)["map-reach"]
    assert not result.ok and "docs/design-docs/orphan.md" in result.detail


def test_a_map_over_120_lines_fails(tree: Path) -> None:
    text = (tree / "AGENTS.md").read_text(encoding="utf-8")
    write(tree, {"AGENTS.md": text + "\nfiller\n" * 30})
    assert not tree_checks(tree)["map-length"].ok


def test_a_tree_file_that_would_overwrite_a_product_file_fails(tree: Path) -> None:
    write(tree, {"docs/HANDBOOK.md": "# Mine now\n"})
    result = tree_checks(tree)["no-overwrite"]
    assert not result.ok and "docs/HANDBOOK.md" in result.detail


def test_a_code_span_that_is_neither_in_the_original_nor_a_path_is_a_new_fact(tree: Path) -> None:
    extra = "\nUse `make_tenant_safe()` and `app/api/deps.py` and `require_writer`.\n"
    write(tree, {"docs/PLANS.md": (tree / "docs/PLANS.md").read_text(encoding="utf-8") + extra})
    result = tree_checks(tree)["no-new-facts"]
    assert not result.ok
    assert "make_tenant_safe()" in result.detail
    assert result.score == pytest.approx(2 / 3)  # one of three points off per unknown span
    assert "require_writer" not in result.detail and "deps.py" not in result.detail


def test_a_missing_layout_file_is_named(tree: Path) -> None:
    (tree / "docs/PLANS.md").unlink()
    result = tree_checks(tree)["layout"]
    assert not result.ok and "docs/PLANS.md" in result.detail


# -- the skill ------------------------------------------------------------------------------------


def test_an_unchanged_copy_of_the_template_fails_the_skill_checks(tree: Path) -> None:
    shutil.rmtree(tree / ".agents" / "skills" / "add-list-endpoint")
    template = check.REPO / "skills" / "skill-template"
    shutil.copytree(template, tree / ".agents" / "skills" / "skill-template")
    results = by_name(check.check_skill(tree))
    assert not results["skill-frontmatter"].ok
    assert not results["skill-sections"].ok
    assert not results["skill-linked"].ok


def test_two_skills_fail_the_one_skill_rule(tree: Path) -> None:
    shutil.copytree(tree / ".agents/skills/add-list-endpoint", tree / ".agents/skills/second-skill")
    assert not by_name(check.check_skill(tree))["skill-valid"].ok


# -- leftovers ------------------------------------------------------------------------------------


def test_todo_markers_left_in_the_work_fail(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(SOLUTION_WORK, work)
    assert check.check_todos(work).ok
    write(work, {"instructions/docs/PLANS.md": "# Plans\nTODO(A1-1): finish\n"})
    result = check.check_todos(work)
    assert not result.ok and "instructions/docs/PLANS.md" in result.detail
