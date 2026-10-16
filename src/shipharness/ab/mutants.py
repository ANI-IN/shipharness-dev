"""Referee-set mutants for a task's `mutant_set` (DESIGN §7: the two sets are disjoint)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog

MUTANT_DIR = Path("teamtrack") / "mutants"


def load_referee_mutants(mutant_set: str, course_repo: Path) -> list[Any]:
    """`mutant_set` is a comma-separated list of module names (`app.services.issues`, resolved to
    `teamtrack/mutants/<name>.jsonl`) or repo-relative `.jsonl` paths. Only the referee set is
    returned; filter-set mutants are never used to judge an arm. Records are validated, but not
    matched against source lines here: the arm may have changed a line, which the mutant runner
    reports as an error for that mutant."""
    from shipharness.filters import load_mutants

    mutants: list[Any] = []
    for token in (t.strip() for t in mutant_set.split(",")):
        if not token:
            continue
        rel = Path(token) if token.endswith(".jsonl") else MUTANT_DIR / f"{token}.jsonl"
        path = Path(course_repo) / rel
        if not path.is_file():
            raise ValueError(f"unknown mutant set {token!r}: {rel.as_posix()} does not exist")
        mutants.extend(m for m in load_mutants(path, None) if m.set == "referee")
    return mutants


def referee_mutants(
    mutant_set: str, course_repo: Path, given: list[Any] | None = None
) -> list[Any]:
    """Mutants that judge one task, for every path that runs the referee (A/B, swap test, replay,
    experiments). `given` wins when set. A missing set is logged and scored 0/0 instead of
    aborting a live run; dataset validation (M5) checks that every mutant set exists."""
    if given:
        return list(given)
    try:
        return load_referee_mutants(mutant_set, course_repo)
    except ValueError as exc:
        structlog.get_logger(__name__).warning("referee mutants unavailable", reason=str(exc))
        return []
