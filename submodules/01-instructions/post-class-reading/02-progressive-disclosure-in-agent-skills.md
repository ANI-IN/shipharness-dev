# Progressive disclosure in the Agent Skills specification

Reading time: about 7 minutes.

Sources (all accessed 2026-10-16; see RESEARCH.md §1.1 and §4.5, and `research/notes/R-b.md`):

- B1, Agent Skills Specification, https://agentskills.io/specification
- B2, What are skills?, https://agentskills.io/what-are-skills
- B3, How to add skills support to your agent,
  https://agentskills.io/client-implementation/adding-skills-support.md
- B5 and B6, the `skills-ref` reference validator (source and PyPI package 0.1.1)

Quotes are verbatim from those files. Where a quote has no finding ID, it comes from the "Agent Skills
spec — normative rules" table in `research/notes/R-b.md`.

The concepts page shows the three tiers in one table. This piece reads the specification more closely:
what a skill must contain, what loads when, what a client is told to do, and how `shipharness` maps
each rule to code.

---

## 1. What a skill is

> "A skill is a directory containing, at minimum, a `SKILL.md` file" (B1)

> "The `SKILL.md` file must contain YAML frontmatter followed by Markdown content." (B1, F-b-01)

The specification defines six frontmatter fields (RESEARCH §4.5):

| Field | Required | Rule (B1) |
|---|---|---|
| `name` | yes | 1-64 characters, lowercase `a-z`, `0-9`, hyphens; no leading, trailing, or double hyphen; "Must match the parent directory name" (F-b-02) |
| `description` | yes | 1-1024 characters; "Should describe both what the skill does and when to use it" (F-b-03) |
| `license` | no | A license name or a bundled license file |
| `compatibility` | no | 1-500 characters, only for real environment requirements |
| `metadata` | no | A map from string keys to string values |
| `allowed-tools` | no | "Experimental. Support for this field may vary between agent implementations" (F-b-04) |

The `name` rule is why the course's blank skill is `skills/skill-template`, not the brief's
`skills/_template`: an underscore can never pass (DESIGN D-17).

Optional folders are `scripts/`, `references/`, and `assets/`. File references use relative paths
from the skill root, and B1 says: "Keep file references one level deep from `SKILL.md`. Avoid deeply
nested reference chains." (F-b-07).

## 2. The three tiers

B1's section on progressive disclosure (F-b-05):

| Tier | B1's words | Loaded |
|---|---|---|
| Metadata | "**Metadata** (~100 tokens): The `name` and `description` fields are loaded at startup for all skills" | At startup |
| Instructions | "**Instructions** (< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated" | On activation |
| Resources | "**Resources** (as needed): Files (e.g. those in `scripts/`, `references/`, or `assets/`) are loaded only when required" | When needed |

B2 names the same stages Discovery, Activation, and Execution. Its Activation line states the trigger:
"When a task matches a skill's description, the agent reads the full `SKILL.md`" (B2).

Two consequences follow, both in B1:

- The body loads whole: "the agent will load this entire file once it's decided to activate a skill.
  Consider splitting longer `SKILL.md` content into referenced files." (B1)
- Hence the size guidance: "Keep your main `SKILL.md` under 500 lines. Move detailed reference material
  to separate files." (B1, F-b-06)

The description carries the most weight per word. At tier 1 it is the only text the agent has about
the skill. If it does not say when to use the skill, the agent has no reason to open it, and tiers 2
and 3 never load.

## 3. What a client is told to do

B3 is written for people building agents that load skills. Points that shaped `shipharness`:

- Where to look is not fixed by the specification: "the Agent Skills specification does not mandate
  where skill directories live (it only defines what goes inside them)" (B3, F-b-08). B3 notes that
  the `.agents/skills/` paths "have emerged as a widely-adopted convention for cross-client skill
  sharing." (B3)
- What to scan for: "look for **subdirectories containing a file named exactly `SKILL.md`**" (B3)
- Be lenient with small errors: "Name doesn't match the parent directory name → warn, load anyway";
  "Description is missing or empty → skip the skill" (B3, F-b-09)
