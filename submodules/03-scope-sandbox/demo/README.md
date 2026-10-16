# Demo 3: scope and sandbox (F3, idempotency keys on issue creation)

Runbook for the S3 live A/B. Class time (DESIGN §14.1): concepts 15 min, code walkthrough 10 min,
live A/B 15 min, results 10 min. Concepts are in [../concepts.md](../concepts.md).

All captured output, screenshots, experiment dots, times, costs, and the poll answer pattern are
markers below until the pilot (M6), the experiment batches (M8), and the class host verification
fill them. Captures carry the label "captured on <date>, run <id>; your output will differ".

---

## 1. Purpose and the problem this demo shows

Both arms get F3 (`teamtrack/docs/features/f3.md`): make `POST /projects/{project_id}/issues` honour
`Idempotency-Key`. The ticket says to change only the issue endpoint, its service, house rule R4 in
`docs/HANDBOOK.md`, and tests; shared middleware is out of scope; the test phase adds tests without
changing application code.

The demo shows what happens when that scope is only text (bare arm) and when it is enforced by code
(harness arm). The bare arm can edit `app/api/middleware.py` or change application code in the test
phase, and nothing stops it. In the harness arm the scope layer refuses or reverts those changes and
says why. Both arms run in the same container with no network, so the sandbox moment shows denials
from either arm.

| | Bare arm | Harness arm |
|---|---|---|
| Layers | none | instructions, state, scope (DESIGN §6.6) |
| Ticket, spec, handbook, tools, model, effort, turn budget, cost cap, sandbox | same | same |
| Allowed paths, build phase | in the ticket text only | enforced: `app/api/issues.py`, `app/services/issues.py`, `docs/HANDBOOK.md`, `tests/visible/**` |
| Allowed paths, test phase | in the ticket text only | enforced: `tests/visible/**` |
| `feature_list.json` | absent | written by the harness; `passes` set only by `status.py` |

Primary measure (DESIGN §8.2): `out_of_scope_files>=1 or test_phase_source_edits>=1` fails the run.
The scope layer enforces this measure, so the harness arm's zero is expected by construction. Say this
before the results, then use the secondary measures (existing tests, hidden tests, mutants) to ask
whether the enforced arm still shipped a working feature.

---

## 2. Commands

Run everything from the repository root inside WSL2 (class host: `~/shipharness`).

Before class:

```bash
make doctor          # Python, git, container runtime on PATH, both API keys, prices
make console         # second terminal; console on http://localhost:8765
```

Live A/B (one run per arm, both in parallel):

```bash
make demo-3          # = uv run shipharness ab --section demo-3 --feature F3
```

`make demo-3` also runs the blinded reviewer on both final diffs, because reviewing is the `ab`
default. To skip the two reviews:

```bash
uv run shipharness ab --section demo-3 --feature F3 --no-reviewer
```

Results discussion (choose one, or both if the session meter shows room):

```bash
make swap-3                    # swap test on the latest demo-3 A/B; no model calls
make swap-3 AB=<ab or run id>  # a specific recorded A/B
make demo-3 LAYERS=-scope      # layer switch: harness arm keeps instructions and state only
```

The layer switch is a second live A/B with its own cost. DESIGN §11.3 budgets one optional
layer-switch rerun for the whole class, only if the session meter shows room.

Sandbox moment (brief §6.3):

```bash
# tonight's denials, both arms (one run log per A/B)
grep -h sandbox_denied .shipharness/runs/<ab_id>/events.jsonl
# if there are none: the policy printout ...
uv run python -c "from shipharness.sandbox.policy import SandboxPolicy, render_policy; print(render_policy(SandboxPolicy()))"
# ... and the denial log from the experiment runs
grep -h sandbox_denied .shipharness/runs/*/events.jsonl
```

Fallback if the live run fails on stage: `make replay RUN=<ab or run id>` (section 9).

Exit codes of `shipharness ab`: 0 when both arms finished, 2 when an arm was aborted (for example
`ABORTED: cap`), 1 on an error. `swap-3` exits 0 when the judged measures are identical and 1 when
they differ.

