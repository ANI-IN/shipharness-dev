"""VerifyLayer (S4): the gate on finish(claim="done") and the test filters at the end of the test
phase. Contract I-8; CONTRACTS §5 (hooks), §13 (gate), §14 (filters)."""

from __future__ import annotations

import hashlib
import json
from typing import Any, ClassVar

from shipharness.harness.base import BaseLayer, LayerContext, register_layer
from shipharness.harness.decisions import HarnessDecision, LayerName
from shipharness.harness.verify import testphase
from shipharness.harness.verify.checkrun import RunnerOutputError, parse_runner_output
from shipharness.harness.verify.checkrun import runner_command as _runner_command
from shipharness.harness.verify.gate import GATE_CHECKS, GateConfig, run_gate
from shipharness.harness.verify.models import GateResult
from shipharness.runner import git
from shipharness.runner.tools import iter_workspace_files

PREFIX = """\
Verification: when you call finish with claim="done", a gate runs in your sandbox before the \
phase can end: the visible tests, the existing tests, house rules R1-R7, the board, and a clean \
state check (all work committed, ruff clean on changed Python files, one migration head, no debug \
output). If any item fails, finish returns the first three failures and the phase continues. Tests \
you write in the test phase are kept only if they pass the test filters."""


def default_seed(feature_id: str, checkpoint: str) -> int:
    """Fixed seed per task, so the gate's property-based checks are reproducible."""
    digest = hashlib.sha256(f"{feature_id}@{checkpoint}".encode()).hexdigest()
    return int(digest[:8], 16)


