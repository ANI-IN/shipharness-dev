"""One A/B: the same task run by the bare arm and the harness arm in parallel, then judged by the
same referee (DESIGN §3.4, §8.3). Used by `shipharness ab`, `make demo-N`, and the experiments.

Integrity rules implemented here: both specs come from one set of values (model, effort, ticket,
checkpoint, budgets, cost cap, tools, sandbox policy); the only differences are the arm label, run
id, layers, and workspace path. The arms run concurrently. Every run, aborted or not, is judged.
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, get_args

from shipharness.ab.referee import (
    Referee,
    RefereeDeps,
    RefereeTask,
    Reviewer,
    SandboxFactory,
)
from shipharness.ab.score import ScoreRecord
from shipharness.ab.workspace import create_arm_workspace, new_ab_id, new_run_id
from shipharness.config import Settings
from shipharness.cost import CostTracker
from shipharness.events import Arm, EventBus
from shipharness.harness.base import LAYER_ORDER, Harness, parse_layers
from shipharness.harness.decisions import LayerName
from shipharness.harness.verify.layer import default_seed
from shipharness.runner import git
from shipharness.runner.loop import RunOptions, run_agent
from shipharness.runner.model import ModelClient
from shipharness.runner.models import AgentRunResult, AgentRunSpec
from shipharness.sandbox.base import Sandbox
from shipharness.tracing import NullTracer, Tracer

ARMS: tuple[Arm, ...] = get_args(Arm)
SECTION_STACKS: dict[str, tuple[LayerName, ...]] = {
    "demo-1": ("instructions",),
    "demo-2": ("instructions", "state"),
    "demo-3": ("instructions", "state", "scope"),
    "demo-4": LAYER_ORDER,
    "final": LAYER_ORDER,
}


def section_layers(section: str, modifier: str | None = None) -> frozenset[LayerName]:
    """The harness arm's layers for a section demo (DESIGN §6.6); `-<layer>` removes one."""
    stack = set(SECTION_STACKS[section])
    if modifier:
        removed = parse_layers(modifier if modifier.startswith("-") else f"-{modifier}")
        stack -= set(LAYER_ORDER) - set(removed)
    return frozenset(stack)


@dataclass
class ABTask:
    feature_id: str
    checkpoint: str
    ticket_text: str
    variant: str = "canonical"
    session_budget: list[int] = field(default_factory=lambda: [30])
    test_phase_turns: int = 12
    hidden_test_ids: list[str] = field(default_factory=list)
    allowed_paths: dict[str, list[str]] = field(default_factory=dict)
    mutant_set: str = ""
    primary_measure: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dataset_line(cls, line: Mapping[str, Any]) -> ABTask:
        inputs, outputs = line["inputs"], line.get("outputs", {})
        metadata = dict(line.get("metadata", {}))
        return cls(
            feature_id=inputs["feature_id"],
            checkpoint=inputs["checkpoint"],
            ticket_text=inputs["ticket_text"],
            variant=inputs.get("variant", "canonical"),
            session_budget=list(inputs.get("session_budget", [30])),
            test_phase_turns=int(metadata.get("test_phase_turns", 12)),
            hidden_test_ids=list(outputs.get("hidden_test_ids", [])),
            allowed_paths={k: list(v) for k, v in outputs.get("allowed_paths", {}).items()},
            mutant_set=outputs.get("mutant_set", ""),
            primary_measure=outputs.get("primary_measure", ""),
            metadata=metadata,
        )

    def harness_kwargs(self) -> dict[str, Any]:
        """Feature data the state and scope layers accept (Harness.from_names kwargs)."""
        return {
            "feature_category": self.metadata.get("category", "feature"),
            "feature_description": self.metadata.get("description", self.ticket_text[:200]),
            "feature_steps": list(self.metadata.get("steps", [])),
        }

    def referee_task(self) -> RefereeTask:
        return RefereeTask(
            feature_id=self.feature_id,
            checkpoint=self.checkpoint,
            ticket_text=self.ticket_text,
            variant=self.variant,
            hidden_test_ids=self.hidden_test_ids,
            allowed_paths=self.allowed_paths,
            primary_measure=self.primary_measure,
            mutant_set=self.mutant_set,
        )


