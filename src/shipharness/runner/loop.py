"""The agent loop (CONTRACTS §4): sessions, the finish tool, caps, and error handling."""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from shipharness.cost import CapExceeded, CostScope, CostTracker
from shipharness.events import EventBus
from shipharness.harness.base import Harness, LayerContext
from shipharness.runner import git
from shipharness.runner.model import ModelClient, ModelResponse, classify_openai_error
from shipharness.runner.models import (
    AgentRunResult,
    AgentRunSpec,
    ClaimValue,
    Phase,
    RunStatus,
    SessionResult,
    ToolCall,
    ToolResult,
)
from shipharness.runner.prompts import (
    BUILD_PHASE,
    CORE_SYSTEM_PROMPT,
    NEUTRAL_RESUME,
    REMINDER,
    TEST_PHASE,
    wrapup_message,
)
from shipharness.runner.tools import TOOL_NAMES, TOOL_SCHEMAS, ToolBox
from shipharness.sandbox.base import Sandbox
from shipharness.tracing import Tracer

# Runs inside the sandbox (never host git on the agent's repo); --no-verify skips repo hooks.
SETUP_COMMIT = (
    "git add -A && git -c user.name=shipharness -c user.email=harness@shipharness.invalid "
    'commit -q --no-verify -m "harness setup"'
)

_ERROR_TEXT = {
    "abort_auth": "OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).",
    "abort_billing": "OpenAI billing limit reached (quota or spend limit); add credit and retry.",
    "abort_other": "OpenAI request failed",
    "retry": "OpenAI request kept failing after retries",
}


@dataclass
class RunOptions:
    wrapup_turns: int = 3
    tool_timeout_s: int = 120
    run_timeout_s: int = 300
    max_attempts: int = 3
    policy_summary: str = ""
    tool_log_dir: Path | None = None
    diff_path: Path | None = None
    sleep: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.monotonic
    tags: list[str] = field(default_factory=list)


