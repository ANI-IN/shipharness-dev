# Code walkthrough

Every walkthrough anchor in the repository, in class order, with the file, the lines, and what to
say. The code blocks below were pulled with `platform/scripts/anchors.py extract`; they are not retyped. If a
block looks out of date, the file wins: print the current lines with
`uv run python platform/scripts/anchors.py extract <id>` and `uv run python platform/scripts/anchors.py list` for the
line numbers. `uv run python platform/scripts/anchors.py check` fails if an anchor is missing, unbalanced, or
longer than 40 lines.

Talking points cite RESEARCH.md source and finding ids. Line numbers in the headings include the two
marker lines; when they drift, `uv run python platform/scripts/anchors.py list` has the current ones. In class
the walkthrough runs while `make show-N` goes on (run sheet, section pattern).

How to show code in class: open the file in the editor at the start marker (search for
`[walkthrough:<id>] start`), font size large enough for the back row, and walk top to bottom. Slides
show at most 12 of these lines; the editor shows the full anchor.

| Section | Time | Anchors |
|---|---|---|
| Opening | about 1 minute each, inside the 3-minute tour | `Opening:two_arms`, `Opening:publish` |
| S1 Instructions | 10 minutes | `S1:agents_md`, `S1:progressive`, `S1:prefix` |
| S2 State and session lifecycle | 10 minutes | `S2:init`, `S2:stop_resume`, `S2:write` |
| S3 Scope and sandbox | 10 minutes | `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile` |
| S4 Verification | 10 minutes | `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate` |
| Final | about 2 minutes each | `Final:dots`, `Final:skill_template` |

---

## Opening

Show the architecture diagram first (DESIGN §3.2), then these two anchors. The point of the opening
code is the fairness of the comparison, not the details.

### Opening:two_arms

File: `platform/src/shipharness/ab/demo.py:403-424` (pulled with `uv run python platform/scripts/anchors.py extract Opening:two_arms`)

```python
        # Same task, same model, effort, budgets, cost cap, tools, and sandbox for both arms.
        # The only difference is the harness. Both arms run at the same time.
        # Both arms are judged by the same referee on what they shipped (aborted runs too),
        # each as soon as it finishes: no idle wait for the other arm.
        def run_and_judge(arm: Arm) -> tuple[AgentRunResult, ScoreRecord]:
            result = run_arm(task, specs[arm], deps, bus, run_dir)
            baseline.join()
            referee.baseline()  # computed by the thread (or now, if the thread failed)
            return result, _judge(referee, specs[arm], result, bus, run_dir)

        try:
            with ThreadPoolExecutor(max_workers=2, thread_name_prefix="arm") as pool:
                futures = {arm: pool.submit(run_and_judge, arm) for arm in arms}
                done = {arm: future.result() for arm, future in futures.items()}
        finally:
            stop.set()  # previews stop (and their containers with them) on every path
            for thread in previews:
                thread.join(timeout=10)
        results = {arm: done[arm][0] for arm in arms}
        records = {arm: done[arm][1] for arm in arms}
```

Talking points:
- Both specs come from one set of values: same model, reasoning effort, ticket, budgets, cost cap,
  tools, and sandbox policy. The only differences are the arm label, run id, layers, and workspace
  path (DESIGN §6.1; integrity rules 1 and 2 in DESIGN §8.3).
- `ThreadPoolExecutor(max_workers=2)`: the two arms run at the same time, so neither gets a quieter
  API or a warmer cache by going second.
- The `finally` block stops the board previews on every path, including a crash.
- `run_and_judge`: each arm is judged by the same referee as soon as it finishes, on what it
  shipped; aborted runs are judged too (DESIGN §8.3 rules 1 and 9). The faster arm does not wait for
  the slower one (owner decision after pilot run 2; VERIFICATION.md, M6).
- Ask the room: "What would make this comparison unfair?" Then show the forbidden list in DESIGN
  §8.3 (different model per arm, re-running until the bare arm fails, dropping runs).

### Opening:publish

File: `platform/src/shipharness/events/bus.py:143-183` (pulled with `uv run python platform/scripts/anchors.py extract Opening:publish`)

```python
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
```

Talking points:
- Every stage of a run goes through `publish`: validate the data against the event type's model
  (CONTRACTS §8.2), redact anything key-shaped (CONTRACTS §20), append one JSON line, flush and
  `fsync`, then notify listeners.
- The console streams this same file over server-sent events (CONTRACTS §8.1). There is no second
  channel that could disagree with the log.
- `recorded=True` is how replays mark their events; the console shows the red RECORDING badge for
  them (DESIGN §13). Point at this field now; it comes back in the fallback story.

---

## S1 Instructions (10 minutes)

Problem first, then code: the rule at risk (R1) is written down in `docs/HANDBOOK.md`, which both
arms can read (DESIGN §6.1). The code shows how the harness arm is pointed at it.

### S1:agents_md (3 minutes)

File: `platform/teamtrack/harness/instructions/AGENTS.md:1-38` (pulled with `uv run python platform/scripts/anchors.py extract S1:agents_md`)

````markdown
# AGENTS.md

This file is the map of the TeamTrack repository: a table of contents, not the manual. It tells you
where each rule lives. Open the document for the part you are changing before you edit code.

TeamTrack is a multi-tenant issue tracker: an HTTP API (FastAPI) plus a small web board (Jinja2 and
HTMX). Each customer is an org, and every customer row carries an `org_id`.

## Where to look

