# Reference

> **Terms on this page**
>
> - **Bare arm**: an agent run with the ticket and the repository, and no harness.
> - **Harness arm**: the same run with the harness turned on.
> - **A/B**: bare arm and harness arm on the same ticket, scored the same way.
> - **Referee**: the program that scores each run after the agent stops.
> - **Class profile**: the settings the live class runs use, the same for both arms (below).
> - **Class date**: the class day in `.env`, which names the LangSmith project and keys the session cap.

This page lists everything you look up but do not read in order: every make target, every setting
and variable, the caps and limits, and the folders. Each table names the file its values come from.

## Make targets

Every target is a thin wrapper over `uv run ...` (`Makefile`). On Windows, run make inside Ubuntu
on WSL2. The "Runs" column is what `make -n <target>` prints. `make help` prints a short list:

> Your output will differ: run times, ids, and the agent's wording change on every run.

```text
setup doctor up console datasets lint format lint-prose test test-all test-live test-docker
demo-N [LAYERS=-<layer>]  show-N  swap-N [AB=<id>]  final [FEATURES=F5,F6]  replay RUN=<id>
warm (before class: images, containers, referee and gate baselines; no model calls)
experiments and reports: uv run shipharness experiments --help; uv run shipharness report --help
```

### Setup and checks (no model calls)

| Target | Runs | What it does |
|---|---|---|
| `make setup` | `uv sync --frozen`, then `make images` | Installs the pinned packages, builds both images, copies `.env.example` to `.env` if missing |
| `make images` | `docker build -f platform/sandbox/Dockerfile ...` | Builds `shipharness-agent:1` and `shipharness-referee:1` |
| `make doctor` | `uv run shipharness doctor --purpose class` | Checks tools, Docker, both keys, prices, and the class date |
| `make warm` | `uv run shipharness warm --purpose class --profile class ...` | Rebuilds changed images, starts each once, caches the baselines |
| `make up` | `uv run shipharness up --port 8000` | TeamTrack and its board on http://127.0.0.1:8000/board |
| `make console` | `uv run shipharness console --port 8765` | The live console on http://127.0.0.1:8765/ |
| `make datasets` | `uv run shipharness datasets upload` | Uploads the two datasets to LangSmith once (Assignment 1 needs them) |

`make doctor` lists OpenAI models to test the key, which uses no tokens. With `PURPOSE=class`,
`make doctor` and `make warm` stop with a clear message when the class date is missing.

### Live runs (call OpenAI)

These call OpenAI live and never fall back to a recording. Each prints a `Cost:` line at the end.

| Target | Runs | What it does | At most, at the caps |
|---|---|---|---|
| `make show-1` to `make show-4` | `uv run shipharness ab --section demo-N --feature FN --arms harness ...` | The harness arm alone, judged by the referee | $0.24 |
| `make demo-1` to `make demo-4` | `uv run shipharness ab --section demo-N --feature FN ...` | A/B: both arms, both judged | $0.48 |
| `make demo-3 FEATURE=F4` | `uv run shipharness ab --section demo-3 --feature F4 ...` | The Section 3 live A/B in class | $0.48 |
| `make final` | one `uv run shipharness ab --section final --feature <f> ...` per feature | One A/B per feature in `FEATURES` | $0.58 per feature |

The worst cases come from the caps in `.env.example`: one arm $0.20 plus one review $0.04; a final
arm $0.25. A `make show-N` run is not an A/B, so its score stays out of every comparison, out of
screen 4, and out of `make swap-N`. Exit codes: 0 when every arm completed, 2 when an arm was
aborted (cost cap or time limit; still judged and shown), 1 on an error.

### Replays and re-judging (no model calls)

| Target | Runs | What it does |
|---|---|---|
| `make swap-1` to `make swap-4` | `uv run shipharness ab --swap latest --section demo-N ...` | Re-judges the latest A/B with the labels swapped (`AB=<id>` picks another) |
| `make replay RUN=<id>` | `uv run shipharness replay <id> --purpose class` | Replays a recorded run with RECORDING on every screen and judges it again |
| `make example-1` to `make example-4` | `uv run shipharness example --section demo-N --profile class` | Optional extra: scripted steps, no model ([extras](extras.md)) |

### Assignments, slides, and tests

