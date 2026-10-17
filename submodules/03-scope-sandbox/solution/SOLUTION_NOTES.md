# A3 solution notes

Reference solution for assignment A3 (`../assignment/README.md`). Code: `a3scope/`; denial test:
`tests/test_a3_sandbox_rule.py`; grader: `grader/grade.py`; hidden cases: `grader/hidden/`.

## Approach

**Part A1, diff parsing (`a3scope/diffparse.py`).** One pass over the lines, split on `\n` (not
`str.splitlines()`, which also splits on form feeds and other separators that can sit inside content).
Two section shapes:

- git sections run from one `diff --git` line to the next. Inside, the parser records `rename from/to`,
  `copy from/to`, `---`/`+++`, `new file mode`, `deleted file mode`, `Binary files`, and
  `GIT binary patch`, and skips every hunk by its line counts. Paths come from the most specific source
  available: rename or copy lines, then `---`/`+++`, then the header. The header is the only source for
  header-only sections (empty new file, mode change), so it is parsed carefully: quoted tokens are
  unquoted, and an unquoted `a/X b/X` is split where both halves are equal (as
  `src/shipharness/ab/artifacts.py` does), falling back to the only ` b/` when there is one.
- plain sections start at a `---` line followed by a `+++` line outside a hunk. Prefixes are stripped
  only when both sides use them (or one side is `/dev/null`), the rule `git apply` follows for `-p1`
  versus `-p0` in `src/shipharness/runner/tools.py`.

Hunk counting is what makes `--- note` inside a hunk content rather than a header; the hidden cases
`good-header-like-lines-in-hunk` (git output) and `good-hand-written-header-like-lines` (no git header)
test it.

**Part A2, scope (`a3scope/scope.py`).** `glob_matches` is the regex translation from
`src/shipharness/harness/scope/guard.py` (`**/` becomes `(?:.*/)?`, `*` becomes `[^/]*`). `check_diff`
walks every path named by the diff in order. Escape detection runs on every name, copy sources
included, because a patch that reads `../../home/agent/.netrc` leaks a file even though it changes
nothing in the workspace. The remaining rules run on changed paths only, in the order of the README
table: harness-only files, state files, a phase without a list, the phase's globs, then the refusal code
(`test_phase_source_edit` in the test phase). A parse failure becomes one `unparseable` refusal: the
policy fails closed.

**Part B, status (`a3scope/status.py`).** The real `update_status` without the layer context. The
order matters for cost: the "none" checks (already set, wrong phase, no done claim for this phase) come
first, so a session without a claim runs nothing. With the verify layer on, the gate is the evidence
and nothing is re-run; the gate counts only if `passed is True` and its items agree (no `fail` or
`pending` item, a `visible tests` item with `pass` and `x/x`, `x > 0`). With the layer off, the visible
tests run once and the last pytest summary line decides. The document is deep-copied twice: once for
the unchanged result and once for the update, so the caller's object never changes.

**Part C, the history rule (`a3scope/policy.py`).** Nine patterns share one message and the reason code
`write_outside_workspace`. Every pattern starts at a command position: the start of the command or after
`;`, `&`, `|`, `(`, a backquote, `$(`, or a newline, then optional `VAR=value` words, `sudo`, and a path
to the binary. That one prefix is what keeps `grep -rn "git rebase" docs/` and
`python -c "print('git reset --hard')"` running while `cd /work && git rebase main` is refused. Git
global options before the subcommand (`-c k=v`, `-C dir`, `--no-pager`) are matched explicitly. Each
pattern then stays inside one simple command (`[^;&|\n]*`), so `git status; git log` cannot borrow a flag
from a neighbour.

## Design choices

- **Interfaces mirror the real code** (`PathRules`/`check_paths`, `update_status`, `DenyRule`,
  `check_command`, `DockerSandbox.exec`), so the class code and the assignment read the same way, but the
  learner's package stands alone: grading needs no keys, no Docker, and no layer context.
- **A phase with no allow list allows the path**, as `PathRules(allowed=None)` does in `guard.py` (the
  scope layer notes "no allowed paths given" in that case). Failing closed there would be stricter; the
  assignment keeps the real behaviour so learners do not learn two rules.
