"""SYNTHETIC live-run evidence for the A1 grader tests. Not a real run.

Every value here is invented so that the tests can exercise the live-evidence checks without
keys, Docker, or model calls. The batch label is `a1-synthetic`, the experiment names say
`synthetic`, the policy summary says `SYNTHETIC`, and no trace URL is set. The real captured run
of the reference solution is a pending marker in `solution/work/live/README.md`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BATCH = "a1-synthetic"
COMMAND = (
    "uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch " + BATCH
)
MODEL = "gpt-6-luna"
RUN_COST = 0.03
LABEL = "SYNTHETIC fixture for grader tests, not a real run"
# Invented commit SHAs, one per checkpoint tag the section-1 tasks use.
SHAS = {
    "m1-s1-start": "1" * 40,
    "m1-alt-a": "a" * 40,
    "m1-alt-b": "b" * 40,
}


def run_id(arm: str, index: int) -> str:
    """Same shape as shipharness.ab.workspace.new_run_id: r-<date>-<time>-<6 hex>."""
    return f"r-20261016-1200{index:02d}-{'b0' if arm == 'bare' else 'c0'}{index:04x}"


def record(rid: str, arm: str, task: tuple[str, str, str], r1: int = 0, r3: int = 0) -> dict:
    feature, variant, checkpoint = task
    return {
        "run_id": rid,
        "ab_id": None,
        "arm": arm,
        "feature_id": feature,
        "variant": variant,
        "checkpoint": checkpoint,
        "checkpoint_sha": SHAS[checkpoint],
        "layers": [] if arm == "bare" else ["instructions"],
        "status": "completed",
        "claim": "done",
        "r1_new_violations": r1,
        "r1_leaks": 0,
        "r2_new_violations": 0,
        "r3_new_failures": r3,
        "r4_duplicates": 0,
        "r5_audit_missing": 0,
        "r6_ok": True,
        "r7_ok": True,
        "regression_passed": 10,
        "regression_total": 10,
        "hidden_passed": 5,
        "hidden_total": 5,
        "mutants_killed": 3,
        "mutants_total": 3,
        "shipped_tests": 2,
        "flaky_tests": 0,
        "out_of_scope_files": 0,
        "test_phase_source_edits": 0,
        "continuity_failure": None,
        "redone_lines_pct": None,
        "board_ok": True,
        "reviewer_verdict": None,
        "reviewer_agrees": None,
        "primary": {"r1_new_violations": r1},
        "passed_primary": r1 == 0,
        "cost_usd": RUN_COST,
        "review_cost_usd": 0.0,
        "turns_total": 12,
        "wall_s": 100.0,
        "trace_url": None,
        "referee_trace_url": None,
        "sandboxed": True,
        "recorded": False,
        "single_arm": False,
        "referee_version": "2026-10-17",
        "constructed": False,
        "captured_at": "2026-10-16T12:00:00+00:00",
    }


def _event(rid: str, seq: int, kind: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "v": 1,
        "ab_id": None,
        "run_id": rid,
        "arm": "harness",
        "seq": seq,
        "ts": f"2026-10-16T12:00:{seq:02d}+00:00",
        "type": kind,
        "data": data,
        "recorded": False,
    }


def run_log(rid: str, task: tuple[str, str, str], placed: list[str]) -> list[dict[str, Any]]:
    feature, variant, checkpoint = task
    spec = {
        "run_id": rid,
        "ab_id": None,
        "arm": "harness",
        "feature_id": feature,
        "checkpoint": checkpoint,
        "ticket_text": LABEL,
        "variant": variant,
        "layers": ["instructions"],
        "phases": ["build", "test"],
        "session_budget": [30],
        "test_phase_turns": 12,
        "allowed_paths": {},
        "model": MODEL,
        "reasoning_effort": "medium",
        "max_output_tokens": 8000,
        "service_tier": "auto",
        "cost_limit_usd": 0.2,
    }
    message = f"placed {len(placed)} instruction files (AGENTS.md map, docs, skills)"
    return [
        _event(rid, 1, "run_start", {"spec": spec, "policy_summary": LABEL}),
        _event(
            rid,
            2,
            "harness_decision",
            {"kind": "note", "layer": "instructions", "message": message, "paths": placed},
        ),
        _event(
            rid,
            3,
            "cost",
            {
                "scope": "run",
                "model": MODEL,
                "call_usd": RUN_COST,
                "run_usd": RUN_COST,
                "session_usd": RUN_COST,
                "limit_usd": 0.2,
            },
        ),
        _event(
            rid,
            4,
            "run_end",
            {
                "status": "completed",
                "claim": "done",
                "cost_usd": RUN_COST,
                "turns_total": 12,
                "wall_s": 100.0,
            },
        ),
    ]


def _dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def exports_layout(
    root: Path,
    tasks: list[tuple[str, str, str]],
    placed: list[str],
    *,
    k: int = 3,
    r1_fail: dict[str, int] | None = None,
    r3_fail: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Write experiments/, scores/, and runs/ under root, as `shipharness experiments` lays them
    out in exports/ and .shipharness/runs/. `r1_fail`/`r3_fail`: arm -> runs that fail."""
    r1_fail, r3_fail = r1_fail or {}, r3_fail or {}
    summary: dict[str, Any] = {"names": {}, "urls": {}, "rows": {}}
    total = 0.0
    for arm in ("bare", "harness"):
        rows = []
        index = 0
        for task in tasks:
            for _ in range(k):
                rid = run_id(arm, index)
                r1 = 1 if index < r1_fail.get(arm, 0) else 0
                r3 = 1 if index < r3_fail.get(arm, 0) else 0
                _dump(root / "scores" / f"{rid}.json", record(rid, arm, task, r1, r3))
                if arm == "harness":
                    lines = [json.dumps(e) for e in run_log(rid, task, placed)]
                    log = root / "runs" / rid / "events.jsonl"
                    log.parent.mkdir(parents=True, exist_ok=True)
                    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
                rows.append(rid)
                total += RUN_COST
                index += 1
        name = f"shipharness-{BATCH}-{arm}-2026-10-16-synthetic"
        url = f"https://smith.langchain.com/o/synthetic/datasets/synthetic/compare?selectedSessions={arm}"
        export = {
            "name": name,
            "url": url,
            "comparison_url": None,
            "dataset": "teamtrack-features-v1",
            "split": "section-1",
            "arm": arm,
            "k": k,
            "metadata": {
                "arm": arm,
                "layers": [] if arm == "bare" else ["instructions"],
                "model": MODEL,
                "effort": "medium",
                "service_tier": "auto",
                "batch": BATCH,
                "k": k,
            },
            "rows": sorted(rows),
            "checkpoint_shas": {t[2]: SHAS[t[2]] for t in tasks},
            "stats": {
                "runs": len(rows),
                "passed_primary": f"{len(rows)}/{len(rows)}",
                "aborted": 0,
                "errors": 0,
                "cost_usd": round(RUN_COST * len(rows), 6),
            },
        }
        _dump(root / "experiments" / f"{name}.json", export)
        summary["names"][arm] = name
        summary["urls"][arm] = url
        summary["rows"][arm] = sorted(rows)
    summary["cost"] = round(total, 6)
    return summary


