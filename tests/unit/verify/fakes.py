"""Fake check runner output (contract I-1) for gate and referee tests."""

from __future__ import annotations

import json
from typing import Any

from shipharness.sandbox import ExecResult

ALL_GATE_CHECKS = [
    "r1_tenant",
    "r2_roles",
    "r3_conventions",
    "r4_idempotency",
    "r5_audit",
    "r6_layering",
    "r7_migrations",
    "regression",
    "board",
]


def check_result(
    check: str,
    *,
    new: int = 0,
    findings: list[dict[str, Any]] | None = None,
    total: int = 10,
    seed: int | None = None,
) -> dict[str, Any]:
    findings = findings or [
        {
            "rule": check.upper(),
            "severity": "violation",
            "endpoint": f"GET /x/{i}",
            "detail": f"{check} problem {i}",
            "baseline": False,
        }
        for i in range(new)
    ]
    return {
        "check": check,
        "passed": new == 0,
        "new_violations": new,
        "baseline_violations": 0,
        "total_probes": total,
        "findings": findings,
        "duration_ms": 5,
        "seed": seed,
        "artifacts": [],
    }


def runner_output(results: list[dict[str, Any]], progress: bool = True) -> str:
    lines = []
    if progress:
        for r in results:
            label = r["check"]
            lines.append(
                json.dumps({"check": label, "done": 1, "total": 2, "label": f"{label} 1/2"})
            )
            lines.append(
                json.dumps({"check": label, "done": 2, "total": 2, "label": f"{label} 2/2"})
            )
    lines.append(json.dumps({"results": results}))
    return "\n".join(lines) + "\n"


def ok(output: str = "") -> ExecResult:
    return ExecResult(exit_code=0, output=output, duration_ms=1)


def fail(output: str = "", code: int = 1) -> ExecResult:
    return ExecResult(exit_code=code, output=output, duration_ms=1)
