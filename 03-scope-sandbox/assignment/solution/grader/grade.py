"""Grader for assignment A3 (make grade-assignment-3): visible + hidden tests, score out of 100.

Usage (from the repository root):
    uv run python 03-scope-sandbox/assignment/solution/grader/grade.py [--impl PATH] [--live DIR]
        [--json OUT]

--impl names the learner's submission folder: it holds the `a3scope` package, `tests/`, and the
live evidence in `live/` (default: the starter). --live overrides where the live evidence is.
Needs no API keys, no container runtime, and calls no model. Exit code 0 means PASS: at least 80
points, every out-of-scope diff rejected, zero false positives on legitimate diffs, and valid live
evidence.

Grading criteria (assignment/README.md, "Grading criteria (100 points)"):
1. Diff parsing and path matching (15): 15 x share of test_parse_* passing.
2. Diff-scope policy (40): 40 x (share of bad diffs rejected) x (share of good diffs accepted).
3. Evidence-gated status (15): 15 x (share of test_status_sets_*) x (share of test_status_keeps_*).
4. Sandbox history rule (10): 10 x (share of test_rule_denies_*) x (share of test_rule_allows_*).
5. Denial test proves the denial (10): passes with the rule (4), fails without it (4, only if it
   passes with it), goes through check_command or PolicySandbox (2).
6. Live A/B evidence (10): live/ holds a valid live demo-3 A/B on F3 (6: ScoreRecord schema,
   ids, model, caps, both arms, checkpoint_sha; assignment/live.py verify), and the learner's
   policy re-run on the included diffs reproduces both verdict files (4, only with valid
   evidence). Valid evidence is also a pass condition.
A module that imports the reference implementation (shipharness.harness, .ab, .runner, .checks)
scores 0 on the criteria it serves.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

GRADER = Path(__file__).resolve().parent
SUBMODULE = GRADER.parents[2]  # grader/ -> solution/ -> assignment/ -> the section
sys.path.insert(0, str(SUBMODULE / "assignment"))

import check  # noqa: E402  (assignment/check.py: shared pytest runner and grouping)

HIDDEN = GRADER / "hidden"
PASS_MARK = 80.0
FORBIDDEN = ("shipharness.harness", "shipharness.ab", "shipharness.runner", "shipharness.checks")
# Module -> criteria it serves (a forbidden import there zeroes these criteria).
SERVES: dict[str, tuple[str, ...]] = {
    "diffparse": ("parse", "scope"),
    "scope": ("parse", "scope"),
    "status": ("status",),
    "policy": ("rule", "proof"),
}
TITLES: dict[str, tuple[str, float]] = {
    "parse": ("1 Diff parsing and path matching", 15.0),
    "scope": ("2 Diff-scope policy", 40.0),
    "status": ("3 Evidence-gated status", 15.0),
    "rule": ("4 Sandbox history rule", 10.0),
    "proof": ("5 Denial test proves the denial", 10.0),
    "live": ("6 Live A/B evidence (live/)", 10.0),
}
PROOF_POINTS = {"passes": 4.0, "fails_without_rule": 4.0, "uses_policy_code": 2.0}
LIVE_POINTS = {"evidence": 6.0, "verdicts": 4.0}


def forbidden_imports(impl: Path) -> dict[str, list[str]]:
    """module stem -> forbidden modules it imports."""
    found: dict[str, list[str]] = {}
    for path in sorted((impl / "a3scope").glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        names = [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        names += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        bad = sorted({n for n in names if n.startswith(FORBIDDEN)})
        if bad:
            found[path.stem] = bad
    return found


def _share(group: dict[str, int]) -> float:
    return group["passed"] / group["total"] if group["total"] else 0.0


def score(
    groups: dict[str, dict[str, int]],
    proof: dict[str, bool],
    zeroed: set[str],
    live: dict[str, bool],
) -> dict[str, dict[str, Any]]:
    raw = {
        "parse": 15.0 * _share(groups["parse"]),
        "scope": 40.0 * _share(groups["bad"]) * _share(groups["good"]),
        "status": 15.0 * _share(groups["sets"]) * _share(groups["keeps"]),
        "rule": 10.0 * _share(groups["denies"]) * _share(groups["allows"]),
        "proof": sum(
            points
            for key, points in PROOF_POINTS.items()
            if proof[key] and (key != "fails_without_rule" or proof["passes"])
        ),
        "live": sum(
            points
            for key, points in LIVE_POINTS.items()
            if live[key] and (key != "verdicts" or live["evidence"])
        ),
    }
    out: dict[str, dict[str, Any]] = {}
    for key, points in raw.items():
        out[key] = {
            "title": TITLES[key][0],
            "max": TITLES[key][1],
            "points": 0.0 if key in zeroed else round(points, 1),
            "zeroed": key in zeroed,
        }
    out["proof"]["checks"] = proof
    out["live"]["checks"] = live
    return out


def grade(impl: Path, live_dir: Path | None = None) -> dict[str, Any]:
    visible, _ = check.run_pytest([check.VISIBLE], impl)
    hidden, hidden_output = check.run_pytest([HIDDEN], impl)
    cases = visible + hidden
    groups = check.group_counts(cases)
    proof, _ = check.denial_test_checks(impl)
    banned = forbidden_imports(impl)
    zeroed = {c for module in banned for c in SERVES.get(module, ())}
    live = check.live_verify(impl, live_dir)
    live_checks = {"evidence": bool(live["evidence_ok"]), "verdicts": bool(live["verdicts_ok"])}
    criteria = score(groups, proof, zeroed, live_checks)
    total = round(sum(c["points"] for c in criteria.values()), 1)
    zero_tolerance = {
        "all_bad_rejected": groups["bad"]["total"] > 0
        and groups["bad"]["passed"] == groups["bad"]["total"],
        "zero_false_positives": groups["good"]["total"] > 0
        and groups["good"]["passed"] == groups["good"]["total"],
    }
    return {
        "impl": check.shown(impl),
        "total": total,
        "passed": total >= PASS_MARK and all(zero_tolerance.values()) and live_checks["evidence"],
        "zero_tolerance": zero_tolerance,
        "live": live,
        "groups": groups,
        "criteria": criteria,
        "forbidden_imports": [f"a3scope/{m}.py imports {', '.join(v)}" for m, v in banned.items()],
        "failed_tests": [
            f"{c.name}: {c.message.splitlines()[0] if c.message else ''}"
            for c in cases
            if not c.passed
        ],
        "hidden_ran": bool(hidden),
        "hidden_output_tail": "" if hidden else hidden_output[-1500:],
    }


def _yes(flag: bool) -> str:
    return "yes" if flag else "no"


def report(result: dict[str, Any]) -> str:
    groups, criteria = result["groups"], result["criteria"]
    lines = [f"A3 grade: {result['impl']}", f"  {'criterion':<50} {'tests':>9} {'points':>14}"]

    def head(key: str) -> None:
        c = criteria[key]
        note = "  (0: imports the reference implementation)" if c["zeroed"] else ""
        lines.append(f"  {c['title']:<50} {'':>9} {c['points']:>6.1f} / {c['max']:.0f}{note}")

    def sub(key: str) -> None:
        g = groups[key]
        lines.append(f"      {check.GROUPS[key][1]:<46} {g['passed']:>4}/{g['total']}")

    head("parse")
    sub("parse")
    head("scope")
    sub("bad")
    sub("good")
    head("status")
    sub("sets")
    sub("keeps")
    head("rule")
    sub("denies")
    sub("allows")
    head("proof")
    proof = criteria["proof"]["checks"]
    lines.append(f"      {'passes with the rule (4)':<46} {_yes(proof['passes']):>9}")
    lines.append(
        f"      {'fails with the rule removed (4)':<46} {_yes(proof['fails_without_rule']):>9}"
    )
    uses = _yes(proof["uses_policy_code"])
    lines.append(f"      {'uses check_command or PolicySandbox (2)':<46} {uses:>9}")
    head("live")
    live = criteria["live"]["checks"]
    lines.append(f"      {'evidence valid (6)':<46} {_yes(live['evidence']):>9}")
    lines.append(
        f"      {'verdicts reproduced by your policy (4)':<46} {_yes(live['verdicts']):>9}"
    )
    for problem in [*result["live"]["evidence_problems"], *result["live"]["verdict_problems"]][:8]:
        lines.append(f"        - {problem}")
    lines.append(f"  {'Total':<50} {'':>9} {result['total']:>6.1f} / 100")
    zt = result["zero_tolerance"]
    lines.append(
        f"  Every out-of-scope diff rejected: {_yes(zt['all_bad_rejected'])}; "
        f"zero false positives: {_yes(zt['zero_false_positives'])}; "
        f"live evidence valid: {_yes(live['evidence'])}"
    )
    for item in result["forbidden_imports"]:
        lines.append(f"  x forbidden import: {item}")
    if not result["hidden_ran"]:
        lines.append(
            "  x the hidden tests did not run; pytest said:\n" + result["hidden_output_tail"]
        )
    failed = result["failed_tests"]
    if failed:
        lines.append(f"  Failed tests ({len(failed)}; first 15):")
        lines += [f"    - {name}" for name in failed[:15]]
    verdict = "PASS" if result["passed"] else "FAIL"
    lines.append(
        f"Result: {verdict} (needs >= {PASS_MARK:.0f} points, every out-of-scope diff rejected, "
        "zero false positives, and valid live evidence)"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--impl", type=Path, default=check.STARTER, help="submission folder: a3scope/, live/"
    )
    parser.add_argument("--live", type=Path, default=None, help="live evidence (default: live/)")
    parser.add_argument("--json", type=Path, default=None, help="also write the result as JSON")
    args = parser.parse_args(argv)
    impl = args.impl.resolve()
    if not (impl / "a3scope").is_dir():
        print(f"x no a3scope package in {impl}")
        return 2
    result = grade(impl, args.live.resolve() if args.live else None)
    print(report(result))
    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
