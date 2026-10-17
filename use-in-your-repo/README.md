# Use the harness in your own repository

Everything in this folder is meant to leave the course and go into a repository of your own:

| What | Where | What it gives you |
|---|---|---|
| The starter kit | [kit/](kit/README.md) | TeamTrack's harness as templates: the AGENTS.md map, the docs it points to, the state files, the feature list and its schema, house-rule checks, a sandbox policy, and a CI workflow; `uv run shipharness init --target <your-repo>` copies it, with a worked example on boltons |
| harness-setup | [skills/harness-setup/](skills/harness-setup/README.md) | A skill that assesses a repository's harness (instructions, state, scope, verification, session lifecycle) with a read-only script that writes an HTML report, then adds the missing parts from templates |
| assured-tests | [skills/assured-tests/](skills/assured-tests/README.md) | A skill that generates unit tests for one Python module and keeps only the tests that pass five filters |
| house-rules | [skills/house-rules/](skills/house-rules/README.md) | A skill that turns a team convention into a house rule: a rule document, a mechanical check, and a test with a seeded violation |
| skill-template | [skills/skill-template/](skills/skill-template/README.md) | A starting point for a skill of your own |
| The guide | [apply-to-your-repo.md](apply-to-your-repo.md) | Step by step: install, copy the kit, fill in the map, define house rules, run the first harnessed command, read the results |

Start with the guide; it uses the kit and the skills in order.
