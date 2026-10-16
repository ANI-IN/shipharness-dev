# CONTRACTS

Interfaces between shipharness components. Builders in M4 code against these; a change to any contract
needs a CONTRACTS.md edit in the same commit and a note in CHANGELOG.md. Design rationale is in
[DESIGN.md](DESIGN.md).

Contract version: `1.3` (2026-10-16, M4: §21 records the interfaces added by the seven M4 builders;
where §21 and an earlier section differ, §21 wins). Version 1.2 (M3): ledger file name, runner fields, sandbox and tracer
signatures as built; see CHANGELOG). Version 1.1: approved at the M2 checkpoint with changes: `finish` tool;
`feature_list.json` read-only to the agent; Flex tier rule; secrets rules in §20).

---

## 0. Conventions

- Python 3.12, type hints throughout. Data models are pydantic v2 `BaseModel` with
  `model_config = ConfigDict(extra="forbid", frozen=True)` unless noted.
- Timestamps: ISO 8601 UTC strings with milliseconds (`2026-10-16T14:03:22.481Z`).
- IDs:
  - `run_id`: `r-<YYYYMMDD>-<HHMMSS>-<6 hex>`; one per arm per task execution.
  - `ab_id`: `ab-<YYYYMMDD>-<HHMMSS>-<6 hex>`; groups the two arms of one A/B.
  - `session_index`: 1-based integer within a run.
- `Arm = Literal["bare", "harness"]`.
- `LayerName = Literal["instructions", "state", "scope", "verify"]`.
- `Phase = Literal["build", "test"]`.
- Paths inside a workspace are POSIX, relative to the workspace root, never absolute, never containing `..`.
- Money is `float` USD rounded to 6 decimals at storage time.

---

## 1. Configuration keys

Loaded by `shipharness.config.Settings` (pydantic-settings) from environment and `.env`. Names match the
brief; no prefix.

| Key | Type | Default | Purpose |
|---|---|---|---|
| `OPENAI_API_KEY` | secret str | required | OpenAI |
| `OPENAI_MODEL` | str | `gpt-6-luna` | Builder and test writer (both arms) |
| `OPENAI_REASONING_EFFORT` | str | `medium` (provisional; M6 pilot sets the final value) | Builder and test writer |
| `OPENAI_EVAL_MODEL` | str | `gpt-5.6-luna` | Reviewer |
| `OPENAI_EVAL_REASONING_EFFORT` | str | `medium` | Reviewer |
| `OPENAI_SERVICE_TIER` | str | `auto` | `flex` for experiment batches only, and only if the M6 pilot confirms multi-turn tool calling on Flex; class runs always `auto`; both arms of a batch use the same tier |
| `LANGSMITH_API_KEY` | secret str | required | LangSmith |
| `LANGSMITH_ENDPOINT` | str | `https://api.smith.langchain.com` | EU users override |
| `LANGSMITH_TRACING` | bool | `true` | |
| `SHIPHARNESS_CLASS_DATE` | str | today | Class project name suffix |
| `MAX_RUN_COST_USD` | float | 0.20 | Per arm per run |
| `MAX_FINAL_RUN_COST_USD` | float | 0.25 | Per arm in `make final` |
| `MAX_REVIEW_COST_USD` | float | 0.04 | Per review |
| `MAX_SESSION_COST_USD` | float | 2.50 | Per class session (persisted) |
| `MAX_BATCH_COST_USD` | float | 2.50 | Per command |
| `MAX_EXPERIMENT_TOTAL_USD` | float | 25.00 | All experiment batches (persisted) |
| `MAX_TURNS_PER_SESSION` | int | 30 | Default; dataset `session_budget` overrides |
| `MAX_OUTPUT_TOKENS` | int | 8000 | Per model call |
| `WRAPUP_TURNS` | int | 3 | Turns granted to both arms at a session stop |
| `TOOL_TIMEOUT_S` | int | 120 | Per tool command |
| `RUN_TIMEOUT_S` | int | 300 | Per arm per run, wall clock (demo limit is 6 minutes including the referee; M6 tunes) |
| `MAX_CONCURRENCY` | int | 4 | Concurrent agent loops across arms |
| `SANDBOX_MODE` | `docker` \| `none` | `docker` | `none` = UNSANDBOXED fallback |
| `SANDBOX_RUNTIME` | str | `docker` | `docker` or `podman` |
| `SANDBOX_IMAGE_AGENT` | str | `shipharness-agent:1` | |
| `SANDBOX_IMAGE_REFEREE` | str | `shipharness-referee:1` | |
| `RUNS_DIR` | path | `.shipharness/runs` | Run logs, workspaces |
| `EXPORTS_DIR` | path | `exports` | LangSmith exports, score records |

`.env.example` lists every key; the two API keys are marked required.

---

## 2. Prices

`config/prices.toml`:

```toml
# USD per 1M tokens. verified = access date of the source page.
[models."gpt-6-luna"]
input = 0.10
cached_input = 0.01
cache_write = 0.125
output = 0.50
source = "https://developers.openai.com/api/docs/models/gpt-6-luna"
verified = "2026-10-16"

[models."gpt-5.6-luna"]
input = 0.20
cached_input = 0.02
cache_write = 0.25
output = 1.20
source = "https://developers.openai.com/api/docs/models/gpt-5.6-luna"
verified = "2026-10-16"
```

A model missing from the file is a startup error (no silent zero cost).

---

## 3. CostTracker

