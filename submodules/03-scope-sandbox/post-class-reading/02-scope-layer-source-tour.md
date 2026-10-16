# The scope layer, line by line

Reading time: about 12 minutes.

Class shows two anchors from the scope layer (`S3:allowed_paths`, `S3:passes`). This piece reads the
code around them: what the agent is told, how a tool call is checked and reverted, what counts as
evidence for `passes`, and how the referee counts the S3 measure. Every excerpt is copied from the
file named above it.

## 1. What the agent is told

`src/shipharness/harness/scope/layer.py`, lines 129-151. This block goes into the harness arm's
context prefix.

```python
    def context_prefix(self, ctx: LayerContext) -> list[str]:
        feature = self.feature(ctx)
        lines = [
            "## Scope",
            f"This task has one feature: {feature['id']} ({feature['description']}). "
            "Work on only this one feature in this session.",
            "The feature list is feature_list.json (read it with read_file). "
            f"{FEATURE_LIST_REASON}: it sets the passes field itself, with evidence, after you "
            'call finish with claim="done" and the checks pass. It is unacceptable to remove or '
            "edit tests because this could lead to missing or buggy functionality.",
            "Files you may change in each phase:",
        ]
        for phase in ctx.spec.phases:
            allowed = ctx.spec.allowed_paths.get(phase)
            listed = ", ".join(allowed) if allowed is not None else "(no list given)"
            lines.append(f"- {phase}: {listed}")
        if "state" in ctx.spec.layers:
            lines.append("- any phase: progress.md, session-handoff.md, docs/exec-plans/**")
        lines.append(
            "A patch that touches any other file is rejected before it is applied. Changes that "
            "a command makes to any other file are reverted after it runs."
        )
        return ["\n".join(lines)]
```

Three things to notice:

- A2's strongly worded sentence is passed to the agent word for word: "It is unacceptable to remove
  or edit tests because this could lead to missing or buggy functionality." (A2, F-a-80).
- The agent is told the consequence before it acts: a patch outside the list is rejected and a
  command's changes are reverted. A1 writes lint error messages "to inject remediation instructions
  into agent context" (A1, F-a-97); the same idea applies here, before the first error.
- The bare arm reads the same scope in the ticket text. The difference between the arms is not what
  they are told; it is that the harness arm's scope is checked.

## 2. How a tool call is checked

`src/shipharness/harness/scope/layer.py`, lines 153-188.

```python
    def before_tool(self, ctx: LayerContext, call: ToolCall) -> HarnessDecision:
        if call.name not in WATCHED_TOOLS:
            return HarnessDecision.allow(self.name)
        if call.name == "apply_patch":
            targets = patch_targets(str(call.arguments.get("patch", "")))
            refused = check_paths(self.rules(ctx), targets)
            if refused:
                parts = self._decisions("block", refused, ctx, "patch not applied")
                return HarnessDecision(
                    kind="block",
                    layer=self.name,
                    message=" | ".join(d.message for d in parts),
                    paths=sorted({p for d in parts for p in d.paths}),
                    data={"phase": ctx.phase},
                )
        self._baseline = (call.call_id, snapshot.take(ctx.workspace))
        return HarnessDecision.allow(self.name)

    def after_tool(
        self, ctx: LayerContext, call: ToolCall, result: ToolResult
    ) -> list[HarnessDecision]:
        baseline, self._baseline = self._baseline, None
        if call.name not in WATCHED_TOOLS or baseline is None or baseline[0] != call.call_id:
            return []
        before = baseline[1]
        changed = snapshot.changed(before, snapshot.take(ctx.workspace))
        refused = check_paths(self.rules(ctx), changed)
        if not refused:
            return []
        problems = snapshot.restore(ctx.workspace, before, [p for v in refused.values() for p in v])
        decisions = self._decisions("revert", refused, ctx, "change reverted")
        if problems:
            decisions[-1] = decisions[-1].model_copy(
                update={"data": {**decisions[-1].data, "problems": problems}}
            )
        return decisions
```

