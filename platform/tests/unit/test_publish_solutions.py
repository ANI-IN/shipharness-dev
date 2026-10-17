"""platform/scripts/publish_solutions.py: solution folders ship; graders and hidden cases do not."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
_spec = importlib.util.spec_from_file_location(
    "publish_solutions", REPO / "platform" / "scripts" / "publish_solutions.py"
)
assert _spec and _spec.loader
ps = importlib.util.module_from_spec(_spec)
sys.modules["publish_solutions"] = ps
_spec.loader.exec_module(ps)

S1 = "01-instructions/assignment/solution"
PATHS = [
    "01-instructions/README.md",
    "01-instructions/assignment/README.md",
    f"{S1}/README.md",
    f"{S1}/AGENTS.md",
    f"{S1}/grader/check.py",
    f"{S1}/grader/tests/test_grade.py",
    f"{S1}/grader/hidden/case_1.py",
    "02-state-lifecycle/assignment/solution/README.md",
]


def test_the_target_is_the_public_course_repository() -> None:
    assert ps.PUBLIC_REPO == "ANI-IN/harness-engineering-session"


def test_the_plan_ships_the_solution_and_keeps_graders_and_hidden_cases_private() -> None:
    # Owner message 14 reverses the earlier rule: the solution folder is public.
    plan = ps.plan(PATHS, 1)
    assert plan.folder == f"{S1}/"
    assert plan.publish == [f"{S1}/AGENTS.md", f"{S1}/README.md"]
    assert plan.withheld == [
        f"{S1}/grader/check.py",
        f"{S1}/grader/hidden/case_1.py",
        f"{S1}/grader/tests/test_grade.py",
    ]


def test_unknown_or_ambiguous_assignment_is_an_error() -> None:
    with pytest.raises(ps.PublishError, match="no section folder"):
        ps.plan(PATHS, 7)
    with pytest.raises(ps.PublishError, match="no solution"):
        ps.plan(["03-scope-sandbox/README.md"], 3)


def _git(cwd: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_NAME="t",
        GIT_AUTHOR_EMAIL="t@t.invalid",
        GIT_COMMITTER_NAME="t",
        GIT_COMMITTER_EMAIL="t@t.invalid",
    )
    subprocess.run(["git", *args], cwd=cwd, capture_output=True, env=env, check=True)


def test_cli_dry_run_reports_the_rule_and_publish_refuses(tmp_path: Path) -> None:
    repo = tmp_path / "dev"
    for rel in PATHS:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("x\n", encoding="utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first")
    script = REPO / "platform" / "scripts" / "publish_solutions.py"
    args = [sys.executable, str(script), "--repo", str(repo), "--assignment", "1"]
    done = subprocess.run([*args, "--dry-run"], capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert "owner message 14" in done.stdout
    assert "ANI-IN/harness-engineering-session" in done.stdout
    assert f"public: {S1}/AGENTS.md" in done.stdout
    assert f"private: {S1}/grader/check.py" in done.stdout
    real = subprocess.run([*args, "--publish"], capture_output=True, text=True, check=False)
    assert real.returncode == 2
    assert "never pushes" in real.stderr