```python
class CapExceeded(Exception):
    scope: Literal["run", "review", "session", "batch", "experiment"]
    limit_usd: float
    spent_usd: float

class Usage(BaseModel):
    input_tokens: int
    cached_tokens: int          # usage.input_tokens_details.cached_tokens
    cache_write_tokens: int     # usage.input_tokens_details.cache_write_tokens (0 if absent)
    output_tokens: int          # includes reasoning
    reasoning_tokens: int       # usage.output_tokens_details.reasoning_tokens

class CostTracker:
    def __init__(self, prices: Prices, caps: Caps, ledger_path: Path) -> None: ...
    def scope(self, kind: Literal["run", "review"], key: str, limit_usd: float) -> "CostScope": ...
    def record(self, scope: "CostScope", model: str, usage: Usage) -> float: ...   # returns call cost; raises CapExceeded
    def check_before_call(self, scope: "CostScope", model: str, est_input_tokens: int, max_output_tokens: int) -> None: ...
    def summary(self) -> "CostSummary": ...
```

- Formula: `uncached = input - cached - cache_write`;
  `cost = (uncached*input + cached*cached_input + cache_write*cache_write_price + output*output_price) / 1e6`.
- `check_before_call` raises if the worst case of the next call (all input uncached, full
  `max_output_tokens`) would cross any active cap. The runner catches `CapExceeded`, ends the arm with
  `ABORTED: cap`, and the referee still runs.
- Session and experiment totals persist in `.shipharness/ledger.jsonl` (append-only JSON Lines; entries carry `session`, `experiment`,
  `run_id`, model, usage, cost).
- Every CLI command prints `CostSummary` (per arm, per model, total, caps remaining).

---

## 4. Runner

```python
class AgentRunSpec(BaseModel):
    run_id: str
    ab_id: str | None
    arm: Arm
    feature_id: str                  # "F1".."F7", "CTRL-n", or "TG-<target>"
    checkpoint: str                  # git tag, e.g. "m1-s1-start"
    ticket_text: str
    variant: str                     # "canonical", "terse", "pm", "bug", "alt-checkpoint-a", "stop-2", "trap-legacy", ...
    layers: frozenset[LayerName]     # empty for bare
    phases: tuple[Phase, ...]        # ("build", "test") for run; ("test",) for testgen
    session_budget: list[int]        # turns per session, e.g. [14, 14]; len = number of sessions
    allowed_paths: dict[Phase, list[str]]   # glob patterns; used only by the scope layer
    model: str
    reasoning_effort: str
    max_output_tokens: int
    cost_limit_usd: float
    test_phase_turns: int = 12       # test-phase turn budget (M6 may lower it to fit the run cap)
    service_tier: str = "auto"
    workspace: Path                  # host path of the arm's fresh repo

class SessionResult(BaseModel):
    index: int
    turns: int
    phase: Phase
    ended_by: Literal["claim_done", "claim_not_done", "turn_budget", "cap", "timeout", "error", "no_tool_call"]
    start_sha: str
    end_sha: str

class AgentRunResult(BaseModel):
    run_id: str
    arm: Arm
    status: Literal["completed", "ABORTED: cap", "ABORTED: timeout", "ERROR"]
    claim: Literal["done", "not_done", "none"]       # from the last finish() call; "none" if never called
    claim_summary: str                                # finish(summary=...), "" if never called
    sessions: list[SessionResult]
    phase_shas: dict[Phase, tuple[str, str]]         # (start, end) commit per phase
    diff_path: Path                                   # unified diff vs checkpoint export
    cost_usd: float
    turns_total: int
    wall_s: float
    trace_url: str | None
    error: str | None = None          # ERROR status: message names the variable, never a key

def run_agent(spec: AgentRunSpec, harness: "Harness", sandbox: "Sandbox",
              bus: "EventBus", cost: CostTracker, tracer: "Tracer") -> AgentRunResult: ...
```

Loop rules:
- Responses API, stateless replay (`store=False`); the full `response.output` (reasoning and function-call
  items) is appended each turn; `parallel_tool_calls=False`.
- Input order (stable prefix first, for caching): developer message (core system prompt) → harness prefix
  blocks from `Harness.context_prefix()` → ticket → history. Tool list order and text are byte-identical
  across turns, arms, and runs.
- A turn = one model call plus its tool executions. `turn_budget` per session from `session_budget`.
- The agent ends a phase only by calling `finish(claim, summary)` (§6). There is no text-based claim
  detection. `finish(claim="done")` triggers `Harness.on_claim_done`; with the verify layer on, a failing
  gate returns its feedback as the `finish` tool result and the phase continues within its turn budget.
  `finish(claim="not_done")` ends the phase without a gate. If the model replies with text and no tool
  call, the runner sends one fixed reminder ("Call a tool, or call finish to end this phase."), identical
  for both arms and counted as a turn; a second text-only reply ends the phase with `claim="none"`.
- Each `finish` call emits a `claim` event.
- Wrap-up: when a session's remaining turns reach `WRAPUP_TURNS`, both arms receive a wrap-up message
  (text from the harness when the state layer is on, neutral otherwise).

---

## 5. Harness and layer interface

