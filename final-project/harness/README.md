# Module 1: Harness Engineering for Coding Agents - Final project harness

This folder holds every file the harness arm of `make final FEATURES=F5` gets from its four layers,
exactly as the agent gets them. Section by section you saw one layer at a time; here they are
together. `platform/scripts/sync_demo_harness.py` writes the folder from the layers' own code, and
`platform/tests/unit/test_demo_harness.py` fails if any file here differs from what the layers
produce. This README is the only file not written by the script.

| Layer | Files here | How the agent gets them |
|---|---|---|
| Instructions | `AGENTS.md`, `ARCHITECTURE.md`, `docs/` (except `exec-plans/`), `.agents/skills/` | Placed in the workspace; the map is in every first message |
| State | `init.sh`, `progress.md`, `session-handoff.md`, `docs/exec-plans/active/F5.md` | Placed and committed before turn 1 |
| Scope | `feature_list.json`, `feature_list.schema.json`, `scope-rules.txt` | The two JSON files are placed; `scope-rules.txt` is the scope block of the first message |
| Verification | `context-prefix.txt`, `gate-items-build.txt`, `gate-items-test.txt` | The first-message block, and the gate's checks per phase |

The same files for one section at a time are in the section demo folders, for example
[section-1-instructions/demo/harness/](../../section-1-instructions/demo/harness/) and
[section-4-verification/demo/harness/](../../section-4-verification/demo/harness/). For F6 or F7,
the state and scope files name that feature instead; the other files are the same.

To refresh the folder after a layer changes:

```bash
uv run python platform/scripts/sync_demo_harness.py
```
