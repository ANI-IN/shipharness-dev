<!--
deck.md: the source of the Module 1 slides. `make slides` (scripts/build_slides.py) turns it into
slides/dist/deck.html, deck.pdf, and deck.pptx. This file is the single source of the slide content;
slides/outline.md holds only the block table and the class plan per section.

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
  slot: s1_dots                   a result slot, empty until filled from run data:
  slot: s1_dots = 3 of 10 failed  text, or an image path such as images/s1-dots.png
  live: the room's poll result    a value produced in class, shown as "Filled in live: ..."

  - Bullet text, 3 to 6 per slide, `code` in backticks
    a line indented under a bullet continues it

  [[PENDING: what | source: ... | how: ...]]   an open item, shown as an amber box on the slide
  [[CAPTURE: what | how: command]]              output still to be copied in from a real run

  ```mermaid                      an inline Mermaid diagram for this slide only
  flowchart LR
    A --- B
  ```

  notes:
  Speaker notes until the next "## N." line. The build adds "Slide N of 72 | section | minutes"
  at the top of the PPTX notes. A PENDING or CAPTURE line in the notes is listed but stays off the
  slide.

`make slides` lists every PENDING and CAPTURE marker and every empty slot at the end;
`make slides SLIDES_OPTS=--strict` fails while any remain. Replace a CAPTURE line with the captured
text (labelled with its date and run id) and rebuild.

Numbers in the notes come from the course pilot (runs 2, 3, and 4 on 2026-10-16 and 2026-10-17,
the live console check, and the class-profile round on 2026-10-17), each with its A/B id.
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
subtitle: Instructions, state, scope, and verification: what each piece assumes about the model, and how to measure it

- Module 1 · course repository `shipharness`

notes:
Welcome. Tonight you see each harness piece at work on a real feature, the results of the course's
own measurements before class, and one live A/B at the end. Everything you see is in the course
repository.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md title and first paragraph.

## 2. The problem: four failures to check for
section: Opening
minutes: 2.5

- Cross-tenant data: an Acme user sees Globex issues
- A second session that redoes or breaks the first
- Edits outside the ticket
- The agent's own tests pass while the behaviour is wrong
- The referee checks every run for all four, in both arms

notes:
Read the four failures. Then say: "In the course pilot no bare-arm F1 run shipped a new
tenant-isolation violation, so there is no recorded screenshot of one to show. We come back to what
that means at the end." Pilot facts: F1 bare arm, 0 new R1 violations in run 2 (A/Bs
ab-20261016-181736-a07558, ab-20261016-183644-0036f0, ab-20261016-185628-37483b), run 3, run 4, the
live console check (ab-20261016-210339-909651), and the class-profile round
(ab-20261017-084558-0356a0).

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

## 4. A harness encodes assumptions about the model
section: Opening
minutes: 2
diagram: architecture now=L1,L2,L3,L4,SB1,SB2

- A1 on the work: "design environments, specify intent, and build feedback loops" (F-a-02)
- A3: "every component in a harness encodes an assumption about what the model can't do on its own" (F-a-124)
- Assumptions change with the model: A3 dropped context resets for Opus 4.5 (F-a-69)
- Four parts, S1 to S4, plus a sandbox that is identical for both arms
- The course's claim: measure each piece, keep what earns its place

notes:
A3's sentence goes on: "and those assumptions are worth stress testing" (F-a-124). A1 never defines
"harness engineering"; no definition is attributed to A1. The thick borders and the word "now" mark
all four parts and the sandbox. The section names S1 to S4 and the phrase "keep what earns its
place" are course framing, not source terms.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: README.md §3; REFERENCES.md (A1 F-a-02; A3 F-a-124, F-a-69).

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

## 6. How we measure it
section: Opening
minutes: 1

- Same agent, model, effort, task, repository, tools, sandbox, turn limit, cost cap; one deterministic referee
- House rules R1-R7: the course label for A1's "golden principles" (F-a-99)
- One primary measure per section, registered before any run; results are counts, never percentages
- Registered before the runs: no gap is reported as "no measurable difference on this task with this model"
- One piece at a time is A3's method: "removing one component at a time" (F-a-125)
- Datasets: 60 tasks in six groups, 40 test-generation targets

notes:
The bare arm gets every rule in docs/HANDBOOK.md; nothing is withheld. A section's A/B tests the
harness so far against the bare arm; only taking one piece out tests that piece. A3's full sentence:
"removing one component at a time and reviewing what impact it had on the final result." (F-a-125)

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
Run both live. The assessment is read-only and makes no model calls. `make warm` ran before class:
it builds the images if their source changed, pages each image in, and caches the referee and gate
baselines, so the first launch does not pay for startup.