@register_layer
class VerifyLayer(BaseLayer):
    name: ClassVar[LayerName] = "verify"

    def __init__(
        self,
        *,
        checks: tuple[str, ...] = GATE_CHECKS,
        seed: int | None = None,
        exemptions: dict[str, list[str]] | None = None,
        baseline_json: str | None = None,
        compute_baseline: bool = True,
        pipeline: testphase.Pipeline | None = None,
        gate_timeout_s: int = 600,
        **_ignored: Any,
    ) -> None:
        self.checks = tuple(checks)
        self.seed = seed
        self.exemptions = dict(exemptions or {})
        self.baseline_json = baseline_json
        self.compute_baseline = compute_baseline
        self.pipeline = pipeline or testphase.filters_pipeline
        self.gate_timeout_s = gate_timeout_s
        self.existing_tests: list[str] = []
        self.gate_count = 0
        self._phase_start: dict[str, tuple[dict[str, str], dict[str, str]]] = {}

    # -- helpers -------------------------------------------------------------------------------

    def _seed(self, ctx: LayerContext) -> int:
        if self.seed is None:
            return default_seed(ctx.spec.feature_id, ctx.spec.checkpoint)
        return self.seed

    def _params(self, ctx: LayerContext) -> dict[str, Any]:
        return {
            "existing_test_files": self.existing_tests,
            "exemptions": self.exemptions,
            "allowed_paths": {k: list(v) for k, v in ctx.spec.allowed_paths.items()},
        }

    def _config(self, ctx: LayerContext) -> GateConfig:
        return GateConfig(
            checkpoint=ctx.spec.checkpoint,
            feature=ctx.spec.feature_id,
            seed=self._seed(ctx),
            checks=self.checks,
            params=self._params(ctx),
            baseline_json=self.baseline_json,
            timeout_s=self.gate_timeout_s,
        )

    def _publish(self, ctx: LayerContext, type_: str, data: Any) -> None:
        if ctx.bus is not None:
            ctx.bus.publish(type_, data, run_id=ctx.spec.run_id, arm=ctx.spec.arm)  # type: ignore[arg-type]

    # -- hooks ---------------------------------------------------------------------------------

    def prepare_workspace(self, ctx: LayerContext) -> list[HarnessDecision]:
        root = ctx.workspace
        self.existing_tests = sorted(
            p.relative_to(root).as_posix()
            for p in iter_workspace_files(root / "tests" / "visible")
            if p.suffix == ".py"
        )
        if self.baseline_json is not None or not self.compute_baseline:
            return []
        self.baseline_json = self._baseline(ctx)
        note = "gate baseline recorded" if self.baseline_json else "gate baseline unavailable"
        return [HarnessDecision(kind="note", layer="verify", message=note)]

    def _baseline(self, ctx: LayerContext) -> str | None:
        """Runner output on the untouched workspace, so the gate counts only new violations."""
        root = f"/tmp/shipharness-gate-baseline-{ctx.spec.run_id}"
        ctx.sandbox.exec(f"rm -rf {root} && mkdir -p {root}/build && cp -a ./. {root}/build/", 300)
        command = _runner_command(
            build=f"{root}/build",
            checks=list(self.checks),
            checkpoint=ctx.spec.checkpoint,
            feature=ctx.spec.feature_id,
            seed=self._seed(ctx),
        )
        output = ctx.sandbox.exec(f"cd {root} && {command}", self.gate_timeout_s)
        ctx.sandbox.exec(f"rm -rf {root}", 60)
        try:
            results, _ = parse_runner_output(output.output)
        except RunnerOutputError:
            return None
        return json.dumps({"results": [r.model_dump(mode="json") for r in results]})

    def context_prefix(self, ctx: LayerContext) -> list[str]:
        if ctx.phase not in self._phase_start:  # first hook of each phase: remember its start
            self._phase_start[ctx.phase] = testphase.snapshot(ctx.workspace)
        return [PREFIX]

    def on_claim_done(self, ctx: LayerContext) -> HarnessDecision | None:
        self.gate_count += 1
        gate_id = f"{ctx.spec.run_id}-g{self.gate_count}"

        def update(result: GateResult) -> None:
            self._publish(ctx, "gate_result", result)

        def progress(item: dict[str, Any]) -> None:
            self._publish(ctx, "check_progress", item)

        result = run_gate(
            ctx.sandbox,
            self._config(ctx),
            gate_id=gate_id,
            # The arm's own changes start after the harness setup commit (placed artifacts).
            base_sha=str(ctx.state.get("harness.setup_sha") or git.initial_sha(ctx.workspace)),
            phase=ctx.phase,
            on_update=update,
            on_progress=progress,
        )
        ctx.state["verify.gate"] = result.model_dump(mode="json")
        data = {"gate_id": gate_id, "seed": self._seed(ctx)}
        if result.passed:
            return HarnessDecision(
                kind="gate_pass", layer="verify", message=f"gate {gate_id} passed", data=data
            )
        return HarnessDecision(kind="gate_fail", layer="verify", message=result.feedback, data=data)

    def on_phase_end(self, ctx: LayerContext) -> list[HarnessDecision]:
        if ctx.phase != "test":
            return []
        shas, texts = self._phase_start.get("test") or testphase.snapshot(ctx.workspace)
        candidates, broken = testphase.find_candidates(ctx.workspace, texts)
        testphase.delete_files(ctx.workspace, list(broken))
        discarded = {f"{rel}::<file>": reason for rel, reason in broken.items()}
        if not candidates:
            return [self._filter_note(ctx, [], discarded, "no new tests to filter")]
        try:
            results = self.pipeline(candidates, ctx, shas)
        except testphase.PipelineUnavailable as exc:
            kept = [c["test_id"] for c in candidates]
            return [self._filter_note(ctx, kept, discarded, f"test filters unavailable: {exc}")]
        reasons = testphase.discarded_reasons(results)
        by_file: dict[str, list[str]] = {}
        for c in candidates:
            if c["test_id"] in reasons:
                by_file.setdefault(c["file"], []).append(c["test_id"].split("::", 1)[1])
        testphase.remove_tests(ctx.workspace, by_file)
        kept = [c["test_id"] for c in candidates if c["test_id"] not in reasons]
        discarded.update(reasons)
        return [self._filter_note(ctx, kept, discarded, "")]

    def _filter_note(
        self, ctx: LayerContext, kept: list[str], discarded: dict[str, str], extra: str
    ) -> HarnessDecision:
        if kept or discarded:
            ctx.sandbox.exec(
                "git add -A tests/visible && git commit -q -m "
                f"'test: keep {len(kept)} tests that passed the filters' || true",
                120,
            )
        message = f"test filters: kept {len(kept)}, discarded {len(discarded)}"
        return HarnessDecision(
            kind="note",
            layer="verify",
            message=f"{message}; {extra}" if extra else message,
            data={"kept": kept, "discarded": discarded},
        )
