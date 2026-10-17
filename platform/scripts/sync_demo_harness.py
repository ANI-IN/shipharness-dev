"""Refresh every section's demo/harness/ from the harness layer that produces it.

Each section's demo folder shows learners what one harness layer gives the agent. The files are
taken from the layer's own code, so they match what the agent gets byte for byte:

- 01-instructions: the instructions tree as `InstructionsLayer.prepare_workspace` places it (the
  layer's file list, with walkthrough markers stripped).
- 02-state-lifecycle: the four files `StateLayer.prepare_workspace` writes for the demo ticket (F2,
  canonical, the dataset line `make show-2` runs).
- 03-scope-sandbox: what the scope layer gives the harness arm of `make demo-3 FEATURE=F4`:
  `feature_list.json` (written from the task), `feature_list.schema.json` (the layer's asset), and
  the "## Scope" block of its context prefix (`scope-rules.txt`).
- 04-verification: the verify layer places no files; its text is the context prefix
  (`VerifyLayer.PREFIX`) and the gate's items per phase, in the order `run_gate` reports them.
- final-project/harness/: the complete harness of `make final FEATURES=F5` (the default of
  final-project/run.sh): all four layers' files together, each taken as above but for the F5 dataset
  line and the final's layer stack.

A section's README.md is its own page and is left alone, and so is final-project/harness/README.md.
`platform/tests/unit/test_demo_harness.py` fails when a copy drifts (the final project's copy
included), and when a section has a demo/harness/ folder with no entry here.

Usage (repository root):
  uv run python platform/scripts/sync_demo_harness.py           # rewrite every copy
  uv run python platform/scripts/sync_demo_harness.py --check   # list drift, exit 1 if any
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

from shipharness.layout import find_repo_root

if TYPE_CHECKING:
    from shipharness.ab.demo import ABTask

REPO = find_repo_root(Path(__file__))
README = frozenset({"README.md"})


def load_task(feature: str, variant: str = "canonical") -> ABTask:
    """The dataset line `shipharness ab --feature <feature>` runs."""
    from shipharness.ab.commands import FEATURES_FILE
    from shipharness.ab.demo import ABTask

    for line in FEATURES_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        inputs = data["inputs"]
        if inputs["feature_id"] == feature and inputs.get("variant", "canonical") == variant:
            return ABTask.from_dataset_line(data)
    raise LookupError(f"no {feature} {variant} line in {FEATURES_FILE}")


# -- section 1: instructions ----------------------------------------------------------------------


def instructions_files(source: Path | None = None) -> dict[str, bytes]:
    """Relative path -> the bytes the instructions layer writes into the workspace."""
    from shipharness.harness.instructions.layer import DEFAULT_SOURCE, source_files
    from shipharness.harness.instructions.router import strip_markers

    source = DEFAULT_SOURCE if source is None else source
    files: dict[str, bytes] = {}
    for rel in source_files(source):
        text = (source / rel).read_text(encoding="utf-8")
        if rel.endswith(".md"):
            text = strip_markers(text)
        files[rel] = text.encode("utf-8")
    return files


# -- section 2: state -----------------------------------------------------------------------------


def state_files(task: ABTask | None = None) -> dict[str, bytes]:
    """The four files StateLayer.prepare_workspace writes for a ticket (default: the demo's F2)."""
    from shipharness.harness.state.templates import initial_files

    task = task or load_task("F2")
    kwargs = task.harness_kwargs()
    spec = SimpleNamespace(feature_id=task.feature_id, ticket_text=task.ticket_text)
    return initial_files(spec, kwargs["feature_description"], kwargs["feature_steps"])  # type: ignore[arg-type]


# -- section 3: scope ----------------------------------------------------------------------------

SCOPE_BLOCK = "scope-rules.txt"


def scope_files(task: ABTask | None = None, section: str = "demo-3") -> dict[str, bytes]:
    """What the scope layer gives the harness arm of `section` (default: demo-3 on F4)."""
    from shipharness.ab.demo import arm_specs, section_layers
    from shipharness.config import Settings
    from shipharness.config.profiles import apply_profile
    from shipharness.harness.base import LayerContext
    from shipharness.harness.scope.features import (
        FEATURE_LIST,
        FEATURE_SCHEMA,
        SCHEMA_ASSET,
        render,
    )
    from shipharness.harness.scope.layer import ScopeLayer
    from shipharness.sandbox import FakeSandbox

    task = task or load_task("F4")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        spec = arm_specs(
            task,
            apply_profile(Settings(_env_file=None), "class"),
            ab_id=None,
            harness_layers=section_layers(section),
            workspaces={"harness": workspace},
            run_ids={"harness": "r-demo-copy"},
            profile="class",
        )["harness"]
        layer = ScopeLayer(**task.harness_kwargs())
        ctx = LayerContext(
            spec=spec,
            phase=spec.phases[0],
            session_index=1,
            turn=0,
            workspace=workspace,
            sandbox=FakeSandbox(),
        )
        block = "\n\n".join(layer.context_prefix(ctx)) + "\n"
        return {
            FEATURE_LIST: render(layer.feature(ctx)),
            FEATURE_SCHEMA: SCHEMA_ASSET.read_bytes(),
            SCOPE_BLOCK: block.encode("utf-8"),
        }


# -- section 4: verification ----------------------------------------------------------------------


class _Stop(Exception):
    """Raised after the gate's first update (its pending items), before any command runs."""


def gate_items(phase: str) -> list[str]:
    """The item names run_gate publishes as pending pills for `phase`, in order. The first update
    comes before the gate touches the sandbox, so no sandbox is needed."""
    from shipharness.harness.verify.gate import GateConfig, run_gate
    from shipharness.harness.verify.models import GateResult

    names: list[str] = []

    def grab(result: GateResult) -> None:
        names.extend(item.name for item in result.items)
        raise _Stop

    try:
        run_gate(
            None,  # type: ignore[arg-type]
            GateConfig(checkpoint="", feature=""),
            gate_id="items",
            base_sha="",
            phase=phase,
            on_update=grab,
        )
    except _Stop:
        return names
    raise RuntimeError("run_gate did not publish its pending items first")


def verify_files() -> dict[str, bytes]:
    """The verify block of the first message, and the gate's items for each phase."""
    from shipharness.harness.verify.layer import PREFIX

    return {
        "context-prefix.txt": (PREFIX + "\n").encode("utf-8"),
        "gate-items-build.txt": ("\n".join(gate_items("build")) + "\n").encode("utf-8"),
        "gate-items-test.txt": ("\n".join(gate_items("test")) + "\n").encode("utf-8"),
    }


# -- final project: every layer at once ----------------------------------------------------------

FINAL_FOLDER = "final-project"
FINAL_FEATURE = "F5"  # the default of final-project/run.sh


def final_files() -> dict[str, bytes]:
    """The complete harness the final's harness arm gets on F5: the instructions tree, the state
    files, the scope files, and the verify text, in layer order. No two layers write one path."""
    task = load_task(FINAL_FEATURE)
    files: dict[str, bytes] = {}
    for part in (
        instructions_files(),
        state_files(task),
        scope_files(task, "final"),
        verify_files(),
    ):
        clash = sorted(files.keys() & part.keys())
        if clash:
            raise ValueError(f"two layers write the same file: {', '.join(clash)}")
        files.update(part)
    return files


# -- every section --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Section:
    expected: Callable[[], dict[str, bytes]]
    keep: frozenset[str] = field(default=frozenset())  # the folder's own pages, not agent files


SECTIONS: dict[str, Section] = {
    "01-instructions": Section(instructions_files),
    "02-state-lifecycle": Section(state_files, README),
    "03-scope-sandbox": Section(scope_files, README),
    "04-verification": Section(verify_files, README),
}


def present(dest: Path, keep: frozenset[str]) -> dict[str, bytes]:
    if not dest.is_dir():
        return {}
    return {
        p.relative_to(dest).as_posix(): p.read_bytes()
        for p in sorted(dest.rglob("*"))
        if p.is_file() and p.relative_to(dest).as_posix() not in keep
    }


def drift(want: dict[str, bytes], dest: Path, keep: frozenset[str] = frozenset()) -> list[str]:
    """One line per difference: missing, extra, then differs; each group sorted by path."""
    have = present(dest, keep)
    missing = [f"missing {rel}" for rel in sorted(want.keys() - have.keys())]
    extra = [f"extra {rel}" for rel in sorted(have.keys() - want.keys())]
    differs = [
        f"differs {rel}" for rel in sorted(want.keys() & have.keys()) if want[rel] != have[rel]
    ]
    return missing + extra + differs


def write(want: dict[str, bytes], dest: Path, keep: frozenset[str] = frozenset()) -> int:
    """Replace the agent files in `dest` with `want`, leaving kept pages; return the count."""
    for rel in present(dest, keep):
        (dest / rel).unlink()
    for rel, data in want.items():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for folder in sorted((p for p in dest.rglob("*") if p.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()
    return len(want)


FINAL = Section(final_files, README)


def harness_dir(folder: str, root: Path = REPO) -> Path:
    if folder == FINAL_FOLDER:
        return root / FINAL_FOLDER / "harness"
    return root / folder / "demo" / "harness"


def targets() -> dict[str, Section]:
    """Every copy this script writes: the sections' demo/harness/ folders, then the final's."""
    return {**SECTIONS, FINAL_FOLDER: FINAL}


def section_drift(folder: str, root: Path = REPO) -> list[str]:
    section = targets()[folder]
    return drift(section.expected(), harness_dir(folder, root), section.keep)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report drift, change nothing")
    parser.add_argument("--root", type=Path, default=REPO, help="repository root")
    args = parser.parse_args(argv)
    problems = 0
    for folder, section in targets().items():
        dest = harness_dir(folder, args.root)
        if args.check:
            lines = drift(section.expected(), dest, section.keep)
            problems += len(lines)
            for line in lines:
                print(f"x {folder}: {line}")
        else:
            count = write(section.expected(), dest, section.keep)
            print(f"wrote {count} files to {dest.relative_to(args.root).as_posix()}")
    if args.check:
        print(f"{problems} differences")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
