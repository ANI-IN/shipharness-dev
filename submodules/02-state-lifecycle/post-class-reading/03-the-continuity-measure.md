# Reading the S2 measure: what `continuity_failure` sees and what it misses

Reading time: about 10 minutes.

Every pilot run gives one dot per arm for `continuity_failure`. Before you trust a dot, know how it is
computed. This piece walks through the referee's continuity check and the host code that feeds it,
shows a measurement bug the pilot found in it, and lists the cases the measure does not catch. The
measure itself was registered before any run (course design); nothing here changes it.

## The three parts

`src/shipharness/checks/continuity.py` fails a run if any of:

- (a) house rule R7 fails ("house rules" is the course's label for what A1 calls "golden
  principles", F-a-99): migration heads are not exactly one, or a fresh `alembic upgrade head`
  fails (it reuses `migration_findings` from the R7 check);
- (b) two migration files contain `create_table("<same name>")`;
- (c) 30% or more of the lines added in session 1 are removed in session 2.

Part (c) is the only part that needs the session history. Its core (`continuity.py`, lines 46-55):

```python
def redone_pct(session_1: str, session_2: str) -> float:
    """Share of session-1 added lines that session 2 removes (same file, same text)."""
    added, removed = _lines_by_file(session_1, "+"), _lines_by_file(session_2, "-")
    total = sum(sum(c.values()) for c in added.values())
    if total == 0:
        return 0.0
    redone = sum(
        sum((lines & removed.get(path, Counter())).values()) for path, lines in added.items()
    )
    return round(100.0 * redone / total, 1)
```

`_lines_by_file` collects non-blank added or removed lines per file, stripped of leading and trailing
spaces, as multisets (`Counter`). The `&` keeps, per file, the lines that session 1 added and
session 2 removed with the same text.

## Where the session patches come from

The patches are written on the host after the run (`src/shipharness/ab/demo.py`, lines 481-505):

```python
def session_patches(
    spec: AgentRunSpec, result: AgentRunResult, out_dir: Path, *, store: Path | None = None
) -> list[Path]:
    """One patch per session (for the continuity check). With working-tree snapshots (`store`),
    each patch is the change between the session's start and end trees, so an arm that never
    commits is measured like one that does. Without them: committed changes between the session's
    start and end commits, and the last session also includes uncommitted work."""
    patches: list[Path] = []
    sessions = list(result.sessions)
    if store is not None and sessions and all(s.start_tree and s.end_tree for s in sessions):
        for session in sessions:
            out = out_dir / f"session-{session.index}.patch"
            written = git.write_tree_diff(store, session.start_tree, session.end_tree, out)
            if written is not None:
                patches.append(written)
        return patches
    for position, session in enumerate(result.sessions):
        out = out_dir / f"session-{session.index}.patch"
        if position == len(result.sessions) - 1:
            written = git.write_diff(spec.workspace, session.start_sha, out)
        else:
            written = git.write_range_diff(spec.workspace, session.start_sha, session.end_sha, out)
        if written is not None:
            patches.append(written)
    return patches
```

The snapshot path is the normal one in an A/B. It exists because of pilot run 1: the bare arms never
committed, so commit-based patches left session 1's work out of part (c) entirely (found in the
course pilot, run 1, 2026-10-16, which ran before the measurement fixes). `result.sessions` holds
every session of the run, build and test phases together, in order. The check uses the first two
patches.

Before the check, the referee hands it copies with harness artifacts removed
(`src/shipharness/ab/referee.py`, lines 267-277):

```python
def _product_sessions(patches: list[Path], out_dir: Path) -> list[Path]:
    """Copies of the per-session patches without harness artifacts, for the continuity check.
    The state layer rewrites progress.md and the handoff every session; those are not product
    work (M6 pilot run 2: they read as session 2 removing session 1's lines)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    copies: list[Path] = []
    for index, patch in enumerate(patches, start=1):
        copy = out_dir / f"session-{index}.patch"
        copy.write_bytes(strip(patch.read_bytes()) if patch.is_file() else b"")
        copies.append(copy)
    return copies
```

`strip` is `strip_harness_artifacts` from `src/shipharness/ab/artifacts.py`; its pattern list includes
`init.sh`, `progress.md`, `session-handoff.md`, and `docs/exec-plans/**` for the state layer.

## A measurement bug the pilot found

Until that function existed, the check read the raw patches. In the course pilot's run 2 (2026-10-16)
every F2 harness arm failed part (c): session 1 added only `progress.md`, `session-handoff.md`, and
the exec plan, and session 2 rewrote them. The score records show the three `redone_lines_pct`
values: 84.0 (`r-20261016-181736-260803`), 76.5 (`r-20261016-184318-fdee0c`), and 50.0
(`r-20261016-190548-9352c4`) (captured on 2026-10-16 from `exports/scores/<run id>.json`, runs as
listed; your output will differ). The bare arms in the same A/Bs scored 2.1, 0.0, and 0.0.

