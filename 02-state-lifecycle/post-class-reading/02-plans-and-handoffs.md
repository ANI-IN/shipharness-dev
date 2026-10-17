# Exec plans and structured handoffs: the templates against their sources

Reading time: about 8 minutes.

The state layer writes two documents that the agent is asked to keep current: an execution plan and
a session handoff. This piece shows the two templates as they ship in `shipharness` and lines each
section up with the source it comes from, so you can write your own versions for a repository that is
not TeamTrack.

## Execution plans (A1, A7)

A1 treats plans as repository files, not chat: "complex work is captured in execution plans with
progress and decision logs that are checked into the repository." (A1, F-a-34). They live with the
code, "allowing agents to operate without relying on external context." (A1, F-a-35).

A7, the OpenAI Cookbook recipe that A1 links as "execution plans", is stricter. A7 is archived
(accessed 2026-10-16), so read it for its definitions:

- Self-contained: "Every ExecPlan must be fully self-contained. Self-contained means that in its
  current form it contains all knowledge and instructions needed for a novice to succeed." (F-a-46)
- Restartable: "it should always be possible to restart from _only_ the ExecPlan and no other work."
  (F-a-47)
- Living sections: "ExecPlans must contain and maintain a `Progress` section, a `Surprises &
  Discoveries` section, a `Decision Log`, and an `Outcomes & Retrospective` section." (F-a-48)
- Proven: "Validation is not optional. Include instructions to run tests, to start the system if
  applicable, and to observe it doing something useful." (F-a-145)
- Discoverable: "We enable Codex to use these documents by first updating AGENTS.md to describe when
  to use PLANS.md" (F-a-45)

The template the initializer step renders (`src/shipharness/harness/state/assets/exec-plan.md`, lines
1-35; `{{...}}` fields are filled from the ticket):

```markdown
# {{feature_id}}: {{description}}

This execution plan is a living document checked into the repository (A7). Keep it self-contained:
a new session must be able to restart from this plan, progress.md, and the git log alone. The
harness moves it to docs/exec-plans/completed/ when the feature passes.

## Purpose

{{description}}

Steps from the ticket:

{{steps}}

## Progress

- [x] Harness initializer step: init.sh, progress.md, session-handoff.md, and this plan created.
- [ ] (add one line per step with a UTC timestamp, for example 2026-10-16T10:00Z)

## Surprises & Discoveries

- None yet.

## Decision Log

- None yet. Record each decision with the reason and the date.

## Outcomes & Retrospective

- Not finished yet.

## Validation

- `bash init.sh` (migrations at one head, basic test run)
- `python -m pytest tests/visible -q`
```

| Template section | Source |
|---|---|
| Header sentence ("restart from this plan, progress.md, and the git log alone") | A7 F-a-47, widened to include A2's progress file and git log (F-a-53) |
| Purpose, Steps from the ticket | A7 F-a-46 (self-contained) |
| Progress, Surprises & Discoveries, Decision Log, Outcomes & Retrospective | A7 F-a-48 |
| Validation | A7 F-a-145 |
| Move to `completed/` when the feature passes | A1 F-a-35 ("Active plans, completed plans"); the trigger is course design (`StateLayer.on_phase_end`, after the scope layer sets `passes`) |

For F2, the decision that matters most is which migration revision holds the comments table. If
session 1 records it in the Decision Log, session 2 does not have to rediscover it.

## Structured handoff (A3)

A3 describes the context reset as a fresh agent "combined with a structured handoff that carries the
previous agent's state and the next steps" (A3, F-a-65). The template
(`src/shipharness/harness/state/assets/session-handoff.md`, lines 1-15):

```markdown
# Session handoff

A structured handoff that carries the previous session's state and the next steps (A3). The
harness rewrites "Machine summary" at every session stop. Write your own notes under "Notes from
the agent" before the session ends.

## Machine summary

No session has ended yet.

## Notes from the agent

- What I was doing:
- What is left:
- What to watch out for:
```

The file has two owners, by design:

- **Machine summary** is written by `lifecycle.session_stop` at every stop: start and end commits,
  files changed in the session, visible-test status with up to five failure lines, the last five
  commits, open `TODO`/`FIXME`/`XXX` markers in changed files, migration heads read from the
  migration files as text, and the harness documents the agent has read so far (`handoff.py`). It
  is rewritten each time.
- **Notes from the agent** are kept exactly as the agent wrote them (`handoff.merge`). The wrap-up
  message asks for them three turns before the stop, including "the house rules and file locations
  from the documents you read that matter for this ticket, so the next session does not need to
  read them again" (`lifecycle.wrapup_text`).

The last two items came from the pilot. In the course pilot's run 2 (2026-10-16) every harness
session re-read 3 to 7 instruction documents and about 15 product files, so the handoff now carries
what was learned from them, and the Getting up to speed routine reads the agent's notes before any
other document (a harness change after run 2, harness arm only). A handoff is only worth its turns
if the next session reads it instead of repeating the work it records.

Having a machine part at all is course design: an agent that runs out of turns
mid-edit may write no notes, and the next session should still start from something. A4's agents
point at a further section worth adding in your own repository: a list of approaches that failed
("a running doc of failed approaches and remaining tasks", A4, F-a-73). The `harness-setup` skill's
checklist (`skills/harness-setup/references/session-lifecycle.md`) includes that item.

## Why it matters for your own repo

Before you write your own plan and handoff templates, answer these:

1. What does a fresh session need to know in its first five tool calls? Put that in the handoff's
   first lines; the harness resume text passes only the first 3,000 characters of the machine summary
   (`lifecycle.resume_text`).
2. Which facts can a script collect better than the agent? Git state, test status, and schema heads
   do not need the model's memory.
3. Which file is the record for which question? In `shipharness`: the plan says what and why, the
   progress log says which session did what, the handoff says where the last session stopped, and git
   holds the changes.
4. When does the agent update these files? Asking for updates throughout the session cost the pilot's
   harness arm turns it needed for the feature; `shipharness` now asks only in the wrap-up turns.
