# house-rules

An Agent Skill that turns a team convention into a house rule: a one-page rule document, a
mechanical check whose error message tells the agent how to fix the problem, and a test with a
seeded violation the check must catch. A skill is a folder with a `SKILL.md` file (YAML
frontmatter, then Markdown instructions) and optional `scripts/`, `references/`, and `assets/`
folders (B1, F-b-01). This page says what the skill does, how to install it in Claude Code, Codex,
and Cursor, how to call it, and how to check that it loaded. The instructions the agent follows
are in [SKILL.md](SKILL.md).

Source ids (A1, B1, ...) and finding ids (F-a-43, ...) refer to the course reference list,
`REFERENCES.md` at the repository root.

## What it does and when to use it

"House rules" is the course's label, not a source term. It stands for what A1 calls "golden
principles" encoded in the repository and "taste invariants" enforced with custom lints (A1,
F-a-96, F-a-99). The idea in one line, also from A1: "When documentation falls short, we promote
the rule into code" (F-a-43).

A house rule is done when all three parts exist:

1. A rule document with the rule in one checkable sentence, why it exists, and the smallest
   correct and incorrect examples.
2. A check that prints one line per violation saying what is wrong and how to fix it. A1 writes
   lint messages "to inject remediation instructions into agent context" (F-a-97), and A4 asks for
   "ERROR" with the reason "on the same line so grep will find it" (F-a-132).
3. A test with a seeded violation the check must catch and a clean case it must pass, written
   before the check.

