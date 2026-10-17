# Sandboxes compared: shipharness, A4, A5, and Codex

Reading time: about 10 minutes.

The S3 sandbox is one Docker container per arm with a fixed policy (`SandboxPolicy` in
`src/shipharness/sandbox/policy.py`; the values are **course design**). This piece puts that policy
next to the boundaries described in two teaching sources (A4, A5) and in the official docs of another
coding agent, Codex (D21-D23). Everything about the other systems comes from the course's research
record of those sources, cited by ID; the full list is in [REFERENCES.md](../../../REFERENCES.md).
Where a cell says "not recorded", the course recorded nothing on it; that does not mean the source
lacks it.

## Side by side

| | shipharness arm container | A4: parallel Claudes | A5: quickstart (README only) | Codex (official docs) |
|---|---|---|---|---|
| Where commands run | A Docker container per arm. The agent loop and the API keys stay on the host | "for each agent, a Docker container is spun up with the repo mounted to /upstream." (F-a-88) | An OS-level sandbox, the first of three layers (F-a-86) | An OS sandbox per command: Seatbelt on macOS, bwrap plus seccomp on Linux, MXC on Windows, the Linux implementation on WSL2 (D21) |
| Network | `--network none`: "Within the container, only the loopback device is created." (D27) | "Claude did not have internet access at any point during its development" (F-a-90) | Not recorded | "By default, the agent runs with network access turned off." (D21); can be turned on for `workspace-write` |
| What the agent can write | `/work` (the arm's repository) and `/tmp`; the root filesystem is read-only | Its container, with the repository mounted at `/upstream` (F-a-88) | "File operations restricted to the project directory only" (F-a-86) | `workspace-write`: the workspace and temp directories; `.git`, `.agents`, `.codex`, `.aws` under writable roots stay read-only (D21) |
| Which commands | Any command; six deny rules refuse network commands before they run; output is checked afterwards | Not recorded | An allowlist: "Commands not in the allowlist are blocked by the security hook." (F-a-87) | Set by the sandbox mode (`read-only`, `workspace-write`, `danger-full-access`) and the approval policy (`on-request`, `never`, `granular`) (D22, D23) |
| Resource limits | 1 CPU (2 in the class profile), 1024 MB with no swap, 256 processes, 120 s per command, 300 s per run | Not recorded | Not recorded | Not recorded |
| Human approval | None; runs are non-interactive | None; the author's advice is "(Run this in a container, not your actual machine)." (F-a-18) | Not recorded | Approval policies, for example `on-request` for interactive runs and `never` for non-interactive ones (D23) |

## Four differences worth noticing

**1. Allowlist or deny list.** A5 allows a fixed list of commands and blocks the rest (F-a-87).
shipharness lets the agent run any command and puts the boundary in the container instead: with no
network, `pip install` cannot succeed whatever the command list says. The six deny rules
(`DEFAULT_DENY_RULES` in `policy.py`) exist to give the agent a fast, readable refusal: the command
never runs, and the tool result says the sandbox has no network and the dependencies are already in
the image. The trade-off is the usual one. An allowlist is tight but has to be kept up to date for
every tool a task needs; a container boundary with a short deny list is looser on commands and
tighter on what any command can reach.

**2. Codex on Linux uses bwrap plus seccomp.** Codex on Linux uses bubblewrap (`bwrap`) plus
seccomp, not Landlock as older descriptions say. The docs say: "Linux uses bwrap plus seccomp by default." (D21).
`landlock` survives only as an alias of the `codex sandbox` test command. The approval policy names
changed too: `untrusted` is retired and `on-failure` is deprecated; the valid values are `on-request`,
`never`, and `granular` (D23).

**3. Who protects the harness's own files.** Codex keeps `.git`, `.agents`, and `.codex` read-only
inside a writable workspace (D21), so the agent cannot rewrite its own configuration. In shipharness
the whole of `/work` is writable, `.git` included, because both arms commit their work. The harness
files are protected one level up, on the host: the scope layer refuses any change to
`feature_list.json` in every phase, and the referee strips harness artifacts from the diff and
restores the checkpoint's test configuration before judging (`strip` and `restore_judge_config` in
`src/shipharness/ab/referee.py`). This keeps the
container identical for both arms; the protection that differs between arms lives in the harness.

**4. Out of memory is not an exit code.** Exit code 137 is the SIGKILL convention (128 + 9), not a
code the Docker pages document; Docker's documented out-of-memory signal is the
`State.OOMKilled` field (D29). Because an arm container stays up for the whole run and runs many
commands, `DockerSandbox.exec` in `src/shipharness/sandbox/docker.py` reads the container's cgroup v2
`oom_kill` counter before and after each command. A quick exit 137 is reported as `memory` when the
counter went up (or when it cannot be read), and a command that reached its limit as `timeout`.

## What the sandbox does not decide

The container decides what the machine allows: network, writable directories, CPU, memory, processes,
time. It does not decide which files inside `/work` belong to this feature. That is the scope layer's
job (`blocked`, harness arm only); the container's refusals are `sandbox_denied` events (both arms).
Module 2 covers detailed sandbox design.

In the course pilot's runs 2 to 4 (2026-10-16 to 2026-10-17) and the class-profile round
(2026-10-17), no command produced a `sandbox_denied` event (counted in each run's `events.jsonl`,
2026-10-17). The agent used what the image had and never tried the network. The container is
never an A/B variable, so the pilot cannot say whether it earns its place; the course keeps it on the
sources' advice, for the run that goes wrong, as in A4's "pkill -9 bash" incident (A4, F-a-19). No
real run has shown a denial; a scripted one is in [docs/extras.md](../../../docs/extras.md)
(optional, not part of class).

## Why it matters for your own repo

- **Decide where the boundary lives before you pick the tool.** An allowlist (A5) needs upkeep per
  tool; a container with no network needs the dependencies baked into the image. If your agent must
  install packages, a no-network container will block it; build the image with them instead, as
  `sandbox/Dockerfile` does.
- **Keep secrets out of the box.** The agent loop and the keys stay on the host; nothing named like a
  key, token, or secret is passed into the container (`docker_run_args`). Copy that split: it is
  what makes "the agent ran a bad command" a contained event.
- **Protect the files that grade the agent.** Codex keeps `.git` and its own configuration read-only
  inside the workspace (D21). Whatever your harness uses as evidence (a feature list, a test config, a
  commit) needs the same protection from the agent, at the container level or in harness code.
- **Report out-of-memory from the kernel, not from an exit code.** Exit 137 alone is ambiguous; read the cgroup counter or `State.OOMKilled` (D29) before you tell the agent it ran
  out of memory.

## Sources

- A4: Nicholas Carlini, Anthropic, "Building a C compiler with a team of parallel Claudes",
  2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
- A5: Anthropic, "Autonomous Coding Agent Demo" (README only).
  https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- D21: OpenAI, Codex "Agent approvals & security".
  https://developers.openai.com/codex/agent-approvals-security
- D22: OpenAI, Codex "Sandboxing concepts". https://developers.openai.com/codex/concepts/sandboxing
- D23: OpenAI, Codex "Configuration reference". https://developers.openai.com/codex/config-reference
- D24-D30: Docker docs (`docker container run`, running containers, resource constraints, none
  network driver, `docker container stats`, Engine API v1.51, Dockerfile reference).
  https://docs.docker.com/reference/cli/docker/container/run/
