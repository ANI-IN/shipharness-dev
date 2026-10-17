# Setup on Linux (Ubuntu)

Exact commands to go from a fresh Ubuntu machine to `make doctor` reporting `result: + ready`. For
Windows, use [windows.md](windows.md) (it ends in the same Ubuntu commands, inside
WSL2). For macOS, use [macos.md](macos.md).

## What was tested, and where

The course's class host is Windows 11 with WSL2, Ubuntu 26.04.1 (systemd on), Docker Engine 29.9.1
inside Ubuntu, the repository at `~/shipharness`, uv 0.13.1, and Python 3.12.15. The commands below
are Ubuntu commands; they were tested in that Ubuntu, which runs inside WSL2. A native Ubuntu
install uses the same commands, but no native install was tested for the course.

| Step | Status on the class host |
|---|---|
| 1 git, make, curl | Installed; versions checked on 2026-10-17 (`git version 2.53.0`, `GNU Make 4.4.1`, curl 8.18.0) |
| 2 uv | Installed in `~/.local/bin`, where the official installer puts it; `uv --version` printed `uv 0.13.1` on 2026-10-17. The install command itself follows the official page |
| 3 Docker Engine | Installed from Docker's apt repository (`download.docker.com`, suite `resolute`, packages `docker-ce 5:29.9.1`); `systemctl is-active docker` printed `active`, and the user is in the `docker` group (checked 2026-10-17). The install commands follow the official page |
| 4 `make setup` | `make -n setup` checked on 2026-10-17 (it prints `uv sync --frozen`, the two image builds, and the `.env` copy); `uv sync --frozen` ran on 2026-10-17. The image builds ran on the class host for the course pilot |
| 5 `.env` | Format from `.env.example` |
| 6 `make doctor` | `uv run shipharness doctor --offline` ran on 2026-10-17 (output below); the online key check is the same command without `--offline` |
| 7 `make up` | Ran on 2026-10-17 (output in step 7); `/board` answered with the sign-in page |

**As of 2026-10-17, the `git clone` command in step 4 has not been run on the class host.** Its URL
is the public learner repository, which can be cloned only after it is published. The class host's
checkout at `~/shipharness` is the course's build repository.

## Accounts first

You need two accounts and one API key in each. Details and reasons are in the
[README](../README.md#7-prerequisites-and-accounts): an OpenAI API account with credit bought (the
"Build" usage tier needs $5 in total credit purchases), and a LangSmith account on the free
Developer plan with no card on file.

## 1. Install git, make, and curl

```bash
sudo apt update && sudo apt install -y git make curl
```

Check:

```bash
git --version && make --version | head -1 && curl --version | head -1
```

## 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To get the same version as the class host, put the version in the URL:

```bash
curl -LsSf https://astral.sh/uv/0.13.1/install.sh | sh
```

The installer places `uv` and `uvx` in `~/.local/bin` and can add that folder to your shell
profile. Open a new terminal, then check with `uv --version`. You do not install Python yourself:
the repository pins 3.12 in `.python-version`, and uv downloads it on first use.

Source: uv installation page, https://docs.astral.sh/uv/getting-started/installation/ (read
2026-10-17).

## 3. Install Docker Engine

These are Docker's commands for Ubuntu ("Install using the apt repository"). On 2026-10-17 Docker
listed Ubuntu 26.10, 26.04 (LTS), 24.04 (LTS), and 22.04 (LTS) as supported.

```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Docker also publishes a convenience script (`curl -fsSL https://get.docker.com -o get-docker.sh`
then `sudo sh get-docker.sh`); its page recommends the script only for testing and development
machines.

Then let your user run Docker without `sudo`, and open a new terminal (or log out and in):

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

`groupadd` reports that the group exists if the package already created it; that is fine.

Check:

```bash
systemctl is-active docker
id -nG | tr ' ' '\n' | grep -x docker
docker info
```

The first line prints `active`; the second prints `docker`. On Ubuntu the Docker service starts on
boot by default. If it is not running: `sudo systemctl start docker`.

Sources: Docker Engine on Ubuntu, https://docs.docker.com/engine/install/ubuntu/; Linux
post-installation steps, https://docs.docker.com/engine/install/linux-postinstall/ (both read
2026-10-17).

Podman also works (`SANDBOX_RUNTIME=podman` in `.env`, and `make setup RUNTIME=podman`), but the
course did not test it.

## 4. Clone and run `make setup`

Keep the repository in your home folder, for example `~/shipharness`. As of 2026-10-17 the
`git clone` line below has not been run on the class host; see the table at the top:

