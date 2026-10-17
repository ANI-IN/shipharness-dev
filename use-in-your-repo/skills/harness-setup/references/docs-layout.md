# Docs layout

Where each harness file lives. Source ids refer to the course's docs/REFERENCES.md. The tree
follows A1's figure "In-repository knowledge store layout" (F-a-30) and adds the state and scope
files from A2, A3, and A7.

```
AGENTS.md                      map, roughly 100 lines (A1)
ARCHITECTURE.md                domains and package layering (A1)
init.sh                        start the app, run a smoke test (A2)
progress.md                    log of what agents have done (A2: claude-progress.txt)
session-handoff.md             structured handoff between sessions (A3)
feature_list.json              list of work, passes per feature (A2, A5)
feature_list.schema.json       schema for the list (course addition)
docs/
  SECURITY.md                  security rules (name from A1)
  RELIABILITY.md               reliability rules (name from A1)
  QUALITY_SCORE.md             grade per domain and layer (A1)
  PLANS.md                     how to write an exec plan (A1, A7)
  clean-state-checklist.md     definition of clean state (A2; course file)
  design-docs/
    index.md                   design decisions, verification status, core beliefs (A1)
  exec-plans/
    active/<feature>.md        living plans for work in progress (A1, A7)
    completed/<feature>.md     finished plans (A1)
    tech-debt-tracker.md       known technical debt (A1)
  generated/
    db-schema.md               generated from the code, never edited by hand (A1)
  product-specs/
    index.md                   what the product does (A1)
  references/
    <library>-llms.txt         notes on a library, written for agents (name pattern from A1)
.agents/skills/<name>/SKILL.md skills for Codex and Cursor (B3, B8, B9)
.claude/skills/<name>/SKILL.md skills for Claude Code and Cursor (B7, B9)
```

## What each source says about the layout

| File or folder | What the source says | Source |
|---|---|---|
| AGENTS.md | Injected into context, "serves primarily as a map, with pointers to deeper sources of truth elsewhere." | A1, F-a-28 |
| ARCHITECTURE.md | At the root; "a top-level map of domains and package layering." | A1, F-a-32 |
| docs/ | "treated as the system of record." | A1, F-a-29 |
| design-docs/ | "catalogued and indexed, including verification status and a set of core beliefs". | A1, F-a-31 |
| QUALITY_SCORE.md | "grades each product domain and architectural layer, tracking gaps over time." | A1, F-a-33 |
| exec-plans/ | Plans "with progress and decision logs that are checked into the repository". | A1, F-a-34, F-a-35 |
| SECURITY.md, RELIABILITY.md, PLANS.md, product-specs/, references/ | Names only, from the layout figure. A1 does not describe their contents. | A1, F-a-30 |
| init.sh, progress file, feature list | Created by A2's initializer agent before the first coding session. | A2, F-a-50, F-a-78 |
| session-handoff.md | A3's "structured handoff". The file name is the course's. | A3, F-a-65 |

## Rules for the layout

- Keep AGENTS.md and ARCHITECTURE.md at the root; everything else under docs/ (A1).
- Prefer a short file per topic over one long file. Agents load what they need, when they need it
  (A1, F-a-36: "agents start with a small, stable entry point and are taught where to look next").
- Generated files say so at the top and are rebuilt by a script, not edited by agents.
