# Session lifecycle checklist: how sessions start, stop, and hand over

Sources are listed at the end of this page.
Assessment checks L1-L5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (L1) AGENTS.md has a "Getting up to speed" routine: run `pwd`, read the progress file and git log, read the feature list and pick the highest-priority unfinished feature. | The session-start steps in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), under the heading "Getting up to speed". | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | (L4) The routine runs init.sh and a basic end-to-end test before any new work. | If the app is already broken, building a new feature on top "would likely make the problem worse." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | (L3) AGENTS.md says to work on one feature per session. | "the next iteration of the coding agent was then asked to work on only one feature at a time." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | (L5) AGENTS.md has an end-of-session routine: clean state, progress update, commit. | "End the session by writing a git commit and progress update." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | (L2) A session-handoff.md carries the state and the next steps when a session stops before the feature is done. | The context reset in [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): "clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps". | [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | The handoff has a part written by a script (files changed, test status, last commits, open TODOs), so it exists even if the agent writes nothing. | A design choice of the course, so the next session never starts from nothing. | Course design |
| [ ] | The handoff lists approaches that failed. | The agents in [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) "maintain a running doc of failed approaches and remaining tasks." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | Do not rely on compaction alone to carry a long task across context windows. | "However, compaction isn’t sufficient." | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |

## Signs the lifecycle part is missing

- Each session starts by exploring, and spends most of its budget re-reading code.
- A session runs out of context mid-feature and leaves it "half-implemented and undocumented"
  ([Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- The work log says a feature is in progress, but nobody can tell which step it stopped at.

## Notes

- Context resets are model-dependent. [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) dropped them for a later model that ran as one continuous
  session with automatic compaction. Use a structured handoff whenever a session can stop
  before the work is done, whatever the reason.
- "Getting up to speed" is the heading in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); avoid inventing other names for the routine.

## Sources

- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
- [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): Prithvi Rajasekaran, "Harness design for long-running application development", Anthropic, 2026-03-24.
- [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler): Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic, 2026-02-05.
