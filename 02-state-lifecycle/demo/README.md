# Module 1: Harness Engineering for Coding Agents - Demo 2: A session stop and a clean resume

## The problem

**Illustrative scenario.** A coding agent adds comments to issues. Its first session writes the
migration for a `comments` table and part of the endpoint, then hits its turn limit without a note.
The second session starts with an empty context. It cannot see what the first one did, so it writes
a second migration for the same table from the old head. The deploy stops on two migration heads.

Anthropic's harness team names the cause: "each new session begins with no memory of what came
before." ([Anthropic, Effective harnesses](../../docs/evidence.md#src-anthropic-long-running)) This
demo stops a live agent at that point: TeamTrack's F2 ticket, comments on issues, with the first
session cut off after 12 turns.

> **Terms on this page**
>
> - **Harness arm**: The same run with the harness turned on.
> - **Bare arm**: An agent run with the ticket and the repository, and no harness.
> - **A/B**: Bare arm and harness arm on the same ticket, scored the same way.
> - **Referee**: The program that scores each run after the agent stops.
> - **Primary verdict**: The referee's answer to the one question the section asks.
> - **Full verdict**: The primary verdict plus every other check: hidden tests, mutants, review.
> - **Console**: The browser page that shows a run live, on five screens.
> - **Session turn budget**: The fixed number of turns a session gets before the runner stops it.
> - **Structured handoff**: A file that carries the last session's state and the next steps to the next session.
> - **Continuity failure**: Two migration heads, a table created twice, or 30% or more of session 1's lines redone in session 2.
> - **R7**: House rule 7, migrations: exactly one Alembic head, and a fresh upgrade works.

## What you'll see

`make show-2 SESSION_BUDGET=12,38` runs the harness arm alone, live, with the instructions and state
layers. Session 1 gets 12 turns. At the stop, the state layer writes the handoff and commits it. A
fresh 38-turn session reads it and carries on. The referee then checks whether session 2 broke or
redid session 1's work.

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Console screen 1 at minute 2: Session 1 stopped, Session 2 resumed, turn 2.1 reads the git log and progress.md](expected/show-2-screen-1-t02m.png)

*The moment that matters: session 1 stops, and session 2's first call reads the state files.*

