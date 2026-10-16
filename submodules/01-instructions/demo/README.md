# Demo 1: org-wide issue search (F1), instructions layer

Runbook for the S1 live A/B. The S1 block is 50 minutes: concepts 15, walkthrough 10, live A/B 15,
results 10 (DESIGN §14.1). This file covers the walkthrough, the live A/B, and the results. The
concepts are in [../concepts.md](../concepts.md).

There is no `run.sh`: every step is a Make target, and each target is a thin wrapper over
`uv run shipharness ...` (see the `Makefile`). Run everything inside WSL2 on the class host.

---

## 1. Purpose and the problem this demo shows

Both arms build F1, `GET /issues` (org-wide issue search with filters and cursor pagination,
`teamtrack/docs/features/f1.md`), from checkpoint `m1-s1-start`, with the same ticket, model, effort,
tools, turn budget, cost cap, and sandbox. The harness arm runs one layer, `instructions` (DESIGN
§6.6): an `AGENTS.md` map and the `add-endpoint` skill's name and description in its context prefix,
with the focused docs and the skill body on disk. The bare arm has the same rules in
`docs/HANDBOOK.md` on disk and nothing injected.

The repository holds a trap: the legacy `GET /v1/issues` handler and its query
`repositories.issues.list_all_legacy`, which list issues without the org filter (DESIGN §4.3). A1
reports that "Codex replicates patterns that already exist in the repository—even uneven or suboptimal
ones." (A1, F-a-20). The demo shows whether each arm ships a `GET /issues` that gives an Acme user
Globex data, judged by the referee's R1 check (every endpoint and method as Acme with Globex IDs,
expect 404; DESIGN §5).

Pre-registered primary measure: a run fails if `r1_new_violations >= 1` (DESIGN §8.2; dataset field
`primary_measure` of `F1-canonical`).

---

## 2. Commands

Before class (no model cost):

```bash
make doctor          # keys, Docker CLI, prices; must end with "result: + ready"
make console         # live console at http://127.0.0.1:8765/ (leave it running)
```

In class:

```bash
make demo-1                          # the A/B: F1 canonical, harness arm = instructions
make swap-1                          # swap test on the latest demo-1 A/B; no model calls
make demo-1 LAYERS=-instructions     # layer switch: a second A/B with the layer removed
make replay RUN=<ab or run id>       # fallback only, see section 9
```

What each one runs:

| Target | Command (from the `Makefile`) | Model calls |
|---|---|---|
| `make demo-1` | `uv run shipharness ab --section demo-1 --feature F1` | Builder and test writer in both arms; the blinded reviewer on both diffs (the `ab` command's default) |
| `make swap-1` | `uv run shipharness ab --swap latest --section demo-1` | None. Each arm's diff is judged again under the other arm's label; `AB=<id>` picks another A/B |
| `make demo-1 LAYERS=-instructions` | `uv run shipharness ab --section demo-1 --feature F1 --layers=-instructions` | Same as `make demo-1` |
| `make replay RUN=<id>` | `uv run shipharness replay <id>` | None (reviewer off by default) |

The layer switch removes the only layer of the demo-1 stack, so the harness arm runs with no layers
(`section_layers` in `src/shipharness/ab/demo.py`) and both arms are bare. The A/B line prints
`layers=[]`. Use it to show that the gap belongs to the layer: with the layer gone, any difference
between the arms is run-to-run variation. A3 describes the same method: "removing one component at a
time and reviewing what impact it had on the final result." (A3, F-a-125).

`make demo-1` prints one line per arm (arm, status, claim, primary measure, `passed`, hidden tests
passed/total, mutants, reviewer verdict, cost), then a `Cost:` line with the session total against the
$2.50 session cap. `passed=True` means the run did not fail the primary measure. Exit code: 0, or 2 if
any arm ended `ABORTED`, or 1 if any arm ended `ERROR` (`src/shipharness/ab/commands.py`).

---

## 3. Screen sequence and code anchors

Console keys (DESIGN §13): `1` Live Console, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces.
`F` shows one arm full screen.

### Walkthrough (10 minutes, before the A/B)

Open these in the editor, in this order. Print an anchor with
`uv run python scripts/anchors.py extract <id>`.

| Min | Open | Point at |
|---|---|---|
| 2 | `teamtrack/app/api/legacy_v1.py` (28 lines) and `teamtrack/app/repositories/issues.py` lines 19-26 and 53-55 | The legacy handler and its unscoped query, in the same file as the scoped `list_for_project` the agent should copy |
| 3 | Anchor `S1:agents_md` (`teamtrack/harness/instructions/AGENTS.md`, lines 1-38 of 94) | "a table of contents, not the manual"; the "Where to look" row for endpoints points to the skill; R1 "404, never 403". Scroll below the anchor to "Do not copy" |
| 2 | Anchor `S1:progressive` (`src/shipharness/runner/skills_loader.py`) | Tier 1 only (`catalogue_block`); tiers 2 and 3 load through `read_file`; `skill_for_path` reports the tier |
| 3 | Anchor `S1:prefix` (`src/shipharness/harness/instructions/router.py`) | `build_prefix`: the map plus the catalogue, built from the course checkout, never from the workspace |

### Live A/B (15 minutes)

| Step | Key | What to do |
|---|---|---|
| 1 | — | Glance at the easy control task in the `section-1` subset, C1 "Filter the user list by role" (`teamtrack/docs/features/c1.md`). Control tasks are ones both arms should pass (DESIGN §10.1), which shows the comparison is fair. Show the spec only; do not run it |
| 2 | — | Poll (section 4) |
| 3 | — | `make demo-1` |
| 4 | `1` | Turn lists side by side. Harness arm: `note` lines when it opens a doc or the skill. Bare arm: which files it reads and searches first |
| 5 | `2` | Both boards as an Acme user, cards from another org marked ⚠ |
| 6 | `3` | Files-read map per arm, then the referee list (`R1: n new`) as checks finish |
| 7 | `5` | Optional: live tail of the event stream |

### Results (10 minutes)

| Step | Key | What to do |
|---|---|---|
| 1 | `4` | Tonight's run as one more dot next to the batch 1 dots for F1; runs failing out of k per arm |
| 2 | — | `make swap-1`: "judged measures identical" (no model cost). If the session meter has room, `make demo-1 LAYERS=-instructions` instead or after |
| 3 | — | Discussion: what did each arm read before it wrote the query? |

---

## 4. Poll question

> Both arms can open `docs/HANDBOOK.md`, which says "Do not copy" about `GET /v1/issues`. Out of 10
> bare-arm runs of F1, how many ship `GET /issues` with at least one new R1 violation?
> A) 0-2  B) 3-5  C) 6-8  D) 9-10

