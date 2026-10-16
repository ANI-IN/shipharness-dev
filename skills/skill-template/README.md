# Writing, testing, and installing a skill

This folder is a starting point for a new Agent Skill. A skill is a folder with a `SKILL.md` file:
YAML frontmatter, then Markdown instructions, plus optional `scripts/`, `references/`, and
`assets/` folders (B1). Source ids refer to the shipharness research register (RESEARCH.md §4.5).

## 1. Copy and name it

```bash
cp -r skills/skill-template skills/my-skill          # bash
```

```powershell
Copy-Item -Recurse skills/skill-template skills/my-skill   # PowerShell
```

Then set `name: my-skill` in `SKILL.md`. The spec's rules for `name` (B1): 1-64 characters,
lowercase letters, digits, and hyphens only, no hyphen at the start or end, no two hyphens in a
row, and equal to the folder name. `shipharness skills validate` reads "letters" as ASCII `a-z`.
Delete the `.gitkeep` files in folders you fill, and delete folders you do not use.

## 2. Write the description

Agents load only `name` and `description` for every installed skill at startup, about 100 tokens
each, and read the rest of `SKILL.md` only when a task matches the description (B1, B2). So the
description decides whether the skill is ever used:

- Say what the skill does and when to use it, in one paragraph of at most 1024 characters (B1).
- Use the words a user would type for that task.
- Start the "when" part with "Use when".
- If a plain value contains `: `, quote it or use a `>` block, as in the template. Otherwise YAML
  parsers, including the reference validator's, reject the frontmatter.

Only six frontmatter fields are allowed: `name`, `description`, `license`, `compatibility` (at most
500 characters), `metadata` (a map of strings to strings), and `allowed-tools` (experimental). The
reference validator rejects any other field, including vendor-specific ones; put such data under
`metadata` instead (B1, B5).

## 3. Write the body

- Keep `SKILL.md` under 500 lines; the spec recommends under 5000 tokens for the instructions (B1).
- Write steps the agent can follow and check: exact commands, the output to expect, what to do
  when it differs.
- Move detail into `references/` and link each file from `SKILL.md` with a relative path from the
  skill folder. Keep references one level deep: a reference file should not send the agent to
  another reference file (B1).
- Put templates and static files in `assets/`.
- Write scripts in Python. Make them deterministic, give them `--help`, keep their output to a few
  lines, and print `ERROR <reason>` on one line when something fails, so the agent can grep for it
  (A4, F-a-131, F-a-132).

## 4. Test it

```bash
uv run shipharness skills validate skills/my-skill
uv run agentskills validate skills/my-skill
```

- `shipharness skills validate` reports errors for everything the reference validator checks, and
  warnings for `SKILL.md` over 500 lines, reference chains deeper than one level, and referenced
  files that do not exist. It exits 1 when there is an error. Point it at `skills/` to check every
  skill at once.
- `agentskills validate` is the reference validator, skills-ref 0.1.1 from PyPI (a dev dependency
  of this repository). Its README calls the command `skills-ref validate`; the PyPI package installs
  it under the name `agentskills`. Its README marks it "for demonstration purposes only" (B5).
- Then test the behaviour: install the skill, ask the agent for a task the description should
  match, and check that it reads `SKILL.md` and follows the steps. Ask for a task it should not
  match, and check that it does not.

## 5. Install it

The spec does not say where skills live; each agent has its own folders (B3).

| Agent | Project folder | Personal folder | Source |
|---|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | B7 |
| Codex | `.agents/skills/<name>/`, scanned from the working directory up to the repository root | `$HOME/.agents/skills/<name>/` | B8 |
| Cursor 2.4 or later | `.agents/skills/<name>/` or `.cursor/skills/<name>/`; also reads the Claude Code and Codex folders | `~/.agents/skills/<name>/` or `~/.cursor/skills/<name>/` | B9, B10 |

No single folder is read by all three. To reach Claude Code, Codex, and Cursor from one project,
install the skill in both `.claude/skills/` and `.agents/skills/`:

```bash
mkdir -p .claude/skills .agents/skills
cp -r skills/my-skill .claude/skills/
cp -r skills/my-skill .agents/skills/
```

```powershell
New-Item -ItemType Directory -Force .claude/skills, .agents/skills | Out-Null
Copy-Item -Recurse skills/my-skill .claude/skills/
Copy-Item -Recurse skills/my-skill .agents/skills/
```

Run the validators again on the installed copies after you change them.

## Sources

- B1: Agent Skills Specification. https://agentskills.io/specification
- B2: What are skills? https://agentskills.io/what-are-skills
- B3: How to add skills support to your agent.
  https://agentskills.io/client-implementation/adding-skills-support.md
- B5, B6: skills-ref, the reference validator. https://github.com/agentskills/agentskills ;
  https://pypi.org/project/skills-ref/
- B7: Extend Claude with skills (Claude Code). https://code.claude.com/docs/en/skills
- B8: Build skills (Codex). https://learn.chatgpt.com/docs/build-skills
- B9, B10: Agent Skills (Cursor docs); Cursor 2.4 changelog. https://cursor.com/docs/context/skills ;
  https://cursor.com/changelog/2-4
- A4: Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic,
  2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