```python
class HarnessDecision(BaseModel):
    kind: Literal["allow", "block", "revert", "gate_fail", "gate_pass", "status_set", "session_stop", "session_resume", "note"]
    layer: LayerName
    message: str                     # shown to the agent when relevant, and in the console
    paths: list[str] = []
    data: dict[str, Any] = {}

class LayerContext(BaseModel):     # mutable view passed to hooks (not frozen)
    spec: AgentRunSpec
    phase: Phase
    session_index: int
    turn: int
    workspace: Path
    sandbox: "Sandbox"
    bus: "EventBus"

class Layer(Protocol):
    name: LayerName
    def prepare_workspace(self, ctx: LayerContext) -> list[HarnessDecision]: ...      # before session 1
    def context_prefix(self, ctx: LayerContext) -> list[str]: ...                     # stable text blocks
    def before_tool(self, ctx: LayerContext, call: "ToolCall") -> HarnessDecision: ... # allow | block
    def after_tool(self, ctx: LayerContext, call: "ToolCall", result: "ToolResult") -> list[HarnessDecision]: ...
    def on_wrapup(self, ctx: LayerContext) -> str | None: ...                         # wrap-up message text
    def on_session_end(self, ctx: LayerContext, result: SessionResult) -> list[HarnessDecision]: ...
    def on_session_start(self, ctx: LayerContext) -> list[str]: ...                   # extra resume text
    def on_claim_done(self, ctx: LayerContext) -> HarnessDecision | None: ...         # on finish(claim="done"); None = no opinion
    def on_phase_end(self, ctx: LayerContext) -> list[HarnessDecision]: ...           # e.g. test filters

class Harness:
    def __init__(self, layers: Sequence[Layer]) -> None: ...   # fixed order: instructions, state, scope, verify
    @classmethod
    def from_names(cls, names: frozenset[LayerName]) -> "Harness": ...
```

- Bare arm = `Harness([])`: every hook is a no-op, except that the runner always applies the neutral
  wrap-up and resume text.
- Hooks run in layer order; the first `block` in `before_tool` wins. `on_claim_done` returns
  `gate_fail` (agent continues) or `gate_pass`.
- Every returned decision is emitted as a `harness_decision` event (`blocked` additionally for
  `block`/`revert`).
- Layers must not call the model. Layers must not read hidden tests, referee mutants, or reference
  implementations (enforced by a unit test that scans `harness/` imports and path literals).

---

## 6. Tools

Seven function tools, identical for both arms: six working tools plus `finish`. All use `strict: true`,
`additionalProperties: false`, all properties required (optional = `["type", "null"]`). Tool results are strings; every result is truncated to `TOOL_OUTPUT_MAX_CHARS` (8,000)
with a trailer `[truncated: N more chars; the full output is kept in the run log outside the workspace, where you cannot read it; narrow the command instead, for example pipe it through grep or tail]` (A4
"Context window pollution", F-a-131).

| Tool | Parameters | Result |
|---|---|---|
| `list_dir` | `path: str`, `depth: int \| null` (default 1, max 3) | Tree listing, directories with trailing `/` |
| `read_file` | `path: str`, `start_line: int \| null`, `max_lines: int \| null` (default 400) | Numbered lines; `[lines a-b of N]` header |
| `search` | `pattern: str` (regex), `path: str \| null`, `max_results: int \| null` (default 50) | `path:line: text` rows |
| `apply_patch` | `patch: str` (unified diff, one or more files; new files via `/dev/null`) | `applied: <files>` or a precise rejection reason (hunk mismatch, path outside workspace, path blocked by scope) |
| `run` | `command: str`, `timeout_s: int \| null` (≤ `TOOL_TIMEOUT_S`) | `exit=<code>` header + combined stdout/stderr; executed in the arm container under `/work` |
| `run_visible_tests` | `selector: str \| null` (pytest node selector within `tests/visible`) | Summary first (`passed=x failed=y errors=z`), then one `FAILED <node>: <reason>` line per failure, grep-friendly (A4, F-a-132) |
| `finish` | `claim: "done" \| "not_done"` (enum), `summary: str` (≤ 2,000 chars) | `accepted` (phase ends), or gate feedback when the verify layer is on and the gate fails (phase continues) |

`finish` schema:

```json
{
  "type": "function",
  "name": "finish",
  "description": "End the current phase. Use claim=done only when the ticket's work for this phase is complete; use not_done to stop without completing it.",
  "parameters": {
    "type": "object",
    "properties": {
      "claim": {"type": "string", "enum": ["done", "not_done"]},
      "summary": {"type": "string", "description": "What was done and how it was checked."}
    },
    "required": ["claim", "summary"],
    "additionalProperties": false
  },
  "strict": true
}
```

```python
class ToolCall(BaseModel):
    call_id: str
    name: Literal["list_dir", "read_file", "search", "apply_patch", "run", "run_visible_tests", "finish"]
    arguments: dict[str, Any]

class ToolResult(BaseModel):
    call_id: str
    ok: bool
    output: str                      # already truncated
    full_output_path: str | None
    exit_code: int | None
    duration_ms: int
    files_changed: list[str]         # computed by git status diff before/after
```

`finish` runs on the host (runner and harness only). `list_dir`, `read_file`, `search` run on the host
against the workspace (read-only, path-checked);
`apply_patch` is validated on the host and applied with `git apply` in the container; `run` and
`run_visible_tests` execute in the container.

---

## 7. Skills loader

```python
class SkillMeta(BaseModel):
    name: str
    description: str
    path: str                        # workspace-relative folder

class SkillsLoader:
    def __init__(self, root: Path) -> None: ...                 # scans <root>/*/SKILL.md
    def catalogue(self) -> list[SkillMeta]: ...                 # tier 1: name + description only
    def catalogue_block(self) -> str: ...                       # stable text for the context prefix
```

Tier 2 and tier 3 (full SKILL.md, referenced files) are loaded by the agent through `read_file`; the
loader emits a `harness_decision` (`kind="note"`, `data={"skill": name, "tier": 2|3}`) when a read hits
a skill path, which drives the S1 files-read map.

`shipharness skills validate <dir>`: errors = skills-ref checks (frontmatter present and parseable; only
`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`; `name` 1-64 chars of
ASCII `a-z0-9-`, no leading/trailing/double hyphen, equals folder name; `description` 1-1024 chars;
`compatibility` ≤ 500 chars; `metadata` string → string). Warnings = SKILL.md over 500 lines; file
references deeper than one level; referenced files missing. Exit 0 if no errors, 1 otherwise.

