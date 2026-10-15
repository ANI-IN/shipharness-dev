from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from shipharness.console.app import create_console_app, sse_events
from shipharness.events import EventBus


def write_events(log: Path, count: int) -> None:
    with EventBus(log, ab_id="ab-1") as bus:
        for n in range(count):
            bus.publish(
                "tool_call",
                {"call_id": f"c{n}", "name": "read_file", "target": f"f{n}.py"},
                run_id="r-1",
                arm="bare",
            )


@pytest.fixture
def runs_dir(tmp_path: Path) -> Path:
    write_events(tmp_path / "ab-1" / "events.jsonl", 5)
    return tmp_path


def test_replay_after_last_event_id(runs_dir: Path) -> None:
    async def collect() -> list[dict[str, str]]:
        log = runs_dir / "ab-1" / "events.jsonl"
        return [m async for m in sse_events(log, after_seq=2, follow=False)]

    messages = asyncio.run(collect())
    assert [m["id"] for m in messages] == ["3", "4", "5"]
    assert all(m["event"] == "tool_call" for m in messages)


def test_follow_delivers_events_appended_later_exactly_once(runs_dir: Path) -> None:
    log = runs_dir / "ab-1" / "events.jsonl"

    async def scenario() -> list[str]:
        seen: list[str] = []
        stop = False

        async def consume() -> None:
            async for message in sse_events(
                log, after_seq=2, follow=True, poll_s=0.01, should_stop=lambda: stop
            ):
                seen.append(message["id"])

        task = asyncio.create_task(consume())
        await asyncio.sleep(0.1)
        write_events(log, 1)  # becomes seq 6
        await asyncio.sleep(0.1)
        stop = True
        await asyncio.wait_for(task, timeout=2)
        return seen

    assert asyncio.run(scenario()) == ["3", "4", "5", "6"]


def test_http_stream_honours_last_event_id(runs_dir: Path) -> None:
    client = TestClient(create_console_app(runs_dir))
    response = client.get("/events/ab-1?follow=false", headers={"Last-Event-ID": "2"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    body = response.text
    assert "id: 3" in body and "id: 5" in body
    assert "id: 2\r\n" not in body and "id: 2\n" not in body
    assert "event: tool_call" in body


def test_unknown_run_is_404(runs_dir: Path) -> None:
    client = TestClient(create_console_app(runs_dir))
    assert client.get("/events/ab-missing?follow=false").status_code == 404


@pytest.mark.parametrize("bad", ["..", "ab-1..", "a b", "ab%2F..%2Fx"])
def test_run_ids_cannot_escape_the_runs_dir(runs_dir: Path, bad: str) -> None:
    client = TestClient(create_console_app(runs_dir))
    response = client.get(f"/events/{bad}?follow=false")
    streamed = response.headers.get("content-type", "").startswith("text/event-stream")
    assert not (response.status_code == 200 and streamed)


def test_index_page_renders(runs_dir: Path) -> None:
    response = TestClient(create_console_app(runs_dir)).get("/")
    assert response.status_code == 200
    assert "shipharness console" in response.text
    assert "ab-1" in response.text