| When you are about to | Read first |
|---|---|
| add or change an endpoint | `.agents/skills/add-endpoint/SKILL.md` (step by step) |
| touch a router, service, repository, or model | `ARCHITECTURE.md` (layers, R6) |
| decide who may see or change data | `docs/SECURITY.md` (R1 tenant isolation, R2 roles) |
| shape a list, an error, or a status code | `docs/design-docs/api-conventions.md` (R3) |
| write a create endpoint or any write | `docs/RELIABILITY.md` (R4 idempotency, R5 audit) |
| change the database schema | `docs/RELIABILITY.md` (R7 migrations) |
| change issue or project behaviour | `docs/product-specs/teamtrack-base.md` |
| write or run tests | `docs/QUALITY_SCORE.md` (testing, known gaps) |
| plan a change or check the roadmap | `docs/PLANS.md` |
| understand why the code is shaped this way | `docs/design-docs/index.md` |
| look up a tool (Alembic, import-linter) | `docs/references/` |

## House rules at a glance

Every endpoint follows all seven rules, new endpoints included. Automated checks find endpoints in
the OpenAPI schema, so a new endpoint is checked the moment it exists.

- R1 Tenant isolation: another org's resource is 404, never 403. See `docs/SECURITY.md`.
- R2 Roles: viewers get 403 on every write; some writes are admin-only. See `docs/SECURITY.md`.
- R3 API conventions: list envelope, error envelope, status codes. See `docs/design-docs/api-conventions.md`.
- R4 Idempotent creates: honour `Idempotency-Key`. See `docs/RELIABILITY.md`.
- R5 Audit log: one audit row per write. See `docs/RELIABILITY.md`.
- R6 Layering: `app/api` never imports `app/db`. See `ARCHITECTURE.md`.
- R7 Migrations: one Alembic head, upgrade works on an empty database. See `docs/RELIABILITY.md`.
````

Talking points:
- A1 describes AGENTS.md as a map: "A short AGENTS.md (roughly 100 lines) is injected into context
  and serves primarily as a map" and "we treat it as the table of contents" (A1, F-a-22, F-a-27,
  F-a-28). The file introduces itself in those terms: "a table of contents, not the manual".
- The anchor is the core 36 lines of the 94-line file (DESIGN §14.2). The "Where to look" table is
  the map: each row sends the agent to one document, following A1's docs layout (A1, F-a-30,
  F-a-31).
- Progressive disclosure for docs: "agents start with a small, stable entry point and are taught
  where to look next" (A1, F-a-36). The documents the map points to are read on demand.
- "House rules at a glance": one line per rule R1-R7 with a pointer. "House rules" is the course's
  label for what A1 calls "golden principles" and "taste invariants" (A1, F-a-96, F-a-99; RESEARCH
  G-9).
- Fairness: the bare arm has the same rules in one unstructured `docs/HANDBOOK.md`; a unit test
  checks every rule id appears in both forms (DESIGN §6.1). The harness changes organisation, never
  facts.
- Ask: "Why not paste all 150 lines of the handbook into the prompt?" Answer from A1: "A giant
  instruction file crowds out the task, the code, and the relevant docs" (A1, F-a-23).

### S1:progressive (3.5 minutes)

File: `platform/src/shipharness/runner/skills_loader.py:49-90` (pulled with `uv run python platform/scripts/anchors.py extract S1:progressive`)

```python
class SkillsLoader:
    """Tier 1 (name + description) goes into the context prefix for every skill.

    Tier 2 (the full SKILL.md) and tier 3 (referenced files) are never pre-loaded: the agent reads
    them with read_file when a task matches, and `skill_for_path` tells the harness which tier a
    read touched, so the console can show which skills the agent actually opened.
    """

    def __init__(self, root: Path, workspace_prefix: str = ".agents/skills") -> None:
        self.root = Path(root)
        self.prefix = workspace_prefix.strip("/")

    def catalogue(self) -> list[SkillMeta]:
        if not self.root.is_dir():
            return []
        skills: list[SkillMeta] = []
        for skill_md in sorted(self.root.glob("*/SKILL.md")):
            fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            if not fields or not fields.get("name") or not fields.get("description"):
                continue
            folder = skill_md.parent.name
            skills.append(
                SkillMeta(
                    name=fields["name"],
                    description=fields["description"],
                    path=f"{self.prefix}/{folder}",
                )
            )
        return sorted(skills, key=lambda s: s.name)

    def catalogue_block(self) -> str:
        skills = self.catalogue()
        if not skills:
            return ""
        rows = [f"- {s.name}: {s.description} (read {s.path}/SKILL.md to use it)" for s in skills]
        return (
            "Available skills (load a skill's SKILL.md only when the task needs it):\n"
            + "\n".join(rows)
        )
```

Talking points:
- Three tiers from the Agent Skills spec: "Metadata (~100 tokens)" at startup, "Instructions (< 5000
  tokens recommended)" on activation, "Resources (as needed)" (B1, B2; F-b-05, F-b-06).
- `catalogue()` skips a skill without `name` or `description`: both fields are required by the spec
  (B1, F-b-01 to F-b-04).
- `catalogue_block()` is the only skill text in the context prefix: one line per skill with the path
  to read. The full SKILL.md is never pre-loaded.
- The docstring names `skill_for_path`: it tells the harness which tier a read touched, so console
  screens 1 and 3 can show which skills the agent actually opened.
- `.agents/skills/` is the cross-client convention (B3; RESEARCH §4.5 lists the install paths per
  agent).

### S1:prefix (3.5 minutes)

File: `platform/src/shipharness/harness/instructions/router.py:28-50` (pulled with `uv run python platform/scripts/anchors.py extract S1:prefix`)

