"""diff.patch is what the referee judges, so the agent must not be able to hide files from it."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from shipharness.runner import git as run_git

GIT_ID = ["-c", "user.name=t", "-c", "user.email=t@x"]


def git(ws: Path, *args: str) -> None:
    subprocess.run(["git", *GIT_ID, *args], cwd=ws, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / "app").mkdir(parents=True)
    (ws / "app" / "main.py").write_text("x = 1\n", encoding="utf-8")
    git(ws, "init", "-q")
    git(ws, "add", ".")
    git(ws, "commit", "-qm", "init")
    return ws


def test_agent_gitignore_does_not_hide_new_files_from_the_diff(repo: Path, tmp_path: Path) -> None:
    (repo / ".gitignore").write_text("app/helper.py\nnotes/\n", encoding="utf-8")
    (repo / "app" / "helper.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    (repo / "notes").mkdir()
    (repo / "notes" / "todo.txt").write_text("hidden\n", encoding="utf-8")
    base = run_git.initial_sha(repo)
    out = run_git.write_diff(repo, base, tmp_path / "diff.patch")
    assert out is not None
    text = out.read_text(encoding="utf-8")
    assert "app/helper.py" in text
    assert "notes/todo.txt" in text
    assert ".gitignore" in text


def test_info_exclude_in_the_agent_git_dir_does_not_hide_files(repo: Path, tmp_path: Path) -> None:
    (repo / ".git" / "info").mkdir(exist_ok=True)
    (repo / ".git" / "info" / "exclude").write_text("app/sneaky.py\n", encoding="utf-8")
    (repo / "app" / "sneaky.py").write_text("z = 3\n", encoding="utf-8")
    base = run_git.initial_sha(repo)
    out = run_git.write_diff(repo, base, tmp_path / "diff.patch")
    assert out is not None
    assert "app/sneaky.py" in out.read_text(encoding="utf-8")


def test_generated_files_stay_out_of_the_diff(repo: Path, tmp_path: Path) -> None:
    (repo / "app" / "__pycache__").mkdir()
    (repo / "app" / "__pycache__" / "main.cpython-312.pyc").write_bytes(b"\x00\x01")
    (repo / ".pytest_cache").mkdir()
    (repo / ".pytest_cache" / "README.md").write_text("cache\n", encoding="utf-8")
    (repo / "teamtrack.db").write_bytes(b"SQLite format 3\x00")
    (repo / "app" / "new.py").write_text("y = 2\n", encoding="utf-8")
    base = run_git.initial_sha(repo)
    out = run_git.write_diff(repo, base, tmp_path / "diff.patch")
    assert out is not None
    text = out.read_text(encoding="utf-8", errors="replace")
    assert "app/new.py" in text
    for generated in ("__pycache__", ".pytest_cache", "teamtrack.db"):
        assert generated not in text
