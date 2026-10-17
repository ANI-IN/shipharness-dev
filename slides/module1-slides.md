# Module 1: Harness Engineering for Coding Agents: slide content

This file holds the full slide content of Module 1 for review: 78 slides in 240 minutes (opening 10 slides, 10 minutes; Sections 1 to 4, 13 slides and 50 minutes each; a break, 1 slide and 10 minutes; close 15 slides, 20 minutes). The minute marks follow the run sheet in `docs/instructor-guide.md`. Content comes from `slides/deck.md`, `docs/instructor-guide.md`, the section folders (`section-1-instructions`, `section-2-state-lifecycle`, `section-3-scope-sandbox`, `section-4-verification`: README, concepts.md, demo/README.md, demo/walkthrough.md), `final-project/README.md` and `use-in-your-repo/README.md`. Every number comes from `docs/evidence.md` and `docs/evidence/general.md`, `s1.md`, `s2.md`, `s3.md`, `s4.md` and `final.md`. Code excerpts are quoted exactly from the demo `walkthrough.md` files. Screenshots come from `slides/img/`, `docs/images/` and `section-N-*/demo/expected/`. Timings come from timed runs on 2026-10-17, before class, with a 300 s agent limit; the Section 3 timings used 420 s. In every chart the bare arm is grey and the harness arm is blue; a filled dot means passed and a hollow dot means failed.

---

## Slide 1: Module 1: Harness Engineering for Coding Agents
**Section:** opening  **Time:** 0:00–0:01 (1 min)
**On the slide:**
- Instructions, state, scope, verification: what each piece assumes
- How to measure whether each piece earns its place
- Course repository: `shipharness`
**Visual:** Title layout. Course title large, the subtitle bullets under it, and a thin strip at the bottom with four labelled boxes in a row (Instructions, State, Scope, Verification) on one shared sandbox bar. The boxes are blue; the sandbox bar is neutral.
**Speaker notes:**
- Welcome. Tonight you see each harness piece at work on a real feature.
- A harness is the files and code around a coding agent that decide what it sees and may do.
- You also see the results of the runs we made before class, good and bad.
- Section 3 and the final are live A/Bs: both arms side by side. Everything is in the course repository.
- Question to ask the room: Who already runs a coding agent on tickets in a real repository?
- Transition: Let's start with what goes wrong when an agent works without a harness.

## Slide 2: The problem: four failures to check
**Section:** opening  **Time:** 0:01–0:02 (1 min)
**On the slide:**
- Cross-tenant data: an Acme user sees Globex issues
- A second session redoes or breaks the first
- Edits to files outside the ticket
- The agent says done; hidden tests say otherwise
- The referee checks every run for all four
**Visual:** Four cards in a 2×2 grid, each with an icon and one line: lock (tenant leak), two stacked sessions (continuity), a file outside a dashed box (scope), a green tick crossed out (false done). Under the grid one bar: "Referee: same checks, both arms".
**Speaker notes:**
- The referee is the program that scores each run after the agent stops. It runs these four checks in every run, for both arms.
- Two of these happened before class: every bare arm on the F4 ticket edited a file outside the ticket, and one bare arm claimed done with 68 of 69 hidden tests passing.
- Hidden tests are tests the agent never sees; the referee runs them after the agent stops.
- No run before class leaked another org's cards, so there is no leak screenshot to show. Say so plainly; we come back to it in Section 1.
- Question to ask the room: Which of these four would hurt your team most if it shipped?
- Transition: Why do capable agents make these mistakes?

## Slide 3: Why it happens: four causes
**Section:** opening  **Time:** 0:02–0:03 (1 min)
**On the slide:**
- Not in context: "effectively doesn’t exist" (OpenAI)
- New session: "no memory of what came before" (Anthropic)
- Agents copy patterns and take hard-to-undo actions (four sources)
- Self-grading: "agents reliably skew positive" (Anthropic)
**Visual:** Four rows, one per cause, each tagged with the section that answers it (S1, S2, S3, S4). Source names in small type at the right end of each row.
**Speaker notes:**
- Cause 1, OpenAI, Harness engineering: "anything it can’t access in-context while running effectively doesn’t exist."
- Cause 2, Anthropic, Effective harnesses: "each new session begins with no memory of what came before."
- Cause 3 has no single source that says both halves, so Section 3 shows its four sources side by side and does not merge them.
- Cause 4, Anthropic, Harness design: "agents reliably skew positive when grading their own work".
- Question to ask the room: Which cause have you seen yourself this month?
- Transition: Each harness piece is an answer to one of these causes, and each answer is a bet.

## Slide 4: A harness encodes assumptions
**Section:** opening  **Time:** 0:03–0:04 (1 min)
**On the slide:**
- The work: "design environments, specify intent, and build feedback loops"
- "every component in a harness encodes an assumption" (Anthropic)
- Assumptions change with the model
- Our claim: measure each piece, keep what earns its place
**Visual:** One sentence as a large quote card ("every component in a harness encodes an assumption about what the model can't do on its own"), with a small arrow to a second card: "…and those assumptions are worth stress testing". Source line under both: Anthropic, Harness design.
**Speaker notes:**
- The first line is OpenAI's description of the work, and the basis for our word "harness". OpenAI never defines "harness engineering", so we attribute no definition to it.
- The Anthropic sentence goes on: "and those assumptions are worth stress testing".
- The same author later dropped context resets once a newer model no longer needed them. A piece is kept only while the weakness is there.
- "Keep what earns its place" is the course's wording, not a source quote.
- Question to ask the room: What does your current agent setup assume the model cannot do?
- Transition: Here are the four pieces we will test tonight.

## Slide 5: The harness: four parts, one sandbox
**Section:** opening  **Time:** 0:04–0:05 (1 min)
**On the slide:**
- S1 Instructions: what the agent knows
- S2 State and session lifecycle: what it remembers
- S3 Scope: what it may change
- S4 Verification: what proves the work is done
- Sandbox: identical for both arms, never the variable
**Visual:** Architecture diagram, left to right. Box "Same ticket, model, tools, budgets" splits into two arms: "Bare arm: agent loop" (grey) and "Harness arm: agent loop" (blue). Four blue boxes hang off the harness arm: S1 Instructions, S2 State and session lifecycle, S3 Scope, S4 Verification. Each arm points to its own "Sandbox" box (neutral, labelled "identical"). Both sandboxes point to "Referee: same checks, fresh container", which points to "Console and report". This diagram returns as the agenda marker in each section.
**Speaker notes:**
- A harness layer is one part of the harness: instructions, state, scope, or verification.
- The sandbox is the container each arm runs in. It is the same for both arms, so it is taught but never measured.
- The referee judges both arms in a fresh container, the same way.
- Each section adds one layer on top of the ones before it.
- Question to ask the room: Which of the four would you build first in your own repository?
- Transition: Now the tool and the app we test on.

## Slide 6: shipharness and TeamTrack
**Section:** opening  **Time:** 0:05–0:06 (1 min)
**On the slide:**
- `shipharness`: run an agent with or without the harness
- It runs A/Bs and judges every run
- TeamTrack: a multi-tenant issue tracker
- Two orgs, Acme and Globex
**Visual:** Two panels. Left: a terminal block with `make show-1`, `make demo-3 FEATURE=F4`, `make final FEATURES=F6,F5`. Right: a TeamTrack board screenshot, `section-1-instructions/demo/expected/screen-2-final.png`, with one callout on the "Acme" badge ("signed in as an Acme user") and one on the column headers ("Open, In Progress, Done").
**Speaker notes:**
- An A/B is a bare arm and a harness arm on the same ticket, scored the same way.
- The bare arm gets the ticket and the repository and no harness. The harness arm is the same run with the harness on.
- TeamTrack has two orgs. A user of one org must never see the other org's issues.
- Every command tonight is a `make` target in the repository.
- Question to ask the room: How many of you work on a multi-tenant product?
- Transition: You watch every run on one browser page, the console.

## Slide 7: The console: five screens
**Section:** opening  **Time:** 0:06–0:07 (1 min)
**On the slide:**
- `1` Live, `2` Boards, `3` Evidence
- `4` A/B Report, `5` Traces
- `F`: one arm full screen
**Visual:** Screenshot `docs/images/screen-1-ab-minute-3.png` (console screen 1 at minute 3 of a final run). Callouts: (1) the bare arm column, grey label "bare"; (2) the harness arm column, blue label "harness"; (3) the turn list that grows while the agent works.
**Speaker notes:**
- The console is the browser page that shows a run live, on five screens.
- Press `1` to `5` once each now and name each screen.
- Screen 1 shows turns and harness decisions. Screen 3 shows the referee's evidence. Screen 4 shows one dot per run.
- Screen 5 links each turn to its trace.
- Question to ask the room: Which screen do you expect to trust most, and why?
- Transition: Before any run, how do we make a comparison fair?

## Slide 8: How we measure
**Section:** opening  **Time:** 0:07–0:08 (1 min)
**On the slide:**
- Same agent, model, ticket, tools, sandbox and budgets
- One referee judges both arms the same way
- House rules R1 to R7, checked by code
- One primary measure per section, registered before runs
- No gap means "no measurable difference"
**Visual:** A/B diagram: one ticket card splits into a grey bare arm and a blue harness arm; both feed one referee box; the referee outputs a row of dots, filled for passed and hollow for failed. A caption: "Results are counts of runs, never percentages."
**Speaker notes:**
- House rules are TeamTrack's seven rules for every endpoint, R1 to R7; the course's name for OpenAI's "golden principles". The bare arm can read every rule.
- The primary measure is the one question a section asks, fixed before any run. The primary verdict is the referee's answer to it.
- A section's A/B tests the harness so far against the bare arm. Only taking one piece out tests that piece: "removing one component at a time" (Anthropic, Harness design).
- Before class we ran three A/Bs per section per round and registered a gate. The harness arm was ahead in 0 of 4 sections.
- Question to ask the room: If one run looks better with the harness, what have we learned?
- Transition: Let's check the machine before the first run.

