# Option A: changes to submodules/01-instructions/concepts.md

Draft, not applied. Line numbers refer to the file at 67cfb3c. Each change gives what changes, the
proposed text between `proposed` markers (public wording, ready to paste), and what stays. Word count:
3,182 now; 3,076 after these changes (counted by applying them to a copy).

What stays: the note on labels, §1 up to the handbook paragraph, §2 (two paragraphs shortened), §3,
§4.1 to §4.3, §4.4 (shortened), §4.6, §5.1 to §5.3, §5.5, and the Sources line. The pilot material
moves from §1 and §5.4 into a new §6.

## Change 1. Opening paragraph (lines 5-9): replace

Adds the closing question every section now answers.

<!-- proposed replace 5-9 -->
This section follows one order: the problem the task sets, the cause (cited), the harness piece, how
`shipharness` implements it, what the A/B measures, and, last, what the piece assumes about the model
and what the course pilot measured. Source IDs (A1, B1, ...) and finding IDs (F-a-NN, F-b-NN) are
listed in [REFERENCES.md](../../REFERENCES.md), which is generated when the course is released. Code
excerpts come from the walkthrough anchors `S1:agents_md`, `S1:progressive`, and `S1:prefix`; print
one with `uv run python scripts/anchors.py extract S1:prefix`.
<!-- /proposed -->

## Change 2. Section 1 heading (line 18): replace

The bare arm did not show the failure in the pilot, so the heading no longer says it did.

<!-- proposed replace 18-18 -->
## 1. The problem the task sets
<!-- /proposed -->

## Change 3. Section 1, the two pilot subsections (lines 51-82): replace

The run-by-run pilot results move to §6. §1 keeps one pointer.

<!-- proposed replace 51-82 -->
The course pilot did not see this failure in any run, on the canonical ticket or on its trap variant;
section 6 gives the results and what they say about the map.
<!-- /proposed -->

## Change 4a. Section 4.4 (lines 264-267): replace

Shorter; the walkthrough shows the file.

<!-- proposed replace 264-267 -->
The anchor covers lines 1-38 of the 94-line `teamtrack/harness/instructions/AGENTS.md`: the opening,
the "Where to look" table, and the house rules at a glance. All 94 lines are in the prefix.
<!-- /proposed -->

## Change 3a. Section 2.1, first paragraph (lines 90-93): replace

Keeps A1's core sentence (F-a-05); F-a-07 says the same about discoverability and stays in the
post-class reading.

<!-- proposed replace 90-93 -->
A1 states the core point: "From the agent’s point of view, anything it can’t access in-context while
running effectively doesn’t exist." (A1, F-a-05).
<!-- /proposed -->

## Change 4. Section 2.2, second paragraph (lines 104-107): replace

Shorter; S3 carries the full side-by-side citation of cause 3.

<!-- proposed replace 104-107 -->
The course's cause 3 has no single source sentence; its sources stand side by side in S3. S1 uses only
A1's pattern copying (F-a-20), for the trap.
<!-- /proposed -->

## Change 5. Section 4.5, the sequence diagram (lines 269-288): delete

The table in §4.1 already lists the three hooks; the diagram repeats it. It can move to the
post-class reading unchanged.

<!-- proposed replace 269-288 -->
<!-- /proposed -->

## Change 6. Section 4.6 heading (line 289): renumber

<!-- proposed replace 289-289 -->
### 4.5 What the bare arm gets
<!-- /proposed -->

## Change 7. Section 5.4, results (lines 334-353): delete

Its table and the three M8 markers move into §6.

<!-- proposed replace 334-353 -->
<!-- /proposed -->

## Change 8. Section 5.5 heading (line 355): renumber

<!-- proposed replace 355-355 -->
### 5.4 What this A/B cannot tell you
<!-- /proposed -->

## Change 9. New section 6, after line 363: insert

<!-- proposed insert 363 -->
---

## 6. What the map assumes, and what the pilot measured

A3 gives the test every harness piece should face: "every component in a harness encodes an
assumption about what the model can't do on its own, and those assumptions are worth stress testing"
(A3, F-a-124). The map's assumption, in the course's words: the model will not apply a rule it has
not been pointed to. Its basis is A1's point about context (A1, F-a-05, F-a-28).

### 6.1 The primary measure

Measured in the course pilot: gpt-6-luna at the same effort for both arms, three A/Bs per run. Runs
failing the primary measure (one or more new R1 violations), per arm:

