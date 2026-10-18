# Run sheet: Module 1 live class (240 minutes)

Minute-by-minute plan for "Module 1: Harness Engineering for Coding Agents": commands, console
screens, what to say while each run is going, and, in the sections marked "Fallback" at the end, the
known failure modes with their exact messages and the replay procedure. Sources: DESIGN §13
(screens) and §14.1 (schedule); VERIFICATION.md, "Class plan per section" (every demo section live,
owner message 7) and "S3 confirmation: result" (Section 3 becomes a live A/B, owner message 9); measured
times and costs from the demo runs measured 2026-10-18 (docs/evidence/general.md, "Demo runs after
the speed-up"). Commands are the Makefile targets as they exist in the repository (`make -n` checked).

Status: final for the class plan. Every demo step launches or shows a live run;
`platform/tests/unit/test_run_sheet_live.py` fails if a replay or a constructed example enters a demo
step.

Companion files: [code-walkthrough.md](code-walkthrough.md) (anchors and talking points),
[poll-questions.md](poll-questions.md) (the one poll, at the start of Section 4), [fallbacks.md](fallbacks.md)
(fallback recordings, replay, and the optional extras),
[review-session-guide.md](review-session-guide.md) (Thursday review), and the class deck
[Harness Engineering for Coding Agents.pptx](../slides/Harness%20Engineering%20for%20Coding%20Agents.pptx),
with its speaker notes in the deck (slides are named below by their title, such as "DEMO - 1"). The
public one-page version with the class-day cheat sheet is
[../docs/instructor-guide.md](../docs/instructor-guide.md).

---

## The story this class tells (open with it)

- **Problem.** Teams hand features to coding agents. In a multi-tenant service the failures are
  specific: an endpoint returns one customer's data to another, a second session redoes or breaks
  the first session's work, the agent edits files it was never asked to touch, and its own tests pass
  while the behaviour is wrong (DESIGN §1).
- **Why it happens.** (1) "From the agent’s point of view, anything it can’t access in-context while
  running effectively doesn’t exist." (A1, F-a-05) (2) "each new session begins with no memory of
  what came before." (A2, F-a-08) (3) Agents copy existing patterns and can take actions that are
  hard to undo; cite A1 (F-a-20), A4 (F-a-18, F-a-19), A5 (F-a-86), and A6 (F-a-21, supplementary)
  side by side, never merged into one claim (RESEARCH G-1). (4) "agents reliably skew positive when
  grading their own work" (A3, F-a-15), and visible tests miss what held-out tests catch (B13,
  F-b-45, F-b-50).
- **Solution.** A harness: the environment around the agent. A1 describes the work as "design
  environments, specify intent, and build feedback loops" (A1, F-a-02); A1 never defines "harness
  engineering", so the course attributes no definition to it (RESEARCH G-2). Four parts: Section 1: Instructions, Section 2: State and sessions, Section 3: Scope and sandbox, Section 4: Verification.
- **The claim.** A harness encodes assumptions about the model; measure each piece, keep what earns
  its place. The first half is A3's: "every component in a harness encodes an assumption about what
  the model can't do on its own, and those assumptions are worth stress testing" (A3, F-a-124). The
  method is A3's too: "removing one component at a time and reviewing what impact it had on the final
  result." (A3, F-a-125). "Keep what earns its place" is course framing; say so.
- **How we measure it.** Same agent, model, effort, task, repository, tools, sandbox, turn limit, and
  cost cap, with and without the harness, judged by the same deterministic referee on what ships. One
  primary measure per section, registered before any run; a section without a gap is reported as "no
  measurable difference on this task with this model" (DESIGN §8, §10.4).
- **What the runs before class found.** On each section's own task, no section showed the harness
  arm ahead: runs 3 (effort medium) and 4 (effort low) and the class-profile round all report "no
  measurable difference on this task with this model", and the pre-registered gate did not pass
  (VERIFICATION.md, "Gate decision", "Class-profile round"). One pre-registered confirmation did show
  a gap: on the Feature 4: Version checks on issue edits ticket, every bare arm changed `app/services/errors.py`, outside the allowed
  paths, and the scope layer blocked that edit in every harness arm (bare 0 of 3 passing, harness 3
  of 3; VERIFICATION.md, "S3 confirmation: result"). That is why Section 3 runs a live A/B. Say all of it in
  the opening and show it in every section. The harness does not have to win; every result is
  reported as measured.

---

## The class plan per section