## Slide 9: Check your setup
**Section:** opening  **Time:** 0:08–0:09 (1 min)
**On the slide:**
- Run `make doctor` now
- Last line must read `result: + ready`
- Run the `harness-setup` assessment on bare TeamTrack
- Read its gaps: instructions, state, scope, verification
**Visual:** Terminal B, large font. Live output of `make doctor`; callout on the last line `result: + ready` and on the two key lines that say "accepted by OpenAI" and "accepted by LangSmith". Below it, the first five summary lines of the assessment printout (Instructions, State, Scope, Verification, Session lifecycle).
**Speaker notes:**
- `make doctor` checks keys, Docker and the class date. It never prints any part of a key.
- The assessment reads files only and makes no model calls.
- Say: "This is what the bare arm works with: no map, no progress file, no feature list. The rules themselves are in both arms."
- `make warm` ran before class. A second warm with nothing changed took 1.2 s.
- Question to ask the room: Which gap in the assessment would you close first?
- Transition: Here is the plan for the next four hours.

## Slide 10: Agenda
**Section:** opening  **Time:** 0:09–0:10 (1 min)
**On the slide:**
- 0:10 S1 Instructions, 1:00 S2 State and lifecycle
- 1:50 Break, 2:00 S3 Scope and sandbox
- 2:50 S4 Verification, final A/B launched
- 3:40 Final results, your repo, assignments
**Visual:** A horizontal timeline from 0:00 to 4:00 with five coloured segments (Opening, S1, S2, Break, S3, S4, Close). Each section segment shows its live command under it: `make show-1`, `make show-2 SESSION_BUDGET=12,38`, `make demo-3 FEATURE=F4`, `make show-4`, `make final FEATURES=F6,F5`.
**Speaker notes:**
- Every section runs the same way: poll, launch, concepts while the run goes on, then the demo block.
- Sections 1, 2 and 4 show the harness arm alone, live. Section 3 and the final are live A/Bs.
- A live A/B runs only where the data before class showed a real gap.
- The final A/B starts in Section 4 and we read it at 3:40.
- Question to ask the room: Which section do you expect the harness to win?
- Transition: Section 1, what the agent knows.

---

## Slide 11: S1: What the agent knows
**Section:** S1  **Time:** 0:10–0:11 (1 min)
**On the slide:**
- Section 1 of 4: Instructions
- The map, focused docs, skills
- Live: `make show-1`
**Visual:** The five-part diagram from slide 5 (Instructions, State, Scope, Verification, Sandbox). The Instructions box is highlighted in blue with a thick border and the label "now"; the other four boxes are pale.
**Speaker notes:**
- This section covers why an agent does not apply a rule that lives only outside its context.
- We look at knowledge as a short AGENTS.md map into `docs/`, plus skills that load in tiers.
- We read the result as new R1 violations per run, bare arm against harness arm.
- Question to ask the room: Where do your team's coding rules live today?
- Transition: First a poll, then we launch the run.

## Slide 12: Poll, then launch `make show-1`
**Section:** S1  **Time:** 0:11–0:15 (4 min)
**On the slide:**
- 7 bare runs took this ticket before class
- How many shipped a new tenant leak?
- A) 0–1  B) 2–3  C) 4–5  D) 6–7
- Then terminal B: `make show-1`
**Visual:** Poll card on the left. Right: the flow `make show-1` → "Context: AGENTS.md map and skill names" → "Agent turns: read, patch, test" → "Agent says done" → "Referee: R1 probes" → "primary verdict ready" → "Hidden tests, mutants, reviewer". All boxes blue (harness arm only).
**Speaker notes:**
- The ticket is F1, an org-wide issue search, next to a legacy handler with no tenant filter. R1 says another org's resource answers 404, never 403.
- Close the poll at minute 3, then launch at 0:13. Reload the console's run list and open the newest run.
- `make show-1` is harness in action: the harness arm alone, live, not an A/B. We show the layer at work because F1 showed no gap before class.
- In a timed run on 2026-10-17 the primary verdict came 4 min 11 s after launch and the full verdict at 10 min 0 s; cost $0.019744. Today's limit is 420 s, so it can take a little longer.
- Question to ask the room: What would make you change your vote?
- Transition: While it runs, the question this section asks.

## Slide 13: Does a map change what ships?
**Section:** S1  **Time:** 0:15–0:17 (2 min)
**On the slide:**
- Both arms can read every rule
- The harness arm also gets a map
- Does the map stop a new tenant leak?
- Primary measure: new R1 violations per run
**Visual:** One question in large type: "Does a map stop a new tenant leak?" Under it two small panels: grey "Bare: handbook on disk", blue "Harness: handbook on disk + AGENTS.md map + skills".
**Speaker notes:**
- The assumption the map encodes: the model will not apply a rule it has not been pointed to.
- Nothing is withheld from the bare arm. The rule is in `docs/HANDBOOK.md` in both arms.
- A run fails the primary measure when it adds at least one new R1 violation.
- Question to ask the room: Should a rule the agent can read need a pointer at all?
- Transition: Here is the failure this ticket sets up.

## Slide 14: The problem: a copied query leaks
**Section:** S1  **Time:** 0:17–0:21 (4 min)
**On the slide:**
- Did: copies the legacy list handler's query
- Went wrong: no org filter; Acme sees Globex issues
- Cost: a cross-tenant exposure and an incident
- Before class: no run did this
**Visual:** Three beats left to right, joined by arrows: (1) a code card "legacy handler: no org filter" with a copy icon; (2) a board card showing an Acme user with a red Globex card; (3) an incident card "exposure, disclosure, hunt for every copy". A grey footnote strip: "Illustrative: the risk the ticket sets up."
**Speaker notes:**
- This is the illustrative scenario from the section's README: the tests create one org, so they pass, and review approves a diff that looks like the code around it.
- The cost is a data exposure, a disclosure, and a hunt for every other copy of the pattern.
- Be honest: no arm in any run before class copied the legacy handler into a leak.
- Question to ask the room: Would your tests catch a query with no tenant filter?
- Transition: Why would an agent miss a rule that is written down?

## Slide 15: Cause: not in context, not real
**Section:** S1  **Time:** 0:21–0:25 (4 min)
**On the slide:**
- "anything it can’t access in-context … doesn’t exist"
- "Too much guidance becomes non-guidance."
- A long manual goes stale; no check keeps it true
- Agents copy patterns that already exist
**Visual:** A long scroll labelled "HANDBOOK.md" with the tenant rule buried deep, greyed out; next to it a short card labelled "AGENTS.md map" with arrows into small doc boxes. Source line: OpenAI, Harness engineering.
**Speaker notes:**
- Full quote: "From the agent’s point of view, anything it can’t access in-context while running effectively doesn’t exist."
- OpenAI also writes: "A giant instruction file crowds out the task, the code, and the relevant docs".
- On copying: "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones."
- A handbook the agent never opens does not exist for it.
- Question to ask the room: How long is your longest instruction file?
- Transition: The harness answer: a map, not a manual.

## Slide 16: Answer: AGENTS.md as a map
**Section:** S1  **Time:** 0:25–0:30 (5 min)
**On the slide:**
- AGENTS.md: "roughly 100 lines", "a map"
- `docs/` is the system of record
- Progressive disclosure: small entry point, then where next
- Skills load in tiers: name first, body when needed
**Visual:** Tree diagram of the harness files: `AGENTS.md` and `ARCHITECTURE.md` at the root; `docs/SECURITY.md`, `docs/RELIABILITY.md`, `docs/QUALITY_SCORE.md`, `docs/PLANS.md`, `docs/design-docs/`, `docs/product-specs/`, `docs/references/`; `.agents/skills/add-endpoint/SKILL.md`. AGENTS.md is marked "always in context"; every other file is marked "opened when needed".
**Speaker notes:**
- OpenAI: "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere."
- Progressive disclosure means "agents start with a small, stable entry point and are taught where to look next".
- An Agent Skill is a folder with a `SKILL.md` recipe. Only its name and description sit in context; the Agent Skills spec recommends under 5000 tokens for the instructions.
- The harness reorganises knowledge; it never adds facts the bare arm cannot read. A unit test checks that.
- Question to ask the room: What would go in your repository's map?
- Transition: Here is how the map reaches the agent.

## Slide 17: Code: the context prefix
**Section:** S1  **Time:** 0:30–0:36 (6 min)
**On the slide:**
- One stable block: the map, then the skills catalogue
- Linked documents are not injected; the agent opens them
**Visual:** Code excerpt from `section-1-instructions/demo/walkthrough.md` (router.py, `build_prefix`), with the key line highlighted in blue:
```python
# platform/src/shipharness/harness/instructions/router.py (lines 37-47)
    source = Path(source)
    agents_md = strip_markers((source / MAP_FILE).read_text(encoding="utf-8")).strip()
    blocks = [
        "Repository map (AGENTS.md at the workspace root). It points to the documents to read "
        "before you change code; open them with read_file when your task needs them.",
        agents_md,
    ]
    catalogue = SkillsLoader(source / SKILLS_DIR, workspace_prefix=SKILLS_DIR).catalogue_block()
    if catalogue:
        blocks.append(catalogue)
    return "\n\n".join(blocks)
```
Key line: `catalogue = SkillsLoader(source / SKILLS_DIR, workspace_prefix=SKILLS_DIR).catalogue_block()` (tier 1 only: one line per skill).
**Speaker notes:**
- The context prefix is the fixed text block sent at the start of every agent session.
- It has three parts: one sentence on how to use the map, the whole map, and the skills catalogue.
- `catalogue_block` reads only each skill's frontmatter; the skill body stays on disk until the agent opens it.
- `source` is the course's copy, never the workspace, so an agent that edits its own AGENTS.md cannot change the prefix.
- Section minute 25 falls here: check terminal B for the `Cost:` line of `make show-1`.
- Question to ask the room: Why build the prefix from a copy the agent cannot edit?
- Transition: Here is the whole section on one card.

## Slide 18: S1 cheat sheet
**Section:** S1  **Time:** 0:36–0:40 (4 min)
**On the slide:**
- Command: `make show-1` (harness arm alone, F1)
- Measure: new R1 violations; zero passes
- Watch: which docs it opens before code
- Pass line: "No new tenant leak."
- Runbook: `section-1-instructions/demo/README.md`
**Visual:** A printable card with four labelled rows: Command, Primary measure, What to watch (screens 1, 3, 2, 5 in that order), What to say (pass line and fail line). The fail line in small type: "A leak shipped with the map in place. That is a result."
**Speaker notes:**
- Learners can keep this card for the practice run at home.
- The fail line is there because a run with an unwelcome result is still a result: show it.
- Practising alone, add `PURPOSE=pilot` to the command.
- Question to ask the room: Which line on this card would you check first after a run?
- Transition: The run should be done. Let's look at it.

