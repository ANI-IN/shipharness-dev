<!--
deck.md: the source of the Module 1 slides. `make slides` (scripts/build_slides.py) turns it into
slides/dist/deck.html, deck.pdf, and deck.pptx. Built from slides/outline.md; keep both in step.

Format, one block per slide:

  ## 12. Slide title              starts a slide: number, a dot, the title (numbers run 1-72)
  section: S1 Instructions        required; shown in the header
  minutes: 2.5                    speaker timing; the build prints the total per section
  layout: title                   optional: default (the usual), title, or statement (one big line)
  subtitle: One line              optional, under the title
  diagram: architecture now=L1    the recurring diagram defined below, with nodes highlighted
  image: images/board.png         a picture, path relative to this folder (must exist)
  code: S1:prefix 10-19           lines of a walkthrough anchor (scripts/anchors.py), e.g. 1-4,9-12;
                                  left-out lines show as "..."; at most 12 code lines per slide
  slot: s1_dots                   a result slot, empty until the lead fills it from run data:
  slot: s1_dots = 3 of 10 failed  text, or an image path such as images/s1-dots.png
  live: tonight's two dots        a value produced in class, shown as "Filled in live: ..."

  - Bullet text, 3 to 6 per slide, `code` in backticks
    a line indented under a bullet continues it

  [[PENDING: what | source: ... | how: ...]]   an open item, shown as an amber box on the slide

  ```mermaid                      an inline Mermaid diagram for this slide only
  flowchart LR
    A --- B
  ```

  notes:
  Speaker notes until the next "## N." line. The build adds "Slide N of 72 | section | minutes"
  at the top of the PPTX notes. A PENDING line in the notes is listed but stays off the slide.

Filling a result: put the value after the slot name (`slot: s1_dots = ...`) and delete the PENDING
line that describes it. `make slides` lists every PENDING marker and empty slot at the end;
`uv run python scripts/build_slides.py --strict` fails while any remain.
-->

::: diagram architecture
flowchart LR
  TK["Same ticket, model, tools, budgets"] --> BA["Bare arm: agent loop"]
  TK --> HA["Harness arm: agent loop"]
  HA --- L1["S1 Instructions"]
  HA --- L2["S2 State and session lifecycle"]
  HA --- L3["S3 Scope"]
  HA --- L4["S4 Verification"]
  BA --> SB1["Sandbox"]
  HA --> SB2["Sandbox, identical"]
  SB1 --> REF["Referee: same checks, fresh container"]
  SB2 --> REF
  REF --> CON["Console and report"]
  classDef now stroke-width:5px,stroke:#0b1f33
:::

## 1. Harness Engineering for Coding Agents
section: Opening
minutes: 0.5
layout: title
subtitle: Instructions, state, scope, and verification that make agent-written code safe to merge

- Module 1 · course repository `shipharness`

notes:
Welcome. Tonight one coding agent builds the same features twice, with and without a harness, and a
referee judges both. Everything you see is in the course repository.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md title and first paragraph.

## 2. The problem: four real failures
section: Opening
minutes: 2.5
slot: bare_f1_board
slot: bare_f1_run_id

- A new endpoint returns one customer's data to another customer
- A second session does not know what the first did, and redoes or breaks it
- The agent changes files it was never asked to touch, and older features stop working
- The agent's own tests pass while the behaviour is wrong
- On the board: a recorded bare-arm F1 run with ⚠ other-org marks, recorded before class

[[PENDING: board screenshot of a recorded bare-arm F1 run with other-org marks, and its run id | source: M6 pilot | how: make demo-1 on the class host; PNG under .shipharness/runs/<ab id>/screenshots/bare/]]

notes:
Read the four failures, then point at the board screenshot. Say "recorded before class" and read out
its run id. "The agent said it passed" is the only evidence a reviewer gets without a harness.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §1.

## 3. Why it happens: four causes
section: Opening
minutes: 2

- Cause 1: "anything it can’t access in-context while running effectively doesn’t exist" (A1, F-a-05)
- Cause 2: "each new session begins with no memory of what came before." (A2, F-a-08)
- Cause 3, side by side: A1 F-a-20; A4 F-a-18, F-a-19; A5 F-a-86; A6 F-a-21 (supplementary)
- Cause 4: "agents reliably skew positive when grading their own work" (A3, F-a-15); B13 F-b-45, F-b-50

notes:
One cited line per cause. Cause 3 (agents copy existing patterns and can take actions that are hard
to undo) has no single source that says both, so the four citations stand side by side and are not
merged. Cause 4: the visible suite passes while held-out tests that compose features fail (B13).

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §2; REFERENCES.md.

## 4. The solution: a harness
section: Opening
minutes: 2
diagram: architecture now=L1,L2,L3,L4,SB1,SB2

- A harness is the environment around the agent, not a better prompt
- A1: "design environments, specify intent, and build feedback loops" (F-a-02)
- Four parts, S1 to S4, plus a sandbox that is identical for both arms
- A1 never defines "harness engineering"; no definition is attributed to A1

notes:
The thick borders and the word "now" mark the parts this slide is about: all four parts and the
sandbox. The section names S1 to S4 are course labels, not source terms.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §3; REFERENCES.md.

## 5. shipharness, TeamTrack, console
section: Opening
minutes: 1.5
code: Opening:two_arms 5-9,11-15,19

- `shipharness`: run an agent with or without the harness, A/B it, judge it
- TeamTrack: multi-tenant issue tracker, orgs Acme and Globex, 25 API operations, 142 visible tests
- Console: five screens on keys `1` to `5`, `F` for full screen per arm

