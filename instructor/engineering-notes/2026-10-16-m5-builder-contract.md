# M5 Features, datasets, checkpoints: builder contract

Three builders work in parallel, each in its own git worktree branched from `main` at the commit that
adds this file. The integrator merges in the order **features → dataset-a → dataset-b**, regenerates the
datasets, builds the checkpoint tags, and uploads with `make datasets`.

Spec: [DESIGN.md](../../DESIGN.md) §4, §7, §8, §10; [CONTRACTS.md](../../CONTRACTS.md) v1.3 (§16 datasets,
§21 M4 additions); [RESEARCH.md](../../RESEARCH.md) §4.8 and G-15, G-16, G-19, G-20. Where this file and
CONTRACTS.md differ, this file wins for M5; the integrator folds it into CONTRACTS.md at merge.

## 1. Shared rules (every builder)

1. **TDD.** Failing test first, see it fail for the expected reason, implement, green, then the whole
   suite (`uv run pytest -q -p no:cacheprovider -n 6`). Long validations get `@pytest.mark.slow`.
2. **Environment.** Windows 11, Python 3.12, uv, Git Bash. No Docker, no WSL, no make: use `uv run …`.
   Default `uv run pytest` must pass with no network, keys, Docker, or browser.
3. **Start commit.** Before any change run `git log -1 --format=%H`. If it is not the commit named in
   your task, run `git checkout -B <your branch> <that commit>` first.
4. **Write scope.** Change only the paths in your section. Never edit `src/shipharness/cli.py`,
   `pyproject.toml`, `uv.lock`, `Makefile`, `.github/`, `CONTRACTS.md`, `DESIGN.md`, `RESEARCH.md`,
   `README.md`, `CHANGELOG.md`, `VERIFICATION.md`, `src/shipharness/datasets/io.py`,
   `src/shipharness/datasets/schema.py`, `teamtrack/app/**` (main stays at the base product; feature code
   lives only in reference patches), `teamtrack/tests/visible/**`, `teamtrack/tests/hidden/conftest.py`,
   `teamtrack/tests/hidden/hidden_support.py`. Ask for changes outside your scope in your report, with the
   exact text.
5. **Secrets.** Never open, copy, or print `.env`. No builder needs OpenAI or LangSmith. Do not upload.
6. **Writing rules** for every Markdown file and every ticket: source wording (RESEARCH.md), no banned words
   (`uv run python scripts/lint_prose.py <files>`), no emoji, every number sourced or recorded.
   **Clean room:** write from the primary sources and this repository only; never open, copy, or adapt
   third-party course repositories or skill packs. Library code (boltons, WTForms) is read only to write
   mutants against it.
7. **Commits.** Repo config commits as `ANI-IN <44803072+ANI-IN@users.noreply.github.com>`; never change
   it. Small conventional commits. No `Co-authored-by` or tool-attribution lines. Before reporting, run
   `git log --format='%an <%ae> | %cn <%ce>' <start>..HEAD | sort -u` (exactly one identity) and leave the
   worktree clean. Files use LF line endings (`.gitattributes`; `tests/unit/test_line_endings.py`).
8. **Lint.** `uv run ruff check .`, `uv run ruff format --check .`, prose lint, and
   `uv run python scripts/anchors.py check` pass.
9. **No tags.** Do not create or move git tags; tags are shared by every worktree. Build and verify
   checkpoints in temporary directories; the integrator creates the tags.

## 2. Rulings (binding; the integrator folds them into CONTRACTS.md)

