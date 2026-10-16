# A map, not a manual: A1's knowledge-base section, annotated

Reading time: about 8 minutes.

Source: A1, Ryan Lopopolo (OpenAI), "Harness engineering: leveraging Codex in an agent-first world",
2026-02-11, https://openai.com/index/harness-engineering/ , sections "Agent legibility is the goal" and
"We made repository knowledge the system of record". Accessed 2026-10-16. Quotes are verbatim, with
their finding IDs; [REFERENCES.md](../../../REFERENCES.md) (generated at release) lists every finding.

Read the whole A1 section after this piece; it is short. The excerpts below follow its argument and
place each step next to the TeamTrack file that applies it.

---

## 1. The starting fact

> "From the agent’s point of view, anything it can’t access in-context while running effectively
> doesn’t exist." (F-a-05)

> "Repository-local, versioned artifacts (e.g., code, markdown, schemas, executable plans) are all it
> can see." (F-a-39)

Two separate conditions are packed in here. Knowledge has to be in the repository (F-a-06: Google Docs,
chat threads, and people's heads do not count), and it has to reach the context while the agent works.
TeamTrack's bare arm meets the first condition: `docs/HANDBOOK.md` holds every house rule. The S1 A/B
tests the second.

A1 frames the cost of failing the second condition in hiring terms: "If it isn’t discoverable to the
agent, it’s illegible in the same way it would be unknown to a new hire joining three months later."
(F-a-07).

## 2. More context, organised

> "We learned that we needed to push more and more context into the repo over time." (F-a-40)

> "organizing and exposing the right information so the agent can reason over it, rather than
> overwhelming it with ad-hoc instructions." (F-a-41)

Note the order. A1 first adds knowledge to the repository, then spends its effort on organisation.
Adding a rule is the easy half.

## 3. Why one big file fails

A1 lists four failure modes of a single large instruction file:

| A1's words | Finding | What it means in practice |
|---|---|---|
| "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs" | F-a-23 | Every token of rules competes with the ticket and the code the agent must read |
| "Too much guidance becomes non-guidance. When everything is “important,” nothing is." | F-a-24 | A rule loses weight when it sits among many others with the same emphasis |
| "It rots instantly. A monolithic manual turns into a graveyard of stale rules." | F-a-25 | Nobody owns a section, so outdated rules stay |
| "A single blob doesn’t lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable." | F-a-26 | A check cannot tell whether the R1 rule is still accurate if R1 is one paragraph among many in a file |

TeamTrack's handbook is 150 lines, not 1,000 pages, so it does not show all four. It does show the
placement problem: the "Legacy /v1 API" warning starts at line 136 of 150, after all the rules and
just before "Notes and history". An agent that reads the top of the handbook and starts coding never
reaches it.

## 4. The alternative: a table of contents

> "give Codex a map, not a 1,000-page instruction manual." (F-a-22)

> "So instead of treating AGENTS.md as the encyclopedia, we treat it as the table of contents."
> (F-a-27)

> "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with
> pointers to deeper sources of truth elsewhere." (F-a-28)

Three properties: short (roughly 100 lines), injected (always in context, no decision needed to read
it), and a map (it says where each fact lives, not the facts in full). TeamTrack's
`teamtrack/harness/instructions/AGENTS.md` is 94 lines. Its opening says it is "a table of contents,
not the manual", and its main table is keyed by what the agent is about to do ("add or change an
endpoint", "decide who may see or change data"), each row naming one file.

The course says "map" and "table of contents", A1's words. It does not call AGENTS.md a "routing
file", although the module that builds the prefix is named `router.py`.

## 5. Where the map points

> "The repository’s knowledge base lives in a structured docs/ directory treated as the system of
> record." (F-a-29)

A1's layout figure (F-a-30) puts `AGENTS.md` and `ARCHITECTURE.md` at the root, and `design-docs/`,
`exec-plans/` (`active/`, `completed/`, `tech-debt-tracker.md`), `generated/db-schema.md`,
`product-specs/`, `references/` (`*-llms.txt` files), and documents such as `PLANS.md`,
`QUALITY_SCORE.md`, `RELIABILITY.md`, and `SECURITY.md` inside `docs/`. Note that `ARCHITECTURE.md`
is at the root, not in `docs/`.

A1 describes some of these files in one sentence each:

- "Architecture documentation provides a top-level map of domains and package layering." (F-a-32)
- "A quality document grades each product domain and architectural layer, tracking gaps over time."
  (F-a-33)
- "Design documentation is catalogued and indexed, including verification status and a set of core
  beliefs that define agent-first operating principles." (F-a-31)

TeamTrack mirrors this: `docs/design-docs/index.md` and `core-beliefs.md`, `docs/QUALITY_SCORE.md`
with known gaps (including the legacy endpoint), and two `references/*-llms.txt` files for Alembic and
import-linter. A1 gives only the file names of the `*-llms.txt` references and does not explain their
format, so the course uses them as plain reference notes.

## 6. Progressive disclosure

> "This enables progressive disclosure: agents start with a small, stable entry point and are taught
> where to look next, rather than being overwhelmed up front." (F-a-36)

"Small" and "stable" both matter for the implementation. Small keeps the context free for the task.
Stable means the same text at the start of every session; in `shipharness` the prefix is built from
the course checkout, so the agent cannot change it by editing its own copy of `AGENTS.md`
(`src/shipharness/harness/instructions/router.py`). The Agent Skills specification applies the same
idea to skills; see [02-progressive-disclosure-in-agent-skills.md](02-progressive-disclosure-in-agent-skills.md).

## 7. Keeping the knowledge base true

> "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and
> structured correctly." (F-a-37)

> "A recurring “doc-gardening” agent scans for stale or obsolete documentation that does not reflect
> the real code behavior and opens fix-up pull requests." (F-a-38)

A split knowledge base has more files that can break: a renamed document leaves a dead link in the
map, and a new rule can land in the code without a doc. Mechanical checks are what make splitting
affordable. Assignment A1 asks you to write one: a checker for broken links and rule coverage across
your restructured `AGENTS.md`, docs, and skill. A1 also writes its lint messages for the agent: "we
write the error messages to inject remediation instructions into agent context." (F-a-97). A checker
message that says which rule is missing and which file should hold it does the same.

The recurring doc-gardening agent is a background run, which is Module 2 material.

## 8. Limits of the source

A1 describes one team's internal product. Its results "should not be assumed to generalize without
similar investment—at least, not yet." (F-a-143). The course takes the structure (map, system of
record, progressive disclosure, checks) from A1 and measures one effect of it on one feature with the
S1 A/B. It does not take A1's productivity numbers as a prediction.

