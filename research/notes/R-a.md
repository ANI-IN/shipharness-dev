# R-a Primary harness sources

Method: each source was downloaded directly (curl) and converted to plain text locally, so quotes come from the page text, not from a summarizer. Quotes keep the sources' own punctuation (curly apostrophes) and spelling, including typos. No third-party course repositories, skill packs or tutorials were opened.

## Sources

| id | title | URL | author(s)/org | publication date | access date | summary |
|---|---|---|---|---|---|---|
| A1 | Harness engineering: leveraging Codex in an agent-first world | https://openai.com/index/harness-engineering/ | Ryan Lopopolo, Member of the Technical Staff, OpenAI (thanks to Victor Zhu, Zach Brock) | 2026-02-11 | 2026-10-16 | Describes five months of building an internal product where Codex wrote every line of code. Covers a short AGENTS.md acting as a map into a structured docs/ directory, making the app UI, logs and metrics legible to the agent, architecture and "taste invariants" enforced by custom linters, and recurring cleanup ("garbage collection") by background agents. |
| A2 | Effective harnesses for long-running agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Justin Young, Anthropic | 2025-11-26 | 2026-10-16 | Describes a two-part harness for work across many context windows: an initializer agent that sets up init.sh, a progress file, a JSON feature list and an initial git commit, and a coding agent that works on one feature per session and leaves a clean state. Includes a session-start routine, end-to-end browser testing, and a table of four failure modes. |
| A3 | Harness design for long-running application development | https://www.anthropic.com/engineering/harness-design-long-running-apps | Prithvi Rajasekaran, Labs team, Anthropic | 2026-03-24 | 2026-10-16 | Introduces a generator/evaluator loop, first for frontend design with four grading criteria, then a planner/generator/evaluator architecture for full-stack apps with sprint contracts. Discusses context resets versus compaction, self-evaluation leniency, cost and duration numbers, and later removal of the sprint construct for Opus 4.6. |
| A4 | Building a C compiler with a team of parallel Claudes | https://www.anthropic.com/engineering/building-c-compiler | Nicholas Carlini, Safeguards team, Anthropic | 2026-02-05 | 2026-10-16 | Reports 16 parallel agents in a loop building a 100,000-line Rust C compiler over nearly 2,000 sessions for about $20,000. Lessons focus on extremely high-quality tests, CI against regressions, designing test output for the model (context window pollution, time blindness), task locks in git, GCC as a known-good oracle, and specialized agent roles. |
| A5 | Autonomous Coding Agent Demo (README of autonomous-coding quickstart) | https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding | Anthropic (commit co-authored by Justin Young) | README committed 2025-11-26 | 2026-10-16 | Reference implementation of the A2 pattern. README only was read: two-agent pattern (initializer in session 1, coding agent in sessions 2+), feature_list.json with 200 test cases as "source of truth", init.sh, claude-progress.txt, fresh context per session, and a three-layer security model (OS sandbox, filesystem restriction, bash allowlist). |
| A6 (supplementary; linked from A2) | Prompting best practices (section "Workflows across multiple context windows" and "State management best practices") | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#workflows-across-multiple-context-windows | Anthropic, Claude Platform Docs | undated living page; current text mentions Claude Sonnet 5 and Opus 4.6 | 2026-10-16 | Official doc that A2 cites as "the updated Claude 4 prompting guide". Gives the multi-window recipe: different first-window prompt, tests in structured format (tests.json), init.sh, starting fresh vs compacting, verification tools, git for state. Text may have changed since A2 cited it. |
| A7 (supplementary; linked from A1) | Using PLANS.md for multi-hour problem solving | https://cookbook.openai.com/articles/codex_exec_plans | Aaron Friel, OpenAI Cookbook | 2025-10-07 (page marked "This recipe is archived") | 2026-10-16 | Official OpenAI recipe that A1 links as "execution plans". Defines "ExecPlan" as a self-contained living design document governed by PLANS.md, referenced from AGENTS.md, with mandatory Progress, Surprises & Discoveries, Decision Log and Outcomes & Retrospective sections. |

## Findings

Format: `ID` | tags | claim | exact quote | source + section.

### Storyline and causes

- `F-a-01` | storyline | A1 frames the engineer's job as steering agents, not writing code. | "Humans steer. Agents execute." | A1, introduction
- `F-a-02` | storyline | A1 says the team's job became designing environments, intent and feedback loops. | "design environments, specify intent, and build feedback loops that allow Codex agents to do reliable work." | A1, introduction
- `F-a-03` | storyline; cause1 | Early slowness came from an underspecified environment, not model weakness. | "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified." | A1, Redefining the role of the engineer
- `F-a-04` | storyline | When the agent fails, the fix is a missing capability, not "try harder". | "“what capability is missing, and how do we make it both legible and enforceable for the agent?”" | A1, Redefining the role of the engineer
- `F-a-05` | cause1; S1 | The agent cannot use knowledge it cannot see in context. | "From the agent’s point of view, anything it can’t access in-context while running effectively doesn’t exist." | A1, Agent legibility is the goal
- `F-a-06` | cause1; S1 | Knowledge outside the repo (docs, chat, heads) is unavailable to the agent. | "Knowledge that lives in Google Docs, chat threads, or people’s heads are not accessible to the system." | A1, Agent legibility is the goal
- `F-a-07` | cause1; S1 | Undiscoverable team decisions are illegible to the agent, like to a late new hire. | "If it isn’t discoverable to the agent, it’s illegible in the same way it would be unknown to a new hire joining three months later." | A1, Agent legibility is the goal
- `F-a-08` | cause2; S2 | Each new session starts with no memory of the previous one. | "each new session begins with no memory of what came before." | A2, introduction
- `F-a-09` | cause2; S2 | A2's analogy: engineers working shifts with no memory of the previous shift. | "Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift." | A2, introduction
- `F-a-10` | cause2; S2 | A fresh agent in a fresh container has no context and spends time orienting. | "each agent is dropped into a fresh container with no context and will spend significant time orienting itself, especially on large projects." | A4, Put yourself in Claude’s shoes
- `F-a-11` | cause2; S2 | Failure mode 1: trying to one-shot the app, running out of context mid-feature. | "the agent tended to try to do too much at once—essentially to attempt to one-shot the app." | A2, The long-running agent problem
- `F-a-12` | cause2; S2 | The next session then had to guess what happened. | "leaving the next session to start with a feature half-implemented and undocumented. The agent would then have to guess at what had happened" | A2, The long-running agent problem
- `F-a-13` | cause4; S4 | Failure mode 2: a later agent sees progress and declares the job done. | "a later agent instance would look around, see that progress had been made, and declare the job done." | A2, The long-running agent problem
- `F-a-14` | cause4; S4 | Agents praise their own work even when it is mediocre. | "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre." | A3, Why naive implementations fall short
- `F-a-15` | cause4; S4 | Agents skew positive when grading their own work. | "agents reliably skew positive when grading their own work." | A3, Why naive implementations fall short
- `F-a-16` | cause4; S4 | Claude marked features complete without end-to-end testing. | "Claude’s tendency to mark a feature as complete without proper testing." | A2, Testing
- `F-a-17` | cause4; S4 | Passing tests can be mistaken for a finished job in autonomous systems. | "For autonomous systems, it is easy to see tests pass and assume the job is done, when this is rarely the case." | A4, Looking forward
- `F-a-18` | cause3; S3 | (Partial support for cause 3.) The loop runs Claude without permission prompts; the author says to use a container. | "(Run this in a container, not your actual machine)." | A4, Enabling long-running Claudes
- `F-a-19` | cause3; S3 | (Partial support for cause 3.) An unconstrained agent killed its own process. | "in one instance, I did see Claude pkill -9 bash on accident, thus killing itself and ending the loop." | A4, Enabling long-running Claudes
- `F-a-20` | cause3; S3 | (Partial support for cause 3.) Codex copies existing patterns, including bad ones, leading to drift. | "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones. Over time, this inevitably leads to drift." | A1, Entropy and garbage collection
- `F-a-21` | cause3; S3 | (Partial support for cause 3; supplementary doc.) Without guidance the model may take hard-to-reverse actions. | "Without guidance, Claude Opus 4.6 may take actions that are difficult to reverse or affect shared systems, such as deleting files, force-pushing, or posting to external services." | A6, Balancing autonomy and safety

