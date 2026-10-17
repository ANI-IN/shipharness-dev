"""Assignment solutions and the public course repository: what ships and what stays private.

    uv run python platform/scripts/publish_solutions.py --assignment 1 --dry-run

Owner message 14 (reverses the earlier rule): the public repository ANI-IN/harness-engineering-
session includes every `section-N-*/assignment/solution/` folder (code, solution notes, captured
outputs, live evidence), except the graders (`grader/`) and hidden grader cases (`hidden/`),
which stay private. The dry run lists both groups for one assignment at --ref. The release build
(platform/scripts/make_release.py) is what ships them; --publish refuses with exit 2 and writes
nothing, since this script never pushes.
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
    "the public repository gets each assignment's solution/ folder, except its graders and hidden "
    "grader cases (owner message 14)"
)
PRIVATE_PARTS = ("grader", "hidden")


class PublishError(ValueError):
    pass


@dataclass(frozen=True)
class Plan:
    assignment: int
    folder: str
    publish: list[str]  # shipped by the release build
    withheld: list[str]  # graders and hidden grader cases


def solution_folder(paths: Iterable[str], assignment: int) -> str:
    prefix = f"section-{assignment}-"
    sections = sorted({p.split("/")[0] for p in paths if p.startswith(prefix) and "/" in p})
    if not sections:
        raise PublishError(f"no section folder for assignment {assignment} ({prefix}*)")
    if len(sections) > 1:
        raise PublishError(f"more than one section folder for assignment {assignment}: {sections}")
    return f"{sections[0]}/assignment/solution/"


def private(path: str) -> bool:
    return any(part in PRIVATE_PARTS for part in path.split("/")[:-1])


def plan(paths: Iterable[str], assignment: int) -> Plan:
    paths = sorted(paths)
    folder = solution_folder(paths, assignment)
    inside = [p for p in paths if p.startswith(folder)]
    if not inside:
        raise PublishError(f"no solution files under {folder}")
    return Plan(
        assignment,
        folder,
        [p for p in inside if not private(p)],
        [p for p in inside if private(p)],
    )


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
        f"assignment {p.assignment}: {RULE}",
        f"{len(p.publish)} file(s) under {p.folder} ship with the release to {PUBLIC_REPO}:",
        *(f"  public: {path}" for path in p.publish),
        f"{len(p.withheld)} file(s) stay private:",
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
    mode.add_argument("--dry-run", action="store_true", help="list what ships (default)")
    mode.add_argument("--publish", action="store_true", help="refused: the release build ships")
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
        print(
            "refused: this script never pushes; the release build "
            "(platform/scripts/make_release.py) ships the solution folders",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
