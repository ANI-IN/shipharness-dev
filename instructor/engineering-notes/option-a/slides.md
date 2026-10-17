# Option A: slide changes against slides/outline.md

Draft, not applied. Each changed slide has its current gist (one line), the proposed text as
speaker-ready bullets, and the evidence for every number. "Proposed text" is public wording: it
names pilot facts in words and cites sources by finding id. The "Evidence" lines are private and cite
VERIFICATION.md (main, section "M6 pilot") by run and A/B id.

Summary: 21 slides change content, 1 slide is new (68, "What the pilot measured"), 2 slides change
timing only (65, 67), and the five wrap-up slides move from 68-72 to 69-73 unchanged. The deck becomes
73 slides; every block keeps its minutes. Slide 2 loses its screenshot slot.

Changes to the outline's header tables:

| Block | Slides | Minutes |
|---|---|---|
| Final results and what the pilot measured | 64-68 (5) | 13 |
| Wrap-up | 69-73 (5) | 7 |
| **Total** | **73** | **240** |

Title line: "Slide outline: Module 1 (73 slides)". The recurring-diagram table and the
poll/launch/demo table keep their numbers (all at or below 64).

---

## Opening (slides 1-7)

| # | Heading | Change |
|---|---|---|
| 1 | Harness Engineering for Coding Agents | Subtitle |
| 2 | The problem: four real failures | Content; screenshot slot removed |
| 3 | Why it happens: four causes | No change |
| 4 | The solution: a harness | Content: the course claim |
| 5 | shipharness, TeamTrack, console | No change |
| 6 | How we prove it | Heading and content |
| 7 | Check your setup | No change |

### Slide 1. Harness Engineering for Coding Agents

Current gist: subtitle "Instructions, state, scope, and verification that make agent-written code
safe to merge".

Proposed text:

- Subtitle: "Instructions, state, scope, and verification: what each piece assumes about the model,
  and how to measure it"

Evidence: no numbers.

### Slide 2. The problem: four failures to check for

Current gist: four failures, one shown with a recorded bare-arm F1 board screenshot with other-org
marks (result slot).

Proposed text:

- Cross-tenant data: an Acme user sees Globex issues
- A second session that redoes or breaks the first
- Edits outside the ticket
- The agent's own tests pass while the behaviour is wrong
- The referee checks every run for all four, in both arms
- Speaker note: "In the course pilot no bare F1 arm shipped a new tenant-isolation violation (runs 2,
  3, and 4, and the live console check, 2026-10-16), so there is no recorded screenshot to show. We
  come back to what that means at the end."

Evidence: F1 bare passed the primary measure (0 new R1 violations) in run 2 (3/3), run 3 (3/3), run 4
(3/3), and the live console check (`ab-20261016-210339-909651`); A/B ids in README.md, "Evidence for
the numbers". Remove the slide 2 PENDING from "Result slots".

### Slide 4. A harness encodes assumptions about the model

Current gist: "the environment around the agent", A1 F-a-02, four parts and the sandbox, diagram.

Proposed text:

- A harness is the environment around the agent. A1 describes the work as "design environments,
  specify intent, and build feedback loops" (F-a-02; A1 gives no definition)
- A3: "every component in a harness encodes an assumption about what the model can't do on its own,
  and those assumptions are worth stress testing" (F-a-124)
