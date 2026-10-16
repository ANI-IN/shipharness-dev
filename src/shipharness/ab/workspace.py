"""Arm workspaces (contract I-6, DESIGN §8.3 rule 6).

Each arm gets a fresh git repository made from a filtered export of `teamtrack/` at the checkpoint,
with one commit, outside the course checkout (`<system temp>/shipharness-ws/<ab_id>/<arm>/ws`).
It is never a worktree: hidden tests, referee mutants, reference implementations, and other
branches are unreachable through git. Host git here only touches the course repository (trusted)
and repositories this module has just created, always with system and global config disabled.
"""

from __future__ import annotations

import fnmatch
import io
import os
import secrets
import shutil
import subprocess
import tarfile
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from shipharness.config.prices import REPO_ROOT
from shipharness.events import Arm

APP_DIR = "teamtrack"
HIDDEN_DIR = "tests/hidden"
WORKSPACE_EXCLUDES: tuple[str, ...] = (
    "harness/**",
    "tests/hidden/**",
    "mutants/**",
    "reference/**",
    "*.db",
    "__pycache__/**",
)
# A fixed identity and date: both arms' checkpoint commits get the same SHA.
_COMMIT_ENV = {
    "GIT_AUTHOR_NAME": "shipharness",
    "GIT_AUTHOR_EMAIL": "checkpoint@shipharness.invalid",
    "GIT_COMMITTER_NAME": "shipharness",
    "GIT_COMMITTER_EMAIL": "checkpoint@shipharness.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z",
}


class CheckpointNotFound(LookupError):
    pass


class WorkspaceInsideCheckout(ValueError):
    pass


def _stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def new_ab_id() -> str:
    return f"ab-{_stamp()}-{secrets.token_hex(3)}"


def new_run_id() -> str:
    return f"r-{_stamp()}-{secrets.token_hex(3)}"


def workspace_base() -> Path:
    return Path(tempfile.gettempdir()) / "shipharness-ws"


def _env() -> dict[str, str]:
    keep = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return {**keep, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cmd = ["git", "-c", "core.autocrlf=false", "-c", "core.hooksPath=" + os.devnull, *args]
    return subprocess.run(cmd, cwd=cwd, capture_output=True, env=_env(), check=check)


def excluded(rel: str, patterns: tuple[str, ...] = WORKSPACE_EXCLUDES) -> bool:
    parts = PurePosixPath(rel).parts
    for pattern in patterns:
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if "/" in prefix:
                if rel == prefix or rel.startswith(prefix + "/"):
                    return True
            elif prefix in parts[:-1] or rel.startswith(prefix + "/"):
                return True
        elif fnmatch.fnmatchcase(parts[-1], pattern):
            return True
    return False


def _safe_member(name: str) -> str | None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path.as_posix()


def _extract(tar_bytes: bytes, prefix: str, dest: Path, keep: Callable[[str], bool]) -> int:
    count = 0
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as archive:
        for member in archive.getmembers():
            name = _safe_member(member.name)
            if name is None or not member.isfile() or not name.startswith(prefix + "/"):
                continue  # links, devices, and paths outside the prefix are never extracted
            rel = name[len(prefix) + 1 :]
            if not keep(rel):
                continue
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            assert source is not None
            target.write_bytes(source.read())
            if member.mode & 0o111:
                target.chmod(0o755)
            count += 1
    return count


def _archive(repo: Path, ref: str, path: str) -> bytes:
    check = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)
    if check.returncode != 0:
        raise CheckpointNotFound(f"checkpoint {ref!r} not found in {repo} (git tag or commit)")
    return _git(repo, "archive", "--format=tar", ref, "--", path).stdout


def export_checkpoint(
    repo: Path, checkpoint: str | None, dest: Path, app_dir: str = APP_DIR
) -> Path:
    """Filtered export of `<repo>/<app_dir>` at `checkpoint` (a git ref) into `dest`.
    `checkpoint=None` exports the working tree (development only; demos use tags)."""
    dest.mkdir(parents=True, exist_ok=True)
    if checkpoint is None:
        src = Path(repo) / app_dir
        for path in sorted(src.rglob("*")):
            rel = path.relative_to(src).as_posix()
            if path.is_symlink() or not path.is_file() or excluded(rel):
                continue
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        return dest
    _extract(_archive(Path(repo), checkpoint, app_dir), app_dir, dest, lambda r: not excluded(r))
    return dest


def export_hidden_tests(
    repo: Path, checkpoint: str | None, dest: Path, app_dir: str = APP_DIR
) -> Path:
    """Hidden tests for the referee container only (mounted read-only; never in a workspace)."""
    dest.mkdir(parents=True, exist_ok=True)
    prefix = f"{app_dir}/{HIDDEN_DIR}"
    if checkpoint is None:
        src = Path(repo) / prefix
        if src.is_dir():
            ignore = shutil.ignore_patterns("__pycache__")
            shutil.copytree(src, dest, dirs_exist_ok=True, ignore=ignore)
        return dest
    try:
        data = _archive(Path(repo), checkpoint, prefix)
    except subprocess.CalledProcessError:  # the checkpoint has no hidden tests
        return dest
    _extract(data, prefix, dest, lambda r: "__pycache__" not in r)
    return dest


def init_repo(path: Path, message: str) -> str:
    """git init + one commit of everything in `path`; returns the commit SHA."""
    _git(path, "init", "-q", "-b", "main")
    _git(path, "add", "-A", "-f")
    env = {**_env(), **_COMMIT_ENV}
    subprocess.run(
        ["git", "-c", "core.autocrlf=false", "commit", "-q", "--no-verify", "-m", message],
        cwd=path,
        capture_output=True,
        env=env,
        check=True,
    )
    return _git(path, "rev-parse", "HEAD").stdout.decode().strip()


def _inside(child: Path, parent: Path) -> bool:
    child, parent = child.resolve(), parent.resolve()
    return child == parent or parent in child.parents


def _open_permissions(root: Path) -> None:
    """The arm container runs as uid 1000; on POSIX hosts let it write the workspace."""
    if os.name != "posix":
        return
    for path in [root, *root.rglob("*")]:
        if not path.is_symlink():
            path.chmod(0o777 if path.is_dir() else 0o666 | (path.stat().st_mode & 0o111))


def create_arm_workspace(
    ab_id: str,
    arm: Arm,
    repo: Path,
    checkpoint: str | None,
    *,
    base: Path | None = None,
    course_root: Path = REPO_ROOT,
) -> Path:
    base = Path(base) if base is not None else workspace_base()
    ws = base / ab_id / arm / "ws"
    for checkout in {Path(repo), Path(course_root)}:
        if _inside(ws, checkout):
            raise WorkspaceInsideCheckout(f"arm workspace {ws} is inside the course checkout")
    if ws.exists():
        raise FileExistsError(f"workspace already exists (never reused): {ws}")
    export_checkpoint(repo, checkpoint, ws)
    init_repo(ws, f"checkpoint {checkpoint or 'working tree'}")
    _open_permissions(ws)
    return ws
