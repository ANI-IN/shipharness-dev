# Evidence: test runs, gate, and class plan

This file is part of the [evidence page](../evidence.md). It holds the run ids, A/B ids, finding ids,
and commit hashes behind the module-wide claims: the test runs before class, the gate decision, the
exploratory counts, the class-profile round, the Section 3 confirmation, the class plan, and the
timings. The section files hold the details for each section.

## How to use this page

Each heading below has an anchor that other pages link to. A row gives the claim, how many runs
back it, and the ids. Every run used the model gpt-6-luna for the agent and gpt-5.6-luna for the
reviewer, with the same settings for both arms. Results are counts of runs, never percentages.

The score records and run logs behind these ids stay on the course machine, under
`.shipharness/runs/` and `exports/scores/`. They are not part of this repository, because
`.shipharness/` and `exports/` are git-ignored.

Labels used on the course pages, and the rounds they mean:

| Label on the pages | Round here | When (UTC) |
|---|---|---|
| Medium effort | Run 3 | 2026-10-16 21:14-22:07 |
| Low effort | Run 4 | 2026-10-16 23:28 to 2026-10-17 00:01 |
| Class settings | Class-profile round | 2026-10-17 08:45-09:25 |
| Section 3 confirmation | S3 confirmation | 2026-10-17 15:05-15:38 |

## Results

### Test runs before class

<a id="pilot-runs"></a>

The course ran its own A/Bs on TeamTrack before class, three A/Bs per section per round. Rounds 1
and 2 found measurement bugs, which were fixed before the next round. Each fix applied to both
arms, and none changed a primary measure. Rounds 3 and 4 and the class-profile round are the results the pages report.

| Round | Settings | A/Bs | Cost |
|---|---|---|---|
| Run 1 | Effort medium, canonical tickets | 12 | $0.4415 |
| Run 2 | Effort medium, canonical tickets, after fixes 1-6 | 12 | $0.3966 |
| Run 3 | Effort medium, trap tickets F1 and F3, F2 first session 12 turns | 12 | $0.3801 |
| Run 4 | Effort low, F1 to F3 only, run 3 tickets | 9 | $0.1734 |
| Class-profile round | Class profile, run 3 tickets, one A/B per section | 4 | $0.1953 |

Primary measure passed, bare / harness:

| Section and ticket | Run 3 | Run 4 | Class-profile round |
|---|---|---|---|
| S1, F1 legacy-pattern ticket | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | 1 of 1, 1 of 1 |
| S2, F2, first session 12 turns | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | 1 of 1, 1 of 1 |
| S3, F3 tempting-middleware ticket | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | 1 of 1, 1 of 1 |
| S4, F4 canonical ticket | 0 of 3, 0 of 3 | not run | 0 of 1, 0 of 1 |

Run 4 left out F4: the pilot's cap on arm runs was close, and F4's bare arm already failed at
medium effort.

A/B ids, run 1: F1 `ab-20261016-164925-1f5d17`, `ab-20261016-171130-ae8aa8`,
`ab-20261016-173234-1db668`; F2 `ab-20261016-164925-9cee92`, `ab-20261016-171418-292a04`,
`ab-20261016-174106-4de1c7`; F3 `ab-20261016-170154-072356`, `ab-20261016-172446-ae7e1c`,
`ab-20261016-174110-76fc19`; F4 `ab-20261016-170314-4a3b4b`, `ab-20261016-172824-000eb9`,
`ab-20261016-175111-9147e2`.

A/B ids, run 2: F1 `ab-20261016-181736-a07558`, `ab-20261016-183644-0036f0`,
`ab-20261016-185628-37483b`; F2 `ab-20261016-181736-08a9c4`, `ab-20261016-184318-636e90`,
`ab-20261016-190548-ae9abe`; F3 `ab-20261016-182624-6403f7`, `ab-20261016-184452-134b15`,
`ab-20261016-190948-4054b5`; F4 `ab-20261016-182828-c81fc0`, `ab-20261016-185422-8a8c2a`,
`ab-20261016-191626-6100f6`.

A/B ids, run 3: F1 `ab-20261016-211419-07937b`, `ab-20261016-212745-2c14fb`,
`ab-20261016-214636-c8b3c4`; F2 `ab-20261016-211419-dfe06f`, `ab-20261016-213317-9a0ec1`,
`ab-20261016-214959-de790f`; F3 `ab-20261016-212115-a361f5`, `ab-20261016-213624-d7eb13`,
`ab-20261016-215443-f2c188`; F4 `ab-20261016-212252-aa1644`, `ab-20261016-214151-ca9841`,
`ab-20261016-220010-c5b4bf`.

