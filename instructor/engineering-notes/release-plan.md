# Release plan: public course repository

Private note (never published: `instructor/` is excluded from the release). Owner of the release
step: the course owner. Tooling: `scripts/make_release.py` (build and dry run) and
`scripts/publish_solutions.py` (refuses: solutions are never published).

## Target

`ANI-IN/harness-engineering-session`, deleted and recreated empty and public by the owner at
release. It receives one fresh commit on `main`, the rebuilt checkpoint tags, and the
`harness-frozen` content record tag. No other branches, no old history.

## Steps

1. Backup (done): a git bundle of the old repository and its metadata are in `~/backups/`
   (WSL) and `C:\Users\Lenovo\Documents\backups\` (`harness-engineering-session-v1.bundle`,
   its `.sha256`, and `harness-engineering-session-meta`).
2. Dry run, and the owner reviews its report:
   `uv run python scripts/make_release.py --dry-run` (report in
   `/tmp/shipharness-release-report.txt`, file list in `/tmp/shipharness-release-files.txt`).
3. After the owner approves the dry run and says a final yes:
   1. `uv run python scripts/make_release.py --build <empty folder>`; it refuses on any leak,
      broken reference, unresolved finding id, frozen path that differs, or checkpoint whose
      `teamtrack/` tree differs from the build repository's tag, and then runs the fast suite.
   2. Delete `ANI-IN/harness-engineering-session` on GitHub and recreate it empty and public.
   3. Run the push commands that the build prints (section 7 of the report):
      `git remote add origin https://github.com/ANI-IN/harness-engineering-session.git`,
      `git push origin main`, then one `git push origin` with every checkpoint tag and
      `refs/tags/harness-frozen`.
4. Verify from a fresh clone of the public repository: `make setup`, `make doctor` (ends with
   `result: + ready`), `make demo-1` (a live A/B, needs the two API keys), and the README renders
   on GitHub.

The tooling never pushes, never calls GitHub, and creates tags only in the new repository.

## Allow-list (owner structure)

Public, verbatim from the owner, as encoded in `scripts/make_release.py`:

- Root: `README.md`, `LICENSE`, `CHANGELOG.md`, `REFERENCES.md` (generated), `Makefile`,
  `pyproject.toml`, `uv.lock`, `.python-version`, `.env.example`, `.gitignore`,
  `.gitattributes`, `.dockerignore`, `.github/workflows/`.
- `docs/`: `setup-macos.md`, `setup-windows.md`, `setup-linux.md`, `instructor-guide.md`,
  `troubleshooting.md`, `architecture.md`, `after-class.md` (only these seven).
- `submodules/01` to `04`: `concepts.md`, `demo/`, `assignment/starter/`,
  `post-class-reading/`, `session-notes.md`, plus the interpretations below.
- `final-project/`, `slides/` (`.md`, `.pdf`, `.pptx` files only), `skills/`, `src/`,
  `teamtrack/` (including `reference/`, the referee's hidden tests, and the mutants),
  `datasets/`, `sandbox/`, `config/`, `tests/`.
- Learner scripts: `scripts/anchors.py` (`make lint`, `make anchors`, CI, submodule docs),
  `scripts/lint_prose.py` (`make lint-prose`, CI, README), `scripts/fetch_testgen_libs.py`
  (assignment 4 README), `scripts/grade_assignment.py` (`make grade-assignment-N`).

Private only: `RESEARCH.md`, `DESIGN.md`, `CONTRACTS.md`, `VERIFICATION.md`, `CODEOWNERS`,
`FREEZE-EXCEPTIONS.toml`, `research/`, `instructor/`, every `solution/` folder and grader test,
internal scripts (every other `scripts/` file), and the pilot and experiment exports
(`exports/`, `.shipharness/`). Anything else is left out as not allow-listed (tonight:
`.vale.ini`, `.vale/`, `setup/PRE-CLASS.md`).

Tests under `tests/` that read or run an excluded file are left out too (tonight 11, for example
`tests/unit/test_pilot.py` and `tests/unit/test_grade_assignment.py`).

## Interpretations

- A learner needs the whole `assignment/` folder, not only `starter/`: `README.md`, `check.py`
  and the files it imports, `starter/`, the visible tests, fixtures, and the live-step helpers
  the assignment README runs (`live_evidence.py`, `ab_summary.py`, `live/run_live.py`,
  `live.py`). Anything under `solution/`, `grader/`, or `hidden/` stays out.
- Each submodule's `README.md` (its folder index) is public; it is not in the owner's list.
- `instructor/` is excluded entirely; the public instructor guide is `docs/instructor-guide.md`.
- `docs/` files and `session-notes.md` may not exist yet: the dry run lists them as missing and
  does not fail on them.
- `grade-assignment-N`: `scripts/grade_assignment.py` stays public, and the Makefile stays the
  same file in both repositories. In the public repository it prints "no grader for assignment
  N: graders are private (build repository only)".
- `setup/PRE-CLASS.md` and the Vale configuration are not in the owner's list and are left out.
- The public `harness-frozen` record carries the public repository's own checkpoint trees, after
  the dry run has checked that every checkpoint's `teamtrack/` tree equals the build
  repository's. Whole-tree ids cannot match, because the build tree also holds the private files.

## Dry-run checks

1. Public files: counts per top-level folder, the full list in a file, and owner-listed files
   that do not exist yet.
2. Leak check over the commit and every checkpoint tag: any private file fails.
3. Broken references: markdown links to any excluded file, `DESIGN §`, `CONTRACTS §`,
   `RESEARCH §`, `VERIFICATION`, paths under `instructor/` and `research/`, `solution/` and
   grader paths, internal scripts. Reported in the dry run; `--build` fails on any.
4. `REFERENCES.md`, generated from `RESEARCH.md` and `research/notes/`: the sources and findings
   the public files cite.
5. Checkpoint tags rebuilt in the temporary repository with `build_commits` (the logic of
   `scripts/build_checkpoints.py`), compared per tag with the build repository's tag: whole
   tree, `teamtrack/` tree, and the public files that differ.
6. Frozen content (`shipharness.freeze`): against `expected_record` when the build repository
   has `harness-frozen`, else against a record made from the build repository's HEAD. Every
   frozen path must match; the record is written as the temporary repository's own tag.
7. Target and the exact push commands, printed, never run.

## Dry run of 2026-10-17 (rel-tools after merging main e7287f4)

- 728 public files; no leaks; 11 owner-listed files missing (the seven `docs/` files and four
  `session-notes.md`).
- 672 broken references in 147 files (511 section citations, mostly `DESIGN §`); 75 of them
  are inside frozen paths.
- `REFERENCES.md`: 32 sources, 177 findings, no unresolved finding ids.
- Checkpoints: all eight rebuilt tags match the build repository's `teamtrack/` tree; 163
  other public files differ, because the build repository's tags were made from an older main.
  `m1-base` is not in `checkpoints.toml` and is not rebuilt.
- Frozen content: no `harness-frozen` tag yet; all 27 frozen paths match a record made from HEAD.

## Open decisions

- Broken references inside frozen paths (code docstrings, datasets, `teamtrack/reference`):
  fix them before the freeze, or record each fix as a no-score-effect exception after it.
- `m1-base`: tag it in the public repository, or leave it out (it is used as a label only).
- `freeze.compare_content` compares whole-tree checkpoint ids; comparing the `teamtrack/`
  subtree would make the record portable between the two repositories.
