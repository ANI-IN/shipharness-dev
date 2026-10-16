# Assignment A3: Scope and sandbox

Build the three S3 controls yourself, in a small package of your own (`a3scope`), and prove each one
against scripted inputs: a per-phase diff-scope policy, an evidence-gated update of the `passes` field,
and one new sandbox policy rule with a test that proves the denial. Then run one live A/B on F3 and
apply your own policy and status gate to what the two real arms changed.

- Difficulty: 3 to 6 hours for a strong engineer (brief §5.1). The hidden cases go past what class
  shows: renames, paths with spaces, quoted names, `../` traversal, harness files, binary files, empty
  new files, hunks whose content looks like file headers, and source edits in the test phase.
- Cost: Parts A to C need no API keys, no agent runs, and no container runtime. The required live
  step runs one `demo-3` A/B (two agent runs under the class caps; see "Cost and trace budget").
- Commands: `make check-assignment-3` (self-check), `assignment/live.py` (live step), and
  `make grade-assignment-3` (grade out of 100).

## Objective

By the end you can:

1. Decide, from a diff alone, every file it changes, including renames, copies, binary files, and names
   that `git` quotes or pads with a tab.
2. Apply a per-phase allow list to that diff with zero false positives and no missed out-of-scope file.
3. Set `passes` only from evidence (a verify gate result or a visible test run), never from the agent's
   claim alone.
4. Add a sandbox deny rule and write a test that fails when the rule is missing.
5. Apply your scope policy and status gate to the diffs of a real A/B and compare your verdicts with
   the referee's `out_of_scope_files` and `test_phase_source_edits`.

## Problem statement

In S3 the harness limits what the coding agent may change and reach. Three gaps remain that you will
close in a package that mirrors the real interfaces:

- The scope guard reads paths from a patch. A patch can hide an out-of-scope file behind a rename, a
  name with a space, a quoted non-ASCII name, a `tests/visible/../../app/...` path that string-matches
  an allowed glob, a header-only section (empty new file, mode change), or a hand-written patch with no
  `diff --git` line. It can also contain lines inside a hunk that look like `---`/`+++` headers. Your
  policy must reject every out-of-scope diff and accept every legitimate one.
- `passes` must change only with evidence. A "done" claim without a passing gate, a gate whose items
  contradict `passed: true`, or a test run whose output does not prove a pass must leave the feature
  list unchanged.
- The scope guard's byte snapshot skips `.git` (`src/shipharness/harness/scope/snapshot.py`), so a
  command that rewrites git history can never be reverted, and the evidence written with `passes`
  names a commit SHA that such a rewrite would orphan. You add a sandbox rule that refuses history
  rewrites before they run.

## Background

Read these before you start; each is short.

- **The feature list is the scope.** A2 keeps the feature list in JSON because "the model is less likely
  to inappropriately change or overwrite JSON files compared to Markdown files" (A2, F-a-81), and asks
  the coding agent to "work on only one feature at a time" (A2, F-a-83). A2's strongly-worded
  instruction: "It is unacceptable to remove or edit tests because this could lead to missing or buggy
  functionality." (A2, F-a-80).
- **Allowed paths per phase** are the course's application of two source statements: A5's security
  model has "File operations restricted to the project directory only" (A5, F-a-86), and A1 says to
  "enforce boundaries centrally, allow autonomy locally" (A1, F-a-98). The per-phase lists come from
  each dataset example's `outputs.allowed_paths` (CONTRACTS §16.1). In the real harness,
  `src/shipharness/harness/scope/guard.py` decides per path (`uv run python scripts/anchors.py extract
  S3:allowed_paths`) and `src/shipharness/harness/scope/layer.py` blocks patches and reverts command
  changes (DESIGN §6.4).
- **Only the harness sets `passes`.** A2 lets the agent mark a feature passing after "careful testing"
  (A2, F-a-108). The course moves that decision to the harness, citing A3: "Separating the agent doing
  the work from the agent judging it proves to be a strong lever" (A3, F-a-110). The `evidence` and
  `testedAt` fields and "only the harness sets `passes`" are course design, not source terms (RESEARCH
  G-6). Real code: `src/shipharness/harness/scope/status.py` (anchor `S3:passes`).
- **The sandbox** is identical for both arms and is not an A/B variable (DESIGN §9). Sources: "for each
  agent, a Docker container is spun up" (A4, F-a-88); "Claude did not have internet access at any point
  during its development" (A4, F-a-90); A5's bash allowlist, where "Commands not in the allowlist are
  blocked by the security hook." (A5, F-a-87). The course policy refuses network commands before they
  run (`DenyRule` and `check_command` in `src/shipharness/sandbox/policy.py`, anchor `S3:policy`).