- **Two checks, two moments.** A patch is checked before it is written, because the harness can read
  its target paths. A shell command cannot be read that way (any command can write any file), so it
  is checked afterwards, against a byte snapshot taken just before it ran.
- **All paths of a patch.** `patch_targets` collects every path a unified diff can touch, including
  `diff --git` lines, renames, and copies, so a rename into `app/api/middleware.py` is caught too.
- **Restore, not git.** The revert uses the snapshot module, which reads bytes, never follows links,
  and refuses paths that leave the workspace (`src/shipharness/harness/scope/snapshot.py`). A2 used git
  so that the model could "revert bad code changes" (A2, F-a-57); here the harness reverts, and it does
  not depend on the agent's git state.
- **The reasons are grouped.** `check_paths` groups refused paths by reason, so one patch that
  touches three out-of-scope files gives one decision that names all three.

The harness turns each `block` or `revert` decision into a `blocked` event with `phase`, `paths`,
`action`, and `reason` (`src/shipharness/harness/base.py`), which is what the console's diff map and
turn flags show.

## 3. What counts as evidence for `passes`

`src/shipharness/harness/scope/status.py`, lines 67-81: the evidence when the verify layer is off,
as in `make demo-3`.

```python
def _visible_tests_evidence(ctx: LayerContext, timeout_s: int) -> tuple[dict[str, Any] | None, str]:
    run = ctx.sandbox.exec(VISIBLE_TESTS_COMMAND, timeout_s)
    summary = summarise_pytest(run.output).splitlines()[0]
    match = _COUNTS.match(summary)
    passed, failed, errors = (int(n) for n in match.groups()) if match else (0, 0, 0)
    if run.exit_code != 0 or failed or errors or passed == 0:
        return None, f"the visible tests did not pass ({summary}, exit {run.exit_code})"
    total = f"{passed}/{passed + failed + errors}"
    return {
        "gate_id": "visible-tests",
        "commit": git.head_sha(ctx.workspace),
        "visible": total,
        "existing": "not run (verify layer off)",
        "checks": [],
    }, ""
```