---

## 8. Events

### 8.1 Envelope

```python
class Event(BaseModel):
    v: Literal[1] = 1
    ab_id: str | None
    run_id: str | None               # None for A/B-level events
    arm: Arm | None
    seq: int                         # monotonically increasing per run log
    ts: str
    type: EventType
    data: dict[str, Any]             # validated against the per-type model below
    recorded: bool = False           # True when emitted by replay
```

Run logs: `RUNS_DIR/<ab_id or run_id>/events.jsonl`, one event per line, flushed per event. The console
tails these files and streams them over SSE (`GET /events/{ab_id}` with `Last-Event-ID` = `seq`).

```python
class EventBus:
    def __init__(self, log_path: Path) -> None: ...
    def publish(self, type: EventType, data: BaseModel, *, run_id: str | None, arm: Arm | None) -> Event: ...
    def subscribe(self) -> Iterator[Event]: ...                 # in-process listeners (tests, CLI printer)
```

### 8.2 Event types and data

| Type | Data fields |
|---|---|
| `run_start` | `spec` (AgentRunSpec minus workspace), `policy_summary` |
| `sandbox_start` | `container_id`, `image`, `network` (`"none"`), `cpus`, `memory_mb`, `pids_limit`, `user`, `read_only_root`, `unsandboxed: bool` |
| `sandbox_usage` | `cpu_pct`, `mem_mb`, `mem_limit_mb`, `pids`, `time_left_s` |
| `sandbox_denied` | `command`, `reason_code` (`network`, `write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`), `detail` |
| `turn` | `session_index`, `turn`, `turns_left`, `input_tokens`, `cached_tokens`, `cache_write_tokens`, `output_tokens`, `reasoning_tokens`, `message_excerpt` |
| `tool_call` | `call_id`, `name`, `target` (path, pattern, or command, ≤ 200 chars) |
| `tool_result` | `call_id`, `ok`, `exit_code`, `duration_ms`, `files_changed`, `output_excerpt` (≤ 500 chars) |
| `harness_decision` | HarnessDecision fields |
| `blocked` | `phase`, `paths`, `action` (`reject_patch` \| `revert`), `reason` |
| `session_stop` | `session_index`, `ended_by`, `end_sha`, `handoff_path` \| null |
| `session_resume` | `session_index`, `start_sha`, `prefix_blocks` (names only) |
| `test_proposed` | `test_id` (`<file>::<name>`), `phase` |
| `test_filter_result` | `test_id`, `filter` (1-5), `passed`, `reason` |
| `check_progress` | `check` (e.g. `R1`), `done`, `total`, `label` (e.g. `"R1 probes 37/112"`) |
| `check_result` | CheckResult summary (§10) |
| `mutant_result` | `mutant_id`, `set` (`filter` \| `referee`), `outcome` (`killed` \| `survived` \| `timeout` \| `error`), `killed_by` |
| `reviewer_output` | Review (§12) |
| `gate_result` | GateResult (§13) |
| `claim` | `phase`, `claim` (`done` \| `not_done` \| `none`), `summary`, `gate_id` \| null |
| `verdict` | `primary` (measure name → value), `passed_primary: bool`, `summary` |
| `cost` | `scope`, `model`, `call_usd`, `run_usd`, `session_usd`, `limit_usd` |
| `screenshot` | `path` (relative to run dir), `view` (`board` \| `issue` \| `conflict`), `as_user`, `overlays` (list of `{issue_id, mark}`) |
| `trace_link` | `url`, `kind` (`agent` \| `referee` \| `experiment` \| `comparison`) |
| `run_end` | AgentRunResult summary (`status`, `claim`, `cost_usd`, `turns_total`, `wall_s`) |

---

## 9. Sandbox

### 9.1 Policy schema (`sandbox/policy.py`)

```python
class SandboxPolicy(BaseModel):
    version: int = 1
    network: Literal["none"] = "none"
    cpus: float = 1.0
    memory_mb: int = 1024
    swap_mb: int = 0                       # --memory-swap == --memory
    pids_limit: int = 256
    user: str = "1000:1000"
    read_only_root: bool = True
    tmpfs: dict[str, str] = {"/tmp": "rw,nosuid,size=256m"}
    cap_drop: list[str] = ["ALL"]
    no_new_privileges: bool = True
    workspace_mount: str = "/work"
    tool_timeout_s: int
    run_timeout_s: int
    deny_command_patterns: list[DenyRule]  # pre-exec refusals
    detect_output_patterns: list[DetectRule]  # post-exec denials

class DenyRule(BaseModel):
    pattern: str                           # regex on the command
    reason_code: str
    message: str                           # shown to the agent

class DetectRule(BaseModel):
    pattern: str                           # regex on combined output
    reason_code: str

def default_policy(settings: Settings) -> SandboxPolicy: ...
def docker_run_args(policy: SandboxPolicy, image: str, workspace: Path, name: str,
                    runtime: str = "docker", env: dict[str, str] | None = None) -> list[str]: ...  # full argv; env names with KEY/TOKEN/SECRET are refused
def render_policy(policy: SandboxPolicy) -> str: ...            # printed at run start
```

### 9.2 Sandbox API

```python
class ExecResult(BaseModel):
    exit_code: int
    output: str                            # combined, untruncated (runner truncates)
    duration_ms: int
    timed_out: bool
    denied: SandboxDenial | None

class Sandbox(Protocol):
    def start(self) -> str: ...                                   # container id; emits sandbox_start
    def exec(self, command: str, timeout_s: int) -> ExecResult: ...  # emits sandbox_denied if any
    def usage(self) -> dict[str, float]: ...
    def stop(self) -> None: ...

class DockerSandbox(Sandbox): ...          # also used with SANDBOX_RUNTIME=podman
class LocalSandbox(Sandbox): ...           # SANDBOX_MODE=none; marks every event unsandboxed
class FakeSandbox(Sandbox): ...            # unit tests; scripted results
```