```bash
git clone https://github.com/ANI-IN/harness-engineering-session.git ~/shipharness
cd ~/shipharness
make setup
```

`make setup` runs, in order (from `make -n setup`):

```
uv sync --frozen
docker build -f platform/sandbox/Dockerfile --target agent -t shipharness-agent:1 .
docker build -f platform/sandbox/Dockerfile --target referee -t shipharness-referee:1 .
```

and copies `.env.example` to `.env` if `.env` does not exist. If it prints
`! docker not found: images not built; sandboxed runs need a container runtime`, Docker is not on
your `PATH`: fix step 3, then run `make images`.

Check that the checkpoint tags came with the clone (the demos start from them):

```bash
git tag -l 'm1-*'
```

It lists nine tags, from `m1-alt-a` to `m1-s4-start`, including `m1-final-start`.

## 5. Put your keys in `.env`

Open `.env` in the repository root in an editor and fill in:

```
OPENAI_API_KEY=
LANGSMITH_API_KEY=
```

If your LangSmith account is in the EU region, also set
`LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com` (no trailing slash).

If you will run `make demo-N`, `make show-N`, `make final`, or `make replay` yourself, also set
`SHIPHARNESS_CLASS_DATE` to the day you run them (`YYYY-MM-DD`). Class commands refuse without it;
it names the LangSmith project `shipharness-class-<date>`, and every command run under that date
shares one $2.50 session cap (`MAX_SESSION_COST_USD`).
The assignments tell you which commands they need.

`.env` is git-ignored. Never commit it, paste it anywhere, or share a screenshot of it.

## 6. `make doctor`

```bash
make doctor
```

It checks Python, git, uv, the container runtime, both keys, the price table, and that `.env` is not
tracked by git. The OpenAI check lists models and uses no tokens. You are done when the last line is
`result: + ready` and the `container runtime` line starts with `+ ok`. Each key line then says
`accepted by OpenAI` or `accepted by LangSmith`.

Captured on 2026-10-17 from `uv run shipharness doctor --offline`, in a checkout
without a `.env` file (no network calls); your output will differ:

```
$ uv run shipharness doctor --offline
shipharness doctor
  + ok          python                 3.12.15
  + ok          git                    /usr/bin/git
  + ok          uv                     /home/ani/.local/bin/uv
  + ok          container runtime      docker at /usr/bin/docker
  x missing     OPENAI_API_KEY         not set
    next step: OPENAI_API_KEY is missing: add it to .env at the repo root
  x missing     LANGSMITH_API_KEY      not set
    next step: LANGSMITH_API_KEY is missing: add it to .env at the repo root
  + ok          prices                 gpt-6-luna, gpt-5.6-luna
  + ok          .env not in git        not tracked
  result: x not ready (fix the items above)
Cost: $0.000000 (no model calls)
```

## 7. `make up`

```bash
make up
```

It prints where the board is, then the server's log. Captured on 2026-10-17 on the class host,
first lines; your output will differ:

```
uv run shipharness up --port 8000
TeamTrack: http://127.0.0.1:8000/board  (API docs: /docs)
INFO:     Started server process [927409]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

How to check it worked, from a second terminal (captured the same day):

```
$ curl -s -o /dev/null -w '%{http_code} %{redirect_url}
' http://127.0.0.1:8000/board
303 http://127.0.0.1:8000/board/login
```

The board sends you to its sign-in page (`<title>Sign in · TeamTrack</title>`, with demo users such
as `admin@acme.test`). Open http://127.0.0.1:8000/board in a browser, pick a demo user on the sign-in
page (for example `admin@acme.test`), and you see the Acme project board. The demo data has two orgs, Acme and Globex
(`platform/teamtrack/docs/HANDBOOK.md`). Stop the server with Ctrl+C. If port 8000 is taken:
`make up PORT=8001`.

## When a step fails

| Symptom | Fix |
|---|---|
| `permission denied` on `/var/run/docker.sock` | The `docker` group is not active in this terminal yet: open a new terminal (or log out and in) after step 3, then `id -nG` must list `docker` |
| `make setup` prints `! docker not found: images not built; sandboxed runs need a container runtime` | Docker is not on your `PATH` or not installed: finish step 3, then `make images` |
| `make doctor`: `x missing     OPENAI_API_KEY` (or `LANGSMITH_API_KEY`) | Step 5: the key goes into `.env` in the repository root |
| `make doctor`: `! warn        container runtime      docker not found: ...` | Start Docker (`sudo systemctl start docker`) or finish step 3 |

Next: the [README](../README.md) for what to run, and
[troubleshooting.md](../docs/troubleshooting.md) for every other message.
