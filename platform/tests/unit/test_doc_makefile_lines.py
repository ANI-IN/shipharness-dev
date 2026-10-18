"""A `make: *** [Makefile:N: target]` line on a course page names the line make reports today.

make reports the first recipe line of the target, so every edit above it moves the number. Captured
terminal files (`*.txt`) are records of a past run and are not checked.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
QUOTED = re.compile(r"\[Makefile:(\d+): ([\w-]+)\]")


def _recipe_lines() -> dict[str, int]:
    lines = (REPO / "Makefile").read_text(encoding="utf-8").splitlines()
    found: dict[str, int] = {}
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^([\w-]+(?: [\w-]+)*):(?!=)", line)
        if match:
            for target in match.group(1).split():
                found.setdefault(target, number + 1)
    return found


def _course_pages() -> list[Path]:
    listed = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=REPO, capture_output=True, text=True, check=False
    ).stdout.split()
    skip = ("research/", "instructor/engineering-notes/")
    return [REPO / p for p in listed if not p.startswith(skip)]


def test_quoted_makefile_lines_match_the_makefile() -> None:
    recipes = _recipe_lines()
    wrong = []
    for page in _course_pages():
        if not page.is_file():
            continue
        for number, target in QUOTED.findall(page.read_text(encoding="utf-8")):
            if recipes.get(target) != int(number):
                rel = page.relative_to(REPO).as_posix()
                wrong.append(f"{rel}: Makefile:{number}: {target} (now {recipes.get(target)})")
    assert not wrong, wrong