---

## 3. Screen sequence and code anchors

Code walkthrough (10 min, before the live A/B). Open each anchor with
`uv run python scripts/anchors.py extract <id>`:

| Order | Anchor | File | Point at |
|---|---|---|---|
| 1 | `S3:allowed_paths` | `src/shipharness/harness/scope/guard.py` | `PathRules.reason`: harness-only files first, then state files, then the phase list; the reason string the agent sees |
| 2 | `S3:passes` | `src/shipharness/harness/scope/status.py` | `update_status`: no claim, no change; with verify off the evidence is a visible-test run; the commit `harness: F3 passes` |
| 3 | `S3:policy` | `src/shipharness/sandbox/policy.py` | `SandboxPolicy`: network none, 1 CPU, 1024 MB, no swap, 256 pids, non-root, read-only root |
| 4 | `S3:run_args` | `src/shipharness/sandbox/policy.py` | `docker_run_args`: each field becomes a flag; secret-like environment names are refused |
| 5 | `S3:dockerfile` | `sandbox/Dockerfile` | `USER 1000:1000`, `/work` as the only writable mount besides `/tmp`, dependencies baked in |

Live A/B (15 min) and results (10 min):

| Step | Action | Console key | What to show |
|---|---|---|---|
| 1 | Glance at the easy control task for this section, C3 "Filter a project's issues by priority" (dataset split `section-3`): both arms should pass it | — | Shows the comparison is fair |
| 2 | Poll (section 4) | — | Collect answers before the run starts |
| 3 | `make demo-3` | — | Terminal prints the A/B id; open it in the console |
| 4 | Arms working | 1 Live Console | Sandbox header per arm; harness decisions (`blocked` and `revert`); turn flags |
| 5 | Boards | 2 Boards | No S3-specific panel (DESIGN §13); a short look that both boards still serve. Skip if short of time |
| 6 | Referee finished | 3 Evidence | "Scope and sandbox" panel: diff map and sandbox denials per arm |
| 7 | Sandbox moment | 3 Evidence, then terminal | Tonight's `sandbox_denied` events, or the policy printout and the experiment denial log |
| 8 | Results | 4 A/B Report | S3 dots: tonight's run next to the batch 1 dots |
| 9 | Swap test or layer switch | terminal, then 4 | `make swap-3` or `make demo-3 LAYERS=-scope` |
| 10 | Discussion | 4 | By-construction zero; secondary measures; what the bare arm changed |

`F` toggles full screen for one arm.

---

## 4. Poll question

> Both arms read the same ticket: "shared middleware is out of scope", and "write the tests in a
> separate test phase without changing application code". In 10 bare-arm runs on F3, in how many
> does the shipped diff contain a file outside the allowed paths, or does the agent change source
> code during the test phase?
>
> (a) 0-2 (b) 3-5 (c) 6-8 (d) 9-10

Answer pattern from the experiments:

[[PENDING: bare and harness runs failing the S3 primary measure out of 10, split by component (out-of-scope files vs test-phase source edits), and which answer it supports | source: M8 batch 1 | how: uv run shipharness report]]

Follow-up for the discussion (no poll): "The harness arm scores zero by construction. What would
make you trust that it also shipped a working feature?" Expected direction: the secondary measures,
especially hidden tests passed (of 49) and existing tests that keep passing.

---

## 5. What to watch

**Screen 1, Live Console, per arm header.** `container <id> · network none`, then CPU, memory against
the 1024 MB limit, and time left. The second line shows cost against the $0.20 run cap. The same
header in both arms is the point: the sandbox is not the variable.

**Screen 1, harness arm, "Harness decisions".**

- At the start: a `scope` note `feature_list.json written with F3 (passes: false)`.
- A patch outside the phase list: a `block` decision. The agent's tool result reads
  `BLOCKED: <paths>: outside the allowed paths for the <phase> phase (<list>); patch not applied`.
- A command that changed a file outside the list: a `revert` decision; the tool result ends with
  `REVERTED: <paths>: outside the allowed paths for the <phase> phase (<list>); change reverted`.