| Target | Runs | What it does |
|---|---|---|
| `make check-assignment-1` to `-4` | `uv run python section-N-*/assignment/check.py` | Offline self-check of your work |
| `make grade-assignment-1` to `-4` | `uv run python platform/scripts/grade_assignment.py N "<SUBMISSION>"` | The instructor's grader; the graders are not in this repository |
| `make slides` | `uv run python platform/scripts/build_slides.py` | Builds `slides/dist/deck.html`, `.pdf`, and `.pptx` (needs Playwright's Chromium) |
| `make test` | `uv run pytest` | The fast suite |
| `make test-all` | `uv run pytest -n auto -m "not live and not docker"` | Every test that needs no key and no container |
| `make test-live` | `uv run pytest -m live platform/tests/live` | Tests that call OpenAI and LangSmith |
| `make test-docker` | `uv run pytest -m docker platform/tests/unit/test_sandbox_docker.py` | Sandbox tests in real containers |
| `make lint` | ruff, the import contract, anchors, skills validation | Code checks |
| `make format` | `uv run ruff check --fix .`, `uv run ruff format .` | Rewrites files |
| `make lint-prose` | `uv run python platform/scripts/lint_prose.py` | Banned words and emoji in the course pages |
| `make anchors` | `uv run python platform/scripts/anchors.py list` | Lists the code walkthrough anchors |

`make experiments` and `make report` show the options of `uv run shipharness experiments` and
`uv run shipharness report`; run those commands directly with the options you need.

### Other commands

| Command | What it does | Model calls |
|---|---|---|
| `uv run shipharness report` | Writes `exports/report.html` from `exports/` | None |
| `uv run shipharness verify --tag class-v1` | Checks that your copy matches the class release tag | None |
| `uv run shipharness init --target <your-repo>` | Copies the starter kit into your repository | None |
| `uv run shipharness testgen ...` | Proposes tests for one module and keeps those that pass five filters | Yes, at most $0.20 |
| `uv run shipharness check ...` | House-rule checks for a FastAPI app; exit 3 on new violations | None |
| `uv run shipharness skills validate <dir>` | Validates Agent Skills folders | None |

`uv run shipharness --help` lists every command. In `init`, `<your-repo>` is the path to a
repository of yours.

### The console

`make console`, then open http://127.0.0.1:8765/ and click a run. Press `1` to `5` to switch
screens and `F` to show one arm full width (both, bare, harness).

| Key | Screen | What it shows |
|---|---|---|
| `1` | Live | Each arm's turns, cost, harness decisions, the gate, and the verdict |
| `2` | Boards | Each arm's running board as an Acme user, every 5 s |
| `3` | Evidence | Files read, the diff map, sandbox denials, the referee's checks, mutants |
| `4` | A/B report | One dot per run for each feature and arm, reviewer agreement |
| `5` | Traces | A live tail of events and the LangSmith trace links |

A replay shows a red `● RECORDING` badge on every screen. A run without a sandbox shows
`⚠ UNSANDBOXED — results not official`.

## Settings and variables

### Make variables

Defaults from the `Makefile`.

| Variable | Default | Used by | Meaning |
|---|---|---|---|
| `PURPOSE` | `class` | live runs, swap, replay, doctor, warm | LangSmith project and cost session (table below) |
| `PROFILE` | `class` | live runs, examples, warm | `class` or `standard` (the settings in `.env`) |
| `FEATURE` | `F3` | demo-3 | `F4` runs the Section 3 class A/B |
| `FEATURES` | `F5,F6` | final | Comma-separated final features, for example `F6` |
| `LAYERS` | empty | demo-N, show-N, final | `-<layer>` removes one layer, for example `-state` |
| `SESSION_BUDGET` | empty | demo-N, show-N | Session turn budgets, for example `12,38` |
| `AB` | `latest` | swap-N | The A/B or run id to re-judge |
| `RUN` | empty | replay | The A/B or run id to replay (required) |
| `SUBMISSION` | empty | grade-assignment-N | Folder or git URL (instructor only) |
| `A1_WORK`, `A2_IMPL`, `A3_IMPL`, `A4_IMPL` | the starter | check-assignment-N | Your work folder |
| `SLIDES_OPTS` | empty | slides | `--check` validates only; `--strict` fails on open items |
| `PORT`, `CONSOLE_PORT` | `8000`, `8765` | up, console | Server ports |
| `RUNTIME` | `docker` | setup, images, warm | `podman` also works (set `SANDBOX_RUNTIME=podman` too) |
| `UV` | `uv` | every target | The uv command |

### The class profile

`PROFILE=class` is the default of the live targets and `make warm`. It sets the same values for
both arms (`platform/src/shipharness/config/profiles.py`):

| Setting | Class profile | Standard profile (`.env`) |
|---|---|---|
| Reasoning effort, agent | `low` | `OPENAI_REASONING_EFFORT` (`medium`) |
| OpenAI service tier, agent | Fast | `OPENAI_SERVICE_TIER` (`auto`) |
| CPUs per container | 2 | `SANDBOX_CPUS` (`1.0`) |
| Agent time limit per arm | 420 s | `RUN_TIMEOUT_S` (300 s) |

The reviewer keeps `OPENAI_EVAL_REASONING_EFFORT` and the Standard tier. Each call is charged by the
tier its response reports: a Fast request answered at the Standard tier is charged the Standard
rate, and `.shipharness/ledger.jsonl` records the tier. The referee also runs the primary measure's
checks first, so the primary verdict shows early, and re-runs each shipped test five times for
flakiness.

### The class date

`SHIPHARNESS_CLASS_DATE` in `.env` is the class day as `YYYY-MM-DD`. It names the LangSmith project
`shipharness-class-<date>`, and every command under one date shares one session cap. Live runs,
`make replay`, `make doctor`, and `make warm` with `PURPOSE=class` refuse to start without it. Set it
to the day you run the commands, or use another purpose:

| `PURPOSE` | LangSmith project | Cost session |
|---|---|---|
| `class` | `shipharness-class-<date>` | One per class date |
| `pilot` | `shipharness-pilot` | One, named `pilot` |
| `assignment` | `shipharness-assignments` | One, named `assignment` |

### Settings in `.env`

`make setup` copies `.env.example` to `.env`. The ones you may change:

| Setting | Default | Meaning |
|---|---|---|
| `OPENAI_API_KEY`, `LANGSMITH_API_KEY` | empty | Required; never printed, logged, traced, or passed into a container |
| `OPENAI_MODEL`, `OPENAI_EVAL_MODEL` | `gpt-6-luna`, `gpt-5.6-luna` | Agent and reviewer models |
| `LANGSMITH_ENDPOINT` | `https://api.smith.langchain.com` | EU accounts: `https://eu.api.smith.langchain.com` |
| `SANDBOX_MODE` | `docker` | `none` runs commands on the host, labelled UNSANDBOXED |
| `RUNS_DIR`, `EXPORTS_DIR` | `.shipharness/runs`, `exports` | Where runs and score records go |

## Caps and limits

The cost tracker checks every model call against these caps before it is sent
(`.env.example`). When a call would cross a cap, the run ends as `ABORTED: cap`, and the referee
still judges and shows it. Commands running at the same time share the caps.

| Cap | Value | Scope |
|---|---|---|
| `MAX_RUN_COST_USD` | $0.20 | One arm of one run; also one `testgen` run |
| `MAX_FINAL_RUN_COST_USD` | $0.25 | One arm of one `make final` run |
| `MAX_REVIEW_COST_USD` | $0.04 | One blinded review |
| `MAX_SESSION_COST_USD` | $2.50 | Every command under one class date or purpose |
| `MAX_BATCH_COST_USD` | $2.50 | Any single command |
| `MAX_EXPERIMENT_TOTAL_USD` | $25.00 | All `shipharness experiments` batches |
| `MAX_BUILD_TOTAL_USD` | $15.00 | Every model call in this machine's cost ledger |

Time and turn limits (`.env.example`; the class profile changes the agent time limit only):

| Limit | Value | Scope |
|---|---|---|
| `RUN_TIMEOUT_S` | 300 s (class profile 420 s) | Agent time per arm per run |
| `HARNESS_TIMEOUT_S` | 120 s | Harness work per arm per run |
| `TOOL_TIMEOUT_S` | 120 s | One tool command |
| `MAX_TURNS_PER_SESSION` | 30 | Turns per session unless the task sets its own budget |

Prices per 1M tokens (`platform/config/prices.toml`):

| Model and tier | Input | Cached input | Output |
|---|---|---|---|
| gpt-6-luna, Standard | $0.10 | $0.01 | $0.50 |
| gpt-6-luna, Fast | $0.20 | $0.02 | $1.00 |
| gpt-5.6-luna (reviewer), Standard | $0.20 | $0.02 | $1.20 |

Cache writes cost $0.125, $0.25, and $0.25 per 1M tokens in the same order. At the caps, the class
plan (three `make show-N` runs, one `make demo-3`, two final features) needs at most $2.36, under the
$2.50 session cap. Measured costs of each class command are on the
[evidence page](evidence/general.md#timings). The four assignments together are planned at no more
than $6 of OpenAI usage and 400 LangSmith traces.

## Folders

| Folder | What it holds |
|---|---|
| `setup/` | First-time setup for Windows, macOS, and Linux |
| `section-1-instructions/` to `section-4-verification/` | One folder per section: concepts, demo, assignment, reading, session notes |
| `final-project/` | The whole harness on a new feature, then your own repository |
| `slides/` | The deck source and its builder |
| `use-in-your-repo/` | The starter kit (`kit/`), four skills (`skills/`), and the guide |
| `docs/` | This page, the instructor guide, troubleshooting, architecture, evidence |
| `platform/src/shipharness/` | The command-line tool: runner, harness layers, referee, console |
| `platform/teamtrack/` | The app the agent works on, with its tests and features |
| `platform/sandbox/` | The Dockerfile for the agent and referee images |
| `platform/config/` | `prices.toml` |
| `platform/datasets/` | The TeamTrack tasks and the test-generation targets |
| `platform/scripts/`, `platform/tests/` | Course scripts and the test suite |

Files that runs write: `.shipharness/runs/<ab id>/` (run log, diffs, board screenshots),
`.shipharness/ledger.jsonl` (one line per model call), and `exports/scores/` (one score record per
arm). All three are git-ignored. More detail: [architecture](architecture.md).
