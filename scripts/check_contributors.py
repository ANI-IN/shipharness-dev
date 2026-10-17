"""Check that every commit in a repository is by ANI-IN alone (private build tool, not shipped).

    uv run python scripts/check_contributors.py [REPO]     # default: this repository

Every commit reachable from any branch, tag, or HEAD must have ANI-IN as author and committer,
with the address 44803072+ANI-IN@users.noreply.github.com, and its message must carry no
Co-authored-by trailer and no "Generated with" attribution. Prints "Contributors: PASS" or
"Contributors: FAIL" and one line per offending commit. Read-only: it never rewrites history.
Exit 0 on PASS, 1 on FAIL, 2 when REPO is not a git repository. scripts/make_release.py runs the
same commit check on the repository it builds.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

NAME = "ANI-IN"
EMAIL = "44803072+ANI-IN@users.noreply.github.com"
EXPECTED = f"{NAME} <{EMAIL}>"
REPO = Path(__file__).resolve().parents[1]

_COAUTHOR = re.compile(r"^\s*co-authored-by\s*:", re.I | re.M)
# "Generated with ..." as its own line (an emoji may come first), or "Generated with [Claude" or
# "Generated with Claude" anywhere in the message.
_GENERATED = re.compile(r"^\W*generated with\b|generated with \[?claude", re.I | re.M)
_FIELD, _RECORD = "\x1f", "\x1e"


class NotARepository(RuntimeError):
    pass


@dataclass(frozen=True)
class CommitProblem:
    sha: str
    subject: str
    problems: list[str]

    def line(self) -> str:
        return f"{self.sha[:12]} {self.subject[:60]!r}: {'; '.join(self.problems)}"


def message_problems(message: str) -> list[str]:
    """Attribution trailers in a commit message."""
    out = []
    if _COAUTHOR.search(message):
        out.append("Co-authored-by trailer")
    if _GENERATED.search(message):
        out.append("Generated with trailer")
    return out


def _log(repo: Path) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    fmt = _FIELD.join(["%H", "%an <%ae>", "%cn <%ce>", "%s", "%B"]) + _RECORD
    done = subprocess.run(
        ["git", "log", "--all", "--no-color", f"--format={fmt}"],
        cwd=repo,
        capture_output=True,
        env=env,
        check=False,
    )
    if done.returncode != 0:
        raise NotARepository(f"{repo}: not a git repository or no commits")
    return done.stdout.decode("utf-8", errors="replace")


def commits(repo: Path) -> list[tuple[str, str, str, str, str]]:
    """(sha, author, committer, subject, message) for every commit reachable from any ref."""
    out = []
    for record in _log(repo).split(_RECORD):
        record = record.strip("\n")
        if record:
            sha, author, committer, subject, message = record.split(_FIELD, 4)
            out.append((sha, author, committer, subject, message))
    return out


def commit_problems(repo: Path) -> list[CommitProblem]:
    """Every commit whose author or committer is not ANI-IN, or whose message has a trailer."""
    found = []
    for sha, author, committer, subject, message in commits(repo):
        problems = []
        if author != EXPECTED:
            problems.append(f"author {author}")
        if committer != EXPECTED:
            problems.append(f"committer {committer}")
        problems += message_problems(message)
        if problems:
            found.append(CommitProblem(sha, subject, problems))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_contributors", description=__doc__.split("\n")[0])
    parser.add_argument("repo", nargs="?", type=Path, default=REPO)
    args = parser.parse_args(argv)
    try:
        total = len(commits(args.repo))
        found = commit_problems(args.repo)
    except NotARepository as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    noun = "commit" if total == 1 else "commits"
    if not found:
        print(f"Contributors: PASS ({total} {noun}, every author and committer {EXPECTED})")
        return 0
    print(f"Contributors: FAIL ({len(found)} of {total} {noun}; expected {EXPECTED})")
    kinds = Counter(p for c in found for p in c.problems)
    for problem, n in kinds.most_common():
        print(f"  {n:>5}  {problem}")
    print("offending commits:")
    for commit in found:
        print(f"  {commit.line()}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