### S1 Instructions

- `F-a-22` | S1 | Give the agent a map, not a long manual. | "give Codex a map, not a 1,000-page instruction manual." | A1, We made repository knowledge the system of record
- `F-a-23` | S1; cause1 | A giant instruction file crowds out the task and code. | "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs" | A1, We made repository knowledge the system of record
- `F-a-24` | S1 | Too much guidance stops being guidance. | "Too much guidance becomes non-guidance. When everything is “important,” nothing is." | A1, We made repository knowledge the system of record
- `F-a-25` | S1 | A monolithic instruction file goes stale. | "It rots instantly. A monolithic manual turns into a graveyard of stale rules." | A1, We made repository knowledge the system of record
- `F-a-26` | S1 | A single blob cannot be checked mechanically, so drift follows. | "A single blob doesn’t lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable." | A1, We made repository knowledge the system of record
- `F-a-27` | S1 | AGENTS.md is treated as a table of contents. | "So instead of treating AGENTS.md as the encyclopedia, we treat it as the table of contents." | A1, We made repository knowledge the system of record
- `F-a-28` | S1 | Short AGENTS.md (roughly 100 lines), injected into context, points to docs/ as the system of record. | "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere." | A1, We made repository knowledge the system of record
- `F-a-29` | S1 | The knowledge base is a structured docs/ directory. | "The repository’s knowledge base lives in a structured docs/ directory treated as the system of record." | A1, We made repository knowledge the system of record
- `F-a-30` | S1 | Layout shown: root AGENTS.md and ARCHITECTURE.md; docs/ holds design-docs/, exec-plans/ (active/, completed/, tech-debt-tracker.md), generated/db-schema.md, product-specs/, references/ (*-llms.txt), and DESIGN.md, FRONTEND.md, PLANS.md, PRODUCT_SENSE.md, QUALITY_SCORE.md, RELIABILITY.md, SECURITY.md. | "In-repository knowledge store layout." (figure caption; file names from the figure, e.g. "uv-llms.txt", "tech-debt-tracker.md") | A1, We made repository knowledge the system of record
- `F-a-31` | S1 | Design docs are indexed with verification status and core beliefs. | "Design documentation is catalogued and indexed, including verification status and a set of core beliefs that define agent-first operating principles." | A1, We made repository knowledge the system of record
- `F-a-32` | S1 | Architecture doc maps domains and package layering. | "Architecture documentation provides a top-level map of domains and package layering." | A1, We made repository knowledge the system of record
- `F-a-33` | S1; S4 | A quality document grades domains and layers over time. | "A quality document grades each product domain and architectural layer, tracking gaps over time." | A1, We made repository knowledge the system of record
- `F-a-34` | S1; S2 | Plans are first-class, checked-in artifacts with progress and decision logs. | "complex work is captured in execution plans with progress and decision logs that are checked into the repository." | A1, We made repository knowledge the system of record
- `F-a-35` | S1; S2 | Active plans, completed plans and tech debt are versioned so agents need no external context. | "Active plans, completed plans, and known technical debt are all versioned and co-located, allowing agents to operate without relying on external context." | A1, We made repository knowledge the system of record
- `F-a-36` | S1 | Progressive disclosure: small entry point, then pointers. | "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front." | A1, We made repository knowledge the system of record
- `F-a-37` | S1 | Docs are enforced by linters and CI jobs. | "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly." | A1, We made repository knowledge the system of record
- `F-a-38` | S1 | A recurring doc-gardening agent fixes stale docs. | "A recurring “doc-gardening” agent scans for stale or obsolete documentation that does not reflect the real code behavior and opens fix-up pull requests." | A1, We made repository knowledge the system of record
- `F-a-39` | S1 | Only repo-local, versioned artifacts are visible to the agent. | "Repository-local, versioned artifacts (e.g., code, markdown, schemas, executable plans) are all it can see." | A1, Agent legibility is the goal
- `F-a-40` | S1 | Push more context into the repo over time. | "We learned that we needed to push more and more context into the repo over time." | A1, Agent legibility is the goal
- `F-a-41` | S1 | More context means organizing information, not adding ad-hoc instructions. | "organizing and exposing the right information so the agent can reason over it, rather than overwhelming it with ad-hoc instructions." | A1, Agent legibility is the goal
- `F-a-42` | S1 | Prefer "boring", in-repo-reasonable dependencies. | "Technologies often described as “boring” tend to be easier for agents to model due to composability, api stability, and representation in the training set." | A1, Agent legibility is the goal
- `F-a-43` | S1; S3 | When docs are not enough, the rule becomes code. | "When documentation falls short, we promote the rule into code" | A1, Enforcing architecture and taste
- `F-a-44` | S1; S3 | Agent struggles are signals to add tools, guardrails or docs to the repo. | "When the agent struggles, we treat it as a signal: identify what is missing—tools, guardrails, documentation—and feed it back into the repository" | A1, What “agent-generated” actually means
- `F-a-45` | S1; S2 | Supplementary: AGENTS.md tells the agent when to use PLANS.md / ExecPlans. | "We enable Codex to use these documents by first updating AGENTS.md to describe when to use PLANS.md" | A7, Using PLANS.md for multi-hour problem solving
- `F-a-46` | S1; S2 | Supplementary: an ExecPlan must be self-contained for a novice. | "Every ExecPlan must be fully self-contained. Self-contained means that in its current form it contains all knowledge and instructions needed for a novice to succeed." | A7, Requirements (PLANS.md)
- `F-a-47` | S2 | Supplementary: restart must be possible from the ExecPlan alone. | "it should always be possible to restart from _only_ the ExecPlan and no other work." | A7, How to use ExecPlans and PLANS.md
- `F-a-48` | S2 | Supplementary: required living sections. | "ExecPlans must contain and maintain a `Progress` section, a `Surprises & Discoveries` section, a `Decision Log`, and an `Outcomes & Retrospective` section." | A7, Living plans and design decisions

