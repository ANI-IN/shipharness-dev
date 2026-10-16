"""Harness freeze (DESIGN §10.4): what the `harness-frozen` tag pins before M8.

When the pilot gate passes, `scripts/freeze_harness.py` creates an annotated tag at HEAD. M8
results are valid only for that state. The tag pins four things:

- treatment, measurement, tasks, and environment files (`FROZEN_PATHS`): any change, or new file,
  under them after the tag is drift;
- the checkpoint tags and their commits (recorded in the tag message);
- the run settings that shape a run (`RUN_SETTINGS`), both the code defaults and the effective values
  (with `.env`); secrets are never recorded.

Console, report, replay tooling, docs, slides, and course content stay editable.
"""

from __future__ import annotations

import json
import subprocess
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


def run_settings(settings: Settings) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key in RUN_SETTINGS:
        value = getattr(settings, key)
        values[key] = value if isinstance(value, int | float | bool) else str(value)
    return values


def checkpoint_tags(repo: Path) -> dict[str, str]:
    """Checkpoint tag name -> commit."""
    names = _git(repo, "tag", "--list", f"{CHECKPOINT_TAG_PREFIX}*").stdout.split()
    return {name: _git(repo, "rev-parse", f"{name}^{{commit}}").stdout.strip() for name in names}


def make_record(repo: Path, effective: Settings) -> dict[str, Any]:
    return {
        "frozen_paths": list(FROZEN_PATHS),
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
        return {
            "frozen_paths": list(FROZEN_PATHS),
            "checkpoint_tags": {},
            "defaults": {},
            "effective": {},
        }
    return json.loads(payload)


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
    record = make_record(repo, effective)
    message = (
        "Harness freeze before M8 (DESIGN 10.4). M8 results are valid only for this state.\n\n"
        f"{_MARKER}\n{json.dumps(record, indent=2, sort_keys=True)}\n"
    )
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


def problems(repo: Path, effective: Settings) -> list[str]:
    """Everything that differs from the frozen state; empty without the tag."""
    record = read_record(repo)
    if record is None:
        return []
    found: list[str] = []
    paths = record.get("frozen_paths") or list(FROZEN_PATHS)
    changed = _git(repo, "diff", "--name-only", TAG, "--", *paths).stdout.split()
    untracked = _git(
        repo, "ls-files", "--others", "--exclude-standard", "--", *paths
    ).stdout.split()
    found += [f"file changed: {p}" for p in sorted(set(changed) | set(untracked))]
    current = checkpoint_tags(repo)
    for name, sha in sorted(record.get("checkpoint_tags", {}).items()):
        if current.get(name) != sha:
            found.append(
                f"checkpoint tag moved: {name} {sha[:12]} -> {current.get(name, 'missing')[:12]}"
            )
    for label, now in (
        ("defaults", run_settings(Settings(_env_file=None))),
        ("effective", run_settings(effective)),
    ):
        for key, value in sorted(record.get(label, {}).items()):
            if now.get(key) != value:
                found.append(f"run setting changed ({label}): {key} {value!r} -> {now.get(key)!r}")
    return found
