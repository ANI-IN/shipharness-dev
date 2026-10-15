"""Host-side git helpers for an arm's workspace repository."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


def _git(workspace: Path, *args: str, env: dict[str, str] | None = None) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=workspace, capture_output=True, text=True, check=False, env=env
        )
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def head_sha(workspace: Path) -> str:
    out = _git(workspace, "rev-parse", "HEAD")
    return out.strip() if out else ""


def initial_sha(workspace: Path) -> str:
    out = _git(workspace, "rev-list", "--max-parents=0", "HEAD")
    return out.strip().splitlines()[0] if out and out.strip() else ""


def write_diff(workspace: Path, base_sha: str, out_path: Path) -> Path | None:
    """Diff of the working tree (including untracked files) against `base_sha`.

    Uses a temporary index so the agent's own staging area is not touched.
    """
    if not base_sha:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        if _git(workspace, "add", "-A", env=env) is None:
            return None
        diff = _git(workspace, "diff", "--cached", "--binary", base_sha, env=env)
    if diff is None:
        return None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(diff, encoding="utf-8", newline="\n")
    return out_path
