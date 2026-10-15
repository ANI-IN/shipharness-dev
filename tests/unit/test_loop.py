from __future__ import annotations

import json
from pathlib import Path

import pytest

from shipharness.config import DEFAULT_PRICES_FILE, Prices
from shipharness.cost import Caps, CostTracker, Usage
from shipharness.events import EventBus, read_events
from shipharness.harness.base import BaseLayer, Harness, LayerContext
from shipharness.harness.decisions import HarnessDecision
from shipharness.runner.loop import RunOptions, run_agent
from shipharness.runner.model import (
    ScriptedModelClient,
    Step,
    classify_openai_error,
    text_step,
    tool_step,
)
from shipharness.runner.models import AgentRunSpec
from shipharness.runner.prompts import NEUTRAL_RESUME, NEUTRAL_WRAPUP, REMINDER
from shipharness.sandbox import FakeSandbox
from shipharness.tracing import NullTracer

from .fakes import fake_openai_key

PRICES = Prices.load(DEFAULT_PRICES_FILE)


def spec(tmp_path: Path, **overrides: object) -> AgentRunSpec:
    ws = tmp_path / "ws"
    ws.mkdir(exist_ok=True)
    (ws / "app.py").write_text("x = 1\n", encoding="utf-8")
    base = dict(
        run_id="r-1",
        arm="bare",
        feature_id="F1",
        checkpoint="m1-s1-start",
        ticket_text="Add a list endpoint.",
        model="gpt-6-luna",
        reasoning_effort="low",
        phases=("build",),
        session_budget=[10],
        cost_limit_usd=0.20,
        workspace=ws,
    )
    base.update(overrides)
    return AgentRunSpec(**base)  # type: ignore[arg-type]


def run(
    tmp_path: Path,
    steps: list[Step],
    *,
    harness: Harness | None = None,
    caps: Caps | None = None,
    options: RunOptions | None = None,
    **spec_overrides: object,
):  # type: ignore[no-untyped-def]
    client = ScriptedModelClient(steps)
    tracker = CostTracker(
        PRICES,
        caps or Caps(run=0.20, review=0.04, session=2.5, batch=2.5, experiment=25.0),
        tmp_path / "ledger.jsonl",
        session_id="test",
    )
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id="ab-1") as bus:
        result = run_agent(
            spec(tmp_path, **spec_overrides),
            harness or Harness([]),
            FakeSandbox(),
            bus,
            tracker,
            NullTracer(),
            client,
            options or RunOptions(wrapup_turns=2, sleep=lambda _s: None),
        )
    return result, list(read_events(log)), client


def types(events) -> list[str]:  # type: ignore[no-untyped-def]
    return [e.type for e in events if e.type != "cost"]


def finish(claim: str = "done", summary: str = "implemented") -> Step:
    return tool_step("finish", claim=claim, summary=summary)


def read_app() -> Step:
    return tool_step("read_file", path="app.py", start_line=None, max_lines=None)


def test_finish_done_completes_the_run(tmp_path: Path) -> None:
    result, events, _ = run(tmp_path, [read_app(), finish()])
    assert result.status == "completed"
    assert result.claim == "done"
    assert result.claim_summary == "implemented"
    assert result.turns_total == 2
    assert types(events) == [
        "run_start",
        "turn",
        "tool_call",
        "tool_result",
        "turn",
        "tool_call",
        "claim",
        "tool_result",
        "run_end",
    ]


def test_text_only_twice_sends_one_reminder_then_claims_none(tmp_path: Path) -> None:
    result, _events, client = run(tmp_path, [text_step("thinking"), text_step("still thinking")])
    assert result.claim == "none"
    reminders = [
        item
        for item in client.inputs[-1]
        if item.get("role") == "user" and REMINDER in str(item.get("content"))
    ]
    assert len(reminders) == 1
    assert result.sessions[-1].ended_by == "no_tool_call"


def test_session_budget_stops_and_resumes_with_fresh_context(tmp_path: Path) -> None:
    steps = [read_app()] * 6
    result, events, client = run(tmp_path, steps, session_budget=[3, 3])
    assert [s.ended_by for s in result.sessions] == ["turn_budget", "turn_budget"]
    assert "session_stop" in types(events) and "session_resume" in types(events)
    first_input, fourth_input = client.inputs[0], client.inputs[3]
    assert fourth_input[0] == first_input[0]  # same stable developer prefix
    assert any(NEUTRAL_RESUME in str(item.get("content")) for item in fourth_input)
    assert not any(item.get("type") == "function_call" for item in fourth_input)


