"""demo/harness/ holds exactly the files the state layer gives the agent in the Section 2 demo."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_PATH = Path(__file__).resolve().parent / "sync_harness.py"
_spec = importlib.util.spec_from_file_location("s2_sync_harness", _PATH)
assert _spec and _spec.loader
sync = importlib.util.module_from_spec(_spec)
sys.modules["s2_sync_harness"] = sync
_spec.loader.exec_module(sync)


def test_demo_harness_matches_what_the_state_layer_writes() -> None:
    assert sync.differences() == [], "run: uv run python 02-state-lifecycle/demo/sync_harness.py"


def test_the_demo_harness_has_the_four_initializer_files() -> None:
    assert sorted(sync.present_files()) == [
        "docs/exec-plans/active/F2.md",
        "init.sh",
        "progress.md",
        "session-handoff.md",
    ]


def test_a_changed_file_is_reported(tmp_path: Path) -> None:
    for rel, data in sync.expected_files().items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(data)
    (tmp_path / "progress.md").write_text("# Progress\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("x\n", encoding="utf-8")
    assert sync.differences(tmp_path) == ["extra: notes.md", "differs: progress.md"]