def output_text(summary: dict[str, Any], command: str = COMMAND) -> str:
    """What the experiments command prints, preceded by the command line."""
    lines = [f"$ {command}"]
    for arm in ("bare", "harness"):
        runs = len(summary["rows"][arm])
        lines.append(f"{arm}: {summary['names'][arm]} {{'runs': {runs}}} {summary['urls'][arm]}")
    cost = summary["cost"]
    lines.append(
        f"Cost: ${cost:.6f} (this command: {MODEL} ${cost:.6f}; experiment ${cost:.6f} of $25.00)"
    )
    return "\n".join(lines) + "\n"


def write_live(
    work: Path,
    tasks: list[tuple[str, str, str]],
    placed: list[str],
    **kwargs: Any,
) -> dict[str, Any]:
    """Write <work>/live/ exactly as live_evidence.py collects it."""
    live = work / "live"
    summary = exports_layout(live, tasks, placed, **kwargs)
    (live / "output.txt").write_text(output_text(summary), encoding="utf-8")
    return summary


def report(summary: dict[str, Any], r1: tuple[str, str], r3: tuple[str, str], runs: int) -> str:
    """An ab-report.md whose values match the synthetic evidence."""
    words = " ".join(["word"] * 60)
    return f"""# A1 A/B report ({LABEL})

## Setup

- Command: `{COMMAND}`
- Instructions tree commit: abc1234
- Runs per arm: {runs}

## Results

| Measure | Bare arm (runs failing of N) | Harness arm (runs failing of N) |
|---|---|---|
| R1: runs with at least one new R1 violation | {r1[0]} | {r1[1]} |
| R3: runs with at least one new R3 failure | {r3[0]} | {r3[1]} |

## Links

- Bare experiment: {summary["urls"]["bare"]}
- Harness experiment: {summary["urls"]["harness"]}

## Cost and traces

- Cost: ${summary["cost"]:.6f}
- Traces: 96

## Reading the result

R1 and R3 are compared here. {words}

## Limits

Three runs per task is a small sample and one model was used, so a difference of one run is noise
and this says nothing about other products.
"""
