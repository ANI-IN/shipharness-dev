---
name: style-and-naming
description: Apply the course's naming and wording rules - plain names, codes only in brackets, full name on first use, no banned or dated words, short plain sentences - and run the style checker and prose lint. Use before every commit of course text, slides, console labels or messages.
---

# Style and naming

Learners read names before they read ideas. One naming form everywhere, plain words, and two
checkers that run before every commit keep pages from drifting. The rules are in sections 2.2, 2.6
and 3.1 of [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md); the module's own copy is the
skeleton's [STYLE.md](../../skeleton/docs/STYLE.md).

## When to use

- Before committing any course page, guide chapter, slide text, console label, or command-line
  message.
- When an editor fixes review findings.

## Inputs

- The files to check.
- The named kinds, codes and id patterns in `platform/config/course.toml`.
- The glossary (`docs/glossary.md`).

## Steps

1. **Plain names, one form.** Everything a learner sees is "<Kind> <N>: <name>" on first mention
   per page or slide, then "<Kind> <N>". Never a bare code such as F4 or R1.
2. **Codes in brackets.** Where a machine code must show (a check name, a config key), put it in
   brackets after the plain name: "Files outside the allowed paths (diff_scope)".
3. **First use in full.** Spell out every abbreviation on first use per page and add it to the
   glossary; the glossary box on each page uses the glossary's wording.
4. **Banned words.** No filler or hype words and no emoji; the list is in the prose lint
   (`platform/scripts/lint_prose.py`). Quoting the list itself needs the allow marker at the line end.
5. **No dated or internal words**: nothing that only makes sense on the day it was written, no
   build-only terms, no placeholder markers.
6. **Plain sentences**: 25 words or fewer, "you", active voice, paragraphs of at most 5 lines, every
   claim with an example, a command, real output, or a linked source.
7. **Ids stay in evidence pages**: run ids, finding ids and hashes appear only there.
8. **Run the checkers**:

   ```bash
   uv run python platform/scripts/check_style.py --strict
   uv run python platform/scripts/lint_prose.py <files>
   ```

   Fix every error and warning; never add an allow marker to get past a real problem.

## Outputs

Files that pass both checkers, with names consistent with the config and the glossary.

## Checks

- `check_style.py --strict`: 0 errors, 0 warnings. Prose lint: 0 problems.
- A search for bare codes (for example `\b[A-Z]\d+\b`) in learner text finds none outside brackets.
- Every term in the page's glossary box matches the glossary word for word.
- Lessons on wording changes and parsers: [lessons-learned.md](../../playbooks/lessons-learned.md).
