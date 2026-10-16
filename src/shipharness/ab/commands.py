"""CLI commands: run, review, ab, replay, report, experiments. Wired into cli.py with register(app).
Every command prints a cost line at exit."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any

import typer

from shipharness.config import Settings
from shipharness.config.prices import REPO_ROOT

FEATURES_FILE = REPO_ROOT / "datasets" / "teamtrack-features-v1.jsonl"


def _settings() -> Settings:
    return Settings()


def _runtime(settings: Settings, project: str, **kw: Any) -> Any:
    from shipharness.ab.runtime import build_runtime

    return build_runtime(settings, project=project, **kw)


# LangSmith project and cost session per purpose. Class projects hold class runs only.
PURPOSE_HELP = "class (needs SHIPHARNESS_CLASS_DATE), pilot, or assignment: the LangSmith project."
OTHER_PURPOSES = {
    "pilot": ("shipharness-pilot", "pilot"),
    "assignment": ("shipharness-assignments", "assignment"),
}


def _trace_target(settings: Settings, purpose: str) -> tuple[str, str]:
    """(LangSmith project, cost session id) for a command's purpose."""
    if purpose in OTHER_PURPOSES:
        return OTHER_PURPOSES[purpose]
    if purpose != "class":
        typer.echo(f"x unknown purpose {purpose!r}: class, pilot, or assignment")
        raise typer.Exit(2)
    day = settings.shipharness_class_date
    if not day:
        typer.echo(
            "x SHIPHARNESS_CLASS_DATE is not set: set it in .env to the class day (YYYY-MM-DD) "
            "for class commands, or pass --purpose pilot for a pilot run"
        )
        raise typer.Exit(2)
    return f"shipharness-class-{day}", day


def _key_problem(settings: Settings) -> str | None:
    """None when OpenAI accepts the key for the agent model (a model metadata request: no tokens,
    no cost); otherwise the error type, never the key or the message text."""
    import openai

    from shipharness.ab import clients

    try:
        clients.make_openai_client(settings, timeout_s=30).models.retrieve(settings.openai_model)
    except openai.AuthenticationError:
        return "invalid key (AuthenticationError)"
    except openai.PermissionDeniedError:
        return "no access (PermissionDeniedError)"
    except openai.NotFoundError:
        return f"no access to {settings.openai_model} (NotFoundError)"
    except openai.APIConnectionError:
        return "OpenAI unreachable (APIConnectionError)"
    except openai.APIError as exc:
        return type(exc).__name__
    return None


def _live_guard(settings: Settings, deps: Any) -> None:
    """Every live A/B (demo-N, final, pilot) calls OpenAI: refuse before any arm starts when the key
    is missing or rejected, or the runtime would use a stand-in model client. Never falls back to a
    scripted or recorded run; replay (RECORDING) is the explicit fallback (owner, 2026-10-17)."""
    from shipharness.runner.model import OpenAIModelClient

    key = settings.openai_api_key.get_secret_value().strip() if settings.openai_api_key else ""
    if not key:
        typer.echo(
            "x OPENAI_API_KEY is missing: live A/B runs call OpenAI and never fall back to a "
            "stand-in; add the key to .env (or use make replay, which shows RECORDING)"
        )
        raise typer.Exit(2)
    problem = _key_problem(settings)
    if problem:
        typer.echo(f"x OpenAI refused the key: {problem}; no arm was started")
        raise typer.Exit(2)
    try:
        client = deps.client_factory("bare")
    except Exception as exc:  # noqa: BLE001 - reported as one line
        typer.echo(f"x the live OpenAI client could not be created: {type(exc).__name__}")
        raise typer.Exit(2) from None
    if not isinstance(client, OpenAIModelClient):
        typer.echo("x live A/B runs need the OpenAI client; a stand-in model client is refused")
        raise typer.Exit(2)


def _purpose_runtime(settings: Settings, purpose: str, **kw: Any) -> Any:
    project, session = _trace_target(settings, purpose)
    return _runtime(settings, project, session_id=session, **kw)


def _load_task(dataset: Path, feature: str | None, example: str | None, variant: str) -> Any:
    from shipharness.ab.demo import ABTask

    if not dataset.is_file():
        typer.echo(f"x dataset not found: {dataset}")
        raise typer.Exit(1)
    for line in dataset.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        meta, inputs = data.get("metadata", {}), data["inputs"]
        if example and meta.get("example_id") == example:
            return ABTask.from_dataset_line(data)
        if not example and inputs["feature_id"] == feature and inputs["variant"] == variant:
            return ABTask.from_dataset_line(data)
    typer.echo(f"x no task for feature={feature} example={example} variant={variant}")
    raise typer.Exit(1)


