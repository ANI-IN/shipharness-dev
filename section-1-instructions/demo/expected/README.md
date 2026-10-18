# Module 1: Harness Engineering for Coding Agents - Demo 1: What one real run looked like

This folder holds the output and the screenshots of one real `make show-1` run, run on 2026-10-18
with the class settings (run id on the
[evidence page](../../../docs/evidence/s1.md#s1-show-1-capture)). Nothing here is
staged or edited, except where a line says it was cut. Use it to check that your run looks roughly
like this one, or to follow the demo without running it. When and how it was captured is on the
[evidence page](../../../docs/evidence/s1.md#s1-show-1-capture).

> **Terms on this page**
>
> - **Primary verdict**: The referee's answer to the one question the section asks.
> - **Full verdict**: The primary verdict plus every other check: hidden tests, mutants, review.
> - **Harness note**: A line the instructions layer adds to screen 1, such as "agent read ARCHITECTURE.md".
> - **Tenant isolation rule**: House rule 1: Tenant isolation, another org's resource answers 404,
>   never 403.
> - **Mutant**: A copy of the code with one small bug planted on purpose; a good test catches (kills) it.
> - **LangSmith**: The tracing service that records every model call of a run.

## Terminal output

| File | What it holds |
|---|---|
| `terminal.txt` | The command, the record line, the cost line, the start and end lines |

The start and end lines (with the wall time) are the capture script's. The running cost
totals are cut from `terminal.txt` where it shows `...`.

## Screenshots

The screenshots were taken after the run, from `make console`, which serves recorded runs. The
minute screens show the console fed with the run's log up to that minute of the console clock.

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Screen 1 at minute 1: build turns, two harness notes, no gate, referee pending](screen-1-minute-1.png)

*Minute 1: 31 instruction files placed and `ARCHITECTURE.md` read. No gate; referee pending.*

![Screen 1 at minute 2: the agent said done and session 2 reads the tests](screen-1-minute-3.png)

*Minute 2: the agent has said done and, in its second session, reads the tests and runs them.*

![Screen 1 at minute 3: primary verdict PASS, secondary checks running](screen-1-minute-4.png)

*Minute 3: "primary verdict ready: PASS", no new tenant isolation violations, other checks still running.*

![Screen 1 after the full verdict: primary verdict PASS, hidden tests 50/52, claim supported](screen-1-final.png)

*The end: 38 turns, hidden tests 50/52, mutants killed 3/4, primary verdict at 02:35, full at 05:34.*

![Screen 2: the board as admin@acme.test](screen-2-final.png)

*Screen 2: only own-org cards, no duplicates.*

![Screen 3: files read, changed files, referee checks](screen-3-final.png)

*Screen 3: `ARCHITECTURE.md` and the handbook read; five files changed; every check 0 new.*

![Screen 4: primary results, one dot per run](screen-4-final.png)

*Screen 4: the test runs before class, one dot per run. This run's verdict is at the top, not a dot.*

![Screen 5: referee events and LangSmith links](screen-5-final.png)

*Screen 5: the live tail of referee events and the LangSmith links for the agent and the referee.*
