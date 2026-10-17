"""scripts/check_contributors.py: every commit's author and committer is ANI-IN, with no
co-author or generated-by trailer (owner message 10.3)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_contributors", REPO / "scripts" / "check_contributors.py"
)
assert _spec and _spec.loader
cc = importlib.util.module_from_spec(_spec)
sys.modules["check_contributors"] = cc
_spec.loader.exec_module(cc)

OWNER = ("ANI-IN", "44803072+ANI-IN@users.noreply.github.com")


def _commit(
    repo: Path,
    message: str,
    author: tuple[str, str] = OWNER,
    committer: tuple[str, str] = OWNER,
) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        GIT_AUTHOR_NAME=author[0],
        GIT_AUTHOR_EMAIL=author[1],
        GIT_COMMITTER_NAME=committer[0],
        GIT_COMMITTER_EMAIL=committer[1],
    )
    (repo / "f.txt").write_text(message, encoding="utf-8")
    run = dict(cwd=repo, env=env, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], **run)  # type: ignore[call-overload]
    subprocess.run(["git", "commit", "-q", "-m", message], **run)  # type: ignore[call-overload]
    done = subprocess.run(["git", "rev-parse", "HEAD"], text=True, **run)  # type: ignore[call-overload]
    return done.stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    path = tmp_path / "r"
    path.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    return path


def test_the_expected_identity_is_the_owner() -> None:
    assert cc.EXPECTED == "ANI-IN <44803072+ANI-IN@users.noreply.github.com>"


def test_owner_only_history_passes(repo: Path) -> None:
    _commit(repo, "first")
    _commit(repo, "second\n\nA body line.")
    assert cc.commit_problems(repo) == []
    assert cc.main([str(repo)]) == 0


def test_another_author_or_committer_is_reported(repo: Path) -> None:
    _commit(repo, "ok")
    bad_author = _commit(repo, "by someone", author=("Someone", "s@example.com"))
    bad_committer = _commit(repo, "applied", committer=("Bot", "bot@example.com"))
    other_email = _commit(repo, "own name, other email", author=("ANI-IN", "ani@example.com"))
    found = {p.sha: p for p in cc.commit_problems(repo)}
    assert set(found) == {bad_author, bad_committer, other_email}
    assert found[bad_author].problems == ["author Someone <s@example.com>"]
    assert found[bad_committer].problems == ["committer Bot <bot@example.com>"]
    assert found[other_email].problems == ["author ANI-IN <ani@example.com>"]


@pytest.mark.parametrize(
    "trailer",
    [
        "Co-authored-by: Someone <s@example.com>",
        "co-authored-by: someone <s@example.com>",
        "\N{ROBOT FACE} Generated with [Claude Code](https://claude.com/claude-code)",
        "Generated with Claude",
    ],
)
def test_coauthor_and_generated_trailers_are_reported(repo: Path, trailer: str) -> None:
    sha = _commit(repo, f"change\n\nbody\n\n{trailer}")
    (problem,) = cc.commit_problems(repo)
    assert problem.sha == sha
    assert any("trailer" in p for p in problem.problems)


def test_commits_on_other_branches_and_tags_are_checked(repo: Path) -> None:
    _commit(repo, "main")
    subprocess.run(["git", "checkout", "-q", "-b", "side"], cwd=repo, check=True)
    side = _commit(repo, "side", author=("Someone", "s@example.com"))
    subprocess.run(["git", "tag", "t1"], cwd=repo, check=True)
    subprocess.run(["git", "checkout", "-q", "main"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "-q", "-D", "side"], cwd=repo, check=True)
    assert [p.sha for p in cc.commit_problems(repo)] == [side]  # reachable from tag t1


def test_cli_prints_pass_or_the_offending_commits(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _commit(repo, "ok")
    assert cc.main([str(repo)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Contributors: PASS")
    assert "1 commit" in out
    sha = _commit(repo, "by someone", author=("Someone", "s@example.com"))
    assert cc.main([str(repo)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("Contributors: FAIL")
    assert sha[:12] in out and "by someone" in out and "author Someone <s@example.com>" in out


def test_cli_on_a_folder_that_is_not_a_repository(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cc.main([str(tmp_path)]) == 2
    assert "not a git repository" in capsys.readouterr().err