class _ModelFailure(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _text_item(role: str, text: str) -> dict[str, Any]:
    return {"role": role, "content": [{"type": "input_text", "text": text}]}


def estimate_input_tokens(items: list[dict[str, Any]], tools: list[dict[str, Any]]) -> int:
    """Rough input size for the cost pre-check: the transcript plus the tool schemas, which are
    sent (and billed) with every call."""
    return (len(json.dumps(items, default=str)) + len(json.dumps(tools))) // 3 + 200


def _target(call: ToolCall) -> str:
    args = call.arguments
    value = args.get("path") or args.get("command") or args.get("pattern") or args.get("selector")
    if call.name == "apply_patch":
        value = ", ".join(
            line[6:]
            for line in str(args.get("patch", "")).splitlines()
            if line.startswith("+++ b/")
        )
    if call.name == "finish":
        value = args.get("claim")
    return str(value or "")[:200]


class _Run:
    """State for one arm's run. Not reused."""

    def __init__(
        self,
        spec: AgentRunSpec,
        harness: Harness,
        sandbox: Sandbox,
        bus: EventBus,
        cost: CostTracker,
        tracer: Tracer,
        client: ModelClient,
        options: RunOptions,
    ) -> None:
        self.spec, self.harness, self.sandbox, self.bus = spec, harness, sandbox, bus
        self.cost, self.tracer, self.client, self.options = cost, tracer, client, options
        self.ctx = LayerContext(
            spec=spec,
            phase=spec.phases[0],
            session_index=0,
            turn=0,
            workspace=spec.workspace,
            sandbox=sandbox,
            bus=bus,
        )
        self.toolbox = ToolBox(
            spec.workspace,
            sandbox,
            bus,
            spec.run_id,
            spec.arm,
            guard=lambda call: harness.before_tool(self.ctx, call),
            tool_log_dir=options.tool_log_dir,
            tool_timeout_s=options.tool_timeout_s,
        )
        self.scope: CostScope = cost.scope("run", spec.run_id, spec.cost_limit_usd)
        self.started = options.clock()
        self.sessions: list[SessionResult] = []
        self.status: RunStatus = "completed"
        self.claim: ClaimValue = "none"
        self.claims: dict[Phase, ClaimValue] = {}
        self.claim_summary = ""
        self.error: str | None = None
        self.turns_total = 0
        self.diff_base: str | None = None  # set to the harness setup commit for harness arms

    # -- events --------------------------------------------------------------------------------

    def emit(self, type_: str, data: Any) -> None:
        self.bus.publish(type_, data, run_id=self.spec.run_id, arm=self.spec.arm)  # type: ignore[arg-type]

    # -- model calls -------------------------------------------------------------------------------

    def call_model(self, items: list[dict[str, Any]]) -> ModelResponse:
        self.cost.check_before_call(
            self.scope,
            self.spec.model,
            estimate_input_tokens(items, TOOL_SCHEMAS),
            self.spec.max_output_tokens,
        )
        attempt = 0
        while True:
            try:
                return self.client.respond(
                    items,
                    TOOL_SCHEMAS,
                    model=self.spec.model,
                    effort=self.spec.reasoning_effort,
                    max_output_tokens=self.spec.max_output_tokens,
                    service_tier=self.spec.service_tier,
                )
            except CapExceeded:
                raise
            except Exception as exc:  # noqa: BLE001 - classified below; never re-raised raw
                kind = classify_openai_error(exc)
                attempt += 1
                if kind != "retry" or attempt >= self.options.max_attempts:
                    detail = _ERROR_TEXT[kind]
                    if kind == "abort_other":
                        status = getattr(exc, "status_code", "n/a")
                        detail = f"{detail}: {type(exc).__name__} (status {status})"
                    raise _ModelFailure(detail) from None
                self.options.sleep(float(2 ** (attempt - 1)))

    def record_usage(
        self, response: ModelResponse, session_index: int, turn: int, turns_left: int
    ) -> None:
        usage = response.usage
        try:
            call_usd = self.cost.record(self.scope, self.spec.model, usage)
        finally:
            excerpt = response.text[:200]
            if not excerpt:
                names = [
                    i.get("name", "")
                    for i in response.output_items
                    if i.get("type") == "function_call"
                ]
                excerpt = ", ".join(names)
            self.emit(
                "turn",
                {
                    "session_index": session_index,
                    "turn": turn,
                    "turns_left": turns_left,
                    "input_tokens": usage.input_tokens,
                    "cached_tokens": usage.cached_tokens,
                    "cache_write_tokens": usage.cache_write_tokens,
                    "output_tokens": usage.output_tokens,
                    "reasoning_tokens": usage.reasoning_tokens,
                    "message_excerpt": excerpt,
                },
            )
        summary = self.cost.summary()
        self.emit(
            "cost",
            {
                "scope": "run",
                "model": self.spec.model,
                "call_usd": round(call_usd, 6),
                "run_usd": round(self.scope.spent_usd, 6),
                "session_usd": round(
                    summary.experiment_total_usd
                    if summary.experiment
                    else summary.session_total_usd,
                    6,
                ),
                "limit_usd": self.scope.limit_usd,
            },
        )

    # -- tool calls -------------------------------------------------------------------------------

    def parse_call(self, item: dict[str, Any]) -> tuple[ToolCall | None, str]:
        call_id = str(item.get("call_id") or item.get("id") or "call_unknown")
        name = str(item.get("name", ""))
        try:
            arguments = json.loads(item.get("arguments") or "{}")
            if not isinstance(arguments, dict):
                raise ValueError("arguments must be a JSON object")
        except (ValueError, TypeError) as exc:
            return None, f"invalid arguments for {name}: not valid JSON ({exc})"
        if name not in TOOL_NAMES:
            return None, f"unknown tool: {name!r}"
        return ToolCall(call_id=call_id, name=name, arguments=arguments), ""  # type: ignore[arg-type]

    def handle_finish(self, call: ToolCall, phase: Phase) -> tuple[ToolResult, str | None]:
        """Returns the tool result and the session end reason (None = keep going)."""
        result = self.toolbox.execute(call)
        if not result.ok:
            return result, None
        claim = call.arguments["claim"]
        summary = str(call.arguments.get("summary", ""))
        self.claim, self.claim_summary = claim, summary
        self.claims[phase] = claim
        # I-5: layers read the claim (the scope layer's status, the verify gate) from state.
        self.ctx.state["last_claim"] = {"phase": phase, "claim": claim, "summary": summary}
        gate_id: str | None = None
        end: str | None = "claim_not_done"
        output = "accepted"
        if claim == "done":
            decision = self.harness.on_claim_done(self.ctx)
            gate_id = decision.data.get("gate_id") if decision else None
            if decision is not None and decision.kind == "gate_fail":
                end = None
                output = f"Not accepted. {decision.message}"
            else:
                end = "claim_done"
        self.emit("claim", {"phase": phase, "claim": claim, "summary": summary, "gate_id": gate_id})
        return result.model_copy(update={"output": output}), end

    # -- sessions ------------------------------------------------------------------------------

    def base_items(self, phase: Phase, resume: bool) -> list[dict[str, Any]]:
        prefix = "\n\n".join([CORE_SYSTEM_PROMPT, *self.harness.context_prefix(self.ctx)])
        phase_text = BUILD_PHASE if phase == "build" else TEST_PHASE
        items = [
            _text_item("developer", prefix),
            _text_item("user", f"{phase_text}\n\nTicket:\n{self.spec.ticket_text}"),
        ]
        if resume:
            extra = self.harness.on_session_start(self.ctx)
            items.append(_text_item("user", "\n\n".join([NEUTRAL_RESUME, *extra])))
        return items

    def run_session(self, phase: Phase, index: int, budget: int, resume: bool) -> SessionResult:
        self.ctx.session_index, self.ctx.turn = index, 0
        start_sha = git.head_sha(self.spec.workspace)
        items = self.base_items(phase, resume)
        turns, text_only, wrapup_sent = 0, 0, False
        ended_by: str = "turn_budget"
        with self.tracer.child(f"session:{index}", "chain", turn_budget=budget, phase=phase):
            while turns < budget:
                remaining = budget - turns
                if not wrapup_sent and remaining <= self.options.wrapup_turns and budget > 1:
                    items.append(
                        _text_item(
                            "user", wrapup_message(remaining, self.harness.wrapup_text(self.ctx))
                        )
                    )
                    wrapup_sent = True
                if self.options.clock() - self.started > self.options.run_timeout_s:
                    ended_by, self.status = "timeout", "ABORTED: timeout"
                    break
                try:
                    response = self.call_model(items)
                    turns += 1
                    self.turns_total += 1
                    self.ctx.turn = turns
                    self.record_usage(response, index, turns, budget - turns)
                except CapExceeded:
                    ended_by, self.status = "cap", "ABORTED: cap"
                    break
                except _ModelFailure as failure:
                    ended_by, self.status, self.error = "error", "ERROR", failure.message
                    break
                items.extend(response.output_items)
                calls = [i for i in response.output_items if i.get("type") == "function_call"]
                if not calls:
                    text_only += 1
                    if text_only >= 2:
                        ended_by, self.claim = "no_tool_call", "none"
                        self.claims[phase] = "none"
                        break
                    items.append(_text_item("user", REMINDER))
                    continue
                text_only = 0
                end = self.process_calls(calls, items, phase)
                if end is not None:
                    ended_by = end
                    break
        result = SessionResult(
            index=index,
            phase=phase,
            turns=turns,
            ended_by=ended_by,  # type: ignore[arg-type]
            start_sha=start_sha,
            end_sha=git.head_sha(self.spec.workspace),
        )
        self.harness.on_session_end(self.ctx, result)
        return result

    def process_calls(
        self, calls: list[dict[str, Any]], items: list[dict[str, Any]], phase: Phase
    ) -> str | None:
        end: str | None = None
        for item in calls:
            call, problem = self.parse_call(item)
            call_id = str(item.get("call_id") or item.get("id") or "call_unknown")
            name = str(item.get("name", ""))
            self.emit(
                "tool_call",
                {"call_id": call_id, "name": name, "target": _target(call) if call else ""},
            )
            if call is None:
                result = ToolResult(call_id=call_id, ok=False, output=problem)
            elif call.name == "finish":
                result, end = self.handle_finish(call, phase)
            else:
                with self.tracer.child(f"tool:{call.name}", "tool", target=_target(call)):
                    result = self.toolbox.execute(call)
                self.harness.after_tool(self.ctx, call, result)
            self.emit(
                "tool_result",
                {
                    "call_id": call_id,
                    "ok": result.ok,
                    "exit_code": result.exit_code,
                    "duration_ms": result.duration_ms,
                    "files_changed": result.files_changed,
                    "output_excerpt": result.output[:500],
                },
            )
            items.append(
                {"type": "function_call_output", "call_id": call_id, "output": result.output}
            )
        return end

    # -- phases --------------------------------------------------------------------------------

    def _run_phases(self, phase_shas: dict[Phase, tuple[str, str]]) -> str | None:
        trace_url: str | None = None
        tags = [self.spec.arm, *self.options.tags]
        with self.tracer.agent_run("agent_run", self.spec.public_dict(), tags=tags) as root:
            trace_url = self.tracer.url(root)
            if trace_url:
                self.emit("trace_link", {"url": trace_url, "kind": "agent"})
            self.harness.prepare_workspace(self.ctx)
            self._commit_harness_setup()
            session_index = 0
            for phase in self.spec.phases:
                if self.status != "completed":
                    break
                self.ctx.phase = phase
                self.claims[phase] = "none"
                phase_start = git.head_sha(self.spec.workspace)
                budgets = (
                    self.spec.session_budget if phase == "build" else [self.spec.test_phase_turns]
                )
                with self.tracer.child(f"phase:{phase}", "chain", session_count=len(budgets)):
                    for position, budget in enumerate(budgets):
                        session_index += 1
                        if position > 0:
                            self.emit(
                                "session_resume",
                                {
                                    "session_index": session_index,
                                    "start_sha": git.head_sha(self.spec.workspace),
                                    "prefix_blocks": ["core", *sorted(self.harness.names)],
                                },
                            )
                        result = self.run_session(phase, session_index, budget, position > 0)
                        self.sessions.append(result)
                        if result.ended_by != "turn_budget":
                            break
                        if position < len(budgets) - 1:
                            self.emit(
                                "session_stop",
                                {
                                    "session_index": session_index,
                                    "ended_by": result.ended_by,
                                    "end_sha": result.end_sha,
                                    "handoff_path": self._handoff_path(),
                                },
                            )
                    self.harness.on_phase_end(self.ctx)
                phase_shas[phase] = (phase_start, git.head_sha(self.spec.workspace))
            if trace_url is None:  # the link lookup can fail transiently; try once more
                trace_url = self.tracer.url(root)
                if trace_url:
                    self.emit("trace_link", {"url": trace_url, "kind": "agent"})
            root.set_outputs({"status": self.status, "claim": self.claim})
        return trace_url

    def _commit_harness_setup(self) -> None:
        """Commit the files the layers placed (AGENTS.md, progress.md, feature_list.json, ...) in
        the sandbox, and diff the harness arm against that commit, so setup files never count as
        the arm's work. The bare arm has no layers: no commit, diff against the checkpoint."""
        if not self.harness.layers:
            return
        self.sandbox.exec(SETUP_COMMIT, self.options.tool_timeout_s)
        setup_sha = git.head_sha(self.spec.workspace)
        if setup_sha:
            self.diff_base = setup_sha
            self.ctx.state["harness.setup_sha"] = setup_sha

    def _handoff_path(self) -> str | None:
        value = self.ctx.state.get("state.handoff_path")
        return str(value) if value else None

    def run(self) -> AgentRunResult:
        self.emit(
            "run_start",
            {"spec": self.spec.public_dict(), "policy_summary": self.options.policy_summary},
        )
        base_sha = ""
        phase_shas: dict[Phase, tuple[str, str]] = {}
        trace_url: str | None = None
        try:
            base_sha = git.initial_sha(self.spec.workspace)
            trace_url = self._run_phases(phase_shas)
        except Exception as exc:  # noqa: BLE001 - the run always ends with a result and run_end
            self.status = "ERROR"
            self.error = f"internal error: {type(exc).__name__}"
        diff_out = self.options.diff_path or (self.spec.workspace.parent / "diff.patch")
        diff_path = None
        try:
            diff_path = git.write_diff(self.spec.workspace, self.diff_base or base_sha, diff_out)
        except Exception as exc:  # noqa: BLE001
            self.error = self.error or f"diff failed: {type(exc).__name__}"
        wall_s = round(self.options.clock() - self.started, 3)
        result = AgentRunResult(
            run_id=self.spec.run_id,
            arm=self.spec.arm,
            status=self.status,
            claim=self.claim,
            claim_summary=self.claim_summary,
            claims=self.claims,
            sessions=self.sessions,
            phase_shas=phase_shas,
            diff_path=diff_path,
            cost_usd=round(self.scope.spent_usd, 6),
            turns_total=self.turns_total,
            wall_s=wall_s,
            trace_url=trace_url,
            error=self.error,
        )
        self.emit(
            "run_end",
            {
                "status": self.status,
                "claim": self.claim,
                "cost_usd": result.cost_usd,
                "turns_total": self.turns_total,
                "wall_s": wall_s,
            },
        )
        return result


def run_agent(
    spec: AgentRunSpec,
    harness: Harness,
    sandbox: Sandbox,
    bus: EventBus,
    cost: CostTracker,
    tracer: Tracer,
    client: ModelClient,
    options: RunOptions | None = None,
) -> AgentRunResult:
    """Run one arm on one task. Always emits run_start and run_end, even on caps and errors."""
    return _Run(spec, harness, sandbox, bus, cost, tracer, client, options or RunOptions()).run()
