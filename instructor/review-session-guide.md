# Review session guide (Thursday, 2 hours)

Plan for the review of the four assignments: about 25 minutes per assignment (expected approach,
solution walkthrough, common mistakes, discussion questions), then 20 minutes of open questions. The
A3 hidden diffs are revealed in this session.

Status: M11 draft. The assignments are being written in parallel (milestone M7). This guide refers to
their folders by path only; details they define (grading criteria weights, starter TODOs, solution
notes, the A3 hidden diffs, the commands each assignment uses) are `[[PENDING]]` and filled in after
M7. The "likely mistakes" lists below come from the design and the section concepts; replace or
extend them with each assignment README's "Common mistakes" section and with what the grader saw.

| Assignment | Brief and grading criteria | Starter | Solution | Self-check | Grader |
|---|---|---|---|---|---|
| A1 Instructions | `submodules/01-instructions/assignment/README.md` | `submodules/01-instructions/assignment/starter/` | `submodules/01-instructions/solution/` | `make check-assignment-1` | `make grade-assignment-1` |
| A2 State and session lifecycle | `submodules/02-state-lifecycle/assignment/README.md` | `submodules/02-state-lifecycle/assignment/starter/` | `submodules/02-state-lifecycle/solution/` | `make check-assignment-2` | `make grade-assignment-2` |
| A3 Scope and sandbox | `submodules/03-scope-sandbox/assignment/README.md` | `submodules/03-scope-sandbox/assignment/starter/` | `submodules/03-scope-sandbox/solution/` | `make check-assignment-3` | `make grade-assignment-3` |
| A4 Verification and portfolio | `submodules/04-verification/assignment/README.md` | `submodules/04-verification/assignment/starter/` | `submodules/04-verification/solution/` | `make check-assignment-4` | `make grade-assignment-4` |

The `check-assignment-N` and `grade-assignment-N` targets print "available after milestone M7" until
the assignment builders' rules are added to the Makefile.

## Agenda

| Time | Item |
|---|---|
| 0:00-0:25 | A1 Instructions |
| 0:25-0:50 | A2 State and session lifecycle |
| 0:50-1:15 | A3 Scope and sandbox, with the hidden-diff reveal |
| 1:15-1:40 | A4 Verification and portfolio |
| 1:40-2:00 | Open questions |

Each 25-minute block: expected approach (5), solution walkthrough (8), common mistakes (5),
discussion (7). For A3 the reveal takes the walkthrough slot plus part of the mistakes slot.

Before the session: run each grader on the reference solution and collect the class's grader output
(score per criterion), so the mistakes discussion uses real counts.

[[PENDING: grader score distribution per assignment and per criterion for this cohort | source: live class | how: make grade-assignment-N on each submission]]

---

## A1 Instructions (0:00-0:25)

**Task** (DESIGN §14.3). Restructure a 900-line instruction file into an AGENTS.md map plus docs plus
one skill built from `skills/skill-template`; write a checker for broken links and rule coverage; run
an A/B on the `section-1` subset with k=3 and report R1 and R3 results. Learner budget ≤ $2.50 and
≤ 150 traces (DESIGN §11.5).

**Expected approach (5 min).**
- Inventory every rule in the long file first, with an id each, before moving anything.
- Keep the map short and pointing outward: A1's map is "roughly 100 lines" and "the table of contents"
  (A1, F-a-22, F-a-27, F-a-28); the docs folder is the system of record (A1, F-a-29, F-a-30).
- Build the skill from `skills/skill-template` with the spec's fields only, `name` equal to the folder
  name, and validate it with `uv run shipharness skills validate <folder>` (B1; RESEARCH §4.5).
- The checker follows A1's mechanical checks: "Dedicated linters and CI jobs validate that the
  knowledge base is up to date, cross-linked, and structured correctly." (A1, F-a-37) Every link in
  the map resolves; every rule id appears in the docs; its messages say how to fix the problem (A1,
  F-a-97).
- The A/B keeps everything equal except the instructions layer and reports counts per arm, not
  percentages (DESIGN §8.3 rule 5).

