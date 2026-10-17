# Option A: the course story, drafted

Status: draft for the owner, not applied (2026-10-17, branch `option-a`). Owner decision: "Regardless
of the outcome: prepare the course story for option A ('a harness encodes assumptions about the model;
measure each piece, keep what earns its place'). Draft the slide and concepts changes but don't apply
them yet." This folder is private (`instructor/`), so it cites VERIFICATION.md (main, 6996508, section
"M6 pilot"). The proposed public text in [slides.md](slides.md) and `concepts-0N.md` states pilot facts
in words and cites no private file.

## The storyline (proposed)

**Problem.** In a multi-tenant service, agent-written features fail in specific ways: another org's data in a response, a second session that redoes or breaks the first, edits
outside the ticket, and the agent's own tests passing while the behaviour is wrong. The sources give
four causes (A1, F-a-05; A2, F-a-08; cause 3 side by side, A1 F-a-20, A4 F-a-18, F-a-19, A5 F-a-86;
A3, F-a-15 with B13, F-b-45).

**The harness and the claim.** A harness is the environment around the agent (A1, F-a-02),
taught in four parts. The course claim: a harness encodes assumptions about the model; measure each
piece, keep what earns its place. The first half is A3's: "every component in a harness encodes an
assumption about what the model can't do on its own, and those assumptions are worth stress testing"
(A3, F-a-124). So is the method: "removing one component at a time and reviewing what impact it had
on the final result." (A3, F-a-125). A3 dropped context resets once Opus 4.5 no longer needed them
(F-a-69) and keeps its evaluator only "when the task sits beyond what the current model does reliably
solo" (F-a-123). Pieces cost turns and money (A3, F-a-68, F-a-152). "Keep what earns its place" is
course framing.

**What the pilot measured.** One pre-registered primary measure per section, three A/Bs per run. In
runs 3 (effort medium) and 4 (effort low): no measurable difference on this task with this model in
any section (F4 from run 3 only, both arms failing 3 of 3). Post hoc, over 34 arm runs per arm,
described and not tested: files changed outside the allowed paths in 0 harness runs against 9 bare
(the scope layer ran only in F3 and F4); done claimed in 10 against 19, none with failing hidden
tests; tests shipped, median 2.5 against 7.5; arm wall time, median 302 s against 190 s; cost per arm,
median $0.0123 against $0.0103.

**How each section teaches it.**

- S1: the map assumes the model will not apply a rule it has not been pointed to (A1, F-a-05,
  F-a-28). The bare arm read the handbook and copied no leak. Round 5 sets the map against one
  monolithic file (A1, F-a-23).
- S2: state files assume a fresh session cannot pick up from the repository (A2, F-a-08). The bare
  arm resumed from `git status`; the harness wrap-up led to two early finishes in run 3. Round 5 fixes
  that and adds a round-only measure.
- S3: allowed paths assume the agent leaves the ticket unless code stops it. On F3 the bare arm never
  did; on F4 it did in 6 of 6 runs, post hoc, against 0 of 6 with the scope layer.
- S4: the gate assumes the agent's "done" cannot be trusted (A3, F-a-15). Post hoc, no done claim
  came with failing hidden tests; on F4 the harness arm never called `finish`, so its gate never ran.
  Round 5 gives both arms more time.

## Evidence for the numbers

| Number | Where (VERIFICATION.md, M6 pilot) | A/Bs |
|---|---|---|
| No measurable difference, F1-F3 runs 3 and 4, F4 run 3 | "Run 3", "Run 4", "Gate decision" | run 3: F1 `ab-20261016-211419-07937b`, `-212745-2c14fb`, `-214636-c8b3c4`; F2 `-211419-dfe06f`, `-213317-9a0ec1`, `-214959-de790f`; F3 `-212115-a361f5`, `-213624-d7eb13`, `-215443-f2c188`; F4 `-212252-aa1644`, `-214151-ca9841`, `-220010-c5b4bf`. Run 4: F1 `-232842-b372c2`, `-233807-3f34fa`, `-234639-4a18bd`; F2 `-232842-ac03b2`, `-234027-226a76`, `-235211-ea59a9`; F3 `-233517-2c9ea4`, `-234509-8b9bfa`, `-235305-723a0f` |
| Post hoc counts and medians (34 arm runs per arm) | "Exploratory analysis of the 94 pilot arm runs", rows "All bare", "All harness" | runs 2-4 and the live console check (`ab-20261016-210339-909651`); run 2 A/Bs: F1 `ab-20261016-181736-a07558`, `-183644-0036f0`, `-185628-37483b`; F2 `-181736-08a9c4`, `-184318-636e90`, `-190548-ae9abe`; F3 `-182624-6403f7`, `-184452-134b15`, `-190948-4054b5`; F4 `-182828-c81fc0`, `-185422-8a8c2a`, `-191626-6100f6` |
| F4 out of scope 6 of 6 bare, 0 of 6 harness | same section, rows "F4 bare", "F4 harness" | run 2 and run 3 F4 A/Bs above |
| Run 3 F2 early finishes | "Run 3", F2 harness row | `ab-20261016-213317-9a0ec1`, `ab-20261016-214959-de790f` |

