"""Scratch directories inside a workspace, and safe reads of files written by sandboxed code.

Filters run pytest through the Sandbox, which sees only the workspace, so temporary copies and
coverage files live in uniquely named `.shipharness-*` directories at the workspace root. The agent
cannot predict the names. Files that sandboxed code wrote are read only if they are regular files
inside the scratch directory (never through a link) and below a size cap.
"""

from __future__ import annotations

import shutil
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from shipharness.runner.tools import iter_workspace_files

SCRATCH_PREFIX = ".shipharness-"
MAX_READ_BYTES = 50_000_000
MAX_COPY_BYTES = 300_000_000


class ScratchError(RuntimeError):
    """A scratch file is missing, a link, outside the workspace, or too large."""


def _is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


@contextmanager
def scratch_dir(workspace: Path, kind: str) -> Iterator[Path]:
    """A fresh `<workspace>/.shipharness-<kind>-<hex>` directory, removed afterwards."""
    path = Path(workspace) / f"{SCRATCH_PREFIX}{kind}-{uuid.uuid4().hex[:12]}"
    path.mkdir()
    try:
        yield path
    finally:
        if not _is_link(path):
            shutil.rmtree(path, ignore_errors=True)


def is_scratch(rel: str) -> bool:
    return rel.split("/", 1)[0].startswith(SCRATCH_PREFIX)


def copy_workspace(workspace: Path, dest: Path) -> int:
    """Copy regular workspace files (no links, no skipped dirs, no scratch dirs) into `dest`."""
    root = Path(workspace)
    files = [
        (path, rel)
        for path in iter_workspace_files(root)
        if not is_scratch(rel := path.relative_to(root).as_posix()) and path.suffix != ".pyc"
    ]
    total = 0
    for path, rel in files:
        size = path.stat().st_size
        total += size
        if total > MAX_COPY_BYTES:
            raise ScratchError(f"workspace larger than {MAX_COPY_BYTES} bytes")
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    return total


def read_scratch_file(scratch: Path, name: str) -> str:
    """Read `scratch/name` written by sandboxed code, refusing links and oversized files."""
    path = scratch / name
    if _is_link(path) or not path.is_file():
        raise ScratchError(f"{name} was not written as a regular file")
    resolved = path.resolve()
    if scratch.resolve() not in resolved.parents:
        raise ScratchError(f"{name} resolves outside the scratch directory")
    if resolved.stat().st_size > MAX_READ_BYTES:
        raise ScratchError(f"{name} is larger than {MAX_READ_BYTES} bytes")
    return resolved.read_text(encoding="utf-8", errors="replace")