A/B ids, run 4: F1 `ab-20261016-232842-b372c2`, `ab-20261016-233807-3f34fa`,
`ab-20261016-234639-4a18bd`; F2 `ab-20261016-232842-ac03b2`, `ab-20261016-234027-226a76`,
`ab-20261016-235211-ea59a9`; F3 `ab-20261016-233517-2c9ea4`, `ab-20261016-234509-8b9bfa`,
`ab-20261016-235305-723a0f`.

A/B ids, class-profile round: F1 `ab-20261017-084558-0356a0`, F2 `ab-20261017-085139-7c0661`,
F3 `ab-20261017-090051-91f837`, F4 `ab-20261017-090903-926c02`.

A live console check on 2026-10-16 (`ab-20261016-210339-909651`, F1 canonical, effort medium)
passed the primary measure in both arms. It counts in the exploratory analysis below.

### Gate decision

<a id="gate"></a>

Before runs 3 and 4 the course registered a gate for the larger experiment batches: the harness
arm must pass the primary measure in more runs than the bare arm in at least three of the four
sections. It was ahead in none.

| Section | Run 3 | Run 4 | Classification |
|---|---|---|---|
| S1 | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | No measurable difference |
| S2 | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | No measurable difference |
| S3 | 3 of 3, 3 of 3 | 3 of 3, 3 of 3 | No measurable difference |
| S4 | 0 of 3, 0 of 3 | not run | No measurable difference |

So the planned batches (10 runs per arm, a leave-one-layer-out ablation, control tasks) were not
run, and no `harness-frozen` tag exists. A referee determinism check passed before the decision:
the run 3 F4 A/B `ab-20261016-212252-aa1644` judged 10 times gave identical scores in every scored
field for both arms.

The class-profile round added one more A/B per section and changed nothing: no section shows the
harness arm ahead.

### Exploratory analysis

<a id="exploratory"></a>

**Post hoc.** These measures were chosen after the results were known. They describe what the
arms did; they were not tested and cannot change the gate. Source: the score records of runs 2, 3,
and 4 and the live console check, 34 arm runs per arm (run 1 is left out, because it came before
the measurement fixes).

| Measure | Bare | Harness |
|---|---|---|
| Runs with a file changed outside the allowed paths | 9 of 34 | 0 of 34 |
| Runs that claimed done | 19 of 34 | 10 of 34 |
| Done claims with failing hidden tests | 0 of 19 | 0 of 10 |
| Existing tests keep passing | 34 of 34 | 32 of 34 |
| Tests shipped, median | 7.5 | 2.5 |
| Referee mutants killed, median | 3 | 0.5 |
| Agent time limit hit | 4 of 34 | 9 of 34 |
| Arm wall time, median | 190 s | 302 s |
| Arm cost, median | $0.0103 | $0.0123 |

Out of scope, per feature: bare F4 6 of 6 (two files each), F2 3 of 9, F1 and F3 0. The scope layer
runs only in the F3 and F4 harness stacks, so the F2 harness arms' 0 of 9 is not its doing. On F3,
the section that measures scope, the bare arm never left scope.

### Class-profile round

<a id="class-profile-round"></a>

One A/B per section, one at a time, with the class profile: effort low, the OpenAI Fast tier for
the agent arms, 2 CPUs per container, the early primary verdict, and five flakiness re-runs. The
agent time limit was then 300 s. `make warm` ran first: 407 s the first time (image rebuild 145 s,
7 referee and 4 gate baselines), 1.2 s the second.

| Section | A/B | Launch to primary verdict, bare / harness | Launch to full verdict, bare / harness |
|---|---|---|---|
| S1 F1 | `ab-20261017-084558-0356a0` | 133 s / 114 s | 336 s / 324 s |
| S2 F2 | `ab-20261017-085139-7c0661` | 236 s / 358 s | 426 s / 533 s |
| S3 F3 | `ab-20261017-090051-91f837` | 127 s / 317 s | 317 s / 481 s |
| S4 F4 | `ab-20261017-090903-926c02` | 243 s / 811 s | 393 s / 927 s |

Every A/B finished within 15.5 minutes of launch. Cost $0.1953: agents $0.1689 at the Fast tier,
reviews $0.0263. In the F4 A/B the bare arm claimed done with 68 of 69 hidden tests passing, and
the referee failed it.

### Section 3 confirmation

<a id="s3-confirmation"></a>