### S2 State and session lifecycle

- `F-a-49` | S2 | Two-part solution: initializer agent on first run, coding agent for incremental progress with artifacts for the next session. | "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session" | A2, introduction
- `F-a-50` | S2 | Initializer sets up init.sh, claude-progress.txt and an initial git commit. | "an init.sh script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit that shows what files were added." | A2, The long-running agent problem
- `F-a-51` | S2 | Coding agent: incremental progress, then structured updates. | "Every subsequent session asks the model to make incremental progress, then leave structured updates." | A2, The long-running agent problem
- `F-a-52` | S2 | The "two agents" differ only by initial user prompt. | "We refer to these as separate agents in this context only because they have different initial user prompts." | A2, Footnote 1
- `F-a-53` | S2 | Key insight: progress file plus git history lets a fresh session understand state. | "accomplished with the claude-progress.txt file alongside the git history." | A2, The long-running agent problem
- `F-a-54` | S2 | Compaction alone was not enough. | "However, compaction isn’t sufficient." | A2, The long-running agent problem
- `F-a-55` | S2 | Compaction may not pass clear instructions to the next agent. | "This happens even with compaction, which doesn’t always pass perfectly clear instructions to the next agent." | A2, The long-running agent problem
- `F-a-56` | S2; S3 | Commit with descriptive messages and write progress summaries; git enables revert. | "ask the model to commit its progress to git with descriptive commit messages and to write summaries of its progress in a progress file." | A2, Incremental progress
- `F-a-57` | S2 | Git lets the model revert bad changes. | "This allowed the model to use git to revert bad code changes and recover working states of the code base." | A2, Incremental progress
- `F-a-58` | S2 | Session-start step: pwd. | "Run pwd to see the directory you’re working in. You’ll only be able to edit files in this directory." | A2, Getting up to speed
- `F-a-59` | S2 | Session-start step: read git logs and progress files. | "Read the git logs and progress files to get up to speed on what was recently worked on." | A2, Getting up to speed
- `F-a-60` | S2; S3 | Session-start step: pick the highest-priority unfinished feature. | "Read the features list file and choose the highest-priority feature that’s not yet done to work on." | A2, Getting up to speed
- `F-a-61` | S2; S4 | init.sh runs the dev server; run a basic end-to-end test before new work. | "ask the initializer agent to write an init.sh script that can run the development server, and then run through a basic end-to-end test before implementing a new feature." | A2, Getting up to speed
- `F-a-62` | S2; S4 | Testing first catches a broken state; building on it makes things worse. | "If the agent had instead started implementing a new feature, it would likely make the problem worse." | A2, Getting up to speed
- `F-a-63` | S2 | Failure table row: session start reads progress and git logs and runs a basic test; session end commits and updates progress. | "End the session by writing a git commit and progress update." | A2, Agent failure modes and solutions (table)
- `F-a-64` | S2 | Failure table row: init.sh solves time spent figuring out how to run the app. | "Write an init.sh script that can run the development server." | A2, Agent failure modes and solutions (table)
- `F-a-65` | S2 | Context reset definition: clear the window and start a fresh agent with a structured handoff. | "Context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps" | A3, Why naive implementations fall short
- `F-a-66` | S2 | Compaction keeps continuity but no clean slate. | "While compaction preserves continuity, it doesn't give the agent a clean slate, which means context anxiety can still persist." | A3, Why naive implementations fall short
- `F-a-67` | S2 | "Context anxiety": wrapping up early near a perceived limit. | "Some models also exhibit \"context anxiety,\" in which they begin wrapping up work prematurely as they approach what they believe is their context limit." | A3, Why naive implementations fall short
- `F-a-68` | S2 | Resets cost orchestration complexity, tokens and latency. | "This solves the core issue, but adds orchestration complexity, token overhead, and latency to each harness run." | A3, Why naive implementations fall short
- `F-a-69` | S2 | Resets are model-dependent: dropped for Opus 4.5, which ran with automatic compaction. | "Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely." | A3, The architecture
- `F-a-70` | S2 | Agents communicated through files. | "Communication was handled via files: one agent would write a file, another agent would read it and respond either within that file or with a new file" | A3, The architecture
- `F-a-71` | S2 | Two lessons carried over: decompose into chunks; structured artifacts for handoff. | "decomposing the build into tractable chunks, and using structured artifacts to hand off context between sessions." | A3, introduction
- `F-a-72` | S2 | Instructions to keep READMEs and progress files updated. | "I included instructions to maintain extensive READMEs and progress files that should be updated frequently with the current status." | A4, Put yourself in Claude’s shoes
- `F-a-73` | S2 | Agents keep a running doc of failed approaches when stuck. | "When stuck on a bug, Claude will often maintain a running doc of failed approaches and remaining tasks." | A4, Running Claude in parallel
- `F-a-74` | S2 | Quickstart: each session has a fresh context; progress persists via feature list and git. | "Progress is persisted via `feature_list.json` and git commits" | A5, Session Management
- `F-a-75` | S2 | Supplementary: different prompt for the first context window. | "Use the first context window to set up a framework (write tests, create setup scripts), then use future context windows to iterate on a todo-list." | A6, Workflows across multiple context windows
- `F-a-76` | S2 | Supplementary: consider a fresh window over compaction; model discovers state from filesystem. | "Claude's latest models are extremely effective at discovering state from the local filesystem." | A6, Workflows across multiple context windows
- `F-a-77` | S2 | Supplementary: JSON for structured state, free text for progress notes, git for state. | "Use structured formats for state data: When tracking structured information (like test results or task status), use JSON or other structured formats" | A6, State management best practices