| Run | Ticket, effort | Bare | Harness | A/Bs |
|---|---|---|---|---|
| 2, 2026-10-16 | `F1-canonical`, medium | 0 of 3 | 0 of 3 | `ab-20261016-181736-a07558`, `ab-20261016-183644-0036f0`, `ab-20261016-185628-37483b` |
| Live console check, 2026-10-16 | `F1-canonical`, medium | 0 of 1 | 0 of 1 | `ab-20261016-210339-909651` |
| 3, 2026-10-16 | `F1-trap`, medium | 0 of 3 | 0 of 3 | `ab-20261016-211419-07937b`, `ab-20261016-212745-2c14fb`, `ab-20261016-214636-c8b3c4` |
| 4, 2026-10-16 | `F1-trap`, low | 0 of 3 | 0 of 3 | `ab-20261016-232842-b372c2`, `ab-20261016-233807-3f34fa`, `ab-20261016-234639-4a18bd` |

Every arm passed 52 of 52 hidden tests; run ids are in [demo/README.md](demo/README.md) section 7.
No measurable difference on this task with this model (course pilot, runs 3 and 4).

### 6.2 Why the assumption did not hold here

On the canonical ticket the bare arm was pointed to the rule anyway. The ticket ends "Follow the house
rules in docs/HANDBOOK.md"; every bare arm in run 2 opened the handbook with its third tool call; and
`read_file` returns up to 400 lines (`src/shipharness/runner/tools.py`), so the whole 150-line
handbook was in context before any code was read. The trap ticket `F1-trap` names
`app/api/legacy_v1.py` as the place where "a lot of the query code exists" and does not mention the
handbook (`datasets/teamtrack-features-v1.jsonl`); still, no arm copied the legacy query. For this
model and these tickets, the map had nothing to fix.

### 6.3 Post hoc: what else the arms did

These measures were chosen after the results were known, so they describe and do not test (10 runs
per arm: runs 2, 3, and 4 and the console check). Harness arms claimed done in 5 runs, bare arms in 9;
no claim was false in either arm. Median cost per arm was $0.0122 against $0.0103, and median arm
wall time 168 s against 177 s; neither arm hit the agent time limit. The map cost little here and
changed nothing the referee measures.

The A/B does not measure everything a map is for. A1's case against one large file includes that it
"rots instantly" and "doesn’t lend itself to mechanical checks" (A1, F-a-25, F-a-26); those are
reasons about the people who maintain the rules, not about one run.

### 6.4 What the next round tests

A1's comparison is a map against one giant instruction file (A1, F-a-23, F-a-24), not against a
handbook on disk (section 5.4). The course's next pre-registered pilot round, round 5, gives the F1
bare arm the same rules as one monolithic instruction file instead of a map.

[[PENDING: F1 round 5 result, runs failing out of k per arm (r1_new_violations>=1), bare arm with the rules as one monolithic instruction file, with A/B ids and run ids | source: M6 pilot | how: course pilot (build repository)]]

[[PENDING: S1 dots for F1 canonical, runs failing out of k per arm (r1_new_violations>=1), with run ids | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: secondary counts for F1 canonical per arm (r1_leaks, r3_new_failures, hidden passed of 52) | source: M8 batch 1 | how: uv run shipharness report]]

[[PENDING: ablation result for the leave-out-instructions configuration (all minus instructions) on the 12 ablation tasks | source: M8 ablation | how: uv run shipharness report]]

On your own repository, keep the map where a measure on your model shows it earns its place, or for
the maintenance reasons above; say which.

<!-- /proposed -->

## Change 10. Check your understanding, question 4 (lines 373-374): replace

<!-- proposed replace 373-374 -->
4. In the pilot the bare arm passed F1 in every run. Which assumption of the map did that test, and
   what does round 5 change?
<!-- /proposed -->

## Evidence (private)

| Statement | VERIFICATION.md (main), M6 pilot |
|---|---|
| Run 2 F1 3/3 both arms | "Run 2" table, F1 rows |
| Console check both arms passed, 52/52 | "Live console check (2026-10-17)" |
| Run 3 F1 trap 3/3 both | "Run 3" table; "Gate decision" |
| Run 4 F1 trap 3/3 both, hidden 52 of 52 | "Run 4" table |
| Third tool call, no arm opened `legacy_v1.py` | run 2 logs, already in the current §1 (lines 55-58) |
| Claimed done 5/10 and 9/10, false 0/5 and 0/9, cost, wall, time limit | "Exploratory analysis", rows "F1 bare" and "F1 harness" |

The 52-of-52 statement for run 3 harness arms comes from the current concepts table (score records);
VERIFICATION's "Run 3" row says "same" for the harness arm.
