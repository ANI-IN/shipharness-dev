# Module 1: Harness Engineering for Coding Agents - Final project: ship a feature with the whole harness

## The problem

**Illustrative scenario.** You have a real feature to ship with an agent. Use the whole harness and
decide which layers earn their place. The easy path is to switch every layer on, run the feature
once, and keep what looked better. A second run might split the other way; nobody runs one.

The cost: every task pays for the harness on one data point, or a good layer goes after one bad run.

> **Terms on this page**
>
> - **Harness**: the files and code around the agent that decide what it sees and may do.
> - **Harness layer**: one part of the harness: instructions, state, scope, or verification.
> - **Bare arm**: an agent run with the ticket and the repository, and no harness.
> - **Harness arm**: the same run with the harness turned on.
> - **A/B**: bare arm and harness arm on the same ticket, scored the same way.
> - **Referee**: the program that scores each run after the agent stops.
> - **Primary verdict**: the referee's answer to the one question the section asks.
> - **Console**: the browser page that shows a run live, on five screens.
> - **Hidden tests**: tests the referee runs that the agent never sees.
> - **Referee-set mutant**: a small planted bug; the arm's own tests should fail on it.

Why it happens:

- Each harness piece encodes an assumption about what the model cannot do on its own, and "those
  assumptions are worth stress testing" ([Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
- The way to find out is "removing one component at a time and reviewing what impact it had on the
  final result" (the same source). One run removes nothing and compares nothing.