### S3 Scope and sandbox

- `F-a-78` | S3 | Initializer writes a comprehensive feature requirements file (200+ features), all initially failing. | "These features were all initially marked as “failing” so that later coding agents would have a clear outline of what full functionality looked like." | A2, Feature list
- `F-a-79` | S3 | Coding agents may only change the passes field. | "We prompt coding agents to edit this file only by changing the status of a passes field" | A2, Feature list
- `F-a-80` | S3 | Strongly-worded instruction against removing or editing tests. | "“It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.”" | A2, Feature list
- `F-a-81` | S3 | JSON chosen because the model is less likely to overwrite it than Markdown. | "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." | A2, Feature list
- `F-a-82` | S3 | Feature entry fields shown: category, description, steps, passes. | "\"passes\": false" (example entry with "category", "description", "steps") | A2, Feature list (code sample)
- `F-a-83` | S3 | One feature at a time was critical. | "the next iteration of the coding agent was then asked to work on only one feature at a time." | A2, Incremental progress
- `F-a-84` | S3; S2 | "Clean state" means mergeable code with no unrelated mess. | "By “clean state” we mean the kind of code that would be appropriate for merging to a main branch" | A2, The long-running agent problem
- `F-a-85` | S3 | Quickstart: feature_list.json is the source of truth. | "feature_list.json         # Test cases (source of truth)" | A5, Generated Project Structure
- `F-a-86` | S3 | Quickstart security: OS sandbox, filesystem limited to project dir, bash allowlist. | "File operations restricted to the project directory only" | A5, Security Model
- `F-a-87` | S3 | Quickstart: commands outside the allowlist are blocked by a hook. | "Commands not in the allowlist are blocked by the security hook." | A5, Security Model
- `F-a-88` | S3 | Per-agent Docker container; clone to /workspace, push to /upstream. | "for each agent, a Docker container is spun up with the repo mounted to /upstream." | A4, Running Claude in parallel
- `F-a-89` | S3 | Task locks as text files in current_tasks/, enforced by git sync. | "Claude takes a \"lock\" on a task by writing a text file to current_tasks/" | A4, Running Claude in parallel
- `F-a-90` | S3 | No internet access during development. | "Claude did not have internet access at any point during its development" | A4, Evaluation
- `F-a-91` | S3 | Isolated app instance per git worktree. | "we made the app bootable per git worktree, so Codex could launch and drive one instance per change." | A1, Increasing application legibility
- `F-a-92` | S3 | Enforce invariants, not implementations. | "By enforcing invariants, not micromanaging implementations, we let agents ship fast without undermining the foundation." | A1, Enforcing architecture and taste
- `F-a-93` | S3 | Fixed layers with validated dependency directions, enforced by custom linters and structural tests. | "These constraints are enforced mechanically via custom linters (Codex-generated, of course!) and structural tests." | A1, Enforcing architecture and taste
- `F-a-94` | S3 | Layer order and Providers interface. | "(Types → Config → Repo → Service → Runtime → UI). Cross-cutting concerns (auth, connectors, telemetry, feature flags) enter through a single explicit interface: Providers." | A1, Enforcing architecture and taste
- `F-a-95` | S3 | Strict architecture is an early prerequisite with agents. | "With coding agents, it’s an early prerequisite: the constraints are what allows speed without decay or architectural drift." | A1, Enforcing architecture and taste
- `F-a-96` | S3 | "Taste invariants" enforced by custom lints. | "we statically enforce structured logging, naming conventions for schemas and types, file size limits, and platform-specific reliability requirements with custom lints." | A1, Enforcing architecture and taste
- `F-a-97` | S3; S1 | Lint error messages carry remediation instructions into context. | "Because the lints are custom, we write the error messages to inject remediation instructions into agent context." | A1, Enforcing architecture and taste
- `F-a-98` | S3 | Enforce boundaries centrally, allow autonomy locally. | "enforce boundaries centrally, allow autonomy locally." | A1, Enforcing architecture and taste
- `F-a-99` | S3 | "Golden principles" plus recurring cleanup tasks. | "we started encoding what we call “golden principles” directly into the repository and built a recurring cleanup process." | A1, Entropy and garbage collection
- `F-a-100` | S3 | Background tasks scan for deviations and open refactoring PRs. | "background Codex tasks that scan for deviations, update quality grades, and open targeted refactoring pull requests." | A1, Entropy and garbage collection
- `F-a-101` | S3 | Planner constrains deliverables, not implementation path. | "It seemed smarter to constrain the agents on the deliverables to be produced and let them figure out the path as they worked." | A3, The architecture
- `F-a-102` | S3 | One-feature-at-a-time worked for scope management. | "The one-feature-at-a-time approach from the earlier harness worked well for scope management." | A3, The architecture
- `F-a-103` | S3 | Supplementary: ask before hard-to-reverse or shared-system actions. | "for actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding." | A6, Balancing autonomy and safety (sample prompt)

### S4 Verification

