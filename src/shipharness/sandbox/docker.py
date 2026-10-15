"""Docker (or Podman) sandbox: one long-lived container per arm; tool commands via `exec`."""

from __future__ import annotations

import json
import re
import subprocess
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from shipharness.events import Arm, EventBus
from shipharness.sandbox._events import emit_denial
from shipharness.sandbox.base import ExecResult
from shipharness.sandbox.policy import (
    SandboxPolicy,
    check_command,
    detect_denial,
    docker_run_args,
)

Runner = Callable[..., subprocess.CompletedProcess[str]]

_SIZE = re.compile(r"([\d.]+)\s*([KMGT]?i?B)", re.IGNORECASE)
_UNITS_MB = {
    "b": 1 / 1024**2,
    "kib": 1 / 1024,
    "kb": 1 / 1000,
    "mib": 1.0,
    "mb": 1.0,
    "gib": 1024.0,
    "gb": 1000.0,
    "tib": 1024.0**2,
}


def _to_mb(text: str) -> float:
    match = _SIZE.search(text)
    if not match:
        return 0.0
    return float(match.group(1)) * _UNITS_MB.get(match.group(2).lower(), 1.0)


class DockerSandbox:
    def __init__(
        self,
        policy: SandboxPolicy,
        image: str,
        workspace: Path,
        bus: EventBus | None,
        run_id: str,
        arm: Arm,
        *,
        runner: Runner = subprocess.run,
        runtime: str = "docker",
        env: dict[str, str] | None = None,
    ) -> None:
        self.policy = policy
        self.image = image
        self.workspace = Path(workspace)
        self.bus = bus
        self.run_id = run_id
        self.arm = arm
        self.runner = runner
        self.runtime = runtime
        self.env = env
        self.name = f"shipharness-{arm}-{uuid.uuid4().hex[:8]}"
        self.container_id = ""

    def _run(
        self, argv: list[str], timeout: float | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Run the runtime CLI, reading bytes and decoding as UTF-8 with replacement, so binary
        or non-UTF-8 command output can neither crash the run nor be lost."""
        result = self.runner(argv, capture_output=True, timeout=timeout, check=False)
        return subprocess.CompletedProcess(
            result.args, result.returncode, _decode(result.stdout), _decode(result.stderr)
        )

    def start(self) -> str:
        argv = docker_run_args(
            self.policy, self.image, self.workspace, self.name, self.runtime, self.env
        )
        result = self._run(argv, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(f"{self.runtime} run failed: {result.stderr.strip()[:500]}")
        self.container_id = result.stdout.strip()[:64]
        if self.bus is not None:
            self.bus.publish(
                "sandbox_start",
                {
                    "container_id": self.container_id[:12],
                    "image": self.image,
                    "network": self.policy.network,
                    "cpus": self.policy.cpus,
                    "memory_mb": self.policy.memory_mb,
                    "pids_limit": self.policy.pids_limit,
                    "user": self.policy.user,
                    "read_only_root": self.policy.read_only_root,
                    "unsandboxed": False,
                },
                run_id=self.run_id,
                arm=self.arm,
            )
        return self.container_id

    def exec(self, command: str, timeout_s: int) -> ExecResult:
        denial = check_command(self.policy, command)
        if denial is not None:
            emit_denial(self.bus, self.run_id, self.arm, denial, command)
            return ExecResult(
                exit_code=126,
                output=f"DENIED by sandbox: {denial.detail}",
                duration_ms=0,
                denied=denial,
            )
        timeout_s = min(timeout_s, self.policy.tool_timeout_s)
        argv = [
            self.runtime,
            "exec",
            self.name,
            "timeout",
            "--kill-after=5",
            str(timeout_s),
            "bash",
            "-lc",
            command,
        ]
        started = time.monotonic()
        try:
            result = self._run(argv, timeout=timeout_s + 15)
            exit_code, output = result.returncode, (result.stdout or "") + (result.stderr or "")
            timed_out = exit_code == 124
        except subprocess.TimeoutExpired as exc:
            exit_code, timed_out = 124, True
            output = _decode(exc.stdout) + _decode(exc.stderr)
        duration_ms = int((time.monotonic() - started) * 1000)
        oom = exit_code == 137 and not timed_out
        denial = detect_denial(self.policy, output, exit_code, oom, timed_out)
        if denial is not None:
            emit_denial(self.bus, self.run_id, self.arm, denial, command)
        return ExecResult(
            exit_code=exit_code,
            output=output,
            duration_ms=duration_ms,
            timed_out=timed_out,
            denied=denial,
        )

    def usage(self) -> dict[str, float]:
        result = self._run(
            [self.runtime, "stats", "--no-stream", "--format", "{{json .}}", self.name], timeout=30
        )
        stats: dict[str, Any] = json.loads(result.stdout.strip().splitlines()[0])
        used, _, limit = str(stats.get("MemUsage", "0B / 0B")).partition("/")
        return {
            "cpu_pct": float(str(stats.get("CPUPerc", "0")).rstrip("%") or 0),
            "mem_mb": round(_to_mb(used), 3),
            "mem_limit_mb": round(_to_mb(limit), 3),
            "pids": int(stats.get("PIDs", 0) or 0),
        }

    def stop(self) -> None:
        self._run([self.runtime, "rm", "-f", self.name], timeout=60)


def _decode(data: bytes | str | None) -> str:
    if data is None:
        return ""
    return data if isinstance(data, str) else data.decode("utf-8", errors="replace")
