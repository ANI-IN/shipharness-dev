"""scripts/publish_solutions.py: what one assignment's solution release would contain."""

from __future__ import annotations

import datetime as dt
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "publish_solutions", REPO / "scripts" / "publish_solutions.py"
)
assert _spec and _spec.loader
ps = importlib.util.module_from_spec(_spec)
sys.modules["publish_solutions"] = ps
_spec.loader.exec_module(ps)

PATHS = [
    "submodules/01-instructions/README.md",
    "submodules/01-instructions/assignment/README.md",
    "submodules/01-instructions/solution/README.md",
    "submodules/01-instructions/solution/AGENTS.md",
    "submodules/01-instructions/solution/grader/check.py",
    "submodules/01-instructions/solution/grader/hidden/case_1.py",
    "submodules/01-instructions/solution/grader/hidden/data/case_1.json",
    "submodules/01-instructions/solution/cases/hidden_cases.jsonl",
    "submodules/01-instructions/solution/cases/visible_cases.jsonl",
    "submodules/02-state-lifecycle/solution/README.md",
]


def test_the_plan_publishes_the_solution_folder_without_hidden_cases() -> None:
    plan = ps.plan(PATHS, 1, dt.date(2026, 11, 3))
    assert plan.folder == "submodules/01-instructions/solution/"
    assert plan.publish == [
        "submodules/01-instructions/solution/AGENTS.md",
        "submodules/01-instructions/solution/README.md",
        "submodules/01-instructions/solution/cases/visible_cases.jsonl",
        "submodules/01-instructions/solution/grader/check.py",
    ]
    assert plan.withheld == [
        "submodules/01-instructions/solution/cases/hidden_cases.jsonl",
        "submodules/01-instructions/solution/grader/hidden/case_1.py",
        "submodules/01-instructions/solution/grader/hidden/data/case_1.json",
    ]
    assert plan.tag == "solutions-a1-2026-11-03"


def test_tag_name() -> None:
    assert ps.tag_name(4, dt.date(2026, 12, 1)) == "solutions-a4-2026-12-01"


@pytest.mark.parametrize(
    ("rel", "hidden"),
    [
        ("grader/hidden/case.py", True),
        ("hidden/x.json", True),
        ("cases/hidden_cases.jsonl", True),
        ("cases/hidden-cases/a.json", True),
        ("grader/check.py", False),
        ("README.md", False),
        ("notes/unhidden.md", False),
    ],
)
def test_hidden_case_data(rel: str, hidden: bool) -> None:
    assert ps.is_hidden_case(rel) is hidden


def test_unknown_or_ambiguous_assignment_is_an_error() -> None:
    with pytest.raises(ps.PublishError, match="no submodule"):
        ps.plan(PATHS, 7, dt.date(2026, 11, 3))
    with pytest.raises(ps.PublishError, match="no solution"):
        ps.plan(["submodules/03-scope-sandbox/README.md"], 3, dt.date(2026, 11, 3))


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


def test_cli_dry_run_prints_the_plan_and_publishes_nothing(tmp_path: Path) -> None:
    repo = tmp_path / "dev"
    for rel in PATHS:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("x\n", encoding="utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first")
    script = REPO / "scripts" / "publish_solutions.py"
    args = [sys.executable, str(script), "--repo", str(repo), "--assignment", "1"]
    done = subprocess.run(
        [*args, "--dry-run", "--date", "2026-11-03"], capture_output=True, text=True, check=False
    )
    assert done.returncode == 0, done.stderr
    assert "solutions-a1-2026-11-03" in done.stdout
    assert "submodules/01-instructions/solution/AGENTS.md" in done.stdout
    assert "withheld: submodules/01-instructions/solution/grader/hidden/case_1.py" in done.stdout
    real = subprocess.run([*args, "--publish"], capture_output=True, text=True, check=False)
    assert real.returncode == 2
    assert "not implemented" in real.stderr