```python
def build_prefix(source: Path) -> str:
    """One stable text block: the map, then tier 1 of every skill (name + description).

    A1: "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a
    map, with pointers to deeper sources of truth elsewhere." The documents the map points to are
    not injected; the agent reads them with read_file when its task needs them. Skills follow the
    same progressive disclosure (B1): only the catalogue line is here, never a SKILL.md body.
    """
    source = Path(source)
    agents_md = strip_markers((source / MAP_FILE).read_text(encoding="utf-8")).strip()
    blocks = [
        "Repository map (AGENTS.md at the workspace root). It points to the documents to read "
        "before you change code; open them with read_file when your task needs them.",
        agents_md,
    ]
    catalogue = SkillsLoader(source / SKILLS_DIR, workspace_prefix=SKILLS_DIR).catalogue_block()
    if catalogue:
        blocks.append(catalogue)
    return "\n\n".join(blocks)
```

Talking points:
- The docstring quotes A1 (F-a-27, F-a-28): the map is injected; the documents it points to are
  not.
- Order of the prefix: one sentence of instructions, the map, then the skills catalogue. Nothing
  else.
- Why "stable": prompt caching needs the whole rendered prefix to match (RESEARCH §4.2, C4). A
  prefix that changes every turn would pay full input price every turn.
- The bare arm gets no injected map and no catalogue; the handbook is on disk (DESIGN §6.2).
- Transition to the demo: "Both arms can read the same rules. One has a map in its context. Let us
  see whether that changes what ships."

---

## S2 State and session lifecycle (10 minutes)

Problem first: a new session starts with an empty context; "each new session begins with no memory
of what came before" (A2, F-a-08). The code shows what the harness leaves on disk for the next
session.

### S2:init (3 minutes)

File: `platform/src/shipharness/harness/state/assets/init.sh:2-29` (pulled with `uv run python platform/scripts/anchors.py extract S2:init`)

```bash
# init.sh for {{feature_id}}, written by the harness initializer step.
# A2: "an init.sh script that can run the development server", then
# "run through a basic end-to-end test before implementing a new feature".
#
#   bash init.sh          scratch database at head, then a basic end-to-end test
#   bash init.sh serve    the same, then the development server in the background
set -euo pipefail
cd "$(dirname "$0")"

# A scratch database outside the repository, so setup leaves no files to commit.
export TEAMTRACK_DATABASE_URL="sqlite:////tmp/teamtrack-dev.db"
export TEAMTRACK_SEED=true

echo "== migrations (house rule R7: exactly one head)"
python -m alembic heads
python -m alembic upgrade head

echo "== basic end-to-end test: issues, stop at the first failure (full suite: run_visible_tests)"
python -m pytest tests/visible/test_issues.py -x -q --no-header -p no:cacheprovider

if [ "${1:-}" = "serve" ]; then
  echo "== development server on http://127.0.0.1:8000 (log in /tmp/teamtrack-dev.log)"
  nohup python -m uvicorn app.main:create_app --factory --port 8000 \
    >/tmp/teamtrack-dev.log 2>&1 &
  echo "server pid $!"
fi
```

Talking points:
- The comments carry A2's own words: "an init.sh script that can run the development server" (A2,
  F-a-50) and a basic end-to-end test before new work (A2, F-a-61).
- The scratch database lives in `/tmp`, outside the repository, so running setup leaves nothing to
  commit (clean state: A2, F-a-84).
- `alembic heads` first: house rule R7 (one head) is what the S2 primary measure watches (DESIGN
  §8.2).
- Who writes it: the harness's initializer step, as deterministic code rather than a model session,
  because the files are fixed by the ticket. The course says so and cites A2's footnote that the
  initializer and coding agents differ only in their initial prompt (A2, F-a-52; DESIGN D-11).

### S2:stop_resume (4 minutes)

File: `platform/src/shipharness/harness/state/lifecycle.py:95-134` (pulled with `uv run python platform/scripts/anchors.py extract S2:stop_resume`)

```python
def session_stop(
    ctx: LayerContext, result: SessionResult, files_changed: list[str], claim: str, timeout_s: int
) -> tuple[list[HarnessDecision], str]:
    """Write the machine part of the handoff and the progress log entry, then commit them."""
    ws: Path = ctx.workspace
    summary, tests = machine_summary(ctx, result, files_changed, timeout_s)
    template = (ASSETS / HANDOFF).read_text(encoding="utf-8")
    write_file(ws, HANDOFF, handoff.merge(read_text(ws, HANDOFF), template, summary).encode())
    log = read_text(ws, PROGRESS) or (ASSETS / PROGRESS).read_text(encoding="utf-8")
    entry = progress.session_entry(result, len(files_changed), tests, claim)
    write_file(ws, PROGRESS, progress.append_session_entry(log, entry).encode())
    commit_paths(
        ctx.sandbox,
        [HANDOFF, PROGRESS],
        f"harness: session {result.index} handoff for {ctx.spec.feature_id}",
    )
    ctx.state["state.handoff_path"] = HANDOFF
    stop = HarnessDecision(
        kind="session_stop",
        layer="state",
        message=f"session {result.index} handoff written to {HANDOFF}",
        paths=[HANDOFF, PROGRESS],
        data={"session_index": result.index, "files_changed": len(files_changed)},
    )
    return [stop], summary


def resume_text(summary: str, phase: str = "build") -> str:
    """Extra resume text for the harness arm (the neutral resume sentence comes first)."""
    text = (
        "Start with the Getting up to speed steps before you change code. The structured "
        "handoff from the last session is in session-handoff.md."
    )
    if phase == "test":
        text = f"{text} {TEST_PHASE_FIRST}"
    return f"{text} Its machine summary:\n\n{summary[:3000]}" if summary else text
```

