"""Screen 4 (A/B Report) data: ScoreRecords and experiments read from `exports/` (CONTRACTS §11).

Counts are shown as "9/10", never as percentages. Unreadable or incomplete files are counted and
skipped so one bad export cannot blank the screen.
"""

from __future__ import annotations

import contextlib
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ARM_ORDER = {"bare": 0, "harness": 1}
_REQUIRED = ("run_id", "arm", "variant", "passed_primary")


def safe_url(value: object) -> str | None:
    """Keep http(s) links only, so an export or event cannot inject a `javascript:` link."""
    if isinstance(value, str) and value.startswith(("https://", "http://")):
        return value
    return None


@dataclass
class Dot:
    run_id: str
    passed: bool
    recorded: bool
    sandboxed: bool


@dataclass
class DotGroup:
    variant: str
    arm: str
    layers: str
    dots: list[Dot] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(d.passed for d in self.dots)

    @property
    def count_label(self) -> str:
        return f"{self.passed}/{len(self.dots)}"


@dataclass
class Bar:
    label: str
    passed: int
    total: int

    @property
    def count_label(self) -> str:
        return f"{self.passed}/{self.total}"


@dataclass
class CostRow:
    arm: str
    spent_usd: float
    verified: int

    @property
    def per_verified_usd(self) -> float | None:
        return self.spent_usd / self.verified if self.verified else None


@dataclass
class AgreementRow:
    arm: str
    agrees: int
    known: int

    @property
    def count_label(self) -> str:
        return f"{self.agrees}/{self.known}"


@dataclass
class Experiment:
    name: str
    url: str | None
    comparison_url: str | None
    split: str


@dataclass
class Report:
    groups: list[DotGroup] = field(default_factory=list)
    ablation: list[Bar] = field(default_factory=list)
    costs: list[CostRow] = field(default_factory=list)
    reviewer: list[AgreementRow] = field(default_factory=list)
    experiments: list[Experiment] = field(default_factory=list)
    skipped: int = 0
    unsandboxed: int = 0
    recorded: int = 0

    @property
    def empty(self) -> bool:
        return not self.groups and not self.experiments


def _read_json_dir(folder: Path) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    skipped = 0
    if not folder.is_dir():
        return rows, skipped
    for path in sorted(folder.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            skipped += 1
            continue
        if isinstance(data, dict):
            rows.append(data)
        else:
            skipped += 1
    return rows, skipped


def exports_signature(exports_dir: Path) -> tuple[tuple[str, int, int], ...]:
    """Cheap change detector: (name, size, mtime_ns) of every scores/experiments file."""
    items: list[tuple[str, int, int]] = []
    for kind in ("scores", "experiments"):
        folder = Path(exports_dir) / kind
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            try:
                stat = path.stat()
            except OSError:
                continue
            items.append((f"{kind}/{path.name}", stat.st_size, stat.st_mtime_ns))
    return tuple(sorted(items))


def _layers_label(layers: object) -> str:
    if not isinstance(layers, list) or not layers:
        return "none (bare)"
    return " + ".join(str(layer) for layer in layers)


def load_report(exports_dir: Path) -> Report:
    exports_dir = Path(exports_dir)
    scores, skipped = _read_json_dir(exports_dir / "scores")
    experiments, skipped_exp = _read_json_dir(exports_dir / "experiments")
    report = Report(skipped=skipped + skipped_exp)

    groups: dict[tuple[str, str], DotGroup] = {}
    ablation: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])  # passed, total, n_layers
    spent: dict[str, float] = defaultdict(float)
    verified: dict[str, int] = defaultdict(int)
    agree: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for record in scores:
        if any(key not in record for key in _REQUIRED):
            report.skipped += 1
            continue
        arm, variant = str(record["arm"]), str(record["variant"])
        passed = bool(record["passed_primary"])
        layers = _layers_label(record.get("layers"))
        group = groups.setdefault((variant, arm), DotGroup(variant, arm, layers))
        group.dots.append(
            Dot(
                str(record["run_id"]),
                passed,
                bool(record.get("recorded", False)),
                bool(record.get("sandboxed", True)),
            )
        )
        bar = ablation[layers]
        bar[0] += passed
        bar[1] += 1
        bar[2] = len(record.get("layers") or [])
        with contextlib.suppress(TypeError, ValueError):
            spent[arm] += float(record.get("cost_usd") or 0) + float(
                record.get("review_cost_usd") or 0
            )
        verified[arm] += passed
        if record.get("reviewer_agrees") is not None:
            agree[arm][0] += bool(record["reviewer_agrees"])
            agree[arm][1] += 1
        report.unsandboxed += not bool(record.get("sandboxed", True))
        report.recorded += bool(record.get("recorded", False))

    def arm_key(arm: str) -> tuple[int, str]:
        return (ARM_ORDER.get(arm, 9), arm)

    report.groups = [groups[k] for k in sorted(groups, key=lambda k: (k[0], *arm_key(k[1])))]
    report.ablation = [
        Bar(label, v[0], v[1])
        for label, v in sorted(ablation.items(), key=lambda kv: (kv[1][2], kv[0]))
    ]
    report.costs = [CostRow(arm, spent[arm], verified[arm]) for arm in sorted(spent, key=arm_key)]
    report.reviewer = [AgreementRow(arm, *agree[arm]) for arm in sorted(agree, key=arm_key)]
    for item in experiments:
        if "name" not in item:
            report.skipped += 1
            continue
        report.experiments.append(
            Experiment(
                str(item["name"]),
                safe_url(item.get("url")),
                safe_url(item.get("comparison_url")),
                str(item.get("split", "")),
            )
        )
    report.experiments.sort(key=lambda e: e.name)
    return report
