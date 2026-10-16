from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, ClassVar

import pytest

from shipharness.ab.demo import ABDeps, ABTask, arm_specs, run_ab, section_layers
from shipharness.config import DEFAULT_PRICES_FILE, Prices, Settings
from shipharness.cost import Caps, CostTracker, Usage
from shipharness.events import read_events
from shipharness.harness.base import BaseLayer, LayerContext
from shipharness.harness.decisions import HarnessDecision
from shipharness.runner.model import ScriptedModelClient, Step, tool_step
from shipharness.sandbox import FakeSandbox
from shipharness.tracing import NullTracer, read_exports

from .test_referee import Factory, all_green

LINE = {
    "inputs": {
        "feature_id": "F1",
        "checkpoint": "m1-s1-start",
        "ticket_text": "Add cursor pagination to GET /projects/{id}/issues.",
        "variant": "canonical",
        "session_budget": [6],
    },
    "outputs": {
        "hidden_test_ids": ["teamtrack/tests/hidden/f1/test_secret.py::test_secret"],
        "allowed_paths": {
            "build": ["app/api/**", "tests/visible/**"],
            "test": ["tests/visible/**"],
        },
        "mutant_set": "f1",
        "primary_measure": "r1_new_violations>=1",
    },
    "metadata": {
        "group": "canonical",
        "example_id": "F1-canonical",
        "category": "api",
        "description": "Cursor pagination",
        "steps": ["GET returns next_cursor"],
    },
    "split": ["section-1"],
}


class FakeInstructions(BaseLayer):
    name = "instructions"
    seen_kwargs: ClassVar[list[dict[str, Any]]] = []

    def __init__(self, **kwargs: Any) -> None:
        FakeInstructions.seen_kwargs.append(kwargs)

    def prepare_workspace(self, ctx: LayerContext) -> list[HarnessDecision]:
        (ctx.workspace / "AGENTS.md").write_bytes(b"# Map\n")
        return [HarnessDecision(kind="note", layer="instructions", paths=["AGENTS.md"])]


def steps() -> list[Step]:
    return [
        tool_step("list_dir", path=".", depth=None),
        tool_step("finish", claim="done", summary="built"),
        tool_step("finish", claim="done", summary="tests"),
    ]


class Clients:
    def __init__(self, barrier: threading.Barrier | None = None, **per_arm: list[Step]) -> None:
        self.barrier = barrier
        self.per_arm = per_arm
        self.clients: dict[str, ScriptedModelClient] = {}

    def __call__(self, arm: str) -> ScriptedModelClient:
        barrier = self.barrier

        class Client(ScriptedModelClient):
            def respond(self, *a: Any, **kw: Any):  # type: ignore[no-untyped-def]
                if barrier is not None and not self.inputs:
                    barrier.wait()  # both arms must be in their first turn at the same time
                return super().respond(*a, **kw)

        client = Client(self.per_arm.get(arm, steps()))
        self.clients[arm] = client
        return client


def make_deps(course_repo: Path, tmp_path: Path, clients: Clients, **kw: Any) -> ABDeps:
    settings = Settings(
        _env_file=None, runs_dir=tmp_path / "runs", exports_dir=tmp_path / "exports"
    )
    cost = CostTracker(
        Prices.load(DEFAULT_PRICES_FILE),
        Caps(0.2, 0.04, 2.5, 2.5, 25.0),
        tmp_path / "ledger.jsonl",
        session_id="t",
    )
    sandboxes: dict[str, FakeSandbox] = {}

    def sandbox_factory(arm, ws, bus, run_id):  # type: ignore[no-untyped-def]
        sandboxes[arm] = FakeSandbox()
        return sandboxes[arm]

    base: dict[str, Any] = dict(
        settings=settings,
        course_repo=course_repo,
        checkpoint_ref="m1-s1-start",
        client_factory=clients,
        sandbox_factory=sandbox_factory,
        referee_sandbox_factory=Factory(all_green()),
        cost=cost,
        tracer=NullTracer(),
        workspace_base=tmp_path / "ws",
        layer_registry={"instructions": FakeInstructions},
    )
    base.update(kw)
    deps = ABDeps(**base)
    deps.sandboxes = sandboxes  # type: ignore[attr-defined]
    return deps


def test_task_from_dataset_line() -> None:
    task = ABTask.from_dataset_line(LINE)
    assert task.feature_id == "F1" and task.session_budget == [6]
    assert task.allowed_paths["build"] == ["app/api/**", "tests/visible/**"]
    assert task.primary_measure == "r1_new_violations>=1"
    assert task.harness_kwargs()["feature_steps"] == ["GET returns next_cursor"]