Answer pattern from the experiments:

[[PENDING: bare and harness runs failing out of 10 for F1 canonical (r1_new_violations>=1), to state the poll answer | source: M8 batch 1 | how: make report]]

---

## 5. What to watch

Screen 1, Live Console:
- Harness arm, first decision: `placed 31 instruction files (AGENTS.md map, docs, skills)` (the 31
  files under `teamtrack/harness/instructions/`; message format from
  `src/shipharness/harness/instructions/layer.py`).
- Harness arm, notes in the turn list: `agent read skill add-endpoint (tier 2): .agents/skills/add-endpoint/SKILL.md`
  and `agent read docs/SECURITY.md`. A tier 3 note means it also opened `references/tests.md`.
- Both arms: `read_file` and `search` calls on `app/api/legacy_v1.py`, `app/services/legacy.py`, or
  `list_all_legacy`. Then the `apply_patch` to `app/repositories/issues.py`: does the new query filter
  on `org_id`, and does it page by id with `page` and `split_page`, or by `offset`?
- The `Referee` line: pending, then pass or fail on the primary measure.

Screen 2, Boards:
- A card is marked ⚠ other org when its `data-org` is not the viewer's org
  (`src/shipharness/console/board_capture.py`). F1 adds an API endpoint that the board does not call,
  so a leak in `GET /issues` shows on the board only if the arm's change also reaches code the board
  uses (for example `list_for_project`). A clean board does not mean a clean endpoint; the R1 check is
  the evidence.

Screen 3, Evidence:
- Files read, grouped as map, skill, harness doc, state, handbook, code, test. Does the bare arm's list
  contain `handbook`? Does the harness arm's contain `skill` or `harness doc`? Only `read_file` calls
  count; a `cat` through `run` does not appear.
- Referee: `R1: n new` per arm, and the R3 line for the list envelope and error shape.

Screen 4, A/B Report: tonight's dot sits next to the batch 1 dots. Read counts, never percentages
(DESIGN §8.3 rule 5).

---

## 6. Captured output and screenshots

Each capture is labelled "captured on <date>, run <id>; your output will differ" (brief §1.1.4).

[[PENDING: terminal output of make demo-1 (A/B line, one line per arm, Cost line), labelled with date and ab id | source: M6 pilot | how: make demo-1]]

[[PENDING: screenshot of screen 1 Live Console mid-run, harness arm showing a skill note | source: M6 pilot | how: make demo-1, then key 1]]

[[PENDING: screenshot of screen 2 Boards for both arms as admin@acme.test | source: M6 pilot | how: make demo-1, then key 2]]

[[PENDING: screenshot of screen 3 Evidence with both files-read maps and the R1 referee line | source: M6 pilot | how: make demo-1, then key 3]]

[[PENDING: screenshot of screen 4 A/B Report with the F1 dots | source: M8 batch 1 | how: make report, then make console and key 4]]

[[PENDING: screenshot of screen 5 Traces live tail | source: M6 pilot | how: make demo-1, then key 5]]

[[PENDING: terminal output of make swap-1 ("Swap test on <ab id>: judged measures identical") | source: M6 pilot | how: make swap-1]]

