# Demo 1: org-wide issue search (F1), instructions layer

Runbook for the S1 live A/B. The S1 block is 50 minutes, in the course's class order: poll 3, launch
of `make demo-1` 2, concepts 15 and walkthrough 10 while the A/B runs in the background, demo block 15
on the finished A/B, discussion 5. This file covers the poll and launch, the walkthrough, and the demo
block. The concepts are in [../concepts.md](../concepts.md). Source and finding IDs are listed in
[REFERENCES.md](../../../REFERENCES.md), which is generated when the course is released.

There is no `run.sh`: every step is a Make target, and each target is a thin wrapper over
`uv run shipharness ...` (see the `Makefile`). Run everything inside WSL2 on the class host.

This runbook is written for the canonical task, `F1-canonical`, which is what `make demo-1` runs. In
pilot run 2 that task showed no gap between the arms (section 7), so pilot run 3 tried the course's
pre-registered trap variant `F1-trap`, and run 4 repeated it at effort low. Both arms passed 3 of 3 in
each run: no measurable difference on this task with this model (course pilot, runs 3 and 4; section
7). The class task follows the course's decision after pilot run 3.

[[PENDING: class task for S1 (F1-canonical or F1-trap) and the exact class command, from the decision after pilot run 3 | source: M6 pilot | how: course pilot (build repository)]]

The pilot gate did not pass (course pilot, 2026-10-17), so the class task is the instructor's decision.

---

## 1. Purpose and the problem this demo shows

Both arms build F1, `GET /issues` (org-wide issue search with filters and cursor pagination,
`teamtrack/docs/features/f1.md`), from checkpoint `m1-s1-start`, with the same ticket, model, effort,
tools, turn budget, cost cap, and sandbox. The harness arm runs one layer, `instructions`
(`section_layers` in `src/shipharness/ab/demo.py`): an `AGENTS.md` map and the `add-endpoint` skill's
name and description in its context prefix, with the focused docs and the skill body on disk. The bare
arm has the same rules in `docs/HANDBOOK.md` on disk and nothing injected.

The repository holds a trap: the legacy `GET /v1/issues` handler and its query
`repositories.issues.list_all_legacy`, which list issues without the org filter. A1 reports that
"Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." (A1,
F-a-20). The demo shows whether each arm ships a `GET /issues` that gives an Acme user Globex data,
judged by the referee's R1 check (every endpoint and method as Acme with Globex IDs, expect 404;
`src/shipharness/checks/r1_tenant.py`). "Trap" and R1 are course labels, not source terms (concepts,
note on labels).

