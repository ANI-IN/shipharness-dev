"""Integration tests against a real container runtime. Run with: pytest -m docker.

Needs the agent image: docker build -f sandbox/Dockerfile --target agent -t shipharness-agent:1 .
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from shipharness.config import Settings
from shipharness.events import EventBus, read_events
from shipharness.sandbox import DockerSandbox, default_policy

pytestmark = [
    pytest.mark.docker,
    pytest.mark.skipif(shutil.which("docker") is None, reason="docker not installed"),
]


@pytest.fixture
def sandbox(tmp_path: Path):  # type: ignore[no-untyped-def]
    settings = Settings(_env_file=None)
    log = tmp_path / "events.jsonl"
    workspace = tmp_path / "ws"
    workspace.mkdir()
    workspace.chmod(0o777)
    with EventBus(log, ab_id=None) as bus:
        box = DockerSandbox(
            default_policy(settings), settings.sandbox_image_agent, workspace, bus, "r-1", "bare"
        )
        box.start()
        try:
            yield box, log, workspace
        finally:
            box.stop()


def test_workspace_is_writable(sandbox) -> None:  # type: ignore[no-untyped-def]
    box, _log, workspace = sandbox
    assert box.exec("echo hi > out.txt && cat out.txt", timeout_s=30).exit_code == 0
    assert (workspace / "out.txt").read_text().strip() == "hi"


def test_network_is_off_and_denial_is_reported(sandbox) -> None:  # type: ignore[no-untyped-def]
    box, log, _ = sandbox
    cmd = "python -c \"import socket; socket.create_connection(('example.com', 80), timeout=3)\""
    result = box.exec(cmd, timeout_s=30)
    assert result.exit_code != 0
    assert result.denied is not None and result.denied.reason_code == "network"
    assert any(e.type == "sandbox_denied" for e in read_events(log))


def test_root_filesystem_is_read_only(sandbox) -> None:  # type: ignore[no-untyped-def]
    box, _log, _ = sandbox
    result = box.exec("touch /etc/shipharness-test", timeout_s=30)
    assert result.denied is not None
    assert result.denied.reason_code == "write_outside_workspace"


def test_runs_as_non_root(sandbox) -> None:  # type: ignore[no-untyped-def]
    box, _log, _ = sandbox
    assert box.exec("id -u", timeout_s=30).output.strip() == "1000"


def test_timeout_is_enforced(sandbox) -> None:  # type: ignore[no-untyped-def]
    box, _log, _ = sandbox
    result = box.exec("sleep 30", timeout_s=2)
    assert result.timed_out is True