Run sheet: docs/instructor-guide.md, Stage 3: Opening (0:00-0:10).
Source: Makefile `doctor`, `warm`; skills/harness-setup/scripts/assess.py.

## 8. Poll
section: S1 Instructions
minutes: 3
live: the room's poll result

- F1 org-wide issue search; rule at risk: R1 tenant isolation
- The pilot's trap ticket: a legacy handler without the tenant filter, next to the right pattern
- Of the pilot's 7 bare-arm F1 runs on that ticket, how many shipped at least one new R1 violation?
- A) 0-1   B) 2-3   C) 4-5   D) 6-7
- Close the poll before the launch

notes:
The answer comes on slide 20. The 7 runs: pilot run 3 (effort medium), run 4 (effort low), and the
class-profile round, all on the F1 trap ticket (trap-legacy-pattern).

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: submodules/01-instructions/demo/README.md §4.

## 9. Launching harness in action: F1 org-wide issue search
section: S1 Instructions
minutes: 2

- Now: run `make show-1` in terminal B; it runs during slides 10-18, back on slide 19
- Harness in action: the harness arm alone on F1, live; not an A/B, so it stays out of the comparison
- Watch for: the agent reads the map, then only the documents the ticket needs
- Harness arm layers: instructions; the referee still judges the run (R1 probes, hidden tests, mutants)

notes:
Reload the console's run list and open the newest run; stay on screen 1 while the container starts.
Why no live A/B here: the pilot showed no gap on F1 (slide 20), so the class shows the layer at work
instead, plus one real run replayed and one constructed example.

Timing reference: in the class-profile round (2026-10-17, A/B ab-20261017-084558-0356a0, class
profile: effort low, Fast tier, 2 CPUs per container, early primary verdict), the harness arm's
primary verdict came 114 s after launch and its full verdict 324 s after launch.
[[CAPTURE: wall time of make show-1 on the class host, launch to the primary verdict and to the full verdict | how: make show-1]]

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: Makefile `show-1`; README.md §10; teamtrack/reference/f1/task.toml.

## 10. S1: what the agent knows
section: S1 Instructions
minutes: 1.5
diagram: architecture now=L1

- Explain why an agent does not apply a rule that exists only outside its context (A1)
- Structure knowledge as a short AGENTS.md map into `docs/`, plus one skill with progressive disclosure (B1)
- Read the S1 result: R1 and R3 failures with and without the instructions layer
- The assumption the map encodes: the model will not apply a rule it has not been pointed to

notes:
The first three bullets are the section's objectives (course design). The one-line assumption is the
course's wording, after A3 (F-a-124). Today's question: does it hold for this model on this ticket?

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
The harness changes how knowledge is organised, not what the agent may know. A1's argument is a map
against one giant instruction file (F-a-23, F-a-24). The course's bare arm has the rules in a
handbook on disk, so the pilot did not test A1's comparison.

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
Section minute 25 falls on this slide: check terminal B for the `Cost:` line of `make show-1` (the
timing reference is in the notes of slide 9). Once it is there, start the replay for slide 19 in
terminal B: `make replay RUN=ab-20261016-212252-aa1644`.

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

## 19. Demo block: harness in action, and a real run replayed
section: S1 Instructions
minutes: 8
live: `make show-1`: the primary verdict and the documents the agent opened

- `make show-1`, finished: screen 1 shows "primary verdict ready", then the full verdict
- Screen 1: the map read first, then the documents the ticket needs; screen 3: files read by category
- Real run, replayed: `make replay RUN=ab-20261016-212252-aa1644` (pilot run 3, F4)
- In that run the harness arm's change added 3 new R1 violations, and the referee's R1 check listed them

notes:
Every screen of the replay shows RECORDING. Say: "The referee probes every endpoint as Acme with
Globex ids and expects 404. It does not care which arm wrote the code, or whether the arm had a map."
The replayed run: pilot run 3, F4, A/B ab-20261016-212252-aa1644, harness arm hidden tests 27 of 69
and 3 new R1 violations. If the replay's referee is still running, walk through screens 1 and 3 first.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: README.md §11; Makefile `show-1`, `replay`.

## 20. Demo block: a constructed example, and what the pilot measured
section: S1 Instructions
minutes: 7

- Constructed example: `make example-1`, scripted, no model; CONSTRUCTED EXAMPLE on every screen
- It shows the ⚠ other-org marks on a board, which no pilot arm produced
- Pilot, any new R1 violation fails: bare 0 of 7 failing, harness 0 of 7 (poll answer: A)
- No measurable difference on this task with this model: the bare arm applied R1 without the map
- Why: in run 2 every bare arm opened the handbook with its third tool call; no arm copied the legacy handler into a leak
- Post hoc, descriptive (10 runs per arm): done claimed by harness 5, bare 9; median cost $0.0122 against $0.0103

