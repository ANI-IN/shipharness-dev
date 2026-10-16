# skill-template

A starting point for writing your own Agent Skill. A skill is a folder with a `SKILL.md` file:
YAML frontmatter, then Markdown instructions, plus optional `scripts/`, `references/`, and
`assets/` folders (B1, F-b-01). This page covers two uses: copying the folder by hand to write a new
skill, and installing it in Claude Code, Codex, or Cursor so the agent does the copying for you.
The template itself is [SKILL.md](SKILL.md).

Source ids (A4, B1, ...) and finding ids (F-b-02, ...) refer to the course reference list,
`REFERENCES.md` at the repository root.

## What it does and when to use it

`SKILL.md` holds frontmatter with the specification's fields (the optional ones commented out) and
a body with the sections a skill needs: what it does, when to use it, steps, and checks before you
finish. Every `<placeholder>` is meant to be replaced. Use it when you want an agent to follow the
same procedure every time for a task your team repeats, and you want that procedure to load in
Claude Code, Codex, and Cursor alike.

## What is in the folder

| Path | What it is |
|---|---|
| `SKILL.md` | Frontmatter and body skeleton with placeholders |
| `scripts/.gitkeep` | Placeholder; put Python scripts the steps run here |
| `references/.gitkeep` | Placeholder; put detail loaded only when a step needs it here |
| `assets/.gitkeep` | Placeholder; put templates and static files the steps copy here |
| `README.md` | This page; not part of the skill's instructions |

## 1. Copy and name it

Run from the root of your shipharness checkout:

```bash
cp -r skills/skill-template skills/my-skill
```

```powershell
Copy-Item -Recurse skills\skill-template skills\my-skill
```

Then set `name: my-skill` in `skills/my-skill/SKILL.md`. Until you do, validation fails, because the
name must equal the folder name. Captured on 2026-10-17 from
`uv run shipharness skills validate <copy>/my-skill` at commit 5e8fb08, on a copy named `my-skill` with
the name not yet changed; your output will differ:

```text
x my-skill: Directory name 'my-skill' must match skill name 'skill-template'
1 skill checked, 1 error, 0 warnings
Cost: $0.000000 (no model calls)
```

The specification's rules for `name`: 1-64 characters, lowercase letters, digits, and hyphens
only, no hyphen at the start or end, no two hyphens in a row, and equal to the folder name (B1,
F-b-02). `shipharness skills validate` reads "letters" as ASCII `a-z`. Delete the `.gitkeep` files
in folders you fill, delete folders you do not use, and replace the copied `README.md` with one
for your skill or delete it.

## 2. Write the description

Agents load only `name` and `description` for every installed skill at startup, and read the rest
of `SKILL.md` only when a task matches the description (B1, B2, F-b-05). So the description decides
whether the skill is ever used:

- Say what the skill does and when to use it, in at most 1024 characters (B1, F-b-03).
- Use the words a user would type for that task.
- Start the "when" part with "Use when".
- If a plain value contains `: `, quote it or use a `>` block, as in the template. Otherwise YAML
  parsers, including the reference validator's, reject the frontmatter.

Only six frontmatter fields are allowed: `name`, `description`, `license`, `compatibility` (at most
500 characters), `metadata` (a map of strings to strings), and `allowed-tools` (experimental) (B1,
F-b-04). The reference validator rejects any other field (B5, F-b-11). Claude Code documents extra
frontmatter fields of its own (B7, F-b-13); a skill that uses them fails the reference validator,
so put such data under `metadata`, or accept that the skill is Claude Code only.

## 3. Write the body

- Keep `SKILL.md` under 500 lines; the specification recommends under 5000 tokens for the
  instructions (B1, F-b-06).
- Write steps the agent can follow and check: exact commands, the output to expect, what to do
  when it differs.
- Move detail into `references/` and link each file from `SKILL.md` with a relative path from the
  skill folder. Keep references one level deep: a reference file should not send the agent to
  another reference file (B1, F-b-07).
- Put templates and static files in `assets/`.
- Write scripts in Python. Make them deterministic, give them `--help`, keep their output to a few
  lines, and print `ERROR <reason>` on one line when something fails, so the agent can grep for it
  (A4, F-a-131, F-a-132).

## 4. Check the files

```bash
uv run shipharness skills validate skills/my-skill
uv run agentskills validate skills/my-skill
```

For the template folder itself, captured on 2026-10-17 from
`uv run shipharness skills validate skills/skill-template` at commit 5e8fb08; your output will differ:

```text
+ skill-template: valid (SKILL.md 46 lines)
1 skill checked, 0 errors, 0 warnings
Cost: $0.000000 (no model calls)
```

`uv run agentskills validate skills/skill-template` printed `Valid skill: skills/skill-template`
(captured on 2026-10-17 from that command at commit 5e8fb08; your output will differ).

- `shipharness skills validate` reports errors for everything the reference validator checks, and
  warnings for a `SKILL.md` over 500 lines, reference chains deeper than one level, and referenced
  files that do not exist. It exits 1 when there is an error. Point it at `skills/` to check every
  skill at once.
- `agentskills validate` is the reference validator, skills-ref 0.1.1 from PyPI (a dev dependency
  of this repository). Its README calls the command `skills-ref validate`; the PyPI package installs
  it under the name `agentskills`. Its README says it is "intended for demonstration purposes only"
  (B5, F-b-10).

The validators check the files. Whether an agent loads and follows the skill is a separate test;
see "Use it" below.

