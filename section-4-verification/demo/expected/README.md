# Module 1: Harness Engineering for Coding Agents - Demo 4 expected output

This folder holds the output and the screenshots of one real `make show-4` run, on a quiet machine,
with the class settings. Nothing here is staged or edited, except where a line says it was cut. Use it
to check that your run looks roughly like this one, or to follow the demo without running it. When
and how it was captured is in the [evidence page](../../../docs/evidence/s4.md#s4-show-4-capture).

> **Terms on this page**
>
> - **Verify gate**: The checks that run in the agent's container when it claims done; a failure sends the claim back.
> - **Test filters**: Five checks a test from the test phase must pass to be kept.
> - **Referee**: The program that scores each run after the agent stops.
> - **Primary verdict**: The referee's answer to the one question the section asks.
> - **Full verdict**: The primary verdict plus every other check: hidden tests, mutants, review.
> - **Referee mutants**: Planted faults the agent never sees; the referee counts how many the shipped tests catch.

## Terminal output

| File | What it holds |
|---|---|
| `terminal.txt` | The end of terminal 2: record line, cost line, wall time |

The run id and the running cost totals are cut from `terminal.txt` where it shows `...`.

## Screenshots

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Screen 1 at minute 1: the scope layer blocks a write to app/services/errors.py](show-4-screen-1-t01m.png)

*Minute 1: turn 1.15 tries to patch `app/services/errors.py`, outside the allowed files, and is blocked.*

![Screen 1 at minute 3: the agent claims done and eleven gate pills wait](show-4-screen-1-t03m.png)

*Minute 3: `finish done` at turn 1.31. Every gate pill is pending; the referee has not started.*

![Screen 1 at minute 4: every gate pill passed, the feature marked as passing, the test phase starts](show-4-screen-1-t04m.png)

*Minute 4: all eleven items pass, the scope layer sets `passes`, and session 2, the test phase, begins.*

![Screen 1 at minute 9: primary verdict FAIL, hidden tests 68, mutants 0, claim not supported](show-4-screen-1-t09m.png)

*Minute 9: the referee's primary verdict is FAIL while the secondary checks still run.*

![Screen 1 after the full verdict](show-4-screen-1-final.png)

*The end: 43 turns, hidden tests 68/69, mutants killed 0/4, primary verdict at 09:19, full at 10:55.*

![Screen 2: the board and the two-tab edit conflict](show-4-screen-2-final.png)

*Screen 2: tab B's stale save gets HTTP 409, so the board stops the lost update.*

![Screen 3: files read, the diff map, referee checks, and the test filter table](show-4-screen-3-final.png)

*Screen 3: one test kept after five filters; two stopped at filter 3, one at filter 2.*

![Screen 4: primary results, one dot per run](show-4-screen-4-final.png)

*Screen 4: the test runs before class. Version checks shows empty dots for both arms. This run is not a dot.*

![Screen 5: first wrong turn, referee events, and LangSmith links](show-4-screen-5-final.png)

*Screen 5: the first wrong turn is the blocked write at turn 1.15; LangSmith links for agent and referee.*
