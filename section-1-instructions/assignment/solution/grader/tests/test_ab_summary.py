"""Tests for assignment/ab_summary.py: R1 and R3 counts per arm from exports/, no model calls."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from helpers import A1, load

summary = load("a1_ab_summary", A1 / "assignment" / "ab_summary.py")


def score(run_id: str, arm: str, variant: str, r1: int, r3: int, **extra: object) -> dict:
    record = {
        "run_id": run_id,
        "arm": arm,
        "feature_id": "F1",
        "variant": variant,
        "checkpoint": "m1-s1-start",
        "status": "COMPLETED",
        "r1_new_violations": r1,
        "r1_leaks": r1,
        "r3_new_failures": r3,
        "cost_usd": 0.05,
        "review_cost_usd": 0.0,
    }
    record.update(extra)
    return record


def experiment(name: str, arm: str, batch: str, rows: list[str]) -> dict:
    return {
        "name": name,
        "url": f"https://smith.langchain.com/o/x/datasets/y/compare?selectedSessions={arm}",
        "comparison_url": "https://smith.langchain.com/o/x/datasets/y/compare?selectedSessions=a,b",
        "dataset": "teamtrack-features-v1",
        "split": "section-1",
        "arm": arm,
        "k": 3,
        "metadata": {"batch": batch, "arm": arm, "model": "gpt-6-luna", "effort": "medium"},
        "rows": rows,
    }


@pytest.fixture
def exports(tmp_path: Path) -> Path:
    root = tmp_path / "exports"
    (root / "scores").mkdir(parents=True)
    (root / "experiments").mkdir()
    records = [
        score("b1", "bare", "canonical", 2, 0),
        score("b2", "bare", "canonical", 1, 1),
        score("b3", "bare", "trap", 0, 0, status="ABORTED: cap"),
        score("h1", "harness", "canonical", 0, 0),
        score("h2", "harness", "canonical", 0, 1),
        score("h3", "harness", "trap", 0, 0, status="ERROR"),
    ]
    for record in records:
        path = root / "scores" / f"{record['run_id']}.json"
        path.write_text(json.dumps(record), encoding="utf-8")
    for name, arm, rows in (
        ("shipharness-a1-sam-bare-2026-10-20-ab12", "bare", ["b1", "b2", "b3"]),
        ("shipharness-a1-sam-harness-2026-10-20-cd34", "harness", ["h1", "h2", "h3"]),
        ("shipharness-batch-1-bare-2026-10-01-ef56", "bare", ["b1"]),
    ):
        batch = "a1-sam" if "a1-sam" in name else "batch-1"
        data = experiment(name, arm, batch, rows)
        (root / "experiments" / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
    return root


def test_counts_runs_failing_per_arm_for_r1_and_r3(
    exports: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert summary.main(["--batch", "a1-sam", "--exports", str(exports)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert "| R1: runs with at least one new R1 violation | 2/3 | 0/3 |" in out
    assert "| R3: runs with at least one new R3 failure | 1/3 | 1/3 |" in out
    assert "| R1 leaks (sum over runs) | 3 | 0 |" in out
    assert "| Runs aborted or errored | 1 | 1 |" in out
    assert "- Runs per arm: 3" in out
    assert "- Model and reasoning effort: gpt-6-luna, medium" in out
    assert "- Cost: $0.300000 (run and review cost in the score exports)" in out
    assert any(line.startswith("- Comparison view: https://smith.langchain.com/") for line in out)


def test_lists_each_task_so_the_reading_can_go_task_by_task(
    exports: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    summary.main(["--batch", "a1-sam", "--exports", str(exports)])
    out = capsys.readouterr().out.splitlines()
    assert "| F1 canonical (m1-s1-start) | 2/2 | 0/2 | 1/2 | 1/2 |" in out
    assert "| F1 trap (m1-s1-start) | 0/1 | 0/1 | 0/1 | 0/1 |" in out


def test_an_unknown_batch_exits_2(exports: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert summary.main(["--batch", "a1-nobody", "--exports", str(exports)]) == 2
    assert "no experiments" in capsys.readouterr().out


def test_two_experiments_for_one_arm_need_a_choice(
    exports: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    again = experiment("shipharness-a1-sam-bare-2026-10-21-zz99", "bare", "a1-sam", ["b1"])
    path = exports / "experiments" / "shipharness-a1-sam-bare-2026-10-21-zz99.json"
    path.write_text(json.dumps(again), encoding="utf-8")
    assert summary.main(["--batch", "a1-sam", "--exports", str(exports)]) == 2
    assert "--bare" in capsys.readouterr().out
    argv = ["--batch", "a1-sam", "--exports", str(exports)]
    argv += ["--bare", "shipharness-a1-sam-bare-2026-10-20-ab12"]
    assert summary.main(argv) == 0


def test_a_missing_score_file_is_reported_not_counted(
    exports: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (exports / "scores" / "h3.json").unlink()
    assert summary.main(["--batch", "a1-sam", "--exports", str(exports)]) == 0
    out = capsys.readouterr().out
    assert "! harness: no score export for run h3" in out
    assert "| R1: runs with at least one new R1 violation | 2/3 | 0/2 |" in out
