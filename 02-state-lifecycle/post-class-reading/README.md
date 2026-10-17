# post-class-reading

Three short pieces for after class, about 27 minutes in total. Each cites the primary sources in
[docs/REFERENCES.md](../../docs/REFERENCES.md) by source id and finding id, points at the `shipharness`
code it describes, and ends with a section "Why it matters for your own repo".

| Piece | Reading time | What it covers |
|---|---|---|
| [01-sessions-in-the-sources.md](01-sessions-in-the-sources.md) | 9 min | A2, A3, A4, A5, and A6 side by side: who writes the first files, how a session learns what happened, fresh context or compaction, what the course changes, and what the pilot's bare arm did across the stop |
| [02-plans-and-handoffs.md](02-plans-and-handoffs.md) | 8 min | The exec-plan and session-handoff templates, section by section against A7, A1, and A3; what the pilot changed in the handoff; questions to answer before writing your own |
| [03-the-continuity-measure.md](03-the-continuity-measure.md) | 10 min | How the referee computes `continuity_failure` and `redone_lines_pct`, the measurement bug pilot run 2 found and its fix, the cases the measure does not catch, the console's file-level "redone" marker, and the F2 stop-point variants |

The primary sources themselves, for a full read:

- A2, "Effective harnesses for long-running agents" (Anthropic, 2025-11-26):
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- A3, "Harness design for long-running application development" (Anthropic, 2026-03-24):
  https://www.anthropic.com/engineering/harness-design-long-running-apps
- A7, "Using PLANS.md for multi-hour problem solving" (OpenAI Cookbook, 2025-10-07, archived):
  https://cookbook.openai.com/articles/codex_exec_plans
