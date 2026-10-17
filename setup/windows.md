# Setup on Windows (WSL2 and Docker Engine in Ubuntu)

On Windows, shipharness runs inside WSL2: an Ubuntu Linux environment on your PC. Everything after
step 1 happens in the Ubuntu terminal, not in PowerShell or cmd. Two rules matter more than any
other on this page:

- **The repository lives in the WSL filesystem** (`~/shipharness`), never under `/mnt/c/...`.
- **Docker Engine runs inside Ubuntu.** This page does not use Docker Desktop.

This is how the course's class host is set up: Windows 11 Pro, WSL 3.0.3.0, Ubuntu 26.04.1 with
systemd on, Docker Engine 29.9.1 inside Ubuntu, the repository at `~/shipharness`, uv 0.13.1, Python
3.12.15, and nothing Docker-related installed on the Windows side.

## What was tested, and where

| Step | Status on the class host |
|---|---|
| 1 WSL2 and Ubuntu | Installed; `wsl.exe -l -v` and `wsl.exe --version` ran on 2026-10-17 (output in step 1). `wsl --install` itself follows the official page |
| 2 systemd | `/etc/wsl.conf` holds `[boot]` and `systemd=true`; `systemctl is-active docker` printed `active` (checked 2026-10-17) |
| 3 to 7 | The Ubuntu commands of [linux.md](linux.md), with the status recorded there |

## 1. Install WSL2 with Ubuntu

Requirements: Windows 11, or Windows 10 version 2004 (build 19041) or later. Open **PowerShell as
administrator** (right-click, "Run as administrator") and run:

```powershell
wsl --install
```

This turns on the Windows features WSL needs and installs Ubuntu, the default distribution. Restart
the PC when asked. The first start of Ubuntu asks you to create a Linux user name and password;
that user is separate from your Windows account.

If WSL was already installed and the command prints its help text instead, list the distributions
and install Ubuntu by name:

```powershell
wsl --list --online
wsl --install -d Ubuntu
```

Check from PowerShell that Ubuntu runs as WSL version 2:

```powershell
wsl -l -v
```

Captured on 2026-10-17 from `wsl -l -v` on the class host (a Windows command, so no repository
commit applies); your output will differ:

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

From now on, open **Ubuntu** from the Start menu (or Windows Terminal) and run every command there.

Source: Install WSL, https://learn.microsoft.com/en-us/windows/wsl/install (read 2026-10-17).

## 2. Check that systemd is on

Docker Engine is a systemd service. Ubuntu installed by `wsl --install` has systemd on by default.
In Ubuntu:

```bash
cat /etc/wsl.conf
```

It must contain:

```
[boot]
systemd=true
```

If it does not, add those two lines (`sudo nano /etc/wsl.conf`), save, and restart WSL from
**PowerShell**:

```powershell
wsl.exe --shutdown
```

Then open Ubuntu again; `systemctl status` shows the running state.

Source: Use systemd to manage Linux services with WSL,
https://learn.microsoft.com/en-us/windows/wsl/systemd (read 2026-10-17).

## 3. Tools, uv, and Docker Engine inside Ubuntu

In the Ubuntu terminal, follow steps 1, 2, and 3 of [linux.md](linux.md) exactly: git,
make, and curl from apt; uv from the official installer; Docker Engine from Docker's apt
repository; then add your user to the `docker` group.

On WSL, "log out and back in" after `usermod -aG docker $USER` means: close every Ubuntu window, run
`wsl.exe --shutdown` in PowerShell, and open Ubuntu again. Then check:

```bash
systemctl is-active docker
id -nG | tr ' ' '\n' | grep -x docker
docker info
```

The first line prints `active` and the second `docker`.

## 4. Clone into the WSL filesystem and run `make setup`

```bash
cd ~
git clone https://github.com/ANI-IN/harness-engineering-session.git ~/shipharness
cd ~/shipharness
make setup
```

Check where you are:

```bash
pwd
```

The answer must start with `/home/<your Linux user>/`. If it starts with `/mnt/c`, you are on the
Windows drive: clone again under `~`. Microsoft's guidance: "For the fastest performance speed,
store your files in the WSL file system if you are working in a Linux command line" (Working across
file systems, https://learn.microsoft.com/en-us/windows/wsl/filesystems, read 2026-10-17). Every
A/B creates fresh git repositories and runs many container commands against them, so the slower
cross-filesystem path is felt on every run. The class host was tested only with the repository at
`~/shipharness`.

To open the folder in Windows Explorer, run `explorer.exe .` inside it; in the Explorer address bar,
`\\wsl$` lists every distribution's files.

What `make setup` does and how to check the tags: step 4 of [linux.md](linux.md).

## 5. Keys in `.env`

Edit `.env` from Ubuntu, for example with `nano .env`, and fill in `OPENAI_API_KEY` and
`LANGSMITH_API_KEY` (step 5 of [linux.md](linux.md), including
`SHIPHARNESS_CLASS_DATE`). An editor on Windows can open the file through `\\wsl$`, but keep the file
where it is.

## 6. `make doctor`

```bash
make doctor
```

Done when the last line is `result: + ready` and the `container runtime` line starts with `+ ok`.
Example output and the meaning of each line: step 6 of [linux.md](linux.md).

## 7. `make up`, and the browser on Windows

```bash
make up
```

Open http://127.0.0.1:8000/board in your Windows browser. In WSL's default networking mode, a
server running in Ubuntu is reachable from a Windows browser at `localhost` (Accessing network
applications with WSL, https://learn.microsoft.com/en-us/windows/wsl/networking, read 2026-10-17).
The live console (`make console`) works the same way at http://127.0.0.1:8765/.

## Windows-specific problems

| Symptom | Fix |
|---|---|
| `make: command not found` or `uv: command not found` in a blue window | You are in PowerShell. Open Ubuntu and run the command there |
| `wsl --install` prints help text | WSL is already installed: `wsl --list --online`, then `wsl --install -d Ubuntu` |
| `System has not been booted with systemd` | Step 2: add `[boot]` / `systemd=true` to `/etc/wsl.conf`, then `wsl.exe --shutdown` |
| `permission denied` on `/var/run/docker.sock` | The `docker` group is not active yet: `wsl.exe --shutdown` in PowerShell, reopen Ubuntu |
| Everything is slow, or the repository path starts with `/mnt/c` | Clone again under `~` (step 4) |
| The board does not open in the Windows browser | Make sure `make up` is still running in Ubuntu; try http://localhost:8000/board |

More: [troubleshooting.md](../docs/troubleshooting.md).