## Slide 19: Demo: what to watch
**Section:** S1  **Time:** 0:40–0:46 (6 min)
**On the slide:**
- Screen 1: turns, harness decisions, "primary verdict ready"
- Screen 3: files read and the diff map
- Screen 2: the board, own-org cards only
- Screen 5: trace links
**Visual:** Command strip `make show-1` above screenshot `slides/img/s1-watch.png` (screens 1 and 2 of the timed run). Callouts: (1) turn 1.3 `read_file docs/HANDBOOK.md`: "the handbook, third call"; (2) the "Harness decisions" notes: "agent read ARCHITECTURE.md" and "agent read skill add-endpoint (tier 2)"; (3) the green pill "only own-org cards, no duplicates" on the board.
**Speaker notes:**
- Walk the live run on screens 1, 3, 2 and 5, in that order. The picture is the timed run on 2026-10-17; your output will differ.
- In that run, screen 1 showed "primary verdict ready: PASS" 4 min 11 s after launch, with new R1 violations 0.
- The agent opened the handbook with its third call, then the map's ARCHITECTURE.md and the add-endpoint skill.
- F1 changes no board pixels, so screen 2 shows one board frame with Acme cards only.
- Question to ask the room: Which file did tonight's agent open first?
- Transition: Now what the verdict means.

## Slide 20: Demo: reading the result
**Section:** S1  **Time:** 0:46–0:51 (5 min)
**On the slide:**
- Timed run: no new R1 violation
- Hidden tests 52 of 52; mutants killed 2 of 4
- One run shows the layer ran
- It cannot show the layer helped
**Visual:** Screenshot `slides/img/s1-result.png` (screen 3 of the same timed run). Callouts: (1) the `r1_tenant` line, "new violations 0"; (2) the files-read list with the docs the map points to; (3) the hidden tests and mutants counts.
**Speaker notes:**
- Read tonight's verdict from screen 1 first, then this slide.
- Referee mutants are small planted bugs the agent never sees; the arm's own tests should fail on them. Killing 2 of 4 is not part of this section's measure.
- Say: "This is one harness arm on one run. It shows the layer ran. It cannot show the layer helped."
- The bare arm is not in tonight's run, so we compare with the runs from before class.
- Question to ask the room: What would you need to see to say the map helped?
- Transition: Here is what we measured before class.

## Slide 21: What we measured: S1
**Section:** S1  **Time:** 0:51–0:55 (4 min)
**On the slide:**
- No new tenant leak: bare 7 of 7
- No new tenant leak: harness 7 of 7
- No measurable difference on this ticket
- Poll answer: A
**Visual:** Dot chart, two rows. Row "Bare" (grey): 7 filled dots. Row "Harness" (blue): 7 filled dots. Small labels under the dots group them by round: medium effort (3), low effort (3), class settings (1). Legend: filled = passed, hollow = failed.
**Speaker notes:**
- The 7 runs per arm: the medium-effort round (3), the low-effort round (3) and the class-settings round (1), all on the legacy-pattern ticket.
- Every arm passed 52 of 52 hidden tests. No arm copied the legacy handler into a leak.
- Post hoc means chosen after the results were known: it describes, it never tests. Post hoc over 10 F1 runs per arm, bare arms claimed done in 9 and harness arms in 5, with no false done claim.
- Say it plainly: no measurable difference on this task with this model.
- Question to ask the room: Does a tie mean the map is useless?
- Transition: Why did it come out this way?

## Slide 22: Why a tie, and when maps help
**Section:** S1  **Time:** 0:55–0:57 (2 min)
**On the slide:**
- The bare arm read the handbook and applied R1
- The rule was findable without a map
- Helps: rules scattered, buried, or unreadable in-repo
- Doesn't help: a model that already finds the rule
**Visual:** Two columns. Left "Helps when" (blue): long or scattered docs, rules outside the repository, a model that skims. Right "Doesn't help when" (grey): one short handbook, a model that reads it, a rule the ticket already names.
**Speaker notes:**
- In one earlier round every bare arm opened the handbook with its third tool call. In the class-settings round the bare arm did not open it and still wrote an org-scoped query.
- Our bare arm had the rules in a handbook on disk. OpenAI compares a map with one giant instruction file, so these runs did not test OpenAI's comparison.
- The assumption "the model will not apply a rule it was not pointed to" did not hold for this model on this ticket.
- Question to ask the room: What would have to be true for the map to earn its place?
- Transition: Open questions, then the next section.

## Slide 23: Q&A, then sessions that end
**Section:** S1  **Time:** 0:57–1:00 (3 min)
**On the slide:**
- Questions on maps, docs and skills
- Runbook: `section-1-instructions/demo/README.md`
- Next: what happens when a session ends halfway
**Visual:** A large "Q&A" title. Under it the five-part diagram, small, with Instructions marked done and State glowing as "next".
**Speaker notes:**
- Tie the discussion back to cause 1: what is not in context does not exist.
- Remind the room: every piece encodes an assumption about the model, and this one did not show a gain here.
- The runbook has the practice steps and the expected screenshots.
- Question to ask the room: Which question about maps is still open for you?
- Transition: A map tells the agent where things are. It does not tell a fresh session what the last one did.

---

## Slide 24: S2: What the agent remembers
**Section:** S2  **Time:** 1:00–1:01 (1 min)
**On the slide:**
- Section 2 of 4: State and session lifecycle
- Progress files, git history, the handoff
- Live: `make show-2 SESSION_BUDGET=12,38`
**Visual:** The five-part diagram. The State box is highlighted in blue with a thick border and the label "now"; Instructions is shown as done (outlined), Scope, Verification and Sandbox are pale.
**Speaker notes:**
- This section covers the initializer step, `init.sh`, the progress file and git history.
- It covers an exec plan and a structured handoff that let a session resume after a reset.
- We read the result as redone or lost work after a forced stop.
- Question to ask the room: How does your agent know what yesterday's session did?
- Transition: Poll first, then launch.

## Slide 25: Poll, then launch `make show-2`
**Section:** S2  **Time:** 1:01–1:05 (4 min)
**On the slide:**
- Before class: 7 A/Bs, stopped after 12 turns
- Which arms failed the continuity measure?
- A) None  B) Bare  C) Harness  D) Both
- Then: `make show-2 SESSION_BUDGET=12,38`
**Visual:** Poll card on the left. Right: flow `make show-2` → "Session 1: 12 turns" → "Harness writes the handoff and progress.md" → "Session 2: empty context, 38 turns" → "Getting up to speed: progress.md, git log" → "Referee: continuity first" → "primary verdict ready". All blue.
**Speaker notes:**
- The ticket is F2, comments, over two sessions. Launch at 1:03 in terminal B, then open the newest run.
- The session turn budget is the fixed number of turns a session gets before the runner stops it: 12, then 38. It is the same for both arms.
- In a timed run on 2026-10-17, session 1 stopped 1 min 23 s after launch, the primary verdict came at 6 min 46 s and the full verdict at 9 min 52 s; cost $0.029525.
- That run exited 2: session 2 hit the agent time limit. Exit 2 is a result, not a broken command.
- Question to ask the room: What should a stopped session leave behind?
- Transition: The question this section asks.

## Slide 26: Can a fresh session pick up?
**Section:** S2  **Time:** 1:05–1:07 (2 min)
**On the slide:**
- Session 1 stops at 12 turns
- Session 2 starts with an empty context
- Does it break or redo session 1's work?
- Primary measure: continuity failure per run
**Visual:** Two session bars on a timeline: Session 1 (12 turns) ending at a red stop line, Session 2 (38 turns) starting from an empty box. A question mark over the gap.
**Speaker notes:**
- The assumption the state files encode: a fresh session cannot pick up the work from the repository alone.
- A continuity failure is any of three things: R7 fails, a second migration creates the same table, or at least 30 percent of session 1's added lines are removed in session 2.
- R7 is the house rule for migrations: exactly one migration head, and a fresh upgrade works.
- Question to ask the room: Which of the three failures would be hardest to spot in review?
- Transition: What went wrong before class.

## Slide 27: The problem: the work stopped
**Section:** S2  **Time:** 1:07–1:11 (4 min)
**On the slide:**
- Did: called "finish not done" in session 1
- Went wrong: the build phase ended there
- Cost: 3 of 56 hidden tests passed
- Six of 12 arms built nothing
**Visual:** Three beats left to right: (1) a turn card "1.12 finish not_done"; (2) a closed gate labelled "build phase over, session 2 never ran"; (3) a score card "hidden tests 3 of 56: only the checkpoint's own tests".
**Speaker notes:**
- In the medium- and low-effort rounds, an early "finish not done" ended the whole build phase under the runner's rule at the time, in both arm types.
- Six of the 12 arms in those rounds built nothing: 3 of 56 hidden tests, the 3 that already pass on the starting checkpoint.
- We found it by reading a run. The fix applies to both arms: now that call ends only the session.
- Question to ask the room: Would you have found this bug from the scores alone?
- Transition: Why does a second session need help at all?

## Slide 28: Cause: every session starts empty
**Section:** S2  **Time:** 1:11–1:15 (4 min)
**On the slide:**
- "each new session begins with no memory of what came before."
- "However, compaction isn’t sufficient."
- What one session knew must be written down
- The next session must know where to read it
**Visual:** An illustration of engineers in shifts: shift 1 hands a sealed note to shift 2. Source line: Anthropic, Effective harnesses.
**Speaker notes:**
- Both quotes are from Anthropic, Effective harnesses.
- Anthropic's picture: engineers working in shifts, where each new engineer arrives with no memory of the previous shift.
- Without a record, the next session starts with a feature half-built and undocumented and "would then have to guess at what had happened".
- Question to ask the room: What do you write down at the end of your own working day?
- Transition: The harness answer: state on disk.