notes:
The code shows both arms running at the same time and each judged by the same referee as soon as it
finishes; the finally block is folded. `Opening:publish` is shown in the editor only. TeamTrack size
as counted at M3 (OpenAPI operations, visible tests).

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §5, §9, §11; anchor Opening:two_arms.

## 6. How we prove it
section: Opening
minutes: 1

- Same agent, model, effort, task, repository, tools, sandbox, turn limit, and cost cap
- One deterministic referee judges what each arm ships
- House rules R1-R7: the course label for A1's "golden principles" (F-a-99)
- Datasets: 60 tasks in six groups, 40 test-generation targets
- One primary measure per section, registered before any run

notes:
The bare arm gets every rule in docs/HANDBOOK.md; nothing is withheld. Results are counts such as
"2/3", never percentages.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §4, §10 (primary measures); teamtrack/docs/HANDBOOK.md (R1-R7); datasets/README.md.

## 7. Check your setup
section: Opening
minutes: 0.5
live: `make doctor` output and the `harness-setup` assessment of the bare TeamTrack

- Run `make doctor` now
- Run the `harness-setup` assessment on the bare TeamTrack
- Read the gaps it reports: instructions, state, scope, verification

notes:
Run both live. The assessment is read-only and makes no model calls.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: Makefile `doctor`; skills/harness-setup/scripts/assess.py.

## 8. Poll
section: S1 Instructions
minutes: 3
live: the room's poll result

- F1 org-wide issue search; rule at risk: R1 tenant isolation
- Both arms can open `docs/HANDBOOK.md`, which says "Do not copy" about `GET /v1/issues`
- Out of 10 bare-arm runs of F1, how many ship `GET /issues` with at least one new R1 violation?
- A) 0-2   B) 3-5   C) 6-8   D) 9-10
- Close the poll before the launch

notes:
Close the poll before launching, so nobody votes after seeing the console.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: submodules/01-instructions/demo/README.md §4.

## 9. Launching the live A/B: F1 org-wide issue search
section: S1 Instructions
minutes: 2
slot: c1_control

- Now: run `make demo-1` in terminal B; it runs during slides 10-18, back on slide 19
- Rule at risk: R1; the trap: a legacy handler without the tenant filter
- Harness arm layers: instructions
- Primary measure: one or more new R1 violations fails the run
- Control glance: C1, both arms should pass this one

[[PENDING: C1 control results per arm | source: M8 batch 4 | how: make experiments, full dataset; make report]]

notes:
Reload the console's run list, open the newest ab-..., stay on screen 1 while both containers start.

