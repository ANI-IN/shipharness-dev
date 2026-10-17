# Module 1: Harness Engineering for Coding Agents: slide content for review

103 slides, about 240 minutes of slide time in a 240-minute class. On-slide text follows the
owner's template (`template.pptx`): density, "Lead: rest" titles, build-ups, numbered series with a cheat
sheet, and the template's wording for breaks, demos, polls, and Q&A. Speaker notes are written so the
class can be taught from the notes alone. Numbers come only from `docs/evidence.md` and
`docs/evidence/*.md`; diagrams are Excalidraw files under `docs/diagrams/` and `section-N-*/diagrams/`.

## Index

| Slide | Title | Block | Diagram |
|---|---|---|---|
| 1 | Module 1: Harness Engineering for Coding Agents | Housekeeping | none |
| 2 | Introduction: Who is teaching tonight | Housekeeping | none |
| 3 | Welcome: Before we begin, pop into the chat | Housekeeping | none |
| 4 | Structure of Class: Four hours, four layers | Housekeeping | none |
| 5 | Recap: The Anatomy of an Agentic Loop (build 1/3) | Recap | docs/diagrams/agent-loop-step-1.png |
| 6 | Recap: The Anatomy of an Agentic Loop (build 2/3) | Recap | docs/diagrams/agent-loop-step-2.png |
| 7 | Recap: The Anatomy of an Agentic Loop (build 3/3) | Recap | docs/diagrams/agent-loop.png |
| 8 | Today's Agenda | Agenda | none |
| 9 | Problem statement: What are we building? | Problem | docs/diagrams/harness-around-loop.png |
| 10 | Problem statement: The problem in the real world | Problem | none |
| 11 | The challenge is: The rules exist, the agent still misses | Problem | none |
| 12 | Why this matters for Engineering Teams | Problem | none |
| 13 | Why We Need a Harness: The 4 Critical Gaps | Problem | docs/diagrams/stories-causes-layers.png |
| 14 | TeamTrack: The data model | Problem | docs/diagrams/teamtrack-data-model.png |
| 15 | Key Tech Stack: TeamTrack and shipharness | Problem | none |
| 16 | Example Tickets: F1 to F7 in plain words | Problem | none |
| 17 | How We'll Measure: Same ticket, two arms (build 1/2) | Problem | docs/diagrams/ab-referee-step-1.png |
| 18 | How We'll Measure: One referee scores both (build 2/2) | Problem | docs/diagrams/ab-referee.png |
| 19 | Let's Get It Started | Problem | none |
| 20 | Section 1: What the agent knows | Section 1 | none |
| 21 | Live Zoom Poll: Will the agent copy the legacy query? | Section 1 | none |
| 22 | Failure story: The search that showed another org | Section 1 | none |
| 23 | Instructions: Why not paste every rule? (build 1/3) | Section 1 | none |
| 24 | Instructions: Why not paste every rule? (build 2/3) | Section 1 | none |
| 25 | Instructions: Why not paste every rule? (build 3/3) | Section 1 | none |
| 26 | 1) A map, not a manual | Section 1 | section-1-instructions/diagrams/manual-vs-map.png |
| 27 | 2) Progressive disclosure: skills load in three tiers | Section 1 | section-1-instructions/diagrams/skills-three-tiers.png |
| 28 | 3) The context prefix: small, fixed, out of reach | Section 1 | section-1-instructions/diagrams/context-prefix.png |
| 29 | 4) Mechanical checks keep the map true | Section 1 | none |
| 30 | Cheat Sheet: The instructions layer in four moves | Section 1 | none |
| 31 | Section 1 - Implementation Notes: The map at work | Section 1 | screenshot: section-1-instructions/demo/expected/screen-1-final.png |
| 32 | What just happened: The run, minute by minute | Section 1 | none |
| 33 | Under the hood: How the prefix is built | Section 1 | none |
| 34 | What we measured: No measurable difference on F1 | Section 1 | section-1-instructions/diagrams/results-s1.png |
| 35 | Apply it Monday: Turn your instruction file into a map | Section 1 | none |
| 36 | Q&A: Section 1, what the agent knows | Section 1 | none |
| 37 | Time for a Break | Break | none |
| 38 | Today's Agenda: Section 2, what the agent remembers | Section 2 | none |
| 39 | Live Zoom Poll: Did session 2 redo session 1? | Section 2 | none |
| 40 | Problem statement: The second session redoes the first | Section 2 | section-2-state-lifecycle/diagrams/alembic-heads.png |
| 41 | Fresh session: Why redo work already on disk? (build 1/3) | Section 2 | none |
| 42 | Fresh session: Why redo work already on disk? (build 2/3) | Section 2 | none |
| 43 | Fresh session: Why redo work already on disk? (build 3/3) | Section 2 | none |
| 44 | 1) Session lifecycle: a planned stop and reset | Section 2 | section-2-state-lifecycle/diagrams/session-lifecycle.png (+ steps) |
| 45 | 2) The handoff: two owners, one file | Section 2 | section-2-state-lifecycle/diagrams/handoff-contents.png |
| 46 | 3) The exec plan and the progress ledger | Section 2 | none |
| 47 | 4) Getting up to speed: `init.sh` before code | Section 2 | section-2-state-lifecycle/diagrams/alembic-heads.png |
| 48 | Cheat Sheet: Four state pieces across a stop | Section 2 | none |
| 49 | Section 2 - Implementation Notes: Stop and resume | Section 2 | screenshot: section-2-state-lifecycle/demo/expected/show-2-screen-1-t02m.png |
| 50 | What just happened: One run, two sessions | Section 2 | none |
| 51 | Under the hood: What runs at every stop | Section 2 | none |
| 52 | What we measured: No measurable difference on F2 | Section 2 | section-2-state-lifecycle/diagrams/results-s2.png |
| 53 | Apply it Monday: State that survives a stop | Section 2 | none |
| 54 | Q&A: State and session lifecycle | Section 2 | none |
| 55 | Today's Agenda: Section 3, what the agent may change | Section 3 | none |
| 56 | Live Zoom Poll: Will the bare arm leave scope? | Section 3 | none |
| 57 | Problem statement: A tidy diff in a shared file | Section 3 | none |
| 58 | Scope: Is the ticket's file list enough? (build 1/2) | Section 3 | none |
| 59 | Scope: Is the ticket's file list enough? (build 2/2) | Section 3 | none |
| 60 | 1) One feature at a time: `feature_list.json` | Section 3 | none |
| 61 | 2) Allowed paths per phase, checked by code | Section 3 | section-3-scope-sandbox/diagrams/scope-check-flow.png |
| 62 | 3) The sandbox boundary: where the keys live | Section 3 | section-3-scope-sandbox/diagrams/sandbox-boundary.png |
| 63 | 4) Least privilege: two refusals, two questions | Section 3 | section-3-scope-sandbox/diagrams/least-privilege.png |
| 64 | Cheat Sheet: Four boundaries for one feature | Section 3 | none |
| 65 | Section 3 - Implementation Notes: Scope at work | Section 3 | screenshot: section-3-scope-sandbox/demo/expected/screen-3-final.png |
| 66 | What just happened: Same pull, two arms | Section 3 | none |
| 67 | Under the hood: One method decides every path | Section 3 | none |
| 68 | What we measured: Scope held on F4, by construction | Section 3 | section-3-scope-sandbox/diagrams/results-s3.png |
| 69 | Apply it Monday: Scope your next agent task | Section 3 | none |
| 70 | Q&A: Scope and sandbox | Section 3 | none |
| 71 | Time for a Break | Break | none |
| 72 | Section 4: What proves the work is done | Section 4 | none |
| 73 | Live Zoom Poll: F4 with all four layers | Section 4 | none |
| 74 | Live Zoom Poll: Pick the final A/B feature | Final | none |
| 75 | Launch: make show-4, the harness arm alone | Section 4 | screenshot: section-4-verification/demo/expected/show-4-screen-1-t03m.png |
| 76 | Launch: make final, the poll winner first | Final | docs/diagrams/ab-referee.png |
| 77 | The problem: Done, but two edits still collide | Section 4 | docs/diagrams/optimistic-concurrency.png |
| 78 | Verification: The suite is green. Is F4 done? (build 1/2) | Section 4 | none |
| 79 | Verification: The suite is green. Is F4 done? (build 2/2) | Section 4 | none |
| 80 | 1) Self-grading and visible tests | Section 4 | section-4-verification/diagrams/verification-pipeline-step-1.png |
| 81 | 2) Test-phase filters: keep tests that prove something | Section 4 | section-4-verification/diagrams/verification-pipeline-step-2.png |
| 82 | 3) Mutation testing and hidden tests | Section 4 | section-4-verification/diagrams/mutation-testing.png |
| 83 | 4) The gate on "done" and the separate referee | Section 4 | section-4-verification/diagrams/verification-pipeline-step-3.png |
| 84 | Cheat Sheet: four checks the agent does not own | Section 4 | section-4-verification/diagrams/verification-pipeline.png |
| 85 | Section 4 - Implementation Notes: The gate at work | Section 4 | screenshot: section-4-verification/demo/expected/show-4-screen-1-final.png |
| 86 | What just happened: eleven minutes of show-4 | Section 4 | screenshot: section-4-verification/demo/expected/show-4-screen-1-t01m.png (+ t03m, t04m, t09m) |
| 87 | Under the hood: the gate's verdict in six lines | Section 4 | none |
| 88 | What we measured: no measurable difference on F4 | Section 4 | section-4-verification/diagrams/results-s4.png |
| 89 | Apply it Monday: check your agent's done | Section 4 | none |
| 90 | Q&A: Section 4, Verification | Section 4 | none |
| 91 | Final A/B: reading the arm lines | Final | none |
| 92 | Final A/B: what to read on screens 1, 3, 5 | Final | screenshot: final-project/expected/screen-1-final.png |
| 93 | Final A/B: the two boards | Final | screenshot: final-project/expected/screen-2-final.png |
| 94 | All results: four sections, one picture | Final | docs/diagrams/results-final.png |
| 95 | Which layer when: match the layer to the failure | Final | docs/diagrams/which-layer-when.png |
| 96 | Use it in your repo: the kit and four skills | Close | docs/diagrams/harness-one-picture.png |
| 97 | Assignments (1 of 2): instructions and state | Close | none |
| 98 | Assignments (2 of 2): scope and verification | Close | none |
| 99 | Final project: one live A/B, read as one dot | Close | screenshot: final-project/expected/screen-4-final.png |
| 100 | References (1 of 2): harness engineering sources | Close | none |
| 101 | References (2 of 2): skills, tests, held-out evaluation | Close | none |
| 102 | Q&A: anything from today | Close | none |
| 103 | Thank you: see you at the review session | Close | none |

---

## Slide 1: Module 1: Harness Engineering for Coding Agents
**Block:** Housekeeping  **Time:** 0.25  **Diagram:** none
**On the slide:**
Module 1: Harness Engineering for Coding Agents
Instructions, state, scope, verification: build each layer, then measure it
**Visual:** Title layout. "Module 1" in blue, the rest of the title in white, the subtitle smaller underneath. No picture.
**Speaker notes:**
- Welcome. Tonight we build four layers around a coding agent, and you watch each one at work, live, on a real feature of a small app.
- Plain version of the topic: a harness is the files and code around the agent that decide what it sees and what it may do. It is not a better prompt.
- What is different about this class: we measured every layer before class. Same agent, same model, same ticket, with and without the layer, scored by the same program.
- We also show results where the layer did not help. In three of the four sections the measure showed no measurable difference on this model. Section 3 showed one gap, on one ticket (F4), partly by construction.
- Analogy: think of a CI check. You keep a check because it catches something real, not because it sounds responsible. Tonight we ask that question of each harness layer.
- Point at the subtitle: "build each layer, then measure it" is the whole course.
- Ask the room: "Who has already given a real ticket to a coding agent?" Expected: many hands. Ask one person what went wrong; you will hear one of tonight's four failures.
- Misconception to name early: "a harness is a long system prompt". No: tonight's harness includes files on disk, session state, a scope guard, and a gate on "done".
- Likely question: "Which model did you measure?" Answer: gpt-6-luna as the agent and gpt-5.6-luna as the blinded reviewer, the same settings for both arms; the results hold for that model only.
- Time: 15 seconds. Next: who is teaching tonight.

## Slide 2: Introduction: Who is teaching tonight
**Block:** Housekeeping  **Time:** 0.5  **Diagram:** none
**On the slide:**
Introduction: Who is teaching tonight
Your instructor, in 30 seconds:
- Where they ship code with coding agents
- One agent failure they had to debug
- The harness layer they would add first
- Where to reach them after class
**Visual:** Template slide 2 layout: "Introduction:" in blue, the lead-in line and four bullets on the left, a plain icon column on the right (laptop, bug, stacked layers, chat bubble). No name, photo, or logos, so the slide works for any instructor with nothing to fill in.
**Speaker notes:**
- Say your name and role aloud; the slide deliberately carries no name.
- Bullet 1, one sentence: your years in software and where you use coding agents today (team, kind of codebase, which agent: Claude Code, Codex, Cursor, Copilot).
- Bullet 2, 15 seconds: one agent diff that passed review and still broke a rule your team cared about. If you have none of your own, tell slide 10's Monday story and say it is the course's illustrative scenario.
- Map your failure to one of tonight's layers out loud: rule not in context (Section 1), lost session (2), edit outside the ticket (3), false "done" (4). It previews the night.
- Bullet 3: name the layer you would add first, and promise to revisit that choice after the results; the measurements may change it.
- Bullet 4: say the channel for questions after class (the course chat, the review session); do not type contact details on the slide.
- Analogy: a conference speaker's one-line bio: enough for the room to judge where your examples come from, nothing more.
- Point at bullet 2: it is the theme of the night, rules that exist but are not applied.
- Ask: "Which coding agents are you using at work?" Expected: Claude Code, Codex, Cursor, Copilot. Say: everything tonight applies to all of them.
- Likely question: "Do I need the repository running to follow along?" Answer: no. The demos run on the instructor's machine; the repository lets you repeat them later.
- Misconception: "this is a product pitch for a harness". Correction: three of tonight's four sections show no measurable difference, and the slides say so.
- Time: 30 seconds. Next: tell us who you are.

## Slide 3: Welcome: Before we begin, pop into the chat
**Block:** Housekeeping  **Time:** 0.5  **Diagram:** none
**On the slide:**
Welcome to today's class, before we begin, pop into the chat:
- Name
- Role
- Location
- The coding agent you use
**Visual:** Template slide 3: four emoji chips (speech bubble, worker, house, robot) around a sample person card. The fourth chip replaces "Organization" with "The coding agent you use".
**Speaker notes:**
- Say: "Welcome everyone. Before we begin, tell us four things in the chat: your name, your role, where you are, and the coding agent you use."
- Why the fourth chip changed: tonight's material applies to any agent that reads an AGENTS.md or skills folder, so knowing the room's tools helps you pick examples.
- Concrete example to read aloud from the chat: "Backend engineer, Berlin, Claude Code". Connect it later: Claude Code, Codex, and Cursor all read a skills folder (Section 1, reading 03 lists where).
- Analogy: a standup round. Short, one line each, no speeches.
- Point at the four chips; read three or four answers aloud.
- Ask: "Anyone running an agent without a human reviewing the diff?" Expected: few or none. Say: tonight shows why review alone is not enough either.
- Likely question: "Will the slides be shared?" Answer: yes, with the repository; the slide source lives under `slides/`.
- Misconception: "this is only for teams with their own agent framework". Correction: Sections 1 to 4 each end with a step you can apply on Monday with an off-the-shelf agent.
- Time: 30 seconds while answers come in. Next: how the class is structured.

## Slide 4: Structure of Class: Four hours, four layers
**Block:** Housekeeping  **Time:** 0.5  **Diagram:** none
**On the slide:**
Structure of Class
- Live class - 4 hr: four sections, two 5-min breaks, a final A/B
- Live demos - every demo is a real model run
- Assignments - four, one per section
- Review session - 2 hr, one slot per assignment
**Visual:** Template slide 4 layout: each line with a bold coloured lead (teal for the first, white for the rest) and white detail; the pacing picture at the bottom.
**Speaker notes:**
- Each section runs the same way: a poll, a live launch, the ideas while the run works, then the finished run on the console, then what we measured.
- Concrete: Section 1 launches `make show-1` at about minute 13 of the class and we read its result around minute 38.
- Assignments: one per section, each with a reference solution and a walkthrough in the section's `assignment/solution/` folder.
- Review session: two hours, about 25 minutes per assignment, then 20 minutes of open questions (instructor guide, "After class").
- Analogy: a sprint with a live demo every 50 minutes; the review session is the retro.
- Point at "every demo is a real model run": the agent's wording, timings, and even the verdict can differ from what we captured before class.
- Ask: "If tonight's run fails, is that a broken demo?" Expected answer: no, a result. We show it either way.
- Likely question: "Is the class recorded?" Answer: yes; the captured runs are also in each section's `demo/expected/` folder.
- Misconception: "live demos are rehearsed recordings". Correction: every launch makes real model calls under a $2.50 session cap; a replay is used only after a failure outside the experiment, and every replay screen shows a red RECORDING badge.
- Time: 30 seconds. Next: a one-picture recap of the agent loop.

## Slide 5: Recap: The Anatomy of an Agentic Loop (build 1/3)
**Block:** Recap  **Time:** 0.25  **Diagram:** docs/diagrams/agent-loop-step-1.png
**On the slide:**
Recap: The Anatomy of an Agentic Loop
**Visual:** Build frame 1 of `agent-loop`: the ticket (prompt) goes to the agent, and the agent calls the model. Nothing else on the slide.
**Speaker notes:**
- Plain explanation: an agent is a loop. It sends the conversation to the model and gets back either text or a tool call.
- Concrete: in tonight's runs the model is gpt-6-luna and the prompt is a TeamTrack ticket such as "Add org-wide issue search: GET /issues".
- Analogy: a junior engineer who can only see what is on their desk; the model is their head, the ticket is the note on the desk.
- Point at the arrow from agent to model: everything the model knows on a turn travels along this arrow.
- Ask: "Where does the agent learn the team's rules in this picture?" Expected: nowhere yet; only the ticket is in context. That is Section 1's problem.
- Likely question: "Is the model stateful between turns?" Answer: no; the loop re-sends the history every turn, which is why context size matters.
- Misconception: "the agent reads the whole repository at the start". Correction: it reads only what it chooses to open, one tool call at a time.
- Time: 15 seconds. Next build: tools.

## Slide 6: Recap: The Anatomy of an Agentic Loop (build 2/3)
**Block:** Recap  **Time:** 0.25  **Diagram:** docs/diagrams/agent-loop-step-2.png
**On the slide:**
Recap: The Anatomy of an Agentic Loop
**Visual:** Build frame 2: the same picture plus the tools box (read a file, patch, run a command) and the "execute tool, return result" arrows back to the agent.
**Speaker notes:**
- Plain explanation: when the model asks for a tool, the agent runs it and appends the result to the history; then it asks the model again.
- Concrete: in Section 1's captured run the agent's early tool calls read `ARCHITECTURE.md` and the `add-endpoint` skill, then patched the issues service and route.
- Analogy: the junior engineer can walk to the file cabinet, but only one drawer at a time, and only if they think to.
- Point at the tools box: every harness layer tonight touches this box or the arrows around it.
- Ask: "If a rule lives in a file the agent never opens, does the rule exist for this run?" Expected: no.
- Likely question: "Do tools run on my machine?" Answer: in this course every tool command runs in a container with no network (Section 3).
- Misconception: "more tools always help". Correction: each tool call costs a turn and context; tonight's runs have turn and cost caps.
- Time: 15 seconds. Next build: when the loop stops.

## Slide 7: Recap: The Anatomy of an Agentic Loop (build 3/3)
**Block:** Recap  **Time:** 0.25  **Diagram:** docs/diagrams/agent-loop.png
**On the slide:**
Recap: The Anatomy of an Agentic Loop
**Visual:** The full `agent-loop` diagram: prompt, agent, model, tools, and the exit arrow to "result" when the model stops calling tools.
**Speaker notes:**
- Plain explanation: the loop ends when the model stops asking for tools, says it is done, or hits a limit (turns, cost, time).
- Concrete: Section 1's captured run ended after 35 turns, 3 min 53 s after launch (evidence page, Section 1 captures).
- Analogy: the junior engineer says "done" and walks away. Nobody has checked the work yet.
- Point at the result box: tonight, "done" is a claim. A separate program, the referee, checks what actually shipped.
- Ask: "Who decides the work is finished in this picture?" Expected: the model itself. That is Section 4's problem.
- Likely question: "What stops a run that never ends?" Answer: the agent time limit (420 s per arm in the class profile) and a cost cap per arm.
- Misconception: "the loop is the harness". Correction: the loop is the engine; the harness is everything around it, which we build tonight.
- Time: 15 seconds. Next: tonight's agenda.

## Slide 8: Today's Agenda
**Block:** Agenda  **Time:** 0.5  **Diagram:** none
**On the slide:**
Today's Agenda
1 Instructions: what the agent knows
2 State and session lifecycle: what it remembers
3 Scope and sandbox: what it may change
4 Verification: what proves it is done
Final A/B and all results
**Visual:** Template slide 13: native numbered boxes 1 to 4 joined by connectors, a "Break" marker after box 1 and after box 3, and a fifth box "Final A/B and all results". No box highlighted yet.
**Speaker notes:**
- Four sections, one layer each, 50 minutes each; a 5-minute break after Section 1 and another after Section 3; 20 minutes of final results at the end.
- Each layer answers one question about the agent: what it knows, what it remembers, what it may change, what proves it is done.
- Concrete: each section has its own TeamTrack ticket: F1 search (Section 1), F2 comments (Section 2), F3 and F4 (Section 3), F4 again (Section 4), F5 to F7 for the final.
- Analogy: onboarding a new engineer. Docs (what they know), a handover note (what they remember), access rights (what they may change), code review and CI (what proves it is done).
- Point at box 3: it is the one section where the measure showed a gap before class, on one ticket (F4), so it runs a live A/B.
- Ask: "Which of the four would you build first in your team?" Expected: most say instructions. Note it; we revisit after the results.
- Likely question: "Do the layers stack?" Answer: yes. Each section's harness arm has the layers so far; Section 3's arm has instructions, state, and scope.
- Misconception: "the order of the four is arbitrary". Correction: it follows one session: what the agent sees at the start (1), what survives a stop (2), what it may touch while working (3), what happens when it claims done (4).
- Time: 30 seconds. Next: what we are building.

## Slide 9: Problem statement: What are we building?
**Block:** Problem  **Time:** 0.5  **Diagram:** docs/diagrams/harness-around-loop.png
**On the slide:**
Tonight we build the harness around a coding agent: the files and code that decide what it sees, remembers, may change, and must prove, on TeamTrack, a small multi-tenant issue tracker.
**Visual:** The full `harness-around-loop` diagram: the agent loop in the middle, four layers around it (instructions, state, scope and sandbox, verification), the referee outside. "TeamTrack" in the accent colour in the framing line.
**Speaker notes:**
- Plain explanation: we do not change the model. We change its environment: what is in its context, what survives a session stop, which files it may touch, and what counts as done.
- OpenAI's harness team describes the job as to "design environments, specify intent, and build feedback loops". That sentence is where the course's word "harness" comes from.
- Concrete: the app is TeamTrack, a FastAPI issue tracker where each customer is an org. The agent adds real features to it.
- Analogy: you would not hand a new hire production access, no docs, and no CI, then judge them on their own report. The harness is the docs, the access rules, and the CI.
- Point at the referee outside the harness: it is not part of what the agent gets. It scores what shipped, the same way for both arms.
- Ask: "Why keep the referee outside the harness?" Expected: so the harness cannot grade itself; the score must not depend on the thing being measured.
- Likely question: "Is shipharness tied to one agent product?" Answer: no; it runs its own loop on the OpenAI API, and the starter kit copies the same files into your repository for Claude Code, Codex, or Cursor.
- Misconception: "the harness makes the agent smarter". Correction: it changes what the agent sees and may do; whether that changes the outcome is what we measure.
- Time: 30 seconds. Next: what goes wrong without it.

## Slide 10: Problem statement: The problem in the real world
**Block:** Problem  **Time:** 1  **Diagram:** none
**On the slide:**
Your team gives a week of tickets on a multi-tenant issue tracker to a coding agent.
The problem we're solving (in the real world)
- Monday: the agent copies an old handler that has no tenant filter. The tests pass, and one customer can now read another customer's issues.
- Tuesday: a session stops halfway through a database migration. The next session cannot see it and writes a second migration for the same table.
- Wednesday: a fix for one endpoint lands in shared middleware, and an older feature breaks.
- Thursday: the agent reports "done" on an edit-conflict feature that still loses updates. The only evidence is its word.
Each failure costs more than the ticket saved.
**Visual:** Template slide 16 layout: the bold framing sentence at the top, the orange subheading "The problem we're solving (in the real world)", four day-labelled bullets with the day in bold, and the closing line in bold. No picture.
**Speaker notes:**
- This is the root README's story, one ticket a day. It is an illustrative scenario, not an incident from our runs; say so.
- Monday is a tenant leak: a data exposure, an incident, a disclosure, and a hunt for every copy of the pattern.
- Tuesday is a lost session: two Alembic heads, so the deploy is blocked until someone merges them by hand.
- Wednesday is scope creep: the ticket was one endpoint, the diff touched middleware every request runs through.
- Thursday is a false "done": the review rests on trust in the agent's own report.
- Concrete tie-in: each failure maps to one section tonight. Monday is Section 1, Tuesday Section 2, Wednesday Section 3, Thursday Section 4.
- Analogy: this is the week of a capable contractor with no onboarding docs, no handover notes, admin access everywhere, and who marks their own tickets as done.
- Point at "The tests pass" in Monday: the tests created one org, so a missing org filter was invisible to them.
- Ask: "Which of the four have you seen in your own team?" Expected: Wednesday and Thursday most often. Take one story, 20 seconds.
- Likely question: "Are these four failures from real incidents?" Answer: the week is illustrative; the mechanisms are not. TeamTrack really has an unfiltered legacy handler, and in Section 3 every bare arm on F4 really edited a shared module.
- Misconception: "better tests would catch all four". Correction: Monday's tests passed because they created one org; Thursday's suite stayed green because the new header is optional. Tests check what their author thought of.
- Time: 1 minute. Next: why a capable agent still does this.