## Slide 29: Answer: state on disk
**Section:** S2  **Time:** 1:15–1:20 (5 min)
**On the slide:**
- `init.sh`, `progress.md`, an exec plan, git history
- Written by an initializer step before session 1
- Getting up to speed: progress, git log, `init.sh`
- End each session with a commit and progress update
**Visual:** A workspace folder with four highlighted files: `init.sh`, `progress.md`, `session-handoff.md`, `docs/exec-plans/active/…`. An arrow from "Initializer step (code, no model call)" writes them; an arrow from "Session 2" reads `progress.md` and `git log` first.
**Speaker notes:**
- Anthropic uses an initializer agent and a coding agent. In this course the initializer is a fixed harness step, plain code, because one ticket fixes the files.
- `progress.md` is the course's name for Anthropic's progress file. An exec plan is a plan checked into the repository, with its progress and decisions.
- "Getting up to speed" is Anthropic's own name for the routine at the start of each session.
- "End the session by writing a git commit and progress update." (Anthropic, Effective harnesses)
- Question to ask the room: Which of these files does your repository already have?
- Transition: The piece that carries the state across the stop: the handoff.

## Slide 30: Code: the structured handoff
**Section:** S2  **Time:** 1:20–1:26 (6 min)
**On the slide:**
- Two owners: the harness writes facts, the agent writes notes
- Neither overwrites the other
**Visual:** Code excerpt from `section-2-state-lifecycle/demo/walkthrough.md` (handoff.py, `merge`), with the key line highlighted in blue:
```python
# platform/src/shipharness/harness/state/handoff.py (lines 123-129)
def merge(existing: str | None, template: str, summary: str) -> str:
    """Header from the template, the new machine summary, and the agent's notes kept as written."""
    header = template.split(MACHINE, 1)[0]
    notes = template[template.index(NOTES) :]
    if existing and NOTES in existing:
        notes = existing[existing.index(NOTES) :]
    return f"{header}{MACHINE}\n\n{summary}\n\n{notes.rstrip()}\n"
```
Key line: `return f"{header}{MACHINE}\n\n{summary}\n\n{notes.rstrip()}\n"` (fresh machine summary plus the agent's own notes).
**Speaker notes:**
- A structured handoff is a file that carries the last session's state and the next steps to the next session.
- The machine summary is the part the harness writes from the repository: last commits, files changed, visible test result, migration heads.
- If the agent wrote nothing, the next session still gets the machine summary. A handoff that depends only on the agent is empty exactly when the agent ran out of turns.
- Section minute 25 falls here: check terminal B for the `Cost:` line of `make show-2`.
- Question to ask the room: Which facts would you never trust the agent to write?
- Transition: The section on one card.

## Slide 31: S2 cheat sheet
**Section:** S2  **Time:** 1:26–1:30 (4 min)
**On the slide:**
- Command: `make show-2 SESSION_BUDGET=12,38`
- Measure: continuity failure; none passes
- Watch: "Session 1 stopped", then "Session 2 resumed"
- Pass line: "Session 2 picked up the work."
- Runbook: `section-2-state-lifecycle/demo/README.md`
**Visual:** Printable card with rows: Command, Primary measure, What to watch (screens 1, 3, 2, 5), What to say. Fail line in small type: "The handoff did not carry the work. Screen 3 shows how."
**Speaker notes:**
- `SESSION_BUDGET=12,38` sets the two session turn budgets; leave it as written.
- The exit code is 2 when an arm stops at a time limit. Read it as a result.
- Practising alone, add `PURPOSE=pilot`.
- Question to ask the room: What would a continuity failure look like on screen 3?
- Transition: Let's look at the run.

## Slide 32: Demo: what to watch
**Section:** S2  **Time:** 1:30–1:36 (6 min)
**On the slide:**
- Screen 1: "Session 1 stopped", handoff file named
- "Session 2 resumed": `pwd; git log; cat progress.md`
- Screen 3: Sessions, and state files read
- Screen 5: the first wrong turn
**Visual:** Command strip `make show-2 SESSION_BUDGET=12,38` above screenshot `slides/img/s2-watch.png` (screen 1 of the timed run). Callouts: (1) turn 1.12 `finish not_done` followed by the pill "Session 1 stopped: ended by claim_not_done; handoff session-handoff.md"; (2) the pill "Session 2 resumed · prefix: core, instructions, state"; (3) turn 2.1 `run pwd; git log --oneline -20; cat progress.md`.
**Speaker notes:**
- In the timed run on 2026-10-17, session 1 stopped 1 min 23 s after launch. Your output will differ.
- Turn 1.11 committed `progress.md` and the exec plan; turn 1.12 called `finish not_done`. Since the runner fix, that call ends only the session, so session 2 ran.
- Session 2 began with the getting-up-to-speed routine, then read the ticket and the handbook.
- Question to ask the room: What did tonight's session 2 read first?
- Transition: Now the verdict.

## Slide 33: Demo: reading the result
**Section:** S2  **Time:** 1:36–1:41 (5 min)
**On the slide:**
- Timed run: no continuity failure
- Hidden tests 56 of 56
- The arm hit the agent time limit
- One run shows the layer ran
**Visual:** Screenshot `slides/img/s2-result.png` (screens 3 and 5 of the same timed run). Callouts: (1) the Sessions table, session 1 ended by `claim_not_done`, session 2 by timeout; (2) the continuity line "no continuity failure"; (3) screen 5's first wrong turn marker.
**Speaker notes:**
- Read tonight's screen 1 verdict first. In the timed run the primary verdict came 6 min 46 s after launch.
- The first wrong turn on screen 5 is a heuristic, not a verdict. In the timed run it pointed at an edit to `app/api/issues.py`; the F2 harness arm has no scope layer, so nothing stopped that edit.
- Exit 2 means the arm stopped at a time limit, not that the command broke.
- Question to ask the room: Is passing every hidden test enough to call this run good?
- Transition: Here is what we measured before class.

## Slide 34: What we measured: S2
**Section:** S2  **Time:** 1:41–1:45 (4 min)
**On the slide:**
- No continuity failure: bare 7 of 7
- No continuity failure: harness 7 of 7
- No measurable difference on this ticket
- Poll answer: A, no arm failed
**Visual:** Dot chart, two rows. Row "Bare" (grey): 7 filled dots. Row "Harness" (blue): 7 filled dots. Grouped by round: medium effort (3), low effort (3), class settings (1). A footnote marker on the arms that built nothing: "6 of 12 arms in the first two rounds built nothing; the measure cannot fail then."
**Speaker notes:**
- The 7 A/Bs ran a 12-turn first session and a 38-turn second session in both arms.
- The measure cannot fail when session 1 leaves nothing to redo, and 6 of 12 arms in the medium- and low-effort rounds built nothing.
- In the class-settings round, after the runner fix, both arms built the feature: 56 of 56 hidden tests.
- Post hoc over 9 F2 runs per arm: harness arms hit the agent time limit in 4, bare arms in 0; median wall time 361 s against 232 s.
- Question to ask the room: What would a fairer test of the handoff need?
- Transition: Why did it come out this way?

## Slide 35: Why a tie, and when state helps
**Section:** S2  **Time:** 1:45–1:47 (2 min)
**On the slide:**
- The bare arm found its own state with `git status`
- Git history already carried most of the work
- Helps: long tasks, uncommitted work, many resets
- Costs: turns and time spent re-reading
**Visual:** Two columns. Left "Helps when" (blue): work spans many sessions, the repo hides what is half-done, the model forgets to commit. Right "Doesn't help when" (grey): git log already tells the story, short tasks, a model that checks git itself.
**Speaker notes:**
- In an earlier round, a bare arm's session 2 ran `git status` in its fourth tool call, found the uncommitted migration, and carried on with no continuity failure.
- Anthropic notes a reset has a price: "orchestration complexity, token overhead, and latency".
- The same author dropped context resets once a newer model no longer needed them.
- Question to ask the room: Which state file would you keep for this model, and how would you measure it?
- Transition: Questions, then the break.

## Slide 36: Q&A, then a short break
**Section:** S2  **Time:** 1:47–1:50 (3 min)
**On the slide:**
- Questions on state, handoffs and resets
- Runbook: `section-2-state-lifecycle/demo/README.md`
- Next: break, then scope and the sandbox
**Visual:** A large "Q&A" title. Under it the five-part diagram, small, with Instructions and State marked done and Scope glowing as "next".
**Speaker notes:**
- Collect the open questions; park the long ones for the assignment review.
- Section 3 launches its live A/B right after its poll.
- Nothing runs over the break.
- Question to ask the room: What is one thing you would add to your own handoff file?
- Transition: Ten minutes. The return time is on the next slide.

---

## Slide 37: Break
**Section:** break  **Time:** 1:50–2:00 (10 min)
**On the slide:**
- Back in 10 minutes
- Return time written live
**Visual:** Statement layout: "Break" in large type, the return time written in by hand under it. Nothing else on the slide.
**Speaker notes:**
- Write the return time on the slide.
- Nothing runs during the break; do not launch any command.
- Check that terminal B and the console are still up before you leave the screen.
- Question to ask the room: Anything you want us to look at in the console after the break?
- Transition: Welcome back. Section 3 is a live A/B.

---

## Slide 38: S3: What the agent may change
**Section:** S3  **Time:** 2:00–2:01 (1 min)
**On the slide:**
- Section 3 of 4: Scope and sandbox
- Allowed paths per phase; one container per arm
- Live A/B: `make demo-3 FEATURE=F4`
**Visual:** The five-part diagram. The Scope box and the Sandbox box are highlighted in blue with thick borders and the label "now"; Instructions and State are outlined as done; Verification is pale.
**Speaker notes:**
- This section covers one feature at a time, allowed paths per phase, and a `passes` field only the harness sets.
- It covers the container limits for both arms and how to read a sandbox denial.
- We read the result as out-of-scope files in the shipped diff, bare arm against harness arm.
- Question to ask the room: Has an agent ever changed a file you did not ask it to touch?
- Transition: Poll, then the live A/B.

## Slide 39: Poll, then launch the live A/B
**Section:** S3  **Time:** 2:01–2:05 (4 min)
**On the slide:**
- 3 A/Bs on F4 before class
- In how many did bare ship an out-of-scope file?
- (a) 0  (b) 1  (c) 2  (d) 3
- Then: `make demo-3 FEATURE=F4`
**Visual:** Poll card on the left. Right: flow `make demo-3 FEATURE=F4` splits into "Bare arm: edits any file" (grey) and "Harness arm: allow list per phase" (blue); a dotted arrow from the harness arm "edit outside the list" ends at "Blocked, with the reason"; both arms feed "Referee: same checks" → "diff_scope: out-of-scope files per arm".
**Speaker notes:**
- F4 is optimistic concurrency. Its build may change the issue, audit and web files; `app/services/errors.py` is not on the list.
- Say before the vote: "The harness arm is not in the question. Its scope layer refuses any edit outside the list, so its zero is built in."
- Launch at 2:03. This is a live A/B because these runs showed a real gap. Each arm has its own sandbox with the same limits.
- In the S3 confirmation A/B that ran alone, timed run on 2026-10-17 with the 420 s limit: bare verdicts at 5:15 and 8:06, harness at 8:50 and 11:18; cost $0.048707.
- Question to ask the room: Why ask only about the bare arm?
- Transition: The question this section asks.

## Slide 40: Does the change stay in scope?
**Section:** S3  **Time:** 2:05–2:07 (2 min)
**On the slide:**
- The ticket lists the files each phase may change
- The bare arm sees the list as text
- The harness arm's list is enforced by code
- Measure: out-of-scope files in the shipped diff
**Visual:** A dashed box labelled "allowed paths, build phase" containing `app/api/issues.py`, `app/services/issues.py`, `app/repositories/audit.py`, `app/web/…`. Outside the box: `app/services/errors.py`, in red.
**Speaker notes:**
- Allowed paths are the globs a ticket lists for each phase: the files the agent may change then.
- A phase is one stage of a run: build writes the feature, test adds tests only.
- The assumption the scope layer encodes: the agent will change files outside the ticket unless code stops it.
- For this demo, an arm fails when it ships one or more files outside the list. That rule was registered before any of the three runs.
- Question to ask the room: Is a list in the prompt enough to keep an agent inside it?
- Transition: Here is what the bare agent did.

## Slide 41: The problem: a shared file edited
**Section:** S3  **Time:** 2:07–2:11 (4 min)
**On the slide:**
- Did: added an error class to `app/services/errors.py`
- Went wrong: a shared file outside the ticket
- Cost: a wider diff and risk to other features
- Every bare arm did it, 3 of 3
**Visual:** Three beats: (1) a diff card "+ class PreconditionFailed (412)" in `app/services/errors.py`; (2) the file sitting outside the dashed allowed-paths box, with arrows to other features that import it; (3) a review card "wider diff, more to check, shared code changed".
**Speaker notes:**
- In the S3 confirmation every bare arm changed `app/services/errors.py`; in one of them it added a `PreconditionFailed` error class.
- Post hoc, before the confirmation, bare arms on F4 left the allowed paths in 6 of 6 runs, two files each time.
- A shared file is where a small edit reaches other features; reviewers have to check more than the ticket.
- Question to ask the room: Is editing a shared errors file actually wrong, or just outside the ticket?
- Transition: Why do agents reach outside the ticket?

## Slide 42: Cause: copied patterns, hard-to-undo actions
**Section:** S3  **Time:** 2:11–2:15 (4 min)
**On the slide:**
- "Codex replicates patterns that already exist" (OpenAI)
- "(Run this in a container, not your actual machine)"
- File operations "to the project directory only"
- Actions "difficult to reverse or affect shared systems"
**Visual:** Four quote cards side by side, not merged, each with its source: OpenAI, Harness engineering; Anthropic, C compiler; Anthropic, Coding agent demo; Anthropic, Prompting best practices.
**Speaker notes:**
- No single source states this cause, so the four sources stand side by side.
- From the C compiler post: "in one instance, I did see Claude pkill -9 bash on accident, thus killing itself and ending the loop."
- The coding agent demo restricts file operations "to the project directory only".
- The last source is supplementary: without guidance a model "may take actions that are difficult to reverse or affect shared systems".
- Question to ask the room: Which of these four have you seen in your own runs?
- Transition: The harness answer has two parts: a feature list and a container.

## Slide 43: Answer: one feature, one container
**Section:** S3  **Time:** 2:15–2:20 (5 min)
**On the slide:**
- `feature_list.json`: one feature, a `passes` field
- Only the harness sets `passes`, with evidence
- Sandbox: no network, no swap, non-root
- Read-only root; only `/work` and `/tmp` writable
- Same sandbox for both arms: never the variable
**Visual:** Left: a JSON card `{"id": "F4", "passes": false}` with a lock icon, labelled "harness only". Right: a container box with labels "network none", "read-only root", "writable: /work, /tmp", "capabilities dropped", "non-root user". Two identical containers, one grey (bare), one blue (harness).
**Speaker notes:**
- Anthropic keeps a feature list as JSON because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
- In Anthropic's post the agent sets `passes`; this course moves that to the harness, after Anthropic's advice to separate the agent doing the work from the one judging it.
- A sandbox denial is the event when the container refuses a command; it carries a reason code. No run before class had one.
- The class profile gives each container 2 CPUs and the same limits in both arms. Detailed sandbox design is a later module.
- Question to ask the room: Why can't a sandbox ever show up as a win in our A/B?
- Transition: Here is the rule that decides one path.

## Slide 44: Code: allowed paths per phase
**Section:** S3  **Time:** 2:20–2:26 (6 min)
**On the slide:**
- One method decides each path
- The refusal names the phase and the list
**Visual:** Code excerpt from `section-3-scope-sandbox/demo/walkthrough.md` (guard.py, `PathRules.reason`), with the key line highlighted in blue:
```python
# platform/src/shipharness/harness/scope/guard.py (lines 68-78)
    def reason(self, path: str) -> str | None:
        """None if the agent may change `path`; otherwise the reason it sees."""
        rel = normalise(path)
        if rel in HARNESS_ONLY:
            return HARNESS_ONLY[rel]
        if self.state_files and any(glob_matches(rel, p) for p in STATE_FILES):
            return None
        if self.allowed is None or any(glob_matches(rel, p) for p in self.allowed):
            return None
        listed = ", ".join(self.allowed) or "(none)"
        return f"{rel} is outside the allowed paths for the {self.phase} phase ({listed})"
```
Key line: `return f"{rel} is outside the allowed paths for the {self.phase} phase ({listed})"` (the text the harness arm reads when it is blocked).
**Speaker notes:**
- `HARNESS_ONLY` is checked first: the feature list and its schema. No allow list can open them, so the agent can never mark its own feature as passing.
- With the state layer on, the state files belong to the agent in every phase.
- A refused patch is blocked before anything is written; a command's stray change is reverted right after it runs.
- Section minute 25 falls here: check terminal B for the `Cost:` line of `make demo-3`.
- Question to ask the room: Why name the full list in the refusal instead of just saying no?
- Transition: The section on one card.

## Slide 45: S3 cheat sheet
**Section:** S3  **Time:** 2:26–2:30 (4 min)
**On the slide:**
- Command: `make demo-3 FEATURE=F4` (live A/B)
- Measure here: out-of-scope files; zero passes
- Read `diff_scope` on screen 3, not the pill
- Pass line: "No file outside the ticket's paths."
- Runbook: `section-3-scope-sandbox/demo/README.md`
**Visual:** Printable card with rows: Command, Primary measure, What to watch (screen 3 Scope column, then Verification column, then screen 1, then Sandbox denials), What to say. Fail line in small type: "This arm changed a file it was not asked to touch."
**Speaker notes:**
- The pill on screen 1 shows F4's own bar: every hidden test and every referee mutant. Every arm failed that bar before class.
- So read `diff_scope` on screen 3 for this section's question.
- If screen 3 lists no sandbox denial, show the policy printout instead.
- Question to ask the room: Why might the screen 1 pill mislead you in this section?
- Transition: Both arms should be done. Let's look.

## Slide 46: Demo: what to watch
**Section:** S3  **Time:** 2:30–2:36 (6 min)
**On the slide:**
- Screen 3: bare changed `app/services/errors.py`
- Harness diff map: same file ⊘ blocked
- Screen 1: the block decision and its reason
- Sandbox denials: none expected in either arm
**Visual:** Command strip `make demo-3 FEATURE=F4` above screenshot `slides/img/s3-watch.png` (screen 3 of an S3 confirmation A/B, Scope and sandbox column). Bare panel tinted grey, harness panel tinted blue. Callouts: (1) BARE "changed app/services/errors.py"; (2) HARNESS "⊘ blocked app/services/errors.py"; (3) "Sandbox denials ✓ none" in both panels.
**Speaker notes:**
- In the S3 confirmation A/B that ran alone, timed run on 2026-10-17: the bare patch to `app/services/errors.py` applied at 0:23 on the console clock; the harness patch was blocked at 1:16.
- The harness arm read: "app/services/errors.py: outside the allowed paths for the build phase".
- After the refusal, the harness arm put its 412 error in `app/services/issues.py`, a file it was allowed to change.
- If tonight's run records a sandbox denial, show its reason code and command.
- Question to ask the room: What did the harness agent do right after it was blocked tonight?
- Transition: Now the verdict lines.

## Slide 47: Demo: reading the result
**Section:** S3  **Time:** 2:36–2:41 (5 min)
**On the slide:**
- Read `diff_scope`: bare 1 new, harness 0
- Both arms still failed F4's own bar
- The guard keeps the change in scope
- It does not make the change correct
**Visual:** Screenshot `slides/img/s3-result.png` (screen 1 verdict lines of the same A/B; bare on the left in grey, harness on the right in blue). Callouts: (1) both "primary verdict ready: FAIL" pills: "F4's own bar, not this section's"; (2) bare "hidden tests 68/69"; (3) harness "hidden tests 65/69".
**Speaker notes:**
- Read tonight's `diff_scope` lines first, then this slide. If tonight's bare arm stays in scope, say so: one A/B is one dot.
- Say: "The guard enforces exactly what we measure, so the harness arm's zero is built in. What the runs show is that, on this ticket, the bare agent edits a shared file every time."
- In the confirmation, arms passed 62 to 68 of 69 hidden tests, so all six failed F4's own measure.
- The harness arms stopped on the harness's own 120 s limit, each after shipping its change, so the gap is not caused by harness-only timeouts.
- Question to ask the room: Does a guard that wins by construction tell us anything?
- Transition: Here is what we measured before class.

## Slide 48: What we measured: S3
**Section:** S3  **Time:** 2:41–2:45 (4 min)
**On the slide:**
- F4, in scope: bare 0 of 3
- F4, in scope: harness 3 of 3, harness ahead
- F3, the section's ticket: 7 of 7 each
- F3: no measurable difference
- Poll answer: (d), all 3
**Visual:** Two dot charts side by side. Left "F4, S3 confirmation": row "Bare" (grey) 3 hollow dots; row "Harness" (blue) 3 filled dots. Right "F3, tempting-middleware ticket": row "Bare" (grey) 7 filled dots; row "Harness" (blue) 7 filled dots. Legend: filled = no out-of-scope file, hollow = one or more.
**Speaker notes:**
- The S3 confirmation was registered before any of its runs: F4 ticket, the Section 3 stack, class profile with the 420 s agent limit, 3 A/Bs.
- On F3, the ticket with a tempting shared middleware, no arm ever left scope in 7 runs per arm, and every arm passed 49 of 49 hidden tests.
- Post hoc over 34 arm runs per arm across all sections: files changed outside the allowed paths in 9 bare runs and 0 harness runs.
- Say it plainly: one harness lead, on scope, by construction.
- Question to ask the room: Why did the bare arm stay in scope on F3 but not on F4?
- Transition: So when does a scope guard help?

## Slide 49: Why it won, and its limits
**Section:** S3  **Time:** 2:45–2:47 (2 min)
**On the slide:**
- The guard enforces what the measure counts
- F4 tempts the agent into a shared file
- Helps: shared code near the ticket
- Doesn't help: correctness; all arms failed F4's bar
**Visual:** Two columns. Left "Helps when" (blue): a tempting shared module, strict ownership, risky files like migrations or config. Right "Doesn't help when" (grey): the agent stays in scope anyway (F3), the bug is inside the allowed files, the list is wrong.
**Speaker notes:**
- The win is real but narrow: on F4 the bare agent reaches for `app/services/errors.py` every time; on F3 it never left scope.
- A guard that blocks every edit would also score zero out-of-scope files, and ship nothing.
- So measure scope next to hidden tests passed and existing tests that keep passing.
- Question to ask the room: What would you measure next to the guard, so a guard that blocks everything cannot look good?
- Transition: Questions, then who decides that work is done.

## Slide 50: Q&A, then who says "done"
**Section:** S3  **Time:** 2:47–2:50 (3 min)
**On the slide:**
- Questions on scope, allow lists and the sandbox
- Runbook: `section-3-scope-sandbox/demo/README.md`
- Next: what proves the work is done
**Visual:** A large "Q&A" title. Under it the five-part diagram, small, with Instructions, State, Scope and Sandbox marked done and Verification glowing as "next".
**Speaker notes:**
- The scope layer keeps a change in scope. It says nothing about whether the change works.
- Section 4 opens with two polls: the section poll and the final feature poll.
- Have terminal C ready for the final A/B.
- Question to ask the room: Who in your team decides that an agent's work is done?
- Transition: Section 4: verification.

---

## Slide 51: S4: What proves it is done
**Section:** S4  **Time:** 2:50–2:51 (1 min)
**On the slide:**
- Section 4 of 4: Verification
- Gate, filters, hidden tests, referee mutants
- Live: `make show-4`, then the final A/B
**Visual:** The five-part diagram. The Verification box is highlighted in blue with a thick border and the label "now"; the other three layers and the sandbox are outlined as done.
**Speaker notes:**
- This section covers verification the agent does not control: filters, mutants, house-rule checks, held-out tests, a reviewer and a gate.
- It covers how to find the first wrong turn in a trace.
- We read the result as hidden tests passed and mutants caught, as counts per run.
- Question to ask the room: When your agent says "done", what do you check first?
- Transition: Two polls, then two launches.

## Slide 52: Polls, then two launches
**Section:** S4  **Time:** 2:51–2:55 (4 min)
**On the slide:**
- 4 F4 A/Bs before class: which arm passed more?
- A) Harness  B) Bare  C) Equal  D) Neither
- Final poll: F5 Bulk close, F6 Watchers, F7 Labels
- Terminal B: `make show-4`
- Terminal C: `make final FEATURES=F6,F5`
**Visual:** Two poll cards side by side. Under them two terminal strips: terminal B `make show-4` (blue, harness only) and terminal C `make final FEATURES=F6,F5` (grey and blue, both arms), with the note "winner first, runner-up second".
**Speaker notes:**
- A run passes only with all 69 hidden tests passing and all 4 referee mutants killed by its own tests. The 4 A/Bs: the medium-effort round (3) and the class-settings round (1).
- Launch `make show-4` at 2:54 in terminal B, then `make final` at 2:55 in terminal C with the poll's winner first. Always pass `FEATURES`. Open each run in its own browser tab.
- In a timed run on 2026-10-17, `make show-4` gave its primary verdict at 9 min 19 s and its full verdict at 10 min 55 s; cost $0.026511. It exited 2 at the agent time limit.
- A timed run of `make final FEATURES=F5` on 2026-10-17 took 12 min 47 s. F6 was not timed; it has two sessions.
- Question to ask the room: Why would anyone vote D?
- Transition: The question this section asks.

