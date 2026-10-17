# Fallbacks and showcases: recorded runs and replay

What is recorded, where it lives, how to replay it with the RECORDING badge, and what to say. Two
kinds of recordings are used in class:

- **Showcases** ("real run, replayed"): one named pilot run per section, replayed in every demo
  block on purpose (VERIFICATION.md, "Class plan per section").
- **Fallbacks**: one recording per class command (`make show-1` to `make show-4`, `make final` per
  feature), replayed only when the live run failed for a reason outside the experiment.

The short version is in [run-sheet.md](run-sheet.md#replay-procedure).

---

## Rules

- A recording is always labelled. Replays show a red ● RECORDING badge on every screen (DESIGN §13);
  say "real run, replayed" (showcase) or "recorded before class" (fallback) out loud as well.
  Unlabelled recordings are forbidden (DESIGN §8.3).
- A replay applies the recorded diffs and runs the referee live (DESIGN §13). The agent part is
  recorded; the judging is not.
- No cherry-picking of fallbacks. For each command, the fallback is the first complete run recorded
  with the class profile, whatever its result. A recording that ended in `ERROR` for an
  infrastructure reason (for example Docker stopped) is kept and listed, and the next complete run is
  recorded as well. The showcases were chosen for what they teach, and each is introduced with the
  run it came from and the pilot result it sits in, so the room can weigh it (the all-results slide).
- Use a fallback only when the live run failed for a reason outside the experiment (Docker, network,
  OpenAI errors, time). A live run with an unwelcome result is a result, not a failure: show it.

---

## What a recording is

A recording is a run directory written by `shipharness ab` (`make show-N`, `make demo-N`, `make
final`) under `RUNS_DIR`, default `.shipharness/runs/` (`src/shipharness/config/settings.py`; the
folder is git-ignored), plus the score exports the referee wrote.

| Path | Contents | Needed by |
|---|---|---|
| `.shipharness/runs/<id>/events.jsonl` | The full run log: every event of the arms and the referee (CONTRACTS §8) | Replay (re-emitted with `recorded=True`) |
| `.shipharness/runs/<id>/ab.json` | Task, seed, section, `checkpoint_sha`, the arms' specs and results, `single_arm` for a show-N run, paths of the diffs and session patches (`write_ab_record` in `src/shipharness/ab/demo.py`) | Replay and swap |
| `.shipharness/runs/<id>/<arm>/diff.patch` | What the arm shipped | Replay and swap |
| `.shipharness/runs/<id>/<arm>/sessions/session-<n>.patch` | One patch per session (continuity check, S2) | Replay and swap |
| `.shipharness/runs/<id>/screenshots/<arm>/*.png` | Board screenshots (screen 2) | Only the original run (see the screenshot gap below) |
| `exports/scores/<run id>.json` | One score record per arm | Swap test; screen 4 |

A show-N recording holds the harness arm only (`single_arm` in `ab.json`). `make replay` replays it;
the swap test refuses it (`x <id> is a single-arm run (harness in action): the swap test needs both
arms; pass the id of an A/B`, `src/shipharness/ab/recorded.py`).

Replay and swap export the checkpoint from the commit recorded in `ab.json` (`checkpoint_sha`), never
from the tag name (CONTRACTS §22). The checkpoint tags were moved on 2026-10-17 with the owner's
approval; the old commits stay reachable under `refs/archive/checkpoints-2026-10-16/<tag>`, so the
pilot's recorded `checkpoint_sha` values still resolve (VERIFICATION.md, change 15).

The recordings are not in the repository. On a class host other than the machine that ran the pilot,
copy each run directory and its score records from that machine to the same paths.

---

## The showcases ("real run, replayed")

| Section | Command | Recorded run | What the referee found |
|---|---|---|---|
| S1 | `make replay RUN=ab-20261016-212252-aa1644` | Pilot run 3, F4 canonical, effort medium | Harness arm: 3 new R1 violations, hidden tests 27 of 69 (a broken change) (VERIFICATION.md, "Run 3") |
| S2 | `make replay RUN=ab-20261016-213317-9a0ec1` | Pilot run 3, F2 with session budget 12, 38 | Harness arm: `finish(claim="not_done")` at the end of the 12-turn session 1 ended the build phase; the 38-turn session never ran; hidden tests 3 of 56. The runner fix for both arms is change 14 |
| S3 | `make replay RUN=ab-20261016-214151-ca9841` | Pilot run 3, F4 canonical | Bare arm: 2 files outside the allowed paths; harness arm (all four layers): 0. In the harness arm the agent time limit cut the test session to 7 turns |
| S4 | `make replay RUN=ab-20261017-090903-926c02` | Class-profile round, F4 canonical, class profile | Bare arm: claimed done, hidden 68 of 69, mutants 4 of 4: primary measure fails. Harness arm: hidden 68 of 69, mutants 1 of 4, test phase ended by the agent time limit; `shipharness ab` exited 2 |

Check each once before class (T-1): `make replay RUN=<id> PURPOSE=pilot`. The referee is
deterministic for a given build (VERIFICATION.md, "Referee determinism check"), so the replay's
verdict should match the recording's.

[[CAPTURE: wall time and result lines of make replay for each showcase id above | how: time make replay RUN=<id> PURPOSE=pilot]]

---

## The fallbacks: how to record them (before class, not on the class date)

Make the recordings on the class host, inside WSL2, on a day other than the class date, with
`PURPOSE=pilot`: the class session cost cap is keyed by `SHIPHARNESS_CLASS_DATE` (DESIGN §11.1), and
pilot-purpose runs trace to `shipharness-pilot`, not the class project.

1. `make doctor` passes; `make warm` ends with `warm: done`.
2. Run each section's live command once, in order: `make show-1 PURPOSE=pilot` to `make show-4
   PURPOSE=pilot`.
3. Run each final feature once, because the poll can pick any of them: `make final FEATURES=F5
   PURPOSE=pilot`, then `F6`, then `F7`.
4. For each command, copy the id from the first result line (`A/B <id> (<feature>, layers=[...],
   profile=class...)`) into the table below, with the date and the per-arm status.
5. Check each recording once: `make replay RUN=<id> PURPOSE=pilot` (no model calls: the replay runs
   without the reviewer by default).
6. Back them up outside the repository: `mkdir -p ~/shipharness-fallbacks && cp -a
   .shipharness/runs/<id> ~/shipharness-fallbacks/` and `cp exports/scores/<run id>.json
   ~/shipharness-fallbacks/` for each arm's run id (in `ab.json` under `arms.<arm>.spec.run_id`). To
   restore, copy them back to the same paths.
7. Record the ids, costs, and times in VERIFICATION.md.

Cost at the caps: $0.24 per show-N run (one arm plus its review) and $0.58 per final feature. In the
class-profile round the harness arms cost $0.0135 to $0.0357 and their reviews $0.0028 to $0.0041
(VERIFICATION.md, "Class-profile round").

## Recorded runs

The course's recordings of `make show-1` to `make show-4` and `make final FEATURES=F5` are the
class-profile runs made on 2026-10-17:

[[CAPTURE: run id, per-arm status line, Cost line, and date of make show-1, make show-2, make show-3, make show-4, and make final FEATURES=F5 (class profile, PURPOSE=pilot) | how: make show-1 PURPOSE=pilot (and show-2, show-3, show-4); make final FEATURES=F5 PURPOSE=pilot]]

| Section | Command | Recorded |
|---|---|---|
| S1 | `make show-1 PURPOSE=pilot` | the class-profile run above |
| S2 | `make show-2 PURPOSE=pilot` | the class-profile run above |
| S3 | `make show-3 PURPOSE=pilot` | the class-profile run above |
| S4 | `make show-4 PURPOSE=pilot` | the class-profile run above |
| Final F5 | `make final FEATURES=F5 PURPOSE=pilot` | the class-profile run above |
| Final F6 | `make final FEATURES=F6 PURPOSE=pilot` | not recorded yet: record it on T-1 (steps above) |
| Final F7 | `make final FEATURES=F7 PURPOSE=pilot` | not recorded yet: record it on T-1 (steps above) |

There is no opening board screenshot to record: no pilot or class-round run leaked another org's
cards (VERIFICATION.md, "Class-profile round"). The ⚠ marks are shown by S1's constructed example.

---

## How to replay in class

1. Say the replay line (below) first.
2. Terminal B: `make replay RUN=<id>` (the Makefile runs `uv run shipharness replay <id> --purpose
   class`; an A/B id or a run id works).
3. Reload the console's runs list (`http://127.0.0.1:8765/`) and open the newest `ab-...` entry. That
   is the replay, under a new id; the recording itself is not changed.
4. What the console shows: the recorded events arrive at once, so screens `1`, `3`, and `5` show the
   finished run immediately, each with the RECORDING badge. Then the referee judges the recorded diffs
   live, and its counters and results appear on screen `3` as it goes.
5. What the terminal prints at the end: `RECORDING: replay <new ab id> of <recorded ab id> (<n>
   events)`, one result line per arm, and the cost line.
6. Screen `4` includes replay dots and says how many there are ("<n> runs are replays (recorded).");
   `uv run shipharness report` leaves replays out unless `--include-recorded` is passed
   (`src/shipharness/ab/commands.py`).

### Screenshot gap (screen 2 in a replay)

`replay_ab` copies each arm's `diff.patch` into the new run directory but not the `screenshots/`
folder, while the replayed `screenshot` events point at paths inside the run directory
(`src/shipharness/ab/recorded.py`, `src/shipharness/console/preview.py`). Screen `2` of a replay
therefore shows broken images. Copy the folder once the replay's directory exists and reload the page
(Ctrl+R; the `F` key is the console's full-screen toggle):

```
cp -a .shipharness/runs/<recorded ab id>/screenshots .shipharness/runs/<replay ab id>/
```

### If Docker itself is down

A replay runs the referee in a container, so it needs Docker too. Last resort: open the recording
directly at `http://127.0.0.1:8765/run/<recorded ab id>`. These are the original events, so the console
shows **no** RECORDING badge: put the "recorded before class" slide up and say it before switching
screens. Do not switch to `SANDBOX_MODE=none` for class results; every screen would show
"UNSANDBOXED — results not official" (DESIGN §9). The constructed examples (`make example-N`) run
scripted steps with no model; they remain available while OpenAI is unreachable.

---

## What to say

**Showcase.** "Real run, replayed: this is <run id> from the course pilot. The agent's turns are
recorded; the referee is judging its code live, right now. Every screen says RECORDING. It is one run;
the all-results slide shows where it sits."

**Fallback.** "The live run stopped for a reason that has nothing to do with the harness: <Docker /
the network / the API / time>. Here is the same command recorded before class on this machine, run
<id>. The agent's turns are recorded; the referee is judging its code live. Every screen says
RECORDING."

**While it judges.** Use the section's screen notes in [run-sheet.md](run-sheet.md); they apply
unchanged, because the screens are built from the same events. Add: "The referee is deterministic for
a given build, so it should reach the same verdict as on the day it was recorded" (DESIGN §8.3 rule
10).

**If the replay's verdict differs from the recording's.** Say it: the referee is meant to be
identical on re-runs of the same code. Note the run ids and fields, and report them after class.

**After it.** "One recorded run is one dot." Then continue with the section's results as planned.
