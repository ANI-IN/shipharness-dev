"""Harness freeze: what the `harness-frozen` tag pins before M8.

When the pilot gate passes, a build-repository freeze script creates an annotated tag at HEAD. M8
results are valid only for that state. The tag pins four things:

- treatment, measurement, tasks, and environment files (`FROZEN_PATHS`): any change, or new file,
  under them after the tag is drift;
- a content hash per frozen path and the checkpoint tags' trees, so the check also works in the
  public repository, whose history is new (rule 2);
- the run settings that shape a run (`RUN_SETTINGS`), both the code defaults and the effective
  values (with `.env`); secrets are never recorded.

Rule 1: after the tag, a change to a frozen path passes only with an entry in the private
`FREEZE-EXCEPTIONS.toml` (its content hash, and either the M8 experiments re-run or a recorded
check that it cannot change any score). No silent changes.

Console, report, replay tooling, docs, slides, and course content stay editable.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tomllib
from pathlib import Path
from typing import Any

from shipharness.config import Settings

TAG = "harness-frozen"
CHECKPOINT_TAG_PREFIX = "m1-"
_MARKER = "frozen-record:"

FROZEN_PATHS: tuple[str, ...] = (
    # treatment
    "src/shipharness/harness",
    "src/shipharness/runner",  # loop, prompts, tools, patch formats
    "src/shipharness/filters",
    "teamtrack/harness",  # instruction files the harness places in the workspace
    # measurement
    "src/shipharness/checks",  # checks and the check runner
    "src/shipharness/reviewer",  # prompt and grading criteria
    "src/shipharness/ab/artifacts.py",
    "src/shipharness/ab/checkpoints.py",
    "src/shipharness/ab/clients.py",
    "src/shipharness/ab/commands.py",
    "src/shipharness/ab/demo.py",
    "src/shipharness/ab/experiments.py",
    "src/shipharness/ab/mutants.py",
    "src/shipharness/ab/referee.py",
    "src/shipharness/ab/runtime.py",
    "src/shipharness/ab/score.py",
    "src/shipharness/ab/workspace.py",
    # tasks
    "datasets",
    "teamtrack/tests/hidden",
    "teamtrack/mutants",
    "teamtrack/reference",  # task manifests, reference patches, checkpoints.toml
    # environment
    "sandbox/Dockerfile",
    "src/shipharness/sandbox",  # policy and container execution
    "src/shipharness/cost",  # caps and reservations
    "config/prices.toml",
    "uv.lock",
    ".python-version",
)

RUN_SETTINGS: tuple[str, ...] = (
    "openai_model",
    "openai_reasoning_effort",
    "openai_eval_model",
    "openai_eval_reasoning_effort",
    "openai_service_tier",
    "max_run_cost_usd",
    "max_final_run_cost_usd",
    "max_review_cost_usd",
    "max_session_cost_usd",
    "max_batch_cost_usd",
    "max_experiment_total_usd",
    "max_build_total_usd",
    "max_turns_per_session",
    "max_output_tokens",
    "wrapup_turns",
    "tool_timeout_s",
    "run_timeout_s",
    "harness_timeout_s",
    "max_concurrency",
    "sandbox_mode",
    "sandbox_runtime",
    "sandbox_image_agent",
    "sandbox_image_referee",
)


class FreezeError(RuntimeError):
    """The tag cannot be created."""


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)


ABSENT = "absent"
EXCEPTIONS_FILE = "FREEZE-EXCEPTIONS.toml"  # private: accepted changes after the tag (rule 1)
EXCEPTION_KINDS = ("rerun", "no-score-effect")


def run_settings(settings: Settings) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key in RUN_SETTINGS:
        value = getattr(settings, key)
        values[key] = value if isinstance(value, int | float | bool) else str(value)
    return values


def checkpoint_tags(repo: Path) -> dict[str, str]:
    """Checkpoint tag name -> commit (informational: commit ids differ between repositories)."""
    names = _git(repo, "tag", "--list", f"{CHECKPOINT_TAG_PREFIX}*").stdout.split()
    return {name: _git(repo, "rev-parse", f"{name}^{{commit}}").stdout.strip() for name in names}


def checkpoint_trees(repo: Path) -> dict[str, str]:
    """Checkpoint tag name -> the id of its `teamtrack/` tree (what arms and the referee use; the
    build repository's checkpoint commits also hold private files, the public rebuild does not),
    or of the whole tree when the tag has no `teamtrack/` (compared, rule 2)."""
    names = _git(repo, "tag", "--list", f"{CHECKPOINT_TAG_PREFIX}*").stdout.split()
    trees: dict[str, str] = {}
    for name in names:
        sub = _git(repo, "rev-parse", "-q", "--verify", f"{name}:teamtrack")
        whole = _git(repo, "rev-parse", f"{name}^{{tree}}")
        trees[name] = (sub.stdout if sub.returncode == 0 else whole.stdout).strip()
    return trees


def content_hashes(repo: Path, paths: list[str] | tuple[str, ...]) -> dict[str, str]:
    """SHA-256 per path over the working-tree bytes of its files (tracked plus untracked, ignored
    files excluded), independent of commit history. `ABSENT` when a path has no files."""
    hashes: dict[str, str] = {}
    root = Path(repo)
    for path in paths:
        listed = _git(
            repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", path
        ).stdout
        files = sorted({f for f in listed.split("\0") if f})
        digest = hashlib.sha256()
        present = 0
        for rel in files:
            file = root / rel
            if file.is_symlink():
                data = b"link:" + os.readlink(file).encode()
            elif file.is_file():
                data = file.read_bytes()
            else:
                continue  # deleted from the working tree
            present += 1
            digest.update(rel.encode() + b"\0" + hashlib.sha256(data).digest())
        hashes[path] = digest.hexdigest() if present else ABSENT
    return hashes


def make_record(repo: Path, effective: Settings) -> dict[str, Any]:
    return {
        "frozen_paths": list(FROZEN_PATHS),
        "content_hashes": content_hashes(repo, FROZEN_PATHS),
        "checkpoint_trees": checkpoint_trees(repo),
        "checkpoint_tags": checkpoint_tags(repo),
        "defaults": run_settings(Settings(_env_file=None)),
        "effective": run_settings(effective),
    }


def read_record(repo: Path) -> dict[str, Any] | None:
    if _git(repo, "rev-parse", "-q", "--verify", f"refs/tags/{TAG}").returncode != 0:
        return None
    message = _git(repo, "tag", "--list", TAG, "--format=%(contents)").stdout
    _, found, payload = message.partition(_MARKER)
    if not found:
        raise FreezeError(f"{TAG} has no frozen record in its message")
    return json.loads(payload)


def read_exceptions(repo: Path) -> tuple[dict[str, str], list[str]]:
    """Accepted changes (path -> content hash) and problems with the exceptions file. An entry is
    valid only with a kind, a verification-record reference, and (for re-runs) the experiments
    re-run."""
    file = Path(repo) / EXCEPTIONS_FILE
    if not file.is_file():
        return {}, []
    accepted: dict[str, str] = {}
    issues: list[str] = []
    for entry in tomllib.loads(file.read_text(encoding="utf-8")).get("change", []):
        path = str(entry.get("path", ""))
        complete = (
            path in FROZEN_PATHS
            and len(str(entry.get("content_hash", ""))) == 64
            and entry.get("kind") in EXCEPTION_KINDS
            and len(str(entry.get("verification", "")).strip()) >= 8
            and (entry.get("kind") != "rerun" or bool(entry.get("experiments")))
        )
        if complete:
            accepted[path] = str(entry["content_hash"])
        else:
            issues.append(
                f"exception incomplete: {path or '(no path)'} needs a frozen path, its content "
                "hash, kind rerun (with experiments) or no-score-effect, and a verification-record "
                "entry"
            )
    return accepted, issues


def expected_record(repo: Path) -> dict[str, Any] | None:
    """The tag's record with valid exceptions applied: what M8 results are valid for."""
    record = read_record(repo)
    if record is None:
        return None
    accepted, _ = read_exceptions(repo)
    return {**record, "content_hashes": {**record["content_hashes"], **accepted}}


def _message(record: dict[str, Any]) -> str:
    return (
        "Harness freeze before M8 (course freeze rules 1 and 2). "
        "M8 results are valid only for this content.\n\n"
        f"{_MARKER}\n{json.dumps(record, indent=2, sort_keys=True)}\n"
    )


def _tag(repo: Path, message: str, identity: tuple[str, str]) -> str:
    name, email = identity
    made = _git(
        repo,
        "-c",
        f"user.name={name}",
        "-c",
        f"user.email={email}",
        "tag",
        "-a",
        TAG,
        "-m",
        message,
    )
    if made.returncode != 0:
        raise FreezeError(made.stderr.strip() or "git tag failed")
    return _git(repo, "rev-parse", f"{TAG}^{{commit}}").stdout.strip()


def _dirty(repo: Path, paths: list[str]) -> list[str]:
    changed = _git(repo, "diff", "--name-only", "HEAD", "--", *paths).stdout.split()
    untracked = _git(
        repo, "ls-files", "--others", "--exclude-standard", "--", *paths
    ).stdout.split()
    return sorted(set(changed) | set(untracked))


def create_tag(repo: Path, effective: Settings, *, identity: tuple[str, str]) -> str:
    """Annotated `harness-frozen` tag at HEAD with the record in its message; returns the commit."""
    if _git(repo, "rev-parse", "-q", "--verify", f"refs/tags/{TAG}").returncode == 0:
        raise FreezeError(f"{TAG} exists; a new freeze needs the owner's decision and an M8 re-run")
    dirty = _dirty(repo, list(FROZEN_PATHS))
    if dirty:
        raise FreezeError("uncommitted changes under frozen paths: " + ", ".join(dirty[:20]))
    return _tag(repo, _message(make_record(repo, effective)), identity)


def write_record_tag(repo: Path, record: dict[str, Any], *, identity: tuple[str, str]) -> str:
    """The same record as an annotated tag in another repository (the public release)."""
    if _git(repo, "rev-parse", "-q", "--verify", f"refs/tags/{TAG}").returncode == 0:
        raise FreezeError(f"{TAG} exists in {repo}")
    return _tag(repo, _message(record), identity)


def compare_content(repo: Path, record: dict[str, Any]) -> list[str]:
    """Frozen content of `repo` against `record` by content hash and checkpoint tree (rule 2)."""
    found: list[str] = []
    paths = record.get("frozen_paths") or list(FROZEN_PATHS)
    now = content_hashes(repo, paths)
    for path in paths:
        if now.get(path) != record.get("content_hashes", {}).get(path):
            found.append(f"content differs: {path}")
    trees = checkpoint_trees(repo)
    for name, tree in sorted(record.get("checkpoint_trees", {}).items()):
        if trees.get(name) != tree:
            found.append(f"checkpoint content differs: {name}")
    return found


def problems(repo: Path, effective: Settings) -> list[str]:
    """Everything that differs from the frozen state (valid exceptions applied); empty without
    the tag. Rule 1: a change passes only with a recorded re-run or a no-score-effect check."""
    expected = expected_record(repo)
    if expected is None:
        return []
    _, issues = read_exceptions(repo)
    found = compare_content(repo, expected) + issues
    for label, now in (
        ("defaults", run_settings(Settings(_env_file=None))),
        ("effective", run_settings(effective)),
    ):
        for key, value in sorted(expected.get(label, {}).items()):
            if now.get(key) != value:
                found.append(f"run setting changed ({label}): {key} {value!r} -> {now.get(key)!r}")
    return found
