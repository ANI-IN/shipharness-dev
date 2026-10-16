# assured-tests

An Agent Skill that generates unit tests for one Python module and keeps only the tests that pass
five filters. A skill is a folder with a `SKILL.md` file (YAML frontmatter, then Markdown
instructions) and optional `scripts/`, `references/`, and `assets/` folders (B1, F-b-01). This page
says what the skill does, how to install it in Claude Code, Codex, and Cursor, how to call it, and
how to check that it loaded. The instructions the agent follows are in [SKILL.md](SKILL.md).

Source ids (B11, B12, ...) and finding ids (F-b-16, ...) refer to the course reference list,
`REFERENCES.md` at the repository root.

## What it does and when to use it

A generated test can fail on correct code, pass by luck, or pass without checking anything.
TestGen-LLM at Meta runs every candidate through "progressively demanding semantic filters" and
keeps only the survivors (B11, F-b-16, F-b-21). This skill applies the same idea. Its script runs
`shipharness testgen`, which proposes tests with a model and keeps a test only if it passes all
five filters, cheapest first:

| # | Filter | Source |
|---|---|---|
| 1 | Imports and runs: pytest collects it with no errors | B11, "buildable" (F-b-17) |
| 2 | Passes on every one of five runs | B11 (F-b-18, F-b-19) |
| 3 | Adds line coverage, or kills a mutant no existing test kills | B11 (F-b-20); B12 (F-b-29, F-b-32) |
| 4 | Has real assertions and does not mock the unit under test | Course filter; no direct source |
| 5 | No source file changed during the test phase | Course filter, built on B11 (F-b-22) and A2 (F-a-80) |

Filters 4 and 5 are the course's own additions and are presented as such. The agent then reads the
result table (one row per proposed test, with the first filter it failed and why) and reviews the
kept tests as code.

Use it when a module has thin coverage and you want tests that are proven to add something; when
you want to protect a specific behaviour (tenant isolation, permission checks) against a known
kind of fault by writing mutants for that fault (B12); or when you want to compare filtered tests
with what an agent writes unfiltered (`--layers none`).

## What is in the folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent loads when the skill is used |
| `scripts/run_testgen.py` | Builds and runs the `shipharness testgen` command; `--dry-run` prints it without running; Python 3.10+ standard library only |
| `references/filters.md` | Why each filter exists and what it cannot catch |
| `references/testgen-llm.md`, `references/ach.md` | Short summaries of the two papers (B11, B12) |

Agents load only the `name` and `description` of every installed skill at startup and read the
rest of `SKILL.md` when a task matches the description; reference files are read only when a step
needs them (B1, B2, F-b-05).

## What you need

