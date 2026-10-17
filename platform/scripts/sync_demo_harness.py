"""Copy the instructions layer's tree into 01-instructions/demo/harness/, as the layer places it.

The Section 1 demo folder shows learners the files the agent receives. The copy uses the layer's own
file list and marker stripping (`source_files` and `strip_markers`, as in
`InstructionsLayer.prepare_workspace`), so it matches what the agent gets byte for byte.
`platform/tests/unit/harness_instructions/test_demo_copy.py` fails when the copy drifts.

Usage (repository root):
  uv run python platform/scripts/sync_demo_harness.py           # rewrite the copy
  uv run python platform/scripts/sync_demo_harness.py --check   # list drift, exit 1 if any
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from shipharness.harness.instructions.layer import DEFAULT_SOURCE, source_files
from shipharness.harness.instructions.router import strip_markers
from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
DEFAULT_DEST = REPO / "01-instructions" / "demo" / "harness"


def expected(source: Path) -> dict[str, bytes]:
    """Relative path -> the bytes the layer writes into the workspace."""
    files: dict[str, bytes] = {}
    for rel in source_files(source):
        text = (source / rel).read_text(encoding="utf-8")
        if rel.endswith(".md"):
            text = strip_markers(text)
        files[rel] = text.encode("utf-8")
    return files


def actual(dest: Path) -> dict[str, bytes]:
    if not dest.is_dir():
        return {}
    return {
        p.relative_to(dest).as_posix(): p.read_bytes()
        for p in sorted(dest.rglob("*"))
        if p.is_file()
    }


def drift(source: Path, dest: Path) -> list[str]:
    """One line per difference: missing, extra, then differs; each group sorted by path."""
    want, have = expected(source), actual(dest)
    missing = [f"missing {rel}" for rel in sorted(want.keys() - have.keys())]
    extra = [f"extra {rel}" for rel in sorted(have.keys() - want.keys())]
    differs = [
        f"differs {rel}" for rel in sorted(want.keys() & have.keys()) if want[rel] != have[rel]
    ]
    return missing + extra + differs


def sync(source: Path, dest: Path) -> int:
    """Replace `dest` with a fresh copy; return the number of files written."""
    files = expected(source)
    if dest.exists():
        shutil.rmtree(dest)
    for rel, data in files.items():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return len(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--check", action="store_true", help="report drift, change nothing")
    args = parser.parse_args(argv)
    if args.check:
        problems = drift(args.source, args.dest)
        for line in problems:
            print(f"x {line}")
        print(f"{len(problems)} differences")
        return 1 if problems else 0
    count = sync(args.source, args.dest)
    print(f"copied {count} files to {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
