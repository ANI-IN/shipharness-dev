# State checklist: what the agent remembers

Source ids and finding ids are listed in `REFERENCES.md` at the repository root.
Assessment checks S1-S4 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (S1) A progress file at the root records what agents have done. | A2's initializer creates "a claude-progress.txt file that keeps a log of what agents have done". The course names it progress.md. | A2, F-a-50 |
| [ ] | progress.md has the sections Current feature, Done, In progress, Next, Session log. | A fresh session reads it, together with git history, to understand the state of the work. | A2, F-a-53; the section names are course design |
| [ ] | (S2) init.sh at the root starts the development server and runs a smoke test. | "an init.sh script that can run the development server, and then run through a basic end-to-end test before implementing a new feature." | A2, F-a-61, F-a-64 |
| [ ] | init.sh prints a few lines and writes full logs to files. | "At most, it should print a few lines of output and log all important information to a file". | A4, F-a-131 |
| [ ] | (S3) Plans for multi-step work are checked in under docs/exec-plans/active/, and move to completed/ when done. | "Active plans, completed plans, and known technical debt are all versioned and co-located". | A1, F-a-34, F-a-35 |
| [ ] | Each exec plan has Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective sections, kept current while working. | A7 requires these four living sections. | A7, F-a-48 |
| [ ] | Each exec plan is self-contained: a new session can restart from it alone. | "it should always be possible to restart from _only_ the ExecPlan and no other work." | A7, F-a-46, F-a-47 |
| [ ] | (S4) The project is a git repository and agents commit with descriptive messages. | Git lets the model "revert bad code changes and recover working states of the code base." | A2, F-a-56, F-a-57 |
| [ ] | Structured state (the feature list, test results) is JSON; notes are free text. | A6 recommends structured formats for state data and free text for progress notes. | A6, F-a-77 |

## Signs the state part is missing

- A session starts by reading half the codebase to work out what is already done.
- The next session redoes work, or adds a second migration for a table that already exists.
- Nobody can say why a decision was made, because it lived only in a past context window.

## Notes

- A2 calls the two prompts "initializer agent" and "coding agent"; they differ only in "different
  initial user prompts" (F-a-52). The shipharness state layer does the initializer's file setup in
  deterministic code because the files are fixed by the ticket.
- A6 is a living documentation page; cite it with the access date that `REFERENCES.md` records.
