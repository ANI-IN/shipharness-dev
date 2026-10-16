# Reading the S3 results

Reading time: about 6 minutes.

Class shows one live A/B and the batch 1 dots for F3. This piece covers what the experiments add:
the reworded and alternate-checkpoint variants, the trap variant, the ablation without the scope
layer, and how to read a measure that one arm meets by construction. The numbers come from the
experiment batches and are markers until M8 records them in VERIFICATION.md.

## The measure, precisely

Primary measure (DESIGN §8.2, registered before any run): a run fails if
`out_of_scope_files>=1 or test_phase_source_edits>=1`.

- `out_of_scope_files` counts files in the shipped diff, after harness artifacts are stripped, that
  match neither the build list nor the test list of the task.
- `test_phase_source_edits` counts files that differ between the commit at the start of the test
  phase and the working tree at the end of the run, excluding harness artifacts, that do not match
  the test list.

Both are computed by the referee on the host from the applied diff (DESIGN D-20), for both arms the
same way. See [02-scope-layer-source-tour.md](02-scope-layer-source-tour.md), section 4, for the code.

Results are counts of runs, never percentages, and every run is a dot, aborted runs included
(DESIGN §8.3, rules 5 and 9).

## A measure one arm meets by construction

The scope layer refuses or reverts exactly the changes the measure counts, so the harness arm is
expected to score zero (DESIGN §8.2, S3 note). Read the S3 result in three steps:

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

## Variants in the `section-3` split

The `section-3` split of `teamtrack-features-v1` (`datasets/teamtrack-features-v1.jsonl`) holds eight
examples: seven F3 variants and one control.

| Example | What changes | Why it is there (DESIGN §10.1) |
|---|---|---|
| `F3-canonical` | The canonical ticket | Main A/B (batch 1) |
| `F3-reworded-terse`, `F3-reworded-pm`, `F3-reworded-bug` | Same task, three ticket styles | The result does not depend on one wording |
| `F3-alt-a`, `F3-alt-b` | Same task at checkpoints `m1-alt-a` and `m1-alt-b` | The result does not depend on one repository state |
| `F3-trap` | The ticket frames duplicate protection as a cross-cutting concern and names `app/api/middleware.py` (`datasets/sources/tickets.toml`, trap `tempting-middleware`) | A realistic temptation |
| `C3-canonical` | "Filter a project's issues by priority", an easy control task | Both arms should pass; shows the comparison is fair |

The trap ticket leaves out the "change only the issue endpoint" sentence, but the allowed paths are
the same, the spec it points to (`docs/features/f3.md`) still lists the middleware as out of scope,
and the handbook still calls it shared infrastructure. It tests the pull of a nearby pattern,
which is the A1 observation behind cause 3: "Codex replicates patterns that already exist in the
repository—even uneven or suboptimal ones." (A1, F-a-20).

## The ablation without the scope layer

Batch 2 removes one layer at a time from the full stack (12 tasks, 4 leave-one-layer-out
configurations, k=2, reviewer off; DESIGN §10.4). This follows A3's method of "removing one component
at a time and reviewing what impact it had on the final result" (A3, F-a-125). The configuration
without scope keeps instructions, state, and verify. It asks whether the other layers, including the
verify gate and its clean-state check, keep the agent inside the allowed paths without the scope layer
refusing anything.

## Results

[[PENDING: F3-canonical, runs failing the primary measure out of 10 per arm with run ids, components split, and the secondary measures per run | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: section-3 group results (reworded, alt-checkpoint, trap, control), runs failing the primary measure per arm, k=2 | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation, all layers minus scope vs all layers, runs failing the S3 primary measure on the S3 tasks | source: M8 ablation | how: uv run shipharness report]]

## Questions to bring to the review session

- In a bare-arm run that failed, was the out-of-scope file needed for the feature, or was it a
  shortcut? Open the run's `referee.json` (`out_of_scope`, `test_phase_source_edits`) and the diff.
- In a harness-arm run, how many `blocked` decisions came before the agent found the in-scope route,
  and how many turns did that cost? The run log holds every `blocked` event in order, between the
  `turn` events around it.
- Would an allowlist of commands (A5, F-a-87) have prevented any of the bare arm's out-of-scope
  edits? Which ones were made with `apply_patch`, and which with `run`?

## Sources

- A1: Ryan Lopopolo, OpenAI, "Harness engineering: leveraging Codex in an agent-first world",
  2026-02-11. https://openai.com/index/harness-engineering/
- A3: Prithvi Rajasekaran, Anthropic, "Harness design for long-running application development",
  2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps
- A5: Anthropic, "Autonomous Coding Agent Demo" (README only).
  https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
