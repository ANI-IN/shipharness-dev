"""shipharness.ab.checkpoints: checkpoint definitions, patch selection, materialize, build."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from shipharness.ab import checkpoints as cp
from shipharness.config.prices import REPO_ROOT

R3_TAGS = {
    "m1-s1-start": [],
    "m1-s2-start": ["f1"],
    "m1-s3-start": ["f1", "f2"],
    "m1-s4-start": ["f1", "f2", "f3"],
    "m1-final-start": ["f1", "f2", "f3", "f4"],
    "m1-complete": ["f1", "f2", "f3", "f4", "f5", "f6", "f7"],
    "m1-alt-a": ["f5", "f6"],
    "m1-alt-b": ["f7"],
}


def test_checkpoints_match_ruling_r3() -> None:
    found = cp.load_checkpoints()
    assert {name: c.tasks for name, c in found.items()} == R3_TAGS


def test_every_task_of_a_checkpoint_has_a_default_patch() -> None:
    for checkpoint in cp.load_checkpoints().values():
        for task in checkpoint.tasks:
            assert (
                REPO_ROOT / "platform" / "teamtrack" / "reference" / task / f"{task}.patch"
            ).is_file()


def test_patch_for_prefers_the_checkpoint_variant() -> None:
    assert cp.patch_for("f1", "m1-s1-start").name == "f1.patch"
    assert cp.patch_for("f1", "m1-alt-a").name == "f1.m1-alt-a.patch"
    assert cp.patch_for("f6", "m1-final-start").name == "f6.patch"


def test_state_before_a_task() -> None:
    assert cp.state_before("f6", "m1-complete") == ["f1", "f2", "f3", "f4", "f5"]
    assert cp.state_before("f1", "m1-alt-a") == ["f5", "f6"]  # not in the list: whole checkpoint
    assert cp.state_before("f5", "m1-alt-a") == []


def test_unknown_checkpoint_or_task_is_an_error() -> None:
    with pytest.raises(cp.CheckpointError, match="unknown checkpoint"):
        cp.checkpoint("m9-nowhere")
    with pytest.raises(cp.CheckpointError, match="no reference patch"):
        cp.patch_for("f99", "m1-s1-start")


def test_load_task_reads_the_manifest() -> None:
    task = cp.load_task("f1")
    assert task.id == "F1"
    assert task.start_checkpoint == "m1-s1-start"
    assert task.hidden["m1-s1-start"]


def test_materialize_base_is_a_filtered_copy(tmp_path: Path) -> None:
    dest = cp.materialize(REPO_ROOT, "m1-s1-start", tmp_path / "b")
    assert (dest / "app" / "main.py").is_file()
    assert not (dest / "reference").exists()
    assert not (dest / "tests" / "hidden").exists()


def test_materialize_applies_reference_patches_in_order(tmp_path: Path) -> None:
    dest = cp.materialize(REPO_ROOT, "m1-s3-start", tmp_path / "b")
    assert "def search(" in (dest / "app" / "services" / "issues.py").read_text(encoding="utf-8")
    assert (dest / "app" / "api" / "comments.py").is_file()
    assert (dest / "migrations" / "versions" / "0002_comments.py").is_file()


def test_apply_reference_failure_is_reported(tmp_path: Path) -> None:
    dest = cp.materialize(REPO_ROOT, "m1-s1-start", tmp_path / "b")
    with pytest.raises(cp.ReferenceApplyError):
        cp.apply_reference("f4", "m1-s4-start", dest)  # F4 needs F1-F3 first


# -- building commits (in a throwaway repository, never in the course checkout) ------------------


def _git(cwd: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_NAME="t",
        GIT_AUTHOR_EMAIL="t@t.invalid",
        GIT_COMMITTER_NAME="t",
        GIT_COMMITTER_EMAIL="t@t.invalid",
    )
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, env=env, check=True)
    return done.stdout.decode().strip()


@pytest.fixture
def toy_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "teamtrack" / "app").mkdir(parents=True)
    (repo / "teamtrack" / "app" / "x.py").write_bytes(b"a = 1\n")
    ref = repo / "teamtrack" / "reference"
    (ref / "f1").mkdir(parents=True)
    (ref / "f1" / "f1.patch").write_bytes(
        b"diff --git a/app/x.py b/app/x.py\n--- a/app/x.py\n+++ b/app/x.py\n"
        b"@@ -1 +1,2 @@\n a = 1\n+b = 2\n"
    )
    (ref / "checkpoints.toml").write_bytes(
        b'[checkpoints."c-base"]\ntasks = []\n\n[checkpoints."c-one"]\ntasks = ["f1"]\n'
    )
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@t.invalid")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    return repo


def test_build_dry_run_creates_nothing(toy_repo: Path) -> None:
    results = cp.build_commits(toy_repo, dry_run=True)
    assert [(r.name, r.tasks) for r in results] == [("c-base", []), ("c-one", ["f1"])]
    assert all(r.commit is None for r in results)
    assert _git(toy_repo, "tag", "--list") == ""


def test_build_creates_one_commit_per_checkpoint_on_main(toy_repo: Path) -> None:
    head = _git(toy_repo, "rev-parse", "HEAD")
    results = cp.build_commits(toy_repo, dry_run=False)
    by_name = {r.name: r for r in results}
    assert _git(toy_repo, "rev-parse", "c-one^") == head
    assert _git(toy_repo, "show", "c-one:teamtrack/app/x.py") == "a = 1\nb = 2"
    assert _git(toy_repo, "show", "c-base:teamtrack/app/x.py") == "a = 1"
    assert by_name["c-one"].commit == _git(toy_repo, "rev-parse", "c-one^{commit}")
    assert _git(toy_repo, "rev-parse", "HEAD") == head  # no branch moved
    with pytest.raises(cp.CheckpointError, match="already exist"):
        cp.build_commits(toy_repo, dry_run=False)


def test_script_dry_run_lists_what_it_would_tag(toy_repo: Path) -> None:
    script = REPO_ROOT / "platform" / "scripts" / "build_checkpoints.py"
    done = subprocess.run(
        [sys.executable, str(script), "--dry-run", "--repo", str(toy_repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    assert "would tag c-base: base" in done.stdout
    assert "would tag c-one: F1" in done.stdout
    assert _git(toy_repo, "tag", "--list") == ""


def test_script_refuses_an_unknown_checkpoint(toy_repo: Path) -> None:
    script = REPO_ROOT / "platform" / "scripts" / "build_checkpoints.py"
    done = subprocess.run(
        [sys.executable, str(script), "--dry-run", "--repo", str(toy_repo), "nowhere"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 1
    assert "unknown checkpoint" in done.stderr


@pytest.mark.slow
def test_every_checkpoint_applies_to_head_in_a_dry_run() -> None:
    results = cp.build_commits(REPO_ROOT, dry_run=True)
    assert [r.name for r in results] == list(R3_TAGS)
    assert all(r.commit is None for r in results)
