"""Build the checkpoint commits and tags from teamtrack/reference/checkpoints.toml (ruling R-3).

    uv run python scripts/build_checkpoints.py --dry-run          # list what it would tag
    uv run python scripts/build_checkpoints.py                    # integrator only: commit + tag
    uv run python scripts/build_checkpoints.py m1-s2-start --force

Each checkpoint becomes one commit whose parent is the current HEAD (main), not on any branch,
with the checkpoint's reference patches applied to teamtrack/ in a temporary index; then a tag of
the same name. Builders never run it without --dry-run: tags are shared by every worktree.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from shipharness.ab.checkpoints import CheckpointError, build_commits
from shipharness.config.prices import REPO_ROOT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_checkpoints", description=__doc__)
    parser.add_argument("names", nargs="*", help="checkpoints to build (default: all)")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--dry-run", action="store_true", help="apply patches, commit nothing")
    parser.add_argument("--force", action="store_true", help="move existing tags")
    args = parser.parse_args(argv)
    try:
        results = build_commits(
            args.repo, args.names or None, dry_run=args.dry_run, force=args.force
        )
    except CheckpointError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for r in results:
        tasks = ", ".join(t.upper() for t in r.tasks) or "base"
        if r.commit is None:
            print(f"would tag {r.name}: {tasks} (tree {r.tree[:12]})")
        else:
            print(f"tagged {r.name} -> {r.commit[:12]}: {tasks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