- **Copy sources are read, not changed.** The real guard's `patch_targets` refuses copy sources too,
  which is conservative for `apply_patch`; the assignment separates "named" (escape check) from
  "changed" (scope check) to make the learner think about what a diff does to each path.
- **The rule's reason code** is `write_outside_workspace`, the closest of the six fixed codes in
  `src/shipharness/sandbox/base.py`. A production change would add a dedicated code; the assignment does
  not, so the learner's rule runs unchanged in `DockerSandbox` (the optional container test does this).
- **Scoring multiplies both sides** of criteria 2 to 4 (bad × good, set × kept, denied × allowed), so a
  reject-everything or allow-everything implementation earns nothing there. The brief's zero-tolerance
  goals (all bad diffs rejected, zero false positives) are printed separately and are part of PASS.
- **Mutation check for the denial test.** "A test that proves the denial" is checked by running the
  learner's test with the rule removed (`assignment/visible_tests/plugins/a3_rule_removed.py`): a test
  that still passes proves nothing about the rule.
- **Hidden diffs are real git output.** `grader/hidden/make_hidden.py` builds each case from file
  operations on a small TeamTrack-shaped tree and records `git diff --cached` (with `-M`, and
  `--find-copies-harder` or `--binary` where a case needs it). Hand-written cases are the patches an
  agent can pass to `apply_patch` directly. A slow test regenerates them and compares bytes.

## Alternatives considered

- **Use `git apply --numstat` or `--summary` to list paths.** Exact for what git will do, but it needs a
  repository and the pre-image, hides the parsing problem the assignment teaches, and cannot run on a
  diff that does not apply. Kept as a production option: run both and refuse on disagreement.
- **A shell parser (`shlex`, `bashlex`) for the history rule.** Splitting the command into words
  removes the quoting problem, but the real policy is `DenyRule(pattern=...)` and `check_command` uses
  `re.search`. A word-level check would mean changing `src/shipharness/sandbox/policy.py`; the
  assignment keeps the real mechanism and accepts its limits (below).
- **A different rule.** Candidates were more network refusals (`uvx`, `uv run --with`, `pip download`,
  `npx`), which only make an existing denial faster, and refusing writes outside `/work`, which the
  read-only root already enforces. The history rule closes a gap that nothing else covers: the
  snapshot guard skips `.git`.
- **Strict copy handling** (refuse copy sources outside the list). Simpler, but a false positive on a
  legitimate test-phase fixture copied from application code.

## Trade-offs

- The parser trusts hunk counts. A hand-written patch with wrong counts may make the parser read the
  next file header as content (or the reverse); `git apply` would reject such a patch, so the
  disagreement is safe in the real tool chain, but `check_diff` alone could accept it.
- Status parsing reads the last pytest summary line. A test that prints a fake summary as its last line
  of output, followed by no real summary (pytest crashed), could pass the parser; the exit-code check
  (must be 0) and the failed/error counts still apply.
- The history rule refuses `git reset --hard` with no revision, which only discards uncommitted work.
  That is stricter than "history rewrite"; the message points to `git checkout -- <path>` and
  `git restore`, which A2's revert use case (A2, F-a-57) still allows.

## Known limits

The history rule is a regex on the command text, so it is a guard rail, not a boundary:

- Git accepts unambiguous abbreviations of long options: `git commit --amen` and `git reset --har` are
  not refused.
- Aliases and indirection: `git -c alias.r=reset r --hard`, `sh -c "$(printf 'git reset --hard')"`,
  `find . -name .git -exec rm -rf {} +`, `python -c "import shutil; shutil.rmtree('.git')"`.
- A branch name as a reset target (`git reset main`) is allowed; telling it from a file name needs the
  repository.
- `[^;&|\n]*` stops at a `;` or `|` inside a quoted argument, so `git commit -m "a; b" --amend` is not
  refused.

A boundary would need the harness to own history: keep the evidence commit in a ref the agent cannot
write (a second repository, or a read-only bind mount of a bare copy), or record the evidence by tree
hash as well as commit SHA. Those are Module 2 sandbox topics (DESIGN §9).

The diff parser reads unified and git diffs only: no context diffs (`***`), no `--no-prefix` edge cases
beyond equal halves, and no file names containing a newline outside git's quoting.

## Hidden cases (revealed at the Thursday review, brief §5.3)

