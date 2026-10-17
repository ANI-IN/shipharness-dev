# Docs layout

Where each harness file lives. Sources are listed at the end of this page. The tree
follows the figure "In-repository knowledge store layout" in [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) and adds the state and scope
files from [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps), and [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans).

```
AGENTS.md                      map, roughly 100 lines (OpenAI, Harness engineering)
ARCHITECTURE.md                domains and package layering (OpenAI, Harness engineering)
init.sh                        start the app, run a smoke test (Anthropic, Effective harnesses)
progress.md                    log of what agents have done (Anthropic, Effective harnesses: claude-progress.txt)
session-handoff.md             structured handoff between sessions (Anthropic, Harness design)
feature_list.json              list of work, passes per feature (Anthropic, Effective harnesses; Anthropic, Autonomous coding demo)
feature_list.schema.json       schema for the list (course addition)
docs/
  SECURITY.md                  security rules (name from OpenAI, Harness engineering)
  RELIABILITY.md               reliability rules (name from OpenAI, Harness engineering)
  QUALITY_SCORE.md             grade per domain and layer (OpenAI, Harness engineering)
  PLANS.md                     how to write an exec plan (OpenAI, Harness engineering; OpenAI, Exec plans)
  clean-state-checklist.md     definition of clean state (Anthropic, Effective harnesses; course file)
  design-docs/
    index.md                   design decisions, verification status, core beliefs (OpenAI, Harness engineering)
  exec-plans/
    active/<feature>.md        living plans for work in progress (OpenAI, Harness engineering; OpenAI, Exec plans)
    completed/<feature>.md     finished plans (OpenAI, Harness engineering)
    tech-debt-tracker.md       known technical debt (OpenAI, Harness engineering)
  generated/
    db-schema.md               generated from the code, never edited by hand (OpenAI, Harness engineering)
  product-specs/
    index.md                   what the product does (OpenAI, Harness engineering)
  references/
    <library>-llms.txt         notes on a library, written for agents (name pattern from OpenAI, Harness engineering)
.agents/skills/<name>/SKILL.md skills for Codex and Cursor (Agent Skills, Client guide; Codex, Skills; Cursor, Skills)
.claude/skills/<name>/SKILL.md skills for Claude Code and Cursor (Claude Code, Skills; Cursor, Skills)
```

## What each source says about the layout

| File or folder | What the source says | Source |
|---|---|---|
| AGENTS.md | Injected into context, "serves primarily as a map, with pointers to deeper sources of truth elsewhere." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| ARCHITECTURE.md | At the root; "a top-level map of domains and package layering." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| docs/ | "treated as the system of record." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| design-docs/ | "catalogued and indexed, including verification status and a set of core beliefs". | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| QUALITY_SCORE.md | "grades each product domain and architectural layer, tracking gaps over time." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| exec-plans/ | Plans "with progress and decision logs that are checked into the repository". | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| SECURITY.md, RELIABILITY.md, PLANS.md, product-specs/, references/ | Names only, from the layout figure. [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) does not describe their contents. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| init.sh, progress file, feature list | Created by the initializer agent in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) before the first coding session. | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| session-handoff.md | The "structured handoff" in [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps). The file name is the course's. | [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |

## Rules for the layout

- Keep AGENTS.md and ARCHITECTURE.md at the root; everything else under docs/ ([OpenAI, Harness engineering](https://openai.com/index/harness-engineering/)).
- Prefer a short file per topic over one long file. Agents load what they need, when they need it
  ([OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): "agents start with a small, stable entry point and are taught where to look next").
- Generated files say so at the top and are rebuilt by a script, not edited by agents.

## Sources

- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11.
- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
- [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): Prithvi Rajasekaran, "Harness design for long-running application development", Anthropic, 2026-03-24.
- [Anthropic, Autonomous coding demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding): Anthropic, "Autonomous Coding Agent Demo" (README in claude-quickstarts), 2025-11-26.
- [OpenAI, Exec plans](https://cookbook.openai.com/articles/codex_exec_plans): Aaron Friel, "Using PLANS.md for multi-hour problem solving", OpenAI Cookbook, 2025-10-07.
- [Agent Skills, Client guide](https://agentskills.io/client-implementation/adding-skills-support.md): Agent Skills project, "How to add skills support to your agent".
- [Claude Code, Skills](https://code.claude.com/docs/en/skills): Anthropic, Claude Code docs, "Extend Claude with skills".
- [Codex, Skills](https://learn.chatgpt.com/docs/build-skills): OpenAI, Codex docs, "Build skills" (redirected from https://developers.openai.com/codex/skills).
- [Cursor, Skills](https://cursor.com/docs/skills): Cursor docs, "Agent Skills" (redirected from https://cursor.com/docs/context/skills).