@pytest.mark.parametrize(
    ("section", "modifier", "expected"),
    [
        ("demo-1", None, {"instructions"}),
        ("demo-2", None, {"instructions", "state"}),
        ("demo-3", None, {"instructions", "state", "scope"}),
        ("demo-4", None, {"instructions", "state", "scope", "verify"}),
        ("final", None, {"instructions", "state", "scope", "verify"}),
        ("demo-3", "-state", {"instructions", "scope"}),
    ],
)
def test_section_layer_stacks_follow_design_6_6(
    section: str, modifier: str | None, expected: set[str]
) -> None:
    assert section_layers(section, modifier) == frozenset(expected)


def test_both_arms_get_identical_inputs(tmp_path: Path) -> None:
    task = ABTask.from_dataset_line(LINE)
    settings = Settings(_env_file=None)
    specs = arm_specs(
        task,
        settings,
        ab_id="ab-1",
        harness_layers=frozenset({"instructions"}),
        workspaces={"bare": tmp_path / "b", "harness": tmp_path / "h"},
        run_ids={"bare": "r-b", "harness": "r-h"},
    )
    bare, harness = specs["bare"].public_dict(), specs["harness"].public_dict()
    for differing in ("arm", "run_id", "layers"):
        bare.pop(differing)
        harness.pop(differing)
    assert bare == harness
    assert specs["bare"].layers == frozenset()


def test_run_ab_runs_both_arms_in_parallel_and_scores_both(
    course_repo: Path, tmp_path: Path
) -> None:
    clients = Clients(barrier=threading.Barrier(2, timeout=20))
    deps = make_deps(course_repo, tmp_path, clients)
    FakeInstructions.seen_kwargs.clear()
    result = run_ab(ABTask.from_dataset_line(LINE), frozenset({"instructions"}), deps)
    assert set(result.arms) == {"bare", "harness"}
    for arm_run in result.arms.values():
        assert arm_run.result.status == "completed"
        assert arm_run.record.arm == arm_run.spec.arm
    log = tmp_path / "runs" / result.ab_id / "events.jsonl"
    events = list(read_events(log))
    starts = {e.arm for e in events if e.type == "run_start"}
    assert starts == {"bare", "harness"}
    assert {e.arm for e in events if e.type == "verdict"} == {"bare", "harness"}
    scores = read_exports("scores", tmp_path / "exports")
    assert {s["run_id"] for s in scores} == {a.spec.run_id for a in result.arms.values()}
    assert FakeInstructions.seen_kwargs[-1]["feature_category"] == "api"


def test_workspaces_are_outside_the_course_checkout_and_bare_has_no_harness_files(
    course_repo: Path, tmp_path: Path
) -> None:
    deps = make_deps(course_repo, tmp_path, Clients())
    result = run_ab(ABTask.from_dataset_line(LINE), frozenset({"instructions"}), deps)
    bare_ws = result.arms["bare"].spec.workspace
    harness_ws = result.arms["harness"].spec.workspace
    assert course_repo.resolve() not in bare_ws.resolve().parents
    assert not (bare_ws / "AGENTS.md").exists()
    assert (harness_ws / "AGENTS.md").exists()
    assert not (harness_ws / "tests" / "hidden").exists()


def test_an_aborted_arm_is_kept_and_scored(course_repo: Path, tmp_path: Path) -> None:
    pricey = Usage(input_tokens=1000, output_tokens=500_000)
    clients = Clients(bare=[tool_step("list_dir", path=".", depth=None, usage=pricey)])
    deps = make_deps(course_repo, tmp_path, clients)
    result = run_ab(ABTask.from_dataset_line(LINE), frozenset({"instructions"}), deps)
    assert result.arms["bare"].result.status == "ABORTED: cap"
    assert result.arms["bare"].record.status == "ABORTED: cap"


def test_sandbox_failure_becomes_an_error_run_that_is_still_scored(
    course_repo: Path, tmp_path: Path
) -> None:
    class Broken(FakeSandbox):
        def start(self) -> str:
            raise RuntimeError("docker run failed")

    deps = make_deps(
        course_repo,
        tmp_path,
        Clients(),
        sandbox_factory=lambda arm, ws, bus, run_id: Broken() if arm == "bare" else FakeSandbox(),
    )
    result = run_ab(ABTask.from_dataset_line(LINE), frozenset({"instructions"}), deps)
    assert result.arms["bare"].result.status == "ERROR"
    assert "docker run failed" in (result.arms["bare"].result.error or "")
    assert result.arms["bare"].record.status == "ERROR"
