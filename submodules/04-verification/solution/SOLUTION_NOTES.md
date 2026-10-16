# Solution notes: assignment A4

Reference solution for R8 (soft delete respected on every endpoint), filter 6 (no duplicate test),
the testgen and LangSmith steps, the portfolio, and the learner skill. Brief:
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
  filter runs without changing `src/`. It reads source only, so it could run first (cheapest); it
  runs last in `apply_filter` because it is applied to testgen's kept tests after the fact.
- Parameters are never renamed. Two tests that differ only in fixture names use different fixtures
  and so test different setups.
- Grader in process. Seeded violations are text patches on a fresh copy of `teamtrack/app`, loaded
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
| Add filter 6 to `DEFAULT_FILTERS` | Needs a change under `src/`; out of the assignment's scope |

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

Before the hidden tests were final, each was checked against a deliberately weakened copy of the
reference solution (scratch script, not committed): `issue_param` without the `{id}` rule fails
the `{id}` test; dropping body probes fails the body test; GET-only path probes fail the
transition test, a hidden baseline test, and two visible tests; id-based list evidence fails 14 tests; no local renaming
fails 3 filter tests; renaming every name fails the global-helper test.

## Review notes (Thursday)

- Expected approach: the four probe kinds, marker evidence, stable `detail_key`, AST
  normalisation with local renaming.
- Discussion: why does the legacy `/v1/issues` finding belong in the baseline rather than in an
  exemption list? (R1 makes the same choice for the same handler: DESIGN §5.)
- Discussion: filter 6 removes copies; filter 3 already discards tests that add nothing. When does
  a duplicate pass filter 3? (When the copy is proposed in the same run as the original: both add
  the same new coverage over the existing suite.)

## Captured output

Real output, produced on this branch with no model calls (paths relative to the repository root):

- `captured/self-check-starter.txt`: the self-check on the starter (exit 1, 2 of 19 visible tests
  pass, every failure names its TODO).
- `captured/self-check-solution.txt`: the self-check on this folder (exit 0, 19 of 19).
- `captured/grade-solution.txt`: the grader on this folder, Score: 100/100.
- `captured/grade-starter.txt`: the grader on the starter, Score: 3/100.
- `captured/r8-teamtrack.json`: `run_r8` on `teamtrack/` (15 probes, one finding at
  `GET /v1/issues`).

## Model-run parts (pending)

The testgen run and the LangSmith experiment need model calls; their output is pending in
`portfolio/evidence-report.md`, `portfolio/langsmith.md`, and `portfolio/case-study.md`:

[[PENDING: testgen run on TG-teamtrack-app-repositories-issues: kept and discarded tests with reasons, filter 6 output, and cost line | source: M6 pilot | how: uv run shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10 --out .shipharness/a4/testgen]]

[[PENDING: LangSmith comparison link and per-arm counts for the section-4 split at k=1 | source: M6 pilot | how: uv run shipharness experiments --dataset teamtrack-features-v1 --split section-4 --k 1 --batch a4-reference]]

## Make targets

The integrator adds these rules to the `Makefile` (and removes `check-assignment-4` and
`grade-assignment-4` from the placeholder rule):

```make
check-assignment-4:
	$(UV) run python submodules/04-verification/assignment/check.py --impl $(or $(A4_IMPL),submodules/04-verification/assignment/starter)

grade-assignment-4:
	$(UV) run python submodules/04-verification/solution/grader/grade.py --impl $(or $(A4_IMPL),submodules/04-verification/solution)
```