- **Why history matters.** A2's agent used git "to revert bad code changes" (A2, F-a-57). Your rule must
  keep that possible (`git revert`, `git checkout -- <path>`, `git restore`) while refusing the commands
  that rewrite or delete history. That split is course design.

## What to build

All code goes in `starter/a3scope/` (or a copy of `starter/`, see "Setup"). Interfaces are given; the
bodies are `TODO`s.

| Part | File | What you implement |
|---|---|---|
| A1 | `a3scope/diffparse.py` | `parse_diff(diff) -> list[FileChange]`, `changed_paths(changes)` |
| A2 | `a3scope/scope.py` | `glob_matches(path, pattern)`, `check_diff(policy, phase, diff) -> ScopeVerdict` |
| B | `a3scope/status.py` | `update_status(document, feature_id, end, sandbox, now) -> StatusDecision` |
| C | `a3scope/policy.py` | `HISTORY_MESSAGE`, `HISTORY_RULES` (the new rule) |
| task 6 | `tests/test_a3_sandbox_rule.py` | your denial test |
| live step | `live/` (written by `assignment/live.py collect`) | evidence of one live `demo-3` A/B on F3 and your verdicts on it |

Given, no TODO: `a3scope/sandbox.py` (`PolicySandbox`, which refuses a command the way
`DockerSandbox.exec` does) and `tests/test_a3_docker_rule.py` (optional real-container check).

## Concepts tested

- Unified and git diff structure: file sections, `---`/`+++` headers, hunk line counts, `rename`/`copy`
  lines, `new file mode`/`deleted file mode`, `Binary files ... differ`, `GIT binary patch`, git's
  C-style quoting, and the tab git appends to names with spaces.
- Glob semantics for allowed paths (`*`, `?`, `**`, `**/`), the same as `guard.py`.
- Fail-closed policy design: unknown input is refused; harness-owned files win over any allow list.
- Evidence over claims: the harness, not the agent, decides `passes`, from a gate result or a test run.
- Pre-exec sandbox denials: a regex rule on the command text, its limits, and how to prove it works.

## Prerequisites

- S3 class (the scope layer, `passes`, the sandbox policy) and the code at the four anchors above.
- Python 3.12 and `uv`; the repository set up with `uv sync` (or `make setup`).
- Comfort with regular expressions and `pytest`.
- For the live step: `OPENAI_API_KEY` (and `LANGSMITH_API_KEY` for traces) in `.env`, `make doctor`
  passing, and Docker or Podman with the sandbox images (`make setup`). Parts A to C do not need them.

## Expected input and output

| Function | Input | Output |
|---|---|---|
| `parse_diff` | diff text (`str` or `bytes`) | `list[FileChange(old_path, new_path, status, binary)]`; raises `DiffParseError` for unparseable text |
| `changed_paths` | the list above | paths whose content or existence changes, in diff order |
| `check_diff` | `PhasePolicy(allowed_paths, state_layer)`, phase name, diff | `ScopeVerdict(phase, refusals)`; `accepted` is true when there are no refusals |
| `update_status` | feature-list document, feature id, `SessionEnd`, a `Sandbox`, a clock | `StatusDecision(kind, message, document, evidence)` |
| `policy()` | (none) | `SandboxPolicy` with the default deny rules first, then `HISTORY_RULES` |

## Detailed requirements

### Part A: diff parsing and the per-phase diff-scope policy

**A1, `parse_diff`.**

1. Accept `str` or `bytes` (decode bytes as UTF-8). An empty or whitespace-only diff gives `[]`.
2. Read two section shapes: git sections (from one `diff --git` line to the next) and plain unified
   sections (a `---` line directly followed by a `+++` line, outside any hunk). Ignore other lines
   outside sections (a commit message, `git format-patch` stat lines).
3. Skip hunks by counting lines with the `@@ -a,b +c,d @@` numbers (a missing count means 1). A line
   inside a hunk that starts with `--- ` or `+++ ` is content, never a header. Lines starting with `\`
   (`\ No newline at end of file`) do not count.
4. Paths, in order of preference: `rename from`/`rename to`, `copy from`/`copy to`, the `---`/`+++`
   lines, and finally the `diff --git` line (needed for header-only sections such as an empty new file,
   a deleted empty file, or a mode change). On the `diff --git` line, git quotes names with special
   characters but not names with spaces: split an unquoted `a/X b/X` where both halves are equal.
5. Remove the `a/` and `b/` prefixes only when the diff uses them (git sections with prefixed headers;
   plain sections where the old side starts with `a/` or is `/dev/null` and the new side starts with
   `b/` or is `/dev/null`). Undo C-style quoting (`"a/caf\303\251.md"` is `a/café.md`; octal escapes are
   UTF-8 bytes). Drop everything from the first tab (git's padding after names with spaces, `diff -u`
   timestamps). Remove leading `./`.
6. Status: `/dev/null` old side, or `new file mode`: `added` (`old_path=None`). `/dev/null` new side, or
   `deleted file mode`: `deleted` (`new_path=None`). Rename lines: `renamed`. Copy lines: `copied`. Equal
   paths: `modified`. Different paths without rename lines: `renamed`.
7. `binary=True` for a `Binary files ... differ` line or a `GIT binary patch` section (skip its data).
8. Split lines on `\n` (and `\r\n`), not with `str.splitlines()`: a form feed in content is not a line end.
9. Raise `DiffParseError` when the text has content but no parseable file section (hunks with no header,
   a section whose paths cannot be read).

**A1, `changed_paths`.** Added: new path. Deleted: old path. Modified: the path. Renamed: both paths.
Copied: the new path only (the source is read, not changed). Diff order, no duplicates.

**A2, `glob_matches`.** `*` and `?` stay inside one path segment; `**` spans any number of segments;
`**/` also matches zero directories (`docs/**/*.md` matches `docs/x.md`). The whole path must match
(`app/api/issues.py` does not match `app/api/issues.py.orig`; `tests/visible/**` does not match
`tests/visible_extra/a.py` or `tests/visible` itself).

**A2, `check_diff`.** Parse the diff; if parsing fails, return one refusal
`Refusal(path="", code="unparseable", ...)`. Otherwise walk the paths in diff order, one refusal per
path, and apply these rules (first match wins):

| Order | Rule | Applies to | Result |
|---|---|---|---|
| 1 | Absolute path, drive letter, or a `..` segment | every path named, copy sources included | refuse, `path_escape` |
| 2 | `feature_list.json` or `feature_list.schema.json` (after removing `./`) | changed paths | refuse, `harness_only`, in every phase, whatever the allow list says |
| 3 | `progress.md`, `session-handoff.md`, `docs/exec-plans/**` with `state_layer=True` | changed paths | allow |
| 4 | The phase has no entry in `allowed_paths` | changed paths | allow (as `PathRules(allowed=None)` in `guard.py`) |
| 5 | Matches one of the phase's globs | changed paths | allow |
| 6 | Anything else | changed paths | refuse: `test_phase_source_edit` in the `test` phase, `outside_allowed_paths` in any other phase |

Each `Refusal.message` names the path. Instruction-layer files (`AGENTS.md`, `.agents/skills/**`) are
not state files: the agent may not change them unless the allow list says so. Only the root-level
`feature_list.json` is harness-only; `tests/visible/fixtures/feature_list.json` is an ordinary path.

### Part B: evidence-gated status

`update_status(document, feature_id, end, sandbox, now, test_timeout_s=300)`:

1. If `end.passes_already_set`, or `end.phase != "build"`, or `end.last_claim` is not a dict with
   `claim == "done"` and `phase == end.phase`: return kind `"none"`, the document unchanged, and run
   nothing on the sandbox.
2. If the document does not hold exactly one feature with `id == feature_id`: kind `"note"`.
3. Verify layer on (`end.verify_layer`): the gate is the evidence, and nothing is run. It counts only if
   `gate` is a dict, `gate["passed"] is True` (not `"true"`, not `1`), no item has status `fail` or
   `pending`, and the `visible tests` item has status `pass` and a detail ratio `x/y` with `x == y > 0`.
   Evidence: `{"gate_id", "commit": end.head_commit, "visible": "x/y", "existing": "x/y" from the
   "existing tests" item or "not run", "checks": [names matching R<digits> with status pass, in order]}`.
4. Verify layer off: run `VISIBLE_TESTS_COMMAND` once with `test_timeout_s`. It counts only if the result
   is not denied, not timed out, exits 0, and its **last** pytest summary line (for example `12 passed,
   1 skipped in 0.41s`, with or without `=` padding) shows `failed == 0`, `errors == 0`, `passed > 0`.
   Evidence: `{"gate_id": "visible-tests", "commit": end.head_commit, "visible": "n/n", "existing":
   "not run (verify layer off)", "checks": []}`.
5. On success: kind `"status_set"`, a **new** document where only that feature changes (`passes: true`,
   `evidence`, `testedAt` = `now()` in UTC as `%Y-%m-%dT%H:%M:%SZ`), `evidence` set, and a message naming
   the feature id and the first 7 characters of the commit. Otherwise kind `"note"` with a message that
   names the feature id and the reason; the document unchanged.
6. Never change the document passed in.

The extra consistency checks in step 3 and the last-summary rule in step 4 are course design: they
close ways a claim could pass without proof.

### Part C: the history rule and its denial test

Fill `HISTORY_RULES` with `DenyRule` patterns (regex on the command, searched with `re.search` by the
real `check_command`) that share `reason_code="write_outside_workspace"` and one `HISTORY_MESSAGE` of
at least 20 characters saying what was refused and what to do instead. The reason codes are fixed by
`ReasonCode` in `src/shipharness/sandbox/base.py`; `write_outside_workspace` is the closest, because
`.git` is outside the files the scope guard can restore. `policy()` (given) puts the defaults first.

Must be denied:

- `git commit ... --amend`, any `git rebase`
- `git reset` with `--hard`, `--soft`, `--keep`, `--merge`, or a revision such as `HEAD~2`, `HEAD^`,
  `@~1`, `ORIG_HEAD`, or a 7 to 40 character hex SHA
- `git update-ref`, `git filter-branch`, `git filter-repo`, `git replace`, `git reflog expire|delete`
- `git branch` with `-d`, `-D`, `-f`, `-M`, `--delete`, `--force`; `git checkout|switch --orphan`
- `rm` or `mv` of the whole `.git` directory (`.git`, `./.git`, `/work/.git`) or of `.git/refs`,
  `.git/logs`, `.git/objects`, `.git/HEAD`, `.git/packed-refs`; a redirect (`>`, `>>`) into
  `.git/refs`, `.git/logs`, `.git/HEAD`, `.git/packed-refs`
- in every form above: git global options before the subcommand (`git -c k=v`, `git -C /work`,
  `git --no-pager`), `VAR=value` prefixes, a path to the binary (`/usr/bin/git`), and compound
  commands (`a && b`, `a; b`, `a || b`)

Must keep running (no false positives):

- every git command the harness itself runs in the sandbox (the setup commit in
  `src/shipharness/runner/loop.py`, `commit_command` in `src/shipharness/harness/state/commit.py`,
  `git apply ... .git/shipharness-patch.diff` in `src/shipharness/runner/tools.py`, the verify layer's
  test commit, `git status`, `git diff <sha>`, `git log`)
- append-only git: `git revert`, `git cherry-pick`, `git stash`, `git tag`, `git commit -m "..."` (a
  message may contain words such as "amend" or "reset"), `git checkout -- <path>`,
  `git checkout HEAD~2 -- <path>`, `git restore`, plain `git reset`, `git reset HEAD <path>`,
  `git reset -- <path>`, `git diff HEAD~1`, `git show HEAD^:<path>`, `git branch <name>`,
  `git switch -c <name>`, `git rm --cached`, `git mv`
- reading `.git` (`cat .git/HEAD`, `ls .git`), and paths that only start with `.git`
  (`.github/`, `.gitignore`)
- a git command quoted inside another command's argument: `grep -rn "git rebase" docs/`,
  `echo "never run git reset --hard" >> progress.md`, `python -c "print('git reset --hard')"`
- the default network rules still decide network commands first (`git push --force` stays `network`)

**Task 6, the denial test** (`tests/test_a3_sandbox_rule.py`). The grader checks three things: every
test in the file passes with your rule; at least one test fails when the rule is removed (the grader
empties `HISTORY_RULES` and makes `policy()` return the default policy); and the denial goes through the
real code (the file uses `check_command` or `PolicySandbox`, and imports from `a3scope.policy`). A good
test wraps a `FakeSandbox` in `PolicySandbox(policy(), inner)`, runs a rewrite, and asserts the reason
code, exit code 126, and `inner.commands == []` (the command never reached the sandbox).

## Constraints

- Do not import `shipharness.harness`, `shipharness.ab`, `shipharness.runner`, or `shipharness.checks`
  from `a3scope/`: that is the reference implementation. A module that does scores 0 on the criteria it
  serves. You may import `shipharness.sandbox` (required for Part B and C) and the standard library.
- Do not edit `visible_tests/`, `fixtures/`, `check.py`, or `live.py`.
- The live step uses the class settings: `OPENAI_MODEL=gpt-6-luna`, `MAX_RUN_COST_USD=0.20` per arm,
  `MAX_BATCH_COST_USD=2.50` per command (CONTRACTS §1, `.env.example`). The grader rejects evidence
  from another model, a raised cap, a replay, a swap test, or an A/B from the working tree.
- Keep the interfaces (names, fields, argument order) exactly as given; the tests call them.
- No network, API keys, or agent runs are needed or allowed in tests.
- `ruff check` and `ruff format --check` pass on your files (the repository's settings).

## Step-by-step tasks

1. Run `make check-assignment-3` and read the FAIL rows and the TODO list.
2. Part A1: implement `parse_diff` and `changed_paths`. Start with the git sections in
   `fixtures/diffs/`, then plain sections, hunk counting, quoting, binary files.
3. Part A2: implement `glob_matches`, then `check_diff` with the rules in table order.
4. Part B: implement `update_status`: the "none" cases first (no command run), then the gate path, then
   the visible-test path with summary parsing.
5. Part C: write `HISTORY_MESSAGE` and `HISTORY_RULES`. Write the "must keep running" list into a scratch
   test before you write a pattern; check every pattern against it.
6. Write your denial test in `tests/test_a3_sandbox_rule.py`; run it once with your rule and once with
   `HISTORY_RULES = ()` to see it fail.
7. Optional: `uv run python -m pytest -q -p no:cacheprovider -m docker submodules/03-scope-sandbox/assignment/starter/tests`
   runs the rule in a real container.
8. Run `make check-assignment-3` until it passes and add your own tricky cases.
9. Live step (next section): one `demo-3` A/B, then `live.py collect` and `live.py verify`.
10. Run `make grade-assignment-3`.

## Live step (required)

Parts A to C prove your controls on scripted diffs. The live step applies them to what a real coding
agent changed: one A/B on F3, the S3 feature, with both arms judged by the referee. Requiring one live
run per assignment is course design; the grade stays reproducible because the grader only checks the
files you submit and re-runs your policy on them, offline.

1. Finish Parts A to C first: the verdicts come from your code, and the grader re-runs it on the
   evidence. If you change your code later, run `collect --force` again (it needs the run folder and
   the arm workspaces of the same A/B).
2. Run the A/B and keep its terminal output:

   ```bash
   uv run shipharness ab --section demo-3 --feature F3 --no-preview 2>&1 | tee ab-output.txt
   ```

   This is `make demo-3` without the board preview containers. The command prints one line per arm and
   a cost line (`Cost: $...`). Each arm stops at `MAX_RUN_COST_USD`, the command at
   `MAX_BATCH_COST_USD`.
3. Right after it, collect the evidence into your submission folder (the arm workspaces live in the
   temp folder and are not kept forever):

   ```bash
   uv run python submodules/03-scope-sandbox/assignment/live.py collect --impl <your folder> \
       --ab-output ab-output.txt \
       --command "uv run shipharness ab --section demo-3 --feature F3 --no-preview"
   uv run python submodules/03-scope-sandbox/assignment/live.py verify --impl <your folder>
   ```

   `<your folder>` is the folder that holds `a3scope/` (`submodules/03-scope-sandbox/assignment/starter`
   if you work in place). `collect` reads the run folder (`RUNS_DIR`, default `.shipharness/runs/<ab_id>/`)
   and `exports/scores/`; `--runs`, `--exports`, and `--ab` override them.
4. Commit `live/` with your code. `make check-assignment-3` shows a "live A/B evidence" row once it is
   there.

What `collect` writes to `<your folder>/live/`:

| File | Content |
|---|---|
| `command.txt` | the exact command you ran (`--command`) |
| `ab-output.txt` | the A/B's terminal output, with the `A/B <ab_id> (F3, ...)` line and the `Cost: $...` line |
| `ab-summary.json` | the fields of the run's `ab.json` the check needs: section, `checkpoint_sha`, per arm the run id, model, layers, cost cap, allowed paths, claims, phase commits, cost, and `test_phase_files` |
| `scores/<run_id>.json` | both arms' ScoreRecords, copied unchanged from `exports/scores/` (fields: `src/shipharness/ab/score.py`) |
| `bare/diff.patch`, `harness/diff.patch` | each arm's recorded diff (`<runs>/<ab_id>/<arm>/diff.patch`) |
| `<arm>/sandbox-log.json` | every command your status gate ran, with its output and exit code |
| `verdict-bare.json`, `verdict-harness.json` | your verdict per arm (below) |

A verdict holds:

- `scope.build`: `check_diff(PhasePolicy(<the arm's allowed_paths>, state_layer=<state layer on>),
  "build", diff.patch)` as `accepted` and `refusals` (`path`, `code`).
- `scope.test`: the same for the `test` phase, on the sections of `diff.patch` that touch the files
  the arm changed during the test phase (`test_phase_files` in `ab.json`).
- `status`: your `update_status` on the arm's build-phase claim (`SessionEnd` with the recorded claim
  and the build phase's end commit; no verify gate in `demo-3`). When your gate runs the visible tests,
  `collect` runs them in the agent sandbox image (`shipharness-agent:1`) on a copy of the arm's final
  workspace, under your `policy()`, and records the result; the grader replays that record.
- `referee`: the referee's `status`, `claim`, `out_of_scope_files`, `test_phase_source_edits`, and
  `passed_primary` from the arm's ScoreRecord, next to yours.
- An `error` field instead of a result when your code raised; the grader compares it like any other
  field.

Read the two verdicts against the referee's counts before the review. They need not agree: the referee
counts out-of-scope files on the diff with harness-owned files removed (`strip_harness_artifacts` in
`src/shipharness/ab/artifacts.py`), while your guard reads the whole diff. In the harness arm, for
example, `feature_list.json` changes when the harness itself sets `passes`, and your rule 2 refuses it.
Be ready to say, for each difference, which side is right for an agent patch and which for a whole-run
diff.

What the grader checks (criterion 6, no model calls, no keys, no container):

- the files above exist; `command.txt` is `make demo-3` or `shipharness ab --section demo-3 --feature
  F3` (`--no-preview` allowed; no `--replay`, `--swap`, `--layers`, `--k`, `--example`, or
  `--from-working-tree`);
- both ScoreRecords validate against `ScoreRecord`, their `run_id`s match the file names and
  `ab-summary.json`, `ab_id` matches the `A/B <ab_id>` line, `feature_id` is `F3`, `checkpoint_sha` is
  present and matches, `recorded` is false, and `sandboxed` is true;
- the section is `demo-3` with both arms (bare: no layers; harness: instructions, state, scope), the
  model is `gpt-6-luna`, each arm's cost is within `MAX_RUN_COST_USD` ($0.20), each review within
  `MAX_REVIEW_COST_USD` ($0.04), and the cost line within `MAX_BATCH_COST_USD` ($2.50);
- your code, re-run on the included diffs with `sandbox-log.json` replayed, gives both verdict files
  exactly, and the log holds no result your gate did not ask for.

A verdict from the reference solution on a real A/B:

[[PENDING: verdict-bare.json and verdict-harness.json of the reference solution on a live demo-3 A/B | source: M8 batch 1 | how: uv run shipharness ab --section demo-3 --feature F3 --no-preview, output saved as ab-output.txt; uv run python submodules/03-scope-sandbox/assignment/live.py collect --impl <reference folder> --ab-output ab-output.txt --command "uv run shipharness ab --section demo-3 --feature F3 --no-preview"]]

## Expected project structure

```text
submodules/03-scope-sandbox/assignment/
├── README.md                 this file
├── check.py                  self-check (make check-assignment-3)
├── live.py                   live step: collect the A/B evidence, verify it
├── fixtures/
│   ├── make_fixtures.py      builds the visible diffs from real git output
│   ├── cases.json            phase, allowed paths, expected result per case
│   └── diffs/*.diff          12 visible scripted diffs (6 out of scope, 6 legitimate)
├── visible_tests/            the self-check's tests (do not edit)
└── starter/                  your work goes here
    ├── a3scope/
    │   ├── diffparse.py      Part A1 (TODO)
    │   ├── scope.py          Part A2 (TODO)
    │   ├── status.py         Part B (TODO)
    │   ├── policy.py         Part C (TODO)
    │   └── sandbox.py        PolicySandbox (given)
    ├── tests/
    │   ├── test_a3_sandbox_rule.py   task 6 (TODO)
    │   └── test_a3_docker_rule.py    optional container check (given)
    └── live/                 written by live.py collect (live step; you commit it)
```

## Setup

```bash
uv sync                      # or: make setup (also builds the sandbox images)
git switch -c a3-<your-name> # work on your own branch
```

Work in place in `assignment/starter/`, or copy it (`cp -r submodules/03-scope-sandbox/assignment/starter $HOME/a3`)
and pass `IMPL=$HOME/a3` to the make targets (`--impl $HOME/a3` to the scripts).

## How to run

```bash
make check-assignment-3                 # visible tests + your denial test + live/ check + TODO list
make grade-assignment-3                 # visible + hidden tests + live evidence, score out of 100
make check-assignment-3 IMPL=$HOME/a3       # a copy elsewhere
uv run python submodules/03-scope-sandbox/assignment/check.py --impl $HOME/a3   # without make
uv run python submodules/03-scope-sandbox/assignment/live.py verify --impl $HOME/a3  # live/ only
```

## How to test

```bash
# the visible tests directly (A3_IMPL defaults to the starter)
uv run python -m pytest -q -p no:cacheprovider submodules/03-scope-sandbox/assignment/visible_tests
# your own tests
uv run python -m pytest -q -p no:cacheprovider submodules/03-scope-sandbox/assignment/starter/tests
# optional: the rule in a real container (needs the shipharness-agent:1 image)
uv run python -m pytest -q -p no:cacheprovider -m docker submodules/03-scope-sandbox/assignment/starter/tests
```

Add your own cases: `fixtures/make_fixtures.py` shows how to turn file operations into real
`git diff --cached` output (`staged_diff([...])`).

## Expected behaviour

- On the starter, the self-check prints a FAIL row per part, the failing tests, and every
  `TODO(A3 ...)` marker, and exits 1. The only rows that pass are the "allows" rows, because an empty
  rule allows everything.
- On a complete solution without `live/`, every row is `ok` and the live row says `missing`; the
  self-check exits 0, and the grader prints 90.0 / 100 and `Result: FAIL` (the live evidence is
  required). With valid live evidence it prints 100.0 / 100 and `Result: PASS`.
- `live.py verify` prints `evidence ok` and `verdicts ok` on a complete live step.
- With `HISTORY_RULES = ()`, your denial test fails.
- The optional container test fails on the starter (the amend runs and rewrites the commit) and passes
  once the rule is in place.

## Example inputs and outputs

A rename that moves an allowed file out of scope (`fixtures/diffs/bad-rename-out-of-scope.diff`, real
`git diff --cached -M` output):

```diff
diff --git a/app/api/issues.py b/app/api/issues_v2.py
similarity index 100%
rename from app/api/issues.py
rename to app/api/issues_v2.py
```

```python
# F3_ALLOWED: the allowed paths of every F3 dataset example (fixtures/make_fixtures.py)
parse_diff(diff)  # [FileChange(old_path="app/api/issues.py", new_path="app/api/issues_v2.py", status="renamed")]
check_diff(PhasePolicy(F3_ALLOWED), "build", diff).refusals
# (Refusal(path="app/api/issues_v2.py", code="outside_allowed_paths", message="app/api/issues_v2.py is outside ..."),)
```

A name with a space: git pads the `---`/`+++` names with a tab (`fixtures/diffs/good-space-in-path.diff`):

```text
--- a/docs/design notes/f3 retry.md<TAB>
+++ b/docs/design notes/f3 retry.md<TAB>
```

The path is `docs/design notes/f3 retry.md`, without the tab.

A status decision with the verify layer off and a passing run:

```python
end = SessionEnd(phase="build", last_claim={"phase": "build", "claim": "done", "summary": ""},
                 verify_layer=False, gate=None, head_commit="c0ffee...")
# sandbox output "....\n4 passed in 0.31s\n", exit 0
decision.kind      # "status_set"
decision.evidence  # {"gate_id": "visible-tests", "commit": "c0ffee...", "visible": "4/4",
                   #  "existing": "not run (verify layer off)", "checks": []}
```

The self-check on the starter (first rows):

```text
A3 self-check: submodules/03-scope-sandbox/assignment/starter
  check                                              visible tests  status  where
  diff parsing and path matching                              0/28  FAIL    a3scope/diffparse.py, a3scope/scope.py (glob_matches)
  out-of-scope diffs rejected                                  0/8  FAIL    a3scope/scope.py (check_diff)
  legitimate diffs accepted                                    0/6  FAIL    a3scope/scope.py (check_diff)
```

## Grading criteria (100 points)

`make grade-assignment-3` runs the visible tests, the hidden tests (more scripted diffs, commands, and
status cases than the visible ones), your denial test, and `live.py verify` on your `live/` folder,
then prints this table. Test-name prefixes decide the group of each test.

| # | Criterion | Points | How it is scored |
|---|---|---|---|
| 1 | Diff parsing and path matching (`test_parse_*`) | 15 | 15 × share passing |
| 2 | Diff-scope policy: out-of-scope diffs rejected with the offending path and code (`test_bad_*`), legitimate diffs accepted (`test_good_*`) | 40 | 40 × share rejected × share accepted |
| 3 | Evidence-gated status: `passes` set with the right evidence (`test_status_sets_*`), kept false otherwise (`test_status_keeps_*`) | 15 | 15 × share set × share kept |
| 4 | Sandbox history rule: rewrites denied (`test_rule_denies_*`), ordinary and harness commands allowed (`test_rule_allows_*`) | 10 | 10 × share denied × share allowed |
| 5 | Denial test proves the denial | 10 | passes with the rule (4); fails with the rule removed (4, only if it passes with it); uses `check_command` or `PolicySandbox` (2) |
| 6 | Live A/B evidence (`live/`, see "Live step") | 10 | valid evidence of one live `demo-3` A/B on F3 (6); your policy re-run on the included diffs reproduces both verdict files (4, only with valid evidence) |

Criteria 2 to 4 multiply both sides, so a policy that refuses everything (or allows everything) earns
nothing there. **Pass:** at least 80 points, every out-of-scope diff rejected, zero false positives on
legitimate diffs, and valid live evidence (criterion 6, first part). Missing or malformed live score
records fail criterion 6 and the pass. A module that imports the reference implementation scores 0 on
its criteria.

## Common mistakes

- Reading `---`/`+++` lines inside hunks as headers (a removed Markdown line `-- note` appears as
  `--- note`), or reading only `---`/`+++` lines and missing header-only sections.
- Splitting `diff --git a/x b/y b/x b/y` at the first ` b/`.
- Leaving git's trailing tab on a name with spaces, or the quotes on a quoted name.
- Matching globs with `startswith` or `fnmatch` without segment rules (`tests/visible_extra/` passes,
  or `*` crosses `/`).
- Checking `..` only at the start of a path: `tests/visible/../../app/x.py` matches `tests/visible/**`.
- Treating a copy source as changed (false positive), or ignoring rename sources (a missed deletion).
- Testing `"feature_list.json" in path` instead of an exact match after removing `./`.
- Setting `passes` when `gate["passed"]` is truthy but not `True`, or when the exit code is 0 but the
  summary shows failures; reading the first pytest summary line instead of the last.
- Running the visible tests when there is no done claim (the agent did not ask; it costs a test run).
- Mutating the document passed in.
- A history pattern such as `git.*reset.*--hard` that also refuses `git commit -m "reset ..."` or
  `grep "git reset" docs/`; or a pattern that refuses `git apply ... .git/shipharness-patch.diff`, which
  breaks the harness's own patch tool.
- A denial test that builds its own `DenyRule` instead of calling `policy()`: it passes without your
  rule, and loses the mutation points.
- Running `collect` days after the A/B: the arm workspaces in the temp folder may be gone, and a gate
  that runs the visible tests then has nothing to run them on.
- Editing your code after `collect` without collecting again: the verdict files no longer match what
  your code gives, and criterion 6 loses its verdict points.
- Raising `MAX_RUN_COST_USD` or changing `OPENAI_MODEL` for the live step: the grader rejects the
  evidence.

## Cost and trace budget

Parts A to C call no model and write no traces. The live step is the only paid command: one
`demo-3` A/B, two agent runs on `gpt-6-luna`. Its caps bound the cost: each arm stops at
`MAX_RUN_COST_USD` ($0.20), each blinded review at `MAX_REVIEW_COST_USD` ($0.04), and the command at
`MAX_BATCH_COST_USD` ($2.50) (CONTRACTS §1). It writes two traces per run, the agent root and the
referee evaluator (DESIGN §12), so four traces. `collect` and `verify` call no model. DESIGN §11.5
planned A3 at ≤ $0.25 and ≤ 30 traces before the live step was added; the measured cost of one A/B:

[[PENDING: cost line (Cost: $...) of one demo-3 A/B with the reference solution's live step | source: M8 batch 1 | how: uv run shipharness ab --section demo-3 --feature F3 --no-preview]]

The live step logs no separate LangSmith experiment: the A/B's traces go to the class project, as in
the section demo.