- Four parts, four assumptions (the one-line forms are the course's):
  - S1 Instructions: the model will not apply a rule it has not been pointed to
  - S2 State: a fresh session cannot pick up the work from the repository alone
  - S3 Scope: the agent will change files outside the ticket unless code stops it
  - S4 Verification: the agent's "done" and its own tests cannot be trusted
- Assumptions change with the model: A3 dropped context resets once Opus 4.5 no longer needed them
  (F-a-69)
- The course's claim: measure each piece, keep what earns its place
- Diagram with all parts highlighted (unchanged)

Evidence: no numbers. Sources: A1 F-a-02; A3 F-a-124, F-a-69. "Keep what earns its place" and the
four one-line assumptions are course framing.

### Slide 6. How we measure it

Current gist (heading "How we prove it"): identical inputs for both arms, one referee, house rules,
datasets, one pre-registered primary measure per section.

Proposed text:

- Same agent, model, effort, task, repository, tools, sandbox, turn limit, cost cap; one
  deterministic referee
- House rules R1-R7: the course's label for A1's "golden principles"
- One primary measure per section, registered before any run; every run is a dot; counts, never
  percentages
- Written down before the runs: a section that shows no gap is reported as "no measurable difference
  on this task with this model"
- A section's A/B tests the harness so far against the bare arm. One piece at a time is A3's method:
  "removing one component at a time and reviewing what impact it had on the final result." (F-a-125)
- Datasets: 60 tasks in six groups, 40 test-generation targets

Evidence: datasets counts unchanged from the current slide (DESIGN §5, §8.2). The outcome rule is
DESIGN §10.4 "Outcome rule, pre-registered now".

---

## S1 Instructions (slides 8-21)

| # | Heading | Change |
|---|---|---|
| 8 | Poll | No change |
| 9 | Launching the live A/B: F1 org-wide issue search | No change |
| 10 | S1: what the agent knows | Content: the assumption |
| 11 | Problem: the rule is written down, the agent does not apply it | No change |
| 12 | Cause: what is not in context does not exist | No change |
| 13 | Harness piece: AGENTS.md as a map | No change |
| 14 | Progressive disclosure | No change |
| 15 | Keep the map true | Speaker note added |
| 16-18 | Code slides | No change |
| 19 | Demo block: what the console shows | No change |
| 20 | Demo block: results | Content: what the pilot measured for S1 |
| 21 | Runbook and next | Discussion question |

### Slide 10. S1: what the agent knows

Current gist: diagram with S1 highlighted, three objectives, the problem under test (legacy handler
without the tenant filter).

Proposed text:

- Diagram with S1 highlighted; the three objectives (unchanged)
- The problem under test: a legacy handler without the tenant filter next to the right pattern
- The assumption the map encodes: the model will not apply a rule it has not been pointed to (the
  course's wording, after A3, F-a-124)
- Today's question: does that hold for this model on this ticket?

Evidence: no numbers.

### Slide 15. Keep the map true

Current gist: docs checked mechanically (A1, F-a-37), lint messages that teach (F-a-97), the fairness
rule and its unit test.

Proposed text (bullets unchanged; speaker note added):

- Speaker note: "A1's argument is a map against one giant instruction file (F-a-23, F-a-24). In
  class the bare arm has the rules in a handbook on disk. The course's next pilot round gives the bare
  arm the same rules as one monolithic instruction file, which is A1's comparison."

Evidence: round 5 design (owner, 2026-10-17); no numbers.

### Slide 20. Demo block: results, and what the map assumed

Current gist: the A/B verdicts, tonight's dots next to the experiment dots, swap test verdict.

Proposed text:

- Tonight's two dots (filled in live), next to the pilot's
- Course pilot, primary measure (a run fails with one or more new tenant-isolation violations):
  - run 2, canonical ticket, effort medium: bare 0 of 3 failing, harness 0 of 3
  - run 3, trap ticket, effort medium: bare 0 of 3, harness 0 of 3
  - run 4, trap ticket, effort low: bare 0 of 3, harness 0 of 3
  - live console check, canonical ticket: bare 0 of 1, harness 0 of 1
- Why: the canonical ticket names the handbook, and every bare arm in run 2 opened it with its third
  tool call; on the trap ticket no arm copied the legacy handler
- No measurable difference on this task with this model: here the assumption did not hold, so the
  map had nothing to fix
- Post hoc (chosen after the results; descriptive): harness arms claimed done in 5 of 10 runs, bare
  arms in 9 of 10; median cost per arm $0.0122 against $0.0103; median arm wall time 168 s against
  177 s; no agent time limit hit in either arm
- Round 5 tests A1's comparison, the map against one monolithic instruction file:

[[PENDING: F1 round 5 result, runs failing out of k per arm (r1_new_violations>=1), bare arm with the rules as one monolithic instruction file, with A/B ids | source: M6 pilot | how: course pilot (build repository)]]

- Swap test verdict (filled in live); experiment dots (existing M8 batch 1 slot, unchanged)

Evidence: run 2 F1 3/3 both arms (`ab-20261016-181736-a07558`, `-183644-0036f0`, `-185628-37483b`);
run 3 F1 trap 3/3 both (`ab-20261016-211419-07937b`, `-212745-2c14fb`, `-214636-c8b3c4`); run 4 3/3
both (`ab-20261016-232842-b372c2`, `-233807-3f34fa`, `-234639-4a18bd`); console check
`ab-20261016-210339-909651`. Third tool call: run 2 logs, as already stated in
`submodules/01-instructions/concepts.md` §1. Post hoc: exploratory analysis, rows "F1 bare" and "F1
harness" (n = 10 each: run 2, console check, run 3, run 4).

### Slide 21. Runbook and next

Current gist: link to the demo runbook, a discussion question, transition to session ends.

Proposed text:

- Link `submodules/01-instructions/demo/README.md`
- Discussion: "The map changed nothing on this ticket. What would have to be true of a model or a
  ticket for it to earn its place?"
- Transition: what happens when a session ends halfway

Evidence: no numbers.

---

## S2 State and session lifecycle (slides 22-34)

| # | Heading | Change |
|---|---|---|
| 22 | Poll | No change |
| 23 | Launching the live A/B: F2 comments | No change |
| 24 | S2: what the agent remembers | Content: the assumption |
| 25 | Cause: every session starts empty | No change |
| 26 | Harness piece: state on disk | No change |
| 27 | Getting up to speed, and ending a session | No change |
| 28 | Exec plans and the structured handoff | Content: A3's reset example |
| 29-31 | Code slides | No change |
| 32 | Demo block: what the console shows | No change |
| 33 | Demo block: results | Content: what the pilot measured for S2 |
| 34 | Runbook and next | Discussion question |

### Slide 24. S2: what the agent remembers

Current gist: diagram with S2 highlighted, objectives, the problem under test (a second session that
does not know what the first did).

Proposed text:

- Diagram with S2 highlighted; objectives (unchanged)
- The problem under test: a second session that does not know what the first did
- The assumption the state files encode: a fresh session cannot pick up the work from the repository
  alone (A2 states the problem, F-a-08; the one-line form is the course's)

Evidence: no numbers.

### Slide 28. Exec plans and the structured handoff

Current gist: exec plans active to completed (A1, A7), A3's context reset with a structured handoff,
the session turn budget (course mechanism), resets are model-dependent.

Proposed text:

- Exec plans, active to completed (A1, A7; F-a-34, F-a-35, F-a-45 to F-a-48)
- A3's context reset: a fresh agent "combined with a structured handoff" (F-a-65)
- The course mechanism: the session turn budget
- A reset has a price: "orchestration complexity, token overhead, and latency" (A3, F-a-68)
- And it was dropped when the model changed: "Opus 4.5 largely removed that behavior on its own, so I
  was able to drop context resets from this harness entirely." (A3, F-a-69)
- That is today's claim from a source: a piece that answers a model's weakness is kept only while the
  weakness is there

Evidence: no numbers.

### Slide 33. Demo block: results, and what the state files assumed

Current gist: the A/B verdicts, tonight's dots next to the experiment dots, swap test, ablation bars.

Proposed text:

- Tonight's dots (filled in live), next to the pilot's
- Course pilot, primary measure, first session 12 turns, then 38: continuity failures 0 of 3 per arm
  in run 3 (effort medium) and in run 4 (effort low): no measurable difference on this task with this
  model
- The measure cannot fail when session 1 leaves nothing to redo: 6 of the 12 arms built nothing
  (3 of 56 hidden tests): two harness arms in run 3, all three bare arms and one harness arm in run 4
- The bare arm found its own state: in run 2 its second session began with `git status` and read the
  migration it had left
- A harness piece caused a failure: in 2 of 3 run 3 A/Bs the harness arm's wrap-up led it to call
  `finish(claim="not_done")` after 12 turns, which ended the build phase; the 38-turn session never
  ran
- Post hoc (descriptive), 9 runs per arm over runs 2-4: harness arms hit the agent time limit in 4,
  bare arms in 0; median arm wall time 361 s against 232 s
- Round 5: the early-finish fix, and a measure for that round only, "no continuity failure and at
  least 50% of hidden tests passed":

[[PENDING: F2 round 5 result, runs passing "continuity AND at least 50% of hidden tests" out of k per arm, after the early-finish fix, with A/B ids | source: M6 pilot | how: course pilot (build repository)]]

- Swap test verdict (filled in live); ablation bars (existing M8 slot, unchanged)

Evidence: run 3 F2 3/3 both (`ab-20261016-211419-dfe06f`, `-213317-9a0ec1`, `-214959-de790f`); run 4
3/3 both (`ab-20261016-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9`); built nothing: "Run 4", F2
across runs 3 and 4 paragraph (run 3 harness `-213317-9a0ec1`, `-214959-de790f`; run 4 bare all three,
harness `-234027-226a76`); early finish: "Run 3", F2 harness row; `git status`: run 2
`ab-20261016-181736-08a9c4`, run `r-20261016-181736-a05ddb` (already captured in
`submodules/02-state-lifecycle/concepts.md` §1); post hoc: exploratory rows "F2 bare", "F2 harness".

### Slide 34. Runbook and next

Current gist: link, discussion question, transition to the break.

Proposed text:

- Link `submodules/02-state-lifecycle/demo/README.md`
- Discussion: "The bare arm found its own state with `git status`. Which state file would you keep
  for this model, and how would you measure it?"
- Transition to the break

Evidence: no numbers.

---

## Break (slide 35)

No change.

---

## S3 Scope and sandbox (slides 36-48)

| # | Heading | Change |
|---|---|---|
| 36 | Poll | No change |
| 37 | Launching the live A/B: F3 idempotency keys | No change |
| 38 | S3: what the agent may change and reach | Content: the assumption |
| 39 | Cause: copied patterns and hard-to-undo actions | No change |
| 40 | Harness piece: one feature list, one feature | No change |
| 41 | Allowed paths per phase | No change |
| 42 | Sandbox 1: why a container | No change |
| 43 | Sandbox 2: the same limits for both arms | One bullet added |
| 44-45 | Code slides | No change |
| 46 | Demo block: what the console shows | No change |
| 47 | Demo block: results and the sandbox moment | Content: what the pilot measured for S3 |
| 48 | Runbook and next | Discussion question |

### Slide 38. S3: what the agent may change and reach

Current gist: diagram with S3 highlighted, objectives, the problem under test (edits outside the
ticket, source edits in the test phase).

Proposed text:

- Diagram with S3 highlighted; objectives (unchanged)
- The problem under test: edits outside the ticket, source edits during the test phase
- The assumption the scope layer encodes: the agent will change files outside the ticket unless code
  stops it (the course's wording; no single source sentence states the cause, so slide 39 shows its
  sources side by side)

Evidence: no numbers.

### Slide 43. Sandbox 2: the same limits for both arms

Current gist: Docker limits for both arms, `sandbox_denied` reason codes, never an A/B variable,
Module 2.

Proposed text (bullets unchanged; one added):

- Never an A/B variable, so the pilot cannot tell you whether it earns its place. The course keeps it
  on the sources' advice: a container per agent and no internet access (A4, F-a-18, F-a-88, F-a-90),
  file operations limited to the project directory (A5, F-a-86)

Evidence: no numbers.

### Slide 47. Demo block: results and the sandbox moment

Current gist: tonight's `sandbox_denied` events or the policy printout, the A/B verdicts, tonight's
dots next to the experiment dots, swap test.

Proposed text:

- Tonight's sandbox denials (filled in live), or the policy printout
- Course pilot, primary measure on the trap ticket: 0 of 3 failing per arm in run 3 and in run 4; no
  shipped diff touched `app/api/middleware.py`: no measurable difference on this task with this model
- Post hoc, F3 (descriptive, 9 runs per arm): harness arms shipped a median of 0 tests against 6,
  killed a median of 0 of 4 referee mutants against 4, and claimed done in 4 runs against 9
- Post hoc, F4, where all four layers ran: bare arms changed files outside the allowed paths in 6 of
  6 runs, harness arms in 0 of 6. The scope layer's clearest effect was on a measure nobody registered
  for it; that is a reason to register it next time, not a result
- Tonight's dots (filled in live); swap test verdict (filled in live); experiment dots (existing M8
  slot, unchanged)

Evidence: run 3 F3 trap 3/3 both (`ab-20261016-212115-a361f5`, `-213624-d7eb13`, `-215443-f2c188`),
run 4 3/3 both (`ab-20261016-233517-2c9ea4`, `-234509-8b9bfa`, `-235305-723a0f`); "Run 3" F3 row
("`app/api/middleware.py` untouched"); post hoc: exploratory rows "F3 bare", "F3 harness", "F4 bare",
"F4 harness" (F4: run 2 and run 3 A/Bs). Do not attribute the F2 harness arms' 0 of 9 to the scope
layer: demo-2 has no scope layer (README.md, "Found while drafting", item 1).

### Slide 48. Runbook and next

Current gist: link, discussion question, transition to who decides the work is done.

Proposed text:

- Link `submodules/03-scope-sandbox/demo/README.md`
- Discussion: "The scope layer's clearest effect showed where it was not the primary measure. How
  would you register that before the next run?"
- Transition: who decides that the work is done

Evidence: no numbers.

---

## S4 Verification (slides 49-63)

| # | Heading | Change |
|---|---|---|
| 49 | Poll | No change |
| 50 | Poll: the final feature | No change |
| 51 | Launching two live A/Bs: F4 and the final | No change |
| 52 | S4: what proves the work is done | Content: the assumption |
| 53 | Cause: self-grading and visible tests | No change |
| 54 | Harness piece: test filters | No change |
| 55 | Mutants and hidden tests | No change |
| 56 | A separate evaluator and a gate | One bullet added |
| 57 | Read the trace | Heading and content: measure each piece |
| 58-60 | Code slides | No change |
| 61 | Demo block: what the console shows | No change |
| 62 | Demo block: results | Content: what the pilot measured for S4 |
| 63 | Runbook and next | Discussion question |

### Slide 52. S4: what proves the work is done

Current gist: diagram with S4 highlighted, objectives, the problem under test (the agent's tests pass
while behaviour is wrong).

Proposed text:

- Diagram with S4 highlighted; objectives (unchanged)
- The problem under test: the agent's tests pass while behaviour is wrong
- The assumption the gate and filters encode: the agent's "done" and its own tests cannot be trusted
  (A3, F-a-15; A4, F-a-17; the one-line form is the course's)

Evidence: no numbers.

### Slide 56. A separate evaluator and a gate

Current gist: blinded reviewer with grading criteria (A3), clean-state gate (A2, A4), house rules.

Proposed text (bullets unchanged; one added):

- A3 on its own evaluator: it "is not a fixed yes-or-no decision. It is worth the cost when the task
  sits beyond what the current model does reliably solo." (F-a-123)

Evidence: no numbers.

### Slide 57. Measure each piece

Current gist (heading "Read the trace"): first wrong turn (A3, F-a-126); leave one layer out (A3,
F-a-125).

Proposed text:

- Read the trace: find the first wrong turn (A3, F-a-126)
- Measure one piece: "removing one component at a time and reviewing what impact it had on the final
  result." (A3, F-a-125)
- In shipharness: `make demo-N LAYERS=-<layer>` for one A/B, and the ablation batch for all four
- A section's A/B tests the stack so far; only taking one piece out tests that piece

Evidence: no numbers. Minutes unchanged (1.5).

### Slide 62. Demo block: results, and what the gate assumed

Current gist: the A/B and reviewer verdicts, tonight's two counts per arm next to the experiment dots,
reviewer agreement, swap test.

Proposed text:

- Tonight's two counts per arm (filled in live), next to the pilot's
- Course pilot, run 3 (effort medium): both arms failed the co-primary measure in 3 of 3 A/Bs
  - bare: hidden tests 66, 66, 69 of 69; referee mutants killed 4, 0, 3 of 4; every bare arm hit the
    agent time limit
  - harness: no tests shipped, so 0 of 4 mutants killed in each; one A/B built a broken change
    (hidden 27 of 69, 3 new tenant-isolation violations)
- No measurable difference on this task with this model (F4 had no run 4)
- On F4 the harness arm never called `finish` in runs 2 and 3, so its verify gate never ran
- Post hoc (descriptive), over all sections (34 runs per arm): no done claim came with failing hidden
  tests in either arm (0 of 19 bare, 0 of 10 harness), and harness arms shipped a median of 2.5 tests
  against 7.5
- What A3 said about its evaluator (slide 56) applies here: in these runs the arms did not fail by
  claiming too much; on F4 they ran out of time (every bare arm in run 3 hit the agent time limit, and
  the limit cut the harness test phase in two runs)
- Round 5: a longer agent time limit for both arms, and a look at why the test phase ships no tests:

[[PENDING: F4 round 5 result with a longer agent time limit for both arms (hidden x of 69 and referee mutants y of 4 per run per arm), and the test-phase findings, with A/B ids | source: M6 pilot | how: course pilot (build repository)]]

- Reviewer agreement (existing M8 slot, unchanged); swap test verdict (filled in live)

Evidence: "Run 3", F4 rows (`ab-20261016-212252-aa1644`, `-214151-ca9841`, `-220010-c5b4bf`; broken
change in `-212252-aa1644`); gate never ran: run logs (`events.jsonl` of the six F4 A/Bs of runs 2
and 3, read 2026-10-17) have no `finish` call by the harness arm, and its only verify decisions are
the gate baseline and the test-filter summary; false done and shipped tests: exploratory rows "All
bare", "All harness". "Ran out of time": "Run 3", F4 rows (every bare arm hit the agent time limit;
"the test phase was cut by the time limit in two runs" of the harness arm).

### Slide 63. Runbook and next

Current gist: link, discussion question, transition to the final results.

Proposed text:

- Link `submodules/04-verification/demo/README.md`
- Discussion: "No done claim in the pilot came with failing hidden tests. What would a gate need to
  catch to earn its turns on this model?"
- Transition to the final results

Evidence: post hoc row "All", false done 0 of 19 and 0 of 10.

---

## Final results and what the pilot measured (slides 64-68, 13 minutes)

| # | Heading | Change | Minutes |
|---|---|---|---|
| 64 | Final results: the A/B lines | No change | 2 |
| 65 | Final results: console | Timing only | 4 to 3 |
| 66 | Final results: boards | No change | 2 |
| 67 | Final results: screen 4, report, and LangSmith comparison | Timing only | 5 to 4 |
| 68 | What the pilot measured | New | 2 |

### Slide 68 (new). What the pilot measured

Proposed text:

- The course ran its own A/Bs before class: gpt-6-luna, both arms identical except the harness, one
  primary measure per section registered in advance, three A/Bs per section per run
- Primary results, runs 3 (effort medium, 2026-10-16) and 4 (effort low, 2026-10-16 to 2026-10-17):
  no measurable difference on this task with this model in all four sections (F4: run 3 only, both
  arms failing 3 of 3)
- Post hoc: measures chosen after the results, descriptive, 34 arm runs per arm over runs 2-4 and
  the live console check:
  - files changed outside the allowed paths: harness arms in 0 of 34 runs, bare arms in 9 of 34 (F4
    6 of 6, F2 3 of 9); the scope layer ran only in F3 and F4
  - claimed done: harness 10 of 34, bare 19 of 34; no claim was false in either arm
  - tests shipped, median: harness 2.5, bare 7.5
  - arm wall time, median: harness 302 s, bare 190 s; agent time limit hit: harness 9 of 34, bare 4 of
    34
  - cost per arm, median: harness $0.0123, bare $0.0103
- What to take home: each piece is a bet on what the model cannot do. On this model the bets on
  knowledge, memory, and self-judgement did not show on their measures; the scope bet showed where it
  was not measured
- A1 warns that its own results should "not be assumed to generalize without similar investment"
  (F-a-143); the same holds for this pilot: one model, one task per section, three runs per arm
- Round 5 (F1, F2, F4):

[[PENDING: round 5 summary, one line per section (F1 monolithic instruction file, F2 early-finish fix with continuity AND at least 50% of hidden tests, F4 longer agent time limit), runs passing out of k per arm, with A/B ids | source: M6 pilot | how: course pilot (build repository)]]

Evidence: "Gate decision" table (runs 3 and 4 per section); exploratory analysis rows "All bare" and
"All harness" (34 each), and rows "F2 bare", "F4 bare" for the out-of-scope split; scope layer only in
demo-3 and demo-4 (`SECTION_STACKS`, `src/shipharness/ab/demo.py`). A/B ids: README.md, "Evidence
for the numbers".

---

## Wrap-up (slides 69-73, 7 minutes)

| New # | Old # | Heading | Change |
|---|---|---|---|
| 69 | 68 | Assignments (1 of 2) | Number only |
| 70 | 69 | Assignments (2 of 2) | Number only |
| 71 | 70 | Skills and templates to take home | Number only |
| 72 | 71 | References (1 of 2) | Number only |
| 73 | 72 | References (2 of 2) | Number only |

---

## Result slots and "Filled in live"

- Remove the slide 2 PENDING (the board screenshot of a bare F1 run with other-org marks): no bare F1
  arm in the pilot had one.
- Add the four round 5 PENDING markers above under slides 20, 33, 62, and 68.
- "Filled in live" keeps slides 64-67; slide 68 has nothing filled in live.
- The speaker-note timing paragraph is unchanged.
