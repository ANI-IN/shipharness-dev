# Pre-class setup

Do this before class. At the end, `make doctor` reports `result: + ready` and the TeamTrack board
opens in your browser.

How long it takes: the course has not timed these steps on a clean machine, so plan for an hour the
first time. The slowest step is building the two sandbox images in step 4; on the course's class host
(Ubuntu in WSL2) a rebuild of both images took 145 s on 2026-10-17. Downloads depend on your network.

## Accounts you need

| Account | Plan | Why |
|---|---|---|
| OpenAI API | Paid, **Build tier or higher, with at least $5 of credit purchased** | The agent model, gpt-6-luna, lists API rate limits only for the paid tiers Build, Launch, and Grow; there is no Free row (https://developers.openai.com/api/docs/models/gpt-6-luna, read 2026-10-17). The four assignments are planned to use at most $6 in total, and no single command more than $2.50 ([README, section 12](../README.md#12-assignments)). |
| LangSmith | **Free Developer plan, no card on file** | Traces and experiments. Without a card, a personal organization is limited to 5,000 traces per month; past the limit LangSmith refuses new traces instead of billing (https://docs.langchain.com/langsmith/billing, read 2026-10-17). The module plans at most 400 traces for you ([README, section 7](../README.md#7-prerequisites-and-accounts)). |

Do not add a credit card to LangSmith. Create one API key in each account and keep both ready for
step 5.

## What runs where

shipharness runs on Linux, macOS, or Windows through WSL2. Native Windows shells
(PowerShell, cmd) are not supported for sandboxed commands, and the Makefile expects a POSIX shell.

| Your machine | Container runtime (any one) | Notes |
|---|---|---|
| Linux | Docker Engine or Podman | |
| macOS | Docker Desktop or Colima | |
| Windows | WSL2 with Ubuntu, then Docker Engine inside Ubuntu or Docker Desktop with the WSL2 backend | Work only inside the Ubuntu terminal. Keep the repository in the WSL2 filesystem (for example `~/shipharness`), not under `/mnt/c` ([setup-windows.md](../docs/setup-windows.md)) |

The class host is a Windows PC with Docker Engine inside the Ubuntu WSL2 distribution, systemd
enabled, and nothing Docker-related installed on the Windows side
([setup-windows.md](../docs/setup-windows.md)). Docker Desktop also works; pick whichever you already
have.

## Steps

### 1. Install git, make, and curl

- Ubuntu, Debian, or WSL2 Ubuntu: `sudo apt update && sudo apt install -y git make curl`
- macOS: `xcode-select --install` (installs git and make)

On Windows, install WSL2 first from PowerShell with `wsl --install -d Ubuntu`, restart if asked, open
the Ubuntu terminal, and run every later command there.

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal afterwards so `uv` is on your `PATH`. You do not need to install Python yourself:
the repository pins Python 3.12 in `.python-version`, and uv fetches it when needed.

### 3. Install a container runtime

| Runtime | Install | Check |
|---|---|---|
| Docker Engine (Linux, WSL2) | `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh`, then `sudo usermod -aG docker $USER` and open a new terminal (on WSL2, run `wsl --shutdown` from PowerShell first) | `docker info` |
| Docker Desktop (macOS, Windows) | Install from docker.com; on Windows turn on the WSL2 backend and integration with your Ubuntu distribution (needs WSL 2.1.5 or later) | `docker info` in the Ubuntu or macOS terminal |
| Colima (macOS) | `brew install colima docker && colima start --cpu 2 --memory 4` | `docker info` |
| Podman (Linux, macOS, Windows) | Install from podman.io; on macOS and Windows run `podman machine init && podman machine start` | `podman info` |

Docker Engine on WSL2 needs systemd: `/etc/wsl.conf` should contain `[boot]` and `systemd=true`
([setup-windows.md](../docs/setup-windows.md#2-check-that-systemd-is-on)). More detail:
[sandbox/README.md](../sandbox/README.md).

### 4. Clone and run `make setup`

```bash
git clone https://github.com/ANI-IN/harness-engineering-session.git ~/shipharness
cd ~/shipharness
make setup
```

`make setup` runs `uv sync --frozen` (pinned dependencies), builds the two sandbox images
`shipharness-agent:1` and `shipharness-referee:1`, and creates `.env` from `.env.example` if it does
not exist. If it prints `! docker not found: images not built`, your container runtime is not on the
`PATH`; fix step 3 and run `make images`.

Podman users: run `make setup RUNTIME=podman` instead, and in step 5 also set `SANDBOX_RUNTIME=podman`
in `.env`.

### 5. Put both keys in `.env`

Open `.env` in the repository root and fill in the two required lines:

```
OPENAI_API_KEY=
LANGSMITH_API_KEY=
```

If your LangSmith account is in the EU region, also set
`LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com` (no trailing slash).

`.env` is git-ignored. Never commit it, paste it into an issue or chat, or share a screenshot of it.
shipharness never prints, logs, traces, or passes the keys into a container
([docs/architecture.md](../docs/architecture.md)).

### 6. `make doctor`

```bash
make doctor
```

It checks Python, git, uv, the container runtime, both keys, the price table, and that `.env` is not
tracked by git. Each key is reported on its own line as `ok`, `missing`, `invalid` (the provider
rejected it), or `unreachable` (network error), with the next step to take; no part of a key is ever
shown. It costs nothing: the OpenAI check lists models and uses no tokens (`src/shipharness/doctor.py`).

You are done with this step when the last line reads `result: + ready` **and** the
`container runtime` line shows `+ ok`. A container-runtime warning does not fail the doctor, but
without a runtime only the UNSANDBOXED fallback can run, and class runs need the sandbox.

### 7. `make up`

```bash
make up
```

Open http://127.0.0.1:8000/board, pick a demo user on the login page (for example `admin@acme.test`),
and you should see the Acme project board. The demo data has two orgs, Acme and Globex
(`teamtrack/docs/HANDBOOK.md`). Stop the server with Ctrl+C. If port 8000 is taken, run
`make up PORT=8001`.

## If something fails

| Symptom | Fix |
|---|---|
| `make: command not found` | Step 1. On Windows, you are in PowerShell instead of the Ubuntu terminal |
| `uv: command not found` | Open a new terminal after step 2 |
| `permission denied` on the Docker socket | Step 3: add yourself to the `docker` group and open a new terminal |
| Doctor: a key line shows `x missing` | Step 5; the file must be `.env` in the repository root |
| Doctor: a key line shows `x invalid` | The provider rejected the key: copy it again, check for spaces, and for OpenAI check that the account has Build-tier credit |
| Doctor: a key line shows `! unreachable` | A network or proxy problem between you and the provider; try again on another network |
| The board shows nothing | Make sure `make up` is still running and you picked a user on the login page |

Bring any remaining error message (never your keys) to the start of class.