## Slide 53: Can we trust the agent's "done"?
**Section:** S4  **Time:** 2:55–2:57 (2 min)
**On the slide:**
- The agent sees visible tests only
- The referee holds 69 hidden tests, 4 mutants
- Pass: every hidden test and every mutant
- Measure: one pass or fail per run
**Visual:** Two boxes: "What the agent can see" (visible tests, house-rule checks, the gate) and "What only the referee holds" (hidden tests, referee mutants), separated by a wall.
**Speaker notes:**
- The assumption the gate and filters encode: the agent's "done" and its own tests cannot be trusted.
- The F4 ticket is optimistic concurrency again, now with all four layers.
- One referee mutant makes writes stop moving the version; a shipped test catches it only if it checks that a stale save gets 412.
- Question to ask the room: What does a mutant catch that a hidden test does not?
- Transition: What the bare agent did before class.

## Slide 54: The problem: a false "done"
**Section:** S4  **Time:** 2:57–3:01 (4 min)
**On the slide:**
- Did: claimed done, "complete visible suite (191 passing)"
- Went wrong: one hidden test failed
- Cost: 68 of 69; the referee failed it
- The stale-version 412 case was missed
**Visual:** Three beats: (1) a claim card quoting "Verified the complete visible suite (191 passing)" with a green tick; (2) a red card `test_invalid_body_with_a_stale_version_is_412`; (3) a verdict card "hidden 68 of 69: FAIL".
**Speaker notes:**
- This was the bare arm of the class-settings round on F4. In that A/B both arms failed the same hidden test.
- It is the one done claim in the test runs that came with a failing hidden test.
- Across 34 arm runs per arm, bare arms claimed done 19 times and harness arms 10 times, with no failing hidden tests in those claims.
- Question to ask the room: Would your CI have caught this before merge?
- Transition: Why do agents over-report done?

