# Session lifecycle checklist: how sessions start, stop, and hand over

Source ids and finding ids are listed in `docs/REFERENCES.md` in the course repository.
Assessment checks L1-L5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (L1) AGENTS.md has a "Getting up to speed" routine: run `pwd`, read the progress file and git log, read the feature list and pick the highest-priority unfinished feature. | A2's session-start steps, under the heading "Getting up to speed". | A2, F-a-58, F-a-59, F-a-60 |
| [ ] | (L4) The routine runs init.sh and a basic end-to-end test before any new work. | If the app is already broken, building a new feature on top "would likely make the problem worse." | A2, F-a-61, F-a-62 |
| [ ] | (L3) AGENTS.md says to work on one feature per session. | "the next iteration of the coding agent was then asked to work on only one feature at a time." | A2, F-a-83 |
| [ ] | (L5) AGENTS.md has an end-of-session routine: clean state, progress update, commit. | "End the session by writing a git commit and progress update." | A2, F-a-63, F-a-84 |
| [ ] | (L2) A session-handoff.md carries the state and the next steps when a session stops before the feature is done. | A3's context reset: "clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps". | A3, F-a-65 |
| [ ] | The handoff has a part written by a script (files changed, test status, last commits, open TODOs), so it exists even if the agent writes nothing. | A design choice of the course, so the next session never starts from nothing. | Course design |
| [ ] | The handoff lists approaches that failed. | A4's agents "maintain a running doc of failed approaches and remaining tasks." | A4, F-a-73 |
| [ ] | Do not rely on compaction alone to carry a long task across context windows. | "However, compaction isn’t sufficient." | A2, F-a-54, F-a-55 |

## Signs the lifecycle part is missing

- Each session starts by exploring, and spends most of its budget re-reading code.
- A session runs out of context mid-feature and leaves it "half-implemented and undocumented"
  (A2, F-a-12).
- The work log says a feature is in progress, but nobody can tell which step it stopped at.

## Notes

- Context resets are model-dependent. A3 dropped them for a later model that ran as one continuous
  session with automatic compaction (F-a-69). Use a structured handoff whenever a session can stop
  before the work is done, whatever the reason.
- "Getting up to speed" is A2's heading; avoid inventing other names for the routine.
