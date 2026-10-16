# Changelog

All notable changes to this project are recorded here.

## Unreleased

### M6 pilot fixes (2026-10-16)
- Total build budget: `MAX_BUILD_TOTAL_USD` $15 over every ledger entry, enforced before each call;
  the cost line shows build spent and remaining.
- `apply_patch` accepts the context-anchored `*** Begin Patch` format and unified diffs without line
  numbers or with wrong counts (most pilot patches failed under strict `git apply`); CONTRACTS §23.
- `.import_linter_cache` is a generated directory everywhere (diff, scope snapshots, clean state).
- S2 session patches and S3 test-phase files come from working-tree snapshots, so arms that never
  commit are measured correctly.
- Referee baseline runs in parallel with the arms and is cached per task.
- Harness overhead cuts (harness arm only): `init.sh` runs one end-to-end test file, the session
  start reuses the handoff's visible-test status, and the gate baseline is cached per checkpoint
  commit. Pilot rules and the `harness-frozen` rule recorded in DESIGN §10.4.
- `shipharness.freeze` and `scripts/freeze_harness.py`: the `harness-frozen` tag pins treatment,
  measurement, tasks (with checkpoint tag commits), and environment (with run settings by value);
  `tests/unit/test_harness_freeze.py` fails on drift once the tag exists.
- Freeze rules 1 and 2: content hash per frozen path and checkpoint trees in the tag record
  (history-independent, for the public release); accepted changes need a `FREEZE-EXCEPTIONS.toml`
  entry with a re-run or a VERIFICATION no-score-effect check.

### M5 Features, datasets, checkpoints (2026-10-16)
- F1-F7 specs (both arms), reference patches, 392 hidden tests, feature mutants; C1-C8 control tasks
  with 49 hidden tests; `teamtrack/reference/checkpoints.toml` and 8 checkpoint tags (D-23).
- `teamtrack-features-v1` (60: 7 canonical, 21 reworded, 8 alternate checkpoints, 9 session stops,
  7 traps, 8 controls) and `testgen-targets-v1` (40: 20 TeamTrack, 10 boltons, 10 WTForms), validated
  against the repository and uploaded to LangSmith.
- Mutants located by exact text and re-validated at every checkpoint; filter and referee sets disjoint
  across all files (D-4 check).
- Owner decisions: regression covers the checkpoint's existing tests only; agent-only run budget with
  `HARNESS_TIMEOUT_S`; F4 If-Match optional; export inspection tests; checkpoint SHA pinned in A/B
  records, score records, and experiment summaries; tags move only with owner approval once results exist.
- Runner, console, testgen: final cap reaches the loop; cost reservation; malformed run-log lines skipped;
  `--doctest-modules`; `testgen --target`; `make demo-N`, `swap-N` (latest of the section), `final`,
  `replay`; fast default suite and parallel `make test-all`.
- Class host on WSL2 with Docker Engine (D-22); real-container tests found and fixed the login-shell PATH
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
- `logging.py` renamed `log_setup.py`; engineering notes moved to `instructor/engineering-notes/`;
  learner skill folder `skills/skill-template` (DESIGN D-17).
- TeamTrack: ids bounded to 64-bit, field validation in the issue service, catch-all error envelope,
  request logging off by default.
- CONTRACTS 1.3 (§21 M4 additions); DESIGN D-17 to D-21 and walkthrough anchors as built.
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
- CONTRACTS 1.2: ledger file name, runner fields, sandbox and tracer signatures as built.
- DESIGN D-15 (no `htmx-ext-sse`: its repository states no license) and D-16 (policy code location).
- Final review fixes: the arm workspace is treated as untrusted (host git never reads the
  agent's `.git/config`; host tools never follow links out of the workspace; bytes-safe output);
  run and tool exception safety; key masking in tool output and run logs; narrower redaction; board
  validation in the service layer; discovery of unauthenticated endpoints; class date defaults to
  today; trace link retried at run end. LangSmith tracing enabled explicitly (found by a live probe).

### M2 Design and contracts (2026-10-16)
- DESIGN.md and CONTRACTS.md 1.1, approved by the owner with changes.
- `.env.example`, `.gitignore`, secrets unit test, PRE-CLASS draft.

### M1 Research (2026-10-16)
- RESEARCH.md and per-stream notes in `research/notes/`.
- Product renamed from the working name `shipproof` to `shipharness` after a name-clash check.
