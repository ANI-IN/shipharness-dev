# Instructions checklist: what the agent knows

Source ids and finding ids are listed in `REFERENCES.md` at the repository root.
Assessment checks I1-I6 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (I1) AGENTS.md exists at the repository root. | It is injected into the agent's context at the start of every session. | A1, F-a-28 |
| [ ] | (I2) AGENTS.md is roughly 100 lines and reads as a map with pointers. | "we treat it as the table of contents"; a giant file "crowds out the task, the code, and the relevant docs". | A1, F-a-23, F-a-27, F-a-28 |
| [ ] | (I3) Every pointer in AGENTS.md resolves to a file or folder. | A1 checks that the knowledge base is "up to date, cross-linked, and structured correctly" with linters and CI jobs. | A1, F-a-37 |
| [ ] | (I4) ARCHITECTURE.md at the root maps domains and package layering. | "Architecture documentation provides a top-level map of domains and package layering." | A1, F-a-30, F-a-32 |
| [ ] | (I5) docs/ holds the detail: SECURITY.md, RELIABILITY.md, QUALITY_SCORE.md, PLANS.md, design-docs/, product-specs/, references/, exec-plans/. | "structured docs/ directory treated as the system of record". A1 gives these names in its layout figure. | A1, F-a-29, F-a-30 |
| [ ] | (I6) Skills sit in both `.claude/skills/` and `.agents/skills/` and pass the spec's validator. | No single folder is read by Claude Code, Codex, and Cursor. | B1, B7, B8, B9 |
| [ ] | Rules that live in chat threads, wikis, or people's heads are moved into the repository. | "Knowledge that lives in Google Docs, chat threads, or people’s heads are not accessible to the system." | A1, F-a-06 |
| [ ] | Code that must not be copied is marked as legacy, next to the pattern to copy instead. | "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." | A1, F-a-20 |
| [ ] | Error messages from custom checks say how to fix the problem. | "we write the error messages to inject remediation instructions into agent context." | A1, F-a-97 |
| [ ] | Each design doc records whether it is verified against the code. | Design docs are indexed "including verification status and a set of core beliefs". | A1, F-a-31 |
| [ ] | A quality document grades each domain and layer and lists known gaps. | "A quality document grades each product domain and architectural layer, tracking gaps over time." | A1, F-a-33 |

## Signs the instructions part is missing

- The agent breaks a rule that is written in a long handbook it never opened.
- The agent copies the oldest handler in the codebase because it was the first match for a search.
- AGENTS.md grows every time something goes wrong, until nobody reads it (A1: "It rots instantly.").

## Notes

- "Map" and "table of contents" are A1's words for AGENTS.md. Avoid calling it a router.
- A1 names SECURITY.md, RELIABILITY.md, PLANS.md, product-specs/, and references/*-llms.txt only in
  its layout figure. The template contents for those files are the course's, not A1's.
