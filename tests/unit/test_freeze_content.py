"""Freeze rules 1 and 2 (owner, M6): content hashes per frozen path, and no silent changes."""

from __future__ import annotations

import subprocess
from pathlib import Path

from shipharness import freeze
from shipharness.config import Settings

IDENT = ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"]
S = Settings(_env_file=None)


def git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *IDENT, *args], cwd=repo, check=True, capture_output=True, text=True
    )
    return out.stdout.strip()


def make_repo(tmp_path: Path, name: str, message: str) -> Path:
    repo = tmp_path / name
    (repo / "src" / "shipharness" / "runner").mkdir(parents=True)
    (repo / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 1\n", encoding="utf-8")
    git(tmp_path, "init", "-q", str(repo))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)
    git(repo, "tag", "m1-s1-start")
    return repo


def test_record_holds_a_content_hash_per_frozen_path_and_checkpoint_trees(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, "build", "base")
    record = freeze.make_record(repo, S)
    assert set(record["content_hashes"]) == set(freeze.FROZEN_PATHS)
    assert len(record["content_hashes"]["src/shipharness/runner"]) == 64
    assert record["content_hashes"]["teamtrack/harness"] == freeze.ABSENT
    assert record["checkpoint_trees"] == {
        "m1-s1-start": git(repo, "rev-parse", "m1-s1-start^{tree}")
    }


def test_same_content_with_new_history_matches_the_record(tmp_path: Path) -> None:
    build = make_repo(tmp_path, "build", "private history")
    public = make_repo(tmp_path, "public", "one fresh commit")
    assert git(build, "rev-parse", "HEAD") != git(public, "rev-parse", "HEAD")
    record = freeze.make_record(build, S)
    freeze.write_record_tag(public, record, identity=("t", "t@t"))
    assert freeze.problems(public, S) == []
    assert freeze.compare_content(public, record) == []


def test_content_change_in_the_public_repo_is_reported(tmp_path: Path) -> None:
    build = make_repo(tmp_path, "build", "a")
    public = make_repo(tmp_path, "public", "b")
    (public / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 2\n", encoding="utf-8")
    found = freeze.compare_content(public, freeze.make_record(build, S))
    assert found == ["content differs: src/shipharness/runner"]


def test_checkpoint_tags_compare_by_tree_not_commit(tmp_path: Path) -> None:
    build = make_repo(tmp_path, "build", "a")
    public = make_repo(tmp_path, "public", "b")
    freeze.write_record_tag(public, freeze.make_record(build, S), identity=("t", "t@t"))
    assert freeze.problems(public, S) == []  # different commit, same tree
    (public / "README.md").write_text("x\n", encoding="utf-8")
    git(public, "add", "-A")
    git(public, "commit", "-qm", "c")
    git(public, "tag", "-f", "m1-s1-start")
    assert any("m1-s1-start" in p for p in freeze.problems(public, S))


def _change_and_hash(repo: Path) -> str:
    (repo / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 2\n", encoding="utf-8")
    return freeze.content_hashes(repo, ["src/shipharness/runner"])["src/shipharness/runner"]


def test_change_with_a_recorded_no_score_effect_check_is_accepted(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, "build", "a")
    freeze.create_tag(repo, S, identity=("t", "t@t"))
    new = _change_and_hash(repo)
    (repo / freeze.EXCEPTIONS_FILE).write_text(
        "[[change]]\n"
        'path = "src/shipharness/runner"\n'
        f'content_hash = "{new}"\n'
        'kind = "no-score-effect"\n'
        'verification = "VERIFICATION.md, M8: comment-only change in tools.py"\n',
        encoding="utf-8",
    )
    assert freeze.problems(repo, S) == []


def test_change_with_a_recorded_rerun_is_accepted(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, "build", "a")
    freeze.create_tag(repo, S, identity=("t", "t@t"))
    new = _change_and_hash(repo)
    (repo / freeze.EXCEPTIONS_FILE).write_text(
        "[[change]]\n"
        'path = "src/shipharness/runner"\n'
        f'content_hash = "{new}"\n'
        'kind = "rerun"\n'
        'verification = "VERIFICATION.md, M8 batch 1 re-run"\n'
        'experiments = ["m8-batch1-rerun"]\n',
        encoding="utf-8",
    )
    assert freeze.problems(repo, S) == []


def test_silent_or_stale_or_incomplete_exceptions_are_problems(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, "build", "a")
    freeze.create_tag(repo, S, identity=("t", "t@t"))
    _change_and_hash(repo)
    assert freeze.problems(repo, S) == ["content differs: src/shipharness/runner"]  # silent
    (repo / freeze.EXCEPTIONS_FILE).write_text(
        '[[change]]\npath = "src/shipharness/runner"\ncontent_hash = "' + "0" * 64 + '"\n'
        'kind = "no-score-effect"\nverification = "VERIFICATION.md, M8"\n',
        encoding="utf-8",
    )
    assert any("content differs" in p for p in freeze.problems(repo, S))  # stale hash
    new = freeze.content_hashes(repo, ["src/shipharness/runner"])["src/shipharness/runner"]
    (repo / freeze.EXCEPTIONS_FILE).write_text(
        f'[[change]]\npath = "src/shipharness/runner"\ncontent_hash = "{new}"\nkind = "rerun"\n',
        encoding="utf-8",
    )
    assert any("exception incomplete" in p for p in freeze.problems(repo, S))  # no record


def test_expected_hashes_apply_valid_exceptions(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, "build", "a")
    freeze.create_tag(repo, S, identity=("t", "t@t"))
    new = _change_and_hash(repo)
    (repo / freeze.EXCEPTIONS_FILE).write_text(
        f'[[change]]\npath = "src/shipharness/runner"\ncontent_hash = "{new}"\n'
        'kind = "no-score-effect"\nverification = "VERIFICATION.md, M8"\n',
        encoding="utf-8",
    )
    record = freeze.expected_record(repo)
    assert record is not None and record["content_hashes"]["src/shipharness/runner"] == new