## Slide 11: The challenge is: The rules exist, the agent still misses
**Block:** Problem  **Time:** 0.5  **Diagram:** none
**On the slide:**
The challenge is: the rules, tests, and code are all in the repository, but the agent still fails because:
- A rule it never reads does not exist for it
- Each session starts with no memory
- It copies whatever pattern sits nearby
- It grades its own work too kindly
**Visual:** Template slide 16's second half on its own: the framing sentence in bold with "The challenge is:" in orange, then four cause bullets, each with a small icon (closed book, blank page, copy icon, self-awarded tick).
**Speaker notes:**
- Each cause has a source. Cause 1, OpenAI: "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."
- Cause 2, Anthropic: "each new session begins with no memory of what came before."
- Cause 3, OpenAI: "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." Anthropic also runs its long agent loop with the note "(Run this in a container, not your actual machine)".
- Cause 4, Anthropic: "agents reliably skew positive when grading their own work".
- Concrete: TeamTrack has a legacy `GET /v1/issues` handler with no org filter, next to where F1's query must go. That is cause 3 in one file.
- Analogy: a drive-by open-source contributor: CONTRIBUTING.md exists, they skim the nearest file instead, copy its style, and mark their own PR "tested".
- Point at the word "still": nothing is withheld. The bare arm gets every rule in `docs/HANDBOOK.md`.
- Ask: "If the rule is in the repository, why is that not enough?" Expected: being on disk is not being in context; the agent must choose to open it.
- Misconception: "a stronger model fixes all four". Correction: a stronger model may need fewer layers, which is why we measure each layer on the model we use.
- Likely question: "Why quote vendor engineering blogs?" Answer: these teams ran long agent loops on real code and wrote down the failures; Section 4 adds the papers (TestGen-LLM, ACH, SpecBench). Each quote was checked against its source.
- Time: 30 seconds. Next: why this matters to a team, not just to one ticket.

## Slide 12: Why this matters for Engineering Teams
**Block:** Problem  **Time:** 0.5  **Diagram:** none
**On the slide:**
Why this matters for Engineering Teams
Each failure has a cost:
- Tenant leak: incident, disclosure, pattern hunt
- Lost session: two migration heads, blocked deploy
- Scope creep: regression in an older feature
- False "done": review rests on trust
A harness costs too: turns, time, money
**Visual:** Template slide 17 style as a native three-column table: failure, what the team pays, which section addresses it. The last line sits in a strip at the bottom in orange.
**Speaker notes:**
- Plain explanation: each failure costs more than the agent saved on the ticket. One missing org filter turns a small ticket into a disclosure plus an audit of every copy of the pattern.
- Concrete cost of a harness, from the runs before class: harness arms ran longer, median 302 s against 190 s, and cost more, median $0.0123 against $0.0103 per arm (evidence, exploratory analysis; chosen after the results, so descriptive).
- So the trade is real: every layer must buy something you can see, or it is overhead.
- Anthropic's harness team: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing".
- Analogy: CI minutes. A slow pipeline is fine if it catches regressions; a slow pipeline that never fails is waste.
- Point at the bottom strip: this is why the course measures instead of recommending.
- Ask: "How would you know a harness layer is not paying off?" Expected: run the same ticket with and without it and compare a measure chosen in advance.
- Likely question: "Are those cost numbers per run or per class?" Answer: per arm run; the whole class plan needs at most $2.36 at the caps, under a $2.50 session cap.
- Misconception: "a harness is free once written". Correction: it costs turns and wall time on every run; post hoc, harness arms hit the agent time limit in 9 of 34 runs, bare arms in 4 of 34.
- Time: 30 seconds. Next: the four gaps, in one picture.

## Slide 13: Why We Need a Harness: The 4 Critical Gaps
**Block:** Problem  **Time:** 0.5  **Diagram:** docs/diagrams/stories-causes-layers.png
**On the slide:**
Why We Need a Harness: The 4 Critical Gaps
**Visual:** The `stories-causes-layers` diagram, three columns read left to right: four stories (Monday to Thursday), four causes, four layers (instructions, state, scope and sandbox, verification). One row per gap.
**Speaker notes:**
- Read the diagram row by row, left to right: story, cause, layer.
- Row 1: tenant leak, rule not in context, instructions layer (Section 1): a short map in context, details on disk.
- Row 2: lost migration, no memory across sessions, state layer (Section 2): a progress file, a plan, and a handoff.
- Row 3: middleware edit, copied patterns and hard-to-undo actions, scope and sandbox layer (Section 3): allowed paths per phase, a container with no network.
- Row 4: false "done", self-grading, verification layer (Section 4): test filters and a gate; the harness, not the agent, marks a feature as passing.
- Analogy: onboarding docs, shift handover, least privilege, and CI gates. Each is a practice your team already trusts for humans.
- Point at the arrows between columns: each layer targets one cause, not one story; the same cause can produce other stories.
- Ask: "Which row do you expect to show the biggest difference in our measurements?" Expected: guesses vary. Answer at the end of the night: only row 3 did, on one ticket.
- Misconception: "one layer fixes several gaps". Correction: each layer here was built for one cause; Section 3 also shows a guard can win by construction, which is not the same as being correct.
- Likely question: "Where is the sandbox in this picture?" Answer: in row 3, but it is the same container for both arms, so no measurement can credit it; only the scope guard differs between arms.
- Time: 30 seconds. Next: the app the agent works on.

## Slide 14: TeamTrack: The data model
**Block:** Problem  **Time:** 0.5  **Diagram:** docs/diagrams/teamtrack-data-model.png
**On the slide:**
TeamTrack: The data model
Every tenant-owned row carries org_id
Two demo orgs: Acme and Globex
**Visual:** The `teamtrack-data-model` diagram: orgs, users, projects, project_members, issues, audit_log, idempotency_keys, with `org_id` highlighted on every tenant-owned table.
**Speaker notes:**
- Seven tables, from `platform/teamtrack/app/db/models.py`. Its docstring is the slide's first line: "Every tenant-owned row carries org_id."
- Issues carry `org_id`, `project_id`, status (open, in_progress, done), priority, an assignee, a `version` column (used by F4), and `deleted_at` for soft deletes.
- Users have a role: admin, member, or viewer. Projects can be archived. Every write adds one row to `audit_log` (house rule R5).
- Concrete: the seed creates Acme and Globex with an admin, a member, and a viewer each, for example `admin@acme.test`.
- House rule R1, tenant isolation: another org's resource answers 404, never 403, because 403 tells the caller it exists.
- Analogy: row-level security done in application code. Every query must say `WHERE org_id = caller's org`, and one missing clause is a leak.
- Point at `org_id` on issues: the referee's R1 check calls every endpoint as an Acme user with Globex ids and expects 404.
- Ask: "Why is a missing org filter invisible to most unit tests?" Expected: the tests create one org, so every row belongs to the caller anyway.
- Likely question: "Is there real auth?" Answer: a demo token from `POST /auth/login`, for local use only; the point is the tenant rule, not authentication.
- Misconception: "tenant isolation is the database's job". Correction: SQLite has no row-level security; every repository function takes `org_id`, and the referee's R1 probes check the result from outside.
- Time: 30 seconds. Next: the stack.

## Slide 15: Key Tech Stack: TeamTrack and shipharness
**Block:** Problem  **Time:** 0.25  **Diagram:** none
**On the slide:**
Key Tech Stack: TeamTrack and shipharness
TeamTrack, the app the agent changes:
- FastAPI, SQLAlchemy, Alembic, SQLite
- Jinja2 and HTMX web board
- pytest, import-linter
shipharness, the harness and referee:
- Python 3.12 and uv
- Docker sandbox with no network
- OpenAI models, LangSmith traces
- Live console on port 8765
**Visual:** Template slide 20 style, built natively: two columns of logo chips, TeamTrack on the left, shipharness on the right, an arrow from shipharness to TeamTrack labelled "runs the agent on".
**Speaker notes:**
- TeamTrack: a FastAPI app, SQLAlchemy models, Alembic migrations, SQLite by default (`sqlite:///./teamtrack.db` in `app/settings.py`), and a small board under `/board` in Jinja2 and HTMX.
- Tests use pytest; layering (house rule R6: `app/api` never imports `app/db`) is checked by import-linter.
- shipharness is the course's command-line tool: it runs an agent with or without the harness, runs A/Bs, judges them, and serves the console.
- Models: gpt-6-luna for the agent, gpt-5.6-luna for the blinded reviewer, the same settings for both arms.
- Every agent tool command and the referee run in Docker containers with no network and the same limits for both arms.
- LangSmith keeps a trace of every model call; screen 5 of the console links to it. Ordinary traces are kept 14 days, so copy links you need.
- Analogy: TeamTrack is the service under test; shipharness is the test rig plus the CI dashboard.
- Ask: "Why does the referee run in its own container?" Expected: so an arm cannot change what judges it; fresh state for every judgement.
- Likely question: "Can I swap the model?" Answer: yes, through settings; the course's results hold only for this model, which is the point of measuring.
- Point at the arrow "runs the agent on": the loop and the keys stay on the host; only tool commands enter the container.
- Misconception: "SQLite makes these toy results". Correction: what is measured (files outside the ticket, Alembic heads, org filters, done claims) does not depend on the database engine.
- Time: 15 seconds. Next: the tickets.

## Slide 16: Example Tickets: F1 to F7 in plain words
**Block:** Problem  **Time:** 0.25  **Diagram:** none
**On the slide:**
Example Tickets
- F1 Search every issue in my org
- F2 Comment on an issue
- F3 Retried creates never duplicate
- F4 Second save refused, plus history
- F5 Close a sprint's issues at once
- F6 Watch issues I care about
- F7 Tag issues with labels
**Visual:** Template slide 21 style: seven ticket cards in a grid, each with the feature id, the plain-words line, and a small tag for where it runs (S1, S2, S3, S3 and S4, Final). F5 to F7 carry a "poll" tag.
**Speaker notes:**
- Each ticket is one example in the dataset `teamtrack-features-v1` (`platform/datasets/`), written like a work ticket, with hidden tests behind it.
- F1 org-wide issue search, `GET /issues` with filters and cursor pagination: Section 1.
- F2 comments on issues, built over two sessions: Section 2. F3 idempotency keys on issue creation: Section 3.
- F4 optimistic concurrency (ETag, If-Match) and issue history: the Section 3 live A/B and Section 4.
- F5 bulk close, F6 watchers, F7 labels: the final. The room votes in Section 4; the winner runs first.
- Concrete trap: most tickets come in a "trap" variant. Legacy-pattern traps (F1, F2, F5, F6) point at the unfiltered `GET /v1/issues`; tempting-middleware traps (F3, F4, F7) point at `app/api/middleware.py`.
- Analogy: realistic tickets from a backlog, including the kind a well-meaning ticket writer makes worse by saying "the code already exists over there".
- Ask: "Which ticket is riskiest for tenant isolation?" Expected: F1, because it reads across every project of an org.
- Likely question: "Are traps fair to the bare arm?" Answer: yes; both arms get the same ticket text, and the trap is a task-design choice present in both.
- Point at the "S3 and S4" tag on F4: the only ticket used twice, once for scope and once for verification.
- Misconception: "F5 to F7 were measured before class like F1 to F4". Correction: they were not part of the registered test runs; the final has no primary measure and is read as counts.
- Time: 15 seconds. Next: how we score a run.

## Slide 17: How We'll Measure: Same ticket, two arms (build 1/2)
**Block:** Problem  **Time:** 0.5  **Diagram:** docs/diagrams/ab-referee-step-1.png
**On the slide:**
How We'll Measure
Same agent, model, ticket, tools, budgets, sandbox:
- Bare arm: ticket and repository only
- Harness arm: the same, plus the layers
**Visual:** Build frame 1 of `ab-referee`: one ticket splitting into two arms, each in an identical sandbox box. The referee is not drawn yet.
**Speaker notes:**
- Plain explanation: an A/B is two runs of the same ticket, one without the harness (bare arm) and one with it (harness arm). Everything else is held equal.
- Held equal: agent, model, effort, ticket, repository, tools, sandbox limits, turn limit, and cost cap.
- Fairness rule from Section 1: the harness may reorganise knowledge, never add facts. The bare arm has every rule in `docs/HANDBOOK.md`, and a unit test checks that both forms carry each rule.
- Concrete: tonight Sections 1, 2, and 4 run the harness arm alone, live (`make show-N`), because the A/Bs before class showed no gap. Section 3 and the final run both arms live.
- Analogy: a controlled experiment, or a feature flag with a holdout group; you change one thing and keep the rest fixed.
- Point at the two sandbox boxes: identical limits; the sandbox is never the variable.
- Ask: "What would make the comparison unfair?" Expected: different budgets, a different model, or the harness smuggling in a fact the bare arm cannot read.
- Likely question: "Does a section's A/B test that one layer?" Answer: it tests the harness so far against bare. Only removing one piece at a time would isolate a layer; the course did not run that ablation.
- Misconception: "the bare arm is a strawman with no rules". Correction: it gets the same ticket and repository, including the 150-line handbook with every house rule.
- Time: 30 seconds. Next build: who scores.

## Slide 18: How We'll Measure: One referee scores both (build 2/2)
**Block:** Problem  **Time:** 0.5  **Diagram:** docs/diagrams/ab-referee.png
**On the slide:**
How We'll Measure
Same agent, model, ticket, tools, budgets, sandbox:
- Bare arm: ticket and repository only
- Harness arm: the same, plus the layers
The referee scores what shipped:
- One primary measure, chosen before any run
- Hidden tests, tenant probes, mutants, reviewer
- Results as counts per arm, never percentages
**Visual:** The full `ab-referee` diagram: both arms feed one referee in a fresh container, which writes the primary verdict first, then the full verdict, to the console.
**Speaker notes:**
- The referee runs after the agent stops, in a fresh container with no network, with checks the agent never sees.
- Primary measure: one question per section, registered before any run. Section 1's: did the change add at least one new R1 (tenant) violation?
- Other checks: hidden tests per ticket, R1 probes (an Acme user asks for Globex ids and expects 404), referee mutants the agent's tests should kill, and a blinded reviewer.
- Console: the primary verdict appears as soon as its check finishes; the full verdict follows. In Section 1's captured run: primary at 4 min 11 s, full at 10 min.
- Results are counts: "0 of 3", never a percentage. With one to seven runs per arm, a percentage hides how few runs there are.
- Before class: rounds at medium effort, low effort, and class settings. Where both arms pass equally often, we say "no measurable difference" plainly.
- Analogy: CI with a hidden test suite the developer cannot see, plus a code reviewer who does not know which arm wrote the diff.
- Ask: "Why choose the primary measure before running?" Expected: so we cannot pick, afterwards, whichever number makes the harness look good.
- Misconception: "one passing run proves the layer works". Correction: one run is one dot; it shows the layer ran, not that it helped.
- Point at the referee box outside both sandboxes: it starts after the agent stops, from a fresh copy plus each arm's diff.
- Likely question: "Is the blinded reviewer part of the verdict?" Answer: no; its accept or reject is a secondary measure, shown next to the primary verdict, never instead of it.
- Time: 30 seconds. Next: check the machine and open the console.

## Slide 19: Let's Get It Started
**Block:** Problem  **Time:** 2  **Diagram:** none
**On the slide:**
Let's Get It Started
- make doctor → result: + ready
- make console → http://127.0.0.1:8765
- Keys 1 to 5: Live, Boards, Evidence, A/B Report, Traces
**Visual:** Template slide 22 divider: the title as one large line, the three commands under it in a monospace card. Switch to terminal B and the console tab while this slide is up.
**Speaker notes:**
- Terminal B (class minute 0:08): run `make doctor`. Read the key lines aloud: both say `accepted by OpenAI` and `accepted by LangSmith`, and the last line is `result: + ready`. It never prints any part of a key.
- The console has been running in terminal A since T-30 (`make console`, `Console: http://127.0.0.1:8765/`). Switch to browser tab 2.
- Console tour: press `1` Live (turns, cost, harness decisions, verdict), `2` Boards (each arm's board as an Acme user), `3` Evidence (files read, diff map, sandbox denials, referee checks), `4` A/B Report (one dot per run), `5` Traces (event tail, LangSmith links). `F` shows one arm full width.
- Then the assessment printout prepared before class (`assess.py` on the bare TeamTrack). Say: "This is what the bare arm works with: no map, no progress file, no feature list. The rules themselves are in both arms."
- `make warm` ran before class; with nothing changed it takes about a second, so the first launch does not pay for image start-up.
- If `make doctor` says `SHIPHARNESS_CLASS_DATE is not set`: repeat the date step from the instructor guide, then rerun. If a key line says `invalid`: fix `.env` and rerun.
- If Docker is not running: `sudo systemctl start docker`, then `make doctor` again.
- Analogy: the pre-flight checklist. Nothing takes off until every line is green.
- Ask: "Following along at home: who has `result: + ready`?" Expected: some; point the rest to `setup/README.md` and `docs/troubleshooting.md` after class.
- Time: 2 minutes, ends at class minute 0:10. Next: Section 1.

## Slide 20: Section 1: What the agent knows
**Block:** Section 1  **Time:** 0.5  **Diagram:** none
**On the slide:**
Today's Agenda
1 Instructions: what the agent knows
2 State and session lifecycle: what it remembers
3 Scope and sandbox: what it may change
4 Verification: what proves it is done
Final A/B and all results
**Visual:** The agenda slide again (template slide 34), with box 1 highlighted and a star next to it; boxes 2 to 4 and the final dimmed.
**Speaker notes:**
- Section 1, class minutes 0:10 to 1:00. The layer: instructions, meaning what is in the agent's context and what it can find on disk.
- The ticket: F1, org-wide issue search, `GET /issues`, next to a legacy handler with no tenant filter.
- The one question the referee asks: did the change add a new tenant leak (a new R1 violation)?
- Plan for the 50 minutes: poll and launch, the failure story, four ideas while the run works, then the finished run, then what we measured.
- Concrete outcome for you: by the end you can turn a long instruction file into a short map, focused docs, and a skill.
- Analogy: a service's runbook index: it does not hold every procedure; it says which runbook to open for which alert.
- Ask: "How long is the agent instruction file in your main repository?" Expected: answers from 20 to several hundred lines. Remember the longest; it comes back in idea 1.
- Likely question: "Is this specific to AGENTS.md?" Answer: no; CLAUDE.md, Cursor rules, and Copilot instructions play the same role.
- Point at box 1 and its star; each dimmed box adds one more layer to the harness arm.
- Misconception: "Section 1 is prompt engineering". Correction: the ticket text is identical in both arms; the layer changes which files exist and what is sent before the ticket.
- Time: 30 seconds. Next: the poll, then the launch.

## Slide 21: Live Zoom Poll: Will the agent copy the legacy query?
**Block:** Section 1  **Time:** 4.5  **Diagram:** none
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 2 minutes to fill out the form.
Then, in terminal B: make show-1
**Visual:** Template slide 56: the heading "Live Zoom Poll", the instruction sentence, the poll picture; the launch line in a monospace chip at the bottom. The poll question is in Zoom, not on the slide.
**Speaker notes:**
- Poll question (in Zoom): "Before class, 7 bare-arm runs took this ticket, with the legacy handler in the repository. How many shipped a new tenant leak? A) 0-1, B) 2-3, C) 4-5, D) 6-7." Close the poll before the launch; do not reveal the answer (it is A, 0 of 7) until the results slide.
- Exact launch, terminal B, at class minute 0:13: `make show-1`. It runs `shipharness ab --section demo-1 --feature F1 --arms harness --purpose class --profile class`.
- This is "harness in action": the harness arm alone, live, not an A/B. The A/Bs before class showed no gap on F1, so class shows the layer at work.
- Console: reload the run list, open the newest run, press `1`. Look for the badge "HARNESS IN ACTION" and the note "placed 31 instruction files".
- What to say while it starts: "Watch which documents the agent opens before it writes code. The map is in its context; everything else it must choose to open."
- Expected timings from the captured run before class (agent limit then 300 s, now 420 s): primary verdict about 4 min 11 s after launch, full verdict about 10 min, cost $0.0197 against a cap of $0.24.
- If it fails: `x OpenAI refused the key` means fix `OPENAI_API_KEY` and rerun `make doctor`. Arm `ERROR` with `docker run failed`: `sudo systemctl start docker`, then `make warm`. `ABORTED: timeout` or `ABORTED: cap` is a result: keep it and read the verdict.
- Fallback: only for a failure outside the experiment (Docker, network, OpenAI account), run `make replay RUN=<fallback id>`; every screen shows a red RECORDING badge. If Docker is down, walk the captured run in `section-1-instructions/demo/expected/` (screenshots plus `terminal.txt`).
- Analogy: kicking off a long CI job before the meeting so the result is ready when you need it.
- Time: minutes 0-3 poll, 3-5 launch. Next: the story behind the ticket.

## Slide 22: Failure story: The search that showed another org
**Block:** Section 1  **Time:** 3  **Diagram:** none
**On the slide:**
Failure story: The search that showed another org
- Ticket: org-wide issue search, GET /issues
- Agent finds list_all_legacy next door
- Copies it: short, already paginates
- Tests create one org, so they pass
- Review approves: looks like the file
- After release: Acme sees Globex issues
**Visual:** A native six-step horizontal strip, one box per bullet, the last box in red with a lock icon broken open. Under step 2, a small code chip: `select(Issue).order_by(Issue.id)` with "no org_id" in red.
**Speaker notes:**
- Illustrative scenario from the section's concepts page: Priya's team asks a coding agent for `GET /issues`. The tenant rule lives in the team handbook, which the ticket does not mention.
- The agent lists the repository, opens the issues code, and finds `list_all_legacy`, a query from an old endpoint that lists every issue of every org.
- The real function in TeamTrack, `app/repositories/issues.py`: its docstring says "LEGACY (used only by /v1/issues). Not tenant-scoped: do not use or copy this function." The query is `select(Issue).order_by(Issue.id).offset(offset).limit(limit)`.
- The tests create one org, so every row belongs to the caller; they pass. The reviewer sees code shaped like the rest of the file.
- Cost: a cross-tenant data exposure, an incident, a disclosure, and a hunt for every other copy of the pattern.
- Nobody broke a rule on purpose. The rule was on disk, not in front of the agent when it wrote the query.
- Analogy: a new hire copies the oldest working example in the codebase because nobody told them it is deprecated.
- Point at the code chip: the line that is missing is `where(Issue.org_id == actor.org_id)`.
- Ask: "Which review comment would have caught this?" Expected: "where is the org filter?", and only if the reviewer knows the rule and reads for it.
- Honesty note: no run before class shipped this leak; say so now, and say we come back to it on the results slide.
- Likely question: "Is Priya's team real?" Answer: no, it is the concepts page's illustrative scenario; the legacy function and its docstring are real TeamTrack code.
- Misconception: "the agent was careless". Correction: it picked the shortest working example next to the target file; without the rule in context that is a reasonable choice, so the fix is context, not scolding.
- Time: 3 minutes. Next: the obvious fix, and why it is not one.

## Slide 23: Instructions: Why not paste every rule? (build 1/3)
**Block:** Section 1  **Time:** 1  **Diagram:** none
**On the slide:**
What the agent knows
- The tenant rule is in docs/HANDBOOK.md
- Both arms can open it
- Can we paste every rule into the prompt?
**Visual:** Template slide 25 frame: the constant header "What the agent knows" top-left, two bullets in white, the question in a highlighted box at the bottom.
**Speaker notes:**
- Plain framing: the rule exists and nothing is hidden. The bare arm gets every house rule in a 150-line handbook.
- So the question is not whether the rule exists; it is whether it is in front of the agent when it writes the query.
- The obvious fix: put every rule in the prompt, always. Let the room try it before you answer.
- Concrete: TeamTrack's handbook states R1 in full at line 53: every query on customer data filters by the caller's `org_id`; another org's resource is 404.
- Analogy: the "read all of this before you change anything" wiki page every team has, and nobody reads to the end.
- Point at the question box; pause for five seconds.
- Ask: "Can we just paste every rule into the prompt? Shout yes or no." Expected: a split room; most say yes for a small file.
- Likely learner answer: "It is only 150 lines, so yes." Response: fair for 150 lines; hold that thought for a real team's file.
- Misconception: "a bigger context window settles this". Correction: the next build shows that the cost is attention and maintenance, not only tokens.
- Time: 1 minute. Next build: the verdict.

## Slide 24: Instructions: Why not paste every rule? (build 2/3)
**Block:** Section 1  **Time:** 1  **Diagram:** none
**On the slide:**
What the agent knows
- The tenant rule is in docs/HANDBOOK.md
- Both arms can open it
- Can we paste every rule into the prompt? - Why not
**Visual:** The same frame; "- Why not" appears in red bold after the question, as on template slide 26.
**Speaker notes:**
- Verdict first, reasons next: no, not as the main mechanism.
- OpenAI's harness team tried the giant file and moved away from it: "give Codex a map, not a 1,000-page instruction manual."
- Concrete: Assignment 1 starts from a real-shaped example, an 899-line `AGENTS.md` for a TeamTrack variant with 70 tagged rules.
- Analogy: a 900-line PR description. Everyone scrolls; nobody reads the line that matters.
- Point at "Why not" in red; let the room guess reasons for 20 seconds.
- Ask: "What goes wrong with an 899-line file in context on every task?" Expected: cost, buried rules, contradictions, stale rules.
- Likely question: "Does Claude Code not load CLAUDE.md in full anyway?" Answer: yes, it does; that is why the file must stay short and point elsewhere.
- Misconception: "the problem is only token cost". Correction: the bigger problems are rules competing for attention and the file rotting without anyone noticing.
- Time: 1 minute. Next build: the reasons.

## Slide 25: Instructions: Why not paste every rule? (build 3/3)
**Block:** Section 1  **Time:** 2  **Diagram:** none
**On the slide:**
Can we paste every rule into the prompt?
- It crowds out the task and code
  - 899 lines paid on every task
- Too much guidance becomes non-guidance
  - R1 at line 204, legacy warning at 586
- It goes stale; no script checks it
  - Four retired rules still inside
What can we use instead?
**Visual:** Template slide 27 layout: three reason bullets in white, each with one nested example in green; the closing question in the accent colour at the bottom.
**Speaker notes:**
- Reason 1, OpenAI: "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs."
- Reason 2, OpenAI: "Too much guidance becomes non-guidance." In the 899-line file, the tenant rule starts at line 204 and the warning about the legacy endpoint at line 586.
- Reason 3, OpenAI: "It rots instantly. A monolithic manual turns into a graveyard of stale rules." The file still holds four retired rules.
- And: "A single blob doesn't lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable." Idea 4 comes back to this.
- Analogy: one 900-line config file with no schema versus small typed config files with a linter.
- Point at the green examples: these are line numbers in a real file in the repository (`section-1-instructions/assignment/starter/original/AGENTS.md`).
- Ask: "What can we use instead?" Expected: a short index pointing to topic files. That is idea 1.
- Likely question: "Is OpenAI's experience general?" Answer: they say their results should "not be assumed to generalize without similar investment"; tonight we measure the idea on our model.
- Misconception: "just move rule 1 to the top of the big file". Correction: reordering lifts one rule and buries another; it fixes neither staleness nor the missing checks.
- Time: 2 minutes. Next: idea 1, the map.

## Slide 26: 1) A map, not a manual
**Block:** Section 1  **Time:** 3.5  **Diagram:** section-1-instructions/diagrams/manual-vs-map.png
**On the slide:**
1) A map, not a manual
AGENTS.md is a table of contents: about 100 lines, always in context.
TeamTrack's map:
- 94 lines, keyed by "When you are about to"
- Each row names one file
- R1 to R7 at a glance
- "Do not copy" names the legacy handler
**Visual:** The `manual-vs-map` diagram: on the left one tall 899-line file with R1 buried in the middle; on the right a short map with arrows to `docs/SECURITY.md`, `ARCHITECTURE.md`, and the `add-endpoint` skill.
**Speaker notes:**
- Plain explanation: the map does not hold the rules; it says where each rule lives. The full R1 text lives once, in `docs/SECURITY.md`.
- OpenAI: "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere." And: "we treat it as the table of contents."
- The details live in `docs/`, "treated as the system of record". TeamTrack copies OpenAI's layout: `AGENTS.md` and `ARCHITECTURE.md` at the root; `SECURITY.md`, `RELIABILITY.md`, `QUALITY_SCORE.md`, `PLANS.md`, `design-docs/`, `product-specs/`, `references/` in `docs/`.
- Concrete rows from `platform/teamtrack/harness/instructions/AGENTS.md`: "add or change an endpoint" → the add-endpoint skill; "decide who may see or change data" → `docs/SECURITY.md` (R1, R2).
- Keyed by action, not by topic: the agent knows what it is about to do, so that is the lookup key.
- "Do not copy" names `GET /v1/issues`, `repositories.issues.list_all_legacy`, and `services.legacy`, and points to `POST /projects` as the right pattern.
- Analogy: onboarding docs with a "start here" page, versus a wiki dump.
- Point at the right side of the diagram: one hop from the map to the rule.
- Ask: "Why key the table by action instead of by topic?" Expected: the agent knows its next action ("touch a repository"), not which topic it needs.
- Misconception: "a short map means fewer rules". Correction: the same rules, organised; a unit test checks every rule is still in the handbook both arms read.
- Likely question: "Why 94 lines and not 20?" Answer: OpenAI's guide is roughly 100; TeamTrack needs one row per common action, R1 to R7, and the "Do not copy" list. Shorter is fine if every row still names one file.
- Time: 3.5 minutes. Next: how the agent gets the details only when needed.

