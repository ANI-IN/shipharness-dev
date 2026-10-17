# Scope checklist: what the agent may change and reach

Sources are listed at the end of this page.
Assessment checks C1-C5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (C1) feature_list.json lists every feature, each starting with `"passes": false`. | The features in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) "were all initially marked as “failing” so that later coding agents would have a clear outline of what full functionality looked like." [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding) labels the file "source of truth". | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding) |
| [ ] | The list is JSON, not Markdown. | "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | (C2) Each entry has `id`, `category`, `description`, `steps`, `passes`; shipharness adds `evidence` and `testedAt`. | The sample entry in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) has category, description, steps, passes. The two extra fields are course design. | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | Agents may change only `passes`, and AGENTS.md says so in strong words. | "We prompt coding agents to edit this file only by changing the status of a passes field"; "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | Decide who sets `passes`. | In [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) the agent sets it after careful testing. shipharness moves the decision to the harness after a gate, citing [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): "Separating the agent doing the work from the agent judging it proves to be a strong lever". | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | (C3) A JSON schema describes the file, so a script can reject a malformed edit. | Structured formats for state data. | [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) |
| [ ] | One feature per session. | "work on only one feature at a time"; [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): "worked well for scope management." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | Each phase has a list of paths the agent may change; changes outside it are rejected or reverted. | [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding): "File operations restricted to the project directory only"; [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): "enforce boundaries centrally, allow autonomy locally." The per-phase list is the course's application of both. | [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding); [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (C4) Layering is enforced by code (an import-linter contract or a structural test). | "These constraints are enforced mechanically via custom linters ... and structural tests." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (C5) The agent runs in a container with no network. | "for each agent, a Docker container is spun up"; "Claude did not have internet access at any point during its development". | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | Commands outside an allowlist are blocked. | "Commands not in the allowlist are blocked by the security hook." | [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding) |

## Signs the scope part is missing

- The agent starts three features in one session and finishes none.
- A feature is marked done by editing its description to match what was built.
- The agent edits a test file in the build phase to make a failing test pass.

## Notes

- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) calls feature-list entries "tests" in its strongly-worded instruction; it means the entries,
  not unit test files.
- File presence is all the assessment can see for C5. A Dockerfile does not prove the agent runs
  inside it.

## Sources

- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11.
- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
- [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): Prithvi Rajasekaran, "Harness design for long-running application development", Anthropic, 2026-03-24.
- [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler): Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic, 2026-02-05.
- [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding): Anthropic, "Autonomous Coding Agent Demo" (README in claude-quickstarts), 2025-11-26.
- [Anthropic, Prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices): Anthropic, Claude docs, "Prompting best practices" (multi-context-window workflows).
