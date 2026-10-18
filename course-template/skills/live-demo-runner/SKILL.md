---
name: live-demo-runner
description: Run a course's live demos for capture and timing from a fresh clone, under the pilot purpose and a budget cap, timing only runs that ran alone, and record each run honestly with its meta. Use when demos need piloting, timing, captures for a guide, or a replay fallback.
---

# Live demo runner

Every class demo is a live run, so each must be proven fast and reliable before class, and its
captures must be real. This role alone makes model calls. The rules for honest timing are in
[honesty-and-measures.md](../../playbooks/honesty-and-measures.md); the demo rules are in section
2.4 of [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- A demo exists and has not been run live three times against its time bar.
- A guide chapter or `expected/` folder needs a fresh capture.
- The class profile or a demo setting changed and timings must be re-measured.

## Inputs

- The public release URL or the dev repository, and the commit to run.
- The demo list, in order, with each command and time bar (for example: no error, first verdict
  within about 6 minutes, full verdict within about 15).
- The budget cap for this phase, and the pilot purpose flag (`<PURPOSE FLAG>`).
- The run folder from the shared brief (`<RUN FOLDER>`), and the [meta template](templates/meta.json).

## Steps

1. **Fresh clone.** Clone the release into a new folder. Link the secrets file from its one home
   (`ln -s <SECRETS PATH> .env`); never open, print or copy it.
2. **Setup in order**: setup, doctor (must end ready), warm the images. Capture each as its own run
   folder.
3. **Pilot purpose.** Every run carries the pilot flag, so it is tagged as a pilot and never counted
   as a measured result.
4. **Budget.** Before each run, check the cumulative cost in `STATUS.md` plus the most this run can
   cost at the caps. Stop at the cap and report.
5. **Alone vs paired.** Time a demo only when it runs alone. If two demos run at once (to save wall
   time, within the heavy-job limit), record `ran: "paired with <demo>"` and do not use those times.
6. **Run and capture.** Save the exact terminal output as `terminal.txt`, host paths redacted to
   `~/...`. Fill `meta.json` from the template with the times the tool printed. Write `DONE` last.
7. **Three times per demo** against the time bar. A fail is recorded as a fail, then diagnosed; fix
   the cause test-first and run three more. Never re-run to replace a bad result.
8. **Fallback.** Keep one good run per demo as the replay fallback; note its run id for the
   instructor guide. A replay is always labelled as recorded.
9. Append each run to `STATUS.md`: demo, outcome, times, cost, cumulative cost.

## Outputs

- `<RUN FOLDER>/<demo>/terminal.txt`, `meta.json`, `DONE` for every run, including failed ones.
- `<RUN FOLDER>/STATUS.md` with the running log and total cost.
- A report: per demo the three outcomes, time ranges, cost; total spend; mechanism events seen.

## Checks

- No secret, key, host path or personal detail in any captured file.
- Every timing used on a page comes from a run marked `ran: "alone"`.
- Total spend is at or under the cap; the budget line in the report
  ([status-and-report-formats.md](../../playbooks/status-and-report-formats.md)) matches `STATUS.md`.
- No run is missing from `STATUS.md`, including errors.