- `F-a-104` | S4 | Unit tests and curl were not enough; the feature did not work end-to-end. | "even do testing with unit tests or curl commands against a development server, but would fail recognize that the feature didn’t work end-to-end." | A2, Testing
- `F-a-105` | S4 | Browser automation and testing "as a human user would" fixed this. | "once explicitly prompted to use browser automation tools and do all testing as a human user would." | A2, Testing
- `F-a-106` | S4 | Testing tools improved performance markedly. | "Providing Claude with these kinds of testing tools dramatically improved performance" | A2, Testing
- `F-a-107` | S4 | Limits: Puppeteer MCP cannot see native alert modals. | "Claude can’t see browser-native alert modals through the Puppeteer MCP, and features relying on these modals tended to be buggier as a result." | A2, Testing
- `F-a-108` | S4 | Only mark features passing after careful testing (single agent self-verifies in A2). | "Self-verify all features. Only mark features as “passing” after careful testing." | A2, Agent failure modes and solutions (table)
- `F-a-109` | S4 | A2 leaves separate testing/QA agents as future work. | "specialized agents like a testing agent, a quality assurance agent, or a code cleanup agent, could do an even better job" | A2, Future work
- `F-a-110` | S4 | Separating doer from judge is a strong lever. | "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue." | A3, Why naive implementations fall short
- `F-a-111` | S4 | Tuning a standalone evaluator to be skeptical is easier than making a generator self-critical. | "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work" | A3, Why naive implementations fall short
- `F-a-112` | S4 | Separation does not remove leniency on its own. | "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs." | A3, Why naive implementations fall short
- `F-a-113` | S4 | Grading criteria turn subjective taste into gradable terms. | "\"Is this design beautiful?\" is hard to answer consistently, but \"does this follow our principles for good design?\" gives Claude something concrete to grade against." | A3, Frontend design: making subjective quality gradable
- `F-a-114` | S4 | Four criteria: design quality, originality, craft, functionality; given to both generator and evaluator. | "I wrote four grading criteria that I gave to both the generator and evaluator agents in their prompts" | A3, Frontend design: making subjective quality gradable
- `F-a-115` | S4 | Evaluator calibrated with few-shot examples. | "I calibrated the evaluator using few-shot examples with detailed score breakdowns." | A3, Frontend design: making subjective quality gradable
- `F-a-116` | S4 | Criteria wording steers the generator. | "The wording of the criteria steered the generator in ways I didn't fully anticipate." | A3, Frontend design: making subjective quality gradable
- `F-a-117` | S4 | Three agents: planner, generator, evaluator. | "a three-agent architecture—planner, generator, and evaluator—that produced rich full-stack applications over multi-hour autonomous coding sessions." | A3, introduction
- `F-a-118` | S4 | Evaluator uses Playwright MCP to click through the app like a user. | "the evaluator used the Playwright MCP to click through the running application the way a user would, testing UI features, API endpoints, and database states." | A3, The architecture
- `F-a-119` | S4 | Each criterion has a hard threshold; failing any fails the sprint. | "Each criterion had a hard threshold, and if any one fell below it, the sprint failed and the generator got detailed feedback on what went wrong." | A3, The architecture
- `F-a-120` | S4 | Sprint contract: agree on "done" before code. | "the generator and evaluator negotiated a sprint contract: agreeing on what \"done\" looked like for that chunk of work before any code was written." | A3, The architecture
- `F-a-121` | S4 | Out of the box Claude is a poor QA agent and talks itself out of issues. | "Out of the box, Claude is a poor QA agent. In early runs, I watched it identify legitimate issues, then talk itself into deciding they weren't a big deal" | A3, Running the harness
- `F-a-122` | S4 | Evaluator tuning loop: read logs, find divergence, update prompt. | "The tuning loop was to read the evaluator's logs, find examples where its judgment diverged from mine, and update the QAs prompt to solve for those issues." | A3, Running the harness
- `F-a-123` | S4 | The evaluator is worth it only beyond what the model does reliably solo. | "The practical implication is that the evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo." | A3, Removing the sprint construct
- `F-a-124` | storyline; S4 | Every harness component encodes an assumption to stress-test. | "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing" | A3, Iterating on the harness
- `F-a-125` | storyline | Remove one component at a time to find what is load-bearing. | "removing one component at a time and reviewing what impact it had on the final result." | A3, Iterating on the harness
- `F-a-126` | storyline | Read traces; re-examine the harness when a new model lands. | "It is always good practice to experiment with the model you're building against, read its traces on realistic problems, and tune its performance" | A3, What comes next
- `F-a-127` | S4 | The verifier must be nearly perfect or the agent solves the wrong problem. | "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem." | A4, Write extremely high-quality tests
- `F-a-128` | S4 | Add tests as new failure modes appear. | "watching for mistakes Claude was making, then designing new tests as I identified those failure modes." | A4, Write extremely high-quality tests
- `F-a-129` | S4 | CI so new commits cannot break existing code. | "I built a continuous integration pipeline and implemented stricter enforcement that allowed Claude to better test its work so that new commits can’t break existing code." | A4, Write extremely high-quality tests
- `F-a-130` | S4 | Write tests for Claude, not for yourself. | "I was writing this test harness for Claude and not for myself" | A4, Put yourself in Claude’s shoes
- `F-a-131` | S4; S2 | Context window pollution: print a few lines, log the rest to a file. | "The test harness should not print thousands of useless bytes. At most, it should print a few lines of output and log all important information to a file" | A4, Put yourself in Claude’s shoes
- `F-a-132` | S4 | Grep-friendly errors and precomputed summaries. | "if there are errors, Claude should write ERROR and put the reason on the same line so grep will find it." | A4, Put yourself in Claude’s shoes
- `F-a-133` | S4 | Time blindness: default --fast sample of 1% or 10%. | "Time blindness: Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress." | A4, Put yourself in Claude’s shoes
- `F-a-134` | S4 | GCC as a known-good compiler oracle to split the kernel task. | "The fix was to use GCC as an online known-good compiler oracle to compare against." | A4, Make parallelism easy
- `F-a-135` | S4; S3 | Specialized agents: dedupe, performance, code quality critique, docs. | "LLM-written code frequently re-implements existing functionality, so I tasked one agent with coalescing any duplicate code it found." | A4, Multiple agent roles
- `F-a-136` | S4 | Effort went into tests, environment and feedback so Claude could orient alone. | "Most of my effort went into designing the environment around Claude—the tests, the environment, the feedback—so that it could orient itself without me." | A4, Lessons from programming with Claude agent teams
- `F-a-137` | S4 | Logs, metrics and traces exposed to Codex via ephemeral per-worktree stack. | "Logs, metrics, and traces are exposed to Codex via a local observability stack that’s ephemeral for any given worktree." | A1, Increasing application legibility
- `F-a-138` | S4 | Query logs with LogQL and metrics with PromQL; performance prompts become tractable. | "Agents can query logs with LogQL and metrics with PromQL." | A1, Increasing application legibility
- `F-a-139` | S4 | Chrome DevTools Protocol wired in for DOM snapshots, screenshots, navigation. | "We also wired the Chrome DevTools Protocol into the agent runtime and created skills for working with DOM snapshots, screenshots, and navigation." | A1, Increasing application legibility
- `F-a-140` | S4 | Agent-to-agent review loop until reviewers are satisfied (Ralph Wiggum Loop). | "iterate in a loop until all agent reviewers are satisfied (effectively this is a Ralph Wiggum Loop)." | A1, Redefining the role of the engineer
- `F-a-141` | S4 | Humans translate feedback into acceptance criteria and validate outcomes. | "We prioritize work, translate user feedback into acceptance criteria, and validate outcomes." | A1, What “agent-generated” actually means
- `F-a-142` | S4 | Minimal blocking merge gates; flakes handled with re-runs (context-specific). | "The repository operates with minimal blocking merge gates." | A1, Throughput changes the merge philosophy
- `F-a-143` | S4 | A1 caveat: the end-to-end autonomy depends on this repo's investment. | "should not be assumed to generalize without similar investment—at least, not yet." | A1, Increasing levels of autonomy
- `F-a-144` | S4 | Supplementary: provide verification tools for UI work. | "Tools that let Claude verify UI work are helpful, such as the computer use tool, the browser use tool, or a browser automation MCP server." | A6, Workflows across multiple context windows
- `F-a-145` | S4; S2 | Supplementary: validation and observable acceptance required in ExecPlans. | "Validation is not optional. Include instructions to run tests, to start the system if applicable, and to observe it doing something useful." | A7, Requirements (PLANS.md)