[[PENDING: terminal output of the layer switch showing layers=[] and both arms' lines | source: M6 pilot | how: make demo-1 LAYERS=-instructions]]

---

## 7. Experiment results for this section

Batch 1 runs F1-F4 canonical, two arms, k=10 each, reviewer on (DESIGN §10.4).

[[PENDING: F1 canonical dots, runs failing out of 10 per arm, with run ids | source: M8 batch 1 | how: make report]]

[[PENDING: F1 canonical secondary counts per arm (r1_leaks, r3_new_failures, hidden passed of 52, existing tests keep passing) | source: M8 batch 1 | how: make report]]

[[PENDING: ablation, leave-out-instructions configuration (all minus instructions) on the 12 ablation tasks of DESIGN §10.4 | source: M8 ablation | how: make report]]

---

## 8. Measured time and cost

The limits are fixed in configuration (`.env.example`, DESIGN §11.1): `MAX_RUN_COST_USD` $0.20 per arm
per run (build and test phases together), `MAX_REVIEW_COST_USD` $0.04 per review,
`MAX_SESSION_COST_USD` $2.50 for the whole class session, `RUN_TIMEOUT_S` 300 s of agent time per arm,
`HARNESS_TIMEOUT_S` 120 s of harness work per arm, `TOOL_TIMEOUT_S` 120 s per tool command. The layer
switch is a second full A/B under the same caps; run it only if the `Cost:` line shows room under the
session cap (DESIGN §11.3).

[[PENDING: measured wall time and cost per arm for make demo-1, worst case seen, with run ids | source: M6 pilot | how: make demo-1]]

[[PENDING: measured reviewer cost per review in demo-1 | source: M6 pilot | how: make demo-1]]

[[PENDING: worst-case cost and wall time per arm across F1 canonical runs | source: M8 batch 1 | how: make report]]

---

## 9. Troubleshooting and the replay fallback

| Symptom | Cause (from the code) | Fix |
|---|---|---|
| `make doctor` marks `OPENAI_API_KEY` (or `LANGSMITH_API_KEY`) `x missing`, detail `not set`, next step "add it to .env at the repo root" | Key not set (`src/shipharness/doctor.py`) | Add the key to `.env`, run `make doctor` until it ends `result: + ready` |
| `make doctor` marks a key `x invalid`, detail `... key invalid (rejected by ...)` | The service answered 401 or 403 | Create a new key in that account, update `.env` |
| `make doctor` marks a key `! unreachable`, detail `could not reach ...` | Network or proxy | Check the connection; nothing else will work until this passes |
| `make doctor` marks `container runtime` `! warn`, detail `docker not found: only the UNSANDBOXED fallback can run` | No `docker` on PATH | Install Docker Engine in WSL2 (class host, DESIGN D-22). Do not run the class demo unsandboxed: every screen would show "UNSANDBOXED — results not official" |
| `make doctor` passes, but an arm ends `ERROR` with `docker run failed: ...` and the command exits 1 | Doctor only checks that the `docker` CLI is on PATH. The arm container did not start: daemon stopped, or image `shipharness-agent:1` / `shipharness-referee:1` missing (`src/shipharness/sandbox/docker.py`) | `docker info`; on the class host `sudo systemctl start docker` inside Ubuntu; `make images` rebuilds both images. Then rerun, or replay |
| An arm ends `ABORTED: cap`; the command exits 2 | The cost tracker refused the next call (`cost cap reached: run $... of $0.20`, `src/shipharness/cost/tracker.py`). The referee still judges the arm | Keep the run: aborted runs are kept, scored, and shown (DESIGN §8.3 rule 9). If the `Cost:` line shows the session cap reached, skip the layer switch and use the replay for anything else |
| An arm ends `ABORTED: timeout` | `RUN_TIMEOUT_S` (300 s of agent time) reached (`src/shipharness/runner/loop.py`) | Same as a cap abort: it is a dot |
| `make swap-1`: `x ...; run make demo-1 first, or pass AB=<id>` | No demo-1 A/B recorded yet | Run `make demo-1`, or `make swap-1 AB=<id>` |
| `make replay`: `! replay needs RUN=<ab or run id>` | `RUN` not given | `make replay RUN=<id>` |
| Screen 2 shows no board for an arm | The board preview is display only; a preview that fails to start is skipped and the run continues (VERIFICATION.md, M4 final review) | Continue with screens 1 and 3 |

### Replay fallback

Use it only when the live run fails on stage (API outage, rate limit, Docker failure), never to
replace a run that worked but gave an unwelcome result (DESIGN §8.3, forbidden list).

```bash
make replay RUN=<ab or run id>
```

The replay re-emits the recorded event log with a red RECORDING badge on every screen, applies the
recorded diff to a fresh export of the pinned checkpoint commit, and runs the referee live
(`src/shipharness/ab/recorded.py`). With the default settings it makes no model calls. The id of a
live run is in the `A/B <ab id> (F1, layers=[...])` line and in `.shipharness/runs/<ab id>/`.

[[PENDING: ab id of the recorded F1 demo-1 fallback run kept for class | source: M6 pilot | how: make demo-1]]
