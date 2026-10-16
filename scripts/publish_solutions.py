"""Publish one assignment's reference solution to the learner repository (stub: dry run only).

    uv run python scripts/publish_solutions.py --assignment 1 --dry-run
    uv run python scripts/publish_solutions.py --assignment 1 --dry-run --date 2026-11-03

Run after the assignment's review session. The release is the assignment's `solution/` folder
(`submodules/0N-*/solution/` at --ref) without hidden-case data: nothing under
`solution/grader/hidden/`, and no path with a folder or file named `hidden`, `hidden_*`, or
`hidden-*`. Hidden cases stay private so they can be reused with the next cohort. The learner
repository would get the files under the same paths in one commit, tagged
`solutions-a<N>-<date>`.

Only the dry run exists: --publish prints the same plan and exits 2 without writing anything.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEARNER_REPO = "ANI-IN/shipharness"
_HIDDEN = re.compile(r"^hidden(?:[-_.].*)?$")


class PublishError(ValueError):
    pass


@dataclass(frozen=True)
class Plan:
    assignment: int
    folder: str
    publish: list[str]
    withheld: list[str]
    tag: str


def tag_name(assignment: int, date: dt.date) -> str:
    return f"solutions-a{assignment}-{date.isoformat()}"


def is_hidden_case(rel: str) -> bool:
    """True for hidden-case data: any folder or file (relative to solution/) named `hidden`,
    `hidden_*`, `hidden-*`, or `hidden.*`."""
    return any(_HIDDEN.match(part) for part in rel.split("/"))


def solution_folder(paths: Iterable[str], assignment: int) -> str:
    prefix = f"submodules/{assignment:02d}-"
    modules = sorted({p.split("/")[1] for p in paths if p.startswith(prefix)})
    if not modules:
        raise PublishError(f"no submodule for assignment {assignment} ({prefix}*)")
    if len(modules) > 1:
        raise PublishError(f"more than one submodule for assignment {assignment}: {modules}")
    return f"submodules/{modules[0]}/solution/"


def plan(paths: Iterable[str], assignment: int, date: dt.date) -> Plan:
    paths = sorted(paths)
    folder = solution_folder(paths, assignment)
    inside = [p for p in paths if p.startswith(folder)]
    if not inside:
        raise PublishError(f"no solution files under {folder}")
    withheld = [p for p in inside if is_hidden_case(p[len(folder) :])]
    publish = [p for p in inside if p not in withheld]
    return Plan(assignment, folder, publish, withheld, tag_name(assignment, date))


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
        f"assignment {p.assignment}: {p.folder} -> {LEARNER_REPO} (same paths)",
        f"tag: {p.tag}",
        f"would publish {len(p.publish)} file(s):",
        *(f"  {path}" for path in p.publish),
        f"withheld (hidden cases, reused across cohorts): {len(p.withheld)} file(s)",
        *(f"  withheld: {path}" for path in p.withheld),
        "steps: copy the files into a clean checkout of the learner repo, commit as ANI-IN "
        f"('solutions: assignment {p.assignment}'), tag {p.tag}, push branch and tag",
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
    mode.add_argument("--dry-run", action="store_true", help="print the plan (the default)")
    mode.add_argument("--publish", action="store_true", help="not implemented: prints the plan")
    parser.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args(argv)
    try:
        result = plan(tracked_paths(args.repo, args.ref), args.assignment, args.date)
    except PublishError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render(result))
    if args.publish:
        print("publishing is not implemented: nothing was written or pushed", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