### Numbers

- `F-a-146` | numbers | A1: zero manually written code, about 1/10th the time. | "We estimate that we built this in about 1/10th the time it would have taken to write the code by hand." | A1, introduction
- `F-a-147` | numbers | A1: about a million lines, ~1,500 PRs, three engineers, 3.5 PRs/engineer/day, now seven engineers. | "roughly 1,500 pull requests have been opened and merged with a small team of just three engineers driving Codex. This translates to an average throughput of 3.5 PRs per engineer per day" | A1, We started with an empty git repository
- `F-a-148` | numbers | A1: single runs of more than six hours. | "We regularly see single Codex runs work on a single task for upwards of six hours (often while the humans are sleeping)." | A1, Increasing application legibility
- `F-a-149` | numbers | A1: Fridays (20%) spent cleaning "AI slop" before automation. | "Our team used to spend every Friday (20% of the week) cleaning up “AI slop.” Unsurprisingly, that didn’t scale." | A1, Entropy and garbage collection
- `F-a-150` | numbers | A1: first commit late August 2025; five months. | "The first commit to an empty repository landed in late August 2025." | A1, We started with an empty git repository
- `F-a-151` | numbers | A2: over 200 features in the claude.ai clone feature list. | "In the claude.ai clone example, this meant over 200 features" | A2, Feature list
- `F-a-152` | numbers | A3: solo 20 min / $9 vs full harness 6 hr / $200; over 20x cost. | "The harness was over 20x more expensive, but the difference in output quality was immediately apparent." | A3, Running the harness (table: Solo 20 min $9; Full harness 6 hr $200)
- `F-a-153` | numbers | A3: 16-feature spec over ten sprints; Sprint 3 had 27 criteria. | "the planner step expanded that prompt into a 16-feature spec spread across ten sprints." / "Sprint 3 alone had 27 criteria covering the level editor" | A3, Running the harness
- `F-a-154` | numbers | A3: frontend loop 5 to 15 iterations, runs up to four hours. | "I ran 5 to 15 iterations per generation" / "Full runs stretched up to four hours." | A3, Frontend design: making subjective quality gradable
- `F-a-155` | numbers | A3: DAW run about 4 hours and $124 (table total 3 hr 50 min, $124.70). | "The run was still lengthy and expensive, at about 4 hours and $124 in token costs." | A3, Results from the updated harness
- `F-a-156` | numbers | A4: 16 agents, nearly 2,000 sessions, $20,000, 100,000 lines, Linux 6.9 on x86, ARM, RISC-V. | "Over nearly 2,000 Claude Code sessions and $20,000 in API costs, the agent team produced a 100,000-line compiler that can build Linux 6.9 on x86, ARM, and RISC-V." | A4, introduction
- `F-a-157` | numbers | A4: two weeks, 2 billion input tokens, 140 million output tokens. | "Opus 4.6 consumed 2 billion input tokens and generated 140 million output tokens, a total cost just under $20,000." | A4, Evaluation
- `F-a-158` | numbers | A4: 99% pass rate on most suites including GCC torture tests. | "has a 99% pass rate on most compiler test suites including the GCC torture test suite." | A4, Evaluation
- `F-a-159` | numbers | A5: 200 test cases; 5-15 minutes per coding session. | "Each coding iteration can take **5-15 minutes** depending on complexity." | A5, Important Timing Expectations
- `F-a-160` | numbers | A7: PLANS.md similar to one that enabled more than seven hours of work. | "very similar to one that has enabled Codex to work for more than seven hours from a single prompt." | A7, introduction

### A5 reference design (own words)

The autonomous-coding README describes a "two-agent pattern (initializer + coding agent)". In session 1 the initializer agent reads an application spec (app_spec.txt), writes feature_list.json with 200 test cases, sets up the project structure and initializes git. Sessions 2 and later run the coding agent, which "picks up where the previous session left off, implements features one by one, and marks them as passing in `feature_list.json`". Each session gets a fresh context window; state lives in feature_list.json (labelled "source of truth") and git commits, with claude-progress.txt as "Session progress notes" and init.sh as the "Environment setup script" that also starts the generated app. The driver auto-continues between sessions after a 3-second delay and can be paused and resumed. The README pairs this flow with a security layer: an OS-level sandbox for bash, file operations limited to the project directory, and a bash command allowlist enforced by a hook. Prompts and templates were not opened or copied.

## Concept inventory

