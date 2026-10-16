# Verification checklist: what proves the work is done

Source ids and finding ids refer to the shipharness research register (RESEARCH.md and
research/notes/R-a.md, R-b.md). Assessment checks V1-V5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (V1) Tests exist and cover the behaviour agents will change. | "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem." | A4, F-a-127 |
| [ ] | New tests are added when a new kind of mistake shows up. | Carlini designed "new tests as I identified those failure modes." | A4, F-a-128 |
| [ ] | (V2) CI runs the tests on every change, so existing tests keep passing. | A4 built CI "so that new commits can’t break existing code." | A4, F-a-129 |
| [ ] | (V3) A linter runs in CI, including custom rules whose messages say how to fix the problem. | A1 enforces "taste invariants" with custom lints and writes their messages "to inject remediation instructions into agent context." | A1, F-a-96, F-a-97 |
| [ ] | (V4) "Clean state" is written down as a checklist and checked before a feature counts as done. | "By “clean state” we mean the kind of code that would be appropriate for merging to a main branch". | A2, F-a-84 |
| [ ] | Test output is short and grep-friendly: a summary line, then one ERROR line per failure with the reason on it. | "Context window pollution"; "write ERROR and put the reason on the same line so grep will find it." | A4, F-a-131, F-a-132 |
| [ ] | Long test suites have a fast sample mode. | "Time blindness: Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress." | A4, F-a-133 |
| [ ] | Features are tested end to end the way a user would use them, not only with unit tests. | A2's agent improved "once explicitly prompted to use browser automation tools and do all testing as a human user would." A3's evaluator used Playwright to click through the app. | A2, F-a-104, F-a-105; A3, F-a-118 |
| [ ] | Someone other than the author judges "done": a separate evaluator with written grading criteria and a hard threshold per criterion. | "agents reliably skew positive when grading their own work"; tuning a separate evaluator to be skeptical is "far more tractable". | A3, F-a-15, F-a-111, F-a-119 |
| [ ] | The evaluator is calibrated, because it is still lenient. | "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs." | A3, F-a-112, F-a-115 |
| [ ] | Some tests are held out from the agent and run only when judging. | SpecBench: visible validation tests check features in isolation; held-out tests compose them and are "never shown to the agent". | B13, F-b-42, F-b-43 |
| [ ] | (V5) Line coverage can be measured, so generated tests can be judged by what they add. | TestGen-LLM discards "Any test that does not improve coverage". | B11, F-b-20 |

## Signs the verification part is missing

- The agent reports "all tests pass" and the feature does not work in the browser.
- A later session sees progress and declares the job done (A2, F-a-13).
- Passing tests are taken as proof of a finished job (A4: "it is easy to see tests pass and assume
  the job is done, when this is rarely the case.").

## Notes

- A2 uses one coding agent that verifies its own work and lists separate testing agents as future
  work (F-a-109). The separate evaluator comes from A3.
- Use A3's term "grading criteria" rather than "rubric".
- SpecBench (B13) is a preprint; its main finding for this checklist is that compositional failures
  are more common than deliberate exploits (F-b-50).