def _exit_code(statuses: list[str]) -> int:
    if any(s == "ERROR" for s in statuses):
        return 1
    return 2 if any(s.startswith("ABORTED") for s in statuses) else 0


def _print_record(record: Any) -> None:
    typer.echo(
        f"  {record.arm:<8} {record.status:<17} claim={record.claim:<8} "
        f"primary={json.dumps(record.primary)} passed={record.passed_primary} "
        f"hidden {record.hidden_passed}/{record.hidden_total} "
        f"mutants {record.mutants_killed}/{record.mutants_total} "
        f"reviewer={record.reviewer_verdict} cost=${record.cost_usd:.4f}"
    )


def register(app: typer.Typer) -> None:
    @app.command("run")
    def run_cmd(
        feature: str = typer.Option(..., help="Feature id, e.g. F1."),
        checkpoint: str = typer.Option(..., help="Checkpoint tag, e.g. m1-s1-start."),
        ticket_file: Path = typer.Option(..., exists=True, dir_okay=False),
        layers: str = typer.Option("all", help="none, all, a list, or -<layer> removals."),
        workspace: Path | None = typer.Option(None, help="Existing arm workspace (git repo)."),
        from_working_tree: bool = typer.Option(False, help="Export the working tree, not a tag."),
        purpose: str = typer.Option("class", help=PURPOSE_HELP),
    ) -> None:
        """Run one agent (harness arm, or bare with --layers none) on a ticket."""
        from shipharness.ab.demo import ABTask, arm_specs, run_arm
        from shipharness.ab.runtime import cost_line
        from shipharness.ab.workspace import create_arm_workspace, new_run_id
        from shipharness.events import EventBus
        from shipharness.harness.base import parse_layers

        settings = _settings()
        names = parse_layers(layers)
        arm = "harness" if names else "bare"
        rt = _purpose_runtime(settings, purpose)
        task = ABTask(feature, checkpoint, ticket_file.read_text(encoding="utf-8"))
        run_id = new_run_id()
        ws = workspace or create_arm_workspace(
            run_id, arm, rt.course_repo, None if from_working_tree else checkpoint
        )
        spec = arm_specs(
            task,
            settings,
            ab_id=None,
            harness_layers=names,
            workspaces={arm: ws},
            run_ids={arm: run_id},
        )[arm]
        run_dir = Path(settings.runs_dir) / run_id
        deps = rt.ab_deps(None if from_working_tree else checkpoint)
        with EventBus(run_dir / "events.jsonl", ab_id=None) as bus:
            result = run_arm(task, spec, deps, bus, run_dir)
        typer.echo(f"{arm}: {result.status}, claim={result.claim}, turns={result.turns_total}")
        typer.echo(f"diff: {result.diff_path}  run log: {run_dir / 'events.jsonl'}")
        if result.error:
            typer.echo(f"error: {result.error}")
        typer.echo(cost_line(rt.cost))
        raise typer.Exit(_exit_code([result.status]))

    @app.command("review")
    def review_cmd(
        diff: Path = typer.Option(..., exists=True, dir_okay=False, help="Unified diff file."),
        task: str = typer.Option(..., help="Ticket text, or @file to read it from a file."),
        criteria: Path | None = typer.Option(None, help="Directory with SECURITY.md etc."),
        purpose: str = typer.Option("class", help=PURPOSE_HELP),
    ) -> None:
        """Blinded review of a diff by OPENAI_EVAL_MODEL (structured output)."""
        from shipharness.ab.runtime import cost_line
        from shipharness.reviewer import ReviewInput, blind, grading_criteria

        settings = _settings()
        rt = _purpose_runtime(settings, purpose)
        ticket = Path(task[1:]).read_text(encoding="utf-8") if task.startswith("@") else task
        text = grading_criteria(criteria) if criteria else grading_criteria()
        inp = ReviewInput(task=ticket, diff=blind(diff.read_bytes()), grading_criteria=text)
        outcome = rt.reviewer(inp)
        if outcome.review is not None:
            typer.echo(outcome.review.model_dump_json(indent=2))
        else:
            typer.echo(f"no verdict: {outcome.status} {outcome.detail}")
        typer.echo(cost_line(rt.cost))
        code = {"ok": 0, "cap": 2}.get(outcome.status, 1)
        raise typer.Exit(code)

    @app.command("ab")
    def ab_cmd(
        feature: str | None = typer.Option(None, help="Feature id (canonical variant)."),
        example: str | None = typer.Option(None, help="Dataset example id, e.g. F1-canonical."),
        variant: str = typer.Option("canonical"),
        section: str | None = typer.Option(None, help="demo-1..demo-4 or final: layer stack."),
        layers: str | None = typer.Option(None, help="Harness arm layers (or -<layer>)."),
        dataset: Path = typer.Option(FEATURES_FILE, help="Features JSONL."),
        k: int = typer.Option(1, min=1, help="Repeat the A/B k times (every run is a dot)."),
        reviewer: bool = typer.Option(True, "--reviewer/--no-reviewer"),
        replay: str | None = typer.Option(None, help="Replay a recorded A/B or run id."),
        swap: str | None = typer.Option(
            None, help="Swap test on a recorded A/B or run id, or `latest` (of --section)."
        ),
        from_working_tree: bool = typer.Option(False, help="Export the working tree, not a tag."),
        preview: bool = typer.Option(
            True, "--preview/--no-preview", help="Board preview containers (off for batch runs)."
        ),
        purpose: str = typer.Option("class", help=PURPOSE_HELP),
        session_budget: str | None = typer.Option(
            None,
            help="Override the task's session turn budget, e.g. 12,38 (pre-registered levers).",
        ),
    ) -> None:
        """Same task, harness off vs on, both judged by the referee."""
        from shipharness.ab.demo import run_ab, section_layers
        from shipharness.ab.runtime import cost_line
        from shipharness.harness.base import parse_layers

        if replay or swap:
            _recorded(replay=replay, swap=swap, reviewer=reviewer, section=section, purpose=purpose)
            return
        settings = _settings()
        task = _load_task(dataset, feature, example, variant)
        if session_budget:
            try:
                turns = [int(part) for part in session_budget.split(",")]
            except ValueError:
                turns = []
            if not turns or min(turns) < 1:
                typer.echo(
                    f"x --session-budget takes positive integers, e.g. 12,38: {session_budget!r}"
                )
                raise typer.Exit(2)
            task = dataclasses.replace(task, session_budget=turns)
        if section:
            modifier = layers if layers and layers.startswith("-") else None
            names = section_layers(section, modifier)
        else:
            names = parse_layers(layers or "all")
        rt = _purpose_runtime(settings, purpose, final=section == "final")
        extra: dict[str, Any] = {} if preview else {"preview_factory": None}
        ref = None if from_working_tree else task.checkpoint
        deps = rt.ab_deps(ref, reviewer=reviewer, **extra)
        _live_guard(settings, deps)
        statuses: list[str] = []
        for _ in range(k):
            result = run_ab(task, names, deps, section=section)
            typer.echo(f"A/B {result.ab_id} ({task.feature_id}, layers={sorted(names)})")
            for arm_run in result.arms.values():
                _print_record(arm_run.record)
                statuses.append(arm_run.result.status)
        typer.echo(cost_line(rt.cost))
        raise typer.Exit(_exit_code(statuses))

    def _recorded(
        *,
        replay: str | None,
        swap: str | None,
        reviewer: bool,
        section: str | None = None,
        purpose: str = "class",
    ) -> None:
        from shipharness.ab.recorded import (
            RecordedDeps,
            UnpinnedRecord,
            find_run_dir,
            load_ab,
            replay_ab,
        )
        from shipharness.ab.recorded import swap_test as run_swap
        from shipharness.ab.runtime import cost_line

        settings = _settings()
        wanted = (replay or swap) or ""
        try:
            run_dir = find_run_dir(Path(settings.runs_dir), wanted, section=section)
            load_ab(run_dir).export_ref()  # refuses a record without a pinned checkpoint commit
        except FileNotFoundError as exc:
            if wanted != "latest":
                hint = "check the A/B or run id"
            elif section:
                hint = f"run `make {section}` first, or pass AB=<id>"
            else:
                hint = "run an A/B first (make demo-N), or pass AB=<id>"
            typer.echo(f"x {exc}; {hint}")
            raise typer.Exit(2) from None
        except UnpinnedRecord as exc:
            typer.echo(f"x {exc}")
            raise typer.Exit(2) from None
        rt = _purpose_runtime(settings, purpose)
        deps = RecordedDeps(
            course_repo=rt.course_repo,
            referee_sandbox_factory=rt.referee_sandbox_factory,
            runs_dir=Path(settings.runs_dir),
            exports_dir=Path(settings.exports_dir),
            tracer=rt.tracer,
            reviewer=rt.reviewer if reviewer and replay else None,
            sandboxed=rt.sandboxed,
            container_paths=rt.sandboxed,
        )
        if swap:
            report = run_swap(run_dir, deps)
            verdict = "identical" if report.identical else "DIFFERENT"
            typer.echo(f"Swap test on {report.ab_id}: judged measures {verdict}")
            for arm, diffs in report.differences.items():
                for name, (before, after) in diffs.items():
                    typer.echo(f"  {arm} {name}: {before} -> {after}")
            typer.echo(cost_line(rt.cost))
            raise typer.Exit(0 if report.identical else 1)
        out = replay_ab(run_dir, deps)
        typer.echo(
            f"RECORDING: replay {out.ab_id} of {out.source_ab_id} ({out.events_replayed} events)"
        )
        for record in out.records.values():
            _print_record(record)
        typer.echo(cost_line(rt.cost))

    @app.command("replay")
    def replay_cmd(
        run: str = typer.Argument(..., help="A/B id or run id."),
        reviewer: bool = typer.Option(False, "--reviewer/--no-reviewer"),
        purpose: str = typer.Option("class", help=PURPOSE_HELP),
    ) -> None:
        """Replay a recorded A/B (RECORDING) and re-run the referee live."""
        _recorded(replay=run, swap=None, reviewer=reviewer, purpose=purpose)

    @app.command("report")
    def report_cmd(
        exports: Path = typer.Option(Path("exports"), help="Exports directory."),
        out: Path | None = typer.Option(None, help="Output directory (default: exports)."),
        include_recorded: bool = typer.Option(False, help="Include replays."),
    ) -> None:
        """A/B report from exports/ only: dots per run and counts per arm."""
        from shipharness.ab.report import build_report, write_report

        path = write_report(exports, out or exports, include_recorded)
        report = build_report(exports, include_recorded)
        for group in report["groups"]:
            counts = ", ".join(f"{a} {i['failing']} failing" for a, i in group["arms"].items())
            typer.echo(f"{group['feature_id']} {group['measure']}: {counts}")
        typer.echo(f"report: {path}")
        typer.echo(f"Cost: $0.000000 (no model calls; runs in exports ${report['cost_usd']:.6f})")
        raise typer.Exit(0)

    @app.command("experiments")
    def experiments_cmd(
        dataset: str = typer.Option("teamtrack-features-v1", help="LangSmith dataset."),
        split: str | None = typer.Option(None, help="Split, e.g. section-1."),
        k: int = typer.Option(2, min=1, help="num_repetitions per arm."),
        layers: str = typer.Option("all", help="Harness arm layers (or -<layer>)."),
        batch: str = typer.Option("batch-1", help="Batch label (project name and tags)."),
        reviewer: bool = typer.Option(False, "--reviewer/--no-reviewer"),
        from_working_tree: bool = typer.Option(False, help="Export the working tree, not tags."),
    ) -> None:
        """Both arms via LangSmith evaluate() with num_repetitions=k; scores to exports/."""
        from shipharness.ab.clients import make_langsmith_client
        from shipharness.ab.experiments import ExperimentPlan, run_experiments
        from shipharness.ab.runtime import cost_line
        from shipharness.harness.base import parse_layers

        settings = _settings()
        rt = _runtime(
            settings, "shipharness-experiments", experiment=True, session_id="experiments"
        )
        names = parse_layers(layers)
        plan = ExperimentPlan(
            dataset=dataset,
            split=split,
            k=k,
            harness_layers=names,
            batch=batch,
            from_working_tree=from_working_tree,
        )
        deps = rt.ab_deps(None, reviewer=reviewer)  # checkpoints come from each example
        exports = run_experiments(plan, deps, make_langsmith_client(settings))
        for arm, export in exports.items():
            typer.echo(f"{arm}: {export['name']} {export['stats']} {export.get('url') or ''}")
        typer.echo(cost_line(rt.cost))
        raise typer.Exit(0)
