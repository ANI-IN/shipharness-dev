# Module 1: Harness Engineering for Coding Agents - Demo 3: Scope at work

## The problem

**Illustrative scenario.** You ask a coding agent to stop lost updates on issues. Along the way it
adds a new error class to the shared errors module that every endpoint imports. The ticket's tests
pass and the diff looks tidy. A week later an older endpoint changes behaviour, and nobody links it
to a ticket that never mentioned that module.

This demo puts the same pull in front of two live agents. TeamTrack's ticket for Feature 4: Version checks on
issue edits asks for ETags, `If-Match` checks that answer 412, and an issue history. The ticket's allowed paths list the issue
and audit files, the board, and the tests. The shared `app/services/errors.py` is not on the list.

> **Terms on this page**
>
> - **Bare arm**: An agent run with the ticket and the repository, and no harness.
> - **Harness arm**: The same run with the harness turned on.
> - **A/B**: Bare arm and harness arm on the same ticket, scored the same way.
> - **Referee**: The program that scores each run after the agent stops.
> - **Primary verdict**: The referee's answer to the one question the section asks.
> - **Console**: The browser page that shows a run live, on five screens.
> - **Ticket**: The task the agent gets, written like a work ticket.
> - **Allowed paths**: The globs a ticket lists for each phase; the files the agent may change then.
> - **Out-of-scope file**: A file in the shipped diff that matches none of the allowed paths.
> - **Block**: A patch the scope layer refuses before anything is written; the agent sees `BLOCKED`.
> - **Lost update**: One edit silently overwriting another made a moment earlier.
> - **Hidden tests**: Tests the referee runs that the agent never sees.
> - **Mutant**: A copy of the code with one small bug planted on purpose; good tests catch (kill) it.

## What you'll see

`make demo-3 FEATURE=version-checks` runs both arms at once on the version checks ticket. The harness
arm has the instructions, state, and scope layers; the bare arm has none. You watch the scope layer
refuse the harness arm's patch to the shared errors module, while the bare arm changes it freely.

![Two tabs read ETag 1; the first save gets ETag 2, the second save with If-Match 1 gets 412](../../docs/diagrams/optimistic-concurrency.svg)

*The version checks ticket both arms build: a save with a stale If-Match gets 412.*

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Console screen 3 after both verdicts: the bare arm's diff map shows app/services/errors.py changed, the harness arm's shows it blocked](expected/screen-3-final.png)

*The bare arm changed the shared errors module; the harness arm was blocked on it (diff_scope 1 new, 0 new).*