Talking points:
- The forced stop is a course mechanism, the session turn budget, which produces what A3 calls a
  context reset: "clearing the context window entirely and starting a fresh agent, combined with a
  structured handoff" (A3, F-a-65 to F-a-69; RESEARCH G-5). For F2 the budget is `[20, 30]`
  (`platform/teamtrack/reference/f2/task.toml`).
- `session_stop` writes the machine part of `session-handoff.md` itself (files changed, test status,
  last commits), so the handoff exists even when the agent writes none (DESIGN §6.3).
- It appends the progress entry and commits both files: "End the session by writing a git commit and
  progress update." (A2, F-a-63)
- `resume_text` is extra text for the harness arm only. Both arms first get the same neutral resume
  sentence (`NEUTRAL_RESUME` in `platform/src/shipharness/runner/prompts.py`), and both get the same number of
  wrap-up turns (DESIGN §6.1).
- `phase == "test"`: a test-phase session starts with the feature's tests (`TEST_PHASE_FIRST`,
  change 9 in VERIFICATION.md, "Pilot-driven changes after run 2"), so the session does not spend its
  turns on the getting-up-to-speed routine before writing any test.
- Context resets are model-dependent: A3 later dropped them for a newer model (RESEARCH §5,
  correction 4). Teach the handoff as a choice, not a law.

### S2:write (3 minutes)

File: `platform/src/shipharness/harness/state/progress.py:11-37` (pulled with `uv run python platform/scripts/anchors.py extract S2:write`)

```python
def session_entry(
    result: SessionResult, files_changed: int, tests: str, claim_summary: str = ""
) -> str:
    """One log line: index, start/end commit, how the session ended, and a summary."""
    entry = (
        f"- Session {result.index} ({result.phase}): start {result.start_sha[:7] or 'none'}, "
        f"end {result.end_sha[:7] or 'none'}, ended by {result.ended_by} after "
        f"{result.turns} turns. {files_changed} files changed; visible tests {tests}."
    )
    summary = " ".join(mask_keys(claim_summary).split())[:200]
    return entry + (f' Agent summary: "{summary}"' if summary else "")


def append_session_entry(text: str, entry: str) -> str:
    """Append `entry` under "## Session log", restoring the heading if the agent removed it.

    The log is the last section, so appending at the end keeps the agent's other edits intact.
    """
    lines = text.replace("\r\n", "\n").rstrip("\n")
    if not any(line.strip() == SESSION_LOG for line in lines.splitlines()):
        lines += f"\n\n{SESSION_LOG}"
    separator = "\n\n" if lines.endswith(SESSION_LOG) else "\n"
    return f"{lines}{separator}{entry}\n"
```

Talking points:
- A2's progress file is "a log of what agents have done" (A2, F-a-50, F-a-53); the course names it
  `progress.md` and says so (RESEARCH §3.2).
- One line per session: start and end commit, how the session ended, turns, files changed, visible
  test result. Facts from the harness, then the agent's own summary, with key-shaped strings masked
  and cut to 200 characters.
- `append_session_entry` restores the "## Session log" heading if the agent deleted it: the agent may
  edit the rest of the file, but it cannot erase the log.
- Git history is the other half of the state: A2 reads "the claude-progress.txt file alongside the
  git history" (A2, F-a-53).

---

## S3 Scope and sandbox (10 minutes)

Problem first: the agent changes files it was never asked to touch. Cause 3 has no single source
sentence; present the citations side by side (RESEARCH G-1): A1 on pattern copying (F-a-20), A4 on
the container warning and the `pkill -9 bash` incident (F-a-18, F-a-19), A5 restricting file
operations "to the project directory only" (F-a-86), A6 as supplementary (F-a-21).

### S3:allowed_paths (2.5 minutes)

File: `platform/src/shipharness/harness/scope/guard.py:59-97` (pulled with `uv run python platform/scripts/anchors.py extract S3:allowed_paths`)

```python
@dataclass(frozen=True)
class PathRules:
    """What the agent may change in one phase. `allowed=None`: the task gave no list."""

    phase: str
    allowed: list[str] | None
    state_files: bool  # the state layer is on, so progress.md and friends are the agent's

    def reason(self, path: str) -> str | None:
        """None if the agent may change `path`; otherwise the reason it sees."""
        rel = normalise(path)
        if rel in HARNESS_ONLY:
            return HARNESS_ONLY[rel]
        if self.state_files and any(glob_matches(rel, p) for p in STATE_FILES):
            return None
        if self.allowed is None or any(glob_matches(rel, p) for p in self.allowed):
            return None
        listed = ", ".join(self.allowed) or "(none)"
        return f"{rel} is outside the allowed paths for the {self.phase} phase ({listed})"


def check_paths(rules: PathRules, paths: list[str]) -> dict[str, list[str]]:
    """Group the refused paths by reason (one blocked decision per reason)."""
    refused: dict[str, list[str]] = {}
    for path in paths:
        reason = rules.reason(path)
        if reason is not None:
            key = reason if normalise(path) in HARNESS_ONLY else _phase_reason(rules)
            refused.setdefault(key, []).append(normalise(path))
    return refused


def _phase_reason(rules: PathRules) -> str:
    listed = ", ".join(rules.allowed or []) or "(none)"
    return f"outside the allowed paths for the {rules.phase} phase ({listed})"
```

Talking points:
- `PathRules` holds one phase's allow list (from the task, for example `[allowed_paths]` in
  `platform/teamtrack/reference/f3/task.toml`).
- Order inside `reason()`: harness-only files first (`feature_list.json` may not be edited at all;
  A2, F-a-80; DESIGN D-14), then the state files when the state layer is on, then the allow list.