## Slide 27: 2) Progressive disclosure: skills load in three tiers
**Block:** Section 1  **Time:** 3.5  **Diagram:** section-1-instructions/diagrams/skills-three-tiers.png
**On the slide:**
2) Progressive disclosure: skills load in three tiers
A small entry point first; the details only when the task needs them.
- Tier 1: name and description, every skill, at start
- Tier 2: full SKILL.md, when the agent picks it
- Tier 3: references, scripts, assets, when a step needs them
**Visual:** The `skills-three-tiers` diagram: three stacked bands growing in size, "always in context" on tier 1, "on disk" on tiers 2 and 3, with the `add-endpoint` skill as the example in each band.
**Speaker notes:**
- OpenAI on docs: "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front."
- Agent Skills specification: "The `name` and `description` fields are loaded at startup for all skills"; the instructions "< 5000 tokens recommended"; resources load "only when required".
- Concrete: TeamTrack's skill `add-endpoint`. Tier 1 is its description: "Add or change a TeamTrack HTTP endpoint so it follows house rules R1-R7 ... Use when a ticket adds a route ...". Tier 2 is the 100-line `SKILL.md`. Tier 3 is `references/tests.md`.
- What the runs showed: in one round, every harness arm read the skill body (tier 2), and none read `references/tests.md` (tier 3). Tier 3 stayed on disk, as designed.
- The description does the routing. It must say what the skill does and when to use it ("Should describe both what the skill does and when to use it").
- Analogy: a man page. You see the one-line summary in the index; you open the page when you need it; you follow "SEE ALSO" only for a specific step.
- Point at tier 1: the only part that costs context on every task.
- Ask: "A skill's description says only 'Endpoint helper.' What breaks?" Expected: tier 1; the agent never decides to open it, so tiers 2 and 3 never load.
- Likely question: "Do Claude Code, Codex, and Cursor all do this?" Answer: all three read Agent Skills from a skills folder; post-class reading 03 lists where each one looks.
- Misconception: "skills are plugins with code". Correction: a skill is a folder with a Markdown recipe; scripts are optional tier 3 files.
- Time: 3.5 minutes. Next: how the map reaches the model.

## Slide 28: 3) The context prefix: small, fixed, out of reach
**Block:** Section 1  **Time:** 3.5  **Diagram:** section-1-instructions/diagrams/context-prefix.png
**On the slide:**
3) The context prefix: small, fixed, out of reach
Sent first in every session:
- A one-line usage note
- The whole map
- The skills catalogue, one line each
Built once, from the course's copy:
- Agent edits to AGENTS.md change nothing
- Bare arm: core prompt only
**Visual:** The `context-prefix` diagram: the first message of a session as a stack (core system prompt, then the prefix: sentence, map, catalogue), with docs and skill bodies drawn outside the stack, on disk, reached by `read_file`.
**Speaker notes:**
- Plain explanation: the prefix is what the harness arm sees before the ticket, in every session. Only the map and the catalogue go in; documents and skill bodies stay on disk.
- Concrete: the map file has 94 lines; the agent gets 92, because two walkthrough comment lines are stripped.
- The runner joins the core system prompt and the prefix into the first message of every session (`platform/src/shipharness/runner/loop.py`). The bare arm gets the same core prompt, without the prefix.
- Built from the course's copy (`platform/teamtrack/harness/instructions/`), never from the arm's workspace. An agent that edits its own `AGENTS.md` changes a file, not what it is told.
- Built once and reused: every session of the run gets the same text, OpenAI's "small, stable entry point".
- The term "context prefix" is the course's design, not a source's term; it is where the course puts OpenAI's "injected into context".
- Analogy: least privilege for instructions. The agent can read its orders but cannot rewrite them.
- Point at the docs drawn outside the stack: the agent must choose to open them, and the harness logs when it does.
- Ask: "Why does a fixed prefix matter for a run with two sessions?" Expected: session 2 gets the same orders as session 1, whatever the agent changed on disk.
- Likely question: "Does the prefix block anything?" Answer: no. This layer only informs; Sections 3 and 4 add limits and checks that block.
- Misconception: "the agent sees the docs because they are in the repository". Correction: only the map and the catalogue are sent; screen 3 later shows which docs it actually opened.
- Time: 3.5 minutes. Next: how to keep the map true over time.

## Slide 29: 4) Mechanical checks keep the map true
**Block:** Section 1  **Time:** 3.5  **Diagram:** none
**On the slide:**
4) Mechanical checks keep the map true
One big file can't be checked by a script. A map and focused docs can:
- Every link in the map resolves
- Every active rule lives in exactly one doc
- Retired rules never come back
- Skill frontmatter passes the validator
**Visual:** A native three-box flow: "map + docs + skill" → "checker" → a terminal chip showing `OK: 13 files, 147 links, 66 rules covered` in green, with an alternative red chip `ERROR: broken link` below it.
**Speaker notes:**
- OpenAI: "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly."
- And on error messages: "we write the error messages to inject remediation instructions into agent context." A lint message that says how to fix the problem teaches the agent too.
- Concrete: Assignment 1 asks you to write `checker/check_docs.py`. The reference checker on the reference tree prints `OK: 13 files, 147 links, 66 rules covered`.
- Skill check: `uv run shipharness skills validate platform/teamtrack/harness/instructions/.agents/skills` validates the frontmatter (name matches the folder, description present, no extra fields).
- Fairness check in this course: `platform/tests/unit/harness_instructions/test_parity.py` fails if a rule or convention in the harness docs is missing from the handbook both arms read. "Reorganise, never add."
- Analogy: CI gates for documentation. A broken link fails the build the same way a broken import does.
- Point at the red chip: the check fails loudly at commit time, not months later when an agent follows a dead link.
- Ask: "Your map points to `docs/SECURITY.md` and someone renames it. What happens without a check?" Expected: the agent follows a dead pointer and falls back to whatever code is nearby.
- Instructor cue: this is about section minute 25. Glance at terminal B for the `Cost:` line of `make show-1`; if it is still running, continue and open the demo on the live screens.
- Likely question: "Who fixes a failing doc check?" Answer: whoever renamed or moved the file, in the same pull request, exactly like a broken import.
- Misconception: "a link checker is enough". Correction: every link can resolve while a rule silently disappears; the coverage check (each of the 66 active rules in exactly one doc) catches that.
- Time: 3.5 minutes. Next: the four ideas on one page.

## Slide 30: Cheat Sheet: The instructions layer in four moves
**Block:** Section 1  **Time:** 1.5  **Diagram:** none
**On the slide:**
Cheat Sheet: The instructions layer in four moves
- Map: about 100 lines, points to docs
- Disclosure: names first, bodies on demand
- Prefix: fixed, built from a read-only copy
- Checks: links, rule coverage, no new facts
It informs. It never blocks.
**Visual:** A native 2 by 2 grid of four cards (map, tiers, prefix, checks), each with an icon and its one line; the closing line in orange across the bottom. Diagram-led summary, no extra text.
**Speaker notes:**
- One sentence for the whole layer: give the agent a short map that is always in its context and points to focused documents and skills, which it opens only when the task needs them.
- Map: keyed by action, one file per row, house rules at a glance, "Do not copy" for legacy code.
- Disclosure: tier 1 always, tier 2 when picked, tier 3 when a step needs it.
- Prefix: built once from a copy the agent cannot edit, the same for every session.
- Checks: a script keeps links, rule coverage, and parity true; a test keeps the A/B fair.
- "It never blocks": the layer's `after_tool` hook returns notes, never a refusal. If you need a guarantee, you need Sections 3 and 4.
- Analogy: a warning-level lint rule: it points at the problem and never fails the build.
- Ask: "Which card would you add to your repository first?" Expected: the map; follow up with "and which check keeps it true?"
- Misconception: "if the agent reads the map, it will follow the rules". Correction: reading is not applying; the referee checks the shipped code, not the reading list.
- Point at the orange line "It informs. It never blocks.": the dividing line between this layer and Sections 3 and 4.
- Likely question: "Can I adopt the cards one at a time?" Answer: yes; the map alone is useful, and the checks start to matter once more than one person edits the docs.
- Time: 1.5 minutes. Next: the live run.

## Slide 31: Section 1 - Implementation Notes: The map at work
**Block:** Section 1  **Time:** 8  **Diagram:** screenshot: section-1-instructions/demo/expected/screen-1-final.png
**On the slide:**
DEMO - 1
Section 1 - Implementation Notes: The map at work
**Visual:** The "DEMO - 1" badge top-left and the screenshot `screen-1-final.png` (screen 1 after the full verdict), with three callouts: arrow to the harness decisions list, "map and skill read"; arrow to the pill, "primary verdict PASS at 04:11"; arrow to the results row, "hidden 52/52, mutants 2/4".
**Speaker notes:**
- Switch to browser tab 2, the live run of `make show-1` (terminal B) launched at section minute 3, class 0:13. It should be finished: full verdict about 10 min after launch, up to 2 min later with the 420 s limit. If it is finished, walk it; if not, walk the live screens and come back for the verdict.
- Screen 1 (`1`): the badge "HARNESS IN ACTION"; the notes "placed 31 instruction files (AGENTS.md map, docs, skills)", "agent read ARCHITECTURE.md", "agent read skill add-endpoint (tier 2)"; patches to the issues service, route, and tests; "No gate."; the test phase; "primary verdict ready: PASS".
- Read the verdict aloud. Pass: "No new tenant leak. One run shows the layer ran, not that it helped." Fail: "A leak shipped with the map in place. That is a result."
- Screen 3 (`3`): files read, grouped as skill, harness doc, handbook, code, test; the five changed files; the referee line `r1_tenant: 0 new`. The old `/v1/issues` leak is part of the starting code and does not count.
- Point out on screen 3: in the captured run the agent opened the skill, `ARCHITECTURE.md`, and the handbook, but not `docs/SECURITY.md`. Only `read_file` calls appear; a `cat` in a shell does not.
- Screen 2 (`2`): the board as `admin@acme.test`: "only own-org cards, no duplicates". F1 changes no board pixels, so there is one frame.
- Screen 5 (`5`): the referee event tail and the LangSmith links; open one to show every model call.
- What to say while the referee finishes: "The primary verdict comes first because R1 probes are quick; hidden tests, mutants, and the review take the remaining minutes."
- If the live run failed for a reason outside the experiment: say so, run `make replay RUN=<fallback id>` (red RECORDING badge on every screen). If Docker itself is down, walk the captured run: the screenshots in `section-1-instructions/demo/expected/` in minute order, and `terminal.txt`.
- If the arm ended `ABORTED: timeout` or `ABORTED: cap`: it is still judged. Say which limit it hit and read the verdict.
- Time: 8 minutes. Next: the run as a timeline.

## Slide 32: What just happened: The run, minute by minute
**Block:** Section 1  **Time:** 3  **Diagram:** none
**On the slide:**
What just happened: The run, minute by minute
- Minute 1: 31 files placed; map and skill read
- Minute 1: patches to service, route, tests
- Minute 3: test phase runs its own test
- 3:53: run ends after 35 turns
- 4:11: primary verdict PASS, 0 new R1
- 10:00: full verdict, hidden 52/52, mutants 2/4
**Visual:** A native horizontal timeline from launch to 10:14, six ticks with the labels above, and three thumbnails under the line: `screen-1-minute-1.png`, `screen-1-minute-3.png`, `screen-1-minute-4.png`. Footnote: "Captured run before class, 2026-10-17; agent limit then 300 s".
**Speaker notes:**
- These times are from the captured run before class (evidence, Section 1 captures), not tonight's run. Read tonight's times from screen 1 next to them; yours will differ.
- Minute 1: the layer did its three jobs in order: placed the files, handed over the prefix, and logged the first two reads (`ARCHITECTURE.md`, then the skill body, tier 2).
- Minute 3: the agent had said done and, in its test phase, wrote and ran `test_org_issue_search.py`.
- 3:53: the run ended after 35 turns. 4:11: the R1 probes finished; PASS, 0 new violations.
- 10:00: hidden tests 52 of 52, referee mutants killed 2 of 4, reviewer accepted, "claim supported". 10:14: the command printed its cost line, $0.019744 ($0.017882 agent, $0.001862 review).
- Mutants 2 of 4 means the agent's own tests caught only half of the referee's planted bugs. Section 4 is about exactly that gap.
- Analogy: a CI timeline: build, unit tests, then the slow integration stage. You read the fast signal first.
- Point at the gap between 3:53 and 4:11: 18 seconds from "agent done" to the answer the section cares about.
- Ask: "What does this timeline not tell us?" Expected: whether the map caused the PASS. One harness arm, no bare arm next to it.
- Likely question: "Why 35 turns for a small endpoint?" Answer: reading docs, patching three files, and writing and running tests in a second session all cost turns; screen 1 lists each turn.
- Misconception: "PASS at 4:11 means the feature is correct". Correction: PASS answers one question, no new tenant leak; the 52 of 52 hidden tests at 10:00 are a separate answer.
- Time: 3 minutes. Next: the code behind those notes.

