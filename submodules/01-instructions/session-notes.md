# S1 session notes: what the agent knows

For learners, after class. Reading time: about 8 minutes. Source IDs (A1, B1, ...) and finding IDs
(F-a-NN, F-b-NN) are listed in [REFERENCES.md](../../REFERENCES.md), which is generated when the course
is released. "S1", "layer", "trap", "blinded reviewer", and the house rules R1-R7 are course labels,
not source terms ([concepts.md](concepts.md), note on labels).

---

## 1. What was shown

| Block | What happened | Where to read it again |
|---|---|---|
| Poll | How many of 10 bare-arm runs of F1 ship `GET /issues` with a new R1 violation? | [demo/README.md](demo/README.md), section 4 |
| Launch | `make demo-1`: one A/B on F1 (org-wide issue search), bare arm against the harness arm with the instructions layer only | [demo/README.md](demo/README.md), sections 1-2 |
| Concepts | Problem, cause, harness piece, implementation, measure | [concepts.md](concepts.md) |
| Walkthrough | The legacy `/v1/issues` handler next to the scoped query; anchors `S1:agents_md`, `S1:progressive`, `S1:prefix` | `uv run python scripts/anchors.py extract S1:prefix` |
| Demo block | Screens 1, 2, 3 (and 5) of the finished A/B; the verdicts; screen 4 with the dots; `make swap-1` | [demo/README.md](demo/README.md), sections 3, 5-8 |

Tonight's class run:

