---
name: evidence-and-results
description: Record every run and result honestly - pre-registered measures, a run log, evidence pages with ids and hashes, re-judging only by fixed rules, counts not percentages, and exact disclosure wording. Use when designing a measured comparison, after any run, or when writing a results table.
---

# Evidence and results

The course's numbers are only as good as the rules that produced them. This skill applies
[honesty-and-measures.md](../../playbooks/honesty-and-measures.md) to the files: where runs are
recorded, how results are written, and which pages may carry ids. Page rules are in section 2.7 of
[STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- Before the first run of a comparison: to pre-register it.
- After any run: to record it.
- When a results table, a "What we measured" section or a slide shows a number.
- When a checker bug is found and stored runs might be re-judged.

## Inputs

- The design notes (private) and the evidence pages (`docs/evidence.md`, `docs/evidence/`).
- The run folders and the tool's stored results.
- The budget record.

## Steps

1. **Pre-register** in the design notes, dated, before any run: question, primary measure,
   secondary measures, arms and the one difference, identical settings, runs per arm, pass, fail and
   error rules, budget cap.
2. **Record every run** in the run log: run id, date, purpose (pilot or measured), arm, outcome per
   measure, cost, settings hash. Failed and error runs too.
3. **Write results as counts** with both arms: "3 of 3 vs 0 of 3". Use the disclosure phrases from
   the playbook: "No measurable difference", "<Arm> ahead", "Both fail".
4. **Evidence pages only** carry run ids, finding ids, hashes and capture details. Teaching pages
   link to the evidence page instead.
5. **Disclose changes**: any setting change gets a dated line on the evidence page with the reason
   and which arms it applies to. Both arms of a comparison keep identical settings.
6. **Re-judge only by the rule**: a checker bug is fixed test-first, then every stored run of both
   arms is re-judged at once, and the before and after counts are disclosed. Never re-judge one arm or
   a chosen subset; never re-run to replace a result.
7. **Post hoc** analysis is labelled "Exploratory (post hoc)" and changes no classification.
8. Add each limitation (one model, small samples, one project) to the front page's "Known
   limitations".

## Outputs

- A pre-registration entry per comparison, dated before its first run.
- A complete run log and evidence pages; results tables with counts and their sources.
- Disclosure lines for every change, and an updated limitations list.

## Checks

- Every number on a page names its file or run; no estimate stands in for a missing number.
- No run id, finding id or hash outside the evidence pages (the style checker enforces this).
- The count of runs in the log equals the count of runs the tool stored for the period.
- Results tables agree across the README, concepts pages, slides and evidence pages.
- Timings follow the timing rules in the playbook.
