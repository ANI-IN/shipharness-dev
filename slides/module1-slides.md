# Module 1: Harness Engineering for Coding Agents: slide content for review

80 slides, 240 minutes in a 240-minute class: Opening 0:00-0:10, Section 1: Instructions 0:10-1:00, a 10-minute break,
Section 2: State and sessions 1:10-2:00, Section 3: Scope and sandbox 2:00-2:50, a 5-minute break,
Section 4: Verification 2:55-3:40 (opening with the one Zoom poll),
final block and close 3:40-4:00. Each section's live run launches on its first slide and finishes before
its DEMO slide. Every slide carries a `**Layout:**` field for the PPTX builder: `template-<name>`,
`key-idea`, `diagram`, `quote-cards`, `steps`, `two-column`, `icon-rows`, `code`, or `table`. Speaker
notes are written so the class can be taught from the notes alone. Numbers come only from
`docs/evidence.md` and `docs/evidence/*.md`; diagrams are Excalidraw files under `docs/diagrams/` and
`section-N-*/diagrams/`. Sources are numbered in the order they are first cited; the list is at the end.

## Index

| Slide | Title | Block | Layout | Diagram |
|---|---|---|---|---|
| 1 | Module 1: Harness Engineering for Coding Agents | Housekeeping | template-cover | none |
| 2 | Introduction: Who is teaching today | Housekeeping | template-intro | none |
| 3 | Welcome: Before we begin, pop into the chat | Housekeeping | template-welcome | none |
| 4 | Structure of Class: Four hours, four layers | Housekeeping | template-structure | none |
| 5 | Optimize Your Experience: the support you have | Housekeeping | template-support | none |
| 6 | Success Hacks | Housekeeping | template-success-hacks | none |
| 7 | Check Your Email for API Key | Housekeeping | template-api-key | none |
| 8 | Clone & Practice: Your Learning Repository | Housekeeping | two-column | none |
| 9 | Recap: The Anatomy of an Agentic Loop (build 1/2) | Recap | diagram | docs/diagrams/agent-loop-step-2.png |
| 10 | Recap: The Anatomy of an Agentic Loop (build 2/2) | Recap | diagram | docs/diagrams/agent-loop.png |
| 11 | Today's Agenda | Agenda | template-agenda | none |
| 12 | Problem statement: What are we building? | Problem | diagram | docs/diagrams/harness-around-loop.png |
| 13 | Problem statement: The problem in the real world | Problem | icon-rows | none |
| 14 | The challenge is: The rules exist, the agent still misses | Problem | quote-cards | none |
| 15 | Why this matters for Engineering Teams | Problem | two-column | none |
| 16 | Why We Need a Harness: The 4 Critical Gaps | Problem | diagram | docs/diagrams/stories-causes-layers.png |
| 17 | TeamTrack: The data model | Problem | diagram | docs/diagrams/teamtrack-data-model.png |
| 18 | House rules: seven rules in plain words | Problem | table | docs/diagrams/house-rules.png |
| 19 | How We'll Measure: Same ticket, two arms, one referee | Problem | diagram | docs/diagrams/ab-referee.png |
| 20 | Glossary: the terms used in every section | Problem | table | docs/diagrams/glossary-terms.png |
| 21 | Section 1: Instructions, what the agent knows | Section 1 | template-agenda | none |
| 22 | Failure story: The search that showed another org | Section 1 | steps | section-1-instructions/diagrams/failure-story-s1.png |
| 23 | Instructions: Why not paste every rule? | Section 1 | key-idea | section-1-instructions/diagrams/socratic-s1-step-3.png |
| 24 | 1) A map, not a manual | Section 1 | diagram | section-1-instructions/diagrams/manual-vs-map.png |
| 25 | 2) Progressive disclosure: skills load in three tiers | Section 1 | diagram | section-1-instructions/diagrams/skills-three-tiers.png |
| 26 | 3) The context prefix: small, fixed, out of reach | Section 1 | diagram | section-1-instructions/diagrams/context-prefix.png |
| 27 | 4) Mechanical checks keep the map true | Section 1 | diagram | section-1-instructions/diagrams/checker-flow.png |
| 28 | Cheat Sheet: The instructions layer in four moves | Section 1 | table | section-1-instructions/diagrams/cheat-sheet-s1.png |
| 29 | Section 1: Instructions - Implementation Notes: The map at work | Section 1 | template-demo | none |
| 30 | What we measured: No measurable difference on org-wide search | Section 1 | two-column | section-1-instructions/diagrams/results-s1.png |
| 31 | Q&A: Section 1: Instructions | Section 1 | template-qa | none |
| 32 | Time for a Break | Break | template-break | none |
| 33 | Section 2: State and sessions, what it remembers | Section 2 | template-agenda | none |
| 34 | Failure story: The second session redoes the first | Section 2 | steps | section-2-state-lifecycle/diagrams/failure-story-s2.png |
| 35 | Fresh session: Why redo work already on disk? | Section 2 | key-idea | section-2-state-lifecycle/diagrams/socratic-s2-step-3.png |
| 36 | 1) Session lifecycle: a planned stop and reset | Section 2 | diagram | section-2-state-lifecycle/diagrams/session-lifecycle.png |
| 37 | 2) The handoff: two owners, one file | Section 2 | diagram | section-2-state-lifecycle/diagrams/handoff-contents.png |
| 38 | 3) The exec plan and the progress ledger | Section 2 | diagram | section-2-state-lifecycle/diagrams/exec-plan-ledger.png |
| 39 | 4) Getting up to speed: init.sh before code | Section 2 | diagram | section-2-state-lifecycle/diagrams/alembic-heads.png |
| 40 | Cheat Sheet: Four state pieces across a stop | Section 2 | table | section-2-state-lifecycle/diagrams/cheat-sheet-s2.png |
| 41 | Section 2: State and sessions - Implementation Notes: Stop and resume | Section 2 | template-demo | none |
| 42 | What we measured: No measurable difference on comments | Section 2 | two-column | section-2-state-lifecycle/diagrams/results-s2.png |
| 43 | Q&A: State and sessions | Section 2 | template-qa | none |
| 44 | Section 3: Scope and sandbox, what it may change | Section 3 | template-agenda | none |
| 45 | Failure story: A tidy diff in a shared file | Section 3 | steps | section-3-scope-sandbox/diagrams/failure-story-s3.png |
| 46 | Scope: Is the ticket's file list enough? | Section 3 | key-idea | section-3-scope-sandbox/diagrams/socratic-s3-step-2.png |
| 47 | 1) One feature at a time: feature_list.json | Section 3 | diagram | section-3-scope-sandbox/diagrams/feature-list-lifecycle.png |
| 48 | 2) Allowed paths per phase, checked by code | Section 3 | diagram | section-3-scope-sandbox/diagrams/scope-check-flow.png |
| 49 | 3) The sandbox boundary: where the keys live | Section 3 | diagram | section-3-scope-sandbox/diagrams/sandbox-boundary.png |
| 50 | 4) Least privilege: two refusals, two questions | Section 3 | diagram | section-3-scope-sandbox/diagrams/least-privilege.png |
| 51 | Cheat Sheet: Four boundaries for one feature | Section 3 | table | section-3-scope-sandbox/diagrams/cheat-sheet-s3.png |
| 52 | Section 3: Scope and sandbox - Implementation Notes: Scope at work | Section 3 | template-demo | none |
| 53 | What we measured: Scope held on version checks | Section 3 | two-column | section-3-scope-sandbox/diagrams/results-s3.png |
| 54 | Q&A: Scope and sandbox | Section 3 | template-qa | none |
| 55 | Time for a Break | Break | template-break | none |
| 56 | Live Zoom Poll: Pick the final A/B feature | Section 4: Verification | template-poll | none |
| 57 | Section 4: Verification, what proves the work is done | Section 4 | template-agenda | none |
| 58 | Failure story: Done, but two edits still collide | Section 4 | steps | section-4-verification/diagrams/failure-story-s4.png |
| 59 | Verification: Suite green. Are version checks done? | Section 4 | key-idea | section-4-verification/diagrams/socratic-s4-step-2.png |
| 60 | 1) Self-grading and visible tests | Section 4 | diagram | section-4-verification/diagrams/verification-pipeline-step-1.png |
| 61 | 2) Test-phase filters: keep tests that prove something | Section 4 | diagram | section-4-verification/diagrams/verification-pipeline-step-2.png |
| 62 | 3) Mutation testing and hidden tests | Section 4 | diagram | section-4-verification/diagrams/mutation-testing.png |
| 63 | 4) The gate on "done" and the separate referee | Section 4 | diagram | section-4-verification/diagrams/verification-pipeline-step-3.png |
| 64 | Cheat Sheet: four checks the agent does not own | Section 4 | table | section-4-verification/diagrams/cheat-sheet-s4.png |
| 65 | Section 4: Verification - Implementation Notes: The gate at work | Section 4 | template-demo | none |
| 66 | What we measured: No measurable difference on version checks | Section 4 | two-column | section-4-verification/diagrams/results-s4.png |
| 67 | Q&A: Section 4: Verification | Section 4 | template-qa | none |
| 68 | Final A/B: reading it live | Final | icon-rows | none |
| 69 | All results: four sections, one picture | Final | diagram | docs/diagrams/results-final.png |
| 70 | Which layer when: match the layer to the failure | Final | diagram | docs/diagrams/which-layer-when.png |
| 71 | Use it in your repo: the kit and four skills | Close | icon-rows | none |
| 72 | Assignments: one per layer | Close | icon-rows | none |
| 73 | Final project: one live A/B, read as one dot | Close | steps | none |
| 74 | The harness in one picture | Close | diagram | docs/diagrams/harness-one-picture.png |
| 75 | Module 1 Summary: Key takeaways | Close | diagram | docs/diagrams/module-summary.png |
| 76 | Glimpse of Module 2: Loop Engineering for Coding Agents | Close | icon-rows | none |
| 77 | References (1 of 2): sources in the order cited | Close | table | none |
| 78 | References (2 of 2): the remaining sources | Close | table | none |
| 79 | Q&A: anything from today | Close | template-qa | none |
| 80 | Thank you: see you at the review session | Close | template-thank-you | none |

---

## Slide 1: Module 1: Harness Engineering for Coding Agents
**Block:** Housekeeping  **Time:** 0.25 min (0:00-0:00:15)  **Diagram:** none  **Layout:** template-cover
**On the slide:**
Module 1: Harness Engineering for Coding Agents
Instructions, state, scope, verification: build each layer, then measure it
**Visual:** Template cover. "Module 1" in blue, the rest of the title in white, the subtitle smaller underneath. No picture.
**Speaker notes:**
- Welcome. Today we build four layers around a coding agent and watch each one at work, live, on a real feature of a small app.
- Plain version: a harness is the files and code around the agent that decide what it sees and what it may do. It is not a better prompt.
- What is different about this class: every layer was measured before class. Same agent, same model, same ticket, with and without the layer, scored by the same program.
- We also show where the layer did not help. In three of the four sections the measure showed no measurable difference on this model. Section 3: Scope and sandbox showed one gap, on Feature 4: Version checks on issue edits, partly by construction.
- Point at the subtitle: "build each layer, then measure it" is the whole course.
- Ask: "Who has already given a real ticket to a coding agent?" Expected: many hands. Ask one person what went wrong; you will hear one of today's four failures.
- Misconception: "a harness is a long system prompt". Correction: today's harness includes files on disk, session state, a scope guard, and a gate on "done".
- Likely question: "Which model did you measure?" Answer: gpt-6-luna as the agent and gpt-5.6-luna as the blinded reviewer, the same settings for both arms; the results hold for that model only.
- Time: 15 seconds. Next: who is teaching today.

## Slide 2: Introduction: Who is teaching today
**Block:** Housekeeping  **Time:** 0.25 min (0:00:15-0:00:30)  **Diagram:** none  **Layout:** template-intro
**On the slide:**
Introduction: Who is teaching today
Your instructor, in 30 seconds:
- Where they ship code with coding agents
- One agent failure they had to debug
- The harness layer they would add first
- Where to reach them after class
**Visual:** Template intro layout: "Introduction:" in blue, the lead-in line and four bullets on the left, a plain icon column on the right (laptop, bug, stacked layers, chat bubble). No name or photo, so the slide works for any instructor.
**Speaker notes:**
- Say your name and role aloud; the slide deliberately carries no name.
- Bullet 1, one sentence: your years in software and the coding agents you use (Claude Code, Codex, Cursor, Copilot).
- Bullet 2, 15 seconds: one agent diff that passed review and still broke a rule your team cared about. If you have none, tell Monday's story from the real-world slide and say it is the course's illustrative scenario.
- Map your failure to a layer out loud: rule not in context (Section 1: Instructions), lost session (Section 2: State and sessions), edit outside the ticket (Section 3: Scope and sandbox), false "done" (Section 4: Verification).
- Bullet 3: name the layer you would add first, and promise to revisit it after the results.
- Bullet 4: say the channel for questions after class (course chat, review session); no contact details on the slide.
- Ask: "Which coding agents are you using at work?" Expected: Claude Code, Codex, Cursor, Copilot. Say: everything today applies to all of them.
- Likely question: "Do I need the repository running to follow along?" Answer: no; the demos run on the instructor's machine, the repository lets you repeat them later.
- Misconception: "this is a product pitch for a harness". Correction: three of today's four sections show no measurable difference, and the slides say so.
- Time: 15 seconds. Next: the chat round.

## Slide 3: Welcome: Before we begin, pop into the chat
**Block:** Housekeeping  **Time:** 0.25 min (0:00:30-0:00:45)  **Diagram:** none  **Layout:** template-welcome
**On the slide:**
Welcome to today's class, before we begin, pop into the chat:
- Name
- Role
- Location
- The coding agent you use
**Visual:** Template welcome slide: four emoji chips around a sample person card; the fourth chip reads "The coding agent you use".
**Speaker notes:**
- Say: "Before we begin, tell us four things in the chat: your name, your role, where you are, and the coding agent you use."
- Why the fourth chip changed: today's material applies to any agent that reads an AGENTS.md or a skills folder, so the room's tools help you pick examples.
- Read three or four answers aloud, for example "Backend engineer, Berlin, Claude Code". Claude Code, Codex, and Cursor all read a skills folder; Section 1: Instructions comes back to that.
- Ask: "Anyone running an agent without a human reviewing the diff?" Expected: few. Say: today shows why review alone is not enough either.
- Likely question: "Will the slides be shared?" Answer: yes, with the repository; the slide source lives under `slides/`.
- Time: 15 seconds; keep reading answers aloud during the next slides. Next: how the class runs.

## Slide 4: Structure of Class: Four hours, four layers
**Block:** Housekeeping  **Time:** 0.25 min (0:00:45-0:01)  **Diagram:** none  **Layout:** template-structure
**On the slide:**
Structure of Class
- Live class - 4 hr: four sections, two breaks, a final A/B
- Live demos - every demo is a real model run
- Assignments - four, one per section
- Review session - 2 hr, one slot per assignment
**Visual:** Template structure layout: each line with a bold coloured lead and white detail; the pacing picture at the bottom.
**Speaker notes:**
- Each section runs the same way: launch the live run at the section start, teach the ideas while it works, open the finished run on the console, then read what we measured.
- Concrete: Section 1: Instructions launches `make show-1` at about class minute 0:11 and we open it around 0:40.
- Breaks: 10 minutes after Section 1, 5 minutes after Section 3: Scope and sandbox. Section 4: Verification runs 45 minutes so the final A/B gets 20 minutes at the end.
- One Zoom poll in the whole class, at the start of Section 4: Verification: you pick the feature for the final A/B.
- Assignments: one per section, each with a reference solution and a walkthrough in its `assignment/solution/` folder.
- Review session: two hours, about 25 minutes per assignment, then 20 minutes of open questions.
- Ask: "If a run in class fails, is that a broken demo?" Expected: no, a result. We show it either way.
- Misconception: "live demos are rehearsed recordings". Correction: every launch makes real model calls under a $2.50 session cap; a replay is used only after a failure outside the experiment, and every replay screen shows a red RECORDING badge.
- Time: 15 seconds. Next: getting the most from the program.

## Slide 5: Optimize Your Experience: the support you have
**Block:** Housekeeping  **Time:** 0.5 min (0:01-0:01:30)  **Diagram:** none  **Layout:** template-support
**On the slide:**
Optimize Your Experience
Ask, practise, and use your resources: what you put in is what you get out.
- Uplevel: recordings, resources, assignments
- Wednesday technical coaching: bring your queries
- Discord: peer learning
- TAs: answer questions in the live class
- Support tickets: raise one on Uplevel any time
**Visual:** Template support layout: the heading, the lead line, one line per feature with the feature name in bold pink and the rest in white; the template's two pictures unchanged.
**Speaker notes:**
- Interact: questions in the chat are welcome all class; TAs collect them and each section's Q&A slide takes the top ones.
- Clarify at once: if a term is new, ask; the glossary slide at the end of the opening defines every term we use.
- Solve the four assignments: each has an offline self-check (`make check-assignment-N`) and feedback at the review session.
- Uplevel: the recording of this class and the learning resources land there.
- Wednesday technical coaching: bring setup problems with the exact terminal message; it is faster to fix.
- Discord: share results from your own repository, as counts per arm.
- Support tickets: anything technical, any time. Never paste your `.env` or a key into a ticket or the chat.
- Each section folder also has `concepts.md`, a demo page, `session-notes.md`, and post-class readings.
- Time: 30 seconds. Next: success hacks.

## Slide 6: Success Hacks
**Block:** Housekeeping  **Time:** 0.25 min (0:01:30-0:01:45)  **Diagram:** none  **Layout:** template-success-hacks
**On the slide:**
Success Hacks
- Be prepared for the class: finish the pre-class setup
- Attend every class
- Participate in class
- Attempt all the assignments
- Actively advocate for yourself
- Keep your goal in mind
- Consistency is the key
Be patient with yourself !
**Visual:** Template success-hacks layout: seven bullets, "Consistency is the key" in pink, the closing line under the list.
**Speaker notes:**
- Be prepared: `setup/pre-class.md` is the checklist: `make doctor`, `make warm`, `make console`.
- Participate: before each result, say your guess in the chat, then compare it with the measurement.
- Attempt all the assignments: each starter fails its self-check on purpose, and each FAIL line names what to build.
- Advocate for yourself: if a demo moves too fast, ask; the captured runs in each `demo/expected/` folder let you replay it later.
- Time: 15 seconds. Next: the API keys.

## Slide 7: Check Your Email for API Key
**Block:** Housekeeping  **Time:** 0.25 min (0:01:45-0:02)  **Diagram:** none  **Layout:** template-api-key
**On the slide:**
Check Your Email for API Key
Use the OpenAI key from the program's email if you received one; otherwise create your own (Build tier) at platform.openai.com.
If you do not see this email:
- Please check your inbox
- Also check your spam or junk folder
If you still cannot find it, please reach out to the Operations Team operations@interviewkickstart.com
LangSmith key: a free account at smith.langchain.com
`make doctor` confirms the key can use the course models
**Visual:** Template API-key layout; in place of the email picture, a small card with the two empty lines from `.env.example`: `OPENAI_API_KEY=` and `LANGSMITH_API_KEY=`.
**Speaker notes:**
- Two keys run every live command: `OPENAI_API_KEY` for the agent and reviewer models, `LANGSMITH_API_KEY` for traces of every model call.
- OpenAI: use the key from the program's email if you received one; otherwise create your own (Build tier) at platform.openai.com, per `.env.example`.
- LangSmith: a free Developer account at smith.langchain.com, no card on file. EU accounts set `LANGSMITH_ENDPOINT` to the EU address in `.env.example`.
- Both keys go in `.env` at the repository root; `make setup` creates it from `.env.example`, and it is git-ignored.
- `make doctor` confirms the OpenAI key can use the course models (gpt-6-luna and gpt-5.6-luna) and that the LangSmith key is accepted; it never prints any part of a key, and the last line must read `result: + ready`.
- Never paste a key into the chat, a support ticket, or a screenshot.
- Time: 15 seconds. Next: the repository.

## Slide 8: Clone & Practice: Your Learning Repository
**Block:** Housekeeping  **Time:** 0.5 min (0:02-0:02:30)  **Diagram:** none  **Layout:** two-column
**On the slide:**
Lead: harness-engineering-session · https://github.com/ANI-IN/harness-engineering-session
Left: What's included
- Four section folders: concepts, demo, assignment
- Final project: one live A/B of every layer
- use-in-your-repo kit and four skills
- Slides and docs
Right: Getting started
- `git clone https://github.com/ANI-IN/harness-engineering-session.git`
- Read `setup/README.md`
- `make setup`: creates `.env` from `.env.example`
- Fill in both keys, then `make doctor`
**Visual:** Two cards: "What's included" on the left, "Getting started" on the right with the clone command in monospace and the three steps numbered. The repository name and URL in the lead strip.
**Speaker notes:**
- This is the public repository the class runs from: every slide, demo, and number is in it.
- Section folders: `section-1-instructions`, `section-2-state-lifecycle`, `section-3-scope-sandbox`, `section-4-verification`. Each has `concepts.md`, a demo with captured runs in `demo/expected/`, `session-notes.md`, and an `assignment/` folder with a starter and a full solution.
- `final-project/`: the whole harness on a feature neither arm has seen, then your own repository.
- `use-in-your-repo/`: the starter kit (`uv run shipharness init --target ../your-repo`) and four Agent Skills.
- `slides/` holds this deck's source; `docs/` holds the reference, troubleshooting, and the evidence pages behind every count.
- Getting started: `setup/README.md` picks your system page (Windows with WSL2, macOS, Linux). `make setup` installs the packages, builds the two sandbox images, and copies `.env.example` to `.env`.
- Then fill in `OPENAI_API_KEY` and `LANGSMITH_API_KEY`, set `SHIPHARNESS_CLASS_DATE`, and run `make doctor` until it ends with `result: + ready`.
- Analogy: a lab notebook: the code, the runs, and the write-up live together, so you can check every claim.
- Likely question: "Do I need Docker to follow along today?" Answer: no; the demos run on the instructor's machine. Docker is needed for your own live runs.
- Misconception: "the repository is only slides". Correction: it holds the full harness, the referee, the console, and TeamTrack itself.
- Time: 30 seconds. Next: a one-picture recap of the agent loop.