## 5. Install it

The Agent Skills specification does not say where skills live; each agent has its own folders
(B3, F-b-08). These are the folders each tool documents, checked on its official page on
2026-10-17. Replace `<name>` with the skill's folder name (`my-skill`, or `skill-template` to
install the template itself).

| Tool | Project folder | User-level folder | Reads `.claude/skills/` | Reads `.agents/skills/` |
|---|---|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | Yes | Not documented as of 2026-10-17 |
| Codex | `.agents/skills/<name>/` | `$HOME/.agents/skills/<name>/` | Not documented as of 2026-10-17 | Yes |
| Cursor 2.4 or later | `.agents/skills/<name>/` or `.cursor/skills/<name>/` | `~/.agents/skills/<name>/` or `~/.cursor/skills/<name>/` | Yes | Yes |

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
SKILL=my-skill          # or skill-template
TARGET=~/my-repo        # your repository; use TARGET=~ for a user-level install
mkdir -p "$TARGET/.claude/skills" "$TARGET/.agents/skills"
cp -r "skills/$SKILL" "$TARGET/.claude/skills/"
cp -r "skills/$SKILL" "$TARGET/.agents/skills/"
```

```powershell
$Skill = "my-skill"              # or skill-template
$Target = "C:\path\to\my-repo"   # your repository; use $Target = $HOME for a user-level install
New-Item -ItemType Directory -Force "$Target\.claude\skills", "$Target\.agents\skills" | Out-Null
Copy-Item -Recurse "skills\$Skill" "$Target\.claude\skills\"
Copy-Item -Recurse "skills\$Skill" "$Target\.agents\skills\"
```

With `TARGET=~` the same commands write `~/.claude/skills/<name>/` (Claude Code and Cursor) and
`~/.agents/skills/<name>/` (Codex and Cursor). To update an installed copy, delete it first and copy
again, so files removed from the skill do not linger. Cursor reads both folders; the course has not
checked which copy it uses when both hold the same name, so keep the two copies identical. Run the
validator on each installed copy after you change it, for example
`uv run shipharness skills validate ~/my-repo/.agents/skills/my-skill`.

## 6. Use it

| Tool | Call it by name | Let the agent choose it | See that it loaded |
|---|---|---|---|
| Claude Code | `/<name>` | Claude uses a skill when the task matches its description | Ask "What skills are available?", or type `/` and look for `/<name>` (B7, read 2026-10-17) |
| Codex (CLI or IDE extension) | Type `$<name>`, or run `/skills` and pick it | Codex can choose a skill when the task matches its description | Run `/skills` and look for it in the list (B8, read 2026-10-17) |
| Cursor | Type `/` in Agent chat and search for `<name>` | The agent applies a skill when it judges it relevant | Open **Customize** in the sidebar, then **Skills** (B9, read 2026-10-17) |

Example prompt with the template installed (prefix `/skill-template` in Claude Code or
`$skill-template` in Codex to call it by name):

```text
Create a new skill called release-notes from the skill template, in skills/release-notes/. It
should collect merged changes since the last tag and draft release notes in CHANGELOG.md. Set the
name and description, replace every placeholder, delete the folders it does not use, and run
uv run shipharness skills validate skills/release-notes until it reports 0 errors.
```

Then test the behaviour of the new skill: install it, ask for a task its description should match,
and check that the agent reads `SKILL.md` and follows the steps. Ask for a task it should not
match, and check that it does not.

## What it costs

The template and any skill you write from it run inside your own agent (Claude Code, Codex, or
Cursor), on that tool's model and your plan or API account with that vendor. The course does not
pay for it and has not measured how many tokens a run uses. Each installed skill adds its `name`
and `description` to the agent's context at startup, about 100 tokens per skill according to the
specification (B1, F-b-05). The shipharness validators print `Cost: $0.000000 (no model calls)`.

## Limits

- The template gives structure, not content. A skill is as good as its steps and checks.
- The reference validator is labelled for demonstration only (B5, F-b-10). Passing it shows that
  the frontmatter and layout follow the specification, not that any tool will load the skill.
- The specification is strict about the name, while its client guide tells agents to warn and load
  the skill anyway on a name and folder mismatch (B3, F-b-09). Do not rely on that leniency; keep
  the name equal to the folder name.
- The tool facts above come from each vendor's documentation as read on 2026-10-17. The course did
  not run skills inside Claude Code, Codex, or Cursor to confirm them; vendors change these pages,
  so check them again if a skill does not appear.

The other course skills are worked examples of this template:
[harness-setup](../harness-setup/README.md), [house-rules](../house-rules/README.md), and
[assured-tests](../assured-tests/README.md).

## Sources

- B1: Agent Skills Specification. https://agentskills.io/specification
- B2: What are skills? https://agentskills.io/what-are-skills
- B3: How to add skills support to your agent.
  https://agentskills.io/client-implementation/adding-skills-support.md
- B5, B6: skills-ref, the reference validator. https://github.com/agentskills/agentskills ;
  https://pypi.org/project/skills-ref/
- B7: Extend Claude with skills (Claude Code). https://code.claude.com/docs/en/skills
- B8: Build skills (Codex). https://learn.chatgpt.com/docs/build-skills
- B9: Agent Skills (Cursor docs). https://cursor.com/docs/skills (redirected from
  https://cursor.com/docs/context/skills on 2026-10-17)
- B10: Cursor 2.4 changelog. https://cursor.com/changelog/2-4
- A4: Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic,
  2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
