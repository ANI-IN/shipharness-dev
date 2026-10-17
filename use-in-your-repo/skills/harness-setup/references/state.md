# State checklist: what the agent remembers

Sources are listed at the end of this page.
Assessment checks `S1`-`S4` test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (`S1`) A progress file at the root records what agents have done. | The initializer in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) creates "a claude-progress.txt file that keeps a log of what agents have done". The course names it progress.md. | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | progress.md has the sections Current feature, Done, In progress, Next, Session log. | A fresh session reads it, together with git history, to understand the state of the work. | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); the section names are course design |
| [ ] | (`S2`) init.sh at the root starts the development server and runs a smoke test. | "an init.sh script that can run the development server, and then run through a basic end-to-end test before implementing a new feature." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | init.sh prints a few lines and writes full logs to files. | "At most, it should print a few lines of output and log all important information to a file". | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | (`S3`) Plans for multi-step work are checked in under docs/exec-plans/active/, and move to completed/ when done. | "Active plans, completed plans, and known technical debt are all versioned and co-located". | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | Each exec plan has Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective sections, kept current while working. | [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans) requires these four living sections. | [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans) |
| [ ] | Each exec plan is self-contained: a new session can restart from it alone. | "it should always be possible to restart from _only_ the ExecPlan and no other work." | [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans) |
| [ ] | (`S4`) The project is a git repository and agents commit with descriptive messages. | Git lets the model "revert bad code changes and recover working states of the code base." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | Structured state (the feature list, test results) is JSON; notes are free text. | [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) recommends structured formats for state data and free text for progress notes. | [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) |

## Signs the state part is missing

- A session starts by reading half the codebase to work out what is already done.
- The next session redoes work, or adds a second migration for a table that already exists.
- Nobody can say why a decision was made, because it lived only in a past context window.

## Notes

- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) calls the two prompts "initializer agent" and "coding agent"; they differ only in "different
  initial user prompts". The shipharness state layer does the initializer's file setup in
  deterministic code because the files are fixed by the ticket.
- [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) is a living documentation page; cite it with the access date that `docs/REFERENCES.md` records.

## Sources

- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11.
- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
- [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler): Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic, 2026-02-05.
- [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices): Anthropic, Claude docs, "Prompting best practices" (multi-context-window workflows).
- [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans): Aaron Friel, "Using PLANS.md for multi-hour problem solving", OpenAI Cookbook, 2025-10-07.
