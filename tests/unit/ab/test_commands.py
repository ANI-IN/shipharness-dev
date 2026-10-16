from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import typer
from typer.testing import CliRunner

from shipharness.ab import commands
from shipharness.config import Settings
from shipharness.reviewer import Review, ReviewOutcome
from shipharness.tracing import NullTracer

from .test_demo import LINE, Clients, make_deps
from .test_referee import Factory, all_green
from .test_report import fixture_exports

COMMANDS = ["run", "review", "ab", "replay", "report", "experiments"]


def make_app() -> typer.Typer:
    app = typer.Typer()

    @app.callback()
    def main() -> None:
        """test app"""

    commands.register(app)
    return app


@pytest.fixture
def env(course_repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):  # type: ignore[no-untyped-def]
    settings = Settings(
        _env_file=None, runs_dir=tmp_path / "runs", exports_dir=tmp_path / "exports"
    )
    deps = make_deps(course_repo, tmp_path, Clients())
    deps.client_factory = lambda arm: Clients()(arm)
    review = Review(findings=[], tenant_isolation_risk="none", verdict="accept", summary="fine")
    reviews: list[Any] = []

    def reviewer(inp):  # type: ignore[no-untyped-def]
        reviews.append(inp)
        return ReviewOutcome(review=review, status="ok", cost_usd=0.001)

    runtime = SimpleNamespace(
        cost=deps.cost,
        course_repo=course_repo,
        tracer=NullTracer(),
        reviewer=reviewer,
        referee_sandbox_factory=Factory(all_green()),
        sandboxed=True,
        ab_deps=lambda ref, reviewer=True, **kw: deps,
    )
    monkeypatch.setattr(commands, "_settings", lambda: settings)
    monkeypatch.setattr(commands, "_runtime", lambda *a, **kw: runtime)
    dataset = tmp_path / "features.jsonl"
    dataset.write_text(json.dumps(LINE) + "\n", encoding="utf-8")
    return SimpleNamespace(settings=settings, dataset=dataset, reviews=reviews, tmp=tmp_path)


def test_register_adds_every_command() -> None:
    app = make_app()
    for name in COMMANDS:
        result = CliRunner().invoke(app, [name, "--help"])
        assert result.exit_code == 0, (name, result.output)


def test_report_command_reads_exports_and_prints_counts(tmp_path: Path) -> None:
    exports = fixture_exports(tmp_path)
    result = CliRunner().invoke(make_app(), ["report", "--exports", str(exports)])
    assert result.exit_code == 0, result.output
    assert "F1 r1_new_violations: bare 2/3 failing, harness 1/3 failing" in result.output
    assert (exports / "report.html").exists()
    assert result.output.strip().splitlines()[-1].startswith("Cost: $")


def test_review_command_blinds_the_diff(env, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    diff = tmp_path / "d.patch"
    diff.write_text(
        "diff --git a/progress.md b/progress.md\n--- a/progress.md\n+++ b/progress.md\n"
        "@@ -1 +1 @@\n-a\n+b\n"
        "diff --git a/app/x.py b/app/x.py\n--- a/app/x.py\n+++ b/app/x.py\n@@ -1 +1 @@\n-a\n+b\n",
        encoding="utf-8",
    )
    result = CliRunner().invoke(
        make_app(), ["review", "--diff", str(diff), "--task", "Add a filter."]
    )
    assert result.exit_code == 0, result.output
    assert '"verdict": "accept"' in result.output
    [inp] = env.reviews
    assert "progress.md" not in inp.diff and "app/x.py" in inp.diff
    assert "Cost: $" in result.output


def test_ab_command_runs_both_arms_and_then_swap_and_replay(env) -> None:  # type: ignore[no-untyped-def]
    app = make_app()
    result = CliRunner().invoke(
        app, ["ab", "--feature", "F1", "--section", "demo-1", "--dataset", str(env.dataset)]
    )
    assert result.exit_code == 0, result.output
    assert "bare" in result.output and "harness" in result.output
    assert "Cost: $" in result.output
    ab_id = next(line.split()[1] for line in result.output.splitlines() if line.startswith("A/B "))

    swap = CliRunner().invoke(app, ["ab", "--swap", ab_id])
    assert swap.exit_code == 0, swap.output
    assert "identical" in swap.output

    replay = CliRunner().invoke(app, ["replay", ab_id])
    assert replay.exit_code == 0, replay.output
    assert "RECORDING" in replay.output and "Cost: $" in replay.output


def test_ab_command_unknown_feature_exits_1(env) -> None:  # type: ignore[no-untyped-def]
    result = CliRunner().invoke(
        make_app(), ["ab", "--feature", "F9", "--dataset", str(env.dataset)]
    )
    assert result.exit_code == 1
    assert "no task" in result.output


def test_run_command_runs_one_arm(env, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ticket = tmp_path / "ticket.md"
    ticket.write_text("Add cursor pagination.", encoding="utf-8")
    result = CliRunner().invoke(
        make_app(),
        [
            "run",
            "--feature",
            "F1",
            "--checkpoint",
            "m1-s1-start",
            "--ticket-file",
            str(ticket),
            "--layers",
            "none",
        ],
    )
    assert result.exit_code == 0, result.output
    assert result.output.startswith("bare: completed")
    assert "Cost: $" in result.output
