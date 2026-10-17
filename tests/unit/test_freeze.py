"""shipharness.freeze: what the `harness-frozen` tag pins, and how drift is found."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from shipharness import freeze
from shipharness.config import Settings

IDENT = ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"]


def git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *IDENT, *args], cwd=repo, check=True, capture_output=True, text=True
    )
    return out.stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "src" / "shipharness" / "runner").mkdir(parents=True)
    (repo / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 1\n", encoding="utf-8")
    (repo / "src" / "shipharness" / "console").mkdir(parents=True)
    (repo / "src" / "shipharness" / "console" / "app.py").write_text("B = 1\n", encoding="utf-8")
    git(repo.parent, "init", "-q", str(repo))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")
    git(repo, "tag", "m1-s1-start")
    return repo


def frozen(repo: Path, settings: Settings | None = None) -> None:
    freeze.create_tag(repo, settings or Settings(_env_file=None), identity=("t", "t@t"))


def test_frozen_paths_cover_treatment_measurement_tasks_and_environment() -> None:
    paths = set(freeze.FROZEN_PATHS)
    for path in (
        "src/shipharness/harness",
        "src/shipharness/runner",
        "src/shipharness/filters",
        "teamtrack/harness",
        "src/shipharness/checks",
        "src/shipharness/ab/referee.py",
        "src/shipharness/reviewer",
        "datasets",
        "teamtrack/tests/hidden",
        "teamtrack/mutants",
        "teamtrack/reference",
        "sandbox/Dockerfile",
        "src/shipharness/sandbox",
    ):
        assert path in paths, path
    for editable in ("src/shipharness/console", "src/shipharness/ab/report.py", "slides", "docs"):
        assert not any(editable == p or editable.startswith(p + "/") for p in paths), editable
    for key in ("openai_model", "openai_reasoning_effort", "max_turns_per_session",
                "run_timeout_s", "harness_timeout_s", "max_run_cost_usd"):  # fmt: skip
        assert key in freeze.RUN_SETTINGS, key


def test_every_frozen_path_exists_in_the_repository() -> None:
    repo = Path(__file__).resolve().parents[2]
    missing = [p for p in freeze.FROZEN_PATHS if not (repo / p).exists()]
    assert missing == []


def test_no_tag_means_no_record(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert freeze.read_record(repo) is None
    assert freeze.problems(repo, Settings(_env_file=None)) == []


def test_tag_records_checkpoint_commits_and_run_settings(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    frozen(repo)
    record = freeze.read_record(repo)
    assert record is not None
    assert record["checkpoint_tags"] == {"m1-s1-start": git(repo, "rev-parse", "m1-s1-start")}
    assert record["checkpoint_trees"] == {
        "m1-s1-start": git(repo, "rev-parse", "m1-s1-start^{tree}")
    }
    assert record["defaults"]["run_timeout_s"] == 300
    assert record["effective"]["openai_model"] == "gpt-6-luna"
    assert "openai_api_key" not in json.dumps(record)
    assert freeze.problems(repo, Settings(_env_file=None)) == []


def test_change_to_a_frozen_path_is_a_problem_and_an_editable_path_is_not(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    frozen(repo)
    (repo / "src" / "shipharness" / "console" / "app.py").write_text("B = 2\n", encoding="utf-8")
    assert freeze.problems(repo, Settings(_env_file=None)) == []
    (repo / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 2\n", encoding="utf-8")
    (repo / "src" / "shipharness" / "runner" / "new.py").write_text("C = 1\n", encoding="utf-8")
    found = freeze.problems(repo, Settings(_env_file=None))
    assert found == ["content differs: src/shipharness/runner"]


def test_moved_checkpoint_tag_is_a_problem(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    frozen(repo)
    (repo / "README.md").write_text("x\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "later")
    git(repo, "tag", "-f", "m1-s1-start")
    assert any("m1-s1-start" in p for p in freeze.problems(repo, Settings(_env_file=None)))


def test_changed_run_setting_is_a_problem(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    frozen(repo)
    changed = Settings(_env_file=None, run_timeout_s=480)
    assert any("run_timeout_s" in p for p in freeze.problems(repo, changed))


def test_tag_is_refused_when_frozen_paths_have_uncommitted_changes(tmp_path: Path) -> None:
    import pytest

    repo = make_repo(tmp_path)
    (repo / "src" / "shipharness" / "runner" / "tools.py").write_text("A = 3\n", encoding="utf-8")
    with pytest.raises(freeze.FreezeError, match="uncommitted"):
        frozen(repo)


def test_tag_is_refused_when_it_already_exists(tmp_path: Path) -> None:
    import pytest

    repo = make_repo(tmp_path)
    frozen(repo)
    with pytest.raises(freeze.FreezeError, match="exists"):
        frozen(repo)


def test_the_tag_message_cites_no_private_build_document() -> None:
    # The record tag is pushed to the public repository at release; its message must stand alone.
    from shipharness.freeze import _message

    message = _message({"content_hashes": {}})
    assert "DESIGN" not in message and "VERIFICATION" not in message