**Solution walkthrough (8 min).** Open `submodules/01-instructions/solution/` and walk the map, one
doc, the skill, and the checker.

[[PENDING: A1 solution files to open, and the reference A/B result on section-1 (k=3) | source: M7 A1 builder | how: submodules/01-instructions/solution/ and its notes]]

**Likely mistakes (5 min).**
- The map copies rule text instead of pointing to it, and grows back toward the original size (A1:
  "Too much guidance becomes non-guidance.", F-a-23 to F-a-26).
- The skill fails validation: `name` differs from the folder name, or the frontmatter has fields the
  spec does not allow (RESEARCH §4.5; DESIGN D-17).
- The checker tests that files exist but not that every rule id is covered, or it misses links in
  tables.
- The A/B changes more than one thing between arms, or reports a percentage from k=3.

**Discussion (7 min).**
- "How long is the instruction file in your own repository, and what would its map look like?"
- "Which rules belong in a skill and which in a doc?" (B1, B2: progressive disclosure, F-b-05,
  F-b-06)
- "With k=3, what result would convince you that the map made a difference?"

---

## A2 State and session lifecycle (0:25-0:50)

**Task** (DESIGN §14.3). Make a three-session feature finish across three forced stops with no
duplicated migration and a consistent progress and exec-plan history. The grader checks migration
heads, redone work, and progress-file integrity. Learner budget ≤ $1.50 and ≤ 60 traces (DESIGN
§11.5).

**Expected approach (5 min).**
- The state a new session reads is on disk: `init.sh`, `progress.md`, the feature list, git history,
  the exec plan, and the structured handoff (A2, F-a-49, F-a-50, F-a-53; A1, F-a-34; A3, F-a-65).
- The session starts with A2's Getting up to speed routine: `pwd`, progress file and `git log`, the
  feature list, `init.sh`, a basic test (A2, F-a-58 to F-a-62).
- Before any migration, check `alembic heads`; one head is house rule R7 and the S2 measure (DESIGN
  §8.2).
- The harness writes the machine part of the handoff itself, so a handoff exists even when the agent
  writes none (DESIGN §6.3; `S2:stop_resume` in `src/shipharness/harness/state/lifecycle.py`).
- The exec plan moves from `active/` to `completed/` when the feature is done (A1, A7; F-a-45 to
  F-a-48).

**Solution walkthrough (8 min).** Open `submodules/02-state-lifecycle/solution/` and show the
session log after three stops and the single migration head.