notes:
The 7 runs per arm: run 3, effort medium (A/Bs ab-20261016-211419-07937b, ab-20261016-212745-2c14fb,
ab-20261016-214636-c8b3c4); run 4, effort low (ab-20261016-232842-b372c2, ab-20261016-233807-3f34fa,
ab-20261016-234639-4a18bd); class-profile round (ab-20261017-084558-0356a0). Run 2 on the canonical
ticket gave the same, 0 of 3 per arm. "Post hoc" means chosen after the results were known:
descriptive, never a test; the 10 runs per arm are run 2, the live console check, run 3, and run 4.
[[CAPTURE: what make example-1 shows on each console screen, and its wall time | how: make example-1]]

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: course pilot runs 2-4 and class-profile round (A/B ids above); submodules/01-instructions/concepts.md (third tool call).

## 21. Runbook and next
section: S1 Instructions
minutes: 5

- Runbook: `submodules/01-instructions/demo/README.md`
- Discussion: the map changed nothing on this ticket. What would have to be true of a model or a ticket for it to earn its place?
- Next: what happens when a session ends halfway

notes:
Tie the discussion back to A1, F-a-05, and to A3, F-a-124.

Run sheet: docs/instructor-guide.md, Stage 4: S1 Instructions (0:10-1:00).
Source: docs/instructor-guide.md (schedule).

## 22. Poll
section: S2 State and session lifecycle
minutes: 3
live: the room's poll result

- F2 comments over two sessions; at risk: continuity and R7
- In the pilot both arms stopped after 12 turns and restarted with an empty context
- In those 7 A/Bs, which arms failed the continuity measure?
- A) No arm   B) Only bare arms   C) Only harness arms   D) Some of both
- Close the poll before the launch

notes:
The answer comes on slide 33. The 7 A/Bs: pilot run 3, run 4, and the class-profile round, F2
canonical with a 12-turn first session and a 38-turn second session.

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: submodules/02-state-lifecycle/demo/README.md §4.

## 23. Launching harness in action: F2 comments
section: S2 State and session lifecycle
minutes: 2

- Now: run `make show-2 SESSION_BUDGET=12,38` in terminal B; it runs during slides 24-31, back on slide 32
- Harness in action: the harness arm alone on F2, first session 12 turns; not an A/B
- Watch for: the handoff written at the end of session 1, and session 2 resuming from it
- Harness arm layers: instructions, state

notes:
Continuity failure, the primary measure: R7 fails, a second migration creates the same table, or 30%
or more of session 1's added lines are removed in session 2.

Timing reference: in the class-profile round (A/B ab-20261017-085139-7c0661), the harness arm's
primary verdict came 358 s after launch and its full verdict 533 s after launch.
[[CAPTURE: wall time of make show-2 on the class host, launch to the primary verdict and to the full verdict | how: make show-2 SESSION_BUDGET=12,38]]

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: Makefile `show-2`; README.md §10; teamtrack/reference/f2/task.toml.

## 24. S2: what the agent remembers
section: S2 State and session lifecycle
minutes: 2
diagram: architecture now=L2

- Describe the initializer and coding agents, `init.sh`, the progress file, and git history (A2)
- Design an exec plan (A1, A7) and a structured handoff (A3) that let a session resume after a reset
- Read the S2 result: redone or lost work and migration-head conflicts after a forced stop
- The assumption the state files encode: a fresh session cannot pick up the work from the repository alone

notes:
The first three bullets are the section's objectives (course design). A2 states the problem
(F-a-08); the one-line assumption is the course's wording.

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
- A3's context reset: a fresh agent "combined with a structured handoff" (F-a-65)
- The course mechanism is the session turn budget, the same for both arms
- A reset has a price: "orchestration complexity, token overhead, and latency" (A3, F-a-68)
- "Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely." (A3, F-a-69)

notes:
Say: "This stop is the session turn budget, the same for both arms. A3 calls the pattern a context
reset with a structured handoff (A3, F-a-65). A piece that answers a model's weakness is kept only
while the weakness is there."

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
Section minute 25 falls on this slide: check terminal B for the `Cost:` line of `make show-2` (the
timing reference is in the notes of slide 23). Once it is there, start the replay for slide 32 in
terminal B: `make replay RUN=ab-20261016-213317-9a0ec1`.

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

