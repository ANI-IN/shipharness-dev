# post-class-reading

Short pieces that go further than the 50 minutes of class allow. Each one quotes the primary sources
verbatim, with finding IDs (listed in [REFERENCES.md](../../../REFERENCES.md), generated at release),
and ties them to TeamTrack and `shipharness` code. Read them in order; together they take about 21 minutes. Each ends with a
section "Why it matters for your own repo".

| Piece | Reading time | What it covers | Sources |
|---|---|---|---|
| [01-map-not-manual.md](01-map-not-manual.md) | about 8 minutes | A1's knowledge-base section, annotated: why one big instruction file fails, AGENTS.md as a table of contents, docs/ as the system of record, progressive disclosure, mechanical checks on docs | A1 |
| [02-progressive-disclosure-in-agent-skills.md](02-progressive-disclosure-in-agent-skills.md) | about 7 minutes | The Agent Skills specification: frontmatter rules, the three tiers, client guidance, the reference validator, and how `SkillsLoader` maps each rule to code | B1, B2, B3, B5, B6 |
| [03-instructions-in-other-agents.md](03-instructions-in-other-agents.md) | about 6 minutes | How instructions reach the agent in A1's and A2's harnesses, and where Claude Code, Codex, and Cursor look for skills | A1, A2, B7-B10 |

After reading, read the primary sources themselves, starting with A1's section "We made repository
knowledge the system of record" and B1's section on progressive disclosure. Pilot results for S1
are in [../demo/README.md](../demo/README.md) (sections 9, 10, and 11). The planned experiment
batches were not run, because the pre-registered pilot gate did not pass. The class recap is in
[../session-notes.md](../session-notes.md).