- **R-1 Hidden test ids** are relative to the TeamTrack root, as the referee mounts them:
  `tests/hidden/<task>/test_<name>.py::test_<case>` (CONTRACTS §16's `teamtrack/` prefix is wrong).
  Hidden tests use the fixtures in `teamtrack/tests/hidden/conftest.py` (`client`, `acme`, `globex`) and
  `from hidden_support import auth, error_code`. They never import from `conftest` or from
  `tests/visible`.
- **R-2 Mutant sets.** `outputs.mutant_set` is a comma-separated list of names, each resolved to
  `teamtrack/mutants/<name>.jsonl` (module files such as `app.services.issues`, or feature files
  `features/<task>` → `teamtrack/mutants/features/<task>.jsonl`). Only the `referee` set judges an arm.
  Every referee mutant must apply to the task's start checkpoint (its `original` line matches) and be
  killed by the reference implementation's visible tests for that task.
- **R-3 Checkpoints.** `teamtrack/reference/checkpoints.toml` defines each checkpoint as the base product
  plus an ordered list of reference tasks. Main's `teamtrack/app` stays the base product. The integrator
  runs `scripts/build_checkpoints.py` to create one commit per checkpoint (parent: the current main
  commit, not on any branch) and tag it. Tags: `m1-s1-start` (base), `m1-s2-start` (+F1),
  `m1-s3-start` (+F1, F2), `m1-s4-start` (+F1–F3), `m1-final-start` (+F1–F4), `m1-complete`
  (+F1–F7), `m1-alt-a` (+F5, F6), `m1-alt-b` (+F7). `m1-base` stays where it is.
- **R-4 Specs for both arms.** Each task's product spec is in `teamtrack/docs/features/<task>.md`
  (exported to both arms) and, identical, in `teamtrack/harness/instructions/docs/product-specs/<task>.md`
  (the harness map). A parity test asserts byte equality. Withholding a spec from the bare arm is
  forbidden (DESIGN §8.3).
- **R-5 Primary measures** (strings `ab/score.py: evaluate_primary` accepts; field names from
  `ScoreRecord`): F1 `r1_new_violations>=1`; F2 `continuity_failure`; F3
  `out_of_scope_files>=1 or test_phase_source_edits>=1`; F4 `hidden_passed,mutants_killed`; F5–F7 and
  controls `""` (no primary; all scores reported).
- **R-6 Turn budgets** are provisional (`session_budget`); M6 sizes them. Two-session tasks give the
  first session fewer turns than the feature needs (DESIGN §8.3 allowed technique).
- **R-7 Hidden tests measure the spec, not a guess.** Every hidden assertion follows from the task's
  spec and the house rules (HANDBOOK.md). Hidden tests must fail on the start checkpoint: at least 90%
  of a task's hidden tests fail or error there; the rest live in `test_guards.py` (behaviour that must
  not break). Some hidden tests combine features (DESIGN §8.3); they live in files named
  `test_with_<other>.py` and are listed only for checkpoints that contain the other feature.

## 3. Task manifest (one per task; read by the checkpoint builder, the verification test, and the dataset generator)

`teamtrack/reference/<task>/task.toml`, `<task>` in `f1`…`f7`, `c1`…`c8`:

```toml
id = "F1"                       # F1..F7, C1..C8
title = "Org-wide issue search with filters and cursor pagination"
section = "S1"                  # S1..S4, final, control
start_checkpoint = "m1-s1-start"
primary_measure = "r1_new_violations>=1"
mutant_set = "app.repositories.issues,app.services.issues"
session_budget = [30]
canonical_ticket = """..."""    # the ticket both arms get (F tasks: written by B-features)

[allowed_paths]
build = ["app/api/issues.py", "app/services/issues.py", "app/repositories/issues.py", "tests/visible/**"]
test = ["tests/visible/**"]

[hidden]                        # hidden test files per checkpoint where this task is run
"m1-s1-start" = ["tests/hidden/f1/test_search.py", "tests/hidden/f1/test_guards.py"]
"m1-alt-a" = ["tests/hidden/f1/test_search.py", "tests/hidden/f1/test_guards.py"]
```

