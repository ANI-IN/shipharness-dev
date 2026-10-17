"""`make grade-assignment-N SUBMISSION=<folder or git URL>` (instructor, build repository only)."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
_spec = importlib.util.spec_from_file_location(
    "grade_assignment", REPO / "platform" / "scripts" / "grade_assignment.py"
)
assert _spec and _spec.loader
ga = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ga)


@pytest.mark.parametrize(
    ("value", "url"),
    [
        ("https://github.com/someone/a1.git", True),
        ("git@github.com:someone/a1.git", True),
        ("ssh://git@host/a1", True),
        ("file:///tmp/a1.git", True),
        ("my-a1", False),
        ("/home/me/work", False),
    ],
)
def test_git_urls_are_told_apart_from_folders(value: str, url: bool) -> None:
    assert ga.is_git_url(value) is url


def test_each_grader_gets_its_submission_flag() -> None:
    for n, flag in ((1, "--work"), (2, "--impl"), (3, "--impl"), (4, "--impl")):
        cmd = ga.grader_command(n, Path("/tmp/sub"))
        assert cmd[-2:] == [flag, "/tmp/sub"]
        assert cmd[1].endswith("solution/grader/grade.py") and f"0{n}-" in cmd[1]


def test_a_local_folder_is_used_in_place(tmp_path: Path) -> None:
    work = tmp_path / "my-a1"
    work.mkdir()
    assert ga.resolve_submission(str(work), tmp_path / "clone") == work.resolve()


def test_a_missing_folder_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ga.SubmissionError, match="not found"):
        ga.resolve_submission(str(tmp_path / "nope"), tmp_path / "clone")


def test_a_git_url_is_cloned_shallow(tmp_path: Path) -> None:
    origin = tmp_path / "origin"
    origin.mkdir()
    (origin / "answer.txt").write_text("42\n", encoding="utf-8")
    ident = ["-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-q"], cwd=origin, check=True)
    subprocess.run(["git", *ident, "add", "-A"], cwd=origin, check=True)
    subprocess.run(["git", *ident, "commit", "-qm", "work"], cwd=origin, check=True)
    got = ga.resolve_submission(origin.as_uri(), tmp_path / "clone")
    assert (got / "answer.txt").read_text(encoding="utf-8") == "42\n"


def test_missing_grader_says_it_is_private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ga, "REPO", tmp_path)
    with pytest.raises(ga.SubmissionError, match="private"):
        ga.grader_command(1, Path("/tmp/sub"))
