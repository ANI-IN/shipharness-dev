"""Grader for assignment A1 (Instructions): visible checks plus hidden checks, score out of 100.

Usage (from the repository root):

    uv run python submodules/01-instructions/solution/grader/grade.py [--work DIR]
        [--allow-pending] [--min-score N]

Visible checks are the self-check (`assignment/check.py`). Hidden checks, kept here and not in the
starter:

- rule coverage measured by the reference checker on the learner's tree (every active rule of the
  original defined once, with at least half of its content words), and the original unchanged;
- the unchanged visible checker tests run against the learner's check_docs.py;
- the learner's checker on the reference tree (no false alarms) and on the reference tree with three
  injected faults (each one found);
- the learner's checker on eleven hidden cases (hidden/checker_cases.py).

No API keys, no Docker, no model calls. The A/B part is graded from the structure of the learner's
committed ab-report.md, never by re-running models. Exit 0 once a score is printed, or 1 when
--min-score is given and the score is below it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

GRADER = Path(__file__).resolve().parent
SOLUTION = GRADER.parent
A1 = SOLUTION.parent
REFERENCE_WORK = SOLUTION / "work"
REFERENCE_CHECKER = REFERENCE_WORK / "checker" / "check_docs.py"
PRISTINE_TESTS = REFERENCE_WORK / "checker" / "test_check_docs.py"
ORIGINAL_SHA256 = "a5de2a450b5896b22f4f1f17a2900f0bcca96f4b8553d4c1f632fa503fc5cfab"

sys.path.insert(0, str(GRADER))
from hidden.checker_cases import CASES, Case  # noqa: E402


def _load(name: str, path: Path) -> ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


check = _load("a1_check", A1 / "assignment" / "check.py")
reference = _load("a1_reference_checker", REFERENCE_CHECKER)
ORIGINAL: Path = check.ORIGINAL
PRODUCT: Path = check.PRODUCT

CRITERIA = {
    "A Map and layout": 15,
    "B Rule coverage": 25,
    "C Skill": 15,
    "D Docs checker": 30,
    "E A/B report": 15,
}
VISIBLE_POINTS = {
    "layout": ("A Map and layout", 5),
    "map-length": ("A Map and layout", 3),
    "map-reach": ("A Map and layout", 4),
    "no-overwrite": ("A Map and layout", 3),
    "skill-valid": ("C Skill", 5),
    "skill-frontmatter": ("C Skill", 2),
    "skill-sections": ("C Skill", 3),
    "skill-linked": ("C Skill", 2),
    "skill-cites": ("C Skill", 3),
    "checker-tests": ("D Docs checker", 2),
    "checker-clean": ("D Docs checker", 2),
    "report-sections": ("E A/B report", 3),
    "report-command": ("E A/B report", 3),
    "report-results": ("E A/B report", 4),
    "report-links": ("E A/B report", 2),
    "report-cost": ("E A/B report", 1),
    "report-reading": ("E A/B report", 2),
}


@dataclass(frozen=True)
class Item:
    criterion: str
    name: str
    points: float
    earned: float
    note: str = ""


@dataclass(frozen=True)
class CaseOutcome:
    passed: bool
    detail: str


# -- running a checker ----------------------------------------------------------------------------


def _error_keys(stdout: str) -> set[tuple[str, str]]:
    keys = set()
    for line in stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "ERROR":
            keys.add((parts[1], parts[2]))
    return keys


def _write(root: Path, files: dict[str, str]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def run_case(checker: Path, case: Case, tmp: Path) -> CaseOutcome:
    """Run one hidden case through a checker command; compare ERROR keys and the exit code."""
    base = tmp / re.sub(r"\W+", "-", case.name)
    original = base / "original.md"
    _write(base, {"original.md": case.original})
    _write(base / "tree", case.tree)
    _write(base / "product", case.product)
    tree = base / "missing" if case.tree_missing else base / "tree"
    try:
        run = check.run_checker(checker, original, tree, base / "product")
    except subprocess.TimeoutExpired:
        return CaseOutcome(False, "timed out")
    got = _error_keys(run.stdout)
    passed = got == set(case.expected) and run.returncode == case.exit_code
    detail = (
        f"expected exit {case.exit_code} and {sorted(case.expected)}; "
        f"got exit {run.returncode} and {sorted(got)}"
    )
    return CaseOutcome(passed, "" if passed else detail)


def _pytest_counts(stdout: str) -> tuple[int, int]:
    def count(word: str) -> int:
        match = re.search(rf"(\d+) {word}", stdout)
        return int(match.group(1)) if match else 0

    passed = count("passed")
    return passed, passed + count("failed") + count("error")


# -- hidden checks --------------------------------------------------------------------------------


def _coverage_items(work: Path, original: Path, visible: dict) -> list[Item]:
    crit = "B Rule coverage"
    tree = work / "instructions"
    digest = hashlib.sha256(original.read_bytes()).hexdigest() if original.is_file() else ""
    if digest != ORIGINAL_SHA256:
        note = "the original file was modified; rule coverage cannot be graded"
        names = [
            ("original-unchanged", 2),
            ("coverage", 12),
            ("no-duplicates", 2),
            ("no-retired", 2),
            ("no-unknown", 2),
            ("no-rule-in-map", 2),
            ("no-new-facts", 3),
        ]
        return [Item(crit, n, p, 0.0, note) for n, p in names]
    source = reference.parse_definitions(original.read_text(encoding="utf-8"))
    active = {d.rule_id for d in source if not d.retired}
    problems = reference.check_rules(original, tree) if tree.is_dir() else []
    by_kind: dict[str, list] = {}
    for p in problems:
        by_kind.setdefault(p.kind, []).append(p)
    uncovered = {p.key for p in by_kind.get("missing-rule", []) + by_kind.get("weak-rule", [])}
    if not tree.is_dir():
        uncovered = set(active)
    share = (len(active) - len(uncovered & active)) / len(active)
    note = f"{len(active) - len(uncovered & active)} of {len(active)} active rules covered"
    if uncovered:
        note += f"; missing or weak: {', '.join(sorted(uncovered)[:8])}"
    items = [
        Item(crit, "original-unchanged", 2, 2 * share, "scaled by coverage"),
        Item(crit, "coverage", 12, 12 * share, note),
    ]
    for name, kind in (
        ("no-duplicates", "duplicate-rule"),
        ("no-retired", "retired-rule"),
        ("no-unknown", "unknown-rule"),
        ("no-rule-in-map", "rule-in-map"),
    ):
        found = by_kind.get(kind, [])
        earned = 0.0 if found else 2 * share
        items.append(Item(crit, name, 2, earned, "; ".join(str(p) for p in found[:4])))
    facts = visible["no-new-facts"]
    items.append(Item(crit, "no-new-facts", 3, 3 * facts.score * share, facts.detail))
    return items


def _pristine_tests(checker: Path) -> Item:
    crit = "D Docs checker"
    if not checker.is_file():
        return Item(crit, "pristine-visible-tests", 6, 0.0, "check_docs.py is missing")
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(checker, Path(tmp) / "check_docs.py")
        shutil.copy(PRISTINE_TESTS, Path(tmp) / "test_check_docs.py")
        run = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", tmp],
            capture_output=True,
            text=True,
            timeout=check.TIMEOUT_S,
            cwd=tmp,
        )
    passed, total = _pytest_counts(run.stdout)
    earned = 6 * passed / total if total else 0.0
    return Item(crit, "pristine-visible-tests", 6, earned, f"{passed} of {total} visible tests")


def _inject_faults(tree: Path) -> set[tuple[str, str]]:
    agents = tree / "AGENTS.md"
    text = agents.read_text(encoding="utf-8").rstrip("\n") + "\n\nSee [moved](docs/MOVED.md).\n"
    agents.write_text(text, encoding="utf-8")
    doc = tree / "docs" / "RELIABILITY.md"
    body = doc.read_text(encoding="utf-8").replace("[R4.3]", "R4.3")
    doc.write_text(body.rstrip("\n") + "\n\nR8.1 is next.\n", encoding="utf-8")
    line = len(text.splitlines())
    return {
        ("broken-link", f"AGENTS.md:{line}"),
        ("missing-rule", "R4.3"),
        ("unknown-rule", "R8.1"),
    }


def _reference_tree(checker: Path, original: Path) -> Item:
    crit = "D Docs checker"
    if not checker.is_file():
        return Item(crit, "reference-tree", 6, 0.0, "check_docs.py is missing")
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "instructions"
        shutil.copytree(REFERENCE_WORK / "instructions", tree)
        clean = check.run_checker(checker, original, tree, PRODUCT)
        clean_ok = clean.returncode == 0 and not _error_keys(clean.stdout)
        expected = _inject_faults(tree)
        faulty = check.run_checker(checker, original, tree, PRODUCT)
        found = expected & _error_keys(faulty.stdout)
    # A checker that reports nothing is "clean" everywhere: clean only counts with a detection.
    earned = (3.0 if clean_ok and found else 0.0) + 3.0 * len(found) / len(expected)
    note = f"clean on the reference tree: {clean_ok}; injected faults found: {len(found)} of 3"
    if not clean_ok:
        note += f"; false alarms: {sorted(_error_keys(clean.stdout))[:4]}"
    return Item(crit, "reference-tree", 6, earned, note)


def _hidden_cases(checker: Path) -> Item:
    crit = "D Docs checker"
    if not checker.is_file():
        return Item(crit, "hidden-cases", 14, 0.0, "check_docs.py is missing")
    with tempfile.TemporaryDirectory() as tmp:
        outcomes = [(case, run_case(checker, case, Path(tmp))) for case in CASES]
    detection = [o.passed for c, o in outcomes if c.exit_code == 1]
    counted = [o.passed for c, o in outcomes if c.exit_code == 1 or any(detection)]
    passed = sum(counted)
    failed = [c.name for c, o in outcomes if not o.passed]
    note = f"{passed} of {len(CASES)} hidden cases"
    if failed:
        note += f"; failing: {', '.join(failed)}"
    return Item(crit, "hidden-cases", 14, 14 * passed / len(CASES), note)


# -- the grade ------------------------------------------------------------------------------------


def grade(work: Path, *, allow_pending: bool = False, original: Path | None = None) -> list[Item]:
    original = original or ORIGINAL
    results = check.run_checks(work, allow_pending=allow_pending, original=original)
    visible = {r.name: r for r in results}
    items: list[Item] = []
    for name, (criterion, pts) in VISIBLE_POINTS.items():
        result = visible[name]
        items.append(Item(criterion, name, pts, pts * result.score, result.detail))
    items += _coverage_items(work, original, visible)
    checker = work / "checker" / "check_docs.py"
    items += [_pristine_tests(checker), _reference_tree(checker, original), _hidden_cases(checker)]
    order = list(CRITERIA)
    return sorted(items, key=lambda i: order.index(i.criterion))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A1 grader")
    parser.add_argument("--work", type=Path, default=check.STARTER)
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument("--min-score", type=float, default=0.0)
    args = parser.parse_args(argv)
    work = args.work.resolve()
    print(f"A1 grade: {check.shown(work)}")
    items = grade(work, allow_pending=args.allow_pending)
    for criterion, total in CRITERIA.items():
        mine = [i for i in items if i.criterion == criterion]
        print(f"{criterion:<40} {sum(i.earned for i in mine):5.1f}/{total}")
        for i in mine:
            line = f"  {i.name:<26} {i.earned:5.1f}/{i.points:g}"
            if i.earned < i.points and i.note:
                line += f"  {i.note}"
            print(line)
    score = round(sum(i.earned for i in items), 1)
    print(f"Score: {score}/100")
    return 1 if score < args.min_score else 0


if __name__ == "__main__":
    sys.exit(main())