Registered before any of its runs: F4 canonical ticket, bare arm against the Section 3 stack
(instructions, state, scope), class profile with a 420 s agent time limit, 3 A/Bs. The primary
measure for this confirmation only: an arm fails when it ships one or more files outside the
allowed paths. Command: `shipharness ab --section demo-3 --feature F4 --profile class --purpose
pilot`, two A/Bs at once, then one.

| A/B | Bare: out-of-scope files | Harness: out-of-scope files | Last event after launch |
|---|---|---|---|
| `ab-20261017-150928-96cf3a` | 1 (fail) | 0 (pass) | 976 s |
| `ab-20261017-150948-cf151f` | 1 (fail) | 0 (pass) | 899 s |
| `ab-20261017-152601-3a7237` | 1 (fail) | 0 (pass) | 688 s |

Every bare arm changed `app/services/errors.py`, which is outside the F4 build phase's allowed
paths. In every harness arm the scope layer blocked the same file: "app/services/errors.py: outside
the allowed paths for the build phase". Result: bare 0 of 3, harness 3 of 3, **harness ahead**.
Cost $0.1439.

Run ids, bare first: `r-20261017-150928-660a37` and `r-20261017-150928-b0ffa0`;
`r-20261017-150948-c81d83` and `r-20261017-150948-45b48a`; `r-20261017-152601-ca37f4` and
`r-20261017-152601-59e165`.

