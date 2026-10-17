# S1 session notes: what the agent knows

For learners, after class. Reading time: about 8 minutes. Source IDs (A1, B1, ...) and finding IDs
(F-a-NN, F-b-NN) are listed in [docs/REFERENCES.md](../docs/REFERENCES.md), which is generated when the course
is released. "S1", "layer", "trap", "blinded reviewer", and the house rules R1-R7 are course labels,
not source terms ([concepts.md](concepts.md), note on labels).

---

## 1. What was shown

| Block | What happened | Where to read it again |
|---|---|---|
| Poll | In how many of 10 runs does each arm add at least one new R1 violation while building F1? | [demo/README.md](demo/README.md), section 9 |
| Launch | `make show-1`: the harness arm alone on F1 (org-wide issue search) with the instructions layer, live. "Harness in action", not an A/B: the pilot showed no gap to demonstrate | [demo/README.md](demo/README.md), parts 1, 4, 5 |
| Concepts | Problem, cause, harness piece, implementation, measure, and what the map assumes | [concepts.md](concepts.md) |
| Walkthrough | The legacy `/v1/issues` handler next to the scoped query; anchors `S1:agents_md`, `S1:progressive`, `S1:prefix` | `uv run python platform/scripts/anchors.py extract S1:prefix` |
| Demo block | The finished `make show-1` run (screens 1, 3, 2); screen 4 with every pilot result | [demo/README.md](demo/README.md), parts 5 and 6 |

The class's `make show-1` run ran on the class host, so its record is not in this repository; in
class, its verdict was read off console screen 1. A captured `make show-1` run (captured on 2026-10-17, run
`ab-20261017-112101-c5d839`, a timing run on a quiet machine) is in
[demo/README.md](demo/README.md), parts 5 and 7.

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
   so the agent cannot rewrite it (`platform/src/shipharness/harness/instructions/router.py`). This is course
   design, not a source term.
8. **The harness may reorganise knowledge, never add it** (a course rule). Every rule in the harness
   docs is also in `docs/HANDBOOK.md`, which both arms have (`platform/tests/unit/harness_instructions/test_parity.py`).
9. **Docs are checked like code.** "Dedicated linters and CI jobs validate that the knowledge base is
   up to date, cross-linked, and structured correctly." (A1, F-a-37). Assignment A1 asks you to build
   one such checker.
10. **Every harness piece encodes an assumption about the model.** "every component in a harness
    encodes an assumption about what the model can't do on its own, and those assumptions are worth
    stress testing" (A3, F-a-124). The map's assumption, in the course's words: the model will not
    apply a rule it has not been pointed to. For this model on these tickets it did not hold
    (section 3).

---

## 3. What the A/B showed

Results are counts of failing runs, never percentages (a course rule). Every number below is from
the course pilot, gpt-6-luna with the same settings for both arms; the per-run records with run ids
are in [demo/README.md](demo/README.md), section 11.

### The primary measure on F1

Runs failing the primary measure (`r1_new_violations >= 1`), per arm:

| Run | Ticket, effort | Bare arm | Harness arm | A/Bs |
|---|---|---|---|---|
| 2, 2026-10-16 | `F1-canonical`, medium | 0 of 3 | 0 of 3 | `ab-20261016-181736-a07558`, `ab-20261016-183644-0036f0`, `ab-20261016-185628-37483b` |
| Live console check, 2026-10-16 | `F1-canonical`, medium | 0 of 1 | 0 of 1 | `ab-20261016-210339-909651` |
| 3, 2026-10-16 | `F1-trap`, medium | 0 of 3 | 0 of 3 | `ab-20261016-211419-07937b`, `ab-20261016-212745-2c14fb`, `ab-20261016-214636-c8b3c4` |
| 4, 2026-10-16 | `F1-trap`, low | 0 of 3 | 0 of 3 | `ab-20261016-232842-b372c2`, `ab-20261016-233807-3f34fa`, `ab-20261016-234639-4a18bd` |
| Class-profile round, 2026-10-17 | `F1-trap`, low, Fast tier | 0 of 1 | 0 of 1 | `ab-20261017-084558-0356a0` |

Every arm had 0 new R1 violations and 52 of 52 hidden tests. No measurable difference on this task
with this model (course pilot, runs 3 and 4 and the class-profile round).

Why: the canonical ticket ends with "Follow the house rules in docs/HANDBOOK.md", every bare arm in
run 2 opened the handbook with its third tool call, and `read_file` returns the whole 150-line file,
so the bare arm had every rule in context. The trap ticket `F1-trap` names the legacy code as the
place where the query code exists and does not point to the handbook; no arm copied the legacy query
into a leak. In the class-profile round the bare arm did not open the handbook in its first nine tool
calls and still wrote a scoped query. What each arm read is in [demo/README.md](demo/README.md),
section 9.

### All four sections, and what was not run

Runs that passed the primary measure, bare arm first, then harness arm, for every section:

| Section | Run 3 (medium) | Run 4 (low) | Class-profile round (low, Fast) | Result |
|---|---|---|---|---|
| F1 (S1) | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 | no measurable difference |
| F2 (S2) | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 | no measurable difference |
| F3 (S3) | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 | no measurable difference |
| F4 (S4) | 0/3, 0/3 | not run | 0/1, 0/1 | no measurable difference (both arms fail) |

The course pre-registered a gate: the harness arm ahead in at least three of four sections. It
passed in none, so the planned experiments (batches of 10 runs per arm and a leave-one-out ablation)
were not run, and every section is reported as no measurable difference on this task with this
model.

### Post hoc: what else the F1 arms did

Chosen after the results were known, so descriptive only, over 10 runs per arm (runs 2, 3, and 4 and
the console check): harness arms claimed done in 5, bare arms in 9, and no claim was false in either
arm; median cost per arm $0.0122 against $0.0103; median arm wall time 168 s against 177 s; neither
arm hit the agent time limit.

### What class showed instead

With no gap to demonstrate, S1 showed the harness arm alone at work (`make show-1`: it reads the map,
then the documents the ticket needs), live, judged by the referee. The map is a bet on what the model
will miss, and only a measure such as the referee's R1 check tells you whether it paid off. Optional
extras outside class (a replayed pilot run and a scripted example) are listed in
[docs/extras.md](../docs/extras.md).

---

## 4. Common questions

**The harness did not win. Was it useless?**
On this model and these tickets the map changed nothing the referee measures: no measurable
difference (section 3). That is a result about one assumption, not a verdict on maps. A3 asks for
exactly this test, "those assumptions are worth stress testing" (A3, F-a-124), and dropped one of its
own pieces, context resets, once its model no longer needed them (A3, F-a-69). The pilot also did
not measure A1's maintenance reasons for a map: one large file goes stale and cannot be checked
mechanically (A1, F-a-25, F-a-26). On your own repository, keep the map where a measure on your model
shows it earns its place, or for the maintenance reasons, and say which.

**Is the harness arm not just given more information?**
No. By course rule the harness may change how knowledge is organised and delivered, not add facts
the bare arm cannot read; a unit test checks that every rule in the harness docs is also in the
handbook (`platform/tests/unit/harness_instructions/test_parity.py`). Both arms always get the same ticket,
model, effort, tools, turn budget, cost cap, and sandbox.

**Why not paste the whole handbook into the prompt?**
A1 gives four reasons against one large instruction file: it crowds out the task (F-a-23), too much
guidance "becomes non-guidance" (F-a-24), it "rots instantly" (F-a-25), and it cannot be checked
mechanically (F-a-26).

**What does the agent see of a skill at the start?**
One catalogue line per skill: name, description, and the path to `SKILL.md`
(`catalogue_block` in `platform/src/shipharness/runner/skills_loader.py`, anchor `S1:progressive`). The body
is tier 2 and loads only when the agent reads it (B1, F-b-05). In pilot run 2 every F1 harness arm
read the body; none read the tier 3 file `references/tests.md`.

**Why is the prefix built from the course checkout and not from the arm's workspace?**
So that the agent cannot change what it is told by editing its own copy of `AGENTS.md`. The prefix
stays the same for the whole run (docstring of `router.py`).

**The reviewer rejected both arms in one A/B, but the referee passed them. Which is right?**
Both, on different questions. The referee's R1 check is the pre-registered primary measure
(`REGISTERED_PRIMARY` in `platform/src/shipharness/datasets/features_checks.py`). The blinded reviewer, a course
design after A3's separate evaluator (A3, F-a-110), is a secondary measure; in
`ab-20261016-183644-0036f0` it objected to how both arms handled an archived project passed as
`project_id`, said `tenant_isolation_risk: none`, and the hidden tests passed 52 of 52 in both arms
([demo/README.md](demo/README.md), section 11).

**Does the files-read map on screen 3 prove the harness worked?**
No. It shows which documents each arm opened with `read_file`, which helps explain a result. The
score is what the referee finds in the shipped code. Reads through `run` (for example `cat`) do not
appear.

**Why counts and not percentages?**
It is a course rule: every run is a dot, and results are counts such as 3/3. With k=1 or k=3, a
percentage hides how few runs there are.

---

## 5. What to try next

1. Start assignment A1: [assignment/README.md](assignment/README.md). Run `make check-assignment-1`
   first; on the unchanged starter it fails by design and every FAIL line says what to fix.
2. Open `platform/teamtrack/docs/HANDBOOK.md` and `platform/teamtrack/harness/instructions/AGENTS.md` side by side. For
   R1, how many lines does an agent read before it reaches the rule in each?
3. Compare the `F1-canonical` and `F1-trap` tickets in `platform/datasets/teamtrack-features-v1.jsonl`. Which
   sentence in each points the agent somewhere, and where?
4. Validate the course skill and read it against the specification:
   `uv run shipharness skills validate platform/teamtrack/harness/instructions/.agents/skills`.
5. Read the post-class pieces, about 21 minutes in total:
   [post-class-reading/README.md](post-class-reading/README.md).
6. In your own repository: count the lines of your agent instruction file, and list the three rules
   your agent most often breaks. Where does each live, and does anything point to it before the
   agent writes code?