---

## 10. Checks (referee and gate)

```python
class Finding(BaseModel):
    rule: str                              # "R1".."R8", "regression", "hidden", "scope", "flaky", "board"
    severity: Literal["violation", "leak", "error", "info"]
    endpoint: str | None                   # "GET /issues/{id}"
    detail: str
    baseline: bool                         # True if present at the checkpoint baseline

class CheckResult(BaseModel):
    check: str
    passed: bool                           # no new violations
    new_violations: int
    baseline_violations: int
    total_probes: int
    findings: list[Finding]                # capped at 200, sorted new-first
    duration_ms: int
    seed: int | None
    artifacts: list[str]                   # files written under the build dir's .referee/

class CheckContext(BaseModel):
    checkpoint: str
    feature_id: str
    phase_allowed_paths: dict[Phase, list[str]]
    exemptions: dict[str, list[str]]       # per rule, e.g. {"R4": ["POST /projects/{id}/issues"]}
    seed: int
    progress: Callable[[int, int, str], None]   # emits check_progress

class Check(Protocol):
    name: str
    def run(self, build_dir: Path, ctx: CheckContext) -> CheckResult: ...
```

Registered checks: `r1_tenant`, `r2_roles`, `r3_conventions`, `r4_idempotency`, `r5_audit`,
`r6_layering`, `r7_migrations`, `regression`, `hidden_tests`, `diff_scope`, `flakiness`, `board`
(Playwright), `continuity` (reads the run log; S2 measures). `build_dir` is a directory inside the
referee container's mount containing the checkpoint export with the arm's diff applied. Checks never
call the model.

---

## 11. Results

```python
class ScoreRecord(BaseModel):            # one per arm per run; also the LangSmith evaluator output
    run_id: str
    ab_id: str | None
    arm: Arm
    feature_id: str
    variant: str
    checkpoint: str
    layers: list[LayerName]
    status: str                            # from AgentRunResult
    claim: str
    r1_new_violations: int
    r1_leaks: int
    r2_new_violations: int
    r3_new_failures: int
    r4_duplicates: int
    r5_audit_missing: int
    r6_ok: bool
    r7_ok: bool
    regression_passed: int
    regression_total: int
    hidden_passed: int
    hidden_total: int
    mutants_killed: int                    # referee set only
    mutants_total: int
    shipped_tests: int
    flaky_tests: int
    out_of_scope_files: int
    test_phase_source_edits: int
    continuity_failure: bool | None        # S2 tasks only
    redone_lines_pct: float | None
    board_ok: bool
    reviewer_verdict: Literal["accept", "reject"] | None
    reviewer_agrees: bool | None           # reviewer verdict == referee verdict
    primary: dict[str, float | int | bool]
    passed_primary: bool
    cost_usd: float
    review_cost_usd: float
    turns_total: int
    wall_s: float
    trace_url: str | None
    referee_trace_url: str | None
    sandboxed: bool
    recorded: bool                         # True for replays
    captured_at: str
```

LangSmith evaluator mapping: `referee_evaluator(run, example) -> list[dict]` returns
`{"key": <field>, "score": <number or bool>}` for: `r1_new_violations`, `r2_new_violations`,
`r3_new_failures`, `r4_duplicates`, `r5_audit_missing`, `r7_ok`, `regression_pass_rate`,
`hidden_passed`, `mutants_killed`, `out_of_scope_files`, `flaky_tests`, `passed_primary` (12 scores),
and writes the full ScoreRecord to `EXPORTS_DIR/scores/<run_id>.json` before returning.

Exports layout:
```
exports/
  scores/<run_id>.json                    # ScoreRecord
  experiments/<experiment_name>.json      # {name, url, comparison_url, dataset, split, arm, k, metadata, rows:[ScoreRecord ids], stats}
  traces/<run_id>.json                    # {trace_url, root_run_id, child_counts, cost, tokens}
  batches/<batch_id>.json                 # {batch, runs, cost_usd, traces_used, started, finished}
```

---

## 12. Reviewer

```python
class ReviewInput(BaseModel):
    task: str                              # ticket text
    diff: str                              # blinded unified diff
    grading_criteria: str                  # assembled from SECURITY.md + ARCHITECTURE.md sections (stable text)

class ReviewFinding(BaseModel):
    file: str
    line: int | None
    severity: Literal["blocker", "major", "minor"]
    criterion: str                         # which grading criterion
    comment: str

class Review(BaseModel):                 # structured output schema (strict); findings before verdict
    findings: list[ReviewFinding]
    tenant_isolation_risk: Literal["none", "possible", "likely"]
    verdict: Literal["accept", "reject"]
    summary: str

def blind(diff: str) -> str: ...           # reviewer/blind.py
def review(inp: ReviewInput, cost: CostTracker, tracer: "Tracer") -> Review: ...
```

`blind` removes hunks and file headers for harness artifacts (`AGENTS.md`, `progress.md`,
`session-handoff.md`, `feature_list.json`, `init.sh`, `.agents/**`, `docs/exec-plans/**`), strips commit
metadata, and normalises paths, so the two arms' diffs differ only in code and tests. The arm label is
never part of the input. Model: `OPENAI_EVAL_MODEL`, `store=False`, `max_output_tokens` sized so the
worst case stays within `MAX_REVIEW_COST_USD`; an incomplete or refused response yields `verdict=None`
in the ScoreRecord.

---

## 13. Gate