Diff cases (`grader/hidden/cases.json`, `diffs/<id>.diff`). Policy: the F3 allowed paths (build:
`app/api/issues.py`, `app/services/issues.py`, `docs/HANDBOOK.md`, `tests/visible/**`; test:
`tests/visible/**`) and the state layer on, unless the case says otherwise.

| Out-of-scope case (26) | Phase | What it hides | Expected refusal |
|---|---|---|---|
| bad-third-file-out-of-scope | build | third file of three, the first two allowed | `app/services/idempotency.py` outside |
| bad-rename-into-scope-deletes-source | build | rename from out of scope into scope | `app/core/config.py` outside |
| bad-space-path-out-of-scope | build | name with spaces (git tab padding) | `docs/design notes/f3 retry.md` outside |
| bad-rename-to-space-path | build | rename to a name with a space | `docs/HANDBOOK old.md` outside |
| bad-traversal-inside-allowed-glob | test | `tests/visible/../../app/services/issues.py` | path_escape |
| bad-absolute-path | build | `+++ /etc/cron.d/agent`, no prefixes | path_escape |
| bad-copy-source-escapes | test | copy from `../../home/agent/.netrc` | path_escape (source) |
| bad-dot-slash-feature-list | build | `./feature_list.json`, hand-written | harness_only |
| bad-schema-edit-under-wide-allow-list | build, allow `**` | schema file under a match-all list | harness_only |
| bad-feature-list-renamed-away | build | rename of the feature list | harness_only + outside |
| bad-progress-without-state-layer | build, state off | `progress.md` | outside |
| bad-instruction-artifacts | build | `AGENTS.md`, `.agents/skills/...` | outside (both) |
| bad-binary-new-with-space | build | new binary file, name with a space | outside |
| bad-git-binary-patch | build | `GIT binary patch` section | outside |
| bad-test-phase-conftest | test | `tests/conftest.py` (not under `tests/visible`) | test_phase_source_edit |
| bad-test-phase-handbook | test | allowed in build, not in test | test_phase_source_edit |
| bad-hand-written-second-file | build | second file in a patch with no git header | outside |
| bad-mode-change-only | build | header-only section (mode change) | outside |
| bad-delete-migration | build | deletion | outside |
| bad-copy-to-out-of-scope | build | copy destination out of scope | outside |
| bad-quoted-non-ascii-path | build | `"a/docs/caf\303\251.md"` | outside |
| bad-hunks-without-file-header | build | hunks only | unparseable |
| bad-glob-prefix-boundary | test | `tests/visible_extra/test_a.py` | test_phase_source_edit |
| bad-exact-pattern-suffix | build | `app/api/issues.py.orig` | outside |
| bad-empty-new-file-header-only | build | empty new file (no `---`/`+++`) | outside |
| bad-crafted-header-only-rename | build | header with different halves, mode change only | outside (or unparseable) |

| Legitimate case (17) | Phase | What could cause a false positive |
|---|---|---|
| good-header-like-lines-in-hunk | build | `--- R4 ...` and `+++ R4 ...` content lines (git output) |
| good-hand-written-header-like-lines | build | the same, no git header, counts with omitted lengths |
| good-diff-u-timestamps | build | `diff -u` names followed by a tab and a timestamp |
| good-exec-plan-moves-to-completed | build | rename inside `docs/exec-plans/**` |
| good-binary-fixture-with-space | test | binary, name with a space, under `tests/visible/**` |
| good-quoted-non-ascii-under-docs-glob | build, allow `docs/**` | quoted name |
| good-double-star-zero-dirs | build, allow `docs/**/*.md` | `**/` matching zero directories; a name with spaces |
| good-phase-without-allow-list | review | phase missing from `allowed_paths` |
| good-dot-slash-prefix | build | `./app/api/issues.py`, hand-written |
| good-dir-name-contains-b-slash | test | empty new file `tests/visible/x b/__init__.py` (header only) |
| good-delete-in-scope | test | deletion inside the allow list |
| good-no-newline-and-two-hunks | build | `\ No newline at end of file`, two hunks |
| good-deep-test-path | test | `tests/visible/api/v2/...` |
| good-mode-and-content-in-scope | build | mode change plus content |
| good-fixture-named-feature-list | test | `tests/visible/fixtures/feature_list.json` |
| good-git-binary-patch-in-scope | test | `GIT binary patch` under `tests/visible/**` |
| good-state-files-test-phase | test | state files in the test phase |

