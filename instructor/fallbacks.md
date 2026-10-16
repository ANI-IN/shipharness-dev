# Fallbacks: recorded runs and replay

What to do when a live run cannot be shown: which recordings exist, how they were made, where they
live, how to replay them with the RECORDING badge, and what to say. The short version is in
[run-sheet.md](run-sheet.md#replay-procedure).

Status: M11 draft. Recorded run ids and measured replay times are `[[PENDING]]` until the recordings
are made on the class host.

---

## Rules

- A recording is always labelled. Replays show a red ● RECORDING badge on every screen (DESIGN §13);
  say "recorded before class" out loud as well. Unlabelled recordings are forbidden (DESIGN §8.3).
- A replay applies the recorded diffs and runs the referee live (DESIGN §13). The agent part is
  recorded; the judging is not.
- No cherry-picking. For each section, the fallback is the first complete A/B recorded on the class
  host after the M6 pilot gate, whatever its result. Re-running until the bare arm fails is forbidden
  (DESIGN §8.3). A recording that ended in `ERROR` for an infrastructure reason (for example Docker
  stopped) is kept and listed, and the next complete A/B is recorded as well.
- Use a replay only when the live run failed for a reason outside the experiment (Docker, network,
  OpenAI errors, time). A live run that the bare arm or the harness arm "lost" is a result, not a
  failure: show it.

---

## What a recording is

A recording is an A/B directory written by `make demo-N` (or `make final`) under `RUNS_DIR`, default
`.shipharness/runs/` (`src/shipharness/config/settings.py`; the folder is git-ignored), plus the score
exports the referee wrote.

| Path | Contents | Needed by |
|---|---|---|
| `.shipharness/runs/<ab id>/events.jsonl` | The full run log: every event of both arms and the referee (CONTRACTS §8) | Replay (re-emitted with `recorded=True`) |
| `.shipharness/runs/<ab id>/ab.json` | Task, seed, section, `checkpoint_sha`, both arms' specs and results, paths of the diffs and session patches (`write_ab_record` in `src/shipharness/ab/demo.py`) | Replay and swap |
| `.shipharness/runs/<ab id>/<arm>/diff.patch` | What the arm shipped | Replay and swap |
| `.shipharness/runs/<ab id>/<arm>/sessions/session-<n>.patch` | One patch per session (continuity check, S2) | Replay and swap |
| `.shipharness/runs/<ab id>/screenshots/<arm>/*.png` | Board screenshots (screen 2) | Only the original run (see the screenshot gap below) |
| `exports/scores/<run id>.json` | One score record per arm | Swap test (compares with the original scores); screen 4 |

Experiment runs (`make experiments`) are not usable as fallbacks: each experiment run is a single-arm
run directory without `ab.json` (`src/shipharness/ab/experiments.py`), so `make replay` cannot load it.

Replay and swap export the checkpoint from the commit recorded in `ab.json` (`checkpoint_sha`), never
from the tag name (CONTRACTS §22). That commit must still exist in `~/shipharness`; checkpoint tags move
only with the owner's approval once results exist (DESIGN D-23).

---

## How to record them (before class, not on the class date)

Make the recordings on the class host, inside WSL2, on a day other than the class date: the session
cost cap is keyed by `SHIPHARNESS_CLASS_DATE`, which defaults to today (DESIGN §11.1).

1. `make doctor` passes; images are current (`make images` after any change to `sandbox/Dockerfile` or
   `src/`).
2. Run each section's demo once, in order: `make demo-1`, `make demo-2`, `make demo-3`, `make demo-4`.
3. Run each final feature once, because the poll can pick any of them: `make final FEATURES=F5`,
   `make final FEATURES=F6`, `make final FEATURES=F7`.
4. For each command, copy the A/B id from the first line of its output (`A/B <ab id> (<feature>,
   layers=[...])`) into the table below, with the date and the per-arm status line.
5. Check each recording once: `make replay RUN=<ab id>` (no model calls: the replay runs without the
   reviewer by default) and `make swap-N AB=<ab id>` (expect `judged measures identical`).
6. Back them up outside the repository, for example:
   `mkdir -p ~/shipharness-fallbacks && cp -a .shipharness/runs/<ab id> ~/shipharness-fallbacks/` and
   `cp exports/scores/<run id>.json ~/shipharness-fallbacks/` for both arms' run ids (they are in
   `ab.json` under `arms.<arm>.spec.run_id`). To restore, copy them back to the same paths.
7. Record the ids, costs, and times in VERIFICATION.md.

[[PENDING: cost and wall time of each recording command | source: M6 pilot | how: cost line and time of make demo-N and make final FEATURES=F5|F6|F7 on the class host]]