Every demo section is live (VERIFICATION.md, "Class plan per section", revised under owner message
7). The rule: a live A/B only where the data shows a real gap; otherwise harness in action. Section 1, Section 2,
and Section 4 run `make show-N`: the harness arm alone, live, with the live referee checks and the live
console, showing the layer doing its job. Section 3 runs a live A/B, `make demo-3 FEATURE=version-checks`, because the
pre-registered Section 3 confirmation came out "harness ahead" (VERIFICATION.md, "S3 confirmation:
result"). The final runs `make final`, the class's measurement lesson. Each section's run launches
at the section start, so it has the whole section to finish before the DEMO slide. The class has
one poll, a Live Zoom Poll at the start of Section 4 (2:55-2:57) that picks the final feature right before
the two Section 4 launches. Recorded showcases and
constructed examples are optional extras, listed in `docs/extras.md` and in
[fallbacks.md](fallbacks.md); they are never part of a demo block. A replay is the emergency fallback
only ([Fallback: replay procedure](#fallback-replay-procedure)).

| Section | Live run |
|---|---|
| Section 1 | `make show-1`: Feature 1: Org-wide issue search, instructions layer; watch the agent read the map, then only the documents the ticket needs |
| Section 2 | `make show-2 SESSION_BUDGET=12,38`: Feature 2: Comments on issues, instructions and state; session 1 stops at its 12-turn budget, the handoff is written, session 2 (38 turns) resumes from it |
| Section 3 | `make demo-3 FEATURE=version-checks`: live A/B on the Feature 4 ticket; harness arm with instructions, state, scope; watch the bare arm change `app/services/errors.py` and the scope layer block the same edit in the harness arm |
| Section 4 | `make show-4`: Feature 4, all four layers; the gate, the test phase, the filters |
| Final | One live A/B: `make final FEATURES=<winner>,<runner-up>` from the poll at the start of Section 4, launched with show-4 at 2:57; one A/B is one dot, read against the dots from before class |

`make show-2 SESSION_BUDGET=12,38` runs the pilot's lever: a 12-turn first session, then 38 turns
(the task's own budget is 20 and 30, `platform/teamtrack/reference/f2/task.toml`).
`make -n show-2 SESSION_BUDGET=12,38` prints `--session-budget=12,38`.

`make demo-3 FEATURE=version-checks` runs `shipharness ab --section demo-3 --feature version-checks
--profile class` (the CLI turns the readable name into the code): the Section 3 layer stack (instructions, state,
scope) on the Feature 4 canonical ticket, the exact setup of the Section 3 confirmation. The Makefile default is
`FEATURE ?= safe-retries`, so always pass `FEATURE=version-checks`.

Label, every time: a show-N run is "harness in action, not an A/B: its score stays out of every
bare-vs-harness comparison". The console shows the purple `HARNESS IN ACTION — one arm, not an A/B`
badge on every screen. The Section 3 A/B and the final have no badge: both arms run.

### Every result, on one slide and one console view

Each section's demo block ends on its "What we measured" slide and on console screen `4`. Say the result
plainly. Primary measure passed, bare / harness (VERIFICATION.md, "Run 3", "Run 4", "Gate decision",
"Class-profile round", "S3 confirmation: result"):

| Section | Run 3, effort medium (k=3) | Run 4, effort low (k=3) | Class-profile round (k=1) | Classification |
|---|---|---|---|---|
| Section 1 Feature 1 `trap-legacy-pattern` | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-084558-0356a0`) | no measurable difference |
| Section 2 Feature 2, session budget 12, 38 | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-085139-7c0661`) | no measurable difference |
| Section 3 Feature 3: Safe retries for issue creation `trap-tempting-middleware` | 3/3, 3/3 | 3/3, 3/3 | 1/1, 1/1 (`ab-20261017-090051-91f837`) | no measurable difference |
| Section 4 Feature 4 canonical | 0/3, 0/3 | not run (pilot cap) | 0/1, 0/1 (`ab-20261017-090903-926c02`) | no measurable difference (both arms fail) |

Section 3 confirmation (pre-registered in DESIGN §10.4 before any of its runs; Feature 4 canonical, Section 3 stack,
class profile with the 420 s agent time limit, k=3; primary measure for this confirmation only:
one or more out-of-scope files in the shipped diff fails): bare 0/3, harness 3/3, **harness
ahead**. A/Bs `ab-20261017-150928-96cf3a`, `ab-20261017-150948-cf151f`, `ab-20261017-152601-3a7237`.
Every bare arm changed `app/services/errors.py`; every harness arm got "app/services/errors.py:
outside the allowed paths for the build phase". The harness arms ended "ABORTED: timeout" on the
harness's own 120 s limit (`HARNESS_TIMEOUT_S`), each after shipping a change. Feature 4's own measure (all
hidden tests and all mutants) failed in all six arms (hidden 62 to 68 of 69).

Say it honestly: the scope layer enforces the very thing this confirmation measures, so the harness
arm's zero is expected by construction. What the confirmation adds is that, on this ticket, the bare
agent went out of scope in all three runs (9 of the 10 A/Bs counted before class; it stayed in scope
in the live guide run of 2026-10-18, [s3.md](../docs/evidence/s3.md#s3-guide-run)).

Run 3 A/Bs: Feature 1 `ab-20261016-211419-07937b`, `-212745-2c14fb`, `-214636-c8b3c4`; Feature 2
`-211419-dfe06f`, `-213317-9a0ec1`, `-214959-de790f`; Feature 3 `-212115-a361f5`, `-213624-d7eb13`,
`-215443-f2c188`; Feature 4 `-212252-aa1644`, `-214151-ca9841`, `-220010-c5b4bf`. Run 4: Feature 1
`ab-20261016-232842-b372c2`, `-233807-3f34fa`, `-234639-4a18bd`; Feature 2 `-232842-ac03b2`,
`-234027-226a76`, `-235211-ea59a9`; Feature 3 `-233517-2c9ea4`, `-234509-8b9bfa`, `-235305-723a0f`.

Post hoc, and labelled so on the slide: measures chosen after the results were known, descriptive,
not tested, over 34 arm runs per arm from runs 2-4 and the live console check (VERIFICATION.md,
"Exploratory analysis of the 94 pilot arm runs"):

| Measure | Bare | Harness |
|---|---|---|
| Runs with a file changed outside the allowed paths | 9 of 34 (Feature 4 6 of 6, Feature 2 3 of 9) | 0 of 34 |
| Runs that claimed done | 19 of 34 | 10 of 34 |
| Done claims with failing hidden tests | 0 of 19 | 0 of 10 |
| Tests shipped, median | 7.5 | 2.5 |
| Arm wall time, median | 190 s | 302 s |
| Agent time limit hit | 4 of 34 | 9 of 34 |
| Cost per arm, median | $0.0103 | $0.0123 |

The Feature 4 out-of-scope count in this table (post hoc) is what led to the pre-registered Section 3
confirmation. The scope layer runs only in the demo-3 and demo-4 stacks. Never credit it for Feature 2's 0
of 9: the Feature 2 harness arm has no scope layer. On Feature 3 the bare arm never left scope either.

The planned experiment batches (the k=10 headline batch, the leave-one-layer-out ablation, the
control tasks) were not run, because the pre-registered gate did not pass.

---

## Before class (start 60 minutes early)

Everything runs inside WSL2 Ubuntu on the instructor's machine, in the repository folder (DESIGN
§9, D-22). `make warm` and the fallback recordings ran on T-1 with `PURPOSE=pilot` (public guide, "The
day before"). Step 1 is the class date: it happens here, at T-30, and not before.

| Step | Command | Expect |
|---|---|---|
| 1. Class date (T-30) | `sed -i "s/^SHIPHARNESS_CLASS_DATE=.*/SHIPHARNESS_CLASS_DATE=$(date +%F)/" .env`, then `grep '^SHIPHARNESS_CLASS_DATE=' .env` | The line shows today's date. Class runs trace to `shipharness-class-<date>` and share that day's $2.50 session |
| 2. Environment | `make doctor` | Every line `+ ok`, including `SHIPHARNESS_CLASS_DATE ... (class runs trace to shipharness-class-<date>)`; last line `result: + ready` |
| 3. Warm-up | `make warm` | Last line `warm: done (<seconds> s)`; seconds when nothing changed since T-1 (1.2 s in the class-profile round). Without the date it prints `x SHIPHARNESS_CLASS_DATE is not set: class runs need the class day (YYYY-MM-DD)` and `warm: nothing done`, exit 2: go back to step 1 |
| 4. Console | `make console` in terminal A (leave it running) | `Console: http://127.0.0.1:8765/` |
| 5. Browser | Open `http://127.0.0.1:8765/` | The run list (one card per run, newest first) and the key legend |
| 6. Fallbacks present | `ls .shipharness/runs/<id>/ab.json` for each fallback in [fallbacks.md](fallbacks.md) | One file per id |
| 7. Policy printout ready (Section 3) | `uv run python -c 'from shipharness.config import Settings; from shipharness.sandbox import default_policy, render_policy; print(render_policy(default_policy(Settings())))'` | Starts with `Sandbox policy (identical for both arms)` |
| 8. Assessment ready (opening) | `uv run python use-in-your-repo/skills/harness-setup/scripts/assess.py platform/teamtrack --out .shipharness/harness-assessment.html` | A summary per area, then one line per check, then `report: ...` |
| 9. Slides | Open the deck on its title slide | |

Do not run `make show-N`, `make demo-3`, or `make final` before class on the class date: the session
cost cap (`MAX_SESSION_COST_USD` $2.50, keyed by `SHIPHARNESS_CLASS_DATE`) is shared by every command
run under that date (DESIGN §11.1). `make warm` makes no model calls.

### Screen layout

| Window | Content |
|---|---|
| Terminal A | `make console` (quiet: only warnings and errors print; leave it alone) |
| Terminal B | The section command (`make show-1`, `make show-2 ...`, `make demo-3 FEATURE=version-checks`, `make show-4`), large font |
| Terminal C | `make final` only: launched at the Section 4 launch (2:57), read in the final block (3:40) |
| Browser tab 1 | Slides |
| Browser tab 2 | Console: the run list at `http://127.0.0.1:8765/`, then the current run at `/run/<id>` |
| Browser tab 3 | Console: the final A/B at `/run/<ab id>`, opened at the Section 4 launch and shown in the final block |
| Browser tab 4 (optional) | LangSmith, signed in, project `shipharness-class-<date>` (DESIGN §12) |

### Console keys (DESIGN §13; `platform/src/shipharness/console/static/stream.js`)

| Key | Screen | Shows |
|---|---|---|
| `1` | Live Console | Per arm: container line (id, network, CPU, memory, time left), cost against the run cap, turns, harness decisions, gate pills, the gate refusals ("Gate refused 'done' (build phase, attempt 1): ... → passed on attempt 2"), "Agent said" vs "Referee", and the "primary verdict ready: PASS" or "FAIL" pill with the time from launch (the final, with no primary measure: "verdict ready: PASS · judged on all checks"); a show-N run's bare arm reads "Not run (harness in action)" |
| `2` | Boards | Board screenshot per arm every 5 s, with marks (⚠ other org, ⧉ duplicate); Section 4 adds the two-tab conflict panel |
| `3` | Evidence | Files read and sessions ("Session 1 · N turns", then "Test phase · N turns"); diff map (✎ changed, ⊘ blocked) and sandbox denials; one row per referee check by plain name with its code in brackets (Files outside the allowed paths (`diff_scope`), Session continuity (`continuity`), Flaky tests (`flakiness`), Existing tests (`regression`), hidden tests, House rule N, board check); filter table, one row per test name; mutant table; the blinded reviewer's one-line reason |
| `4` | A/B Report | "Measured before class: N runs per arm": one dot per run from the course's records (`docs/evidence/scores/`), one row per feature, variant, and arm, with the new runs from `exports/` next to them; the Section 3 demo's rows are judged by files outside the allowed paths; records of an older referee version and harness-in-action runs are counted and left out |
| `5` | Traces | Live tail of events, first wrong turn per arm, trace links |
| `F` | | Cycles full screen for one arm: both, bare, harness |
| `H`, `Esc` | | Back to the run list; the "← All runs" link at the top left does the same |

Finding the current run: the command prints the run id only when it finishes. While it runs,
reload the run list and open the top card (newest first; each card shows the section, the
feature, "harness in action" or "A/B", "running" or "finished", and the start time). The run list
does not refresh by itself. In Section 4 two runs start together at 2:57: open each one right after its
own launch ([Section 4](#section-4-verification-255-340)).

---

## Minute-by-minute

Times are elapsed from the start of class. Slides are named by their title in the class deck,
[Harness Engineering for Coding Agents.pptx](../slides/Harness%20Engineering%20for%20Coding%20Agents.pptx).
Each section launches its live run on
its start slide, one minute in, so the run has the whole section to finish; the section teaches the
failure story and the four ideas while the run proceeds, then the DEMO slide walks through the
implementation notes and the finished run, then "What we measured" and the Q&A
([Section pattern](#section-pattern)). Two breaks: 10 minutes after Section 1, 5 minutes after
Section 3; Section 4 has 45 minutes. Section 3's live run is an A/B with both arms. The class has
exactly one poll, a Live Zoom Poll at the start of Section 4 (2:55-2:57), which picks the final
feature. Right after it, Section 4 launches `make show-4` in terminal B and `make final` in
terminal C, both at 2:57; the final block at 3:40 walks through the finished final A/B and starts no run.

| Time | Block | What happens | Command or screen | Slide |
|---|---|---|---|---|
| 0:00-0:03 | Opening: welcome | Title, instructor, welcome and chat, class structure, experience and support, success hacks, API key | | Opening slides |
| 0:03-0:05 | Opening: the repository | Clone and practice; the agentic loop recap; the agenda | | Clone & practice, agenda |
| 0:05-0:08 | Opening: the problem | What we are building, the problem in the real world, the challenge, why it matters, the four gaps, TeamTrack, house rules | Architecture diagram | The 4 gaps |
| 0:08-0:10 | Opening: how we measure | How we measure it and what the runs before class found; the glossary; `make doctor`; the `harness-setup` assessment; console tour (keys 1-5) | Terminal B, console tab | How we measure |
| 0:10-0:12 | Section 1 launch | Section 1 start slide: `make show-1` at 0:11; open the new run on screen 1 | Terminal B, console | Section 1 start |
| 0:12-0:20 | Section 1 story (run going) | Failure story and the Socratic reveal | | Failure story |
| 0:20-0:40 | Section 1 ideas (run going) | Four ideas, one slide each, then the cheat sheet; at 0:25 check terminal B for the `Cost:` line | Terminal B at 0:25 | Ideas, cheat sheet |
| 0:40-0:50 | Section 1 demo: implementation notes and the run | `S1:agents_md`, `S1:progressive`, `S1:prefix`; then the finished show-1 run: screens 1, 3, 5, and 2 | Editor, console | DEMO - 1 |
| 0:50-0:56 | Section 1 demo: what we measured | show-1's verdict on screen 1; the Section 1 row of the results; screen 4; when the layer earns its place; apply it Monday | Slides, console | What we measured |
| 0:56-1:00 | Section 1 Q&A | Questions; transition | | Q&A |
| 1:00-1:10 | Break | Return time on screen | | Break |
| 1:10-1:12 | Section 2 launch | Section 2 start slide: `make show-2 SESSION_BUDGET=12,38` at 1:11; open the new run on screen 1 | Terminal B, console | Section 2 start |
| 1:12-1:20 | Section 2 story (run going) | Failure story and the Socratic reveal | | Failure story |
| 1:20-1:40 | Section 2 ideas (run going) | Four ideas, then the cheat sheet; at 1:25 check terminal B for the `Cost:` line | Terminal B at 1:25 | Ideas, cheat sheet |
| 1:40-1:50 | Section 2 demo: implementation notes and the run | `S2:init`, `S2:stop_resume`, `S2:write`; then session stop and resume, the handoff: screens 1, 3, 2, and 5 | Editor, console | DEMO - 2 |
| 1:50-1:56 | Section 2 demo: what we measured | show-2's verdict on screen 1; screen 3 "Sessions"; the Section 2 row; screen 4; apply it Monday | Slides, console | What we measured |
| 1:56-2:00 | Section 2 Q&A | Questions; transition | | Q&A |
| 2:00-2:02 | Section 3 launch | Section 3 start slide: `make demo-3 FEATURE=version-checks` at 2:01, the live A/B (it takes the place of `make show-3`); open the new run on screen 1: two sandbox lines, one per arm | Terminal B, console | Section 3 start |
| 2:02-2:09 | Section 3 story (A/B going) | Failure story and the Socratic reveal | | Failure story |
| 2:09-2:28 | Section 3 ideas (A/B going) | Four ideas, including the sandbox boundary, then the cheat sheet; at 2:15 check terminal B for the `Cost:` line | Terminal B at 2:15 | Ideas, cheat sheet |
| 2:28-2:38 | Section 3 demo: implementation notes and the A/B | `S3:allowed_paths`, `S3:passes`, `S3:policy`, `S3:run_args`, `S3:dockerfile`; then screen 3 diff maps (bare ✎ changed, harness ⊘ blocked) and the Files outside the allowed paths (`diff_scope`) row; screen 1 harness decision ⊘ block with its reason; the sandbox moment | Editor, console | DEMO - 3 |
| 2:38-2:44 | Section 3 demo: what we measured | Out-of-scope files per arm, the measure on the screen 1 pill; Feature 4's hidden tests and mutants as secondary; what "by construction" means; the Section 3 rows; screen 4, before class bare 1/10, harness 10/10, plus tonight's dots | Slides, console | What we measured |
| 2:44-2:50 | Section 3 Q&A | Questions; read the session figure on the `Cost:` line for the final | Terminal B | Q&A |
| 2:50-2:55 | Break | Return time on screen | | Break |
| 2:55-2:57 | Live Zoom Poll: the final feature | Section 4 start slide, then the one poll of the class: bulk close, watchers, or labels; note the winner and the runner-up; close it before the launch | | Section 4 start, Live Zoom Poll |
| 2:57-2:59 | Section 4 launch | `make show-4` at 2:57 in terminal B, opened in browser tab 2; `make final FEATURES=<winner>,<runner-up>` at 2:57 in terminal C, opened in browser tab 3; back to show-4 on screen 1 | Terminals B and C, console | Section 4 start |
| 2:59-3:06 | Section 4 story (two runs going) | Failure story and the Socratic reveal | | Failure story |
| 3:06-3:22 | Section 4 ideas (two runs going) | Four ideas, then the cheat sheet; at 3:10 check terminal B (show-4) and terminal C (final) for their `Cost:` lines | Terminals B and C at 3:10 | Ideas, cheat sheet |
| 3:22-3:31 | Section 4 demo: implementation notes and the run | `S4:filters`, `S4:probe`, `S4:blind`, `S4:gate`; then test phase, filter table, gate pills, boards: screens 1, 3, 2, and 5 | Editor, console, tab 2 | DEMO - 4 |
| 3:31-3:37 | Section 4 demo: what we measured | show-4's "Agent said" against the referee on screen 1; hidden tests and mutants on screen 3; the Section 4 row; screen 4 | Slides, console | What we measured |
| 3:37-3:40 | Section 4 Q&A | One question, shortened; transition to the final A/B | | Q&A |
| 3:40-3:44 | Final A/B: arm lines | Terminal C: arm lines and the session figure | Terminal C | Reading the final A/B |
| 3:44-3:48 | Final A/B: screens | Screens 1, 3, 5, then both boards on screen 2, of the finished final A/B | Console, tab 3 | Reading the final A/B |
| 3:48-3:51 | Final A/B and all results | Screen 4: tonight's final next to the dots from before class; all results in one picture; `Final:dots`; which layer when | Console, slides | All results |
| 3:51-3:56 | Close: take it home | Use it in your repo (the kit and four skills, `shipharness init`, `Final:skill_template`); assignments; final project | | Use it in your repo |
| 3:56-4:00 | Close | The harness in one picture; Module 1 summary; Module 2; references; Q&A; thank you | | Thank you |

### How long the runs take

Measured 2026-10-18: three runs of each class command, after `make warm`, with `PURPOSE=pilot`, the
class profile (agent time limit 420 s, harness limit 900 s), two runs at a time on the class
machine, as in Section 4. `make show-1` ran before the harness speed-up of that morning, the others
after it (docs/evidence/general.md, "Verification runs after the rename" and "Demo runs after the
speed-up"; the show-1 run after the speed-up took 2:43 and 5:41). Times run from the make command's
launch; the console's own clock starts 10 to 20 s later. Each cell is the range over the three runs;
the command ends a few seconds after the last full verdict. The fallback is the first complete run
of each command after the speed-up ([fallbacks.md](fallbacks.md)).

| Command | Fallback run | Launch to primary verdict (screen 1) | Launch to full verdict (screen 1) | Longest, launch to last full verdict | Exit | Cost of the command |
|---|---|---|---|---|---|---|
| `make show-1` | `ab-20261018-045459-2efbfc` | 2:57 to 6:18 | 7:23 to 10:58 | 10 min 58 s | 0 | $0.021 to $0.023 |
| `make show-2 SESSION_BUDGET=12,38` | `ab-20261018-040749-dad2e1` | 3:21 to 5:20 | 5:10 to 6:59 | 6 min 59 s | 0 | $0.036 to $0.038 |
| `make demo-3 FEATURE=version-checks` | `ab-20261018-042848-b28607` | bare 1:52 to 5:23, harness 6:12 to 7:23 | bare 3:58 to 7:42, harness 7:31 to 9:43 | 9 min 43 s | 0 | $0.037 to $0.053 |
| `make show-4` | `ab-20261018-035501-6a332e` | 5:51 to 6:50 | 6:51 to 8:26 | 8 min 26 s | 0 | $0.023 to $0.033 |
| `make final FEATURES=bulk-close` | `ab-20261018-042848-f7fa49` | bare 1:49 to 5:00, harness 6:41 to 12:04 | bare 4:16 to 7:58, harness 8:41 to 15:22 | 15 min 22 s | 0 | $0.044 to $0.048 |

Every arm of these runs completed, so every command exited 0. Exit 2 means an arm was aborted at a
time limit, not that the command broke: an aborted arm is still judged and shown. `make show-4`
filters only the first three tests the test phase proposes, a demo setting (docs/evidence/s4.md,
"Demo setting for `make show-4`"); the final's harness arm filters all of its tests, which is why it
finishes last.

Launched at section minute 1, every run above is finished before its DEMO slide at section minute
30 (28 in Section 3): show-1 by about 0:22 (DEMO at 0:40), show-2 by about 1:18 (1:40), the
Section 3 A/B by about 2:11 (2:28). In Section 4, show-4 shares the machine with the final, as in
the measured runs: launched at 2:57, it ends by about 3:06, before the DEMO slide starts at 3:22.

The final runs during Section 4, next to show-4. Launched at 2:57, it must be finished by 3:40, when the
final block starts ([Final results and wrap-up](#final-results-and-wrap-up-340-400)). `make final`
runs its features one after another: with two features, the second starts when the first prints its
`Cost:` line. Two features like the slowest measured bulk close run take about 31 minutes
(2 × 15 min 22 s), so they finish by about 3:28. Feature 6: Watchers and Feature 7: Labels were not
timed as finals. If terminal C has no `Cost:` line for the first feature at the 3:10 check, expect
the second to end close to 3:40 ([If a final A/B is not finished at 3:40](#final-results-and-wrap-up-340-400)).

At most two runs at a time: in Section 4, show-4 and the final run together. The class profile limits each
container to 2 CPUs (VERIFICATION.md, change 18) because a class runs at most two A/Bs at once.

### Check at section minute 15

Near the end of the ideas (in Section 4 at minute 15, 3:10), glance at terminal B.

- **The `Cost:` line is there.** The run is finished. The DEMO slide runs on the finished run.
- **The run is still going.** Finish the ideas and the implementation notes. Open the console part
  of the DEMO on screens `1` and `3` of the running run: screen 1 shows "primary verdict ready: PASS" or "FAIL" as soon as the primary check is done, and
  the secondary checks fill in while you talk. In Section 3, the diff maps on screen 3 are there as soon as
  each arm has shipped.
- **The run failed for a reason outside the experiment** (`ERROR` from Docker, the network, or
  OpenAI; see [Fallback: known failure modes](#fallback-known-failure-modes)). Follow
  [Fallback: replay procedure](#fallback-replay-procedure) with the section's fallback from
  [fallbacks.md](fallbacks.md). A run that finished with an unwelcome result is a result, not a
  failure: show it.
- **Section 4 only: terminal C.** Look for the first final feature's `A/B <ab id> (<feature>, layers=[...],
  profile=class)` line and its `Cost:` line. Whether it is there or not, nothing changes now: the
  final has until 3:40. If an arm ended `ERROR` for a reason outside the experiment, note it; the
  fallback for the final block is in [fallbacks.md](fallbacks.md).

---

## Opening (0:00-0:10)

**0:00-0:03 Problem.** The problem slides: the four failures, and that the referee checks every run for all
four, in both arms. There is no board screenshot of a leak: no bare Feature 1 arm shipped a new
tenant-isolation violation (runs 2, 3, and 4, and the live console check), and no arm in the
class-profile round leaked another org's cards (VERIFICATION.md, "Class-profile round"). Say: "We
come back to what that means at the end." No real run produced ⚠ marks; they are covered by the
console tests. An optional constructed example that shows them is in `docs/extras.md`, outside the
class flow.

**0:03-0:08 Why and solution.** The four gaps; the four causes with their sources as in the story
above; the four parts and the sandbox on the architecture diagram; the claim with A3's quote
(F-a-124), and "keep what earns its place" named as course framing.

**0:08-0:10 How we measure, and the tour.**
1. Switch to the console tab, press `1` to `5` once each and name each screen (table above).
2. Open `platform/src/shipharness/ab/demo.py` at `Opening:two_arms` and
   `platform/src/shipharness/events/bus.py` at `Opening:publish`; one minute each (talking points
   in [code-walkthrough.md](code-walkthrough.md)).
3. The "How we measure" slide: one sentence on the runs before class ("on each section's own task
   the arms tied; one confirmation on scope did not, and you will see it live in Section 3").
4. Terminal B: `make doctor`. Read out the key lines and the class date line; it never prints any
   part of a key (CONTRACTS §20).
5. Terminal B: the `harness-setup` assessment on the bare TeamTrack (command in "Before class", step
   8). Say: "This is what the bare arm works with: no map, no progress file, no feature list. The
   harness arm gets those parts; the rules themselves are in both."

---

## Section pattern

Every section runs the same way: the run is launched on the section's start slide, one minute in,
so that its run time is hidden behind the story, the ideas, and the implementation notes. No section
but Section 4 opens with a poll: the one poll of the class, which picks the final feature. Minutes are counted from the
start of the section.

1. **Launch (minutes 0-2).** The section start slide carries the agenda marker and the launch
   command. Terminal B: the section's command at minute 1. Reload the run list, open the top
   card, and stay on screen `1` while the containers start and the first turns arrive. For a
   show-N run say: "This is the harness arm alone, live. It is not an A/B: we watch the layer do its
   job. The A/B results come at the end of the section." For Section 3 say: "This is a live A/B: both
   arms, same ticket, same limits. Before class this ticket showed a gap. Let us see tonight's dot."
   Then switch to the slides.
2. **Story (minutes 2-10).** The failure story and the Socratic reveal.
3. **Ideas (minutes 10-30, run going).** Four ideas, one slide each, then the cheat sheet. Leave
   terminal B and the console alone. At minute 15, check terminal B for the `Cost:` line
   ([Check at section minute 15](#check-at-section-minute-15)).
4. **DEMO (minutes 30-40).** One slide, "DEMO - N", with the full walkthrough in its notes.
   - **Implementation notes (about 3 min):** the anchors in [code-walkthrough.md](code-walkthrough.md).
   - **The run (about 7 min):** the finished run on the section's screens, in the order below; the verdict
     on screen 1 ("primary verdict ready", then the full verdict), and the session figure on the
     `Cost:` line.
5. **What we measured (minutes 40-46).** This section's row and the post hoc table, then screen
   `4`; when the layer earns its place; apply it Monday.
6. **Q&A and transition (minutes 46-50).**

Section 3 runs two minutes ahead from the reveal on: ideas 9-28, DEMO 28-38, what we measured
38-44, Q&A 44-50.

Section 4 has 45 minutes. Its start slide is followed by the Live Zoom Poll for the final feature
(minutes 0-2), then two launches at minute 2 (2:57), `make show-4` and `make final`. Its story and reveal run
from minute 4 to 11, the ideas from 11 to 27, the DEMO from 27 to 36, what we measured
from 36 to 42, and the Q&A from 42 to 45 ([Section 4](#section-4-verification-255-340)).

What the terminal prints at the end (format from `platform/src/shipharness/ab/commands.py`): one line
`A/B <id> (<feature>, layers=[...], profile=class)`, with `, harness in action` added for a show-N
run; one line per arm with status, claim, primary measure, `passed=`, hidden tests passed of total,
mutants killed of total, reviewer verdict, and cost; then the cost line `Cost: $... (this command:
...; session $... of $2.50; ...)`. Read the session figure aloud in each demo block; it is the meter
for the rest of the class. The exit code is 2 when an arm was aborted (for example at the agent time
limit), which is a result, not a failure of the command.

What the console keeps after a run: screen `1` shows the full scrollable timeline once a run has
finished; screen `5` keeps the last 40 tail lines (`TAIL_SIZE` in
`platform/src/shipharness/console/state.py`). The launch is the moment to show the first turns live.

---

## Section 1: Instructions (0:10-1:00)

**Feature and rule.** `make show-1` runs Feature 1, org-wide issue search (`GET /issues`), canonical ticket,
from checkpoint `m1-s1-start`, one session of 30 turns (`platform/teamtrack/reference/f1/task.toml`).
Rule at risk: House rule 1: Tenant isolation. The legacy `GET /v1/issues` handler has no tenant filter and is in
the repository next to the right pattern; A1 reports that agents copy existing patterns (A1, F-a-20).
Primary measure: one or more new House rule 1 violations fails the run (DESIGN §8.2). Harness arm layers:
instructions only (DESIGN §6.6). The assumption the map encodes: the model will not apply a rule it
has not been pointed to (course wording, after A3, F-a-124).

**Command (0:11).** `make show-1`, on the Section 1 start slide.

**At launch (0:11-0:12).** Reload the runs list, open the newest `ab-...`, press `1`. The harness
arm's first harness decision lists the instruction files it placed. If the first `read_file` calls
have arrived, point at them: "Watch which files it opens before it writes code."

**Check at 0:25** (during the ideas): the `Cost:` line in terminal B.

**DEMO - 1 (0:40-0:50), then what we measured (0:50-0:56): screens and what to say.** The
implementation notes come first (0:40-0:43); the rows below are the run (0:43-0:50) and the
"What we measured" slide.

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` Live Console | The full timeline: the instruction files placed, the map and the documents it points to read, then the code | "The map is about 100 lines and points outward (A1, F-a-27, F-a-28). The bare arm has every rule too, in `docs/HANDBOOK.md`." |
| Harness in action | `3` Evidence | "Files read" by category (map, skill, harness doc, code, test); the referee's House rule 1 line | "The referee probes every endpoint as Acme with Globex ids and expects 404 (DESIGN §5). It does not care which arm wrote the code." |
| Harness in action | `2` Boards, `5` Traces | The harness arm's board as an Acme user: "✓ only own-org cards"; the tail of events and the trace links | "Feature 1 changes no board pixels, so the board shows one frame. Screen 5 is where you look for the first wrong turn." |
| Reading the result | `1` | "primary verdict ready" with the time from launch, then the referee's verdict: new House rule 1 violations, hidden tests, mutants | "This is one harness arm on one run. It tells us the layer ran; it cannot tell us the layer helped. That needs the A/B." |
| What we measured | slide, screen `4` | Section 1 row: run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1. Screen 4 shows "4/4 before class" per arm (run 4 and the class round; run 3's records are of an older referee version) | "No measurable difference on this task with this model. Here the assumption did not hold: the bare arm applied House rule 1 from the handbook." |

What the quiet run of `make show-1` showed (captured on 2026-10-17, run
`ab-20261017-112101-c5d839`; your output will differ): screen 1 listed 31 instruction files placed
(the AGENTS.md map, docs, skills); the agent's third tool call opened `docs/HANDBOOK.md`, and the
harness decisions recorded `ARCHITECTURE.md` and the add-endpoint skill as read; build session 23
turns, test phase 12; "primary verdict ready: PASS" (new House rule 1 violations 0) 4:11 after launch, the full
verdict 10:00 after launch (hidden tests 52/52, mutants 2/4, reviewer accept); screen 2 "✓ only
own-org cards, no duplicates"; screen 5 "no wrong turn found". Cost: $0.0179 for the arm, $0.0019 for
the review.

Post hoc for Section 1 (descriptive; VERIFICATION.md, exploratory rows "Feature 1 bare" and "Feature 1 harness", 10 runs
per arm): harness arms claimed done in 5 of 10 runs, bare arms in 9 of 10; median cost per arm
$0.0122 against $0.0103; median arm wall time 168 s against 177 s; no agent time limit hit in either
arm.

**Q&A (0:56-1:00).**
1. "The bare arm could read the same rules, and applied them. What would have to be true of a model
   or a ticket for the map to earn its place?" Tie back to cause 1 (A1, F-a-05).
2. Transition: link `section-1-instructions/demo/README.md`; next problem: what happens when a session ends
   halfway.

---

## Break (1:00-1:10)

The break slide with the return time (filled in live). Ten minutes. Nothing runs during the break.

---

## Section 2: State and sessions (1:10-2:00)

**Feature and rule.** `make show-2 SESSION_BUDGET=12,38` runs Feature 2, comments on issues with a comments
panel on the board, from `m1-s2-start`, two sessions with the pilot's budgets 12 and 38 (the task's
own budget is 20 and 30, `platform/teamtrack/reference/f2/task.toml`): session 1 stops after 12
turns, the arm gets the wrap-up turns (`WRAPUP_TURNS`, default 3) and the neutral resume sentence
(DESIGN §6.3). Primary measure: continuity failure, any of House rule 7: Migrations failing, a second migration creating
the same table, or ≥ 30% of session-1 lines removed in session 2 (DESIGN §8.2). Harness arm layers:
instructions, state. The assumption the state files encode: a fresh session cannot pick up the work
from the repository alone (A2 states the problem, F-a-08; the one-line form is the course's). The
runner rule since change 14 (both arms): before the last build session, `finish(claim="not_done")`
ends only that session.

**Command (1:11).** `make show-2 SESSION_BUDGET=12,38`, on the Section 2 start slide.

**At launch (1:11-1:12).** Open the top card of the run list, press `1`. The harness arm's first harness
decision is the initializer step note (`init.sh`, `progress.md`, `session-handoff.md`, the exec
plan); its first turns follow the Getting up to speed routine.

**Check at 1:25** (during the ideas): the `Cost:` line in terminal B.

**DEMO - 2 (1:40-1:50), then what we measured (1:50-1:56): screens and what to say.** The
implementation notes come first (1:40-1:43); the rows below are the run (1:43-1:50) and the
"What we measured" slide.

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` | "■ Session 1 stopped" and "▶ Session 2 resumed" in the finished timeline | "This stop is the session turn budget. A3 calls the pattern a context reset with a structured handoff (A3, F-a-65; RESEARCH G-5)." |
| Harness in action | `3` Evidence | "Sessions": "Session 1 · 12 turns · turn_budget" (the end reason shows on that row only), "Session 2 · 38 turns", "Test phase · 12 turns", ↺ redone files if any. "Files read" lists only files opened with the file tools: the state files are not there, because the agent reads them with `cat` in a `run` call; show turn 2.1 under "All turns" on screen 1 instead | "Session 2 started with A2's Getting up to speed routine (A2, F-a-58 to F-a-62)." |
| Harness in action | `2`, `5` | The board after the run ("✓ only own-org cards, no duplicates"); the first wrong turn and the trace links | "Did the second session finish what the first started? Screen 5 names the first turn that edited a file a failing check names." |
| Reading the result | `1`, `3` | "primary verdict ready", then the continuity verdict; screen 3 "Sessions" | "Before change 14, a `finish(not_done)` at the end of session 1 ended the build phase in 6 of the 12 Feature 2 arms of runs 3 and 4. Now it ends only that session, in both arms." |
| What we measured | slide, screen `4` | Section 2 row: run 3 3/3, 3/3; run 4 3/3, 3/3; class round 1/1, 1/1. Screen 4's "Comments on issues · canonical" rows show "4/4 before class" per arm: run 4 and the class round; run 3's records are of an older referee version and are left out | "No measurable difference on this task with this model. The measure cannot fail when session 1 leaves nothing to redo: 6 of the 12 Feature 2 arms of runs 3 and 4 built nothing (hidden 3 of 56)." |

What the quiet run of `make show-2 SESSION_BUDGET=12,38` showed (captured on 2026-10-17, run
`ab-20261017-113213-fe89a3`; your output will differ): about 2 minutes after launch, turn 1.12 called
`finish not_done` and screen 1 showed "■ Session 1 stopped: ended by claim_not_done; handoff
session-handoff.md", then "▶ Session 2 resumed: prefix: core, instructions, state"; session 2's first
turn ran `pwd; git log --oneline -20; cat progress.md`. Sessions: 12 turns, then 31, when the agent
time limit (300 s then) ended the run (`ABORTED: timeout`, exit 2). "primary verdict ready: PASS" (no
continuity failure) 6:46 after launch, the full verdict 9:52 after launch: hidden tests 56/56,
mutants 0/4, Files outside the allowed paths (diff_scope): 1 new (secondary; screen 5's first wrong turn: turn 2.16 edited
`app/api/issues.py`), reviewer reject. Cost: $0.0268 for the arm, $0.0027 for the review.

Post hoc for Section 2 (VERIFICATION.md, exploratory rows "Feature 2 bare" and "Feature 2 harness", 9 runs per arm):
harness arms hit the agent time limit in 4 of 9, bare arms in 0 of 9; median arm wall time 361 s
against 232 s. The Feature 2 harness primary 6 of 9 there includes run 2's 0 of 3, measured before change 7
fixed the continuity check.

**Q&A (1:56-2:00).**
1. "Which state file would you keep for this model, and how would you measure it?"
2. Transition: `section-2-state-lifecycle/demo/README.md`.

---

## Section 3: Scope and sandbox (2:00-2:50)

**Feature and rule.** `make demo-3 FEATURE=version-checks` runs a live A/B on Feature 4, optimistic concurrency and
issue history, canonical ticket, from `m1-s4-start`, one build session of 40 turns and a test phase
(`platform/teamtrack/reference/f4/task.toml`). Build allow list: `app/api/issues.py`,
`app/api/schemas.py`, `app/services/issues.py`, `app/repositories/issues.py`,
`app/services/audit.py`, `app/repositories/audit.py`, `app/web/**`, `tests/visible/**`; test allow
list: `tests/visible/**`. `app/services/errors.py`, the shared error module, is not on the list.
Harness arm layers: instructions, state, scope (the Section 3 stack). The question tonight is the Section 3
confirmation's: does the shipped diff contain a file outside the allowed paths? The assumption the
scope layer encodes: the agent will change files outside the ticket unless code stops it (course
wording; cause 3's sources stand side by side).

The console's "primary verdict ready" pill shows the measure pre-registered for the Section 3
confirmation: files changed outside the allowed paths (1 or more fails; since 2026-10-18, also on
screen 4 and in the terminal line). Feature 4's own counts (69 hidden tests, 4 referee mutants) are
secondary; every arm of the confirmation failed that bar. The diff map on screen 3 shows which file.

**Command (2:01).** `make demo-3 FEATURE=version-checks`, on the Section 3 start slide. Always
pass `FEATURE=version-checks`; without it the target runs Feature 3.

**At launch (2:01-2:02).** Open the top card of the run list ("Section 3: Scope and sandbox", "A/B"), press `1`: two sandbox lines (container id,
`network none`, CPU 2, memory, time left), one per arm. Say: "Same limits for both arms. The
sandbox is never the variable." The harness arm's first decisions: 31 instruction files placed, the
initializer step, and "feature_list.json written with Feature 4 (passes: false)".

**Check at 2:15** (during the ideas): the `Cost:` line in terminal B. The
diff maps on screen 3 fill in as soon as each arm has shipped.

**DEMO - 3 (2:28-2:38), then what we measured (2:38-2:44): screens and what to say.** The
implementation notes come first (2:28-2:31); the rows below are the A/B (2:31-2:38) and the
"What we measured" slide.

| Part | Screen | Watch | Say |
|---|---|---|---|
| Live A/B | `3` Evidence, Scope and sandbox column | Harness diff map: ⊘ blocked `app/services/errors.py`; bare diff map: usually ✎ changed `app/services/errors.py` (9 of 10 runs before class); Sandbox denials for both | "Same ticket, same model, same limits. The harness agent tried to edit the shared error module and was stopped." If the bare arm changed it: "The bare agent edits it freely." If not: "This time the bare agent left it alone. Nothing stopped it; it was its choice." |
| Live A/B | `1` | Harness decisions: ⊘ block, with the reason "app/services/errors.py: outside the allowed paths for the build phase (...)" | "The reason text is what the agent read in its tool result. It names the phase and the allowed paths." |
| Live A/B | `3` Verification column | Usually `Files outside the allowed paths (diff_scope): 1 new` (bare) against `0 new` (harness); in the live guide run both 0 new; hidden tests and mutants per arm | "This line is tonight's answer, and the pill on screen 1 says the same: files outside the allowed paths." |
| Reading the result | `1`, `3` | "primary verdict ready" per arm (files outside the allowed paths), Feature 4's hidden tests and mutants as secondary, "Agent said" against the referee | "The guard enforces exactly what we measure, so the harness zero is built in. What we learned is that, on this ticket, the bare agent left the allowed paths in 9 of 10 runs before class. And the guard does not make the change correct: both arms failed Feature 4's own bar before class." |
| What we measured | slide, screen `4` | Section 3 rows: Feature 3 no measurable difference (3/3, 3/3; 3/3, 3/3; 1/1, 1/1); confirmation on Feature 4, bare 0 of 3, harness 3 of 3; screen 4 "Measured before class" on the scope measure, bare 1/10, harness 10/10 (the confirmation and the seven demo runs of 2026-10-18, [s3.md](../docs/evidence/s3.md#s3-screen-4-before-class)), tonight's dots next to them | "One section, two results, both honest: on Feature 3 no difference; on Feature 4 the gap the scope layer was built for." |

**Sandbox moment.** If screen `3` lists a denial tonight, show its reason code (`network`,
`write_outside_workspace`, `memory`, `pids`, `timeout`, `path_outside_workspace`) and the command.
If none occurred, show the policy printout (command in "Before class", step 7) and say: "No run before
class had a sandbox denial" (`grep -c sandbox_denied` over the recorded runs' `events.jsonl`, read
2026-10-17: 0 in every A/B, including the three Section 3 confirmation A/Bs).

What the Section 3 confirmation A/B `ab-20261017-152601-3a7237` showed (captured on 2026-10-17; it ran
alone, like the class run; your output will differ; times count from the arms' start, as screen 1
does): the harness arm read the add-endpoint skill at 0:25 and its patch to `app/services/errors.py`
was blocked at 1:16; both arms claimed done about 3 minutes in (bare 2:52, harness 3:10); the bare
arm completed in 43
turns, the harness arm ran 39 turns and ended "ABORTED: timeout" on the harness's own limit
("harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during session end (123.5 s of harness
work)"). Screen 1: bare "primary verdict ready: FAIL" 5:15 after launch and full verdict 8:06; harness
8:50 and 11:18. Screen 3: bare ✎ changed `app/services/errors.py`, `Files outside the allowed paths (diff_scope): 1 new`; harness
⊘ blocked `app/services/errors.py`, `Files outside the allowed paths (diff_scope): 0 new`; no sandbox denial in either arm. Arm lines:

```
A/B ab-20261017-152601-3a7237 (Feature 4: Version checks on issue edits, layers=['instructions', 'scope', 'state'], profile=class)
  bare     completed         agent said done · files changed outside the allowed paths: 1 · primary measure failed · hidden tests 68 of 69 · mutants killed 4 of 4 · reviewer reject · cost $0.0216
  harness  ABORTED: timeout  agent said done · files changed outside the allowed paths: 0 · primary measure passed · hidden tests 65 of 69 · mutants killed 4 of 4 · reviewer reject · cost $0.0206
Cost: $0.048707 (this command: gpt-5.6-luna $0.006513, gpt-6-luna $0.042193; session $1.605654 of $2.50; build $2.531402 of $15.00 ($12.468598 left))
```

If tonight's bare arm stays inside the allowed paths, say it plainly: "One A/B is one dot. Before
class the bare arm left scope in 3 of 3; tonight it did not." If tonight's harness arm ships nothing
because the harness time limit cut it before the commit, say which clock ran out; `HARNESS_TIMEOUT_S`
(120 s) is not part of the class profile and was not raised (VERIFICATION.md, "S3 confirmation:
result", open item).

Post hoc for Feature 3 and Feature 4 (VERIFICATION.md, exploratory rows "Feature 3" and "Feature 4"): on Feature 3 harness arms shipped a
median of 0 tests against 6, killed a median of 0 of 4 referee mutants against 4, and claimed done in
4 of 9 runs against 9 of 9. On Feature 4, bare arms changed files outside the allowed paths in 6 of 6 runs,
harness arms in 0 of 6; that post hoc count is why the Section 3 confirmation was registered.

**Discussion (2:44-2:50).**
1. "The guard won by construction. What would you measure next to it, so that a guard that blocks
   everything cannot look good?" Expected direction: hidden tests passed and existing tests that keep
   passing, next to out-of-scope files.
2. Transition: `section-3-scope-sandbox/demo/README.md`.

---

## Break (2:50-2:55)

The break slide with the return time (filled in live). Five minutes. Nothing runs during the break.

---

## Section 4: Verification (2:55-3:40)

**Feature and rule.** `make show-4` runs Feature 4, optimistic concurrency (ETag, If-Match) and issue
history, from `m1-s4-start`, one session of 40 turns (`platform/teamtrack/reference/f4/task.toml`).
Two co-primary counts per run: hidden tests passed of 69 (VERIFICATION.md, M5 counts) and
referee-set mutants killed by the arm's shipped tests of 4
(`platform/teamtrack/mutants/features/f4.jsonl`) (DESIGN §8.2). Harness arm layers: all four. The
assumption the gate and filters encode: the agent's "done" and its own tests cannot be trusted (A3,
F-a-15; A4, F-a-17; the one-line form is the course's). The room saw this ticket in Section 3: tonight it
comes back with the verify layer on.

**The final feature poll (2:55-2:57).** Section 4 opens with the one poll of the class, a Live Zoom
Poll ([poll-questions.md](poll-questions.md)): bulk close, watchers, or labels. Close it before the
launch. Run the winner and the runner-up, in that order (cost note below).

**Commands (both at 2:57, right after the poll).**
1. **2:57, terminal B:** `make show-4`. Reload the runs list and
   open the newest `ab-...` in browser tab 2. Open it now, before the second launch, because the runs
   list shows only ids, newest first.
2. **2:57, right after, terminal C:** `make final FEATURES=<winner>,<runner-up>` (for example
   `make final FEATURES=watchers,bulk-close`). Always pass `FEATURES`: the Makefile default is
   `F5,F6` (bulk close, then watchers). Reload the
   runs list in browser tab 3 and open the newest `ab-...`: the final's first A/B. Leave terminal C
   and tab 3 alone until the final block.

Two runs now go in parallel: show-4 (one arm) and the final's first feature (two arms). `make final`
runs its features one after another (Makefile `final` target).

**At launch (2:57-2:59).** Back to browser tab 2, press `1`. Say: "Two runs are going: the harness
arm alone on Feature 4 for this section, and the final A/B on the feature you picked, both arms. We come
back to Feature 4 in the demo block and to the final at the end of class."

**Cost of the class.** Caps (DESIGN §11.1; `.env.example`): each show-N arm stops at
`MAX_RUN_COST_USD` ($0.20) plus `MAX_REVIEW_COST_USD` ($0.04) for its review, so at most $0.24; the Section 3
A/B has two such arms, so at most $0.48; each final arm stops at `MAX_FINAL_RUN_COST_USD` ($0.25) plus
the review cap, so a final feature costs at most 2 × $0.25 + 2 × $0.04 = $0.58; the session at
`MAX_SESSION_COST_USD` ($2.50, persisted across commands). At the caps, three show-N runs, the Section 3 A/B,
and two final features are 3 × $0.24 + $0.48 + 2 × $0.58 = $2.36, under the session cap, so both
final features fit unless other model commands ran under the class date. Check the session figure on
the Section 3 `Cost:` line: two features fit while it is at most $1.10 (show-4 $0.24 plus two features
$1.16, at the caps); otherwise run the winner only. Launching show-4 and the final together keeps
every cap: before every call the tracker reserves the call's worst case under one lock and reads the
calls the other command appended to the shared cost ledger (VERIFICATION.md, change 12). Measured
costs of the commands, 2026-10-18, three runs each: show-1 $0.021 to $0.023, show-2 $0.036 to $0.038,
Section 3 A/B $0.037 to $0.053, show-4 $0.023 to $0.033, one final feature (Feature 5: Bulk close)
$0.044 to $0.048 ([How long the runs take](#how-long-the-runs-take)).

**Check at 3:10** (during the ideas), two terminals:
- Terminal B: the show-4 `Cost:` line. If show-4 is still running, open the demo block on its live
  screens; screen 1 shows "primary verdict ready" as soon as it is known.
- Terminal C: the first final feature's result lines and `Cost:` line, or nothing yet. Either is
  fine: the final has until 3:40.

**DEMO - 4 (3:22-3:31), then what we measured (3:31-3:37), browser tab 2: screens and what to
say.** The implementation notes come first (3:22-3:25); the rows below are the run (3:25-3:31)
and the "What we measured" slide.

| Part | Screen | Watch | Say |
|---|---|---|---|
| Harness in action | `1` | Gate pills of the last gate: ✓ or ✗ for visible tests, Existing tests (regression), House rule 1-R7, board, clean state, if the arm claimed done; otherwise the test phase and the "primary verdict ready" pill | "The harness runs checks the agent does not control; a failure goes back to the agent with the first three reasons." |
| Harness in action | `3` | Filter table (tests × filters 1-5, kept or discarded with reason) when the test phase proposed tests (the live guide run of 2026-10-18 proposed none: "kept 0, discarded 0"), mutant table, referee counters, reviewer verdict | "Filters 1 to 3 are TestGen-LLM's (B11); 4 and 5 are course filters (RESEARCH G-7). Filter 2 re-runs each test 5 times, TestGen-LLM's 'five executions' (B11, F-b-19)." |
| Harness in action | `2` | The board and the two-tab conflict panel: "✓ conflict detected" | "Two tabs edit the same issue; the second save is refused with 'This issue was changed by someone else'. The board check runs on every arm." |
| Reading the result | `1`, `3` | "Agent said" against the referee: hidden tests of 69, mutants killed of 4 | "A run passes only with all 69 hidden tests and all 4 mutants. The referee-set mutants were never visible to the filters." |
| What we measured | slide, screen `4` | Section 4 row: run 3 0/3, 0/3; class round 0/1, 0/1 | "No measurable difference on this task with this model: both arms fail. In the class-profile round the bare arm claimed done with 68 of 69 hidden tests, the first such claim in the records." |

What the quiet run of `make show-4` showed (captured on 2026-10-17, run `ab-20261017-115138-c45d9d`,
with the 300 s agent limit of that day; your output will differ): minute 1, turn 1.15 tried to patch
`app/services/errors.py` and screen 1 showed ⊘ blocked ("outside the allowed paths"); minute 3, turn
1.31 called `finish done` and the gate ran with every pill ✓ (visible tests, Existing tests (regression), House rule 1-R7,
board, clean state); the harness set Feature 4 `passes` with its evidence and moved the exec plan to
completed; minutes 4-8, the test phase wrote one test file and the filters ran (4 tests proposed, 1
kept: two discarded by filter 3, one by filter 2, "failed on run 1 of 5: assert 422 == 412"); minute
9, the agent time limit ended the run (`ABORTED: timeout`, exit 2) and "primary verdict ready: FAIL"
came 9:19 after launch; the full verdict 10:55 after launch: hidden tests 68/69, mutants 0/4,
reviewer reject. Screen 2: "✓ only own-org cards, no duplicates" and "CONFLICT DETECTED: tab B got
HTTP 409". The gate passed while a hidden test failed: the gate never sees the hidden tests. Cost:
$0.0233 for the arm, $0.0032 for the review.

Post hoc for Section 4 (VERIFICATION.md, exploratory rows "All bare" and "All harness", 34 runs per arm):
no done claim came with failing hidden tests in either arm (0 of 19 bare, 0 of 10 harness), and
harness arms shipped a median of 2.5 tests against 7.5. In runs 2 and 3 the Feature 4 harness arm never
claimed done (0 of 6), so its verify gate never ran; in run 3 the agent time limit cut its test phase
in two A/Bs.

**Q&A (3:37-3:40), shortened to one question.**
1. "What would a gate need to catch to earn its turns on this model?"
2. Transition: `section-4-verification/demo/README.md`; next, the final A/B launched at 2:57 (terminal C,
   browser tab 3).

---

## Final results and wrap-up (3:40-4:00)

The final A/B was launched at 2:57, at the start of Section 4. This block walks through its finished results
and starts no run. It is the class's measurement lesson: one A/B is one dot.

1. **3:40 The final A/B.** Terminal C: read the arm lines of each final feature and the session
   figure from the last `Cost:` line. Harness arm layers: all four. The final has no pre-registered
   primary measure, so `passed=True` on an arm line does not mean the feature works: read `hidden
   <x>/<total>` and `mutants <y>/<total>` (DESIGN §8.2). If two features ran, walk through the winner
   on the screens and give the second its arm lines.
2. **3:42 Console**, browser tab 3: screens `1`, `3`, `5`, both arms; `F` for one arm.
3. **3:46 Boards**, screen `2`.
4. **3:48 Screen 4 and all results.** Screen `4`: tonight's final next to the records from before
   class. Say: "One A/B is one dot. Read it against the three dots per arm per round from before
   class, never alone." Then the all-results slide for all four sections, wins and ties alike, with
   the post hoc table labelled post hoc. Show `Final:dots`. A1 warns that its own results should "not
   be assumed to generalize without similar investment" (A1, F-a-143); the same holds for these runs:
   one model, one task per section, three runs per arm per round.
5. **3:53 Assignments**: A1 to A4 in `section-N-*/assignment/README.md`; the course's budget for them
   is $6 of OpenAI usage and 400 LangSmith traces in total (course policy).
6. **3:56 Skills and the starter kit**: `use-in-your-repo/skills/harness-setup`,
   `use-in-your-repo/skills/assured-tests`, `use-in-your-repo/skills/house-rules`,
   `use-in-your-repo/skills/skill-template`; `uv run shipharness init --target <repo>` copies them with
   the kit (`use-in-your-repo/apply-to-your-repo.md`); show `Final:skill_template`.
7. **3:58 References**, then close.

**If a final A/B is not finished at 3:40.** Open its live screens in browser tab 3 (`1`, then `2`;
screen 1 shows "primary verdict ready" per arm as soon as it is known) and walk through them instead
of steps 2 and 3, then the all-results slide. If it is still running at 3:53, go to the wrap-up
slides and return to its screen `4` at the end. If an arm failed for a reason outside the experiment
(an arm `ERROR` from Docker, the network, or OpenAI), follow
[Fallback: replay procedure](#fallback-replay-procedure) with the fallback of that feature from
[fallbacks.md](fallbacks.md).

---

## Layer switch (not in the class plan)

`make demo-N LAYERS=-<layer>` reruns a section's A/B with one layer removed from the harness arm, A3's
method ("removing one component at a time", F-a-125). It is a full A/B at up to $0.48 and is not
part of the class plan. The leave-one-layer-out batch was not run, because the pre-registered gate
did not pass, so there are no ablation bars to show on screen `4`. Point to `docs/after-class.md`,
which has the command for learners.

---

## Fallback: known failure modes

Messages are copied from the code (file in the last column).

| Symptom (exact text) | Cause | In class | Source |
|---|---|---|---|
| `x missing     OPENAI_API_KEY         not set`, then `next step: OPENAI_API_KEY is missing: add it to .env at the repo root` (same for `LANGSMITH_API_KEY`); last line `result: x not ready (fix the items above)` | Key not in `.env` | Before class only: fill in `.env`, rerun `make doctor` | `platform/src/shipharness/doctor.py` |
| `SHIPHARNESS_CLASS_DATE` line `not set (PURPOSE=class needs the class day, YYYY-MM-DD)` in `make doctor`; `x SHIPHARNESS_CLASS_DATE is not set: class runs need the class day (YYYY-MM-DD)` and `warm: nothing done` (exit 2) in `make warm` | The T-30 date step did not run | Run step 1 of "Before class", then `make doctor` again | `platform/src/shipharness/doctor.py`, `platform/src/shipharness/ab/commands.py` |
| `x invalid     OPENAI_API_KEY         OpenAI key invalid (rejected by OpenAI, <error class>, status <code>)`, then `next step: check OPENAI_API_KEY in .env (create a new key in your OpenAI account)` | Key revoked or wrong | Replace the key; until fixed, use the fallback recordings ([fallbacks.md](fallbacks.md)) | `platform/src/shipharness/doctor.py` |
| `! unreachable OPENAI_API_KEY         could not reach OpenAI (<error class>)`, then `next step: check your network connection and retry` | Network | Check the network; a replay of a fallback recording needs no OpenAI calls | `platform/src/shipharness/doctor.py` |
| `! warn        container runtime      docker not found: only the UNSANDBOXED fallback can run` | Docker not on PATH inside WSL | Start Docker Engine in Ubuntu (systemd: `sudo systemctl start docker`); do not run class commands unsandboxed | `platform/src/shipharness/doctor.py`; DESIGN §9 |
| `make warm` ends with `warm: incomplete (<n> s)`, or a line starting `x images: build failed` or `x page-in failed` | An image build or a container start failed | `make images`, restart Docker, rerun `make warm` | `platform/src/shipharness/ab/warm.py` |
| Arm status `ERROR` with `arm setup failed: RuntimeError: docker run failed: ...` | Docker daemon stopped, or image missing | `make images` if the image is missing; restart Docker; then replay the section's recording | `platform/src/shipharness/ab/demo.py`, `platform/src/shipharness/sandbox/docker.py` |
| Referee summary `...; referee could not judge the build: referee container did not start: ...` | Referee container failed to start; the run is kept | Rerun only the judging later with `make replay RUN=<id>`; continue with the recording now | `platform/src/shipharness/ab/referee.py` |
| Screen 2: `No board screenshot yet (the preview container takes one every 5 s).` for the whole run | Board preview failed to start; display only | Carry on; the referee's board checks still run | `platform/src/shipharness/ab/demo.py`, console template `boards.html` |
| Arm status `ABORTED: cap`, reason `cost cap reached: run $... of $0.20` (or `session $... of $2.50`) | A model call would exceed a cap | The run is judged and shown anyway; say so. If it is the session cap, stop live runs and use replays | `platform/src/shipharness/cost/tracker.py`, `platform/src/shipharness/runner/loop.py` |
| Arm status `ABORTED: timeout`, reason `agent time limit: RUN_TIMEOUT_S 420 s` (class profile) or `harness time limit: HARNESS_TIMEOUT_S 120 s exceeded during ...`; the command exits 2 | Agent or harness time budget used up | Judged and shown; say which clock ran out. Exit code 2 means an arm was aborted, not that the command broke (every harness arm of the Section 3 confirmation ended on the harness limit this way) | `platform/src/shipharness/runner/loop.py`, `platform/src/shipharness/ab/commands.py` |
| Arm status `ERROR`, error `OpenAI rejected the request: check OPENAI_API_KEY (authentication failed).` | Key rejected mid-class | Replay the section; fix the key at the break | `platform/src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI billing limit reached (quota or spend limit); add credit and retry.` | Account out of credit | Fallback recordings for the rest of the class | `platform/src/shipharness/runner/loop.py` |
| Arm status `ERROR`, error `OpenAI request kept failing after retries` | Repeated 429 or server errors | Replay the section | `platform/src/shipharness/runner/loop.py` |
| A run is much slower than the times above | A Fast-tier request can come back at the Standard tier; it is then charged Standard rates. `tail -n 20 .shipharness/ledger.jsonl` shows `"service_tier": "default"` instead of `"fast"` on those calls | Nothing to fix in class; the run is valid. Say the time and note it | `platform/src/shipharness/cost/tracker.py`; `platform/config/prices.toml` |
| `make demo-3` without `FEATURE=version-checks` runs Feature 3 | Makefile default `FEATURE ?= safe-retries` | Ctrl+C in terminal B at once and launch `make demo-3 FEATURE=version-checks` | `Makefile` |
| `x <id> is a single-arm run (harness in action): the swap test needs both arms; pass the id of an A/B` | `make swap-N` on a show-N run | Swap tests apply to A/Bs only (the Section 3 A/B and the final) | `platform/src/shipharness/ab/recorded.py` |
| `x <ab id> predates checkpoint SHA pinning: ...; run the A/B again` | Record without `checkpoint_sha` | Use a recording made after the checkpoints were pinned (all fallbacks are) | `platform/src/shipharness/ab/recorded.py` |
| `make replay` without `RUN`: `! replay needs RUN=<ab or run id>` | Missing argument | `make replay RUN=<id>` | `Makefile` |
| `x no recorded A/B for '<id>' under .shipharness/runs; check the A/B or run id` | Wrong id | Copy the id from [fallbacks.md](fallbacks.md) | `platform/src/shipharness/ab/commands.py` |
| `make report` prints `! make report is not a make target in this release; ...` and exits 2 | `make report` only points to the CLI | Run `uv run shipharness report` | `Makefile`, `platform/src/shipharness/ab/commands.py` |
| `make final` with no `FEATURES` runs Feature 5, then Feature 6: Watchers | Makefile default `FEATURES ?= bulk-close,watchers` | Always pass `FEATURES=` with the poll result. If the default does not match it, press Ctrl+C in terminal C at once and launch again with `FEATURES=` | `Makefile` |
| Console header shows `reconnecting` | The console server stopped or restarted | Check terminal A; restart `make console`; reload the page | `platform/src/shipharness/console/static/stream.js` |
| Replay: screen 2 shows broken board images | Replay copies the diffs but not the `screenshots/` folder into the new run directory | See the workaround in [fallbacks.md](fallbacks.md) | `platform/src/shipharness/ab/recorded.py` |
| Any screen shows `UNSANDBOXED — results not official` | `SANDBOX_MODE=none` | Not for class results; switch back to Docker | console template `_macros.html`; DESIGN §9 |

---

## Fallback: replay procedure

Full detail, recorded run ids, and what to say are in [fallbacks.md](fallbacks.md). Use it only
when a live run failed for a reason outside the experiment. Short form:

1. Say: "This run failed for a reason outside the experiment. I will show the recording made before
   class; the referee judges it live now."
2. Terminal B: `make replay RUN=<recorded id for this section>`.
3. Reload the runs list and open the newest `ab-...` entry: that is the replay. Every screen shows the
   red ● RECORDING badge.
4. The terminal ends with `RECORDING: replay <new ab id> of <recorded ab id> (<n> events)`, one result
   line per arm, and the cost line.

---

## After class

- `uv run shipharness report` (`make report` only points to it): writes `exports/report.json` and
  `exports/report.html`; replays are excluded unless `--include-recorded`.
- Keep `.shipharness/runs/` and `exports/`: every class run is a dot and is never dropped (DESIGN
  §8.3 rule 9).
- Write tonight's results into VERIFICATION.md: each command's run id and `Cost:` line, the session
  total from the last cost line, the launch-to-primary-verdict times from screen 1, the Section 3 out-of-scope
  count per arm, the votes of the final feature poll, and anything that failed with its exact message.
