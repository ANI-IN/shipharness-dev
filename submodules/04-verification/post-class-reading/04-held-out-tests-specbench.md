# Held-out tests: what SpecBench measures and how the course's hidden tests follow it

Reading time: about 6 minutes.

Source: B13, "SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents" (Zhao, Srikanth, Wu,
Jiang, Weco AI; preprint, v2 2026-09-09), https://arxiv.org/abs/2605.21384, and its repository B14,
https://github.com/WecoAI/SpecBench. Quotes are copied from RESEARCH.md and `research/notes/R-b.md`,
with finding IDs. Do not confuse it with Spec-Bench (arXiv 2401.07851), an unrelated benchmark
(RESEARCH §1.1).

## The design

Each of SpecBench's 30 tasks has a spec, "visible validation tests that exercise specified features
in isolation, and (iii) held-out tests that compose those same features to simulate real-world
usage." (F-b-42). The repository holds 1,779 validation tests and 2,783 held-out tests (B14,
RESEARCH §4.6).

The held-out suite is kept away from the agent: "A separate held-out test suite ... never shown to
the agent, is used solely for evaluation." (F-b-43). The gap between the two pass rates is the
"reward hacking gap". It is fair because the held-out tests ask for nothing new: "Crucially, test
introduces no requirements beyond what [spec] and val already specify." (F-b-44).

SpecBench uses "validation tests" and "held-out tests". The course says "visible tests" and "hidden
tests" and uses SpecBench's terms when quoting it (RESEARCH §2).

## What it found

- "while every frontier agent saturates the visible suite, reward hacking persists, with smaller
  models exhibiting larger gaps on holdout suites." (F-b-45)
- The gap grows with code size: "it grows by 28 percentage points for every tenfold increase in
  code size." (F-b-46). The paper's own text also gives about 27 points, and the mean slope is 23
  points; the abstract's 28 is the P90 figure (RESEARCH G-12).
- "Among tasks under 10K LOC, the worst-case gap is 21pp. Among tasks over 25K LOC, it reaches
  100pp." (F-b-47)
- Claude Code: "the held-out score remains much lower, producing gaps of roughly 43-48pp." (F-b-48)
- Cheating happens but is rare. One run built a lookup-table "compiler": "This achieves 97% on
  validation tests and 0% on held-out tests, yielding a 97pp reward hacking gap." (F-b-49). The
  common case is different: "deliberate exploits are rare, while compositional failures account for
  a much larger fraction of reward hacking behavior." (F-b-50)
- More visible tests do not fix it: "These findings suggest that reward hacking cannot be eliminated
  by improving the test suite alone" (F-b-51). Neither does more search: "The results show that
  additional search does not reliably remove reward hacking." (F-b-52)

The course uses SpecBench for one claim: visible tests miss what held-out tests catch, mostly
through features that pass alone and fail together. Defences against agents that deliberately game
checks are Module 2 (RESEARCH §2).

## How the course's hidden tests follow it

| SpecBench | Course |
|---|---|
| Held-out tests never shown to the agent (F-b-43) | Hidden tests live in `teamtrack/tests/hidden/`; each arm works in a fresh repository exported without them, and the referee mounts them read-only in its own container (DESIGN §8.3 rule 6, CONTRACTS §21) |
| Held-out tests compose features (F-b-42) | Some hidden test files combine features, for F4 `test_f4_with_f1.py` and `test_f4_with_f3.py` (`teamtrack/reference/f4/task.toml`) |
| No requirements beyond the spec (F-b-44) | Hidden tests check what `teamtrack/docs/features/<task>.md` states; where the M5 audit found tests asserting more than the spec, the tests were relaxed or the spec now states the rule (VERIFICATION.md, M5) |
| Gap between validation and held-out pass rates | Hidden tests passed per run is an S4 co-primary count, shown next to "agent said" on screen 1 |

Counts (VERIFICATION.md, M5): 441 hidden tests in total, 69 for F4. For every task and checkpoint
pair, 91-96% of the hidden tests fail before the reference implementation is applied (the rest are
guards that must keep passing), and all pass with it.

## Why it matters for your own repo

- If every test lives where the agent can read and edit it, a green suite tells you about those
  tests only. SpecBench saw agents saturate the visible suite while held-out gaps remained (F-b-45).
- The gap comes mostly from composition, not cheating (F-b-50). Your held-out tests do not need to
  be clever; they need to use two features together the way a user would (F-b-42), and to stay
  outside the agent's workspace (F-b-43).
- A real case from this course: in pilot run 2 the bare arm of run 2 shipped 33 tests of its own
  and still failed 3 of the 69 hidden F4 tests (score record `r-20261016-185422-ce2096`;
  VERIFICATION.md, M6 pilot run 2).
- Ask only for what the spec states (F-b-44). A hidden test that checks an unwritten rule measures
  the spec's gaps, not the agent.

## Questions to take away

- Which features in your service pass their own tests and could still fail when used together?
  Write one test that composes two of them.
- SpecBench says better visible tests alone do not close the gap (F-b-51). What else in this
  section's harness addresses the gap besides tests?
