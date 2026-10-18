# Playbooks: running a course build with an AI agent team

These documents describe how a lead (a person, or a lead agent working for the course owner) runs
the build of a course with a team of agents. Read them with the structure guide,
[STRUCTURE-AND-TASTE.md](../STRUCTURE-AND-TASTE.md), its
[checklist](../STRUCTURE-AND-TASTE-CHECKLIST.md), and the skills in [../skills/](../skills/).

| Playbook | Use it when |
|---|---|
| [brief-template.md](brief-template.md) | The owner starts a phase of work: goals, hard rules, deliverables, stop points, report format |
| [shared-agent-brief-template.md](shared-agent-brief-template.md) | Several agents work in parallel on one phase and must share an environment, folders and conventions |
| [agent-prompt-templates.md](agent-prompt-templates.md) | The lead starts one agent in a fixed role |
| [status-and-report-formats.md](status-and-report-formats.md) | Anyone reports: a short status, a phase line, or the final report |
| [merge-and-verify.md](merge-and-verify.md) | Agents hand back branches and the lead combines, checks and pushes |
| [honesty-and-measures.md](honesty-and-measures.md) | A result is measured, timed, re-judged or disclosed |
| [lessons-learned.md](lessons-learned.md) | Before planning a phase: the failures earlier builds hit and how to avoid them |

## The order of a build

1. The owner writes the governing brief from [brief-template.md](brief-template.md).
2. The lead fixes the conventions and folders in a shared brief from
   [shared-agent-brief-template.md](shared-agent-brief-template.md), before any agent starts.
3. The lead starts agents with the prompts in [agent-prompt-templates.md](agent-prompt-templates.md),
   independent work in parallel, at most the heavy-job limit at once.
4. Agents report in the formats in [status-and-report-formats.md](status-and-report-formats.md).
5. The lead merges and verifies with [merge-and-verify.md](merge-and-verify.md), then reports once.