## Slide 9: Recap: The Anatomy of an Agentic Loop (build 1/2)
**Block:** Recap  **Time:** 0.25 min (0:02:30-0:02:45)  **Diagram:** docs/diagrams/agent-loop-step-2.png  **Layout:** diagram
**On the slide:**
Lead: An agent is a loop: send the history to the model, run the tool it asks for, repeat.
Key idea: The model sees only what travels along these arrows.
**Visual:** Build frame 2 of `agent-loop`: the ticket (prompt) goes to the agent, the agent calls the model, the tools box (read a file, patch, run a command) returns results to the agent.
**Speaker notes:**
- Plain explanation: the agent sends the conversation to the model and gets back text or a tool call; it runs the tool, appends the result to the history, and asks again.
- Concrete: in this session's runs the model is gpt-6-luna and the prompt is a TeamTrack ticket such as "Add org-wide issue search: GET /issues".
- Concrete: in Section 1: Instructions' captured run, the early tool calls read `ARCHITECTURE.md` and the `add-endpoint` skill, then patched the issues service and route.
- Analogy: a junior engineer who sees only what is on their desk, and can open one file-cabinet drawer at a time, if they think to.
- Point at the tools box: every harness layer today touches this box or the arrows around it.
- Ask: "Where does the agent learn the team's rules in this picture?" Expected: nowhere yet; only the ticket is in context. That is Section 1's problem.
- Likely question: "Is the model stateful between turns?" Answer: no; the loop re-sends the history every turn, which is why context size matters.
- Likely question: "Do tools run on my machine?" Answer: in this course every tool command runs in a container with no network (Section 3: Scope and sandbox).
- Misconception: "the agent reads the whole repository at the start". Correction: it reads only what it chooses to open, one tool call at a time; more tools are not free either, each call costs a turn and context.
- Time: 15 seconds. Next build: when the loop stops.

## Slide 10: Recap: The Anatomy of an Agentic Loop (build 2/2)
**Block:** Recap  **Time:** 0.25 min (0:02:45-0:03)  **Diagram:** docs/diagrams/agent-loop.png  **Layout:** diagram
**On the slide:**
Lead: The loop ends when the model stops calling tools, says done, or hits a limit.
Key idea: "Done" is the model's own claim. Nobody has checked it yet.
**Visual:** The full `agent-loop` diagram: prompt, agent, model, tools, and the exit arrow to "result".
**Speaker notes:**
- Plain explanation: three ways out of the loop: no more tool calls, a done claim, or a limit on turns, cost, or time.
- Concrete: Section 1: Instructions' captured run ended after 35 turns, 3 min 53 s after launch.
- Analogy: the junior engineer says "done" and walks away; nobody has reviewed the work.
- Point at the result box: today "done" is a claim, and a separate program, the referee, checks what actually shipped.
- Ask: "Who decides the work is finished in this picture?" Expected: the model itself. That is Section 4: Verification's problem.
- Likely question: "What stops a run that never ends?" Answer: the agent time limit (420 s per arm in the class profile) and a cost cap per arm.
- Misconception: "the loop is the harness". Correction: the loop is the engine; the harness is everything around it, which we build today.
- Transition sentence: "Four layers around this loop, one per section."
- Time: 15 seconds. Next: today's agenda.

## Slide 11: Today's Agenda
**Block:** Agenda  **Time:** 0.25 min (0:03-0:03:15)  **Diagram:** none  **Layout:** template-agenda
**On the slide:**
Today's Agenda
1 Instructions: what the agent knows
2 State and sessions: what it remembers
3 Scope and sandbox: what it may change
4 Verification: what proves it is done
Final A/B and all results
**Visual:** Template agenda: numbered boxes 1 to 4 joined by connectors, a "Break" marker after box 1 and after box 3, a fifth box "Final A/B and all results". No box highlighted yet.
**Speaker notes:**
- Four sections, one layer each: 50 minutes each for Section 1: Instructions, Section 2: State and sessions, and Section 3: Scope and sandbox, 45 for Section 4: Verification; breaks after Section 1 (10 min) and Section 3 (5 min); 20 minutes of final results.
- Each layer answers one question: what the agent knows, what it remembers, what it may change, what proves it is done.
- The tickets, as seven TeamTrack features: Feature 1: Org-wide issue search (Section 1), Feature 2: Comments on issues (Section 2), Feature 3: Safe retries for issue creation and Feature 4: Version checks on issue edits (Section 3), Feature 4 again (Section 4), and for the final Feature 5: Bulk close, Feature 6: Watchers, or Feature 7: Labels, picked by the room.
- Each ticket is one example in the dataset `teamtrack-features-v1` (`platform/datasets/`), written like a work ticket, with hidden tests behind it. Most come in a "trap" variant: an unfiltered legacy handler nearby (Features 1, 2, 5, 6) or a tempting shared middleware (Features 3, 4, 7).
- Commands use readable names: `make demo-3 FEATURE=version-checks`, `make final FEATURES=watchers,bulk-close`. The console still prints short codes; the glossary slide explains them once.
- Analogy: onboarding a new engineer: docs (knows), a handover note (remembers), access rights (may change), code review and CI (proves done).
- Point at box 3: the one section where the measure showed a gap before class, so it runs a live A/B.
- Ask: "Which of the four would you build first?" Expected: most say instructions. Note it; we revisit after the results.
- Misconception: "the order is arbitrary". Correction: it follows one session: what the agent sees at the start, what survives a stop, what it may touch while working, what happens when it claims done.
- Time: 15 seconds. Next: what we are building.

## Slide 12: Problem statement: What are we building?
**Block:** Problem  **Time:** 0.5 min (0:03:15-0:03:45)  **Diagram:** docs/diagrams/harness-around-loop.png  **Layout:** diagram
**On the slide:**
Lead: The harness around a coding agent, on TeamTrack, a small multi-tenant issue tracker.
Key idea: Same model; we change what it sees, remembers, may change, and must prove.
**Visual:** The full `harness-around-loop` diagram: the agent loop in the middle, four layers around it (instructions, state, scope and sandbox, verification), the referee outside.
**Speaker notes:**
- Plain explanation: we do not change the model. We change its environment: what is in its context, what survives a session stop, which files it may touch, and what counts as done.
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/) describes the job as to "design environments, specify intent, and build feedback loops". That is where the course's word "harness" comes from.
- Concrete: TeamTrack is a FastAPI issue tracker where each customer is an org; the agent adds real features to it.
- Analogy: you would not hand a new hire production access, no docs, and no CI, then judge them on their own report. The harness is the docs, the access rules, and the CI.
- Point at the referee outside the harness: it is not part of what the agent gets, and it scores what shipped the same way for both arms.
- Ask: "Why keep the referee outside the harness?" Expected: so the harness cannot grade itself.
- Likely question: "Is shipharness tied to one agent product?" Answer: no; it runs its own loop on the OpenAI API, and the starter kit copies the same files into your repository for Claude Code, Codex, or Cursor.
- Misconception: "the harness makes the agent smarter". Correction: it changes what the agent sees and may do; whether that changes the outcome is what we measure.
- Time: 30 seconds. Next: what goes wrong without it.

## Slide 13: Problem statement: The problem in the real world
**Block:** Problem  **Time:** 1 min (0:03:45-0:04:45)  **Diagram:** none  **Layout:** icon-rows
**On the slide:**
Lead: Your team gives a week of tickets on a multi-tenant issue tracker to a coding agent.
- [leak] Monday: copies an old handler with no tenant filter; tests pass, one customer reads another's issues
- [split] Tuesday: a session stops mid-migration; the next writes a second migration for the same table
- [spread] Wednesday: a fix for one endpoint lands in shared middleware; an older feature breaks
- [tick] Thursday: "done" on an edit-conflict feature that still loses updates; the only evidence is its word
Each failure costs more than the ticket saved.
**Visual:** Four icon rows, the day in bold at the start of each; the closing line in bold under them. Template subheading "The problem we're solving (in the real world)" in orange above the rows.
**Speaker notes:**
- This is the root README's story, one ticket a day. It is an illustrative scenario, not an incident from our runs; say so.
- Monday is a tenant leak: a data exposure, an incident, a disclosure, and a hunt for every copy of the pattern.
- Tuesday is a lost session: two Alembic heads (two "newest" migrations, so `alembic upgrade head` cannot pick one); the deploy is blocked until someone merges them by hand.
- Wednesday is scope creep: the ticket was one endpoint, the diff touched middleware every request runs through.
- Thursday is a false "done": the review rests on trust in the agent's own report.
- Each failure maps to one section: Monday to Section 1: Instructions, Tuesday to Section 2: State and sessions, Wednesday to Section 3: Scope and sandbox, Thursday to Section 4: Verification.
- Point at "tests pass" on Monday: the tests created one org, so a missing org filter was invisible to them.
- Ask: "Which of the four have you seen in your team?" Expected: Wednesday and Thursday most often. Take one story, 20 seconds.
- Likely question: "Are these from real incidents?" Answer: the week is illustrative, the mechanisms are not: TeamTrack has an unfiltered legacy handler, and in Section 3 every bare arm on Feature 4: Version checks on issue edits really edited a shared module.
- Misconception: "better tests would catch all four". Correction: Monday's tests created one org; Thursday's suite stayed green because the new header is optional. Tests check what their author thought of.
- Time: 1 minute. Next: why a capable agent still does this.

