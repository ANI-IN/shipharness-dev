# S4 demo: `make demo-4` (F4, all layers)

Runbook for the S4 live A/B. Class plan (DESIGN §14.1): glance at an easy control task, poll,
`make demo-4`, screens 1, 2, 3; then results on screen 4, the swap test or the layer switch, and
discussion. Concepts: [../concepts.md](../concepts.md).

Every captured output and screenshot in this file is labelled "captured on <date>, run <id>; your
output will differ". Items that need a real run are marked `[[PENDING ...]]` until the pilot (M6),
batch 1 (M8), or the live class fills them.

---

## 1. Purpose and the problem this demo shows

Both arms build F4, optimistic concurrency and issue history (`teamtrack/docs/features/f4.md`), from
checkpoint `m1-s4-start`, with the same ticket, model, tools, sandbox, turn budget, and cost cap. The
bare arm runs with no layers; the harness arm runs all four (DESIGN §6.6).

The problem: the `If-Match` header is optional, so every existing test keeps passing whether or not
concurrency works. An agent can test the happy path, call `finish(claim="done")`, and ship a board
where two people editing one issue silently overwrite each other. In the bare arm nothing checks
the claim. In the harness arm the verify gate runs before "done" is accepted, the five filters
decide which tests the agent ships, and the referee judges both arms on two counts neither arm can
see: hidden tests passed (of 69) and referee-set mutants killed by the shipped tests (of 4).

## 2. Commands

Run everything inside WSL2 from the repository root (`~/shipharness`).

Before class:

```sh
make doctor          # keys, Docker, versions; fix anything that is not ok
make console         # second terminal: console at http://localhost:8765
```

In class:

```sh
make demo-4                     # A/B on F4: bare vs all layers, then the referee and reviewer
make swap-4                     # swap test on the latest demo-4 A/B (no model calls)
make demo-4 LAYERS=-verify      # layer switch: harness arm without the verify layer
make replay RUN=<ab or run id>  # fallback only: replays a recorded A/B, referee runs live
```

What each one runs (`Makefile`):

| Target | Command |
|---|---|
| `make demo-4` | `uv run shipharness ab --section demo-4 --feature F4` |
| `make swap-4` | `uv run shipharness ab --swap latest --section demo-4` (`AB=<id>` picks another A/B) |
| `make demo-4 LAYERS=-verify` | `uv run shipharness ab --section demo-4 --feature F4 --layers=-verify` (harness arm: instructions, state, scope) |
| `make replay RUN=<id>` | `uv run shipharness replay <id>` |

`make demo-4` prints `A/B <ab_id> (F4, layers=[...])`. Open `http://localhost:8765/run/<ab_id>`
(or pick the run on `http://localhost:8765/`). Keys `1` to `5` switch screens; `F` shows one arm
full screen.

The layer switch runs both arms again and calls the model. Each arm is capped at `MAX_RUN_COST_USD`
($0.20) and each review at `MAX_REVIEW_COST_USD` ($0.04) (`.env.example`). DESIGN §11.3 allows one
optional layer-switch rerun only if the session meter shows room; the session cap
(`MAX_SESSION_COST_USD`, $2.50) blocks it otherwise. Check the last line `make demo-4` printed
(`Cost: ... session $<spent> of $2.50`) before choosing the layer switch over the swap test.

## 3. Screen sequence and code anchors

| When | Key | Screen | Show |
|---|---|---|---|
| While the arms build | `1` | Live Console | Harness arm: gate pills ⏳ then ✓/✗ after each `finish(done)`; harness decisions; bare arm: "No gate (verify layer off)." |
| End of the runs | `2` | Boards | The "Two-tab edit conflict" panel: ✗ lost update or ✓ conflict detected, per arm |
| Referee running | `3` | Evidence | Verification panel: referee counters, test filter table (1-5) with discard reasons, coverage line, mutant matrix |
| Results | `4` | A/B Report | S4 dots for both co-primary counts, tonight's run next to the experiment runs |
| After results | `1` | Live Console | "Agent said" vs "Referee" for each arm |

