# Case study: making "deleted means gone" a checked rule

Reference version. Numbers from model runs are `[[PENDING]]` until the instructor's run.

## Problem

TeamTrack's handbook says a deleted issue behaves as if it does not exist: 404 on read, hidden
from lists. Nothing checked that. A coding agent that adds an endpoint can query the issues table
without the `deleted_at` filter, and the visible tests still pass, because no visible test deletes
an issue first. A1 describes the fix for this class of problem: rules the team cares about become
checks, "enforced mechanically via custom linters ... and structural tests" (A1, F-a-93). The
legacy `/v1/issues` handler already shows the failure: it lists deleted issues today.

## What I built

- R8, a generic check in the shipharness check framework. It reads the app's OpenAPI schema,
  soft-deletes the first issue of each project directly in the database, gives those rows a marker
  title, and probes every endpoint as an admin: lists must not show a marker, any operation that
  addresses a deleted issue must answer 404, and a write that names a deleted issue in its body
  must fail. Findings carry a stable `detail_key`, so the referee's baseline marks the legacy
  finding as old and counts only new ones.
- Filter 6 for the test pipeline: a proposed test that repeats an existing test, or a test kept
  earlier in the same run, is discarded with the name of the test it copies. TestGen-LLM added a
  filter "to remove previously seen test cases" (B11, F-b-26); this one also ignores renamed local
  variables, which is a course choice.
- A skill, `testgen-evidence`, that turns a testgen run into an evidence report.

## Evidence

- On a TeamTrack copy the grader seeds faults the visible tests do not show: a new list endpoint,
  a deleted issue nested inside a board response, a write-only lookup, a `{id}` path parameter, an
  issue parameter after a project parameter, and an issue id in a request body. R8 reports each one
  at the right endpoint and reports nothing on correct versions of the same endpoints
  (`../captured/grade-solution.txt`).
- On TeamTrack itself R8 makes 15 probes and finds one violation, the legacy list
  (`evidence-report.md`, "R8 on TeamTrack").
- Testgen on `app/repositories/issues.py`:

[[PENDING: kept and discarded counts from the testgen run, and how many kept tests filter 6 removed | source: M6 pilot | how: commands in evidence-report.md, "Commands"]]

- The live A/B on F4, bare against the demo-4 layers (`langsmith.md`):

[[PENDING: per-arm hidden tests passed and mutants killed from the two score records of the F4 A/B | source: M6 pilot | how: uv run shipharness ab --section demo-4 --feature F4 --no-preview]]

## What I learned

The marker title mattered more than the probes. My first idea was to look for the deleted issue's
id in each response, but project 1, user 1, and org 1 share that number, so every list of projects
would have been a finding. Text that only the deleted row can contain removes that whole class of
false positive. The second lesson is about baselines: a check that reports the legacy handler on
every run is noise unless its findings match across runs, which is what `detail_key` is for. A4
warns that "it is easy to see tests pass and assume the job is done, when this is rarely the
case" (A4, F-a-17); seeded faults are how I found out whether my own check was done.

## Next steps

- Probe search endpoints with the marker as the query text, so a required filter parameter cannot
  hide a leak.
- Extend the adapter to archived projects, which the handbook treats the same way.
- Run filter 6 inside `shipharness testgen` rather than after it.