[[PENDING: A2 solution files to open, and the reference run's progress log and migration heads | source: M7 A2 builder | how: submodules/02-state-lifecycle/solution/ and its notes]]

**Likely mistakes (5 min).**
- Relying on the agent to write the handoff; when a stop lands mid-edit, nothing is written.
- A second migration that creates the same table, or two heads after the second session.
- Rewriting earlier progress entries instead of appending (the log is history, not a status field).
- Different wrap-up or resume prompts for the two arms, which breaks the comparison (DESIGN §6.1).

**Discussion (7 min).**
- "Would compaction have been enough?" A2: "However, compaction isn’t sufficient." (A2, F-a-54) A3
  later dropped context resets for a newer model (RESEARCH §5, correction 4): when would you?
- "What does your team's handoff look like when a person, not an agent, stops halfway?"

---

## A3 Scope and sandbox, with the hidden-diff reveal (0:50-1:15)

**Task** (DESIGN §14.3). Implement a per-phase diff-scope policy and evidence-gated status updates,
and add one sandbox policy rule with a test that proves the denial. The grader replays hidden
scripted diffs, out-of-scope and legitimate: all bad diffs rejected, zero false positives. Learner
budget ≤ $0.25 and ≤ 30 traces, mostly deterministic (DESIGN §11.5).

**Expected approach (5 min).**
- Path rules are globs per phase, with segment-aware matching (`*` stays inside one path segment,
  `**` spans segments), as in `S3:allowed_paths` (`src/shipharness/harness/scope/guard.py`).
- Normalise paths before matching (leading `./`, backslashes); harness-only files such as
  `feature_list.json` are refused in every phase (A2, F-a-80; DESIGN D-14).
- Status changes only with evidence; the agent's claim alone is never enough (`S3:passes` in
  `src/shipharness/harness/scope/status.py`; course design: A2, F-a-108 and A3, F-a-110; RESEARCH G-6).
- The sandbox rule has a reason code and a message the agent can act on, and the test runs a command
  that the rule must refuse, then asserts the denial (`S3:policy` in
  `src/shipharness/sandbox/policy.py`; CONTRACTS §9).

**Reveal: the hidden diffs (10 min).** The diffs live with the A3 grader:

[[PENDING: path of the A3 hidden scripted diffs and the expected verdict for each | source: M7 A3 builder | how: submodules/03-scope-sandbox/assignment/ grader files]]

How to run the reveal:
1. Show one diff at a time, with the phase it was replayed in.
2. Ask the room: "Reject or accept, and why?" Take two or three answers before showing the expected
   verdict.
3. Show which submissions got it wrong, as a count (from the grader output collected before the
   session).
4. Pair a rejected diff with the legitimate diff closest to it: the pair shows where a false positive
   comes from.

**Likely mistakes (3 min).**
- Prefix matching with `startswith`, so an allow entry like `app/api` also allows `app/api_v2/...`.
- Checking only the new path of a rename, or ignoring deleted files.
- Refusing the state files (`progress.md`, `session-handoff.md`, `docs/exec-plans/**`) when the state
  layer is on: a false positive (`STATE_FILES` in `src/shipharness/harness/scope/guard.py`).
- A denial test that checks the regular expression but never runs the command through the sandbox.

**Discussion (7 min).**
- "Which costs your team more: a false positive that blocks a legitimate change, or a missed
  out-of-scope edit?"
- "The sandbox was identical for both arms in every run. Where in your own CI would its limits
  (no network, read-only root, process limit) catch something?" (DESIGN §9; A4, F-a-88, F-a-90)

---

## A4 Verification and portfolio (1:15-1:40)

**Task** (DESIGN §14.3). Add house rule R8 (soft delete respected on every endpoint) and one new test
filter; run `shipharness testgen` on the learner's own repository or an open-source repository;
publish the evidence report, the LangSmith experiment link, a one-page case study, and their own
skill. Learner budget ≤ $1.75 and ≤ 120 traces (DESIGN §11.5).

**Expected approach (5 min).**
- R8 discovers endpoints from the OpenAPI schema like R1 does (`S4:probe` in
  `src/shipharness/checks/r1_tenant.py`) and reports new violations against the checkpoint baseline
  (DESIGN §5).
- The new filter gives a reason for every discard, like the five course filters (`S4:filters` in
  `src/shipharness/filters/pipeline.py`); say whether it has a source or is a course filter, as the
  course does for filters 4 and 5 (RESEARCH G-7).
- `shipharness testgen` on a repository whose existing suite passes first; kept tests are the ones
  that pass all filters (B11, F-b-16 to F-b-22).
- The evidence report gives counts per run, not percentages, and links the LangSmith experiment.

**Solution walkthrough (8 min).**

[[PENDING: A4 solution files to open (R8 check, new filter, sample evidence report) | source: M7 A4 builder | how: submodules/04-verification/solution/ and its notes]]

**Likely mistakes (5 min).**
- R8 checks list endpoints only, and misses get-by-id, nested lists, and writes that still resolve a
  soft-deleted row.
- A filter that discards without a reason, or that crashes the pipeline instead of discarding.
- Testgen on a repository whose baseline suite already fails, so no generated test can be judged.
- A skill with frontmatter fields the spec does not allow (RESEARCH §4.5).

**Discussion (7 min).**
- "What did your filter discard, and would you have merged those tests?"
- "ACH found that 49% of tests that uniquely kill a mutant add no line coverage (B12, F-b-40). Did
  your kept tests kill mutants, add coverage, or both?"
- "What would make your case study convincing to a reviewer who distrusts agent-written code?"

---

## Open questions (1:40-2:00)

Prompts if the room is quiet:
- "Which of the four layers would you add to your repository first, and why?"
- "Which result from class surprised you most, compared with your poll answer?"
- "What would you need to see before letting an agent merge without a human reading the diff?"