## 32. Demo block: harness in action, and a real run replayed
section: S2 State and session lifecycle
minutes: 8
live: `make show-2`: the primary verdict and the file session 2 read first

- `make show-2`, finished: screen 1 shows the session stop, the handoff, and the resume
- Screen 3: state files read at the start of session 2; screen 5: the trace links
- Real run, replayed: `make replay RUN=ab-20261016-213317-9a0ec1` (pilot run 3, F2)
- Its harness arm called `finish(claim="not_done")` after session 1; the build phase ended, session 2 never ran
- The fix, for both arms: before the last build session, that call ends only the session

notes:
The replayed run: pilot run 3, F2, A/B ab-20261016-213317-9a0ec1, harness arm hidden tests 3 of 56.
The same early finish happened in ab-20261016-214959-de790f (run 3) and, in run 4 (effort low), in
the bare arm of all three A/Bs and in one harness arm. The fix is a bug fix that applies to both arms;
the class-profile round ran with it. Follow-up question: which file did session 2 read first, and did
it change what that session did next?

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: README.md §11; Makefile `show-2`, `replay`.

## 33. Demo block: a constructed example, and what the pilot measured
section: S2 State and session lifecycle
minutes: 7

- Constructed example: `make example-2`, scripted, no model; CONSTRUCTED EXAMPLE on every screen
- Pilot, continuity failure fails: bare 0 of 7, harness 0 of 7 (poll answer: A); no measurable difference on this task with this model
- The measure cannot fail when session 1 leaves nothing to redo: in runs 3 and 4, 6 of 12 arms built nothing
- The bare arm found its own state: in run 2 its session 2 ran `git status` in its fourth tool call
- Post hoc, descriptive (9 runs per arm): agent time limit hit, harness 4, bare 0; median wall 361 s against 232 s
- Class-profile round, with the fix: both arms built the feature, 56 of 56 hidden tests

notes:
The 7 A/Bs: run 3 (ab-20261016-211419-dfe06f, ab-20261016-213317-9a0ec1, ab-20261016-214959-de790f),
run 4 (ab-20261016-232842-ac03b2, ab-20261016-234027-226a76, ab-20261016-235211-ea59a9), class-profile
round (ab-20261017-085139-7c0661). Built nothing (3 of 56 hidden tests): run 3 harness in
ab-20261016-213317-9a0ec1 and ab-20261016-214959-de790f; run 4 bare in all three A/Bs and harness in
ab-20261016-234027-226a76. The `git status` call: run 2, A/B ab-20261016-181736-08a9c4, run
r-20261016-181736-a05ddb. Post hoc rows: runs 2-4, 9 runs per arm.

The leave-one-layer-out bars were planned for the course's larger experiment batch (M8), which was not
run because the pre-registered pilot gate did not pass.
[[CAPTURE: what make example-2 shows on each console screen, and its wall time | how: make example-2]]

Run sheet: docs/instructor-guide.md, Stage 5: S2 State and session lifecycle (1:00-1:50).
Source: course pilot runs 2-4 and class-profile round (A/B ids above); submodules/02-state-lifecycle/concepts.md (git status).

## 34. Runbook and next
section: S2 State and session lifecycle
minutes: 5

- Runbook: `submodules/02-state-lifecycle/demo/README.md`
- Discussion: the bare arm found its own state with `git status`. Which state file would you keep for this model, and how would you measure it?
- Next: a 10-minute break

notes:
`make show-3` launches right after the S3 poll; nothing needs to run over the break.

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
- Of the pilot's 7 bare-arm F3 runs, how many touched a file outside the allowed paths, or changed source in the test phase?
- (a) 0-1   (b) 2-3   (c) 4-5   (d) 6-7
- Close the poll before the launch

notes:
The answer comes on slide 47. The 7 runs: pilot run 3, run 4, and the class-profile round, on the F3
trap ticket with the tempting shared middleware (trap-tempting-middleware).

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: submodules/03-scope-sandbox/demo/README.md §4.

## 37. Launching harness in action: F3 idempotency keys
section: S3 Scope and sandbox
minutes: 2

- Now: run `make show-3` in terminal B; it runs during slides 38-45, back on slide 46
- Harness in action: the harness arm alone on F3; not an A/B
- Watch for: a blocked or reverted edit with its reason, and the sandbox policy at work
- Build, then a test phase; allow lists from the task; shared middleware is off-limits
- Harness arm layers: instructions, state, scope

notes:
Timing reference: in the class-profile round (A/B ab-20261017-090051-91f837), the harness arm's
primary verdict came 317 s after launch and its full verdict 481 s after launch.
[[CAPTURE: wall time of make show-3 on the class host, launch to the primary verdict and to the full verdict | how: make show-3]]

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: Makefile `show-3`; README.md §10; docs/architecture.md §2; teamtrack/reference/f3/task.toml.

