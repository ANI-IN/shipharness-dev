# Extend Claude with skills, Build skills, and Agent Skills in Cursor

Reading time: about 5 minutes.
Source: the skills pages of Claude Code <https://code.claude.com/docs/en/skills>, Codex <https://learn.chatgpt.com/docs/build-skills>, and Cursor <https://cursor.com/docs/skills>, read 2026-10-17 ([evidence](../../docs/evidence/s1.md#src-claude-code-skills)).

> **Terms on this page**
>
> - **Agent Skill**: A folder with a `SKILL.md` recipe that the agent loads only when a task needs it.
> - **Entry point**: The small text an agent always gets first: a map, a session prompt, or a skills catalogue.
> - **Loader**: The part of an agent that finds skills on disk and builds its catalogue.

## Why it matters

You will use what Section 1 teaches in an agent other than shipharness. Each agent finds its skills
in its own folders. A skill in a folder your agent never scans does not exist for that agent.

## Three key ideas

1. **Every harness uses a small entry point.** OpenAI's team gives Codex a short `AGENTS.md` "injected
   into context" as a map ([OpenAI](../../docs/evidence/s1.md#src-openai-harness)). Anthropic's
   long-running harness tells each session where to look first: "Read the git logs and progress files
   to get up to speed on what was recently worked on."
   ([Anthropic](../../docs/evidence/s1.md#src-anthropic-long-running)) Skills start as a catalogue of
   names and descriptions.

2. **Who builds the entry point differs.** In shipharness the harness code puts the map into context,
   from a copy the agent cannot edit. In Claude Code, Codex, and Cursor, the agent's own loader scans
   folders and builds the catalogue. There, your job is to put the files where the loader looks.

3. **No single folder works for all three.** Claude Code scans `.claude/skills/` from the start
   folder up to the repository root, and its page does not mention `.agents/skills/`. Codex scans
   `.agents/skills` in every folder from the working folder up to the repository root. Cursor reads
   `.agents/skills/` and `.cursor/skills/`, and also the Claude and Codex folders.

Where each agent looks for skills, from its own page:

| Agent | Project skills | User skills |
|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| Codex | `.agents/skills` | `$HOME/.agents/skills` |
| Cursor (2.4 and later) | `.agents/skills/`, `.cursor/skills/` | `~/.agents/skills/`, `~/.cursor/skills/` |

## Apply it to your repo

1. Decide who builds the entry point. If your agent loads `AGENTS.md` and skills itself, your work is
   the files and their folders. If you run your own harness, you also decide what goes in the first
   message and whether the agent can change it.
2. To reach all three agents, install each skill in both `.claude/skills/<name>/` and
   `.agents/skills/<name>/`. That is the course's reading of the table, not a sentence from one page.
3. Keep one source and copy the rest. Two copies of a skill drift; a small script that compares them
   is the kind of check OpenAI's team runs on its docs.
4. Put vendor-specific data under `metadata`, so the skill keeps to the six standard fields.
5. Test discovery: start your agent and ask it. Claude Code's page suggests "What skills are
   available?".