Secondary (the F4 ticket's own primary measure: every hidden test and every referee mutant): no arm
passed; hidden tests 62 to 68 of 69. That is why the console's primary verdict on screen 1 reads
FAIL for both arms of this task; the scope result shows on screen 3 as `diff_scope` and `⊘ blocked`.
The harness arms ended "ABORTED: timeout" on the harness's own 120 s limit (`HARNESS_TIMEOUT_S`),
after each had shipped a change, so under the registered rule the difference is not caused by
harness-only timeouts.

### Class plan

<a id="class-plan"></a>

The rule: a live A/B only where the data shows a real gap (the harness arm passes the primary
measure in more runs than bare); otherwise the harness arm alone, live (`make show-N`). Every demo
section is live; `make replay` is the emergency fallback only.

| Section | Data, primary passed bare / harness | Class demo |
|---|---|---|
| S1 | 7 of 7, 7 of 7 | `make show-1` |
| S2 | 7 of 7, 7 of 7 | `make show-2 SESSION_BUDGET=12,38` |
| S3 | S3 confirmation: 0 of 3, 3 of 3 | `make demo-3 FEATURE=F4` (live A/B) |
| S4 | 0 of 4, 0 of 4 | `make show-4` |
| Final | not part of the test runs | `make final` (live A/B) |

S1 to S3 data are runs 3 and 4 and the class-profile round. S4 data are run 3 and the
class-profile round.

### Timings

<a id="timings"></a>

The class commands, run one at a time on a quiet machine after `make warm`, with `PURPOSE=pilot`,
2026-10-17 11:18-12:17 UTC. The agent time limit was then 300 s; the class profile now uses 420 s.
Times are the `real` line of `time make ...`, from launch to the cost line.

| Command | A/B | Result | Launch to cost line |
|---|---|---|---|
| `make show-1` | `ab-20261017-112101-c5d839` | Primary pass, hidden 52 of 52 | 10 min 14 s |
| `make show-2 SESSION_BUDGET=12,38` | `ab-20261017-113213-fe89a3` | Primary pass, hidden 56 of 56 | 10 min 7 s |
| `make show-3` | `ab-20261017-114259-b64f54` | Primary pass, hidden 49 of 49 | 7 min 43 s |
| `make show-4` | `ab-20261017-115138-c45d9d` | Primary fail, hidden 68 of 69 | 11 min 6 s |
| `make final FEATURES=F5` | `ab-20261017-120323-c97138` | Hidden 46 of 46 in both arms | 12 min 47 s |

Costs: $0.019744, $0.029525, $0.017216, $0.026511, and $0.045597. In `make show-1` the primary
verdict came 4 min 11 s after launch and the full verdict at 10 min 0 s. `make show-2` and
`make show-4` hit the 300 s agent time limit (exit 2); so did the final's harness arm.

`make demo-3 FEATURE=F4` was not timed as a make command. The three S3 confirmation A/Bs, run with
the same settings, ended 688 s to 976 s after launch (table above); the first two ran at the same
time.

A re-timing of `make show-2`, `make show-4`, and `make final` with the 420 s limit was started on
2026-10-17 at 17:18 UTC and stopped at its first step (`make warm` and `make show-2` failed before
any model call), so no 420 s timings exist yet.

<a id="costs"></a>

At the caps, the class plan needs at most: three `make show-N` runs at $0.24, one `make demo-3` at
$0.48, and two final features at $0.58, so $2.36, under the $2.50 session cap (caps from
`.env.example`).

### Optional extras

<a id="extras"></a>

Constructed examples (`make example-1` to `make example-4`), 2026-10-17, scripted steps, no model:
`ab-20261017-100044-031a15`, `ab-20261017-100051-c21e99`, `ab-20261017-100915-6f03a4`,
`ab-20261017-103436-ae374a`. Times (the `real` line of `time make example-N`): 3 min 17 s, 7 min
59 s, 12 min 22 s, and 11 min 21 s; the first three ran while other runs shared the machine.

Recorded runs for replay, one per section:

| Section | A/B | What it shows |
|---|---|---|
| 1 | `ab-20261016-212252-aa1644` (run 3, F4) | The harness arm added 3 new R1 violations |
| 2 | `ab-20261016-213317-9a0ec1` (run 3, F2) | The harness arm gave up the build phase after a 12-turn session 1 |
| 3 | `ab-20261016-214151-ca9841` (run 3, F4) | The bare arm changed 2 files outside the allowed paths; the harness arm 0 |
| 4 | `ab-20261017-090903-926c02` (class-profile round, F4) | The bare arm claimed done with 68 of 69 hidden tests passing |

### Harness text renamed after the measurements (2026-10-18)

<a id="harness-rename"></a>

On 2026-10-18 the harness text the agent reads changed its wording: the bare codes for features,
house rules, sections, and test filters were replaced by their plain names ("House rule 1: Tenant
isolation", "Feature 4: Version checks on issue edits"). The rules, the checks, and the tasks did
not change. The files that changed:

- the instruction files the instructions layer places (`AGENTS.md`, `ARCHITECTURE.md`, `docs/`, and
  the add-endpoint skill) and the handbook both arms read (`docs/HANDBOOK.md`), with the feature
  specs in `docs/features/`;
- the state files the state layer writes (`progress.md`, `session-handoff.md`, `init.sh`, the exec
  plan), the scope block of the first message, and the verify block;
- the gate's feedback when it refuses a done claim, and the test filters' names;
- the ticket text of the Feature 3 tasks in the dataset.

Every measurement on these pages, in this file and in the section files, was made with the earlier
text. One live verification run per section follows, with the class profile, to confirm that the
renamed text gives the same results.

### Checkpoint tags moved after the harness rename (2026-10-18)

<a id="checkpoint-move-rename"></a>

The checkpoint commits carry TeamTrack's directory, which holds the renamed harness text, the
handbook, and the feature specs, so the eight checkpoint tags no longer matched a fresh build and
the release build refused them. With the owner's approval (option B: move the tags), they were
rebuilt on 2026-10-18 on main 449833a with `build_checkpoints.py --force --owner-approved-move`:
m1-s1-start e82c59f -> 821db62, m1-s2-start 6d8102e -> aa24113, m1-s3-start d06688a -> c111cca,
m1-s4-start d0b98d0 -> add3e45, m1-final-start 6b0050e -> 4cf12f7, m1-complete 764b2b2 -> adee528,
m1-alt-a a0aef38 -> 0d46a40, m1-alt-b 846baab -> f5077ef. In all eight the TeamTrack tree differs
only in the renamed text (46 files under `platform/teamtrack/docs/`, `harness/instructions/`, and
`reference/f3/`); the application code and the tests are unchanged.

The old commits are archived under `refs/archive/checkpoints-2026-10-18/<tag>`, next to the
earlier archives `checkpoints-2026-10-16` and `checkpoints-2026-10-17b`. Every recorded result on
these pages names the commit it ran on (`checkpoint_sha`), which is one of the archived commits,
not the new tags: the measurements were made on the old checkpoints. The graders that compare a
record with the tag treat a rebuilt checkpoint with the same TeamTrack tree as the same
checkpoint; after this move the trees differ, so the Assignment 4 grader also accepts the earlier
`m1-s4-start` commits listed here (a9d6be2, which the Assignment 4 reference run names, and
d0b98d0), and nothing else. No result was changed.

### Verification runs after the rename

The runs are listed below once they are complete.

## Captures

<a id="captures-root"></a>

### Root README screenshots

All from `make console` on the course machine, 2026-10-17, taken with a headless browser at
1920 by 1080.

| File | Run | Taken |
|---|---|---|
| `docs/images/screen-1-ab-minute-3.png` | `ab-20261017-120323-c97138` (`make final FEATURES=F5`) | Minute 3 of the run |
| `docs/images/screen-1-primary-verdict.png` | `ab-20261017-112101-c5d839` (`make show-1`) | Minute 5 of the run |
| `docs/images/screen-2-boards.png` | `ab-20261017-120323-c97138` | After the run |
| `docs/images/screen-4-report.png` | `ab-20261017-120323-c97138` | After the run |
| `docs/images/screen-3-scope-blocked.png` | `ab-20261017-150928-96cf3a` (S3 confirmation) | After the run, 17:30 UTC |

<a id="captures-setup"></a>

### Setup and reference captures

- `make doctor` in a checkout with no `.env`, `make warm` with no class date, `make help`,
  `uv run shipharness --help`, the console start lines, `git tag -l 'm1-*'`, the image sizes, and
  every `make -n` line on the reference page: captured 2026-10-17 17:28 UTC in a clean checkout of
  the course-first layout, commit 6ed6c33.
- The `make warm` lines with the class date set: captured 2026-10-17 11:18 UTC before the quiet
  timing runs (images rebuilt because their source had changed).
- WSL, Docker, git, uv, and make version lines on the Windows and Linux pages: captured
  2026-10-17 on the course machine (version commands, no run id).
- The terminal lines of the first live run: `make show-1`, `ab-20261017-112101-c5d839`.

## Sources and findings

<a id="sources"></a>

Quotes on the root README and the shared pages, with their finding ids (the full list of sources
and findings is [REFERENCES.md](../REFERENCES.md)):

- **F-a-05** (A1, OpenAI, "Harness engineering"): "From the agent’s point of view, anything it
  can’t access in-context while running effectively doesn’t exist."
- **F-a-08** (A2, Anthropic, "Effective harnesses for long-running agents"): "each new session
  begins with no memory of what came before."
- **F-a-20** (A1): "Codex replicates patterns that already exist in the repository—even uneven or
  suboptimal ones."
- **F-a-18** (A4, Anthropic, "Building a C compiler"): "(Run this in a container, not your actual
  machine)"
- **F-a-15** (A3, Anthropic, "Harness design for long-running application development"): "agents
  reliably skew positive when grading their own work"
- **F-a-02** (A1): "design environments, specify intent, and build feedback loops" (the basis for
  the course's word "harness").
- **F-a-124** (A3): "every component in a harness encodes an assumption about what the model can't
  do on its own, and those assumptions are worth stress testing"
- **F-a-125** (A3): "removing one component at a time and reviewing what impact it had on the final
  result."
- **F-a-143** (A1): its results should "not be assumed to generalize without similar investment".
- **F-a-28** (A1): "A short AGENTS.md (roughly 100 lines) is injected into context and serves
  primarily as a map, with pointers to deeper sources of truth elsewhere."
- **F-b-19** (B11, Meta, TestGen-LLM): "five executions" (the flakiness re-runs).
- **F-a-110** (A3): a separate evaluator judges the work (the harness, not the agent, sets
  `passes`; course design).
- **F-a-126** (A3): "read its traces on realistic problems"
- LangSmith billing page (read 2026-10-17): "Base traces have the base retention and are short-lived
  (14 days)"
- **F-a-108** (A2): A2 lets the agent set `passes` after testing; the course moves that to the
  harness.

Account and plan facts on the setup pages come from the providers' pages, each read on 2026-10-17
and linked where used: OpenAI's model page for gpt-6-luna and its rate-limits guide, LangSmith's
pricing and billing pages, and Microsoft's and Docker's install pages.

## Commits and tags

<a id="commits"></a>

| What | Commit or tag |
|---|---|
| Early primary verdict, five flakiness re-runs | 76ff2ca |
| Class profile (effort low, Fast tier, 2 CPUs) | 3f5a7c7 |
| Class profile agent time limit 420 s; class-date checks in `make doctor` and `make warm` | e15eae1 |
| `finish(not_done)` ends only the session (F2 fix) | 501be88 |
| S3 confirmation registered, before its runs | a87136d |
| S3 confirmation run on | main 1a70f84 |
| `make demo-3 FEATURE=F4` | da92e38 |
| Release tag for the class | `class-v1` (no `harness-frozen` tag) |

The 8 checkpoint tags (`m1-s1-start` to `m1-alt-b`) were rebuilt on 2026-10-17; the `teamtrack/`
tree of each differs from the old commit only in a comment in `reference/checkpoints.toml`, and the
old commits stay reachable, so recorded checkpoint commits still resolve.