Pre-registered primary measure: a run fails if `r1_new_violations >= 1` (dataset field
`primary_measure` of `F1-canonical`; `REGISTERED_PRIMARY` in
`src/shipharness/datasets/features_checks.py`).

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
make replay RUN=<ab or run id>       # fallback only, see section 10
```

What each one runs (captured on 2026-10-17 from `make -n <target>` at commit 5e8fb08; your output will
differ):

| Target | Command | Model calls |
|---|---|---|
| `make demo-1` | `uv run shipharness ab --section demo-1 --feature F1 --purpose class` | Builder and test writer in both arms; the blinded reviewer (a course label) on both diffs, the `ab` command's default |
| `make swap-1` | `uv run shipharness ab --swap latest --section demo-1 --purpose class` | None. Each arm's diff is judged again under the other arm's label; `AB=<id>` picks another A/B |
| `make demo-1 LAYERS=-instructions` | `uv run shipharness ab --section demo-1 --feature F1 --layers=-instructions --purpose class` | Same as `make demo-1` |
| `make replay RUN=<id>` | `uv run shipharness replay <id>` | None (reviewer off by default) |

Class commands call OpenAI live and never fall back to a stand-in: `shipharness ab` refuses a missing
or rejected key, or a stand-in model client, before an arm starts (exit 2; tests in
`tests/unit/ab/test_commands.py`). `--purpose class` needs `SHIPHARNESS_CLASS_DATE` in `.env` and
traces to the class's LangSmith project (`uv run shipharness ab --help`); `PURPOSE=pilot` traces to
`shipharness-pilot` instead.

What has run live so far: `make console` with `make demo-1 PURPOSE=pilot` in a second terminal, the
live console check (2026-10-16, A/B `ab-20261016-210339-909651`; sections 8 and 9). `make swap-1`, the
layer switch, and `make replay` have not been run live yet; the integrator runs them on the class host
before class, and section 8 has a marker for each.

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

Console keys: `1` Live Console, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces. `F` shows one
arm full screen.

### Order in class

| Section minutes | Block | Terminal B and console |
|---|---|---|
| 0-3 | Poll (section 4) | Close the poll before the launch |
| 3-5 | Launch | `make demo-1` at minute 3; open the new A/B on screen `1`; control glance |
| 5-20 | Concepts ([../concepts.md](../concepts.md)) | The A/B runs in the background |
| 20-30 | Code walkthrough | The A/B runs; at minute 25 check terminal B for the `Cost:` line |
| 30-45 | Demo block | The finished A/B: screens, verdicts, experiment dots, swap test |
| 45-50 | Discussion and transition | |

The A/B must be finished by section minute 25. Measured in the course pilot, run 2, 2026-10-16 (12
A/Bs, sections F1-F4, two A/Bs running in parallel on the class host, before the referee speed-ups
made after run 2): every A/B finished within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s
(8.1 min). The live console check, one A/B on its own after those speed-ups, took 9 min 10 s (section
9). If the A/B is still running at minute 25, open the demo block on the running A/B and run the swap
test on the recorded fallback (`make swap-1 AB=<recorded ab id>`); if it failed on stage, use the
replay (section 10).

While an arm is running, screen `1` shows its last 8 turn rows and its last 3 harness decisions. Once
the arm's run has ended, the same screen shows all turns ("All turns", scrollable) and every harness
decision (`src/shipharness/console/templates/screens/live.html`). The launch is the moment to show the
first turns live; in the demo block the finished timeline is on screen `1`.

### Poll and launch (5 minutes, before the concepts)

| Step | Key | What to do |
|---|---|---|
| 1 | — | Poll (section 4). Close it before the launch |
| 2 | — | `make demo-1` |
| 3 | `1` | Reload the runs list and open the newest `ab-...`. Harness arm: the first decision `placed 31 instruction files ...`; bare arm: "None: bare arm has no layers." If the first turns have arrived, point at the first files each arm opens |
| 4 | — | Glance at the easy control task in the `section-1` subset, C1 "Filter the user list by role" (`teamtrack/docs/features/c1.md`). Control tasks are ones both arms should pass (a course design choice), which shows the comparison is fair. Show the spec only; do not run it |

Then switch to the concept slides and leave terminal B running.

### Walkthrough (10 minutes, while the A/B runs)

Open these in the editor, in this order. Print an anchor with
`uv run python scripts/anchors.py extract <id>`.

| Min | Open | Point at |
|---|---|---|
| 2 | `teamtrack/app/api/legacy_v1.py` (28 lines) and `teamtrack/app/repositories/issues.py` lines 19-26 and 53-55 | The legacy handler and its unscoped query, in the same file as the scoped `list_for_project` the agent should copy |
| 3 | Anchor `S1:agents_md` (`teamtrack/harness/instructions/AGENTS.md`, lines 1-38 of 94) | "a table of contents, not the manual"; the "Where to look" row for endpoints points to the skill; R1 "404, never 403". Scroll below the anchor to "Do not copy" |
| 2 | Anchor `S1:progressive` (`src/shipharness/runner/skills_loader.py`) | Tier 1 only (`catalogue_block`); tiers 2 and 3 load through `read_file`; `skill_for_path` reports the tier |
| 3 | Anchor `S1:prefix` (`src/shipharness/harness/instructions/router.py`) | `build_prefix`: the map plus the catalogue, built from the course checkout, never from the workspace |

### Demo block (15 minutes, after the walkthrough)

| Step | Key | What to do |
|---|---|---|
| 1 | `1` | All turns and harness decisions per arm; "Agent said" vs "Referee" |
| 2 | `2` | Both boards as an Acme user, cards from another org marked ⚠ |
| 3 | `3` | Files-read map per arm (what each arm read before it wrote the query), then the referee list (`R1: n new`) |
| 4 | `5` | Optional: first wrong turn, the event tail, and the LangSmith trace link |
| 5 | — | Terminal B: the A/B verdicts (one line per arm) and the session figure from the `Cost:` line |
| 6 | `4` | Tonight's run as one more dot next to the pilot and batch 1 dots for F1; runs failing out of k per arm. Screen 4 groups the dots by feature from the console fix made on 2026-10-17; before it, the screen pooled all features and pre-fix records (section 5) |
| 7 | — | `make swap-1`: "judged measures identical" (no model cost). If the session meter has room, `make demo-1 LAYERS=-instructions` instead or after; it runs into S2, and `make demo-2` waits for its `Cost:` line |

Discussion (section minutes 45-50): what did each arm read before it wrote the query, and did the
ticket itself point at the rules? Section 6 has the pilot answer.

---

## 4. Poll question

> Both arms can open `docs/HANDBOOK.md`, which says "Do not copy" about `GET /v1/issues`. Out of 10
> bare-arm runs of F1, how many ship `GET /issues` with at least one new R1 violation?
> A) 0-2  B) 3-5  C) 6-8  D) 9-10

What the pilot gives so far, measured in the course pilot, run 2, 2026-10-16: on `F1-canonical`, 0 of
3 bare runs and 0 of 3 harness runs failed. Three runs are too few to answer a question about 10; the
answer comes from batch 1:

[[PENDING: bare and harness runs failing out of 10 for F1 canonical (r1_new_violations>=1), to state the poll answer | source: M8 batch 1 | how: uv run shipharness report]]

---

## 5. What to watch

Screen 1, Live Console:
- Harness arm, first decision: `placed 31 instruction files (AGENTS.md map, docs, skills)` (the 31
  files under `teamtrack/harness/instructions/`; message format from
  `src/shipharness/harness/instructions/layer.py`).
- Harness arm, notes in the turn list: `agent read skill add-endpoint (tier 2): .agents/skills/add-endpoint/SKILL.md`
  and `agent read docs/SECURITY.md`. A tier 3 note means it also opened `references/tests.md`; no
  pilot run 2 arm did.
- Both arms: `read_file` and `search` calls on `app/api/legacy_v1.py`, `app/services/legacy.py`, or
  `list_all_legacy`. Then the `apply_patch` to `app/repositories/issues.py`: does the new query filter
  on `org_id`, and does it page by id with `page` and `split_page`, or by `offset`? In pilot run 2 no
  arm opened the legacy files.
- Both arms: does the arm open `docs/HANDBOOK.md`? The canonical ticket tells it to.
- The `Referee` line: pending, then pass or fail on the primary measure.
- Gate pills: none in demo-1. The bare arm shows "No gate (verify layer off)" and the harness arm "No
  gate." because the verification layer is not in the demo-1 stack. There are no BLOCKED lines
  either: the instructions layer never blocks a tool call.

Screen 2, Boards:
- A card is marked ⚠ other org when its `data-org` is not the viewer's org
  (`src/shipharness/console/board_capture.py`). F1 adds an API endpoint that the board does not call,
  so a leak in `GET /issues` shows on the board only if the arm's change also reaches code the board
  uses (for example `list_for_project`). In the live console check screen 2 did not change during the
  run: F1 changes no board pixels, so each arm kept its first frame. A clean board does not mean a
  clean endpoint; the R1 check is the evidence.

Screen 3, Evidence:
- Files read, grouped as map, skill, harness doc, state, handbook, code, test. Does the bare arm's list
  contain `handbook`? Does the harness arm's contain `skill` or `harness doc`? Only `read_file` calls
  count; a `cat` through `run` does not appear.
- Referee: `R1: n new` per arm, and the R3 line for the list envelope and error shape. The existing
  `GET /v1/issues` leak appears as a baseline finding in both arms and counts against neither.

Screen 4, A/B Report: tonight's dot sits next to the pilot and batch 1 dots. Read counts, never
percentages (a course rule). In the live console check screen 4 still pooled every score record into
one row per arm (all features, and pilot run 1's records from before the measurement fixes); the
console fix of 2026-10-17 groups the report by feature, so the F1 row shows F1 runs only.

---

## 6. What the harness arm did differently, and why

The harness piece is the answer to "the rule is on disk, but is it in context when the query is
written?" (A1, F-a-05). The map is in the harness arm's developer message from turn 1, it names
`docs/SECURITY.md` for R1 and the skill for endpoint work, and the skill's step 0 names the right
example and the wrong one. The bare arm gets the rules only if it decides to open the handbook.

Pilot run 2 shows both halves of that. The first eight tool calls of each arm in
`ab-20261016-185628-37483b` (fields `name` and `target` of the `tool_call` events):

```text
captured on 2026-10-16, run ab-20261016-185628-37483b; your output will differ
bare     r-20261016-185628-8aa524: list_dir . | read_file docs/features/f1.md | read_file docs/HANDBOOK.md |
         list_dir app | read_file app/api/issues.py | read_file app/repositories/issues.py |
         read_file app/services/issues.py | read_file app/db/models.py