- The returned string is what the agent reads in its tool result. A1 writes lint messages "to inject
  remediation instructions into agent context" (A1, F-a-97); the reason names the phase and the
  allowed paths.
- `check_paths` groups refused paths by reason, so the console shows one `blocked` decision per
  reason rather than one per file.
- Source status: per-phase path lists are the course's application of A5 (F-a-86) and A1's "enforce
  boundaries centrally, allow autonomy locally" (F-a-92); mark it as composite (RESEARCH §3.3).

### S3:passes (2.5 minutes)

File: `platform/src/shipharness/harness/scope/status.py:84-120` (pulled with `uv run python platform/scripts/anchors.py extract S3:passes`)

```python
def update_status(
    ctx: LayerContext,
    result: SessionResult,
    feature: dict[str, Any],
    now: Callable[[], datetime],
    test_timeout_s: int = 300,
) -> list[HarnessDecision]:
    """Set `passes` for the feature if, and only if, the evidence is there."""
    if ctx.state.get("scope.passes_set") or result.phase != "build":
        return []
    if not claimed_done(ctx, result):
        return []  # no claim, no status change, nothing run
    if "verify" in ctx.spec.layers:
        evidence, why_not = _gate_evidence(ctx)
    else:
        evidence, why_not = _visible_tests_evidence(ctx, test_timeout_s)
    if evidence is None:
        message = f"passes stays false for {feature['id']}: {why_not}"
        return [HarnessDecision(kind="note", layer="scope", message=message)]
    tested_at = now().astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    feature.update(passes=True, evidence=evidence, testedAt=tested_at)
    write_feature_list(ctx.workspace, feature)
    commit_paths(ctx.sandbox, [FEATURE_LIST, FEATURE_SCHEMA], f"harness: {feature['id']} passes")
    ctx.state["scope.passes_set"] = True
    return [
        HarnessDecision(
            kind="status_set",
            layer="scope",
            message=f"{feature['id']} passes: {evidence['gate_id']} at {evidence['commit'][:7]}",
            paths=[FEATURE_LIST],
            data={"feature_id": feature["id"], "evidence": evidence, "testedAt": tested_at},
        )
    ]
```

Talking points:
- Nothing happens without a `finish` claim of done in the build phase.
- Evidence comes from the verify gate when that layer is on, otherwise from the visible tests.
  Without evidence the harness writes a note, "passes stays false for ...", and changes nothing.
- With evidence it sets `passes`, `evidence`, and `testedAt` and commits the file itself.
- Course design, said out loud (RESEARCH G-6): A2 lets the agent set `passes` after careful testing
  (A2, F-a-108). The course moves that decision to the harness, citing A3: "Separating the agent
  doing the work from the agent judging it proves to be a strong lever" (A3, F-a-110).

### S3:policy (2 minutes)

File: `platform/src/shipharness/sandbox/policy.py:62-87` (pulled with `uv run python platform/scripts/anchors.py extract S3:policy`)

```python
class SandboxPolicy(BaseModel):
    """Machine-level limits. Identical for both arms in every run; never an A/B variable."""

    model_config = ConfigDict(frozen=True)

    version: int = 1
    network: str = "none"  # only loopback inside the container
    cpus: float = 1.0
    memory_mb: int = 1024
    swap_mb: int = 0  # --memory-swap equal to --memory: no swap
    pids_limit: int = 256
    user: str = "1000:1000"  # non-root
    read_only_root: bool = True  # writes only to /work (workspace) and /tmp
    tmpfs: dict[str, str] = {"/tmp": "rw,nosuid,size=256m"}
    cap_drop: tuple[str, ...] = ("ALL",)
    no_new_privileges: bool = True
    workspace_mount: str = "/work"
    workspace_read_only: bool = False  # True for board previews: they only read the arm
    tool_timeout_s: int = 120
    run_timeout_s: int = 300
    deny_command_patterns: tuple[DenyRule, ...] = DEFAULT_DENY_RULES
    detect_output_patterns: tuple[DetectRule, ...] = DEFAULT_DETECT_RULES
```

Talking points:
- One frozen policy, identical for both arms in every run: the sandbox is never an A/B variable
  (DESIGN §9).