The harness runs the visible suite itself, in the arm's container, after the agent's done claim. It
does not read the agent's own test output. Zero passing tests is not evidence. The evidence records
the commit it was taken at, so a reviewer can check out exactly what was tested. With the verify layer
on (demo-4 and the final), `_gate_evidence` uses the verify gate's result instead and records which
house-rule checks passed ("house rules" is the course's label for what A1 calls "golden
principles", A1 F-a-99).

How this compares with A2:

| | A2 | shipharness |
|---|---|---|
| Who writes the feature list | The initializer agent (A2, F-a-78) | Harness code before the first session (course design) |
| Who changes `passes` | The coding agent, "only by changing the status of a passes field" (A2, F-a-79), after "careful testing" (A2, F-a-108) | `status.py` only; the agent may not edit the file (course design) |
| What `passes: true` rests on | The agent's own testing | A visible-test run or a verify gate the harness ran, recorded in `evidence` with the commit |
| Extra fields | none | `evidence`, `testedAt` (course design) |

The source basis for moving the decision is A3: "Separating the agent doing the work from the agent
judging it proves to be a strong lever to address this issue." (A3, F-a-110).

## 4. How the referee counts the S3 measure

`src/shipharness/ab/referee.py`, lines 513-526.

```python
        product = strip(diff)  # harness artifacts are state, not product changes
        patch = rdir / "product.patch"
        patch.write_bytes(product)
        apply_error = _apply(build, patch)
        restore_judge_config(build, config)  # the arm never configures how it is judged
        paths = [p for p in diff_paths(product) if p != "/dev/null"]
        allowed = self.task.allowed_paths
        scope_globs = [*allowed.get("build", []), *allowed.get("test", [])]
        out_of_scope = [p for p in paths if scope_globs and not _allowed(p, scope_globs)]
        phase_edits = [
            p
            for p in (test_phase_files or [])
            if not is_harness_artifact(p) and allowed and not _allowed(p, allowed.get("test", []))
        ]
```

The test-phase files come from `phase_changed_files` in `src/shipharness/ab/demo.py`, lines 441-452:

```python
def phase_changed_files(
    spec: AgentRunSpec, result: AgentRunResult, *, store: Path | None = None
) -> list[str]:
    """Files the arm changed during the test phase (the S3 measure's second half). With
    working-tree snapshots (`store`): the change from the first test session's start tree to the
    last test session's end tree, so build-phase work the arm never committed is not counted.
    Without them: the working tree against the commit at the start of the test phase."""
    tests = [s for s in result.sessions if s.phase == "test"]
    if store is not None and tests and all(s.start_tree and s.end_tree for s in tests):
        return git.tree_changed_files(store, tests[0].start_tree, tests[-1].end_tree)
    shas = result.phase_shas.get("test")
    return git.changed_files(spec.workspace, shas[0]) if shas else []
```

- The referee never uses the scope layer's decisions. It judges the shipped diff, the same way for
  both arms.
- Harness artifacts (`AGENTS.md`, `progress.md`, `feature_list.json`, and the rest of the list in
  `src/shipharness/ab/artifacts.py`) are stripped first, so the harness arm is not charged for its own
  state files.
- A file is in scope if either phase allows it. The test-phase rule is separate: a file changed after
  the test phase started must match the test list.
- The test-phase files are the difference between two working-tree snapshots: the start of the first
  test session and the end of the last one. A source edit that the agent made and undid within the
  test phase leaves no trace and is not counted.
- The snapshot version is a pilot fix. The first version compared the working tree with the commit
  at the start of the test phase, so an arm that never committed its build work had that work
  counted as test-phase source edits: in the course pilot's run 1 (2026-10-16, before the
  measurement fixes) the bare arms' `app/api/issues.py` and `app/services/issues.py` were counted
  that way. Pilot run 1 also counted 4 files of the import linter's cache (`.import_linter_cache/`) as
  out of scope in every F3 arm. Both fixes apply to both arms; the measure itself did not change.

## Try it without a model call

```bash
uv run python scripts/anchors.py extract S3:allowed_paths
```

The unit tests in `tests/unit/harness_scope/` drive the guard, the snapshot revert, the status
writer, and the layer with a fake sandbox; reading `test_layer.py` next to this piece shows each rule
as a test.

## Why it matters for your own repo

- **Check after the command, not only before.** A patch can be read before it is applied; a shell
  command cannot. If your agent can run commands, a pre-check on patches alone leaves the larger
  door open. A byte snapshot before each command and a comparison after it is the cheap way to
  close it.
- **Keep a generated-files list next to the allowed paths.** Linters, test runners, and type checkers
  write caches. In the pilot, a missing entry for one cache folder turned every F3 run into a
  failure. Write the list once, use it in the scope check, the diff, and the clean-state check, as
  shipharness now does.
- **Measure from snapshots, not from commits.** Agents do not commit on a schedule. A measure that
  reads `HEAD` charges an arm for when it committed, not for what it changed.
- **Tell the agent the consequence first.** The scope block says what is refused and reverted before
  the first tool call, in the spirit of A1's error messages that "inject remediation instructions into
  agent context" (A1, F-a-97).

## Sources

- A1: Ryan Lopopolo, OpenAI, "Harness engineering: leveraging Codex in an agent-first world",
  2026-02-11. https://openai.com/index/harness-engineering/
- A2: Justin Young, Anthropic, "Effective harnesses for long-running agents", 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- A3: Prithvi Rajasekaran, Anthropic, "Harness design for long-running application development",
  2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps
