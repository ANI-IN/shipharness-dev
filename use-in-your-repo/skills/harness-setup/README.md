# harness-setup

An Agent Skill that checks a repository's harness for coding agents and fills the gaps from
templates. A skill is a folder with a `SKILL.md` file (YAML frontmatter, then Markdown
instructions) and optional `scripts/`, `references/`, and `assets/` folders (B1, F-b-01). This page
says what the skill does, how to install it in Claude Code, Codex, and Cursor, how to call it, and
how to check that it loaded. The instructions the agent follows are in [SKILL.md](SKILL.md).

Source ids (A1, B1, ...) and finding ids (F-b-12, ...) refer to the course reference list,
`REFERENCES.md` at the repository root.

## What it does and when to use it

The course describes the harness as "the environment around the agent": what the agent can read,
what it remembers between sessions, what it may change, and what proves its work is done. The cited
basis is A1: engineers "design environments, specify intent, and build feedback loops" (A1,
F-a-02). The skill works in three steps:

1. Assess. `scripts/assess.py` reads the repository and writes an HTML report with one row per
   check across five areas (instructions, state, scope, verification, session lifecycle). The
   areas are the course's way of grouping the checks; each check names the source it comes from.
2. Fill the gaps. For each failing check, the agent copies a template from `assets/templates/`,
   replaces every placeholder with facts about your repository, and runs each command it writes
   down.
3. Assess again and compare.

Use it:

