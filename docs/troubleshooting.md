# Troubleshooting

Find the exact text you see in the first column. Messages are copied from the code; the last column
names the file, so you can read the code that prints them. Never paste your `.env` or a key into an
issue or chat; the messages below never contain one.

Contents: [Setup](#setup) · [make doctor](#make-doctor) · [Running an A/B](#running-an-ab) ·
[Arm status and result lines](#arm-status-and-result-lines) ·
[Replay and swap test](#replay-and-swap-test) · [Console](#console) ·
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

## Running an A/B

`make demo-N`, `make final`, and `uv run shipharness ab` call OpenAI live and never fall back to a
recorded or scripted run (source: `src/shipharness/ab/commands.py`).

| Message | Cause | Fix |
|---|---|---|
| `x SHIPHARNESS_CLASS_DATE is not set: set it in .env to the class day (YYYY-MM-DD) for class commands, or pass --purpose pilot for a pilot run` | Class commands need the class date | Set `SHIPHARNESS_CLASS_DATE=<the day you run>` in `.env`, or use `PURPOSE=assignment` (traces to `shipharness-assignments`) |
| `x OPENAI_API_KEY is missing: live A/B runs call OpenAI and never fall back to a stand-in; add the key to .env (or use make replay, which shows RECORDING)` | No key | Fill in `.env`; `make doctor` |
| `x OpenAI refused the key: <reason>; no arm was started` | The key is invalid, has no access to the model, or OpenAI is unreachable | `make doctor` names the problem; the reason `no access to gpt-6-luna (NotFoundError)` means the account cannot use the course model |
| `x no task for feature=<id> example=None variant=canonical` | The feature id is not in `datasets/teamtrack-features-v1.jsonl` | Use F1 to F7 (`make final` takes F5, F6, F7) |
| `! replay needs RUN=<ab or run id>` | `make replay` without `RUN` | `make replay RUN=<id>` (source: `Makefile`) |
| `! experiments is available after milestones M6 and M8` (same for `report`, `pilot`) | These Make targets are placeholders in this release | Use the `uv run shipharness ...` command directly, for example `uv run shipharness report` |
| `! slides are built in milestone M10` | Placeholder target | No action |

## Arm status and result lines

At the end of an A/B the terminal prints `A/B <ab id> (<feature>, layers=[...])`, one line per arm,
and a cost line. The exit code is 0 when both arms completed, 2 when an arm was aborted, 1 when an
arm ended in `ERROR`.

| Status or text | Cause | What it means for the result |
|---|---|---|
| `ABORTED: cap`, reason `cost cap reached: run $<x> of $0.20` (or `session $<x> of $2.50`) | A model call would have crossed a cap (source: `src/shipharness/cost/tracker.py`) | The run is still judged and shown; every run is a dot. A session cap hit stops all live runs under that class date |
| `ABORTED: timeout`, reason `agent time limit: RUN_TIMEOUT_S 300 s` | The arm used its 300 s of agent time | Judged and shown, with whatever the arm shipped |
| `ABORTED: timeout`, reason `harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during ...` | The harness work (preparation, gates) used its 120 s | Judged and shown |
| `ERROR`, `OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).` | The key stopped working mid-run (source: `src/shipharness/runner/loop.py`) | Fix the key; the run is not a measurement of the harness |
| `ERROR`, `OpenAI billing limit reached (quota or spend limit); add credit and retry.` | The OpenAI account is out of credit or at its spend limit | Add credit |
| `ERROR`, `OpenAI request kept failing after retries` | Repeated rate-limit or server errors | Try again later |
| `ERROR`, `arm setup failed: RuntimeError: docker run failed: ...` | Docker stopped, or an image is missing | `make images`; restart Docker |
| `passed=True` on a `make final` line, but low `hidden <x>/<total>` | F5-F7 have no primary measure, so `passed` is always true for them | Read the hidden-test and mutant counts ([final-project/README.md](../final-project/README.md#51-the-final-has-no-primary-measure)) |

## Replay and swap test

Source: `src/shipharness/ab/commands.py` and `src/shipharness/ab/recorded.py`.

| Message | Cause | Fix |
|---|---|---|
| ``x no recorded A/B for section demo-N under .shipharness/runs; run `make demo-N` first, or pass AB=<id>`` | `make swap-N` found no finished A/B of that section | Run the demo first, or `make swap-N AB=<ab id>` |
| `x no recorded A/B for '<id>' under .shipharness/runs; check the A/B or run id` | Wrong id | Copy the id from the console's run list |
| `x <ab id> predates checkpoint SHA pinning: ...` | The record has no pinned checkpoint commit | Use a newer recording |
| `Swap test on <ab id>: judged measures DIFFERENT`, then `<arm> <field>: <before> -> <after>` lines | The referee judged the same diff differently under the other label | Report it with the A/B id; the referee is meant to be deterministic for a given build |
| `make replay` asks for `SHIPHARNESS_CLASS_DATE` | `shipharness replay` always runs under the class purpose | Set the class date in `.env` (replay without the reviewer makes no model calls) |
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
| Screen 4 rows mix features (for example `CANONICAL bare`) | Screen 4 groups exports by variant and arm, not by feature (`src/shipharness/console/report.py`) | For per-feature dots run `uv run shipharness report` and open `exports/report.html` |
| Any screen shows `UNSANDBOXED — results not official` | `SANDBOX_MODE=none`, or no runtime was found | Fix Docker; unsandboxed results are for exploring only |

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
