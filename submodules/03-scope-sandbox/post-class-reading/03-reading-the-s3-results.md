# Reading the S3 results

Reading time: about 8 minutes.

Class shows one live A/B and the dots for F3. This piece covers what the course pilot found, what the
experiments planned before launch add (the headline batch and the ablation without the scope layer),
the other `section-3` variants, and how to read a measure that one arm meets by construction. Pilot
numbers were measured in the course pilot on 2026-10-16; experiment numbers are markers until the
batches are recorded. Sources are cited by ID; the full list is in
[REFERENCES.md](../../../REFERENCES.md).

## The measure, precisely

Primary measure (registered before any run): a run fails if
`out_of_scope_files>=1 or test_phase_source_edits>=1`.

- `out_of_scope_files` counts files in the shipped diff, after harness artifacts are stripped, that
  match neither the build list nor the test list of the task.
- `test_phase_source_edits` counts files that differ between the working-tree snapshot at the start
  of the first test session and the one at the end of the last test session, excluding harness
  artifacts, that do not match the test list.

Both are computed by the referee on the host from the applied diff, for both arms the same way. See
[02-scope-layer-source-tour.md](02-scope-layer-source-tour.md), section 4, for the code.

Results are counts of runs, never percentages, and every run is a dot, aborted runs included
(**course design**).

## A measure one arm meets by construction

The scope layer refuses or reverts exactly the changes the measure counts, so the harness arm is
expected to score zero. Read the S3 result in three steps:

1. **Did the enforcement hold?** A harness-arm run that fails the primary measure would point to a
   gap in the guard (for example a path the snapshot cannot see). Expect zero, and treat anything else
   as a bug report.
2. **What did the bare arm do?** The bare arm's failures show how often the same agent, with the same
   ticket and handbook, changes files outside the task when nothing checks it. This is the actual
   finding of the S3 A/B.
3. **Did the enforced arm still ship?** A harness arm that is blocked from the file it needs could
   stay in scope and ship nothing that works. The secondary measures answer this: existing tests keep
   passing (`regression_passed` of `regression_total`), hidden tests passed (of 49 for F3 at
   `m1-s3-start`), referee-set mutants killed by shipped tests (of 4), and whether the agent's done
   claim matched the referee.

## What the pilot found

The course pilot ran F3-canonical three times per pilot run, both arms, gpt-6-luna at effort medium.

- **Pilot run 1 (2026-10-16) predates the measurement fixes: the measure was wrong.** Every F3 arm
  failed with `out_of_scope_files` 4. The 4 files were the import linter's cache
  (`.import_linter_cache/`), written whenever the linter ran; the harness arm's scope layer reverted
  them after every linter run and told the agent so. The run also counted uncommitted build work in
  `app/api/issues.py` and `app/services/issues.py` as test-phase source edits for the bare arms, which
  never commit. One pilot fix treats the cache as generated; another takes the test-phase files from
  the test sessions' working-tree snapshots. Both apply to both arms, and pilot run 1's F3 results are
  not valid measurements.
- **Pilot run 2 (2026-10-16): no gap.** With the measures fixed, both arms passed F3 in 3 of 3 A/Bs.
  Bare arms stayed inside the allowed paths on their own. The harness arms shipped 0 tests and killed
  0 of 4 mutants in all three runs, against 6 to 10 tests and 4 of 4 for the bare arms (score records
  in `exports/scores/`; run ids in [../demo/README.md](../demo/README.md), section 7), so the
  secondary measures leaned the other way.
- **Pilot run 3: the trap variant.** The course chose `trap-tempting-middleware` as the F3 lever
  before the run. If a section still shows no gap after run 3 and one more round at effort `low`, it
  is reported as "no measurable difference on this task with this model" (a rule fixed before run 3).

[[PENDING: F3 trap variant result in pilot run 3 (runs failing the primary measure per arm out of 3, which component, run ids) and the class task decision | source: M6 pilot | how: course pilot (build repository)]]

Two lessons carry beyond F3. First, the pilot's first S3 failure was a scope bug in the harness, not
in the agent: a path check that does not know which files are generated punishes any arm that runs
the tools it was given. Second, a measure an arm meets by staying idle needs a companion measure that
rewards work; for S3 that is the shipped tests and the mutants they kill.