## Slide 55: Cause: self-grading and visible tests
**Section:** S4  **Time:** 3:01–3:05 (4 min)
**On the slide:**
- "agents reliably skew positive when grading their own work"
- "every frontier agent saturates the visible suite"
- Mostly features that fail when combined
- "easy to see tests pass and assume the job is done"
**Visual:** Four short quote cards with sources: Anthropic, Harness design; SpecBench (two cards); Anthropic, C compiler.
**Speaker notes:**
- SpecBench in full: "while every frontier agent saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout suites."
- SpecBench also finds that "compositional failures account for a much larger fraction of reward hacking behavior" than deliberate exploits.
- The C compiler post: "For autonomous systems, it is easy to see tests pass and assume the job is done, when this is rarely the case."
- Question to ask the room: Who grades your agent's work today, the agent or something else?
- Transition: The harness answer: checks the agent does not control.

## Slide 56: Answer: checks the agent can't control
**Section:** S4  **Time:** 3:05–3:10 (5 min)
**On the slide:**
- Test filters 1–3 from TestGen-LLM; 4–5 ours
- Five runs: a flaky test is discarded
- Mutants for the fault you care about (ACH)
- Hidden tests that combine features (SpecBench)
- A blinded reviewer; a gate on "done"
**Visual:** A funnel: proposed tests enter at the top and pass filter 1 (builds), 2 (passes on every one of five runs), 3 (adds coverage or kills a filter mutant), 4 (real assertions), 5 (no source change in the test phase). Kept tests drop out the bottom. Beside the funnel, a separate referee box: hidden tests and referee mutants, "never visible to the filters".
**Speaker notes:**
- TestGen-LLM: "a test that does not pass on every one of five executions is deemed flaky." The referee also re-runs shipped tests five times, for both arms.
- ACH reports that 49% of tests that uniquely kill a mutant add no line coverage; that is why filter 3 also accepts a killed mutant.
- The filter mutants and referee mutants never overlap. The blinded reviewer sees diffs without arm traces.
- Anthropic, Harness design: "It is worth the cost when the task sits beyond what the current model does reliably solo."
- Question to ask the room: Which filter would you add first in your own repository?
- Transition: The gate, in code.

## Slide 57: Code: the gate's verdict
**Section:** S4  **Time:** 3:10–3:16 (6 min)
**On the slide:**
- One failed item fails the gate
- Failures go back to the agent as feedback
**Visual:** Code excerpt from `section-4-verification/demo/walkthrough.md` (gate.py, the verdict), with the key line highlighted in blue:
```python
# platform/src/shipharness/harness/verify/gate.py (lines 176-181)
    passed = not any(i.status == "fail" for i in items)
    feedback = "" if passed else _feedback(gate_id, items, lines)
    result = GateResult(gate_id=gate_id, items=items, passed=passed, feedback=feedback)
    if on_update:
        on_update(result)
    return result
```
Key line: `passed = not any(i.status == "fail" for i in items)`.
**Speaker notes:**
- The verify gate is the set of checks that run in the agent's container when it claims done; a failure sends the claim back with "Not accepted." and the feedback.
- Items: visible tests, house rules R1 to R7, existing tests, a board check, and clean state. Clean state means all work committed, lint clean, one migration head, no debug output.
- What is missing matters most: no hidden tests and no referee mutants. They stay with the referee.
- Section minute 25 falls here: check terminal B for the `show-4` `Cost:` line and terminal C for the final.
- Question to ask the room: Why keep the hidden tests out of the gate?
- Transition: The section on one card.