harness  r-20261016-185628-758650: list_dir . | read_file docs/features/f1.md | read_file docs/HANDBOOK.md |
         read_file .agents/skills/add-endpoint/SKILL.md | read_file ARCHITECTURE.md |
         read_file docs/SECURITY.md | read_file docs/design-docs/api-conventions.md | list_dir app
```

Across the three F1 A/Bs of pilot run 2:

| What the run logs show | Bare arm | Harness arm |
|---|---|---|
| Opened `docs/HANDBOOK.md` (third call; the canonical ticket names it) | 3 of 3 | 3 of 3 |
| Opened the skill body (tier 2), on the fourth call | — | 3 of 3 |
| Opened the skill's `references/tests.md` (tier 3) | — | 0 of 3 |
| Opened `ARCHITECTURE.md` / `docs/SECURITY.md` / `docs/design-docs/api-conventions.md` | — | 3 / 2 / 3 of 3 |
| Opened `app/api/legacy_v1.py` or `app/services/legacy.py` | 0 of 3 | 0 of 3 |
| New query filters on `Issue.org_id` and `Project.org_id`, pages with `page` and `split_page` | 3 of 3 | 3 of 3 |

So the harness arm did read differently: it loaded the skill and the focused docs on top of the
handbook. It did not ship differently, because the bare arm had the same rules in context too. The
query both arms wrote in A/B 1 of the F1 A/Bs of pilot run 2 (`app/repositories/issues.py` in each
arm's `diff.patch`, cut to the scoping lines):

```text
captured on 2026-10-16, run ab-20261016-181736-a07558; your output will differ
bare (search):
+        .join(Project, Issue.project_id == Project.id)
+        .where(
+            Issue.org_id == org_id,
+            Project.org_id == org_id,
+            Issue.deleted_at.is_(None),
+            Project.archived_at.is_(None),
+        )
+    stmt = page(stmt, Issue.id, after, limit)
harness (list_for_org):
+        .join(Project, Project.id == Issue.project_id)
+        .where(
+            Issue.org_id == org_id,
+            Project.org_id == org_id,
+            Project.archived_at.is_(None),
+            Issue.deleted_at.is_(None),
+        )
+    stmt = page(base, Issue.id, after, limit)
```

The lesson for the class: the A/B can only show the harness piece working on a task where the bare
arm is not handed the pointer. The trap variant removes the handbook line from the ticket and names
the legacy code instead. Pilot runs 3 and 4 tested it, and both arms passed 3 of 3 in each run: no
measurable difference on this task with this model (section 7).

---

## 7. Pilot dots and experiment results

Measured in the course pilot, run 2, 2026-10-16: F1 canonical, k=3, gpt-6-luna, effort medium, reviewer
on, two A/Bs in parallel. Then the live console check, 2026-10-16, one A/B on its own with board
previews on (`make demo-1 PURPOSE=pilot`). One row per run, copied from the score records
(`exports/scores/<run id>.json`):

| A/B | Arm | Run id | Primary | R1 new | R1 leaks | R3 new | Hidden | Existing tests | Mutants | Reviewer |
|---|---|---|---|---|---|---|---|---|---|---|
| `ab-20261016-181736-a07558` | bare | `r-20261016-181736-490aa2` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | accept |
| | harness | `r-20261016-181736-c00503` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | accept |
| `ab-20261016-183644-0036f0` | bare | `r-20261016-183644-7e7ec9` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | reject |
| | harness | `r-20261016-183644-ba3b9a` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | reject |
| `ab-20261016-185628-37483b` | bare | `r-20261016-185628-8aa524` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | accept |
| | harness | `r-20261016-185628-758650` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | accept |
| `ab-20261016-210339-909651` (console check) | bare | `r-20261016-210339-bfe8e0` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 2/4 | accept |
| | harness | `r-20261016-210339-817dbf` | pass | 0 | 0 | 0 | 52/52 | 144/144 | 3/4 | reject |

Runs failing the primary measure: pilot run 2 bare 0 of 3, harness 0 of 3; console check bare 0 of 1,
harness 0 of 1. "Existing tests" is the `regression` check: existing tests keep passing. The reviewer
rejections are about archived projects passed as `project_id`, not about tenancy (each of those
reviews says `tenant_isolation_risk: none`); the referee's hidden tests passed 52 of 52 in both arms.
The reviewer is a secondary measure.

Pilot runs 3 and 4 and the batches:

Measured in the course pilot, run 3, 2026-10-16, A/Bs `ab-20261016-211419-07937b`,
`ab-20261016-212745-2c14fb`, and `ab-20261016-214636-c8b3c4`: ticket `F1-trap`, k=3, gpt-6-luna,
effort medium, reviewer on, two A/Bs in parallel. Then run 4, effort low, 2026-10-16, A/Bs
`ab-20261016-232842-b372c2`, `ab-20261016-233807-3f34fa`, and `ab-20261016-234639-4a18bd`: the same
ticket and settings with effort low for both arms. One row per run, from the score records:

| Run | A/B | Arm | Run id | Primary | R1 new | R1 leaks | Hidden | Mutants | Shipped tests | Turns | Agent time (s) | Cost | Reviewer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | `ab-20261016-211419-07937b` | bare | `r-20261016-211419-8fb5f4` | pass | 0 | 0 | 52/52 | 3/4 | 7 | 34 | 142 | $0.0086 | accept |
| | | harness | `r-20261016-211419-741ab3` | pass | 0 | 0 | 52/52 | 2/4 | 7 | 42 | 170 | $0.0124 | accept |
| 3 | `ab-20261016-212745-2c14fb` | bare | `r-20261016-212745-a9900c` | pass | 0 | 0 | 52/52 | 3/4 | 7 | 42 | 194 | $0.0110 | accept |
| | | harness | `r-20261016-212745-8a0bbf` | pass | 0 | 0 | 52/52 | 3/4 | 10 | 42 | 248 | $0.0121 | accept |
| 3 | `ab-20261016-214636-c8b3c4` | bare | `r-20261016-214636-8e13f4` | pass | 0 | 0 | 52/52 | 2/4 | 5 | 41 | 223 | $0.0102 | accept |
| | | harness | `r-20261016-214636-53d21a` | pass | 0 | 0 | 52/52 | 3/4 | 12 | 42 | 197 | $0.0115 | accept |
| 4, effort low | `ab-20261016-232842-b372c2` | bare | `r-20261016-232842-1b27e7` | pass | 0 | 0 | 52/52 | 2/4 | 8 | 26 | 112 | $0.0051 | accept |
| | | harness | `r-20261016-232842-f3515e` | pass | 0 | 0 | 52/52 | 2/4 | 7 | 39 | 165 | $0.0087 | accept |
| 4, effort low | `ab-20261016-233807-3f34fa` | bare | `r-20261016-233807-7f74f1` | pass | 0 | 0 | 52/52 | 3/4 | 9 | 32 | 123 | $0.0068 | accept |
| | | harness | `r-20261016-233807-36c040` | pass | 0 | 0 | 52/52 | 3/4 | 20 | 37 | 176 | $0.0086 | accept |
| 4, effort low | `ab-20261016-234639-4a18bd` | bare | `r-20261016-234639-cd17ac` | pass | 0 | 0 | 52/52 | 2/4 | 6 | 30 | 108 | $0.0058 | accept |
| | | harness | `r-20261016-234639-209fdf` | pass | 0 | 0 | 52/52 | 3/4 | 18 | 37 | 153 | $0.0084 | reject |

Runs failing the primary measure (`r1_new_violations >= 1`): run 3 bare 0 of 3, harness 0 of 3; run 4,
effort low, bare 0 of 3, harness 0 of 3. No arm added an R1 violation; the legacy `/v1` handler was not
copied into a leak. No measurable difference on this task with this model (course pilot, runs 3 and 4).
A/B wall time, in table order: run 3 415.7 s, 519.3 s, 486.3 s; run 4 395.7 s, 420.2 s, 386.0 s.

[[PENDING: F1 canonical dots, runs failing out of 10 per arm, with run ids | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: F1 canonical secondary counts per arm (r1_leaks, r3_new_failures, hidden passed of 52, existing tests keep passing) | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation, leave-out-instructions configuration (all minus instructions) on the 12 ablation tasks | source: M8 ablation | how: uv run shipharness report]]

Batch 1 runs F1-F4 canonical, two arms, k=10 each, reviewer on.

---

## 8. Captured output and screenshots

Pilot run 2 ran with board previews off, so it has run logs and score records
but no `make demo-1` terminal output and no board screenshots. What it has:

The harness arm's decisions (fields `ts` and `data.message` of the `harness_decision` events):

```text
captured on 2026-10-16, run ab-20261016-185628-37483b; your output will differ
2026-10-16T18:56:30.554Z  placed 31 instruction files (AGENTS.md map, docs, skills)
2026-10-16T18:56:37.308Z  agent read skill add-endpoint (tier 2): .agents/skills/add-endpoint/SKILL.md
2026-10-16T18:56:38.650Z  agent read ARCHITECTURE.md
2026-10-16T18:56:39.935Z  agent read docs/SECURITY.md
2026-10-16T18:56:41.435Z  agent read docs/design-docs/api-conventions.md
```

The referee's verdicts (field `data.summary` of the `verdict` events):

```text
captured on 2026-10-16, run ab-20261016-185628-37483b; your output will differ
harness  agent said none; referee: passes the primary measure; hidden tests 52/52, mutants killed 3/4, R1 new 0
bare     agent said none; referee: passes the primary measure; hidden tests 52/52, mutants killed 3/4, R1 new 0
```

"Agent said none" means the arm did not call `finish` before its build session's turn budget ran
out; the referee judges what it shipped either way. In the live console check the bare arm did call
`finish`:

```text
captured on 2026-10-16, run ab-20261016-210339-909651; your output will differ
harness  agent said none; referee: passes the primary measure; hidden tests 52/52, mutants killed 3/4, R1 new 0
bare     agent said done; referee: passes the primary measure; hidden tests 52/52, mutants killed 2/4, R1 new 0
```

The R1 check on the harness arm (one `check_result` event, cut): the existing `/v1/issues` leak is
found, marked `baseline`, and does not count:

```text
captured on 2026-10-16, run ab-20261016-185628-37483b; your output will differ
{"check": "r1_tenant", "passed": true, "new_violations": 0, "baseline_violations": 1, "total_probes": 53, ...
 "findings": [{"rule": "R1", "severity": "leak", "endpoint": "GET /v1/issues",
 "detail": "no_path: GET /v1/issues -> 200 [{\"id\":1,\"org_id\":1, ...", "baseline": true}]}
