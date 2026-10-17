# Fallbacks and optional extras: recorded runs, replay, constructed examples

What is recorded, where it lives, how to replay it with the RECORDING badge, and what to say. Every
demo section of the class is live (VERIFICATION.md, "Class plan per section", revised 2026-10-17 under
owner message 7). This file holds everything that is not live, in two clearly separate groups:

- **Fallbacks**: one recording per class command (`make show-1` to `make show-4`, `make final` per
  feature), replayed only when the live run failed for a reason outside the experiment.
- **Optional extras** (not in the demo flow): the four real-mistake showcases from the pilot and the
  constructed examples (`make example-N`). They are listed for learners in `docs/extras.md` and are
  never part of a demo block, the run sheet's demo steps, or a demo README's main steps.

The short version of the replay is in [run-sheet.md](run-sheet.md#fallback-replay-procedure).

---

## Rules

- A recording is always labelled. Replays show a red ● RECORDING badge on every screen (DESIGN §13);
  say "recorded before class" out loud as well. Unlabelled recordings are forbidden (DESIGN §8.3).
- A replay applies the recorded diffs and runs the referee live (DESIGN §13). The agent part is
  recorded; the judging is not.
- No cherry-picking of fallbacks. For each command, the fallback is the first complete run of that
  exact command recorded with the class profile, whatever its result. A recording that ended in
  `ERROR` for an infrastructure reason (for example Docker stopped) is kept and listed, and the next
  complete run is recorded as well.
- Use a fallback only when the live run failed for a reason outside the experiment (Docker, network,
  OpenAI errors, time). A live run with an unwelcome result is a result, not a failure: show it.
- Never use an optional extra in place of a live run or a fallback. A constructed example is
  scripted; a showcase is a different run from a different task.

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

## The fallbacks: how to record them (before class, not on the class date)

Make the recordings on the class host, inside WSL2, on a day other than the class date, with
`PURPOSE=pilot`: the class session cost cap is keyed by `SHIPHARNESS_CLASS_DATE` (DESIGN §11.1), and
pilot-purpose runs trace to `shipharness-pilot`, not the class project.

1. `make doctor` passes; `make warm` ends with `warm: done`.
2. Run each section's live command once, in order, exactly as the class runs it: `make show-1
   PURPOSE=pilot`, `make show-2 SESSION_BUDGET=12,38 PURPOSE=pilot`, `make show-3 PURPOSE=pilot`,
   `make show-4 PURPOSE=pilot`.
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

On the machine that ran the pilot, each class command was first run once under load (VERIFICATION.md,
"Live command check under load", 2026-10-17 09:28-10:26 UTC) and then once more on a quiet machine
(the quiet runs, 2026-10-17, one command at a time, the source of the class timings in
[run-sheet.md](run-sheet.md#how-long-the-runs-take)). Under the rule above, the fallback is the first
complete run of the exact class command. The under-load `make show-2` ran the task's 20/30 budget,
not the class command `make show-2 SESSION_BUDGET=12,38`, so it cannot be the S2 fallback.

FALLBACK_TABLE

On another class host, record its own fallbacks on T-1 with the steps above; these ids are this
machine's.

There is no opening board screenshot to record: no pilot or class-round run leaked another org's
cards (VERIFICATION.md, "Class-profile round"). No real run produced ⚠ marks; they are covered by the
console tests, and the optional constructed example `make example-1` shows them (below).

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
"UNSANDBOXED — results not official" (DESIGN §9).

---

## Optional extras (not in the demo flow)

Listed here so the instructor can answer questions about them; learners find them in
`docs/extras.md`. None of them is shown in a demo block, and none is a result.

### The real-mistake showcases (replays of pilot runs)

| Section topic | Command | Recorded run | What the referee found |
|---|---|---|---|
| S1 | `make replay RUN=ab-20261016-212252-aa1644` | Pilot run 3, F4 canonical, effort medium | Harness arm: 3 new R1 violations, hidden tests 27 of 69 (a broken change) (VERIFICATION.md, "Run 3") |
| S2 | `make replay RUN=ab-20261016-213317-9a0ec1` | Pilot run 3, F2 with session budget 12, 38 | Harness arm: `finish(claim="not_done")` at the end of the 12-turn session 1 ended the build phase; the 38-turn session never ran; hidden tests 3 of 56. The runner fix for both arms is change 14 |
| S3 | `make replay RUN=ab-20261016-214151-ca9841` | Pilot run 3, F4 canonical | Bare arm: 2 files outside the allowed paths; harness arm (all four layers): 0. In the harness arm the agent time limit cut the test session to 7 turns |
| S4 | `make replay RUN=ab-20261017-090903-926c02` | Class-profile round, F4 canonical, class profile | Bare arm: claimed done, hidden 68 of 69, mutants 4 of 4: primary measure fails. Harness arm: hidden 68 of 69, mutants 1 of 4, test phase ended by the agent time limit; `shipharness ab` exited 2 |

Each is one run, chosen after the fact for what it shows; say so if a learner asks, and point to the
all-results slide for where it sits.

### Constructed examples

`make example-1` to `make example-4` (`uv run shipharness example --section demo-N`) run section N's
layer stack on its canonical task in the real sandbox, judged by the real referee, with the model
replaced by scripted steps that make the mistake the layer exists to catch. They cost $0, need no API
key, carry the `CONSTRUCTED EXAMPLE` badge on every screen, and are never counted
(`src/shipharness/examples/`). They need Docker, but not OpenAI.

| Command | What it shows (from the scenario's docstring) |
|---|---|
| `make example-1` | `GET /issues` written without the org filter: the board shows the other org's cards (⚠ "other org" on screen 2) and the referee's R1 check reports the new violation |
| `make example-2` | A 3-turn session 1, the handoff written by the state layer, and session 2 reading `session-handoff.md` first and finishing without redoing session 1's work |
| `make example-3` | A patch to the out-of-scope `app/api/middleware.py` rejected (BLOCKED), a package install denied by the sandbox (DENIED network), then the change in the allowed files |
| `make example-4` | A wrong test of the agent's own, a done claim refused by the verify gate ("Not accepted"), then the fixed test and a passing gate |

---

## What to say

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
