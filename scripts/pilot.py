"""M6 pilot gate runner (brief M6; DESIGN §16 AS-4 to AS-9).

Runs the section A/Bs (F1-F4 canonical, `make demo-N` layer stacks) k times at one reasoning effort,
with board previews off, several at once, under a hard total budget: a new A/B starts only while the
spend since the pilot began plus the worst case of every A/B in flight and of the next one fits the
budget. Writes one JSON summary under `.shipharness/pilot/` and prints the gate conditions.

    uv run python scripts/pilot.py --k 3 --effort medium --parallel 2 --budget 10
    uv run python scripts/pilot.py --determinism 10 --ab <ab id>   # referee re-runs, no model calls
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SECTIONS = {"F1": "demo-1", "F2": "demo-2", "F3": "demo-3", "F4": "demo-4"}
# Fields that differ between two judgements of the same build by design (ids, links, timings, cost).
VOLATILE = {
    "captured_at",
    "run_id",
    "ab_id",
    "trace_url",
    "referee_trace_url",
    "recorded",
    "review_cost_usd",
    "reviewer_verdict",
    "reviewer_agrees",
}


def can_launch(*, spent: float, in_flight: int, worst: float, budget: float) -> bool:
    """True while spend so far plus the worst case of each A/B in flight and one more fits."""
    return spent + (in_flight + 1) * worst <= budget + 1e-9


def spend_since(ledger: Path, start_ts: str) -> float:
    """Dollars recorded in the cost ledger at or after `start_ts` (ISO, UTC, ...Z)."""
    if not ledger.is_file():
        return 0.0
    total = 0.0
    for line in ledger.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if str(row.get("ts", "")) >= start_ts:
            total += float(row.get("cost_usd", 0.0))
    return round(total, 6)


def evaluate_gate(runs: list[dict[str, Any]], *, max_arm_cost: float, max_ab_wall_s: float) -> dict:
    """Gate conditions 1, 2, and 4 (condition 3, determinism, is checked separately)."""
    features = sorted({r["feature"] for r in runs})
    fails: dict[tuple[str, str], int] = {}
    totals: dict[tuple[str, str], int] = {}
    for r in runs:
        key = (r["feature"], r["arm"])
        totals[key] = totals.get(key, 0) + 1
        fails[key] = fails.get(key, 0) + (0 if r["passed_primary"] else 1)
    no_gap = [
        f
        for f in features
        if totals.get((f, "bare"), 0) == 0
        or fails.get((f, "bare"), 0) * 3 < totals.get((f, "bare"), 0) * 2
    ]
    better = [
        f
        for f in features
        if fails.get((f, "harness"), 0) / max(totals.get((f, "harness"), 1), 1)
        < fails.get((f, "bare"), 0) / max(totals.get((f, "bare"), 1), 1)
    ]
    within = all(r["cost_usd"] <= max_arm_cost + 1e-9 for r in runs) and all(
        r["ab_wall_s"] <= max_ab_wall_s for r in runs
    )
    return {
        "failures": {
            f"{f}/{a}": f"{fails.get((f, a), 0)}/{totals.get((f, a), 0)}"
            for f in features
            for a in ("bare", "harness")
        },
        "bare_fails_each_section": not no_gap,
        "sections_without_gap": no_gap,
        "harness_better_sections": len(better),
        "within_cost_and_time": within,
        "passed_1_2_4": not no_gap and len(better) * 4 >= len(features) * 3 and within,
    }


def judged(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if k not in VOLATILE}


def _settings() -> Any:
    sys.path.insert(0, str(REPO / "src"))
    from shipharness.config import get_settings

    return get_settings()


def ab_command(feature: str, variant: str | None, budget: str | None = None) -> list[str]:
    """`shipharness ab` for one section; `variant` picks a pre-registered dataset variant and
    `budget` a pre-registered session budget override (e.g. "12,38")."""
    cmd = ["uv", "run", "shipharness", "ab", "--section", SECTIONS[feature], "--feature", feature]
    if variant:
        cmd += ["--variant", variant]
    if budget:
        cmd += ["--session-budget", budget]
    return [*cmd, "--purpose", "pilot", "--no-preview"]


def parse_budgets(value: str) -> dict[str, str]:
    """`F2=12/38` -> {"F2": "12,38"} (slashes inside, commas between features)."""
    pairs = [item.split("=", 1) for item in value.split(",") if item.strip()]
    return {feature.strip(): budget.strip().replace("/", ",") for feature, budget in pairs}


def parse_variants(value: str) -> dict[str, str]:
    """`F1=trap-legacy-pattern,F2=stop-1` -> {feature: dataset variant}."""
    pairs = [item.split("=", 1) for item in value.split(",") if item.strip()]
    return {feature.strip(): variant.strip() for feature, variant in pairs}


def _one_ab(
    feature: str,
    effort: str,
    runs_dir: Path,
    exports_dir: Path,
    variant: str | None = None,
    budget: str | None = None,
) -> list[dict[str, Any]]:
    env = {**os.environ, "OPENAI_REASONING_EFFORT": effort}
    cmd = ab_command(feature, variant, budget)
    started = time.monotonic()
    done = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True, check=False)
    wall = round(time.monotonic() - started, 1)
    ab_id = next(
        (line.split()[1] for line in done.stdout.splitlines() if line.startswith("A/B ")), None
    )
    if ab_id is None:
        tail = (done.stdout + done.stderr)[-800:]
        return [{"feature": feature, "error": f"exit {done.returncode}: {tail}", "ab_wall_s": wall}]
    record = json.loads((runs_dir / ab_id / "ab.json").read_text(encoding="utf-8"))
    rows = []
    for arm, data in record["arms"].items():
        result = data["result"]
        score_path = exports_dir / "scores" / f"{result['run_id']}.json"
        score = json.loads(score_path.read_text(encoding="utf-8")) if score_path.is_file() else {}
        rows.append(
            {
                "feature": feature,
                "variant": variant or "canonical",
                "arm": arm,
                "ab_id": ab_id,
                "run_id": result["run_id"],
                "status": result["status"],
                "abort_reason": result.get("abort_reason"),
                "cost_usd": result["cost_usd"],
                "turns_total": result["turns_total"],
                "wall_s": result["wall_s"],
                "agent_wall_s": result.get("agent_wall_s"),
                "harness_wall_s": result.get("harness_wall_s"),
                "ab_wall_s": wall,
                "passed_primary": bool(score.get("passed_primary")),
                "primary": score.get("primary"),
                "review_cost_usd": score.get("review_cost_usd"),
            }
        )
    return rows


def run_pilot(args: argparse.Namespace) -> int:
    settings = _settings()
    runs_dir, exports_dir = Path(settings.runs_dir), Path(settings.exports_dir)
    if not runs_dir.is_absolute():
        runs_dir = REPO / runs_dir
    if not exports_dir.is_absolute():
        exports_dir = REPO / exports_dir
    ledger = REPO / ".shipharness" / "ledger.jsonl"
    worst = 2 * settings.max_run_cost_usd + 2 * settings.max_review_cost_usd
    start_ts = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    queue = [(f, rep) for rep in range(args.k) for f in args.features]
    results: list[dict[str, Any]] = []
    lock = threading.Lock()
    in_flight: list[Future] = []
    stopped = ""
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        while queue:
            in_flight = [f for f in in_flight if not f.done()]
            if len(in_flight) >= args.parallel:
                time.sleep(2)
                continue
            spent = spend_since(ledger, start_ts)
            if not can_launch(
                spent=spent, in_flight=len(in_flight), worst=worst, budget=args.budget
            ):
                if in_flight:
                    time.sleep(2)
                    continue
                stopped = f"budget: ${spent:.4f} spent, next worst case ${worst:.2f}"
                break
            feature, rep = queue.pop(0)
            print(f"start {feature} rep {rep + 1}/{args.k} (spent ${spent:.4f})", flush=True)

            def job(feature: str = feature) -> None:
                rows = _one_ab(
                    feature,
                    args.effort,
                    runs_dir,
                    exports_dir,
                    args.variants.get(feature),
                    args.budgets.get(feature),
                )
                with lock:
                    results.extend(rows)
                for row in rows:
                    print(
                        json.dumps(
                            {
                                k: row.get(k)
                                for k in (
                                    "feature",
                                    "variant",
                                    "arm",
                                    "ab_id",
                                    "status",
                                    "passed_primary",
                                    "cost_usd",
                                    "ab_wall_s",
                                    "error",
                                )
                            }
                        ),
                        flush=True,
                    )

            in_flight.append(pool.submit(job))
    good = [r for r in results if "error" not in r]
    gate = (
        evaluate_gate(
            good, max_arm_cost=settings.max_run_cost_usd, max_ab_wall_s=args.max_ab_wall_s
        )
        if good
        else {}
    )
    summary = {
        "started": start_ts,
        "effort": args.effort,
        "k": args.k,
        "parallel": args.parallel,
        "budget_usd": args.budget,
        "spent_usd": spend_since(ledger, start_ts),
        "stopped": stopped,
        "errors": [r for r in results if "error" in r],
        "runs": good,
        "gate": gate,
    }
    out = (
        REPO
        / ".shipharness"
        / "pilot"
        / f"pilot-{args.effort}-{start_ts[:19].replace(':', '')}.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "summary": str(out),
                "spent_usd": summary["spent_usd"],
                "gate": gate,
                "stopped": stopped,
            },
            indent=2,
        )
    )
    return 0 if not summary["errors"] else 1


def run_determinism(args: argparse.Namespace) -> int:
    settings = _settings()
    from shipharness.ab.recorded import RecordedDeps, find_run_dir, replay_ab
    from shipharness.ab.runtime import build_runtime

    rt = build_runtime(settings, project="shipharness-pilot")
    runs_dir = Path(settings.runs_dir)
    run_dir = find_run_dir(runs_dir, args.ab)
    deps = RecordedDeps(
        course_repo=rt.course_repo,
        referee_sandbox_factory=rt.referee_sandbox_factory,
        runs_dir=runs_dir,
        exports_dir=Path(settings.exports_dir) / "determinism",
        tracer=rt.tracer,
        reviewer=None,
        sandboxed=rt.sandboxed,
        container_paths=rt.sandboxed,
    )
    seen: list[dict[str, Any]] = []
    for i in range(args.determinism):
        out = replay_ab(run_dir, deps)
        seen.append({arm: judged(r.model_dump(mode="json")) for arm, r in out.records.items()})
        print(f"re-run {i + 1}/{args.determinism}: {out.ab_id}", flush=True)
    identical = sum(1 for s in seen if s == seen[0])
    print(json.dumps({"ab": args.ab, "re_runs": len(seen), "identical_to_first": identical}))
    return 0 if identical == len(seen) else 1


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "--features", type=lambda s: [x.strip() for x in s.split(",")], default=list(SECTIONS)
    )
    p.add_argument("--variants", type=parse_variants, default={}, help="F1=trap-legacy-pattern,...")
    p.add_argument("--budgets", type=parse_budgets, default={}, help="F2=12/38,...")
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--effort", default="medium")
    p.add_argument("--parallel", type=int, default=2)
    p.add_argument("--budget", type=float, default=10.0)
    p.add_argument("--max-ab-wall-s", type=float, default=360.0)
    p.add_argument("--determinism", type=int, default=0)
    p.add_argument("--ab", default="")
    args = p.parse_args()
    if args.determinism:
        return run_determinism(args)
    return run_pilot(args)


if __name__ == "__main__":
    raise SystemExit(main())