```

What the live console check showed on the screens (A/B `ab-20261016-210339-909651`): screens 1, 3, and
5 updated during the run; screen 2 kept one board frame per arm, because F1 changes no board pixels;
after the run, screen 1 showed the full timeline and all decisions in scrollable lists, and screen 5
listed the LangSmith links; no RECORDING badge, since it was a live run.

Still to capture:

[[PENDING: terminal output of make demo-1 (A/B line, one line per arm, Cost line), labelled with date and ab id | source: live class | how: make demo-1]]

[[PENDING: screenshot of screen 1 Live Console mid-run, harness arm showing a skill note | source: live class | how: make demo-1, then key 1]]

[[PENDING: screenshot of screen 2 Boards for both arms as admin@acme.test | source: live class | how: make demo-1, then key 2]]

[[PENDING: screenshot of screen 3 Evidence with both files-read maps and the R1 referee line | source: live class | how: make demo-1, then key 3]]

[[PENDING: screenshot of screen 4 A/B Report with the F1 dots grouped by feature | source: M8 batch 1 | how: uv run shipharness report, then make console and key 4]]

[[PENDING: screenshot of screen 5 Traces live tail | source: live class | how: make demo-1, then key 5]]

[[PENDING: terminal output of make swap-1 ("Swap test on <ab id>: judged measures identical") | source: live class | how: make swap-1]]

[[PENDING: terminal output of the layer switch showing layers=[] and both arms' lines | source: live class | how: make demo-1 LAYERS=-instructions]]

---

## 9. Measured time and cost

The limits are fixed in configuration (`.env.example`, `src/shipharness/config/settings.py`):
`MAX_RUN_COST_USD` $0.20 per arm per run (build and test phases together), `MAX_REVIEW_COST_USD` $0.04
per review, `MAX_SESSION_COST_USD` $2.50 for the whole class session, `RUN_TIMEOUT_S` 300 s of agent
time per arm, `HARNESS_TIMEOUT_S` 120 s of harness work per arm, `TOOL_TIMEOUT_S` 120 s per tool
command. The layer switch is a second full A/B under the same caps; run it only if the `Cost:` line
shows room under the session cap.

Pilot run 2 and the live console check, F1 canonical (score records; agent time is `wall_s`; A/B times
are the first event and the last verdict in `events.jsonl`):

| A/B (first event to last verdict, UTC) | Arm | Cost | Review cost | Agent time | Turns |
|---|---|---|---|---|---|
| `ab-20261016-181736-a07558` (18:17:37 to 18:26:21) | bare | $0.012671 | $0.002649 | 184.0 s | 42 |
| | harness | $0.013504 | $0.003464 | 177.6 s | 42 |
| `ab-20261016-183644-0036f0` (18:36:45 to 18:44:50) | bare | $0.011580 | $0.003134 | 170.6 s | 41 |
| | harness | $0.012539 | $0.002649 | 165.6 s | 42 |
| `ab-20261016-185628-37483b` (18:56:28 to 19:05:46) | bare | $0.011696 | $0.002428 | 192.8 s | 42 |
| | harness | $0.012703 | $0.003028 | 126.9 s | 42 |
| `ab-20261016-210339-909651`, console check (21:03:48 to 21:12:46) | bare | $0.010304 | $0.002630 | 198.7 s | 40 |
| | harness | $0.012331 | $0.002557 | 133.1 s | 42 |

Every arm stayed far under the $0.20 run cap. Most of each pilot run 2 A/B's wall time was the
referee, not the agents: the median referee span was 331 s from an arm's end to its verdict, including
the wait for the other arm. Two referee changes were made after run 2 to cut it (judge each arm when it
ends; one pytest process for the unmutated pass step). The live console check ran after those changes,
one A/B on its own on the class host: 9 min 10 s wall time for the whole command, $0.027821 in total
(both arms and both reviews, from the course's cost ledger).

[[PENDING: worst-case cost and wall time per arm across F1 canonical runs | source: M8 batch 1 | how: uv run shipharness report]]

---

## 10. Troubleshooting and the replay fallback

| Symptom | Cause (from the code) | Fix |
|---|---|---|
| `make doctor` marks `OPENAI_API_KEY` (or `LANGSMITH_API_KEY`) `x missing`, detail `not set`, next step "add it to .env at the repo root" | Key not set (`src/shipharness/doctor.py`) | Add the key to `.env`, run `make doctor` until it ends `result: + ready` |
| `make doctor` marks a key `x invalid`, detail `... key invalid (rejected by ...)` | The service answered 401 or 403 | Create a new key in that account, update `.env` |
| `make doctor` marks a key `! unreachable`, detail `could not reach ...` | Network or proxy | Check the connection; nothing else will work until this passes |
| `make demo-1` exits 2 before any arm starts | `shipharness ab` refuses a missing or rejected `OPENAI_API_KEY` or a stand-in model client; there is no fallback (tests in `tests/unit/ab/test_commands.py`) | Fix the key with `make doctor`; if the API is down, use the replay |
| `make doctor` marks `container runtime` `! warn`, detail `docker not found: only the UNSANDBOXED fallback can run` | No `docker` on PATH | Install Docker Engine in WSL2 ([docs/setup-windows.md](../../../docs/setup-windows.md)). Do not run the class demo unsandboxed: every screen would show "UNSANDBOXED — results not official" |
| `make doctor` passes, but an arm ends `ERROR` with `docker run failed: ...` and the command exits 1 | Doctor only checks that the `docker` CLI is on PATH. The arm container did not start: daemon stopped, or image `shipharness-agent:1` / `shipharness-referee:1` missing (`src/shipharness/sandbox/docker.py`) | `docker info`; on the class host `sudo systemctl start docker` inside Ubuntu; `make images` rebuilds both images. Then rerun, or replay |
| An arm ends `ABORTED: cap`; the command exits 2 | The cost tracker refused the next call (`cost cap reached: run $... of $0.20`, `src/shipharness/cost/tracker.py`). The referee still judges the arm | Keep the run: aborted runs are kept, scored, and shown (a course rule). If the `Cost:` line shows the session cap reached, skip the layer switch and use the replay for anything else |
| An arm ends `ABORTED: timeout` | `RUN_TIMEOUT_S` (300 s of agent time) reached (`src/shipharness/runner/loop.py`) | Same as a cap abort: it is a dot |
| `make swap-1`: `x ...; run make demo-1 first, or pass AB=<id>` | No demo-1 A/B recorded yet | Run `make demo-1`, or `make swap-1 AB=<id>` |
| `make replay`: `! replay needs RUN=<ab or run id>` | `RUN` not given | `make replay RUN=<id>` |
| Screen 2 shows no board for an arm | The board preview is display only; a preview that fails to start is skipped and the run continues (`src/shipharness/ab/demo.py`) | Continue with screens 1 and 3 |

### Replay fallback

Use it only when the live run fails on stage (API outage, rate limit, Docker failure), never to
replace a run that worked but gave an unwelcome result (a course rule: every run is a dot).

```bash
make replay RUN=<ab or run id>
```

The replay re-emits the recorded event log with a red RECORDING badge on every screen, applies the
recorded diff to a fresh export of the pinned checkpoint commit, and runs the referee live
(`src/shipharness/ab/recorded.py`). With the default settings it makes no model calls. The id of a
live run is in the `A/B <ab id> (F1, layers=[...])` line and in `.shipharness/runs/<ab id>/`. The
three pilot run 2 A/Bs and the console check A/B above are recorded F1 runs of the canonical task.

[[PENDING: ab id of the recorded demo-1 fallback run kept for class (task as decided after pilot run 3) | source: M6 pilot | how: course pilot (build repository)]]
