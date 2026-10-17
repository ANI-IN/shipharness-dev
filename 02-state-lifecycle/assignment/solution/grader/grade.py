"""A2 grader: the visible and hidden scenarios against a state layer, plus the live-run evidence,
scored out of 100.

    uv run python 02-state-lifecycle/assignment/solution/grader/grade.py --impl <submission>
        [--visible-only] [--details] [--json <file>] [--fail-under <score>]

`--impl` is the submission: the folder that holds the `a2_state` package and the `live/` evidence,
or a folder (a cloned repository) with exactly one such folder below it (default:
assignment/starter). The scenarios run the test stand-in agent (a2_scenario/literal_agent.py),
not a model, so their scores repeat. Each scenario criterion's points are multiplied by the share
of scenarios it passes in (a half pass counts half). The live-run criterion (10 points) checks the
files in `live/` (a2_scenario/live_evidence.py) and never re-runs the model. Exit code 0, or 1
when `--fail-under` is given and the score is below it. No model calls, no network, no Docker.
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
ASSIGNMENT = HERE.parents[1]  # grader/ -> solution/ -> assignment/
for path in (ASSIGNMENT, HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from a2_hidden import HIDDEN  # noqa: E402
from a2_scenario import live_evidence  # noqa: E402
from a2_scenario.measures import CRITERIA, total_points  # noqa: E402
from a2_scenario.report import (  # noqa: E402
    ScenarioResult,
    load_layer,
    print_scenario,
    run_and_evaluate,
    shown,
)
from a2_scenario.runner import LayerFactory  # noqa: E402
from a2_scenario.scenarios import VISIBLE, Scenario  # noqa: E402

AGENT_LINE = (
    "Agent in the scenarios: the test stand-in agent (a2_scenario/literal_agent.py), "
    "deterministic, not a model."
)


@dataclass
class Report:
    results: list[ScenarioResult]
    points: dict[str, float]  # criterion key -> points earned (live_run included)
    live_problems: list[str]
    live_description: str = ""

    @property
    def score(self) -> float:
        return round(sum(self.points.values()), 1)


def grade(
    factory: LayerFactory,
    scenarios: Sequence[Scenario],
    root: Path,
    submission: Path | None = None,
) -> Report:
    results = [run_and_evaluate(factory, s, root / s.name) for s in scenarios]
    points = {}
    for index, criterion in enumerate(CRITERIA):
        share = sum(r.outcomes[index].fraction for r in results) / max(len(results), 1)
        points[criterion.key] = round(criterion.points * share, 1)
    if submission is None:
        problems = ["no submission folder given"]
    else:
        problems = live_evidence.validate(submission)
    description = live_evidence.describe(submission) if submission and not problems else ""
    points[live_evidence.LIVE_KEY] = 0.0 if problems else float(live_evidence.LIVE_POINTS)
    return Report(results, points, problems, description)


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
    if report.live_problems:
        print("Live run evidence: not valid")
        for problem in report.live_problems:
            print(f"  - {problem}")
    else:
        print(f"Live run evidence: valid ({report.live_description})")
    print()
    live = live_evidence
    rows = [(f"{c.key}: {c.title}", c.key, c.points) for c in CRITERIA]
    rows.append((f"{live.LIVE_KEY}: {live.LIVE_TITLE}", live.LIVE_KEY, live.LIVE_POINTS))
    width = max(len(title) for title, _, _ in rows)
    print(f"{'Criterion':<{width}} {'Points':>6} {'Earned':>7}")
    for title, key, points in rows:
        print(f"{title:<{width}} {points:>6} {report.points[key]:>7.1f}")
    print(f"\nScore: {report.score}/{total_points()}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A2 grader (visible and hidden scenarios).")
    parser.add_argument(
        "--impl",
        type=Path,
        default=ASSIGNMENT / "starter",
        help="submission folder (a2_state/ and live/), or a repository holding one",
    )
    parser.add_argument("--visible-only", action="store_true", help="skip the hidden scenarios")
    parser.add_argument("--details", action="store_true", help="show each session's actions")
    parser.add_argument("--json", type=Path, help="also write the result as JSON")
    parser.add_argument("--fail-under", type=float, help="exit 1 below this score")
    args = parser.parse_args(argv)
    submission = live_evidence.find_submission(args.impl)
    factory = load_layer(submission)
    scenarios = VISIBLE if args.visible_only else (*VISIBLE, *HIDDEN)
    print(
        f"A2 grade: {len(scenarios)} scenarios ({len(VISIBLE)} visible, "
        f"{len(scenarios) - len(VISIBLE)} hidden) against {shown(submission)}"
    )
    print(f"{AGENT_LINE}\n")
    root = Path(tempfile.mkdtemp(prefix="a2-grade-"))
    try:
        report = grade(factory, scenarios, root, submission)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print_report(report, args.details)
    if args.json:
        data = {
            "score": report.score,
            "points": report.points,
            "live": {"valid": not report.live_problems, "problems": report.live_problems},
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
