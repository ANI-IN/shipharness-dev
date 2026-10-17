# Harness starter kit

The kit is TeamTrack's harness, packaged as templates for your own repository: the AGENTS.md map,
the docs it points to, the state files a session reads and writes, the feature list with its
schema, house-rule checks, a sandbox policy, a CI workflow, and the four course skills. Every
template holds TeamTrack's real, working values as the example, with a REPLACE marker next to each
value that says what it means and what to write instead.

`shipharness init` copies the kit into a repository and `shipharness init --check` lists the markers
you have not filled yet. Both are deterministic: no model calls and no network. The step-by-step
guide, with a worked example on a real repository, is
[docs/apply-to-your-repo.md](../docs/apply-to-your-repo.md).

## Use it

```bash
uv run shipharness init --target <your-repo>            # copy the kit; existing files are skipped
uv run shipharness init --target <your-repo> --skills claude   # skills only in .claude/skills
uv run shipharness init --check <your-repo>             # list REPLACE markers still unfilled
```

`--target` refuses to overwrite a file that exists with other content: it prints
`! skipped <file>: exists with other content (--force overwrites)` and leaves the file alone. A
second run on the same repository writes nothing. `--check` exits 1 while markers remain and 0
when none are left; a kit file you deleted on purpose is listed as not present and does not count.

## What gets copied, and where each file comes from

| In your repository | What it is | Taken from (shipharness repository) |
|---|---|---|
| `AGENTS.md` | The map: where each rule lives, house rules at a glance, commands, the session start and end steps | `teamtrack/harness/instructions/AGENTS.md`; session steps from `src/shipharness/harness/state/lifecycle.py` |
| `ARCHITECTURE.md` | Domains, layers, what each layer may import | `teamtrack/harness/instructions/ARCHITECTURE.md` |
| `docs/SECURITY.md`, `docs/RELIABILITY.md`, `docs/QUALITY_SCORE.md`, `docs/PLANS.md` | The rules R1-R7, quality grades, plans and known debt | `teamtrack/harness/instructions/docs/` |
| `docs/design-docs/`, `docs/product-specs/`, `docs/references/` | Design decisions, product specs (the base product and F1), notes on tools | `teamtrack/harness/instructions/docs/` |
| `docs/clean-state-checklist.md` | What "ready to merge" means, as commands | `skills/harness-setup/assets/templates/clean-state-checklist.md` and `src/shipharness/harness/verify/clean_state.py` |
| `docs/house-rules.md` | How to adapt R1-R7 to your API, which adapter method each rule needs | `src/shipharness/checks/` |
| `docs/exec-plans/active/F1.md` | An exec plan, as the harness writes it for TeamTrack's F1 | `src/shipharness/harness/state/assets/exec-plan.md` |
| `feature_list.json`, `feature_list.schema.json` | The list of work (`passes`, `evidence`, `testedAt`) and its schema | `src/shipharness/harness/scope/features.py` and `scope/assets/feature_list.schema.json` |
| `progress.md`, `session-handoff.md`, `init.sh` | The session log, the structured handoff, the start script | `src/shipharness/harness/state/assets/` |
| `harness/shipharness_adapter.py`, `harness/check-params.json` | What `shipharness check` needs to know about your app | `TeamTrackAdapter` in `src/shipharness/checks/adapter.py`; `src/shipharness/checks/params.py` |
| `harness/sandbox-policy.toml` | Container limits for a coding agent | `SandboxPolicy` in `src/shipharness/sandbox/policy.py` |
| `.github/workflows/shipharness.yml` | `shipharness check` on every push; `shipharness testgen` on demand | `.github/workflows/ci.yml` and the `check` and `testgen` commands |
| `.claude/skills/<name>/`, `.agents/skills/<name>/` | harness-setup, assured-tests, house-rules, skill-template | `skills/` |

Files the harness renders at run time (progress.md, session-handoff.md, init.sh, the exec plan,
feature_list.json) were rendered with the harness's own functions for TeamTrack's feature F1. One
value is the kit's own: the six `steps` of F1, shortened from the API section of
`teamtrack/docs/features/f1.md`. In the course's A/B runs the dataset line has no `steps`, so the
state and scope layers take them from the ticket's bullet lines or, failing that, its title
(`src/shipharness/harness/scope/features.py`); the kit writes them out so you see the shape a good
step list has.

## The REPLACE markers

One form per file type, each on its own line, so `grep` finds all of them:

| File type | Marker |
|---|---|
| Markdown | `<!-- REPLACE: what the field means; the TeamTrack value is shown below it -->` |
| Shell, YAML, TOML, Python, text | `# REPLACE: ...` |
| JSON | a `"_replace": "..."` key |

`grep -rn "REPLACE:" .` and `grep -rn '"_replace"' .` find the same lines as
`shipharness init --check`. The feature list schema rejects the `_replace` key, so a feature list
that still has its note fails validation. Delete each marker line when you have replaced the value
below it, or delete the whole section or file when it does not apply to your repository.

## How the kit stays true to its sources

`tests/unit/kit/test_templates.py` compares every template with the source it was taken from: a
copied document must equal its TeamTrack source once the marker lines are removed; a rendered file
must equal a fresh rendering; the feature list and schema must match the scope layer's; the sandbox
policy must equal `SandboxPolicy()`; the adapter template must answer like `TeamTrackAdapter` and
pass the R2, R5, and R6 checks on TeamTrack (`tests/unit/checks/test_kit_adapter.py`). When a source
changes, the test names the template to recopy. Print a fresh rendering with
`uv run python -m shipharness.kit.sources progress.md` (or `init.sh`, `session-handoff.md`,
`docs/exec-plans/active/F1.md`, `feature_list.json`, `feature_list.schema.json`).

## When it fails

| Output | Fix |
|---|---|
| `x target directory not found: <dir>` | Create the repository folder first, or fix the path |
| `! skipped <file>: exists with other content (--force overwrites)` | Merge the template into your file by hand, or pass `--force` |
| `x no kit files in <dir>: run shipharness init --target <dir> first` | `--check` was pointed at a folder without the kit |
| `x <n> REPLACE markers left in <m> files` (exit 1) | Fill or delete each listed line, then run `--check` again |

More, with captured output: the "When something goes wrong" table in
[docs/apply-to-your-repo.md](../docs/apply-to-your-repo.md).

## What the kit does not do

- It writes rules down; only the checks, tests, and CI enforce them. `docs/house-rules.md` and the
  adapter template are where enforcement starts.
- It does not run sessions for you. In TeamTrack the harness sends the session start and end
  steps, writes the machine summary in the handoff, and sets `passes`; in your repository, the
  AGENTS.md map tells the agent to do those steps itself.
- It does not call a model. The first step that does is `shipharness testgen`, which costs money
  (see the guide).