- Python 3.12+, uv, and the shipharness CLI with an OpenAI key (the skill's `compatibility` field).
  The script calls `shipharness` if it is on your PATH and `uv run shipharness` otherwise, which
  works from inside the shipharness checkout.
- A repository with a pytest suite, and coverage.py configured (filter 3 measures line coverage).
- Docker, if you want generated tests to run in a container (`--sandbox docker --image <image>`).
  Without it, generated tests run on your machine with your permissions, and both the script and
  shipharness say UNSANDBOXED. Use a container for any repository you do not trust.

## Install

The Agent Skills specification does not say where skills live; each agent has its own folders
(B3, F-b-08). These are the folders each tool documents, checked on its official page on
2026-10-17.

| Tool | Project folder | User-level folder | Reads `.claude/skills/` | Reads `.agents/skills/` |
|---|---|---|---|---|
| Claude Code | `.claude/skills/assured-tests/` | `~/.claude/skills/assured-tests/` | Yes | Not documented as of 2026-10-17 |
| Codex | `.agents/skills/assured-tests/` | `$HOME/.agents/skills/assured-tests/` | Not documented as of 2026-10-17 | Yes |
| Cursor 2.4 or later | `.agents/skills/assured-tests/` or `.cursor/skills/assured-tests/` | `~/.agents/skills/assured-tests/` or `~/.cursor/skills/assured-tests/` | Yes | Yes |

What each page says:

- Claude Code reads personal skills from `~/.claude/skills/<skill-name>/SKILL.md` and project
  skills from `.claude/skills/<skill-name>/SKILL.md`, in the folder where you start it and in every
  parent folder up to the repository root. If the same name exists at both levels, the personal
  skill wins. Claude Code watches these folders and picks up added or edited skills without a
  restart; if the `.claude/skills/` folder did not exist when the session started, run
  `/reload-skills`. The page does not mention `.agents/skills/`. (B7, F-b-12;
  https://code.claude.com/docs/en/skills, read 2026-10-17.)
- Codex scans `.agents/skills` in every folder from the working directory up to the repository
  root, then `$HOME/.agents/skills` and `/etc/codex/skills`. It detects new skills automatically;
  if one does not appear, restart Codex. It follows symlinked skill folders. The page does not
  mention `.claude/skills/`. (B8, F-b-14; https://learn.chatgpt.com/docs/build-skills, redirected
  from https://developers.openai.com/codex/skills, read 2026-10-17.)
- Cursor reads `.agents/skills/` and `.cursor/skills/` in the project and `~/.agents/skills/` and
  `~/.cursor/skills/` in your home folder, and for compatibility also `.claude/skills/`,
  `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`. It discovers skills when it
  starts. (B9, F-b-15; https://cursor.com/docs/skills, redirected from
  https://cursor.com/docs/context/skills, read 2026-10-17.) Skills arrived in
  Cursor 2.4, released 2026-01-22, "in the editor and CLI" (B10;
  https://cursor.com/changelog/2-4, read 2026-10-17). The page does not say whether a skill added
  while Cursor is open appears without a restart (not documented as of 2026-10-17); restart Cursor
  if it does not appear.

No single folder is documented for all three tools. Copy the skill into both `.claude/skills/` and
`.agents/skills/`: Claude Code reads the first, Codex the second, and Cursor both. Run these from
the root of your shipharness checkout:

```bash
SKILL=assured-tests
TARGET=~/my-repo        # your repository; use TARGET=~ for a user-level install
mkdir -p "$TARGET/.claude/skills" "$TARGET/.agents/skills"
cp -r "skills/$SKILL" "$TARGET/.claude/skills/"
cp -r "skills/$SKILL" "$TARGET/.agents/skills/"
```

```powershell
$Skill = "assured-tests"
$Target = "C:\path\to\my-repo"   # your repository; use $Target = $HOME for a user-level install
New-Item -ItemType Directory -Force "$Target\.claude\skills", "$Target\.agents\skills" | Out-Null
Copy-Item -Recurse "skills\$Skill" "$Target\.claude\skills\"
Copy-Item -Recurse "skills\$Skill" "$Target\.agents\skills\"
```

With `TARGET=~` the same commands write `~/.claude/skills/assured-tests/` (Claude Code and Cursor)
and `~/.agents/skills/assured-tests/` (Codex and Cursor). To update an installed copy, delete it
first and copy again, so files removed from the skill do not linger. Cursor reads both folders;
the course has not checked which copy it uses when both hold the same name, so keep the two copies
identical.

## Check the files before you start an agent

Run the course validator on the source folder and on each installed copy:

```bash
uv run shipharness skills validate skills/assured-tests
uv run shipharness skills validate ~/my-repo/.claude/skills/assured-tests
uv run shipharness skills validate ~/my-repo/.agents/skills/assured-tests
```

Captured on 2026-10-17 from `uv run shipharness skills validate skills/assured-tests` at commit 5e8fb08;
your output will differ:

```text
+ assured-tests: valid (SKILL.md 96 lines)
1 skill checked, 0 errors, 0 warnings
Cost: $0.000000 (no model calls)
```

`shipharness skills validate` runs the checks of skills-ref, the reference validator, and adds
warnings for a `SKILL.md` over 500 lines, reference chains deeper than one level, and missing
referenced files (B1, B5, F-b-06, F-b-07, F-b-10, F-b-11). The skill uses only the six frontmatter
fields the specification allows, so it also passes the reference validator itself,
`uv run agentskills validate skills/assured-tests` (captured on 2026-10-17 from that command at commit
5e8fb08: `Valid skill: skills/assured-tests`; your output will differ).

The validators check the files. They do not show that a tool loaded the skill; for that, see the
next section.

## Use it

| Tool | Call it by name | Let the agent choose it | See that it loaded |
|---|---|---|---|
| Claude Code | `/assured-tests` | Claude uses a skill when the task matches its description | Ask "What skills are available?", or type `/` and look for `/assured-tests` (B7, read 2026-10-17) |
| Codex (CLI or IDE extension) | Type `$assured-tests`, or run `/skills` and pick it | Codex can choose a skill when the task matches its description | Run `/skills` and look for it in the list (B8, read 2026-10-17) |
| Cursor | Type `/` in Agent chat and search for `assured-tests` | The agent applies a skill when it judges it relevant | Open **Customize** in the sidebar, then **Skills** (B9, read 2026-10-17) |

Example prompt, the same in all three tools (prefix `/assured-tests` in Claude Code or
`$assured-tests` in Codex to call it by name):

```text
Add assured tests for app/services/members.py. Run the existing suite first and tell me about
any failures. Preview the testgen command with --dry-run and wait for my go-ahead before the real
run, because it calls a model. Then explain every discarded test by the first filter it failed,
and review the kept tests as code.
```

The agent runs the script from the installed folder, for example
`python .claude/skills/assured-tests/scripts/run_testgen.py --repo . --module <path> --max-tests 8 --dry-run`.
Captured on 2026-10-17 against the course's TeamTrack app from
`python3 skills/assured-tests/scripts/run_testgen.py --repo teamtrack --module app/services/members.py --max-tests 8 --dry-run`
(run from the checkout root, with no `shipharness` on the PATH, so the script falls back to
`uv run shipharness`) at commit 5e8fb08; your output will differ:

```text
command: uv run shipharness testgen --repo teamtrack --module app/services/members.py --layers verify --max-tests 8
note: UNSANDBOXED. Generated tests will run on this machine with your permissions. Use --sandbox docker --image <image> to run them in a container.
note: this calls a model and costs money; the command prints a Cost: line at the end.
```

The dry run makes no model calls. The real run, without `--dry-run`, does; this README shows no
captured output from one.

## What it costs

Two things cost money, and both are yours:

- The skill runs inside your own agent (Claude Code, Codex, or Cursor), on that tool's model and
  your plan or API account with that vendor. The course does not pay for it and has not measured
  how many tokens a run uses.
- `shipharness testgen` calls the OpenAI API with your key. It prints `Cost: $X` when it ends and
  stops at the per-run cost cap, `MAX_RUN_COST_USD`, whose default is $0.20
  (`src/shipharness/config/settings.py`). The course has no typical cost per testgen run to quote.
  When LangSmith tracing is on and `LANGSMITH_API_KEY` is set, the run is also traced to the
  `shipharness-testgen` project, which counts against your LangSmith trace allowance.

## Limits

- The current code is the oracle. A kept test asserts what the code does today, so it protects
  against future regressions, but it "cannot detect existing faults residing in the code base"
  (B12, F-b-41).
- Five runs catch most flaky tests, not all of them. The number five is TestGen-LLM's (B11).
- The filters prove a test runs reliably and adds coverage or catches a mutant. They do not prove
  that its name and assertions describe the behaviour you want; review kept tests as code.
- On a well-tested module most proposals fail filter 3. That is expected; add mutants for the
  faults you care about and run again.
- Without `--sandbox docker`, generated tests run with your permissions on your machine.
- The tool facts above come from each vendor's documentation as read on 2026-10-17. The course did
  not run the skill inside Claude Code, Codex, or Cursor to confirm them; vendors change these
  pages, so check them again if a skill does not appear.

Related skills: [harness-setup](../harness-setup/README.md) checks whether coverage is configured
(check V5); [house-rules](../house-rules/README.md) turns a rule into a check with a seeded
violation.

## Sources

- B11: Alshahwan et al., "Automated Unit Test Improvement using Large Language Models at Meta",
  FSE '24, arXiv 2402.09171. https://arxiv.org/abs/2402.09171
- B12: Foster et al., "Mutation-Guided LLM-based Test Generation at Meta", arXiv 2501.12862.
  https://arxiv.org/abs/2501.12862
- A2: Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- B1: Agent Skills Specification. https://agentskills.io/specification
- B2: What are skills? https://agentskills.io/what-are-skills
- B3: How to add skills support to your agent.
  https://agentskills.io/client-implementation/adding-skills-support.md
- B5: skills-ref, the reference validator. https://github.com/agentskills/agentskills
- B7: Extend Claude with skills (Claude Code). https://code.claude.com/docs/en/skills
- B8: Build skills (Codex). https://learn.chatgpt.com/docs/build-skills
- B9: Agent Skills (Cursor docs). https://cursor.com/docs/skills (redirected from
  https://cursor.com/docs/context/skills on 2026-10-17)
- B10: Cursor 2.4 changelog. https://cursor.com/changelog/2-4