This is not an A/B. The course already compared both arms on this ticket and found no measurable
difference ([evidence](../../docs/evidence.md#section-2)). So class shows the state layer doing its
job, and screen 4 shows the comparison.

```mermaid
flowchart LR
  T2["Terminal 2:<br/>make show-2"] --> S1["Session 1<br/>12 turns"]
  S1 -->|"stop: handoff written, committed"| S2["Session 2<br/>38 turns, empty context"]
  S2 --> TP["Test phase"]
  TP -->|"shipped code, session patches"| R["Referee<br/>continuity first"]
  R --> C["Terminal 1: make console"]
```

## Run it

Before the first run, follow [setup/](../../setup/README.md) until `make doctor` ends with
`result: + ready`, then run `make warm` once. Neither makes a model call.

Use two terminals, both in the repository root.

**Terminal 1, the console.** Leave it running:

```bash
make console
```

It prints the address to open:

```text
uv run shipharness console --port 8765
Console: http://127.0.0.1:8765/
INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
```

Open `http://127.0.0.1:8765/` in your browser. On Windows, the Windows browser works.

**Class date or practice run.** A class run is traced to the LangSmith project of the class day, so
`.env` needs the day. Add this line to `.env` and replace YYYY-MM-DD with your class day:

```bash
SHIPHARNESS_CLASS_DATE=YYYY-MM-DD
```

Outside class, skip the date and add `PURPOSE=pilot` to the command in the next step instead.

**Terminal 2, the live run:**

```bash
./02-state-lifecycle/demo/run.sh
```

The script checks your keys, Docker, and the class date, then runs
`make show-2 SESSION_BUDGET=12,38`. Outside class, run `PURPOSE=pilot ./02-state-lifecycle/demo/run.sh`.
You can also call the make target directly; without `SESSION_BUDGET=12,38` the first session runs
the ticket's 20 turns. At the end, terminal 2 prints the arm's record line and the cost line (cut
where marked `...`; the full capture is in [expected/terminal.txt](expected/terminal.txt)):

```text
A/B <run id> (F2, layers=['instructions', 'state'], profile=class, harness in action)
  harness  ABORTED: timeout  claim=not_done primary={"continuity_failure": false} passed=True hidden 56/56 mutants 0/4 reviewer=reject cost=$0.0268
Cost: $0.029525 (this command: gpt-5.6-luna $0.002702, gpt-6-luna $0.026823; ...)
make: *** [Makefile:121: show-2] Error 2
```

The command exits with 0 when the arm completed, 2 when it ended `ABORTED`, and 1 on `ERROR`. The
`Error 2` above is that exit code: the agent time limit ended the run, and the referee still judged
it. One run costs at most $0.24: the per-arm cap plus the per-review cap.

**In the browser**, reload the runs list, open the newest run, and press `1`. Keys: `1` Live,
`2` Boards, `3` Evidence, `4` A/B Report, `5` Traces.

## What to watch

Minutes count from the launch, in one real run on a quiet machine
([evidence](../../docs/evidence.md#s2-show-2-capture)). That run had a 300 s agent time limit; the
class profile now has 420 s.

| Minute | Screen | What appears |
|---|---|---|
| 0 | 1 | Notes "placed 31 instruction files" and "initializer step: init.sh, ..." |
| 0-1 | 1 | Turn 1.1 runs Getting up to speed; then the ticket, handbook, skill, code |
| 1 | 1 | Wrap-up: turns 1.10 and 1.11 update and commit the state files; 1.12 is `finish not_done` |
| 1-2 | 1 | "Session 1 stopped", "session 1 handoff written", "Session 2 resumed" |
| 2-4 | 1 | Session 2 builds: model, service, route, seed, migration `0002_comments.py`, tests |
| 6-7 | 1 | "run ABORTED: timeout · 43 turns", then "primary verdict ready: PASS" at 06:46 |
| 10 | 1 | Full verdict at 09:52: hidden tests 56/56, mutants killed 0/4 |

![Screen 1 at minute 1: turns 1.10 to 1.12 update and commit the state files, then finish not_done](expected/show-2-screen-1-t01m.png)

*Minute 1. The wrap-up turns write the notes the next session will read.*

![Screen 1 at minute 4: session 2 writes the migration 0002_comments.py, the web route, and the tests](expected/show-2-screen-1-t04m.png)

*Minute 4. One new migration, written once, from the current head.*

![Screen 1 at minute 7: run ABORTED timeout after 43 turns, primary verdict PASS, continuity failure no](expected/show-2-screen-1-t07m.png)

*Minute 7. The primary verdict arrives before the slower checks finish. Read it aloud.*

Session 1 ended with `finish(claim="not_done")` on its twelfth turn, and session 2 still started.
That is a runner fix at work: before it, that call ended the build phase, and the 38-turn session
never ran ([evidence](../../docs/evidence.md#s2-runner-fix)).

What session 2 read first is in [expected/](expected/README.md): its git log starts with
"harness: session 1 handoff for F2", and the agent's own notes list the house rules and files that
matter.

Then switch screens.

**Screen 3, Evidence.** Sessions "Session 1 · 12 turns · claim_not_done" and "Session 2 · 31 turns".
The referee list shows `continuity: 0 new` (the primary measure) and `r7_migrations: 0 new`. It also
shows `diff_scope: 1 new`: the agent edited `app/api/issues.py`, outside F2's allowed paths. Nothing
stopped it, because the scope layer starts in Section 3.

![Screen 3: sessions 12 and 31 turns, the diff map, continuity 0 new, diff_scope 1 new](expected/show-2-screen-3-final.png)

*Screen 3. Two sessions, no continuity failure, and one file outside scope.*

**Screen 5, Traces.** The live tail, the LangSmith links, and the first wrong turn: turn 2.16,
named by the scope check. Open the agent's trace and look at session 2's first calls.

![Screen 5: live tail, first wrong turn 2.16 named by the scope check, LangSmith links](expected/show-2-screen-5-final.png)

*Screen 5. The first wrong turn is a scope problem, not a continuity problem.*

**Screen 2, Boards.** One frame of `/board` with "only own-org cards, no duplicates". The comments
panel is on the issue page, which the preview does not open; the hidden board tests judge it.

![Screen 2: the harness arm's board as admin@acme.test](expected/show-2-screen-2-final.png)

*Screen 2. No other org's data on the board.*

**Screen 4, A/B Report.** The test runs before class, one dot per run, per feature and arm. Say:
"Tonight's run is not a dot in the comparison."

![Screen 4: primary results, one dot per run, for each feature and arm](expected/show-2-screen-4-final.png)

*Screen 4. The comparison comes from the test runs, not from tonight's run.*

## What the result means

The primary verdict answers one question: did session 2 break or redo session 1's work? It fails
on two Alembic heads or a failed fresh upgrade (R7), on a table created by two migrations, or when
session 2 removes 30% or more of the lines session 1 added. PASS means none of the three happened.

PASS does not mean the feature was built. Read the hidden-test count next to it. The measure also
cannot fail when session 1 leaves no product code to redo, and a 12-turn session 1 often spends its
turns reading and wrapping up, as this one did.

One run cannot compare arms. The comparison needs both arms, many times:

| Reading | What it looks like here | What the test runs found |
|---|---|---|
| Harness ahead | Fewer continuity failures in the harness arm | Not seen |
| No measurable difference | About the same number in both arms | Seen: no failing run in either arm |
| Bare ahead | Fewer continuity failures in the bare arm | Not seen |

In one of those runs the bare arm, with no state files, found session 1's uncommitted work with
`git status` and carried on ([evidence](../../docs/evidence.md#s2-bare-found-state)). What the demo does show is the state layer's path: what it writes at the stop, and what
the next session reads first. The [walkthrough](walkthrough.md) shows the code behind each step.

## If it fails

| What you see | Why | What to do |
|---|---|---|
| `x OpenAI refused the key`, exit 2, no arm started | The key is missing or rejected | Fix `OPENAI_API_KEY`; rerun `make doctor` |
| `x SHIPHARNESS_CLASS_DATE is not set`, exit 2 | A class run needs the class day | Set it, or add `PURPOSE=pilot` |
| The first session runs 20 turns, not 12 | `SESSION_BUDGET=12,38` was left out | Let it run; the stop comes at turn 20 |
| No "Session 1 stopped" marker | The agent called `finish(claim="done")` in session 1, or hit a cap | Say the arm never faced the stop |
| The arm ends `ERROR` with `docker run failed` | Docker is not running, or an image is missing | `sudo systemctl start docker`, then `make warm` |
| `make console` says `address already in use` | Another program holds port 8765 | `make console CONSOLE_PORT=8766` |
| The record line says `ABORTED: timeout` or `ABORTED: cap` | The agent time limit or a cost cap | Keep the run; read its primary verdict as usual |

The demo never falls back to a recording or a stand-in model. Still stuck? See
[docs/troubleshooting.md](../../docs/troubleshooting.md).
