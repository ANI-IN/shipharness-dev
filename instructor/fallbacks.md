# Fallbacks and optional extras: recorded runs, replay, constructed examples

What is recorded, where it lives, how to replay it with the RECORDING badge, and what to say. Every
demo section of the class is live (VERIFICATION.md, "Class plan per section", revised 2026-10-17 under
owner message 7; S3 a live A/B since "S3 confirmation: result"). This file holds everything that is
not live, in two clearly separate groups:

- **Fallbacks**: one recording per class command (`make show-1`, `make show-2
  SESSION_BUDGET=12,38`, `make demo-3 FEATURE=version-checks`, `make show-4`, and `make final` per feature),
  replayed only when the live run failed for a reason outside the experiment.
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
final`) under `RUNS_DIR`, default `.shipharness/runs/` (`platform/src/shipharness/config/settings.py`; the
folder is git-ignored), plus the score exports the referee wrote.

| Path | Contents | Needed by |
|---|---|---|
| `.shipharness/runs/<id>/events.jsonl` | The full run log: every event of the arms and the referee (CONTRACTS §8) | Replay (re-emitted with `recorded=True`) |
| `.shipharness/runs/<id>/ab.json` | Task, seed, section, `checkpoint_sha`, the arms' specs and results, `single_arm` for a show-N run, paths of the diffs and session patches (`write_ab_record` in `platform/src/shipharness/ab/demo.py`) | Replay and swap |
| `.shipharness/runs/<id>/<arm>/diff.patch` | What the arm shipped | Replay and swap |
| `.shipharness/runs/<id>/<arm>/sessions/session-<n>.patch` | One patch per session (continuity check, S2) | Replay and swap |
| `.shipharness/runs/<id>/screenshots/<arm>/*.png` | Board screenshots (screen 2) | Only the original run (see the screenshot gap below) |
| `exports/scores/<run id>.json` | One score record per arm | Swap test; screen 4 |

A show-N recording holds the harness arm only (`single_arm` in `ab.json`). `make replay` replays it;
the swap test refuses it (`x <id> is a single-arm run (harness in action): the swap test needs both
arms; pass the id of an A/B`, `platform/src/shipharness/ab/recorded.py`).

Replay and swap export the checkpoint from the commit recorded in `ab.json` (`checkpoint_sha`), never
from the tag name (CONTRACTS §22). The checkpoint tags were moved on 2026-10-17 with the owner's
approval; the old commits stay reachable under `refs/archive/checkpoints-2026-10-16/<tag>`, so the
pilot's recorded `checkpoint_sha` values still resolve (VERIFICATION.md, change 15).

The recordings are not in the repository. On an instructor machine other than the one that ran the pilot,
copy each run directory and its score records from that machine to the same paths.

---

## The fallbacks: how to record them (before class, not on the class date)

Make the recordings on the instructor's machine, inside WSL2, on a day other than the class date,
with `PURPOSE=pilot`: the class session cost cap is keyed by `SHIPHARNESS_CLASS_DATE` (DESIGN
§11.1), pilot-purpose runs trace to `shipharness-pilot`, not the class project, and the class date is
set only at T-30 on the class day (run sheet, "Before class", step 1).

1. `make doctor PURPOSE=pilot` passes; `make warm PURPOSE=pilot` ends with `warm: done`.
2. Run each section's live command once, in order, exactly as the class runs it: `make show-1
   PURPOSE=pilot`, `make show-2 SESSION_BUDGET=12,38 PURPOSE=pilot`, `make demo-3 FEATURE=version-checks
   PURPOSE=pilot`, `make show-4 PURPOSE=pilot`.
3. Run each final feature once, because the poll can pick any of them: `make final FEATURES=bulk-close
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

Cost at the caps: $0.24 per show-N run (one arm plus its review), $0.48 for the Section 3 A/B (two
arms plus two reviews), and $0.58 per final feature. Measured 2026-10-18 with the class profile,
three runs each: show-1 $0.021 to $0.023, show-2 $0.036 to $0.038, Section 3 A/B $0.037 to $0.053,
show-4 $0.023 to $0.033, final bulk close $0.044 to $0.048 (docs/evidence/general.md, "Demo runs
after the speed-up").

## Recorded runs

The current fallbacks are the first complete run of each class command after the harness speed-up
of 2026-10-18, class profile (agent time limit 420 s, harness limit 900 s), `PURPOSE=pilot`, two
runs at a time (docs/evidence/general.md, "Demo runs after the speed-up", fallbacks after the
speed-up). Times run from the make command's launch.

| Command | Fallback (first complete run after the speed-up, 2026-10-18) | What it recorded |
|---|---|---|
| `make show-1 PURPOSE=pilot` | `ab-20261018-045459-2efbfc` | Completed; primary verdict 2:43, full 5:41; House rule 1 0 new, hidden 50/52; $0.0218 |
| `make show-2 SESSION_BUDGET=12,38 PURPOSE=pilot` | `ab-20261018-040749-dad2e1` | Completed; stop and resume 1:01, session 2 read the state files first; primary 4:30, full 6:43; hidden 56/56; $0.0379 |
| `make demo-3 FEATURE=version-checks PURPOSE=pilot` | `ab-20261018-042848-b28607` | Both arms completed; harness patch to `app/services/errors.py` blocked 1:26; out-of-scope files bare 1, harness 0; primary 5:00 and 6:20, full 7:22 and 7:31; $0.0479 |
| `make show-4 PURPOSE=pilot` | `ab-20261018-035501-6a332e` | Completed; blocked patch 1:02, gate pass and done claim 3:01; 4 tests proposed, 3 filtered, 0 kept; primary 5:51, full 6:51; $0.0225 |
| `make final FEATURES=bulk-close PURPOSE=pilot` | `ab-20261018-042848-f7fa49` | Both arms completed; harness gate 3:42, 5 tests, 1 kept; hidden 46/46 each; primary 2:17 and 12:04, full 5:42 and 15:22; $0.0440 |
| `make final FEATURES=watchers PURPOSE=pilot` | not recorded yet: record it on T-1 (steps above) | - |
| `make final FEATURES=labels PURPOSE=pilot` | not recorded yet: record it on T-1 (steps above) | - |

Replay checks (step 5): `make replay RUN=ab-20261018-035501-6a332e PURPOSE=pilot` gave 212 events,
the referee re-run, the RECORDING badge, $0. The show-4 run that kept and discarded tests,
`ab-20261018-040352-f8c404`, also replays (255 events, all five screens populated, $0); use it when
the class should see both kinds of filter result. Replay the others once on the class machine with
the current code before you rely on them.

Earlier fallbacks, superseded: the first complete runs after the harness-limit change, earlier on
2026-10-18 (docs/evidence/general.md, "Verification runs after the rename"), and the runs of
2026-10-17 under load and on a quiet machine, measured with the earlier 300 s agent limit and the
120 s harness limit (VERIFICATION.md, "Live command check under load" and "Class commands
re-timed"). They still replay, but their times and costs no longer match the class commands.

On another instructor machine, record its own fallbacks on T-1 with the steps above; these ids are this
machine's. A fresh clone has no recorded runs: `make replay` with one of these ids prints `x no
recorded A/B` there. Use the ids from your own run list, or from the `A/B ab-…` line your own
command printed.

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
   (`platform/src/shipharness/ab/commands.py`).

### Screenshot gap (screen 2 in a replay)

`replay_ab` copies each arm's `diff.patch` into the new run directory but not the `screenshots/`
folder, while the replayed `screenshot` events point at paths inside the run directory
(`platform/src/shipharness/ab/recorded.py`, `platform/src/shipharness/console/preview.py`). Screen `2` of a replay
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
`docs/extras.md`. None of them is shown in a demo block, and none is a result. The recorded runs in
the table below exist only on the course machine; on a fresh clone these commands print `x no
recorded A/B`.

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
(`platform/src/shipharness/examples/`). They need Docker, but not OpenAI.

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