[[PENDING: tonight's demo-1 result, one line per arm (primary measure, R1 new, hidden tests, reviewer verdict, cost), with the ab id and run ids | source: live class | how: make demo-1]]

---

## 2. Key ideas, with sources

1. **What is not in context does not exist for the agent.** "From the agent’s point of view, anything
   it can’t access in-context while running effectively doesn’t exist." (A1, F-a-05). A rule in a
   file the agent never opens is, for that run, not a rule.
2. **Agents copy what they find.** "Codex replicates patterns that already exist in the
   repository—even uneven or suboptimal ones." (A1, F-a-20). TeamTrack's legacy `GET /v1/issues`
   handler lists every org's issues and sits next to the query F1 must write.
3. **One big instruction file is not the fix.** "Context is a scarce resource. A giant instruction
   file crowds out the task, the code, and the relevant docs" (A1, F-a-23); "Too much guidance
   becomes non-guidance." (A1, F-a-24).
4. **AGENTS.md is a map.** "give Codex a map, not a 1,000-page instruction manual." (A1, F-a-22);
   "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map,
   with pointers to deeper sources of truth elsewhere." (A1, F-a-28). TeamTrack's map is 94 lines.
5. **docs/ is the system of record**, in A1's layout: `ARCHITECTURE.md` at the root, `SECURITY.md`,
   `RELIABILITY.md`, `QUALITY_SCORE.md`, `PLANS.md`, `design-docs/`, `product-specs/` under `docs/`
   (A1, F-a-29, F-a-30).
6. **Progressive disclosure, for docs and for skills.** "agents start with a small, stable entry
   point and are taught where to look next" (A1, F-a-36). For skills, only `name` and `description`
   load at startup (B1, F-b-05); the body loads when the skill is used, and resources only when
   required.
7. **The context prefix** is the course's place for A1's "injected into context": the map plus the
   skills catalogue, sent as the developer message of every session, built from the course checkout
   so the agent cannot rewrite it (`src/shipharness/harness/instructions/router.py`). This is course
   design, not a source term.
8. **The harness may reorganise knowledge, never add it** (a course rule). Every rule in the harness
   docs is also in `docs/HANDBOOK.md`, which both arms have (`tests/unit/harness_instructions/test_parity.py`).
9. **Docs are checked like code.** "Dedicated linters and CI jobs validate that the knowledge base is
   up to date, cross-linked, and structured correctly." (A1, F-a-37). Assignment A1 asks you to build
   one such checker.

---

## 3. What the A/B showed

Read every live result next to the experiment dots, never alone; results are counts of failing runs,
never percentages (a course rule).

### Pilot run 2 (2026-10-16)

Measured in the course pilot, run 2, 2026-10-16: twelve A/Bs, F1-F4 canonical, k=3 per section,
gpt-6-luna at effort medium for both arms, two A/Bs in parallel. Primary measure passed, per section
and arm (the F1 run ids are in [demo/README.md](demo/README.md), section 7):

| Section | Bare arm | Harness arm | Why runs failed |
|---|---|---|---|
| F1 (S1) | 3/3 | 3/3 | none failed: no new R1 violation |
| F2 (S2) | 3/3 | 0/3 | harness arms failed on a measurement bug, fixed after run 2 |
| F3 (S3) | 3/3 | 3/3 | none failed |
| F4 (S4) | 0/3 | 0/3 | the measure needs every hidden test passed and every mutant killed; no run had both |

For S1 that means no gap: three bare and three harness runs, each with 0 new R1 violations and 52
of 52 hidden tests. The run logs explain it. The canonical ticket ends with "Follow the house rules
in docs/HANDBOOK.md", every bare arm opened the handbook with its third tool call, and `read_file`
returns the whole 150-line file, so the bare arm had every rule in context. The harness arm read the
handbook too, then the `add-endpoint` skill and the focused docs. No arm opened the legacy handler.
Both arms wrote the same org-scoped query. Per-run records with run ids, and what each arm read, are
in [demo/README.md](demo/README.md), sections 6 and 7.

The live console check on 2026-10-16 (A/B `ab-20261016-210339-909651`, `make demo-1 PURPOSE=pilot`,
F1 canonical) adds one more pair of dots: both arms passed, 0 new R1 violations and 52 of 52 hidden
tests each, 9 min 10 s and $0.027821 for the whole A/B (run ids in
[demo/README.md](demo/README.md), section 7).

What changed because of it: the course's pre-registered next step for a section with no gap is its
trap variant. `F1-trap` names the legacy code as the place where the query code exists and does not
point to the handbook.

### Pilot run 3 and the experiments

[[PENDING: pilot run 3 result for S1 (F1-trap), runs failing of 3 per arm on r1_new_violations>=1, with run ids, and the class decision for S1 | source: M6 pilot | how: course pilot (build repository)]]

[[PENDING: batch 1 dots for F1 canonical, runs failing out of 10 per arm, with run ids | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation result for the leave-out-instructions configuration (all minus instructions) | source: M8 ablation | how: uv run shipharness report]]

If S1 still shows no gap after these, the course has pre-registered how it is reported: as no
measurable difference on this task with this model, shown with the live A/B, the dots, and a
discussion of why.

---

## 4. Common questions

**The bare arm passed without a map. Does the map do nothing?**
On the canonical ticket the ticket itself pointed to the handbook, so both arms had the rules in
context (section 3). The A/B measures the map only on tickets that do not do that work for it. That
is why the pre-registered next task is the trap variant, and why "what did each arm read before it
wrote the query?" is the question for the discussion.

**Is the harness arm not just given more information?**
No. By course rule the harness may change how knowledge is organised and delivered, not add facts
the bare arm cannot read; a unit test checks that every rule in the harness docs is also in the
handbook (`tests/unit/harness_instructions/test_parity.py`). Both arms always get the same ticket,
model, effort, tools, turn budget, cost cap, and sandbox.

**Why not paste the whole handbook into the prompt?**
A1 gives four reasons against one large instruction file: it crowds out the task (F-a-23), too much
guidance "becomes non-guidance" (F-a-24), it "rots instantly" (F-a-25), and it cannot be checked
mechanically (F-a-26).

**What does the agent see of a skill at the start?**
One catalogue line per skill: name, description, and the path to `SKILL.md`
(`catalogue_block` in `src/shipharness/runner/skills_loader.py`, anchor `S1:progressive`). The body
is tier 2 and loads only when the agent reads it (B1, F-b-05). In pilot run 2 every F1 harness arm
read the body; none read the tier 3 file `references/tests.md`.

**Why is the prefix built from the course checkout and not from the arm's workspace?**
So that the agent cannot change what it is told by editing its own copy of `AGENTS.md`. The prefix
stays the same for the whole run (docstring of `router.py`).

**The reviewer rejected both arms in one A/B, but the referee passed them. Which is right?**
Both, on different questions. The referee's R1 check is the pre-registered primary measure
(`REGISTERED_PRIMARY` in `src/shipharness/datasets/features_checks.py`). The blinded reviewer, a course
design after A3's separate evaluator (A3, F-a-110), is a secondary measure; in
`ab-20261016-183644-0036f0` it objected to how both arms handled an archived project passed as
`project_id`, said `tenant_isolation_risk: none`, and the hidden tests passed 52 of 52 in both arms
([demo/README.md](demo/README.md), section 7).

**Does the files-read map on screen 3 prove the harness worked?**
No. It shows which documents each arm opened with `read_file`, which helps explain a result. The
score is what the referee finds in the shipped code. Reads through `run` (for example `cat`) do not
appear.

**Why counts and not percentages?**
It is a course rule: every run is a dot, and results are counts such as 9/10. With k=3 or k=10, a
percentage hides how few runs there are.

---

## 5. What to try next

1. Start assignment A1: [assignment/README.md](assignment/README.md). Run `make check-assignment-1`
   first; on the unchanged starter it fails by design and every FAIL line says what to fix.
2. Open `teamtrack/docs/HANDBOOK.md` and `teamtrack/harness/instructions/AGENTS.md` side by side. For
   R1, how many lines does an agent read before it reaches the rule in each?
3. Compare the `F1-canonical` and `F1-trap` tickets in `datasets/teamtrack-features-v1.jsonl`. Which
   sentence in each points the agent somewhere, and where?
4. Validate the course skill and read it against the specification:
   `uv run shipharness skills validate teamtrack/harness/instructions/.agents/skills`.
5. Read the post-class pieces, about 21 minutes in total:
   [post-class-reading/README.md](post-class-reading/README.md).
6. In your own repository: count the lines of your agent instruction file, and list the three rules
   your agent most often breaks. Where does each live, and does anything point to it before the
   agent writes code?
