# Setup on macOS (Docker Desktop or Colima)

> **Not tested on macOS.** No command on this page was run on a Mac for the course. Every step
> follows the official documentation cited next to it (each page read on 2026-10-17). The course's
> tested platform is Ubuntu (inside WSL2 on the class host): see [setup-linux.md](setup-linux.md)
> and [setup-windows.md](setup-windows.md). If a step fails on your Mac, bring the exact message to
> class, and see [troubleshooting.md](troubleshooting.md).

You need a container runtime that provides the `docker` command. Pick **one**:

- **Docker Desktop**: Docker's app. Free for personal use, education, and small businesses; larger
  companies need a paid subscription (terms below).
- **Colima**: an open-source runtime started from the terminal, used with the Docker command-line
  client from Homebrew.

## 1. git and make

Apple's Command Line Tools include git:

```bash
xcode-select --install
```

Check:

```bash
git --version
make --version
```

If `make` is missing after that, install the Command Line Tools again from Apple's prompt; do not
continue without `make`, because every course command is a Make target.

Source: Git for macOS, https://git-scm.com/install/mac ("Apple ships a binary package of Git with
Xcode Command Line Tools").

## 2. Homebrew (needed for Colima, optional otherwise)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The script explains what it will do and pauses before it does it. Source: https://brew.sh/.

## 3. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or, with Homebrew, `brew install uv`. For the class host's version, put it in the URL:
`curl -LsSf https://astral.sh/uv/0.13.1/install.sh | sh`. Open a new terminal and check with
`uv --version`. uv downloads Python 3.12 for the repository when needed (`.python-version`).

Source: uv installation, https://docs.astral.sh/uv/getting-started/installation/.

## 4a. Docker Desktop

Requirements from Docker's page: one of the current and two previous major macOS releases, and at
least 4 GB of RAM, on Apple silicon or Intel.

1. Download the installer for your chip (Apple silicon or Intel) from
   https://docs.docker.com/desktop/setup/install/mac-install/.
2. Open `Docker.dmg` and drag Docker into Applications.
3. Open Docker from Applications and accept the subscription agreement.

Docker's command-line alternative after downloading `Docker.dmg`:

```bash
sudo hdiutil attach Docker.dmg
sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
sudo hdiutil detach /Volumes/Docker
```

Licence terms, from the same page: Docker Desktop "is free for small businesses (fewer than 250
employees AND less than $10 million in annual revenue)", personal use, education, and non-commercial
open-source projects; other professional use needs a paid subscription.

Check in a new terminal:

```bash
docker info
```

Source: Install Docker Desktop on Mac, https://docs.docker.com/desktop/setup/install/mac-install/.

## 4b. Colima (instead of Docker Desktop)

```bash
brew install colima docker
colima start --cpu 2 --memory 4
docker info
```

`brew install docker` installs the Docker command-line client that Colima needs. Colima's default
virtual machine has 2 CPUs and 2 GiB of memory; `--memory 4` gives it 4 GiB. Each arm container is
limited to 1 CPU and 1 GiB, and an A/B runs two arm containers, two board previews, and the referee,
so give the virtual machine room. To change the size later: `colima stop`, then `colima start` with
new values.

After a restart of the Mac, run `colima start` again before any course command.

Source: Colima, https://github.com/abiosoft/colima.

## 5. Clone, `make setup`, keys, `make doctor`, `make up`

From here the commands are the same as on Linux: steps 4 to 7 of [setup-linux.md](setup-linux.md).

```bash
git clone https://github.com/ANI-IN/harness-engineering-session.git ~/shipharness
cd ~/shipharness
make setup
# edit .env: OPENAI_API_KEY, LANGSMITH_API_KEY (and SHIPHARNESS_CLASS_DATE for class commands)
make doctor
make up
```

`make doctor` must end with `result: + ready`, with `+ ok` on the `container runtime` line.

## Things that may differ on a Mac

These are expectations from the official pages, not observations:

- Docker Desktop on Mac installs its command-line tools under `$HOME/.docker/bin` and, by default,
  does not create the default Docker socket (Docker's install page; Settings > Advanced changes
  both). If `make doctor` reports `docker not found`, open a new terminal so the `PATH` change takes
  effect, or check that setting.
- The sandbox images are built locally by `make setup` for your machine's architecture.
- On Apple silicon, Docker's page recommends Rosetta 2, though no longer strictly required
  (`softwareupdate --install-rosetta`). Whether the course images need it was not tested.

If anything on this page turns out to be wrong on your Mac, tell the instructor with the command
and the full message.
