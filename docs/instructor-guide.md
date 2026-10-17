# Instructor guide

This guide runs the live class of Module 1: Harness Engineering for Coding Agents. The first section
fits on one printed page. The sections after it give the detail behind each line.

> **Terms on this page**
>
> - **Harness arm**: The same run with the harness turned on.
> - **Bare arm**: An agent run with the ticket and the repository, and no harness.
> - **A/B**: Bare arm and harness arm on the same ticket, scored the same way.
> - **Harness in action**: A `make show-N` run: the harness arm alone, live, not an A/B.
> - **Referee**: The program that scores each run after the agent stops.
> - **Primary verdict**: The referee's answer to the one question the section asks.
> - **Console**: The browser page that shows a run live, on five screens.
> - **Fallback recording**: A run you record the day before and replay only if a live run breaks.

## Class-day cheat sheet

Run every command in the repository folder, in an Ubuntu terminal. Terminal A runs the console.
Terminal B runs the section demos. Terminal C runs the final.

| Time | Terminal | Command | What you should see |
|---|---|---|---|
| T-30 min | B | `sed -i "s/^SHIPHARNESS_CLASS_DATE=.*/SHIPHARNESS_CLASS_DATE=$(date +%F)/" .env` | `grep ^SHIPHARNESS_CLASS_DATE= .env` shows today |
| T-30 min | B | `make doctor` | Last line `result: + ready` |
| T-30 min | B | `make warm` | `warm: done` |
| T-30 min | A | `make console` | `Console: http://127.0.0.1:8765/`; open it |
| 0:08 | B | `make doctor` | Read the key lines aloud |
| 0:13 | B | `make show-1` | Section 1, harness in action |
| 1:03 | B | `make show-2 SESSION_BUDGET=12,38` | Section 2, two sessions |
| 2:03 | B | `make demo-3 FEATURE=F4` | Section 3, live A/B |
| 2:54 | B | `make show-4` | Section 4, harness in action |
| 2:55 | C | `make final FEATURES=F6,F5` | The final A/B; put the poll's winner first |
| 3:40 | C | No command | Read the final's arm lines |

After each launch, reload the console's run list and open the newest run. At section minute 25,
look for the `Cost:` line in terminal B.

