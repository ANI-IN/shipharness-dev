"""`scripts/build_checkpoints.py`: tags never move under recorded results without the owner's
approval (--owner-approved-move); --dry-run says what would move and whether results exist. Every
test uses a temporary repository: the real tags are never touched."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

from shipharness.config.prices import REPO_ROOT


def _script() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "build_checkpoints_script", REPO_ROOT / "scripts" / "build_checkpoints.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
def toy(tmp_path: Path) -> dict[str, Path]:
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
    runs, exports = tmp_path / "runs", tmp_path / "exports"
    runs.mkdir()
    exports.mkdir()
    return {"repo": repo, "runs": runs, "exports": exports}


def run(toy: dict[str, Path], capsys: pytest.CaptureFixture[str], *args: str) -> tuple[int, str]:
    argv = [*args, "--repo", str(toy["repo"])]
    argv += ["--runs-dir", str(toy["runs"]), "--exports-dir", str(toy["exports"])]
    code = _script().main(argv)
    captured = capsys.readouterr()
    return code, captured.out + captured.err


def tags(repo: Path) -> dict[str, str]:
    names = _git(repo, "tag", "--list").split()
    return {n: _git(repo, "rev-parse", f"{n}^{{commit}}") for n in names}


def advance(repo: Path) -> None:
    """A new main commit, so rebuilt checkpoint commits differ from the tagged ones."""
    (repo / "NOTES.md").write_bytes(b"next\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "next")


def record_ab(runs: Path) -> None:
    (runs / "ab-20261016-090000-aaaaaa").mkdir()
    (runs / "ab-20261016-090000-aaaaaa" / "ab.json").write_text("{}", encoding="utf-8")


def record_score(exports: Path) -> None:
    (exports / "scores").mkdir()
    (exports / "scores" / "r-1.json").write_text(json.dumps({"run_id": "r-1"}), encoding="utf-8")


@pytest.mark.parametrize("recorder", [record_ab, record_score])
def test_force_refuses_to_move_tags_when_results_exist(toy, capsys, recorder) -> None:  # type: ignore[no-untyped-def]
    assert run(toy, capsys)[0] == 0
    before = tags(toy["repo"])
    recorder(toy["runs"] if recorder is record_ab else toy["exports"])
    code, out = run(toy, capsys, "--force")
    assert code == 1
    assert "owner" in out and "--owner-approved-move" in out
    assert tags(toy["repo"]) == before


def test_force_moves_tags_when_no_results_exist(toy, capsys) -> None:  # type: ignore[no-untyped-def]
    run(toy, capsys)
    before = tags(toy["repo"])
    advance(toy["repo"])
    code, out = run(toy, capsys, "--force")
    assert code == 0, out
    after = tags(toy["repo"])
    assert after.keys() == before.keys() and all(after[n] != before[n] for n in before)


def test_owner_approved_move_moves_tags_and_names_each_move(toy, capsys) -> None:  # type: ignore[no-untyped-def]
    run(toy, capsys)
    before = tags(toy["repo"])
    record_ab(toy["runs"])
    record_score(toy["exports"])
    advance(toy["repo"])
    code, out = run(toy, capsys, "--owner-approved-move")
    assert code == 0, out
    after = tags(toy["repo"])
    for name in ("c-base", "c-one"):
        assert after[name] != before[name]
        assert f"moved {name}: {before[name][:12]} -> {after[name][:12]}" in out


def test_dry_run_reports_moves_and_recorded_results(toy, capsys) -> None:  # type: ignore[no-untyped-def]
    run(toy, capsys)
    before = tags(toy["repo"])
    code, out = run(toy, capsys, "--dry-run")
    assert code == 0, out
    assert f"would move c-one from {before['c-one'][:12]}" in out
    assert "recorded results: none" in out
    record_ab(toy["runs"])
    code, out = run(toy, capsys, "--dry-run")
    assert code == 0
    assert "recorded results: 1" in out and "--owner-approved-move" in out
    assert tags(toy["repo"]) == before


def test_dry_run_of_new_tags_says_would_tag(toy, capsys) -> None:  # type: ignore[no-untyped-def]
    code, out = run(toy, capsys, "--dry-run")
    assert code == 0
    assert "would tag c-base: base" in out and "would tag c-one: F1" in out
    assert tags(toy["repo"]) == {}
