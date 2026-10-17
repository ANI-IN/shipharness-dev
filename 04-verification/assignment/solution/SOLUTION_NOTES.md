# Solution notes: assignment A4

Reference solution for R8 (soft delete respected on every endpoint), filter 6 (no duplicate test),
the live step (testgen with filter 6, and an A/B on F4), the portfolio, and the learner skill. Brief:
`../assignment/README.md`. Source ids point to `RESEARCH.md` and `research/notes/`.

## Approach

1. Soft-delete in the database, not through the API. `TeamTrackSoftDeleteAdapter.soft_delete`
   picks the lowest-id live issue of each of the home org's projects (issues 1 and 11 in the seed),
   sets `deleted_at`, and sets the title to a marker such as `[r8-deleted:1]`
   (`a4_verification/adapter.py`).
2. Plan probes from the OpenAPI schema, lists first (`plan` in `a4_verification/r8_soft_delete.py`):
   one `deleted_list` probe per GET endpoint that does not address an issue, one `deleted_body`
   probe per write whose generated body has `issue_id`, and one `deleted_path` probe per endpoint
   of any method that addresses an issue.
3. Judge each response on text, not ids (`judge`): a list fails when a 2xx body contains a marker,
   a path probe fails on anything but 404, a body probe fails on 2xx.
4. Report through the framework: `Finding(rule="R8", detail_key=<probe kind>)`,
   `apply_exemptions`, `make_result`, `ctx.progress`, registered with `register_check` as
   `r8_soft_delete`. `run_r8` hands everything else to `shipharness.checks.runner`, so baselines,
   exit codes, and the JSON document are the framework's own.
5. Filter 6 normalises each test's syntax tree (docstring dropped, locals renamed in order of first
   appearance) and compares decorators, parameters, and body (`a4_verification/dedup_filter.py`).
   It remembers the candidates it kept, so a later copy in the same run is discarded too.

## Design choices

- Marker titles. Project 1, user 1, org 1, and audit row ids share the numbers of the deleted
  issues, so "id 1 appears in the body" flags `GET /projects`, `GET /me`, and `GET /orgs/current`
  on a correct build. A marker only the deleted row can contain makes every list finding a real
  appearance, at any nesting depth, in any response shape. The brackets stop `[r8-deleted:1]`
  from matching inside `[r8-deleted:11]`.
- Database soft delete. If R8 deleted through `DELETE /issues/{id}`, a build with a broken delete
  endpoint would make R8 fail for the wrong reason, and the delete endpoint's own behaviour is
  already probed by R1, R2, and R5. The cost is that the adapter knows a table and a column name.
  That knowledge sits in the adapter, like `audit_count` for R5.
- Adapter default. The check uses `a4_verification.adapter:TeamTrackSoftDeleteAdapter` unless the
  caller names an adapter, so `run_r8 --adapter module:attr` points R8 at another app with the
  same two methods (`soft_delete`, `deleted_marker`).
- Lists before writes. A write probe that wrongly succeeds (a PATCH that renames the issue) would
  remove the marker; lists run first so every list sees every marker.
- `detail_key` is exactly the probe kind. `mark_baseline` keys on `(rule, endpoint, severity,
  detail_key)`; ids, statuses, and response text stay in `detail`, so the legacy `/v1/issues`
  finding matches across runs and counts as baseline.