Code walkthrough (about 10 minutes, before the live A/B; `uv run python scripts/anchors.py extract
<id>` prints each one):

| Order | Anchor | File and lines | Point at |
|---|---|---|---|
| 1 | `S4:filters` | `src/shipharness/filters/pipeline.py:34-74` | A test stops at its first failing filter; every result is published with a reason |
| 2 | `S4:probe` | `src/shipharness/checks/r1_tenant.py:65-104` | R1: a foreign id must give 404; a 2xx carrying Globex data is a leak |
| 3 | `S4:blind` | `src/shipharness/reviewer/blind.py:15-39` | What the reviewer never sees: harness artifacts, commit metadata, workspace paths, run ids, the arm label |
| 4 | `S4:gate` | `src/shipharness/harness/verify/gate.py:133-172` | Pending pills first, checks in the arm container, feedback only on failure; `GATE_CHECKS` (lines 31-41) has no hidden tests or mutants |

## 4. Poll question and answer pattern

Ask before `make demo-4`:

> Both arms will probably say "done". F4's `If-Match` header is optional, so every existing test
> passes even if no concurrency check was built. The referee holds four mutants the agents never
> see; one makes writes stop moving the version (`version += 0`), which brings back lost updates.
> How many of the four will each arm's shipped tests kill?
>
> A. Both arms kill all four.
> B. The harness arm kills more than the bare arm.
> C. About the same for both arms.
> D. Neither arm kills the lost-update mutant.

Answer pattern from the experiments:

