# Case study: making "deleted means gone" a checked rule

Reference version. The run numbers come from the reference solution's live run, captured on
2026-10-17 (`../live/`).

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
- Testgen on `app/repositories/issues.py` (run `r-20261017-093940-52dde8`, $0.003287) proposed 5
  tests and kept 1; filter 3 discarded the other 4: no new coverage and no mutant kill over the
  existing suite. Filter 6 removed none: the kept test copies none of the 23 existing tests
  (`evidence-report.md`, "Results" and "Filter 6 on the kept tests").
- The live A/B on F4 (`ab-20261017-094339-3b29e3`, `langsmith.md`): the bare arm passed 68 of 69
  hidden tests and killed 4 of 4 referee mutants; the harness arm (demo-4 layers) stopped on a
  timeout with 43 of 69 and 0 of 4. Neither passed the primary measure, and one run per arm is an
  example, not a rate.

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
