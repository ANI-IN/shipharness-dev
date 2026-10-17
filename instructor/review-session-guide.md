# Review session guide (Thursday, 2 hours)

Plan for the review of the four assignments: about 25 minutes per assignment (expected approach,
solution walkthrough, common mistakes, discussion questions), then 20 minutes of open questions. The
A3 hidden diffs are revealed in this session.

The "likely mistakes" lists below come from the design, the section concepts, and each solution's
`SOLUTION.md`; extend them with each assignment README's "Common mistakes" section and with
what the grader saw.

| Assignment | Brief and grading criteria | Starter | Solution | Self-check | Grader |
|---|---|---|---|---|---|
| A1 Instructions | `section-1-instructions/assignment/README.md` | `section-1-instructions/assignment/starter/` | `section-1-instructions/assignment/solution/` | `make check-assignment-1` | `make grade-assignment-1` |
| A2 State and session lifecycle | `section-2-state-lifecycle/assignment/README.md` | `section-2-state-lifecycle/assignment/starter/` | `section-2-state-lifecycle/assignment/solution/` | `make check-assignment-2` | `make grade-assignment-2` |
| A3 Scope and sandbox | `section-3-scope-sandbox/assignment/README.md` | `section-3-scope-sandbox/assignment/starter/` | `section-3-scope-sandbox/assignment/solution/` | `make check-assignment-3` | `make grade-assignment-3` |
| A4 Verification and portfolio | `section-4-verification/assignment/README.md` | `section-4-verification/assignment/starter/` | `section-4-verification/assignment/solution/` | `make check-assignment-4` | `make grade-assignment-4` |

