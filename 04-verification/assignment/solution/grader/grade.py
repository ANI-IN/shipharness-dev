"""Grader for assignment A4: visible + hidden tests, scored against the grading criteria (100).

    uv run python submodules/04-verification/solution/grader/grade.py [--impl <submission>]

`--impl` is the submission: the folder that holds `a4_verification/`, `tests/`, `skill/`,
`portfolio/`, and `live/` (default: the reference solution). A checkout of the whole course repo
also works: its `submodules/04-verification/assignment/starter/` folder is graded then. Each test
carries `@pytest.mark.criterion("<id>")`; a criterion's points are split evenly over its tests.
Nothing here calls a model, Docker, or the network: R8 runs in process on TeamTrack copies, the
portfolio is checked for presence and structure, and the live evidence in `live/` (testgen report
and A/B score records) is validated as files, never re-run.

Exit codes: 0 when grading ran (whatever the score), 1 when the grader could not run the tests.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

GRADER = Path(__file__).resolve().parent
SOLUTION = GRADER.parent
ASSIGNMENT = SOLUTION.parent / "assignment"
# Where the implementation folder sits inside a checkout of the course repo.
IMPL_IN_REPO = Path("submodules/04-verification/assignment/starter")
VISIBLE = ASSIGNMENT / "visible_tests"
HIDDEN = GRADER / "hidden_tests"
sys.path.insert(0, str(VISIBLE))

from a4_runner import Outcome, RunError, run_tests  # noqa: E402


@dataclass(frozen=True)
class Criterion:
    id: str
    title: str
    points: int


# The README's "Grading criteria (100 points)" table lists the same rows.
CRITERIA: tuple[Criterion, ...] = (
    Criterion("R8-interface", "R8 registered through shipharness; runner, CLI, progress", 5),
    Criterion("R8-visible", "R8 finds the visible seeded violations", 9),
    Criterion("R8-hidden", "R8 finds the hidden seeded violations", 17),
    Criterion("R8-no-false-positives", "R8 reports nothing a correct build does not violate", 8),
    Criterion("R8-baseline", "Stable detail keys: baseline deltas and exemptions work", 7),
    Criterion("F6-interface", "Filter 6 follows the Filter protocol and runs in the pipeline", 4),
    Criterion("F6-visible", "Filter 6 on the visible candidate tests", 6),
    Criterion("F6-hidden", "Filter 6 on the hidden candidate tests", 13),
    Criterion("own-tests", "At least 8 own tests, all passing", 5),
    Criterion("skill", "Own skill: valid, renamed, placeholders replaced", 6),
    Criterion("portfolio-evidence", "Evidence report: sections, commands, results table", 5),
    Criterion("portfolio-langsmith", "LangSmith page: trace links of the A/B and command", 2),
    Criterion("portfolio-case-study", "Case study: sections, one page", 3),
    Criterion("live-evidence", "Live testgen report with filter 6 and F4 A/B score records", 10),
)


@dataclass(frozen=True)
class CriterionScore:
    criterion: Criterion
    passed: int
    total: int

    @property
    def earned(self) -> float:
        return self.criterion.points * self.passed / self.total if self.total else 0.0


def score(outcomes: list[Outcome]) -> list[CriterionScore]:
    by_id = {c.id: c for c in CRITERIA}
    unknown = sorted({o.criterion for o in outcomes} - set(by_id))
    if unknown:
        raise ValueError(f"tests name criteria the grader does not know: {unknown}")
    scores = []
    for criterion in CRITERIA:
        mine = [o for o in outcomes if o.criterion == criterion.id]
        scores.append(CriterionScore(criterion, sum(o.passed for o in mine), len(mine)))
    return scores


def _points(value: float) -> str:
    text = f"{value:.1f}"
    return text[:-2] if text.endswith(".0") else text


def format_report(scores: list[CriterionScore], outcomes: list[Outcome], impl: Path) -> str:
    lines = [f"A4 grade for {impl}", ""]
    lines.append(f"{'Criterion':<24} {'Points':>11}  Tests")
    for s in scores:
        earned = f"{_points(s.earned)}/{s.criterion.points}"
        note = "" if s.total else "  (no tests found: grader error)"
        lines.append(f"{s.criterion.id:<24} {earned:>11}  {s.passed}/{s.total}{note}")
        for o in outcomes:
            if o.criterion == s.criterion.id and not o.passed:
                lines.append(f"    FAIL {o.name}: {o.message}")
    total = sum(s.earned for s in scores)
    lines += ["", f"Score: {_points(total)}/100"]
    return "\n".join(lines)


def resolve_impl(path: Path) -> Path:
    """The implementation folder of a submission: `path` itself, or the starter folder when
    `path` is a checkout of the course repo (it has no `a4_verification/` at its top)."""
    path = path.resolve()
    nested = path / IMPL_IN_REPO
    if not (path / "a4_verification").is_dir() and (nested / "a4_verification").is_dir():
        return nested
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grade.py", description=__doc__)
    parser.add_argument("--impl", type=Path, default=SOLUTION)
    args = parser.parse_args(argv)
    impl = resolve_impl(args.impl)
    try:
        outcomes, _output = run_tests(impl, [VISIBLE, HIDDEN])
        scores = score(outcomes)
    except (RunError, ValueError) as exc:
        print(f"ERROR grader could not run: {exc}")
        return 1
    print(format_report(scores, outcomes, impl))
    print("Cost: $0.000000 (no model calls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