- Each field maps to a Docker flag from the official docs (D24-D30): `--network none` ("only the
  loopback device is created"), memory with no swap, a process limit, a non-root user, a read-only
  root with `/work` and `/tmp` writable, all capabilities dropped, no new privileges.
- Two kinds of rules: `deny_command_patterns` refuse a command before it runs (network installs,
  `curl`, `git clone`); `detect_output_patterns` classify a failure after it runs. Both produce a
  `sandbox_denied` event (CONTRACTS §8.2).
- Compare another agent: Codex has `read-only`, `workspace-write`, and `danger-full-access` modes,
  and "By default, the agent runs with network access turned off." (D21-D23)

### S3:run_args (1.5 minutes)

File: `platform/src/shipharness/sandbox/policy.py:90-124` (pulled with `uv run python platform/scripts/anchors.py extract S3:run_args`)

```python
def docker_run_args(
    policy: SandboxPolicy,
    image: str,
    workspace: Path,
    name: str,
    runtime: str = "docker",
    env: dict[str, str] | None = None,
    extra_mounts: list[Mount] | None = None,
) -> list[str]:
    """Full argv that starts one arm container. Never passes the host environment or keys."""
    args = [runtime, "run", "-d", "--rm", "--name", name, "--init"]
    args += ["--network", policy.network]
    mem = f"{policy.memory_mb}m"
    args += ["--memory", mem, "--memory-swap", f"{policy.memory_mb + policy.swap_mb}m"]
    args += ["--cpus", str(policy.cpus), "--pids-limit", str(policy.pids_limit)]
    if policy.read_only_root:
        args.append("--read-only")
    for mount, options in policy.tmpfs.items():
        args += ["--tmpfs", f"{mount}:{options}"]
    args += ["--user", policy.user]
    for cap in policy.cap_drop:
        args += ["--cap-drop", cap]
    if policy.no_new_privileges:
        args += ["--security-opt", "no-new-privileges"]
    for key, value in _container_env(env).items():
        args += ["-e", f"{key}={value}"]
    mode = ":ro" if policy.workspace_read_only else ""
    args += ["-v", f"{Path(workspace).resolve()}:{policy.workspace_mount}{mode}"]
    args += _mount_args(policy, extra_mounts)
    args += ["-w", policy.workspace_mount, image, "sleep", "infinity"]
    return args
```

Talking points:
- The full `docker run` argument list built from the policy. Read it top to bottom against the
  previous anchor.
- `_container_env` builds an explicit environment and refuses any name that looks like a secret; the
  host environment and the API keys never enter a container (CONTRACTS §20).
- Board previews mount the workspace read-only (`:ro`), so a preview can never change an arm's diff.
- `sleep infinity`: one long-lived container per arm; every tool command runs in it through
  `docker exec` (DESIGN §9). The agent loop itself runs on the host.

### S3:dockerfile (1.5 minutes)

File: `platform/sandbox/Dockerfile:19-33` (pulled with `uv run python platform/scripts/anchors.py extract S3:dockerfile`)

```dockerfile
RUN uv sync --frozen --no-install-project --group dev
# Non-root user; the workspace is bind-mounted at /work and is the only writable path besides /tmp.
RUN useradd --uid 1000 --create-home agent \
    && git config --system user.name "agent" \
    && git config --system user.email "agent@sandbox.invalid" \
    && git config --system --add safe.directory /work
# The check runner (python -m shipharness.checks.runner) comes from the image, never the workspace.
COPY platform/src/ /opt/shipharness/src/
ENV PYTHONPATH=/opt/shipharness/src

FROM base AS agent
USER 1000:1000
WORKDIR /work
```

Talking points:
- `uv sync --frozen` at image build time: dependencies are baked in, so nothing at run time needs
  the network. A4: "Claude did not have internet access at any point during its development" (A4,
  F-a-88, F-a-90).
- Non-root user with uid 1000, matching the policy's `user`.
- The check runner comes from the image (`/opt/shipharness/src`), never from the workspace, so an arm
  cannot ship its own referee (CONTRACTS §21).
- Transition to the demo: "The scope layer blocks by construction, so the harness arm will show zero
  out-of-scope files. The question is whether it still ships a working feature." (DESIGN §8.2, S3
  note)

---

## S4 Verification (10 minutes)

Problem first: "agents reliably skew positive when grading their own work" (A3, F-a-15), and visible
tests miss what held-out tests catch (B13, F-b-45, F-b-50).

### S4:filters (2.5 minutes)

File: `platform/src/shipharness/filters/pipeline.py:34-74` (pulled with `uv run python platform/scripts/anchors.py extract S4:filters`)

```python
def run_pipeline(
    cands: list[CandidateTest],
    ctx: FilterContext,
    bus: EventBus | None,
    *,
    filters: Sequence[Filter] = DEFAULT_FILTERS,
    run_id: str | None = None,
    arm: Arm | None = None,
    phase: Literal["build", "test"] = "test",
) -> list[FilterResult]:
    """Run each proposed test through the filters; stop at its first failure. 1 imports and runs,
    2 passes 5 runs, 3 adds coverage or kills a mutant, 4 real assertions and no mocking of the
    unit under test, 5 no source change in the test phase."""
    results: list[FilterResult] = []
    for cand in cands:
        if bus is not None:
            bus.publish(
                "test_proposed", {"test_id": cand.test_id, "phase": phase}, run_id=run_id, arm=arm
            )
        for flt in filters:
            try:
                result = flt.evaluate(cand, ctx)
            except Exception as exc:  # noqa: BLE001 - a crashing filter discards, with a reason
                result = FilterResult(
                    test_id=cand.test_id,
                    filter=flt.number,
                    passed=False,
                    reason=f"filter error: {type(exc).__name__}: {exc}"[:500],
                )
            if not result.reason:
                result = result.model_copy(update={"reason": f"filter {flt.number}: no reason"})
            results.append(result)
            if bus is not None:
                bus.publish("test_filter_result", result, run_id=run_id, arm=arm)
            if not result.passed:
                break  # discarded: later (more expensive) filters never run
    return results
```

