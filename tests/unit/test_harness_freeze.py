"""Harness freeze (owner rule, M6): once the pilot gate passes, `harness-frozen` tags the treatment.

M8 results are valid only for the tagged harness, runner, prompts, and tools. After the tag, any
change under the frozen paths fails this test; such a change would require re-running M8. Without
the tag (before the gate passes, or a shallow CI checkout) the test is skipped.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TAG = "harness-frozen"
FROZEN_PATHS = (
    "src/shipharness/harness",
    "src/shipharness/runner",  # loop, prompts, tools, patch formats
    "teamtrack/harness",  # instruction files the harness places in the workspace
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False)


def test_frozen_paths_match_the_harness_frozen_tag() -> None:
    if _git("rev-parse", "-q", "--verify", f"refs/tags/{TAG}").returncode != 0:
        pytest.skip(f"no {TAG} tag yet")
    changed = _git("diff", "--name-only", TAG, "--", *FROZEN_PATHS).stdout.split()
    untracked = _git(
        "ls-files", "--others", "--exclude-standard", "--", *FROZEN_PATHS
    ).stdout.split()
    assert not changed and not untracked, (
        f"files changed since {TAG} (re-run M8 or revert): {sorted(changed + untracked)}"
    )
