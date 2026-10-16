# The scope layer, line by line

Reading time: about 10 minutes.

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
house-rule checks passed.

How this compares with A2:

| | A2 | shipharness |
|---|---|---|
| Who writes the feature list | The initializer agent (A2, F-a-78) | Harness code before the first session (DESIGN D-11) |
| Who changes `passes` | The coding agent, "only by changing the status of a passes field" (A2, F-a-79), after "careful testing" (A2, F-a-108) | `status.py` only; the agent may not edit the file (DESIGN D-14) |
| What `passes: true` rests on | The agent's own testing | A visible-test run or a verify gate the harness ran, recorded in `evidence` with the commit |
| Extra fields | none | `evidence`, `testedAt` (course design, RESEARCH G-6) |

The source basis for moving the decision is A3: "Separating the agent doing the work from the agent
judging it proves to be a strong lever to address this issue." (A3, F-a-110).

## 4. How the referee counts the S3 measure

`src/shipharness/ab/referee.py`, lines 449-462.

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

The test-phase files come from `phase_changed_files` in `src/shipharness/ab/demo.py`:

```python
def phase_changed_files(spec: AgentRunSpec, result: AgentRunResult) -> list[str]:
    """Files the arm changed during the test phase (the S3 measure's second half)."""
    shas = result.phase_shas.get("test")
    return git.changed_files(spec.workspace, shas[0]) if shas else []
```

- The referee never uses the scope layer's decisions. It judges the shipped diff, the same way for
  both arms (DESIGN §8.3, rule 1).
- Harness artifacts (`AGENTS.md`, `progress.md`, `feature_list.json`, and the rest of the list in
  `src/shipharness/ab/artifacts.py`) are stripped first, so the harness arm is not charged for its own
  state files (DESIGN D-18).
- A file is in scope if either phase allows it. The test-phase rule is separate: a file changed after
  the test phase started must match the test list.
- `git.changed_files` compares the working tree at the end of the run with the commit at the start of
  the test phase, untracked files included. A source edit that the agent made and undid within the
  test phase leaves no trace and is not counted.

## Try it without a model call

```bash
uv run python -m pytest -q -p no:cacheprovider tests/unit/harness_scope
uv run python scripts/anchors.py extract S3:allowed_paths
```

The unit tests in `tests/unit/harness_scope/` drive the guard, the snapshot revert, the status
writer, and the layer with a fake sandbox; reading `test_layer.py` next to this piece shows each rule
as a test.

## Sources

- A1: Ryan Lopopolo, OpenAI, "Harness engineering: leveraging Codex in an agent-first world",
  2026-02-11. https://openai.com/index/harness-engineering/
- A2: Justin Young, Anthropic, "Effective harnesses for long-running agents", 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- A3: Prithvi Rajasekaran, Anthropic, "Harness design for long-running application development",
  2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps
