# Apply the harness kit to your own repository

This guide takes the harness you saw on TeamTrack and puts it into your own repository, one step at
a time: install, copy the kit, fill in the map, define house rules, run the first harnessed
command, read the results, and decide which layers earn their place. Every step gives the exact
command, what you should see, how to check that it worked, and the mistakes people make. A worked
example on a real repository, three modules of boltons, runs through all of it with captured
output.

Why it matters: a coding agent sees only what is in the repository. A1 keeps the instructions as a
map, "we treat it as the table of contents", "roughly 100 lines" (A1, F-a-27, F-a-28), and A2 notes
that "each new session begins with no memory of what came before" (A2, F-a-08). The kit gives your
repository the same map, the same session files, and the same checks TeamTrack has in the course,
starting from TeamTrack's real values. Source ids (A1, F-a-27, ...) are listed in `REFERENCES.md`
at the root of the course repository.

What it costs: steps 1 to 4 make no model calls and print `Cost: $0.000000 (no model calls)`. Step 5
calls OpenAI and costs money, within a cap you set on the command line.

| Step | What you do | Model calls |
|---|---|---|
| [1](#step-1-install) | Install shipharness | none |
| [2](#step-2-copy-the-kit-into-your-repository) | `shipharness init --target` | none |
| [3](#step-3-fill-in-the-map) | Replace the REPLACE markers; `shipharness init --check` | none |
| [4](#step-4-define-your-house-rules) | Adapt the house rules; `shipharness check` | none |
| [5](#step-5-the-first-harnessed-run) | `shipharness testgen` on one module | yes, capped |
| [6](#step-6-read-the-results) | Read the check and testgen output | none |
| [7](#step-7-decide-which-layers-earn-their-place) | Keep, change, or drop each layer | none |

## The worked example

The example repository is three modules of boltons 26.2.0 (`typeutils`, `listutils`,
`queueutils`) with their tests: a real, small, BSD-3-Clause library that the course already pins for
`shipharness testgen`. It is not a FastAPI app, so it also shows what to do when most of TeamTrack's
house rules do not apply. The end state of every file is in
[kit/examples/boltons-queueutils/](../kit/examples/boltons-queueutils/README.md).

Build it from the shipharness checkout (the fetch uses git and the network, never a model):

```bash
uv run python scripts/fetch_testgen_libs.py boltons
bash kit/examples/boltons-queueutils/make_repo.sh /tmp/boltons-queueutils
```

Every capture in this guide was made on 2026-10-17 in a shipharness checkout, with the worked
example at `/tmp/boltons-queueutils`. In the captured lines, the checkout's own path is written as
`$SHIPHARNESS` (the only change made to them); yours show your own path.

Captured on 2026-10-17 from `uv run python scripts/fetch_testgen_libs.py boltons`,
on a checkout without the clone (the script cloned boltons and verified the pinned commit); your
output will differ:

```text
ok boltons 26.2.0 4332b35a278d694f30c99881faa61cde695c7a96 -> $SHIPHARNESS/.shipharness/libs/boltons/src
```

Captured on 2026-10-17 from `bash kit/examples/boltons-queueutils/make_repo.sh /tmp/boltons-queueutils`; your output will differ:

```text
created /tmp/boltons-queueutils from boltons 4332b35
.gitignore
LICENSE
boltons/__init__.py
boltons/listutils.py
boltons/queueutils.py
boltons/typeutils.py
tests/__init__.py
tests/conftest.py
tests/test_listutils.py
tests/test_queueutils.py
tests/test_typeutils.py
```

In the commands below, `SHIPHARNESS` is the path of your shipharness checkout and `TARGET` is your
repository. Set them once per terminal:

```bash
export SHIPHARNESS=~/shipharness          # where you cloned shipharness (README, Quick start)
export TARGET=/tmp/boltons-queueutils     # your repository; the worked example uses this path
```

## Step 1: Install

What it is: shipharness runs from its own checkout, with its own Python environment. Your
repository does not need to install anything.

```bash
cd "$SHIPHARNESS"
uv sync
uv run shipharness --version
```

What you should see. Captured on 2026-10-17 from `uv sync` and `uv run shipharness --version`; your output will differ:

```text
Resolved 85 packages in 3ms
Checked 83 packages in 1ms
shipharness 0.1.0
```

How to check it worked: `uv run shipharness init --help` lists `--target`, `--check`, `--skills`,
and `--force`.

Common mistakes:

- Running `uv sync` outside the checkout. Captured on 2026-10-17 from `uv sync` in an empty
  folder (exit code 2); your output will differ:

  ```text
  error: No `pyproject.toml` found in current directory or any parent directory
  ```

  Run `cd "$SHIPHARNESS"` first.
- On Windows, running from PowerShell. Use the Ubuntu terminal (README, Troubleshooting).

## Step 2: Copy the kit into your repository

What it is: `shipharness init` copies the kit's templates and the four course skills into your
repository. Every template holds TeamTrack's real values with a REPLACE marker next to each value.
The file list and where each file comes from are in [kit/README.md](../kit/README.md).

Commit or stash your own changes first, so the kit's files show up as one change.

```bash
cd "$SHIPHARNESS"
uv run shipharness init --target "$TARGET"
```

What you should see: one `+ <path>` line per file written, then a summary. In the worked example,
captured on 2026-10-17 from `uv run shipharness init --target /tmp/boltons-queueutils`, first two and last eleven lines; your output will differ:

```text
Kit: $SHIPHARNESS/kit/templates -> /tmp/boltons-queueutils
+ .agents/skills/assured-tests/README.md
...
+ feature_list.json
+ feature_list.schema.json
+ harness/check-params.json
+ harness/sandbox-policy.toml
+ harness/shipharness_adapter.py
+ init.sh
+ progress.md
+ session-handoff.md
wrote 97 files, 0 overwritten, 0 skipped, 0 unchanged
Next: fill the REPLACE markers, then run: shipharness init --check /tmp/boltons-queueutils
Cost: $0.000000 (no model calls)
```

The 97 files are 27 templates plus the four skills twice: once in `.claude/skills/` (Claude Code,
Cursor) and once in `.agents/skills/` (Codex, Cursor). `--skills claude` or `--skills agents`
installs one copy only. Each skill's README says which tool reads which folder, for example
[skills/harness-setup/README.md](../skills/harness-setup/README.md).

How to check it worked:

1. Run the same command again: it writes nothing. Captured on 2026-10-17 from the same command at
   commit d132507; your output will differ:

   ```text
   Kit: $SHIPHARNESS/kit/templates -> /tmp/boltons-queueutils
   wrote 0 files, 0 overwritten, 0 skipped, 97 unchanged
   Next: fill the REPLACE markers, then run: shipharness init --check /tmp/boltons-queueutils
   Cost: $0.000000 (no model calls)
   ```

2. Validate the installed skills. Captured on 2026-10-17 from
   `uv run --project "$SHIPHARNESS" shipharness skills validate .claude/skills` (run in the
   repository); your output will differ:

   ```text
   + assured-tests: valid (SKILL.md 96 lines)
   + harness-setup: valid (SKILL.md 103 lines)
   + house-rules: valid (SKILL.md 94 lines)
   + skill-template: valid (SKILL.md 46 lines)
   4 skills checked, 0 errors, 0 warnings
   Cost: $0.000000 (no model calls)
   ```

   The same command on `.agents/skills` prints the same four lines.

3. Commit the kit as copied (`git add -A && git commit -m "kit: shipharness init"`), so the next
   commit shows exactly what you filled in.

Common mistakes:

- The target does not exist. Captured on 2026-10-17 from
  `uv run shipharness init --target /tmp/no-such-repo`:

  ```text
  x target directory not found: /tmp/no-such-repo
  Cost: $0.000000 (no model calls)
  ```

- Your repository already has one of the files, for example its own `AGENTS.md`. init never
  overwrites it and says so. Captured on 2026-10-17 from
  `uv run shipharness init --target /tmp/kit-skip-demo --skills claude | grep -v "^+ "` (a folder
  holding only an `AGENTS.md`):

  ```text
  Kit: $SHIPHARNESS/kit/templates -> /tmp/kit-skip-demo
  ! skipped AGENTS.md: exists with other content (--force overwrites)
  wrote 61 files, 0 overwritten, 1 skipped, 0 unchanged
  Next: fill the REPLACE markers, then run: shipharness init --check /tmp/kit-skip-demo
  Cost: $0.000000 (no model calls)
  ```

  Merge by hand: open `kit/templates/AGENTS.md` in the shipharness checkout next to your own file.
  Use `--force` only when you want the template to replace your file.

## Step 3: Fill in the map

What it is: replacing TeamTrack's values with facts about your repository, file by file, until no
REPLACE marker is left. Each marker says what the value means; the TeamTrack value below it shows
the shape. The markers have one form per file type (`<!-- REPLACE: ... -->` in Markdown,
`# REPLACE: ...` in shell, YAML, TOML, and Python, a `"_replace"` key in JSON), so
`shipharness init --check` finds all of them.

```bash
cd "$TARGET"
uv run --project "$SHIPHARNESS" shipharness init --check .
```

What you should see first: one line per marker, `file:line: what to write`, then a count and exit
code 1. Captured on 2026-10-17 from `uv run shipharness init --check /tmp/boltons-queueutils`, first four and last three lines; your output will differ:

```text
.github/workflows/shipharness.yml:1: CI for your repository's house rules. The values are TeamTrack's, as if teamtrack/ were its own repository: the app is at the repository root, the existing tests are in tests/visible, and the adapter is harness/shipharness_adapter.py.
.github/workflows/shipharness.yml:20: the module testgen writes tests for, relative to the repository root.
.github/workflows/shipharness.yml:24: the existing tests of that module (filter 3 measures coverage over them).
.github/workflows/shipharness.yml:41: the shipharness repository you cloned for the course (README, Quick start).
...
session-handoff.md:14: nothing to fill now: the agent writes these notes at the end of each session. Delete this line.
x 103 REPLACE markers left in 27 files
Cost: $0.000000 (no model calls)
```

Fill the files in this order, because later files point at earlier ones:

1. `AGENTS.md`: what the repository is, where each rule lives, the commands, the session start and
   end steps. Keep it a map near 100 lines; the rules go into the documents it points to.
2. `ARCHITECTURE.md`: modules or packages, layers, and what each may import.
3. `docs/`: the rules (`SECURITY.md`, `RELIABILITY.md`), quality grades, plans, design decisions,
   product specs, notes on tools, the clean-state checklist.
4. `feature_list.json`, `docs/exec-plans/active/<id>.md`, `progress.md`, `session-handoff.md`: one
   real feature to work on next. Every entry starts with `"passes": false`.
5. `init.sh`: reach a known state, then run one basic end-to-end test.

A document that does not apply is deleted, not left half-filled. `--check` lists a deleted kit file
as not present and does not count it. Run every command you write into AGENTS.md, init.sh, and the
checklist before you commit it.

In the worked example, the map, the architecture document, and the docs were rewritten for the
three modules, and six documents were deleted because a library with no API, tenants, or database
has no use for them. The feature is a real bug: the docstrings of `peek` and `pop` say an empty
queue raises `KeyError`, and the code raises `IndexError`. Captured on 2026-10-17 from
`uv run --project "$SHIPHARNESS" python -c "from boltons.queueutils import HeapPriorityQueue; HeapPriorityQueue().pop()"`, last line of the traceback:

```text
IndexError: pop on empty queue
```

Compare [the filled map](../kit/examples/boltons-queueutils/filled/AGENTS.md) with
[the template](../kit/templates/AGENTS.md) to see the edits.

How to check it worked:

1. `--check` exits 0. Captured on 2026-10-17 from
   `uv run --project "$SHIPHARNESS" shipharness init --check .` in the filled worked example at
   commit d132507; your output will differ:

   ```text
   - docs/RELIABILITY.md: not present (deleted, or never installed)
   - docs/SECURITY.md: not present (deleted, or never installed)
   - docs/design-docs/api-conventions.md: not present (deleted, or never installed)
   - docs/design-docs/cursor-pagination.md: not present (deleted, or never installed)
   - docs/product-specs/teamtrack-base.md: not present (deleted, or never installed)
   - docs/references/alembic-llms.txt: not present (deleted, or never installed)
   + no REPLACE markers left in the kit files
   Cost: $0.000000 (no model calls)
   ```

2. `init.sh` passes. Captured on 2026-10-17 from `uv run --project "$SHIPHARNESS" bash init.sh` at
   commit d132507; your output will differ:

   ```text
   == imports: the three modules load
   == basic end-to-end test: queueutils, stop at the first failure (full suite: see AGENTS.md)
   ...                                                                      [100%]
   3 passed in 0.73s
   ```

3. Every path the map names exists: open each row of the "Where to look" table.

Common mistakes:

- Deleting the marker line but leaving TeamTrack's value under it. `--check` cannot see that; read
  each file once more and search for `TeamTrack`, `org_id`, and `app/api`.
- Leaving a `"_replace"` key in `feature_list.json`. The schema sets `additionalProperties` to false,
  so the file no longer validates against `feature_list.schema.json` until the key is gone.
- A map that grows into a manual. Move each rule into the document it belongs to and leave one line
  and a pointer in AGENTS.md.
- Commands that were never run. An agent trusts AGENTS.md; a wrong test command costs it a session.

## Step 4: Define your house rules

What it is: a house rule is a convention written as one checkable sentence, with a check that finds
every violation. "House rules" is the course's label for what A1 calls "golden principles" and
"taste invariants" enforced mechanically (A1, F-a-96, F-a-99), and A1's reason for checks over
documents is "When documentation falls short, we promote the rule into code" (A1, F-a-43).
`shipharness check` runs TeamTrack's seven rules (R1-R7) on any FastAPI app, with no model calls.

Three files hold your version:

| File | What you decide |
|---|---|
| `docs/house-rules.md` | Which of R1-R7 you keep, and why; the table lists what each check needs |
| `harness/shipharness_adapter.py` | The facts the checks need about your app; delete the methods of rules you drop |
| `harness/check-params.json` | `regression_targets`: the pytest targets of your existing suite |

For a FastAPI service, keep the template's methods and change their values: two seeded tenants,
how a test client signs in as a role, the seeded ids, how to count audit rows. The adapter template
answers exactly like TeamTrack's built-in adapter, so it is a working starting point.

For a library, keep R6 as a layering rule for your packages and the check that existing tests keep
passing. The worked example keeps `layering_contract()` with an import-linter layers contract
(`queueutils` above `listutils` above `typeutils`) and `exemptions()`
([its adapter](../kit/examples/boltons-queueutils/filled/harness/shipharness_adapter.py)).

Record today's violations once as the baseline, then check against it. Run from your repository:

```bash
cd "$TARGET"
PYTHONPATH=harness uv run --project "$SHIPHARNESS" shipharness check --app . \
  --adapter shipharness_adapter:HouseRulesAdapter --rules R6,regression \
  --params harness/check-params.json --json > harness/check-baseline.json
PYTHONPATH=harness uv run --project "$SHIPHARNESS" shipharness check --app . \
  --adapter shipharness_adapter:HouseRulesAdapter --rules R6,regression \
  --params harness/check-params.json --baseline harness/check-baseline.json
```

Use your own list after `--rules`, for example `R1,R2,R3,R4,R5,R6,R7` for a service that keeps all
seven.

What you should see: one `PASS` or `FAIL` line per check. Captured on 2026-10-17 from the second
command in the worked example; your output will differ:

```text
UNSANDBOXED: the checks import and run this app's code on this machine.
  R6 import-linter
  existing tests
PASS  r6_layering      new=0 baseline=0 probes=1 576 ms
PASS  regression       new=0 baseline=0 probes=21 4488 ms
Cost: $0.000000 (no model calls)
```

The 21 probes of `regression` are the 16 test functions and 5 doctests, because
`check-params.json` sets `regression_targets` to `--doctest-modules boltons tests`.

How to check it worked: break the rule on purpose and watch the check fail. Captured on 2026-10-17
from these two commands in the worked example; your output will differ:

```text
$ echo "from .queueutils import PriorityQueue" >> boltons/typeutils.py
$ PYTHONPATH=harness uv run --project "$SHIPHARNESS" shipharness check --app . --adapter shipharness_adapter:HouseRulesAdapter --rules R6,regression --params harness/check-params.json --baseline harness/check-baseline.json
UNSANDBOXED: the checks import and run this app's code on this machine.
  R6 import-linter
  existing tests
FAIL  r6_layering      new=1 baseline=0 probes=1 721 ms
      [violation] forbidden import: boltons.typeutils -> boltons.queueutils
PASS  regression       new=0 baseline=0 probes=21 4531 ms
Cost: $0.000000 (no model calls)
```

The exit code was 3 (a new violation). Undo the change (`git checkout -- boltons/typeutils.py`).
A check that never fails proves nothing.

Then wire it into CI: `.github/workflows/shipharness.yml` runs the second command on every push.
Commit `harness/check-baseline.json` with it. The workflow checks out shipharness next to your
repository; replace the repository name if you cloned a fork.

Common mistakes:

- `PYTHONPATH` missing, so the adapter cannot be imported. Captured on 2026-10-17 from the check
  command without `PYTHONPATH=harness`, last line:

  ```text
  ModuleNotFoundError: No module named 'shipharness_adapter'
  ```

- A rule in `--rules` whose adapter methods you deleted. Captured on 2026-10-17 from
  `PYTHONPATH=harness uv run --project "$SHIPHARNESS" shipharness check --app . --adapter shipharness_adapter:HouseRulesAdapter --rules R2`
  in the worked example:

  ```text
  UNSANDBOXED: the checks import and run this app's code on this machine.
  FAIL  r2_roles         new=1 baseline=0 probes=0 0 ms
        [error] check crashed: AttributeError: 'HouseRulesAdapter' object has no attribute 'create_app'
  Cost: $0.000000 (no model calls)
  ```

  The exit code is 1. Drop the rule, or add the methods `docs/house-rules.md` lists for it.
- Running the checks on code you do not trust. They import and run your app in this process; the
  first line says so.
- Writing the R6 contract into your repository's own `.importlinter` only. The check reads the
  contract from the adapter on purpose, so a change under review cannot weaken it.

## Step 5: The first harnessed run

What it is: the first command that puts a model to work on your code. `shipharness testgen` asks a
model for tests of one module and keeps a proposed test only if it passes five filters: it runs,
it passes five runs in a row, it adds coverage or kills a mutant, it has real assertions, and it
changed no source file (the filters and their sources are in
[final-project/README.md, part 9](../final-project/README.md#9-run-shipharness-on-your-own-repository)).
`--layers verify` gives the model the course's verify layer. It works on any repository with a
pytest suite, which makes it the first harnessed run for a repository that is not TeamTrack.

It costs money. Set a cap below the default for a first try: `MAX_RUN_COST_USD` is $0.20 per run
by default (`src/shipharness/config/settings.py`), and the cost tracker refuses a model call that
would cross it (README, [Costs and caps](../README.md#13-costs-and-caps)). Prices per 1M tokens are
in `config/prices.toml`: gpt-6-luna $0.10 input, $0.01 cached input, $0.50 output. The variable
overrides the default for one command; captured on 2026-10-17 from
`MAX_RUN_COST_USD=0.10 uv run --project "$SHIPHARNESS" python -c "from shipharness.config import Settings; print(Settings().max_run_cost_usd)"`:

```text
0.1
```

The command for the worked example, run from the repository, with a $0.10 cap and three proposed
tests. testgen has no `--purpose` option; when LangSmith is set up, it traces to the
`shipharness-testgen` project.

```bash
cd "$TARGET"
MAX_RUN_COST_USD=0.10 uv run --project "$SHIPHARNESS" shipharness testgen --repo . \
  --module boltons/queueutils.py --tests tests/test_queueutils.py --layers verify \
  --max-tests 3 --sandbox local --python "$SHIPHARNESS/.venv/bin/python" \
  --out /tmp/boltons-queueutils-testgen
```

`--sandbox local` runs the generated tests on your machine with your permissions, and the command
prints UNSANDBOXED; for code you do not trust, build an image and pass `--sandbox docker --image`.
`--python` is an interpreter with your repository's dependencies, pytest, and coverage; the
shipharness environment has all three for this example. With `--layers verify`, the visible tests the
layer runs are the folder of `--tests` (here `tests/`), and the migration-head check runs only when the
repository has an Alembic configuration, so a library such as boltons needs neither TeamTrack's
`tests/visible` folder nor a database (a bug fixed on 2026-10-17: before the fix, every gate on
boltons failed on those two TeamTrack paths).

What you should see (the format is in `src/shipharness/testgen/commands.py`): a `Baseline:` line,
a summary `testgen <run id>: <status>; kept <n> of <m> proposed tests`, one line per proposed test
(`+ <test id>` for a kept test, `- <test id>: filter <n>: <reason>` for a discarded one),
`Kept tests and report: <folder>`, and the cost line.

Captured on 2026-10-17, run r-20261017-121823-aa1c4b; your output will differ:

```text
! UNSANDBOXED — results not official: generated tests run on this machine
Baseline: existing suite without doctests
testgen r-20261017-121823-aa1c4b: completed; kept 3 of 3 proposed tests
+ tests/test_queueutils_generated.py::test_priority_updates_preserve_order_for_equal_priorities
+ tests/test_queueutils_generated.py::test_remove_and_empty_queue_defaults
+ tests/test_queueutils_generated.py::test_custom_priority_key_and_unexpected_keyword
Kept tests and report: /tmp/boltons-queueutils-testgen
Cost: $0.002031 (testgen, model gpt-6-luna)
```

The run stayed far below the $0.10 cap: three proposed tests, all kept, for $0.002031.

How to check it worked: the output folder holds the kept tests and `testgen-report.json`, and the
last line is a cost line at or below your cap.

Common mistakes:

- No API key. testgen stops before any model call. Captured on 2026-10-17 from the command above
  with `OPENAI_API_KEY=` (empty) in front:

  ```text
  x OPENAI_API_KEY is missing: add it to .env at the repo root
  Cost: $0.000000 (no model calls)
  ```

  The key goes into `.env` in the shipharness checkout, never into your repository.
- `--python` points at an interpreter without your dependencies, so even the existing tests fail
  and nothing can be kept.
- `--out` inside your repository leaves untracked files behind; use a folder outside it, or add the
  folder to `.gitignore`.

## Step 6: Read the results

The check output, line by line:

| Part | Meaning |
|---|---|
| `PASS` / `FAIL` | `FAIL` means at least one new violation |
| `new=` | Violations not in the baseline: these fail CI |
| `baseline=` | Violations already in `check-baseline.json`: shown, not counted |
| `probes=` | Requests sent (R1-R5), contracts run (R6), or tests run (`regression`) |
| `[violation] ...` | One line per new violation, naming the endpoint or the import chain |
| exit code | 0 no new violation, 3 a new violation, 1 an error |

Add `--json` for one JSON document with every finding; that is also the baseline format.

The testgen output: a kept test asserts what the code does today, so it guards against future
regressions but cannot catch a fault that is already in the code (B12, F-b-41). Review each kept
test as code before you commit it. A discarded test's line names the filter that rejected it;
without mutants, filter 3 keeps only tests that add line coverage, so on a well-covered module most
proposed tests are discarded there (`skills/assured-tests/SKILL.md`).

In the worked example, `testgen-report.json` lists the kept tests and one result per filter per
test. Captured on 2026-10-17, run r-20261017-121823-aa1c4b, from
`/tmp/boltons-queueutils-testgen/testgen-report.json`; cut to the first test's five results; your
output will differ:

```json
  "run_id": "r-20261017-121823-aa1c4b",
  "status": "completed",
  "unsandboxed": true,
  "kept": [
    "tests/test_queueutils_generated.py::test_priority_updates_preserve_order_for_equal_priorities",
    "tests/test_queueutils_generated.py::test_remove_and_empty_queue_defaults",
    "tests/test_queueutils_generated.py::test_custom_priority_key_and_unexpected_keyword"
  ],
  "results": [
    {"test_id": "...::test_priority_updates_preserve_order_for_equal_priorities", "filter": 1, "passed": true, "reason": "collected 1 test"},
    {"test_id": "...", "filter": 2, "passed": true, "reason": "passed 5 of 5 runs"},
    {"test_id": "...", "filter": 3, "passed": true, "reason": "adds 5 covered lines: boltons/queueutils.py:134,163-165,170"},
    {"test_id": "...", "filter": 4, "passed": true, "reason": "has real assertions and does not mock boltons.queueutils"},
    {"test_id": "...", "filter": 5, "passed": true, "reason": "no source file changed during the test phase"},
```

The other two kept tests passed filter 3 by adding 9 covered lines (`boltons/queueutils.py:163-170,183`)
and 1 covered line (`boltons/queueutils.py:114`). The kept tests are in one file,
`tests/test_queueutils_generated.py`, under the `--out` folder; review it before you copy it into your
repository. (The JSON above is reformatted to one result per line and the repeated test ids are
shortened to `...`; the values are unchanged.)

What to do when a result surprises you: rerun the check alone (`--rules R6`) to see one rule's
findings; for testgen, open `testgen-report.json` and read the reason recorded for each test.

## Step 7: Decide which layers earn their place

What it is: the course's harness has four layers: instructions (S1), state and session lifecycle
(S2), scope and sandbox (S3), and verification (S4). Not every repository needs all of them in full.
A3's method is to remove "one component at a time" and review "what impact it had on the final
result" (A3, F-a-125). On TeamTrack, `make demo-2 LAYERS=-state` does that for you
([after-class.md](after-class.md), costs money). On your own repository there is no A/B runner, so
decide per layer from what it prevents and what it costs to keep current.

Each layer encodes an assumption about what the model cannot do on its own; A3 says "those
assumptions are worth stress testing" (A3, F-a-124). The course pilot is a worked case: on TeamTrack
with gpt-6-luna, no section showed a measurable difference on its primary measure, and the harness
arms ran longer and cost more per run. Post hoc (measures chosen after the results, not tested): on
F4, bare arms changed files outside the allowed paths in 6 of 6 runs and harness arms with the scope
layer in 0 of 6 (README, [How the course measures it](../README.md#4-how-the-course-measures-it)). A result like that is a reason to keep a layer small
and cheap, or to measure it on your own failures, not a reason to keep it by default.

| Layer | Kit files | The worked example's decision | Why |
|---|---|---|---|
| S1 Instructions | `AGENTS.md`, `ARCHITECTURE.md`, `docs/` | kept, smaller | The map and the layering rule are short; six TeamTrack documents were deleted because nothing in a library uses them |
| S2 State and session lifecycle | `progress.md`, `session-handoff.md`, `init.sh`, exec plans | kept | One feature can still span sessions; the test step of `init.sh` took 0.73 s in step 3 |
| S3 Scope and sandbox | `feature_list.json`, `harness/sandbox-policy.toml` | feature list kept; policy kept as reference | One feature at a time; no container is used for this repository yet |
| S4 Verification | `harness/`, `docs/clean-state-checklist.md`, the CI workflow, testgen | kept | The layering check failed on a seeded violation (step 4) and costs nothing to run |

How to check your decision: write it down in `docs/PLANS.md` with the date, and revisit it when an
agent makes a mistake the dropped layer would have caught. The failure each part prevents is listed
in `skills/harness-setup/references/failure-modes.md`.

## When something goes wrong

| Symptom | Fix |
|---|---|
| `x target directory not found` | Create the repository folder, or fix `--target` |
| `! skipped <file>` | Your file exists; merge by hand or pass `--force` |
| `--check` still lists markers you removed | You removed text but not the whole marker line; delete the line |
| `ModuleNotFoundError: No module named 'shipharness_adapter'` | Run from the repository root with `PYTHONPATH=harness` |
| `check crashed: AttributeError: ... no attribute 'create_app'` | A dropped rule is still in `--rules` |
| `x OPENAI_API_KEY is missing` | Add the key to `.env` in the shipharness checkout |

More on the commands: [final-project/README.md, part 9](../final-project/README.md#9-run-shipharness-on-your-own-repository).
More on the kit itself: [kit/README.md](../kit/README.md).