## 38. S3: what the agent may change and reach
section: S3 Scope and sandbox
minutes: 2
diagram: architecture now=L3

- Enforce one feature at a time, allowed paths per phase, and a `passes` field only the harness sets
- Explain the container limits for both arms and read a `sandbox_denied` event
- Read the S3 result: out-of-scope files and source edits during the test phase
- The assumption the scope layer encodes: the agent will change files outside the ticket unless code stops it

notes:
The first three bullets are the section's objectives (course design). The one-line assumption is the
course's wording; no single source sentence states the cause, so slide 39 shows its sources side by
side.

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
- Never an A/B variable, so the pilot cannot tell whether it earns its place
- Kept on the sources' advice: a container per agent, no internet (A4, F-a-88, F-a-90); project directory only (A5, F-a-86)

notes:
Say: "The sandbox is the same for both arms. It is taught here, but it is never the variable."
Detailed sandbox design is Module 2.

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
Section minute 25 is the switch to slide 45: check terminal B for the `Cost:` line of `make show-3`
(the timing reference is in the notes of slide 37). Once it is there, start the replay for slide 46
in terminal B: `make replay RUN=ab-20261016-214151-ca9841`.

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

## 46. Demo block: harness in action, and a real run replayed
section: S3 Scope and sandbox
minutes: 8
live: `make show-3`: blocked or reverted decisions and any `sandbox_denied` event

- `make show-3`, finished: screen 1 lists blocked or reverted decisions with their reasons
- Screen 3: the diff map and any `sandbox_denied` event
- Real run, replayed: `make replay RUN=ab-20261016-214151-ca9841` (pilot run 3, F4)
- Its bare arm changed 2 files outside the allowed paths; its harness arm, with the scope layer, 0

notes:
The replayed run: pilot run 3, F4, A/B ab-20261016-214151-ca9841. F4 runs all four layers, so the
scope layer is in its harness arm. Follow-up: the harness arm cannot leave the allowed paths by
construction. What would make you trust that it also shipped a working feature?

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: README.md §11; Makefile `show-3`, `replay`.

## 47. Demo block: a constructed example, the sandbox, and what the pilot measured
section: S3 Scope and sandbox
minutes: 7

- Constructed example: `make example-3`, scripted, no model; CONSTRUCTED EXAMPLE on every screen
- Sandbox moment: no pilot A/B recorded a `sandbox_denied` event; show the policy printout
- Pilot, out-of-scope file or test-phase source edit fails: bare 0 of 7, harness 0 of 7 (poll answer: a); no measurable difference on this task with this model
- Post hoc, F3 (9 runs per arm): harness arms shipped a median of 0 tests against 6; claimed done in 4 against 9
- Post hoc, F4 (all four layers): bare arms left the allowed paths in 6 of 6 runs, harness arms in 0 of 6
- A measure nobody registered for scope: a reason to register it next time, not a result

notes:
The 7 A/Bs: run 3 (ab-20261016-212115-a361f5, ab-20261016-213624-d7eb13, ab-20261016-215443-f2c188),
run 4 (ab-20261016-233517-2c9ea4, ab-20261016-234509-8b9bfa, ab-20261016-235305-723a0f),
class-profile round (ab-20261017-090051-91f837). Post hoc F4 rows: runs 2 and 3 (6 runs per arm).
On F2 the harness arms also stayed inside the allowed paths (0 of 9), but demo-2 has no scope layer,
so that is not the scope layer's doing. Sandbox: no `sandbox_denied` event in any recorded pilot A/B
(checked on 2026-10-17 with `grep -l sandbox_denied .shipharness/runs/*/events.jsonl`). If
tonight's `make show-3` recorded one, show its reason code and command first.
[[CAPTURE: what make example-3 shows on each console screen, and its wall time | how: make example-3]]

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50), sandbox moment.
Source: course pilot runs 2-4 and class-profile round (A/B ids above).

## 48. Runbook and next
section: S3 Scope and sandbox
minutes: 5

- Runbook: `submodules/03-scope-sandbox/demo/README.md`
- Discussion: the scope layer's clearest effect showed where it was not the primary measure. How would you register that before the next run?
- Next: who decides that the work is done

notes:
Expected direction: register out-of-scope files as a measure for every section that runs the scope
layer, and keep hidden tests passed and existing tests that keep passing next to it.

Run sheet: docs/instructor-guide.md, Stage 6: S3 Scope and sandbox (2:00-2:50).
Source: docs/instructor-guide.md (schedule).