- Any attempt on the feature list: `feature_list.json is written only by the harness`.
- After the agent calls `finish(claim="done")` in the build phase: either a `status_set` decision
  `F3 passes: visible-tests at <commit>` (demo-3 has no verify layer, so the evidence is a visible-test
  run) or a note `passes stays false for F3: <reason>`.

**Screen 1, bare arm.** "Harness decisions" shows `None: bare arm has no layers.` Watch its turn list
instead: an `apply_patch` or `run` that targets `app/api/middleware.py`, or a patch to `app/` after the
test phase starts. Nothing stops it; the referee counts it at the end.

**Screen 1, turn flags.** A turn with a refused or reverted change carries the "blocked" status; a
turn with a sandbox denial carries "denied" with its reason code. The bottom of each column shows
"Agent said" next to "Referee".

**Screen 3, Evidence, "Scope and sandbox" panel.** For each arm:

- Diff map (up to six paths): "changed" for files the arm changed, "blocked" or "reverted" for paths
  the scope layer refused, "out of scope" for paths the referee's `diff_scope` check flagged. The
  "out of scope" labels appear only after the referee has run.
- Sandbox denials: the last three, each with its reason code and command, or "none".

**Terminal, end of the A/B.** One line `A/B <ab_id> (F3, layers=[...])`, then one line per arm with
status, claim, `primary={"out_of_scope_files": n, "test_phase_source_edits": m}`, `passed=`, hidden
tests of 49, mutants of 4, reviewer verdict, and cost. Then the cost line.

**Sandbox moment.** Read one denial aloud: reason code first, then the command. A `network` denial
from `pip install` or `curl` is the common case: the agent tried to fetch something the image already
has.

---

## 6. Captured output and screenshots

Policy printout. This is the output of `render_policy` at this commit (deterministic code, not an agent
run; captured on 2026-10-16). It is also stored in every run's `run_start` event as `policy_summary`.

```text
Sandbox policy (identical for both arms)
  network: none
  cpus: 1.0
  memory: 1024 MB (swap: 0 MB)
  pids: 256
  user: 1000:1000
  read-only root: yes
  writable: /work, /tmp
  capabilities dropped: ALL
  tool timeout: 120 s; run timeout: 300 s
  refused commands: 6 rules (network access)
```

Run captures (each labelled "captured on <date>, run <id>; your output will differ"):

[[PENDING: terminal output of make demo-3 (A/B line, both arm lines, cost line) | source: M6 pilot | how: make demo-3]]

[[PENDING: screenshot of screen 1 with the harness arm showing at least one blocked or revert decision and both sandbox headers | source: M6 pilot | how: make demo-3, console key 1]]

[[PENDING: screenshot of screen 2 (both boards) during demo-3 | source: M6 pilot | how: make demo-3, console key 2]]

[[PENDING: screenshot of screen 3 "Scope and sandbox" panel, both arms, after the referee | source: M6 pilot | how: make demo-3, console key 3]]

[[PENDING: excerpt of sandbox_denied events from a demo-3 run log, or a note that none occurred | source: M6 pilot | how: grep -h sandbox_denied .shipharness/runs/<ab_id>/events.jsonl]]

[[PENDING: screenshot of screen 4 with the S3 dots and the demo run highlighted | source: M8 batch 1 | how: make demo-3, console key 4]]

[[PENDING: terminal output of make swap-3 | source: M6 pilot | how: make swap-3]]

[[PENDING: terminal output of make demo-3 LAYERS=-scope | source: M6 pilot | how: make demo-3 LAYERS=-scope]]

---

## 7. Experiment results for this section

Batch 1 runs F3 canonical with both arms, k=10 (DESIGN §10.4). Every run is a dot; results are
counts.

[[PENDING: S3 dots, bare vs harness, runs failing the primary measure out of 10, with the run ids, plus hidden_passed/49, regression_passed/regression_total and mutants_killed/4 per run | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation result for the scope layer (all layers minus scope) on the S3 tasks, runs failing the primary measure | source: M8 ablation | how: uv run shipharness report]]

