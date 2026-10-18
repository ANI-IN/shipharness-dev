# Module 1: Harness Engineering for Coding Agents - Final project: what one real run looked like

This folder holds the terminal output and the console screenshots of one real `make final` run on
Feature 5: Bulk close, run on 2026-10-18 with `make final FEATURES=bulk-close PURPOSE=pilot` and the
class profile (run id on the [evidence page](../../docs/evidence/final.md#final-project-captures)).
Nothing here is staged; the running cost totals are cut from `terminal.txt` where it shows `...`,
and its start and end lines (with the wall time) are the capture script's.
When and how it was captured is on the
[evidence page](../../docs/evidence/final.md#final-project-captures).

> **Terms on this page**
>
> - **Referee**: the program that scores each run after the agent stops.
> - **Primary verdict**: the referee's answer to the one question the section asks.
> - **Full verdict**: the primary verdict plus every other check: hidden tests, mutants, review.
> - **Mutant**: a copy of the code with one small planted bug; a test that fails on it catches it.
> - **Gate**: the checks the verify layer runs when the agent says done; the agent cannot skip them.
> - **Harness note**: a line a layer adds to screen 1, such as "placed 31 instruction files".

## Terminal output

| File | What it holds |
|---|---|
| `terminal.txt` | The command, both arm lines, the cost line, the start and end lines |

Read the two arm lines column by column: status, claim, hidden tests, mutants killed, the
reviewer's verdict, and the arm's cost. Both arms completed in this run. If an arm is aborted on
time, the command ends with `Error 2`, and both arms are still judged.

## Screenshots

The screenshots were taken after the run, from `make console`, which serves recorded runs. The
minute screens show the console fed with the run's log up to that minute of the console clock.

> Your output will differ: run times, ids, and the agent's wording change on every run.

![Screen 1 at minute 1: both arms at work](screen-1-minute-1.png)

*Minute 1: both arms are at work; the harness arm's notes show the skill it read and the files its layers wrote.*

![Screen 1 at minute 3: bare arm judged, harness arm still building](screen-1-minute-5.png)

*Minute 3: the bare arm completed after 36 turns, primary verdict PASS; Feature 5 has no primary measure, so PASS says nothing about the feature.*

![Screen 1 at minute 6: harness gate passed and the test phase started](screen-1-minute-7.png)

*Minute 6: the harness arm said done; every gate pill passed, the feature was marked as passing, and session 2, the test phase, began.*

![Screen 1 after both full verdicts: hidden tests 46 of 46 in both arms, both runs completed](screen-1-final.png)

*The end: hidden tests 46/46 in both arms, mutants killed 2/3 (bare) and 3/3 (harness), full verdicts at 05:31 and 15:11.*

![Screen 2: both boards as an Acme user](screen-2-final.png)

*Screen 2, Boards: Feature 5 changes no board pixels, so both boards show only their own org's cards.*

![Screen 3: files read, diff maps, sandbox denials, referee checks](screen-3-final.png)

*Screen 3, Evidence: both arms changed only allowed files and had no sandbox denials; every referee check 0 new.*

![Screen 4: primary measures, one dot per run](screen-4-final.png)

*Screen 4, A/B Report: both arms' verdicts at the top; below, one dot per scored run in the course machine's `exports/`.*

![Screen 5: referee events and LangSmith links](screen-5-final.png)

*Screen 5, Traces: the live tail, no first wrong turn in either arm, and the LangSmith links of each arm.*

## How to read each screen

| Screen | Look at | It answers |
|---|---|---|
| 1 Live | Status, "Agent said", the gate pills, the referee line | Did each arm finish, and does its claim match the counts? |
| 2 Boards | Each card's org | Did a change leak another org's data onto the board? |
| 3 Evidence | Files read, the diff map, sandbox denials | What did each arm read and change, and what was refused? |
| 4 A/B Report | One dot per run | Is tonight's dot in line with the earlier runs? |
| 5 Traces | The LangSmith links | Which model calls led to the result? |