## Why it matters for your own repo

- Count what your agent is told before it reads any code. If your instruction file is long enough
  that a rule sits at line 136 of 150, the agent has it only if it reads that far (F-a-23, F-a-24).
  Move the rule to a focused document and point to it from a short map.
- Write the map by task, not by topic: "add or change an endpoint" leads to one file. That is the
  table-of-contents idea (F-a-27) in a form an agent can act on at the moment it starts a change.
- Look at what your tickets say. Measured in the course pilot, run 2, 2026-10-16: the canonical F1
  ticket told the agent to follow the handbook, every bare arm opened it, and the two arms showed no
  difference ([../demo/README.md](../demo/README.md) sections 6 and 7 list the A/B ids). If your team
  writes "see the handbook" in every ticket, part of the map's work is already done by people, and
  it stops being done the day someone forgets the line.
- Add one mechanical check before you split anything: dead links and missing rules (F-a-26, F-a-37).
  A split knowledge base without a check drifts faster than the single file it replaced.

## Questions to take away

1. Open `teamtrack/docs/HANDBOOK.md` and `teamtrack/harness/instructions/AGENTS.md` side by side. For
   R1, how many lines does an agent read before it reaches the rule in each?
2. Which of the four failure modes in section 3 would a link checker catch, and which would it not?
