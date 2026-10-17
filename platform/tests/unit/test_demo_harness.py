"""Every section's demo/harness/ holds exactly what its harness layer gives the agent.

The copies are written by `platform/scripts/sync_demo_harness.py` from the layer code itself. When a
layer changes, these tests fail until the copies are refreshed with
`uv run python platform/scripts/sync_demo_harness.py`.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from shipharness.harness.instructions.layer import InstructionsLayer
from shipharness.layout import find_repo_root

from .harness_instructions.conftest import make_ctx, write

REPO = find_repo_root(Path(__file__))
FIX = "run: uv run python platform/scripts/sync_demo_harness.py"

_spec = importlib.util.spec_from_file_location(
    "sync_demo_harness", REPO / "platform" / "scripts" / "sync_demo_harness.py"
)
assert _spec and _spec.loader
sync = importlib.util.module_from_spec(_spec)
sys.modules["sync_demo_harness"] = sync  # dataclasses look their module up
_spec.loader.exec_module(sync)

PRESENT = sorted(p.parent.parent.name for p in REPO.glob("0[1-4]-*/demo/harness"))
MARKER = "<!-- [walkthrough:S1:agents_md] start -->\n"


def _tree(root: Path, keep: frozenset[str] = frozenset()) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.relative_to(root).as_posix() not in keep
    }


def test_the_sections_with_a_demo_harness_are_found() -> None:
    assert {
        "01-instructions",
        "02-state-lifecycle",
        "03-scope-sandbox",
        "04-verification",
    } <= set(PRESENT)


@pytest.mark.parametrize("folder", PRESENT)
def test_every_demo_harness_present_has_a_source(folder: str) -> None:
    assert folder in sync.SECTIONS, f"{folder}/demo/harness/ has no entry in sync_demo_harness.py"


@pytest.mark.parametrize("folder", [f for f in PRESENT if f in sync.SECTIONS])
def test_the_demo_harness_has_no_drift(folder: str) -> None:
    assert sync.section_drift(folder) == [], FIX


def test_the_section_1_copy_equals_what_the_layer_places(tmp_path: Path) -> None:
    InstructionsLayer().prepare_workspace(make_ctx(tmp_path))
    assert _tree(REPO / "01-instructions" / "demo" / "harness") == _tree(tmp_path), FIX


def test_the_section_2_copy_has_the_four_initializer_files() -> None:
    section = sync.SECTIONS["02-state-lifecycle"]
    assert sorted(_tree(REPO / "02-state-lifecycle" / "demo" / "harness", section.keep)) == [
        "docs/exec-plans/active/F2.md",
        "init.sh",
        "progress.md",
        "session-handoff.md",
    ]


def test_the_section_3_feature_files_equal_what_the_layer_writes(tmp_path: Path) -> None:
    from shipharness.ab.demo import arm_specs, section_layers
    from shipharness.config import Settings
    from shipharness.config.profiles import apply_profile
    from shipharness.harness.base import LayerContext
    from shipharness.harness.scope.features import FEATURE_LIST, FEATURE_SCHEMA
    from shipharness.harness.scope.layer import ScopeLayer
    from shipharness.sandbox import FakeSandbox

    task = sync.load_task("F4")
    spec = arm_specs(
        task,
        apply_profile(Settings(_env_file=None), "class"),
        ab_id=None,
        harness_layers=section_layers("demo-3"),
        workspaces={"harness": tmp_path},
        run_ids={"harness": "r-test"},
        profile="class",
    )["harness"]
    ctx = LayerContext(
        spec=spec, phase="build", session_index=1, turn=0, workspace=tmp_path,
        sandbox=FakeSandbox(),
    )  # fmt: skip
    ScopeLayer(**task.harness_kwargs()).prepare_workspace(ctx)
    copy = REPO / "03-scope-sandbox" / "demo" / "harness"
    want = sync.scope_files(task)
    for rel in (FEATURE_LIST, FEATURE_SCHEMA):
        assert (tmp_path / rel).read_bytes() == want[rel] == (copy / rel).read_bytes(), FIX


def test_the_section_3_copy_is_the_f4_ticket_with_passes_false() -> None:
    copy = REPO / "03-scope-sandbox" / "demo" / "harness"
    (feature,) = json.loads((copy / "feature_list.json").read_text(encoding="utf-8"))["features"]
    assert feature["id"] == "F4"
    assert feature["passes"] is False and feature["evidence"] is None
    rules = (copy / sync.SCOPE_BLOCK).read_text(encoding="utf-8")
    for phase, paths in sync.load_task("F4").allowed_paths.items():
        assert f"- {phase}: {', '.join(paths)}" in rules
    assert "progress.md, session-handoff.md, docs/exec-plans/**" in rules  # the state layer is on


def test_the_section_4_gate_items_follow_the_gate() -> None:
    build = sync.gate_items("build")
    assert build[0] == "visible tests" and build[-1] == "clean state"
    assert [n for n in build if n.startswith("R")] == [f"R{i}" for i in range(1, 8)]
    assert sync.gate_items("test") == ["visible tests", "clean state"]


def test_drift_names_missing_extra_and_changed_files_and_skips_kept_ones(tmp_path: Path) -> None:
    write(tmp_path, "docs/SECURITY.md", "R1 changed\n")
    write(tmp_path, "docs/OLD.md", "old\n")
    write(tmp_path, "README.md", "the folder's own page\n")
    want = {"AGENTS.md": b"# Map\n", "docs/SECURITY.md": b"R1\n"}
    assert sync.drift(want, tmp_path, frozenset({"README.md"})) == [
        "missing AGENTS.md",
        "extra docs/OLD.md",
        "differs docs/SECURITY.md",
    ]


def test_write_replaces_the_copy_and_keeps_the_readme(tmp_path: Path) -> None:
    write(tmp_path, "stale.md", "stale\n")
    write(tmp_path, "README.md", "page\n")
    want = {"AGENTS.md": b"# Map\n"}
    assert sync.write(want, tmp_path, frozenset({"README.md"})) == 1
    assert sync.drift(want, tmp_path, frozenset({"README.md"})) == []
    assert not (tmp_path / "stale.md").exists()
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "page\n"


def test_the_instructions_copy_has_no_walkthrough_markers(tmp_path: Path) -> None:
    write(tmp_path, "AGENTS.md", MARKER + "# Map\n")
    write(tmp_path, ".agents/skills/s/SKILL.md", "---\nname: s\n---\n")
    files = sync.instructions_files(tmp_path)
    assert files["AGENTS.md"] == b"# Map\n"
    assert sorted(files) == [".agents/skills/s/SKILL.md", "AGENTS.md"]


def test_check_mode_exits_1_on_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    section = sync.Section(lambda: {"AGENTS.md": b"# Map\n"}, frozenset())
    monkeypatch.setattr(sync, "SECTIONS", {"09-test": section})
    monkeypatch.setattr(sync, "targets", lambda: {"09-test": section})
    args = ["--root", str(tmp_path), "--check"]
    assert sync.main(args) == 1
    assert sync.main(args[:-1]) == 0
    assert sync.main(args) == 0
    assert (tmp_path / "09-test" / "demo" / "harness" / "AGENTS.md").is_file()


# -- final project: the complete harness ---------------------------------------------------------

FINAL_COPY = REPO / "final-project" / "harness"


def test_the_final_project_harness_has_no_drift() -> None:
    assert sync.section_drift(sync.FINAL_FOLDER) == [], FIX


def test_the_final_harness_is_every_layer_on_f5() -> None:
    task = sync.load_task("F5")
    want: dict[str, bytes] = {}
    for part in (
        sync.instructions_files(),
        sync.state_files(task),
        sync.scope_files(task, "final"),
        sync.verify_files(),
    ):
        want.update(part)
    assert sync.final_files() == want
    have = _tree(FINAL_COPY, sync.FINAL.keep)
    assert have == want, FIX
    for rel in ("AGENTS.md", "progress.md", "docs/exec-plans/active/F5.md", "context-prefix.txt"):
        assert rel in have
    (feature,) = json.loads(have["feature_list.json"])["features"]
    assert feature["id"] == "F5" and feature["passes"] is False
    rules = have[sync.SCOPE_BLOCK].decode("utf-8")
    for phase, paths in task.allowed_paths.items():
        assert f"- {phase}: {', '.join(paths)}" in rules


def test_the_final_harness_drift_check_fails_on_a_changed_copy(tmp_path: Path) -> None:
    dest = sync.harness_dir(sync.FINAL_FOLDER, tmp_path)
    assert dest == tmp_path / "final-project" / "harness"
    sync.write(sync.final_files(), dest, sync.FINAL.keep)
    assert sync.section_drift(sync.FINAL_FOLDER, tmp_path) == []
    (dest / "AGENTS.md").write_text("# edited by hand\n", encoding="utf-8")
    (dest / "notes.md").write_text("extra\n", encoding="utf-8")
    (dest / "progress.md").unlink()
    assert sync.section_drift(sync.FINAL_FOLDER, tmp_path) == [
        "missing progress.md",
        "extra notes.md",
        "differs AGENTS.md",
    ]