| concept term (source wording) | source id(s) | finding IDs | submodule |
|---|---|---|---|
| harness engineering (title only in A1) / harness design | A1, A3 | F-a-02, F-a-124 | opening |
| "Humans steer. Agents execute." | A1 | F-a-01 | opening |
| underspecified environment | A1 | F-a-03 | opening |
| "anything it can’t access in-context ... effectively doesn’t exist" | A1 | F-a-05, F-a-06, F-a-39 | opening (cause 1), S1 |
| "no memory of what came before" | A2 | F-a-08, F-a-09 | opening (cause 2), S2 |
| self-evaluation; "skew positive when grading their own work" | A3 | F-a-14, F-a-15 | opening (cause 4), S4 |
| "declare the job done" / "declares victory" | A2 | F-a-13 | opening (cause 4) |
| "give Codex a map, not a 1,000-page instruction manual" | A1 | F-a-22 | S1 |
| AGENTS.md as "table of contents" (roughly 100 lines) | A1 | F-a-27, F-a-28 | S1 |
| "system of record" (structured docs/ directory) | A1 | F-a-29, F-a-30 | S1 |
| design-docs, core beliefs, verification status | A1 | F-a-31 | S1 |
| ARCHITECTURE.md / "Architecture documentation" | A1 | F-a-30, F-a-32 | S1 |
| product-specs, references (*-llms.txt), generated/db-schema.md | A1 | F-a-30 | S1 |
| QUALITY_SCORE.md / "A quality document grades..." | A1 | F-a-33 | S1, S4 |
| RELIABILITY.md, SECURITY.md, DESIGN.md, FRONTEND.md, PRODUCT_SENSE.md | A1 | F-a-30 | S1 |
| execution plans (exec-plans/active, completed, tech-debt-tracker.md), PLANS.md | A1, A7 | F-a-34, F-a-35, F-a-45..48 | S1, S2 |
| ExecPlan ("living document", "self-contained") | A7 | F-a-46..48, F-a-145 | S2 |
| progressive disclosure | A1 | F-a-36 | S1 |
| "We enforce this mechanically" (linters, CI jobs) | A1 | F-a-37 | S1 |
| "doc-gardening" agent | A1 | F-a-38 | S1 |
| agent legibility | A1 | F-a-05..07, F-a-39..41 | S1 |
| initializer agent / coding agent | A2, A5 | F-a-49..52 | S2 |
| init.sh | A2, A5, A6 | F-a-50, F-a-61, F-a-64 | S2 |
| claude-progress.txt / progress file | A2, A5 | F-a-50, F-a-53, F-a-56 | S2 |
| git history / git logs | A2, A6 | F-a-53, F-a-57, F-a-59 | S2 |
| "Getting up to speed" / "get its bearings" | A2 | F-a-58..62 | S2 |
| compaction | A2, A3 | F-a-54, F-a-55, F-a-66 | S2 |
| context resets; "structured handoff"; "handoff artifact" | A3 | F-a-65, F-a-68, F-a-69 | S2 |
| "context anxiety" | A3 | F-a-67, F-a-69 | S2 |
| feature list (feature_list.json), "passes" field | A2, A5 | F-a-78..82, F-a-85 | S3 |
| "strongly-worded instructions" | A2 | F-a-79, F-a-80 | S3 |
| one feature at a time / incremental progress | A2, A3 | F-a-83, F-a-102 | S3 |
| "clean state" | A2 | F-a-84, F-a-63 | S3, S2 |
| OS-level Sandbox, Filesystem Restrictions, Bash Allowlist | A5 | F-a-86, F-a-87 | S3 |
| container per agent; no internet access | A4 | F-a-18, F-a-88, F-a-90 | S3 |
| task "lock" in current_tasks/ | A4 | F-a-89 | S3 |
| per-worktree app instance | A1 | F-a-91 | S3, S4 |
| "enforcing invariants, not micromanaging implementations" | A1 | F-a-92 | S3 |
| layers / "permissible edges" / Providers; custom linters and structural tests | A1 | F-a-93..95 | S3 |
| "taste invariants" | A1 | F-a-96, F-a-97 | S3 |
| "golden principles"; garbage collection | A1 | F-a-99, F-a-100 | S3, final |
| end-to-end testing "as a human user would"; Puppeteer MCP | A2 | F-a-104..107 | S4 |
| generator / evaluator; planner | A3 | F-a-110..123 | S4 |
| grading criteria; hard threshold; few-shot calibration | A3 | F-a-113..116, F-a-119 | S4 |
| sprint contract | A3 | F-a-120 | S4 |
| Playwright MCP | A3 | F-a-118 | S4 |
| "task verifier is nearly perfect"; "extremely high-quality tests" | A4 | F-a-127, F-a-128 | S4 |
| continuous integration pipeline | A4 | F-a-129 | S4 |
| "Context window pollution"; "Time blindness" | A4 | F-a-131..133 | S4 |
| "known-good compiler oracle" | A4 | F-a-134 | S4 |
| observability stack (logs, metrics, traces; LogQL, PromQL) | A1 | F-a-137, F-a-138 | S4 |
| Ralph Wiggum Loop | A1, A3, A4 ("Ralph-loop") | F-a-140 | S4 |
| "every component in a harness encodes an assumption" | A3 | F-a-124, F-a-125 | final |

## Terms the course must NOT coin

