# How instructions reach the agent in other harnesses

Reading time: about 5 minutes.

The S1 layer in `shipharness` does two things: it puts a short map in the context prefix, and it lists
skills by name and description so the agent can load the rest on demand. This piece compares that with
what the primary sources say about other harnesses: the two harnesses the teaching sources describe
(A1 at OpenAI, A2 and A5 at Anthropic) and the skill loading of three coding agents (B7-B10).

A note on wording: the vendor documentation pages (B7-B9) were read through a summarising fetch tool,
so RESEARCH G-11 requires each sentence to be copied again from the live page before it is quoted.
This piece therefore quotes none of them. The directory paths are reliable (G-11) and are given
exactly. Findings F-b-12 to F-b-15 are in `research/notes/R-b.md`.

---

## 1. A1: the Codex team's repository

A1 describes the harness around Codex for one internal product. The instruction file is `AGENTS.md`,
short and always in context: "A short AGENTS.md (roughly 100 lines) is injected into context and
serves primarily as a map, with pointers to deeper sources of truth elsewhere." (A1, F-a-28). The rest
lives in `docs/` as "the system of record" (A1, F-a-29), checked by "Dedicated linters and CI jobs"
(A1, F-a-37).

`shipharness` copies this structure for TeamTrack. Two differences are course choices: the map is
injected by the harness code (`build_prefix`), and the prefix is built from the course checkout, so
the agent's edits to its own `AGENTS.md` do not change what it is told.

## 2. A2 and A5: Anthropic's long-running harness

In A2 the instructions are the prompt itself, and there are two of them. The initializer agent and the
coding agent are "separate agents in this context only because they have different initial user
prompts." (A2, F-a-52). The coding agent's prompt tells it where to look before it works, the routine
A2 calls "Getting up to speed": "Read the git logs and progress files to get up to speed on what was
recently worked on." (A2, F-a-59).

So A2 also gives the agent a small entry point that names where the knowledge is (here the state
files), rather than pasting the knowledge in. S2 builds on this routine. A5 is the reference
implementation of the A2 pattern; the course read its README only, and its prompts were not opened
(RESEARCH, clean-room statement).

## 3. Skills in three coding agents

All three agents below state that they follow the Agent Skills standard (B7, B8, B9; F-b-12, F-b-14,
F-b-15). They differ in where they look (RESEARCH §4.5):

| Agent | Project skills | User skills | Also reads | Finding |
|---|---|---|---|---|
| Claude Code | `.claude/skills/<name>/` (from the start directory up to the repository root) | `~/.claude/skills/<name>/` | Enterprise, plugin, and nested `.claude/skills/` folders. B7 does not mention `.agents/skills/` | F-b-12 |
| OpenAI Codex | `.agents/skills` in every directory from the working directory up to the repository root | `$HOME/.agents/skills` | `/etc/codex/skills` (admin) and bundled system skills | F-b-14 |
| Cursor (2.4 and later, B10) | `.agents/skills/`, `.cursor/skills/` | `~/.agents/skills/`, `~/.cursor/skills/` | `.claude/skills/`, `.codex/skills/` and their home equivalents | F-b-15 |

No single directory is read by all three. To reach all of them, install a skill into both
`.claude/skills/<name>/` and `.agents/skills/<name>/` (RESEARCH §4.5, inference from this table).

## 4. Frontmatter: the standard and the extensions

Claude Code treats `name` as optional and adds fields outside the specification (B7, F-b-13). Cursor
documents extra optional fields too (B9). The reference validator rejects any key outside the six
specification fields: "Unexpected fields in frontmatter: {extras}. Only {allowed} are allowed." (B5,
F-b-11).

The course's choice (RESEARCH §4.5): skills use only `name`, `description`, `license`,
`compatibility`, `metadata`, and `allowed-tools`, so they pass the reference validator and load in all
three agents. Vendor-specific data can go under `metadata`. `uv run shipharness skills validate skills`
checks the four course skills (`harness-setup`, `assured-tests`, `house-rules`, `skill-template`).

## 5. What is the same everywhere

Across these sources the shape repeats:

- A small, always-present entry point: an `AGENTS.md` map (A1), a session prompt that names where to
  look (A2), or a skills catalogue of names and descriptions (B1 tier 1, loaded "at startup for all
  skills", F-b-05).
- The detail stays on disk and is loaded when the task needs it: `docs/` (A1, F-a-36), the progress
  file and git log (A2), `SKILL.md` bodies and their resources (B1).

What differs is who builds the entry point. In A1 and in `shipharness` it is a file the harness puts in
context. In the three coding agents it is the agent's own loader, scanning the directories in the table
above. When you take the course skills home, the loader is the agent's; your job is to put the skill
in a directory it scans and write a description that matches the tasks it should handle.

## Questions to take away

1. You use Codex and Claude Code on the same repository. Where do you put a team skill so both load
   it, and how do you keep the two copies from drifting? (A1's F-a-26 on mechanical checks applies.)
2. A skill uses a Claude Code-only frontmatter field. What happens when you run
   `uv run shipharness skills validate` on it, and what would you change?
