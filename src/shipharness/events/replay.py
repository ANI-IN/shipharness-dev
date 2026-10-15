"""Replay a recorded run log: every re-emitted event carries recorded=True (RECORDING badge)."""

from __future__ import annotations

from pathlib import Path

from shipharness.events.bus import EventBus, read_events


def replay(log_path: Path, bus: EventBus) -> int:
    """Re-emit all events from `log_path` onto `bus`. Returns the number of events replayed."""
    count = 0
    for event in read_events(log_path):
        bus.publish(event.type, event.data, run_id=event.run_id, arm=event.arm, recorded=True)
        count += 1
    return count