- B3's client table gives the catalogue a budget of "~50-100 tokens per skill" at "Session start"
  (B3).

Note the tension: B1 is strict about `name`, and B3 tells clients to load the skill anyway. Authors
should follow B1; clients follow B3.

## 4. How shipharness maps each rule to code

| Specification | `shipharness` | File |
|---|---|---|
| Skills in `.agents/skills/` (B3 convention) | The instructions layer places skills at `.agents/skills/` in the harness arm's workspace | `src/shipharness/harness/instructions/layer.py` |
| Scan for `*/SKILL.md` (B3) | `self.root.glob("*/SKILL.md")` | `src/shipharness/runner/skills_loader.py` |
| Skip a skill with no description (B3) | `catalogue()` skips any skill whose frontmatter lacks `name` or `description` | same |
| Tier 1 at startup (B1) | `catalogue_block()` writes one line per skill (name, description, path to `SKILL.md`) into the context prefix | same, anchor `S1:progressive` |
| Tiers 2 and 3 on demand (B1) | Never pre-loaded; the agent uses `read_file`. `skill_for_path` reports tier 2 for `SKILL.md` and tier 3 for any other file in the skill folder | same |
| Validation (B1 points to skills-ref) | `uv run shipharness skills validate <dir>`: the skills-ref checks as errors, plus warnings for over 500 lines and references deeper than one level (CONTRACTS §7) | `src/shipharness/skills_cli/` |

The loader parses frontmatter with a small reader of top-level scalar fields, enough for `name` and
`description`; it is not a full YAML parser (`parse_frontmatter` in `skills_loader.py`).

## 5. The reference validator

B1 says to "Use the skills-ref reference library to validate your skills" (B1). Facts from its source
and package (RESEARCH §4.5, B5, B6):

- Its README says: "This library is intended for demonstration purposes only. It is not meant to be
  used in production." (F-b-10)
- It rejects any frontmatter key outside the six spec fields: "Unexpected fields in frontmatter:
  {extras}. Only {allowed} are allowed." (F-b-11)
- It does not check body length, file references, or the token budget.
- Version 0.1.1 installs its command as `agentskills`: `uv run agentskills validate <dir>`.

The F-b-11 rule decides portability. Vendor extension fields (see
[03-instructions-in-other-agents.md](03-instructions-in-other-agents.md)) fail the reference validator,
so the course skills use only the six spec fields (RESEARCH §4.5). VERIFICATION.md records the four
course skills passing `shipharness skills validate skills` with 0 errors and 0 warnings (M4).

## 6. Read one skill against the specification

Open `teamtrack/harness/instructions/.agents/skills/add-endpoint/SKILL.md` and check:

1. Does `name` match the folder?
2. Does the description say what the skill does and when to use it? Which words would match the F1
   ticket ("Add org-wide issue search: GET /issues")?
3. Is `SKILL.md` under 500 lines? (The validator reports 100.)
4. Is `references/tests.md` one level deep, linked with a relative path?

Then run `uv run shipharness skills validate teamtrack/harness/instructions/.agents/skills` and compare
its result with your answers. On 2026-10-17 in the course build worktree it printed (your output will
differ):

```text
+ add-endpoint: valid (SKILL.md 100 lines)
1 skill checked, 0 errors, 0 warnings
Cost: $0.000000 (no model calls)
```

## Why it matters for your own repo

- The description is the only part of a skill the agent sees before it decides to open it (B1,
  F-b-05). Write it with the words your tickets use and a "when to use" clause (F-b-03); a skill
  whose description never matches a ticket is never read, however good its body is.
- Opening a skill is observable. In the course's pilot run 2, every harness arm on F1 opened the
  `add-endpoint` body (tier 2) on its fourth tool call and none opened `references/tests.md` (tier
  3) ([../demo/README.md](../demo/README.md) section 6). Log which tier your agent reads; if tier 3
  is never read, either the body already says enough or the pointer to the reference is too weak.
- Stay inside the six specification fields so one skill folder loads in every agent that follows
  the standard (F-b-11; [03-instructions-in-other-agents.md](03-instructions-in-other-agents.md)).
  Run a validator in CI, as A1 does for its docs (A1, F-a-37).
