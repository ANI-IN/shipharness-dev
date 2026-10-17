# Changelog

All notable changes to this project are recorded here.

## Unreleased

### Release tag class-v1, no freeze (2026-10-17)
- No experiment freeze: the pilot gate did not pass, so the release carries no `harness-frozen` tag.
  The release build writes the public `harness-frozen` tag only when the build repository
  has a freeze record, and otherwise says so in its report.
- `class-v1` is the release tag: an annotated tag on the public commit whose message reads "Class
  version 1: the code, datasets, and settings used for the class. No experiment freeze; the pilot
  gate did not pass (see the course notes)." followed by a record of the content hashes, the
  checkpoint `platform/teamtrack/` trees, and the run settings.
- `shipharness verify --tag class-v1` compares a clone with that record and prints either "your
  copy matches class-v1" or one line per difference.

### Class profile, class plan, starter kit, slides (2026-10-17)
- `shipharness ab --profile standard|class`: the class profile (reasoning effort low, 2 CPUs per arm,
  referee, and preview container, OpenAI Fast tier for the agent arms) is identical for both arms and
  used by `make demo-N`, `make show-N`, `make final`, and `make warm` (`PROFILE ?= class`); pilot and
  experiment runs keep standard. The reviewer keeps its own settings and the Standard tier.
- Fast tier pricing: `platform/config/prices.toml` has a `.fast` table for gpt-6-luna (twice the Standard
  token rates); each call is charged by the tier its response reports, so a downgraded request costs
  the Standard rate; the worst case held before a call uses the requested tier, and the ledger
  records the reported tier.
- Early primary verdict: the referee runs the checks a task's primary measure needs first and emits
  `primary_verdict` per arm; the console shows "primary verdict ready" with the time from launch, and
  the secondary checks follow. Measurement change for both arms with no outcome change.