ClientFactory = Callable[[Arm], ModelClient]
ArmSandboxFactory = Callable[[Arm, Path, EventBus, str], Sandbox]


@dataclass
class ABDeps:
    settings: Settings
    course_repo: Path
    checkpoint_ref: str | None
    client_factory: ClientFactory
    sandbox_factory: ArmSandboxFactory
    referee_sandbox_factory: SandboxFactory
    cost: CostTracker
    tracer: Tracer = field(default_factory=NullTracer)
    reviewer: Reviewer | None = None
    grading_criteria: str = ""
    workspace_base: Path | None = None
    layer_registry: Mapping[str, type] | None = None
    harness_kwargs: dict[str, Any] = field(default_factory=dict)
    mutants: list[Any] = field(default_factory=list)
    seed: int | None = None
    sandboxed: bool = True
    container_paths: bool = True
    policy_summary: str = ""
    tags: list[str] = field(default_factory=list)
    preview_factory: Callable[[Arm, EventBus, str], Any] | None = None  # board preview (console)


@dataclass
class ArmRun:
    spec: AgentRunSpec
    result: AgentRunResult
    record: ScoreRecord


@dataclass
class ABResult:
    ab_id: str
    arms: dict[Arm, ArmRun]
    run_dir: Path


def arm_specs(
    task: ABTask,
    settings: Settings,
    *,
    ab_id: str,
    harness_layers: frozenset[LayerName],
    workspaces: Mapping[Arm, Path],
    run_ids: Mapping[Arm, str],
) -> dict[Arm, AgentRunSpec]:
    shared: dict[str, Any] = dict(
        ab_id=ab_id,
        feature_id=task.feature_id,
        checkpoint=task.checkpoint,
        ticket_text=task.ticket_text,
        variant=task.variant,
        phases=("build", "test"),
        session_budget=list(task.session_budget),
        test_phase_turns=task.test_phase_turns,
        allowed_paths=task.allowed_paths,
        model=settings.openai_model,
        reasoning_effort=settings.openai_reasoning_effort,
        max_output_tokens=settings.max_output_tokens,
        service_tier=settings.openai_service_tier,
        cost_limit_usd=settings.max_run_cost_usd,
    )
    return {
        arm: AgentRunSpec(
            **shared,
            run_id=run_ids[arm],
            arm=arm,
            layers=harness_layers if arm == "harness" else frozenset(),
            workspace=workspaces[arm],
        )
        for arm in ARMS
    }


def _error_result(spec: AgentRunSpec, message: str) -> AgentRunResult:
    return AgentRunResult(
        run_id=spec.run_id,
        arm=spec.arm,
        status="ERROR",
        claim="none",
        claim_summary="",
        sessions=[],
        phase_shas={},
        diff_path=None,
        cost_usd=0.0,
        turns_total=0,
        wall_s=0.0,
        trace_url=None,
        error=message[:300],
    )


def _harness(
    task: ABTask, spec: AgentRunSpec, deps: ABDeps, layers: frozenset[LayerName]
) -> Harness:
    if spec.arm == "bare" or not layers:
        return Harness([])
    kwargs = {**task.harness_kwargs(), **deps.harness_kwargs}
    return Harness.from_names(layers, deps.layer_registry, **kwargs)


def _run_arm(
    task: ABTask, spec: AgentRunSpec, deps: ABDeps, bus: EventBus, run_dir: Path
) -> AgentRunResult:
    """One arm, start to finish. Never raises: a failure becomes an ERROR result."""
    s = deps.settings
    options = RunOptions(
        wrapup_turns=s.wrapup_turns,
        tool_timeout_s=s.tool_timeout_s,
        run_timeout_s=s.run_timeout_s,
        policy_summary=deps.policy_summary,
        tool_log_dir=run_dir / spec.arm / "tool-logs",
        diff_path=run_dir / spec.arm / "diff.patch",
        tags=list(deps.tags),
    )
    try:
        harness = _harness(task, spec, deps, spec.layers)
        sandbox = deps.sandbox_factory(spec.arm, spec.workspace, bus, spec.run_id)
        sandbox.start()
    except Exception as exc:  # noqa: BLE001 - recorded as an ERROR run, still judged
        return _error_result(spec, f"arm setup failed: {type(exc).__name__}: {exc}")
    try:
        client = deps.client_factory(spec.arm)
        return run_agent(spec, harness, sandbox, bus, deps.cost, deps.tracer, client, options)
    finally:
        sandbox.stop()