- Model output changes from run to run. The course ran `make final` on the same feature several
  times, and the A/Bs split differently ([evidence](../docs/evidence/final.md#final-project)).

The final project runs one live A/B with all four layers and teaches you to read it as one dot among
many. Then you put the same harness on your own repository. The course measures whether the harness
helps, and reports every result as measured.

## What you'll see

You pick one feature, bulk close, watchers, or labels, and run both arms on it at the same time. The
harness arm gets all four layers; everything else is the same: ticket, model, tools, sandbox, turn
budgets (the most turns each session may take), and cost cap. One referee scores both arms, and you
watch them side by side on console screen 1.

```mermaid
flowchart LR
  T["Pick a feature<br/>tasks/"] --> B["Bare arm<br/>own container"]
  T --> H["Harness arm<br/>4 layers, harness/"]
  B --> R["Referee<br/>fresh copy + the arm's diff"]
  H --> R
  R --> V["Verdict per arm<br/>terminal 2, screens 1-5"]
  V --> D["Your decision:<br/>which layers earn their place"]
```

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Console screen 1 after the full verdict of the course's own run](expected/screen-1-final.png)

*The end of the course's own run: both arms at hidden tests 46/46; mutants killed 3/3 (bare) and 1/3 (harness), whose run ended on its time limit inside the gate.*

| Path | What it holds |
|---|---|
| [run.sh](run.sh) | The live run: checks, then `make final` |
| [tasks/](tasks/f5-bulk-close.md) | Bulk close, watchers, labels: the ask, the rules at risk, the referee's checks |
| [harness/](harness/README.md) | Every file the harness arm gets, all four layers |
| [walkthrough.md](walkthrough.md) | One run through the code, step by step |
| [expected/](expected/README.md) | Real terminal output and all five screens from one run |
| [your-repo/](your-repo/README.md) | Part 2: the harness on your own repository |
| [CHECKLIST.md](CHECKLIST.md) | What to show when you are done |

## Run it

### Step 1: Get ready

First time on this machine? Follow [setup/](../setup/README.md) until `make doctor` ends with
`result: + ready`. Then run `make warm` once: it builds the images and caches the referee and gate
baselines, with no model calls. In class, `.env` holds `SHIPHARNESS_CLASS_DATE` with the class day.
Practising alone, put `PURPOSE=pilot` in front of the command instead.

### Step 2: Pick the feature

In class, a poll picks one. Each feature is a separate A/B. The task pages say what each asks for,
which house rules it puts at risk, and what the referee checks.

| Feature | Task page | Build sessions (turns each) | Hidden tests |
|---|---|---|---|
| Bulk close | [f5-bulk-close.md](tasks/f5-bulk-close.md) | 1 (30) | 46 |
| Watchers | [f6-watchers.md](tasks/f6-watchers.md) | 2 (20, then 30) | 54 |
| Labels | [f7-labels.md](tasks/f7-labels.md) | 2 (25, then 35) | 64 |

### Step 3: Start the console

In terminal 1, leave it running, then open `http://127.0.0.1:8765/`:

```bash
make console
```

### Step 4: Run the A/B

In terminal 2. `run.sh` checks the keys, the class date, Docker, and the console, then runs
`make final FEATURES=bulk-close`; `FEATURES=watchers` or `FEATURES=labels` picks another feature:

```bash
PURPOSE=pilot ./final-project/run.sh
```

In the browser, open the newest run and press `1`. When both arms are judged, terminal 2 prints one
line per arm and a cost line. The course's own run, with the A/B id cut (the full output is in
[expected/terminal.txt](expected/terminal.txt)); `F5` in the A/B line is bulk close:

```text
A/B ... (F5, layers=['instructions', 'scope', 'state', 'verify'], profile=class)
  bare     completed         claim=done     primary={} passed=True hidden 46/46 mutants 3/3 reviewer=accept cost=$0.0196
  harness  ABORTED: timeout  claim=done     primary={} passed=True hidden 46/46 mutants 1/3 reviewer=reject cost=$0.0139
Cost: $0.038253 (this command: gpt-5.6-luna $0.004675, gpt-6-luna $0.033578; session $0.060114 of $2.50; build $0.060114 of $15.00 ($14.939886 left))
make: *** [Makefile:173: final] Error 2
```

The harness arm said done after 20 turns. Its gate then ran the house-rule checks in the arm's
container, and on a busy machine two gate commands hit their time limits. The gate failed on those
timeouts, the harness's own time ran out, and the arm ended `ABORTED: timeout` before a test phase.
An aborted arm is still judged and shown, so the command exits 2: a result, not a failure.

`make final FEATURES=bulk-close LAYERS=-scope` removes one layer from the harness arm. That is the
leave-one-out idea from the problem above, one layer and one feature at a time.

### Time and cost

The caps come from `.env.example` and `platform/src/shipharness/config/settings.py`: at most $0.25
per arm and $0.04 per review, so at most $0.58 per feature. The class profile gives each arm an
agent time limit of 420 s (`platform/src/shipharness/config/profiles.py`), plus 120 s for the
harness's own work (`HARNESS_TIMEOUT_S`). Prices are in `platform/config/prices.toml`.

The course's own bulk close run on 2026-10-17 took 12 min 9 s from `run.sh` to the cost line and
cost $0.038253, with one other live batch running on the same machine. After the A/B's launch, the
primary verdicts came at 4 min 27 s (bare) and 5 min 46 s (harness), and the full verdicts at
11 min 39 s and 11 min 41 s ([evidence](../docs/evidence/final.md#final-project)).

## What to watch

| Minute after the course run's launch | Screen | What appears |
|---|---|---|
| 1 | 1 | Both arms at work; the harness arm shows its layer notes |
| 5 | 1 | Bare: run completed after 42 turns, then "primary verdict ready: PASS" |
| 7 | 1 | Harness: said done after 20 turns; gate items fail; "run ABORTED: timeout" |
| 12 | 1 to 5 | Both full verdicts; terminal 2 prints both lines |

Then switch screens with the keys `1` to `5`; [expected/](expected/README.md) shows each screen and what to notice on it.

![Screen 1 at minute 1: both arms at work, harness notes for the placed files](expected/screen-1-minute-1.png)

*Minute 1. The harness arm's notes show the map, the state files, and the feature list in place.*

![Screen 1 at minute 5: bare arm completed with primary verdict PASS, harness arm still building](expected/screen-1-minute-5.png)

*Minute 5. The bare arm is judged; its secondary checks still run.*

![Screen 1 at minute 7: harness arm said done, gate items failed, run aborted on time](expected/screen-1-minute-7.png)

*Minute 7. The harness arm's gate failed on time limits, and the arm ended on its own time limit.*

## What the result means

**The three final features have no primary measure.** Their `task.toml` files set `primary_measure = ""`, so the
referee marks every run as passed. On screen 1, "primary verdict ready: PASS" says nothing about the
feature. Compare the counts instead:

| Count | Where | What it tells you |
|---|---|---|
| Hidden tests passed | `hidden 46/46` | Does the feature work as specified? |
| Mutants killed | `mutants 2/3` | Do the arm's own tests catch planted bugs? |
| Claim | `claim=done` | Did the agent say it was done? |
| Out-of-scope files | Screen 3 diff map | Did it change files it should not? |

Each arm's full record is in `exports/scores/`, one JSON file per run. "It is easy to see tests pass
and assume the job is done, when this is rarely the case" ([Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler)).
So compare the claim with the counts, not with the agent's summary.

**One A/B is one dot.** Read the three outcomes like this:

- **Harness ahead**: the harness arm has better counts, and many runs already show the same gap.
- **No measurable difference**: the counts are equal, or differ in a way one run can produce.
- **Bare ahead**: the same as harness ahead, the other way round.

![Dot chart: one dot per run per arm for the four section features, filled for passed, hollow for failed](../docs/diagrams/results-final.svg)

*Tonight's A/B adds one dot per arm to rows like these.*

The course's own run: both arms passed 46 of 46 hidden tests. The bare arm's tests killed 3 of 3
mutants and the harness arm's 1 of 3, and the blinded reviewer (a separate model that reads the diff
without knowing which arm wrote it) rejected the harness arm's change over its audit row. The
harness arm never reached its test phase, because its gate ran out of time on a busy machine. As one
dot it reads bare ahead on mutants, for a reason that is about time, not about the layers. An
earlier bulk close run split the other way: 1 of 3 (bare) against 3 of 3 (harness).

**What many runs showed.** Before class, the course ran each section's ticket several times per
arm, plus a confirmation on a second Section 3 ticket ([evidence](../docs/evidence/final.md#final-project)):

| Section | Primary measure | Result |
|---|---|---|
| 1 Instructions | No new tenant leak | No measurable difference |
| 2 State | Work survives a session stop | No measurable difference |
| 3 Scope (idempotent creation, the section's ticket) | No file outside the allowed paths | No measurable difference |
| 3 Scope (version checks, the confirmation) | No file outside the allowed paths | Harness ahead: 3 of 3 against 0 of 3 |
| 4 Verification | All hidden tests and mutants | No measurable difference (both fail) |

To draw your own dots from every run in `exports/`, run the report. It makes no model calls and
writes `exports/report.html`, one dot per run, filled for passed and hollow for failed:

```bash
uv run shipharness report
```

## If it fails

| What you see | Why | What to do |
|---|---|---|
| Results printed, then `Error 2` | An arm was aborted on time or cost | Nothing: the run is judged and shown |
| Harness arm `ABORTED: timeout` with 0 turns | Gate baseline not cached: setup used the 120 s | `make warm`, then run again |
| `x OPENAI_API_KEY is not set` | The key is missing from `.env` | Add it, then `make doctor` |
| `x SHIPHARNESS_CLASS_DATE is not set` | Class runs need the class day | Set it in `.env`, or use `PURPOSE=pilot` |
| `x FEATURES=F4: the final project runs F5, F6, or F7` | The four section features are not final features | Pick `bulk-close`, `watchers`, or `labels` |
| `x Docker is not running` | The Docker service is stopped | `sudo systemctl start docker`, then `make warm` |
| `! console not reachable` | The console is not started | `make console` in another terminal |

The command never falls back to a recording. If Docker, the network, or OpenAI fails in class, the
instructor can show a recorded A/B with `make replay RUN=` and the A/B id; every screen then says
RECORDING. More fixes: [docs/troubleshooting.md](../docs/troubleshooting.md).

## Use it on your own repository

The harness pieces work outside TeamTrack. [your-repo/](your-repo/README.md) takes you step by step
from `shipharness init` to filling the map, setting house rules, a first harnessed run, reading the
results, and deciding which layers to keep. Every step shows its command and the real output it
printed on a worked example, a small library, in [your-repo/example/](your-repo/example/README.md).

| Tool | What it does | Model calls |
|---|---|---|
| `shipharness init` | Copies the starter kit into your repository | None |
| `shipharness check` | Runs your house rules against a baseline | None |
| `shipharness testgen` | Writes tests and keeps only those that pass five filters | Yes, capped |

The four course skills package the same work for Claude Code, Codex, and Cursor; start at
[use-in-your-repo/](../use-in-your-repo/README.md). When you are done, show the items in
[CHECKLIST.md](CHECKLIST.md). Report results the way this page does: as counts, one dot per run.

## Sources

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (Anthropic)
- [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) (Anthropic)