| term in brief | used by sources? | source wording to use instead |
|---|---|---|
| "Instructions" as a harness part name | No | A1: "repository knowledge", "knowledge base", "system of record", "map"; A2/A3: "prompt" |
| "State and session lifecycle" | "lifecycle" only as "software development lifecycle" | A2: "sessions", "context windows", "Getting up to speed"; A3: "context resets", "structured handoff" |
| "Scope and sandbox" | "sandbox" only in A5 ("OS-level Sandbox"); "scope" only as "scope management" / "under-scoped" (A3) | A1: "strict boundaries", "invariants", "constraints"; A4: "container"; A5: "Filesystem Restrictions", "Bash Allowlist" |
| "Verification" as a part name | Partly: "verifying features end-to-end" (A2), "task verifier" (A4), "verification headroom" (A3) | A2: "Testing"; A3: "evaluator", "QA"; A4: "tests", "task verifier" |
| "self-evaluation bias" | "bias" not used | A3: "self-evaluation", "skew positive", "leniency", "inclined to be generous" |
| "initializer session" | No | A2/A5: "initializer agent" (A2 footnote: same harness, different initial prompt) |
| "init script" | No | "init.sh script" |
| "session start routine" | No | A2: "Getting up to speed", "get its bearings" |
| "flip a status field" | No | A2: "edit this file only by changing the status of a passes field" |
| "git history as memory" | "memory" appears only in "no memory" | A2: "the claude-progress.txt file alongside the git history"; A6: "Use git for state tracking" |
| "handoff" (generic) | Yes in A3 only | A3: "structured handoff", "handoff artifact"; A2: "leaving clear artifacts for the next session" |
| "tests as oracle" | No | A4: "GCC as an online known-good compiler oracle" (GCC is the oracle, not the tests) |
| "context pollution" | No | A4: "Context window pollution" |
| "time-blindness" (hyphenated) | No | A4: "Time blindness" |
| "CI preventing regressions" | No | A4: "continuous integration pipeline ... so that new commits can’t break existing code" |
| "high-quality tests" | Close | A4 heading: "Write extremely high-quality tests" |
| "quality score" docs | File name only | A1: "QUALITY_SCORE.md"; "A quality document grades each product domain and architectural layer" |
| "in-repo exec plans" | Close | A1: "execution plans", "exec-plans/" (active/, completed/); A7: "ExecPlan" |
| "what the agent can't see doesn't exist" | Paraphrase | A1: "anything it can’t access in-context while running effectively doesn’t exist" |
| "guardrails" | Once in A1 | A1: "tools, guardrails, documentation" (list only; not defined) |
| "rubric" | No | A3: "grading criteria" |
| "source of truth" | A5 only; A1 has "sources of truth" | A5: "Test cases (source of truth)"; A1: "pointers to deeper sources of truth" |

## Open gaps

1. A1 never defines "harness engineering" in its body; the word "harness" appears only in the title and once as "Evaluation harnesses". Any definition the course gives must come from elsewhere or be marked as course wording.
2. Cause 3 ("nothing limits what the agent changes/reaches") has no single sentence in the five primary sources that states it as a cause. Supporting evidence is indirect: A4's container warning and pkill incident (F-a-18, F-a-19), A1's drift from copied patterns (F-a-20), A2's JSON-over-Markdown overwrite risk (F-a-81). The most direct statement is in the supplementary doc A6 (F-a-21). A2 and A3 do not discuss sandboxing or permissions; only A5 (README) and A4 do.
3. A6 is a living docs page; its current text names Claude Sonnet 5 and Opus 4.6, so it has been revised since A2 cited it (Nov 2025). The quotes are from the 2026-10-16 version.
4. A7 is marked "This recipe is archived and may reference outdated models or APIs." The PLANS.md content was read only for definitions; its template was not copied.
5. A5: only the README was read, per the brief. The README does not state that the initializer writes init.sh or claude-progress.txt; it lists them in "Generated Project Structure". Prompt files were deliberately not opened, so exact prompt behavior is unverified.
6. A2 has an internal naming inconsistency: the example transcript reads both "feature_list.json" and "tests.json". A6 uses "tests.json" and a "status" field; A2 and A5 use "feature_list.json" and "passes".
7. Images/diagrams (A1 layer diagram, A2 screenshots, A3 videos) were not inspected; only their text and captions.
8. A1 page shows "Loading…" in one area; the article body was complete in the downloaded HTML, but any interactive embeds were not captured.

## Corrections to the brief

1. "~100 lines": confirmed. Exact wording: "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map". Use "roughly 100 lines", "map", "table of contents".
2. ARCHITECTURE.md sits at the repository root next to AGENTS.md, not inside docs/. PLANS.md, QUALITY_SCORE.md, RELIABILITY.md, SECURITY.md, DESIGN.md, FRONTEND.md, PRODUCT_SENSE.md are inside docs/. The tree also has generated/db-schema.md and exec-plans/tech-debt-tracker.md, which the brief omits.
3. "references (e.g. *-llms.txt)": confirmed (design-system-reference-llms.txt, nixpacks-llms.txt, uv-llms.txt). A1 does not explain these files in prose.
4. "agent may only flip a status field": A2 says agents edit the file "only by changing the status of a passes field". The field is "passes" (boolean), not "status". "status" appears only in A6's tests.json example. The "tests" in the strongly-worded instruction are the feature-list entries, not unit test files.
5. "Initializer session vs coding-agent sessions": A2 calls them agents, and footnote 1 says they differ only in initial user prompt; system prompt, tools and harness are identical.
6. "Separate evaluator agent" belongs to A3, not A2. A2 uses a single coding agent that must "Self-verify all features" and lists testing/QA agents as future work.
7. "Puppeteer/Playwright MCP": A2 uses the Puppeteer MCP for the coding agent's own testing; A3 gives the Playwright MCP to the evaluator. A1 uses the Chrome DevTools Protocol, not MCP.
8. "Context resets vs compaction": A3 shows resets were needed for Sonnet 4.5 ("context anxiety") but dropped for Opus 4.5, which ran as "one continuous session" with automatic compaction. Teach resets as model-dependent, not universal. A2 says only "compaction isn’t sufficient"; it does not use the term "context reset".
9. "Sprint contracts": A3 later removed the sprint construct for Opus 4.6 and moved the evaluator to "a single pass at the end of the run". Sprint contracts are a dated design point, not a standing recommendation. A3 also says the evaluator "is not a fixed yes-or-no decision".
10. "Tests as oracle (C compiler: GCC torture tests...)": the oracle in A4 is GCC itself ("known-good compiler oracle"), used to split the Linux kernel build. The GCC torture test suite is cited as an evaluation result (99% pass rate), not as the steering mechanism.
11. "Observability/traces given to agents": supported by A1 (logs, metrics, traces; LogQL/PromQL). A3's "read its traces" is advice to the harness builder, not a tool given to the agent.
12. "Strongly-worded instructions": confirmed wording in A2. A6 repeats the same sentence as a reminder about tests.
13. "Mechanical enforcement of docs": confirmed ("We enforce this mechanically"), and A1 also uses custom lint error messages to "inject remediation instructions into agent context", which the brief does not mention.
14. A1 caveat the course should carry: its autonomy results "should not be assumed to generalize without similar investment". A1's "minimal blocking merge gates" is described as a high-throughput tradeoff that "would be irresponsible in a low-throughput environment".