```python
class GateItem(BaseModel):
    name: str                              # "visible tests", "existing tests", "R1".."R7", "board", "clean state"
    status: Literal["pending", "pass", "fail", "skipped"]
    detail: str

class GateResult(BaseModel):
    gate_id: str
    items: list[GateItem]
    passed: bool
    feedback: str                          # text sent to the agent on failure (first 3 failures, grep-friendly)
```

The gate runs in the arm's own container on the arm's workspace. It never runs `hidden_tests` or
referee-set mutants.

---

## 14. Filters and mutants

```python
class CandidateTest(BaseModel):
    test_id: str                           # "<file>::<name>"
    file: str
    source: str

class FilterContext(BaseModel):
    workspace: Path
    sandbox: Sandbox
    baseline_coverage: "CoverageMap"
    filter_mutants: list["Mutant"]         # filter set only
    source_shas_at_phase_start: dict[str, str]

class FilterResult(BaseModel):
    test_id: str
    filter: int                            # 1..5
    passed: bool
    reason: str

class Filter(Protocol):
    number: int
    name: str
    def evaluate(self, cand: CandidateTest, ctx: FilterContext) -> FilterResult: ...

def run_pipeline(cands: list[CandidateTest], ctx: FilterContext, bus: EventBus) -> list[FilterResult]: ...
# stops at the first failing filter per test; emits test_proposed / test_filter_result

class Mutant(BaseModel):
    id: str                                # "<target>-m<n>"
    target: str                            # module path
    set: Literal["filter", "referee"]
    file: str
    line: int
    original: str                          # exact text on that line
    replacement: str
    rationale: str                         # risky behaviour it simulates

def run_mutant(m: Mutant, tests: list[str], workdir: Path, sandbox: Sandbox, timeout_s: int) -> Literal["killed", "survived", "timeout", "error"]: ...
```

Mutant files: `teamtrack/mutants/<module>.jsonl` and `datasets/mutants/<library>/<module>.jsonl`, one
Mutant per line. A mutant whose `original` text does not match the line is an error at load time.

---

## 15. Workspace artifacts

### 15.1 `feature_list.json`

```json
{
  "$schema": "./feature_list.schema.json",
  "features": [
    {
      "id": "F3",
      "category": "api",
      "description": "Idempotency keys on create-issue",
      "steps": ["POST /projects/{id}/issues with Idempotency-Key twice returns the same issue", "..."],
      "passes": false,
      "evidence": null,
      "testedAt": null
    }
  ]
}
```

`evidence` (set only by the harness): `{"gate_id": str, "commit": str, "visible": "x/y", "existing": "x/y", "checks": ["R1", ...]}`.

The agent may not edit `feature_list.json` at all (A2: "It is unacceptable to remove or edit tests",
F-a-80). The scope layer rejects any `apply_patch` hunk that touches the file and reverts any change made
by a `run` command, emitting `blocked` with reason `feature_list.json is written only by the harness`.
Only `harness/scope/status.py` writes the file, after the gate (or, with verify off, the visible tests)
passes. The agent reads it with `read_file`.

### 15.2 `progress.md`
Sections in order: `# Progress`, `## Current feature`, `## Done`, `## In progress`, `## Next`, `## Session log`
(one entry per session: index, start/end commit, summary). The harness appends the session-log entry; the
agent edits the other sections.

### 15.3 `session-handoff.md`
`## Machine summary` (written by the harness: files changed, visible test status, last 5 commits, open
TODO markers, migration heads) and `## Notes from the agent` (written by the agent at wrap-up).

### 15.4 Exec plan (`docs/exec-plans/active/<feature>.md`)
Sections from A7: `Purpose`, `Progress` (checkbox list with timestamps), `Surprises & Discoveries`,
`Decision Log`, `Outcomes & Retrospective`, `Validation` (commands). Moved to `completed/` when `passes`
becomes true.

---

## 16. Datasets

### 16.1 `datasets/teamtrack-features-v1.jsonl`

```json
{
  "inputs": {
    "feature_id": "F1",
    "checkpoint": "m1-s1-start",
    "ticket_text": "...",
    "variant": "canonical",
    "session_budget": [30]
  },
  "outputs": {
    "hidden_test_ids": ["teamtrack/tests/hidden/f1/test_list_filters.py::test_cursor_stable", "..."],
    "allowed_paths": {"build": ["app/api/issues.py", "app/services/issues.py", "app/repositories/issues.py", "tests/visible/**"], "test": ["tests/visible/**"]},
    "mutant_set": "f1",
    "primary_measure": "r1_new_violations>=1"
  },
  "metadata": {"group": "canonical", "example_id": "F1-canonical", "control": false},
  "split": ["section-1", "smoke"]
}
```

### 16.2 `datasets/testgen-targets-v1.jsonl`

```json
{
  "inputs": {"target_id": "TG-boltons-mathutils", "repo": "boltons", "pin": "26.2.0", "module": "boltons/mathutils.py", "existing_tests": ["tests/test_mathutils.py"]},
  "outputs": {"filter_mutants": "datasets/mutants/boltons/mathutils.jsonl#filter", "referee_mutants": "datasets/mutants/boltons/mathutils.jsonl#referee", "known_failures": []},
  "metadata": {"source": "library", "license": "BSD-3-Clause"},
  "split": ["testgen"]
}
```

Validation: `make datasets` validates every line against these models before upload and fails on any
error; counts per group are asserted (60 and 40).

---

## 17. Tracing

