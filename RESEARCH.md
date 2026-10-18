# RESEARCH

Research record for Module 1, "Harness Engineering for Coding Agents". Product name: `shipharness` (renamed from the working name `shipproof`; see G-18). Every concept, term, and
number used in concepts.md, READMEs, skills, slides, and reading must trace to an entry here.

- Research milestone: M1, completed 2026-10-16. Access date for every source: 2026-10-16.
- Method: five research streams (R-a to R-e). Each stream's full notes, with every finding ID and
  verbatim quote, are in [research/notes/](research/notes/). This file consolidates them.
- Clean-room statement: only the primary sources listed in the brief (§1.9) and official vendor
  documentation were read. No third-party course repositories, course skill packs, or tutorials were
  opened. The Anthropic autonomous-coding quickstart was read at README level only, as a reference
  design; its prompts and templates were not opened.
- Quote policy: quotes are verbatim, at most 30 words, and keep the source's punctuation. R-a quotes
  were checked by script against locally downloaded source text. R-b vendor-doc quotes (Claude Code,
  Codex, Cursor) came through a summarising fetch tool and must be re-copied from the live page before
  they appear in course material as verbatim (see Open gaps G-11).

Finding IDs (`F-a-NN`, `F-b-NN`) point to entries in the notes files.

---

## 1. Source register

### 1.1 Teaching sources (§1.9)

| ID | Title | URL | Author / org | Date | Summary |
|---|---|---|---|---|---|
| A1 | Harness engineering: leveraging Codex in an agent-first world | https://openai.com/index/harness-engineering/ | Ryan Lopopolo, OpenAI | 2026-02-11 | Five months building an internal product where Codex wrote every line. Short AGENTS.md as a map into a structured docs/ directory; app UI, logs, and metrics made legible to the agent; architecture and "taste invariants" enforced by custom linters; recurring cleanup by background agents. |
| A2 | Effective harnesses for long-running agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Justin Young, Anthropic | 2025-11-26 | Initializer agent sets up init.sh, a progress file, a JSON feature list, and a first commit; a coding agent then works one feature per session and leaves a clean state. Session-start routine, end-to-end browser testing, table of four failure modes. |
| A3 | Harness design for long-running application development | https://www.anthropic.com/engineering/harness-design-long-running-apps | Prithvi Rajasekaran, Anthropic | 2026-03-24 | Generator/evaluator loop with grading criteria, then planner/generator/evaluator for full-stack apps with sprint contracts. Context resets vs compaction, self-evaluation leniency, cost and duration numbers, later removal of sprints for Opus 4.6. |
| A4 | Building a C compiler with a team of parallel Claudes | https://www.anthropic.com/engineering/building-c-compiler | Nicholas Carlini, Anthropic | 2026-02-05 | 16 parallel agents, nearly 2,000 sessions, about $20,000, a 100,000-line Rust C compiler. Lessons: extremely high-quality tests, CI against regressions, test output designed for the model, task locks, GCC as a known-good oracle, specialised roles. |
| A5 | Autonomous Coding Agent Demo (README) | https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding | Anthropic | README committed 2025-11-26 | Reference implementation of the A2 pattern: initializer in session 1, coding agent in sessions 2+, feature_list.json as "source of truth", init.sh, claude-progress.txt, fresh context per session, three-layer security model (OS sandbox, filesystem restriction, bash allowlist). README only. |
| A6 | Prompting best practices (multi-context-window and state-management sections) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#workflows-across-multiple-context-windows | Anthropic, Claude docs | living page | Official doc linked from A2. Multi-window recipe (different first-window prompt, tests in structured format, init.sh, fresh window vs compaction, git for state) and the autonomy/safety section. Supplementary; text has changed since A2 cited it. |
| A7 | Using PLANS.md for multi-hour problem solving | https://cookbook.openai.com/articles/codex_exec_plans | Aaron Friel, OpenAI Cookbook | 2025-10-07 (archived) | Official recipe linked from A1 as "execution plans". Defines the ExecPlan: a self-contained living design document governed by PLANS.md, with required Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective sections. Supplementary. |
| B1 | Agent Skills Specification | https://agentskills.io/specification | Agent Skills project | undated | Normative format: skill directory, SKILL.md frontmatter fields and constraints, optional directories, progressive disclosure, file references, validation with skills-ref. |
| B2 | What are skills? | https://agentskills.io/home | Agent Skills project | undated | Three progressive-disclosure stages: Discovery, Activation, Execution. |
| B3 | How to add skills support to your agent | https://agentskills.io/client-implementation/adding-skills-support.md | Agent Skills project | undated | Client guidance: three-tier loading, `.agents/skills/` cross-client convention, collision precedence, lenient validation. |
| B4 / B5 / B6 | agentskills repo; skills-ref source and README; skills-ref on PyPI | https://github.com/agentskills/agentskills ; https://pypi.org/project/skills-ref/ | Agent Skills project (skills-ref by Keith Lazuka, Anthropic) | skills-ref 0.1.1, 2026-01-10 | Reference validator library and CLI. README: "for demonstration purposes only". Apache-2.0, Python >=3.11. |
| B7 | Extend Claude with skills | https://code.claude.com/docs/en/skills | Anthropic | living page | Claude Code skill locations and precedence; follows the Agent Skills standard; extension fields. |
| B8 | Build skills (Codex) | https://learn.chatgpt.com/docs/build-skills (redirect from https://developers.openai.com/codex/skills) | OpenAI | living page | Codex skill discovery under `.agents/skills` and `/etc/codex/skills`. |
| B9 / B10 | Agent Skills (Cursor docs); Cursor 2.4 changelog | https://cursor.com/docs/context/skills ; https://cursor.com/changelog/2-4 | Anysphere | 2026-01-22 (2.4) | Cursor reads `.agents/skills/`, `.cursor/skills/`, and the Claude and Codex directories. |
| B11 | Automated Unit Test Improvement using Large Language Models at Meta (TestGen-LLM) | https://arxiv.org/abs/2402.09171 | Alshahwan et al., Meta | 2024-02-14; FSE '24 | Keeps only LLM-generated tests that build, pass reliably (five executions), and add line coverage. Evaluation and deployment results at Instagram and Facebook. |
| B12 | Mutation-Guided LLM-based Test Generation at Meta (ACH) | https://arxiv.org/abs/2501.12862 | Foster et al., Meta | 2025-01-22; submitted to FSE 2025 Industry Track | Issue-specific mutants (privacy faults), LLM equivalence detector, modified TestGen-LLM writes tests that pass on the original and fail on the mutant. |
| B13 / B14 | SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents; WecoAI/SpecBench repo | https://arxiv.org/abs/2605.21384 ; https://github.com/WecoAI/SpecBench | Zhao, Srikanth, Wu, Jiang (Weco AI) | v1 2026-05-20, v2 2026-09-09; preprint | 30 systems tasks, each with a spec, visible validation tests that check features in isolation, and held-out tests that compose them. The gap between validation and held-out pass rates grows with code size and is larger for smaller models. |