[[PENDING: S4 poll answer pattern: referee mutants killed per arm across batch 1 runs (how often each of A-D held), plus tonight's result | source: M8 batch 1 | how: make report]]

## 5. What to watch

Screen 1, Live Console:

- Harness arm, after `finish(claim="done")` in the build phase: pills for `visible tests`,
  `existing tests`, `R1` to `R7`, `board`, and `clean state` appear as ⏳, then turn ✓ or ✗
  (`run_gate` in `gate.py`). Progress labels such as `R1 probes <done>/<total>` show the gate
  working (`probe_all` in `r1_tenant.py`).
- On a failed gate, the harness decision shows the feedback the agent received:
  `Gate <id>: <n> of <m> items failed (<names>).`, up to three failure lines, then `Fix these,
  commit your work, and call finish again.` (`_feedback` in `gate.py`). Watch the next turns: does
  the agent fix the named item, or work around it?
- After the test phase: the decision `test filters: kept <n>, discarded <m>` (`verify/layer.py`).
- Bare arm: "No gate (verify layer off)." and "None: bare arm has no layers." The phase ends on the
  agent's claim.
- Bottom of each panel: "Agent said" next to "Referee", then supported or unsupported. For F4 the
  referee mark is ✓ only when all 69 hidden tests pass and all 4 referee mutants are killed
  (`evaluate_primary` in `src/shipharness/ab/score.py`).

Screen 2, Boards:

- The conflict panel appears once per arm after its run ends (the preview container captures it
  for F4 only; `src/shipharness/ab/runtime.py`). The screenshot banner reads `✗ LOST UPDATE: tab B
  overwrote tab A without a conflict` or `✓ CONFLICT DETECTED: tab B got HTTP <status>`; a line
  starting `!` means the save failed some other way (`capture_conflict` in
  `src/shipharness/console/board_capture.py`).

Screen 3, Evidence, Verification panel:

- Referee rows per rule (`R1: <n> new` and so on) and, after the review, `reviewer accept` or
  `reviewer reject` with the tenant-isolation risk.
- Test filters (1-5): one row per proposed test, ✓/✗ per filter, `kept` or `discarded`, and the
  discard reason under the row. Point at one discard and read its reason aloud.
- `Coverage (filter 3: adds coverage or kills a mutant): <x> of <y> tests`.
- Mutants: one row per mutant, columns "filter set" and "referee set", outcome `killed` or
  `survived`. In `make demo-4` expect the filter-set column to show `–`: the verify layer's test
  phase builds its filter context without a mutant list (`filters_pipeline` in
  `src/shipharness/harness/verify/testphase.py`), so only the referee's rows appear. Find
  `app.services.issues-m401` (the lost-update mutant) for each arm.

Screen 4, A/B Report: two dot rows for F4, `hidden_passed` (of 69) and `mutants_killed` (of 4), one
dot per run per arm, with counts, never percentages.

Terminal: `make demo-4` ends with one line per arm in this format (`_print_record` in
`src/shipharness/ab/commands.py`), then the cost line:

```text
  <arm> <status> claim=<claim> primary={"hidden_passed": <x>, "mutants_killed": <y>} passed=<bool> hidden <x>/69 mutants <y>/4 reviewer=<verdict> cost=$<usd>
Cost: $<this command> (this command: <model> $<usd>, ...; session $<spent> of $2.50)
```

`make swap-4` prints `Swap test on <ab_id>: judged measures identical` and exits 0; any difference
is listed field by field and the exit code is 1 (`src/shipharness/ab/commands.py`).

## 6. Captured output and screenshots

Each item below is labelled "captured on <date>, run <id>; your output will differ" once filled.

[[PENDING: terminal output of make demo-4 (A/B line, both record lines, cost line) | source: M6 pilot | how: make demo-4]]

[[PENDING: screenshot, screen 1 Live Console during the harness arm's first gate (pills pending, then results; bare arm "No gate") | source: M6 pilot | how: make demo-4 with make console open, key 1]]

[[PENDING: screenshot, screen 1 Live Console after the referee ("Agent said" vs "Referee" for both arms) | source: M6 pilot | how: make demo-4, key 1]]

[[PENDING: screenshot, screen 2 Boards with the two-tab edit conflict panel for both arms | source: M6 pilot | how: make demo-4, key 2]]

[[PENDING: screenshot, screen 3 Evidence, Verification panel (referee counters, filter table with a discard reason, coverage line, mutant matrix) | source: M6 pilot | how: make demo-4, key 3]]

[[PENDING: screenshot, screen 4 A/B Report with the S4 dots | source: M8 batch 1 | how: make report, then make demo-4, key 4]]

[[PENDING: terminal output of make swap-4 | source: M6 pilot | how: make swap-4]]

[[PENDING: terminal output and screen 1 of make demo-4 LAYERS=-verify | source: M6 pilot | how: make demo-4 LAYERS=-verify]]

## 7. Experiment results for this section

Batch 1 runs F4 canonical, two arms, k=10 (DESIGN §10.4). Each run is a dot for each co-primary
count.

[[PENDING: S4 batch 1 dots (hidden x/69 and referee mutants y/4, per run, bare vs harness) with run ids and the LangSmith comparison link | source: M8 batch 1 | how: make experiments BATCH=1, then make report]]

[[PENDING: S4 secondary measures from batch 1 (existing tests, R1-R7 new violations, flaky tests, reviewer agreement) | source: M8 batch 1 | how: make report]]

[[PENDING: leave-one-out result with the verify layer removed, on the ablation tasks | source: M8 ablation | how: make experiments BATCH=2, then make report]]

## 8. Measured time and cost

Limits from the repository (not measurements): agent time per arm `RUN_TIMEOUT_S` 300 s, harness
work per arm `HARNESS_TIMEOUT_S` 120 s, tool command `TOOL_TIMEOUT_S` 120 s (`.env.example`); F4
session budget 40 turns (`teamtrack/reference/f4/task.toml`); cost caps $0.20 per arm and $0.04 per
review (DESIGN §11.1). The class budget reserves $0.40 for the two demo-4 arms and $0.08 for the two
S4 reviews (DESIGN §11.3). The design target for a demo is at most 6 minutes (DESIGN §16, AS-9).

[[PENDING: measured wall time of make demo-4 per arm, plus referee time, worst case seen | source: M6 pilot | how: make demo-4 (wall_s, agent_wall_s, harness_wall_s in exports/scores)]]

[[PENDING: measured cost of make demo-4 per arm and per review, worst case seen | source: M6 pilot | how: make demo-4 (cost line and exports/scores)]]

[[PENDING: tonight's time and cost of make demo-4 | source: live class | how: make demo-4]]

## 9. Troubleshooting and the replay fallback

| Symptom | Cause (from the code) | What to do |
|---|---|---|
| `make swap-4` prints a line starting `x` that ends "run `make demo-4` first, or pass AB=<id>", and exits 2 | No demo-4 A/B in `RUNS_DIR` (`.shipharness/runs`) | Run `make demo-4`, or pass `AB=<id>` of a recorded A/B |
| `make swap-4` or `make replay` prints `x ...` about an unpinned record and exits 2 | The A/B record has no `checkpoint_sha` (`UnpinnedRecord` in `src/shipharness/ab/recorded.py`) | Use an A/B recorded after SHA pinning |
| Every gate pill ✗ with `could not write the check inputs in the container` or `check runner failed (exit <n>)` | The harness time limit (`HARNESS_TIMEOUT_S`) ran out; every gate command is capped by the harness time left (`GateConfig.limit`) | Keep the run: it is scored like any other (DESIGN §8.3 rule 9). Say what happened; show the experiment dots |
| A tool result reads `Refused, not run: ...` | A tool call came after the run or session ended (CONTRACTS §22) | Nothing to fix; the referee still judges the shipped diff |
| Status `ABORTED: cap` or `ABORTED: timeout` | Run cost cap or `RUN_TIMEOUT_S` reached (`runner/loop.py`) | The referee still runs; the run stays a dot (DESIGN §11.1, §8.3 rule 9) |
| No "Two-tab edit conflict" panel; boards say "No board screenshot yet" | The preview container failed to start and was skipped (CONTRACTS §21) | Use screen 3 (board check) and the hidden board tests counted in `hidden <x>/69` |
| `mutants 0/0` in the record | The mutant set could not be loaded; the run continues and scores 0/0 (DESIGN D-21) | Run `uv run shipharness datasets validate` (checks that every mutant set exists); the run still counts as recorded |
| `reviewer=None` | The review was incomplete, refused, failed, or hit `MAX_REVIEW_COST_USD` (`reviewer/review.py`) | Primary counts are unaffected; say so |
| Verdict text `referee could not judge the build: ...` | The referee container failed to start (`ab/referee.py`) | Check Docker (`make doctor`), then `make swap-4` re-judges the recorded diffs without model calls |
| Red badge `UNSANDBOXED — results not official` | `SANDBOX_MODE` is not `docker` | Set `SANDBOX_MODE=docker` in `.env`, start Docker Engine in WSL2, `make doctor` |
| Layer-switch arms end at once with `ABORTED: cap` | Session cap reached (`MAX_SESSION_COST_USD`); the tracker reserves each call's worst case first (DESIGN §11.1) | Use `make swap-4` (no model calls) and the ablation dots instead |

### Replay fallback

Use only when the live run fails on stage. `make replay RUN=<id>` takes an A/B id or run id. It
re-emits the recorded events with `recorded=True` (red RECORDING badge on every screen), applies the
recorded diffs to a fresh export of the pinned checkpoint commit, and runs the referee live
(`src/shipharness/ab/recorded.py`). The reviewer is off by default for `replay`, so no model is
called. The terminal prints `RECORDING: replay <new id> of <source id> (<n> events)`, the record
lines, and the cost line.

[[PENDING: run id of the recorded F4 A/B to use for make replay, with its capture date | source: M6 pilot | how: make demo-4, then note the A/B id]]
