from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from shipharness.events import (
    EVENT_DATA_MODELS,
    Event,
    EventBus,
    RunLogLocked,
    read_events,
    replay,
)

CONTRACT_EVENT_TYPES = {
    "run_start",
    "sandbox_start",
    "sandbox_usage",
    "sandbox_denied",
    "turn",
    "tool_call",
    "tool_result",
    "harness_decision",
    "blocked",
    "session_stop",
    "session_resume",
    "test_proposed",
    "test_filter_result",
    "check_progress",
    "check_result",
    "mutant_result",
    "reviewer_output",
    "gate_result",
    "claim",
    "verdict",
    "cost",
    "screenshot",
    "trace_link",
    "run_end",
}


def tool_call_data(n: int) -> dict[str, object]:
    return {"call_id": f"c{n}", "name": "read_file", "target": f"app/file{n}.py"}


def test_every_contract_event_type_has_a_data_model() -> None:
    assert set(EVENT_DATA_MODELS) == CONTRACT_EVENT_TYPES


def test_seq_starts_at_one_and_increments(tmp_path: Path) -> None:
    with EventBus(tmp_path / "events.jsonl", ab_id="ab-1") as bus:
        first = bus.publish("tool_call", tool_call_data(1), run_id="r-1", arm="bare")
        second = bus.publish("tool_call", tool_call_data(2), run_id="r-1", arm="bare")
    assert (first.seq, second.seq) == (1, 2)


def test_published_event_round_trips_through_the_log(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id="ab-1") as bus:
        sent = bus.publish("tool_call", tool_call_data(1), run_id="r-1", arm="harness")
    [read] = list(read_events(log))
    assert read == sent
    assert read.ab_id == "ab-1"
    assert read.recorded is False


def test_invalid_data_is_rejected_and_nothing_is_written(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id=None) as bus, pytest.raises(ValidationError):
        bus.publish("tool_call", {"call_id": "c1"}, run_id="r-1", arm="bare")
    assert list(read_events(log)) == []


def test_unknown_event_type_is_rejected(tmp_path: Path) -> None:
    with EventBus(tmp_path / "events.jsonl", ab_id=None) as bus, pytest.raises(ValueError):
        bus.publish("not_a_type", {}, run_id=None, arm=None)  # type: ignore[arg-type]


def test_read_events_after_seq(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id=None) as bus:
        for n in range(5):
            bus.publish("tool_call", tool_call_data(n), run_id="r-1", arm="bare")
    assert [e.seq for e in read_events(log, after_seq=3)] == [4, 5]


def test_second_bus_on_same_log_is_rejected(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id=None), pytest.raises(RunLogLocked):
        EventBus(log, ab_id=None)


def test_bus_reopened_after_close_continues_seq(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id=None) as bus:
        bus.publish("tool_call", tool_call_data(1), run_id="r-1", arm="bare")
    with EventBus(log, ab_id=None) as bus:
        again = bus.publish("tool_call", tool_call_data(2), run_id="r-1", arm="bare")
    assert again.seq == 2


def test_listeners_receive_each_event(tmp_path: Path) -> None:
    seen: list[Event] = []
    with EventBus(tmp_path / "events.jsonl", ab_id=None) as bus:
        bus.add_listener(seen.append)
        bus.publish("tool_call", tool_call_data(1), run_id="r-1", arm="bare")
    assert [e.type for e in seen] == ["tool_call"]


def test_replay_marks_events_recorded_and_keeps_content(tmp_path: Path) -> None:
    source = tmp_path / "original.jsonl"
    with EventBus(source, ab_id="ab-1") as bus:
        bus.publish("tool_call", tool_call_data(1), run_id="r-1", arm="bare")
        bus.publish(
            "claim",
            {"phase": "build", "claim": "done", "summary": "ok", "gate_id": None},
            run_id="r-1",
            arm="bare",
        )
    target = tmp_path / "replay.jsonl"
    with EventBus(target, ab_id="ab-1") as bus:
        replay(source, bus)
    original, replayed = list(read_events(source)), list(read_events(target))
    assert [e.type for e in replayed] == [e.type for e in original]
    assert [e.data for e in replayed] == [e.data for e in original]
    assert all(e.recorded for e in replayed)
