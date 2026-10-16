# Reading the S2 measure: what `continuity_failure` sees and what it misses

Reading time: about 8 minutes.

In class you see one dot per run for `continuity_failure`. Before you trust a dot, know how it is
computed. This piece walks through the referee's continuity check and the host code that feeds it,
and lists the cases the measure does not catch. The measure itself was registered before any run
(DESIGN §8.2); nothing here changes it.

## The three parts

`src/shipharness/checks/continuity.py` fails a run if any of:

- (a) house rule R7 fails: migration heads are not exactly one, or a fresh `alembic upgrade head`
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

The patches are written on the host after the run, from the commits the runner recorded at each
session's start and end (`src/shipharness/ab/demo.py`, lines 458-470):

```python
def session_patches(spec: AgentRunSpec, result: AgentRunResult, out_dir: Path) -> list[Path]:
    """One patch per session (for the continuity check): committed changes between the session's
    start and end commits; the last session also includes uncommitted work."""
    patches: list[Path] = []
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

`result.sessions` holds every session of the run, build and test phases together, in order. The
check uses the first two patches.

## Cases to keep in mind

| Case | What the measure does |
|---|---|
| Session 1 leaves its work uncommitted | Session 1's patch has only committed changes, so its uncommitted lines are not in the denominator. The work stays on disk and shows up in a later patch. Committing at the end of a session is in both arms' prompt ("Commit your work to git with descriptive messages", `runner/prompts.py`), but the measure depends on it |
| Session 2 moves code to another file | Removal is matched per file and per line text, so lines moved to a new file count as removed only from the old file; lines rewritten with different text in the same place count as removed |
| Session 2 reformats lines | Leading and trailing spaces are stripped before matching, so re-indenting alone does not count as redone if the text is unchanged; any other text change does |
| The build phase ends in one session | No stop happens. Patch 2 is then the test phase's session, which also starts with an empty context (`runner/loop.py`), so (c) compares the build session with the test session |
| The harness commits between sessions | `session_stop` commits the handoff and log after session 1's end commit is recorded and before session 2 starts, so those commits are in neither patch |
| The second migration has a different table name | (b) does not fire; (a) fires only if the history now has two heads or fails to upgrade |

None of these favour one arm: both arms go through the same code. They do mean a single dot can be a
near miss, which is one reason the course reports runs out of k and shows the components next to the
primary measure (DESIGN §8.2).

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
file in session 2 is normal and also gets the marker. The judged number is `redone_lines_pct` from the
referee, shown on screen 4 after the run.

## Other stop points

The dataset has session-stop variants of F2 that move the stop
(`datasets/teamtrack-features-v1.jsonl`, group "Session-stop variants", DESIGN §10.1):

| Example | `session_budget` | First-session share |
|---|---|---|
| F2-canonical | [20, 30] | (canonical) |
| F2-stop-1 | [13, 37] | 0.25 |
| F2-stop-2 | [25, 25] | 0.5 |
| F2-stop-3 | [38, 12] | 0.75 |

A stop after a quarter of the turns tests whether session 2 can start from very little; a stop at
three quarters tests whether a nearly finished feature survives. These variants run in the
full-dataset batch (DESIGN §10.4, batch 4, k=2). `make report` groups dots by feature and measure
(`src/shipharness/ab/report.py`), so these runs appear among the F2 dots; each score export
(`exports/scores/<run_id>.json`) carries its `variant`, which is how to separate them.

## Questions for your own harness

1. If your agent's work spans sessions, which repository facts would show that a later session redid
   or broke earlier work? For a schema, heads and duplicate tables; for an API, maybe duplicate routes.
2. Can you compute them from git and the build alone, without trusting the agent's own notes? The
   referee here never reads `progress.md` or the handoff; it reads the build and the diffs.
