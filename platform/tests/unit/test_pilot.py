"""The M6 pilot runner's budget guard and gate evaluation (pure functions; no runs)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
_spec = importlib.util.spec_from_file_location("pilot", REPO / "platform" / "scripts" / "pilot.py")
assert _spec and _spec.loader
pilot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pilot)


def test_launch_only_while_the_worst_case_fits_the_budget() -> None:
    assert pilot.can_launch(spent=9.1, in_flight=1, worst=0.48, budget=10.0) is False  # 9.1 + 0.96
    assert pilot.can_launch(spent=8.0, in_flight=1, worst=0.48, budget=10.0) is True
    assert pilot.can_launch(spent=0.0, in_flight=0, worst=10.01, budget=10.0) is False


def test_spend_since_counts_only_entries_after_the_start(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    rows = [
        {"ts": "2026-10-16T10:00:00.000Z", "cost_usd": 5.0},
        {"ts": "2026-10-16T12:00:00.000Z", "cost_usd": 0.25},
        {"ts": "2026-10-16T12:30:00.000Z", "cost_usd": 0.5},
    ]
    ledger.write_text("\n".join(json.dumps(r) for r in rows) + "\nnot json\n", encoding="utf-8")
    assert pilot.spend_since(ledger, "2026-10-16T11:00:00.000Z") == 0.75
    assert pilot.spend_since(tmp_path / "missing.jsonl", "2026-10-16T11:00:00.000Z") == 0.0


def _run(feature: str, arm: str, passed: bool, cost: float = 0.1, wall: float = 200.0) -> dict:
    return {
        "feature": feature,
        "arm": arm,
        "passed_primary": passed,
        "cost_usd": cost,
        "ab_wall_s": wall,
    }


def test_gate_conditions_from_runs() -> None:
    runs = []
    for f in ("F1", "F2", "F3", "F4"):
        runs += [_run(f, "bare", False), _run(f, "bare", False), _run(f, "bare", True)]
        runs += [_run(f, "harness", True)] * 3
    gate = pilot.evaluate_gate(runs, max_arm_cost=0.20, max_ab_wall_s=360)
    assert gate["bare_fails_each_section"] is True  # 2/3 per section
    assert gate["harness_better_sections"] == 4
    assert gate["within_cost_and_time"] is True
    assert gate["passed_1_2_4"] is True


def test_gate_fails_when_one_section_shows_no_gap() -> None:
    runs = []
    for f in ("F1", "F2", "F3", "F4"):
        bare_fail = f != "F2"
        runs += [_run(f, "bare", not bare_fail)] * 3
        runs += [_run(f, "harness", True)] * 3
    runs.append(_run("F1", "harness", True, cost=0.21))
    gate = pilot.evaluate_gate(runs, max_arm_cost=0.20, max_ab_wall_s=360)
    assert gate["bare_fails_each_section"] is False
    assert gate["sections_without_gap"] == ["F2"]
    assert gate["within_cost_and_time"] is False
    assert gate["passed_1_2_4"] is False


def test_judged_fields_ignore_ids_and_timings() -> None:
    a = {
        "run_id": "r1",
        "ab_id": "x",
        "hidden_passed": 3,
        "referee_trace_url": "u1",
        "r1_new_violations": 0,
    }
    b = {
        "run_id": "r2",
        "ab_id": "y",
        "hidden_passed": 3,
        "referee_trace_url": "u2",
        "r1_new_violations": 0,
    }
    assert pilot.judged(a) == pilot.judged(b)
    assert pilot.judged({**a, "hidden_passed": 2}) != pilot.judged(b)


def test_ab_command_selects_the_pre_registered_variant() -> None:
    assert pilot.ab_command("F1", None) == [
        "uv", "run", "shipharness", "ab", "--section", "demo-1", "--feature", "F1",
        "--purpose", "pilot", "--no-preview", "--profile", "standard",
    ]  # fmt: skip
    assert pilot.ab_command("F2", "stop-1")[-7:-2] == [
        "--variant", "stop-1", "--purpose", "pilot", "--no-preview",
    ]  # fmt: skip


def test_variants_option_maps_features_to_dataset_variants() -> None:
    assert pilot.parse_variants("F1=trap-legacy-pattern, F2=stop-1") == {
        "F1": "trap-legacy-pattern",
        "F2": "stop-1",
    }
    assert pilot.parse_variants("") == {}


def test_budgets_option_adds_the_session_budget_override() -> None:
    assert pilot.parse_budgets("F2=12/38") == {"F2": "12,38"}
    cmd = pilot.ab_command("F2", None, "12,38")
    assert cmd[-7:-2] == ["--session-budget", "12,38", "--purpose", "pilot", "--no-preview"]


def test_profile_option_passes_through_and_defaults_to_standard() -> None:
    # Owner, 2026-10-17: pilot runs keep the standard profile unless asked.
    assert pilot.ab_command("F1", None)[-2:] == ["--profile", "standard"]
    assert pilot.ab_command("F3", None, None, "class")[-2:] == ["--profile", "class"]
    args = pilot.parse_args([])
    assert args.profile == "standard"
    assert pilot.parse_args(["--profile", "class"]).profile == "class"


def test_judged_fields_ignore_the_capture_time() -> None:
    # The 2026-10-17 determinism check: ten judgements differed only in `captured_at`.
    first = {"run_id": "r-1", "passed_primary": True, "captured_at": "2026-10-16T22:15:29Z"}
    later = {"run_id": "r-2", "passed_primary": True, "captured_at": "2026-10-16T22:16:19Z"}
    assert pilot.judged(first) == pilot.judged(later)
