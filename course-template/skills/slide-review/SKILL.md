---
name: slide-review
description: Read-only review of the owner's slide deck - extract each slide's text and speaker notes, check names, numbers, commands, timings and flows against the repository, and produce a change list. Never edits the deck. Use when the repository changed after the deck was made, or before class.
---

# Slide review

The owner makes and owns the final deck. Agents never edit it; they hand the owner a precise change
list. The slide rules (at most 80 slides, one poll, one DEMO slide per section with badge and title
only, notes deliverable alone) are in section 2.9 of
[STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- Results, timings, names or commands changed in the repository after the deck was built.
- Before class, as the last consistency check between the deck and the pages.

## Inputs

- The deck file (`<DECK PATH>`), read-only. Work on a copy if a tool needs a writable file.
- The repository at a fixed commit: README results, concepts pages, run sheet, instructor guide,
  glossary, evidence pages.

## Steps

1. **Extract** each slide's title, body text and speaker notes to plain text (for example with
   python-pptx), numbered by slide. Do not save the deck.
2. **Check each slide** against the repository:
   - names in "<Kind> N: <name>" form, full on first use, matching the glossary;
   - every number (counts, times, costs) matching its source page;
   - every command exactly as in the reference page;
   - the flow: section order, breaks, the one poll, one DEMO slide per section, total time;
   - speaker notes that let an instructor deliver from the notes alone, with a pass and a fail
     script for each demo.
3. **Check the deck rules**: slide count, one poll, no recap slides, no screenshots on DEMO slides,
   titles of at most 10 words.
4. **Write the change list**: one row per change, with the exact current text and the exact new
   text, so the owner can paste it.

## Outputs

A change list, given in chat or as the owner asks:

```text
| Slide | Field (title / body / notes) | Current text | New text | Source in the repository |
```

Followed by a count of changes by kind (numbers, names, commands, flow, rules).

## Checks

- The deck file's checksum is unchanged after the review.
- Every row has a source path, so the owner can confirm it.
- No change rewrites style the owner chose; changes are about facts and the deck rules, unless the
  owner asked for more.
- Names follow [style-and-naming](../style-and-naming/SKILL.md); the prompt is in
  [agent-prompt-templates.md](../../playbooks/agent-prompt-templates.md).