Inline hidden tests add: quoted-name unquoting, binary-patch section end, header-only empty file,
statuses of a deletion and a mode change, CRLF line endings, a form feed inside content, and a
`git format-patch` preamble.

Status cases (`grader/hidden/test_a3_hidden_status.py`, 40): `passes` set from a gate with skipped
items, only the named feature changed, `testedAt` converted from another time zone, no
`existing tests` item, a run with skips, xfails and warnings, a `=`-padded summary, the timeout passed
through; kept false for five claim shapes, the test phase, already set, thirteen gate shapes (`passed`
as a string, as `1`, missing; no visible item; failed, 11/12, 0/0, or no ratio; a failed rule check; a
pending item; failed existing tests; not a dict), twelve test-run outputs (failures, errors, no tests
with exit 5 and 0, failures with exit 0, no summary, empty, a fake summary followed by the real one,
timed out, exit 124, denied, "passed" in a test name), and an unknown feature.

Command cases (`grader/hidden/test_a3_hidden_rule.py`): 28 rewrites denied, 4 network commands still
decided by the default rules, 42 commands allowed (including the harness's own commit, apply, status,
and diff commands built from the real `commit_command`, `SETUP_COMMIT`, and `PATCH_FILE`).

## Captured output

Real runs, from the repository root, in `captured/`. Each file starts with a line giving the date and
commit it was captured at. `make` exits 2 whenever the script it runs exits non-zero.

| File | Command | Captured | Result |
|---|---|---|---|
| `check-starter.txt` | `make check-assignment-3` | 2026-10-17, 61ec849 | every part FAIL, script exit 1 |
| `check-solution.txt` | `make check-assignment-3 A3_IMPL=submodules/03-scope-sandbox/solution` | 2026-10-17, SHA_CAP | CHECK_RESULT |
| `grade-starter.txt` | `make grade-assignment-3 SUBMISSION=submodules/03-scope-sandbox/assignment/starter` | 2026-10-17, e7287f4 | 0.0 / 100, FAIL |
| `grade-solution.txt` | `make grade-assignment-3 SUBMISSION=submodules/03-scope-sandbox/solution` | 2026-10-17, SHA_CAP | 100.0 / 100, PASS |
| `docker-solution.txt` | `uv run python -m pytest -q -p no:cacheprovider -m docker submodules/03-scope-sandbox/solution/tests` | 2026-10-16, recorded in 3dcc7a1 | 2 passed |

The reference solution scores 100.0 / 100 with `Result: PASS` on its captured live run (A/B
`ab-20261017-092810-d5d31c`, captured on 2026-10-17 into `solution/live/`): criterion 6 (live A/B
evidence, 10 points) is 10 / 10, graded like any submission's `live/`. Before that capture it
scored 90.0 / 100 with `Result: FAIL`, because valid live evidence is a pass condition. The run is
described in [README.md](README.md), "Captured live run of this solution".

## Live step: design choices

- The evidence is what the run already writes: the ScoreRecords in `exports/scores/`, the arm diffs in
  `<runs>/<ab_id>/<arm>/diff.patch`, and `ab.json`. `live.py collect` copies them and keeps only the
  fields of `ab.json` the check needs (no ticket text, no claim summaries). ScoreRecord has no model
  field, so the model is checked from the arm specs in `ab.json` and from the cost line.
- The verdict reuses the learner's interfaces unchanged: `check_diff` on the whole diff for `build`,
  on the sections touching `test_phase_files` for `test`, and `update_status` with a `SessionEnd` built
  from the recorded build claim and build end commit. Rebuilding a test-phase diff from the section
  list uses the learner's own `parse_diff`; a section it cannot read is kept (fail closed).
- `demo-3` has no verify layer, so a gate that wants evidence runs the visible tests. A replay of the
  agent's own `run_visible_tests` calls is not possible (the runner keeps only a summary), so `collect`
  runs them once in the agent image on a copy of the arm's final workspace, under the learner's
  `policy()`, and records each result. The grader replays the record: the verdict check stays offline,
  and a recorded result the gate never asked for is reported. The final workspace includes the test
  phase's changes; the commit in the evidence is the build phase's end commit.