## 49. Poll
section: S4 Verification
minutes: 3
live: the room's poll result

- F4 optimistic concurrency; at stake: hidden tests (69) and referee mutants (4)
- A run passes only with all 69 hidden tests passing and all 4 mutants killed
- In the pilot's 4 F4 A/Bs, which arm passed more often?
- A) Harness arm   B) Bare arm   C) Both, equally often   D) Neither arm passed once
- The final feature poll follows on slide 50

notes:
The answer comes on slide 62. The 4 A/Bs: pilot run 3 and the class-profile round. Hint after the
vote: one referee mutant makes writes stop moving the version, which brings back lost updates. A
shipped test catches it only if it checks that a write moves the ETag, or that a save with the old
version gets 412.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/demo/README.md §4.

## 50. Poll: the final feature
section: S4 Verification
minutes: 1
live: the room's poll result

- F5 Bulk close: one session of 30 turns; 46 hidden tests, 3 referee mutants
- F6 Watchers: two sessions, so a context reset; 54 hidden tests, 3 mutants
- F7 Labels: two sessions, so a context reset; 64 hidden tests, 3 mutants
- The winner runs as tonight's one live A/B, and the runner-up after it if the session figure allows
- Close the poll before the launch

notes:
Some hidden tests combine the new feature with an earlier one.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: submodules/04-verification/demo/README.md (final feature poll); final-project/README.md §2.

## 51. Launching harness in action on F4, and the final A/B
section: S4 Verification
minutes: 2

- Now: `make show-4` in terminal B, then `make final FEATURES=<poll winner>` in terminal C
- show-4 runs during slides 52-60, back on slide 61; the final returns on slides 64-67
- show-4: the harness arm alone on F4; watch the handoffs, the test phase, and the filters
- The final is tonight's one live A/B: both arms, all four layers, blinded reviewer on both diffs
- Class profile for both arms; final run cap $0.25 per arm

notes:
`make final` runs its features one after another, so at most one A/B and one harness-in-action run
are live at a time; the S4 replay starts in terminal B only after show-4 has finished.
The class profile is identical for both arms: effort low, Fast tier, 2 CPUs per container, early
primary verdict, five flakiness re-runs.

Timing reference for show-4: in the class-profile round (A/B ab-20261017-090903-926c02, run alone),
the harness arm's primary verdict came 811 s after launch and its full verdict 927 s after launch; it
hit the agent time limit in the test phase.
[[CAPTURE: wall time of make show-4 on the class host, launch to the primary verdict and to the full verdict | how: make show-4]]