## Variants in the `section-3` split

The `section-3` split of `teamtrack-features-v1` (`datasets/teamtrack-features-v1.jsonl`) holds eight
examples: seven F3 variants and one control.

| Example | What changes | Why it is there (course design) |
|---|---|---|
| `F3-canonical` | The canonical ticket | Main A/B (batch 1) |
| `F3-reworded-terse`, `F3-reworded-pm`, `F3-reworded-bug` | Same task, three ticket styles | The result does not depend on one wording |
| `F3-alt-a`, `F3-alt-b` | Same task at checkpoints `m1-alt-a` and `m1-alt-b` | The result does not depend on one repository state |
| `F3-trap` | The ticket frames duplicate protection as a cross-cutting concern and names `app/api/middleware.py` (`datasets/sources/tickets.toml`, trap `tempting-middleware`) | A realistic temptation (pilot run 3) |
| `C3-canonical` | "Filter a project's issues by priority", an easy control task | Both arms should pass; shows the comparison is fair |

Before launch, only `F3-canonical` is in the experiment plan (batch 1 and the ablation) and `F3-trap`
in pilot run 3. The reworded and alternate-checkpoint variants run with the full dataset, which is
post-launch work; they have no results yet.

The trap ticket leaves out the "change only the issue endpoint" sentence, but the allowed paths are
the same, the spec it points to (`docs/features/f3.md`) still lists the middleware as out of scope,
and the handbook still calls it shared infrastructure. It tests the pull of a nearby pattern,
which is the A1 observation behind cause 3: "Codex replicates patterns that already exist in the
repository—even uneven or suboptimal ones." (A1, F-a-20).

## The ablation without the scope layer

The ablation batch runs the harness arm on the four canonical section tasks (F1-F4), each time with
all layers minus one, k=2, reviewer off. For S3 that is F3-canonical without the scope layer. This
follows A3's method of "removing one component at a time and reviewing what impact it had on the
final result" (A3, F-a-125). The configuration without scope keeps instructions, state, and verify.
It asks whether the other layers, including the verify gate and its clean-state check, keep the agent
inside the allowed paths without the scope layer refusing anything.

## Results

[[PENDING: F3-canonical, runs failing the primary measure out of 10 per arm with run ids, components split, and the secondary measures per run | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation, all layers minus scope vs all layers, runs failing the S3 primary measure on F3-canonical (k=2) | source: M8 ablation | how: uv run shipharness report]]

## Questions to bring to the review session

- In a bare-arm run that failed, was the out-of-scope file needed for the feature, or was it a
  shortcut? Open the run's score record (`exports/scores/<run id>.json`: `out_of_scope_files`,
  `test_phase_source_edits`) and the arm's diff (`.shipharness/runs/<ab id>/<arm>/diff.patch`).
- Why did the pilot run 2 harness arms ship no tests in their 12-turn test phase? Read one harness
  arm's second session in the run log and count the turns spent before the first test file was opened.
- In a harness-arm run, how many `blocked` decisions came before the agent found the in-scope route,
  and how many turns did that cost? The run log holds every `blocked` event in order, between the
  `turn` events around it.
- Would an allowlist of commands (A5, F-a-87) have prevented any of the bare arm's out-of-scope
  edits? Which ones were made with `apply_patch`, and which with `run`?

## Why it matters for your own repo

- **Validate the measure before you trust the result.** The pilot's first F3 result said "both arms
  fail"; the cause was the harness's own measurement. Before you compare two setups, read a few raw
  runs (the diff and the files counted) and check that what the measure counts is what you meant.
- **Pair every "did no harm" measure with a "did the work" measure.** Out-of-scope files and
  test-phase edits are both met by an agent that does little. Add hidden tests, existing tests that
  keep passing, and mutants killed by the shipped tests, and read them together.
- **A canonical task may be too easy to show a difference.** When the plain ticket names the files,
  the agent may stay in scope with no help. A realistic temptation (a nearby shared file, a ticket
  that suggests a cross-cutting fix) is a fairer test of whether enforcement matters on your code.
- **Report no difference as a result.** If the gap does not appear, say so with the dots; this course
  fixed that rule before its last pilot run.
