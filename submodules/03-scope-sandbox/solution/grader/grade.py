"""Grader for assignment A3 (make grade-assignment-3): visible + hidden tests, score out of 100.

Usage (from the repository root):
    uv run python submodules/03-scope-sandbox/solution/grader/grade.py [--impl PATH] [--json OUT]

--impl names the folder that holds the learner's `a3scope` package and `tests/` (default: the
starter). Needs no API keys and no container runtime. Exit code 0 means PASS: at least 80 points,
every out-of-scope diff rejected, and zero false positives on legitimate diffs.

Grading criteria (assignment/README.md, "Grading criteria (100 points)"):
1. Diff parsing and path matching (15): 15 x share of test_parse_* passing.
2. Diff-scope policy (45): 45 x (share of bad diffs rejected) x (share of good diffs accepted).
3. Evidence-gated status (20): 20 x (share of test_status_sets_*) x (share of test_status_keeps_*).
4. Sandbox history rule (10): 10 x (share of test_rule_denies_*) x (share of test_rule_allows_*).
5. Denial test proves the denial (10): passes with the rule (4), fails without it (4, only if it
   passes with it), goes through check_command or PolicySandbox (2).
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
SUBMODULE = GRADER.parents[1]
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
    "scope": ("2 Diff-scope policy", 45.0),
    "status": ("3 Evidence-gated status", 20.0),
    "rule": ("4 Sandbox history rule", 10.0),
    "proof": ("5 Denial test proves the denial", 10.0),
}
PROOF_POINTS = {"passes": 4.0, "fails_without_rule": 4.0, "uses_policy_code": 2.0}


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
    groups: dict[str, dict[str, int]], proof: dict[str, bool], zeroed: set[str]
) -> dict[str, dict[str, Any]]:
    raw = {
        "parse": 15.0 * _share(groups["parse"]),
        "scope": 45.0 * _share(groups["bad"]) * _share(groups["good"]),
        "status": 20.0 * _share(groups["sets"]) * _share(groups["keeps"]),
        "rule": 10.0 * _share(groups["denies"]) * _share(groups["allows"]),
        "proof": sum(
            points
            for key, points in PROOF_POINTS.items()
            if proof[key] and (key != "fails_without_rule" or proof["passes"])
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
    return out


def grade(impl: Path) -> dict[str, Any]:
    visible, _ = check.run_pytest([check.VISIBLE], impl)
    hidden, hidden_output = check.run_pytest([HIDDEN], impl)
    cases = visible + hidden
    groups = check.group_counts(cases)
    proof, _ = check.denial_test_checks(impl)
    banned = forbidden_imports(impl)
    zeroed = {c for module in banned for c in SERVES.get(module, ())}
    criteria = score(groups, proof, zeroed)
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
        "passed": total >= PASS_MARK and all(zero_tolerance.values()),
        "zero_tolerance": zero_tolerance,
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
    lines.append(f"  {'Total':<50} {'':>9} {result['total']:>6.1f} / 100")
    zt = result["zero_tolerance"]
    lines.append(
        f"  Every out-of-scope diff rejected: {_yes(zt['all_bad_rejected'])}; "
        f"zero false positives: {_yes(zt['zero_false_positives'])}"
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
        "and zero false positives)"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--impl", type=Path, default=check.STARTER, help="folder holding a3scope/")
    parser.add_argument("--json", type=Path, default=None, help="also write the result as JSON")
    args = parser.parse_args(argv)
    impl = args.impl.resolve()
    if not (impl / "a3scope").is_dir():
        print(f"x no a3scope package in {impl}")
        return 2
    result = grade(impl)
    print(report(result))
    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