Times and cost measured on 2026-10-18 with the class profile, three live runs of
`make demo-3 FEATURE=version-checks`: bare primary verdict 4:19 to 6:51 after launch and full
verdict 7:25 to 10:30; harness primary verdict 7:21 to 10:46 and full verdict 9:47 to 13:43;
$0.048 to $0.051 per A/B. All six arms completed. In all three, the bare arm changed
`app/services/errors.py` (`diff_scope` 1 new) and the scope layer blocked the harness arm's patch
to it (`diff_scope` 0 new)
([evidence](../../docs/evidence/general.md#verification-runs-after-the-rename)).

This is a real A/B, because the course measured a gap on this ticket before class: in three test
runs, every bare arm changed `app/services/errors.py` and every harness arm stayed inside the list
([evidence](../../docs/evidence/s3.md#s3-confirmation)). The files the scope layer gives the agent are in
[harness/](harness/): `feature_list.json`, its schema, and `scope-rules.txt`, the exact scope text in
the agent's context. `sandbox-policy.toml` next to them holds the container limits that both arms
of this demo run under.

![Flowchart: a patch to feature_list.json or outside the allowed paths is blocked; a command's changes outside are reverted](../diagrams/scope-check-flow.svg)

*In the demo, the harness arm's patch to app/services/errors.py takes the BLOCKED branch.*

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

**Terminal 2, the live A/B:**

```bash
./section-3-scope-sandbox/demo/run.sh
```

The script checks your keys, Docker, and the class date, then runs `make demo-3 FEATURE=version-checks`.
Outside class, run `PURPOSE=pilot ./section-3-scope-sandbox/demo/run.sh`. You can also call the make
target directly. Without `FEATURE=version-checks`, `make demo-3` runs the ticket for Feature 3: Safe
retries for issue creation instead.

At the end, terminal 2 prints one record line per arm and the cost line. This capture is the command
that `make demo-3 FEATURE=version-checks PURPOSE=pilot` runs (cut where marked `...`; the full
capture is in [expected/terminal.txt](expected/terminal.txt)). `F4` in the record is the version
checks feature:

```text
A/B <run id> (F4, layers=['instructions', 'scope', 'state'], profile=class)
  bare     completed         claim=done     primary={"hidden_passed": 68, "mutants_killed": 4} passed=False hidden 68/69 mutants 4/4 reviewer=reject cost=$0.0216
  harness  ABORTED: timeout  claim=done     primary={"hidden_passed": 65, "mutants_killed": 4} passed=False hidden 65/69 mutants 4/4 reviewer=reject cost=$0.0206
Cost: $0.048707 (this command: gpt-5.6-luna $0.006513, gpt-6-luna $0.042193; ...)
```

The record line's `primary` is the feature's own measure: every hidden test and every referee mutant.
No arm met it in the test runs. The scope result is not on this line; it is on screen 3.

The command exits with 0 when both arms completed, 2 when an arm ended `ABORTED`, and 1 on `ERROR`.
With the class profile, expect 0: all six arms of the 2026-10-18 runs completed. The capture above
exits 2: under an older harness time limit its harness arm ended `ABORTED: timeout` (see "What the
result means"). One A/B costs at most $0.48, two arms and two reviews at their caps.

**In the browser**, reload the runs list, open the newest run, and press `1`. Keys: `1` Live, `2`
Boards, `3` Evidence, `4` A/B Report, `5` Traces; `F` shows one arm full screen.

### Files and links

- [run.sh](run.sh): the script that checks your setup and starts the run
- [walkthrough.md](walkthrough.md): the code behind the layer, explained
- [harness/](harness/): the files the layer gives the agent
- [expected/](expected/README.md): a captured run, the fallback when you cannot run it live
- [Evidence page](../../docs/evidence/s3.md): every run behind the results
- Console: [http://127.0.0.1:8765](http://127.0.0.1:8765) (after `make console`)

## What to watch

Screen 1, Live, shows both arms as they go: the harness arm's notes (instruction files, state
files, `feature_list.json`), the bare arm's patch to `app/services/errors.py` going through, and a
`block` row for the same file in the harness arm; then each arm's primary verdict and full verdict
([evidence](../../docs/evidence/s3.md#s3-demo-capture)). `F4` in the console notes is the version
checks feature.

The refusal, as the harness arm's run log records it (one event, cut to its data):

```json
{"type":"blocked","data":{"phase":"build","paths":["app/services/errors.py"],"action":"reject_patch","reason":"app/services/errors.py: outside the allowed paths for the build phase (app/api/issues.py, app/api/schemas.py, app/services/issues.py, app/repositories/issues.py, app/services/audit.py, app/repositories/audit.py, app/web/**, tests/visible/**); patch not applied"}}
```

The agent's tool result starts with `BLOCKED:` and carries the same reason, so the agent learns which
files it may change. Nothing was written to the workspace.

![Console screen 1 after both verdicts: both arms FAIL the feature's measure, the harness arm ABORTED: timeout, both claims not supported](expected/screen-1-final.png)

*Screen 1 at the end. Both pills say FAIL: that is the feature's measure, not the scope question.*

**Screen 3, Evidence.** Read the middle panel, "Scope and sandbox". The bare arm's diff map lists
`app/services/errors.py` as changed. The harness arm's lists it as blocked. In the right panel, the
referee row `diff_scope` says 1 new for bare and 0 new for harness. "Sandbox denials: none" for both:
the container refused nothing. The same pattern held in the other two test runs:

![Screen 3 of test run 1: the bare arm changed app/services/errors.py, the harness arm was blocked on it](expected/screen-3-run-1.png)

*Test run 1: the same file, changed by the bare arm and blocked for the harness arm.*

![Screen 3 of test run 2: the bare arm changed app/services/errors.py, the harness arm was blocked on it](expected/screen-3-run-2.png)

*Test run 2: the same again. Three runs, three times the same shared file.*

**Screen 5, Traces.** "First wrong turn" names the turn where each arm first went wrong: the bare
arm's edit of `app/services/errors.py`, and the harness arm's blocked patch.

![Screen 5: first wrong turn, bare turn 1.14 edited app/services/errors.py, harness turn 1.12 blocked](expected/screen-5-final.png)

*Screen 5. The bare arm's first wrong turn is an edit; the harness arm's is a refusal.*

**Screen 2, Boards.** The board as an Acme user, and the two-tab edit test the referee runs for version checks.

![Screen 2: both boards show only own-org cards, and both arms detect the two-tab edit conflict](expected/screen-2-final.png)

*Screen 2. Both arms built the board conflict page: a stale save gets a 409 page.*

![The referee's two-tab capture for the harness arm: tab B got HTTP 409 and the page says the issue was changed by someone else](expected/conflict-harness.png)

*The referee's own frame: tab A saved first, so tab B's stale save is refused.*

**Screen 4, A/B Report.** One dot per run, per feature and arm, on each feature's own primary
measure. The version checks rows are all hollow: no arm has met that feature's measure. Say: "The scope count is on
screen 3, not here."

![Screen 4: primary measures, one dot per run, per feature and arm](expected/screen-4-final.png)

*Screen 4. These dots score the feature's own measure, which neither arm met.*

## What the result means

The scope question is one count per arm: `out_of_scope_files`, the files in the shipped diff that
match none of the allowed paths. The referee computes it on both arms the same way, after removing
harness files such as `feature_list.json`. Zero means the change stayed inside the ticket's list. One
or more means the arm changed a file the ticket did not allow.

The harness arm's zero is expected: the scope layer refuses exactly what the count measures. The
finding is the bare arm's count. With the same ticket, handbook, model, and container, it changed a
shared file every time nothing stopped it.

| Reading | What it looks like here | What the test runs found |
|---|---|---|
| Harness ahead | The bare arm leaves the list in more runs than the harness arm | Seen: bare 0 of 3 passed, harness 3 of 3 |
| No measurable difference | Both arms stay inside, or leave, in about the same number of runs | Seen on safe retries, a different ticket |
| Bare ahead | The harness arm leaves the list more often | Not seen |

![Dot chart: on version checks the bare arm failed 3 of 3 runs and the harness arm passed 3 of 3; on safe retries for issue creation all runs passed](../diagrams/results-s3.svg)

*The three test runs before class, one dot each: bare 0 of 3 passed, harness 3 of 3.*

What the result cannot tell you:

- **That the stray file broke anything.** Existing tests kept passing in every arm. The count says the
  change left the ticket's scope; it does not say the change was wrong.
- **That the harness arm built a better feature.** Both arms failed the feature's own measure in every test
  run. Harness arms passed fewer hidden tests in two of three runs, and all of them ended
  `ABORTED: timeout`.
- **Why the harness arm timed out.** It hit the harness's own limit on harness work, 120 s
  (`HARNESS_TIMEOUT_S`), not the 420 s agent limit. The handoffs and the visible-test run that sets
  `passes` count toward it. Each harness arm still shipped a change, and the referee scored it.
  Since 2026-10-18 the class profile gives harness work 900 s, so in class the harness arm
  completes; the three test runs above ran with 120 s
  ([evidence](../../docs/evidence/general.md#class-harness-limit)).

One A/B in class is one more dot. Read it against the three test runs, not alone. The
[walkthrough](walkthrough.md) shows the code behind the block and the count.

## If it fails

| What you see | Why | What to do |
|---|---|---|
| `x OpenAI refused the key`, exit 2, no arm started | The key is missing or rejected | Fix `OPENAI_API_KEY`; rerun `make doctor` |
| `x SHIPHARNESS_CLASS_DATE is not set`, exit 2 | A class run needs the class day | Set it, or add `PURPOSE=pilot` |
| An arm ends `ERROR` with `docker run failed` | Docker is not running, or an image is missing | `sudo systemctl start docker`, then `make warm` |
| `make console` says `address already in use` | Another program holds port 8765 | `make console CONSOLE_PORT=8766` |
| The record line says `ABORTED: timeout` | An agent or harness time limit | Rare with the class profile; read the verdicts as usual |
| The bare arm stays inside the list | The agent chose other files this time | A real result: one more dot for the comparison |
| The run builds safe retries, not version checks | `FEATURE=version-checks` was left out | Rerun with `make demo-3 FEATURE=version-checks` |

The demo never falls back to a recording or a stand-in model. Still stuck? See
[docs/troubleshooting.md](../../docs/troubleshooting.md).
