"""A2 grader: the visible and hidden scenarios against a state layer, scored out of 100.

    uv run python submodules/02-state-lifecycle/solution/grader/grade.py [--impl <folder>]
        [--visible-only] [--details] [--json <file>] [--fail-under <score>]

`--impl` is the folder that holds the `a2_state` package (default: assignment/starter). Each
criterion's points are multiplied by the share of scenarios it passes in (a half pass counts
half). Exit code 0, or 1 when `--fail-under` is given and the score is below it. No model calls,
no network, no Docker.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSIGNMENT = HERE.parents[1] / "assignment"
for path in (ASSIGNMENT, HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from a2_hidden import HIDDEN  # noqa: E402
from a2_scenario.measures import CRITERIA, total_points  # noqa: E402
from a2_scenario.report import (  # noqa: E402
    ScenarioResult,
    load_layer,
    print_scenario,
    run_and_evaluate,
)
from a2_scenario.runner import LayerFactory  # noqa: E402
from a2_scenario.scenarios import VISIBLE, Scenario  # noqa: E402


@dataclass
class Report:
    results: list[ScenarioResult]
    points: dict[str, float]  # criterion key -> points earned

    @property
    def score(self) -> float:
        return round(sum(self.points.values()), 1)


def grade(factory: LayerFactory, scenarios: Sequence[Scenario], root: Path) -> Report:
    results = [run_and_evaluate(factory, s, root / s.name) for s in scenarios]
    points = {}
    for index, criterion in enumerate(CRITERIA):
        share = sum(r.outcomes[index].fraction for r in results) / max(len(results), 1)
        points[criterion.key] = round(criterion.points * share, 1)
    return Report(results, points)


def print_report(report: Report, details: bool) -> None:
    for result in report.results:
        failing = [o for o in result.outcomes if o.fraction < 1.0]
        status = "PASS" if not failing else f"{len(failing)} criteria not met"
        print(f"{result.scenario.name}: {status}")
        if details:
            print_scenario(result, details=True)
        else:
            for outcome in failing:
                print(f"  {outcome.key}: {outcome.detail}")
        if result.error and not details:
            print(f"  ERROR: {result.error.strip().splitlines()[-1]}")
    print()
    titles = {c.key: f"{c.key}: {c.title}" for c in CRITERIA}
    width = max(len(t) for t in titles.values())
    print(f"{'Criterion':<{width}} {'Points':>6} {'Earned':>7}")
    for criterion in CRITERIA:
        earned = report.points[criterion.key]
        print(f"{titles[criterion.key]:<{width}} {criterion.points:>6} {earned:>7.1f}")
    print(f"\nScore: {report.score}/{total_points()}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A2 grader (visible and hidden scenarios).")
    parser.add_argument("--impl", type=Path, default=ASSIGNMENT / "starter")
    parser.add_argument("--visible-only", action="store_true", help="skip the hidden scenarios")
    parser.add_argument("--details", action="store_true", help="show each session's actions")
    parser.add_argument("--json", type=Path, help="also write the result as JSON")
    parser.add_argument("--fail-under", type=float, help="exit 1 below this score")
    args = parser.parse_args(argv)
    factory = load_layer(args.impl)
    scenarios = VISIBLE if args.visible_only else (*VISIBLE, *HIDDEN)
    print(
        f"A2 grade: {len(scenarios)} scenarios ({len(VISIBLE)} visible, "
        f"{len(scenarios) - len(VISIBLE)} hidden) against {args.impl}\n"
    )
    root = Path(tempfile.mkdtemp(prefix="a2-grade-"))
    try:
        report = grade(factory, scenarios, root)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print_report(report, args.details)
    if args.json:
        data = {
            "score": report.score,
            "points": report.points,
            "scenarios": [
                {
                    "name": r.scenario.name,
                    "passed": r.passed,
                    "outcomes": {o.key: o.fraction for o in r.outcomes},
                }
                for r in report.results
            ],
        }
        args.json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if args.fail_under is not None and report.score < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