| Run | `run_type` | Name | Parent | Metadata |
|---|---|---|---|---|
| Agent run (root) | chain | `agent_run` | — | `run_id, ab_id, arm, feature_id, variant, checkpoint, layers, model, effort, sandboxed` |
| Phase | chain | `phase:build`, `phase:test` | agent run | `phase, session_count` |
| Session | chain | `session:<n>` | phase | `turn_budget, ended_by` |
| Model call | llm | (from `wrap_openai`) | session | usage, cost |
| Tool call | tool | `tool:<name>` | session | `call_id, target, exit_code` |
| Referee (root) | chain | `referee` | — (evaluator trace) | `run_id, arm, seed` |
| Check | tool | `check:<name>` | referee | `new_violations, total_probes` |
| Reviewer | llm | (from `wrap_openai`) | referee | blinded flag |

```python
class Tracer(Protocol):
    def agent_run(self, name: str, metadata: dict, tags: list[str] | None = None,
                  inputs: dict | None = None) -> ContextManager["RunHandle"]: ...  # inputs/metadata scrubbed
    def child(self, name: str, run_type: str, **metadata: Any) -> ContextManager["RunHandle"]: ...
    def url(self, handle: "RunHandle") -> str | None: ...
    def wrap_openai(self, client: Any) -> Any: ...  # LangSmith wrap_openai; NullTracer returns the client
```

Tags: `section-N` or `batch-N`, arm, `class` or `experiment` or `assignment`.

---

## 18. CLI and Makefile

### 18.1 CLI (Typer)

| Command | Key options | Exit codes |
|---|---|---|
| `shipharness run` | `--feature`, `--checkpoint`, `--ticket-file`, `--layers`, `--workspace` | 0 completed, 2 aborted (cap/timeout), 1 error |
| `shipharness testgen` | `--repo`, `--module`, `--layers none\|verify`, `--max-tests` | 0, 2, 1 |
| `shipharness check` | `--app`, `--rules R1,...`, `--baseline <ref>`, `--json` | 0 no new violations, 3 new violations, 1 error |
| `shipharness review` | `--diff`, `--task`, `--criteria` | 0, 2, 1 |
| `shipharness ab` | `--feature`, `--layers`, `--dataset/--split`, `--k`, `--reviewer/--no-reviewer`, `--replay <run_id>` | 0, 2, 1 |
| `shipharness console` | `--port` (default 8765) | — |
| `shipharness skills validate` | `<path>` | 0, 1 |
| `shipharness doctor` | `--offline` | 0 all pass, 1 any fail |
| `shipharness report` | `--exports` | 0, 1 |

### 18.2 Make targets
`setup`, `doctor`, `up` (TeamTrack + board on the host), `console`, `datasets`, `demo-1`..`demo-4`
(`LAYERS=-<layer>` optional), `swap-1`..`swap-4`, `final FEATURES=F5,F6`, `replay RUN=<id>`,
`experiments` (`BATCH=1..4` optional), `report`, `pilot`, `check-assignment-1`..`4`,
`grade-assignment-1`..`4`, `lint`, `format`, `lint-prose`, `test` (unit), `test-live`, `slides`.

---

## 19. Walkthrough anchors

```python
# [walkthrough:S3:allowed_paths] start
...code shown in class...
# [walkthrough:S3:allowed_paths] end
```

Markdown and shell files use their comment syntax (`<!-- [walkthrough:S1:agents_md] start -->`).
`scripts/anchors.py extract <id>` prints the lines; slides and docs include them by ID. A unit test fails
if an anchor in DESIGN.md §14.2 is missing, unbalanced, or longer than 40 lines.

---

## 20. Secrets

- Keys live only in `.env` at the repo root (created from `.env.example`) or in the process
  environment. `.env` is in `.gitignore`; `tests/unit/test_secrets.py` fails if `.env` is tracked by git
  and fails if any tracked file contains a string matching an OpenAI or LangSmith key pattern.
- `Settings` holds keys as `pydantic.SecretStr`. `repr`, `str`, logs, events, run logs, exports, traces,
  and error messages never contain a key value. structlog has a processor that redacts any value of a
  field whose name contains `key`, `token`, or `secret`, and any string matching the key patterns.
- LangSmith tracing: `@traceable` uses `process_inputs`/`process_outputs` hooks that drop credential
  fields; the OpenAI client is constructed from the key, never traced with it.
- Containers: `docker_run_args` builds an explicit environment (`HOME`, `PATH`, `PYTHONDONTWRITEBYTECODE`,
  `TEAMTRACK_*`) and never passes the host environment, `--env-file`, or any variable whose name contains
  `KEY`, `TOKEN`, or `SECRET`. A unit test asserts this on the generated argument list.