`make check-assignment-N` is the learner's offline self-check. `make grade-assignment-N
SUBMISSION=<folder or git URL>` runs the private grader in `section-N-*/assignment/solution/grader/`; in the
learner repository it stops with `no grader for assignment N: graders are private (build repository
only)`. Reference scores (each solution's `captured/grade-solution.txt`, captured 2026-10-17): A1
83/100, A2 90/100, A3 90/100 (FAIL: valid live evidence is a pass condition), A4 100/100 (20 of those
points pass on pending markers accepted for the reference folder only). Every lost or
marker-held point is the reference solution's live run, which had not been captured on that date.

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

Before the session: run each grader on the reference solution and on every submission, and tally the
output per criterion: how many submissions lost points on it, and its most common message. The
mistakes discussion uses those counts, not impressions. Bring the tally as one table per assignment.

---

## A1 Instructions (0:00-0:25)

**Task** (DESIGN §14.3). Restructure a 900-line instruction file into an AGENTS.md map plus docs plus
one skill built from `use-in-your-repo/skills/skill-template`; write a checker for broken links and rule coverage; run
an A/B on the `section-1` subset with k=3 and report R1 and R3 results. Learner budget ≤ $2.50 and
≤ 150 traces (DESIGN §11.5).

**Expected approach (5 min).**
- Inventory every rule in the long file first, with an id each, before moving anything.
- Keep the map short and pointing outward: A1's map is "roughly 100 lines" and "the table of contents"
  (A1, F-a-22, F-a-27, F-a-28); the docs folder is the system of record (A1, F-a-29, F-a-30).
- Build the skill from `use-in-your-repo/skills/skill-template` with the spec's fields only, `name` equal to the folder
  name, and validate it with `uv run shipharness skills validate <folder>` (B1; RESEARCH §4.5).
- The checker follows A1's mechanical checks: "Dedicated linters and CI jobs validate that the
  knowledge base is up to date, cross-linked, and structured correctly." (A1, F-a-37) Every link in
  the map resolves; every rule id appears in the docs; its messages say how to fix the problem (A1,
  F-a-97).
- The A/B keeps everything equal except the instructions layer and reports counts per arm, not
  percentages (DESIGN §8.3 rule 5).

**Solution walkthrough (8 min).** Open `section-1-instructions/assignment/solution/` and walk, in this
order: `work/instructions/AGENTS.md` (the map), `work/instructions/ARCHITECTURE.md`, one document
under `work/instructions/docs/` (`SECURITY.md` holds R1), the `add-list-endpoint` skill (`work/instructions/.agents/skills/add-list-endpoint/SKILL.md`), and the
checker `work/checker/check_docs.py` with its tests `work/checker/test_check_docs.py`. Then
`SOLUTION.md`, "Design choices and why" and "Trade-offs and known limits". The reference A/B on `section-1` (k=3) has
not been run: `work/ab-report.md` has the full structure with its values still marked pending, and the
reference scores 83/100 because criterion E (A/B values, 5 points) and criterion F (live run evidence,
12 points) need that run (`captured/grade-solution.txt`). Say so, and show the report's structure,
which is what a learner's report must have. For a measured comparison on this section, point to the
class pilot's S1 results (run sheet, all-results table): no measurable difference on F1 with this
model.

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
  writes none (DESIGN §6.3; `S2:stop_resume` in `platform/src/shipharness/harness/state/lifecycle.py`).
- The exec plan moves from `active/` to `completed/` when the feature is done (A1, A7; F-a-45 to
  F-a-48).

**Solution walkthrough (8 min).** Open `section-2-state-lifecycle/assignment/solution/a2_state/layer.py`
(the `ResumableStateLayer`), then `ledger.py` and `progress_log.py`, then `SOLUTION.md`. The
grader's hidden scenarios (`grader/a2_hidden.py`, four scenarios and a hidden four-step feature) run
a scripted stand-in agent, not a model. On the reference solution every scenario criterion passes, among them
"progress.md logs every session exactly once, in order", "Exec plan moved to
docs/exec-plans/completed/, with an outcome", and "session-handoff.md: final summary, migration heads,
agent notes kept" (`captured/grade-solution.txt`, 90.0/100; the 10 live-run points need the reference
live run). Show `captured/grade-class-s2-layer.txt` next to it: the class's own S2 layer graded as a
baseline, so the room sees which criteria the course layer does not meet.

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
  `**` spans segments), as in `S3:allowed_paths` (`platform/src/shipharness/harness/scope/guard.py`).
- Normalise paths before matching (leading `./`, backslashes); harness-only files such as
  `feature_list.json` are refused in every phase (A2, F-a-80; DESIGN D-14).
- Status changes only with evidence; the agent's claim alone is never enough (`S3:passes` in
  `platform/src/shipharness/harness/scope/status.py`; course design: A2, F-a-108 and A3, F-a-110; RESEARCH G-6).
- The sandbox rule has a reason code and a message the agent can act on, and the test runs a command
  that the rule must refuse, then asserts the denial (`S3:policy` in
  `platform/src/shipharness/sandbox/policy.py`; CONTRACTS §9).

**Reveal: the hidden diffs (10 min).** The diffs live with the A3 grader:
`section-3-scope-sandbox/assignment/solution/grader/hidden/diffs/` (43 diffs: 26 named `bad-*`, 17 named
`good-*`), with the expected verdict, phase, allow lists, and refusal reason of each in
`grader/hidden/cases.json` (built by `make_hidden.py`). The pass condition is every bad diff rejected
and zero false positives. Pairs that show where a false positive or a miss comes from:

| Rejected | Accepted | What the pair shows |
|---|---|---|
| `bad-glob-prefix-boundary` (`tests/visible_extra/test_a.py`, test phase) | `good-deep-test-path` (`tests/visible/api/v2/test_replay.py`) | `tests/visible/**` must not match a sibling folder that shares the prefix |
| `bad-exact-pattern-suffix` (`app/api/issues.py.orig`) | `good-dot-slash-prefix` (`app/api/issues.py` written as `./app/api/issues.py`) | An exact path allows only itself; a leading `./` is normalised, not refused |
| `bad-progress-without-state-layer` (`progress.md`, state layer off) | `good-exec-plan-moves-to-completed` (state layer on) | State files are allowed only when the state layer is on |
| `bad-space-path-out-of-scope` (`docs/design notes/f3 retry.md` under the F3 allow list) | `good-double-star-zero-dirs` (the same path under `docs/**/*.md`) | A path with spaces is parsed, then judged by the allow list in force |
| `bad-traversal-inside-allowed-glob` (`tests/visible/../../app/services/issues.py`) | `good-delete-in-scope` (`tests/visible/test_old.py`) | `..` that leaves the allowed folder is refused as `path_escape` |

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
  layer is on: a false positive (`STATE_FILES` in `platform/src/shipharness/harness/scope/guard.py`).
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
  `platform/src/shipharness/checks/r1_tenant.py`) and reports new violations against the checkpoint baseline
  (DESIGN §5).
- The new filter gives a reason for every discard, like the five course filters (`S4:filters` in
  `platform/src/shipharness/filters/pipeline.py`); say whether it has a source or is a course filter, as the
  course does for filters 4 and 5 (RESEARCH G-7).
- `shipharness testgen` on a repository whose existing suite passes first; kept tests are the ones
  that pass all filters (B11, F-b-16 to F-b-22).
- The evidence report gives counts per run, not percentages, and links the LangSmith experiment.

**Solution walkthrough (8 min).** Open, in order:
`section-4-verification/assignment/solution/a4_verification/r8_soft_delete.py` (the R8 check) with its
adapter `adapter.py` and `captured/r8-teamtrack.json` (R8 on TeamTrack, real output, no model call);
`dedup_filter.py` (filter 6) and `apply_filter.py`; `portfolio/evidence-report.md`,
`portfolio/case-study.md`, and `portfolio/langsmith.md`; the example learner skill
`skill/testgen-evidence/SKILL.md`. The portfolio's model-run sections and `live/` hold pending
markers until the reference live run is captured; the grader accepts them for the reference folder
only, so its 100/100 includes 20 points that rest on those markers (`SOLUTION.md`, "Known
limits"). Say so when you show the score.

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
