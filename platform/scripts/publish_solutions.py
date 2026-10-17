"""Assignment solutions and the public course repository: nothing is ever published.

    uv run python platform/scripts/publish_solutions.py --assignment 1 --dry-run

Owner decision (release brief): the public repository ANI-IN/harness-engineering-session never
gets a `solution/` folder or assignment grader tests, also not after a review session. The dry
run lists what stays private for one assignment (`submodules/0N-*/solution/` at --ref);
--publish refuses with exit 2 and writes nothing. scripts/make_release.py enforces the same rule
for the release build (its leak check fails on any solution/ or grader path).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file())
PUBLIC_REPO = "ANI-IN/harness-engineering-session"
RULE = (
    "the public repository never gets a solution/ folder or assignment grader tests "
    "(owner decision)"
)


class PublishError(ValueError):
    pass


@dataclass(frozen=True)
class Plan:
    assignment: int
    folder: str
    publish: list[str]  # always empty (owner decision)
    withheld: list[str]


def solution_folder(paths: Iterable[str], assignment: int) -> str:
    prefix = f"submodules/{assignment:02d}-"
    modules = sorted({p.split("/")[1] for p in paths if p.startswith(prefix)})
    if not modules:
        raise PublishError(f"no submodule for assignment {assignment} ({prefix}*)")
    if len(modules) > 1:
        raise PublishError(f"more than one submodule for assignment {assignment}: {modules}")
    return f"submodules/{modules[0]}/solution/"


def plan(paths: Iterable[str], assignment: int) -> Plan:
    paths = sorted(paths)
    folder = solution_folder(paths, assignment)
    inside = [p for p in paths if p.startswith(folder)]
    if not inside:
        raise PublishError(f"no solution files under {folder}")
    return Plan(assignment, folder, [], inside)


def tracked_paths(repo: Path, ref: str) -> list[str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    done = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--name-only", "--full-tree", ref],
        cwd=repo,
        capture_output=True,
        env=env,
        check=False,
    )
    if done.returncode != 0:
        raise PublishError(done.stderr.decode("utf-8", errors="replace").strip())
    return [p for p in done.stdout.decode("utf-8").split("\0") if p]


def render(p: Plan) -> str:
    lines = [
        f"assignment {p.assignment}: publishes nothing to {PUBLIC_REPO}: {RULE}",
        f"{len(p.withheld)} file(s) under {p.folder} stay private:",
        *(f"  private: {path}" for path in p.withheld),
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="publish_solutions",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--assignment", type=int, required=True, choices=range(1, 10))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="list what stays private (default)")
    mode.add_argument("--publish", action="store_true", help="refused (owner decision)")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args(argv)
    try:
        result = plan(tracked_paths(args.repo, args.ref), args.assignment)
    except PublishError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render(result))
    if args.publish:
        print(f"refused: solutions are never published: {RULE}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