- `shipharness doctor` reports each key separately as `missing`, `invalid` (auth error from the provider),
  `unreachable` (network error), or `ok`, with the next step for each (for example "OPENAI_API_KEY is
  missing: add it to .env at the repo root"). It never echoes any part of a key.

---

## 21. M4 additions (binding)

Built by the seven M4 builders against the builder contract
(`instructor/engineering-notes/2026-10-16-m4-builder-contract.md`) and integrated on `main`.

**Runner and layers**
- `AgentRunResult.claims: dict[Phase, ClaimValue] = {}` (one claim per phase); `claim` stays as the last claim.
- Shared `LayerContext.state` keys: `last_claim` (`{"phase", "claim", "summary"}`, set by the loop at
  every `finish`), `verify.gate` (last `GateResult` dict), `scope.passes_set` (bool),
  `state.handoff_path` (workspace-relative), `instructions.files_read` (list), `harness.setup_sha`
  (commit after `prepare_workspace`).
- The loop appends `REVERTED: <reason>` lines to a tool result when `after_tool` returns `block` or
  `revert` decisions; `session_stop.handoff_path` comes from `state.handoff_path`.
- `shipharness.harness.layers` imports all four layers; `Harness.from_names(names, **kwargs)` passes the
  same keyword arguments to every layer, and every layer ignores unknown ones. State/scope kwargs:
  `feature_category`, `feature_description`, `feature_steps`, `now`, `status_test_timeout_s`,
  `handoff_test_timeout_s`.
- Host-side tool limits: `read_file` refuses files over 1,000,000 bytes and cuts lines at 2,000 chars;
  `search` skips files over 1,000,000 bytes, matches the first 2,000 chars of a line, and stops after
  10 s, saying so. Tool logs stay outside the workspace.

**Checks**
- Runner: `python -P -m shipharness.checks.runner --build <dir> --checks a,b --checkpoint <tag> --feature
  <id> --seed <n> [--params f.json] [--baseline f.json] [--nonce <hex>]`; stdout `{"results":
  [CheckResult, ...], "nonce": <hex>}`, stderr one JSON progress line per update; exit 0 no new
  violations, 3 new violations, 1 error. `-P` keeps the working directory (the arm's build, for the
  referee) off `sys.path`; callers pass a fresh nonce and accept only the results document carrying it.
- Parameter names live in `shipharness.checks.params` (`hidden_tests`, `shipped_tests`,
  `regression_targets`, `regression_expected`, `run_id`, `changed_files`, `phase_files`, `allowed_paths`,
  `harness_artifacts`, `exemptions`, `flaky_runs`, `run_log`, `session_patches`, `artifacts_dir`, ...).
  The referee and the gate build params only with these names; a test checks that every name a check
  reads is declared. Without `exemptions` the runner uses the adapter's documented exemptions; the gate
  sends the same params to its baseline run and every gate run.
- `Sandbox.exec(command, timeout_s)` honours the caller's limit. Agent tool calls are capped at
  `TOOL_TIMEOUT_S` in `runner/tools.py`; harness commands (gate, gate baseline, referee) pass their own.
- `Finding.detail_key: str = ""` is part of the baseline key `(rule, endpoint, severity, detail_key)`;
  `info` findings are shown, never counted. `CheckResult.metrics: dict[str, float | int | bool | None]`.
  `CheckContext.params` and `CheckContext.is_exempt(rule, endpoint)`.
- Tenant app adapter `shipharness.checks.adapter.TenantAppAdapter` (TeamTrack built in;
  `shipharness check --adapter module:attr`). Endpoint discovery includes every operation except the
  public allowlist (`GET /health`, `POST /auth/login`).
- `shipharness.checks.scores.score_fields(results)` maps runner results to ScoreRecord fields; failing
  counts use `max(counted findings, new + baseline violations)` because findings are capped at 200.

**Filters and testgen**
- `FilterContext` adds `existing_tests`, `surviving_mutant_ids`, `target_module`, `python`,
  `timeout_s`, `runs` (all defaulted). `build_context(workspace, sandbox, *, existing_tests, mutants,
  target_module, python, timeout_s, runs)`.
- `run_pipeline(cands, ctx, bus, *, filters, run_id, arm, phase)`; `run_mutant(..., python=)`.
- `Mutant.target` is the dotted module (`app.services.issues`); ids `<target>-m<n>`; files
  `teamtrack/mutants/<target>.jsonl`. The verify layer's test phase builds the context with the tests that
  existed at phase start and phase-start fingerprints restricted to source files.
- `shipharness testgen --repo --module [--layers none|verify] [--max-tests N] [--sandbox local|docker]
  [--image] [--tests] [--python] [--out]`.

**A/B, referee, sandbox**
- `docker_run_args(..., extra_mounts: list[tuple[Path, str, "ro" | "rw"]] | None = None)` and the same on
  `DockerSandbox`; mounts inside `/work` must be `ro`, and nothing may cover `/work` itself.
- `ab/artifacts.py: HARNESS_ARTIFACT_PATTERNS` (DESIGN D-18). Referee-set mutants load by
  `mutant_set` (`ab/mutants.py: referee_mutants`, used by the A/B, the swap test, replay, and
  experiments; names resolve to `teamtrack/mutants/<name>.jsonl`; DESIGN D-21). Only shipped tests that
  pass on the arm's unmutated build judge mutants.
- Before judging, the referee restores the checkpoint's `conftest.py`, `tests/conftest.py`,
  `pytest.ini`, `setup.cfg`, `tox.ini`, and `pyproject.toml`, removes anything the arm put under
  `tests/hidden`, and sends `regression_expected` (the checkpoint's visible test ids; a missing one is a
  regression). A referee container that fails to start gives a "could not judge" verdict, not an error.
- `ABDeps.preview_factory(arm, bus, spec)` returns an object with `start_server()` and `run(stop)`;
  the runtime builds one preview container per arm on the referee image when sandboxed, and none when
  unsandboxed. A preview that fails to start is logged and skipped; previews stop on every path. The
  preview server reloads when the arm changes `app/`. Preview containers mount the arm workspace
  read-only (`SandboxPolicy.workspace_read_only`), so a preview can never change the arm's diff.
- `continuity` counts `session_stop` events of `params.run_id` only: an A/B writes both arms to one
  run log, and the referee passes the scored run's id.

**Console**
- Routes: `GET /` (runs), `GET /run/{id}` (five screens), `GET /screens/{id}` (SSE of rendered screens),
  `GET /events/{id}` (raw events, `Last-Event-ID`), `GET /runs/{id}/files/{path}` (PNG files inside the
  run directory only). `create_console_app(runs_dir, exports_dir=None)`.
- `screenshot.overlays[].mark` is one of `other_org`, `duplicate`, `lost_update`, `conflict_detected`,
  `error`.

**CLI**: `doctor`, `up`, `console`, `datasets`, `check`, `testgen`, `run`, `review`, `ab`, `replay`,
`report`, `experiments`, `skills validate`.