## Slide 33: Under the hood: How the prefix is built
**Block:** Section 1  **Time:** 5  **Diagram:** none
**On the slide:**
Under the hood: How the prefix is built
platform/src/shipharness/harness/instructions/router.py, lines 37-47
**Visual:** The code excerpt, quoted exactly, with line 2 highlighted as the key line (`agents_md = ...`, read from `source`, the course's copy):
```python
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
**Speaker notes:**
- This is the body of `build_prefix`, from the section's walkthrough. Three parts: one sentence on how to use the map, the whole map, the skills catalogue.
- Key line: `agents_md` is read from `source`, which is `platform/teamtrack/harness/instructions/`, never the arm's workspace. Editing the workspace copy changes nothing the agent is told.
- `strip_markers` drops the class's walkthrough comment lines; that is why the agent gets 92 of the map's 94 lines.
- `catalogue_block` reads only each skill's frontmatter and writes one line per skill: name, description, path. The skill body stays on disk: tier 1 only.
- Not shown, same layer: `context_prefix` in `layer.py` (lines 113-116) caches this string, so every session gets identical text.
- Also not shown: `after_tool` (lines 126-136) logs each harness file the agent opens once, and tags skill reads with their tier. It returns a note; it never blocks.
- Concrete: those `after_tool` notes are the "agent read skill add-endpoint (tier 2)" lines you just saw on screen 1.
- Analogy: building an immutable config object at startup from a read-only mount, then injecting it everywhere.
- Ask: "What would go wrong if `source` pointed at the workspace?" Expected: the agent could rewrite its own instructions mid-run, and session 2 would get the edited map.
- Likely question: "Do I need this code to use a map?" Answer: no. Most coding agents load `AGENTS.md` and skills themselves; you need the files. Write code like this only if you run your own loop.
- Point at the highlighted line, then at `catalogue_block()`: the only two things that reach the model's context.
- Misconception: "the agent can edit its prefix like any file". Correction: the prefix is a string built in the harness process on the host; the workspace `AGENTS.md` is only a copy.
- Time: 5 minutes. Next: what the measurements say.

## Slide 34: What we measured: No measurable difference on F1
**Block:** Section 1  **Time:** 3.5  **Diagram:** section-1-instructions/diagrams/results-s1.png
**On the slide:**
What we measured: No measurable difference on F1
A run fails if it adds a new R1 violation:
- Bare arm: 0 of 7 runs failed
- Harness arm: 0 of 7 runs failed
It earns its place when:
- Rules are many and far from code
- The code cannot show the rule
- Several people own the rules
**Visual:** The `results-s1` dot chart: one dot per run, bare arm in grey and harness arm in blue, filled for passed, by round (medium effort 3, low effort 3, class settings 1). Every dot filled. The two bullet groups sit to the right of the chart.
**Speaker notes:**
- Poll answer: A. Before class, 0 of 7 bare-arm runs shipped a new tenant leak, and 0 of 7 harness-arm runs. Rounds: medium effort (3 per arm), low effort (3), class settings (1).
- Say it plainly: no measurable difference on this task with this model. Neither arm copied the legacy query, so the map had nothing to fix.
- Every arm in every round passed 52 of 52 hidden tests. An earlier round on the plain ticket gave the same result, 0 of 3 per arm.
- In the class-settings run, the bare arm did not open the handbook in its first nine tool calls and still wrote an org-scoped query. The model already did the right thing.
- Post hoc (chosen after the results, so descriptive only), 10 runs per arm: harness arms claimed done in 5, bare arms in 9, no false claim in either; median cost $0.0122 against $0.0103.
- When it earns its place: many or long rules far from the code; a rule the code cannot show, such as "404, never 403"; several maintainers (small files can be owned and checked, one big file "rots instantly"); a recurring task worth a skill.
- When it does not: the model already does it; the ticket already points to the rule; the map is stale; you need a guarantee (it never blocks).
- Analogy: a code-review checklist item for a mistake your team has stopped making. Keep it if it is cheap or the mistake is costly; know which.
- Ask (discussion): "The bare arm read the same rules and applied them. What would have to be true for the map to earn its place?" Expected: a model or ticket where bare arms leak; more rules; or maintenance value you can name.
- Misconception: "no difference means maps are useless". Correction: it is a result about one bet on one model and one ticket; the maintenance reasons were not measured.
- Point at the two rows of dots: every dot filled, in both arms, in all three rounds.
- Likely question: "Was the trap too weak?" Answer: possibly; in one round no arm of either kind opened the legacy files. A stronger trap would need a new registered test, not a reinterpretation of this one.
- Time: 3.5 minutes. Next: what to do on Monday.

## Slide 35: Apply it Monday: Turn your instruction file into a map
**Block:** Section 1  **Time:** 1.5  **Diagram:** none
**On the slide:**
Apply it Monday: Turn your instruction file into a map
In your own repository:
- Count your instruction file's lines
- List three rules your agent breaks
- One "read first" row per action
- Add "Do not copy" for legacy code
Then keep it true:
- A link and rule check in CI
- Log which docs the agent opens
**Visual:** A native checklist card with two groups and empty tick boxes; a small footer chip: `uv run shipharness init --target ../your-repo`.
**Speaker notes:**
- Step 1: count the lines of your AGENTS.md, CLAUDE.md, or rules file. Compare with OpenAI's "roughly 100 lines".
- Step 2: list the three rules your agent breaks most often. For each: where does it live, and does anything point to it before the agent writes code?
- Step 3: rewrite the top of the file as a "When you are about to → Read first" table, one file per row, like TeamTrack's map.
- Step 4: a "Do not copy" section naming the legacy handler or deprecated pattern your agent keeps finding, and the file to copy instead.
- Spoken extra (not on the slide): one skill for the task you hand to agents most, with a description that says what it does and when to use it.
- Step 5: a CI check for broken links and rule coverage; Assignment 1 has you write one.
- Step 6: log which documents the agent opens; it is the cheapest way to see whether the map is used.
- Starter kit: `uv run shipharness init --target ../your-repo` copies the map and docs templates, with a REPLACE marker next to every TeamTrack value. See `use-in-your-repo/README.md`.
- Analogy: refactoring a god object into modules with an index; you do not change behaviour, you make it findable and testable.
- Ask: "Which of these can you do in 30 minutes on Monday?" Expected: steps 1 to 4.
- Point at the second group: the CI check and the read log are what keep the new map from rotting.
- Likely question: "What if my agent ignores AGENTS.md?" Answer: check the log of opened files (step 6); if it never opens the docs, sharpen the "When you are about to" keys.
- Misconception: "delete the long file once the map exists". Correction: move every rule to a doc and check coverage first, as Assignment 1 does; a rule lost in the move is a silent regression.
- Time: 1.5 minutes. Next: questions.

## Slide 36: Q&A: Section 1, what the agent knows
**Block:** Section 1  **Time:** 1.5  **Diagram:** none
**On the slide:**
Ask about anything:
- Concepts from today's sections
- How this applies to your work
- Implementation details
- Clarifications on what we covered
Quick Request
- Please do not mind if a question gets skipped accidentally
- Repost politely in chat if needed
- We will try our best to cover as many questions as possible
Remember: If you're wondering about it, others probably are too.
No Question Is Too Small Every Question Deserves an Answer!!
**Visual:** Template slide 32 unchanged: the two bullet groups, the reminder line, the banner, and the picture.
**Speaker notes:**
- Take questions from the chat first; TAs pick the top ones.
- Likely: "Is the harness arm not just given more information?" Answer: no; it may reorganise knowledge, never add facts. Same ticket, model, tools, budgets, and sandbox, and `test_parity.py` checks the rules match.
- Likely: "Why not paste the whole handbook into the prompt?" Answer: "Too much guidance becomes non-guidance"; it crowds out the task and goes stale.
- Likely: "Does the files-read list on screen 3 prove the harness worked?" Answer: no; it explains a path. The score is what the referee finds in the shipped code.
- Likely: "Would the map help a weaker model?" Answer: unknown; we measured one model. `make demo-1` runs both arms on F1 if you want to find out.
- Likely: "What does the agent see of a skill at the start?" Answer: one catalogue line: name, description, and the path to `SKILL.md`.
- Misconception to correct if it comes up: "the map failed". Correction: the model did not need it on this ticket; that is a finding about the bet, measured.
- Analogy for wrap-up: a "deprecated, use X" comment pays off only if someone would otherwise have called the old function.
- After class: Assignment 1 (`make check-assignment-1`; it fails on the starter by design), the post-class readings, and `section-1-instructions/session-notes.md`.
- Time: 1.5 minutes, section ends at class minute 1:00. Next: Section 2, what happens when a session stops halfway.

## Slide 37: Time for a Break
**Block:** Break  **Time:** 5  **Diagram:** none
**On the slide:**
A 5-minute break is starting now. Please return when the timer ends to continue the presentation
**Visual:** The template's break layout and timer picture. Write the return time next to the timer.
**Speaker notes:**
- Write the return time on the slide before you step away.
- Nothing runs during the break; do not launch any command, and leave the console (terminal A) open.
- Check that terminal B is free: Section 2 launches `make show-2 SESSION_BUDGET=12,38` right after the poll.
- If a learner's setup failed in Section 1, point them to `setup/` and `docs/troubleshooting.md` for the break.
- Return time: class minute 1:05 in this deck.
- Transition: "Welcome back. The agent now knows the rules. Next: what happens when its session ends halfway through the work."

## Slide 38: Today's Agenda: Section 2, what the agent remembers
**Block:** Section 2  **Time:** 1  **Diagram:** none
**On the slide:**
1 Instructions
2 State and session lifecycle (current)
3 Scope and sandbox
4 Verification
Final A/B
**Visual:** The template's agenda layout: five numbered boxes joined by connectors. Box 1 outlined as done; box 2 highlighted with the star; boxes 3, 4 and Final pale.
**Speaker notes:**
- Explain: Section 1 decided what the agent knows when a session starts. Section 2 asks what survives when a session stops before the work is done.
- Example: the ticket is F2, comments on issues: a `comments` table, endpoints, and a board panel. It is too big for one 12-turn session.
- Analogy: an on-call handover. The next engineer arrives with no memory of the last shift; the handover note is all they have.
- Point at: box 2, and the live command we launch next, `make show-2 SESSION_BUDGET=12,38`.
- Ask the room: "How does your agent know what yesterday's session did?" Expected answer: mostly it doesn't; people paste a summary or hope it reads git.
- Likely question: "Isn't a longer context window the fix?" Answer: a session still ends somewhere, by a turn limit, a crash or a timeout; this section is about that moment.
- Misconception: "State means a database or a memory service." Correction: here state is a few plain files and the git history, checked into the repository.
- Time and transition: 1 minute. "Before I explain anything, you predict the result. Poll first."

## Slide 39: Live Zoom Poll: Did session 2 redo session 1?
**Block:** Section 2  **Time:** 4  **Diagram:** none
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 2 minutes to fill out the form.
Then, live: `make show-2 SESSION_BUDGET=12,38`
**Visual:** The template's poll picture. Under it, one command strip in monospace: `make show-2 SESSION_BUDGET=12,38`.
**Speaker notes:**
- Poll question (Zoom, not on the slide): "Before class we ran 7 A/Bs on the comments ticket, each with session 1 stopped after 12 turns. Which arm had more continuity failures? A) Bare B) Harness C) About the same D) Neither arm failed once." Do not reveal; the answer (D, 0 of 7 each) comes on the "What we measured" slide.
- Define before the vote: a continuity failure is two Alembic heads or a failed fresh upgrade (house rule R7), a table created by two migrations, or session 2 removing 30% or more of the lines session 1 added.
- Close the poll, then terminal B: `make show-2 SESSION_BUDGET=12,38`. Leave out `SESSION_BUDGET` and session 1 runs the ticket's 20 turns instead of 12.
- Browser tab 2: reload the run list, open the newest run, press `1` (Live). Keys: `1` Live, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces.
- Say: "This is the harness arm alone, not an A/B. The comparison was done before class; tonight shows the state layer doing its job."
- What to expect, from the timed run on 2026-10-17: session 1 stopped at 1 min 23 s, primary verdict at 6 min 46 s, full verdict at 9 min 52 s, cost $0.029525. That run had a 300 s agent limit; class now has 420 s, so it can take up to 2 minutes longer.
- While it runs: teach the next slides; glance at screen 1 for "Session 1 stopped" around minute 1-2.
- If `x OpenAI refused the key`: fix `OPENAI_API_KEY` in `.env`, run `make doctor`, relaunch.
- If `x SHIPHARNESS_CLASS_DATE is not set`: `sed -i "s/^SHIPHARNESS_CLASS_DATE=.*/SHIPHARNESS_CLASS_DATE=$(date +%F)/" .env`, relaunch.
- If the arm ends `ERROR` with `docker run failed`: `sudo systemctl start docker`, then `make warm`, then relaunch. If Docker stays down, `make replay RUN=<fallback id>`; if even that fails, walk the captured run in `section-2-state-lifecycle/demo/expected/` and say "recorded before class".
- If `make console` says `address already in use`: `make console CONSOLE_PORT=8766`.
- Clock: in this deck the poll starts at class 1:06 and the launch lands about 1:08 (the instructor guide's run sheet says 1:03, because it puts one 10-minute break after Section 2). Either way the run, about 10 min and up to 12 with the 420 s limit, finishes before the demo slide at about 1:32.
- Time and transition: 4 minutes including the launch. "While it runs, here is the failure we are guarding against."

## Slide 40: Problem statement: The second session redoes the first
**Block:** Section 2  **Time:** 3  **Diagram:** section-2-state-lifecycle/diagrams/alembic-heads.png
**On the slide:**
**Marco asks a coding agent to add comments to TeamTrack issues: a `comments` table, three endpoints, a board panel. The work needs two sessions (illustrative).**
The problem we're solving (in the real world)
Session 1 hits its turn limit and leaves:
- A migration for the `comments` table
- Half an endpoint, never committed
- No note for the next session
- A ticket that still says "add comments"
Session 2 starts with an empty context, so:
- It writes a second migration from the old head
- Two Alembic heads stop the deploy
- A reviewer untangles two versions of one change
- The team pays for the same work twice
**Visual:** Template slide-16 layout: framing line bold, product name TeamTrack in the accent colour, the orange subheading, two bullet groups. Right third: `alembic-heads.png` small, showing two migrations branching from `0001_initial` into two heads, with the R7 marker.
**Speaker notes:**
- Explain: this is an illustrative scenario from the section's concepts page, built from the failure Anthropic describes: a session that ends "with a feature half-implemented and undocumented", leaving the next one "to guess at what had happened".
- Example: in TeamTrack, house rule R7 says exactly one Alembic head and a working fresh upgrade. Two migrations that both claim `0001_initial` as their parent make two heads; `alembic upgrade head` refuses to pick one.
- Analogy: two engineers on different shifts each writing the same schema change because nobody wrote "I already did the migration" on the ticket.
- Point at: the diagram's fork. That fork is what the referee's R7 check looks for in every run.
- Ask the room: "Session 2 has the whole repository, including the uncommitted migration. Why would it write a second one?" Expected answer: having the file is not the same as looking at it; if it never runs `git status` or lists `migrations/versions`, it works from the ticket alone.
- Likely question: "Would CI catch two heads?" Answer: R7-style checks do, but only after the duplicate work is done and paid for; the goal is that session 2 never starts it.
- Likely question: "Did this happen in your runs?" Answer: not on this model. Keep that for the measured slide; it matters.
- Misconception: "Uncommitted work is lost work." Correction: the files are still on disk; the problem is that nothing tells the next session to look.
- Time and transition: 3 minutes. "So why would a capable model redo work that is sitting right there? Let me ask it as a question."

## Slide 41: Fresh session: Why redo work already on disk? (build 1/3)
**Block:** Section 2  **Time:** 1  **Diagram:** none
**On the slide:**
What the agent remembers
- Session 2 has the whole repository
- But it starts with an empty context
- Can we carry the old context over?
**Visual:** Native layout as in template slides 25-27: header fixed, three bullets, the last one in the accent colour as the question. Small two-box sketch on the right: "Session 1 (12 turns)" box ending at a red stop line, "Session 2 (38 turns)" box empty.
**Speaker notes:**
- Explain: every session is a fresh model call with a fresh context. Anthropic's harness team: "each new session begins with no memory of what came before."
- Example: in our runs, session 1 gets 12 turns and session 2 gets 38. The stop is the same for both arms.
- Analogy: a laptop reimaged overnight: the repository is still on the server, but every open tab, note, and half-typed command is gone.
- Point at: the empty Session 2 box.
- Ask the room: "Can we just carry the old context over, squeezed down?" Let them answer before the next click. Expected answer: many will say yes, summarise or compact it.
- Likely question: "Is the 12-turn stop realistic?" Answer: it is the course's own mechanism, a session turn budget, so the stop happens at a known point in both arms; real sessions end by limits, timeouts, crashes.
- Misconception: "The model remembers the repo between sessions." Correction: nothing carries over except what is on disk.
- Time and transition: 1 minute. Click for the verdict.

## Slide 42: Fresh session: Why redo work already on disk? (build 2/3)
**Block:** Section 2  **Time:** 1  **Diagram:** none
**On the slide:**
What the agent remembers
- Session 2 has the whole repository
- But it starts with an empty context
- Can we carry the old context over? - Why not
**Visual:** Same frame as build 1. "- Why not" added in red bold after the question, as in template slide 26.
**Speaker notes:**
- Explain: the answer is "not on its own". Anthropic's own words: "However, compaction isn't sufficient."
- Example: a compacted transcript still says "I started the migration" without saying where the file is or whether it was committed.
- Analogy: a meeting summary versus the actual pull request; the summary drops the detail you need.
- Point at: the red "Why not".
- Ask the room: "What would compaction lose?" Expected answer: exact file names, what was committed, which decisions were made and why.
- Likely question: "Does compaction help at all?" Answer: Anthropic says it "preserves continuity" but does not give the agent "a clean slate".
- Misconception: "A bigger summary is a better summary." Correction: the next session needs facts it can check against the repository, not a longer story.
- Time and transition: 1 minute. Click for the reasons.

## Slide 43: Fresh session: Why redo work already on disk? (build 3/3)
**Block:** Section 2  **Time:** 1  **Diagram:** none
**On the slide:**
Can we carry the old context over?
- Compaction keeps a squeezed copy
  - "However, compaction isn't sufficient."
- The repository holds it, but unread
  - Only `git status` would show the migration
What can we use instead?
**Visual:** Same header; body replaced by the two reasons with one nested example each, then the closing question in the accent colour, as in template slide 27.
**Speaker notes:**
- Explain: two reasons. A compressed context is still the old context with gaps. The repository has the truth, but only if the session is told to read it first.
- Example: in one test run before class, the bare arm's session 2 ran `git status` as its fourth tool call, saw `?? migrations/versions/0002_comments.py`, read it and carried on. Nothing told it to; this model sometimes does it by itself.
- Analogy: a `git stash` nobody mentioned: the work exists, but only someone who runs `git stash list` finds it.
- Point at: the closing question. The next four numbered slides answer it.
- Ask the room: "What would you write down for the next session?" Expected answer: what I did, what is left, what to watch out for, and how to check the app still works.
- Likely question: "Why not just tell the agent to run `git status`?" Answer: that is part of the answer, the getting-up-to-speed routine on slide 4.
- Misconception: "If the work is in git, the agent will find it." Correction: `git status` is one of many possible first calls; the bare arm found the migration by itself once, and nothing made that happen every time.
- Time and transition: 1 minute. "The answer is a reset plus a structured handoff. Four pieces, one per slide."

## Slide 44: 1) Session lifecycle: a planned stop and reset
**Block:** Section 2  **Time:** 3.5  **Diagram:** section-2-state-lifecycle/diagrams/session-lifecycle.png (+ steps)
**On the slide:**
A context reset clears the context and starts a fresh session, with a structured handoff.
Every session runs the same loop:
- Getting up to speed: read, run `init.sh`
- Work, commit as you go
- Wrap-up: notes, progress, commit
- Stop: the harness writes the facts
**Visual:** `session-lifecycle.png` shown as builds: `session-lifecycle-step-1.png` (session 1: up to speed, work, wrap-up), `-step-2.png` (the stop: harness writes the facts into the repository), `-step-3.png` (session 2 reads the files first), then the full image.
**Speaker notes:**
- Explain: the source term is Anthropic's "context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps".
- Explain the loop: two routines wrap each session. At the start, "Getting up to speed". At the end, "End the session by writing a git commit and progress update." Both quotes are from Anthropic's long-running harness.
- Example: near the end of each session both arms get the same message, "This session is ending soon." In the captured run, turns 1.10 and 1.11 updated and committed the state files, and turn 1.12 called `finish(claim="not_done")`.
- Example: a runner bug we found by reading runs. Earlier, any `finish` ended the build phase, so session 2 never ran. Now `finish(claim="not_done")` before the last session ends only that session, in both arms.
- Analogy: a shift pattern with a fixed handover time; the handover is part of the shift, not an afterthought.
- Point at: frame 2, the stop. The harness writes there whatever the agent did.
- Ask the room: "Why does the harness write at the stop instead of trusting the wrap-up turns?" Expected answer: the agent can run out of turns before it writes anything.
- Likely question: "Who decides when the session ends?" Answer: the runner, by the session turn budget (12 then 38 here), or the agent by calling `finish`.
- Misconception: "A reset throws work away." Correction: it throws away the context, not the repository; the work is on disk and in git.
- Time and transition: 3.5 minutes. "The file that crosses the stop is the handoff, and it has two owners."

## Slide 45: 2) The handoff: two owners, one file
**Block:** Section 2  **Time:** 4  **Diagram:** section-2-state-lifecycle/diagrams/handoff-contents.png
**On the slide:**
`session-handoff.md` carries the last session's state and the next steps.
Two owners, neither overwrites the other:
- Harness: machine summary, rewritten every stop
- Commits, files changed, tests, migration heads
- Agent: notes from its wrap-up turns
- Doing, left, watch out for
**Visual:** `handoff-contents.png`: the file split in two bands, "Machine summary (harness, from git)" on top and "Notes from the agent" below, each listing its fields.
**Speaker notes:**
- Explain: the harness owns "Machine summary" and writes it from the repository at every stop. The agent owns "Notes from the agent". The harness's `merge` replaces only its own part and keeps the agent's notes as written.
- Example of a fact line: the migration heads line says "house rule R7 needs exactly one" when it finds two heads, so session 2 sees the problem before writing another migration.
- Example of real agent notes from the captured run: "API/web must not import `app.db`; all customer queries must filter org." A fresh session cannot see that in the code.
- Analogy: an incident handover with two parts: the dashboard snapshot (facts, generated) and the engineer's note (judgement, written).
- Point at: the top band. It exists even if the bottom band is empty.
- Ask the room: "Which facts would you never trust the agent to write?" Expected answer: what was committed, which files changed, whether tests pass, how many heads.
- Likely question: "What if the agent writes wrong notes?" Answer: they stay as written; the machine summary above them is regenerated from git at every stop, so session 2 can check one against the other.
- Likely question: "What if the agent deletes the file?" Answer: the harness rebuilds it from its template at the next stop and the log line still lands.
- Misconception: "A handoff written by the agent is enough." Correction: it is empty exactly when the agent ran out of turns.
- Time and transition: 4 minutes. "The handoff covers one stop. For the whole task there is a plan and a ledger."

## Slide 46: 3) The exec plan and the progress ledger
**Block:** Section 2  **Time:** 3  **Diagram:** none
**On the slide:**
"it should always be possible to restart from _only_ the ExecPlan and no other work." (OpenAI, PLANS.md)
Two files, two jobs:
- `progress.md`: done, in progress, next
- Session log: one harness entry per stop
- Exec plan: progress, surprises, decisions, outcomes
- Both checked in, both read first
**Visual:** The exec plan the harness writes, lines 1-5 quoted exactly from `section-2-state-lifecycle/demo/harness/docs/exec-plans/active/F2.md` (key line marked); a caption under it lists the sections that follow: Progress, Surprises & Discoveries, Decision Log, Outcomes & Retrospective, Validation.
```markdown
# F2: Comments on issues, with a comments panel on the board

This execution plan is a living document checked into the repository (A7). Keep it self-contained:
a new session must be able to restart from this plan, progress.md, and the git log alone. The   <-- key line
harness moves it to docs/exec-plans/completed/ when the feature passes.
```
**Speaker notes:**
- Explain: OpenAI's harness team keeps "execution plans with progress and decision logs that are checked into the repository". The PLANS.md recipe asks for four living sections: Progress, Surprises & Discoveries, Decision Log, Outcomes & Retrospective.
- Explain: `progress.md` is the course's name for Anthropic's `claude-progress.txt`: what each session did and what is next. The agent edits every section except "Session log", where the harness appends one entry per stop.
- Example: a decision such as "comments use keyset paging, ascending id, like projects" goes in the Decision Log, so session 2 does not reopen it.
- Analogy: a design doc plus a changelog. The doc says what and why; the changelog says what happened when.
- Point at: the key line; the restart bar is the test of a good plan.
- Ask the room: "Could someone restart your current task from only your notes?" Expected answer: usually no; the decisions live in chat or in someone's head.
- Likely question: "Why Markdown here and JSON for the feature list later?" Answer: these are notes the agent writes freely; the feature list in Section 3 is graded state the agent must not edit.
- Misconception: "The plan is written once at the start." Correction: it is a living document; progress lines get a UTC timestamp, and the harness moves it to `completed/` when the feature passes.
- Time and transition: 3 minutes. "Files only help if the next session reads them first. That is the routine."

## Slide 47: 4) Getting up to speed: `init.sh` before code
**Block:** Section 2  **Time:** 3.5  **Diagram:** section-2-state-lifecycle/diagrams/alembic-heads.png
**On the slide:**
"Read the git logs and progress files to get up to speed on what was recently worked on."
Session 2's first call, in the captured run:
- `pwd; git log --oneline -20`
- `cat progress.md`, `cat session-handoff.md`
- `cat docs/exec-plans/active/F2.md`
- `bash init.sh`: one head, basic test
**Visual:** `alembic-heads.png` on the right: one head passes `init.sh`; two heads trip house rule R7. On the left, the four lines above set as a terminal card.
**Speaker notes:**
- Explain: the routine is Anthropic's own heading, "Getting up to speed": read the git log and progress file, then run `init.sh` and a basic test before touching code, because starting new work on a broken app "would likely make the problem worse."
- Example: TeamTrack's `init.sh` runs `alembic heads`, `alembic upgrade head` on a scratch SQLite database, then `pytest tests/visible/test_issues.py -x`. It leaves no files to commit.
- Example: in the captured run, session 2's git log began with "harness: session 1 handoff for F2", and session 2 wrote exactly one migration, `0002_comments.py`, from the current head.
- Analogy: the first ten minutes of an on-call shift: read the handover, check the dashboards are green, then start.
- Point at: the `alembic heads` line in the diagram. One command would have stopped the opening story.
- Ask the room: "What is the cheapest check that would have prevented the two-head story?" Expected answer: list the heads before writing a migration.
- Likely question: "Who writes `init.sh`?" Answer: an initializer step before session 1. Anthropic uses a model session for it; this course uses plain code, because one ticket fixes the files, so it costs no model call.
- Misconception: "`init.sh` is for humans setting up a laptop." Correction: here it is the agent's smoke test, run at the start of every session.
- Time and transition: 3.5 minutes. "Four pieces. One card to take away."

## Slide 48: Cheat Sheet: Four state pieces across a stop
**Block:** Section 2  **Time:** 2  **Diagram:** none
**On the slide:**
- `init.sh`: setup and a basic test
- `progress.md`: what each session did, what's next
- Exec plan: plan, decisions, restart bar
- `session-handoff.md`: harness facts plus agent notes
Refer back to this slide when you add state files to your repo
**Visual:** A native four-row card, one row per file, with a small "who writes it" tag on each: harness (init.sh), both (progress.md), agent (exec plan), two owners (handoff). The refer-back line at the bottom.
**Speaker notes:**
- Explain: four files, each with one job, plus the git history that ties them together.
- Example: the initializer step writes all four and commits them as "harness: initializer step for F2" before session 1.
- Analogy: README, CHANGELOG, design doc, and handover note in a well-run repository: each answers one question for whoever arrives next.
- Point at: the "who writes it" tags; ownership is the design decision, more than the file names.
- Ask the room: "Which of these does your repository already have under another name?" Expected answer: a README with setup steps, sometimes a TODO file; rarely a handoff.
- Likely question: "Do I need all four?" Answer: no; measure. The next slides show they made no measurable difference on this ticket with this model.
- Misconception: "More state files mean more reliable agents." Correction: they cost turns; harness arms hit the agent time limit more often (post hoc, next slides).
- Instructor cue: this slide sits at section minute 25. Glance at terminal B for the `Cost:` line of `make show-2`; if it is there, read the session figure aloud.
- Time and transition: 2 minutes. "The run should be done. Let's look at it."

## Slide 49: Section 2 - Implementation Notes: Stop and resume
**Block:** Section 2  **Time:** 6  **Diagram:** screenshot: section-2-state-lifecycle/demo/expected/show-2-screen-1-t02m.png
**On the slide:**
DEMO - 2
Section 2 - Implementation Notes: Stop and resume
**Visual:** "DEMO - 2" badge top-left; screenshot of console screen 1 at minute 2. Callouts: (1) arrow to the pill "Session 1 stopped" with label "turn budget spent"; (2) arrow to "Session 2 resumed" with label "empty context"; (3) arrow to turn 2.1 `pwd; git log --oneline -20; cat progress.md` with label "reads state first".
**Speaker notes:**
- Switch to browser tab 2, tonight's run of `make show-2 SESSION_BUDGET=12,38` (terminal B, launched at the poll). If it is still going, stay on screen 1 (`1`); "primary verdict ready" appears as soon as the continuity check is done.
- Screen 1 (`1`): scroll to "Session 1 stopped" and "session 1 handoff written", then "Session 2 resumed · prefix: core, instructions, state". Then turn 2.1: the getting-up-to-speed call.
- Screen 1, later: session 2 writes the model, service, route, seed, and one migration `0002_comments.py`. Then "primary verdict ready".
- Screen 3 (`3`): Sessions table (in the capture "Session 1 · 12 turns · claim_not_done", "Session 2 · 31 turns"); referee list `continuity: 0 new` and `r7_migrations: 0 new`. Also `diff_scope: 1 new`: an edit to `app/api/issues.py`, outside F2's allowed paths. Nothing stopped it: the scope layer starts in Section 3.
- Screen 2 (`2`): the board as an Acme user, own-org cards only. The comments panel is on the issue page; hidden tests judge it.
- Screen 5 (`5`): the first wrong turn, named by the scope check (turn 2.16 in the capture), and the LangSmith trace links; open session 2's first calls.
- Screen 4 (`4`): the dots from before class. Say: "Tonight's run is not a dot in the comparison."
- Say at a PASS: "Session 2 picked up the work. No continuity failure." At a FAIL: "The handoff did not carry the work. Screen 3 shows how."
- If no "Session 1 stopped" marker: the agent called `finish(claim="done")` in session 1 or hit a cap; say this arm never faced the stop and walk the captured screens.
- If the run is not finished: read screen 1 live, then come back to screens 3 and 4 after the under-the-hood look.
- Fallback if the run broke for a reason outside the experiment (Docker, network, account): `make replay RUN=<fallback id>`, or walk `section-2-state-lifecycle/demo/expected/` (screen files `show-2-screen-1-t01m.png` to `show-2-screen-5-final.png`), saying "recorded before class".
- What to say while it finishes: "The continuity check comes first because it needs only git and Alembic; hidden tests, mutants, and the review take the remaining minutes."
- Time and transition: 6 minutes. "Here is the same run on one line."

## Slide 50: What just happened: One run, two sessions
**Block:** Section 2  **Time:** 3  **Diagram:** none
**On the slide:**
- 0:00 initializer writes four files, commits
- 1:23 session 1 stops at 12 turns
- 1:23 handoff committed, session 2 resumes
- 6:36 run ends at the time limit, 43 turns
- 6:46 primary verdict: PASS
- 9:52 full verdict: hidden 56/56, mutants 0/4
**Visual:** A native horizontal timeline, minutes from launch, six ticks with the labels above. Session 1 segment short and blue, session 2 segment long. The two verdict ticks in green. Caption: "Captured run, 2026-10-17, 300 s agent limit".
**Speaker notes:**
- Explain: these are the times of the captured run on 2026-10-17, with the earlier 300 s agent limit. Tonight's times will differ; class now uses 420 s.
- Example: the run ended `ABORTED: timeout` and the command exited 2. Exit 2 means an arm stopped at a time or cost limit; the referee still judged it. The command finished at 10 min 7 s.
- Example: session 1 spent its 12 turns reading and wrapping up; session 2 did the building in its 31 turns.
- Analogy: a database failover log: primary down, replica promoted, writes resumed; you read the gap between events, not the totals.
- Point at: the gap between 6:46 and 9:52: the primary verdict comes before hidden tests, mutants and review finish.
- Ask the room: "Session 1 wrote no product code. What does a PASS on continuity tell us then?" Expected answer: very little; there was nothing to redo.
- Likely question: "Why mutants 0/4 if hidden tests pass?" Answer: the agent shipped no tests that kill the referee's mutants; that is Section 4's subject.
- Misconception: "PASS means the feature is done." Correction: PASS means session 2 did not break or redo session 1's work. Read the hidden-test count next to it.
- Time and transition: 3 minutes. "What code ran at 1:23? Let's read it."

## Slide 51: Under the hood: What runs at every stop
**Block:** Section 2  **Time:** 5  **Diagram:** none
**On the slide:**
The facts come from the repository, not the agent
**Visual:** Code excerpt, `platform/src/shipharness/harness/state/lifecycle.py` (lines 100-111), key line marked:
```python
    ws: Path = ctx.workspace
    summary, tests = machine_summary(ctx, result, files_changed, timeout_s)   # <-- key line
    template = (ASSETS / HANDOFF).read_text(encoding="utf-8")
    write_file(ws, HANDOFF, handoff.merge(read_text(ws, HANDOFF), template, summary).encode())
    log = read_text(ws, PROGRESS) or (ASSETS / PROGRESS).read_text(encoding="utf-8")
    entry = progress.session_entry(result, len(files_changed), tests, claim)
    write_file(ws, PROGRESS, progress.append_session_entry(log, entry).encode())
    commit_paths(
        ctx.sandbox,
        [HANDOFF, PROGRESS],
        f"harness: session {result.index} handoff for {ctx.spec.feature_id}",
    )
```
**Speaker notes:**
- Explain: this is the body of `session_stop`, which the runner calls after every session ends. Four steps: compute the facts, merge them into the handoff, append a progress line, commit.
- Explain the key line: `machine_summary` reads the last commits, files changed, the visible test result, open TODO markers, the migration heads, and the documents the agent opened. It runs the visible suite once per stop, on harness time, not the agent's turns.
- Example: `handoff.merge` keeps the template header, inserts the new summary, and keeps everything from "Notes from the agent" down exactly as the agent wrote it.
- Example: if the agent deleted `progress.md`, the `or` falls back to the template and the log line still lands.
- Example: `commit_paths` names its paths, so anything the agent half-staged stays out of the harness commit. Its message is the first line session 2 sees in `git log`.
- Analogy: a CI job that writes a build summary on every run, pass or fail, instead of asking the developer to fill in a form.
- Point at: the key line, then the commit message string.
- Ask the room: "Why commit here rather than leave the files uncommitted?" Expected answer: the git log becomes the index; the next session finds the handoff by reading history, the routine it already follows.
- Likely question: "Where does session 2 get told about it?" Answer: `resume_text` adds "Start with the Getting up to speed steps before you change code" plus the machine summary, after the neutral resume sentence both arms get.
- Misconception: "The harness summarises the conversation." Correction: it never reads the transcript; it reads the repository.
- Time and transition: 5 minutes. "So did it help? Here is what we measured."

## Slide 52: What we measured: No measurable difference on F2
**Block:** Section 2  **Time:** 4  **Diagram:** section-2-state-lifecycle/diagrams/results-s2.png
**On the slide:**
Continuity failures before class:
- Bare arm: 0 of 7 runs
- Harness arm: 0 of 7 runs
- 6 of 12 arms built nothing
It earns its place when:
- Tasks outlast one session
- Half-done work is hard to see
- People and agents share a task
**Visual:** `results-s2.png`: one dot per run, two rows (bare grey, harness blue), grouped by round: medium effort (3), low effort (3), class settings (1). All dots "no continuity failure". A marker on the six arms that built nothing.
**Speaker notes:**
- Reveal the poll: answer D. Neither arm failed in any of the 7 A/Bs: medium effort 0 of 3 each, low effort 0 of 3 each, class settings 0 of 1 each. Model gpt-6-luna, same settings both arms. Say plainly: "No measurable difference on this task with this model."
- Limit 1: in the medium- and low-effort rounds, 6 of 12 arms built nothing (3 of 56 hidden tests, the 3 that pass on the checkpoint). The measure cannot fail when session 1 leaves nothing to redo.
- Limit 2: those six runs exposed the runner bug from idea 1; the fix applies to both arms. In the class-settings round both arms passed 56 of 56 hidden tests.
- Why a tie: in one earlier test run the bare arm's session 2 ran `git status` as its fourth tool call and found the uncommitted migration by itself. The repository was enough state for this model.
- Cost, post hoc (chosen after the results, so descriptive only), 9 runs per arm: harness arms hit the agent time limit in 4 of 9, bare in 0 of 9; median arm wall time 361 s against 232 s.
- Analogy: a feature flag rolled out with no change in your metrics: keep it for a reason you can name, or remove it.
- Point at: the identical rows of dots.
- Ask the room: "What would a fairer test of the handoff need?" Expected answer: longer tasks, more stops, sessions that leave real half-done code, and more runs.
- Likely question: "So are state files useless?" Answer: this is one bet on one model and ticket; it says nothing about longer tasks, other models, or people picking up the work. Anthropic dropped context resets from its own harness once a later model no longer needed them.
- Misconception: "No difference means it was a waste to measure." Correction: the measurement found a runner bug and showed the files cost turns; both are worth knowing before you roll it out.
- Time and transition: 4 minutes. "What can you do with this on Monday?"

## Slide 53: Apply it Monday: State that survives a stop
**Block:** Section 2  **Time:** 2  **Diagram:** none
**On the slide:**
In your repository this week:
- Stop your agent mid-task, restart fresh
- Watch its first five tool calls
- Add `progress.md` and a two-owner handoff
- Write facts from git at every stop
Then measure:
- Count redone lines and migration heads
- Drop the files if nothing changes
**Visual:** A native checklist card, two groups, with a small arrow from "Then measure" back to the first group ("repeat").
**Speaker notes:**
- Explain: start with the experiment, not the files. Stop your agent halfway and see whether a fresh session finds the work by itself.
- Example: watch for `git status`, `git log`, or a look at `migrations/versions` in the first five calls. If they are there, your model may not need much more.
- Example: the facts part is a short script at the stop: `git log -3 --oneline`, `git status --short`, `alembic heads`, the visible test result, appended to the handoff and committed with explicit paths.
- Analogy: adding an on-call handover template only after you have seen a handover go wrong.
- Point at: "Then measure". The course's measure was redone lines (30% threshold), duplicate tables and heads.
- Ask the room: "Which state file would you keep for your model, and how would you measure it?" Expected answer: a handoff with machine facts, measured by redone work after a forced stop.
- Likely question: "Where is a starter?" Answer: `use-in-your-repo/` and Assignment 2, a state layer that survives three stops; run `make check-assignment-2` first.
- Misconception: "Ask the agent to write a summary at the end." Correction: write the facts from code; let the agent add notes.
- Time and transition: 2 minutes. "Questions."

## Slide 54: Q&A: State and session lifecycle
**Block:** Section 2  **Time:** 3  **Diagram:** none
**On the slide:**
Ask about anything:
- Concepts from today's sections
- How this applies to your work
- Implementation details
- Clarifications on what we covered
Quick Request
- Please do not mind if a question gets skipped accidentally
- Repost politely in chat if needed
- We will try our best to cover as many questions as possible
Remember: If you're wondering about it, others probably are too.
No Question Is Too Small Every Question Deserves an Answer!!
**Visual:** The template's Q&A layout and picture, unchanged.
**Speaker notes:**
- Collect questions from chat; park long ones for the assignment review session (Assignment 2 slot, 25 minutes).
- Ready answer, "Why 12 turns for session 1?": a pre-registered lever, the same for both arms, so the stop lands mid-feature; without `SESSION_BUDGET` session 1 gets the ticket's 20 turns.
- Ready answer, "Why did session 2 edit `app/api/issues.py`?": the state layer has no scope guard; Section 3 adds one. The referee's `diff_scope` row counted the edit anyway.
- Ready answer, "Does PASS mean the feature works?": no; read the hidden-test count next to it.
- Ready answer, "Why still use a stop if newer models need no resets?": to make the problem visible at a known point, the same for both arms.
- Point learners to `section-2-state-lifecycle/demo/README.md` and `session-notes.md`.
- Ask the room: "What is one line you would add to your own handoff file?" Expected answer: the current test status, or the migration head.
- Time and transition: 3 minutes. "Next: what the agent may change. Section 3 is a live A/B."

## Slide 55: Today's Agenda: Section 3, what the agent may change
**Block:** Section 3  **Time:** 1  **Diagram:** none
**On the slide:**
1 Instructions
2 State and session lifecycle
3 Scope and sandbox (current)
4 Verification
Final A/B
**Visual:** The template's agenda layout: five numbered boxes and connectors. Boxes 1 and 2 outlined as done; box 3 highlighted with the star; box 4 and Final pale.
**Speaker notes:**
- Explain: Sections 1 and 2 shaped what the agent knows and remembers. Section 3 limits what it may change and what it can reach.
- Example: the ticket is F4, version checks: an ETag on every issue, `If-Match`, and a 412 on a stale save, plus an issue history.
- Analogy: least privilege for a service account, applied to an agent: the files of one feature, inside one container.
- Point at: box 3. This is the one section with a live A/B, because the data before class showed a real gap.
- Ask the room: "Has an agent ever changed a file you did not ask it to touch?" Expected answer: most hands go up; config files, shared utils, lockfiles.
- Likely question: "Is the sandbox part of the comparison?" Answer: no. Both arms run in the same container; it is taught here but never the variable.
- Misconception: "Scope is about security." Correction: the scope layer is about keeping a change inside the ticket; the container is the security boundary.
- Time and transition: 1 minute. "Predict first. Poll."

## Slide 56: Live Zoom Poll: Will the bare arm leave scope?
**Block:** Section 3  **Time:** 4  **Diagram:** none
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 2 minutes to fill out the form.
Then, live A/B: `make demo-3 FEATURE=F4`
**Visual:** The template's poll picture. Under it, one command strip in monospace: `make demo-3 FEATURE=F4`.
**Speaker notes:**
- Poll question (Zoom, not on the slide): "Before class we ran this A/B 3 times. In how many runs did the bare arm change a file outside the ticket's allowed paths? A) 0 B) 1 C) 2 D) 3." Answer D comes on the "What we measured" slide.
- Say before the vote: "The harness arm is not in the question. Its scope layer refuses any edit outside the list, so its zero is built in."
- Close the poll, then terminal B: `make demo-3 FEATURE=F4`. Without `FEATURE=F4` it runs F3, a ticket with no gap.
- Browser tab 2: reload the run list, open the newest run, press `1`. `F` shows one arm full screen.
- Both arms run at once, each in its own container with the same limits. The harness arm has the instructions, state and scope layers; the bare arm has none.
- What to expect, from the timed run on 2026-10-17 (420 s agent limit, ran alone): bare verdicts at 5:15 and 8:06, harness at 8:50 and 11:18 on the console clock; command finished at 11 min 41 s; cost $0.048707. Expect exit 2: every harness arm before class ended `ABORTED: timeout`.
- While it runs: teach the next slides; around minute 1, screen 1 may show a `block` row for `app/services/errors.py` in the harness arm.
- If `x OpenAI refused the key`: fix `OPENAI_API_KEY`, `make doctor`, relaunch. If `x SHIPHARNESS_CLASS_DATE is not set`: run the date `sed` line from the instructor guide, relaunch.
- If an arm ends `ERROR` with `docker run failed`: `sudo systemctl start docker`, `make warm`, relaunch. If that fails, `make replay RUN=<fallback id>`; if Docker is down, walk the captured A/B in `section-3-scope-sandbox/demo/expected/` and say "recorded before class".
- If the run uses F3: `FEATURE=F4` was left out; Ctrl+C and relaunch with it.
- Clock: in this deck the launch lands about class 1:58 (run sheet: 2:03, one break after Section 2). Before class the A/B took 11 min 41 s alone and 15-17 min when two ran at once; either way it finishes before the demo slide at about 2:22.
- Time and transition: 4 minutes including the launch. "Here is the failure this section is about."

## Slide 57: Problem statement: A tidy diff in a shared file
**Block:** Section 3  **Time:** 3  **Diagram:** none
**On the slide:**
**Sam asks a coding agent for version checks on TeamTrack issues: an ETag, `If-Match`, a 412 on stale saves. The ticket lists the files to change (illustrative).**
The problem we're solving (in the real world)
The agent needs a new error class, so it:
- Follows the handbook to `app/services/errors.py`
- Edits a module every endpoint imports
- Passes the ticket's tests
- Gets a small diff approved
A month later the cost shows up:
- Another team changes the shared error mapping
- Version checks answer the wrong status
- Nobody links it to this ticket
- Every agent diff now needs a full review
**Visual:** Template slide-16 layout: bold framing line with TeamTrack in the accent colour, orange subheading, two bullet groups. No image.
**Speaker notes:**
- Explain: an illustrative scenario from the concepts page. The list of files was written down, but nothing checked it.
- Example, real: before class, in the S3 confirmation, every bare arm on F4 changed `app/services/errors.py`, which is not in the build phase's allowed paths. In one run it added a `PreconditionFailed` error class with status 412 there.
- Example: the handbook points to the shared errors module for every new error, so the agent is following a pattern. OpenAI: "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones."
- Analogy: a pull request that touches a shared library in a monorepo without the library owners in CODEOWNERS review.
- Point at: "Edits a module every endpoint imports"; that is where a small edit reaches other features.
- Ask the room: "Was adding the error class wrong?" Expected answer: not by itself; it was outside what the ticket allowed, so the owners of the shared module never reviewed it.
- Likely question: "Did the stray edit break anything in your runs?" Answer: no; existing tests kept passing (190 of 190) in every arm. The count measures scope, not correctness.
- Misconception: "A small diff is a safe diff." Correction: size says nothing about where the lines landed.
- Time and transition: 3 minutes. "Both arms read the same list. Why isn't that enough?"

## Slide 58: Scope: Is the ticket's file list enough? (build 1/2)
**Block:** Section 3  **Time:** 1.5  **Diagram:** none
**On the slide:**
What the agent may change
- The ticket lists the files to change
- Both arms read the same list
- Is the list enough to keep the agent inside?
**Visual:** Native frame as in template slides 25-27: three bullets, the last as the question in the accent colour. Right: a dashed box "allowed paths, build phase" with `app/services/issues.py`, `app/repositories/audit.py`, `app/web/**`; outside it `app/services/errors.py` with a "?".
**Speaker notes:**
- Explain: allowed paths are the globs a ticket lists for each phase: the files the agent may change then. A phase is one stage of a run: build writes the feature, test adds tests only.
- Example: F4's build list is the issue and audit API, services and repositories, `app/web/**` and `tests/visible/**`. `app/services/errors.py` is not on it.
- Analogy: a "staff only" sign versus a locked door.
- Point at: the file with the "?" outside the dashed box.
- Ask the room: "Is a list in the prompt enough?" Let them answer before the click. Expected answer: split; some trust the model to follow instructions.
- Likely question: "Does the bare arm see the list?" Answer: yes, in the same ticket text. The difference is only whether code checks it.
- Misconception: "If the model is told, it complies." Correction: wait for the next click.
- Time and transition: 1.5 minutes. Click.

## Slide 59: Scope: Is the ticket's file list enough? (build 2/2)
**Block:** Section 3  **Time:** 1.5  **Diagram:** none
**On the slide:**
Is the list enough to keep the agent inside? - Why not
- Text is a request; nothing checks it
  - The handbook points errors to `errors.py`
- "Less likely" is not "never"
  - JSON chosen as "less likely" to be overwritten
What can we use instead?
**Visual:** Same frame; "- Why not" in red bold after the question, two reasons with one nested example each, the closing question in the accent colour.
**Speaker notes:**
- Explain: a list in text makes a bad edit rarer; it does not make it impossible. Code has to check it.
- Example: Anthropic's long-running harness told its agent "It is unacceptable to remove or edit tests" and kept the feature list in JSON because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." "Less likely" is the point.
- Example: in our F4 runs, the same ticket text did not stop the bare arm in any of 3 runs.
- Analogy: "please don't push to main" in the team wiki versus a protected branch.
- Point at: the closing question.
- Ask the room: "Where would you enforce it: in the prompt, in review, or in the tool call?" Expected answer: in the tool call, before the write lands.
- Likely question: "Why not just review harder?" Answer: review comes after the cost; a refused patch never lands, and the agent learns the boundary at once.
- Misconception: "Strong wording in the prompt works like a rule." Correction: OpenAI's harness team names the alternative: "enforce boundaries centrally, allow autonomy locally."
- Time and transition: 1.5 minutes. "Four boundaries, one per slide."

## Slide 60: 1) One feature at a time: `feature_list.json`
**Block:** Section 3  **Time:** 3.5  **Diagram:** none
**On the slide:**
The harness writes one feature with `passes: false`. Only the harness sets it to true, from its own test run.
Why a JSON file:
- One feature, named in every session
- Off limits to the agent, every phase
- `evidence` and `testedAt` record the proof
- JSON is "less likely" to be overwritten
**Visual:** The feature entry, lines 4-14 quoted exactly from `section-3-scope-sandbox/demo/harness/feature_list.json` (key line marked):
```json
    {
      "id": "F4",
      "category": "feature",
      "description": "Optimistic concurrency (ETag, If-Match) and issue history",
      "steps": [
        "Optimistic concurrency (ETag, If-Match) and issue history"
      ],
      "passes": false,          <-- key line: only the harness sets this
      "evidence": null,
      "testedAt": null
    }
```
**Speaker notes:**
- Explain: the feature list is the scope. Anthropic's coding agent "was then asked to work on only one feature at a time"; the scope block in context names that one feature.
- Explain: in Anthropic's harness the agent edits the list "only by changing the status of a passes field". This course goes further: the agent may not edit it at all. It calls `finish`, and the harness sets `passes` after its own test run.
- Why: Anthropic's later harness: "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue." `evidence` and `testedAt` are the course's additions.
- Example: in the captured run, at 4:30 on the console clock the harness arm got `F4 passes: visible-tests at ...`: the harness set it, not the agent.
- Analogy: CI status on a pull request. The author cannot click "checks passed"; the CI system sets it.
- Point at: the `passes` line.
- Ask the room: "What goes wrong if the agent can set `passes`?" Expected answer: it can mark its own work done, the false "done" Section 4 is about.
- Likely question: "Why one feature, not the whole backlog?" Answer: the boundary is per feature; with one feature the allowed paths are one list.
- Misconception: "The feature list is a to-do list for the agent." Correction: it is graded state owned by the harness; the agent reads it and cannot write it.
- Time and transition: 3.5 minutes. "One feature, so one list of files per phase."

## Slide 61: 2) Allowed paths per phase, checked by code
**Block:** Section 3  **Time:** 4  **Diagram:** section-3-scope-sandbox/diagrams/scope-check-flow.png
**On the slide:**
Allowed paths are the globs a ticket lists for each phase: the files the agent may change then.
The scope check, every tool call:
- Patch: checked before it applies, `BLOCKED`
- Command: snapshot compared after, `REVERTED`
- Build phase: feature files and tests
- Test phase: `tests/visible/**` only
**Visual:** `scope-check-flow.png`: agent tool call → "path allowed in this phase?" → yes: workspace; no: BLOCKED (patch, nothing written) or REVERTED (command, restored from snapshot).
**Speaker notes:**
- Explain: a patch lists its paths, so it can be checked before anything is written; one refused path refuses the whole patch. A shell command can write anything, so the layer takes a byte snapshot before it runs and restores any file outside the list after.
- Example, real refusal text the harness arm read: "app/services/errors.py: outside the allowed paths for the build phase (...); patch not applied". The reason names the full list, so the agent learns where it may write.
- Example: after the refusal, every harness arm defined its 412 error in `app/services/issues.py`, a file on the list.
- Example: the test phase allows tests only, so the agent cannot make a failing test pass by changing the code.
- Analogy: branch protection plus CODEOWNERS, applied per tool call instead of per merge.
- Point at: the two "no" exits in the diagram.
- Ask the room: "Why check commands after they run, not before?" Expected answer: the command's text does not say which files it will write; `sed -i` or a code generator only shows up in the result.
- Likely question: "Did any run need a revert?" Answer: none of this demo's test runs; the agents changed files with `apply_patch`.
- Misconception: "This micromanages the agent." Correction: the agent still chooses how to build the feature and where inside the list; the harness only decides which files.
- Time and transition: 4 minutes. "That's the file boundary. The machine boundary is the container."

## Slide 62: 3) The sandbox boundary: where the keys live
**Block:** Section 3  **Time:** 3.5  **Diagram:** section-3-scope-sandbox/diagrams/sandbox-boundary.png
**On the slide:**
Every tool command runs in one container per arm. The agent loop and the API keys stay on the host.
Inside the container:
- `--network none`: loopback only
- Read-only root; `/work`, `/tmp` writable
- Same container for both arms
- Never the A/B variable
**Visual:** `sandbox-boundary.png`: host box (agent loop, API keys, harness) outside; container box inside (tool commands, `/work`), with network crossed out and only `/work` and `/tmp` writable.
**Speaker notes:**
- Explain: the model call and the keys live on the host; only tool commands run in the container. A bad command cannot reach the keys or the network.
- Example: with `--network none`, Docker's docs say "only the loopback device is created". No installs, downloads, or calls out.
- Example from a source: Anthropic's C compiler agents each had a container, and "Claude did not have internet access at any point during its development." The author advises "(Run this in a container, not your actual machine)", after seeing Claude "pkill -9 bash on accident, thus killing itself and ending the loop."
- Analogy: a CI runner: the job runs in a throwaway container; the deploy credentials are injected elsewhere, not left in the workspace.
- Point at: the keys sitting outside the container in the diagram.
- Ask the room: "Why can the sandbox never show up as a win in our A/B?" Expected answer: both arms get the identical container, so it is never what differs.
- Likely question: "Did the sandbox refuse anything before class?" Answer: no `sandbox_denied` event in any test run. It is there for the run that goes wrong.
- Misconception: "A container is a sandbox by default." Correction: only with the flags: no network, read-only root, non-root user, dropped capabilities, limits.
- Time and transition: 3.5 minutes. "Those flags are one principle: least privilege."

## Slide 63: 4) Least privilege: two refusals, two questions
**Block:** Section 3  **Time:** 3  **Diagram:** section-3-scope-sandbox/diagrams/least-privilege.png
**On the slide:**
"enforce boundaries centrally, allow autonomy locally." (OpenAI)
Grant only what the task needs:
- Non-root user, all capabilities dropped
- Memory, CPU, process and time caps
- Scope asks: in scope now? `blocked`
- Sandbox asks: possible at all? `sandbox_denied`
**Visual:** `least-privilege.png`: nested rings, from outside in: container limits (both arms), allowed paths for the phase (harness arm), the one feature. The two refusal labels on their rings.
**Speaker notes:**
- Explain: give the agent the smallest set of files, permissions and resources the task needs, and enforce it centrally. The agent keeps its freedom inside.
- Example, the class sandbox policy: `--user 1000:1000`, `--cap-drop ALL`, `--memory 1024m` with no swap, `--pids-limit 256`, 2 CPUs in the class profile, an agent time limit of 420 s for both arms.
- Example: the two refusals differ. `blocked` comes from the scope layer on the host, harness arm only, asking "is this file in scope now?". `sandbox_denied` comes from the container policy, both arms, asking "can this machine do this at all?".
- Analogy: IAM roles: a service account gets read on one bucket, not admin on the project.
- Point at: the inner ring; the scope boundary is the only part that differs between arms.
- Ask the room: "Which ring would have stopped the `errors.py` edit?" Expected answer: the allowed-paths ring; the container allows writes anywhere in `/work`.
- Likely question: "What if the list is wrong and the feature truly needs another file?" Answer: the agent has to work around it and the result can be worse; fix the list, not the guard.
- Misconception: "Least privilege is free." Correction: harness arms ran longer overall (median 302 s against 190 s, post hoc, all layers together); the block itself cost the agent one refused patch before it moved its error class to an allowed file.
- Time and transition: 3 minutes. "Four boundaries on one card."

## Slide 64: Cheat Sheet: Four boundaries for one feature
**Block:** Section 3  **Time:** 2  **Diagram:** none
**On the slide:**
- `feature_list.json`: one feature, harness sets `passes`
- Allowed paths: per phase; patch blocked, command reverted
- Sandbox: no network, keys on the host
- Least privilege: non-root, caps, two refusal types
Refer back to this slide when you scope your next agent task
**Visual:** A native four-row card, each row tagged "harness arm only" (rows 1-2) or "both arms" (rows 3-4). The refer-back line at the bottom.
**Speaker notes:**
- Explain: rows 1 and 2 are the scope layer, the A/B variable. Rows 3 and 4 are the container, identical for both arms.
- Example: the harness arm also sees the scope block in its context: "Files you may change in each phase", the build and test lists, and "A patch that touches any other file is rejected before it is applied."
- Analogy: the four checks a platform team runs before giving a contractor access: which repo, which paths, which machine, which permissions.
- Point at: the "harness arm only" tags.
- Ask the room: "Which row do you already have at work?" Expected answer: containers often; enforced per-task file lists rarely.
- Likely question: "Is the scope block in the prompt the thing that works?" Answer: the block tells; the check makes it true. The bare arm read the same list in its ticket.
- Misconception: "The sandbox and the scope layer do the same job." Correction: different questions, different arms.
- Instructor cue: section minute 25. If `make demo-3` has printed its `Cost:` line, read the session figure aloud; it decides one or two final features later ($1.10 rule).
- Time and transition: 2 minutes. "Both arms should be done or close. Let's look."

## Slide 65: Section 3 - Implementation Notes: Scope at work
**Block:** Section 3  **Time:** 6  **Diagram:** screenshot: section-3-scope-sandbox/demo/expected/screen-3-final.png
**On the slide:**
DEMO - 3
Section 3 - Implementation Notes: Scope at work
**Visual:** "DEMO - 3" badge; console screen 3, bare panel left, harness panel right. Callouts: (1) bare diff map, arrow to `app/services/errors.py` "changed"; (2) harness diff map, arrow to the same file "blocked"; (3) referee rows, arrow to `diff_scope: 1 new` vs `0 new`.
**Speaker notes:**
- Switch to browser tab 2, tonight's A/B from `make demo-3 FEATURE=F4` (terminal B, launched at the poll). Screen 3 (`3`) first, the middle column "Scope and sandbox": look for `changed app/services/errors.py` under bare and `blocked app/services/errors.py` under harness.
- Screen 3, right column: `diff_scope: 1 new` (bare) against `diff_scope: 0 new` (harness). Then "Sandbox denials: none" in both: the container refused nothing.
- Screen 1 (`1`): the harness decision row `block` with the reason the agent read. Both pills likely say FAIL: that is F4's own bar (every hidden test and every referee mutant), which every arm failed before class. Say so; the scope result is on screen 3.
- Screen 5 (`5`): "First wrong turn": in the capture, bare turn 1.14 edited `app/services/errors.py`; harness turn 1.12 was the blocked patch.
- Screen 2 (`2`): both boards own-org only; the referee's two-tab capture where tab B's stale save gets a 409 page.
- Screen 4 (`4`): F4 dots are hollow on F4's own measure. Say: "The scope count is on screen 3, not here."
- Say at a pass: "No file outside the ticket's paths." At a fail: "This arm changed a file it was not asked to touch." If tonight's bare arm stays in scope, say so: it is one more dot.
- If screen 3 lists a sandbox denial, show its reason code and command. If not, show the policy printout and say: "The sandbox is the same for both arms. It is taught here, but it is never the variable."
- If the harness arm is still running: it often ends late on the harness's own time limit; show the bare arm's screen 3 now and return.
- Fallback if the A/B broke for a reason outside the experiment: `make replay RUN=<fallback id>`, or walk `section-3-scope-sandbox/demo/expected/` (`screen-3-final.png`, then `screen-3-run-1.png` and `screen-3-run-2.png` for the other two runs), saying "recorded before class".
- What to say while the harness arm finishes: "It spends extra minutes on handoffs and the visible-test run that sets `passes`; the scope answer is already on screen 3."
- Time and transition: 6 minutes. "The same A/B on one timeline."

## Slide 66: What just happened: Same pull, two arms
**Block:** Section 3  **Time:** 3  **Diagram:** none
**On the slide:**
- 0:23 bare patches `app/services/errors.py`
- 1:16 harness patch to the same file: blocked
- 4:30 harness sets `passes` from visible tests
- 5:15 bare primary verdict
- 7:22 harness arm ends `ABORTED: timeout`
- 11:18 harness full verdict
**Visual:** A native two-lane timeline, console clock: bare lane on top (grey) with the 0:23 edit marked red; harness lane below (blue) with the 1:16 block marked as a stop sign. Verdict ticks: bare 5:15 and 8:06, harness 8:50 and 11:18. Caption: "Captured run 3, 2026-10-17, 420 s agent limit".
**Speaker notes:**
- Explain: the times of run 3 of the S3 confirmation, which ran alone. The console clock starts at the first run event, 18 s after launch; the command finished 11 min 41 s after launch and exited 2.
- Example: runs 1 and 2 ran at the same time and took 16 min 34 s and 15 min 22 s, so a busy machine stretches this a lot.
- Example: both arms felt the same pull within the first 76 seconds. Only the harness arm was stopped. The bare arm ended at 3:42 after 43 turns; the harness arm at 7:22 after 39 turns.
- Example: every harness arm ended on `HARNESS_TIMEOUT_S`, 120 s for the harness's own work (handoffs and the visible-test run that sets `passes`), not on the 420 s agent limit. Each still shipped a change, and the referee scored it.
- Analogy: the same commit pushed to two remotes, one with a pre-receive hook: same author, only one push is refused.
- Point at: 0:23 versus 1:16, the same file in both lanes.
- Ask the room: "What did the harness agent do right after it was blocked?" Expected answer: put its 412 error in `app/services/issues.py`, a file on the list.
- Likely question: "Is the harness timeout unfair to the harness arm?" Answer: it was recorded as an open item; raising it was not pre-registered, so it was not changed.
- Misconception: "ABORTED means the run is invalid." Correction: an aborted arm is judged on what it shipped; exit 2 is a result.
- Time and transition: 3 minutes. "Here is the method that decided that block."

## Slide 67: Under the hood: One method decides every path
**Block:** Section 3  **Time:** 5  **Diagram:** none
**On the slide:**
The refusal names the phase and the full list
**Visual:** Code excerpt, `platform/src/shipharness/harness/scope/guard.py` (lines 68-78), key line marked:
```python
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
        return f"{rel} is outside the allowed paths for the {self.phase} phase ({listed})"   # <-- key line
```
**Speaker notes:**
- Explain the order: `HARNESS_ONLY` first (`feature_list.json` and its schema), so no allow list can open them and the agent can never mark its own feature as passing. Then the state files, which belong to the agent in every phase. Then the phase's globs.
- Explain globs: `*` stays inside one folder; `**` spans folders.
- Example: the key line produces the text after `BLOCKED:` that the agent reads; in the capture, "app/services/errors.py: outside the allowed paths for the build phase".
- Example, the callers: `before_tool` in `scope/layer.py` (lines 156-167) runs `check_paths` over `patch_targets`, both header lines, renames and copies, and returns a `block` decision; `after_tool` (lines 177-183) compares byte snapshots and restores stray files, with no git involved.
- Example, the referee (`ab/referee.py`, lines 589-592): it strips harness files from the diff, then counts paths matching neither the build nor the test list. That count is `out_of_scope_files` and the `diff_scope` row, computed the same way for both arms.
- Analogy: a policy engine that returns a human-readable deny reason instead of a bare 403.
- Point at: the key line, then `HARNESS_ONLY`.
- Ask the room: "Why name the full list in the refusal instead of just saying no?" Expected answer: so the agent's next attempt lands inside the list in one turn.
- Likely question: "Can a rename sneak a file out?" Answer: `patch_targets` checks the new name too.
- Misconception: "The referee trusts the guard's log." Correction: it recomputes from the shipped diff, and runs on the bare arm, which has no guard at all.
- Time and transition: 5 minutes. "Now the honest numbers."

## Slide 68: What we measured: Scope held on F4, by construction
**Block:** Section 3  **Time:** 5  **Diagram:** section-3-scope-sandbox/diagrams/results-s3.png
**On the slide:**
Runs with a file outside the allowed paths:
- F4: bare 3 of 3, harness 0 of 3
- F3: bare 0 of 10, harness 0 of 10
What it does and doesn't prove:
- The guard blocks exactly what we count
- The bare arm's count is the finding
- Existing tests passed in every arm
- No arm met F4's own bar
**Visual:** `results-s3.png`: two dot panels. Left "F4, S3 confirmation": bare row 3 hollow dots (out of scope), harness row 3 filled. Right "F3, idempotency ticket": 10 filled dots in each row. Legend: filled = no out-of-scope file.
**Speaker notes:**
- Reveal the poll: answer D, all 3. The S3 confirmation was pre-registered before any of its runs: F4, the Section 3 stack, class profile, 3 A/Bs, and "harness ahead" only if the gap was not caused by harness-only timeouts. Result: harness ahead.
- F3, the section's own ticket, plain and with a tempting shared middleware: no arm ever left scope in 10 runs per arm, and every arm passed 49 of 49 hidden tests. Say plainly: "On F3, no measurable difference."
- Why the gap is partly by construction: the scope layer refuses exactly what `out_of_scope_files` counts, so the harness arm's zero is built in. What the runs show is that, on this ticket, the same agent with the same ticket and handbook edits a shared file every time nothing stops it.
- What it does not prove: that the stray file broke anything (existing tests 190 of 190 in every arm); that the harness built a better feature (hidden tests: bare 68 of 69 in each run, harness 68, 62 and 65; no arm met F4's own bar).
- Post hoc, descriptive only: in the earlier F4 pilot, bare arms left the allowed paths in 6 of 6 runs; median tests shipped were 15.5 for bare and 0 for harness. A guard that blocks everything would also score zero.
- When it earns its place: a shared file looks like the natural home for the change, the ticket's files can be listed as globs, and you need a guarantee, not a request.
- Analogy: a linter rule that bans an import will always show zero violations in the repo that runs it; the useful number is how often code without the rule violates it.
- Point at: the hollow bare dots on F4 next to the all-filled F3 panel.
- Ask the room: "What would you measure next to the guard, so a guard that blocks everything cannot look good?" Expected answer: hidden tests passed, existing tests kept green, tests shipped, time to done.
- Likely question: "Why did the bare arm stay in scope on F3 but not F4?" Answer: F4 needs a new error and the handbook points to the shared module; F3 did not pull it out.
- Misconception: "harness ahead on F4 means the harness built F4 better". Correction: it means no shipped file outside the list; on hidden tests the bare arms did as well or better (68 of 69 in every run).
- Time and transition: 5 minutes. "What to do with it on Monday."

## Slide 69: Apply it Monday: Scope your next agent task
**Block:** Section 3  **Time:** 2  **Diagram:** none
**On the slide:**
For your next agent task:
- Write the allowed paths as globs first
- Compare with `git diff --name-only` after
- Check patches before, commands after
- Keep grading files out of reach
For the runtime:
- Container, `--network none`, non-root
- Keys stay on the host
**Visual:** A native checklist card, two groups. A small terminal strip under the first group: `git diff --name-only` with one line in red outside the globs.
**Speaker notes:**
- Explain: start by counting, not blocking. Write the globs, run the agent, and count files outside them with `git diff --name-only`. That is the bare arm's number for your repo.
- Example: if the count is zero across several tasks, like F3, a guard adds little. If a shared module shows up again and again, like `errors.py` on F4, enforce it.
- Example: enforce in two places: before a patch applies, and after each command with a snapshot. A check on patches alone misses `sed -i` and generated files.
- Example: make the files that grade the agent (feature list, test fixtures for the referee) off limits in every phase, before any allow list is read.
- Analogy: turn on CODEOWNERS in report mode before you make it required.
- Point at: the red line in the terminal strip.
- Ask the room: "What is the first shared file your agent would reach for?" Expected answer: a utils module, a shared config, the error types, the lockfile.
- Likely question: "Where is a starter?" Answer: Assignment 3 (a diff-scope policy, a `passes` gate, a sandbox rule; run `make check-assignment-3` first) and `use-in-your-repo/`.
- Misconception: "Turn on the guard and you're done." Correction: say why in the refusal and name the allowed files, or the agent wastes turns guessing.
- Time and transition: 2 minutes. "Questions, then a break."

## Slide 70: Q&A: Scope and sandbox
**Block:** Section 3  **Time:** 2  **Diagram:** none
**On the slide:**
Ask about anything:
- Concepts from today's sections
- How this applies to your work
- Implementation details
- Clarifications on what we covered
Quick Request
- Please do not mind if a question gets skipped accidentally
- Repost politely in chat if needed
- We will try our best to cover as many questions as possible
Remember: If you're wondering about it, others probably are too.
No Question Is Too Small Every Question Deserves an Answer!!
**Visual:** The template's Q&A layout and picture, unchanged.
**Speaker notes:**
- Collect questions; park long ones for the review session (Assignment 3 slot, with the hidden-diff reveal).
- Ready answer, "If the harness scores zero by construction, why run an A/B?": for the bare arm's count; on F4 it left the list every run.
- Ready answer, "Why did both pills say FAIL?": they score F4's own bar, every hidden test and every mutant; the scope result is on screen 3.
- Ready answer, "What if the agent edits with `sed`?": the snapshot comparison after the command restores the file and the tool result ends with `REVERTED`.
- Ready answer, "Did the sandbox refuse anything?": no command in any test run; it is the same for both arms, so no run measures it.
- Point learners to `section-3-scope-sandbox/demo/README.md` and `session-notes.md`.
- Ask the room: "Who in your team owns the shared modules an agent might touch?" Expected answer: often nobody explicitly, which is the point.
- Time and transition: 2 minutes. "Break. Nothing runs during the break."

## Slide 71: Time for a Break
**Block:** Break  **Time:** 5  **Diagram:** none
**On the slide:**
A 5-minute break is starting now. Please return when the timer ends to continue the presentation
**Visual:** The template's break layout and timer picture. Write the return time next to the timer.
**Speaker notes:**
- Write the return time on the slide before you step away.
- Nothing runs during the break; do not launch any command.
- Check that terminal A (console) and terminal B are still up, and have terminal C ready for the final A/B.
- Section 4 opens with two polls: the Section 4 poll, then the final-feature poll (F5, F6 or F7); `make final FEATURES=` takes the winner first, then the runner-up.
- Return time: class minute 2:50, the start of Section 4 on the run sheet.
- Transition: "Welcome back. We know what the agent knows, remembers and may change. Now: what proves it is done."

## Slide 72: Section 4: What proves the work is done
**Block:** Section 4  **Time:** 1 min (2:50-2:51)  **Diagram:** none
**On the slide:**
Today's Agenda
1 Instructions
2 State and session lifecycle
3 Scope and sandbox
4 Verification
Final A/B
**Visual:** The template's agenda layout: numbered boxes joined by connectors, boxes 1-3 dimmed with a tick, box 4 "Verification" highlighted with the star, "Final A/B" as a last smaller box after it.
**Speaker notes:**
- Plain explanation: three layers done (what the agent knows, remembers, may change). The last one asks who decides that the work is finished.
- This section is about the agent's "done": the call `finish(claim="done")` and what we check before we believe it.
- Engineering example to preview: F4 on TeamTrack, optimistic concurrency on issue edits (`ETag`, `If-Match`, 412). It is the hardest ticket in the course.
- Analogy: a pull request that says "tested locally". Nobody merges on that sentence; CI and review decide.
- Point at box 4 and at the "Final A/B" box: the final A/B is launched inside this section and read at 3:40.
- Question for the room: "When did an agent last tell you it was done when it was not?" Expected answer: stories of green tests and a broken feature; take one or two.
- Likely learner question: "Is this just CI?" Answer: partly. The difference is when the checks run (at the done claim, while the agent still has context) and which checks it never sees.
- Misconception: "Verification means the agent runs the tests." Correction: the agent running tests is self-grading; this section moves the judgment out of the agent.
- Time: 1 minute. Transition: "Before I explain anything, two polls."

## Slide 73: Live Zoom Poll: F4 with all four layers
**Block:** Section 4  **Time:** 2 min (2:51-2:53)  **Diagram:** none
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 2 minutes to fill out the form.
**Visual:** The template's poll slide: heading, the one instruction sentence, and the poll picture. The question is in Zoom, not on the slide.
**Speaker notes:**
- Poll question (paste into Zoom): "Before class, both arms ran F4 in 7 A/Bs. A run passes only with all 69 hidden tests passing and all 4 referee mutants caught by its own tests. Which arm passed more runs?"
- Options: A) Harness arm. B) Bare arm. C) Both, equally often. D) Neither arm passed once.
- Answer (do not reveal now; it comes on "What we measured"): D. Both arms failed in all 7 A/Bs, 3 rounds: 3 of 3, 3 of 3, 1 of 1 failing per arm.
- Explain the two counts while the poll runs: hidden tests are tests the agent never sees; referee mutants are planted faults the agent never sees, and the arm's shipped tests must fail on each.
- Concrete hint, after the vote closes: a mutant that stops a write from moving the version brings back lost updates; only a test that checks the `ETag` moves, or that a stale save gets 412, catches it.
- Analogy: a code review that also asks "would your tests catch this bug if I planted it?"
- Question for the room after closing: "Why would the harness arm not win, with a gate on done?" Expected answer: guesses; park them until the measured slide.
- Likely learner question: "Why both counts at once?" Answer: passing tests says the feature works; caught mutants say the tests would catch a regression. The primary measure was registered before any run.
- Misconception: "More layers always score better." Correction: Sections 1 and 2 already showed no measurable difference on their tickets.
- Point at the instruction sentence while you read the two pass conditions aloud: all 69 hidden tests and all 4 mutants.
- Time: 2 minutes, close the poll before the launch. Transition: "Now the second poll: you pick the final A/B's feature."

## Slide 74: Live Zoom Poll: Pick the final A/B feature
**Block:** Final  **Time:** 1 min (2:53-2:54)  **Diagram:** none
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 1 minute to fill out the form.
Which feature runs as the final live A/B:
- F5 Bulk close: close many issues in one request
- F6 Watchers: follow an issue; work spans a session stop
- F7 Labels: tag issues, filter lists by label
**Visual:** The template's poll slide with the three options as three cards under the sentence: F5, F6, F7, each with a one-line plain description.
**Speaker notes:**
- Plain explanation: the final is the one live A/B of the whole stack, all four layers against the bare arm, on a feature neither arm has seen in class.
- F5 Bulk close: at the end of a sprint a team closes all finished work in one request, `POST /projects/{project_id}/issues/bulk-close`, with one audit row per request.
- F6 Watchers: users watch and unwatch issues; admins can add watchers for others. The work is split over a session stop, so the next session starts with an empty context and needs the handoff from Section 2.
- F7 Labels: teams tag issues with their own labels and filter issue lists by label. It also spans a session stop.
- Engineering point: F6 and F7 test the state layer again; F5 is a single session, closest to Section 4's gate.
- Analogy: picking which ticket goes into a canary release. You learn about the system, not about one ticket.
- Question for the room: "Which one do you expect the harness to help most?" Expected answer: F6 or F7, because of the session stop. Remind them Section 2 showed no measurable difference on its ticket.
- Likely learner question: "Why not run all three?" Answer: the session cap is $2.50. Run two features only if the session figure on the Section 3 `Cost:` line is $1.10 or less (instructor guide); otherwise run the winner alone.
- Misconception: "The final will settle which arm is better." Correction: one A/B is one dot; we read it next to the runs from before class.
- Point at the three cards: F6 and F7 carry a session stop, F5 does not.
- Time: 1 minute. Note the winner and the runner-up. Transition: "Two launches now: show-4 first, then the final."

## Slide 75: Launch: make show-4, the harness arm alone
**Block:** Section 4  **Time:** 1 min (2:54-2:55)  **Diagram:** screenshot: section-4-verification/demo/expected/show-4-screen-1-t03m.png
**On the slide:**
Terminal B: `make show-4`
Harness in action: one arm, not an A/B
Watch on screen 1:
- A blocked edit near minute 1
- `finish done`, then the gate pills
- The test phase and its filters
- The referee: hidden tests and mutants
**Visual:** The minute-3 screenshot, small, on the right. Callouts: arrow to the row of pending pills, label "the gate runs before the phase can end"; arrow to "Agent said done", label "the claim".
**Speaker notes:**
- Exact command, terminal B, repository root: `make show-4`. It runs `shipharness ab --section demo-4 --feature F4 --arms harness --profile class`. Outside class add `PURPOSE=pilot`.
- Then: reload the console run list at http://127.0.0.1:8765, open the newest run, press `1`. Keys: `1` Live, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces.
- Which screen when (captured run before class, 300 s agent limit; the class limit is now 420 s, so allow up to 2 minutes more): minute 1 screen 1, the scope layer blocks `app/services/errors.py`; minute 2-3, `finish done` and the gate pills; minute 3-4, every pill passes and the test phase starts; minutes 5-8, screen 3, the filters; minute 9, primary verdict; minute 11, full verdict.
- Timed before class: primary verdict 9:19, full verdict 10:55, cost $0.0265, cap $0.24.
- What to say while waiting: "This is not an A/B. The comparison on F4 was run before class; we read it later. Tonight we watch what the gate and the filters do."
- If it fails: `x OpenAI refused the key` means fix `OPENAI_API_KEY` and rerun `make doctor`; `x SHIPHARNESS_CLASS_DATE is not set` means set it in `.env` or add `PURPOSE=pilot`; `docker run failed` means `sudo systemctl start docker`, then `make warm`; port in use means `make console CONSOLE_PORT=8766`.
- `ABORTED: timeout` is a result, not a failure: the arm is still judged. Exit 2 means an arm hit a time or cost limit.
- Fallback: if a failure comes from outside the experiment (Docker, network, OpenAI account), say so and walk the captured run in `section-4-verification/demo/expected/` (screenshots plus `terminal.txt`); `make replay RUN=<fallback id>` only after an `ERROR`.
- Analogy: starting a long CI job and then teaching while it runs; we come back to the result.
- Load: the final runs at the same time. Two S3 A/Bs run at once took 15-17 min against 11 min 41 s alone, so expect show-4's full verdict nearer 3:10 than 3:06; the demo slide is at 3:15.
- Time: 1 minute, class 2:54-2:55. Transition: "One more launch, in terminal C: the final."

## Slide 76: Launch: make final, the poll winner first
**Block:** Final  **Time:** 1 min (2:55-2:56)  **Diagram:** docs/diagrams/ab-referee.png
**On the slide:**
Terminal C: `make final FEATURES=F6,F5`
- Poll winner first, runner-up second
- Bare arm against all four layers
- Same ticket, model, caps, one referee
- Read in the final block, at 3:40
**Visual:** The A/B referee diagram, full frame: one checkpoint, two arms in their own containers, one referee scoring both. No callouts.
**Speaker notes:**
- Exact command, terminal C: `make final FEATURES=<winner>,<runner-up>`, for example `make final FEATURES=F6,F5`. Always pass `FEATURES`: the default is `F5,F6`.
- Two features only if the Section 3 `Cost:` line showed a session figure of $1.10 or less; otherwise one feature. At the caps one feature costs at most $0.58.
- Then open the newest run in browser tab 3 and go back to tab 2 (show-4). The features run one after another, so at most one A/B and one harness-in-action run are live at a time.
- Timing: the timed F5 run before class took 12 min 47 s to the cost line; bare verdicts at 3:27 and 6:50, harness at 9:48 and 12:32. F6 was not timed as a final before class, so do not promise a finish time; it has two build sessions.
- What to say while waiting: "Both arms get the same ticket, model, tools, sandbox, turn budgets, and cost cap. One referee scores both. We come back to it at 3:40."
- Point at the diagram: two arms, one referee. The referee works on a fresh copy plus each arm's diff, so neither arm can touch the scoring.
- Analogy: an A/B test in production; same traffic, same metric, one variable changed.
- If it fails: wrong feature started means Ctrl+C in terminal C and launch again; `Error 2` after the results means an arm was aborted on time or cost, and the run is judged.
- Fallback: walk the captured final in `final-project/expected/` (screens 1 to 5 and the terminal lines in `final-project/README.md`).
- Two features run one after another: at the F5 pace (12 min 47 s) both finish around 3:21-3:30, before the final block at 3:40; F6 has two build sessions and may run longer, so read whatever has finished.
- Time: 1 minute, class 2:55-2:56. Transition: "While both run: the story of F4."

## Slide 77: The problem: Done, but two edits still collide
**Block:** Section 4  **Time:** 3 min (2:56-2:59)  **Diagram:** docs/diagrams/optimistic-concurrency.png
**On the slide:**
**Ticket F4: stop lost updates on issue edits, with an `ETag` and an `If-Match` check.**
What the agent did:
- Added the header check to three endpoints
- Wrote a happy-path test
- Ran the suite: all green
- Reported "Done, the full suite passes"
Why every check approved it:
- `If-Match` is optional, so old tests pass
- No existing test sends a stale header
- Review saw green CI and a confident summary
- After release, two editors still overwrite each other
**Visual:** The optimistic-concurrency diagram: tab A and tab B both read `ETag: "3"`; A saves with `If-Match: "3"` and the version becomes 4; B saves with the stale `If-Match: "3"` and should get 412 and change nothing. Mark B's arrow red with "lost update if the check is wrong".
**Speaker notes:**
- Plain explanation: F4 asks for optimistic concurrency. `GET /issues/{id}` returns `ETag: "<version>"`; a write with a stale `If-Match` must return 412 `precondition_failed` and change nothing; every successful change moves the version up by one.
- The scenario on the slide is illustrative (the repo labels it so). The real version from before class is on the next slide: a bare arm claimed done on F4 with a failing hidden test.
- Engineering detail: the header is optional on purpose, so existing clients keep working. That is exactly why the old suite stays green whether the check works or not.
- Check order in the spec: 401, 403, 404, then 412, then 422. A stale `If-Match` with an invalid body must give 412, not 422. Remember this; it comes back in the demo.
- Point at the diagram: walk tab A, then tab B. Ask where the lost update happens: at B's save, when the server does not compare versions.
- Analogy: a code review that approves "tests pass" when the tests never exercise the changed branch. Coverage of the happy path, not of the race.
- Question for the room: "Which test would have caught this?" Expected answer: two writers, the second with the old version, expecting 412 and no change.
- Likely learner question: "Isn't this just a bad test suite?" Answer: yes, and the agent wrote the suite it then graded. That is the cause we fix.
- Misconception: "The agent lied." Correction: the concepts page puts it plainly: nobody lied; the agent checked what it could see, and what it could see was not the feature.
- Time: 3 minutes. Transition: "Here is what really happened before class."

## Slide 78: Verification: The suite is green. Is F4 done? (build 1/2)
**Block:** Section 4  **Time:** 1 min (2:59-3:00)  **Diagram:** none
**On the slide:**
A bare arm on F4, before class:
- Visible suite: 191 passing
- Its claim: "Verified the complete visible suite"
- `finish(claim="done")`
Is F4 done?
**Visual:** A fixed frame: on the left a green terminal box "191 passed"; on the right a speech bubble with the claim; under them a large "?" box. Step 2 keeps the frame and fills the box.
**Speaker notes:**
- This is real: in the class-profile round, the bare arm ended its build with the claim text "Verified the complete visible suite (191 passing)".
- Plain explanation: the agent ran every test it could see, they passed, and it called `finish(claim="done")`. In the bare arm, that call ends the phase.
- Ask the room before revealing: "Is F4 done? Hands up for yes." Expected answer: most say "probably" or "we can't tell"; that second answer is the right instinct.
- Engineering example: the same pattern as a PR with a green check where the CI job only runs unit tests for unchanged modules.
- Analogy: a smoke test that only hits `/health`: green, while the checkout page is broken.
- Point at the "?" box: the question is who answers it, not only what the answer is.
- Likely learner question: "191 tests is a lot. Isn't that enough?" Answer: count says nothing about which behaviour they check; none of them sends a stale header with an invalid body.
- Misconception: "Green suite equals done." Correction: Anthropic's compiler team: "it is easy to see tests pass and assume the job is done, when this is rarely the case."
- Time: 1 minute. Transition: click to the answer.

## Slide 79: Verification: The suite is green. Is F4 done? (build 2/2)
**Block:** Section 4  **Time:** 2 min (3:00-3:02)  **Diagram:** none
**On the slide:**
A bare arm on F4, before class:
- Visible suite: 191 passing
- Its claim: "Verified the complete visible suite"
- `finish(claim="done")`
**No: the referee failed it, 68 of 69 hidden tests**
Why not:
- The visible suite missed a combined case
  - stale `If-Match` plus invalid body: 412 expected
- The agent graded its own work
  - nobody else checked the claim
Who should decide "done"?
**Visual:** Same frame as build 1/2. The "?" box becomes a red box "No: 68 of 69 hidden tests". The two reasons appear under it with their nested examples; the closing question at the bottom in blue.
**Speaker notes:**
- The failing hidden test was `test_invalid_body_with_a_stale_version_is_412`. Both arms of that A/B failed the same test.
- Plain explanation of reason 1: each piece works alone (the `ETag`, the header check, the validation). The bug appears only when they meet: validation ran before the version check.
- SpecBench names this shape: "compositional failures account for a much larger fraction of reward hacking behavior" than deliberate exploits.
- Plain explanation of reason 2: the agent wrote the tests, ran them, and judged the result. Anthropic's harness team: "agents reliably skew positive when grading their own work."
- Concrete engineering example: this was the one done claim in the whole pilot that came with a failing hidden test. It came in the class-settings round, after the 34-run post hoc count, which had none (0 of 19 bare claims, 0 of 10 harness).
- Analogy: a developer approving their own pull request. Usually fine; when it is not, nobody notices.
- Question for the room: "Who should decide done?" Expected answer: something the agent does not control: a gate, CI, a second reviewer, tests it never saw. Write their answers down; the next four slides map to them.
- Likely learner question: "Would a second LLM fix this?" Answer: partly. A3 says separating doer and judge is "a strong lever", but "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs."
- Misconception: "This is reward hacking, the agent gamed the tests." Correction: no sign of deliberate gaming; it is an untested combination.
- Point at the red box: 68 of 69 means one hidden test, a case the agent's own 191 tests never exercised.
- Time: 2 minutes. Transition: "Four ideas answer that question. First, why self-grading fails."

## Slide 80: 1) Self-grading and visible tests
**Block:** Section 4  **Time:** 3 min (3:02-3:05)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-1.png
**On the slide:**
The agent writes the tests, runs them, and grades the result.
Two gaps:
- Agents "reliably skew positive" grading themselves
- Every agent saturates the visible suite
- Held-out tests still find failures
- Mostly features that fail only combined
**Visual:** Pipeline build frame 1: "Agent, build phase" with the visible tests inside its box, an arrow "finish done" straight to "Shipped diff". Nothing between the claim and the ship. A dashed box outside the agent's reach labelled "hidden tests (not yet used)".
**Speaker notes:**
- Plain explanation: in the bare arm the agent is author, tester, and judge. The visible suite is the only evidence, and the agent chose what went into it.
- Source 1, Anthropic, Harness design: "agents reliably skew positive when grading their own work."
- Source 2, SpecBench (Weco AI): "while every frontier agent saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout suites."
- Source 3, Anthropic, C compiler: "it is easy to see tests pass and assume the job is done, when this is rarely the case."
- Engineering example: F4's visible suite passed 191 tests in the bare arm's run; the held-out suite of 69 caught the one combination it missed.
- Analogy: grading your own exam with your own answer key. You will agree with yourself.
- Point at the diagram: the arrow from "finish done" to "Shipped diff" has nothing on it. Each of the next three ideas adds a box on that arrow.
- Question for the room: "Where is the visible suite in your repo, and who writes most of the new tests now?" Expected answer: in the repo, and more and more the agent; so the agent writes its own exam.
- Likely learner question: "Why not just show the agent more tests?" Answer: then they are visible tests too, and become a target. Held-out checks only measure while they stay held out.
- Misconception: "A smarter model fixes self-grading." Correction: SpecBench found the gap in every frontier agent it tested; the fix is structural, not a better prompt.
- Time: 3 minutes. Transition: "If the agent writes tests, which ones do we keep?"

## Slide 81: 2) Test-phase filters: keep tests that prove something
**Block:** Section 4  **Time:** 3 min (3:05-3:08)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-2.png
**On the slide:**
After the build, a short test phase. Each proposed test must pass five filters, cheapest first:
1. Collects with no errors
2. Passes five runs in a row
3. Adds coverage, or catches a new mutant
4. Real assertions, no mock of the code
5. No source file changed
**Visual:** Pipeline build frame 2: adds "Agent, test phase" after the build, then a funnel "Five test filters" with "kept tests" going to "Shipped diff". A small side note on the funnel: "1-3 TestGen-LLM, 4-5 course".
**Speaker notes:**
- Plain explanation: a generated test can fail on correct code, pass by luck, or pass without checking anything. Each filter removes one of those.
- Source: Meta's TestGen-LLM keeps a test only after "a series of progressively demanding semantic filters". Filter 2 quotes it: "a test that does not pass on every one of five executions is deemed flaky."
- Filters 1 to 3 come from TestGen-LLM (filter 3's mutant branch from Meta's ACH). Filters 4 and 5 are the course's own, with no source sentence: they stop a test that asserts nothing or mocks the code it claims to test, and a test phase that edits the code until its test passes.
- Engineering example from the captured demo run: 4 proposed tests, 1 kept. One was discarded at filter 2 with "failed on run 1 of 5: assert 422 == 412".
- Analogy: CI gates on a pull request: lint, flaky-test quarantine, coverage diff. Same idea, applied to tests the agent wrote.
- Point at frame 2: the funnel narrows; only kept tests ship.
- Question for the room: "Why run the cheapest filter first?" Expected answer: most tests fail early, so you avoid five runs and coverage on tests that do not even collect.
- Likely learner question: "Does filter 3 just reward coverage?" Answer: no; a test that adds no coverage is still kept if it catches a mutant no existing test catches. Next slide.
- Misconception: "Filtered tests prove the code is correct." Correction: filters treat the current code as correct; a failing test is discarded even when the test is right. Remember the 422.
- Time: 3 minutes. Transition: "So how do we know the kept tests would catch anything?"

## Slide 82: 3) Mutation testing and hidden tests
**Block:** Section 4  **Time:** 3 min (3:08-3:11)  **Diagram:** section-4-verification/diagrams/mutation-testing.png
**On the slide:**
**Mutant:** a copy of the code with one small planted fault. A test that fails on it catches it.
Two held-out checks, owned by the referee:
- Hidden tests: does the feature work?
- Referee mutants: would your tests notice?
- Two mutant sets that never overlap
- Neither is in the agent's workspace
**Visual:** The mutation-testing diagram: original line and mutated line side by side (for F4: a write that no longer moves the version); the shipped tests run on both; "fails on mutant = caught", "passes on mutant = survived". Under it, two boxes: "filter set (filter 3)" and "referee set (scoring)", with "no shared mutation" between them.
**Speaker notes:**
- Plain explanation: coverage says a line ran. A mutant asks whether a test would notice that line going wrong.
- Source, Meta's ACH: about half of tests that catch a new mutant add no line coverage; the paper's figure is 49%. That is why filter 3 has a mutant branch.
- Engineering example for F4: a mutant that stops a write from moving the version brings lost updates back. A test catches it only if it checks that the `ETag` moves, or that a stale save gets 412.
- Course design: hand-written mutants, not a mutation tool, so they target chosen lines. A filter set feeds filter 3; a separate referee set scores the run; they share no mutation.
- Hidden tests: 69 for F4, never shown to the agent. SpecBench uses held-out tests "never shown to the agent" and "used solely for evaluation"; the course does the same.
- Analogy: a fire drill. You do not test the alarm by reading its manual; you light a small, controlled fire.
- Point at the two boxes: the filter set helps pick tests; the referee set judges them. If they overlapped, the agent's filters would be tuned to the exam.
- Question for the room: "Why does a test that fails everywhere not count as catching a mutant?" Expected answer: it catches everything and proves nothing; the referee counts a catch only with shipped tests that pass on the unmutated build.
- Likely learner question: "Can I do this without a fancy tool?" Answer: yes; write one planted fault for your riskiest line by hand, run the suite, and if nothing fails you found a test to write.
- Misconception: "Mutation testing finds existing bugs." Correction: ACH: it "cannot detect existing faults residing in the code base"; it protects against regressions.
- Time: 3 minutes. Transition: "Last piece: who decides the claim."

## Slide 83: 4) The gate on "done" and the separate referee
**Block:** Section 4  **Time:** 3 min (3:11-3:14)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-3.png
**On the slide:**
`finish(claim="done")` starts a check, not the end of the phase.
The verify gate runs:
- Visible and existing tests
- House rules R1 to R7, board check
- Clean state: committed, lint, one migration head
- Any failure: "Not accepted", fix and retry
The referee scores later, in its own container.
**Visual:** Pipeline build frame 3, the full pipeline: "Verify gate, in the arm's container" between "finish done" and the test phase, with a red return arrow "refused: first 3 failures"; at the end "Referee, own container: hidden tests + referee mutants" and "Primary verdict". The gate and the referee boxes in different colours.
**Speaker notes:**
- Plain explanation: in the harness arm, `finish(claim="done")` runs the gate. If any item fails, the result of `finish` is "Not accepted." plus up to three failure lines and "Fix these, commit your work, and call finish again." The phase goes on.
- Only a passed gate lets the scope layer set `passes` to true in `feature_list.json`. The agent cannot mark its own feature done.
- Sources: A3, "Separating the agent doing the work from the agent judging it proves to be a strong lever"; A4, "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem"; A2's clean state, code "appropriate for merging to a main branch". The composition into one gate is course design.
- The separate referee: a different program, its own container, after the agent stops. A blinded model reviewer also reads both final diffs; its verdict is secondary.
- Engineering example: in the captured demo run the gate passed every item on the first claim, with 190 visible tests, and the referee still failed the run.
- Analogy: CI as a required status check plus a separate QA sign-off. The developer cannot merge past CI, and CI is not QA.
- Point at the red return arrow: feedback arrives while the agent still has the context, not hours later in a PR.
- Question for the room: "Why not put the hidden tests in the gate? It would catch more." Expected answer: once the agent gets feedback from a check, the check becomes a target and stops measuring held-out behaviour.
- Likely learner question: "The gate and the referee both run R1 to R7. Is that fair?" Answer: a disclosed overlap; the harness arm should do better on R1 to R7 by construction, so the primary measure uses hidden tests and mutants only.
- Misconception: "The gate makes the agent correct." Correction: it makes the claim checked. A gate on wrong checks makes the agent solve the wrong problem faster.
- Time: 3 minutes. Transition: "All four on one sheet."

## Slide 84: Cheat Sheet: four checks the agent does not own
**Block:** Section 4  **Time:** 1 min (3:14-3:15)  **Diagram:** section-4-verification/diagrams/verification-pipeline.png
**On the slide:**
| Check | When | Asks |
|---|---|---|
| Verify gate | At the done claim | Tests, rules, clean state pass? |
| Test filters | After the test phase | Runs, stable, adds something? |
| Hidden tests | After the agent stops | Works in combination? |
| Referee mutants | After the agent stops | Would the tests notice? |
**Visual:** The complete verification-pipeline diagram above a four-row native table. Each table row has the colour of its box in the diagram.
**Speaker notes:**
- Plain explanation: four checks, each owned by someone other than the agent. Two give feedback to the agent (gate, filters); two never do (hidden tests, mutants).
- The split matters: feedback checks shape behaviour; held-out checks measure it. You need both, and you must not mix them.
- Engineering example: map to your own stack. Gate = a pre-merge hook the agent triggers; filters = rules for accepting generated tests; hidden tests = a contract suite in a separate repo; mutants = a few planted faults on your riskiest lines.
- Analogy: a restaurant kitchen: the cook tastes while cooking (gate, filters); the inspector arrives unannounced with their own checklist (hidden tests, mutants).
- Point at the "When" column: one check at the claim, one after the test phase, two after the agent stops.
- Question for the room: "Which of these four could your agent currently see or edit?" Expected answer: the CI config, often; a held-out suite usually does not exist, so nothing is out of reach.
- Likely learner question: "Which one is cheapest to add?" Answer: the gate, because it reuses checks you already run; mutants by hand cost minutes per risky line.
- Misconception: "Held-out checks are only for research." Correction: a contract suite the agent's repo cannot see is a held-out check; many teams already have one.
- Section minute 25: check terminal B for the show-4 `Cost:` line and terminal C for the final.
- Time: 1 minute. Transition: "Let's see the finished run."

## Slide 85: Section 4 - Implementation Notes: The gate at work
**Block:** Section 4  **Time:** 6 min (3:15-3:21)  **Diagram:** screenshot: section-4-verification/demo/expected/show-4-screen-1-final.png
**On the slide:**
DEMO - 4
Section 4 - Implementation Notes: The gate at work
**Visual:** The template's DEMO layout: "DEMO - 4" badge, title, and the screen-1 screenshot after the full verdict. Callouts: (1) arrow to the row of green gate pills, "gate: every item passed"; (2) arrow to "Agent said done", "the claim"; (3) arrow to "primary verdict ready: FAIL, hidden tests passed 68, mutants killed 0", "the referee disagrees".
**Speaker notes:**
- Switch to browser tab 2, the run of `make show-4` launched in terminal B at 2:54. Press `1` for the live screen. If the run is still going, screen 1 shows "primary verdict ready" as soon as the first check is done; work from what is there.
- Screen 1, in order: harness notes from all four layers; turn 1.15 blocked by the scope layer; `finish done`; the 11 gate pills of the build phase (visible tests, existing tests, R1 to R7, board, clean state: `names` in `run_gate`, `gate.py`); then the referee lines.
- Say at the verdict: "The agent said done. The hidden tests and mutants say no." If tonight's run passes: "Every hidden test and every mutant. The work is done."
- Then press `3`, Evidence: the Verification panel has the filter table, one row per proposed test, a mark per filter, the reason per discard. Read the filter 2 reason aloud: "assert 422 == 412".
- Then press `2`, Boards: the two-tab conflict panel. Tab A saves, tab B saves from a stale form, tab B gets HTTP 409 and a "changed by someone else" page. The board stops the lost update; one hidden test still fails.
- Then press `4`, A/B Report: one dot per run before class. Say: "Tonight's run is not a dot in the comparison."
- What to say while switching: "The gate checks what the agent can see. The hidden tests and the referee's mutants stay out of its reach."
- If no gate pills appear: the agent never claimed done; show the filter table and the referee counts instead. If every pill fails with `check runner failed`: the harness time limit ran out during the gate; keep the run and say so.
- Fallback: if the live run broke for a reason outside the experiment, open the screenshots in `section-4-verification/demo/expected/` (screen-1 final, screen-3 final, screen-2 final, screen-4 final) and the arm line in `terminal.txt`.
- Time: 6 minutes. Transition: "Let's put the eleven minutes on a timeline."

## Slide 86: What just happened: eleven minutes of show-4
**Block:** Section 4  **Time:** 4 min (3:21-3:25)  **Diagram:** screenshot: section-4-verification/demo/expected/show-4-screen-1-t01m.png (+ t03m, t04m, t09m)
**On the slide:**
- 0:55 scope layer blocks `app/services/errors.py`
- 2:18 `finish done`, gate pills pending
- 3:24 gate passes every item, 190 visible tests
- 5:51-8:34 filters: 4 proposed, 1 kept
- 8:34 run ends, `ABORTED: timeout`, 43 turns
- 9:19 primary verdict: FAIL
- 10:55 full verdict: hidden 68/69, mutants 0/4
**Visual:** A horizontal native timeline with the seven marks; four screenshot thumbnails above it at 0:55, 2:18, 3:24 and 9:19. The 3:24 mark green, the 9:19 mark red, so the green gate and the red verdict stand out. Caption: "captured before class, 300 s agent limit".
**Speaker notes:**
- These times are the captured run before class (300 s agent limit then; 420 s tonight). Compare with tonight's run aloud: earlier or later, same order of events.
- 0:55: the agent tried to patch `app/services/errors.py`, outside the build list. The scope layer from Section 3 refused it. The bare arms changed that same file in every F4 confirmation run.
- 2:18 to 3:24: the claim, then the gate. All items passed on the first try. Only then was `passes` set and the test phase started.
- 5:51 to 8:34: the test phase proposed 4 tests. The kept one was `test_stale_or_malformed_if_match_refuses_without_mutation`.
- The discarded one that matters: `test_precondition_order_history_order_and_isolation` asserted that a stale `If-Match` with an invalid body gives 412, and got 422. The test was right; the code was wrong; filter 2 discarded it because it failed.
- 9:19: the hidden test that failed is the same case, `test_invalid_body_with_a_stale_version_is_412`. The kept test caught 0 of 4 referee mutants (3 survived, 1 ended in an error).
- Cost of the whole command: $0.026511, finished at 11:06.
- Analogy: a postmortem timeline. The interesting moment is 5:51-8:34: the agent found the bug, and our own filter threw the evidence away.
- Question for the room: "Was the agent's 422 test wrong?" Expected answer: no; it expected the spec's 412. Filters assume the current code is correct.
- Likely learner question: "Then why keep filter 2?" Answer: it removes flaky and wrong tests far more often than it removes right ones; the fix is to read every discard reason, not to drop the filter.
- Misconception: "The gate failed." Correction: the gate did its job; its job does not include the held-out checks.
- Point at the green 3:24 mark next to the red 9:19 mark: same run, the gate said yes, the referee said no.
- Time: 4 minutes. Transition: "Here is the code that made the gate's decision."

## Slide 87: Under the hood: the gate's verdict in six lines
**Block:** Section 4  **Time:** 5 min (3:25-3:30)  **Diagram:** none
**On the slide:**
- One failed item fails the gate
- Feedback: summary, first three failures, next step
- Checks run on a copy, in the arm's container
- Not in the check list: hidden tests, referee mutants
**Visual:** The code excerpt, quoted exactly from `section-4-verification/demo/walkthrough.md`, line 2 (`passed = ...`) highlighted as the key line:
```python
# platform/src/shipharness/harness/verify/gate.py (lines 176-181)
    passed = not any(i.status == "fail" for i in items)
    feedback = "" if passed else _feedback(gate_id, items, lines)
    result = GateResult(gate_id=gate_id, items=items, passed=passed, feedback=feedback)
    if on_update:
        on_update(result)
    return result
```
**Speaker notes:**
- Plain explanation: `items` holds one result per gate item. One `fail` and the whole gate fails. No weighting, no "mostly passed".
- Why that strict: A4, "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."
- `_feedback` (lines 191-200) writes "Gate <id>: <n> of <m> items failed (<names>).", the first three failure lines, and "Fix these, commit your work, and call finish again." A4 again: the harness "should not print thousands of useless bytes", and errors carry the reason on the same line.
- The runner turns a failed gate into the `finish` result "Not accepted." plus that text (`runner/loop.py`, lines 291-300). A passed gate is stored in the run state; the scope layer reads it and only then sets `passes`.
- Earlier in `run_gate` (lines 155-162): pending pills go out first, so the console shows the gate running; then the workspace is copied to `/tmp`, so the checks cannot change the agent's files. `cfg.limit` caps each command by the harness time left.
- What is left out is the point: `GATE_CHECKS` (lines 33-43) lists R1 to R7, `regression`, `board`. No hidden tests, no referee mutants, so they stay held out.
- Engineering example: the same pattern as a required CI status that posts its first three failures as a PR comment, so the author fixes them without reading the whole log.
- Analogy: a pre-merge hook that refuses the push and tells you exactly which three things to fix.
- Question for the room: "What happens if one gate check is flaky?" Expected answer: the agent burns turns fixing nothing; a gate is only as good as its least reliable check, so flaky checks must be fixed or removed first.
- Likely learner question: "Why only three failures?" Answer: context budget; the agent fixes three, calls finish again, and sees the next ones.
- Misconception: "This needs shipharness." Correction: any script that runs your checks on a copy and returns a short failure summary as the answer to "done" is the same gate.
- Point at the highlighted `passed =` line: it tests for "fail" only, so an item marked "skipped" does not fail the gate.
- Time: 5 minutes; the walkthrough reads all 38 lines. Transition: "Did it help? Here is what we measured."

## Slide 88: What we measured: no measurable difference on F4
**Block:** Section 4  **Time:** 4 min (3:30-3:34)  **Diagram:** section-4-verification/diagrams/results-s4.png
**On the slide:**
Primary measure: all 69 hidden tests and all 4 referee mutants.
Runs failing, bare / harness:
- Medium effort, round 1: 3 of 3 / 3 of 3
- Medium effort, round 2: 3 of 3 / 3 of 3
- Class settings: 1 of 1 / 1 of 1
Earns its place when:
- The agent can claim done too early
- Checks are cheap, exact, partly held out
**Visual:** The results-s4 dot chart: one dot per run, bare grey and harness blue, filled = passed, hollow = failed. Every dot hollow in both arms. No percentages.
**Speaker notes:**
- Reveal the poll: answer D. Neither arm passed once, in 7 A/Bs: no measurable difference on this task with this model.
- Say it plainly: the harness did not win here. The registered gate for larger batches needed the harness ahead in 3 of 4 sections; it was ahead in none, so the batches of 10 runs per arm and the leave-one-out ablation were not run.
- Why the gate barely mattered: no F4 harness arm claimed done in those 7 A/Bs. Six used all their build turns, one stopped `not_done`. A gate on the claim never ran.
- Two bare arms claimed done, and the referee failed both (one with 69 of 69 hidden tests and a surviving mutant, one with 68 of 69). The reviewer rejected all 14 arms and agreed with the referee each time.
- Post hoc, chosen after the results, descriptive only: harness arms shipped fewer tests (median 0 against 15.5 on F4), and both arms hit the agent time limit in 4 of 6 F4 runs. Across all sections harness arms claimed done in 10 of 34 runs, bare in 19 of 34.
- When it earns its place (concepts page): the agent can claim done before the work is done; your checks are cheap and exact; some checks stay out of the agent's reach; the agent writes tests you will keep.
- When it does not: the agent never claims done; the bug is in the code and the test is right (filter 2 discards it); few tests are proposed; the checks themselves are wrong.
- Analogy: a smoke detector in a room nobody entered. It did not fail; it was never tested.
- Question for the room (the run sheet's discussion): "What would a gate need to catch to earn its turns on this model?" Expected answer: the bare arm's false done claims; a held-out-style check such as a two-writer test; fewer turns spent before the claim.
- Misconception: "No difference means verification is useless." Correction: A3, a separate judge "is worth the cost when the task sits beyond what the current model does reliably solo"; this result is about F4 with this model, measured a few times per arm.
- Point at the two rows: every dot hollow, in both arms, in all three rounds.
- Likely question: "Why not rerun with more turns so the harness reaches its gate?" Answer: that would be a new registered experiment; changing settings after seeing the result is how a harness gets made to look good.
- Time: 4 minutes. Transition: "What to do with this on Monday."

## Slide 89: Apply it Monday: check your agent's done
**Block:** Section 4  **Time:** 2 min (3:34-3:36)  **Diagram:** none
**On the slide:**
In your repo this week:
- Run your checks when the agent says done
- Return failures as the answer, three at most
- Run them where the agent cannot edit
- Keep a few checks it never sees
- Plant one fault on your riskiest line
**Visual:** Five short lines, each with a small icon (terminal, reply arrow, lock, eye-off, bug). Under them in small type: "`uv run shipharness testgen --help`".
**Speaker notes:**
- Plain explanation: you do not need shipharness for any of this. These are the walkthrough's "If you copy this into your repo" points plus one exercise from the session notes.
- Step 1: hook your test, lint, and migration checks to the agent's done (a stop hook, a wrapper script, or the CI job it must trigger), not only to the pull request.
- Step 2: cap the feedback: a one-line summary, the first few failures with the reason on the same line, and "fix these and call done again".
- Step 3: run on a copy, in a container, or in CI, so the agent cannot edit the check or its fixtures.
- Step 4: keep a small held-out suite, for example contract tests in another repo, and score agent work with it; never feed its output back.
- Step 5, the cheapest one: write one planted fault for your riskiest line (original line, replacement), apply it by hand, run your suite. If nothing fails, you have found a test to write.
- Engineering example: for an `If-Match` feature, plant "do not increment version on write"; if no test fails, write the two-writer test.
- Analogy: a bank's two-person rule: the clerk runs the transaction; a second person, with keys the clerk does not hold, signs it off.
- Question for the room: "Which of the five could you do in under an hour?" Expected answer: step 5, then step 2.
- Misconception: "Held-out tests are dishonest towards the agent." Correction: they measure the work; the agent still gets full feedback from the gate.
- Point at the last line, the planted fault: the one step that needs no tooling at all.
- Likely question: "Where do I hook this with an off-the-shelf agent?" Answer: wherever the agent signals done: a stop hook, a wrapper script around the agent CLI, or the CI job it must trigger.
- Time: 2 minutes. Transition: "Questions on Section 4."

## Slide 90: Q&A: Section 4, Verification
**Block:** Section 4  **Time:** 4 min (3:36-3:40)  **Diagram:** none
**On the slide:**
Ask about anything:
- Concepts from today's modules
- How this applies to your work
- Implementation details
- Clarifications on what we covered
Quick Request
- Please do not mind if a question gets skipped accidentally
- Repost politely in chat if needed
- We will try our best to cover as many questions as possible
Remember: If you're wondering about it, others probably are too.
No Question Is Too Small Every Question Deserves an Answer!!
**Visual:** The template's Q&A slide unchanged: boilerplate text, banner, and picture.
**Speaker notes:**
- Likely question: "The harness did not win. Was verification useless?" Answer: on F4 the runs barely tested it: the gate never ran in an A/B and the filters saw few tests. A result about this task and this model.
- Likely question: "The bare arm caught more mutants. Do the filters hurt?" Answer: the bare arm shipped more tests (median 15.5 against 0 on F4). A test nobody writes cannot catch a mutant.
- Likely question: "Why does the gate not run the hidden tests?" Answer: they would stop being held out; a check the agent gets feedback from becomes a target.
- Likely question: "Why are filters 4 and 5 not from a paper?" Answer: no source states them; they guard against a test that mocks the code it tests and a test phase that edits code until its test passes.
- Likely question: "Is the model reviewer worth it?" Answer: as a secondary measure; A3 warns it is "inclined to be generous towards LLM-generated outputs". On F4 it rejected all 14 arms and agreed with the referee.
- Likely question: "How do I read the gate in the repo?" Answer: `uv run python platform/scripts/anchors.py extract S4:gate`, then `S4:filters`.
- Keep an eye on terminal C: if the final has finished its first feature, say so; we read it next.
- Point learners to `section-4-verification/session-notes.md` and the four post-class readings for what we skipped.
- Time: 4 minutes; stop at 3:40 even if questions remain, and collect the rest in chat for the end.
- Transition: "The final A/B has been running since 2:55. Let's read it."

## Slide 91: Final A/B: reading the arm lines
**Block:** Final  **Time:** 3 min (3:40-3:43)  **Diagram:** none
**On the slide:**
No primary measure for F5 to F7. Read per arm:
- `hidden`: does the feature work?
- `mutants`: would its tests notice a bug?
- `claim`: did the agent say done?
- `passed=True` here means nothing
**Visual:** Terminal C's real output from the course's F5 run, quoted exactly from `final-project/README.md`, with callouts on `claim=done` / `claim=none`, on `hidden 46/46`, and on `mutants 2/3`:
```text
A/B <A/B id> (F5, layers=['instructions', 'scope', 'state', 'verify'], profile=class)
  bare     completed         claim=done     primary={} passed=True hidden 46/46 mutants 2/3 reviewer=accept cost=$0.0177
  harness  ABORTED: timeout  claim=none     primary={} passed=True hidden 46/46 mutants 2/3 reviewer=accept cost=$0.0226
```
**Speaker notes:**
- Switch to terminal C and read tonight's lines aloud, one feature at a time, then the session figure on the `Cost:` line.
- Plain explanation: F5 to F7 set `primary_measure = ""`, so the referee marks every run passed; "primary verdict ready: PASS" says nothing about the feature. Compare the counts instead.
- The course's F5 run before class: both arms 46 of 46 hidden tests and 2 of 3 mutants; bare completed with `claim=done` in 37 turns, harness `ABORTED: timeout` with no claim in 42 turns. Reading: no measurable difference.
- An earlier F5 run, on a loaded machine, split differently: mutants 1 of 3 (bare) and 3 of 3 (harness), hidden 46 of 46 in both. Same feature, same harness, a different split.
- The command exits 2 when an arm was aborted on time or cost. The arm is still judged; it is a result.
- Analogy: reading a canary deployment: you compare error rates, not the deploy tool's "success" message.
- Question for the room: "The harness arm made no claim but has the same counts. Better or worse?" Expected answer: same work, slower, no false claim; one run cannot say more.
- Likely learner question: "Why no primary measure on the final?" Answer: the final was not part of the registered test runs; it is a teaching A/B, so we read counts, not a verdict.
- Misconception: "The arm with `passed=True` won." Correction: both lines say `passed=True` because there is no primary measure.
- If the final has not finished: walk its live screens 1 and 2 now, and come back to the lines at the end. Fallback: the captured lines above and `final-project/expected/`.
- Point at `claim=done` against `claim=none`, then at the identical `hidden 46/46 mutants 2/3` on both lines.
- Time: 3 minutes. Transition: "Now the same run on the console."

## Slide 92: Final A/B: what to read on screens 1, 3, 5
**Block:** Final  **Time:** 3 min (3:43-3:46)  **Diagram:** screenshot: final-project/expected/screen-1-final.png
**On the slide:**
- Screen 1: both arms, claims, verdict counts
- Screen 3: diff maps, referee checks, filters
- Screen 5: first wrong turn, trace links
**Visual:** Screen 1 of the course's F5 run after the full verdict. Callouts: (1) bare "Agent said done" and "claim supported"; (2) harness "Agent said no claim"; (3) both referee lines "hidden tests 46/46, mutants killed 2/3".
**Speaker notes:**
- Browser tab 3, the final's run. Press `1`: both arms side by side. Read for each arm: run status and turns, harness decisions (map placed, handoff written), the gate, "Agent said", and the referee line.
- In the captured F5 run: bare completed, primary verdict at 3:27, full at 6:50; harness hit its time limit in the test phase, primary at 9:48, full at 12:32. Its test phase started by reading the handoff from the build session.
- Press `3`, Evidence: files read, diff maps (any `⊘ blocked` or out-of-scope file?), referee checks per rule, the filter table, the mutant table. In the F5 run both arms changed only allowed files and one mutant survived in each.
- Press `5`, Traces: the first wrong turn per arm, the live tail of referee events, and LangSmith links. Open one link to show every model call.
- For F6 or F7 tonight: look on screen 1 for "session stop" and the handoff, and on screen 3 for whether session 2 redid session 1's work.
- Engineering example: the first wrong turn on screen 5 is where you start a debug session, exactly like the first failing span in a distributed trace.
- Analogy: reading a flame graph: overview first, then the hot frame, then the source line.
- Question for the room: "Where would you look first if the harness arm had shipped a file outside its paths?" Expected answer: screen 3's diff map, then screen 5's first wrong turn.
- Likely learner question: "Why did the harness arm run out of time?" Answer: its extra phases (handoff, test phase, gate) cost turns and wall time; post hoc, harness arm wall time had a median of 302 s against 190 s for bare.
- Misconception: "The slower arm is the worse arm." Correction: time is a cost to weigh, not a quality measure; read the counts.
- Point at callout 2, "Agent said no claim": the harness arm never claimed done, so its gate never ran.
- Time: 3 minutes. Transition: "Screen 2, the boards."

## Slide 93: Final A/B: the two boards
**Block:** Final  **Time:** 2 min (3:46-3:48)  **Diagram:** screenshot: final-project/expected/screen-2-final.png
**On the slide:**
Screen 2: each arm's running board, as an Acme user.
Look for:
- ⚠ other-org cards
- ⧉ duplicate cards
- Anything the feature changed
**Visual:** Screen 2 of the course's F5 run: both boards side by side. Callouts: arrow to each "✓ only own-org cards, no duplicates" badge, label "trusted check, not the agent's".
**Speaker notes:**
- Press `2`. Each arm's TeamTrack runs with its own changes; the console logs in as an Acme user and screenshots the board.
- The marks come from trusted data attributes, not from anything the agent wrote, so an arm cannot fake a clean badge.
- In the F5 run both boards stayed clean and unchanged: bulk close adds an API endpoint and changes no board pixels. Say so if F5 ran.
- If F6 or F7 ran: look for what the feature adds to the issue pages, and for a Globex card on an Acme board (a tenant leak, Section 1's failure).
- Engineering example: the same idea as a synthetic monitor that logs in as a test tenant and checks it sees only its own data.
- Analogy: a visual regression check after deploy, run by the pipeline, not by the developer.
- Question for the room: "Why check the board at all when the API tests pass?" Expected answer: the board is a second path to the same data; leaks and duplicates show up there that an API test may not cover.
- Likely learner question: "What would a leak look like?" Answer: a card with the ⚠ other-org mark. No run before class leaked another org's cards, so there is no leak screenshot to show.
- Misconception: "A clean board means the feature works." Correction: it means no leak and no duplicates on that page; the hidden tests decide whether the feature works.
- Point at the two boards side by side: same seed data, same Acme user, so any difference comes from the arm's change.
- Time: 2 minutes. Transition: "Now tonight's run next to everything we ran before class."

## Slide 94: All results: four sections, one picture
**Block:** Final  **Time:** 3 min (3:48-3:51)  **Diagram:** docs/diagrams/results-final.png
**On the slide:**
(title only)
**Visual:** The results-final diagram: one row per section and ticket (S1 F1, S2 F2, S3 F3, S3 confirmation on F4, S4 F4), one dot per run, bare grey and harness blue, filled = passed, hollow = failed. The S3 confirmation row is the only row where the arms differ. Diagram only.
**Speaker notes:**
- Press `4` on the console first: screen 4 shows one dot per recorded run; tonight's final adds one dot per arm. Say: "One A/B is one dot. Read it next to the runs from before class, never alone."
- S1, no new tenant leak: bare 7 of 7, harness 7 of 7 passing. S2, no continuity failure: 7 of 7 each. S3 on its own ticket F3: 7 of 7 each. No measurable difference.
- S3 confirmation on F4, registered before its runs: bare 0 of 3, harness 3 of 3. Every bare arm changed `app/services/errors.py`; the scope layer blocked the same file in every harness arm. Harness ahead, the one gap.
- S4, all hidden tests and mutants on F4: bare 0 of 4, harness 0 of 4 in run 3 and the class round (and 0 of 3 each in the earlier medium round). No measurable difference: both fail.
- The registered gate for the larger batches needed the harness ahead in 3 of 4 sections; it was ahead in 0, so the batches of 10 runs per arm and the ablation were not run.
- Post hoc over 34 runs per arm, descriptive only: files outside the allowed paths in 9 bare runs and 0 harness runs; done claimed in 19 against 10, none of them with failing hidden tests; median cost per arm $0.0103 bare, $0.0123 harness.
- Analogy: a release dashboard with error bars: one good night does not move a decision.
- Question for the room: "Why did the one gap show up on scope?" Expected answer: the scope layer blocks the edit by construction; the other layers only change what the agent reads or how it ends.
- Likely learner question: "So should I skip the other layers?" Answer: measure them on your own failures. OpenAI says its results "should not be assumed to generalize without similar investment—at least, not yet." The same holds here: one model, one ticket per section, a few runs per arm.
- Misconception: "No measurable difference means no difference." Correction: it means these few runs cannot show one; a smaller effect needs more runs.
- Point at the S3 confirmation row, the only row where the colours differ, and say "partly by construction" as you point.
- Time: 3 minutes. Transition: "So which layer when?"

## Slide 95: Which layer when: match the layer to the failure
**Block:** Final  **Time:** 2 min (3:51-3:53)  **Diagram:** docs/diagrams/which-layer-when.png
**On the slide:**
(title only)
**Visual:** The which-layer-when diagram: four rows (instructions, state, scope, verification), each with the failure it prevents, the signal that says "add it", and what it costs. Scope carries a "measured gap" tag. Diagram only.
**Speaker notes:**
- Plain explanation: each layer is a bet on one thing the model cannot do on its own. A3: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."
- Instructions: add a map when the agent breaks rules that live in a wiki or copies legacy patterns. Cost: keeping the docs true.
- State: add progress files and a handoff when work spans sessions. Cost: a few turns per stop.
- Scope: add allowed paths and a sandbox when agents edit outside the ticket. The only layer with a measured gap here: bare 0 of 3 in scope, harness 3 of 3, on F4, partly by construction.
- Verification: add a gate when the agent can claim done early and your checks are cheap and exact; keep some checks held out.
- How to decide in your repo: A3's method, "removing one component at a time and reviewing what impact it had on the final result". On TeamTrack, `make final FEATURES=F5 LAYERS=-scope` removes one layer from the harness arm.
- Analogy: a security review that picks controls from the incidents you have had, not from a vendor's full catalogue.
- Question for the room: "Which failure do you see most in your repo?" Expected answer: varied; map each answer to a row.
- Misconception: "A harness is all four layers or nothing." Correction: the kit's worked example kept every layer but cut instructions down for a small library; decide per layer and write the decision down.
- Point at the "measured gap" tag on the scope row; it is the only tag on the diagram.
- Likely question: "Is there a layer you would never skip?" Answer: not on this evidence. The sandbox is the one to keep without a measurement: it limits damage on the run that goes wrong, which no A/B here measures.
- Time: 2 minutes. Transition: "Here is how to take it home."

## Slide 96: Use it in your repo: the kit and four skills
**Block:** Close  **Time:** 2 min (3:53-3:55)  **Diagram:** docs/diagrams/harness-one-picture.png
**On the slide:**
`uv run shipharness init --target ~/my-repo`
`uv run shipharness init --check ~/my-repo`
The starter kit: map, state files, feature list, house-rule checks, sandbox policy, CI
Four Agent Skills:
- `harness-setup`: assess a repo, fill gaps
- `assured-tests`: keep tests passing five filters
- `house-rules`: convention to rule, check, test
- `skill-template`: start your own skill
**Visual:** The harness-one-picture diagram (the four layers around the agent loop), with a small caption: "the same layers, copied into your repo".
**Speaker notes:**
- Plain explanation: `shipharness init` copies the kit into your repository with no model calls. Every template holds TeamTrack's real values with a REPLACE marker next to each; `--check` lists the markers still to fill.
- It never overwrites your files: an existing `AGENTS.md` is skipped and reported; `--force` replaces it only if you ask.
- The skills install twice: `.claude/skills/` (Claude Code, Cursor) and `.agents/skills/` (Codex, Cursor). They follow the Agent Skills format: a folder with a `SKILL.md`.
- The guide is `use-in-your-repo/apply-to-your-repo.md`: seven steps, install, copy, fill, check, run, read, decide. Steps 1 to 4 make no model calls.
- Concrete example from the guide: testgen on the boltons queue module kept 3 of 3 proposed tests for $0.002031. The assured-tests example on TeamTrack kept 1 of 5 for $0.003287; the other four failed filter 3.
- Analogy: a cookiecutter template: real defaults, with a marker on every value you must change.
- Question for the room: "Which skill would you install first?" Expected answer: `house-rules` (turns a repeated review comment into a check) or `assured-tests`.
- Likely learner question: "Does testgen run my tests on my machine?" Answer: with `--sandbox local`, yes, and it prints UNSANDBOXED; for code you do not trust, use `--sandbox docker --image`.
- Misconception: "Install the kit and you are done." Correction: step 7 of the guide is deciding which layers earn their place; measure before you keep a piece.
- Point at the two commands: `init` copies the kit, `init --check` lists the REPLACE markers still to fill.
- Time: 2 minutes. Transition: "Four assignments practise each layer."

## Slide 97: Assignments (1 of 2): instructions and state
**Block:** Close  **Time:** 1 min (3:55-3:56)  **Diagram:** none
**On the slide:**
**A1: from one long instruction file to a map**
- Split a long `AGENTS.md` into map, docs, skill
- Write a checker for lost rules and links
- One live A/B; report R1 and R3 counts
**A2: three forced stops, one history**
- Complete a state layer with a step ledger
- Facts from git, never the agent's word
- Offline scenarios, then one live run
**Visual:** Two cards side by side, A1 and A2, each with its folder path in small type: `section-1-instructions/assignment/`, `section-2-state-lifecycle/assignment/`.
**Speaker notes:**
- Every assignment has the same shape: a starter folder, `make check-assignment-N` that runs offline with no keys, one live step, grading criteria out of 100 points, and a full solution with a step-by-step walkthrough in `solution/`. Tell learners to try first.
- A1: the starter is a long single `AGENTS.md` with tagged rules. Build a short map, focused docs, one Agent Skill, and `checker/check_docs.py` that fails when a link breaks or a rule goes missing. Then one live A/B with your tree and `ab-report.md` with R1 and R3 as counts.
- A2: complete `ResumableStateLayer`. At every stop it writes what the next session needs, derived from git and the files on disk. A deterministic stand-in agent drives the real runner across three forced stops, offline; then one live run with the course model.
- Engineering example: A2's failure is the classic second migration for a table that already exists; the step ledger prevents it.
- Analogy: A1 is writing onboarding docs that a linter keeps honest; A2 is an on-call handover template filled from the system, not from memory.
- Question for the room: "Why must A2's facts come from git?" Expected answer: the agent's account of what it did is a claim, the same lesson as tonight's done claim.
- Likely learner question: "Do I need Docker for the self-check?" Answer: no; the self-checks run offline. Only the live step needs keys and Docker.
- Misconception: "The live step must show the harness winning." Correction: report what you measured, as counts; a tie is a valid result.
- Review session: two hours, about 25 minutes per assignment, then open questions.
- Point at the two folder paths: each holds the starter, the solution, and a README with the grading criteria.
- Time: 1 minute. Transition: "A3 and A4."

## Slide 98: Assignments (2 of 2): scope and verification
**Block:** Close  **Time:** 1 min (3:56-3:57)  **Diagram:** none
**On the slide:**
**A3: scope you can check**
- Diff parser and per-phase scope policy
- `passes` set only with evidence
- A deny rule for history rewrites
**A4: verification and portfolio**
- R8: deleted issues answer 404, never listed
- Filter 6: drop duplicate generated tests
- testgen plus one live F4 A/B
- A portfolio a reader can check
**Visual:** Two cards side by side, A3 and A4, with `section-3-scope-sandbox/assignment/` and `section-4-verification/assignment/` in small type.
**Speaker notes:**
- A3: build `a3scope`: a diff parser that finds every changed path (renames, quoted names, `../` paths, empty new files), a policy that refuses paths outside the phase's list, an evidence-gated update of `passes`, and a sandbox rule that refuses git history rewrites with a test that proves the denial. Live step: one `demo-3` A/B on F3.
- A3 grading multiplies both sides, so a policy that refuses everything, or allows everything, earns nothing there.
- A4: turn TeamTrack's soft-delete rule into house rule R8. On unchanged TeamTrack it finds one violation, at `GET /v1/issues`. Add filter 6, which discards a test that repeats another. Then a testgen run and one live F4 A/B, kept in `live/`, and a portfolio: evidence report, LangSmith link, one-page case study, your own skill.
- A4's reference solution passes its self-check 23 of 23; the unchanged starter passes 2 of 23, by design. Each FAIL line names what to build.
- Engineering example: A4's R8 error message should tell the agent how to fix the problem; A1's source, OpenAI: "we write the error messages to inject remediation instructions into agent context."
- Analogy: A3 is least privilege enforced by code review bots; A4 is adding a missing lint rule after an incident.
- Question for the room: "Why does R8 probe every endpoint from the app's schema?" Expected answer: so endpoints an agent adds later are covered too.
- Likely learner question: "Is the grader in the repo?" Answer: no; `make check-assignment-N` runs the visible checks, and the instructor's grader adds hidden cases, the same idea as tonight's hidden tests.
- Misconception: "A4's live A/B must pass F4." Correction: in the reference run neither arm passed the primary measure; the grade is for valid evidence, honestly reported.
- Point at "Filter 6": the one addition that extends tonight's five filters.
- Time: 1 minute. Transition: "And the final project ties them together."

## Slide 99: Final project: one live A/B, read as one dot
**Block:** Close  **Time:** 1 min (3:57-3:58)  **Diagram:** screenshot: final-project/expected/screen-4-final.png
**On the slide:**
- Run `make final FEATURES=F5` yourself
- Remove one layer: `LAYERS=-scope`
- Read counts, never one verdict
- Draw your dots: `uv run shipharness report`
- Feeds A4's portfolio
**Visual:** Screen 4 of the course's final run: one dot per run per feature and arm. Callout: arrow to a single new dot, label "one A/B = one dot".
**Speaker notes:**
- Plain explanation: the final project repeats tonight's final on your machine: `make final FEATURES=F5`, with `PURPOSE=pilot` outside class. At the caps one feature costs at most $0.58.
- Leave-one-out: `make final FEATURES=F5 LAYERS=-scope` removes one layer from the harness arm; this is A3's method, one feature at a time.
- `uv run shipharness report` makes no model calls and writes `exports/report.html`: one dot per run, filled for passed, hollow for failed.
- The portfolio for A4: the A/B's score records and trace links, the kit's check and testgen output on a repository you choose, a one-page case study, and a skill of your own.
- Concrete example: the course ran F5 twice before class and the two A/Bs split differently on mutants (2 of 3 each, then 1 of 3 against 3 of 3). That is the reason for "one dot".
- Analogy: a benchmark result you publish with its run count and variance, not a single best run.
- Question for the room: "How many runs would you need before you believed a gap?" Expected answer: more than one per arm; the course planned 10 per arm for its larger batches.
- Misconception: "My one A/B shows the harness works on my repo." Correction: it shows one dot; report it as counts and say what more runs would need to show.
- Point at the single new dot on screen 4 among the dots from before class.
- Likely question: "Can I run the final without Docker?" Answer: not for results; the instructor guide forbids `SANDBOX_MODE=none` for class results, because both arms must run in the same kind of container.
- Time: 1 minute. Transition: "Where every quote tonight came from."

## Slide 100: References (1 of 2): harness engineering sources
**Block:** Close  **Time:** 0.5 min (3:58-3:58:30)  **Diagram:** none
**On the slide:**
- OpenAI, Harness engineering: leveraging Codex in an agent-first world · Ryan Lopopolo · 2026-02-11
- Anthropic, Effective harnesses for long-running agents · Justin Young · 2025-11-26
- Anthropic, Harness design for long-running application development · Prithvi Rajasekaran · 2026-03-24
- Anthropic, Building a C compiler with a team of parallel Claudes · Nicholas Carlini · 2026-02-05
- Anthropic, Autonomous Coding Agent Demo (README) · 2025-11-26
- OpenAI Cookbook, Using PLANS.md for multi-hour problem solving · Aaron Friel · 2025-10-07
**Visual:** A plain list, source name in blue, author and date in white. No picture.
**Speaker notes:**
- These are the sources behind the four causes and the four layers; titles are exact, so the OpenAI title keeps its own wording.
- OpenAI, Harness engineering: the map instead of a giant instruction file, "golden principles" behind the house rules, and the warning that results should not be assumed to generalize.
- Anthropic, Effective harnesses: sessions start with no memory; clean state; progress files and the feature list.
- Anthropic, Harness design: self-grading skews positive; separating doer and judge; removing one component at a time.
- Anthropic, C compiler: a nearly perfect verifier; short test output; run it in a container.
- The demo README and the PLANS.md article are supplementary: the feature list and the exec plan.
- Where to find links: `docs/evidence/s1.md` to `s4.md` and `docs/evidence/final.md`, Sources and findings; the full list is `REFERENCES.md`.
- Likely learner question: "Which one should I read first?" Answer: Anthropic's Harness design, then OpenAI's Harness engineering.
- Time: 30 seconds. Transition: next slide.

## Slide 101: References (2 of 2): skills, tests, held-out evaluation
**Block:** Close  **Time:** 0.5 min (3:58:30-3:59)  **Diagram:** none
**On the slide:**
- Agent Skills: Specification; What are skills?; Adding skills support · agentskills.io
- Claude Code, Codex, and Cursor skills docs
- Alshahwan et al. (Meta), TestGen-LLM · FSE '24
- Foster et al. (Meta), Mutation-Guided LLM-based Test Generation (ACH) · 2025
- Zhao, Srikanth, Wu, Jiang (Weco AI), SpecBench · 2026, and its repository
**Visual:** A plain list, same style as part 1 of 2.
**Speaker notes:**
- Agent Skills specification and guides: the `SKILL.md` folder format behind the four course skills; the Claude Code, Codex, and Cursor pages for where each client loads skills.
- TestGen-LLM (arXiv 2402.09171): filters 1 to 3 and the five-run flakiness check.
- ACH (arXiv 2501.12862): mutants targeted at the fault you care about; filter 3's mutant branch; the limit that it cannot find existing faults.
- SpecBench (arXiv 2605.21384 and github.com/WecoAI/SpecBench): visible against held-out suites, and compositional failures. Not the unrelated Spec-Bench paper.
- Links and access dates: `docs/evidence/s4.md` and `docs/evidence/final.md`, Sources.
- Post-class readings in `section-4-verification/post-class-reading/` summarise the last three in about 20 minutes.
- Likely learner question: "Are the quotes checked?" Answer: yes; each quote on the course pages was checked against the source text, and the pages list them.
- Misconception: "Filters 4 and 5 are from TestGen-LLM." Correction: they are the course's own; the evidence page says so.
- Time: 30 seconds. Transition: "Last questions."

## Slide 102: Q&A: anything from today
**Block:** Close  **Time:** 1 min (3:59-4:00)  **Diagram:** none
**On the slide:**
Ask about anything:
- Concepts from today's modules
- How this applies to your work
- Implementation details
- Clarifications on what we covered
Quick Request
- Please do not mind if a question gets skipped accidentally
- Repost politely in chat if needed
- We will try our best to cover as many questions as possible
Remember: If you're wondering about it, others probably are too.
No Question Is Too Small Every Question Deserves an Answer!!
**Visual:** The template's Q&A slide unchanged.
**Speaker notes:**
- Take questions collected in chat during Section 4 first.
- Likely question: "Which layer should I add first at work?" Answer: the one that matches a failure you have seen; scope is the only one with a measured gap here, on one ticket and partly by construction; start by counting out-of-scope files before you enforce anything.
- Likely question: "Will these results hold for a stronger model?" Answer: unknown; each layer encodes an assumption about the model, and A3 dropped context resets for a newer model. Re-measure when the model changes.
- Likely question: "How much did tonight cost?" Answer: read the session figure from the last `Cost:` line in terminal C; the session cap was $2.50.
- Likely question: "Where do I start tomorrow?" Answer: `use-in-your-repo/apply-to-your-repo.md`, step 1, or Assignment 1.
- Remind: the review session covers each assignment, about 25 minutes each, with common mistakes counted per criterion.
- After class (instructor): `uv run shipharness report`, back up `.shipharness/runs/` and `exports/`, note each command's `Cost:` line.
- Time: 1 minute; stop at 4:00.
- Transition: "Thank you."

## Slide 103: Thank you: see you at the review session
**Block:** Close  **Time:** 0 min (4:00)  **Diagram:** none
**On the slide:**
Thank you
**Visual:** The template's closing picture slide: full image, one line of text.
**Speaker notes:**
- Thank the room for the polls and the questions.
- Repeat the one line of the night: each harness piece is a bet on what the model cannot do; measure it before you keep it.
- Point to the repository: section folders, `use-in-your-repo/`, and `final-project/`.
- Point to the four assignments and their offline self-checks.
- Remind them the class run records stay on the instructor's machine; captured runs are in each `demo/expected/` folder.
- Invite results from their own repos, reported as counts.
- Stop the console (Ctrl+C in terminal A) only after the last screen is closed.
- End on time at 4:00.
