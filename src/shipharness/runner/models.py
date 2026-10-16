"""Runner data models."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from shipharness.events import Arm
from shipharness.harness.decisions import LayerName

Phase = Literal["build", "test"]
ToolName = Literal[
    "list_dir", "read_file", "search", "apply_patch", "run", "run_visible_tests", "finish"
]
ClaimValue = Literal["done", "not_done", "none"]
RunStatus = Literal["completed", "ABORTED: cap", "ABORTED: timeout", "ERROR"]


class AgentRunSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    ab_id: str | None = None
    arm: Arm
    feature_id: str
    checkpoint: str
    ticket_text: str
    variant: str = "canonical"
    layers: frozenset[LayerName] = frozenset()
    phases: tuple[Phase, ...] = ("build", "test")
    session_budget: list[int] = [30]
    test_phase_turns: int = 12
    allowed_paths: dict[Phase, list[str]] = {}
    model: str
    reasoning_effort: str
    max_output_tokens: int = 8000
    service_tier: str = "auto"
    cost_limit_usd: float = 0.20
    workspace: Path

    def public_dict(self) -> dict[str, Any]:
        """Spec for events and traces (no host paths)."""
        data = self.model_dump(mode="json", exclude={"workspace"})
        data["layers"] = sorted(self.layers)
        return data


class SessionResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    index: int
    phase: Phase
    turns: int
    ended_by: Literal[
        "claim_done", "claim_not_done", "turn_budget", "cap", "timeout", "error", "no_tool_call"
    ]
    start_sha: str
    end_sha: str
    # Working-tree snapshots (runner/git.py snapshot_tree), committed or not; "" when not taken.
    start_tree: str = ""
    end_tree: str = ""


class AgentRunResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    arm: Arm
    status: RunStatus
    claim: ClaimValue  # from the last finish() call; "none" if never called
    claim_summary: str
    claims: dict[Phase, ClaimValue] = {}  # last claim per phase that started; "none" if no finish
    sessions: list[SessionResult]
    phase_shas: dict[Phase, tuple[str, str]]
    diff_path: Path | None
    cost_usd: float
    turns_total: int
    wall_s: float  # total wall time: agent_wall_s + harness_wall_s
    trace_url: str | None
    error: str | None = None
    agent_wall_s: float = 0.0  # agent working time (model calls, tools); RUN_TIMEOUT_S applies
    harness_wall_s: float = 0.0  # deterministic harness work; HARNESS_TIMEOUT_S applies
    abort_reason: str | None = None  # ABORTED runs: the limit that ended the run


class ToolCall(BaseModel):
    model_config = ConfigDict(frozen=True)

    call_id: str
    name: ToolName
    arguments: dict[str, Any]


class ToolResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    call_id: str
    ok: bool
    output: str  # already truncated
    full_output_path: str | None = None
    exit_code: int | None = None
    duration_ms: int = 0
    files_changed: list[str] = []