def test_wrapup_message_sent_when_turns_left_equal_wrapup_turns(tmp_path: Path) -> None:
    _result, _events, client = run(tmp_path, [read_app()] * 4, session_budget=[4])
    sent_at = [
        i
        for i, received in enumerate(client.inputs)
        if any(NEUTRAL_WRAPUP in str(item.get("content")) for item in received)
    ]
    assert sent_at[0] == 2  # 4 turns, wrap-up when 2 turns remain


def test_cost_cap_aborts_and_still_ends_the_run(tmp_path: Path) -> None:
    expensive = Usage(input_tokens=1_000, output_tokens=500_000)  # $0.25 per call
    result, events, _ = run(
        tmp_path, [tool_step("list_dir", path=".", depth=None, usage=expensive)]
    )
    assert result.status == "ABORTED: cap"
    assert types(events)[-1] == "run_end"


def test_gate_fail_feedback_is_the_finish_result_and_loop_continues(tmp_path: Path) -> None:
    class Gate(BaseLayer):
        name = "verify"
        calls = 0

        def on_claim_done(self, ctx: LayerContext) -> HarnessDecision | None:
            Gate.calls += 1
            if Gate.calls == 1:
                return HarnessDecision(
                    kind="gate_fail", layer="verify", message="R1: GET /issues leaks"
                )
            return HarnessDecision(kind="gate_pass", layer="verify", message="all checks pass")

    result, _events, client = run(
        tmp_path, [finish(), read_app(), finish()], harness=Harness([Gate()])
    )
    assert result.claim == "done"
    assert result.turns_total == 3
    outputs = [item for item in client.inputs[1] if item.get("type") == "function_call_output"]
    assert "R1: GET /issues leaks" in outputs[-1]["output"]


def test_tool_list_is_identical_every_turn(tmp_path: Path) -> None:
    _result, _events, client = run(tmp_path, [read_app(), read_app(), finish()])
    first = json.dumps(client.tools[0])
    assert all(json.dumps(tools) == first for tools in client.tools)


def test_invalid_json_arguments_become_an_error_result(tmp_path: Path) -> None:
    bad = Step(
        output_items=[
            {
                "type": "function_call",
                "call_id": "c9",
                "name": "read_file",
                "arguments": "{not json",
            }
        ]
    )
    result, _events, client = run(tmp_path, [bad, finish()])
    assert result.status == "completed"
    outputs = [item for item in client.inputs[1] if item.get("type") == "function_call_output"]
    assert "invalid arguments" in outputs[0]["output"]


class FakeAPIError(Exception):
    def __init__(self, status_code: int | None, code: str | None = None) -> None:
        super().__init__(f"status {status_code}")
        self.status_code = status_code
        self.code = code


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        (FakeAPIError(429, "insufficient_quota"), "abort_billing"),
        (FakeAPIError(429, "credit_balance_exhausted"), "abort_billing"),
        (FakeAPIError(429), "retry"),
        (FakeAPIError(401), "abort_auth"),
        (FakeAPIError(403), "abort_auth"),
        (FakeAPIError(500), "retry"),
        (FakeAPIError(400), "abort_other"),
    ],
)
def test_classify_openai_error(exc: Exception, expected: str) -> None:
    assert classify_openai_error(exc) == expected


def test_rate_limit_is_retried_with_backoff(tmp_path: Path) -> None:
    sleeps: list[float] = []
    steps = [Step(error=FakeAPIError(429)), Step(error=FakeAPIError(429)), finish()]
    result, _e, _c = run(tmp_path, steps, options=RunOptions(wrapup_turns=2, sleep=sleeps.append))
    assert result.status == "completed"
    assert sleeps == [1.0, 2.0]


def test_auth_error_ends_with_error_naming_the_variable_not_the_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", fake_openai_key())
    result, events, _ = run(tmp_path, [Step(error=FakeAPIError(401))])
    assert result.status == "ERROR"
    assert result.error is not None and "OPENAI_API_KEY" in result.error
    assert fake_openai_key() not in result.error
    assert types(events)[-1] == "run_end"
