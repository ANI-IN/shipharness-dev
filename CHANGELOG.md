# Changelog

All notable changes to this project are recorded here.

## Unreleased

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
  legacy `/v1/issues` (documented do-not-copy), web board, team handbook, 139 visible tests.
- Console skeleton with server-sent events and `Last-Event-ID` resume.
- Makefile, GitHub Actions CI (lint, unit, sandbox, live on manual dispatch), prose lint, walkthrough
  anchors.
- CONTRACTS 1.2: ledger file name, runner fields, sandbox and tracer signatures as built.
- DESIGN D-15 (no `htmx-ext-sse`: its repository states no license) and D-16 (policy code location).

### M2 Design and contracts (2026-10-16)
- DESIGN.md and CONTRACTS.md 1.1, approved by the owner with changes.
- `.env.example`, `.gitignore`, secrets unit test, PRE-CLASS draft.

### M1 Research (2026-10-16)
- RESEARCH.md and per-stream notes in `research/notes/`.
- Product renamed from the working name `shipproof` to `shipharness` after a name-clash check.
