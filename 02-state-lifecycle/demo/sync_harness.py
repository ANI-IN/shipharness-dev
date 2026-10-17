"""Write the files the state layer gives the agent in the Section 2 demo into demo/harness/.

The state layer renders four templates for the ticket before session 1
(`StateLayer.prepare_workspace`, `platform/src/shipharness/harness/state/templates.py`). This script
renders them the same way, from the same dataset line that `make show-2` uses (F2, canonical), so
the files in demo/harness/ are byte for byte what the agent finds in its workspace.

Usage, from the repository root:
    uv run python 02-state-lifecycle/demo/sync_harness.py           # write the files
    uv run python 02-state-lifecycle/demo/sync_harness.py --check   # exit 1 if a file differs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from shipharness.ab.commands import FEATURES_FILE
from shipharness.ab.demo import ABTask
from shipharness.harness.state.templates import initial_files

HARNESS_DIR = Path(__file__).resolve().parent / "harness"
FEATURE, VARIANT = "F2", "canonical"
KEEP = {"README.md"}  # the folder's own page, not an agent file


def demo_task(dataset: Path = FEATURES_FILE) -> ABTask:
    """The dataset line `shipharness ab --section demo-2 --feature F2` runs."""
    for line in dataset.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        inputs = data["inputs"]
        if inputs["feature_id"] == FEATURE and inputs.get("variant", "canonical") == VARIANT:
            return ABTask.from_dataset_line(data)
    raise LookupError(f"no {FEATURE} {VARIANT} line in {dataset}")


def expected_files() -> dict[str, bytes]:
    """The four files StateLayer.prepare_workspace writes for the demo ticket."""
    task = demo_task()
    kwargs = task.harness_kwargs()
    spec = SimpleNamespace(feature_id=task.feature_id, ticket_text=task.ticket_text)
    return initial_files(spec, kwargs["feature_description"], kwargs["feature_steps"])  # type: ignore[arg-type]


def present_files(folder: Path = HARNESS_DIR) -> dict[str, bytes]:
    return {
        p.relative_to(folder).as_posix(): p.read_bytes()
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.relative_to(folder).as_posix() not in KEEP
    }


def differences(folder: Path = HARNESS_DIR) -> list[str]:
    """One line per file that is missing, extra, or different."""
    want, have = expected_files(), present_files(folder)
    problems = [f"missing: {rel}" for rel in sorted(set(want) - set(have))]
    problems += [f"extra: {rel}" for rel in sorted(set(have) - set(want))]
    both = sorted(set(want) & set(have))
    problems += [f"differs: {rel}" for rel in both if want[rel] != have[rel]]
    return problems


def write(folder: Path = HARNESS_DIR) -> list[str]:
    for rel in present_files(folder):
        (folder / rel).unlink()
    files = expected_files()
    for rel, data in files.items():
        target = folder / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return sorted(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report differences, write nothing")
    args = parser.parse_args(argv)
    if args.check:
        problems = differences()
        for line in problems:
            print(line)
        print("demo/harness matches the state layer" if not problems else "run without --check")
        return 1 if problems else 0
    for rel in write():
        print(f"wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
