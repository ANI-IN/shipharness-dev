# Troubleshooting

Find the exact text you see in the first column. Messages are copied from the code; the last column
names the file, so you can read the code that prints them. Never paste your `.env` or a key into an
issue or chat; the messages below never contain one.

Contents: [Setup](#setup) · [make doctor](#make-doctor) · [make warm](#make-warm) ·
[Running an A/B](#running-an-ab) · [Arm status and result lines](#arm-status-and-result-lines) ·
[The class profile and the Fast tier](#the-class-profile-and-the-fast-tier) ·
[Replay and swap test](#replay-and-swap-test) · [Console](#console) · [Slides](#slides) ·
[Assignments](#assignments) · [Your own repository](#your-own-repository)

## Setup

| Symptom | Cause | Fix |
|---|---|---|
| `make: command not found` | make is not installed, or you are in PowerShell on Windows | Linux and WSL2: `sudo apt install -y make`. Windows: open the Ubuntu terminal ([setup-windows.md](setup-windows.md)) |
| `uv: command not found` | The terminal started before uv was installed | Open a new terminal; check `ls ~/.local/bin/uv` |
| `! docker not found: images not built; sandboxed runs need a container runtime` (from `make setup`) | Docker is not on the `PATH` | Install a runtime ([Linux](setup-linux.md#3-install-docker-engine), [macOS](setup-macos.md)), then `make images` (source: `Makefile`) |
| `permission denied` on `/var/run/docker.sock` | Your user is not in the `docker` group yet | `sudo usermod -aG docker $USER`, then a new login (WSL: `wsl.exe --shutdown` in PowerShell) |
| `System has not been booted with systemd` (WSL) | systemd is off | [setup-windows.md](setup-windows.md#2-check-that-systemd-is-on) |
| `git tag -l 'm1-*'` prints nothing | The clone has no checkpoint tags (for example a copy made without git) | Clone the repository with `git clone`; the demos start from these tags |
| The repository path starts with `/mnt/c` (WSL) | The repository is on the Windows drive | Clone again under `~` ([setup-windows.md](setup-windows.md#4-clone-into-the-wsl-filesystem-and-run-make-setup)) |

## make doctor

Source: `src/shipharness/doctor.py`. The last line is `result: + ready` or
`result: x not ready (fix the items above)`.

| Line | Cause | Fix |
|---|---|---|
| `x missing     OPENAI_API_KEY         not set` and `next step: OPENAI_API_KEY is missing: add it to .env at the repo root` (same for `LANGSMITH_API_KEY`) | The key is not in `.env`, or `.env` is not in the repository root | Fill in `.env` in the folder that holds the `Makefile` |
| `x invalid     OPENAI_API_KEY ...` | OpenAI rejected the key | Copy the key again (no spaces or quotes); check that the account has credit bought |
| `x invalid     LANGSMITH_API_KEY ...` | LangSmith rejected the key | Create a new key; EU accounts also set `LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com` |
| `! unreachable ...` | Network or proxy problem | Try again, or from another network |
| `! warn        container runtime      docker not found: only the UNSANDBOXED fallback can run` | No Docker on the `PATH` | Install or start Docker (Linux and WSL2: `sudo systemctl start docker`) |
| `x invalid     .env not in git ...` | `.env` is tracked by git | `git rm --cached .env`, then make sure `.gitignore` still lists it |

`uv run shipharness doctor --offline` runs every check without contacting OpenAI or LangSmith; it
only tells you whether the keys are set.

## make warm

`make warm` runs `uv run shipharness warm --profile class` before class: it rebuilds the two images
through `make images` only if their source changed, starts and removes one container per image, and
caches the referee and gate baselines of the class tasks. It makes no model calls and prints one line
per step with its time (source: `src/shipharness/ab/warm.py`). In the course's class-profile round on
2026-10-17 the first run took 407 s (image rebuild 145 s, 7 referee and 4 gate baselines) and the
second 1.2 s.

| Line | Cause | Fix |
|---|---|---|
| `images: built (<image>: no record of its source; ...)` | First warm-up on this machine, or the images were built without `make warm` | None: it builds once and records the source it built from |
| `images: built (<image>: ...)` on every run | The image source (`sandbox/Dockerfile`, `src/`) changed since the last warm-up | Expected after a code change; the next run says `up to date, nothing built` |
| `x images: build failed (...)` | `make images` failed, usually because Docker is stopped | `sudo systemctl start docker`, then `make images` to see the build error |
| `x page-in failed <image>` | The image does not start a container | `make images`; check `docker image ls shipharness-agent` |
| A baseline line starting with `x` | A referee or gate baseline could not be computed | Read the line's detail; rerun `make warm` (finished baselines are cached) |
| Last line `warm: incomplete (<s> s)` | One of the steps above failed | Fix that step and rerun; class commands still work, but the first launch pays the missing step |

## Running an A/B

`make demo-N`, `make show-N`, `make final`, and `uv run shipharness ab` call OpenAI live and never
fall back to a recorded or scripted run (source: `src/shipharness/ab/commands.py`).

| Message | Cause | Fix |
|---|---|---|
| `x SHIPHARNESS_CLASS_DATE is not set: set it in .env to the class day (YYYY-MM-DD) for class commands, or pass --purpose pilot for a pilot run` | Class commands need the class date | Set `SHIPHARNESS_CLASS_DATE=<the day you run>` in `.env`, or use `PURPOSE=assignment` (traces to `shipharness-assignments`) |
| `x OPENAI_API_KEY is missing: live A/B runs call OpenAI and never fall back to a stand-in; add the key to .env (or use make replay, which shows RECORDING)` | No key | Fill in `.env`; `make doctor` |
| `x OpenAI refused the key: <reason>; no arm was started` | The key is invalid, has no access to the model, or OpenAI is unreachable | `make doctor` names the problem; the reason `no access to gpt-6-luna (NotFoundError)` means the account cannot use the course model |
| `x no task for feature=<id> example=None variant=canonical` | The feature id is not in `datasets/teamtrack-features-v1.jsonl` | Use F1 to F7 (`make final` takes F5, F6, F7) |
| `! replay needs RUN=<ab or run id>` | `make replay` without `RUN` | `make replay RUN=<id>` (source: `Makefile`) |
| `! make experiments is not a make target in this release; use uv run shipharness experiments --help or uv run shipharness report --help` (same for `report`, `pilot`) | These are not make targets in this release | Use the `uv run shipharness ...` command directly, for example `uv run shipharness report` |
| `x unknown --arms '<value>': both or harness` | `--arms` takes `both` (an A/B) or `harness` (the harness arm alone, what `make show-N` runs) | Use one of the two |
| `x unknown --profile '<value>': standard, class` | `--profile` takes `standard` or `class` | Use one of the two; `make` targets pass `PROFILE=class` by default |

## Arm status and result lines

At the end of a run the terminal prints `A/B <id> (<feature>, layers=[...], profile=<profile>)`
(with `, harness in action` for `make show-N`), one line per arm, and a cost line.

**Exit code 2 although results were printed.** `shipharness ab` exits 0 when every arm completed, 2
when an arm was aborted (`ABORTED: cap` or `ABORTED: timeout`), and 1 when an arm ended in `ERROR`.
Under make, exit 2 shows as `make: *** [Makefile:<line>: <target>] Error 2` after the cost line. The
run is complete and judged: an aborted arm is a result, scored and shown like any other. In the
course's class-profile round on 2026-10-17, the F4 A/B `ab-20261017-090903-926c02` exited 2 because
its harness arm hit the agent time limit in the test phase. `make final` keeps running its other
features and exits with the last non-zero code.

| Status or text | Cause | What it means for the result |
|---|---|---|
| `ABORTED: cap`, reason `cost cap reached: run $<x> of $0.20` (or `session $<x> of $2.50`) | A model call would have crossed a cap (source: `src/shipharness/cost/tracker.py`) | The run is still judged and shown; every run is a dot. A session cap hit stops all live runs under that class date |
| `ABORTED: timeout`, reason `agent time limit: RUN_TIMEOUT_S 300 s` | The arm used its 300 s of agent time | Judged and shown, with whatever the arm shipped |
| `ABORTED: timeout`, reason `harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during ...` | The harness work (preparation, gates) used its 120 s | Judged and shown |
| `ERROR`, `OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).` | The key stopped working mid-run (source: `src/shipharness/runner/loop.py`) | Fix the key; the run is not a measurement of the harness |
| `ERROR`, `OpenAI billing limit reached (quota or spend limit); add credit and retry.` | The OpenAI account is out of credit or at its spend limit | Add credit |
| `ERROR`, `OpenAI request kept failing after retries` | Repeated rate-limit or server errors | Try again later |
| `ERROR`, `arm setup failed: RuntimeError: docker run failed: ...` | Docker stopped, or an image is missing | `make images`; restart Docker |
| `passed=True` on a `make final` line, but low `hidden <x>/<total>` | F5-F7 have no primary measure, so `passed` is always true for them | Read the hidden-test and mutant counts ([final-project/README.md](../final-project/README.md#61-the-final-has-no-primary-measure)) |

## The class profile and the Fast tier

`PROFILE=class` (the default of `make demo-N`, `make show-N`, `make final`, and `make warm`) runs both
arms at reasoning effort `low` with 2 CPUs per arm and referee container, and asks OpenAI for the
Fast tier for the agent's calls. Fast costs twice the Standard rate per token for gpt-6-luna
(`config/prices.toml`). Each call is charged by the tier its response reports, never by the tier that
was asked for.

| Symptom | Cause | Fix |
|---|---|---|
| A class run takes much longer than usual, or costs less than the Fast rates predict | OpenAI answered some Fast requests at the Standard tier (a downgrade). Those calls report `default` and are charged the Standard rate. Check the cost ledger: `tail -n 20 .shipharness/ledger.jsonl` shows `"service_tier": "default"` on downgraded calls and `"service_tier": "fast"` on the others | Nothing to fix: the run is valid and correctly priced. The cost caps hold at either tier, because each call's worst case is held at the Fast rate before it is sent |
| Startup error naming `OPENAI_SERVICE_TIER` and a missing `[models."<model>".fast]` table | `OPENAI_SERVICE_TIER=fast` in `.env`, or the class profile, with a model that has no Fast prices in `config/prices.toml` | Use the course model, or set `PROFILE=standard` |
| You want the settings from `.env` instead (for example effort `medium`) | The class profile overrides them | Add `PROFILE=standard` to the make command |

## Replay and swap test

Source: `src/shipharness/ab/commands.py` and `src/shipharness/ab/recorded.py`.

| Message | Cause | Fix |
|---|---|---|
| ``x no recorded A/B for section demo-N under .shipharness/runs; run `make demo-N` first, or pass AB=<id>`` | `make swap-N` found no finished A/B of that section | Run the demo first, or `make swap-N AB=<ab id>` |
| `x no recorded A/B for '<id>' under .shipharness/runs; check the A/B or run id` | Wrong id | Copy the id from the console's run list |
| `x <ab id> predates checkpoint SHA pinning: ...` | The record has no pinned checkpoint commit | Use a newer recording |
| `x <id> is a single-arm run (harness in action): the swap test needs both arms; pass the id of an A/B` | The swap test was pointed at a `make show-N` run, which has the harness arm only | Pass the id of an A/B (`make demo-N` or `make final`); `make replay` works on single-arm runs |
| `Swap test on <ab id>: judged measures DIFFERENT`, then `<arm> <field>: <before> -> <after>` lines | The referee judged the same diff differently under the other label | Report it with the A/B id; the referee is meant to be deterministic for a given build |
| `make replay` asks for `SHIPHARNESS_CLASS_DATE` | `make replay` runs under `PURPOSE=class` by default | Set the class date in `.env`, or add `PURPOSE=pilot` or `PURPOSE=assignment` (replay without the reviewer makes no model calls) |
| Screen 2 of a replay shows broken images | Replay copies the diffs but not the `screenshots/` folder | `cp -a .shipharness/runs/<recorded ab id>/screenshots .shipharness/runs/<replay ab id>/`, then reload the page |

## Console

| Symptom | Cause | Fix |
|---|---|---|
| `No runs yet. Start one with make demo-1.` | Nothing under `.shipharness/runs/` (`RUNS_DIR`) of the folder where you started the console | Start `make console` from the repository root |
| The run list does not show a new A/B | The run list does not refresh by itself | Reload the page; ids start with a time stamp, newest first |
| Header shows `reconnecting` | The console server stopped | Restart `make console`, reload the page |
| Port 8765 (or 8000) already in use | Another server runs on it | `make console CONSOLE_PORT=8766`, `make up PORT=8001` |
| Screen 2: `No board screenshot yet (the preview container takes one every 5 s).` for the whole run | The board preview container did not start | Display only; the referee's board checks still run |
| Screen 4: `No exports yet` | Nothing in `exports/scores/` yet | Wait for the referee to finish the first arm |
| Screen 4 does not show a run you just made | Screen 4 shows score records of the current referee version only, and leaves out `make show-N` runs (single arm, nothing to compare with); it counts what it leaves out (`src/shipharness/console/report.py`) | Expected for show-N runs; for every record, run `uv run shipharness report` and open `exports/report.html` |
| Any screen shows `UNSANDBOXED — results not official` | `SANDBOX_MODE=none`, or no runtime was found | Fix Docker; unsandboxed results are for exploring only |

## Slides

`make slides` runs `uv run python scripts/build_slides.py`: it validates `slides/deck.md` and writes
`slides/dist/deck.html`, `deck.pdf`, and `deck.pptx`. `make slides SLIDES_OPTS=--check` validates and
lists open items without starting a browser. Exit codes (source: `scripts/build_slides.py`):

| Exit code and message | Cause | Fix |
|---|---|---|
| 2, `x <message>` lines and `<n> validation errors; nothing built` | The deck does not parse or validate | Fix the slide each message names |
| 3, `x browser step failed: ...` | The browser that renders diagrams and prints the PDF did not start | Run `uv run playwright install chromium` and build again |
| 1, `x --strict: open items remain` | `SLIDES_OPTS=--strict` and a marker or empty result slot is left | Fill the listed slots; the default build allows them |

## Assignments

| Symptom | Fix |
|---|---|
| `make check-assignment-N` exits with `Error 1` and FAIL lines on a fresh clone | Expected: the starter files have TODOs. Each FAIL line names what to fix |
| `! grade-assignment-N needs SUBMISSION=<folder or git URL>`, or `no grader for assignment N: graders are private (build repository only)` | `grade-assignment-N` is for the instructor; it needs the private graders, which are not in this repository (source: `scripts/grade_assignment.py`). Use `make check-assignment-N` |
| A live step stops at `cost cap reached` | Read the assignment's "Cost and trace budget" section; the run is still recorded and judged |

## Your own repository

| Symptom | Fix |
|---|---|
| `UNSANDBOXED: the checks import and run this app's code on this machine.` from `shipharness check` | Expected: `check` runs the app in process. Run it only on code you trust |
| `shipharness testgen` keeps no tests on a well-covered module | Filter 3 keeps a test only if it adds line coverage or kills a mutant no existing test kills; give it mutants, or pick a less covered module (`skills/assured-tests/SKILL.md`) |
| `testgen` prints UNSANDBOXED | `--sandbox local` (the default without `--image`) runs generated tests with your permissions; build an image and pass `--sandbox docker --image <image>` for code you do not trust |
| `shipharness skills validate` reports a `name` error | `name` must equal the folder name: lowercase `a-z`, `0-9`, hyphens (`skills/skill-template/README.md`) |