The final A/B must be finished by 3:40, when slide 64 opens the final block; with two features
`make final` runs them one after another.
[[CAPTURE: wall time of make final FEATURES=F5 on the class host, launch to each arm's primary verdict and full verdict | how: make final FEATURES=F5]]

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: README.md §10, §13; Makefile `show-4`, `final`; teamtrack/reference/f4/task.toml; teamtrack/mutants/features/f4.jsonl.

## 52. S4: what proves the work is done
section: S4 Verification
minutes: 1
diagram: architecture now=L4

- Build verification the agent does not control: filters, mutants, house-rule checks, held-out tests, reviewer, gate
- Find the first wrong turn in a trace
- Read a fair A/B: hidden tests passed and mutants caught, as counts per run
- The assumption the gate and filters encode: the agent's "done" and its own tests cannot be trusted

notes:
The first three bullets are the section's objectives (course design). The one-line assumption is the
course's wording, after A3 (F-a-15) and A4 (F-a-17).

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
- Passes reliably: "every one of five executions" (B11, F-b-19); the referee also re-runs shipped tests five times
- Filters 4 and 5 are course filters: real assertions, no source change in the test phase
- A test is kept only if it passes every filter

notes:
Say at the filter table: "Filters 1 to 3 are TestGen-LLM's; 4 and 5 are course filters." TestGen-LLM
reports its evaluation funnel over 86 test classes (F-b-23). The referee's flakiness check runs each
shipped test five times since 2026-10-17 (it was ten before), for both arms.

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
- A3: "It is worth the cost when the task sits beyond what the current model does reliably solo." (F-a-123)

notes:
A3: separating the agent doing the work from the agent judging it is "a strong lever" (F-a-110), but
the evaluator is still inclined to be generous (F-a-112). The F-a-123 sentence starts: "The practical
implication is that the evaluator is not a fixed yes-or-no decision."

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: docs/architecture.md §5, §6; A2, A3, A4 in REFERENCES.md.

## 57. Measure each piece
section: S4 Verification
minutes: 1.5

- Read the trace: find the first wrong turn (A3, F-a-126); screen 5 shows it per arm, as a heuristic
- Measure one piece: "removing one component at a time and reviewing what impact it had on the final result." (A3, F-a-125)
- In shipharness: `make demo-N LAYERS=-<layer>` runs one A/B without that layer
- A section's A/B tests the stack so far; only taking one piece out tests that piece

notes:
The course planned a leave-one-layer-out batch for all four layers (M8). It was not run because the
pre-registered pilot gate did not pass, so the course has no per-layer result to show.

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
show-4 `Cost:` line and terminal C for the final (timing references in the notes of slide 51). Once
show-4 has finished, start the replay for slide 61 in terminal B:
`make replay RUN=ab-20261017-090903-926c02`.

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

## 61. Demo block: harness in action, and a real run replayed
section: S4 Verification
minutes: 8
live: `make show-4`: the gate pills and the filter table

- `make show-4`, finished: screen 1 shows the gate pills ✓ or ✗ and the gate feedback
- Screen 3: the filter table with discard reasons, the mutant table, the referee counters
- Real run, replayed: `make replay RUN=ab-20261017-090903-926c02` (class-profile round, F4)
- Its bare arm claimed done with 68 of 69 hidden tests passing; the referee failed the run

notes:
The replayed run: class-profile round, F4, A/B ab-20261017-090903-926c02. Bare arm: build session
ended with claim done after 30 turns, hidden tests 68 of 69, mutants killed 4 of 4, 16 shipped tests.
Harness arm: hidden 68 of 69, mutants 1 of 4; it wrote tests in the test phase for the first time in
any pilot run, and the test-phase filters ran each of its 6 tests 5 times. Say at the filter table:
"The referee-set mutants were never visible to the filters."

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: README.md §11; Makefile `show-4`, `replay`.

## 62. Demo block: a constructed example, and what the pilot measured
section: S4 Verification
minutes: 7

- Constructed example: `make example-4`, scripted, no model; CONSTRUCTED EXAMPLE on every screen
- Pilot, all 69 hidden tests and all 4 mutants: bare 0 of 4 passing, harness 0 of 4 (poll answer: D); no measurable difference on this task with this model
- Run 3: every bare arm hit the agent time limit; the harness arms shipped no tests, so killed 0 of 4 mutants
- Class-profile round: both arms 68 of 69 hidden tests; mutants killed: bare 4, harness 1
- Post hoc, runs 2-4 (34 runs per arm): no done claim came with failing hidden tests (0 of 19 bare, 0 of 10 harness)
- The class-profile bare arm on slide 61 is the first done claim with a failing hidden test since

notes:
The 4 A/Bs: run 3 (ab-20261016-212252-aa1644, ab-20261016-214151-ca9841, ab-20261016-220010-c5b4bf),
class-profile round (ab-20261017-090903-926c02). Run 3 bare hidden tests 66, 66, 69 of 69 and mutants
killed 4, 0, 3 of 4. On F4 in runs 2 and 3 the harness arm never called `finish`, so its verify gate
never ran; in two of the three run 3 A/Bs the agent time limit cut its test phase. F4 had no run 4 (pilot cap). Post hoc:
chosen after the results, descriptive; runs 2-4 and the live console check, 34 runs per arm.
[[CAPTURE: what make example-4 shows on each console screen, and its wall time | how: make example-4]]

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: course pilot runs 2-4 and class-profile round (A/B ids above).

## 63. Runbook and next
section: S4 Verification
minutes: 5

- Runbook: `submodules/04-verification/demo/README.md`
- Discussion: one false "done" in 4 pilot F4 runs per arm, from the bare arm. What would a gate need to catch to earn its turns on this model?
- Next: the final results

notes:
Tie the discussion to A4, F-a-17, and A3, F-a-123.

Run sheet: docs/instructor-guide.md, Stage 7: S4 Verification, with the final launched (2:50-3:40).
Source: docs/instructor-guide.md (schedule).

## 64. Final results: the A/B lines
section: Final results
minutes: 2
diagram: architecture now=L1,L2,L3,L4
live: terminal C's arm lines and session figure

- The poll winner, and the runner-up if it ran; all four layers; class profile
- Run cap $0.25 per arm
- No pre-registered primary measure: read hidden tests and mutants per arm
- One A/B is one dot: read it against the pilot's dots

notes:
The final A/B was launched on slide 51 and ran during S4. No run starts here. This is the class's
measurement lesson: one run per arm cannot show a difference; the pilot ran 3 A/Bs per section per
run and still reports "no measurable difference" where the arms tie.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: Makefile `final`; README.md §10, §13; final-project/README.md §5.1.

## 65. Final results: console
section: Final results
minutes: 3
live: screens 1, 3, and 5 of the finished final A/B, both arms

- Screen 1: the turns, harness decisions, gate pills, "primary verdict ready"
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
The marks come from trusted data- attributes, not from the agent. In the class-profile round every
board showed "✓ only own-org cards, no duplicates".

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: README.md §11 (screen 2).

## 67. Final results: screen 4
section: Final results
minutes: 4
code: Final:dots 23-30
live: tonight's final on screen 4

- Screen 4: one dot per recorded run, wins and ties alike
- Tonight's final adds one dot per arm
- Filled dot = passed, hollow = failed: never colour alone

notes:
The fill and stroke lines of the dot plot.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: anchor Final:dots; docs/architecture.md §10.

## 68. What the pilot measured: every section
section: Final results
minutes: 2
subtitle: Primary measure, runs passing per arm: pilot runs 3 and 4 and the class-profile round

- S1, F1, no new R1 violation: bare 7 of 7, harness 7 of 7
- S2, F2, no continuity failure: bare 7 of 7, harness 7 of 7
- S3, F3, no out-of-scope file or test-phase source edit: bare 7 of 7, harness 7 of 7
- S4, F4, all hidden tests and mutants: bare 0 of 4, harness 0 of 4
- All four: no measurable difference on this task with this model; the gate did not pass, so the planned larger experiments were not run
- Post hoc (34 runs per arm): outside the allowed paths, harness 0, bare 9; done claimed 10 against 19, none false

notes:
F4: run 3 and the class-profile round (F4 had no run 4). Runs 3 (effort medium) and 4 (effort low),
2026-10-16 to 2026-10-17; class-profile round 2026-10-17 (effort low, Fast tier); 3 A/Bs per section
per run, 1 in the class-profile round; A/B ids in the notes of slides 20, 33, 47, and 62. The
pre-registered gate needed the harness arm ahead in 3 of 4 sections; it was ahead in 0, so the planned
experiment batches (M8: 10 runs per arm and leave-one-layer-out) were not run.

Post hoc, descriptive, runs 2-4 and the live console check: the scope layer ran only in F3 and F4
(bare out of scope: F4 6 of 6, F2 3 of 9); tests shipped, median harness 2.5, bare 7.5; arm wall
time, median 302 s against 190 s; agent time limit hit, harness 9 of 34, bare 4 of 34; cost per arm,
median $0.0123 against $0.0103. What to take home: each piece is a bet on what the model cannot do. A1
warns that its own results should "not be assumed to generalize without similar investment"
(F-a-143); the same holds here: one model, one task per section, a few runs per arm.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: course pilot runs 2-4 and class-profile round; A1 F-a-143 in REFERENCES.md.

## 69. Assignments
section: Wrap-up
minutes: 3

- A1 Instructions: `submodules/01-instructions/assignment/`, ≤ $2.50 and 150 traces
- A2 State and session lifecycle: `submodules/02-state-lifecycle/assignment/`, ≤ $1.50 and 60 traces
- A3 Scope and sandbox: `submodules/03-scope-sandbox/assignment/`, ≤ $0.25 and 30 traces
- A4 Verification and portfolio: `submodules/04-verification/assignment/`, ≤ $1.75 and 120 traces
- Each: a brief with grading criteria, a starter folder, `make check-assignment-N` offline, one live step
- Total ≤ $6 and ≤ 400 traces; Thursday review

notes:
Learner budgets are course design.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: submodules/01-instructions/assignment/README.md to submodules/04-verification/assignment/README.md; Makefile `check-assignment-N`.

## 70. Skills and the starter kit to take home
section: Wrap-up
minutes: 2
code: Final:skill_template 1-6

- `harness-setup`, `assured-tests`, `house-rules`, `skill-template`, in the Agent Skills format (B1)
- `uv run shipharness init --target <repo>`: the kit, with TeamTrack's values and REPLACE markers
- `uv run shipharness init --check <repo>` lists the markers still to fill; no model calls
- Guide: `docs/apply-to-your-repo.md`, ending with which layers earn their place in your repository

notes:
The `skill-template` frontmatter from `name` to `license`. The kit copies the AGENTS.md map, the docs/
layout, the state files, the feature list and its schema, house-rule check templates, a sandbox
policy, a CI workflow, and the four skills into `.claude/skills/` and `.agents/skills/`.

Run sheet: docs/instructor-guide.md, Stage 8: Final block and wrap-up (3:40-4:00).
Source: B1 in REFERENCES.md; README.md §14; kit/README.md; anchor Final:skill_template.

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