B15 (Spec-Bench, arXiv 2401.07851) is a speculative-decoding benchmark with a similar name. It is
unrelated and must not be cited.

### 1.2 Technical references (official docs; used for build decisions, not for teaching concepts)

| Group | IDs | Main URLs |
|---|---|---|
| OpenAI API | C1-C19 | https://developers.openai.com/api/docs/models/gpt-6-luna ; /api/docs/pricing ; /api/docs/guides/prompt-caching ; /guides/function-calling ; /guides/structured-outputs ; /guides/reasoning ; /guides/conversation-state ; /guides/rate-limits ; /guides/error-codes ; /guides/flex-processing ; /guides/batch ; /api/reference/resources/responses/methods/create ; https://pypi.org/project/openai/ |
| LangSmith | D1-D20 | https://www.langchain.com/pricing ; https://docs.langchain.com/langsmith/administration-overview ; /billing ; /observability-concepts ; /evaluation-concepts ; /repetition ; /multiple-scores ; /summary ; /compare-experiment-results ; /evaluate-pairwise ; /manage-datasets-programmatically ; /fetch-perf-metrics-experiment ; /export-traces ; /smithdb-sdk-migration-query-runs ; /observability-quickstart ; /cost-tracking ; https://pypi.org/project/langsmith/ |
| Codex sandbox | D21-D23 | https://developers.openai.com/codex/agent-approvals-security ; /codex/concepts/sandboxing ; /codex/config-reference |
| Docker and alternatives | D24-D36 | https://docs.docker.com/reference/cli/docker/container/run/ ; /engine/containers/run/ ; /engine/containers/resource_constraints/ ; /engine/network/drivers/none/ ; /reference/cli/docker/container/stats/ ; /desktop/features/wsl/ ; https://podman.io/docs/installation ; https://github.com/abiosoft/colima |
| Marp, Vale | D37-D44 | https://github.com/marp-team/marp-cli ; https://marpit.marp.app/usage?id=presenter-notes ; https://vale.sh/docs/checks/existence ; https://docs.vale.sh/topics/cli.md |
| Packages, libraries, name check | E1-E22 | https://pypi.org/pypi/{package}/json ; https://github.com/mahmoud/boltons/tree/26.2.0 ; https://github.com/pallets-eco/wtforms/tree/3.2.2 ; https://registry.npmjs.org/htmx.org ; https://htmx.org/extensions/sse/ ; https://pypi.org/project/mutmut/3.8.0/ ; https://pypi.org/project/shipproof/ |

Full per-source rows (title, URL, summary) are in the notes files R-c, R-d, and R-e.

---

## 2. Storyline evidence: why agents fail (§0.1)

| Cause (brief) | Strongest source sentence | ID | Status |
|---|---|---|---|
| 1. The agent cannot follow rules it cannot see in its context | "From the agent’s point of view, anything it can’t access in-context while running effectively doesn’t exist." (A1) | F-a-05; also F-a-06, F-a-07, F-a-23 | Direct |
| 2. Each new session starts without memory of the previous one | "each new session begins with no memory of what came before." (A2) | F-a-08; also F-a-09, F-a-10, F-a-12 | Direct |
| 3. Agents copy existing patterns, including bad ones, and can take actions that are hard to undo | "(Run this in a container, not your actual machine)." (A4); "in one instance, I did see Claude pkill -9 bash on accident, thus killing itself and ending the loop." (A4); "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." (A1); A5 security model: "File operations restricted to the project directory only" | F-a-18, F-a-19, F-a-20, F-a-86; supplementary F-a-21 (A6) | Indirect; see G-1 |
| 4. The agent judges its own work, and its visible tests miss what held-out tests catch | "agents reliably skew positive when grading their own work." (A3); "a later agent instance would look around, see that progress had been made, and declare the job done." (A2); "while every frontier agent saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout suites." (B13) | F-a-13, F-a-14, F-a-15, F-a-16, F-a-17; F-b-45, F-b-50 | Direct |

Notes on cause 4:
- SpecBench's main finding for Module 1 is the compositional one: "deliberate exploits are rare,
  while compositional failures account for a much larger fraction of reward hacking behavior"
  (F-b-50). The course uses SpecBench for "visible tests miss what held-out tests catch". Defenses
  against agents that deliberately game checks are Module 2.
- SpecBench calls the visible suite "validation tests" and the hidden suite "held-out tests". The
  course uses "visible tests" as the plain label and cites SpecBench's terms where it quotes the paper.

Supporting framing for the opening (A1): "Humans steer. Agents execute." (F-a-01); "Early progress was
slower than we expected, not because Codex was incapable, but because the environment was
underspecified." (F-a-03). A1 never defines "harness engineering"; the phrase appears only in the
title (G-2).

---

## 3. Concept inventory (§2.7-2.8 coverage)

Status key: **Direct** = the source states the concept. **Composite** = the course mechanism combines
two or more source statements; the course must cite each part and must not present the combination as
a source's named idea. **Course mechanism** = experimental or tooling machinery with no harness-source
term; it is described plainly and not given a concept name.

### 3.1 S1 Instructions: what the agent knows