Talking points:
- The docstring lists the five filters in order, cheapest first (DESIGN §7).
- Filters 1-3 come from TestGen-LLM: builds, passes reliably ("a test that does not pass on every one
  of five executions is deemed flaky"), adds coverage (B11, F-b-16 to F-b-22). The mutant branch of
  filter 3 comes from ACH hardening (B12, F-b-29, F-b-32).
- Filters 4 and 5 are course filters with no direct source (RESEARCH G-7). Say so.
- A test stops at its first failure (`break`); later, more expensive filters never run.
- A crashing filter discards the test with a reason instead of crashing the run. Every discarded
  test is shown with its reason on screen 3 (DESIGN §6.5).

### S4:probe (3 minutes)

File: `platform/src/shipharness/checks/r1_tenant.py:65-104` (pulled with `uv run python platform/scripts/anchors.py extract S4:probe`)

```python
def judge(probe: Probe, response: Any, t: Target, home: str, other: str) -> Finding | None:
    """Compare one response with what tenant isolation requires."""
    status, body = response.status_code, json_body(response)
    ok = 200 <= status < 300
    leaked = ok and (
        t.adapter.is_foreign(body, other)
        or (probe.kind == "anonymous" and t.adapter.is_foreign(body, home))
    )
    if probe.kind in ("foreign_path",) or probe.kind.startswith("foreign_param:"):
        failed = status != 404
    else:  # no_path, foreign_body, anonymous: success itself is the failure (no_path: only leaks)
        failed = leaked if probe.kind == "no_path" else ok
    if not failed:
        return None
    return Finding(
        rule="R1",
        severity="leak" if leaked else "violation",
        endpoint=probe.endpoint.label,
        detail_key=probe.kind,
        detail=f"{probe.kind}: {probe.endpoint.method} {probe.path} -> {status} "
        f"{excerpt(response)}",
    )


def probe_all(t: Target, ctx: CheckContext) -> tuple[list[Finding], int]:
    home, other = t.adapter.orgs()
    probes = plan(t, home, other)
    findings: list[Finding] = []
    for done, probe in enumerate(probes, start=1):
        e = probe.endpoint
        response = t.send(e.method, probe.path, probe.body, probe.headers)
        finding = judge(probe, response, t, home, other)
        if finding is not None:
            findings.append(finding)
        ctx.progress(done, len(probes), f"R1 probes {done}/{len(probes)}")
    return findings, len(probes)
```

Talking points:
- `judge` compares one response with what tenant isolation requires: a foreign path or parameter
  must give 404; a leak is a 2xx whose body carries the other org's data (DESIGN §5, R1).
- Severity is `leak` or `violation`; both count as new violations against the checkpoint baseline,
  so the legacy `/v1/issues` leak does not count against either arm (DESIGN §5).
- `probe_all` runs the plan over every endpoint found in the app's OpenAPI schema, so a new endpoint
  is probed the moment it exists. `ctx.progress` drives the "R1 probes n/m" counter on screen 3.
- These are documented house rules both arms can read; the verify gate runs the same checks. That
  overlap is disclosed (DESIGN §8.3 rule 8). Hidden tests and referee-set mutants are never in the
  gate.

### S4:blind (1.5 minutes)

File: `platform/src/shipharness/reviewer/blind.py:15-39` (pulled with `uv run python platform/scripts/anchors.py extract S4:blind`)

```python
def blind(diff: str | bytes) -> str:
    """Return the diff with every arm-identifying trace removed, so two arms that shipped the
    same code produce the same text.

    1. Harness artifacts (AGENTS.md, progress.md, feature_list.json, .agents/, exec plans,
       handoff, init.sh, ...) are dropped file by file: they exist only in the harness arm.
    2. Commit metadata (mail headers before the first file, blob hashes on `index` lines)
       is removed.
    3. Host workspace paths (which contain the arm name) and run ids are normalised.
    The arm label itself is never an input: ReviewInput has no field for it.
    """
    text = diff.decode("utf-8", errors="replace") if isinstance(diff, bytes) else diff
    text = strip_harness_artifacts(text)
    lines = text.splitlines()
    first = next((i for i, line in enumerate(lines) if line.startswith("diff --git ")), None)
    if first is None:
        return ""
    kept = [line for line in lines[first:] if not _INDEX.match(line)]
    body = "\n".join(kept) + "\n"
    body = _WORKSPACE.sub("<workspace>", body)
    return _IDS.sub("<id>", body)
```

Talking points:
- The reviewer is the separate evaluator taught from A3: "tuning a standalone evaluator to be
  skeptical turns out to be far more tractable" (A3, F-a-111).
- Blinding is A/B design machinery, not a source term (RESEARCH §3.4): drop harness artifacts file
  by file, strip commit metadata and blob hashes, normalise workspace paths and run ids.
- `ReviewInput` has no field for the arm label, so the label cannot leak by accident (DESIGN §8.3
  rule 3).
- A3's caveat belongs on the same slide: "the evaluator is still an LLM that is inclined to be
  generous towards LLM-generated outputs" (A3, F-a-112). That is why the referee's deterministic
  checks decide the measures and the reviewer's agreement is reported next to them.

### S4:gate (3 minutes)

File: `platform/src/shipharness/harness/verify/gate.py:143-184` (pulled with `uv run python platform/scripts/anchors.py extract S4:gate`)

```python
def run_gate(
    sandbox: Sandbox,
    cfg: GateConfig,
    *,
    gate_id: str,
    base_sha: str,
    phase: str,
    on_update: Callable[[GateResult], None] | None = None,
    on_progress: Callable[[dict], None] | None = None,
) -> GateResult:
    """Verification the agent does not control: every item runs in the arm container."""
    root = f"/tmp/shipharness-gate-{_SAFE.sub('_', gate_id)}"
    names = ["visible tests", *(_ITEM_ORDER if phase == "build" else []), "clean state"]
    if on_update:  # pending pills first, so the console shows the gate running
        pending = [GateItem(name=n, status="pending") for n in names]
        on_update(GateResult(gate_id=gate_id, items=pending, passed=False, feedback=""))
    sandbox.exec(
        f"rm -rf {root} && mkdir -p {root}/build && cp -a ./. {root}/build/", cfg.limit(300)
    )
    visible, lines = _visible_tests(sandbox, f"{root}/build", cfg)
    items = [visible]
    if phase == "build":
        check_items, check_lines = _check_items(sandbox, cfg, root, on_progress)
        items += sorted(check_items, key=_order)
        lines += check_lines
    clean = clean_state_check(
        sandbox, base_sha, cfg.limit(120), migrations=cfg.migrations, ruff_select=cfg.ruff_select
    )
    items.append(clean)
    if clean.status == "fail":
        lines.append(f"FAIL clean state: {clean.detail}")
    sandbox.exec(f"rm -rf {root}", cfg.limit(60))
    passed = not any(i.status == "fail" for i in items)
    feedback = "" if passed else _feedback(gate_id, items, lines)
    result = GateResult(gate_id=gate_id, items=items, passed=passed, feedback=feedback)
    if on_update:
        on_update(result)
    return result
```

Talking points:
- "Verification the agent does not control": every item runs in the arm container on a copy of the
  workspace.
- Pending pills go to the console first, so screen 1 shows ⏳ before ✓ or ✗.
- Build phase items: visible tests, existing tests, R1-R7, board smoke check, clean state (git clean,
  ruff clean, one migration head, no debug output; A2, F-a-84). Clean state is composite with A4's
  "task verifier is nearly perfect" point (A4, F-a-127; RESEARCH §3.4). `ruff_select`: when the
  repository has no ruff config of its own, the clean-state ruff check pins ruff's documented default
  rules (`E4,E7,E9,F`; VERIFICATION.md, change 21).
- On failure the agent gets feedback with the first three failures and continues within its turn
  budget (`_feedback` in the same file).
- Disclosed overlap: the gate runs the same R1-R7 as the referee; the S4 primary measures (hidden
  tests, referee-set mutants) are never available to the gate or the agent (DESIGN §6.5, §8.3 rule 8).

---

## Final

### Final:dots (2 minutes)

File: `platform/src/shipharness/ab/report.py:83-119` (pulled with `uv run python platform/scripts/anchors.py extract Final:dots`)

```python
def render_dot_plot(group: dict[str, Any], width: int = 640) -> str:
    """One row per arm, one dot per run. Filled = passed the primary measure, hollow = failed,
    so pass/fail never depends on colour alone. The row label carries the count."""
    rows = [a for a in ARM_ORDER if a in group["arms"]]
    values = [_num(d["value"]) for a in rows for d in group["arms"][a]["dots"]]
    totals = [_num(d["total"]) for a in rows for d in group["arms"][a]["dots"] if d["total"]]
    top = max([1.0, *values, *totals])
    left, right, row_h = 150, 24, 56
    height = row_h * len(rows) + 40
    x = lambda v: left + (width - left - right) * (_num(v) / top)  # noqa: E731
    label = f"{group['feature_id']} {group['measure']}"
    parts = _frame(label, width, height, left, right, top)
    for i, arm in enumerate(rows):
        y = row_h * i + 30
        info = group["arms"][arm]
        parts.append(
            f'<text class="label" x="0" y="{y + 5}">{arm} ({info["failing"]} failing)</text>'
        )
        seen: dict[float, int] = defaultdict(int)
        for dot in info["dots"]:
            stack = seen[_num(dot["value"])]
            seen[_num(dot["value"])] += 1
            fill = f"var(--{arm})" if dot["passed"] else "var(--surface)"
            tip = f"{dot['run_id']}: {dot['value']}" + (
                f" of {dot['total']}" if dot["total"] else ""
            )
            parts.append(
                f'<circle cx="{x(dot["value"]):.1f}" cy="{y - stack * 10}" r="5" '
                f'fill="{fill}" stroke="var(--{arm})" stroke-width="2">'
                f"<title>{html.escape(tip)} ({dot['status']})</title></circle>"
            )
    parts.append("</svg>")
    return "".join(parts)
```

Talking points:
- One row per arm, one dot per run. Filled means the run passed the primary measure, hollow means it
  failed, so the result never depends on colour alone.
- The row label carries the count ("N failing"). Results are counts, not percentages (DESIGN §8.3
  rule 5).
- The report reads only `exports/` (DESIGN §12): the same files the console's screen 4 reads.

### Final:skill_template (2 minutes)

File: `use-in-your-repo/skills/skill-template/SKILL.md:2-35` (pulled with `uv run python platform/scripts/anchors.py extract Final:skill_template`)

````markdown
name: skill-template
description: >
  Starting point for writing a new Agent Skill: frontmatter with the spec's fields and a guide to
  the sections of the body. Use when creating a new skill: copy this folder, rename it, set name to
  the new folder name, and replace every placeholder.
license: MIT
# Optional spec fields. Uncomment the ones you need; the spec allows no other fields.
# compatibility: Python 3.12+ and uv
# allowed-tools: Bash Read
# metadata:
#   author: your-name
#   version: "0.1.0"
---

# <Skill title>

<One paragraph: what this skill does and the result the user gets.>

## When to use

- <A situation, in the words a user would type, where this skill applies.>
- <When not to use it, and what to use instead.>

## Steps

1. <First action. Name the exact command, for example `python platform/scripts/<script>.py <args>`.>
2. <What to check in the output before going on.>
3. <...>

## Checks before you finish

- [ ] <A check the agent can run, with the command and the expected result.>
````

Talking points:
- Only the spec's six frontmatter fields; the reference validator rejects any other key (B1;
  RESEARCH §4.5).
- `name` must equal the folder name, which is why the folder is `skill-template` and not `_template`
  (DESIGN D-17).
- `description` says what the skill does and when to use it: it is the tier-1 text an agent sees
  (B1, F-b-05).
- Validate a copy with `uv run shipharness skills validate use-in-your-repo/skills/<name>`. Install into
  `.claude/skills/` and `.agents/skills/`: no single directory is read by Claude Code, Codex, and
  Cursor (RESEARCH §4.5).