The A/B must be finished by section minute 25. In pilot run 2 (12 A/Bs, sections F1-F4, two A/Bs
running in parallel on the class host, before the approved referee speed-ups) every A/B finished
within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s (8.1 min) (course pilot, run 2,
2026-10-16). Course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4 with the pilot's task variants, effort
medium, two A/Bs in parallel on the class host): wall time per A/B min 384 s, median 512 s, max 620 s.
Run 4, effort low, 2026-10-16 to 2026-10-17 (9 A/Bs, F1-F3, two in parallel): min 309 s, median 414 s,
max 565 s. Neither run timed one A/B on its own.
[[PENDING: wall time of make demo-1 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-1 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: README.md §10; teamtrack/reference/f1/task.toml; teamtrack/docs/features/c1.md.

## 10. S1: what the agent knows
section: S1 Instructions
minutes: 1.5
diagram: architecture now=L1

- Explain why an agent does not apply a rule that exists only outside its context (A1)
- Structure knowledge as a short AGENTS.md map into `docs/`, plus one skill with progressive disclosure (B1)
- Read the S1 A/B result: R1 and R3 failures with and without the instructions layer
- Testing right now: a legacy handler without the tenant filter, next to the right pattern

notes:
The first three bullets are the section's objectives (course design). The legacy handler is
`GET /v1/issues`; the A/B running in terminal B tests whether the agent copies it.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: S1 learning objectives (course design); README.md §10 (legacy GET /v1/issues).

## 11. Problem: the rule is written down, the agent does not apply it
section: S1 Instructions
minutes: 2

- F1 builds `GET /issues`, an org-wide issue search
- R1: another org's resource is 404, never 403
- The rule is in `docs/HANDBOOK.md`, and both arms can read it
- Nothing is withheld from the bare arm

notes:
Both arms get every rule. The question is not whether the rule exists but whether the agent applies it.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: teamtrack/docs/HANDBOOK.md (R1); README.md §4; teamtrack/docs/features/f1.md.

## 12. Cause: what is not in context does not exist
section: S1 Instructions
minutes: 2.5

- "anything it can’t access in-context while running effectively doesn’t exist" (A1, F-a-05)
- "A giant instruction file crowds out the task, the code, and the relevant docs" (A1, F-a-23)
- "Too much guidance becomes non-guidance." (A1, F-a-24)
- A long manual goes stale and cannot be checked mechanically (A1, F-a-25, F-a-26)
- Agents copy existing patterns, including uneven ones (A1, F-a-20)

notes:
Cause 1 from the opening, in A1's words. A handbook the agent never opens does not exist for it.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: A1 in REFERENCES.md.

## 13. Harness piece: AGENTS.md as a map
section: S1 Instructions
minutes: 3

- "roughly 100 lines", "a map", "the table of contents" (A1, F-a-22, F-a-27, F-a-28)
- `docs/` is the system of record (A1, F-a-29, F-a-30)
- A1's layout: ARCHITECTURE.md at the root; SECURITY.md, RELIABILITY.md, QUALITY_SCORE.md, PLANS.md in docs/
- Also in docs/: design-docs/, product-specs/, references/ (A1, F-a-30, F-a-31)

notes:
TeamTrack's harness instructions follow this layout: teamtrack/harness/instructions/. The map points;
the documents hold the rules.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: A1 in REFERENCES.md; teamtrack/harness/instructions/.

## 14. Progressive disclosure
section: S1 Instructions
minutes: 3

- Docs: "agents start with a small, stable entry point and are taught where to look next" (A1, F-a-36)
- Skills, three tiers: "Metadata (~100 tokens)", "Instructions (< 5000 tokens recommended)", "Resources (as needed)"
- Tiers from B1 and B2 (F-b-05, F-b-06)
- SKILL.md needs `name` and `description` (F-b-01 to F-b-04)

notes:
Only tier 1 (name and description) sits in the context for every skill; the agent opens the rest
when a task needs it.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: A1, B1, B2 in REFERENCES.md.

## 15. Keep the map true
section: S1 Instructions
minutes: 3

- Docs are checked mechanically by linters and CI jobs (A1, F-a-37)
- Lint messages that teach: the error carries the fix into the agent's context (A1, F-a-97)
- Fairness: the bare arm gets every rule in `docs/HANDBOOK.md`
- A unit test checks that both forms carry each rule id

notes:
The harness changes how knowledge is organised, not what the agent may know.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: A1 in REFERENCES.md; README.md §4.

## 16. Code: the map
section: S1 Instructions
minutes: 3
code: S1:agents_md 9,11-21

- The "Where to look" table of TeamTrack's AGENTS.md
- Each row: what you are about to do, and the document to read first

notes:
The header and the first rows of the table. The house rules follow further down the same file.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: anchor S1:agents_md.

## 17. Code: skills, tier 1 only
section: S1 Instructions
minutes: 3.5
code: S1:progressive 31-39

- `catalogue_block`: one line per skill, name and description
- The full SKILL.md is never pre-loaded; the agent reads it when the task matches

notes:
Section minute 25 falls on this slide: check terminal B for the `Cost:` line.
[[PENDING: wall time of make demo-1 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-1 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00), "Check at section minute 25".
Source: anchor S1:progressive.

## 18. Code: the stable prefix
section: S1 Instructions
minutes: 3.5
code: S1:prefix 10-19

- One stable text block: the map, then tier 1 of every skill
- The documents the map points to are not injected; the agent opens them

notes:
From `agents_md = ...` to `return`.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: anchor S1:prefix.

## 19. Demo block: what the console shows
section: S1 Instructions
minutes: 8

- The finished A/B, screen by screen
- Screen 1: harness decisions, and "Agent said" next to "Referee"
- Screen 2: ⚠ other-org cards on each arm's board
- Screen 3: files read by category (did the agent open the documents the map points to)
- Screen 3: new R1 violations in the referee list

notes:
Say: "The referee probes every endpoint as Acme with Globex ids and expects 404. It does not care
which arm wrote the code."

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: README.md §11.

## 20. Demo block: results
section: S1 Instructions
minutes: 7
slot: s1_experiment_dots
live: tonight's two dots; swap test verdict

- The A/B verdicts
- Tonight's two dots next to the experiment dots
- `make swap-1`: the referee judges code, not labels

[[PENDING: S1 experiment dots, runs failing out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report]]

notes:
Screen 4 for the dots. An unwelcome result is a result: show it.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: M8 experiment results (make report); make swap-1.

## 21. Runbook and next
section: S1 Instructions
minutes: 5

- Runbook: `submodules/01-instructions/demo/README.md`
- Discussion: the bare arm could read the same rules. Why did it (or did it not) apply them?
- Next: what happens when a session ends halfway

notes:
Tie the discussion back to A1, F-a-05.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: docs/instructor-guide.md (schedule).

## 22. Poll
section: S2 State and session lifecycle
minutes: 3
live: the room's poll result

- F2 comments over two sessions; at risk: continuity and R7
- Both agents stop after 20 turns, before F2 is finished, and restart with an empty context
- After session 2, which arm ships one migration head, one `comments` table, and keeps session 1's work?
- A) Both arms   B) Only the harness arm   C) Only the bare arm   D) Neither
- Close the poll before the launch

notes:
If the class runs the 12-turn lever, say "after 12 turns" instead.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: submodules/02-state-lifecycle/demo/README.md §4.

## 23. Launching the live A/B: F2 comments
section: S2 State and session lifecycle
minutes: 2
slot: c2_control

- Now: run `make demo-2` in terminal B; it runs during slides 24-31, back on slide 32
- Two sessions, budgets 20 and 30; same wrap-up turns and resume sentence for both arms
- Harness arm layers: instructions, state
- Primary measure: continuity failure
- Control glance: C2, both arms should pass this one

[[PENDING: C2 control results per arm | source: M8 batch 4 | how: make experiments, full dataset; make report]]

notes:
Continuity failure: R7 fails, a second migration creates the same table, or 30% or more of session
1's added lines are removed in session 2.