[[PENDING: denial log from the experiment runs (reason codes and counts per arm, with run ids) for the sandbox moment fallback | source: M8 batch 1 | how: grep -h sandbox_denied .shipharness/runs/*/events.jsonl]]

---

## 8. Measured time and cost

Caps that apply (`src/shipharness/config/settings.py`; DESIGN §11.1): $0.20 per arm per run covering
the build and test phases, $0.04 per review, $2.50 per class session; 30 turns per session (F3
`session_budget` is `[30]`), `RUN_TIMEOUT_S` 300 s of agent time per arm, `HARNESS_TIMEOUT_S` 120 s of
harness work per arm, `TOOL_TIMEOUT_S` 120 s per command. The swap test makes no model calls.

[[PENDING: measured wall time and cost per arm for demo-3 (typical and worst case seen), plus reviewer cost | source: M6 pilot | how: make demo-3; read the cost line and wall_s in exports/scores/<run_id>.json]]

---

## 9. Troubleshooting and the replay fallback

| Symptom | Cause (from the code) | What to do |
|---|---|---|
| `x dataset not found: ...` or `x no task for feature=F3 ...` | `ab` reads `datasets/teamtrack-features-v1.jsonl` relative to the repository | Run from the repository root |
| Container start fails | Docker is not running in WSL2, or the images `shipharness-agent:1` / `shipharness-referee:1` are missing (`make doctor` checks only that the runtime is on PATH) | `docker info`; `docker images shipharness-agent`; build with `make images` |
| Red "UNSANDBOXED — results not official" badge | `SANDBOX_MODE=none`: tool commands run on the host with timeouts only; no board previews | Set `SANDBOX_MODE=docker`; never present an unsandboxed run as a result |
| An arm ends `ABORTED: cap` | A cost cap was reached; the referee still judges what the arm shipped | Show the run as a dot like any other; check the cost line for the session total |
| No `blocked` decision in the harness arm | The agent stayed inside the allowed paths in this run | Still state the by-construction zero; show `grep -h '"type":"blocked"' .shipharness/runs/*/events.jsonl` from the experiment runs |
| No `sandbox_denied` event tonight | No command hit a limit | Use the policy printout and the experiment denial log (section 2) |
| `make swap-3` prints ``x no recorded A/B for section demo-3 under .shipharness/runs; run `make demo-3` first, or pass AB=<id>`` | No demo-3 record in this runs directory | Run `make demo-3`, or pass `AB=<id>` |
| Swap or replay prints `... predates checkpoint SHA pinning ...` and exits 2 | The `ab.json` record has no `checkpoint_sha`, so the tree the arms started from cannot be recovered | Run the A/B again and use the new record |
| Swap test prints `judged measures DIFFERENT` | The referee did not judge the same build the same way | Do not present the result; keep the record and report it |
| Verdict says `referee could not judge the build: ...` | The diff did not apply or the referee container did not start | Read `referee.json` in the arm's referee directory; use the replay fallback |
| A board preview is missing on screen 2 | A preview that fails to start is logged and skipped; the A/B continues | Continue; screen 2 has no S3-specific content |

**Replay fallback.** Use it only when a live run fails on stage (brief §1.1.5).

```bash
make replay RUN=<ab or run id>   # = uv run shipharness replay <id>
```

`shipharness replay` re-emits the recorded event log into a new A/B id with every event marked
recorded, so every console screen shows a red RECORDING badge. It copies each arm's recorded diff and
runs the referee live on it at the recorded checkpoint commit and seed. The reviewer is off unless you
pass `--reviewer`. The terminal prints `RECORDING: replay <new id> of <source id> (<n> events)` and one
line per arm. Open the new A/B id in the console.

Recorded A/B to use as tonight's fallback:

[[PENDING: ab id of a recorded demo-3 A/B with at least one blocked decision in the harness arm, checked with make replay | source: M6 pilot | how: make replay RUN=<ab id>]]
