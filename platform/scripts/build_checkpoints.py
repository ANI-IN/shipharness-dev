"""Build the checkpoint commits and tags from TeamTrack's reference/checkpoints.toml (R-3).

    uv run python platform/scripts/build_checkpoints.py --dry-run   # what it would tag or move
    uv run python platform/scripts/build_checkpoints.py             # integrator only: commit + tag
    uv run python platform/scripts/build_checkpoints.py m1-s2-start --force

Each checkpoint becomes one commit whose parent is the current HEAD (main), not on any branch,
with the checkpoint's reference patches applied to TeamTrack's directory (platform/teamtrack/, or
teamtrack/ when HEAD is in the layout before the course-first one) in a temporary index; then a
tag of the same name. Builders never run it without --dry-run: tags are shared by every worktree.

Moving a tag changes what every recorded result that names it would be judged against. --force
moves existing tags only while no recorded result exists (no `<runs>/*/ab.json`, no JSON export
under `<exports>`); with recorded results, tags move only with the owner's approval, given as
--owner-approved-move, and the script prints each tag's old and new commit.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from shipharness.ab.checkpoints import (
    CheckpointError,
    build_commits,
    load_checkpoints,
    recorded_results,
    tag_commits,
)
from shipharness.config.prices import REPO_ROOT

APPROVAL_FLAG = "--owner-approved-move"


def _configured_dirs(repo: Path) -> tuple[Path, Path]:
    """RUNS_DIR and EXPORTS_DIR from the settings; relative paths are relative to the repo."""
    from shipharness.config import Settings

    settings = Settings()
    runs, exports = Path(settings.runs_dir), Path(settings.exports_dir)
    return (
        runs if runs.is_absolute() else repo / runs,
        exports if exports.is_absolute() else repo / exports,
    )


def _results_line(results: list[Path]) -> str:
    if not results:
        return "recorded results: none (--force may move tags)"
    shown = ", ".join(p.as_posix() for p in results[:3]) + (" ..." if len(results) > 3 else "")
    return (
        f"recorded results: {len(results)} ({shown}); moving tags needs the owner's approval "
        f"({APPROVAL_FLAG})"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_checkpoints",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("names", nargs="*", help="checkpoints to build (default: all)")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--dry-run", action="store_true", help="apply patches, commit nothing")
    parser.add_argument(
        "--force", action="store_true", help="move existing tags (only while no results exist)"
    )
    parser.add_argument(
        APPROVAL_FLAG,
        dest="owner_approved_move",
        action="store_true",
        help="move existing tags even though recorded results exist (the owner approved it)",
    )
    parser.add_argument("--runs-dir", type=Path, default=None, help="default: RUNS_DIR")
    parser.add_argument("--exports-dir", type=Path, default=None, help="default: EXPORTS_DIR")
    args = parser.parse_args(argv)
    repo = Path(args.repo)
    if args.runs_dir is None or args.exports_dir is None:
        runs, exports = _configured_dirs(repo)
        args.runs_dir = args.runs_dir or runs
        args.exports_dir = args.exports_dir or exports
    try:
        wanted = args.names or list(load_checkpoints(repo))
        before = tag_commits(repo, wanted)
        results = recorded_results(args.runs_dir, args.exports_dir)
        force = args.force or args.owner_approved_move
        if before and force and results and not args.owner_approved_move and not args.dry_run:
            print(
                f"error: refusing to move tag(s) {sorted(before)}: {len(results)} recorded "
                "result(s) name checkpoints by tag, and a moved tag changes what they would be "
                "judged against. Tags may only move with the owner's approval; if the owner "
                f"approved this move, run again with {APPROVAL_FLAG}.",
                file=sys.stderr,
            )
            print(_results_line(results), file=sys.stderr)
            return 1
        built = build_commits(repo, args.names or None, dry_run=args.dry_run, force=force)
    except CheckpointError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for r in built:
        tasks = ", ".join(t.upper() for t in r.tasks) or "base"
        old = before.get(r.name)
        if r.commit is None:
            if old:
                print(f"would move {r.name} from {old[:12]}: {tasks} (tree {r.tree[:12]})")
            else:
                print(f"would tag {r.name}: {tasks} (tree {r.tree[:12]})")
        elif old == r.commit:
            print(f"kept {r.name} at {old[:12]} (same commit): {tasks}")
        elif old:
            print(f"moved {r.name}: {old[:12]} -> {r.commit[:12]}: {tasks}")
        else:
            print(f"tagged {r.name} -> {r.commit[:12]}: {tasks}")
    if args.dry_run:
        print(_results_line(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
