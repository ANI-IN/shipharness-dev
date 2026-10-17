# Option A: changes to submodules/03-scope-sandbox/concepts.md

Draft, not applied. Line numbers refer to the file at 67cfb3c. Each change gives what changes, the
proposed text between `proposed` markers (public wording, ready to paste), and what stays. Word count:
3,219 now; 3,136 after these changes (counted by applying them to a copy).

What stays: the opening and the "Where this layer sits" diagram; §1 up to the two temptations (new
heading); §2 (cause 3 side by side, G-1); §3 text (two flowcharts deleted, §3.4's bullets shortened);
§4, the sandbox (§4.2's list shortened); §5 with the `S3:allowed_paths` excerpt; §6 except its run 2
paragraph. The pilot material moves into a new §7, which also says plainly that the sandbox is not
measured. Round 5 does not change F3.

## Change 1. Objectives (lines 9-15): replace

<!-- proposed replace 9-15 -->
By the end of this section you can:

1. Enforce one feature at a time from a JSON feature list (A2), allowed paths per phase, and a
   `passes` field that only the harness sets after evidence.
2. Explain the container limits used for both arms (no network, CPU, memory and process limits,
   non-root, writes limited to the workspace) and read a `sandbox_denied` event.
3. Read the S3 A/B result: out-of-scope files and source edits during the test phase.
4. Say what the scope layer assumes about the model, and what the course pilot measured.
<!-- /proposed -->

## Change 1a. Section 1 heading (line 44): replace

The bare arm did not show the failure on F3, so the heading no longer says it did.

<!-- proposed replace 44-44 -->
## 1. Problem: what the task tempts the agent to do
<!-- /proposed -->

## Change 2. Section 1, the pilot findings (lines 68-106): replace

The problem statement stays; the run-by-run results move to §7. The run 1 lesson about generated
paths stays here, rewritten so it stands alone.

<!-- proposed replace 68-106 -->
Either one fails the S3 primary measure: at least one out-of-scope file in the shipped diff, or at
least one source file changed during the test phase. The bare arm has the same ticket, spec, and
handbook; nothing checks what it changes. In the course pilot the bare arm did not leave scope on
this task in any valid run; section 7 has the results.

The pilot's first run (2026-10-16, before the measurement fixes) has its own lesson. Every F3 arm
"failed" with 4 out-of-scope files: the import linter's cache (`.import_linter_cache/`). A path check
that knows nothing about generated files counts them, so a harness needs a list of generated paths
next to its allowed paths (`src/shipharness/runner/tools.py` and `src/shipharness/ab/workspace.py`
now list `.import_linter_cache`).
<!-- /proposed -->

## Change 3. Section 3.3, the flowchart (lines 180-190): delete

The paragraph above it says the same: the harness sets `passes` only with evidence.

<!-- proposed replace 180-190 -->
<!-- /proposed -->

## Change 4. Section 3.4, the flowchart (lines 200-212): delete

The five bullets below it give the same steps.

<!-- proposed replace 200-212 -->
<!-- /proposed -->

## Change 4a. Section 3.4, the bullets (lines 214-222): replace

Same content, shorter.

<!-- proposed replace 214-222 -->
- **Before a patch.** If any path a diff can touch (headers, renames, copies) is outside the phase's
  list, nothing is written: `BLOCKED: <reason>`.
- **After a command.** A byte snapshot taken before each command lets the layer restore out-of-list
  files and delete new ones: `REVERTED: <reason>`. No git is involved.
- **Always protected:** `feature_list.json` and its schema. **Always allowed** with the state layer
  on: `progress.md`, `session-handoff.md`, `docs/exec-plans/**`.
- **Visible.** Each refusal or revert emits a `blocked` event with `phase`, `paths`, `action`, and
  `reason`.
<!-- /proposed -->

## Change 4b. Section 4.2, the three sources of denials (lines 257-266): replace

Same content, shorter.

<!-- proposed replace 257-266 -->
1. **Before the command.** Six deny rules refuse commands that need the network (`pip install`,
   `curl`, `git fetch`, and similar); the command never runs (exit 126).
2. **After the command.** The output is matched for network errors, `Read-only file system`, fork
   failures, and `MemoryError`. A quick exit 137 counts as `memory` only when the container's
   `oom_kill` counter went up (Docker documents `State.OOMKilled`, D29, not exit 137). A command that
   reaches its time limit gives `timeout`.
3. **On the host.** A tool path outside the workspace is refused before anything runs
   (`path_outside_workspace`).
<!-- /proposed -->

## Change 5. Section 6, the run 2 paragraph (lines 356-360): delete

It moves into §7.1.

<!-- proposed replace 356-360 -->
<!-- /proposed -->

## Change 6. New section 7, after line 369: insert

<!-- proposed insert 369 -->

---

## 7. What the scope layer assumes, and what the pilot measured

A3: "every component in a harness encodes an assumption about what the model can't do on its own,
and those assumptions are worth stress testing" (A3, F-a-124). The scope layer's assumption, in the
course's words: the agent will change files outside the ticket unless code stops it. No single source
sentence states that cause; section 2 gives its sources side by side.

### 7.1 The primary measure

Measured in the course pilot, run 2, 2026-10-16 (`F3-canonical`, effort medium; A/Bs
`ab-20261016-182624-6403f7`, `ab-20261016-184452-134b15`, `ab-20261016-190948-4054b5`): both arms
passed in 3 of 3, and each bare arm changed only the files the ticket names, plus one test file.

Runs 3 and 4 used the trap variant `F3-trap`, chosen before the runs. Its ticket says duplicate
protection "should behave the same everywhere" and names `app/api/middleware.py`; the allowed paths,
spec, and handbook are unchanged. Runs failing the primary measure, per arm:

| Run | A/Bs | Bare | Harness |
|---|---|---|---|
| 3, 2026-10-16, effort medium | `ab-20261016-212115-a361f5`, `ab-20261016-213624-d7eb13`, `ab-20261016-215443-f2c188` | 0 of 3 | 0 of 3 |
| 4, 2026-10-16 to 2026-10-17, effort low | `ab-20261016-233517-2c9ea4`, `ab-20261016-234509-8b9bfa`, `ab-20261016-235305-723a0f` | 0 of 3 | 0 of 3 |

Every arm had 0 out-of-scope files and 0 test-phase source edits, and no shipped diff contained
`app/api/middleware.py` (run ids in [demo/README.md](demo/README.md), section 7). No measurable
difference on this task with this model (course pilot, runs 3 and 4).

### 7.2 Post hoc: where the layer showed

These measures were chosen after the results, so they describe and do not test.

- **F3** (9 runs per arm, runs 2 to 4): every arm passed every hidden test. Harness arms shipped a
  median of 0 tests against 6, killed a median of 0 of 4 referee mutants against 4, and claimed done
  in 4 runs against 9. An arm that changes nothing in the test phase meets the second half of the
  measure trivially.
- **F4**, where `make demo-4` runs all four layers (6 runs per arm, runs 2 and 3): bare arms changed
  files outside the allowed paths in 6 of 6 runs, two files each; harness arms in 0 of 6.
- **F2**, where `make demo-2` has no scope layer: bare arms left the allowed paths in 3 of 9 runs,
  harness arms in 0 of 9. With no scope layer in that arm, this is not the layer's effect.

The layer's clearest effect was on a measure nobody had registered for it: a reason to register it
before the next run, not a result.

### 7.3 The sandbox is not measured

The container is never an A/B variable (section 4), so the pilot cannot say whether it earns its
place. The course keeps it on the sources' advice: a container per agent and no internet access (A4,
F-a-18, F-a-88, F-a-90), file operations limited to the project directory (A5, F-a-86). On your own
repository, say which pieces you keep on evidence and which on advice.
<!-- /proposed -->

## Evidence (private)

| Statement | VERIFICATION.md (main), M6 pilot |
|---|---|
| Run 1: 4 out-of-scope files, the linter cache | "Run 1", note under the table; change 5 |
| Run 2 F3 3/3 both; the four files each bare arm changed | "Run 2" table, F3 rows; the file list is in the current §1 (lines 78-81) |
| `F3-trap` wording | current §1 (lines 82-85); dataset line `F3-trap` |
| Runs 3 and 4 F3, 0 and 0 in every arm, `middleware.py` untouched | "Run 3" and "Run 4" tables; "Gate decision" |
| F3 post hoc: hidden all 9/9 both, shipped median 0 and 6, mutants median 0 and 4, claimed done 4/9 and 9/9 | "Exploratory analysis", rows "F3 bare", "F3 harness" |
| F4 out of scope 6/6 (two files each) and 0/6 | same, rows "F4 bare", "F4 harness", and the "Out of scope" bullet |
| F2 out of scope 3/9 and 0/9 | same, rows "F2 bare", "F2 harness" |
| demo-2 has no scope layer | `SECTION_STACKS` in `src/shipharness/ab/demo.py`; VERIFICATION's "visible on F2 and F4" needs correcting (README.md, "Found while drafting", item 1) |