## Slide 14: The challenge is: The rules exist, the agent still misses
**Block:** Problem  **Time:** 0.75 min (0:04:45-0:05:30)  **Diagram:** none  **Layout:** quote-cards
**On the slide:**
Lead: The rules, tests, and code are all in the repository. The agent still misses, because:
Card 1: "anything it can't access in-context while running effectively doesn't exist." (Source 1: [Harness engineering](https://openai.com/index/harness-engineering/))
Card 2: "each new session begins with no memory of what came before." (Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))
Card 3: "Codex replicates patterns that already exist in the repository" ([Source 1](https://openai.com/index/harness-engineering/))
Card 4: "agents reliably skew positive when grading their own work" (Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps))
**Visual:** Four quote cards in a row, each with a small icon (closed book, blank page, copy, self-awarded tick), the quote in dark text and the linked source name under it.
**Speaker notes:**
- Four causes, one per card: a rule it never reads does not exist for it; each session starts with no memory; it copies whatever pattern sits nearby; it grades its own work too kindly.
- Card 3 in full: "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones."
- Source 4: [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) adds the container advice we use in Section 3: Scope and sandbox: "(Run this in a container, not your actual machine)".
- Concrete: TeamTrack has a legacy `GET /v1/issues` handler with no org filter, next to where the Feature 1: Org-wide issue search query must go. That is card 3 in one file.
- Analogy: a drive-by open-source contributor: CONTRIBUTING.md exists, they skim the nearest file instead, copy its style, and mark their own PR "tested".
- Point at the lead's word "still": nothing is withheld. The bare arm gets every rule in `platform/teamtrack/docs/HANDBOOK.md`.
- Ask: "If the rule is in the repository, why is that not enough?" Expected: on disk is not in context; the agent must choose to open it.
- Misconception: "a stronger model fixes all four". Correction: a stronger model may need fewer layers, which is why we measure each layer on the model we use.
- Likely question: "Why quote vendor engineering blogs?" Answer: these teams ran long agent loops on real code and wrote down the failures; Section 4: Verification adds three papers from Meta and Weco AI. Each quote was checked against its source, and the References slides list every one.
- Time: 45 seconds. Next: why this matters to a team.

## Slide 15: Why this matters for Engineering Teams
**Block:** Problem  **Time:** 0.25 min (0:05:30-0:05:45)  **Diagram:** none  **Layout:** two-column
**On the slide:**
Lead: Each failure costs the team; a harness costs too.
Left: What a failure costs
- Tenant leak: incident, disclosure, pattern hunt
- Lost session: two migration heads, blocked deploy
- Scope creep: regression in an older feature
- False "done": review rests on trust
Right: What a harness costs
- More turns per run
- Median 302 s against 190 s per arm
- Median $0.0123 against $0.0103 per arm
**Visual:** Two cards: failure costs on the left in amber, harness costs on the right in blue.
**Speaker notes:**
- Plain explanation: each failure costs more than the agent saved on the ticket. One missing org filter turns a small ticket into a disclosure plus an audit of every copy of the pattern.
- The harness numbers are from the runs before class: harness arms ran longer, median 302 s against 190 s, and cost more, median $0.0123 against $0.0103 per arm (exploratory, chosen after the results, so descriptive only).
- Post hoc again: harness arms hit the agent time limit in 9 of 34 runs, bare arms in 4 of 34.
- So the trade is real: every layer must buy something you can see, or it is overhead.
- Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing".
- Analogy: CI minutes. A slow pipeline is fine if it catches regressions; a slow pipeline that never fails is waste.
- Ask: "How would you know a layer is not paying off?" Expected: run the same ticket with and without it and compare a measure chosen in advance.
- Likely question: "Per run or per class?" Answer: per arm run; the whole class plan needs at most $2.36 at the caps, under a $2.50 session cap.
- Misconception: "a harness is free once written". Correction: it costs turns and wall time on every run.
- Time: 15 seconds. Next: the four gaps in one picture.

## Slide 16: Why We Need a Harness: The 4 Critical Gaps
**Block:** Problem  **Time:** 0.25 min (0:05:45-0:06)  **Diagram:** docs/diagrams/stories-causes-layers.png  **Layout:** diagram
**On the slide:**
Lead: Each story has a cause, and each cause gets one layer.
Key idea: One layer per cause: instructions, state, scope and sandbox, verification.
**Visual:** The `stories-causes-layers` diagram, three columns left to right: four stories (Monday to Thursday), four causes, four layers. One row per gap.
**Speaker notes:**
- Read the diagram row by row, left to right: story, cause, layer.
- Row 1: tenant leak, rule not in context, Section 1: Instructions: a short map in context, details on disk.
- Row 2: lost migration, no memory across sessions, Section 2: State and sessions: a progress file, a plan, and a handoff.
- Row 3: middleware edit, copied patterns and hard-to-undo actions, Section 3: Scope and sandbox: allowed paths per phase, a container with no network.
- Row 4: false "done", self-grading, Section 4: Verification: test filters and a gate; the harness, not the agent, marks a feature as passing.
- Analogy: onboarding docs, shift handover, least privilege, CI gates: practices your team already trusts for humans.
- Ask: "Which row do you expect to show the biggest difference?" Expected: guesses vary. Answer at the end: only row 3, on one ticket.
- Likely question: "Where is the sandbox?" Answer: row 3, but it is the same container for both arms, so no measurement can credit it; only the scope guard differs.
- Misconception: "one layer fixes several gaps". Correction: each layer here targets one cause; Section 3 also shows a guard can win by construction, which is not the same as being correct.
- Time: 15 seconds. Next: the app.

## Slide 17: TeamTrack: The data model
**Block:** Problem  **Time:** 0.75 min (0:06-0:06:45)  **Diagram:** docs/diagrams/teamtrack-data-model.png  **Layout:** diagram
**On the slide:**
Lead: Seven tables; two demo orgs, Acme and Globex.
Key idea: Every tenant-owned row carries org_id.
**Visual:** The `teamtrack-data-model` diagram: orgs, users, projects, project_members, issues, audit_log, idempotency_keys, with `org_id` highlighted on every tenant-owned table.
**Speaker notes:**
- Seven tables, from `platform/teamtrack/app/db/models.py`; its docstring is the key-idea line.
- Issues carry `org_id`, `project_id`, status (open, in_progress, done), priority, an assignee, a `version` column (used by Feature 4: Version checks on issue edits), and `deleted_at` for soft deletes. Users are admin, member, or viewer; every write adds one `audit_log` row.
- The seed creates Acme and Globex with an admin, a member, and a viewer each, for example `admin@acme.test`.
- Stack, TeamTrack: FastAPI, SQLAlchemy, Alembic migrations, SQLite by default, and a small board under `/board` in Jinja2 and HTMX (a small JavaScript library that swaps parts of a server-rendered page); tests in pytest; import-linter checks the layering.
- Stack, shipharness: the course's command-line tool in Python 3.12 with uv. It runs an agent with or without the harness, runs A/Bs, judges them, and serves the console on port 8765. Every tool command and the referee run in Docker containers with no network.
- LangSmith keeps a trace of every model call; ordinary traces are kept 14 days (Source 5: [LangSmith billing](https://docs.langchain.com/langsmith/billing)), so copy links you need.
- Analogy: row-level security done in application code. Every query must say `WHERE org_id = caller's org`; one missing clause is a leak.
- Ask: "Why is a missing org filter invisible to most unit tests?" Expected: the tests create one org, so every row belongs to the caller anyway.
- Likely question: "Is there real auth?" Answer: a demo token from `POST /auth/login`, for local use only.
- Misconception: "SQLite makes these toy results". Correction: what is measured (files outside the ticket, Alembic heads, org filters, done claims) does not depend on the database engine.
- Time: 45 seconds. Next: the seven house rules.

## Slide 18: House rules: seven rules in plain words
**Block:** Problem  **Time:** 0.75 min (0:06:45-0:07:30)  **Diagram:** docs/diagrams/house-rules.png  **Layout:** table
**On the slide:**
Lead: TeamTrack's handbook rules; both arms get all seven.
| House rule | TeamTrack example |
|---|---|
| House rule 1: Tenant isolation | Another org's issue answers 404, never 403 |
| House rule 2: Roles | A viewer's POST, PATCH or DELETE gets 403 |
| House rule 3: API conventions | Lists return items and next_cursor |
| House rule 4: Safe retries | Same Idempotency-Key, one new project |
| House rule 5: Audit log | Every write adds exactly one audit row |
| House rule 6: Layering | app/api never imports app/db |
| House rule 7: Migrations | One Alembic head, fresh upgrade works |
**Visual:** A native two-column table, rule name in blue, example in dark text; House rule 1 and House rule 7 rows marked as the rules Sections 1 and 2 measure. The `house-rules` grid diagram holds the same content for the repository pages.
**Speaker notes:**
- The rules come from `platform/teamtrack/docs/HANDBOOK.md`. Both arms get the full handbook; the harness arm also gets them as one line each in its map.
- House rule 1: Tenant isolation: every query on customer data filters by the caller's `org_id`; another org's resource answers 404 `not_found`, never 403, because 403 tells the caller it exists. An assignee id in a body must belong to the caller's org too.
- House rule 2: Roles: every POST, PUT, PATCH, and DELETE from a viewer returns 403 `forbidden`, using `require_writer` and `require_admin` from `app/api/deps.py`.
- House rule 3: API conventions: lists return `{"items": [...], "next_cursor": ...}` with keyset paging by ascending id (each page starts after the last id seen); errors use the `{"error": {"code", "message"}}` envelope; 201 for creates, 204 for deletes.
- House rule 4: Safe retries: the same `Idempotency-Key` header with the same body returns the first response and creates nothing new; `POST /projects` is the pattern. Issue creation does not support keys yet: that is Feature 3: Safe retries for issue creation.
- House rule 5: Audit log: one row per write, through `services.audit.record`. House rule 6: Layering: `app/api` and `app/web` never import `app/db`; import-linter checks it. House rule 7: Migrations: run `alembic heads` first, keep exactly one head.
- Every rule ends with "The check:" in the handbook, for example an Acme user with Globex ids must get 404 on every endpoint.
- Analogy: your code-review checklist, each item turned into a test that runs on every endpoint, including new ones.
- Ask: "Which rule can the code not show you?" Expected: House rule 1's "404, never 403"; nothing in a working handler says 403 leaks existence.
- Likely question: "Does the harness arm get extra rules?" Answer: no; the harness may reorganise knowledge, never add facts, and a unit test checks every rule is in the handbook both arms read.
- Misconception: "house rules are style preferences". Correction: House rule 1 is a data-exposure rule and a broken House rule 7 blocks deploys; the referee checks both from outside.
- Time: 45 seconds. Next: how we measure.

## Slide 19: How We'll Measure: Same ticket, two arms, one referee
**Block:** Problem  **Time:** 1.75 min (0:07:30-0:09:15)  **Diagram:** docs/diagrams/ab-referee.png  **Layout:** diagram
**On the slide:**
Lead: Bare arm and harness arm get the same agent, model, ticket, tools, budgets, and sandbox.
Key idea: One referee, one primary measure chosen before any run, counts per arm.
**Visual:** The full `ab-referee` diagram: one ticket splitting into two arms in identical sandboxes, both feeding one referee in a fresh container, which writes the primary verdict first, then the full verdict, to the console.
**Speaker notes:**
- An A/B is two runs of the same ticket: bare arm (ticket and repository only) and harness arm (the same plus the layers so far). Held equal: agent, model, effort, ticket, repository, tools, sandbox limits, turn limit, cost cap.
- Fairness rule: the harness may reorganise knowledge, never add facts; the bare arm has the 150-line handbook with every house rule.
- The referee runs after the agent stops, in a fresh container with no network, on a fresh copy plus the arm's diff: hidden tests, tenant isolation probes (an Acme user asks for Globex ids and expects 404), referee mutants the agent's tests should catch, and a blinded reviewer whose verdict is secondary.
- Results are counts, "0 of 3", never percentages: with one to seven runs per arm a percentage hides how few runs there are. Where both arms pass equally often we say "no measurable difference".
- In class, Sections 1, 2, and 4 run the harness arm alone ("harness in action", `make show-N`) because the A/Bs before class showed no gap; Section 3: Scope and sandbox and the final run both arms live.
- Live now, terminal B: `make doctor`. Read the key lines aloud: `accepted by OpenAI`, `accepted by LangSmith`, last line `result: + ready`. It never prints a key. If it says `SHIPHARNESS_CLASS_DATE is not set`, repeat the date step from the instructor guide; if Docker is down, `sudo systemctl start docker`.
- Then the console (running in terminal A since before class, http://127.0.0.1:8765): press `1` Live, `2` Boards, `3` Evidence, `4` A/B Report, `5` Traces, once each. `F` shows one arm full width. `make warm` ran before class, so the first launch does not pay for image start-up.
- Then the assessment printout prepared before class. Say: "This is what the bare arm works with: no map, no progress file, no feature list. The rules themselves are in both arms."
- Analogy: CI with a hidden test suite the developer cannot see, plus a reviewer who does not know which arm wrote the diff.
- Ask: "Why choose the primary measure before running?" Expected: so nobody can pick the flattering number afterwards.
- Likely question: "Does a section's A/B test that one layer?" Answer: it tests the harness so far against bare; isolating one layer needs a leave-one-out run, which the course did not run.
- Misconception: "one passing run proves the layer works". Correction: one run is one dot; it shows the layer ran, not that it helped.
- Time: 1 minute 45 seconds. Next: the terms.

## Slide 20: Glossary: the terms used in every section
**Block:** Problem  **Time:** 0.75 min (0:09:15-0:10)  **Diagram:** docs/diagrams/glossary-terms.png  **Layout:** table
**On the slide:**
Lead: One line per term; come back here when a word is new.
| Term | Meaning | Term | Meaning |
|---|---|---|---|
| Arm | One agent run, bare or harness | Tenant | One customer org and its data |
| Referee | Scores a run after the agent stops | Idempotent | A retry has no second effect |
| Primary measure | One question, chosen before any run | Optimistic concurrency | Stale save gets 412 |
| Hidden tests | Never seen by the agent | Alembic head | Newest migration; two block upgrades |
| Mutant | Code with one planted fault | Context reset | Fresh session plus written handoff |
| Allowed paths | Files a phase may change | Compaction | Old context squeezed to a summary |
| Gate | Checks run when the agent says done | Glob | Path pattern; ** spans folders |
| Harness in action | Harness arm alone, live | Least privilege | Only the access the task needs |
| Held out | Hidden, used only to score | Flaky test | Passes and fails on the same code |
| Post hoc | Chosen after results; descriptive | Ablation | Remove one layer, measure again |
**Visual:** A native four-column table, terms in blue, meanings in dark text on the light panel. The `glossary-terms` diagram holds the first eight cards for the repository pages.
**Speaker notes:**
- Arm: the bare arm gets the ticket and repository; the harness arm gets the same plus the layers built so far.
- Primary measure, Section 1: Instructions' example: "did the change add a new tenant isolation violation?", registered before any run.
- Hidden tests and mutants are the held-out checks: Feature 4: Version checks on issue edits has 69 hidden tests and 4 referee mutants; a run's own tests must fail on a mutant to catch it.
- Allowed paths and gate: the build phase writes the feature, the test phase adds tests only; in the harness arm `finish(claim="done")` runs checks first and a failure returns "Not accepted." (Section 4: Verification).
- Optimistic concurrency: `GET` returns an `ETag` holding the issue's version; a save sends it back in `If-Match`; if someone saved in between, 412 and no change. Alembic head: each migration names its parent; two with the same parent make two heads.
- Context reset versus compaction (Section 2: State and sessions); glob and least privilege (Section 3: Scope and sandbox): `app/web/**` matches every file under `app/web`.
- Defined where they come up: exec plan, handoff, keyset paging, frontmatter (the YAML header of a `SKILL.md`), Linux capabilities, loopback, reward hacking (passing checks without doing the task), compositional failure, pass^k, hill climbing.
- Console codes, said once here: the console prints `F1` to `F7` for the seven features, Feature 1: Org-wide issue search to Feature 7: Labels, in the agenda's order (`F4` is Feature 4), and `R1` to `R7` for House rule 1: Tenant isolation to House rule 7: Migrations. Commands take the readable names.
- Ask: "Hidden test or mutant: what is the difference?" Expected: a hidden test checks the feature; a mutant checks whether the agent's own tests would notice a planted bug.
- Misconception: "post hoc numbers are wrong". Correction: they are real counts, chosen after the results, so they describe and cannot confirm.
- Time: 45 seconds, opening ends at 0:10. Next: Section 1, and its launch.

## Slide 21: Section 1: Instructions, what the agent knows
**Block:** Section 1: Instructions  **Time:** 2 min (0:10-0:12)  **Diagram:** none  **Layout:** template-agenda
**On the slide:**
Today's Agenda
1 Instructions: what the agent knows (now)
2 State and sessions
3 Scope and sandbox
4 Verification
Final A/B and all results
Launch, terminal B: `make show-1`
**Visual:** The agenda slide again with box 1 highlighted and a star; boxes 2 to 4 and the final dimmed. The launch command in a monospace chip at the bottom.
**Speaker notes:**
- Section 1: Instructions, class minutes 0:10 to 1:00. The layer: what is in the agent's context and what it can find on disk.
- The ticket: Feature 1: Org-wide issue search, `GET /issues`, next to a legacy handler with no tenant filter. The referee's one question: did the change add a new tenant leak (a new House rule 1: Tenant isolation violation)?
- Launch now, about class minute 0:11, terminal B: `make show-1`. It runs `shipharness ab --section demo-1 --feature F1 --arms harness --purpose class --profile class` (`F1` is the console's code for Feature 1).
- Say: "This is harness in action: the harness arm alone, live, not an A/B. The A/Bs before class showed no gap on this ticket, so class shows the layer at work."
- Browser tab 2 (http://127.0.0.1:8765): reload the run list, open the newest run, press `1`. Look for the badge "HARNESS IN ACTION" and "placed 31 instruction files".
- Expected from the timed run before class (agent limit then 300 s, now 420 s): primary verdict about 4 min 11 s after launch, full verdict about 10 min, up to 2 min more with the 420 s limit, so done by about 0:23. Cost $0.0197 against a $0.24 cap. We open it at the DEMO slide, about 0:40.
- If it fails at once: `x OpenAI refused the key` means fix `OPENAI_API_KEY` and rerun `make doctor`; `docker run failed` means `sudo systemctl start docker`, then `make warm`, then relaunch. `ABORTED: timeout` or `ABORTED: cap` later is a result, not a failure.
- Ask: "How long is the agent instruction file in your main repository?" Expected: 20 to several hundred lines. Remember the longest; it comes back in idea 1.
- Likely question: "Is this specific to AGENTS.md?" Answer: no; CLAUDE.md, Cursor rules, and Copilot instructions play the same role.
- Misconception: "Section 1 is prompt engineering". Correction: the ticket text is identical in both arms; the layer changes which files exist and what is sent before the ticket.
- Time: 2 minutes including the launch. Next: the story behind the ticket.

## Slide 22: Failure story: The search that showed another org
**Block:** Section 1: Instructions  **Time:** 4 min (0:12-0:16)  **Diagram:** section-1-instructions/diagrams/failure-story-s1.png  **Layout:** steps
**On the slide:**
Lead: An illustrative ticket: Feature 1: Org-wide issue search, GET /issues
1. Agent finds list_all_legacy next door
2. Copies it: short, already paginates
3. Tests create one org, so they pass
4. Review approves: looks like the file
5. After release: Acme sees Globex issues
**Visual:** Five numbered step cards left to right, the last in red (the content of `failure-story-s1`). Under card 1 a small code chip: `select(Issue).order_by(Issue.id)` with "no org_id" in red.
**Speaker notes:**
- Illustrative scenario from the section's concepts page: Priya's team asks a coding agent for `GET /issues`. House rule 1: Tenant isolation lives in the team handbook, which the ticket does not mention.
- The agent lists the repository, opens the issues code, and finds `list_all_legacy`, a query from an old endpoint that lists every issue of every org.
- The real function, `app/repositories/issues.py`: its docstring says "LEGACY (used only by /v1/issues). Not tenant-scoped: do not use or copy this function." The query is `select(Issue).order_by(Issue.id).offset(offset).limit(limit)`.
- The tests create one org, so every row belongs to the caller; they pass. The reviewer sees code shaped like the rest of the file.
- Cost: a cross-tenant data exposure, an incident, a disclosure, and a hunt for every other copy of the pattern.
- Nobody broke a rule on purpose: the rule was on disk, not in front of the agent when it wrote the query.
- Analogy: a new hire copies the oldest working example in the codebase because nobody told them it is deprecated.
- Point at the code chip: the missing line is `where(Issue.org_id == actor.org_id)`.
- Ask: "Which review comment would have caught this?" Expected: "where is the org filter?", and only if the reviewer knows the rule.
- Honesty note: no run before class shipped this leak; say so now and come back to it on the results slide.
- Misconception: "the agent was careless". Correction: it picked the shortest working example next to the target file; without the rule in context that is reasonable, so the fix is context, not scolding.
- Time: 4 minutes. Next: the obvious fix, and why it is not one.

## Slide 23: Instructions: Why not paste every rule?
**Block:** Section 1: Instructions  **Time:** 4 min (0:16-0:20)  **Diagram:** section-1-instructions/diagrams/socratic-s1-step-3.png  **Layout:** key-idea
**On the slide:**
Lead: The tenant rule is in docs/HANDBOOK.md and both arms can open it. Can we paste every rule into the prompt?
Key idea: Not as the main mechanism: give the agent a map, not a manual.
- It crowds out the task and the code
- Too much guidance becomes non-guidance
- It goes stale; no script checks it
**Visual:** The final frame of `socratic-s1`: the question, the red "Why not", the three reasons. Reveal in class as question, then the key-idea box, then the rows.
**Speaker notes:**
- Ask first, pause five seconds: "Can we just paste every rule into the prompt? Shout yes or no." Expected: a split room; most say yes for a small file. Fair for TeamTrack's 150-line handbook; hold that thought for a real team's file.
- Then the verdict: no, not as the main mechanism. Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): "give Codex a map, not a 1,000-page instruction manual."
- Assignment 1: Instructions starts from a real-shaped example: an 899-line `AGENTS.md` for a TeamTrack variant with 70 tagged rules (`section-1-instructions/assignment/starter/original/AGENTS.md`).
- Reason 1, [Source 1](https://openai.com/index/harness-engineering/): "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs." The 899 lines are paid on every task.
- Reason 2: "Too much guidance becomes non-guidance." In the 899-line file the tenant rule starts at line 204 and the warning about the legacy endpoint at line 586.
- Reason 3: "It rots instantly. A monolithic manual turns into a graveyard of stale rules." The file still holds four retired rules. And a single blob "doesn't lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable." Idea 4 comes back to this.
- Analogy: a 900-line PR description, or one 900-line config file with no schema versus small typed config files with a linter.
- Likely question: "Does Claude Code not load CLAUDE.md in full anyway?" Answer: yes, it does; that is why the file must stay short and point elsewhere.
- Likely question: "Is OpenAI's experience general?" Answer: they say their results should "not be assumed to generalize without similar investment"; today we measure the idea on our model.
- Misconception: "the problem is only token cost" or "just move the tenant rule to the top". Correction: rules compete for attention and the file rots unnoticed; reordering lifts one rule and buries another.
- Time: 4 minutes. Next: idea 1, the map.

## Slide 24: 1) A map, not a manual
**Block:** Section 1: Instructions  **Time:** 4.5 min (0:20-0:24:30)  **Diagram:** section-1-instructions/diagrams/manual-vs-map.png  **Layout:** diagram
**On the slide:**
Lead: AGENTS.md is a table of contents: about 100 lines, always in context.
Key idea: The map says where each rule lives; it does not hold the rules.
**Visual:** The `manual-vs-map` diagram: on the left one tall 899-line file with the tenant rule buried in the middle; on the right a short map with arrows to `platform/teamtrack/harness/instructions/docs/SECURITY.md`, `ARCHITECTURE.md`, and the `add-endpoint` skill.
**Speaker notes:**
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere." And: "we treat it as the table of contents."
- The details live in `docs/`, "treated as the system of record". TeamTrack copies that layout: `AGENTS.md` and `ARCHITECTURE.md` at the root; `SECURITY.md`, `RELIABILITY.md`, `QUALITY_SCORE.md`, `PLANS.md`, `design-docs/`, `product-specs/`, `references/` in `docs/`.
- TeamTrack's map, `platform/teamtrack/harness/instructions/AGENTS.md`: 94 lines, keyed by "When you are about to", one file per row, all seven house rules at a glance.
- Concrete rows: "add or change an endpoint" → the add-endpoint skill; "decide who may see or change data" → `platform/teamtrack/harness/instructions/docs/SECURITY.md` (House rule 1: Tenant isolation, House rule 2: Roles). The full tenant rule lives once, in `platform/teamtrack/harness/instructions/docs/SECURITY.md`.
- "Do not copy" names `GET /v1/issues`, `repositories.issues.list_all_legacy`, and `services.legacy`, and points to `POST /projects` as the right pattern.
- Keyed by action, not topic: the agent knows what it is about to do ("touch a repository"), not which topic it needs.
- Analogy: onboarding docs with a "start here" page versus a wiki dump, or a runbook index that says which runbook to open for which alert.
- Point at the right side: one hop from the map to the rule.
- Ask: "Why key the table by action instead of topic?" Expected: the agent's next action is the lookup key it has.
- Likely question: "Why 94 lines and not 20?" Answer: one row per common action, the seven house rules, and the "Do not copy" list; shorter is fine if every row still names one file.
- Misconception: "a short map means fewer rules". Correction: the same rules, organised; a unit test checks every rule is still in the handbook both arms read.
- Time: 4.5 minutes. Next: how the details load only when needed.

## Slide 25: 2) Progressive disclosure: skills load in three tiers
**Block:** Section 1: Instructions  **Time:** 4.5 min (0:24:30-0:29)  **Diagram:** section-1-instructions/diagrams/skills-three-tiers.png  **Layout:** diagram
**On the slide:**
Lead: A small entry point first; the details only when the task needs them.
Key idea: Names and descriptions always; the body when picked; references when a step needs them.
**Visual:** The `skills-three-tiers` diagram: three stacked bands growing in size, "always in context" on tier 1, "on disk" on tiers 2 and 3, with the `add-endpoint` skill as the example in each band.
**Speaker notes:**
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front."
- Source 6: [Agent Skills Specification](https://agentskills.io/specification): "The `name` and `description` fields are loaded at startup for all skills"; instructions "< 5000 tokens recommended"; resources load "only when required".
- Tier 1: name and description of every skill, at start. Tier 2: the full `SKILL.md`, when the agent picks it. Tier 3: references, scripts, assets, when a step needs them.
- Concrete, TeamTrack's `add-endpoint`: tier 1 is its description ("Add or change a TeamTrack HTTP endpoint so it follows house rules ... Use when a ticket adds a route ..."), tier 2 the 100-line `SKILL.md`, tier 3 `references/tests.md`.
- What the runs showed: in one round every harness arm read the skill body (tier 2), and none read `references/tests.md` (tier 3). Tier 3 stayed on disk, as designed.
- The description does the routing: it "should describe both what the skill does and when to use it".
- Analogy: a man page: the one-line summary in the index, the page when you need it, "SEE ALSO" only for a specific step.
- Ask: "A skill's description says only 'Endpoint helper.' What breaks?" Expected: tier 1; the agent never opens it, so tiers 2 and 3 never load.
- Likely question: "Do Claude Code, Codex, and Cursor all do this?" Answer: all three read Agent Skills from a skills folder: Source 7: [Extend Claude with skills](https://code.claude.com/docs/en/skills), Source 8: [Build skills](https://learn.chatgpt.com/docs/build-skills), Source 9: [Agent Skills (Cursor docs)](https://cursor.com/docs/skills); post-class reading 03 lists where each one looks.
- Misconception: "skills are plugins with code". Correction: a skill is a folder with a Markdown recipe; scripts are optional tier 3 files.
- Time: 4.5 minutes. Next: how the map reaches the model.

## Slide 26: 3) The context prefix: small, fixed, out of reach
**Block:** Section 1: Instructions  **Time:** 4.5 min (0:29-0:33:30)  **Diagram:** section-1-instructions/diagrams/context-prefix.png  **Layout:** diagram
**On the slide:**
Lead: Sent first in every session: a usage note, the whole map, the skills catalogue.
Key idea: Built once from the course's copy, so agent edits to AGENTS.md change nothing.
**Visual:** The `context-prefix` diagram: the first message of a session as a stack (core system prompt, then the prefix: sentence, map, catalogue), with docs and skill bodies outside the stack, on disk, reached by `read_file`.
**Speaker notes:**
- Plain explanation: the prefix is what the harness arm sees before the ticket, in every session. Only the map and the catalogue go in; documents and skill bodies stay on disk. The bare arm gets the same core prompt without the prefix.
- The map file has 94 lines; the agent gets 92, because two walkthrough comment lines are stripped.
- The code, `platform/src/shipharness/harness/instructions/router.py` lines 37-47, the body of `build_prefix`: three blocks, one usage sentence, the map, the skills catalogue, joined with blank lines.
- Key line: `agents_md = strip_markers((source / MAP_FILE).read_text(encoding="utf-8")).strip()`. `source` is `platform/teamtrack/harness/instructions/`, never the arm's workspace; `strip_markers` drops the two comment lines.
- `catalogue_block()` reads only each skill's frontmatter and writes one line per skill (name, description, path): tier 1 only.
- Same layer, not on screen: `context_prefix` in `layer.py` (lines 113-116) caches the string so every session gets identical text, the "small, stable entry point" of Source 1: [Harness engineering](https://openai.com/index/harness-engineering/); `after_tool` (lines 126-136) logs each harness file the agent opens and tags skill reads with their tier. It returns a note and never blocks; those notes are the "agent read skill add-endpoint (tier 2)" lines on screen 1.
- "Context prefix" is the course's term, not a source's.
- Analogy: least privilege for instructions, or an immutable config object built at startup from a read-only mount: the agent can read its orders but not rewrite them.
- Ask: "What would go wrong if `source` pointed at the workspace?" Expected: the agent could rewrite its own instructions mid-run, and session 2 would get the edited map.
- Likely question: "Do I need this code to use a map?" Answer: no; most coding agents load `AGENTS.md` and skills themselves. Write code like this only if you run your own loop.
- Misconception: "the agent sees the docs because they are in the repository". Correction: only the map and the catalogue are sent; screen 3 later shows which docs it opened.
- Time: 4.5 minutes. Next: keeping the map true.

## Slide 27: 4) Mechanical checks keep the map true
**Block:** Section 1: Instructions  **Time:** 4.5 min (0:33:30-0:38)  **Diagram:** section-1-instructions/diagrams/checker-flow.png  **Layout:** diagram
**On the slide:**
Lead: One big file can't be checked by a script. A map and focused docs can.
Key idea: Links resolve, each rule lives in one doc, retired rules stay out.
**Visual:** The `checker-flow` diagram: "map + docs + skill" → "checker" → a green terminal chip `OK: 13 files, 147 links, 66 rules covered`, with a red chip `ERROR: broken link` below it.
**Speaker notes:**
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly."
- And: "we write the error messages to inject remediation instructions into agent context." A lint message that says how to fix the problem teaches the agent too.
- The four checks: every link in the map resolves; every active rule lives in exactly one doc; retired rules never come back; the skill header (frontmatter) passes the validator.
- Assignment 1: Instructions asks you to write `checker/check_docs.py`; the reference checker on the reference tree prints `OK: 13 files, 147 links, 66 rules covered`.
- Skill check: `uv run shipharness skills validate platform/teamtrack/harness/instructions/.agents/skills` checks the frontmatter (name matches the folder, description present, no extra fields).
- Fairness check: `platform/tests/unit/harness_instructions/test_parity.py` fails if a rule in the harness docs is missing from the handbook both arms read. "Reorganise, never add."
- Analogy: CI gates for documentation: a broken link fails the build like a broken import.
- Ask: "Your map points to `platform/teamtrack/harness/instructions/docs/SECURITY.md` and someone renames it. What happens without a check?" Expected: the agent follows a dead pointer and falls back to nearby code.
- Likely question: "Who fixes a failing doc check?" Answer: whoever moved the file, in the same pull request.
- Misconception: "a link checker is enough". Correction: every link can resolve while a rule silently disappears; the coverage check (each of the 66 active rules in exactly one doc) catches that.
- Instructor cue: glance at terminal B; `make show-1` should have printed its `Cost:` line by now.
- Time: 4.5 minutes. Next: the four ideas on one page.

## Slide 28: Cheat Sheet: The instructions layer in four moves
**Block:** Section 1: Instructions  **Time:** 2 min (0:38-0:40)  **Diagram:** section-1-instructions/diagrams/cheat-sheet-s1.png  **Layout:** table
**On the slide:**
Lead: It informs. It never blocks.
| Move | What it does |
|---|---|
| Map | About 100 lines, points to docs |
| Disclosure | Names first, bodies on demand |
| Prefix | Fixed, built from a read-only copy |
| Checks | Links, rule coverage, no new facts |
**Visual:** A native four-row table; the lead line in amber across the top. The `cheat-sheet-s1` diagram holds the same four cards for the repository pages.
**Speaker notes:**
- One sentence for the layer: a short map always in context, pointing to focused documents and skills the agent opens only when the task needs them.
- Map: keyed by action, one file per row, house rules at a glance, "Do not copy" for legacy code.
- Disclosure: tier 1 always, tier 2 when picked, tier 3 when a step needs it.
- Prefix: built once from a copy the agent cannot edit, the same for every session.
- Checks: a script keeps links, rule coverage, and parity true; a test keeps the A/B fair.
- "It never blocks": the layer's `after_tool` hook returns notes, never a refusal. A guarantee needs Section 3: Scope and sandbox or Section 4: Verification.
- Analogy: a warning-level lint rule: it points at the problem and never fails the build.
- Ask: "Which row would you add to your repository first?" Expected: the map; follow up with "and which check keeps it true?"
- Misconception: "if the agent reads the map, it will follow the rules". Correction: reading is not applying; the referee checks shipped code, not the reading list.
- Time: 2 minutes. Next: the live run.

## Slide 29: Section 1: Instructions - Implementation Notes: The map at work
**Block:** Section 1: Instructions  **Time:** 10 min (0:40-0:50)  **Diagram:** none  **Layout:** template-demo
**On the slide:**
DEMO - 1
Section 1: Instructions - Implementation Notes: The map at work
**Visual:** Template DEMO layout: "DEMO - 1" badge and the title only; no screenshot. Switch to the console.
**Speaker notes:**
- Files for this demo: `section-1-instructions/demo/run.sh` (the command), `section-1-instructions/demo/walkthrough.md` (the code, explained), `section-1-instructions/demo/harness/` (the map, docs, and skills the arm gets), `section-1-instructions/demo/expected/` (the captured run, the fallback), `docs/evidence/s1.md` (every number), console http://127.0.0.1:8765.
- Switch to browser tab 2, the run of `make show-1` launched at about 0:11. It should have finished by about 0:23. Walk screens 1, 3, 2, 5, 4.
- Screen 1 (`1`), Live. Point at "HARNESS IN ACTION", then the decisions: "placed 31 instruction files (AGENTS.md map, docs, skills)", "agent read ARCHITECTURE.md", "agent read skill add-endpoint (tier 2)". Say: "Map and skill read before any code."
- Screen 1, lower: patches to the issues service, route, and tests; "No gate." (that layer comes in Section 4: Verification); the test phase; the pill "primary verdict ready" and the results row.
- Read today's verdict aloud. Pass: "No new tenant leak. One run shows the layer ran, not that it helped." Fail: "A leak shipped with the map in place. That is a result."
- Captured run before class, for comparison (agent limit then 300 s): minute 1, 31 files placed, map and skill read, patches to service, route, tests; minute 3, the test phase wrote and ran `test_org_issue_search.py`; 3:53, run ended after 35 turns; 4:11, primary verdict PASS, 0 new violations; 10:00, hidden tests 52 of 52, referee mutants 2 of 4, reviewer accepted; 10:14, cost line $0.019744.
- Say about mutants 2 of 4: "The agent's own tests caught half of the referee's planted bugs. Section 4: Verification is about that gap." About 3:53 to 4:11: "18 seconds from agent done to the answer this section cares about."
- Screen 3 (`3`), Evidence. Point at files read, grouped as skill, harness doc, handbook, code, test; the five changed files; the referee line `r1_tenant: 0 new` (`r1_tenant` is the House rule 1: Tenant isolation check). Say: "The old `/v1/issues` leak is starting code and does not count."
- Screen 3, also say: in the captured run the agent opened the skill, `ARCHITECTURE.md`, and the handbook, but not `platform/teamtrack/harness/instructions/docs/SECURITY.md`. Only `read_file` calls appear; a `cat` in a shell does not.
- Screen 2 (`2`), Boards: the board as `admin@acme.test`, badge "only own-org cards, no duplicates". Feature 1: Org-wide issue search changes no board pixels, so there is one frame.
- Screen 5 (`5`), Traces: the referee event tail and LangSmith links; open one to show every model call. Screen 4 (`4`), A/B Report: the dots from before class; today's verdict sits at the top, not as a dot. Say: "One run in class is not a dot in the comparison."
- Code to mention while on screen 1: the prefix comes from `build_prefix` in `router.py` (idea 3); `walkthrough.md` has every excerpt.
- If the screen differs from the capture (other files read, turns, times): say so and compare the order of events, not the minutes. `ABORTED: timeout` or `ABORTED: cap`: it is still judged; say which limit and read the verdict.
- If the run is still going: walk screen 1 live, teach the results slide, and come back for the verdict.
- If it failed for a reason outside the experiment (Docker, network, OpenAI account): say so, then `make replay RUN=<id>` with the fallback id recorded the day before (red RECORDING badge). If Docker is down, walk `section-1-instructions/demo/expected/`: screen-1 frames in minute order, then screens 3, 2, 5, 4, and `terminal.txt`, saying "recorded before class".
- Time: 10 minutes. Next: what the measurements say.

## Slide 30: What we measured: No measurable difference on org-wide search
**Block:** Section 1: Instructions  **Time:** 6 min (0:50-0:56)  **Diagram:** section-1-instructions/diagrams/results-s1.png  **Layout:** two-column
**On the slide:**
Lead: Earns its place when rules are many, far from code, and the code cannot show them.
Left: What we measured
- A run fails if it adds a tenant leak
- Bare arm: 0 of 7 runs failed
- Harness arm: 0 of 7 runs failed
Right: Apply it Monday
- Count your instruction file's lines
- One "read first" row per action
- "Do not copy" for legacy code
- A link and rule check in CI
**Visual:** Left card holds the `results-s1` dot chart (one dot per run, bare grey, harness blue, every dot filled, by round: medium effort 3, low effort 3, class settings 1) above its three lines; right card is a checklist with empty tick boxes.
**Speaker notes:**
- Before class: 0 of 7 bare-arm runs shipped a new tenant leak, and 0 of 7 harness-arm runs. Rounds: medium effort (3 per arm), low effort (3), class settings (1). Say plainly: no measurable difference on this task with this model.
- Every arm in every round passed 52 of 52 hidden tests; an earlier round on the plain ticket gave the same, 0 of 3 per arm.
- In the class-settings run the bare arm did not open the handbook in its first nine tool calls and still wrote an org-scoped query. Neither arm copied the legacy query, so the map had nothing to fix.
- Post hoc (descriptive only), 10 runs per arm: harness arms claimed done in 5, bare in 9, no false claim in either; median cost $0.0122 against $0.0103.
- Earns its place: many or long rules far from the code; a rule the code cannot show ("404, never 403"); several maintainers; a recurring task worth a skill. Not when: the model already does it, the ticket points to the rule, the map is stale, or you need a guarantee (it never blocks).
- Monday, in your repository: count the lines of AGENTS.md or CLAUDE.md against the "roughly 100" of Source 1: [Harness engineering](https://openai.com/index/harness-engineering/); list three rules your agent breaks and where each lives; rewrite the top as a "When you are about to → Read first" table; add "Do not copy" naming the legacy pattern and the file to copy instead.
- Then keep it true: a CI check for links and rule coverage (Assignment 1: Instructions has you write one), and a log of which docs the agent opens. Spoken extra: one skill for your most common agent task.
- Starter kit: `uv run shipharness init --target ../your-repo` copies the map and doc templates with a REPLACE marker on every TeamTrack value; see `use-in-your-repo/README.md`.
- Ask (discussion): "The bare arm read the same rules and applied them. What would have to be true for the map to earn its place?" Expected: a model or ticket where bare arms leak, more rules, or maintenance value you can name.
- Likely question: "Was the trap too weak?" Answer: possibly; in one round no arm opened the legacy files. A stronger trap needs a new registered test, not a reinterpretation.
- Misconception: "no difference means maps are useless" or "delete the long file once the map exists". Correction: one bet on one model and ticket; and move every rule and check coverage first, a lost rule is a silent regression.
- Time: 6 minutes. Next: questions.

## Slide 31: Q&A: Section 1: Instructions
**Block:** Section 1: Instructions  **Time:** 4 min (0:56-1:00)  **Diagram:** none  **Layout:** template-qa
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
**Visual:** Template Q&A slide unchanged.
**Speaker notes:**
- Take questions from the chat first; TAs pick the top ones.
- Likely: "Is the harness arm not just given more information?" Answer: no; it may reorganise knowledge, never add facts, and `test_parity.py` checks the rules match.
- Likely: "Why not paste the whole handbook into the prompt?" Answer: "Too much guidance becomes non-guidance"; it crowds out the task and goes stale.
- Likely: "Does the files-read list on screen 3 prove the harness worked?" Answer: no; it explains a path. The score is what the referee finds in shipped code.
- Likely: "Would the map help a weaker model?" Answer: unknown; we measured one model. `make demo-1` runs both arms on Feature 1: Org-wide issue search if you want to find out.
- Likely: "What does the agent see of a skill at the start?" Answer: one catalogue line: name, description, and the path to `SKILL.md`.
- Misconception if it comes up: "the map failed". Correction: the model did not need it on this ticket; that is a measured finding about the bet.
- After class: Assignment 1: Instructions (`make check-assignment-1` fails on the starter by design), the post-class readings, `section-1-instructions/session-notes.md`.
- Time: 4 minutes, section ends at 1:00. Next: a 10-minute break.

## Slide 32: Time for a Break
**Block:** Break  **Time:** 10 min (1:00-1:10)  **Diagram:** none  **Layout:** template-break
**On the slide:**
A 10-minute break is starting now. Please return when the timer ends to continue the presentation
**Visual:** The template's break layout and timer picture. Write the return time next to the timer.
**Speaker notes:**
- Write the return time (1:10) on the slide before you step away.
- Nothing runs during the break; leave the console (terminal A) open.
- Check terminal B is free: Section 2: State and sessions launches `make show-2 SESSION_BUDGET=12,38` on its first slide, at about 1:11.
- If a learner's setup failed, point them to `setup/README.md` and `docs/troubleshooting.md`.
- Transition: "Welcome back. The agent now knows the rules. Next: what happens when its session ends halfway through the work."

## Slide 33: Section 2: State and sessions, what it remembers
**Block:** Section 2: State and sessions  **Time:** 2 min (1:10-1:12)  **Diagram:** none  **Layout:** template-agenda
**On the slide:**
1 Instructions
2 State and sessions (now)
3 Scope and sandbox
4 Verification
Final A/B
Launch, terminal B: `make show-2 SESSION_BUDGET=12,38`
**Visual:** Template agenda: box 1 outlined as done, box 2 highlighted with the star, the rest pale; the launch command in a monospace chip at the bottom.
**Speaker notes:**
- Section 2: State and sessions asks what survives when a session stops before the work is done. The ticket: Feature 2: Comments on issues, a `comments` table, endpoints, and a board panel, too big for one 12-turn session.
- The primary verdict: did session 2 break or redo session 1's work? A continuity failure is two Alembic heads or a failed fresh upgrade (House rule 7: Migrations), a table created by two migrations, or session 2 removing 30% or more of the lines session 1 added.
- Launch now, about 1:11, terminal B: `make show-2 SESSION_BUDGET=12,38`. Session 1 gets 12 turns, session 2 gets 38; without `SESSION_BUDGET` session 1 runs the ticket's 20 turns.
- Browser tab 2: reload the run list, open the newest run, press `1`. Say: "Harness arm alone, not an A/B; the comparison was done before class."
- Expected, timed run on 2026-10-17 (300 s agent limit then, 420 s now, so up to 2 minutes longer): session 1 stopped at 1 min 23 s, primary verdict 6 min 46 s, full verdict 9 min 52 s, cost $0.029525. Done by about 1:23; the DEMO slide is at about 1:40.
- If `x OpenAI refused the key`: fix `.env`, `make doctor`, relaunch. If `x SHIPHARNESS_CLASS_DATE is not set`: `sed -i "s/^SHIPHARNESS_CLASS_DATE=.*/SHIPHARNESS_CLASS_DATE=$(date +%F)/" .env`, relaunch. If the console says `address already in use`: `make console CONSOLE_PORT=8766`.
- Analogy: an on-call handover: the next engineer arrives with no memory of the last shift; the note is all they have.
- Ask: "How does your agent know what yesterday's session did?" Expected: mostly it doesn't; people paste a summary or hope it reads git.
- Likely question: "Isn't a longer context window the fix?" Answer: a session still ends somewhere, by a turn limit, a crash, or a timeout; this section is about that moment.
- Misconception: "state means a database or a memory service". Correction: here state is a few plain files and the git history, checked into the repository.
- Time: 2 minutes including the launch. Next: the failure we guard against.

## Slide 34: Failure story: The second session redoes the first
**Block:** Section 2: State and sessions  **Time:** 4 min (1:12-1:16)  **Diagram:** section-2-state-lifecycle/diagrams/failure-story-s2.png  **Layout:** steps
**On the slide:**
Lead: An illustrative ticket: Feature 2: Comments on issues, over two sessions
1. Session 1 writes the comments migration, stops at its limit
2. Half an endpoint, uncommitted, no note left
3. Session 2 starts with an empty context
4. Writes a second migration from the old head
5. Two Alembic heads block the deploy
**Visual:** Five numbered step cards, the last in red (the content of `failure-story-s2`).
**Speaker notes:**
- Illustrative scenario from the concepts page: Marco asks a coding agent for comments on TeamTrack issues: a `comments` table, three endpoints, a board panel. It is built from the failure in Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): a session that ends "with a feature half-implemented and undocumented", leaving the next one "to guess at what had happened".
- Session 1 leaves a migration, half an endpoint, no note, and a ticket that still says "add comments". Session 2 writes a second migration; a reviewer untangles two versions of one change; the team pays twice.
- House rule 7: Migrations says exactly one Alembic head and a working fresh upgrade. Two migrations that both name `0001_initial` as their parent make two heads; `alembic upgrade head` refuses to pick one.
- Analogy: two engineers on different shifts each writing the same schema change because nobody wrote "I already did the migration" on the ticket.
- Point at card 5: that fork is what the referee's migrations check looks for in every run.
- Ask: "Session 2 has the whole repository, including the uncommitted migration. Why would it write a second one?" Expected: having the file is not looking at it; without `git status` or a look at `migrations/versions` it works from the ticket alone.
- Likely question: "Would CI catch two heads?" Answer: migration checks do, but only after the duplicate work is done and paid for; the goal is that session 2 never starts it.
- Likely question: "Did this happen in your runs?" Answer: not on this model; keep that for the results slide.
- Misconception: "uncommitted work is lost work". Correction: the files are on disk; nothing tells the next session to look.
- Time: 4 minutes. Next: why a capable model redoes work.

## Slide 35: Fresh session: Why redo work already on disk?
**Block:** Section 2: State and sessions  **Time:** 4 min (1:16-1:20)  **Diagram:** section-2-state-lifecycle/diagrams/socratic-s2-step-3.png  **Layout:** key-idea
**On the slide:**
Lead: Session 2 has the whole repository but an empty context. Can we carry the old context over?
Key idea: Not on its own: "compaction isn't sufficient." Reset, then hand over written state.
- Compaction keeps a squeezed copy with gaps
- The repository holds the work, but unread
**Visual:** The final frame of `socratic-s2`: question, red "Why not", the two reasons. Reveal as question, key-idea box, then rows.
**Speaker notes:**
- Ask first: "Can we just carry the old context over, squeezed down?" Expected: many say yes, summarise or compact it.
- Every session is a fresh model call: Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): "each new session begins with no memory of what came before." In our runs session 1 gets 12 turns, session 2 gets 38; the stop is the same for both arms.
- The verdict, [Source 2](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): "However, compaction isn't sufficient." A compacted transcript still says "I started the migration" without where the file is or whether it was committed.
- Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) says compaction "preserves continuity" but does not give the agent "a clean slate".
- Reason 2: the repository has the truth, but only if the session reads it first. In one test run before class, the bare arm's session 2 ran `git status` as its fourth tool call, saw `?? migrations/versions/0002_comments.py`, and carried on. Nothing told it to.
- Analogy: a `git stash` nobody mentioned: only someone who runs `git stash list` finds it. Or a meeting summary versus the actual pull request.
- Ask: "What would you write down for the next session?" Expected: what I did, what is left, what to watch for, how to check the app still works. The four ideas answer it.
- Likely question: "Is the 12-turn stop realistic?" Answer: it is a session turn budget, so the stop lands at a known point in both arms; real sessions end by limits, timeouts, crashes.
- Likely question: "Why not just tell the agent to run `git status`?" Answer: that is part of the answer: the getting-up-to-speed routine, idea 4.
- Misconception: "a bigger summary is a better summary". Correction: the next session needs facts it can check against the repository, not a longer story.
- Time: 4 minutes. Next: idea 1, the planned stop.

## Slide 36: 1) Session lifecycle: a planned stop and reset
**Block:** Section 2: State and sessions  **Time:** 4.5 min (1:20-1:24:30)  **Diagram:** section-2-state-lifecycle/diagrams/session-lifecycle.png  **Layout:** diagram
**On the slide:**
Lead: Every session: get up to speed, work and commit, wrap up, stop.
Key idea: At the stop, the harness writes the facts, whatever the agent did.
**Visual:** The full `session-lifecycle` diagram: session 1 (up to speed, work, wrap-up), the stop where the harness writes the facts into the repository, session 2 reading the files first.
**Speaker notes:**
- The source term, Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps".
- Two routines wrap each session, both from Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): "Getting up to speed" at the start, and "End the session by writing a git commit and progress update."
- Near the end of each session both arms get the same message, "This session is ending soon." In the captured run, turns 1.10 and 1.11 updated and committed the state files, and turn 1.12 called `finish(claim="not_done")`.
- A runner bug we found by reading runs: earlier, any `finish` ended the build phase, so session 2 never ran. Now `finish(claim="not_done")` before the last session ends only that session, in both arms.
- The code at the stop, `platform/src/shipharness/harness/state/lifecycle.py` lines 100-111, the body of `session_stop`: compute the facts, merge them into the handoff, append a progress line, commit.
- Key line: `summary, tests = machine_summary(ctx, result, files_changed, timeout_s)`. It reads the last commits, files changed, the visible test result, open TODO markers, the migration heads, and the docs the agent opened; it runs the visible suite once per stop on harness time, not the agent's turns.
- `commit_paths` names its paths, so anything half-staged stays out; its message, "harness: session N handoff for ..." is the first line session 2 sees in `git log`. If the agent deleted `progress.md`, the code falls back to the template and the log line still lands.
- Analogy: a shift pattern with a fixed handover time, or a CI job that writes a build summary on every run instead of asking the developer to fill in a form.
- Ask: "Why does the harness write at the stop instead of trusting the wrap-up turns?" Expected: the agent can run out of turns before writing anything.
- Likely question: "Who decides when the session ends?" Answer: the runner, by the session turn budget (12 then 38 here), or the agent by calling `finish`.
- Misconception: "a reset throws work away" or "the harness summarises the conversation". Correction: it clears the context, not the repository, and it never reads the transcript, only the repository.
- Time: 4.5 minutes. Next: the file that crosses the stop.

## Slide 37: 2) The handoff: two owners, one file
**Block:** Section 2: State and sessions  **Time:** 4.5 min (1:24:30-1:29)  **Diagram:** section-2-state-lifecycle/diagrams/handoff-contents.png  **Layout:** diagram
**On the slide:**
Lead: session-handoff.md carries the last session's state and the next steps.
Key idea: The harness writes the facts from git; the agent writes its notes; neither overwrites the other.
**Visual:** The `handoff-contents` diagram: the file in two bands, "Machine summary (harness, from git)" on top (commits, files changed, tests, migration heads) and "Notes from the agent" below (doing, left, watch out for).
**Speaker notes:**
- The harness owns "Machine summary" and rewrites it at every stop. The agent owns "Notes from the agent". `handoff.merge` replaces only the harness part and keeps the agent's notes as written.
- Example fact line: the migration heads line ends `house rule R7 needs exactly one` when it finds two heads (`R7` is the code's name for House rule 7: Migrations), so session 2 sees the problem before writing another migration.
- Real agent notes from the captured run: "API/web must not import `app.db`; all customer queries must filter org." A fresh session cannot see that in the code.
- Session 2 is told: `resume_text` adds "Start with the Getting up to speed steps before you change code" plus the machine summary, after the neutral resume sentence both arms get.
- Analogy: an incident handover in two parts: the dashboard snapshot (facts, generated) and the engineer's note (judgement, written).
- Point at the top band: it exists even when the bottom band is empty.
- Ask: "Which facts would you never trust the agent to write?" Expected: what was committed, which files changed, whether tests pass, how many heads.
- Likely question: "What if the agent writes wrong notes?" Answer: they stay as written; the summary above is regenerated from git at every stop, so session 2 can check one against the other.
- Likely question: "What if the agent deletes the file?" Answer: the harness rebuilds it from its template at the next stop.
- Misconception: "a handoff written by the agent is enough". Correction: it is empty exactly when the agent ran out of turns.
- Time: 4.5 minutes. Next: the plan and the ledger for the whole task.

## Slide 38: 3) The exec plan and the progress ledger
**Block:** Section 2: State and sessions  **Time:** 4.5 min (1:29-1:33:30)  **Diagram:** section-2-state-lifecycle/diagrams/exec-plan-ledger.png  **Layout:** diagram
**On the slide:**
Lead: Two checked-in files: progress.md (done, in progress, next) and the exec plan.
Key idea: "it should always be possible to restart from _only_ the ExecPlan and no other work."
**Visual:** The `exec-plan-ledger` diagram: the exec plan (progress, surprises, decisions, outcomes) and `progress.md` (done, in progress, next, session log) side by side, "harness appends one entry per stop" on the session log, "restart from these alone" under both.
**Speaker notes:**
- The key-idea quote is from Source 10: [Using PLANS.md for multi-hour problem solving](https://cookbook.openai.com/articles/codex_exec_plans), which asks for four living sections: Progress, Surprises & Discoveries, Decision Log, Outcomes & Retrospective.
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/) keeps "execution plans with progress and decision logs that are checked into the repository".
- `progress.md` is the course's name for the `claude-progress.txt` of Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): what each session did and what is next. The agent edits every section except "Session log", where the harness appends one entry per stop.
- Example decision for the Decision Log: "comments use keyset paging, ascending id, like projects", so session 2 does not reopen it.
- The harness's own plan for comments says a new session must be able to restart from the plan, `progress.md`, and the git log alone.
- Analogy: a design doc plus a changelog: the doc says what and why, the changelog what happened when.
- Ask: "Could someone restart your current task from only your notes?" Expected: usually no; decisions live in chat or in someone's head.
- Likely question: "Why Markdown here and JSON for the feature list later?" Answer: these are notes the agent writes freely; the feature list in Section 3: Scope and sandbox is graded state the agent must not edit.
- Misconception: "the plan is written once at the start". Correction: it is a living document; progress lines get a UTC timestamp, and the harness moves the plan to `completed/` when the feature passes.
- Time: 4.5 minutes. Next: the routine that reads these files first.

## Slide 39: 4) Getting up to speed: init.sh before code
**Block:** Section 2: State and sessions  **Time:** 4.5 min (1:33:30-1:38)  **Diagram:** section-2-state-lifecycle/diagrams/alembic-heads.png  **Layout:** diagram
**On the slide:**
Lead: "Read the git logs and progress files to get up to speed on what was recently worked on."
Key idea: Read state, then run init.sh: one migration head and a basic test, before any code.
**Visual:** The `alembic-heads` diagram: one head passes `init.sh`; two heads trip House rule 7: Migrations. A small terminal card beside it with session 2's first call: `pwd; git log --oneline -20; cat progress.md`.
**Speaker notes:**
- The routine is a heading in Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), "Getting up to speed": read the git log and progress file, then run `init.sh` and a basic test before touching code, because new work on a broken app "would likely make the problem worse."
- Session 2's first calls in the captured run: `pwd; git log --oneline -20`, then `cat progress.md` and `cat session-handoff.md`, then the plan `section-2-state-lifecycle/demo/harness/docs/exec-plans/active/F2.md` (`F2` is the code for Feature 2: Comments on issues), then `bash init.sh`.
- TeamTrack's `init.sh` runs `alembic heads`, `alembic upgrade head` on a scratch SQLite database, then `pytest tests/visible/test_issues.py -x`, and leaves no files to commit.
- In the captured run session 2's git log began with the harness's session 1 handoff commit, and session 2 wrote exactly one migration, `0002_comments.py`, from the current head.
- Analogy: the first ten minutes of an on-call shift: read the handover, check the dashboards are green, then start.
- Point at the `alembic heads` line: one command would have stopped the opening story.
- Ask: "What is the cheapest check that would have prevented the two-head story?" Expected: list the heads before writing a migration.
- Likely question: "Who writes `init.sh`?" Answer: an initializer step before session 1. The source uses a model session; the course uses plain code, because one ticket fixes the files, so it costs no model call.
- Misconception: "`init.sh` is for humans setting up a laptop". Correction: here it is the agent's smoke test at the start of every session.
- Time: 4.5 minutes. Next: four files on one card.

## Slide 40: Cheat Sheet: Four state pieces across a stop
**Block:** Section 2: State and sessions  **Time:** 2 min (1:38-1:40)  **Diagram:** section-2-state-lifecycle/diagrams/cheat-sheet-s2.png  **Layout:** table
**On the slide:**
Lead: Four files, one job each; refer back when you add state to your repo.
| File | Job | Who writes it |
|---|---|---|
| init.sh | Setup and a basic test | Harness |
| progress.md | What each session did, what's next | Both |
| Exec plan | Plan, decisions, restart bar | Agent |
| session-handoff.md | Harness facts plus agent notes | Two owners |
**Visual:** A native three-column table; the "Who writes it" column as small tags. The `cheat-sheet-s2` diagram holds the same rows for the repository pages.
**Speaker notes:**
- Four files, each with one job, plus the git history that ties them together.
- The initializer step writes all four and commits them before session 1, as "harness: initializer step for ..." in the git log.
- Point at "Who writes it": ownership is the design decision, more than the file names.
- Analogy: README, CHANGELOG, design doc, and handover note in a well-run repository: each answers one question for whoever arrives next.
- Ask: "Which of these does your repository already have under another name?" Expected: a README with setup steps, sometimes a TODO file, rarely a handoff.
- Likely question: "Do I need all four?" Answer: no; measure. The results slide shows no measurable difference on this ticket with this model.
- Misconception: "more state files mean more reliable agents". Correction: they cost turns; harness arms hit the agent time limit more often (post hoc, next slides).
- Instructor cue: `make show-2` should have printed its `Cost:` line; read the session figure aloud.
- Time: 2 minutes. Next: the live run.

## Slide 41: Section 2: State and sessions - Implementation Notes: Stop and resume
**Block:** Section 2: State and sessions  **Time:** 10 min (1:40-1:50)  **Diagram:** none  **Layout:** template-demo
**On the slide:**
DEMO - 2
Section 2: State and sessions - Implementation Notes: Stop and resume
**Visual:** Template DEMO layout: "DEMO - 2" badge and the title only; no screenshot. Switch to the console.
**Speaker notes:**
- Files for this demo: `section-2-state-lifecycle/demo/run.sh`, `section-2-state-lifecycle/demo/walkthrough.md`, `section-2-state-lifecycle/demo/harness/` (the state files the arm starts with), `section-2-state-lifecycle/demo/expected/` (the captured run, the fallback), `docs/evidence/s2.md`, console http://127.0.0.1:8765.
- Switch to browser tab 2, the run of `make show-2 SESSION_BUDGET=12,38` launched at about 1:11; it should have finished by about 1:23. Walk screens 1, 3, 2, 5, 4.
- Screen 1 (`1`), Live. Scroll to the pill "Session 1 stopped" and say: "Turn budget spent: 12 turns." Point at "session 1 handoff written", then "Session 2 resumed · prefix: core, instructions, state". Say: "Session 2 starts with an empty context; only the files carry over."
- Screen 1, turn 2.1: point at `pwd; git log --oneline -20; cat progress.md`. Say: "It reads state first, before any code." Then session 2 writes the model, service, route, seed, and one migration `0002_comments.py`; then "primary verdict ready".
- Read today's verdict. Pass: "Session 2 picked up the work. No continuity failure." Fail: "The handoff did not carry the work. Screen 3 shows how."
- Captured run before class (300 s agent limit): 0:00 initializer writes four files and commits; 1:23 session 1 stops at 12 turns, handoff committed, session 2 resumes; 6:36 run ends at the time limit after 43 turns (`ABORTED: timeout`, exit 2, still judged); 6:46 primary verdict PASS; 9:52 full verdict, hidden 56 of 56, mutants 0 of 4; command finished at 10 min 7 s.
- Say: "Session 1 spent its 12 turns reading and wrapping up; session 2 built in its 31 turns. So a PASS on continuity tells us little here: there was little to redo." Mutants 0 of 4: the agent shipped no tests that catch the referee's mutants, Section 4: Verification's subject.
- Screen 3 (`3`), Evidence. Point at the Sessions table (capture: "Session 1 · 12 turns · claim_not_done", "Session 2 · 31 turns"), then `continuity: 0 new` and `r7_migrations: 0 new` (`r7_migrations` is the House rule 7: Migrations check).
- Screen 3, also `diff_scope: 1 new`: an edit to `app/api/issues.py`, outside the Feature 2: Comments on issues ticket's allowed paths. Say: "Nothing stopped it: the scope layer starts in Section 3: Scope and sandbox."
- Screen 2 (`2`), Boards: Acme user, own-org cards only; the comments panel is on the issue page, and hidden tests judge it.
- Screen 5 (`5`), Traces: the first wrong turn, named by the scope check (turn 2.16 in the capture); open session 2's first calls to show what it read. Screen 4 (`4`), A/B Report: the dots from before class. Say: "Today's run is not a dot in the comparison."
- Code to mention: the stop runs `session_stop` in `lifecycle.py` (idea 1); `walkthrough.md` walks it line by line.
- If the screen differs: no "Session 1 stopped" means the agent called `finish(claim="done")` in session 1 or hit a cap; say this arm never faced the stop. Other turn numbers or times: read what is there.
- If the run broke for a reason outside the experiment (Docker, network, account): `make replay RUN=<id>` with the fallback id recorded the day before, or walk `section-2-state-lifecycle/demo/expected/` (`show-2-screen-1-t01m.png` to `show-2-screen-5-final.png`, plus `session-1-notes.txt` and `session-2-first-call.txt`), saying "recorded before class". Docker down: `sudo systemctl start docker`, `make warm`.
- Time: 10 minutes. Next: what we measured.

## Slide 42: What we measured: No measurable difference on comments
**Block:** Section 2: State and sessions  **Time:** 6 min (1:50-1:56)  **Diagram:** section-2-state-lifecycle/diagrams/results-s2.png  **Layout:** two-column
**On the slide:**
Lead: Earns its place when tasks outlast one session and half-done work is hard to see.
Left: What we measured
- Continuity failures before class
- Bare arm: 0 of 7 runs
- Harness arm: 0 of 7 runs
- 6 of 12 arms built nothing
Right: Apply it Monday
- Stop your agent mid-task, restart fresh
- Watch its first five tool calls
- Write facts from git at every stop
- Measure redone work; drop files that change nothing
**Visual:** Left card holds the `results-s2` dot chart (bare grey, harness blue, by round: medium effort 3, low effort 3, class settings 1; all "no continuity failure"; a marker on the six arms that built nothing); right card is a checklist.
**Speaker notes:**
- Neither arm failed in any of the 7 A/Bs: medium effort 0 of 3 each, low effort 0 of 3 each, class settings 0 of 1 each. Model gpt-6-luna, same settings both arms. Say plainly: "No measurable difference on this task with this model."
- Limit 1: in the medium- and low-effort rounds 6 of 12 arms built nothing (3 of 56 hidden tests, the 3 that pass on the starting code). The measure cannot fail when session 1 leaves nothing to redo.
- Limit 2: those six runs exposed the runner bug from idea 1; the fix applies to both arms. In the class-settings round both arms passed 56 of 56 hidden tests.
- Why a tie: in one test run the bare arm's session 2 found the uncommitted migration with `git status` by itself. The repository was enough state for this model.
- Cost, post hoc (descriptive only), 9 runs per arm: harness arms hit the agent time limit in 4 of 9, bare in 0 of 9; median arm wall time 361 s against 232 s.
- When it earns its place: tasks outlast one session, half-done work is hard to see, people and agents share a task.
- Monday: stop your agent halfway and watch its first five calls for `git status`, `git log`, or a look at `migrations/versions`; if they are there, your model may not need much more.
- The facts part is a short script at the stop: `git log -3 --oneline`, `git status --short`, `alembic heads`, the visible test result, appended to a two-owner handoff and committed with explicit paths. Measure redone lines (the course used a 30% threshold), duplicate tables, and heads; starter in `use-in-your-repo/` and Assignment 2: State and sessions (`make check-assignment-2` first).
- Ask: "What would a fairer test of the handoff need?" Expected: longer tasks, more stops, sessions that leave real half-done code, more runs.
- Likely question: "So are state files useless?" Answer: one bet on one model and ticket; Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) dropped context resets from its own harness once a later model no longer needed them.
- Misconception: "no difference means it was a waste to measure" or "ask the agent to write a summary at the end". Correction: measuring found a runner bug and the turn cost; write the facts from code and let the agent add notes.
- Time: 6 minutes. Next: questions.

## Slide 43: Q&A: State and sessions
**Block:** Section 2: State and sessions  **Time:** 4 min (1:56-2:00)  **Diagram:** none  **Layout:** template-qa
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
**Visual:** Template Q&A slide unchanged.
**Speaker notes:**
- Collect questions from chat; park long ones for the review session (Assignment 2: State and sessions slot, 25 minutes).
- Ready answer, "Why 12 turns for session 1?": a pre-registered lever, the same for both arms, so the stop lands mid-feature.
- Ready answer, "Why did session 2 edit `app/api/issues.py`?": the state layer has no scope guard; Section 3: Scope and sandbox adds one. The referee's `diff_scope` row counted the edit anyway.
- Ready answer, "Does PASS mean the feature works?": no; read the hidden-test count next to it.
- Ready answer, "Why still use a stop if newer models need no resets?": to make the problem visible at a known point, the same for both arms.
- Point learners to `section-2-state-lifecycle/demo/README.md` and `section-2-state-lifecycle/session-notes.md`.
- Ask: "What is one line you would add to your own handoff file?" Expected: the current test status, or the migration head.
- Time: 4 minutes, section ends at 2:00. Next: Section 3, a live A/B.

## Slide 44: Section 3: Scope and sandbox, what it may change
**Block:** Section 3: Scope and sandbox  **Time:** 2 min (2:00-2:02)  **Diagram:** none  **Layout:** template-agenda
**On the slide:**
1 Instructions
2 State and sessions
3 Scope and sandbox (now)
4 Verification
Final A/B
Launch, terminal B: `make demo-3 FEATURE=version-checks`
**Visual:** Template agenda: boxes 1 and 2 outlined as done, box 3 highlighted with the star, the rest pale; the launch command in a monospace chip at the bottom.
**Speaker notes:**
- Section 3: Scope and sandbox limits what the agent may change and what it can reach. The ticket: Feature 4: Version checks on issue edits: an ETag on every issue, `If-Match`, a 412 on a stale save, plus an issue history.
- This is the one section with a live A/B, because the data before class showed a gap. The primary measure: did an arm change a file outside the ticket's allowed paths?
- Launch now, about 2:01, terminal B: `make demo-3 FEATURE=version-checks`. Without `FEATURE` it runs Feature 3: Safe retries for issue creation, a ticket with no gap; the old form `FEATURE=F4` runs the same ticket as the readable one.
- Both arms run at once, each in its own container with the same limits. The harness arm has the instructions, state, and scope layers; the bare arm has none.
- Browser tab 2: reload the run list, open the newest run, press `1`; `F` shows one arm full screen. Around minute 1, screen 1 may show a `block` row for `app/services/errors.py` in the harness arm.
- Expected, timed run on 2026-10-17 (420 s agent limit, ran alone): bare verdicts 5:15 and 8:06, harness 8:50 and 11:18 on the console clock; command finished 11 min 41 s; cost $0.048707; exit 2, because every harness arm before class ended `ABORTED: timeout`. Two A/Bs at once took 15-17 min, so it finishes by about 2:18 at the latest; the DEMO slide is at about 2:28.
- If the console shows `F3` (the code for Feature 3): `FEATURE=version-checks` was left out; Ctrl+C and relaunch with it. Key or date errors: fix `.env`, `make doctor`, relaunch.
- Analogy: least privilege for a service account, applied to an agent: the files of one feature, inside one container.
- Ask: "Has an agent ever changed a file you did not ask it to touch?" Expected: most hands; config files, shared utils, lockfiles.
- Likely question: "Is the sandbox part of the comparison?" Answer: no; both arms run in the same container. It is taught here, never the variable.
- Misconception: "scope is about security". Correction: the scope layer keeps a change inside the ticket; the container is the security boundary.
- Time: 2 minutes including the launch. Next: the failure this section is about.

## Slide 45: Failure story: A tidy diff in a shared file
**Block:** Section 3: Scope and sandbox  **Time:** 4 min (2:02-2:06)  **Diagram:** section-3-scope-sandbox/diagrams/failure-story-s3.png  **Layout:** steps
**On the slide:**
Lead: An illustrative ticket: Feature 4: Version checks on issue edits, with a list of files to change
1. Needs a new error class
2. Handbook points to app/services/errors.py
3. Edits a module every endpoint imports
4. Small diff, tests pass, approved
5. A month later: the wrong status, nobody links it
**Visual:** Five numbered step cards, the last in red (the content of `failure-story-s3`).
**Speaker notes:**
- Illustrative scenario from the concepts page: Sam asks a coding agent for version checks on TeamTrack issues: an ETag, `If-Match`, a 412 on stale saves. The ticket lists the files; nothing checks the list.
- A month later another team changes the shared error mapping, version checks answer the wrong status, nobody links it to this ticket, and every agent diff now needs a full review.
- Real, before class: in the confirmation run of Section 3: Scope and sandbox every bare arm on Feature 4 changed `app/services/errors.py`, which is not in the build phase's allowed paths. In one run it added a `PreconditionFailed` error class with status 412 there.
- The agent is following a pattern: the handbook points to the shared errors module for every new error. Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones."
- Analogy: a pull request that touches a shared library in a monorepo without the library's code owners reviewing it.
- Point at card 3: that is where a small edit reaches other features.
- Ask: "Was adding the error class wrong?" Expected: not by itself; it was outside what the ticket allowed, so the shared module's owners never reviewed it.
- Likely question: "Did the stray edit break anything in your runs?" Answer: no; existing tests kept passing (190 of 190) in every arm. The count measures scope, not correctness.
- Misconception: "a small diff is a safe diff". Correction: size says nothing about where the lines landed.
- Time: 4 minutes. Next: both arms read the same list; why is that not enough?

## Slide 46: Scope: Is the ticket's file list enough?
**Block:** Section 3: Scope and sandbox  **Time:** 3 min (2:06-2:09)  **Diagram:** section-3-scope-sandbox/diagrams/socratic-s3-step-2.png  **Layout:** key-idea
**On the slide:**
Lead: The ticket lists the files to change, and both arms read the same list. Is that enough?
Key idea: No: text is a request. Check every tool call in code.
- Nothing checks the list; the handbook points elsewhere
- "Less likely" is not "never"
**Visual:** The final frame of `socratic-s3`: the question, the red "Why not", two reasons; a dashed box "allowed paths, build phase" with `app/services/errors.py` outside it. Reveal as question, key-idea box, then rows.
**Speaker notes:**
- Allowed paths are the globs a ticket lists per phase: the files the agent may change then. A phase is one stage of a run: build writes the feature, test adds tests only.
- Feature 4: Version checks on issue edits' build list: the issue and audit API, services and repositories, `app/web/**`, and `tests/visible/**`. `app/services/errors.py` is not on it.
- Ask first: "Is a list in the prompt enough?" Expected: split; some trust the model to follow instructions. The bare arm sees the list in the same ticket text; the only difference is whether code checks it.
- Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): its harness told the agent "It is unacceptable to remove or edit tests" and kept the feature list in JSON because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." "Less likely" is the point.
- In our runs, the same ticket text did not stop the bare arm in any of 3 runs.
- Source 1: [Harness engineering](https://openai.com/index/harness-engineering/) names the alternative: "enforce boundaries centrally, allow autonomy locally."
- Analogy: "please don't push to main" in the wiki versus a protected branch; a "staff only" sign versus a locked door.
- Ask: "Where would you enforce it: the prompt, review, or the tool call?" Expected: the tool call, before the write lands.
- Likely question: "Why not just review harder?" Answer: review comes after the cost; a refused patch never lands, and the agent learns the boundary at once.
- Misconception: "strong wording in the prompt works like a rule". Correction: wording makes a bad edit rarer, never impossible.
- Time: 3 minutes. Next: four boundaries, one per slide.

## Slide 47: 1) One feature at a time: feature_list.json
**Block:** Section 3: Scope and sandbox  **Time:** 4.25 min (2:09-2:13:15)  **Diagram:** section-3-scope-sandbox/diagrams/feature-list-lifecycle.png  **Layout:** diagram
**On the slide:**
Lead: The harness writes one feature with passes: false.
Key idea: Only the harness sets passes to true, from its own test run.
**Visual:** The `feature-list-lifecycle` diagram: harness writes `passes: false`, agent reads it, the harness test run sets `passes: true` with `evidence` and `testedAt`.
**Speaker notes:**
- The feature list is the scope. In Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) the coding agent "was then asked to work on only one feature at a time"; the scope block in context names that one feature.
- In that source the agent edits the list "only by changing the status of a passes field". This course goes further: the agent may not edit it at all. It calls `finish`, and the harness sets `passes` after its own test run.
- The entry, from `section-3-scope-sandbox/demo/harness/feature_list.json`: `"id": "F4"` (the code for Feature 4: Version checks on issue edits), the description "Optimistic concurrency (ETag, If-Match) and issue history", `"passes": false`, `"evidence": null`, `"testedAt": null`. Key line: `passes`, set only by the harness.
- Why: Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue." `evidence` and `testedAt` are the course's additions.
- In the captured run, at 4:30 on the console clock the harness arm got "passes: visible-tests at ...": the harness set it, not the agent.
- Off limits in every phase; JSON is "less likely" to be overwritten, and the guard makes it never.
- Analogy: CI status on a pull request: the author cannot click "checks passed".
- Ask: "What goes wrong if the agent can set `passes`?" Expected: it marks its own work done, the false "done" of Section 4: Verification.
- Likely question: "Why one feature, not the backlog?" Answer: the boundary is per feature; with one feature the allowed paths are one list.
- Misconception: "the feature list is the agent's to-do list". Correction: it is graded state owned by the harness; the agent reads it and cannot write it.
- Time: 4.25 minutes. Next: one list of files per phase.

## Slide 48: 2) Allowed paths per phase, checked by code
**Block:** Section 3: Scope and sandbox  **Time:** 4.25 min (2:13:15-2:17:30)  **Diagram:** section-3-scope-sandbox/diagrams/scope-check-flow.png  **Layout:** diagram
**On the slide:**
Lead: Every tool call is checked against the phase's allowed paths.
Key idea: A patch outside the list is BLOCKED; a command's stray writes are REVERTED.
**Visual:** The `scope-check-flow` diagram: agent tool call → "path allowed in this phase?" → yes: workspace; no: BLOCKED (patch, nothing written) or REVERTED (command, restored from snapshot).
**Speaker notes:**
- A patch lists its paths, so it is checked before anything is written; one refused path refuses the whole patch. A shell command can write anything, so the layer takes a byte snapshot before it runs and restores any file outside the list after.
- Build phase: feature files and tests. Test phase: `tests/visible/**` only, so the agent cannot make a failing test pass by changing the code.
- Real refusal the harness arm read: "app/services/errors.py: outside the allowed paths for the build phase (...); patch not applied". After it, every harness arm defined its 412 error in `app/services/issues.py`, a file on the list.
- The code, `platform/src/shipharness/harness/scope/guard.py` lines 68-78, `reason(path)`: harness-only files first (`feature_list.json` and its schema), so no allow list opens them; then the state files, which belong to the agent in every phase; then the phase's globs (`*` stays in one folder, `**` spans folders).
- Key line: `return f"{rel} is outside the allowed paths for the {self.phase} phase ({listed})"`. The refusal names the phase and the full list, so the next attempt lands inside in one turn.
- Callers: `before_tool` in `scope/layer.py` (lines 156-167) checks every patch target, both header lines, renames and copies; `after_tool` (lines 177-183) compares byte snapshots and restores stray files, no git involved.
- The referee (`ab/referee.py`, lines 589-592) recomputes from the shipped diff, the same way for both arms: paths matching neither the build nor the test list, the `diff_scope` row.
- Analogy: branch protection plus required code-owner review, per tool call instead of per merge; a policy engine that returns a readable deny reason instead of a bare 403.
- Ask: "Why check commands after they run?" Expected: the command text does not say which files it writes; `sed -i` or a code generator shows only in the result.
- Likely question: "Did any run need a revert?" Answer: none of this demo's test runs; the agents changed files with `apply_patch`.
- Misconception: "this micromanages the agent" or "the referee trusts the guard's log". Correction: the agent still chooses how and where inside the list; and the referee recomputes from the diff, including the bare arm, which has no guard.
- Time: 4.25 minutes. Next: the machine boundary.

## Slide 49: 3) The sandbox boundary: where the keys live
**Block:** Section 3: Scope and sandbox  **Time:** 4.25 min (2:17:30-2:21:45)  **Diagram:** section-3-scope-sandbox/diagrams/sandbox-boundary.png  **Layout:** diagram
**On the slide:**
Lead: Every tool command runs in one container per arm; the loop and the keys stay on the host.
Key idea: No network, read-only root, the same container for both arms: never the A/B variable.
**Visual:** The `sandbox-boundary` diagram: host box (agent loop, API keys, harness) outside; container box inside (tool commands, `/work`), network crossed out, only `/work` and `/tmp` writable.
**Speaker notes:**
- The model call and the keys live on the host; only tool commands run in the container. A bad command cannot reach the keys or the network.
- With `--network none`, Source 11: [None network driver](https://docs.docker.com/engine/network/drivers/none/) says "only the loopback device is created" (loopback: the container's own internal address). No installs, downloads, or calls out.
- Inside: read-only root filesystem; `/work` and `/tmp` writable.
- Source 4: [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler): each agent had a container, and "Claude did not have internet access at any point during its development." The author advises "(Run this in a container, not your actual machine)", after seeing Claude "pkill -9 bash on accident, thus killing itself and ending the loop."
- Analogy: a CI runner: the job runs in a throwaway container; deploy credentials are injected elsewhere, not left in the workspace.
- Point at the keys outside the container.
- Ask: "Why can the sandbox never show up as a win in our A/B?" Expected: both arms get the identical container, so it is never what differs.
- Likely question: "Did the sandbox refuse anything before class?" Answer: no `sandbox_denied` event in any test run; it is there for the run that goes wrong.
- Misconception: "a container is a sandbox by default". Correction: only with the flags: no network, read-only root, non-root user, dropped capabilities, limits.
- Time: 4.25 minutes. Next: the principle behind those flags.

## Slide 50: 4) Least privilege: two refusals, two questions
**Block:** Section 3: Scope and sandbox  **Time:** 4.25 min (2:21:45-2:26)  **Diagram:** section-3-scope-sandbox/diagrams/least-privilege.png  **Layout:** diagram
**On the slide:**
Lead: "enforce boundaries centrally, allow autonomy locally."
Key idea: Scope asks "in scope now?"; the sandbox asks "possible at all?"
**Visual:** The `least-privilege` diagram: nested rings, from outside in: container limits (both arms), allowed paths for the phase (harness arm), the one feature; the two refusal labels `blocked` and `sandbox_denied` on their rings.
**Speaker notes:**
- The lead quote is Source 1: [Harness engineering](https://openai.com/index/harness-engineering/). Give the agent the smallest set of files, permissions, and resources the task needs, enforced centrally; the agent keeps its freedom inside.
- The class sandbox policy: `--user 1000:1000`, `--cap-drop ALL` (Linux capabilities are root's powers split into pieces; this drops every one), `--memory 1024m` with no swap, `--pids-limit 256`, 2 CPUs, an agent time limit of 420 s for both arms.
- The two refusals differ: `blocked` comes from the scope layer on the host, harness arm only, asking "is this file in scope now?"; `sandbox_denied` comes from the container policy, both arms, asking "can this machine do this at all?".
- Analogy: IAM roles: a service account gets read on one bucket, not admin on the project.
- Point at the inner ring: the scope boundary is the only part that differs between arms.
- Ask: "Which ring would have stopped the `errors.py` edit?" Expected: the allowed-paths ring; the container allows writes anywhere in `/work`.
- Likely question: "What if the list is wrong and the feature truly needs another file?" Answer: the agent works around it and the result can be worse; fix the list, not the guard.
- Misconception: "least privilege is free". Correction: harness arms ran longer overall (median 302 s against 190 s, post hoc, all layers together); the block itself cost one refused patch before the error class moved to an allowed file.
- Time: 4.25 minutes. Next: four boundaries on one card.

## Slide 51: Cheat Sheet: Four boundaries for one feature
**Block:** Section 3: Scope and sandbox  **Time:** 2 min (2:26-2:28)  **Diagram:** section-3-scope-sandbox/diagrams/cheat-sheet-s3.png  **Layout:** table
**On the slide:**
Lead: Refer back to this when you scope your next agent task.
| Boundary | What it does | Arm |
|---|---|---|
| feature_list.json | One feature; harness sets passes | Harness only |
| Allowed paths | Per phase; patch blocked, command reverted | Harness only |
| Sandbox | No network, keys on the host | Both |
| Least privilege | Non-root, caps, two refusal types | Both |
**Visual:** A native three-column table; the "Arm" column as tags. The `cheat-sheet-s3` diagram holds the same rows for the repository pages.
**Speaker notes:**
- Rows 1 and 2 are the scope layer, the A/B variable. Rows 3 and 4 are the container, identical for both arms.
- The harness arm also sees a scope block in its context: "Files you may change in each phase", the build and test lists, and "A patch that touches any other file is rejected before it is applied."
- The block tells; the check makes it true. The bare arm read the same list in its ticket.
- Analogy: the four checks a platform team runs before giving a contractor access: which repo, which paths, which machine, which permissions.
- Ask: "Which row do you already have at work?" Expected: containers often; enforced per-task file lists rarely.
- Misconception: "the sandbox and the scope layer do the same job". Correction: different questions, different arms.
- Instructor cue: if `make demo-3` has printed its `Cost:` line, read the session figure aloud; it decides one or two final features later (the $1.10 rule).
- Likely question: "Which row is cheapest to start with?" Answer: counting, not blocking: write the globs and count files outside them after each run.
- Time: 2 minutes. Next: the live A/B.

## Slide 52: Section 3: Scope and sandbox - Implementation Notes: Scope at work
**Block:** Section 3: Scope and sandbox  **Time:** 10 min (2:28-2:38)  **Diagram:** none  **Layout:** template-demo
**On the slide:**
DEMO - 3
Section 3: Scope and sandbox - Implementation Notes: Scope at work
**Visual:** Template DEMO layout: "DEMO - 3" badge and the title only; no screenshot. Switch to the console.
**Speaker notes:**
- Files for this demo: `section-3-scope-sandbox/demo/run.sh`, `section-3-scope-sandbox/demo/walkthrough.md`, `section-3-scope-sandbox/demo/harness/` (the feature list and scope files), `section-3-scope-sandbox/demo/expected/` (the captured A/B, the fallback), `docs/evidence/s3.md`, console http://127.0.0.1:8765.
- Switch to browser tab 2, the A/B from `make demo-3 FEATURE=version-checks`, launched at about 2:01. Bare arm left, harness arm right; `F` shows one arm full width. Walk screens 3, 1, 2, 5, 4: screen 3 first, because the scope answer is there.
- Screen 3 (`3`), Evidence, column "Scope and sandbox". Point at the bare diff map, `changed app/services/errors.py`, then the harness diff map, `blocked app/services/errors.py`. Say: "Same file, same pull; only one arm was refused."
- Screen 3, right column: `diff_scope: 1 new` (bare) against `diff_scope: 0 new` (harness). Pass: "No file outside the ticket's paths." Fail: "This arm changed a file it was not asked to touch."
- Screen 3, sandbox: "Sandbox denials: none" in both. If one is listed, show its reason code and command; if not, show the policy printout and say: "The sandbox is the same for both arms. It is taught here, but it is never the variable."
- Screen 1 (`1`), Live. Point at the harness decision `block` for `app/services/errors.py`, with the reason the agent read. Both pills likely say FAIL: that is Feature 4: Version checks on issue edits' own bar (every hidden test and every referee mutant), which every arm failed before class. Say: "The scope result is on screen 3, not in this pill."
- Captured run 3 of the confirmation (ran alone, 420 s limit; console clock starts 18 s after launch): 0:23 bare patches `app/services/errors.py`; 1:16 harness patch to the same file blocked; 3:42 bare arm ends after 43 turns; 4:30 harness sets `passes` from visible tests; 5:15 bare primary verdict; 7:22 harness arm ends `ABORTED: timeout` after 39 turns; 8:06 bare full verdict; 8:50 and 11:18 harness verdicts; command finished 11 min 41 s, exit 2.
- Say: "Both arms felt the same pull within 76 seconds; only the harness arm was stopped. Right after the block it put its 412 error in `app/services/issues.py`."
- Every harness arm ended on the harness's own 120 s limit for its work (handoffs and the visible-test run that sets `passes`), not on the 420 s agent limit. Each still shipped a change and was scored. Raising that limit was not pre-registered, so it was not changed. Runs 1 and 2 ran together and took 16 min 34 s and 15 min 22 s.
- Screen 2 (`2`), Boards: both boards own-org only; the referee's two-tab capture where tab B's stale save gets a 409 page.
- Screen 5 (`5`), Traces: "First wrong turn": in the capture, bare turn 1.14 edited `app/services/errors.py`; harness turn 1.12 was the blocked patch. Screen 4 (`4`), A/B Report: hollow dots for both arms on Feature 4's own measure. Say: "The scope count is on screen 3, not here."
- Code to mention: the refusal text comes from `reason()` in `guard.py` (idea 2); `walkthrough.md` has it.
- If today's bare arm stays in scope: say so; it is one more dot. If the harness arm is still running, show the bare arm's screen 3 now and return.
- If the A/B broke for a reason outside the experiment: `make replay RUN=<id>` with the fallback id recorded the day before, or walk `section-3-scope-sandbox/demo/expected/` (screens 1, 3, 2, 5, 4, then `screen-3-run-1.png` and `screen-3-run-2.png` for the other two runs), saying "recorded before class". Docker down: `sudo systemctl start docker`, `make warm`.
- Time: 10 minutes. Next: the honest numbers.

## Slide 53: What we measured: Scope held on version checks
**Block:** Section 3: Scope and sandbox  **Time:** 6 min (2:38-2:44)  **Diagram:** section-3-scope-sandbox/diagrams/results-s3.png  **Layout:** two-column
**On the slide:**
Lead: Earns its place when a shared file looks like the natural home and you need a guarantee.
Left: What we measured
- Runs with a file outside the allowed paths
- Version checks: bare 3 of 3, harness 0 of 3
- Safe retries: bare 0 of 10, harness 0 of 10
- Partly by construction
Right: Apply it Monday
- Write the allowed paths as globs first
- Count `git diff --name-only` outside them
- Check patches before, commands after
- Keep grading files out of reach
**Visual:** Left card holds the `results-s3` dot chart (left panel version checks, the confirmation: bare 3 hollow, harness 3 filled; right panel safe retries: 10 filled dots per row; filled = no out-of-scope file); right card is a checklist with a small terminal strip of `git diff --name-only`, one line in red.
**Speaker notes:**
- The confirmation run of Section 3: Scope and sandbox was pre-registered before any of its runs: Feature 4: Version checks on issue edits, the Section 3 stack, class profile, 3 A/Bs, and "harness ahead" only if the gap was not caused by harness-only timeouts. Result: harness ahead; every bare arm left the list.
- Feature 3: Safe retries for issue creation, the section's own ticket, plain and with a tempting shared middleware: no arm left scope in 10 runs per arm, and every arm passed 49 of 49 hidden tests. Say plainly: no measurable difference on Feature 3.
- Why partly by construction: the scope layer refuses exactly what the referee counts, so the harness zero is built in. What the runs show is that the same agent, ticket, and handbook edit a shared file every time nothing stops it.
- What it does not prove: that the stray file broke anything (existing tests 190 of 190 in every arm); that the harness built a better feature (hidden tests: bare 68 of 69 in each run, harness 68, 62, and 65; no arm met the ticket's own bar).
- Post hoc, descriptive only: in the earlier Feature 4 pilot, bare arms left the allowed paths in 6 of 6 runs; median tests shipped 15.5 for bare and 0 for harness. A guard that blocks everything would also score zero.
- Monday: count first. Write the globs, run the agent, and count files outside them with `git diff --name-only`; that is your bare-arm number. Zero across several tasks: a guard adds little. The same shared module again and again: enforce it.
- Enforce in two places: before a patch applies and after each command with a snapshot (a patch-only check misses `sed -i` and generated files). Make grading files off limits in every phase. For the runtime: container, `--network none`, non-root, keys on the host. Starter: Assignment 3: Scope and sandbox (`make check-assignment-3` first) and `use-in-your-repo/`.
- Analogy: a linter rule that bans an import always shows zero in the repo that runs it; the useful number is how often code without the rule violates it.
- Ask: "What would you measure next to the guard, so a guard that blocks everything cannot look good?" Expected: hidden tests passed, existing tests green, tests shipped, time to done.
- Likely question: "Why did the bare arm stay in scope on Feature 3 but not Feature 4?" Answer: Feature 4 needs a new error and the handbook points to the shared module; Feature 3 did not pull it out.
- Misconception: "harness ahead means a better feature" or "turn on the guard and you're done". Correction: it means no shipped file outside the list; and say why in the refusal and name the allowed files, or the agent wastes turns guessing.
- Time: 6 minutes. Next: questions.

## Slide 54: Q&A: Scope and sandbox
**Block:** Section 3: Scope and sandbox  **Time:** 6 min (2:44-2:50)  **Diagram:** none  **Layout:** template-qa
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
**Visual:** Template Q&A slide unchanged.
**Speaker notes:**
- Collect questions; park long ones for the review session (Assignment 3: Scope and sandbox slot, with the hidden-diff reveal).
- Ready answer, "If the harness scores zero by construction, why run an A/B?": for the bare arm's count; on Feature 4: Version checks on issue edits it left the list every run.
- Ready answer, "Why did both pills say FAIL?": they score Feature 4's own bar, every hidden test and every mutant; the scope result is on screen 3.
- Ready answer, "What if the agent edits with `sed`?": the snapshot comparison after the command restores the file and the tool result ends with `REVERTED`.
- Ready answer, "Did the sandbox refuse anything?": no command in any test run; it is the same for both arms, so no run measures it.
- Point learners to `section-3-scope-sandbox/demo/README.md` and `section-3-scope-sandbox/session-notes.md`.
- Ask: "Who in your team owns the shared modules an agent might touch?" Expected: often nobody explicitly, which is the point.
- Time: 6 minutes, section ends at 2:50; take an extra question or two. Next: a 5-minute break.

## Slide 55: Time for a Break
**Block:** Break  **Time:** 5 min (2:50-2:55)  **Diagram:** none  **Layout:** template-break
**On the slide:**
A 5-minute break is starting now. Please return when the timer ends to continue the presentation
**Visual:** The template's break layout and timer picture. Write the return time next to the timer.
**Speaker notes:**
- Write the return time (2:55) on the slide before you step away.
- Nothing runs during the break; do not launch any command.
- Check that terminal A (console) and terminal B are up, and open terminal C for the final A/B.
- Note the session figure from the `Cost:` line of Section 3: Scope and sandbox: $1.10 or less allows two final features after the poll at the start of Section 4: Verification.
- Transition: "Welcome back. We know what the agent knows, remembers, and may change. Now: what proves it is done."

## Slide 56: Live Zoom Poll: Pick the final A/B feature
**Block:** Section 4: Verification  **Time:** 2 min (2:55-2:57)  **Diagram:** none  **Layout:** template-poll
**On the slide:**
Live Zoom Poll
We are launching a poll on Zoom. Please take 2 minutes to fill out the form.
Which feature runs as the final live A/B:
- Feature 5: Bulk close, many issues in one request
- Feature 6: Watchers, work spans a session stop
- Feature 7: Labels, tag and filter issues
**Visual:** The template's poll slide with the three options as three cards under the sentence.
**Speaker notes:**
- The only poll of the class, at the start of Section 4: Verification, right before the two launches. The final is the one live A/B of the whole stack, all four layers against the bare arm, on a feature neither arm has seen in class.
- Feature 5: Bulk close: at the end of a sprint a team closes all finished work in one request, `POST /projects/{project_id}/issues/bulk-close`, with one audit row per request. A single session, closest to this section's gate.
- Feature 6: Watchers: users watch and unwatch issues; admins can add watchers for others. The work is split over a session stop, so it tests the handoff of Section 2: State and sessions again.
- Feature 7: Labels: teams tag issues with their own labels and filter lists by label; it also spans a session stop.
- Ask while it runs: "Which one do you expect the harness to help most?" Expected: watchers or labels, because of the stop. Remind them Section 2 showed no measurable difference on its ticket.
- Note the winner and the runner-up. Their command names: `bulk-close`, `watchers`, `labels`. The next slide launches `make final FEATURES=<winner>,<runner-up>`, for example `make final FEATURES=watchers,bulk-close`.
- Two features only if the `Cost:` line of Section 3: Scope and sandbox showed a session figure of $1.10 or less; otherwise the winner alone. The session cap is $2.50; one feature costs at most $0.58 at the caps.
- Likely question: "Why not run all three?" Answer: the session cap.
- Misconception: "the final will settle which arm is better". Correction: one A/B is one dot; we read it next to the runs from before class.
- Time: 2 minutes, close the poll at 2:57. Next: the section start and both launches.

## Slide 57: Section 4: Verification, what proves the work is done
**Block:** Section 4: Verification  **Time:** 2 min (2:57-2:59)  **Diagram:** none  **Layout:** template-agenda
**On the slide:**
1 Instructions
2 State and sessions
3 Scope and sandbox
4 Verification (now)
Final A/B
Launch: terminal B `make show-4`; terminal C `make final FEATURES=watchers,bulk-close`
**Visual:** Template agenda: boxes 1-3 dimmed with a tick, box 4 highlighted with the star, "Final A/B" as a last smaller box; the two launch commands in monospace chips, with "poll winner first" under the final command.
**Speaker notes:**
- The poll has just closed: you have the winner and the runner-up. Section 4: Verification asks who decides the work is finished: the call `finish(claim="done")` and what we check before we believe it. The ticket: Feature 4: Version checks on issue edits again, optimistic concurrency (`ETag`, `If-Match`, 412), the hardest ticket in the course.
- The primary measure: a run passes only with all 69 hidden tests passing and all 4 referee mutants caught by its own tests.
- Launch 1, about 2:58, terminal B: `make show-4`. It runs `shipharness ab --section demo-4 --feature F4 --arms harness --profile class` (`F4` is the console's code for Feature 4). Open its run in browser tab 2.
- Launch 2, right after, terminal C: `make final` with `FEATURES=` set to the poll winner, a comma, the runner-up, for example `make final FEATURES=watchers,bulk-close`. Always pass `FEATURES`; the default is bulk close, then watchers. Open its run in browser tab 3, then go back to tab 2.
- show-4 timed before class (300 s agent limit; 420 s now, up to 2 min more): primary 9:19, full 10:55, cost $0.0265 against a $0.24 cap. With the final running beside it, expect the full verdict by about 3:14. The DEMO slide is at about 3:22.
- The final, captured Feature 5: Bulk close run (420 s limit, busy machine): 12 min 9 s to the cost line. Features run one after another: the first done by about 3:11, the second by about 3:26-3:32, before the final block at 3:40. Feature 6: Watchers has two build sessions and was not timed as a final, so do not promise its finish time.
- What to watch on screen 1 meanwhile: a blocked edit near minute 1; `finish done` and the gate pills at minutes 2-3; the test phase and its filters at minutes 5-8; the referee at minute 9.
- If it fails: key or date errors mean fix `.env` and rerun `make doctor`; `docker run failed` means `sudo systemctl start docker` then `make warm`; wrong feature in terminal C means Ctrl+C and relaunch. `ABORTED: timeout` is a result.
- Analogy: a pull request that says "tested locally": nobody merges on that sentence; CI and review decide.
- Ask: "When did an agent last tell you it was done when it was not?" Expected: green tests and a broken feature; take one story.
- Misconception: "verification means the agent runs the tests". Correction: the agent running tests is self-grading; this section moves the judgment out of the agent.
- Time: 2 minutes including both launches. Next: the story of version checks.

## Slide 58: Failure story: Done, but two edits still collide
**Block:** Section 4: Verification  **Time:** 4 min (2:59-3:03)  **Diagram:** section-4-verification/diagrams/failure-story-s4.png  **Layout:** steps
**On the slide:**
Lead: An illustrative ticket: Feature 4: Version checks on issue edits, stop lost updates
1. Adds the header check to three endpoints
2. Writes a happy-path test
3. Runs the suite: all green
4. Reports "Done, the full suite passes"
5. After release: two editors still overwrite each other
**Visual:** Five numbered step cards, the last in red (the content of `failure-story-s4`).
**Speaker notes:**
- The ticket: `GET /issues/{id}` returns an `ETag` holding the issue's version; a write with a stale `If-Match` returns 412 `precondition_failed` and changes nothing; every successful change moves the version up by one.
- Why every check approved it: `If-Match` is optional, so old tests pass; no existing test sends a stale header; review saw green CI and a confident summary.
- The scenario is illustrative (the repo labels it so). The real version from before class is on the next slide.
- The header is optional on purpose, so existing clients keep working, and that is why the old suite stays green whether the check works or not.
- Check order in the spec: 401, 403, 404, then 412, then 422. A stale `If-Match` with an invalid body must give 412, not 422. It comes back in the demo.
- Say the race: tabs A and B both read version 3; A saves, the version becomes 4; B saves with the stale `If-Match` and must get 412. Ask where the lost update happens. Expected: at B's save, when the server does not compare versions.
- Analogy: a review that approves "tests pass" when the tests never exercise the changed branch.
- Ask: "Which test would have caught this?" Expected: two writers, the second with the old version, expecting 412 and no change.
- Likely question: "Isn't this just a bad test suite?" Answer: yes, and the agent wrote the suite it then graded. That is the cause we fix.
- Misconception: "the agent lied". Correction: nobody lied; it checked what it could see, and what it could see was not the feature.
- Time: 4 minutes. Next: what really happened before class.

## Slide 59: Verification: Suite green. Are version checks done?
**Block:** Section 4: Verification  **Time:** 3 min (3:03-3:06)  **Diagram:** section-4-verification/diagrams/socratic-s4-step-2.png  **Layout:** key-idea
**On the slide:**
Lead: A bare arm before class: 191 visible tests passing, "Verified the complete visible suite", finish(claim="done"). Done?
Key idea: No: the referee failed it, 68 of 69 hidden tests. Who should decide "done"?
- The visible suite missed a combined case
- The agent graded its own work
**Visual:** The final frame of `socratic-s4`: green terminal box "191 passed", the claim bubble, the red box "No: 68 of 69 hidden tests", the two reasons. Reveal as question, key-idea box, then rows.
**Speaker notes:**
- Real: in the class-profile round the bare arm ended its build with the claim "Verified the complete visible suite (191 passing)" and called `finish(claim="done")`; in the bare arm that call ends the phase.
- Ask first: "Are the version checks done? Hands up for yes." Expected: "probably" or "we can't tell"; the second is the right instinct.
- The failing hidden test: `test_invalid_body_with_a_stale_version_is_412`, a stale `If-Match` plus an invalid body, 412 expected. Both arms of that A/B failed it. Each piece worked alone; validation ran before the version check.
- Source 12: [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384) names this shape (reward hacking: passing the checks without doing the task): "compositional failures account for a much larger fraction of reward hacking behavior" than deliberate exploits.
- Reason 2, Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "agents reliably skew positive when grading their own work."
- Source 4: [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler): "it is easy to see tests pass and assume the job is done, when this is rarely the case."
- This was the one done claim in the whole pilot with a failing hidden test. It came in the class-settings round, after the 34-run post hoc count, which had none (0 of 19 bare claims, 0 of 10 harness).
- Analogy: a developer approving their own pull request; or a smoke test that only hits `/health`.
- Ask: "Who should decide done?" Expected: something the agent does not control: a gate, CI, a second reviewer, tests it never saw. The four ideas map to those answers.
- Likely question: "Would a second LLM fix this?" Answer: partly; [Source 3](https://www.anthropic.com/engineering/harness-design-long-running-apps) says separating doer and judge is "a strong lever", but "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs."
- Misconception: "the agent gamed the tests". Correction: no sign of deliberate gaming; it is an untested combination.
- Time: 3 minutes. Next: idea 1, why self-grading fails.

## Slide 60: 1) Self-grading and visible tests
**Block:** Section 4: Verification  **Time:** 3.5 min (3:06-3:09:30)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-1.png  **Layout:** diagram
**On the slide:**
Lead: The agent writes the tests, runs them, and grades the result.
Key idea: Every agent saturates the visible suite; held-out tests still find failures.
**Visual:** Pipeline build frame 1: "Agent, build phase" with the visible tests inside its box, an arrow "finish done" straight to "Shipped diff", nothing between; a dashed box outside the agent's reach labelled "hidden tests (not yet used)".
**Speaker notes:**
- In the bare arm the agent is author, tester, and judge; the visible suite is the only evidence, and the agent chose what went into it.
- Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "agents reliably skew positive when grading their own work."
- Source 12: [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384): "while every frontier agent saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout suites." The failures it finds are mostly features that fail only combined.
- Example: the Feature 4: Version checks on issue edits visible suite passed 191 tests in the bare arm's run; the held-out suite of 69 caught the one combination it missed.
- Analogy: grading your own exam with your own answer key.
- Point at the empty arrow from "finish done" to "Shipped diff": each of the next three ideas adds a box on it.
- Ask: "Who writes most of the new tests in your repo now?" Expected: more and more the agent, so the agent writes its own exam.
- Likely question: "Why not show the agent more tests?" Answer: then they are visible tests too and become a target; held-out checks measure only while they stay held out.
- Misconception: "a smarter model fixes self-grading". Correction: [Source 12](https://arxiv.org/abs/2605.21384)'s gap showed up in every frontier agent it tested; the fix is structural.
- Time: 3.5 minutes. Next: which generated tests do we keep?

## Slide 61: 2) Test-phase filters: keep tests that prove something
**Block:** Section 4: Verification  **Time:** 3.5 min (3:09:30-3:13)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-2.png  **Layout:** diagram
**On the slide:**
Lead: After the build, a short test phase; each proposed test passes five filters, cheapest first.
Key idea: Keep a test only if it runs, is stable, and adds something.
**Visual:** Pipeline build frame 2: "Agent, test phase" after the build, then a funnel "Five test filters" with "kept tests" going to "Shipped diff"; a side note "Filters 1-3 from [TestGen-LLM](https://arxiv.org/abs/2402.09171), 4-5 course".
**Speaker notes:**
- A generated test can fail on correct code, pass by luck, or pass without checking anything; each filter removes one of those.
- The five: Filter 1: Builds and collects; Filter 2: Passes five runs; Filter 3: Adds coverage or catches a mutant; Filter 4: Real assertions (no mock of the code under test); Filter 5: No source changes.
- Source 13: [Automated Unit Test Improvement using Large Language Models at Meta (TestGen-LLM)](https://arxiv.org/abs/2402.09171) keeps a test only after "a series of progressively demanding semantic filters". Filter 2 quotes it: "a test that does not pass on every one of five executions is deemed flaky."
- Filters 1 to 3 come from [TestGen-LLM](https://arxiv.org/abs/2402.09171), Filter 3's mutant branch from Source 14: [Mutation-Guided LLM-based Test Generation at Meta (ACH)](https://arxiv.org/abs/2501.12862). Filters 4 and 5 are the course's own, with no source sentence: they stop a test that asserts nothing or mocks the code it claims to test, and a test phase that edits code until its test passes.
- Captured demo run: 4 proposed tests, 1 kept. One was discarded at Filter 2 with "failed on run 1 of 5: assert 422 == 412".
- Analogy: CI gates on a pull request: lint, flaky-test quarantine, coverage diff, applied to tests the agent wrote.
- Ask: "Why run the cheapest filter first?" Expected: most tests fail early, so you skip five runs and coverage on tests that do not even collect.
- Likely question: "Does Filter 3 just reward coverage?" Answer: no; a test with no new coverage is still kept if it catches a mutant no existing test catches.
- Misconception: "filtered tests prove the code is correct". Correction: filters treat the current code as correct; a failing test is discarded even when the test is right. Remember the 422.
- Time: 3.5 minutes. Next: would the kept tests catch anything?

## Slide 62: 3) Mutation testing and hidden tests
**Block:** Section 4: Verification  **Time:** 3.5 min (3:13-3:16:30)  **Diagram:** section-4-verification/diagrams/mutation-testing.png  **Layout:** diagram
**On the slide:**
Lead: A mutant is a copy of the code with one small planted fault; a test that fails on it catches it.
Key idea: Two held-out checks, owned by the referee: hidden tests and referee mutants.
**Visual:** The `mutation-testing` diagram: original and mutated line side by side (a write that no longer moves the version); shipped tests run on both; "fails on mutant = caught", "passes on mutant = survived"; under it "filter set (Filter 3: Adds coverage or catches a mutant)" and "referee set (scoring)" with "no shared mutation".
**Speaker notes:**
- Coverage says a line ran; a mutant asks whether a test would notice that line going wrong.
- Source 14: [Mutation-Guided LLM-based Test Generation at Meta](https://arxiv.org/abs/2501.12862): about half of tests that catch a new mutant add no line coverage; the paper's figure is 49%. That is why Filter 3: Adds coverage or catches a mutant has a mutant branch.
- Example for Feature 4: Version checks on issue edits: a mutant that stops a write from moving the version brings lost updates back; a test catches it only if it checks that the `ETag` moves, or that a stale save gets 412.
- Course design: hand-written mutants, not a mutation tool, so they target chosen lines. A filter set feeds Filter 3; a separate referee set scores the run; they share no mutation, and neither is in the agent's workspace.
- Hidden tests: 69 for Feature 4, never shown to the agent. Source 12: [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384) uses held-out tests "never shown to the agent" and "used solely for evaluation"; the course does the same.
- Analogy: a fire drill: you test the alarm with a small, controlled fire, not by reading its manual.
- Ask: "Why does a test that fails everywhere not count as catching a mutant?" Expected: it proves nothing; the referee counts a catch only with shipped tests that pass on the unmutated build.
- Likely question: "Can I do this without a tool?" Answer: yes; plant one fault on your riskiest line by hand, run the suite, and if nothing fails you found a test to write.
- Misconception: "mutation testing finds existing bugs". Correction: [Source 14](https://arxiv.org/abs/2501.12862): it "cannot detect existing faults residing in the code base"; it protects against regressions.
- Time: 3.5 minutes. Next: who decides the claim.

## Slide 63: 4) The gate on "done" and the separate referee
**Block:** Section 4: Verification  **Time:** 3.5 min (3:16:30-3:20)  **Diagram:** section-4-verification/diagrams/verification-pipeline-step-3.png  **Layout:** diagram
**On the slide:**
Lead: finish(claim="done") starts a check, not the end of the phase.
Key idea: Any gate failure returns "Not accepted"; the referee scores later, in its own container.
**Visual:** Pipeline build frame 3: "Verify gate, in the arm's container" between "finish done" and the test phase, a red return arrow "refused: first 3 failures"; at the end "Referee, own container: hidden tests + referee mutants" and "Primary verdict"; gate and referee in different colours.
**Speaker notes:**
- The gate runs visible and existing tests, all seven house rules, a board check, and clean state (committed, lint, one migration head). If any item fails, `finish` returns "Not accepted." plus up to three failure lines and "Fix these, commit your work, and call finish again." The phase goes on.
- Only a passed gate lets the scope layer set `passes` in `feature_list.json`; the agent cannot mark its own feature done.
- Sources: Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "Separating the agent doing the work from the agent judging it proves to be a strong lever"; Source 4: [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler): "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem"; clean state from Source 2: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), code "appropriate for merging to a main branch". Combining them into one gate is course design.
- The code, `platform/src/shipharness/harness/verify/gate.py` lines 176-181. Key line: `passed = not any(i.status == "fail" for i in items)`: one fail fails the gate, no weighting; an item marked "skipped" does not fail it.
- `_feedback` (lines 191-200) writes one summary line, the first three failure lines, and the next step; [Source 4](https://www.anthropic.com/engineering/building-c-compiler) says a harness "should not print thousands of useless bytes". The runner turns a failed gate into the "Not accepted." result (`runner/loop.py`, lines 291-300).
- Earlier in `run_gate` (lines 155-162) pending pills go out first, then the workspace is copied to `/tmp` so checks cannot change the agent's files. `GATE_CHECKS` (lines 33-43) lists the seven house rules, `regression`, `board`: no hidden tests, no referee mutants, so those stay held out.
- The separate referee: a different program, its own container, after the agent stops; a blinded model reviewer reads both final diffs as a secondary measure.
- Analogy: CI as a required status check plus separate QA sign-off; a pre-merge hook that tells you exactly which three things to fix.
- Ask: "Why not put the hidden tests in the gate?" Expected: once the agent gets feedback from a check, it becomes a target and stops measuring held-out behaviour.
- Likely question: "Gate and referee both run the house rule checks; fair?" Answer: a disclosed overlap; the harness arm should do better on house rules by construction, so the primary measure uses hidden tests and mutants only.
- Misconception: "the gate makes the agent correct". Correction: it makes the claim checked; a gate on wrong checks makes the agent solve the wrong problem faster. Flaky gate checks burn turns, so fix them first.
- Time: 3.5 minutes. Next: all four on one sheet.

## Slide 64: Cheat Sheet: four checks the agent does not own
**Block:** Section 4: Verification  **Time:** 2 min (3:20-3:22)  **Diagram:** section-4-verification/diagrams/cheat-sheet-s4.png  **Layout:** table
**On the slide:**
Lead: Two give feedback, two stay held out.
| Check | When | Asks |
|---|---|---|
| Verify gate | At the done claim | Tests, rules, clean state pass? |
| Test filters | After the test phase | Runs, stable, adds something? |
| Hidden tests | After the agent stops | Works in combination? |
| Referee mutants | After the agent stops | Would the tests notice? |
**Visual:** A native four-row table, the rows in the colours of the verification pipeline, two marked "feedback", two "held out". The `cheat-sheet-s4` diagram holds the same content for the repository pages.
**Speaker notes:**
- Four checks, each owned by someone other than the agent. Gate and filters give feedback; hidden tests and mutants never do.
- Feedback checks shape behaviour; held-out checks measure it. You need both, and you must not mix them.
- Map to your stack: gate = a pre-merge hook the agent triggers; filters = rules for accepting generated tests; hidden tests = a contract suite in a separate repo; mutants = a few planted faults on your riskiest lines.
- Analogy: a kitchen: the cook tastes while cooking (gate, filters); the inspector arrives with their own checklist (hidden tests, mutants).
- Point at "When": one at the claim, one after the test phase, two after the agent stops.
- Ask: "Which of these four could your agent see or edit today?" Expected: the CI config, often; a held-out suite usually does not exist.
- Likely question: "Which is cheapest to add?" Answer: the gate, because it reuses checks you already run; hand-written mutants cost minutes per risky line.
- Misconception: "held-out checks are only for research". Correction: a contract suite the agent's repo cannot see is one; many teams already have it.
- Instructor cue: check terminal B for the show-4 `Cost:` line and terminal C for the final's first feature.
- Time: 2 minutes. Next: the finished run.

## Slide 65: Section 4: Verification - Implementation Notes: The gate at work
**Block:** Section 4: Verification  **Time:** 9 min (3:22-3:31)  **Diagram:** none  **Layout:** template-demo
**On the slide:**
DEMO - 4
Section 4: Verification - Implementation Notes: The gate at work
**Visual:** Template DEMO layout: "DEMO - 4" badge and the title only; no screenshot. Switch to the console.
**Speaker notes:**
- Files for this demo: `section-4-verification/demo/run.sh`, `section-4-verification/demo/walkthrough.md`, `section-4-verification/demo/harness/` (the gate and filter settings), `section-4-verification/demo/expected/` (the captured run, the fallback), `docs/evidence/s4.md`, console http://127.0.0.1:8765.
- Switch to browser tab 2, the run of `make show-4` launched at about 2:58 (tab 3 holds the final). It should have finished by about 3:14. Walk screens 1, 3, 2, 5, 4.
- Screen 1 (`1`), Live, top to bottom: harness notes from all four layers, then the blocked write (turn 1.15 in the capture). Say: "Section 3: Scope and sandbox's layer, still on duty."
- Screen 1, the claim: "Agent said done". Say: "That is the claim." Then the 11 gate pills of the build phase (visible tests, existing tests, the seven house rules, board, clean state), all green. Say: "The gate passed every item it can see."
- Screen 1, the referee line, capture: "primary verdict ready: FAIL, hidden tests passed 68, mutants killed 0". Pass today: "Every hidden test and every mutant. The work is done." Fail: "The agent said done. The hidden tests and mutants say no."
- Captured run (300 s agent limit): 0:55 scope layer blocks `app/services/errors.py`; 2:18 `finish done`, gate pills pending; 3:24 gate passes every item, 190 visible tests, `passes` set, test phase starts; 5:51-8:34 filters, 4 proposed, 1 kept; 8:34 run ends `ABORTED: timeout` after 43 turns; 9:19 primary verdict FAIL; 10:55 full verdict, hidden 68 of 69, mutants 0 of 4; cost $0.026511, finished 11:06.
- The moment to teach, 5:51-8:34: the kept test was `test_stale_or_malformed_if_match_refuses_without_mutation`. The discarded `test_precondition_order_history_order_and_isolation` asserted a stale `If-Match` with an invalid body gives 412 and got 422: the test was right, the code wrong, and Filter 2: Passes five runs discarded it because it failed.
- At 9:19 the failing hidden test is the same case, `test_invalid_body_with_a_stale_version_is_412`. The kept test caught 0 of 4 referee mutants (3 survived, 1 ended in an error).
- Say: "The gate said yes at 3:24, the referee said no at 9:19, same run. The gate did its job; its job does not include held-out checks." Ask: "Was the agent's 422 test wrong?" Expected: no; filters assume the current code is correct, so read every discard reason.
- Screen 3 (`3`), Evidence: the Verification panel's filter table, one row per proposed test, a mark per filter, the reason per discard; read "assert 422 == 412" aloud.
- Screen 2 (`2`), Boards: the two-tab conflict panel: tab A saves, tab B saves from a stale form and gets HTTP 409 and a "changed by someone else" page. Say: "The board stops the lost update; one hidden test still fails."
- Screen 5 (`5`), Traces: the first wrong turn and the LangSmith links for agent and referee. Screen 4 (`4`), A/B Report: Feature 4: Version checks on issue edits rows, empty dots for both arms. Say: "Today's run is not a dot in the comparison."
- If the screen differs: no gate pills means the agent never claimed done; show the filter table and referee counts instead. Every pill failing with `check runner failed` means the harness time limit ran out during the gate; keep the run and say so.
- If the run broke for a reason outside the experiment: `make replay RUN=<id>` with the fallback id recorded the day before, or walk `section-4-verification/demo/expected/` (the screen-1 frames in minute order, then screens 3, 2, 5, 4, and the arm line in `terminal.txt`), saying "recorded before class".
- Time: 9 minutes. Next: what we measured.

## Slide 66: What we measured: No measurable difference on version checks
**Block:** Section 4: Verification  **Time:** 6 min (3:31-3:37)  **Diagram:** section-4-verification/diagrams/results-s4.png  **Layout:** two-column
**On the slide:**
Lead: Earns its place when the agent can claim done early and checks are cheap, exact, partly held out.
Left: What we measured
- Pass: all 69 hidden tests, all 4 mutants
- Bare arm: failed 7 of 7 runs
- Harness arm: failed 7 of 7 runs
- No harness arm claimed done
Right: Apply it Monday
- Run your checks when the agent says done
- Return three failures at most
- Run them where the agent cannot edit
- Plant one fault on your riskiest line
**Visual:** Left card holds the `results-s4` dot chart (bare grey, harness blue, every dot hollow, rounds: medium effort 3, medium effort 3, class settings 1; no percentages); right card is a checklist with icons (terminal, reply arrow, lock, bug).
**Speaker notes:**
- Neither arm passed once in 7 A/Bs (medium effort round 1: 3 of 3 failing per arm; round 2: 3 of 3; class settings: 1 of 1). No measurable difference on this task with this model.
- The registered gate for larger batches needed the harness ahead in 3 of 4 sections; it was ahead in none, so the batches of 10 runs per arm and the leave-one-out ablation were not run.
- Why the gate barely mattered: no harness arm on Feature 4: Version checks on issue edits claimed done in those 7 A/Bs; six used all their build turns, one stopped `not_done`. A gate on the claim never ran.
- Two bare arms claimed done and the referee failed both (one with 69 of 69 hidden tests and a surviving mutant, one with 68 of 69). The reviewer rejected all 14 arms and agreed with the referee each time.
- Post hoc, descriptive only: harness arms shipped fewer tests (median 0 against 15.5 on Feature 4); both arms hit the agent time limit in 4 of 6 Feature 4 runs; across all sections harness arms claimed done in 10 of 34 runs, bare in 19 of 34.
- When it does not earn its place: the agent never claims done; the bug is in the code and the test is right (Filter 2: Passes five runs discards it); few tests are proposed; the checks are wrong.
- Monday: hook test, lint, and migration checks to the agent's done (a stop hook, a wrapper script, or the CI job it must trigger); return a one-line summary and the first few failures; run on a copy, in a container, or in CI; keep a small held-out suite and never feed its output back.
- Cheapest step: plant one fault on your riskiest line by hand, for example "do not increment version on write" for an `If-Match` feature; if no test fails, write the two-writer test. `uv run shipharness testgen --help` shows the course's test generator with the five filters.
- Ask (discussion): "What would a gate need to catch to earn its turns on this model?" Expected: the bare arm's false done claims; a two-writer test; fewer turns spent before the claim.
- Likely question: "Why not rerun with more turns so the harness reaches its gate?" Answer: that is a new registered experiment; changing settings after seeing the result is how a harness gets made to look good.
- Misconception: "no difference means verification is useless". Correction: Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): a separate judge "is worth the cost when the task sits beyond what the current model does reliably solo"; this result is one ticket, one model, a few runs per arm.
- Time: 6 minutes. Next: questions.

## Slide 67: Q&A: Section 4: Verification
**Block:** Section 4: Verification  **Time:** 3 min (3:37-3:40)  **Diagram:** none  **Layout:** template-qa
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
**Visual:** Template Q&A slide unchanged.
**Speaker notes:**
- Likely: "The harness did not win. Was verification useless?" Answer: on Feature 4: Version checks on issue edits the runs barely tested it: the gate never ran in an A/B and the filters saw few tests.
- Likely: "The bare arm caught more mutants. Do the filters hurt?" Answer: the bare arm shipped more tests (median 15.5 against 0); a test nobody writes cannot catch a mutant.
- Likely: "Why does the gate not run the hidden tests?" Answer: they would stop being held out.
- Likely: "Why are Filter 4: Real assertions and Filter 5: No source changes not from a paper?" Answer: no source states them; they guard against a test that mocks the code it tests and a test phase that edits code until its test passes.
- Likely: "Is the model reviewer worth it?" Answer: as a secondary measure; Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) warns it is "inclined to be generous towards LLM-generated outputs". On Feature 4 it rejected all 14 arms and agreed with the referee.
- Likely: "How do I read the gate in the repo?" Answer: `uv run python platform/scripts/anchors.py extract S4:gate`, then `S4:filters` (`S4` is the code for Section 4: Verification).
- Keep an eye on terminal C: if the final has finished its first feature, say so; we read it next.
- Point learners to `section-4-verification/session-notes.md` and the post-class readings.
- Time: 3 minutes; stop at 3:40 and collect the rest in chat. Next: the final A/B, running since about 2:58.

## Slide 68: Final A/B: reading it live
**Block:** Final  **Time:** 5 min (3:40-3:45)  **Diagram:** none  **Layout:** icon-rows
**On the slide:**
Lead: The final has no primary measure: read each arm's counts.
- [check] hidden: does the feature work?
- [bug] mutants: would its tests notice a bug?
- [chat] claim: did the agent say done?
- [board] Screen 2: other-org or duplicate cards?
- [trace] Screen 5: the first wrong turn
**Visual:** Five icon rows; a small note under them: "passed=True means nothing here". Then switch to terminal C and the console, browser tab 3.
**Speaker notes:**
- Terminal C: read today's lines aloud, one feature at a time, then the session figure on the `Cost:` line. The first line names the feature by its code: `F5` is Feature 5: Bulk close, `F6` Feature 6: Watchers, `F7` Feature 7: Labels.
- The three final tickets set `primary_measure = ""`, so the referee marks every run passed: `passed=True` and "primary verdict ready: PASS" say nothing about the feature. Compare hidden tests, mutants, and claims instead.
- The captured Feature 5 run before class (420 s limit, busy machine; `final-project/README.md`): both arms 46 of 46 hidden tests and both said done; mutants killed 3 of 3 (bare) against 1 of 3 (harness); the reviewer accepted bare and rejected harness. Bare completed in 42 turns.
- Its harness arm said done after 20 turns, two gate commands timed out on the busy machine, and the 120 s harness limit ended the arm before a test phase (`ABORTED: timeout`), a known open item. Reading: bare ahead on mutants, one dot, with a cause in machine time rather than in the layers.
- An earlier Feature 5 run (2026-10-17, quiet machine, 300 s agent limit) split differently: mutants 2 of 3 in each arm, hidden 46 of 46 in both. Same feature, same harness, a different split.
- Exit 2 means an arm was aborted on time or cost; it is still judged.
- Console, browser tab 3, press `1`: both arms side by side: status and turns, harness decisions (map placed, handoff written), the gate, "Agent said", the referee line. Capture: bare primary at 4:27, full at 11:39; harness primary at 5:46, full at 11:41; the harness gate pills red on time limits, not on the code.
- Press `3`: files read, diff maps (any `⊘ blocked` or out-of-scope file?), referee checks per rule, the filter and mutant tables. In the Feature 5 capture both arms changed only allowed files; the harness arm's two sandbox denials are the gate's timed-out commands.
- Press `2`: each arm's board as an Acme user. The "✓ only own-org cards, no duplicates" badge comes from trusted data attributes, not from anything the agent wrote. Feature 5 changes no board pixels; for watchers or labels look at the issue pages and for a Globex card (a tenant leak). No run before class leaked, so there is no leak screenshot.
- Press `5`: the first wrong turn per arm and the LangSmith links; that turn is where you start debugging, like the first failing span in a trace. For watchers or labels, also look for the session stop and the handoff on screen 1.
- Ask: "Both arms said done, but the harness arm killed fewer mutants. Did the layers make it worse?" Expected: not on this evidence; its time limit ended it before a test phase; one run cannot say more.
- Misconception: "the arm with `passed=True` won" or "the slower arm is worse". Correction: both say `passed=True` because there is no primary measure; time is a cost to weigh, not a quality measure.
- If the final has not finished or broke: read whatever screen 1 shows, or walk `final-project/expected/` (screens 1 to 5, `terminal.txt`), saying "recorded before class".
- Time: 5 minutes. Next: today's run next to everything from before class.

## Slide 69: All results: four sections, one picture
**Block:** Final  **Time:** 3 min (3:45-3:48)  **Diagram:** docs/diagrams/results-final.png  **Layout:** diagram
**On the slide:**
Lead: One row per section and ticket, one dot per run, bare and harness.
Key idea: One gap, on scope, partly by construction; elsewhere no measurable difference.
**Visual:** The `results-final` diagram: one row per section and ticket, the five rows the notes read out; bare grey, harness blue, filled = passed, hollow = failed. The confirmation row on version checks is the only one where the arms differ.
**Speaker notes:**
- Press `4` on the console first: one dot per recorded run; today's final adds one dot per arm. Say: "One A/B is one dot. Read it next to the runs from before class, never alone."
- Section 1: Instructions, no new tenant leak on Feature 1: Org-wide issue search: 7 of 7 passing per arm. Section 2: State and sessions, no continuity failure on Feature 2: Comments on issues: 7 of 7 each. Section 3: Scope and sandbox on Feature 3: Safe retries for issue creation: 7 of 7 each. No measurable difference.
- Section 3 confirmation on Feature 4: Version checks on issue edits, registered before its runs: bare 0 of 3 in scope, harness 3 of 3. Every bare arm changed `app/services/errors.py`; the scope layer blocked it in every harness arm. Harness ahead, the one gap.
- Section 4: Verification, all hidden tests and mutants on Feature 4: bare 0 of 4, harness 0 of 4 in run 3 and the class round (and 0 of 3 each in the earlier medium round). Both fail; no measurable difference.
- The registered gate for larger batches needed the harness ahead in 3 of 4 sections; it was ahead in 0, so the batches of 10 runs per arm and the ablation were not run.
- Post hoc over 34 runs per arm, descriptive only: files outside the allowed paths in 9 bare runs and 0 harness runs; done claimed in 19 against 10, none with failing hidden tests; median cost per arm $0.0103 bare, $0.0123 harness.
- Analogy: a release dashboard with error bars: one good run does not move a decision.
- Ask: "Why did the one gap show up on scope?" Expected: the scope layer blocks the edit by construction; the other layers only change what the agent reads or how it ends.
- Likely question: "So should I skip the other layers?" Answer: measure them on your own failures. Source 1: [Harness engineering](https://openai.com/index/harness-engineering/): its results "should not be assumed to generalize without similar investment—at least, not yet." The same holds here: one model, one ticket per section, a few runs per arm.
- Misconception: "no measurable difference means no difference". Correction: these few runs cannot show one; a smaller effect needs more runs.
- Time: 3 minutes. Next: which layer when.

## Slide 70: Which layer when: match the layer to the failure
**Block:** Final  **Time:** 2.5 min (3:48-3:50:30)  **Diagram:** docs/diagrams/which-layer-when.png  **Layout:** diagram
**On the slide:**
Lead: Each layer is a bet on one thing the model cannot do on its own.
Key idea: Add the layer that matches a failure you have seen, then measure it.
**Visual:** The `which-layer-when` diagram: four rows (instructions, state, scope, verification), each with the failure it prevents, the signal that says "add it", and its cost; scope carries the only "measured gap" tag.
**Speaker notes:**
- Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."
- Instructions: add a map when the agent breaks rules that live in a wiki or copies legacy patterns. Cost: keeping the docs true.
- State: progress files and a handoff when work spans sessions. Cost: a few turns per stop.
- Scope: allowed paths and a sandbox when agents edit outside the ticket. The only measured gap here: bare 0 of 3 in scope, harness 3 of 3, on Feature 4: Version checks on issue edits, partly by construction.
- Verification: a gate when the agent can claim done early and your checks are cheap and exact; keep some checks held out.
- How to decide in your repo, from [Source 3](https://www.anthropic.com/engineering/harness-design-long-running-apps): "removing one component at a time and reviewing what impact it had on the final result". On TeamTrack, `make final FEATURES=bulk-close LAYERS=-scope` removes one layer from the harness arm.
- Analogy: a security review that picks controls from the incidents you have had, not a vendor's full catalogue.
- Ask: "Which failure do you see most in your repo?" Expected: varied; map each answer to a row.
- Likely question: "Is there a layer you would never skip?" Answer: not on this evidence; the sandbox is the one to keep without a measurement, because it limits damage on the run that goes wrong, which no A/B here measures.
- Misconception: "all four layers or nothing". Correction: the kit's worked example kept every layer but cut instructions down for a small library; decide per layer and write it down.
- Time: 2.5 minutes. Next: take it home.

## Slide 71: Use it in your repo: the kit and four skills
**Block:** Close  **Time:** 1.5 min (3:50:30-3:52)  **Diagram:** none  **Layout:** icon-rows
**On the slide:**
Lead: `uv run shipharness init --target ~/my-repo` copies the kit; `init --check` lists what to fill.
- [map] harness-setup: assess a repo, fill gaps
- [filter] assured-tests: keep tests passing five filters
- [rule] house-rules: convention to rule, check, test
- [template] skill-template: start your own skill
**Visual:** The two commands in a terminal strip as the lead; four icon rows, one per skill.
**Speaker notes:**
- `shipharness init` copies the starter kit (map, state files, feature list, house-rule checks, sandbox policy, CI) with no model calls. Every template holds TeamTrack's real values with a REPLACE marker next to each; `--check` lists the markers still to fill.
- It never overwrites your files: an existing `AGENTS.md` is skipped and reported; `--force` replaces it only if you ask.
- The skills install to `.claude/skills/` (Claude Code, Cursor) and `.agents/skills/` (Codex, Cursor), in the format of Source 6: [Agent Skills Specification](https://agentskills.io/specification): a folder with a `SKILL.md`.
- The guide is `use-in-your-repo/apply-to-your-repo.md`: seven steps: install, copy, fill, check, run, read, decide. Steps 1 to 4 make no model calls.
- Example from the guide: testgen on the boltons queue module kept 3 of 3 proposed tests for $0.002031; the assured-tests example on TeamTrack kept 1 of 5 for $0.003287, the other four failed Filter 3: Adds coverage or catches a mutant.
- Analogy: a cookiecutter template with real defaults and a marker on every value you must change.
- Ask: "Which skill would you install first?" Expected: `house-rules` (turns a repeated review comment into a check) or `assured-tests`.
- Likely question: "Does testgen run my tests on my machine?" Answer: with `--sandbox local`, yes, and it prints UNSANDBOXED; for code you do not trust use `--sandbox docker --image`.
- Misconception: "install the kit and you are done". Correction: step 7 is deciding which layers earn their place; measure before you keep a piece.
- Time: 1.5 minutes. Next: the assignments.

## Slide 72: Assignments: one per layer
**Block:** Close  **Time:** 1.5 min (3:52-3:53:30)  **Diagram:** none  **Layout:** icon-rows
**On the slide:**
Lead: Starter, offline self-check, one live step, full solution.
- [1] Assignment 1: Instructions: a long AGENTS.md to map, docs, skill, checker
- [2] Assignment 2: State and sessions: three forced stops, facts from git
- [3] Assignment 3: Scope and sandbox: diff parser, scope policy, evidence-gated passes
- [4] Assignment 4: Verification: House rule 8: Deleted issues stay hidden; Filter 6: No duplicate tests
**Visual:** Four numbered icon rows, each with its folder in small type: `section-1-instructions/assignment/`, `section-2-state-lifecycle/assignment/`, `section-3-scope-sandbox/assignment/`, `section-4-verification/assignment/`.
**Speaker notes:**
- Same shape for all four: a starter folder, `make check-assignment-N` that runs offline with no keys, one live step, grading criteria out of 100 points, and a full solution with a walkthrough in `solution/`. Try first.
- Assignment 1: Instructions: split a long single `AGENTS.md` with tagged rules into a short map, focused docs, and one Agent Skill; write `checker/check_docs.py` that fails when a link breaks or a rule goes missing; one live A/B and `ab-report.md` with House rule 1: Tenant isolation and House rule 3: API conventions violations as counts.
- Assignment 2: State and sessions: complete `ResumableStateLayer`, which writes what the next session needs from git and the files on disk; a deterministic stand-in agent drives the real runner across three forced stops, offline, then one live run. Its failure is the classic second migration for a table that exists; the step ledger prevents it.
- Assignment 3: Scope and sandbox: a diff parser that finds every changed path (renames, quoted names, `../` paths, empty new files), a per-phase policy, an evidence-gated update of `passes`, and a sandbox rule that refuses git history rewrites. Grading multiplies both sides, so a policy that refuses or allows everything earns nothing there.
- Assignment 4: Verification: turn the soft-delete rule into House rule 8: Deleted issues stay hidden (on unchanged TeamTrack it finds one violation, at `GET /v1/issues`); add Filter 6: No duplicate tests; a testgen run, one live Feature 4: Version checks on issue edits A/B, and a portfolio (evidence report, LangSmith link, one-page case study, your own skill).
- Assignment 4's reference solution passes its self-check 23 of 23; the unchanged starter passes 2 of 23, by design. Each FAIL line names what to build.
- Ask: "Why must Assignment 2's facts come from git?" Expected: the agent's account is a claim, the same lesson as today's done claim.
- Likely question: "Is the grader in the repo?" Answer: no; the self-check runs the visible checks, the instructor's grader adds hidden cases, like today's hidden tests.
- Misconception: "the live step must show the harness winning". Correction: report counts; a tie is a valid result. In Assignment 4's reference run neither arm passed the primary measure.
- Time: 1.5 minutes; the review session gives each about 25 minutes. Next: the final project.

## Slide 73: Final project: one live A/B, read as one dot
**Block:** Close  **Time:** 1 min (3:53:30-3:54:30)  **Diagram:** none  **Layout:** steps
**On the slide:**
Lead: Repeat today's final on your machine.
1. Run `make final FEATURES=bulk-close`
2. Remove one layer: `LAYERS=-scope`
3. Read counts, never one verdict
4. Draw your dots: `uv run shipharness report`
**Visual:** Four numbered step cards with the commands in monospace; a footer: "Feeds the portfolio of Assignment 4: Verification".
**Speaker notes:**
- Run `make final FEATURES=bulk-close`, with `PURPOSE=pilot` outside class. At the caps one feature costs at most $0.58.
- Leave-one-out: `make final FEATURES=bulk-close LAYERS=-scope` removes one layer from the harness arm, the method of Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), one feature at a time.
- `uv run shipharness report` makes no model calls and writes `exports/report.html`: one dot per run, filled for passed, hollow for failed.
- The portfolio for Assignment 4: Verification: the A/B's score records and trace links, the kit's check and testgen output on a repository you choose, a one-page case study, and a skill of your own.
- Why "one dot": the course ran Feature 5: Bulk close more than once before class and the A/Bs split differently on mutants: 2 of 3 each in an earlier run, then 3 of 3 (bare) against 1 of 3 (harness).
- Analogy: a benchmark result published with its run count and variance, not a single best run.
- Ask: "How many runs before you believe a gap?" Expected: more than one per arm; the course planned 10 per arm for its larger batches.
- Likely question: "Can I run it without Docker?" Answer: not for results; `SANDBOX_MODE=none` is not allowed for results, because both arms must run in the same kind of container.
- Misconception: "my one A/B shows the harness works on my repo". Correction: it shows one dot; report counts and say what more runs would need to show. The guide is `final-project/README.md`.
- Time: 1 minute. Next: one picture of everything.

## Slide 74: The harness in one picture
**Block:** Close  **Time:** 1 min (3:54:30-3:55:30)  **Diagram:** docs/diagrams/harness-one-picture.png  **Layout:** diagram
**On the slide:**
Lead: Four layers around an unchanged model, one sandbox, one referee outside.
Key idea: Each layer changes what the agent sees, keeps, may touch, or must prove.
**Visual:** The `harness-one-picture` diagram, full frame: the agent loop in the centre, the four layers around it, the sandbox around both arms, the referee outside.
**Speaker notes:**
- Instructions: a map of about 100 lines in context, details on disk, skills that load in tiers. It informs; it never blocks.
- State: a progress file, an exec plan, and a two-owner handoff; the harness writes the facts from git at every stop.
- Scope: one feature at a time, allowed paths per phase checked on every tool call, `passes` set only by the harness.
- Verification: a gate on "done", five test filters, and held-out hidden tests and mutants the agent never sees.
- The sandbox: one container per arm, no network, keys on the host; the same for both arms, so no A/B here measures it.
- The referee sits outside the harness and scores what shipped, the same way for both arms.
- Analogy: onboarding docs, a shift handover, least privilege, and CI gates: four practices your team trusts for humans, applied to an agent.
- Point at the scope ring: the one layer with a measured gap, on Feature 4: Version checks on issue edits, partly by construction.
- Ask: "Which ring would you add first?" Expected: the one that matches a failure you have seen.
- Misconception: "more rings means a safer agent". Correction: each ring costs turns and time; harness arms ran longer than bare arms before class.
- Time: 1 minute. Next: the summary.

## Slide 75: Module 1 Summary: Key takeaways
**Block:** Close  **Time:** 1.5 min (3:55:30-3:57)  **Diagram:** docs/diagrams/module-summary.png  **Layout:** diagram
**On the slide:**
Lead: Four layers, four measurements, one rule.
Key idea: Every layer is a bet on what the model cannot do alone; measure it before you keep it.
**Visual:** The `module-summary` diagram: four section boxes, each with its mechanism and measured result, leading to numbered takeaways in "X = Y" form.
**Speaker notes:**
- Takeaway 1, instructions = a short map in context, details on disk, checked by a script. On Feature 1: Org-wide issue search: no measurable difference; the model already scoped its query.
- Takeaway 2, state = facts from git at every stop, notes from the agent. On Feature 2: Comments on issues: no measurable difference; the repository was enough state for this model.
- Takeaway 3, scope = allowed paths checked by code, a sandbox for both arms. On Feature 4: Version checks on issue edits: bare 0 of 3 in scope, harness 3 of 3, partly by construction; on Feature 3: Safe retries for issue creation, no measurable difference.
- Takeaway 4, verification = checks the agent does not own: a gate, filters, hidden tests, mutants. On Feature 4: both arms failed every run; no measurable difference.
- Takeaway 5, every layer = a bet on what the model cannot do on its own: same ticket, model, and referee, counts per arm, never one run.
- Concrete next step: count your agent's out-of-scope files with `git diff --name-only` before you enforce anything; it is the cheapest measurement in the module.
- Analogy: a post-incident review: keep the controls that would have caught a failure you actually had.
- Ask: "Which takeaway surprised you?" Expected: that three of four layers showed no measurable difference on this model.
- Likely question: "Will these results hold for my model?" Answer: unknown; re-measure when the model changes.
- Misconception: "no measurable difference means the layer is useless". Correction: these few runs on one ticket per section cannot show a smaller effect.
- Time: 1.5 minutes. Next: a glimpse of Module 2.

## Slide 76: Glimpse of Module 2: Loop Engineering for Coding Agents
**Block:** Close  **Time:** 1 min (3:57-3:58)  **Diagram:** none  **Layout:** icon-rows
**On the slide:**
Lead: Module 1 built the harness around one run; Module 2 builds the loop around many.
- [bolt] Background and event-driven runs: agents that start on events
- [chart] Hill climbing: change one thing, keep it if the score rises
- [shield] Defenses against agents that actively game checks
- [repeat] pass^k reliability: does it pass every one of k tries?
- [box] Detailed sandbox design
**Visual:** Five icon rows, one per topic, under the lead line.
**Speaker notes:**
- Background and event-driven runs: the agent starts from an event (a new ticket, a failing check) instead of a person at a terminal.
- Hill climbing: change one piece of the harness, re-measure, keep it only if the measure improves; it reuses today's referee and A/B.
- Gaming defenses: today no run showed deliberate gaming; Module 2 covers agents that actively work around checks, building on today's held-out tests and mutants.
- pass^k: one passing run is one dot; pass^k asks whether all k tries pass, a stricter reading of reliability.
- Sandbox design in detail: today's container flags were the same for both arms; Module 2 designs the boundary itself.
- Ask: "Which would you want for your own agent first?" Expected: varied; event-driven runs are common in CI.
- Analogy: Module 1 was one well-instrumented build; Module 2 is the CI system that runs many of them and learns from the results.
- Misconception: "Module 2 replaces the harness". Correction: every Module 2 topic runs on today's harness, referee, and A/B.
- Time: 1 minute. Next: where every quote came from.

## Slide 77: References (1 of 2): sources in the order cited
**Block:** Close  **Time:** 0.25 min (3:58-3:58:15)  **Diagram:** none  **Layout:** table
**On the slide:**
Lead: Every source cited today, numbered in order of first use, with its link.
| Source | Title, author, date |
|---|---|
| Source 1 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), Ryan Lopopolo, OpenAI, 2026-02-11 |
| Source 2 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), Justin Young, Anthropic, 2025-11-26 |
| Source 3 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), Prithvi Rajasekaran, Anthropic, 2026-03-24 |
| Source 4 | [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler), Nicholas Carlini, Anthropic, 2026-02-05 |
| Source 5 | [Billing (LangSmith docs)](https://docs.langchain.com/langsmith/billing), LangChain, living page |
| Source 6 | [Agent Skills Specification](https://agentskills.io/specification), Agent Skills project, undated |
| Source 7 | [Extend Claude with skills](https://code.claude.com/docs/en/skills), Anthropic, Claude Code docs, living page |
| Source 8 | [Build skills](https://learn.chatgpt.com/docs/build-skills), OpenAI, Codex docs, living page |
| Source 9 | [Agent Skills (Cursor docs)](https://cursor.com/docs/skills), Anysphere, Cursor docs, living page |
**Visual:** A native two-column table: "Source N" in blue, the linked title, author, and date in dark text.
**Speaker notes:**
- These are the sources behind the four causes and the four layers, numbered in the order the slides first cite them, with exact titles and links from the course's evidence pages.
- [Source 1](https://openai.com/index/harness-engineering/): the map instead of a giant instruction file, the house rules, and the warning that results should not be assumed to generalize.
- [Source 2](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): sessions start with no memory; clean state; progress files and the feature list. [Source 3](https://www.anthropic.com/engineering/harness-design-long-running-apps): self-grading skews positive; separating doer and judge; removing one component at a time. [Source 4](https://www.anthropic.com/engineering/building-c-compiler): a nearly perfect verifier, short test output, run it in a container.
- The skills pages say where each client looks for skills; the starter kit installs into `.claude/skills/` and `.agents/skills/` for that reason, and post-class reading 03 in `section-1-instructions/` summarises them.
- Where the links come from: the Sources sections of `docs/evidence/s1.md` to `docs/evidence/s4.md` and `docs/evidence/final.md`, which also list every quote.
- Likely question: "Which one should I read first?" Answer: [Source 3](https://www.anthropic.com/engineering/harness-design-long-running-apps), then [Source 1](https://openai.com/index/harness-engineering/).
- Each entry gives the title, the link, the author, and the date; living documentation pages carry no date, so they say so.
- Ask: "Which source would you send to your team lead first?" Expected: the one about the failure your team has seen.
- Time: 15 seconds. Next: the rest.

## Slide 78: References (2 of 2): the remaining sources
**Block:** Close  **Time:** 0.25 min (3:58:15-3:58:30)  **Diagram:** none  **Layout:** table
**On the slide:**
Lead: The rest of today's sources, with links.
| Source | Title, author, date |
|---|---|
| Source 10 | [Using PLANS.md for multi-hour problem solving](https://cookbook.openai.com/articles/codex_exec_plans), Aaron Friel, OpenAI Cookbook, 2025-10-07 |
| Source 11 | [None network driver (Docker docs)](https://docs.docker.com/engine/network/drivers/none/), Docker, living page |
| Source 12 | [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384), Zhao, Srikanth, Wu, Jiang, Weco AI ([repository](https://github.com/WecoAI/SpecBench)), 2026-05-20 |
| Source 13 | [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/abs/2402.09171), Alshahwan et al., Meta, FSE 2024 |
| Source 14 | [Mutation-Guided LLM-based Test Generation at Meta](https://arxiv.org/abs/2501.12862), Foster et al., Meta, 2025 |
| Source 15 | [Autonomous Coding Agent Demo (README)](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding), Anthropic, 2025-11-26 |
| Source 16 | [What are skills?](https://agentskills.io/what-are-skills), Agent Skills project, undated |
| Source 17 | [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support.md), Agent Skills project, undated |
**Visual:** The same table style as part 1.
**Speaker notes:**
- The Meta papers: Source 13 ([TestGen-LLM](https://arxiv.org/abs/2402.09171)) gives Filters 1 to 3 and the five-run flakiness check; Source 14 ([ACH](https://arxiv.org/abs/2501.12862)) gives targeted mutants, the mutant branch of Filter 3: Adds coverage or catches a mutant, and the limit that it cannot find existing faults.
- [Source 12](https://arxiv.org/abs/2605.21384) and its repository: visible against held-out suites, and compositional failures. Not the unrelated Spec-Bench paper.
- [Source 11](https://docs.docker.com/engine/network/drivers/none/): what `--network none` leaves inside the container. Source 5: [LangSmith billing](https://docs.langchain.com/langsmith/billing): ordinary traces are kept 14 days. [Source 10](https://cookbook.openai.com/articles/codex_exec_plans): the exec plan of Section 2: State and sessions; [Source 15](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding): the feature list and `init.sh` pattern.
- Post-class readings in `section-4-verification/post-class-reading/` summarise the three papers in about 20 minutes.
- Likely question: "Are the quotes checked?" Answer: yes; each was checked against the source text, and the evidence pages list them.
- The same numbered list sits in the Sources section at the end of the slide file, so every "Source N" in the notes resolves to one entry.
- Time check: the close should be at about 3:58:30 here; keep the last Q&A short.
- Misconception: "Filter 4: Real assertions and Filter 5: No source changes are from [TestGen-LLM](https://arxiv.org/abs/2402.09171)". Correction: they are the course's own; the evidence page says so.
- Time: 15 seconds. Next: last questions.

## Slide 79: Q&A: anything from today
**Block:** Close  **Time:** 1.25 min (3:58:30-3:59:45)  **Diagram:** none  **Layout:** template-qa
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
**Visual:** Template Q&A slide unchanged.
**Speaker notes:**
- Take the questions collected in chat during Section 4: Verification first.
- Likely: "Which layer should I add first at work?" Answer: the one that matches a failure you have seen; scope is the only one with a measured gap here, on one ticket and partly by construction; count out-of-scope files before you enforce anything.
- Likely: "Will these results hold for a stronger model?" Answer: unknown; each layer encodes an assumption about the model, and Source 3: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) dropped context resets for a newer model. Re-measure when the model changes.
- Likely: "How much did this session cost?" Answer: read the session figure from the last `Cost:` line in terminal C; the cap was $2.50.
- Likely: "Where do I start tomorrow?" Answer: `use-in-your-repo/apply-to-your-repo.md`, step 1, or Assignment 1: Instructions.
- Remind: the review session covers each assignment, about 25 minutes each.
- After class (instructor): `uv run shipharness report`, back up `.shipharness/runs/` and `exports/`, note each command's `Cost:` line.
- Time: 1 minute 15 seconds; collect the rest in chat. Next: thank you.

## Slide 80: Thank you: see you at the review session
**Block:** Close  **Time:** 0.25 min (3:59:45-4:00)  **Diagram:** none  **Layout:** template-thank-you
**On the slide:**
Thank you
**Visual:** The template's closing picture slide: full image, one line of text.
**Speaker notes:**
- Thank the room for the poll and the questions.
- Repeat the one line of the session: each harness piece is a bet on what the model cannot do; measure it before you keep it.
- Point to the repository: section folders, `use-in-your-repo/`, and `final-project/`; the four assignments and their offline self-checks.
- Class run records stay on the instructor's machine; captured runs are in each `demo/expected/` folder.
- Invite results from their own repos, reported as counts.
- Stop the console (Ctrl+C in terminal A) only after the last screen is closed. End at 4:00.

## Sources

- Source 1: Harness engineering: leveraging Codex in an agent-first world, <https://openai.com/index/harness-engineering/>, Ryan Lopopolo (OpenAI), 2026-02-11
- Source 2: Effective harnesses for long-running agents, <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>, Justin Young (Anthropic), 2025-11-26
- Source 3: Harness design for long-running application development, <https://www.anthropic.com/engineering/harness-design-long-running-apps>, Prithvi Rajasekaran (Anthropic), 2026-03-24
- Source 4: Building a C compiler with a team of parallel Claudes, <https://www.anthropic.com/engineering/building-c-compiler>, Nicholas Carlini (Anthropic), 2026-02-05
- Source 5: Billing (LangSmith docs), <https://docs.langchain.com/langsmith/billing>, LangChain (LangSmith docs), n.d.
- Source 6: Agent Skills Specification, <https://agentskills.io/specification>, Agent Skills project, n.d.
- Source 7: Extend Claude with skills, <https://code.claude.com/docs/en/skills>, Claude Code docs (Anthropic), n.d.
- Source 8: Build skills, <https://learn.chatgpt.com/docs/build-skills>, Codex docs (OpenAI), n.d.
- Source 9: Agent Skills (Cursor docs), <https://cursor.com/docs/skills>, Cursor docs, n.d.
- Source 10: Using PLANS.md for multi-hour problem solving, <https://cookbook.openai.com/articles/codex_exec_plans>, Aaron Friel (OpenAI Cookbook), 2025-10-07
- Source 11: None network driver (Docker docs), <https://docs.docker.com/engine/network/drivers/none/>, Docker documentation, n.d.
- Source 12: SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents, <https://arxiv.org/abs/2605.21384>, Zhao, Srikanth, Wu, and Jiang (Weco AI), 2026-05-20
- Source 13: Automated Unit Test Improvement using Large Language Models at Meta, <https://arxiv.org/abs/2402.09171>, Alshahwan et al. (Meta), 2024-02-14
- Source 14: Mutation-Guided LLM-based Test Generation at Meta, <https://arxiv.org/abs/2501.12862>, Foster et al. (Meta), 2025-01-22
- Source 15: Autonomous Coding Agent Demo (README), <https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding>, Anthropic, 2025-11-26
- Source 16: What are skills?, <https://agentskills.io/what-are-skills>, Agent Skills project, n.d.
- Source 17: How to add skills support to your agent, <https://agentskills.io/client-implementation/adding-skills-support.md>, Agent Skills project, n.d.