- before you hand a repository to a coding agent for work that spans more than one session;
- when an agent breaks rules that are written somewhere it does not look (A1: "anything it can’t
  access in-context while running effectively doesn’t exist", F-a-05);
- when a new session repeats or undoes the last session's work (A2: "each new session begins with
  no memory of what came before", F-a-08).

## What is in the folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent loads when the skill is used |
| `scripts/assess.py` | The read-only assessment; Python 3.10+ standard library only |
| `references/instructions.md`, `state.md`, `scope.md`, `verification.md`, `session-lifecycle.md` | One checklist per area, with the reason for each check |
| `references/docs-layout.md`, `failure-modes.md` | Where the files go, and what each part prevents |
| `assets/templates/` | `AGENTS.md`, `ARCHITECTURE.md`, `SECURITY.md`, `feature_list.json` and its schema, `progress.md`, `session-handoff.md`, `exec-plan.md`, `clean-state-checklist.md`, `init.sh` |

Agents load only the `name` and `description` of every installed skill at startup and read the
rest of `SKILL.md` when a task matches the description; reference files are read only when a step
needs them (B1, B2, F-b-05).

## Install

The Agent Skills specification does not say where skills live; each agent has its own folders
(B3, F-b-08). These are the folders each tool documents, checked on its official page on
2026-10-17.

| Tool | Project folder | User-level folder | Reads `.claude/skills/` | Reads `.agents/skills/` |
|---|---|---|---|---|
| Claude Code | `.claude/skills/harness-setup/` | `~/.claude/skills/harness-setup/` | Yes | Not documented as of 2026-10-17 |
| Codex | `.agents/skills/harness-setup/` | `$HOME/.agents/skills/harness-setup/` | Not documented as of 2026-10-17 | Yes |
| Cursor 2.4 or later | `.agents/skills/harness-setup/` or `.cursor/skills/harness-setup/` | `~/.agents/skills/harness-setup/` or `~/.cursor/skills/harness-setup/` | Yes | Yes |

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
SKILL=harness-setup
TARGET=~/my-repo        # your repository; use TARGET=~ for a user-level install
mkdir -p "$TARGET/.claude/skills" "$TARGET/.agents/skills"
cp -r "skills/$SKILL" "$TARGET/.claude/skills/"
cp -r "skills/$SKILL" "$TARGET/.agents/skills/"
```

```powershell
$Skill = "harness-setup"
$Target = "C:\path\to\my-repo"   # your repository; use $Target = $HOME for a user-level install
New-Item -ItemType Directory -Force "$Target\.claude\skills", "$Target\.agents\skills" | Out-Null
Copy-Item -Recurse "skills\$Skill" "$Target\.claude\skills\"
Copy-Item -Recurse "skills\$Skill" "$Target\.agents\skills\"
```

With `TARGET=~` the same commands write `~/.claude/skills/harness-setup/` (Claude Code and Cursor)
and `~/.agents/skills/harness-setup/` (Codex and Cursor). To update an installed copy, delete it
first and copy again, so files removed from the skill do not linger. Cursor reads both folders;
the course has not checked which copy it uses when both hold the same name, so keep the two copies
identical.

## Check the files before you start an agent

Run the course validator on the source folder and on each installed copy:

```bash
uv run shipharness skills validate skills/harness-setup
uv run shipharness skills validate ~/my-repo/.claude/skills/harness-setup
uv run shipharness skills validate ~/my-repo/.agents/skills/harness-setup
```

Captured on 2026-10-17 from `uv run shipharness skills validate skills/harness-setup`;
your output will differ:

```text
+ harness-setup: valid (SKILL.md 103 lines)
1 skill checked, 0 errors, 0 warnings
Cost: $0.000000 (no model calls)
```

`shipharness skills validate` runs the checks of skills-ref, the reference validator, and adds
warnings for a `SKILL.md` over 500 lines, reference chains deeper than one level, and missing
referenced files (B1, B5, F-b-06, F-b-07, F-b-10, F-b-11). The skill uses only the six frontmatter
fields the specification allows, so it also passes the reference validator itself,
`uv run agentskills validate skills/harness-setup` (captured on 2026-10-17 from that command: `Valid skill: skills/harness-setup`; your output will differ).

The validators check the files. They do not show that a tool loaded the skill; for that, see the
next section.

## Use it

| Tool | Call it by name | Let the agent choose it | See that it loaded |
|---|---|---|---|
| Claude Code | `/harness-setup` | Claude uses a skill when the task matches its description | Ask "What skills are available?", or type `/` and look for `/harness-setup` (B7, read 2026-10-17) |
| Codex (CLI or IDE extension) | Type `$harness-setup`, or run `/skills` and pick it | Codex can choose a skill when the task matches its description | Run `/skills` and look for it in the list (B8, read 2026-10-17) |
| Cursor | Type `/` in Agent chat and search for `harness-setup` | The agent applies a skill when it judges it relevant | Open **Customize** in the sidebar, then **Skills** (B9, read 2026-10-17) |

Example prompt, the same in all three tools (prefix `/harness-setup` in Claude Code or
`$harness-setup` in Codex to call it by name):

```text
Assess this repository's harness for coding agents. Write the report to
harness-assessment.html, then fill the failing checks area by area from the skill's templates.
Run every command you write into AGENTS.md, init.sh, and the clean-state checklist before you
commit. Assess again at the end and list any check still failing with the reason.
```

The agent runs the script from the installed folder, for example
`python .claude/skills/harness-setup/scripts/assess.py . --out harness-assessment.html` in Claude
Code or `python .agents/skills/harness-setup/scripts/assess.py . --out harness-assessment.html` in
Codex. You can run it yourself first. This is the summary it printed for the course's TeamTrack
app, cut to the first lines; captured on 2026-10-17 from
`uv run python skills/harness-setup/scripts/assess.py teamtrack --out harness-assessment.html` (run
from the checkout root); your output will differ:

```text
Instructions       pass 0  partial 1  fail 5
State              pass 0  partial 0  fail 4
Scope              pass 1  partial 1  fail 3
Verification       pass 1  partial 1  fail 3
Session lifecycle  pass 0  partial 0  fail 5
FAIL     I1 AGENTS.md map at the repository root: no AGENTS.md at the repository root
```

TeamTrack has no harness files at its root on purpose: in the course A/B the bare arm works without
them, and the harness arm has `AGENTS.md` placed at the workspace root from
`teamtrack/harness/instructions/`. So most checks fail on the app folder itself.

## What it costs

The skill runs inside your own agent (Claude Code, Codex, or Cursor), on that tool's model and your
plan or API account with that vendor. The course does not pay for it and has not measured how
many tokens a run uses. `scripts/assess.py` makes no model or network calls; the cost is the
agent's own work reading the report and writing the files. The shipharness validators print
`Cost: $0.000000 (no model calls)`.

## Limits

- Keyword checks (for example "does AGENTS.md mention init.sh") are heuristics, and the report says
  so in their evidence.
- The script reads files only. It never runs the repository's code, so it cannot tell whether
  `init.sh` or the test command works; rule 3 in `SKILL.md` asks the agent to run each one.
- The templates write rules down; they do not enforce them. A1: "When documentation falls short,
  we promote the rule into code" (F-a-43). Use [house-rules](../house-rules/README.md) to turn a
  rule into a check and [assured-tests](../assured-tests/README.md) to add tests that are kept only
  when they prove something.
- `evidence` and `testedAt` in the feature list template are course additions to A2's design, as
  is the rule that only the harness sets `passes` to true (course design, built on A2 and A3).
- The tool facts above come from each vendor's documentation as read on 2026-10-17. The course did
  not run the skill inside Claude Code, Codex, or Cursor to confirm them; vendors change these
  pages, so check them again if a skill does not appear.

## Sources

- A1: Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI,
  2026-02-11. https://openai.com/index/harness-engineering/
- A2: Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- A3: Prithvi Rajasekaran, "Harness design for long-running application development", Anthropic,
  2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps
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