def _start_previews(
    deps: ABDeps, bus: EventBus, specs: Mapping[Arm, AgentRunSpec]
) -> tuple[threading.Event, list[threading.Thread]]:
    stop = threading.Event()
    threads: list[threading.Thread] = []
    if deps.preview_factory is None:
        return stop, threads
    for arm, spec in specs.items():
        preview = deps.preview_factory(arm, bus, spec.run_id)
        preview.start_server()
        thread = threading.Thread(target=preview.run, args=(stop,), daemon=True)
        thread.start()
        threads.append(thread)
    return stop, threads


def run_ab(
    task: ABTask,
    harness_layers: frozenset[LayerName],
    deps: ABDeps,
    *,
    ab_id: str | None = None,
) -> ABResult:
    ab_id = ab_id or new_ab_id()
    run_dir = Path(deps.settings.runs_dir) / ab_id
    run_ids = {arm: new_run_id() for arm in ARMS}
    workspaces = {
        arm: create_arm_workspace(
            ab_id, arm, deps.course_repo, deps.checkpoint_ref, base=deps.workspace_base
        )
        for arm in ARMS
    }
    specs = arm_specs(
        task,
        deps.settings,
        ab_id=ab_id,
        harness_layers=harness_layers,
        workspaces=workspaces,
        run_ids=run_ids,
    )
    seed = deps.seed if deps.seed is not None else default_seed(task.feature_id, task.checkpoint)
    referee = Referee(
        task.referee_task(),
        RefereeDeps(
            course_repo=deps.course_repo,
            checkpoint_ref=deps.checkpoint_ref,
            sandbox_factory=deps.referee_sandbox_factory,
            exports_dir=Path(deps.settings.exports_dir),
            base_dir=workspaces["bare"].parent.parent / "referee",
            seed=seed,
            tracer=deps.tracer,
            reviewer=deps.reviewer,
            grading_criteria=deps.grading_criteria,
            mutants=deps.mutants,
            sandboxed=deps.sandboxed,
            container_paths=deps.container_paths,
        ),
    )
    with EventBus(run_dir / "events.jsonl", ab_id=ab_id) as bus:
        stop, previews = _start_previews(deps, bus, specs)
        # [walkthrough:Opening:two_arms] start
        # Same task, same model, effort, budgets, cost cap, tools, and sandbox for both arms.
        # The only difference is the harness. Both arms run at the same time.
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="arm") as pool:
            futures = {
                arm: pool.submit(_run_arm, task, specs[arm], deps, bus, run_dir) for arm in ARMS
            }
            results = {arm: future.result() for arm, future in futures.items()}
        stop.set()
        for thread in previews:
            thread.join(timeout=10)

        # Both arms are judged by the same referee on what they shipped (aborted runs too).
        referee.baseline()
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="referee") as pool:
            verdicts = {
                arm: pool.submit(_judge, referee, specs[arm], results[arm], bus, run_dir)
                for arm in ARMS
            }
            records = {arm: future.result() for arm, future in verdicts.items()}
        # [walkthrough:Opening:two_arms] end
    arms = {arm: ArmRun(specs[arm], results[arm], records[arm]) for arm in ARMS}
    return ABResult(ab_id=ab_id, arms=arms, run_dir=run_dir)


def phase_changed_files(spec: AgentRunSpec, result: AgentRunResult) -> list[str]:
    """Files the arm changed during the test phase (the S3 measure's second half)."""
    shas = result.phase_shas.get("test")
    return git.changed_files(spec.workspace, shas[0]) if shas else []


def _judge(
    referee: Referee, spec: AgentRunSpec, result: AgentRunResult, bus: EventBus, run_dir: Path
) -> ScoreRecord:
    diff = result.diff_path.read_bytes() if result.diff_path and result.diff_path.exists() else b""
    verdict = referee.judge(
        run_id=spec.run_id,
        ab_id=spec.ab_id,
        arm=spec.arm,
        layers=sorted(spec.layers),
        result=result,
        diff=diff,
        bus=bus,
        run_log=run_dir / "events.jsonl",
        test_phase_files=phase_changed_files(spec, result),
    )
    return verdict.record
