"""01-instructions/demo/harness/ shows learners the files the agent gets in Section 1.

The copy must equal what InstructionsLayer.prepare_workspace places, byte for byte. When a file in
platform/teamtrack/harness/instructions/ changes, these tests fail until the copy is refreshed with
`uv run python platform/scripts/sync_demo_harness.py`.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from shipharness.harness.instructions.layer import DEFAULT_SOURCE, InstructionsLayer
from shipharness.layout import find_repo_root

from .conftest import make_ctx, write

REPO = find_repo_root(Path(__file__))
DEMO_COPY = REPO / "01-instructions" / "demo" / "harness"
FIX = "run: uv run python platform/scripts/sync_demo_harness.py"

_spec = importlib.util.spec_from_file_location(
    "sync_demo_harness", REPO / "platform" / "scripts" / "sync_demo_harness.py"
)
assert _spec and _spec.loader
sync_demo_harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync_demo_harness)

MARKER = "<!-- [walkthrough:S1:agents_md] start -->\n"


def _tree(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_the_demo_copy_has_no_drift() -> None:
    assert sync_demo_harness.drift(DEFAULT_SOURCE, DEMO_COPY) == [], FIX


def test_the_demo_copy_equals_what_the_layer_places(tmp_path: Path) -> None:
    InstructionsLayer().prepare_workspace(make_ctx(tmp_path))
    assert _tree(DEMO_COPY) == _tree(tmp_path), FIX


def test_drift_names_missing_changed_and_extra_files(tmp_path: Path) -> None:
    source, dest = tmp_path / "source", tmp_path / "dest"
    write(source, "AGENTS.md", MARKER + "# Map\n")
    write(source, "docs/SECURITY.md", "R1\n")
    write(dest, "docs/SECURITY.md", "R1 changed\n")
    write(dest, "docs/OLD.md", "old\n")
    assert sync_demo_harness.drift(source, dest) == [
        "missing AGENTS.md",
        "extra docs/OLD.md",
        "differs docs/SECURITY.md",
    ]


def test_sync_rewrites_the_copy_without_walkthrough_markers(tmp_path: Path) -> None:
    source, dest = tmp_path / "source", tmp_path / "dest"
    write(source, "AGENTS.md", MARKER + "# Map\n")
    write(source, ".agents/skills/s/SKILL.md", "---\nname: s\n---\n")
    write(dest, "stale.md", "stale\n")
    assert sync_demo_harness.sync(source, dest) == 2
    assert sync_demo_harness.drift(source, dest) == []
    assert (dest / "AGENTS.md").read_text(encoding="utf-8") == "# Map\n"
    assert not (dest / "stale.md").exists()


def test_check_mode_exits_1_on_drift(tmp_path: Path) -> None:
    source, dest = tmp_path / "source", tmp_path / "dest"
    write(source, "AGENTS.md", "# Map\n")
    args = ["--source", str(source), "--dest", str(dest), "--check"]
    assert sync_demo_harness.main(args) == 1
    assert sync_demo_harness.main(args[:-1]) == 0
    assert sync_demo_harness.main(args) == 0