- Remediation in the message. Each `detail` says what to change ("add `deleted_at IS NULL` to the
  query", "load the issue with the live-issue lookup"), following A1: "we write the error messages
  to inject remediation instructions into agent context" (A1, F-a-97).
- Issue parameters. `{issue_id}`, or a parameter without a `_id` resource name right after an
  `issues` segment. This matches how `fill_path` resolves `{id}` (`checks/payloads.py`).
- Filter 6 as number 6, outside `DEFAULT_FILTERS`. The pipeline takes a `filters` sequence, so the
  filter runs without changing `platform/src/`. It reads source only, so it could run first (cheapest); it
  runs last in `apply_filter` because it is applied to testgen's kept tests after the fact.
  `--update-report` appends its rows to the testgen report, so one file shows all six filters.
- Parameters are never renamed. Two tests that differ only in fixture names use different fixtures
  and so test different setups.
- Grader in process. Seeded violations are text patches on a fresh copy of `platform/teamtrack/app`, loaded
  with `shipharness.checks.probe.load_app` on a temporary SQLite file: no Docker, a few seconds per
  build. A patch whose old text is missing fails loudly, so a TeamTrack change cannot turn a seeded
  violation into a silent pass.
- One pytest subprocess per grading run, with `A4_IMPL` naming the folder; the `a4_verification`
  package of that folder is the only one imported, so the check registry has one `r8_soft_delete`.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Find deleted issues by `id` in response bodies | False positives on every resource that shares the number (hidden test `test_shared_numeric_ids_are_not_evidence`) |
| Soft-delete through `DELETE /issues/{id}` | Couples R8 to the delete endpoint working; R1, R2, R5 already cover that endpoint |
| Probe only GET endpoints | Misses writes that resolve a deleted issue (hidden test `test_write_endpoint_that_resolves_a_deleted_issue`) |
| A list of issue endpoints in the check | Misses endpoints the build adds (hidden tests for `/recent-issues`, `/columns`, `/issues/{id}/history`) |
| Compare test source text or a hash of it | Comments and formatting change the text, not the test |
| Token or embedding similarity for duplicates | Not exact: a threshold either keeps copies or drops near tests that check something different, and every discard needs a reason a reader can verify |
| Add filter 6 to `DEFAULT_FILTERS` | Needs a change under `platform/src/`; out of the assignment's scope |

## Trade-offs

- One deleted id per path and body probe keeps the probe count at one per endpoint (15 probes on
  TeamTrack) at the cost of not checking every deleted row on every endpoint.
- The marker changes the title of the deleted rows. An endpoint that validates or reformats titles
  could hide the marker; TeamTrack returns titles as stored.
- Filter 6 is exact and explainable but misses semantic duplicates (two tests that check the same
  rule through different calls).

## Known limits

- A list endpoint with a required query parameter (for example a search `q`) gets a generated value
  that filters the deleted rows out, so a leak there stays hidden. A next step is a probe that
  sends the marker as the search text.
- Only the first page of each list is read. The deleted rows have the lowest ids, so they are on
  the first page of every id-ordered list; a list in another order could push them off it.
- Archived projects behave like deleted issues in the handbook ("Archived projects behave as if
  they do not exist"); R8 covers issues only.
- Body probes look for a top-level `issue_id` key; a nested or differently named reference
  (`parent_issue_id`) is not probed.
- Filter 6 renames names inside nested functions in a test body along with the test's own locals.
- The reference solution's live evidence is one testgen run and one F4 A/B at k=1, captured on
  2026-10-17 (`live/README.md`). In that A/B the harness arm stopped with `ABORTED: timeout` (43 of
  69 hidden tests, 0 of 4 referee mutants, no shipped test) and neither arm passed the primary
  measure (`portfolio/langsmith.md`). The live-evidence criterion grades the files, not the
  outcome, so the reference earns its 10 points on them; the run is an example of the evidence,
  not a result about the harness.
- No criterion rests on a PENDING marker. Until 2026-10-17 the grader accepted markers for
  this folder only (`pending_only` in `a4_live.py`, `reference_mode` in `a4_support.py`), so 20
  of its 100 points were not earned on real work. That special case is removed: the visible tests
  and the self-check no longer name this folder, and `grader/tests/test_live.py` and
  `grader/tests/test_portfolio.py` check that a marker fails the live-evidence and portfolio
  criteria for every folder, and that this folder passes them on its captured run.

## Hidden tests (reveal in the Thursday review)

`grader/hidden_tests/hidden_seeds.py` builds these TeamTrack copies:

| Seed | What it adds or breaks | Expected R8 finding |
|---|---|---|
| `H_RECENT` | New `GET /projects/{project_id}/recent-issues` without `deleted_at` | `deleted_list` there |
| `H_NESTED_LIST` | New `GET /projects/{project_id}/columns`, issues inside a dict of lists | `deleted_list` there |
| `H_TRANSITION` | Only the transition service skips the live-issue lookup | only `deleted_path` at `POST /issues/{issue_id}/transition` |
| `H_ID_PARAM` | New `GET /issues/{id}/history` | `deleted_path` there |
| `H_NESTED_PATH` | New `GET /projects/{project_id}/issues/{issue_id}/peek` | `deleted_path` there |
| `H_BODY` | New `POST /projects/{project_id}/watches` taking `issue_id` in the body | `deleted_body` there |
| `H_RECENT_OK`, `H_BODY_OK` | Correct versions of the two new endpoints | nothing new |
| `H_DECOY` | New `GET /projects/{project_id}/digest` returning `{"id": 1, ...}` | nothing new |

The hidden filter tests (`grader/hidden_tests/test_filter_hidden.py`) cover consistent and swapped
local renames, fixture names, global helpers, attributes, parametrize data, earlier kept
candidates, an existing test compared with itself, class methods, async tests, loop, `with`, and
`except` names, and a file that does not parse.

Before the hidden tests were final, the author checked them against deliberately weakened copies
of the reference solution with a scratch script that is not committed, and the outcomes were not
recorded, so this check cannot be rerun or verified from the repository. The weakenings tried were:
`issue_param` without the `{id}` rule, no body probes, GET-only path probes, id-based list
evidence, no local renaming in filter 6, and renaming every name. Each hidden test is meant to
catch one of them (for example `test_shared_numeric_ids_are_not_evidence` for id-based evidence);
a committed mutation check of the grader is an open item.

## Review notes (Thursday)

- Expected approach: the four probe kinds, marker evidence, stable `detail_key`, AST
  normalisation with local renaming.
- Discussion: why does the legacy `/v1/issues` finding belong in the baseline rather than in an
  exemption list? (R1 makes the same choice for the same handler: DESIGN §5.)
- Discussion: filter 6 removes copies; filter 3 already discards tests that add nothing. When does
  a duplicate pass filter 3? (When the copy is proposed in the same run as the original: both add
  the same new coverage over the existing suite.)

## Captured output

Real output, no model calls, each command run once. Each text file starts with the label
"captured on 2026-10-17 from `<command>` at commit <sha> (no model calls); your output will
differ", then `$ <command>`, then everything `make` printed and the exit code. The two solution
files were captured again at commit 65d70a0, after the live run went into `live/` and the
marker special case was removed; the starter files are from commit 155dc77 (that change does not
touch what the starter scores).

| File | Commit | Command | Result |
|---|---|---|---|
| `captured/self-check-starter.txt` | 155dc77 | `make check-assignment-4` | 2 of 23 visible tests pass, every failure names its TODO, 32 TODO markers listed; `check.py` exits 1, so `make` exits 2 |
| `captured/self-check-solution.txt` | 65d70a0 | `make check-assignment-4 A4_IMPL=04-verification/assignment/solution` | exit 0, 23 of 23, the four live-evidence tests and the three portfolio tests on the captured run |
| `captured/grade-solution.txt` | 65d70a0 | `make grade-assignment-4 SUBMISSION=04-verification/assignment/solution` | Score: 100/100, every criterion on real work (no marker accepted) |
| `captured/grade-starter.txt` | 155dc77 | `make grade-assignment-4 SUBMISSION=04-verification/assignment/starter` | Score: 3/100 (one R8-interface test and one F6-interface test pass) |
| `captured/r8-teamtrack.json` | 155dc77 | `PYTHONPATH=04-verification/assignment/solution uv run python -m a4_verification.run_r8 --build platform/teamtrack --checkpoint m1-base --feature A4` (stdout only; JSON, so it carries no label line; exit 3) | 15 probes, one finding at `GET /v1/issues` (`deleted_list`, `leak`) |

`make grade-assignment-4` runs `grade.py` through `platform/scripts/grade_assignment.py`, which passes the
absolute folder (hence `A4 grade for /home/ani/wt/<worktree>/...`) and adds a `grading assignment 4:
<folder>` line.

## Live step and model-run parts

The live step of the brief applies to this folder too. The run was captured on 2026-10-17:
testgen run `r-20261017-093940-52dde8` ("kept 1 of 5 proposed tests", `Cost: $0.003287 (testgen,
model gpt-6-luna)`) and the F4 A/B `ab-20261017-094339-3b29e3` (cost line `Cost: $0.042138`, both
arms' records in `live/scores/`). `live/README.md` lists the files and the commands that produced
them; the files are validated like any submission's.

How the grader reads "filter 6 in the pipeline": `shipharness testgen` runs filters 1-5 and writes
their rows to `testgen-report.json`; it has no option to add a filter (`platform/src/shipharness/testgen/`).
`apply_filter --update-report` runs the learner's `NoDuplicateTest` through `run_pipeline` over
the tests testgen kept and appends one row with `"filter": 6` per kept test, after the testgen
rows, plus a `filter6` object (`kept`, `existing_tests`). The grader requires that shape: at least
one kept test, exactly one filter-6 row with a reason per kept test, rows after filters 1-5, and
`filter6.kept` equal to the passed filter-6 rows. It cannot prove the rows came from the learner's
filter without the target repository's existing tests, which a submission does not carry; the
hidden filter tests grade the filter itself.

Why the F4 A/B replaces the section-4 experiment: by the caps, the A/B (two runs at $0.20 and two
reviews at $0.04) costs at most $0.48 and the live step at most $0.68, inside the A4 plan of $1.75
(DESIGN §11.5); the experiment's per-command cap alone ($2.50) was above that plan.

The run sections of `portfolio/evidence-report.md`, `portfolio/langsmith.md`, and
`portfolio/case-study.md` are filled from those files: counts, run ids, `trace_url` values, and
cost lines as the files hold them. What the A/B shows: the bare arm passed 68 of 69 hidden tests
and killed 4 of 4 referee mutants; the harness arm stopped with `ABORTED: timeout` after 43 turns
with 43 of 69 and 0 of 4 and no shipped test; neither passed the primary measure.

What pilot run 2 says about the F4 A/B in the live step (VERIFICATION.md, M6 pilot run 2): both
arms failed the primary measure in all three F4 A/Bs. The bare arm killed 3, 4, 3 of 4 referee
mutants and passed 69, 66, 69 of 69 hidden tests; the harness arm shipped 0, 0, 3 tests and so
killed 0, 0, 2 mutants. None of its shipped tests came from the 12-turn test phase: in the first
two A/Bs the test phase proposed no test, and in `ab-20261016-191626-6100f6` the 3 shipped tests
were written in build session 1 while the test phase's one new test was discarded by the filters
("kept 0, discarded 1"). Change 9 (a test-phase session starts with the feature's tests) was the
harness-arm change for run 3; changes 10 and 11 (judge each arm when it finishes; one batched
unmutated-pass step, shown equivalent on 181 tests) change referee speed, not outcomes. Run 3
(VERIFICATION.md, "Run 3"): both arms failed 3 of 3 again, and the harness arm shipped no tests (its
test phase was cut short by the agent time limit, "F4 test phase (investigated, no bug)"). The
class-profile round (VERIFICATION.md, "Class-profile round", `ab-20261017-090903-926c02`, class
profile, which the assignment's A/B does not use): both arms 68 of 69 hidden tests, mutants 4 of 4
(bare) and 1 of 4 (harness). The live step is graded on its files, not on these results.

The live A/B command carries `--purpose assignment`. Without it `shipharness ab` uses the class
purpose, which refuses to start unless `SHIPHARNESS_CLASS_DATE` is set and otherwise traces into
the class project (`_trace_target` in `platform/src/shipharness/ab/commands.py`). `ab_run_problems` in
`a4_live.py` requires it, and parses the cost line in the form `cost_line` prints today (with the
`; build $X of $15.00 ($Y left)` part, which the first version of the check rejected). The A/B
line may end with `, profile=<name>`, which `shipharness ab` prints since 2026-10-17 and the real
capture has (78df3f5). All three are covered in `grader/tests/test_live.py`.

## Make targets

Both targets are in the `Makefile` (9fd8273); `make -n` shows what they run:

| Target | Command |
|---|---|
| `make check-assignment-4` | `uv run python 04-verification/assignment/check.py` (with `A4_IMPL=<folder>`: `--impl <folder>`) |
| `make grade-assignment-4 SUBMISSION=<folder or git URL>` | `uv run python platform/scripts/grade_assignment.py 4 "<folder or git URL>"`, which runs `grade.py --impl <folder>` (instructor only) |

`SUBMISSION` is a folder (the learner's implementation folder with `live/`, or a checkout of the
learner's course repo, in which case `grade.py` grades
`04-verification/assignment/starter/` inside it, `resolve_impl`) or a git URL, which
`platform/scripts/grade_assignment.py` clones shallow into a temporary folder first.
