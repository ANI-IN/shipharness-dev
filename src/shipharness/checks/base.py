"""Check interface for the referee and verify gate (CONTRACTS §10). Checks never call a model."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict


class Finding(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule: str  # "R1".."R8", "regression", "hidden", "scope", "flaky", "board"
    severity: Literal["violation", "leak", "error", "info"]
    endpoint: str | None = None  # "GET /issues/{issue_id}"
    detail: str
    baseline: bool = False  # present at the checkpoint baseline


class CheckResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    check: str
    passed: bool  # no new violations
    new_violations: int
    baseline_violations: int
    total_probes: int
    findings: list[Finding]
    duration_ms: int
    seed: int | None = None
    artifacts: list[str] = []


def _no_progress(_done: int, _total: int, _label: str) -> None:
    return None


@dataclass
class CheckContext:
    checkpoint: str
    feature_id: str
    seed: int = 0
    phase_allowed_paths: dict[str, list[str]] = field(default_factory=dict)
    exemptions: dict[str, list[str]] = field(default_factory=dict)  # rule -> ["POST /path", ...]
    progress: Callable[[int, int, str], None] = _no_progress


class Check(Protocol):
    name: str

    def run(self, build_dir: Path, ctx: CheckContext) -> CheckResult: ...


_REGISTRY: dict[str, type[Check]] = {}


def register_check[C](cls: C) -> C:
    name = cls.name  # type: ignore[attr-defined]
    if name in _REGISTRY:
        raise ValueError(f"check {name!r} is already registered")
    _REGISTRY[name] = cls  # type: ignore[assignment]
    return cls


def get_check(name: str) -> Check:
    try:
        return _REGISTRY[name]()
    except KeyError:
        raise KeyError(f"no check named {name!r}; registered: {sorted(_REGISTRY)}") from None


def registered_checks() -> list[str]:
    return sorted(_REGISTRY)


def _key(f: Finding) -> tuple[str, str | None, str]:
    return (f.rule, f.endpoint, f.severity)


def mark_baseline(current: CheckResult, baseline: CheckResult | None) -> CheckResult:
    """Mark findings already present at the checkpoint; count and gate only the new ones."""
    known = {_key(f) for f in baseline.findings} if baseline else set()
    marked = [f.model_copy(update={"baseline": _key(f) in known}) for f in current.findings]
    new = [f for f in marked if not f.baseline]
    old = [f for f in marked if f.baseline]
    return current.model_copy(
        update={
            "findings": (new + old)[:200],
            "new_violations": len(new),
            "baseline_violations": len(old),
            "passed": not new,
        }
    )
