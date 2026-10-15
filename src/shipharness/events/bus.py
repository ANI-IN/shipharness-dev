"""EventBus: validates events and appends them to a JSONL run log (CONTRACTS §8.1)."""

from __future__ import annotations

import json
import os
import threading
import time
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from shipharness.events.models import EVENT_DATA_MODELS, Arm, Event, EventType
from shipharness.logging import redact


class RunLogLocked(RuntimeError):
    """Raised when another EventBus already writes to the same run log."""


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class EventBus:
    """One writer per run log. Use as a context manager so the lock is released."""

    def __init__(self, log_path: Path, ab_id: str | None) -> None:
        self.log_path = Path(log_path)
        self.ab_id = ab_id
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_path = self.log_path.with_name(self.log_path.name + ".lock")
        try:
            fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise RunLogLocked(f"run log already open: {self.log_path}") from None
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        self._mutex = threading.Lock()
        self._listeners: list[Callable[[Event], None]] = []
        self._seq = max((event.seq for event in read_events(self.log_path)), default=0)
        self._closed = False

    def __enter__(self) -> EventBus:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._lock_path.unlink(missing_ok=True)

    def add_listener(self, listener: Callable[[Event], None]) -> None:
        self._listeners.append(listener)

    # [walkthrough:Opening:publish] start
    def publish(
        self,
        type: EventType,
        data: BaseModel | dict[str, Any],
        *,
        run_id: str | None,
        arm: Arm | None,
        recorded: bool = False,
    ) -> Event:
        """Validate `data`, append one JSON line, notify listeners. Every stage of a run goes
        through here; the console streams the same file over SSE."""
        model = EVENT_DATA_MODELS.get(type)
        if model is None:
            raise ValueError(f"unknown event type: {type!r}")
        raw = data.model_dump() if isinstance(data, BaseModel) else data
        raw = redact(raw)  # no key-shaped string or credential field ever reaches a run log
        payload = model.model_validate(raw).model_dump(mode="json")
        with self._mutex:
            if self._closed:
                raise RuntimeError("EventBus is closed")
            self._seq += 1
            event = Event(
                ab_id=self.ab_id,
                run_id=run_id,
                arm=arm,
                seq=self._seq,
                ts=_now(),
                type=type,
                data=payload,
                recorded=recorded,
            )
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(event.model_dump_json() + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        for listener in self._listeners:
            listener(event)
        return event

    # [walkthrough:Opening:publish] end


def read_events(log_path: Path, after_seq: int = 0) -> Iterator[Event]:
    """Yield complete events from a run log with seq > after_seq."""
    path = Path(log_path)
    if not path.exists():
        return
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.endswith("\n"):
                break  # partial line still being written
            if not line.strip():
                continue
            event = Event.model_validate(json.loads(line))
            if event.seq > after_seq:
                yield event


def follow_events(
    log_path: Path,
    after_seq: int = 0,
    poll_s: float = 0.2,
    stop: Callable[[], bool] | None = None,
) -> Iterator[Event]:
    """Tail a run log, yielding each new event once, until `stop()` returns True."""
    last = after_seq
    while True:
        for event in read_events(log_path, after_seq=last):
            last = event.seq
            yield event
        if stop is not None and stop():
            return
        time.sleep(poll_s)
