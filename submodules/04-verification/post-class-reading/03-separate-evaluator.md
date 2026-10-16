# Separate evaluators: what A3 found and how the course reviewer uses it

Reading time: about 7 minutes.

Source: A3, "Harness design for long-running application development" (Prithvi Rajasekaran,
Anthropic, 2026-03-24),
https://www.anthropic.com/engineering/harness-design-long-running-apps. Supporting: A2, "Effective
harnesses for long-running agents". Quotes are verbatim, with finding IDs that resolve in
[REFERENCES.md](../../../REFERENCES.md).

## The problem A3 starts from

"When asked to evaluate work they've produced, agents tend to respond by confidently praising the
work—even when, to a human observer, the quality is obviously mediocre." (F-a-14). In short: "agents
reliably skew positive when grading their own work." (F-a-15).

A2's single coding agent checks itself: "Self-verify all features. Only mark features as “passing”
after careful testing." (F-a-108). A2 names the next step as future work: "specialized agents like a
testing agent, a quality assurance agent, or a code cleanup agent, could do an even better job"
(F-a-109). The separate evaluator as a working design comes from A3, not A2.

## What A3 built

A3 describes "a three-agent architecture—planner, generator, and evaluator—that produced rich
full-stack applications over multi-hour autonomous coding sessions." (F-a-117). The central claim:
"Separating the agent doing the work from the agent judging it proves to be a strong lever to
address this issue." (F-a-110). The reason it works: "tuning a standalone evaluator to be skeptical
turns out to be far more tractable than making a generator critical of its own work" (F-a-111).

Three details make the evaluator useful rather than polite:

- **Grading criteria.** "\"Is this design beautiful?\" is hard to answer consistently, but \"does
  this follow our principles for good design?\" gives Claude something concrete to grade against."
  (F-a-113). A3 "wrote four grading criteria that I gave to both the generator and evaluator agents
  in their prompts" (F-a-114), and "Each criterion had a hard threshold, and if any one fell below
  it, the sprint failed and the generator got detailed feedback on what went wrong." (F-a-119).
- **Calibration.** "I calibrated the evaluator using few-shot examples with detailed score
  breakdowns." (F-a-115). The tuning loop was "to read the evaluator's logs, find examples where its
  judgment diverged from mine, and update the QAs prompt to solve for those issues." (F-a-122).
- **Using the product.** "the evaluator used the Playwright MCP to click through the running
  application the way a user would, testing UI features, API endpoints, and database states."
  (F-a-118).

## The limits A3 reports

- Separation does not remove leniency: "the evaluator is still an LLM that is inclined to be
  generous towards LLM-generated outputs." (F-a-112).
- "Out of the box, Claude is a poor QA agent. In early runs, I watched it identify legitimate
  issues, then talk itself into deciding they weren't a big deal" (F-a-121).
- Criteria steer the generator too: "The wording of the criteria steered the generator in ways I
  didn't fully anticipate." (F-a-116).
- The evaluator is a cost decision: "It is worth the cost when the task sits beyond what the current
  model does reliably solo." (F-a-123). A3's own comparison was a solo run of 20 minutes and $9
  against a full harness of 6 hours and $200 (F-a-152).

A3's choices are dated and model-dependent, not standing rules: "every
component in a harness encodes an assumption about what the model can't do on its own, and those
assumptions are worth stress testing" (F-a-124).

## How the course applies it

The course uses two judges, neither of them the agent.

**A deterministic judge for the primary measures.** The verify gate and the referee run code, not a
model: tests, R1-R7 probes, mutants. A3's point about leniency (F-a-112) is why the S4 primary
counts come from the referee, and the reviewer's verdict is a secondary measure.

**A separate model as reviewer.** `shipharness review` and the referee's reviewer step
(`src/shipharness/reviewer/`) follow A3 with these choices:

| A3 idea | Course choice | Where |
|---|---|---|
| Separate evaluator (F-a-110) | A different model from the agent: `OPENAI_EVAL_MODEL` = `gpt-5.6-luna`, a different generation from `gpt-6-luna` | `src/shipharness/config/settings.py` |
| Grading criteria (F-a-114) | Built from `docs/SECURITY.md` and `ARCHITECTURE.md` of the harness instructions; the house rules when those are missing; the same bytes for every review | `reviewer/criteria.py` |
| Hard threshold (F-a-119) | The prompt asks for findings first, then the verdict: reject on any blocker or if the ticket is not implemented | `reviewer/review.py` |
| Few-shot calibration (F-a-115) | Not used; a candidate extension | — |
| Clicking through the app (F-a-118) | Done by the referee's Playwright board check, not by the reviewer | `src/shipharness/checks/board.py` |

The course adds two things A3 did not need, because the course compares two arms:

- **Blinding** (A/B design, not a source term). `blind()` drops harness artifacts, commit metadata,
  host workspace paths, and run ids from the diff, so two arms that shipped the same code produce
  the same text; the arm label is never an input (anchor `S4:blind`; course design).
- **Placement.** The reviewer runs on both arms' final diffs as referee output, not inside the gate,
  so the harness arm never receives reviewer feedback the bare arm cannot get (course design). Its
  agreement with the referee is recorded per run (`reviewer_agrees` in the score record).

Each review is capped at `MAX_REVIEW_COST_USD` ($0.04, `src/shipharness/config/settings.py`). An incomplete or refused
response gives no verdict rather than a guessed one (`reviewer/review.py` docstring).

## Why it matters for your own repo

- An agent that reviews its own pull request has the leniency A3 describes (F-a-15). If you add a
  model reviewer, make it a separate call with grading criteria taken from your repository's own
  documents, the same text every time (F-a-114, F-a-119).
- Keep its verdict secondary to checks that run code. A3 says the separate evaluator "is still an
  LLM that is inclined to be generous towards LLM-generated outputs." (F-a-112).
- A real case from this course: in the course pilot's run 2 the blinded reviewer rejected all six
  F4 arms and agreed with the referee each time (`reviewer_verdict` and `reviewer_agrees` in the six
  score records). One of its findings on A/B 1 named the weakness behind the mutant that survived:
  "Writes without If-Match do not increment issue.version." (captured on 2026-10-16, run
  ab-20261016-182828-c81fc0, `reviewer_output`; your output will differ). Every arm failed there,
  so this shows agreement on failures, not that the reviewer finds what the referee misses.

## Questions to take away

- Your team already has a reviewer: a human. Which of A3's three details (criteria, calibration,
  using the product) does your review process have, and which does it skip?
- If the reviewer and the referee disagree on a run, which one do you trust, and what would you
  change in the grading criteria?