- Flakiness re-runs of shipped tests: 5 instead of 10 (TestGen-LLM's "five executions"); a
  secondary measurement change for both arms (`flaky_tests` from earlier records counts 10).
- Runner rule for both arms: before the last build session, `finish(claim="not_done")` ends only that
  session, and the next session starts as after a spent turn budget (pilot run 3 had harness arms end
  the build phase after a 12-turn first session).
- `shipharness ab --arms harness` and `make show-N`: the harness arm alone ("harness in action"),
  judged by the referee and left out of every bare-vs-harness comparison, screen 4, and swap tests;
  `make replay` replays such runs.

### Constructed examples (2026-10-17)
- `shipharness example --section demo-N` and `make example-1` .. `make example-4`, optional extras
  that are not part of any demo section ([docs/extras.md](extras.md)): the harness arm with
  section N's layer stack on its canonical task, in the real sandbox and judged by the real referee,
  driven by scripted steps that make the mistake the layer exists to catch (a cross-org query, a
  session that runs out of turns, an out-of-scope patch and a network command, a claim of done with
  a failing test). No model, no API key, $0. Every console screen shows CONSTRUCTED EXAMPLE; the run
  record and score are marked `constructed`, the score stays in the run directory, and the A/B
  report, screen 4, swap tests, and exports never count it.
- `testgen --layers verify` on a repository that is not TeamTrack: the visible-test directory comes
  from the run (`--tests` folder or `--visible-tests`), and the migration-head check runs only with
  an Alembic configuration (bug fix; TeamTrack runs unchanged).
- The verify gate's ruff check uses ruff's default rule set (`E4,E7,E9,F`) when the repository has no
  ruff configuration of its own (bug fix, harness arm only).
- `make warm`: images rebuilt only when their source changed, containers paged in, and the referee
  and gate baselines of the class tasks cached, with no model calls.
- `shipharness ab` exits 2 when an arm was aborted (cost cap or time limit); the run is still judged.
- Class plan: the pre-registered pilot gate did not pass (no measurable difference on this task with
  this model in any section), so S1 to S4 run harness in action (`make show-N`, live); the final
  keeps one live A/B; recorded showcases and constructed examples are optional extras outside the
  demo flow, and `make replay` is the emergency fallback; one slide and console screen 4 show every
  result. Screen 4 groups dots by feature and leaves out records of an older referee version.
- Starter kit: `use-in-your-repo/kit/` and `shipharness init --target <repo>` (and `--check`) copy TeamTrack's harness
  as templates with REPLACE markers, deterministically, with a worked example on three boltons
  modules and the guide `use-in-your-repo/apply-to-your-repo.md`.
- Feature steps: a dataset line without `steps` lets the state and scope layers take the ticket's
  bullet lines or its title (harness arm only).
- `make slides`: `platform/scripts/build_slides.py` validates `slides/deck.md` and writes HTML, PDF, and PPTX
  with speaker notes; `SLIDES_OPTS=--check` or `--strict`.
- Documentation: README, instructor guide and run sheet, troubleshooting, final project, and after
  class updated for the class plan, the pilot results, and the class-profile round.

### M6 pilot fixes (2026-10-16)
- Trace projects by purpose: class runs only in `shipharness-class-<date>` with an explicit class
  date; pilot runs in `shipharness-pilot`; assignments in `shipharness-assignments`.
- Cost caps hold across concurrent commands: trackers read each other's ledger entries.
- Total build budget: `MAX_BUILD_TOTAL_USD` $15 over every ledger entry, enforced before each call;
  the cost line shows build spent and remaining.
- `apply_patch` accepts the context-anchored `*** Begin Patch` format and unified diffs without line
  numbers or with wrong counts (most pilot patches failed under strict `git apply`).
- `.import_linter_cache` is a generated directory everywhere (diff, scope snapshots, clean state).
- S2 session patches and S3 test-phase files come from working-tree snapshots, so arms that never
  commit are measured correctly.
- Referee baseline runs in parallel with the arms and is cached per task.
- Harness overhead cuts (harness arm only): `init.sh` runs one end-to-end test file, the session
  start reuses the handoff's visible-test status, and the gate baseline is cached per checkpoint
  commit; budgets stay identical for both arms and primary measures never change (pilot rules).
- `shipharness.freeze`: the `harness-frozen` tag (only if the pilot gate passes) pins treatment,
  measurement, tasks (with checkpoint tag commits), and environment (with run settings by value);
  `platform/tests/unit/test_harness_freeze.py` fails on drift once the tag exists.
- Freeze rules 1 and 2: content hash per frozen path and checkpoint trees in the tag record
  (history-independent, for the public release); accepted changes need a recorded freeze exception
  with a re-run or a recorded check that the change cannot affect any score.

### M5 Features, datasets, checkpoints (2026-10-16)
- F1-F7 specs (both arms), reference patches, 392 hidden tests, feature mutants; C1-C8 control tasks
  with 49 hidden tests; `platform/teamtrack/reference/checkpoints.toml` and 8 checkpoint tags.
- `teamtrack-features-v1` (60: 7 canonical, 21 reworded, 8 alternate checkpoints, 9 session stops,
  7 traps, 8 controls) and `testgen-targets-v1` (40: 20 TeamTrack, 10 boltons, 10 WTForms), validated
  against the repository and uploaded to LangSmith.
- Mutants located by exact text and re-validated at every checkpoint; filter and referee sets
  checked to be disjoint across all files.
- Owner decisions: regression covers the checkpoint's existing tests only; agent-only run budget with
  `HARNESS_TIMEOUT_S`; F4 If-Match optional; export inspection tests; checkpoint SHA pinned in A/B
  records, score records, and experiment summaries; tags move only with owner approval once results exist.
- Runner, console, testgen: final cap reaches the loop; cost reservation; malformed run-log lines skipped;
  `--doctest-modules`; `testgen --target`; `make demo-N`, `swap-N` (latest of the section), `final`,
  `replay`; fast default suite and parallel `make test-all`.
- Class host on WSL2 with Docker Engine; real-container tests found and fixed the login-shell PATH
  bug and the preview start bug.

### M4 Harness layers and tooling (2026-10-16)
- Seven builders merged on `main`: checks R1-R7 plus regression, hidden tests, diff scope, flakiness,
  continuity, and board, with a container check runner and tenant app adapter; layers S1 instructions,
  S2 state and session lifecycle, S3 scope; S4 verify layer and gate; five test filters, targeted mutant
  runner, `shipharness testgen`, TeamTrack mutant sets; blinded reviewer, A/B runner, referee,
  experiments, report; five live console screens with board capture; four Agent Skills and
  `shipharness skills validate`.
- Integration: one module of check parameter names (`checks/params.py`) shared by the referee, the gate,
  and the checks, with a contract test; the verify test phase runs the real filter pipeline; referee
  mutants load by the task's mutant set (a missing set scores 0/0); one board preview container per arm
  when sandboxed; failing counts stay right when findings are capped.
- `logging.py` renamed `log_setup.py`; learner skill folder `use-in-your-repo/skills/skill-template` (a skill's
  `name` must equal its folder name and use only `a-z`, `0-9`, and hyphens, so `_template` cannot
  validate).
- TeamTrack: ids bounded to 64-bit, field validation in the issue service, catch-all error envelope,
  request logging off by default.
- Walkthrough anchors placed in the code as built.
- Final review fixes: harness commands keep their own time limits; gate exemptions match its
  baseline; the arm's build cannot replace the referee's runner, and results without the run's nonce
  are rejected; failing shipped tests
  never kill mutants; the arm cannot change test configuration or drop existing tests unnoticed; every
  referee path uses the task's mutant set; preview and referee container failures never lose a run; the
  board preview reloads the arm's code; diff paths with spaces; emptied test classes stay valid.

### M3 Core (2026-10-16)
- Package `shipharness` with pinned dependencies (uv) and CLI: `doctor`, `up`, `console`,
  `datasets validate|upload`.
- Config (`SecretStr` keys, `.env`), prices with cache-write pricing, log redaction of keys.
- CostTracker with run, review, batch, session, and experiment caps; append-only ledger
  `.shipharness/ledger.jsonl`.
- Typed events (24 types), JSONL run log, replay with `recorded=True`.
- Sandbox policy, Docker/Podman, local (UNSANDBOXED) and fake runtimes, denial detection, images.
- Tracing to LangSmith with input scrubbing; local exports.
- Runner: seven tools (six working tools plus `finish`) with path safety and output truncation; skills
  loader with progressive disclosure; agent loop with sessions, wrap-up, resume, caps, and API error
  handling.
- Harness layer hook interface and composition (`--layers` parsing).
- Check framework: OpenAPI endpoint discovery, baseline deltas, in-process probes.
- TeamTrack base: 25 operations, layered architecture with an import-linter contract, cursor
  pagination and error envelope, idempotent creates, audit log, Alembic migration, deterministic seed,
  legacy `/v1/issues` (documented do-not-copy), web board, team handbook, 142 visible tests.
- Console skeleton with server-sent events and `Last-Event-ID` resume.
- Makefile, GitHub Actions CI (lint, unit, sandbox, live on manual dispatch), prose lint, walkthrough
  anchors.
- Live streaming uses the browser `EventSource` API instead of `htmx-ext-sse`, whose repository
  states no license; the sandbox policy code lives in `platform/src/shipharness/sandbox/policy.py`.
- Final review fixes: the arm workspace is treated as untrusted (host git never reads the
  agent's `.git/config`; host tools never follow links out of the workspace; bytes-safe output);
  run and tool exception safety; key masking in tool output and run logs; narrower redaction; board
  validation in the service layer; discovery of unauthenticated endpoints; class date defaults to
  today (replaced in M6 by an explicit class date); trace link retried at run end. LangSmith tracing enabled explicitly (found by a live probe).

### M2 Design and contracts (2026-10-16)
- Course plan and module interfaces agreed; `.env.example`, `.gitignore`, secrets unit test,
  PRE-CLASS draft.

### M1 Research (2026-10-16)
- Source research: the teaching sources and findings the course cites, listed in
  [docs/REFERENCES.md](REFERENCES.md).
- Product renamed from the working name `shipproof` to `shipharness` after a name-clash check.
