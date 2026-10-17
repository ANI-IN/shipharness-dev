# Instructions checklist: what the agent knows

Sources are listed at the end of this page.
Assessment checks I1-I6 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (I1) AGENTS.md exists at the repository root. | It is injected into the agent's context at the start of every session. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (I2) AGENTS.md is roughly 100 lines and reads as a map with pointers. | "we treat it as the table of contents"; a giant file "crowds out the task, the code, and the relevant docs". | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (I3) Every pointer in AGENTS.md resolves to a file or folder. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) checks that the knowledge base is "up to date, cross-linked, and structured correctly" with linters and CI jobs. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (I4) ARCHITECTURE.md at the root maps domains and package layering. | "Architecture documentation provides a top-level map of domains and package layering." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (I5) docs/ holds the detail: SECURITY.md, RELIABILITY.md, QUALITY_SCORE.md, PLANS.md, design-docs/, product-specs/, references/, exec-plans/. | "structured docs/ directory treated as the system of record". [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) gives these names in its layout figure. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (I6) Skills sit in both `.claude/skills/` and `.agents/skills/` and pass the spec's validator. | No single folder is read by Claude Code, Codex, and Cursor. | [Agent Skills, Specification](https://agentskills.io/specification); [Claude Code, Skills](https://code.claude.com/docs/en/skills); [Codex, Skills](https://learn.chatgpt.com/docs/build-skills); [Cursor, Skills](https://cursor.com/docs/skills) |
| [ ] | Rules that live in chat threads, wikis, or people's heads are moved into the repository. | "Knowledge that lives in Google Docs, chat threads, or people’s heads are not accessible to the system." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | Code that must not be copied is marked as legacy, next to the pattern to copy instead. | "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | Error messages from custom checks say how to fix the problem. | "we write the error messages to inject remediation instructions into agent context." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | Each design doc records whether it is verified against the code. | Design docs are indexed "including verification status and a set of core beliefs". | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | A quality document grades each domain and layer and lists known gaps. | "A quality document grades each product domain and architectural layer, tracking gaps over time." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |

## Signs the instructions part is missing

- The agent breaks a rule that is written in a long handbook it never opened.
- The agent copies the oldest handler in the codebase because it was the first match for a search.
- AGENTS.md grows every time something goes wrong, until nobody reads it ([OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): "It rots instantly.").

## Notes

- "Map" and "table of contents" are the words [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) uses for AGENTS.md. Avoid calling it a router.
- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) names SECURITY.md, RELIABILITY.md, PLANS.md, product-specs/, and references/*-llms.txt only in
  its layout figure. The template contents for those files are the course's, not from [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/).

## Sources

- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11.
- [Agent Skills, Specification](https://agentskills.io/specification): Agent Skills project, "Agent Skills Specification".
- [Claude Code, Skills](https://code.claude.com/docs/en/skills): Anthropic, Claude Code docs, "Extend Claude with skills".
- [Codex, Skills](https://learn.chatgpt.com/docs/build-skills): OpenAI, Codex docs, "Build skills" (redirected from https://developers.openai.com/codex/skills).
- [Cursor, Skills](https://cursor.com/docs/skills): Cursor docs, "Agent Skills" (redirected from https://cursor.com/docs/context/skills).