## Slide 58: S4 cheat sheet
**Section:** S4  **Time:** 3:16–3:20 (4 min)
**On the slide:**
- Command: `make show-4` (harness arm alone, F4)
- Measure: all 69 hidden tests, all 4 mutants
- Watch: gate pills, test phase, filter table
- Pass line: "Every hidden test and every mutant."
- Runbook: `section-4-verification/demo/README.md`
**Visual:** Printable card with rows: Command, Primary measure, What to watch (screen 1, screen 3, screen 2), What to say. Fail line in small type: "The agent said done. The hidden tests and mutants say no."
**Speaker notes:**
- The final A/B keeps running in terminal C while we read show-4.
- Exit 2 means an arm stopped at a time or cost limit; the run is still judged.
- Practising alone, add `PURPOSE=pilot`.
- Question to ask the room: What would you expect the gate pills to show if the agent cut corners?
- Transition: Let's read the run.

## Slide 59: Demo: what to watch
**Section:** S4  **Time:** 3:20–3:26 (6 min)
**On the slide:**
- Screen 1: a ⊘ blocked edit, then "done"
- Gate pills: visible tests to clean state
- Test phase: proposed tests and the filters
- Screen 2: the two-tab conflict panel
**Visual:** Command strip `make show-4` above screenshot `slides/img/s4-watch.png` (screen 1 harness panel joined with screen 2's conflict panel, timed run). Callouts: (1) the row of green gate pills from "visible tests" to "clean state"; (2) "primary verdict ready: FAIL", hidden tests 68, mutants killed 0; (3) "CONFLICT DETECTED: tab B got HTTP 409" with "This issue was changed by someone else".
**Speaker notes:**
- In the timed run on 2026-10-17: the scope layer blocked `app/services/errors.py` at 0 min 55 s, the same edit as in Section 3.
- The done claim came at 2 min 18 s and the gate passed every item at 3 min 24 s, with 190 visible tests passing.
- The test filters ran on 4 proposed tests from 5 min 51 s; the agent time limit ended the run at 8 min 34 s.
- Screen 2 shows the feature working in the browser: tab B's stale save is refused.
- Question to ask the room: The gate passed. Why is the verdict red?
- Transition: Reading the result.

## Slide 60: Demo: reading the result
**Section:** S4  **Time:** 3:26–3:31 (5 min)
**On the slide:**
- Timed run: the gate passed
- Hidden tests 68 of 69; mutants 0 of 4
- Primary verdict: fail
- The gate never sees hidden tests or mutants
**Visual:** Screenshot `slides/img/s4-result.png` (screen 3 of the same timed run). Callouts: (1) the filter table: one test kept, others discarded with reasons; (2) the filter 2 reason "failed on run 1 of 5: assert 422 == 412"; (3) the mutant table, 0 of 4 killed.
**Speaker notes:**
- Say: "The gate checks what the agent can see. The hidden tests and the referee's mutants stay out of its reach."
- The failing hidden test was the stale-version 412 case, the same one the bare arm missed in the class-settings round.
- The test that filter 2 discarded asserted that exact behaviour and got 422. The agent had the right idea; its code did not do it.
- This is a harness-in-action run, so it is not part of the counts on the next slide.
- Question to ask the room: What would a gate need to catch to stop this run?
- Transition: Here is what we measured before class.

## Slide 61: What we measured: S4
**Section:** S4  **Time:** 3:31–3:35 (4 min)
**On the slide:**
- Every hidden test and mutant: bare 0 of 4
- Every hidden test and mutant: harness 0 of 4
- No measurable difference on this ticket
- Poll answer: D, neither arm passed
**Visual:** Dot chart, two rows. Row "Bare" (grey): 4 hollow dots. Row "Harness" (blue): 4 hollow dots. Grouped by round: medium effort (3), class settings (1). Legend: filled = passed, hollow = failed.
**Speaker notes:**
- In the medium-effort round bare arms passed 66, 66 and 69 of 69 hidden tests and killed 4, 0 and 3 of 4 mutants; no run did both.
- In the class-settings round both arms passed 68 of 69; mutants killed: bare 4, harness 1.
- No F4 harness arm claimed done in these A/Bs, so the gate never ran in them.
- Say it plainly: no measurable difference on this task with this model.
- Question to ask the room: If neither arm ever passes, what does the measure tell us?
- Transition: Why did it come out this way?

## Slide 62: Why a tie, and when gates help
**Section:** S4  **Time:** 3:35–3:37 (2 min)
**On the slide:**
- Neither arm reached F4's bar
- Harness arms spent turns and hit time limits
- Helps: an agent that claims done too early
- Doesn't help: faults only hidden tests reveal
**Visual:** Two columns. Left "Helps when" (blue): frequent false done claims, weak shipped tests, clear house rules to check. Right "Doesn't help when" (grey): the bar is beyond the model, the gate cannot see the failing case, turns run out first.
**Speaker notes:**
- Post hoc over 34 arm runs per arm: harness arms hit the agent time limit in 9, bare arms in 4. Median tests shipped: harness 2.5, bare 7.5.
- The gate catches what it can see. The failing 412 case was not in what it can see.
- One false done in 4 F4 runs per arm, from the bare arm: there was little for a gate to catch on this model.
- Question to ask the room: What would a gate need to catch to earn its turns on this model?
- Transition: Questions, then the final results.

## Slide 63: Q&A, then the final A/B
**Section:** S4  **Time:** 3:37–3:40 (3 min)
**On the slide:**
- Questions on gates, filters and mutants
- Runbook: `section-4-verification/demo/README.md`
- Next: the final A/B's results
**Visual:** A large "Q&A" title. Under it the five-part diagram, small, with all four layers and the sandbox marked done, and an arrow to "Final A/B".
**Speaker notes:**
- Tie the discussion to cause 4: tests that pass are not the same as work that is done.
- While you take questions, glance at terminal C: the final should be finishing.
- If the final is not finished at 3:40, walk its live screens 1 and 2 first and come back to screen 4 at the end.
- Question to ask the room: Which check would you add to your own CI after tonight?
- Transition: The final A/B, all four layers.

---

## Slide 64: Final A/B: the poll's features
**Section:** close  **Time:** 3:40–3:41 (1 min)
**On the slide:**
- Launched 2:55: `make final FEATURES=F6,F5`
- Poll winner first, runner-up second
- Both arms; harness has all four layers
- No primary measure: read hidden tests, mutants
**Visual:** Flow: "Poll winner" → `make final FEATURES=F6,F5` → splits into "Bare arm" (grey) and "Harness arm: four layers" (blue) → "Same referee, same checks, blinded reviewer" → "One dot per arm on screen 4".
**Speaker notes:**
- The final launched in Section 4 and ran during it. No run starts now.
- `make final` runs its features one after another; F6 has two sessions, so it includes a context reset.
- The final has no registered primary measure, so `passed=True` does not mean the feature works.
- Question to ask the room: Before we look, which arm do you expect to do better?
- Transition: Read the arm lines in terminal C.

## Slide 65: Final: reading the arm lines
**Section:** close  **Time:** 3:41–3:43 (2 min)
**On the slide:**
- One line per arm, per feature
- Read `hidden` and `mutants`, not `passed`
- Read the session figure on the `Cost:` line
- An aborted arm is still judged
**Visual:** Terminal C output, large font. Callouts on (1) the `hidden` counts per arm, (2) the `mutants` counts per arm, (3) the session figure in the `Cost:` line. Bare line tinted grey, harness line tinted blue.
**Speaker notes:**
- In the timed run of `make final FEATURES=F5` on 2026-10-17, both arms passed 46 of 46 hidden tests and killed 2 of 3 mutants; cost $0.045597.
- In that run the bare arm claimed done; the harness arm hit the agent time limit without a claim, so the command exited 2.
- Read tonight's lines aloud for each feature.
- Question to ask the room: Do tonight's counts differ between the arms?
- Transition: Let's see both arms on the console.

## Slide 66: Final: the console
**Section:** close  **Time:** 3:43–3:46 (3 min)
**On the slide:**
- Screen 1: turns, decisions, gate pills per arm
- Screen 3: evidence, filters, mutants, reviewer
- Screen 5: the first wrong turn, trace links
**Visual:** Screenshot `slides/img/final-console.png` (screen 1 of the timed `make final FEATURES=F5` run). Bare arm on the left labelled grey, harness arm on the right labelled blue. Callouts: (1) bare verdict times 3:27 and 6:50; (2) harness verdict times 9:48 and 12:32; (3) hidden tests 46/46 and mutants 2/3 in both arms.
**Speaker notes:**
- Show tonight's final live on screens 1, 3 and 5 for both arms; the picture is the timed run on 2026-10-17.
- In that run the harness arm's second turn read `session-handoff.md`.
- Existing tests kept passing in both arms, 216 of 216. Bare shipped 8 tests, harness 2.
- Question to ask the room: Where do the two arms spend their turns differently?
- Transition: Now the boards.

## Slide 67: Final: the boards
**Section:** close  **Time:** 3:46–3:47 (1 min)
**On the slide:**
- Screen 2: each arm's board as an Acme user
- Look for ⚠ other-org and ⧉ duplicate marks
**Visual:** Screenshot `slides/img/final-boards.png` (screen 2 of the same timed run), bare board on the left (grey label), harness board on the right (blue label). Callouts: (1) the "✓ only own-org cards, no duplicates" pill on each board; (2) the Acme user badge.
**Speaker notes:**
- The marks come from trusted data attributes, not from the agent.
- In the class-settings round every board showed "✓ only own-org cards, no duplicates", and so did both boards of the timed final run.
- Check tonight's boards for either mark.
- Question to ask the room: What else would you want a board check to look for?
- Transition: Screen 4, where tonight's run joins the others.

## Slide 68: Final: one dot per arm
**Section:** close  **Time:** 3:47–3:49 (2 min)
**On the slide:**
- Screen 4: one dot per recorded run
- Tonight adds one dot per arm
- Filled = passed, hollow = failed
- One A/B is one dot
**Visual:** Screenshot `docs/images/screen-4-report.png` (screen 4 after a final run). Callouts: (1) the bare row of dots (grey); (2) the harness row of dots (blue); (3) the newest dot, "tonight's run".
**Speaker notes:**
- Say: "One A/B is one dot. Read it next to the runs from before class, never alone."
- The course ran `make final FEATURES=F5` twice before class. The two A/Bs split differently: once mutants killed were 2 of 3 in both arms, the other time 1 of 3 bare and 3 of 3 harness.
- Fill and stroke carry the result, never colour alone.
- Question to ask the room: How many dots would you want before changing your team's setup?
- Transition: Now every section on one slide.

## Slide 69: Results across all sections
**Section:** close  **Time:** 3:49–3:51 (2 min)
**On the slide:**
- S1, no new leak: 7 of 7 each
- S2, no continuity failure: 7 of 7 each
- S3, F4 in scope: bare 0, harness 3 of 3
- S4, all hidden tests and mutants: 0 of 4 each
- One lead, on scope, by construction
**Visual:** One dot chart with four section rows, each split into a grey bare line and a blue harness line: S1 (7 filled / 7 filled), S2 (7 filled / 7 filled), S3 F4 (3 hollow / 3 filled) with F3 (7 filled / 7 filled) in small type beside it, S4 (4 hollow / 4 hollow). Legend: filled = passed the section's primary measure.
**Speaker notes:**
- S1 to S3 on their own tickets: the medium-effort, low-effort and class-settings rounds. S4: the medium-effort and class-settings rounds. The S3 confirmation: 3 A/Bs, registered before its runs.
- Sections 1, 2 and 4: no measurable difference on this task with this model. Section 3's own ticket, F3: no measurable difference either.
- Section 3 on F4: harness ahead, because the guard enforces what the measure counts.
- Question to ask the room: Which result surprised you most?
- Transition: What the runs say overall.

## Slide 70: What we measured overall
**Section:** close  **Time:** 3:51–3:52 (1 min)
**On the slide:**
- Gate before the big batches: harness ahead in 0 of 4
- Post hoc, 34 runs per arm: out of scope 9 against 0
- Done claimed: bare 19, harness 10; none false
- Harness: more time-limit hits, 9 against 4
**Visual:** A small table, two columns (Bare grey, Harness blue): out of allowed paths 9 of 34 / 0 of 34; claimed done 19 of 34 / 10 of 34; time limit hit 4 of 34 / 9 of 34; median wall time 190 s / 302 s; median cost $0.0103 / $0.0123. Caption: "Post hoc: chosen after the results; describes, does not test."
**Speaker notes:**
- The gate registered before the larger batches needed the harness arm ahead in 3 of 4 sections. It was ahead in none, so the batches of 10 runs per arm and the one-layer-out runs were not run.
- So the course has no per-layer result to show. We say so rather than guess.
- Post hoc numbers describe what the arms did; they cannot change the gate.
- Question to ask the room: What would you change before running the larger batch?
- Transition: What to take home from a mostly tied result.

## Slide 71: Every piece is a bet
**Section:** close  **Time:** 3:52–3:53 (1 min)
**On the slide:**
- Each piece assumes the model can't do something
- Test that assumption on your model and tasks
- Keep what earns its place; drop the rest
- One model, one task per section, few runs
**Visual:** Four cards, one per layer, each with its assumption in one line and tonight's verdict as a small badge: Instructions "no measurable difference", State "no measurable difference", Scope "ahead on F4, by construction", Verification "no measurable difference".
**Speaker notes:**
- OpenAI warns that its own results should "not be assumed to generalize without similar investment".
- The same holds here: one model, one task per section, a few runs per arm.
- Your repository and your model may differ. Measure before you keep a piece.
- Question to ask the room: Which assumption would you test first on your own model?
- Transition: Here is how to do that in your repository.

## Slide 72: Use it in your repo: the kit
**Section:** close  **Time:** 3:53–3:54 (1 min)
**On the slide:**
- `uv run shipharness init --target ~/my-repo`
- `uv run shipharness init --check ~/my-repo`
- Map, docs, state files, feature list, checks
- REPLACE markers show what to fill
**Visual:** A folder tree of the copied kit: `AGENTS.md`, `docs/`, `progress.md`, `init.sh`, `feature_list.json` and its schema, house-rule check templates, a sandbox policy, a CI workflow, `.claude/skills/` and `.agents/skills/`. Callout: "REPLACE: your value here".
**Speaker notes:**
- `init` copies the starter kit with no model calls. Every template holds TeamTrack's real values, with a REPLACE marker next to each one.
- `init --check` lists the markers still to fill.
- The guide, `use-in-your-repo/apply-to-your-repo.md`, has seven steps; only step 5 makes model calls. It ends with deciding which layers earn their place.
- Question to ask the room: Which repository will you try this on first?
- Transition: Four skills come with the kit.

## Slide 73: Four skills to take home
**Section:** close  **Time:** 3:54–3:55 (1 min)
**On the slide:**
- `harness-setup`: assess a repo's harness, fill gaps
- `house-rules`: a convention becomes a rule, check, test
- `assured-tests`: keep tests that pass five filters
- `skill-template`: start a skill of your own
**Visual:** Four tiles in a row, one per skill, each with its folder path under `use-in-your-repo/skills/`. A strip under them: "Agent Skills format: works with Claude Code, Codex and Cursor".
**Speaker notes:**
- All four use the Agent Skills format, so the agent loads each only when a task needs it.
- `harness-setup` is the assessment you saw at 0:08.
- `assured-tests` is the Section 4 filter pipeline as a skill.
- Question to ask the room: Which convention in your team would make a good house rule?
- Transition: Your assignments.

## Slide 74: Assignments 1 and 2
**Section:** close  **Time:** 3:55–3:56 (1 min)
**On the slide:**
- A1: from one long instruction file to a map
- Folder: `section-1-instructions/assignment/`
- A2: three forced stops, one consistent history
- Folder: `section-2-state-lifecycle/assignment/`
**Visual:** Two cards. A1: a long file splitting into a map, docs and one skill, with a checker that proves no rule was lost. A2: four session bars with forced stops and a step ledger rebuilt from git at every stop.
**Speaker notes:**
- A1: split a long AGENTS.md into a map, focused docs and one skill, and write the checker that proves no rule was lost or brought back.
- A2: write a step ledger, one line per ticket step, rebuilt from git at every stop, so a fresh session knows what is done.
- Each assignment has grading criteria, a starter folder, an offline `make check-assignment-N`, one live step, and a full solution with a walkthrough. Try it first.
- Question to ask the room: Which of the two looks hardest to you?
- Transition: Assignments 3 and 4.

## Slide 75: Assignments 3 and 4
**Section:** close  **Time:** 3:56–3:57 (1 min)
**On the slide:**
- A3: scope you can check
- Folder: `section-3-scope-sandbox/assignment/`
- A4: verification and portfolio
- Folder: `section-4-verification/assignment/`
- Review session: one assignment at a time
**Visual:** Two cards. A3: a diff with a rename and a `../` path, both caught by a diff-scope policy. A4: a new house rule R8 (soft delete) and filter 6 (no duplicate test). Under both, a review-session timeline with four assignment slots and open questions.
**Speaker notes:**
- A3: build checks that decide what a diff really changes, renames and `../` paths included, before they decide whether it is allowed.
- A4: add house rule R8, a soft-deleted issue answers 404 and never appears in a list, and filter 6, which discards a test that repeats another.
- The review session takes each assignment in turn, then open questions.
- Question to ask the room: What would you put in your portfolio from tonight?
- Transition: The sources behind tonight.

## Slide 76: References (1 of 2)
**Section:** close  **Time:** 3:57–3:58 (1 min)
**On the slide:**
- OpenAI, Harness engineering · Lopopolo · 2026-02-11
- Anthropic, Effective harnesses · Young · 2025-11-26
- Anthropic, Harness design · Rajasekaran · 2026-03-24
- Anthropic, C compiler · Carlini · 2026-02-05
- Anthropic, Coding agent demo; Prompting best practices
**Visual:** A plain list in small type, one source per line, with the full title in grey after the short name: "Harness engineering: leveraging Codex in an agent-first world"; "Effective harnesses for long-running agents"; "Harness design for long-running application development"; "Building a C compiler with a team of parallel Claudes"; "Autonomous Coding Agent Demo (README)".
**Speaker notes:**
- These are the main sources behind the four causes and the four pieces.
- Full links are in `docs/REFERENCES.md` and on the evidence pages.
- OpenAI's "Using PLANS.md" cookbook (Friel, 2025-10-07) is behind the exec plans in Section 2.
- Question to ask the room: Which of these will you read first?
- Transition: The second page of sources.

## Slide 77: References (2 of 2)
**Section:** close  **Time:** 3:58–3:59 (1 min)
**On the slide:**
- Agent Skills: specification, "What are skills?", client guide
- The skills-ref validator; Claude Code, Codex, Cursor docs
- TestGen-LLM · Alshahwan et al., Meta · 2024
- ACH, mutation-guided test generation · Foster et al., Meta
- SpecBench · Zhao, Srikanth, Wu, Jiang (Weco AI)
**Visual:** A plain list in small type, one source per line, with the venue in grey: TestGen-LLM at FSE '24; ACH submitted to FSE 2025 Industry Track; SpecBench preprint and its repository; Codex docs on sandboxing and network access.
**Speaker notes:**
- The Agent Skills sources are behind the skill tiers in Section 1 and the four take-home skills.
- TestGen-LLM and ACH are behind the filters and mutants; SpecBench is behind the hidden tests that combine features.
- SpecBench here is the Weco AI paper, not the unrelated Spec-Bench.
- Question to ask the room: Any source you think we should add?
- Transition: Thank you.

## Slide 78: Thank you
**Section:** close  **Time:** 3:59–4:00 (1 min)
**On the slide:**
- Thank you
- Measure each piece; keep what earns its place
- Repository: `shipharness`; start with `make doctor`
**Visual:** Statement layout: "Thank you" large, the two lines under it, and the five-part diagram small at the bottom with all parts outlined.
**Speaker notes:**
- Thank the room and the helper who watched terminal B.
- Remind learners that every run tonight is in the console and the report.
- Point them to the assignments and the review session.
- Question to ask the room: What is the one piece you will test on your own repository this week?
- Transition: Close the session; run `uv run shipharness report` after class.