Times and costs, measured on 2026-10-17, before class ([evidence](evidence.md#captures)):

| Run | Primary, then full verdict | Cost | Cap |
|---|---|---|---|
| `make show-1` | 4:11, 10:00 | $0.0197 | $0.24 |
| `make show-2` | 6:46, 9:52 | $0.0295 | $0.24 |
| `make demo-3` | bare 5:15, 8:06; harness 8:50, 11:18 | $0.0487 | $0.48 |
| `make show-4` | 9:19, 10:55 | $0.0265 | $0.24 |
| `make final`, one feature | bare 3:27, 6:50; harness 9:48, 12:32 | $0.0456 | $0.58 |

Section 3 ran with the class agent time limit, 420 s. The others ran with the earlier 300 s, so a
run that reaches the limit now takes up to 2 minutes longer. The session cap is $2.50: run two final
features only if the session figure on the Section 3 `Cost:` line is $1.10 or less.

What to say at each verdict:

| Section | Pass | Fail |
|---|---|---|
| 1 | "No new tenant leak. One run shows the layer ran, not that it helped." | "A leak shipped with the map in place. That is a result." |
| 2 | "Session 2 picked up the work. No continuity failure." | "The handoff did not carry the work. Screen 3 shows how." |
| 3 | "No file outside the ticket's paths." | "This arm changed a file it was not asked to touch." |
| 4 | "Every hidden test and every mutant. The work is done." | "The agent said done. The hidden tests and mutants say no." |
| Final | No primary measure: read hidden tests and mutants per arm. | "One A/B is one dot." |

In Section 3 the pill on screen 1 shows F4's own bar, which every arm failed before class. Read
`diff_scope` on screen 3 instead. Before class: bare 0 of 3 in scope, harness 3 of 3.

Console keys: `1` Live, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces, `F` one arm full screen.

If a demo stalls:

1. `docker ps`: the arm and referee containers stay listed while the run works.
2. `tail -n 3 .shipharness/ledger.jsonl`: a new line appears after each model call.
3. `make replay RUN=<fallback id>`: only after an `ERROR` from outside the experiment.

Who to call: the helper you named the day before. They watch terminal B and restart Docker.

## The day before

The class date is not set yet, so every command today uses `PURPOSE=pilot`. Pilot runs trace to the
LangSmith project `shipharness-pilot` and leave the class session untouched.

### Check the machine

```bash
make doctor PURPOSE=pilot
make warm PURPOSE=pilot
```

`make doctor` ends with `result: + ready`. Both key lines say `accepted by OpenAI` and `accepted by
LangSmith`. `make warm` builds the images if their source changed, starts each image once, and
caches the referee and gate baselines. It makes no model calls. After an image rebuild it took 2 min
21 s and 3 min 40 s before class. With nothing changed it took 1.2 s. It ends like this:

> Your output will differ: run times, ids, and the agent's wording change on every run.

```text
gate baseline final F7: cached (0.0 s)
warm: done (140.6 s)
Cost: $0.000000 (this command: no calls; session $0.000000 of $2.50; build $2.248909 of $15.00 ($12.751091 left))
```

If `make warm` ends with `warm: incomplete`, run `make images`, then `make warm PURPOSE=pilot` again.

### Record the fallbacks

Run each class command once, in class order. The poll can pick any final feature, so record all three:

```bash
make show-1 PURPOSE=pilot
make show-2 SESSION_BUDGET=12,38 PURPOSE=pilot
make demo-3 FEATURE=F4 PURPOSE=pilot
make show-4 PURPOSE=pilot
make final FEATURES=F5 PURPOSE=pilot
make final FEATURES=F6 PURPOSE=pilot
make final FEATURES=F7 PURPOSE=pilot
```

The first line of each result starts with `A/B` and the id. Write each id down. The fallback for a
command is the first complete run, whatever its result. Do not run a command again to get a nicer
result.

All pilot commands share one cost session, capped at $2.50. Read the session figure on each `Cost:`
line before the next command. If the rest would not fit at the caps, record the final features first.

Check each recording once, then copy it out of the repository. Replace `ID` with the id you wrote
down:

```bash
make replay RUN=ID PURPOSE=pilot
mkdir -p ~/shipharness-fallbacks && cp -a .shipharness/runs/ID ~/shipharness-fallbacks/
```

The replay makes no model calls and shows a red RECORDING badge on every screen. Copy each arm's
score record from `exports/scores/` too. The arms' run ids are in `.shipharness/runs/ID/ab.json`.

### Name a helper

Pick one person who can watch terminal B during class and restart Docker
(`sudo systemctl restart docker`). Give them this page.

## Thirty minutes before

<a id="stage-2-t-30-minutes"></a>

### Set the class date

Class runs trace to the LangSmith project `shipharness-class-` plus the date, and every class command
shares that day's $2.50 session. `make doctor` and `make warm` refuse to start without the date.
Write today's date into `.env`:

```bash
sed -i "s/^SHIPHARNESS_CLASS_DATE=.*/SHIPHARNESS_CLASS_DATE=$(date +%F)/" .env
grep '^SHIPHARNESS_CLASS_DATE=' .env
```

The second command prints the line with today's date. If it prints nothing, the line is missing.
Add `SHIPHARNESS_CLASS_DATE=` followed by today's date (YYYY-MM-DD) to `.env`, and check again.

### Check, warm, and open the console

| Step | Terminal | Command | You should see |
|---|---|---|---|
| 1 | B | `make doctor` | `result: + ready`; the date line names today's class project |
| 2 | B | `make warm` | `warm: done`, in seconds when nothing changed |
| 3 | A | `make console` | `Console: http://127.0.0.1:8765/`; leave it running |
| 4 | Browser | Open `http://127.0.0.1:8765/` | The run list and the key legend |

If `make doctor` or `make warm` says `SHIPHARNESS_CLASS_DATE is not set`, the date step did not
work. `make warm` then prints `warm: nothing done` and exits 2. Repeat the date step.

Do not run `make show-1`, `make demo-3`, or `make final` before class. They would spend the class
session.

### Arrange the screen

| Window | What it shows |
|---|---|
| Terminal A | `make console`; leave it alone |
| Terminal B | The section commands, in a large font |
| Terminal C | `make final`, from the Section 4 launch to the final block |
| Browser tab 1 | The slides |
| Browser tab 2 | The console: the run list, then the current run |
| Browser tab 3 | The console: the final A/B, opened at its launch |

### Prepare the two opening printouts

Both commands make no model calls:

```bash
uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'
uv run python use-in-your-repo/skills/harness-setup/scripts/assess.py platform/teamtrack --out .shipharness/harness-assessment.html
```

The first prints the sandbox policy with the settings as loaded. The class profile raises the CPU
limit to 2 and the agent time limit to 420 s, the same for both arms:

```text
Sandbox policy (identical for both arms)
  network: none
  cpus: 1.0
  memory: 1024 MB (swap: 0 MB)
  pids: 256
  user: 1000:1000
  read-only root: yes
  writable: /work, /tmp
  capabilities dropped: ALL
  tool timeout: 120 s; run timeout: 300 s
  refused commands: 6 rules (network access)
```

The second assesses the bare TeamTrack. It begins with one summary line per area:

```text
Instructions       pass 0  partial 1  fail 5
State              pass 0  partial 0  fail 4
Scope              pass 1  partial 1  fail 3
Verification       pass 1  partial 1  fail 3
Session lifecycle  pass 0  partial 0  fail 5
```

## Section by section

Each section runs the same way. Minutes count from the start of the section.

| Minutes | What happens |
|---|---|
| 0-3 | Poll: the room predicts the result from before class; close it before the launch |
| 3-5 | Launch in terminal B. Open the newest run on screen 1 |
| 5-30 | Concepts, then the walkthrough, while the run goes on; check terminal B at 25 |
| 30-45 | Demo block: the finished run, then all results on one slide and screen 4 |
| 45-50 | Discussion, and the link to the section's demo page |

If the run is still going at minute 25, finish the walkthrough. Then open the demo block on the
running screens: screen 1 shows `primary verdict ready` as soon as the first check is done. A run
with an unwelcome result is a result: show it.

At the end of a run, terminal B prints one `A/B` line, one line per arm, and the `Cost:` line. Read
the session figure aloud. The exit code is 0 when every arm completed, 2 when an arm stopped at a
time or cost limit, and 1 when an arm ended in `ERROR`. Exit 2 is a result, not a broken command.

### Opening (0:00-0:10)

1. The problem slide: the four failures the referee checks in every run.
2. Why it happens, and the harness: one diagram, four layers, one sandbox for both arms.
3. The console tour: press `1` to `5` once each and name each screen.
4. Terminal B: `make doctor`. It never prints any part of a key.
5. Terminal B: the assessment printout. Say: "This is what the bare arm works with: no map, no
   progress file, no feature list. The rules themselves are in both arms."

No run before class leaked another org's cards, so there is no leak screenshot to show. Say so.

### Section 1: Instructions (0:10-1:00)

`make show-1` gives the harness arm the AGENTS.md map, the documents it points to, and the skills.
The ticket is org-wide issue search, next to a legacy handler with no tenant filter. The primary
verdict asks one question: did the change add a new tenant leak?

Demo block, in this order: screen 1 (the files placed, the map and a skill read, then the code),
screen 3 (files read, and the `r1_tenant` line), screen 2 (the board, own-org cards only), screen 5
(trace links).

Say at the result: "This is one harness arm on one run. It shows the layer ran. It cannot show the
layer helped." Before class, no arm leaked in any run: no measurable difference
([evidence](evidence.md#section-1)).

Discussion: "The bare arm read the same rules and applied them. What would have to be true for the
map to earn its place?"

### Section 2: State and session lifecycle (1:00-1:50)

`make show-2 SESSION_BUDGET=12,38` stops session 1 after 12 turns. The harness writes the handoff,
and session 2 starts with an empty context and 38 turns. The primary verdict asks: did session 2
break or redo session 1's work?

Demo block: screen 1 (`Session 1 stopped`, then `Session 2 resumed`), screen 3 (Sessions, and the
state files under Files read), screen 2 (the board with the comments panel), screen 5 (the first
wrong turn).

Say at the result: "Before class, neither arm failed continuity. The measure cannot fail when
session 1 leaves nothing to redo. In the medium- and low-effort rounds, 6 of 12 arms built nothing"
([evidence](evidence.md#section-2)).

Discussion: "Which state file would you keep for this model, and how would you measure it?"

### Break (1:50-2:00)

Put the return time on the break slide. Nothing runs during the break.

### Section 3: Scope and sandbox (2:00-2:50)

This section runs a live A/B. Before class, three A/Bs on the F4 ticket showed a real gap: every bare
arm changed `app/services/errors.py`, a file outside the ticket's allowed paths. The scope layer
blocked the same edit in every harness arm. Bare 0 of 3 in scope, harness 3 of 3
([evidence](evidence.md#section-3)).

`make demo-3 FEATURE=F4` runs both arms at once. The harness arm has the instructions, state, and
scope layers. Each arm has its own sandbox with the same limits.

Demo block: screen 3, the Scope and sandbox column first. Look for `changed app/services/errors.py`
under the bare arm and `blocked app/services/errors.py` under the harness arm. Then the Verification
column: `diff_scope: 1 new` against `diff_scope: 0 new`. Then screen 1: the harness decision
`block`, with the reason the agent read. Then Sandbox denials on screen 3.

Say at the result: "The guard enforces exactly what we measure, so the harness arm's zero is built
in. What the runs show is that, on this ticket, the bare agent edits a shared file every time." Then:
"Both arms still failed F4's own bar. The guard keeps the change in scope. It does not make the
change correct."

If screen 3 lists a sandbox denial, show its reason code and command. If not, show the policy
printout and say: "The sandbox is the same for both arms. It is taught here, but it is never the
variable."

Discussion: "The guard won by construction. What would you measure next to it, so that a guard that
blocks everything cannot look good?"

### Section 4: Verification (2:50-3:40)

Two polls open this section: the Section 4 poll, then the final feature poll (F5, F6, or F7).

1. 2:54, terminal B: `make show-4`. Open its run in browser tab 2 right away.
2. 2:55, terminal C: `make final` with `FEATURES=` set to the winner, a comma, and the runner-up,
   for example `make final FEATURES=F6,F5`. Always pass `FEATURES`: the default is `F5,F6`. Open the
   newest run in browser tab 3, then go back to tab 2.

`make show-4` runs F4 with all four layers. A run passes only with all 69 hidden tests and all 4
referee mutants killed by its own tests.

Demo block: screen 1 (the gate pills, then the test phase), screen 3 (the filter table and the
mutant table), screen 2 (the two-tab conflict panel).

Say at the result: "The gate checks what the agent can see. The hidden tests and the referee's
mutants stay out of its reach." Before class, neither arm passed F4 once: no measurable difference
([evidence](evidence.md#section-4)).

Discussion: "What would a gate need to catch to earn its turns on this model?"

### Final results and wrap-up (3:40-4:00)

The final A/B started at 2:55. This block starts no run.

1. Terminal C: read each arm line and the session figure. The final has no primary measure, so
   `passed=True` does not mean the feature works. Read `hidden` and `mutants` instead.
2. Browser tab 3: screens 1, 3, and 5 for both arms, then screen 2.
3. Screen 4, then the all-results slide. Say: "One A/B is one dot. Read it next to the runs from
   before class, never alone."
4. Assignments, the skills, and the starter kit (`uv run shipharness init --target ../your-repo`).
5. References: [REFERENCES.md](REFERENCES.md).

If the final is not finished at 3:40, walk through its live screens 1 and 2 instead of step 2. Come
back to its screen 4 at the end.

## If something breaks

| What you see | Why | What to do |
|---|---|---|
| `x SHIPHARNESS_CLASS_DATE is not set` | The date step did not run | Repeat the date step |
| `x invalid` on a key line of `make doctor` | The key is wrong or revoked | Replace it in `.env`, run `make doctor` |
| `docker not found` | Docker is not running in Ubuntu | `sudo systemctl start docker` |
| `warm: incomplete` | An image build or start failed | `make images`, then `make warm` |
| Arm `ERROR` with `docker run failed` | Docker stopped, or an image is missing | Restart Docker, then replay the fallback |
| Arm `ABORTED: timeout` or `ABORTED: cap` | A time or cost limit | Nothing: the run is judged. Say which limit |
| Arm `ERROR`: OpenAI billing limit reached | The account is out of credit | Replay fallbacks for the rest of the class |
| Console header says `reconnecting` | The console stopped | Restart `make console` in terminal A, reload |
| Wrong final feature started | `FEATURES` missing or wrong | Ctrl+C in terminal C, launch again |

<a id="replay-procedure"></a>

Use a replay only when a live run failed for a reason outside the experiment: Docker, the network,
the OpenAI account, or time. A run the harness arm "lost" is a result.

1. Say: "This run failed for a reason outside the experiment. Here is the same command, recorded
   yesterday. The referee judges it live now."
2. Terminal B: `make replay RUN=ID`, with the fallback id in place of `ID`.
3. Reload the run list and open the newest run. Every screen shows the red RECORDING badge.

Screen 2 of a replay shows broken images, because the replay does not copy the board screenshots.
Copy them once the replay's folder exists, then reload. `ID` is the fallback id and `NEW` is the
replay's id:

```bash
cp -a .shipharness/runs/ID/screenshots .shipharness/runs/NEW/
```

If Docker itself is down, a replay cannot run either. Open the recording at
`http://127.0.0.1:8765/run/` followed by the fallback id, and say "recorded yesterday" before you
switch screens. Never switch to `SANDBOX_MODE=none` for class results.

The full list of messages is in [troubleshooting.md](troubleshooting.md).

## After class

1. Run `uv run shipharness report`. It writes `exports/report.html`. Harness-in-action runs and
   replays stay out of the A/B report.
2. Back up `.shipharness/runs/` and `exports/`. Every class run counts, including aborted ones.
3. Write down each command's run id, its `Cost:` line, the times from screen 1, and the session
   total.

The review session runs two hours: about 25 minutes per assignment, then 20 minutes of open
questions.

| Time | Item |
|---|---|
| 0:00-0:25 | Assignment 1, Instructions |
| 0:25-0:50 | Assignment 2, State and session lifecycle |
| 0:50-1:15 | Assignment 3, Scope and sandbox, with the hidden-diff reveal |
| 1:15-1:40 | Assignment 4, Verification |
| 1:40-2:00 | Open questions |

Each assignment's reference solution is in its `assignment/solution/` folder, with a step-by-step
walkthrough. The graders and their hidden cases are kept outside this repository. Count the lost
points per criterion before the session, and use those counts in each "common mistakes" slot.