## Recorded runs

| Section | Command | A/B id | Bare arm status | Harness arm status | Recorded on |
|---|---|---|---|---|---|
| S1 | `make demo-1` | see marker below | | | |
| S2 | `make demo-2` | see marker below | | | |
| S3 | `make demo-3` | see marker below | | | |
| S4 | `make demo-4` | see marker below | | | |
| Final F5 | `make final FEATURES=F5` | see marker below | | | |
| Final F6 | `make final FEATURES=F6` | see marker below | | | |
| Final F7 | `make final FEATURES=F7` | see marker below | | | |

[[PENDING: recorded A/B id and per-arm status for demo-1 | source: M6 pilot | how: make demo-1 on the class host]]

[[PENDING: recorded A/B id and per-arm status for demo-2 | source: M6 pilot | how: make demo-2 on the class host]]

[[PENDING: recorded A/B id and per-arm status for demo-3 | source: M6 pilot | how: make demo-3 on the class host]]

[[PENDING: recorded A/B id and per-arm status for demo-4 | source: M6 pilot | how: make demo-4 on the class host]]

[[PENDING: recorded A/B ids and per-arm status for the final features F5, F6, F7 | source: M6 pilot | how: make final FEATURES=F5, then F6, then F7 on the class host]]

The opening's board screenshot (slide 2) comes from the S1 recording:
`.shipharness/runs/<S1 ab id>/screenshots/bare/board-<n>.png`, one with ⚠ other-org marks.

---

## How to replay in class

1. Say the replay line (below) first.
2. Terminal B: `make replay RUN=<recorded ab id>` (the Makefile runs `uv run shipharness replay
   <id>`; an A/B id or either arm's run id works).
3. Reload the console's runs list (`http://127.0.0.1:8765/`) and open the newest `ab-...` entry. That
   is the replay, under a new A/B id; the recording itself is not changed.
4. What the console shows: the recorded events arrive at once, so screens `1`, `3`, and `5` show the
   finished run immediately, each with the RECORDING badge. Then the referee judges the recorded diffs
   live, and its counters and results appear on screen `3` as it goes.
5. What the terminal prints at the end: `RECORDING: replay <new ab id> of <recorded ab id> (<n>
   events)`, one result line per arm, and the cost line.
6. Screen `4` includes replay dots and says how many there are ("<n> runs are replays (recorded).");
   `make report` leaves replays out unless `--include-recorded` is passed
   (`src/shipharness/ab/commands.py`).
7. The swap test works on the recording: `make swap-N AB=<recorded ab id>`.

[[PENDING: wall time of make replay for each recording (referee only) | source: M6 pilot | how: time make replay RUN=<id>]]

### Screenshot gap (screen 2 in a replay)

`replay_ab` copies each arm's `diff.patch` into the new run directory but not the `screenshots/`
folder, while the replayed `screenshot` events point at paths inside the run directory
(`src/shipharness/ab/recorded.py`, `src/shipharness/console/preview.py`). Screen `2` of a replay
therefore shows broken images. Until that is fixed, copy the folder once the replay's directory exists
and reload the page (Ctrl+R; the `F` key is the console's full-screen toggle):

```
cp -a .shipharness/runs/<recorded ab id>/screenshots .shipharness/runs/<replay ab id>/
```

### If Docker itself is down

A replay runs the referee in a container, so it needs Docker too. Last resort: open the recording
directly at `http://127.0.0.1:8765/run/<recorded ab id>`. These are the original events, so the console
shows **no** RECORDING badge: put the "recorded before class" slide up and say it before switching
screens. Do not switch to `SANDBOX_MODE=none` for class results; every screen would show
"UNSANDBOXED — results not official" (DESIGN §9).

---

## What to say

**Starting a replay.** "The live run stopped for a reason that has nothing to do with the harness:
<Docker / the network / the API / time>. Here is the same A/B recorded before class on this machine,
run <ab id>. The agents' turns are recorded; the referee is judging their code live, right now. Every
screen says RECORDING."

**While it judges.** Use the section's screen notes in [run-sheet.md](run-sheet.md); they apply
unchanged, because the screens are built from the same events. Add: "The referee is deterministic for
a given build, so it should reach the same verdict as on the night it was recorded" (DESIGN §8.3 rule
10).

**If the replay's verdict differs from the recording's.** Say it: that would break the pilot gate
condition that the referee is identical on re-runs of the same code. Note the run ids and fields, and
report them after class.

**After it.** "One recorded run is one dot. Here it is next to the experiment dots", then continue
with the section's results as planned.
