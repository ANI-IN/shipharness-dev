# A1 solution notes

Reference solution for assignment A1 ([brief](../assignment/README.md)). Source ids refer to
`RESEARCH.md`. Everything marked "course design" was designed for this course and is not a claim of
the sources.

## Approach

1. **Inventory.** The original (`assignment/starter/original/AGENTS.md`, 899 lines) has 70 tags:
   66 active rules and 4 retired ones (R2.5, R3.8, R7.5, CV-23). Everything else is background:
   history, incident notes, review comments, questions and answers, a glossary.
2. **Checker first, test-first.** The visible tests (`work/checker/test_check_docs.py`, a byte copy of
   the starter's) and the eleven hidden cases (`grader/hidden/checker_cases.py`) were written before
   the reference checker, seen failing against the starter stubs (12 of 15 visible tests fail), and
   then made to pass. The checker ran after every document of the split.
3. **One home per rule.** Each document answers one question an agent asks before it edits code:

   | Tags | Home | Question |
   |---|---|---|
   | R1.1 to R1.6, R2.1 to R2.4, R2.6, CV-22, CV-25 | `docs/SECURITY.md` | who may see or change this data? |
   | R3.1 to R3.7, R3.9, CV-13 to CV-16 | `docs/design-docs/api-conventions.md` | what shape must the response and request have? |
   | R4.1 to R4.7, R5.1 to R5.6, R7.1 to R7.4, R7.6, CV-11 | `docs/RELIABILITY.md` | is this write safe to repeat, audited, and migrated? |
   | R6.1 to R6.5, CV-01, CV-02, CV-19, CV-20, CV-21, CV-24 | `ARCHITECTURE.md` | where does this code go, and what may it import? |
   | CV-04 to CV-07, CV-17, CV-18 | `docs/product-specs/teamtrack-base.md` | how does the product behave? |
   | CV-03, CV-08 to CV-10 | `docs/QUALITY_SCORE.md` | how do I test it, and what must I not copy? |
   | CV-12 | `docs/PLANS.md` | how big should this change be? |
   | R2.5, R3.8, R7.5, CV-23 (retired) | not carried over | history only, in `docs/design-docs/decisions.md` |

   The counts add up to 66 (13 + 12 + 19 + 11 + 6 + 4 + 1).
4. **The map** (`work/instructions/AGENTS.md`, 94 lines) is a table of contents in A1's sense: "we
   treat it as the table of contents" (A1, F-a-27). It holds a "where to look" table keyed by what
   the agent is about to do, the seven house rules as references with anchored links, the "do not
   copy" warning for the legacy handler (A1, F-a-20), the commands, the layout, and a short "before
   you finish" list. It defines no rule.
5. **The skill** `add-list-endpoint` targets the work the A/B measures: every section-1 task except
   the control task C1 is a variant of F1, an org-wide list endpoint (canonical, three rewordings, two
   alternate checkpoints, and the trap variant; `datasets/teamtrack-features-v1.jsonl`), and the
   measures are R1 and R3. Its description is the only part loaded up front (B1, F-b-05); the steps
   and `references/tests.md` load when the skill is used.
6. **The A/B** is the command in the brief with `--batch a1-reference`. It is the live step, and it
   has not been captured yet: the report (`work/ab-report.md`) carries pending markers, and
   `work/live/README.md` holds the exact commands and the pending marker where the captured files
   go.

## Design choices

- **Rule tags as the unit of coverage** (course design). A1 names coverage and cross-links as the
  checks a single blob cannot have: "A single blob doesn’t lend itself to mechanical checks
  (coverage, freshness, ownership, cross-links), so drift is inevitable." (A1, F-a-26). Tags make
  coverage countable; the overlap floor stops an id list from passing as coverage.
- **Overlap on content words, threshold 0.5** (course design). Deterministic, needs no model, allows
  rewording, and catches a rule cut down to its first sentence (the brief's example: R1.1 copied
  without its second sentence keeps 41% of its content words). The stopword list is fixed in the
  starter so that the learner's checker and the grader's reference agree on every count.
- **Workspace overlay for link resolution.** `InstructionsLayer.prepare_workspace` copies the tree
  onto the arm's workspace root (`src/shipharness/harness/instructions/layer.py`), so a link from
  `docs/product-specs/index.md` to `../features/` is correct when it resolves in `teamtrack/`. The
  checker resolves in the tree first, then at the same path in the product.
- **Code-span paths are checked too.** The course's own map points with code spans
  (`teamtrack/harness/instructions/AGENTS.md`), so a checker that reads only Markdown links would
  miss most pointers.
- **No new facts** (DESIGN §6.1, applied to the learner's tree). The bare arm reads
  `docs/HANDBOOK.md` and the code; every fact in the original comes from one of the two. Requiring
  each code span of the tree to appear in the original, or to be an existing path, keeps the A/B a
  test of organisation, not of extra information.
- **Error lines an agent can act on.** "write ERROR and put the reason on the same line so grep will
  find it" (A4, F-a-132); the self-check's FAIL lines say what to fix, following A1's remediation
  messages (F-a-97).
- **Grader.** Visible checks are shared with the self-check (`assignment/check.py`), so the two never
  disagree. Hidden checks add: coverage measured by the reference checker; a pinned SHA-256 of the
  original (editing it zeroes criterion B); the unchanged visible tests against the learner's
  checker; the learner's checker on the reference tree and on three injected faults; and the eleven
  hidden cases. Hygiene points scale with coverage and "clean" points need at least one detected
  fault, so an empty tree or a checker that reports nothing scores near zero (the starter scores 1.8).
- **Report graded by structure.** The brief forbids re-running models in grading. The structure
  checks enforce what DESIGN §8.3 asks of every A/B: counts, not percentages, one primary measure
  (R1, DESIGN §8.2) reported per arm, the budget. `--allow-pending` exists only so the reference can
  reach 100 before its live run is captured; learners are graded without it.
- **The A/B is the required live step** (course design, owner decision). The learner submits what
  the run wrote: the experiment exports, the ScoreRecord of every run (`exports/scores/`), the
  harness arm's run logs, and the command with its output. `assignment/live_evidence.py` collects
  them into `live/` and holds the checks, so the self-check and the grader (criterion F, 12 points)
  apply the same rules. The checks validate files only: the ScoreRecord schema with every field
  present, events against the event models, run ids and tasks against the command and the
  `section-1` split of `datasets/teamtrack-features-v1.jsonl`, `gpt-6-luna` (export metadata, the
  run logs' `run_start` and `cost` events, the cost line), `recorded` false, `sandboxed` true, and
  the caps of CONTRACTS §1. Missing or malformed evidence zeroes all of F.
- **Proof that the learner's tree was used.** `ScoreRecord` names the layers, not the tree, so the
  check reads the run log instead: `InstructionsLayer.prepare_workspace` writes one
  `harness_decision` note per harness run, "placed N instruction files", whose `paths` are the files
  it copied from `teamtrack/harness/instructions/`. Every harness log must list exactly the files of
  the submitted `instructions/` tree. The course's own tree (one skill, `add-endpoint`) fails this.
- **The report checked against the evidence.** The report's command, runs per arm, R1 and R3 counts,
  and links must equal what the score records and exports say, so the numbers can no longer be typed
  by hand without losing points (criterion F, `live-report`).
- **Points for F** come from criteria whose weight the live evidence now covers or that had slack:
  E A/B report 15 to 10 (its counts are now cross-checked in F), D hidden cases 14 to 10, C Skill 15
  to 12. The totals stay at 100.
- **`ab_summary.py` reads only `exports/`**, as `make report` does (DESIGN §12), so the numbers in a
  report come from the score records and never from memory.

## Alternatives considered

- **Coverage by id only.** Rejected: a list of 66 ids in one file would pass.
- **Semantic similarity with embeddings or a model judge.** Rejected: needs keys, costs money, and is
  not reproducible; the self-check must run with no keys.
- **Verbatim statements.** Rejected: it forbids the rewording that makes focused documents readable.
- **A third arm with the 900-line file injected as `AGENTS.md`.** It would separate "instructions in
  context" from "instructions organised", but it doubles the A/B cost beyond A1's $2.50 (DESIGN
  §11.5), and `shipharness experiments` compares a bare arm with a harness arm only. The two-arm A/B
  compares the bare arm, which has the same facts in `docs/HANDBOOK.md` on disk, with the restructured
  tree in context.
- **One skill per house rule.** Rejected for the assignment: the brief asks for one skill, and B1's
  progressive disclosure favours one well-described skill over several overlapping descriptions.
- **Checking orphans in the checker.** Kept in the self-check instead (`map-reach`): reachability is
  a property of the map, while the checker's job is broken pointers and lost rules.

## Trade-offs

- The overlap floor is lenient by design: a rule can keep half its words and still lose its point
  ("404" kept, "never 403" dropped). The README's common mistakes say so; reviewers still read.
- The code-span path rule skips anything with a space or a colon, so a wrong command in a code span
  is not caught. Checking commands would need running them.
- The fixed stopword list makes overlap values identical across implementations but is English-only
  and small.
- Grading from files cannot prove that the files came from a real run: a learner could edit JSON by
  hand. The checks make that much more work than running the A/B (48 consistent records, 24 run
  logs, checkpoint SHAs that match the tags), and the experiment URLs in the exports can be opened
  in LangSmith by the instructor.
- The tree check compares file lists, not file contents, because the placement note lists paths
  only. An edit inside a document after the run is not detected; adding or removing a document is.
- R-L2 asks for all 24 runs per arm. If `MAX_BATCH_COST_USD` stops the command early, the
  learner keeps the shorter batch (dropping runs is forbidden) and loses part of `live-command`.

## Known limits

- The anchor rule follows GitHub for ASCII headings; headings with non-ASCII punctuation may slug
  differently on other renderers.
- Reference-style links are checked only through their definitions (`[label]: target`); a
  `[text][label]` with no definition is not reported.
- The hidden-case outcome lists failing case names in the grader output, which hints at the area of
  a bug without showing the fixture.
- The reference A/B has not been run. Results, cost, time, and trace counts (the captured files go
  in `work/live/`, see the marker in `work/live/README.md`):

[[PENDING: R1 and R3 runs-failing counts per arm for the reference tree on section-1, k=3 | source: M8 batch 1 | how: uv run python submodules/01-instructions/assignment/ab_summary.py --batch a1-reference]]

[[PENDING: measured cost, wall time, and LangSmith trace count of the a1-reference A/B | source: M8 batch 1 | how: uv run shipharness experiments --split section-1 --k 3 --layers instructions --batch a1-reference]]

## Captured output

Real output of the commands below, captured on 2026-10-16 in the M7 worktree, is in `captured/`:

| File | Command |
|---|---|
| `captured/self-check-starter.txt` | `uv run python submodules/01-instructions/assignment/check.py` |
| `captured/self-check-solution.txt` | `uv run python submodules/01-instructions/assignment/check.py --work submodules/01-instructions/solution/work --allow-pending` |
| `captured/grade-starter.txt` | `uv run python submodules/01-instructions/solution/grader/grade.py` |
| `captured/grade-solution.txt` | `uv run python submodules/01-instructions/solution/grader/grade.py --work submodules/01-instructions/solution/work --allow-pending` |
| `captured/grade-solution-no-pending.txt` | the same without `--allow-pending` |
| `captured/checker-solution.txt` | the reference checker on the reference tree |
| `captured/tests.txt` | the grader tests (run with `-n 2`) and the checker tests |

Summary: the self-check passes 0 of 24 checks on the starter and 24 of 24 on the solution; the
grader gives the starter 1.8/100, the solution 100.0/100 with `--allow-pending`, and 83.0/100
without it (no live evidence yet). The grader tests also grade a SYNTHETIC submission (the
reference work folder plus invented live evidence from `grader/tests/synthetic_live.py`), which
scores 100 without `--allow-pending`; that is a test fixture, not a run.