The arithmetic was right and the harness did what it was built to do: the wrap-up asks the agent to
rewrite its notes, and the state layer rewrites the machine summary at every stop. The check simply
counted the treatment's own bookkeeping as product work. The fix is labelled "bug fix,
applies to both arms": the bare arm has no such files, so its numbers cannot move, and the primary
measure's definition is unchanged. The run 2 harness dots stay in the record as they were scored, with
the bug named next to them.

Two habits this teaches. Read the per-run detail behind a surprising dot before reading the total:
here the session patches named the files. And when a measure compares two arms, check that nothing
one arm writes for its own use can reach the measure; the shipped diff already had this filter, the
session patches did not.

## Cases to keep in mind

| Case | What the measure does |
|---|---|
| Session 1 leaves its work uncommitted | Counted: the snapshot patches compare working trees, so uncommitted lines are in session 1's patch. Without snapshots, the commit-based fallback would leave them out |
| Session 2 moves code to another file | Removal is matched per file and per line text, so lines moved to a new file count as removed only from the old file; lines rewritten with different text in the same place count as removed |
| Session 2 reformats lines | Leading and trailing spaces are stripped before matching, so re-indenting alone does not count as redone if the text is unchanged; any other text change does |
| The build phase ends in one session | After `finish(claim="done")` in session 1 no stop happens. Patch 2 is then the test phase's session, which also starts with an empty context (`runner/loop.py`), so (c) compares the build session with the test session. Until a runner fix after pilot run 4, `finish(claim="not_done")` ended the build phase too: pilot run 2 had one such arm (`r-20261016-184318-fdee0c`), runs 3 and 4 had six. Since the fix, it ends only that session, for both arms |
| The harness writes between sessions | The state layer's files are stripped before the check; a harness that wrote product files between sessions would still be counted |
| Session 1 writes only harness files, or nothing | After stripping, session 1 has no added lines, `redone_pct` returns 0.0, and (c) passes; (a) and (b) still judge the migrations. In pilot runs 3 and 4 six arms passed this way while building nothing (3 of 56 hidden tests): a pass is not a built feature |
| The second migration has a different table name | (b) does not fire; (a) fires only if the history now has two heads or fails to upgrade |

None of these favour one arm: both arms go through the same code. They do mean a single dot can be a
near miss, which is one reason the course reports runs out of k and shows the components next to the
primary measure.

## The console's "redone" marker is not part (c)

Screen 3's session timeline marks a file "redone" when a session changes a file that an earlier
session also changed (`src/shipharness/console/state.py`, `ArmState.sessions`, lines 246-263):

```python
    def sessions(self) -> list[SessionSummary]:
        summaries: dict[int, SessionSummary] = {}
        seen: set[str] = set()
        for row in self.timeline:
            summary = summaries.setdefault(row.session_index, SessionSummary(row.session_index))
            if row.kind != "turn":
                continue
            summary.turns += 1
            for tool in row.tools:
                for path in tool.files_changed:
                    if path not in summary.files:
                        summary.files.append(path)
        for index in sorted(summaries):
            summary = summaries[index]
            summary.ended_by = self._session_ends.get(index, "")
            summary.redone = [p for p in summary.files if p in seen]
            seen.update(summary.files)
        return [summaries[i] for i in sorted(summaries)]
```

That is a live, file-level hint from tool events while the run is going. Continuing work on the same
file in session 2 is normal and also gets the marker, and the harness arm's own `progress.md` gets it
in every session. The judged number is `redone_lines_pct` from the referee, shown on screen 4 after
the run.

## Other stop points

The dataset has session-stop variants of F2 that move the stop
(`datasets/teamtrack-features-v1.jsonl`, `metadata.group` `session_stop`):

| Example | `session_budget` | First-session share |
|---|---|---|
| F2-canonical | [20, 30] | (canonical) |
| F2-stop-1 | [13, 37] | 0.25 |
| F2-stop-2 | [25, 25] | 0.5 |
| F2-stop-3 | [38, 12] | 0.75 |

A stop after a quarter of the turns tests whether session 2 can start from very little; a stop at
three quarters tests whether a nearly finished feature survives. These variants belong to the
course's full-dataset batch set (60 tasks, two arms, k=2), which was not run because the
pre-registered pilot gate did not pass. `uv run shipharness report` groups dots by feature and measure
(`src/shipharness/ab/report.py`), so runs of these variants would appear among the F2 dots; each score export
(`exports/scores/<run_id>.json`) carries its `variant`, which is how to separate them.

Pilot runs 3 and 4 and the class-profile round use a fifth split that is not a dataset line: F2
canonical with `--session-budget 12,38`, an override of the task's budget for one run (registered
before run 3); the class uses it too. Its score records
carry `variant` `canonical`, so keep the A/B ids of such runs if you compare them with the dataset's
dots.

## Why it matters for your own repo

If your agent's work spans sessions, the question "did a later session redo or break earlier work?"
can be answered from the repository, without trusting the agent's notes:

1. List the facts that would show it. For a schema: heads and duplicate tables. For an API: maybe
   duplicate routes. For a library: a public function defined twice.
2. Compute them from git and the build alone. The referee here never reads `progress.md` or the
   handoff; it reads the build and the diffs.
3. Keep your harness's own files out of the comparison, and test that with an arm that writes
   nothing but those files. That test would have caught the pilot's bug before a run.