- Points: 6 for valid evidence, 4 for reproduced verdicts, rebalanced from criteria 2 (45 to 40) and 3
  (20 to 15). Valid evidence is also a pass condition, so a submission without the live step fails
  even at 90 points.
- Known limits: the evidence files are not signed, so a learner could edit a ScoreRecord by hand; the
  checks catch inconsistent edits (ids, costs, the cost line) but not a consistent forgery. The review
  can open the A/B's LangSmith traces when `trace_url` is set.

## Review notes (about 25 minutes, brief §5.3)

1. Expected approach (5 min): one parser that counts hunks; rules in a fixed order with escape first and
   harness-only second; status checks ordered by cost; the command-position prefix in every pattern.
2. Solution walkthrough (8 min): `diffparse._git_section`, `scope.check_diff`, `status._gate_evidence`,
   `policy._CMD`.
3. Reveal the hidden diffs (5 min): open `good-header-like-lines-in-hunk.diff`,
   `bad-traversal-inside-allowed-glob.diff`, `good-dir-name-contains-b-slash.diff`, and
   `bad-empty-new-file-header-only.diff` side by side; ask which line each naive parser misreads.
4. Common mistakes (4 min): the list in the assignment README; show which hidden cases each one fails
   (the grader prints the failed test ids).
5. Discussion questions (3 min):
   - The history rule cannot stop `git commit --amen`. What would make history a boundary instead of a
     guard rail, and where would that live: the sandbox (DESIGN §9) or the harness?
   - A2's agent used git "to revert bad code changes" (A2, F-a-57). Which revert commands should an agent
     keep, and does `git reset --hard` with no revision belong on the deny list?
   - The gate check refuses `passed: true` with a failed item. Who can produce such a gate result, and
     what does that say about trusting any single field as evidence (A3, F-a-110)?
   - Should a phase without an allow list fail closed? What would break in the real layer if it did?

## Live step: what the pilot showed

The M6 pilot ran the live step's A/B (`shipharness ab --section demo-3 --feature F3 --no-preview`)
three times per pilot run (VERIFICATION.md, M6 pilot). Two findings matter for the live verdicts:

- Pilot run 1 (before the measurement fixes) charged every F3 arm with 4 out-of-scope files that were the import linter's cache
  (`.import_linter_cache/`), and counted uncommitted build work as test-phase source edits for arms
  that never commit. Pilot changes 5 and 6 fixed both for both arms. A learner verdict built on a run
  from before those changes would disagree with today's referee for that reason alone.
- Pilot run 2, with the measures fixed, had `out_of_scope_files` 0 and `test_phase_source_edits` 0 in all
  six F3 arms. On the canonical task, a learner's `check_diff` should accept the bare arm's diff in
  both phases; on the harness arm's whole-run diff, rule 2 refuses `feature_list.json` when the
  harness set `passes` (two of the three pilot run 2 harness arms), while the referee strips it. That
  difference is the one the assignment README asks learners to explain.

Pilot run 3 uses the trap variant for F3 (`trap-tempting-middleware`, DESIGN §10.4); the live step stays on
the canonical task (`--feature F3`), and the grader checks for that.

## Integration notes

- Make targets: `check-assignment-3` (`A3_IMPL=<folder>`) and `grade-assignment-3`
  (`SUBMISSION=<folder or git URL>`, passed to the grader as `--impl` by
  `scripts/grade_assignment.py`).
- The live-step command now carries `--purpose assignment` (traces to `shipharness-assignments`,
  DESIGN §12). `assignment/live.py` accepts it (it bans only `--replay`, `--swap`, `--layers`, `--k`,
  `--example`, and `--from-working-tree`), its usage text shows the flag, and
  `test_verify_accepts_the_assignment_purpose` covers it.
- `check.py`'s closing hint names the instructor grader (`make grade-assignment-3
  SUBMISSION=<folder>`); `test_check_points_to_the_instructor_grader` covers both branches.
- `solution/grader/tests/` is not under the repository's `testpaths`
  (`["tests/unit", "teamtrack/tests/visible"]` in `pyproject.toml`); run it on its own. Its last test
  is marked `slow`.