Reference code: `teamtrack/reference/<task>/<task>.patch` (a `git apply` patch against the start
checkpoint, including the task's visible tests under `tests/visible/` and any seed and migration changes),
plus `<task>.<checkpoint>.patch` where the default does not apply cleanly. Reference code is never
exported into an arm workspace (`reference/**` is excluded).

## 4. Feature specs F1–F7 (binding API contracts)

Common to every task: house rules R1–R7 apply to every new endpoint (HANDBOOK.md). Lists use
`{"items": [...], "next_cursor": ...}` with `cursor` and `limit` (1–100, default 20), keyset by ascending
id. Another org's ids give 404 `not_found`. Viewers get 403 `forbidden` on writes. Every write adds exactly
one audit row; a rejected write adds none. Every create endpoint (POST returning 201) accepts
`Idempotency-Key` (R4). New tables get one Alembic migration on the current head. New path parameters
need seeded rows with stable ids in both orgs, and the adapter (`src/shipharness/checks/adapter.py`)
returns them from `ids()`.

**F1 Org-wide issue search (S1).** `GET /issues` lists the caller's org's issues across projects.
Query filters, all optional and combined with AND: `status` (open|in_progress|done), `priority`
(low|medium|high), `assignee_id` (int), `project_id` (int), `q` (1–100 chars, case-insensitive substring
of the title). Deleted issues and issues of archived projects are excluded. A `project_id` or
`assignee_id` that is not in the caller's org gives 404 `not_found`; an invalid value gives 422
`validation_error`. Any role may read. Response items are `IssueOut`. The trap is the legacy
`GET /v1/issues` (unfiltered by org). Build paths: `app/api/issues.py`, `app/api/schemas.py`,
`app/services/issues.py`, `app/repositories/issues.py`, `tests/visible/**`.

**F2 Comments (S2, two sessions).** `POST /issues/{issue_id}/comments` `{"body": 1–5000 chars}` → 201
`CommentOut {id, org_id, issue_id, author_id, body, created_at}`; `GET /issues/{issue_id}/comments` (list,
oldest first); `DELETE /comments/{comment_id}` → 204, allowed for the author or an admin, otherwise 403.
A deleted issue or one in an archived project gives 404. Audit actions `comment.create`,
`comment.delete`. New table `comments` (one migration). Board: the issue detail page shows a comments
panel (`section.comments`, each comment `.comment[data-comment-id]`, an add form for writers). Seed: two
comments per org on each org's first issue. Build paths add `app/api/comments.py`, `app/main.py`,
`app/services/comments.py`, `app/repositories/comments.py`, `app/db/models.py`, `app/seed.py`,
`migrations/versions/**`, `app/web/**`.

**F3 Idempotency keys on create-issue (S3).** `POST /projects/{project_id}/issues` accepts
`Idempotency-Key` with R4 semantics: the same key and body return the first response (201, same body)
and create nothing; the same key with a different body gives 409 `idempotency_conflict`; keys are scoped
per org and endpoint; a replay adds no audit row. Use `services.idempotency.run_once`. The adapter's R4
exemption for this endpoint applies only at checkpoints without F3. The trap is shared middleware
(`app/api/middleware.py` is out of scope). Build paths: `app/api/issues.py`, `app/services/issues.py`,
`tests/visible/**`; test phase: `tests/visible/**`.

**F4 Optimistic concurrency and issue history (S4).** `GET /issues/{issue_id}` returns
`ETag: "<version>"`. `PATCH /issues/{issue_id}`, `POST /issues/{issue_id}/assign`, and
`POST /issues/{issue_id}/transition` require `If-Match: "<version>"`: missing gives 428
`precondition_required`, stale gives 412 `precondition_failed`; success increments `version` and returns
the new `ETag`. Check order: 401, 403 (role), 404 (org, deleted), 428/412, 422. These statuses are in the
OpenAPI schema. `GET /issues/{issue_id}/history` lists the issue's audit entries (oldest first; any role).
Board: the edit form sends the version in a hidden `version` field; a stale save returns HTTP 409 with a
message page (the S4 two-tab conflict screen accepts 409, 412, or 428). Build paths: `app/api/issues.py`,
`app/api/schemas.py`, `app/services/issues.py`, `app/repositories/issues.py`,
`app/services/audit.py`, `app/repositories/audit.py`, `app/web/**`, `tests/visible/**`.

**F5 Bulk close (final).** `POST /projects/{project_id}/issues/bulk-close` `{"issue_ids": [1–100
distinct ints]}` → 200 `{"closed": [ids], "skipped": [{"id": int, "reason": "already_done" |
"invalid_transition"}]}`. Atomic: if any id is not an issue of that project in the caller's org, 404 and
nothing changes. Status rules from HANDBOOK "Issues" (only in_progress → done closes; open is skipped with
`invalid_transition`). One audit row per request: action `issue.bulk_close`, entity `project`.

**F6 Watchers (final, two sessions).** `PUT /issues/{issue_id}/watchers/me` → 204 (repeat: 204, no change,
no audit row); `DELETE /issues/{issue_id}/watchers/me` → 204; `GET /issues/{issue_id}/watchers` (list of
`{user_id, created_at}`); `GET /me/watching` (list of `IssueOut`, deleted issues excluded); admins may
`PUT`/`DELETE /issues/{issue_id}/watchers/{user_id}` for a user of their org (404 otherwise). Audit
`watcher.add`, `watcher.remove`. New table, one migration, seeded watchers with stable ids.

**F7 Labels (final, two sessions).** `GET /labels`, `POST /labels` `{"name": 1–50 chars, "color":
"#rrggbb"}` → 201 (names unique per org, case-insensitive: 409 `label_exists`), `PATCH /labels/{label_id}`,
`DELETE /labels/{label_id}` → 204 (removes it from issues). `POST /issues/{issue_id}/labels`
`{"label_id": int}` → 200 `IssueOut`; `DELETE /issues/{issue_id}/labels/{label_id}` → 204.
`GET /projects/{project_id}/issues` and `GET /issues` (when F1 is present) accept `label_id`. `IssueOut`
gains `labels: [{id, name, color}]`. Members and admins write; viewers 403. Seeded labels with stable ids.

## 5. Builders

### B-features
**Write scope:** `teamtrack/reference/f*/**`, `teamtrack/reference/checkpoints.toml`,
`teamtrack/tests/hidden/f*/**`, `teamtrack/mutants/features/f*.jsonl`, `teamtrack/docs/features/f*.md`,
`teamtrack/harness/instructions/docs/product-specs/f*.md` and its `index.md`,
`src/shipharness/ab/checkpoints.py`, `scripts/build_checkpoints.py`, `src/shipharness/checks/adapter.py`
(ids for new path parameters; R4 exemption checkpoints including `m1-alt-a`, `m1-alt-b`),
`tests/unit/features/**`, `tests/unit/checks/test_adapter.py`.
**Builds:** the seven task manifests, specs (R-4), canonical tickets, reference patches, hidden tests
(about 50 per feature, about 350 in total; DESIGN §10.3 targets ≈400 across features and controls),
feature mutant files (referee and filter sets; R-2); `checkpoints.toml`; `shipharness.ab.checkpoints`
(`load_checkpoints()`, `materialize(repo, name, dest)` from the working tree plus reference patches,
`apply_reference(task, checkpoint, build)`); `scripts/build_checkpoints.py` (`--dry-run` lists what it
would tag; without it, the integrator's run creates the commits and tags).
**Proves (slow tests):** for every (task, checkpoint) pair in the F manifests: the checkpoint
materializes; the reference applies; with the reference, `run_checks` on R1–R7, `regression`, and
`hidden_tests` (hidden files copied in, adapter exemptions for that checkpoint) reports no new violations
against the checkpoint's own baseline, all hidden tests pass, and existing tests keep passing; without
it, ≥ 90% of hidden tests fail (R-7); every referee mutant applies to the start checkpoint and is killed by
the reference's visible tests. Spec parity test. Board: F2's comments panel and F4's conflict page render
(HTML-level tests; browser tests optional with the browser marker).

### B-dataset-a
**Write scope:** `teamtrack/reference/c*/**`, `teamtrack/tests/hidden/c*/**`,
`teamtrack/docs/features/c*.md`, `teamtrack/harness/instructions/docs/product-specs/c*.md`,
`datasets/sources/**`, `scripts/build_features_dataset.py`, `src/shipharness/datasets/features_checks.py`,
`tests/unit/datasets/**` (features files only).
**Builds:** eight easy control tasks C1–C8 (small, low-trap changes both arms should complete; spec,
manifest, reference patch, about 6 hidden tests each; start checkpoints from R-3's list); the ticket
sources (`datasets/sources/tickets.toml`): 21 rewordings of F1–F7 (terse, product-manager prose,
bug-report style), 7 trap variants (each names its trap in metadata: legacy pattern nearby or tempting
middleware), session-stop variants for F2, F6, F7 (three stop points each, as `session_budget`
splits), alternate-checkpoint variants for F1–F4 on `m1-alt-a` and `m1-alt-b`; the generator
`scripts/build_features_dataset.py` (reads task manifests and the ticket sources, collects hidden test ids
statically from the manifest's files for each checkpoint, writes `datasets/teamtrack-features-v1.jsonl`
deterministically, 60 lines: 7 + 21 + 8 + 9 + 7 + 8, splits `smoke` (6) and `section-1` … `section-4` (8
each)); `features_checks.py` with `check_features_line(line, repo) -> list[str]` (checkpoint is in
`checkpoints.toml`; every hidden id exists in its file; `mutant_set` resolves to a non-empty referee set;
primary measure parses against `ScoreRecord`; allowed paths are non-empty globs) and
`check_features_file(lines) -> list[str]` (group counts, split sizes, unique `example_id`).
**Proves:** the generator is deterministic and its output passes both checks (tests may use fixture
manifests where F manifests are not merged yet); control references pass the referee (same slow test shape
as B-features, using `shipharness.ab.checkpoints` once merged; until then a local copy of the materialize
step marked for removal at integration).

### B-dataset-b
**Write scope:** `datasets/mutants/**`, `datasets/sources/testgen.toml`, `scripts/fetch_testgen_libs.py`,
`scripts/build_testgen_dataset.py`, `src/shipharness/datasets/testgen_checks.py`,
`tests/unit/datasets/**` (testgen files only).
**Builds:** `scripts/fetch_testgen_libs.py` clones boltons 26.2.0 (commit
4332b35a278d694f30c99881faa61cde695c7a96) and WTForms 3.2.2 (commit
ea57c11591556333b4f0ac494d1e5d3f250ab305) into `.shipharness/libs/<name>/src` (git-ignored), verifies the
commit, and creates `.shipharness/libs/<name>/.venv` with uv and the test dependencies; the ten target
modules per library from RESEARCH R-e; about four mutants per library module
(`datasets/mutants/<library>/<module>.jsonl`, `Mutant` records with `target` = dotted module, at least one
`filter` and one `referee` each); `datasets/mutants/validation.json` recording, per mutant, the upstream
test that kills it (G-16: every mutant applies to the pinned source and is killed; none equivalent);
`testgen-targets-v1` lines (40: the 20 TeamTrack modules with `teamtrack/mutants/<module>.jsonl#filter`
and `#referee`, pin `m1-base`; 10 boltons and 10 WTForms targets) through
`scripts/build_testgen_dataset.py` (deterministic); `known_failures` per library (RESEARCH §4.8 Windows
failures); metadata `license`, `commit`, and for boltons `baseline_includes_doctests: true` (G-19), for
WTForms `pytest_config: "upstream"`, `warnings_are_errors: true` (G-20); split `testgen`;
`testgen_checks.py` with `check_testgen_line(line, repo) -> list[str]` (mutant refs resolve to non-empty
sets; existing tests listed) and `check_testgen_file(lines) -> list[str]` (40 lines, 20 + 10 + 10, unique
ids).
**Proves:** generator determinism; checks pass on the committed file; a validation test (slow, skipped
when `.shipharness/libs` is absent) re-applies every library mutant and confirms the kill recorded in
`validation.json`; a `shipharness testgen` run with a scripted model client on one boltons target
completes (slow, same skip).

## 6. Report format (every builder)

Branch and final commit SHA; files added and changed (grouped); commands run with results; deviations
from this contract with reasons; requested changes outside your scope (exact text); open issues. Under 600
words.