| Brief term | Source wording to use | Source / finding | Status |
|---|---|---|---|
| Routing AGENTS.md (~100 lines) | "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map"; "we treat it as the table of contents" | A1; F-a-27, F-a-28, F-a-22 | Direct. Use "map" and "table of contents", not "routing" |
| Why not one big file | "A giant instruction file crowds out the task, the code, and the relevant docs"; "Too much guidance becomes non-guidance." | A1; F-a-23, F-a-24, F-a-25, F-a-26 | Direct |
| docs/ as system of record | "structured docs/ directory treated as the system of record" | A1; F-a-29, F-a-30 | Direct |
| ARCHITECTURE.md | "Architecture documentation provides a top-level map of domains and package layering." File sits at repo root. | A1; F-a-30, F-a-32 | Direct |
| SECURITY.md, RELIABILITY.md, PLANS.md, design-docs/, product-specs/, references/*-llms.txt | File names from A1's layout figure | A1; F-a-30, F-a-31 | Direct (names only; A1 does not explain llms.txt files) |
| QUALITY_SCORE.md | "A quality document grades each product domain and architectural layer, tracking gaps over time." | A1; F-a-33 | Direct |
| Progressive disclosure (docs) | "agents start with a small, stable entry point and are taught where to look next" | A1; F-a-36 | Direct |
| Docs checked mechanically | "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly." | A1; F-a-37, F-a-38 | Direct (basis for A1 assignment's link/coverage checker) |
| Lint messages that teach | "we write the error messages to inject remediation instructions into agent context" | A1; F-a-97 | Direct |
| Skills (format) | SKILL.md with YAML frontmatter; `name`, `description` required | B1; F-b-01 to F-b-04 | Direct |
| Progressive disclosure (skills) | "Metadata (~100 tokens)" at startup; "Instructions (< 5000 tokens recommended)" on activation; "Resources (as needed)" | B1, B2; F-b-05, F-b-06 | Direct |
| Legacy pattern copied by the agent (trap) | "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." | A1; F-a-20 | Direct (justifies the legacy /v1 handler trap) |

### 3.2 S2 State and session lifecycle: what the agent remembers

| Brief term | Source wording to use | Source / finding | Status |
|---|---|---|---|
| Initializer vs coding-agent sessions | "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session"; they differ only in "different initial user prompts" | A2, A5; F-a-49, F-a-52 | Direct. Say "initializer agent", not "initializer session" |
| init.sh | "an init.sh script that can run the development server" | A2, A5; F-a-50, F-a-61, F-a-64 | Direct |
| progress.md | A2/A5 name the file claude-progress.txt, "a log of what agents have done"; A6: free text for progress notes | A2; F-a-50, F-a-53, F-a-56; A6 F-a-77 | Direct (file name differs; course uses progress.md and says so) |
| Git history as state | "the claude-progress.txt file alongside the git history"; "use git to revert bad code changes" | A2; F-a-53, F-a-57 | Direct |
| Session start routine | A2 heading "Getting up to speed": run pwd, read git logs and progress files, read the feature list and pick the highest-priority unfinished feature, run a basic end-to-end test | A2; F-a-58 to F-a-62 | Direct. Use "Getting up to speed" |
| Session end | "End the session by writing a git commit and progress update." | A2; F-a-63 | Direct |
| Exec plans active → completed | "execution plans with progress and decision logs that are checked into the repository"; exec-plans/active, completed | A1, A7; F-a-34, F-a-35, F-a-45 to F-a-48 | Direct |
| session-handoff.md | "a structured handoff that carries the previous agent's state and the next steps" | A3; F-a-65 | Direct ("structured handoff", "handoff artifact") |
| Forced session stop | A3 "context reset": "clearing the context window entirely and starting a fresh agent, combined with a structured handoff" | A3; F-a-65 to F-a-69 | Composite. The forced stop is a course mechanism (session turn budget smaller than the feature, §1.8 allowed technique) that produces an A3 context reset. Teach resets as model-dependent: A3 dropped them for Opus 4.5 |
| Compaction is not enough | "However, compaction isn’t sufficient." | A2; F-a-54, F-a-55 | Direct |

### 3.3 S3 Scope and sandbox: what the agent is allowed to change and reach

| Brief term | Source wording to use | Source / finding | Status |
|---|---|---|---|
| feature_list.json as the only scope | "feature_list.json # Test cases (source of truth)"; JSON because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files" | A2, A5; F-a-78, F-a-81, F-a-85 | Direct |
| Status field | A2's field is `passes` (boolean): "edit this file only by changing the status of a passes field" | A2; F-a-79, F-a-82 | Direct. Field is `passes`, not `status`. `evidence` and `testedAt` are course additions (see G-6) |
| Strongly-worded instruction | "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." | A2; F-a-80 | Direct. "tests" here means feature-list entries |
| One feature per session | "work on only one feature at a time"; A3: "worked well for scope management" | A2, A3; F-a-83, F-a-102 | Direct |
| Allowed paths per phase | A5: "File operations restricted to the project directory only"; A1: "enforce boundaries centrally, allow autonomy locally"; "By enforcing invariants, not micromanaging implementations" | A5, A1; F-a-86, F-a-92, F-a-98 | Composite. Per-phase path lists are the course's application of these statements |
| Out-of-scope edits reverted (BLOCKED) | A5: "Commands not in the allowlist are blocked by the security hook."; A2: git used "to revert bad code changes" | A5, A2; F-a-87, F-a-57 | Composite |
| Only the harness sets `passing` | A2: agent sets `passes` after "careful testing" (F-a-108); A3: "Separating the agent doing the work from the agent judging it proves to be a strong lever" | A2, A3; F-a-108, F-a-110 | Composite. A2 lets the agent set the field; the course moves that decision to the harness, citing A3 |
| Clean state | "By “clean state” we mean the kind of code that would be appropriate for merging to a main branch" | A2; F-a-84 | Direct |
| Layering enforced by code | "These constraints are enforced mechanically via custom linters ... and structural tests." | A1; F-a-93, F-a-94, F-a-95 | Direct (basis for R6) |
| Sandbox: container, no network | "for each agent, a Docker container is spun up"; "Claude did not have internet access at any point during its development" | A4; F-a-88, F-a-90, F-a-18 | Direct |
| Sandbox: OS-level layers | A5 security model: OS-level sandbox, filesystem restrictions, bash allowlist | A5; F-a-86, F-a-87 | Direct |
| Sandbox: modes and approvals in another agent | Codex `read-only`, `workspace-write`, `danger-full-access`; approvals `on-request`, `never`, `granular`; "By default, the agent runs with network access turned off." | D21-D23 | Direct (official docs) |
| Sandbox: Docker limits | `--network none` ("only the loopback device is created"), `--memory`, `--cpus`, `--pids-limit`, `--read-only`, `--user`, `--cap-drop ALL`, `--security-opt no-new-privileges`; `State.OOMKilled` | D24-D30 | Direct (official docs) |

### 3.4 S4 Verification: what proves the work is done

| Brief term | Source wording to use | Source / finding | Status |
|---|---|---|---|
| Test filters (§2.3) | "progressively demanding semantic filters": builds; "does not pass on first execution" discarded; "a test that does not pass on every one of five executions is deemed flaky"; "Any test that does not improve coverage is also discarded." | B11; F-b-16 to F-b-22 | Direct for filters 1-3 |
| Filter 3, mutant branch | ACH: "construct mutants that denote faults that are both relevant to the issue of concern and also currently not caught (unkilled) by any existing test case"; "Hardening: The new tests catch faults that no existing test can catch" | B12; F-b-29, F-b-32, F-b-34, F-b-40 | Direct |
| Filter 4 (real assertions, no mocking of the unit under test) | None found in B11/B12 | — | Course mechanism; G-7 |
| Filter 5 (no source change during test phase) | B11: existing tests kept, "guaranteeing there will be no regression, by construction"; A2: "It is unacceptable to remove or edit tests" | B11, A2; F-b-22, F-a-80 | Composite; G-7 |
| "Assured" tests | Assured LLMSE: survivors "are thus guaranteed to improve the existing test class, and to provide reliable regression test signal" | B11, B12; F-b-21, F-b-30 | Direct |
| Targeted mutants on risky lines | Issue-specific mutants (ACH, privacy) | B12; F-b-29, F-b-33 | Direct (concept). Implementation is a hand-written mutant runner; see §4.7 |
| Hidden tests | "held-out tests that compose those same features to simulate real-world usage"; "never shown to the agent" | B13, B14; F-b-42, F-b-43, F-b-44 | Direct |
| PASS_TO_PASS (brief term) | A4: "new commits can’t break existing code"; B11: "no regression, by construction" | A4, B11; F-a-129, F-b-22 | Composite. Taught as "existing tests keep passing"; internal key `regression` (G-8, closed) |
| House rules R1-R7 | A1: "golden principles" encoded in the repo; "taste invariants" enforced "with custom lints"; "enforcing invariants" | A1; F-a-92, F-a-96, F-a-99 | Composite. "House rules" is the course's label for A1's invariants; G-9 |
| Blinded reviewer | A3: separate evaluator; "tuning a standalone evaluator to be skeptical turns out to be far more tractable"; "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs" | A3; F-a-110, F-a-111, F-a-112 | Direct for separate evaluator. "Blinded" is A/B-design machinery (§1.8), not a source term |
| Reviewer rubric | A3 says "grading criteria", with "a hard threshold" per criterion and few-shot calibration | A3; F-a-113 to F-a-116, F-a-119 | Direct. Use "grading criteria", not "rubric" (G-10) |
| Playwright board checks | A3: evaluator "used the Playwright MCP to click through the running application the way a user would"; A2: test "as a human user would" | A3, A2; F-a-118, F-a-105 | Direct |
| Clean-state gate | A2 "clean state" (F-a-84) plus A4 "task verifier is nearly perfect, otherwise Claude will solve the wrong problem" | A2, A4; F-a-84, F-a-127 | Composite |
| Traces, first wrong turn | A3: "read its traces on realistic problems"; A1: logs, metrics, and traces exposed to the agent | A3, A1; F-a-126, F-a-137 | Direct (A3 is advice to the harness builder) |
| Test output for the model | "Context window pollution"; "Time blindness"; "write ERROR and put the reason on the same line" | A4; F-a-131 to F-a-133 | Direct (applies to `run_visible_tests` output) |
| Agents' visible tests pass but job not done | "it is easy to see tests pass and assume the job is done, when this is rarely the case." | A4; F-a-17 | Direct |
| Ablation (leave one layer out) | "removing one component at a time and reviewing what impact it had on the final result" | A3; F-a-125, F-a-124 | Direct (justifies `LAYERS=-<layer>`) |

### 3.5 Skills (§2.8)

| Skill | Sources | Status |
|---|---|---|
| `harness-setup` | A1 (map, docs layout, plans, quality doc), A2 (init.sh, progress file, feature list, clean state, getting up to speed), A3 (structured handoff, separate evaluator), A7 (ExecPlan sections), B1 (format) | Direct for each template; templates written from these sources, not copied |
| `assured-tests` | B11 (filters, five executions, line coverage), B12 (mutant-guided hardening, equivalence), B1 | Direct |
| `house-rules` | A1 (golden principles, taste invariants, custom lints with remediation messages, structural tests), B1 | Composite (label "house rules", G-9) |
| `skill-template` | B1 (frontmatter, directories, size guidance, references one level deep), B3 (`.agents/skills/` convention), B7-B9 (install paths) | Direct |

Coverage result: every concept in §2.7-2.8 has at least one §1.9 source. Items marked Composite or
Course mechanism carry the citation rules above and are listed in Open gaps.

---

## 4. Verified technical facts

### 4.1 Wording rules for course material

| Avoid (brief or common wording) | Use (source wording) |
|---|---|
| routing AGENTS.md | AGENTS.md as a "map" / "table of contents" (A1) |
| initializer session; init script | initializer agent; init.sh script (A2) |
| session start routine | "Getting up to speed" (A2) |
| flip a status field | edit the feature list "only by changing the status of a passes field" (A2) |
| handoff (generic) | "structured handoff", "handoff artifact" (A3) |
| rubric | "grading criteria" (A3) |
| self-evaluation bias | self-evaluation; "skew positive when grading their own work" (A3) |
| tests as oracle | GCC as a "known-good compiler oracle" (A4); the oracle is GCC, not the tests |
| context pollution; time-blindness | "Context window pollution"; "Time blindness" (A4) |
| visible tests vs hidden tests (when quoting SpecBench) | "validation tests" vs "held-out tests"; "reward hacking gap" (B13) |
| "what the agent can't see doesn't exist" | "anything it can’t access in-context while running effectively doesn’t exist" (A1) |

Section titles (S1 Instructions, S2 State and session lifecycle, S3 Scope and sandbox, S4
Verification) are fixed course labels (§0.2). They organise the module and are not presented as
source terms; the concepts inside each section use the wording above.

### 4.2 OpenAI (C1-C19)

| Item | Value | Source |
|---|---|---|
| Agent model | `gpt-6-luna` exists. $0.10 input, $0.01 cached input, **$0.125 cache write**, $0.50 output per 1M tokens. 1,050,000 context (922,000 max input), 128,000 max output. Efforts: none, low, medium (default), high, xhigh, max. Function calling, strict structured outputs, prompt caching on Responses | C1, C2 |
| Reviewer candidates | `gpt-5.6-luna` $0.20 / $0.02 / $0.25 write / $1.20; `gpt-6.1-sol` $2.00 / $0.10 / $2.50 / $10.00; `gpt-6-luna` as above | C16, C18, C2 |
| Unsuitable | `gpt-6-astra` (docs default, $10/$50); `gpt-5.4-mini` and `gpt-6.1-sol` exceed $0.20 per agent run | C2, C19 |
| Usage fields | `usage.input_tokens`, `usage.input_tokens_details.cached_tokens`, `usage.input_tokens_details.cache_write_tokens`, `usage.output_tokens`, `usage.output_tokens_details.reasoning_tokens`, `usage.total_tokens` | C13 |
| Cost formula | uncached = input − cached − cache_write; cost = (uncached·P_in + cached·P_cached + write·P_write + output·P_out) / 1e6 | C4 |
| Tool shape (Responses) | `{"type":"function","name","description","parameters","strict":true}`; strict needs `additionalProperties:false` and all properties required (optional = union with null) | C5, C13 |
| Tool loop | Output items `function_call` (`call_id`, `name`, `arguments` JSON string); reply with `{"type":"function_call_output","call_id","output"}`; pass reasoning items back; `parallel_tool_calls`, `tool_choice`, `max_output_tokens` (includes reasoning; overflow gives `status="incomplete"`) | C5, C7 |
| State | `store` defaults true. Stateless replay (`store=false`) returns encrypted reasoning by default. `previous_response_id` still bills all prior input | C7, C8, C13 |
| Structured outputs | `text={"format":{"type":"json_schema","name","schema","strict":true}}`; SDK `client.responses.parse(text_format=Model)` → `output_parsed`; check for refusal and incomplete | C6 |
| Prompt caching | Automatic; minimum 1,024 tokens; whole rendered prefix must match (tools, `text.format`, effort are part of it); `prompt_cache_options` (`mode` implicit/explicit, `ttl` "30m"); `prompt_cache_retention` deprecated for GPT-5.6+; cache write 1.25x input; cached tokens count toward TPM | C4 |
| Rate limits | Tiers Free / Build / Launch / Grow. gpt-6-luna: Build 5,000 RPM / 2,000,000 TPM; Launch 10,000 / 10,000,000. No Free row on the luna page. Billing 429s (`insufficient_quota`, `credit_balance_exhausted`, spend limits) must abort, not retry | C1, C9, C10 |
| Batch / flex | Both 50% off. Batch cannot run multi-turn agents. Flex is synchronous, slower, can return 429 (not charged); function calling not explicitly confirmed | C11, C12 |
| SDK | `openai` 3.31.0 (2026-10-14), Python >=3.10. 3.0.0 (2026-08-12) breaking: HTTPX2 replaces httpx | C14, C15 |
| Modelled cost per agent run | 25 turns, 8K prefix, 2.3K added per turn, gpt-6-luna medium: $0.032 (ideal cache hits), $0.105 (no caching), $0.128 (all lookups miss). High effort: $0.057-$0.153. Model estimate only; M6 measures the real value | R-c cost section |
| Modelled cost per review | gpt-6-luna high ~$0.003; gpt-5.6-luna medium ~$0.006; gpt-6.1-sol low $0.030-$0.038 (fits $0.04 only with ≤10K input and ≤1,500 output) | R-c cost section |

### 4.3 LangSmith (D1-D20)

| Item | Value | Status |
|---|---|---|
| Developer plan | 1 seat, $0; 5,000 base traces per month | docs-verified |
| Retention | Base 14 days; extended 180 days for new traces since 2026-09-14 | docs-verified |
| No card | "Personal organizations are limited to 5,000 traces per month until a credit card is added." Past the cap: HTTP 429, traces not stored; resets each UTC month. Also 50,000 events/hour and 500 MB/hour | docs-verified; live test pending |
| Overage (with card) | 0.005 LSU per base trace; 0.0025 LSU per extended upgrade; 1 LSU = $1 (tooltip text) | docs-verified; recheck before publishing |
| Trace | Root run plus all children = 1 trace; max 25,000 runs per trace | docs-verified |
| Evaluator traces | Each evaluator call per run in `evaluate()` is its own trace in project `evaluators`; `disable_evaluator_tracing=True` turns this off | docs- and source-verified; live test pending |
| Experiment retention | "Experiments: Runs are created at extended retention by default." Live, 2026-10-16: the API reports `trace_tier: longlived`, `ttl_seconds: 34560000` (400 days) on experiment runs created 2026-10-16, and the account's `/api/v1/ttl-settings` has `longlived_ttl_days: null`; the docs say extended traces get 180 days for new traces from 2026-09-14. The deletion date cannot be observed until expiry, so planning uses the documented 180 days; `exports/` is the durable record either way | docs-verified; live value conflicts (VERIFICATION.md, extended retention re-check) |
| Feedback upgrades | SDK `create_feedback` defaults to `extend_trace_retention=True`; UI feedback and manual annotation-queue adds do not upgrade; datasets kept indefinitely | source- and docs-verified |
| SDK | `langsmith` 0.14.9 (2026-10-15), Python >=3.10. `wrap_openai` traces `responses.create` and `responses.parse` with usage (since 0.3.16). `@traceable` nesting gives one trace per agent run. `RunTree.get_url()` for links | source-verified; live test pending |
| evaluate() | `num_repetitions`, `max_concurrency`, `experiment_prefix`, `metadata`, `upload_results`, `disable_evaluator_tracing`; one evaluator may return a list of `{"key","score"}` dicts; `ExperimentResults.comparison_url`; UI comparison view | source- and docs-verified |
| Datasets | No JSONL uploader: build examples in Python and call `create_examples`; examples may carry several `split` values (use for `smoke`, `section-1` ...) | docs-verified |
| Export | Write rows from the `ExperimentResults` iterator to local JSON at run time; `read_project(include_stats=True)` for aggregates; `list_runs`, `get_run_url`, `get_experiment_results` deprecated (removal after 2027-01-31) → `client.runs.query()` (async), `client.runs.get_url` | docs- and source-verified |
| Key check for `make doctor` | `next(iter(Client().list_projects(limit=1)), None)`; catch `LangSmithAuthError`, `LangSmithRateLimitError`, `LangSmithConnectionError`. `Client.info` does not prove a key is valid | source-verified; live test pending |

Retention decision input (for DESIGN.md): scores do not change experiment retention because experiment
runs start at extended retention. Recommendation carried into M2: store scores in run outputs and
metadata plus local exports; pass `extend_trace_retention=False` on any direct feedback call; keep
`disable_evaluator_tracing` as a per-batch switch; live-test trace and retention accounting on a fresh
no-card account in M3.

### 4.4 Sandbox (D21-D36)

- Codex modes: `read-only`, `workspace-write` (default for version-controlled folders), `danger-full-access`.
  Approvals: `on-request`, `never`, `granular` (`untrusted` retired, `on-failure` deprecated). Network off
  by default. Mechanisms: Seatbelt (macOS), bwrap plus seccomp (Linux), MXC (Windows), Linux sandbox on WSL2.
- Docker flags for one arm (from D24-D30): `--rm --network none --memory 1g --memory-swap 1g --cpus 1
  --pids-limit 256 --read-only --tmpfs /tmp:rw,nosuid,size=256m --user 1000:1000 --cap-drop ALL
  --security-opt no-new-privileges -v <workspace>:/work -w /work`. Live usage: `docker stats --no-stream
  --format "{{ json . }}"`. OOM: `State.OOMKilled`; exit 137 is the SIGKILL convention, not a Docker-documented code.
- Docker Desktop on Windows needs WSL >= 2.1.5; resource caps for the VM live in `.wslconfig`; keep
  bind-mounted workspaces in the Linux filesystem, not `/mnt/c`.
- Alternatives: Docker Engine via get.docker.com (Linux, WSL2); Podman v6.1.4 (Docker-compatible CLI,
  `podman machine` on macOS and Windows, rootless by default); Colima v0.10.3 on macOS (`colima start
  --cpu 2 --memory 4`).

### 4.5 Agent Skills (B1-B10)

- Frontmatter: `name` required (1-64 chars, lowercase a-z, 0-9, hyphens; no leading, trailing, or double
  hyphen; must match the folder name). `description` required (1-1024 chars; what it does and when to
  use it). Optional: `license`, `compatibility` (1-500 chars), `metadata` (string-to-string map),
  `allowed-tools` (experimental).
- Body: SKILL.md under 500 lines; instructions under 5000 tokens recommended; file references relative
  and one level deep; `platform/scripts/`, `references/`, `assets/` optional.
- Validator: `skills-ref` 0.1.1 (PyPI, Apache-2.0, Python >=3.11), "for demonstration purposes only".
  It rejects any frontmatter key outside the six spec fields. It does not check body length, file
  references, or token budget. The npm package `skills-ref` is by an unrelated author.
- Decision input: course skills use only the six spec fields so they pass the reference validator
  (skills-ref 0.1.1 installs its CLI as `agentskills`: `uv run agentskills validate <dir>`) and
  load in all three agents. `shipharness skills validate` runs the skills-ref checks (ASCII reading of the
  name charset) plus warnings for the 500-line and one-level-deep recommendations.
- Install paths: Claude Code `~/.claude/skills/<name>/`, `.claude/skills/<name>/`. Codex
  `.agents/skills` from the working directory up to the repo root, `$HOME/.agents/skills`,
  `/etc/codex/skills`. Cursor (2.4+) `.agents/skills/`, `.cursor/skills/`, home equivalents, and the
  Claude and Codex directories. No single directory is read by all three: install into
  `.claude/skills/` and `.agents/skills/`.

### 4.6 TestGen-LLM, ACH, SpecBench numbers (for slides and reading)

| Number | Value and unit | Source |
|---|---|---|
| Flakiness check | pass on "every one of five executions" | B11 §2 (F-b-19) |
| Evaluation funnel | per test class, 86 classes: 75% had a test that builds, 57% pass reliably, 25% increase line coverage | B11 §3.3 (F-b-23) |
| Deployment | about 10% of test classes improved (abstract says 11.5%); 73% of improvements accepted | B11 §4 (F-b-24) |
| ACH scale | 10,795 classes; 9,095 mutants that build and pass (31,677 generated); 4,660 non-equivalent; 571 tests; 73% acceptance | B12 (F-b-38, F-b-39) |
| Mutation vs coverage | 49% of tests that uniquely kill a mutant add no line coverage | B12 §6 (F-b-40) |
| Equivalence detector | precision/recall 0.95/0.96 with rule-based pre-processing (0.79/0.47 LLM only) | B12 §5.3 (F-b-37) |
| SpecBench scale | 30 tasks; 1,779 validation tests; 2,783 held-out tests | B14 |
| SpecBench gap vs size | +28 pp per tenfold code size (P90, abstract and Fig. 2 legend); text says about 27 pp; mean slope +23 pp | B13 (F-b-46; G-12) |
| SpecBench by size | worst-case gap 21 pp under 10K LOC; 100 pp over 25K LOC | B13 §3.1 (F-b-47) |
| A3 cost comparison | solo 20 min / $9 vs full harness 6 hr / $200 | A3 (F-a-152) |
| A4 scale | nearly 2,000 sessions; $20,000; 100,000 lines; 99% pass on most compiler suites incl. GCC torture tests | A4 (F-a-156 to F-a-158) |
| A1 scale | roughly 1,500 PRs; three engineers; 3.5 PRs per engineer per day | A1 (F-a-147) |

### 4.7 Tool versions (latest stable on 2026-10-16; all support Python 3.12)

| Package | Version | Package | Version |
|---|---|---|---|
| fastapi | 0.143.2 | coverage | 7.16.2 |
| uvicorn | 0.54.0 | pytest | 9.1.1 |
| sqlalchemy | 2.1.4 (needs >=3.11) | pytest-cov | 7.1.0 |
| alembic | 1.20.0 | pytest-xdist | 3.8.0 |
| jinja2 | 3.1.6 | hypothesis | 6.170.0 (MPL-2.0, dev only) |
| pydantic | 2.14.1 | playwright (Python) | 1.64.0 |
| pydantic-settings | 2.16.0 | ruff | 0.17.1 |
| structlog | 26.1.0 | openai | 3.31.0 |
| httpx | 0.28.1 | langsmith | 0.14.9 |
| schemathesis | 4.31.1 | typer | 0.27.3 |
| import-linter | 2.15 | rich | 15.0.0 |
| sse-starlette | 3.5.0 | python-multipart | 0.0.32 |
| skills-ref | 0.1.1 | uv | 0.13.1 (local 0.13.0) |
| htmx.org | 2.0.11 (pin; htmx 4.0.0 is on the `next` tag with a different extension model) | htmx-ext-sse | 2.2.4 (`hx-ext="sse"`, `sse-connect`, `sse-swap`) |
| @marp-team/marp-cli | 4.5.1 (Node >=18; PDF/PPTX need Chrome, Edge, or Firefox) | Vale | v3.24.0 (banned-word rule must be `level: error` to fail CI) |

Pin exact versions for all 0.x packages. mutmut 3.8.0 needs `fork` (WSL only on Windows) and cannot
target hand-chosen lines, so it is not used; shipharness uses a small targeted mutant runner (one
hand-written mutant applied at a time). Marp: use `--pptx` (slide images with presenter notes);
`--pptx-editable` is experimental and drops notes.

### 4.8 testgen-targets-v1 libraries (measured on Windows 11, Python 3.12.10)

| Library | Pin | License | Suite | Notes |
|---|---|---|---|---|
| boltons | 26.2.0, commit 4332b35a278d694f30c99881faa61cde695c7a96 | BSD-3-Clause | 672 tests (154 doctests), 3.4 s, 76% statement coverage | One Windows-only baseline failure: `tests/test_jsonutils.py::test_reverse_iter_lines`. Room for coverage gains |
| WTForms | 3.2.2, commit ea57c11591556333b4f0ac494d1e5d3f250ab305 | BSD-3-Clause | 354 tests, 0.9-2.3 s, 98% branch coverage | One Windows-only baseline failure: `tests/fields/test_date.py::test_basic`. Kept tests will mostly need to kill mutants. `filterwarnings = ["error"]` upstream |

Ten proposed target modules per library are in R-e. packaging 26.3 was rejected after measurement
(about 60 s suite; pytest depends on it, so mutants would change pytest itself).

---

## 5. Corrections to the brief

1. Feature list field is `passes` (boolean), not `status` (A2). `evidence` and `testedAt` are course additions.
2. ARCHITECTURE.md sits at the repo root next to AGENTS.md; PLANS.md, QUALITY_SCORE.md, RELIABILITY.md,
   SECURITY.md are inside docs/. A1's tree also has generated/db-schema.md and exec-plans/tech-debt-tracker.md.
3. The separate evaluator comes from A3. A2 has one coding agent that self-verifies and lists QA agents
   as future work.
4. Context resets and sprint contracts are dated, model-dependent choices in A3, not standing rules.
5. In A4 the oracle is GCC; the GCC torture suite is an evaluation result.
6. TestGen-LLM has three filters (builds; passes, including five-execution flakiness check; improves
   line coverage) plus a later dedup filter. "5 runs" is TestGen-LLM's number, not ACH's.
7. SpecBench is arXiv 2605.21384 (Weco AI, preprint). Its terms are "validation tests", "held-out tests",
   "reward hacking gap".
8. gpt-6-luna has a cache-write price ($0.125 per 1M) that the brief omits.
9. OpenAI "Tier 1" no longer exists; first paid tier is Build (2M TPM for luna).
10. LangSmith extended retention is documented as 180 days for new traces since 2026-09-14 (the API on
    the course account still reports a 400-day TTL on new experiment runs; planning uses 180); experiment runs start at extended
    retention; evaluator calls are separate traces.
11. Codex on Linux uses bwrap plus seccomp (not Landlock); approval policy names changed.
12. No single skills directory is read by Claude Code, Codex, and Cursor; skills-ref rejects vendor
    extension fields.
13. A1 does not define "harness engineering" in its body.
14. A1 limits its own results: its end-to-end autonomy "should not be assumed to generalize without
    similar investment—at least, not yet" (F-a-143). Course material that cites A1's numbers (for example
    roughly 1,500 PRs, 3.5 PRs per engineer per day) must carry this caveat next to them.

---

## 6. Open gaps

| ID | Gap | Plan | Milestone |
|---|---|---|---|
| G-1 | Cause 3 has no single direct sentence in A1-A5; support is A4 (container warning, pkill incident), A1 (pattern copying), A5 (security model), and A6 (supplementary) | Present cause 3 with these citations side by side; do not paraphrase them into one claim the sources do not make | M2, M7 |
| G-2 | A1 never defines "harness engineering" | Course gives no definition attributed to A1; the README and slides describe the harness as "the environment around the agent" with A1 F-a-02 ("design environments, specify intent, and build feedback loops") as the cited basis | M2 |
| G-3 | A6 is a living page (revised since A2 cited it); A7 is archived | Cite with access date; prefer A1-A5 quotes where both exist | M7 |
| G-4 | A2 uses both "feature_list.json" and "tests.json"; A6 uses "status" | Course uses feature_list.json and `passes` (A2, A5) | M2 |
| G-5 | "Forced session stop" is not a source term | Teach as A3 "context reset"; name the mechanism plainly ("session turn budget") | M2, M7 |
| G-6 | `evidence`, `testedAt`, and "only the harness sets passing" extend A2's design | Mark as course design in DESIGN.md and concepts; cite A2 for the base and A3 for separating doer and judge | M2 |
| G-7 | Filters 4 (real assertions, no mocking of the unit under test) and 5 (no source change in the test phase) have no direct source | Present as course filters with the composite citations in §3.4; candidate for "Open gaps" note in S4 concepts | M2, M7 |
| G-8 | "PASS_TO_PASS" is not a §1.9 term (it comes from SWE-bench, which is not on the source list) | **Closed 2026-10-16. Decision: `regression`.** Docs and slides say "existing tests keep passing" (A4 F-a-129, B11 F-b-22); code, score fields, and check names use `regression` (`regression_passed`, `regression_total`, check `regression`). "PASS_TO_PASS" does not appear in course material | Closed |
| G-9 | "House rules" is a course label | Cite A1 "golden principles" and "taste invariants" when introducing it | M2, M7 |
| G-10 | "Rubric" is not A3's wording | Use "grading criteria" in docs; code identifiers may say `criteria` | M2 |
| G-11 | Vendor-doc sentences (B7-B9) came through a summarising fetch tool | Re-copy any sentence before quoting it verbatim; path strings are reliable | M7 |
| G-12 | SpecBench states its slope as both 27 and 28 pp per tenfold size | Quote the abstract (28 pp, P90) and note the paper's own variation | M7 |
| G-13 | LangSmith behaviour on a no-card account (do experiment traces count against the 5,000 cap; are extended upgrades blocked or allowed; evaluator-trace tier; 401 vs 403 body; SDK behaviour on 429; dataset size limits) | **Partly closed 2026-10-16 by a live probe (VERIFICATION.md, M3):** on a personal no-card account, experiment runs are `longlived` (upgrades are not blocked); the API reports a 400-day TTL while the docs say 180 days for new extended traces, so planning uses 180, evaluator traces are `shortlived` (14 days) and one per evaluator call, an invalid key gives HTTP 403 and SDK `LangSmithError`. Still open: cap accounting for long-lived traces and the response at the cap (read the usage page after M6) | M6 |
| G-14 | OpenAI: whether replayed reasoning items are billed as input on later turns; real cache hit rates under parallel loops; reasoning tokens per turn; whether Free-tier orgs can call gpt-6-luna; flex with function calling | Measure in the M6 pilot from per-turn usage logs | M6 |
| G-15 | Library timings measured on Windows only; one Windows-only baseline failure per library | Known-failures list per library in testgen-targets-v1; repeat timings in CI (Linux) | M5 |
| G-16 | Mutant lines for the 40 testgen targets are sketches | Choose and validate in M5 (each mutant killed by at least one reference test, none equivalent) | M5 |
| G-17 | htmx-ext-sse license not stated in npm metadata | **Closed 2026-10-16.** The bigskysoftware/htmx-extensions repository has no LICENSE file and no license field in its package.json files, so `htmx-ext-sse` is not vendored. The console uses the browser `EventSource` API with a small own script (DESIGN D-15). htmx 2.0.11 itself is 0BSD and is vendored | Closed |
| G-18 | Product name clash: `shipproof` is taken on PyPI (a 0.1.0 CLI that checks AI coding agents' deploy claims) and npm; about 31 GitHub repos use the name, many in the same area; shipproof.io is a live product | **Resolved 2026-10-16 by the owner: the product is renamed `shipharness`.** On 2026-10-16 `shipharness` returned 404 on PyPI, npm, and github.com/shipharness, and a GitHub repository search for the name returned 0 results. No trademark search was done. Repository: `github.com/ANI-IN/shipharness`. Other free names checked: proofharness, testvetter, proofsieve, keptests | Closed |
| G-19 | boltons: 154 of its 672 tests are doctests (upstream runs `pytest --doctest-modules`). Whether doctests count in the baseline suite changes filter 3 ("adds coverage") and the referee's coverage numbers for boltons targets | **Accepted 2026-10-16 (owner):** doctests are part of the baseline suite (matches the upstream `pytest --doctest-modules` command). Recorded per target in testgen-targets-v1 metadata (`baseline_includes_doctests: true`) | M5 |
| G-20 | WTForms: upstream `pyproject.toml` sets `filterwarnings = ["error"]`, so a generated test that triggers any warning fails filters 1-2 under the upstream config | **Accepted 2026-10-16 (owner):** keep the upstream `filterwarnings = [\"error\"]`; a generated test that triggers a warning is discarded with the warning as the reason. Recorded per target in testgen-targets-v1 metadata (`pytest_config: upstream`, `warnings_are_errors: true`) | M5 |

---

## 7. Vendor pages re-read on 2026-10-17 (G-11)

G-11 asks for vendor-doc sentences to be re-copied from the live page before they are quoted. On
2026-10-17 each page below was downloaded (curl) and the quoted text was matched against the page
text by search, not through a summarising tool. Quotes are verbatim; "Uses" names the learner files
that quote or paraphrase the page. Paraphrased facts in those files were checked against the
sentences listed here.

| Source | URL (read 2026-10-17) | Verbatim text on the page | Uses |
|---|---|---|---|
| B7 Claude Code skills | https://code.claude.com/docs/en/skills | "Claude Code loads project skills from .claude/skills/ in the directory where you start it and in every parent directory up to the repository root"; precedence: "Enterprise over personal, and personal over project."; "If you create a top-level skills directory that didn’t exist when the session started, run /reload-skills to pick up the skills you put there."; "What skills are available?" (quoted). The page does not mention `.agents/skills` | `use-in-your-repo/skills/*/README.md` (Install, "What each page says", Use it) |
| B8 Codex skills | https://learn.chatgpt.com/docs/build-skills (https://developers.openai.com/codex/skills redirects here) | "Codex scans .agents/skills in every directory from your current working directory up to the repository root."; "Codex detects skill changes automatically. If an update doesn’t appear, restart Codex."; "Codex supports symlinked skill folders and follows the symlink target when scanning these locations."; "In Codex CLI or the IDE extension, run /skills or type $ to mention a skill."; "ChatGPT or Codex can choose a skill when your task matches the skill description." Also lists `$HOME/.agents/skills` and `/etc/codex/skills`; no `.claude/skills` | `use-in-your-repo/skills/*/README.md` |
| B9 Cursor skills | https://cursor.com/docs/skills (https://cursor.com/docs/context/skills redirects here since the M1 read) | Locations table: `.agents/skills/`, `.cursor/skills/` (project), `~/.agents/skills/`, `~/.cursor/skills/` (user); "For compatibility, Cursor also loads skills from Claude and Codex directories"; "When Cursor starts, it automatically discovers skills from skill directories and makes them available to Agent."; "To view discovered skills, open Customize in the sidebar and go to Skills"; "Skills can also be manually invoked by typing / in Agent chat"; "By default, skills are automatically applied when the agent determines they are relevant." No statement about restarting | `use-in-your-repo/skills/*/README.md` (URL updated to the new address) |
| B10 Cursor 2.4 changelog | https://cursor.com/changelog/2-4 | Dated "Jan 22, 2026"; "Cursor now supports Agent Skills in the editor and CLI" (quoted: "in the editor and CLI") | `use-in-your-repo/skills/*/README.md` |
| C9 OpenAI rate limits | https://developers.openai.com/api/docs/guides/rate-limits | Build tier row: "$5 in total credit purchases" (quoted) | `README.md` (accounts), `setup/linux.md` |
| C1 gpt-6-luna model page | https://developers.openai.com/api/docs/models/gpt-6-luna | Rate-limit table: "Free Not supported"; Build 5,000 RPM / 2,000,000 TPM; Launch 10,000 / 10,000,000; Grow 30,000 / 180,000,000. Changed since M1 (§4.2 said no Free row); quoted: "Not supported" | `README.md` (accounts; corrected) |
| D1 LangSmith pricing | https://www.langchain.com/pricing | Developer plan: "$0 / seat per month"; "Up to 5k base traces / mo" (both quoted) | `README.md` |
| D3 LangSmith billing | https://docs.langchain.com/langsmith/billing | "Personal organizations are limited to 5,000 traces per month until a credit card is added." (as §4.3); "Base traces have the base retention and are short-lived (14 days)" (both quoted) | `README.md`, `docs/after-class.md` |
| WSL file systems (Microsoft) | https://learn.microsoft.com/en-us/windows/wsl/filesystems | "For the fastest performance speed, store your files in the WSL file system if you are working in a Linux command line" (quoted) | `setup/windows.md` |
| Docker Desktop on Mac | https://docs.docker.com/desktop/setup/install/mac-install/ | "is free for small businesses (fewer than 250 employees AND less than $10 million in annual revenue)" (quoted) | `setup/macos.md` |
| Git for macOS | https://git-scm.com/install/mac | "Apple ships a binary package of Git with Xcode Command Line Tools" (quoted) | `setup/macos.md` |
| D32 Docker Engine on Ubuntu | https://docs.docker.com/engine/install/ubuntu/ | Section "Install using the apt repository" (quoted); supported versions now Ubuntu 26.10, 26.04 (LTS), 24.04 (LTS), 22.04 (LTS) | `setup/linux.md` (version list corrected) |