The A/B must be finished by section minute 25. In pilot run 2 (12 A/Bs, sections F1-F4, two A/Bs
running in parallel on the class host, before the approved referee speed-ups) every A/B finished
within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s (8.1 min) (course pilot, run 2,
2026-10-16). Course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4 with the pilot's task variants, effort
medium, two A/Bs in parallel on the class host): wall time per A/B min 384 s, median 512 s, max 620 s.
Run 4, effort low, 2026-10-16 to 2026-10-17 (9 A/Bs, F1-F3, two in parallel): min 309 s, median 414 s,
max 565 s. Neither run timed one A/B on its own.
[[PENDING: wall time of make demo-2 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-2 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: README.md §10; teamtrack/reference/f2/task.toml.

## 24. S2: what the agent remembers
section: S2 State and session lifecycle
minutes: 2
diagram: architecture now=L2

- Describe the initializer and coding agents, `init.sh`, the progress file, and git history (A2)
- Design an exec plan (A1, A7) and a structured handoff (A3) that let a session resume after a reset
- Read the S2 A/B result: redone or lost work and migration-head conflicts after a forced stop
- Testing right now: a second session that does not know what the first did

notes:
The first three bullets are the section's objectives (course design).

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: S2 learning objectives (course design); README.md §1.

## 25. Cause: every session starts empty
section: S2 State and session lifecycle
minutes: 2.5

- "each new session begins with no memory of what came before." (A2, F-a-08)
- "However, compaction isn’t sufficient." (A2, F-a-54, F-a-55)
- What the last session knew must be written down somewhere the next one reads

notes:
Cause 2 from the opening.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: A2 in REFERENCES.md.

## 26. Harness piece: state on disk
section: S2 State and session lifecycle
minutes: 3.5

- An initializer agent and a coding agent (A2, F-a-49, F-a-52)
- `init.sh` (F-a-50) and a progress file (F-a-50, F-a-53); the course names it `progress.md`
- Git history as state and as a way back (F-a-53, F-a-57)
- Course design: the initializer is a deterministic harness step

notes:
A2's two agents differ only by their first prompt (F-a-52). In the course, the harness writes the
initial files itself.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: A2 in REFERENCES.md; docs/architecture.md §5.

## 27. Getting up to speed, and ending a session
section: S2 State and session lifecycle
minutes: 3

- A2's routine: `pwd`, progress and git log, the feature list, `init.sh`, a basic test (F-a-58 to F-a-62)
- "End the session by writing a git commit and progress update." (F-a-63)
- Both steps are the same every session

notes:
"Getting up to speed" is A2's own name for the routine.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: A2 in REFERENCES.md.

## 28. Exec plans and the structured handoff
section: S2 State and session lifecycle
minutes: 4

- Exec plans move from active to completed (A1, A7; F-a-34, F-a-35, F-a-45 to F-a-48)
- A3's context reset: a fresh agent with a structured handoff (F-a-65 to F-a-69)
- The course mechanism is the session turn budget
- In A3, resets are a dated, model-dependent choice, not a standing rule

notes:
Say: "This stop is the session turn budget, the same for both arms. A3 calls the pattern a context
reset with a structured handoff (A3, F-a-65)."

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: A1, A3, A7 in REFERENCES.md.

## 29. Code: init.sh
section: S2 State and session lifecycle
minutes: 3
code: S2:init 14-19

- Migrations first: house rule R7, exactly one head
- Then a basic end-to-end test that stops at the first failure

notes:
From `echo "== migrations` to the pytest line.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: anchor S2:init.

## 30. Code: stop and resume
section: S2 State and session lifecycle
minutes: 4
code: S2:stop_resume 28-36

- `resume_text`: extra resume text for the harness arm
- The neutral resume sentence comes first, the same for both arms

notes:
Section minute 25 falls on this slide: check terminal B for the `Cost:` line.
[[PENDING: wall time of make demo-2 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-2 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50), "Check at section minute 25".
Source: anchor S2:stop_resume.

## 31. Code: the session log
section: S2 State and session lifecycle
minutes: 3
code: S2:write 1-11

- `session_entry`: one log line per session
- Index, start and end commit, how the session ended, and a summary

notes:
The next session reads this line during Getting up to speed.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: anchor S2:write.

## 32. Demo block: what the console shows
section: S2 State and session lifecycle
minutes: 8

- The finished A/B, screen by screen
- Screen 1: the last turns, session stop and resume markers if still listed
- Screen 3: sessions with redone work, state files read
- Screen 2: each arm's board
- Screen 5: the first wrong turn and the trace link

notes:
Follow-up: which file did each arm's session 2 read first, and did it change what that session did next?

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: README.md §11.

## 33. Demo block: results
section: S2 State and session lifecycle
minutes: 7
slot: s2_experiment_dots
slot: s2_ablation_bars
live: tonight's dots; swap test verdict

- The A/B verdicts
- Tonight's dots next to the experiment dots
- `make swap-2`: the same verdicts with the labels swapped
- Layer effect: the ablation bars

[[PENDING: S2 experiment dots, continuity failures out of 10 per arm | source: M8 batch 1 | how: make experiments batch 1; make report]]

[[PENDING: ablation bars, runs passing per leave-one-layer-out configuration | source: M8 ablation | how: make experiments batch 2; make report]]

notes:
Screen 4 for the dots and the ablation bars.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: M8 experiment results (make report); make swap-2.

## 34. Runbook and next
section: S2 State and session lifecycle
minutes: 5

- Runbook: `submodules/02-state-lifecycle/demo/README.md`
- Discussion: what would your team's handoff file need for a stranger to continue tomorrow?
- Next: a 10-minute break

notes:
Run one A/B at a time in S1 to S3: the next demo launches after this one has printed its `Cost:` line.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: docs/instructor-guide.md (schedule).

## 35. Break
section: Break
minutes: 10
layout: statement
live: return time

- Back in 10 minutes

notes:
Write the return time on the slide.

Run sheet: docs/instructor-guide.md, Schedule (240 minutes).
Source: docs/instructor-guide.md (schedule).

## 36. Poll
section: S3 Scope and sandbox
minutes: 3
live: the room's poll result

- F3 idempotency keys; at risk: scope
- The ticket: "shared middleware is out of scope"; tests in a separate test phase, no app code changes
- In 10 bare-arm runs, how often does the diff touch a file outside the allowed paths, or change source in the test phase?
- (a) 0-2   (b) 3-5   (c) 6-8   (d) 9-10
- Close the poll before the launch

notes:
Both arms read the same ticket.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: submodules/03-scope-sandbox/demo/README.md §4.

## 37. Launching the live A/B: F3 idempotency keys
section: S3 Scope and sandbox
minutes: 2
slot: c3_control

- Now: run `make demo-3` in terminal B; it runs during slides 38-45, back on slide 46
- Build, then a test phase; allow lists from the task; shared middleware is off-limits
- Harness arm layers: instructions, state, scope
- Primary measure: an out-of-scope file, or a source edit in the test phase
- Zero for the harness arm by construction, so watch the secondary measures; control glance: C3

[[PENDING: C3 control results per arm | source: M8 batch 4 | how: make experiments, full dataset; make report]]

notes:
The tempting shared middleware is the trap both arms see.

The A/B must be finished by section minute 25. In pilot run 2 (12 A/Bs, sections F1-F4, two A/Bs
running in parallel on the class host, before the approved referee speed-ups) every A/B finished
within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s (8.1 min) (course pilot, run 2,
2026-10-16). Course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4 with the pilot's task variants, effort
medium, two A/Bs in parallel on the class host): wall time per A/B min 384 s, median 512 s, max 620 s.
Run 4, effort low, 2026-10-16 to 2026-10-17 (9 A/Bs, F1-F3, two in parallel): min 309 s, median 414 s,
max 565 s. Neither run timed one A/B on its own.
[[PENDING: wall time of make demo-3 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-3 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: README.md §10; docs/architecture.md §2; teamtrack/reference/f3/task.toml.

## 38. S3: what the agent may change and reach
section: S3 Scope and sandbox
minutes: 2
diagram: architecture now=L3

- Enforce one feature at a time, allowed paths per phase, and a `passes` field only the harness sets
- Explain the container limits for both arms and read a `sandbox_denied` event
- Read the S3 A/B result: out-of-scope files and source edits during the test phase
- Testing right now: edits outside the ticket, source edits during the test phase

notes:
The first three bullets are the section's objectives (course design).

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: S3 learning objectives (course design); README.md §1.

## 39. Cause: copied patterns and hard-to-undo actions
section: S3 Scope and sandbox
minutes: 2.5

- "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones" (A1, F-a-20)
- A4: "(Run this in a container, not your actual machine)"; the agent ran `pkill -9 bash` (F-a-18, F-a-19)
- A5: file operations "to the project directory only" (F-a-86)
- A6, supplementary: actions "that are difficult to reverse or affect shared systems" (F-a-21)

notes:
Four citations side by side, not merged: no single source states cause 3.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: README.md §2 (cause 3); REFERENCES.md.

## 40. Harness piece: one feature list, one feature
section: S3 Scope and sandbox
minutes: 3.5

- `feature_list.json` as the source of truth; JSON over Markdown (A2, A5; F-a-78, F-a-81, F-a-85)
- The `passes` field (F-a-79, F-a-82); one feature at a time (F-a-83)
- "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." (F-a-80)
- Course design: only the harness sets `passes`, with `evidence` and `testedAt` (A2 F-a-108, A3 F-a-110)

notes:
A2 lets the agent set `passes` (F-a-108); the course follows A3's separation of doer and judge
(F-a-110). That choice is course design.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: A2, A3, A5 in REFERENCES.md.

## 41. Allowed paths per phase
section: S3 Scope and sandbox
minutes: 3

- Build and test phases each have an allow list
- A patch outside the list is rejected
- A command's change outside the list is reverted
- The agent reads the reason
- Composite citation: A5 F-a-86, F-a-87; A1 F-a-92, F-a-98; A2 F-a-57

notes:
A1: "enforce boundaries centrally, allow autonomy locally." (F-a-98)

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: docs/architecture.md §5; A1, A2, A5 in REFERENCES.md.

## 42. Sandbox 1: why a container
section: S3 Scope and sandbox
minutes: 2
diagram: architecture now=SB1,SB2

- A4: "for each agent, a Docker container is spun up", and no internet access (F-a-88, F-a-90)
- A5's three-layer security model (F-a-86, F-a-87)
- Codex: "By default, the agent runs with network access turned off." (D21-D23)

notes:
The sandbox is highlighted on the diagram: one per arm, identical.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: A4, A5 in REFERENCES.md.

## 43. Sandbox 2: the same limits for both arms
section: S3 Scope and sandbox
minutes: 2

- `--network none`, memory without swap, 256 processes, non-root (D24-D30)
- Read-only root; only `/work` and `/tmp` writable; all capabilities dropped
- `sandbox_denied` events carry a reason code
- Never an A/B variable; detailed sandbox design is Module 2

notes:
Say: "The sandbox is the same for both arms. It is taught here, but it is never the variable."

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: docs/architecture.md §2 (sandbox policy); submodules/03-scope-sandbox/concepts.md (sandbox_denied).

## 44. Code: allowed paths and evidence
section: S3 Scope and sandbox
minutes: 5
code: S3:allowed_paths 12-17
code: S3:passes 17-21

- The three `if` checks of `reason()`: harness-only files, state files, the allow list
- `passes` is set only when the evidence is there

notes:
Section minute 25 is the switch to slide 45: check terminal B for the `Cost:` line.
[[PENDING: wall time of make demo-3 on the class host, one A/B at a time | source: M6 pilot | how: time make demo-3 on the class host (pilot run 3)]]

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50), "Check at section minute 25".
Source: anchors S3:allowed_paths, S3:passes.

## 45. Code: the sandbox policy
section: S3 Scope and sandbox
minutes: 5
code: S3:policy 7-16

- `SandboxPolicy`: identical for both arms in every run
- Network, CPU, memory, swap, processes, user, root, tmpfs, capabilities

notes:
Fields from `network` to `no_new_privileges`. Show `S3:run_args` and `S3:dockerfile` in the editor only.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: anchors S3:policy, S3:run_args, S3:dockerfile.

## 46. Demo block: what the console shows
section: S3 Scope and sandbox
minutes: 8

- The finished A/B, screen by screen
- Screen 1: blocked or reverted decisions with reasons; the gate line
- Screen 2: does each arm's app still serve the board
- Screen 3: the diff map and sandbox denials

notes:
Follow-up: the harness arm scores zero by construction. What would make you trust that it also
shipped a working feature?

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: README.md §11.

## 47. Demo block: results and the sandbox moment
section: S3 Scope and sandbox
minutes: 7
slot: s3_sandbox_denials
slot: s3_experiment_dots
live: tonight's `sandbox_denied` events; tonight's dots; swap test verdict

- Tonight's `sandbox_denied` events, or the policy printout and the experiment denial log
- The A/B verdicts
- Tonight's dots next to the experiment dots
- `make swap-3`

[[PENDING: sandbox_denied events from the experiment runs (command, reason code, arm) | source: M8 batch 1 | how: grep -h '"type":"sandbox_denied"' .shipharness/runs/*/events.jsonl]]

[[PENDING: S3 experiment dots, runs failing out of 10 per arm, with hidden tests and existing tests as secondary | source: M8 batch 1 | how: make experiments batch 1; make report]]

notes:
Sandbox moment: if screen 3 lists a denial, show its reason code and the command. If none occurred,
show the policy printout and the experiments' denial log.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50), sandbox moment.
Source: M8 experiment results (make report); make swap-3.

## 48. Runbook and next
section: S3 Scope and sandbox
minutes: 5

- Runbook: `submodules/03-scope-sandbox/demo/README.md`
- Discussion: the harness arm scores zero by construction. What else would you check?
- Next: who decides that the work is done

notes:
Expected direction: the secondary measures, especially hidden tests passed and existing tests that
keep passing.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: docs/instructor-guide.md (schedule).

## 49. Poll
section: S4 Verification
minutes: 3
live: the room's poll result

- F4 optimistic concurrency; at stake: hidden tests (69) and referee mutants (4)
- Both arms' visible tests pass at the end. Which arm passes more hidden tests and kills more mutants?
- A) Harness arm on both counts   B) Harness arm on hidden tests only   C) Harness arm on mutants only   D) No clear difference
- The final feature poll follows on slide 50

notes:
Hint after the vote: one referee mutant makes writes stop moving the version, which brings back lost
updates. A shipped test catches it only if it checks that a write moves the ETag, or that a save with
the old version gets 412.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/demo/README.md §4.

## 50. Poll: the final feature
section: S4 Verification
minutes: 1
live: the room's poll result

- F5 Bulk close: one session of 30 turns; 46 hidden tests, 3 referee mutants
- F6 Watchers: two sessions, so a context reset; 54 hidden tests, 3 mutants
- F7 Labels: two sessions, so a context reset; 64 hidden tests, 3 mutants
- The winner runs, and the runner-up after it if the session figure allows
- Close the poll before the launch

notes:
Some hidden tests combine the new feature with an earlier one.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/demo/README.md (final feature poll); final-project/README.md §2.

## 51. Launching two live A/Bs: F4 and the final
section: S4 Verification
minutes: 2
slot: c4_control

- Now: `make demo-4` in terminal B, then `make final FEATURES=<poll winner(s)>` in terminal C
- demo-4 runs during slides 52-60, back on slide 61; the final returns on slides 64-67
- F4: ETag, If-Match, issue history; counts: hidden tests passed of 69, mutants killed of 4
- Harness arm layers: all four, in both A/Bs; blinded reviewer on both diffs
- Final run cap $0.25 per arm; control glance: C4

[[PENDING: C4 control results per arm | source: M8 batch 4 | how: make experiments, full dataset; make report]]

notes:
`make final` runs its features one after another, so at most two A/Bs run at a time.

The A/B must be finished by section minute 25. In pilot run 2 (12 A/Bs, sections F1-F4, two A/Bs
running in parallel on the class host, before the approved referee speed-ups) every A/B finished
within 923 s (15.4 min); median 641 s (10.7 min), minimum 485 s (8.1 min) (course pilot, run 2,
2026-10-16). Course pilot, run 3, 2026-10-16 (12 A/Bs, F1-F4 with the pilot's task variants, effort
medium, two A/Bs in parallel on the class host): wall time per A/B min 384 s, median 512 s, max 620 s.
Run 4, effort low, 2026-10-16 to 2026-10-17 (9 A/Bs, F1-F3, two in parallel): min 309 s, median 414 s,
max 565 s. Neither run timed `make demo-4` with `make final` in parallel.
[[PENDING: wall time of make demo-4 on the class host with make final running in parallel | source: M6 pilot | how: time make demo-4 on the class host, with make final FEATURES=F5 started one minute later]]

The final A/B must be finished by 3:40, when slide 64 opens the final block; with two features
`make final` runs them one after another.
[[PENDING: wall time of one make final feature on the class host while S4 runs (make demo-4 in parallel) | source: M6 pilot | how: time make final FEATURES=F5 (and F6, F7) on the class host, started one minute after make demo-4]]

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: README.md §10, §13; Makefile `final`; teamtrack/reference/f4/task.toml; teamtrack/mutants/features/f4.jsonl.

## 52. S4: what proves the work is done
section: S4 Verification
minutes: 1
diagram: architecture now=L4

- Build verification the agent does not control: filters, mutants, house-rule checks, held-out tests, reviewer, gate
- Find the first wrong turn in a trace
- Read a fair A/B: hidden tests passed and mutants caught, as counts per run
- Testing right now: the agent's tests pass while behaviour is wrong

notes:
The first three bullets are the section's objectives (course design).

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: S4 learning objectives (course design); README.md §1.

## 53. Cause: self-grading and visible tests
section: S4 Verification
minutes: 2.5

- "agents reliably skew positive when grading their own work" (A3, F-a-15)
- "while every frontier agent saturates the visible suite, reward hacking persists" (B13, F-b-45)
- Mostly features that pass alone and fail when combined (B13, F-b-50)
- "it is easy to see tests pass and assume the job is done, when this is rarely the case." (A4, F-a-17)

notes:
Cause 4 from the opening.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: A3, A4, B13 in REFERENCES.md.

## 54. Harness piece: test filters
section: S4 Verification
minutes: 3

- Filters 1-3 from TestGen-LLM: builds, passes reliably, adds coverage (B11, F-b-16 to F-b-22)
- TestGen-LLM's evaluation funnel over 86 test classes (F-b-23)
- Filters 4 and 5 are course filters: real assertions, no source change in the test phase
- A test is kept only if it passes every filter

notes:
Say at the filter table: "Filters 1 to 3 are TestGen-LLM's; 4 and 5 are course filters."

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/concepts.md §3.3; B11 in REFERENCES.md.

## 55. Mutants and hidden tests
section: S4 Verification
minutes: 3

- ACH: mutants for the fault of concern, then hardening (B12, F-b-29, F-b-32)
- 49% of tests that uniquely kill a mutant add no line coverage (F-b-40)
- Filter-set and referee-set mutants never overlap (course design)
- Hidden tests that compose features (B13, B14; F-b-42 to F-b-44)
- 441 hidden tests across F1-F7 and controls; 69 for F4

notes:
The referee-set mutants were never visible to the filters.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/concepts.md §3.4; B12, B13, B14 in REFERENCES.md; counts in submodules/04-verification/post-class-reading/04-held-out-tests-specbench.md.

## 56. A separate evaluator and a gate
section: S4 Verification
minutes: 3

- Blinded reviewer with grading criteria (A3, F-a-110 to F-a-112)
- Clean-state gate (A2, F-a-84; A4, F-a-127)
- House rules R1-R7 (course label)

notes:
A3: separating the agent doing the work from the agent judging it is "a strong lever" (F-a-110), but
the evaluator is still inclined to be generous (F-a-112).

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: docs/architecture.md §5, §6; A2, A3, A4 in REFERENCES.md.

## 57. Read the trace
section: S4 Verification
minutes: 1.5

- Find the first wrong turn (A3, F-a-126)
- Leave one layer out to see what each part does (A3, F-a-125)
- Screen 5 shows the first wrong turn per arm, labelled as a heuristic

notes:
The ablation bars on screen 4 are the leave-one-layer-out runs.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: A3 in REFERENCES.md; docs/architecture.md §5 (leave one layer out).

## 58. Code: the filter pipeline
section: S4 Verification
minutes: 2.5
code: S4:filters 20-23,30-36

- Each proposed test goes through the filters in order
- The first failure discards it, with a reason; later filters never run

notes:
The inner `for flt in filters` loop with the exception branch folded.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: anchor S4:filters.

## 59. Code: a tenant probe and blinding
section: S4 Verification
minutes: 4
code: S4:probe 1-12

- `judge`: compare one response with what tenant isolation requires
- A foreign path must return 404; anything else fails

notes:
Show `S4:blind` in the editor. Section minute 25 falls on this slide: check terminal B for the
demo-4 `Cost:` line and terminal C for the final.
[[PENDING: wall time of make demo-4 on the class host with make final running in parallel | source: M6 pilot | how: time make demo-4 on the class host, with make final FEATURES=F5 started one minute later]]
[[PENDING: wall time of one make final feature on the class host while S4 runs (make demo-4 in parallel) | source: M6 pilot | how: time make final FEATURES=F5 (and F6, F7) on the class host, started one minute after make demo-4]]

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40), "Check at section minute 25".
Source: anchors S4:probe, S4:blind.

## 60. Code: the gate
section: S4 Verification
minutes: 3.5
code: S4:gate 13,22-29,31

- Verification the agent does not control
- Visible tests, the build-phase checks, the clean-state check
- The gate passes only if no item fails

notes:
`names = ...`, the build-phase branch, the clean-state check, and `passed = ...`.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: anchor S4:gate.

## 61. Demo block: what the console shows
section: S4 Verification
minutes: 8

- The finished demo-4 A/B, screen by screen
- Screen 1: the harness arm's last gate pills ✓ or ✗, and the gate feedback
- Screen 2: the two-tab edit conflict
- Screen 3: filter table with discard reasons, mutant table, referee counters, reviewer verdict

notes:
Say at the filter table: "The referee-set mutants were never visible to the filters."

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: README.md §11.

## 62. Demo block: results
section: S4 Verification
minutes: 7
slot: s4_experiment_dots
slot: s4_reviewer_agreement
live: tonight's two counts per arm; swap test verdict

- The A/B and reviewer verdicts
- Tonight's two counts per arm next to the experiment dots
- Reviewer agreement with the referee
- `make swap-4`

[[PENDING: S4 experiment dots, hidden tests passed of 69 and referee mutants killed of 4 per run per arm | source: M8 batch 1 | how: make experiments batch 1; make report]]

[[PENDING: reviewer agreement with the referee per arm | source: M8 batch 1 | how: make report; screen 4 reviewer agreement]]

notes:
Screen 4 for the dots and the reviewer agreement.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: M8 experiment results (make report); make swap-4.

## 63. Runbook and next
section: S4 Verification
minutes: 5

- Runbook: `submodules/04-verification/demo/README.md`
- Discussion: your agent's tests pass. What evidence would you accept before merging?
- Next: the final results

notes:
Tie the discussion to A4, F-a-17.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: docs/instructor-guide.md (schedule).

## 64. Final results: the A/B lines
section: Final results
minutes: 2
diagram: architecture now=L1,L2,L3,L4
live: terminal C's arm lines and session figure

- The poll winner, and the runner-up if it ran; all four layers
- Run cap $0.25 per arm
- No pre-registered primary measure: read hidden tests and mutants per arm

notes:
The final A/B was launched on slide 51 and ran during S4. No run starts here.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: Makefile `final`; README.md §10, §13; final-project/README.md §5.1.

## 65. Final results: console
section: Final results
minutes: 4
live: screens 1, 3, and 5 of the finished final A/B, both arms

- Screen 1: the turns, harness decisions, gate pills
- Screen 3: evidence, filters, mutants, reviewer verdict
- Screen 5: the first wrong turn and the trace links

notes:
Both arms, side by side.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: README.md §11; final-project/README.md §4.

## 66. Final results: boards
section: Final results
minutes: 2
live: both boards side by side

- Screen 2: each arm's running board as an Acme user
- Look for ⚠ other-org and ⧉ duplicate marks

notes:
The marks come from trusted data- attributes, not from the agent.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: README.md §11 (screen 2).

## 67. Final results: screen 4, report, and LangSmith comparison
section: Final results
minutes: 5
code: Final:dots 23-30
slot: experiment_report
live: tonight's final

- Screen 4: tonight's final next to the experiment results
- `make report` output and the LangSmith comparison view
- Filled dot = passed, hollow = failed: never colour alone

[[PENDING: experiment report and LangSmith comparison link | source: M8 batch 1 | how: make report; comparison_url in exports/experiments/]]

notes:
The fill and stroke lines of the dot plot.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: anchor Final:dots; docs/architecture.md §10.

## 68. Assignments (1 of 2)
section: Wrap-up
minutes: 1.5

- A1 Instructions: `submodules/01-instructions/assignment/`, budget ≤ $2.50 and 150 traces
- A2 State and session lifecycle: `submodules/02-state-lifecycle/assignment/`, ≤ $1.50 and 60 traces
- Each: a brief with grading criteria, a starter folder, an offline self-check, one live step

notes:
Learner budgets are course design.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: submodules/01-instructions/assignment/README.md, submodules/02-state-lifecycle/assignment/README.md.

## 69. Assignments (2 of 2)
section: Wrap-up
minutes: 1.5

- A3 Scope and sandbox: `submodules/03-scope-sandbox/assignment/`, ≤ $0.25 and 30 traces
- A4 Verification and portfolio: `submodules/04-verification/assignment/`, ≤ $1.75 and 120 traces
- Total ≤ $6 and ≤ 400 traces
- Thursday review

notes:
Learner budgets are course design.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: submodules/03-scope-sandbox/assignment/README.md, submodules/04-verification/assignment/README.md.

## 70. Skills and templates to take home
section: Wrap-up
minutes: 2
code: Final:skill_template 1-6

- `harness-setup`, `assured-tests`, `house-rules`, `skill-template`
- Install into `.claude/skills/` and `.agents/skills/`
- Each follows the Agent Skills format (B1)

notes:
The `skill-template` frontmatter from `name` to `license`.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: B1 in REFERENCES.md; README.md §14; anchor Final:skill_template.

## 71. References (1 of 2)
section: Wrap-up
minutes: 1

- A1 Harness engineering: leveraging Codex in an agent-first world · Ryan Lopopolo, OpenAI · 2026-02-11
- A2 Effective harnesses for long-running agents · Justin Young, Anthropic · 2025-11-26
- A3 Harness design for long-running application development · Prithvi Rajasekaran, Anthropic · 2026-03-24
- A4 Building a C compiler with a team of parallel Claudes · Nicholas Carlini, Anthropic · 2026-02-05
- A5 Autonomous Coding Agent Demo (README) · Anthropic · 2025-11-26
- A6 Prompting best practices · Anthropic, Claude docs · living page; A7 Using PLANS.md · Aaron Friel, OpenAI · 2025-10-07

notes:
Full links in REFERENCES.md.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: REFERENCES.md.

## 72. References (2 of 2)
section: Wrap-up
minutes: 1

- B1 Agent Skills Specification; B2 What are skills?; B3 How to add skills support · Agent Skills project
- B4-B6 agentskills repo and skills-ref; B7 Claude Code skills; B8 Codex skills; B9-B10 Cursor skills
- B11 TestGen-LLM · Alshahwan et al., Meta · 2024; B12 ACH · Foster et al., Meta · 2025
- B13 SpecBench · Zhao, Srikanth, Wu, Jiang (Weco AI) · 2026; B14 WecoAI/SpecBench repo
- B15 (Spec-Bench, speculative decoding) is unrelated and not cited

notes:
Full links in REFERENCES.md.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: REFERENCES.md.
