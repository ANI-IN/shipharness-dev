# Governing brief template

The governing brief is the owner's instruction for one phase of work (a day, a night, a review
round). Every agent and the lead read it first; the newest brief governs where two differ. Keep it
on one page. Save it in the course's private engineering notes as
`<YYYY-MM-DD>-<phase>.md`, word for word, and record each decision taken under it next to it.

Copy the block below and fill every `<...>`.

```markdown
# <PHASE NAME> (owner message, <YYYY-MM-DD> <time>)

Work autonomously; don't ask between stop points. Record every decision and its reason in
<ENGINEERING NOTES PATH>. ONE final report at the end, in chat.

## Goals
1. <GOAL 1: the outcome, not the activity, e.g. "every demo passes its time bar three times live">
2. <GOAL 2>
3. <GOAL 3>
Top priority if time runs short: <GOAL N>.

## Hard rules
- SECRETS: never open, print, copy or screenshot <SECRETS FILE> or any key. Secret scan of the
  working tree and the full history before every push.
- IDENTITY: every commit by <OWNER IDENTITY>; no co-author or "generated with" lines anywhere.
- BUDGET: model spend this phase at most <$X> (build cap <$Y>). Only <ROLE> makes model calls.
- HEAVY JOBS: at most <N> at once (live runs, containers, full test suites). If the machine
  hangs: restart, verify the repository (status, fsck), resume.
- HONESTY: never change a pre-registered measure, pick or drop runs, or edit captured output.
  Report failures as measured. Disclose any setting change with date and reason.
- DON'T: <things never to touch, e.g. delete old copies, rename repositories, push to main>.

## Deliverables
1. <AREA>: <exact output, where it lives, how it is checked>
2. <AREA>: <...>
FINISH: style strict, prose lint, link check, fast suite, full suite once, release dry run,
contributor check, secret scan; CI green on both repositories; refresh the test copy.

## Stop points
Stop and wait only at:
- ⏸ <publishing / deleting or renaming repositories / spend beyond budget / changing a primary measure>
- ⏸ <phase-specific approval, e.g. slide Markdown before any deck is built>
Everything else: decide with the existing rules, record the decision, continue.

## Report format
Final report in chat, in this order: changes per area; live results and timings; bugs fixed;
links checked; not done and why; repository and CI status; decisions for you; budget line.
```

## Goals

Write outcomes a reviewer can check yes or no ("each demo 3 times live, all within the time bar"),
not activities ("work on demos"). Number them; name the top priority, so a short night still
delivers the most important one. Keep a goal per area: content, demos, slides, release.

## Hard rules

Five rules appear in every brief, because each one, once broken, costs more than the phase:

| Rule | Why it is fixed |
|---|---|
| Secrets | A key in an image, terminal render or commit cannot be taken back after a push |
| Identity | A public repository with a second contributor or attribution lines must be rebuilt |
| Budget | Model spend is the only cost that grows without anyone watching |
| Heavy-job limit | Too many containers or suites at once hang the machine and lose the night |
| Honesty | A re-run or edited result invalidates every number in the course |

Write each with the exact number or path, never "be careful with spend". See
[honesty-and-measures.md](honesty-and-measures.md) for the honesty rules in full.

## Deliverables

One numbered line per area, each naming the output file or folder and the check that proves it
done. End with the FINISH line, the checks run once on the combined tree
([merge-and-verify.md](merge-and-verify.md)).

## Stop points

Mark each with ⏸. Four stop points cover a whole course build (see section 4.2 of the
[structure guide](../STRUCTURE-AND-TASTE.md)): project and sections approval, design approval,
slide Markdown review, publish. A phase brief adds its own only when the owner must see something
before work can continue. Between stop points, agents answer their own questions from the rules.

## Report format

Name the sections of the final report in order and require the budget line. The formats are in
[status-and-report-formats.md](status-and-report-formats.md). Reports go in chat, not into report
files, unless the owner asks for a file.