Use it when the same review comment keeps coming back, when agents copy a pattern that should not
be copied (A1: agents replicate "patterns that already exist in the repository—even uneven or
suboptimal ones", F-a-20), or when a rule is written in the docs and agents still break it. Do not
use it for what a formatter already handles or for one-off decisions; A1 enforces invariants and
does not micromanage implementations (F-a-92).

## What is in the folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent loads when the skill is used |
| `scripts/new_rule.py` | Writes the rule document, a check stub, and a failing test stub; Python 3.10+ standard library only |
| `assets/rule-template.md` | The rule document template the script copies |

Agents load only the `name` and `description` of every installed skill at startup and read the
rest of `SKILL.md` when a task matches the description (B1, B2, F-b-05).

## Install

The Agent Skills specification does not say where skills live; each agent has its own folders
(B3, F-b-08). These are the folders each tool documents, checked on its official page on
2026-10-17.

| Tool | Project folder | User-level folder | Reads `.claude/skills/` | Reads `.agents/skills/` |
|---|---|---|---|---|
| Claude Code | `.claude/skills/house-rules/` | `~/.claude/skills/house-rules/` | Yes | Not documented as of 2026-10-17 |
| Codex | `.agents/skills/house-rules/` | `$HOME/.agents/skills/house-rules/` | Not documented as of 2026-10-17 | Yes |
| Cursor 2.4 or later | `.agents/skills/house-rules/` or `.cursor/skills/house-rules/` | `~/.agents/skills/house-rules/` or `~/.cursor/skills/house-rules/` | Yes | Yes |

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
SKILL=house-rules
TARGET=~/my-repo        # your repository; use TARGET=~ for a user-level install
mkdir -p "$TARGET/.claude/skills" "$TARGET/.agents/skills"
cp -r "skills/$SKILL" "$TARGET/.claude/skills/"
cp -r "skills/$SKILL" "$TARGET/.agents/skills/"
```

```powershell
$Skill = "house-rules"
$Target = "C:\path\to\my-repo"   # your repository; use $Target = $HOME for a user-level install
New-Item -ItemType Directory -Force "$Target\.claude\skills", "$Target\.agents\skills" | Out-Null
Copy-Item -Recurse "skills\$Skill" "$Target\.claude\skills\"
Copy-Item -Recurse "skills\$Skill" "$Target\.agents\skills\"
```

With `TARGET=~` the same commands write `~/.claude/skills/house-rules/` (Claude Code and Cursor)
and `~/.agents/skills/house-rules/` (Codex and Cursor). To update an installed copy, delete it
first and copy again, so files removed from the skill do not linger. Cursor reads both folders;
the course has not checked which copy it uses when both hold the same name, so keep the two copies
identical.

## Check the files before you start an agent

Run the course validator on the source folder and on each installed copy:

```bash
uv run shipharness skills validate skills/house-rules
uv run shipharness skills validate ~/my-repo/.claude/skills/house-rules
uv run shipharness skills validate ~/my-repo/.agents/skills/house-rules
```

Captured on 2026-10-17 from `uv run shipharness skills validate skills/house-rules`;
your output will differ:

```text
+ house-rules: valid (SKILL.md 94 lines)
1 skill checked, 0 errors, 0 warnings
Cost: $0.000000 (no model calls)
```

`shipharness skills validate` runs the checks of skills-ref, the reference validator, and adds
warnings for a `SKILL.md` over 500 lines, reference chains deeper than one level, and missing
referenced files (B1, B5, F-b-06, F-b-07, F-b-10, F-b-11). The skill uses only the six frontmatter
fields the specification allows, so it also passes the reference validator itself,
`uv run agentskills validate skills/house-rules` (captured on 2026-10-17 from that command: `Valid skill: skills/house-rules`; your output will differ).

The validators check the files. They do not show that a tool loaded the skill; for that, see the
next section.

## Use it

| Tool | Call it by name | Let the agent choose it | See that it loaded |
|---|---|---|---|
| Claude Code | `/house-rules` | Claude uses a skill when the task matches its description | Ask "What skills are available?", or type `/` and look for `/house-rules` (B7, read 2026-10-17) |
| Codex (CLI or IDE extension) | Type `$house-rules`, or run `/skills` and pick it | Codex can choose a skill when the task matches its description | Run `/skills` and look for it in the list (B8, read 2026-10-17) |
| Cursor | Type `/` in Agent chat and search for `house-rules` | The agent applies a skill when it judges it relevant | Open **Customize** in the sidebar, then **Skills** (B9, read 2026-10-17) |

Example prompt, the same in all three tools (prefix `/house-rules` in Claude Code or
`$house-rules` in Codex to call it by name):

```text
Make a house rule R8: soft-deleted rows never appear in list endpoints. Scaffold it with the
skill's script, write the seeded-violation test first and show me it failing, then write the
check until it passes. Run the check on the whole repository, put existing violations in the
baseline, and add the rule to AGENTS.md and CI.
```

The agent runs the script from the installed folder, for example
`python .claude/skills/house-rules/scripts/new_rule.py --id R8 --title "..." --root .`. You can
preview what it writes with `--dry-run`. Captured on 2026-10-17 against the course's TeamTrack app from
`uv run python skills/house-rules/scripts/new_rule.py --id R8 --title "Soft-deleted rows never appear" --root teamtrack --dry-run`
(run from the checkout root); your output will differ:

```text
would write docs/rules/R8-soft-deleted-rows-never-appear.md
would write checks/check_r8_soft_deleted_rows_never_appear.py
would write tests/test_check_r8_soft_deleted_rows_never_appear.py
```

## What it costs

The skill runs inside your own agent (Claude Code, Codex, or Cursor), on that tool's model and your
plan or API account with that vendor. The course does not pay for it and has not measured how
many tokens a run uses. `scripts/new_rule.py` makes no model or network calls; the cost is the
agent's own work writing the rule, the check, and the test. The shipharness validators print
`Cost: $0.000000 (no model calls)`.

## Limits

- The script writes stubs. The test stub fails on purpose until the agent writes the seeded
  violation, and the check stub finds nothing until the agent writes `check()`.
- A check is only as exact as the method you pick. A text search misses aliased imports; an `ast`
  walk misses behaviour that only shows at run time, which needs a probe against the running app.
- A baseline lets the rule apply to new code from today. The existing violations stay until
  someone removes them, so open a piece of work for each one.
- A rule that is not wired into CI and the gate before "done" is still only documentation. Step 7
  of `SKILL.md` covers this.
- The tool facts above come from each vendor's documentation as read on 2026-10-17. The course did
  not run the skill inside Claude Code, Codex, or Cursor to confirm them; vendors change these
  pages, so check them again if a skill does not appear.

Related skills: [harness-setup](../harness-setup/README.md) adds the map and docs a rule is linked
from; [skill-template](../skill-template/README.md) is the starting point for a skill of your own.

## Sources

- A1: Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI,
  2026-02-11. https://openai.com/index/harness-engineering/
- A4: Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic,
  2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
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