## Research support (RESEARCH.md and research/notes/R-a.md)

| Part of the claim | Support | Status |
|---|---|---|
| Each piece encodes an assumption about the model | A3, F-a-124 (quote above) | Direct |
| Measure each piece by taking it out | A3, F-a-125; the course's `LAYERS=-<layer>` and the M8 ablation already cite it | Direct |
| Assumptions change with the model | A3, F-a-69 (resets dropped for Opus 4.5); RESEARCH §5 correction 4 and R-a correction 9 (sprint construct removed for Opus 4.6; no finding id of its own, so not cited in public text) | Direct (F-a-69) |
| A piece is worth keeping only where the model needs it | A3, F-a-123 (the evaluator) | Direct for one component |
| Pieces have a cost | A3, F-a-68 (resets), F-a-152 (harness over 20x more expensive) | Direct |
| Test against your own model | A3, F-a-126 ("experiment with the model you're building against, read its traces") | Direct |
| Pieces are added after observed failures | A1, F-a-44; A4, F-a-128 | Direct |
| One repository's result does not generalise | A1, F-a-143 | Direct (A1's caveat about its own results) |
| A fresh session recovering state from files | A6, F-a-76 (supplementary, about Claude models; the pilot model is not one) | Supplementary |

Course framing, with no source: the phrase "keep what earns its place" and the rule of dropping a
piece that shows no effect; using a pre-registered bare-against-harness A/B per section as the test;
the one-line assumption named for each section (S1 to S4 are course labels); reading the pilot's
result as a statement about this model and these tasks.

## Files that would change

| File | Change |
|---|---|
| `slides/outline.md` | 21 slides change content, 1 new slide (68, "What the pilot measured"), 2 change timing only (65, 67), wrap-up renumbered 69-73; slide 2's screenshot slot removed. See [slides.md](slides.md) |
| `submodules/01-instructions/concepts.md` ... `04-verification/concepts.md` | New closing section per file ("What the piece assumes, and what the pilot measured"); pilot material moved there and cut. Words now 3,182, 3,416, 3,219, 3,138; after 3,076, 3,092, 3,136, 3,146 (counted by applying each draft to a copy). See `concepts-0N.md` |
| `submodules/0N-*/session-notes.md` (4 files) | "Key ideas": one item naming the piece's assumption (A3, F-a-124); "What the A/B showed": the post hoc counts for the section and the round 5 slot; one common question ("The harness did not win. Was it useless?") |
| `README.md` | Tagline (line 3-4); §3 adds the claim with F-a-124 and F-a-125; §4 "How the course proves it" becomes "How the course measures it", with the pre-registered outcome rule and a three-line pilot summary |
| `DESIGN.md` (integrator) | Title line 4 and §1 "How we prove it", same wording as README |
| `instructor/run-sheet.md`, `docs/instructor-guide.md` | "How we prove it" (run sheet line 35, guide line 44) reworded; final-block timings for slides 64-68; guide line 260 (slide 2 screenshot slot) removed |
| `submodules/0N-*/demo/README.md` (4 files) | Results sections: the post hoc counts next to the primary results, labelled post hoc; round 5 slot |
| `CHANGELOG.md` | One entry |

## PENDING items in these drafts

All with `source: M6 pilot | how: course pilot (build repository)`: round 5 results for F1 (bare
arm with one monolithic instruction file), F2 (early-finish fix; round-only measure "continuity AND
at least 50% of hidden tests"), F4 (longer agent time limit for both arms; test-phase findings); the
pooled "what the pilot measured" slide's round 5 row. Existing M8 markers stay unchanged.

## Found while drafting

1. VERIFICATION.md (exploratory analysis) says "The scope layer's effect is visible on F2 and F4".
   The demo-2 harness arm runs instructions and state only (`SECTION_STACKS` in
   `src/shipharness/ab/demo.py`), so F2's 0 of 9 is not the scope layer's effect. The drafts
   attribute only F4 (demo-4, all four layers) to it. Suggest correcting that line.
2. A section A/B compares the stack so far against bare, not one piece: demo-2 adds state on top of
   instructions. Only the leave-one-out ablation measures one piece (A3, F-a-125), and the gate did
   not pass, so M8 has not run. The drafts say this plainly.
3. Slide 2's slot (a bare F1 run with other-org marks, source M6 pilot) cannot be filled: no bare F1
   arm had a new R1 violation in runs 2-4 or the console check. The draft removes it.
4. Run logs (read-only, `events.jsonl` of the six F4 A/Bs of runs 2 and 3): the harness arm never
   called `finish`, and its only verify decisions are the gate baseline and the test-filter summary,
   so the verify gate never ran on F4 in the pilot. The single `finish` call is the bare arm's in
   `ab-20261016-220010-c5b4bf`. VERIFICATION does not state this yet.
5. Every concepts.md is already above 3,000 words (3,182; 3,416; 3,219; 3,138), so each draft cuts
   more than it adds.
