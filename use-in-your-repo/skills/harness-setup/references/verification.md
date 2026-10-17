# Verification checklist: what proves the work is done

Sources are listed at the end of this page.
Assessment checks V1-V5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (V1) Tests exist and cover the behaviour agents will change. | "it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | New tests are added when a new kind of mistake shows up. | Carlini designed "new tests as I identified those failure modes." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | (V2) CI runs the tests on every change, so existing tests keep passing. | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) built CI "so that new commits can’t break existing code." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | (V3) A linter runs in CI, including custom rules whose messages say how to fix the problem. | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) enforces "taste invariants" with custom lints and writes their messages "to inject remediation instructions into agent context." | [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) |
| [ ] | (V4) "Clean state" is written down as a checklist and checked before a feature counts as done. | "By “clean state” we mean the kind of code that would be appropriate for merging to a main branch". | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| [ ] | Test output is short and grep-friendly: a summary line, then one ERROR line per failure with the reason on it. | "Context window pollution"; "write ERROR and put the reason on the same line so grep will find it." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | Long test suites have a fast sample mode. | "Time blindness: Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress." | [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler) |
| [ ] | Features are tested end to end the way a user would use them, not only with unit tests. | The agent in [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) improved "once explicitly prompted to use browser automation tools and do all testing as a human user would." The evaluator in [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) used Playwright to click through the app. | [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | Someone other than the author judges "done": a separate evaluator with written grading criteria and a hard threshold per criterion. | "agents reliably skew positive when grading their own work"; tuning a separate evaluator to be skeptical is "far more tractable". | [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | The evaluator is calibrated, because it is still lenient. | "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs." | [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| [ ] | Some tests are held out from the agent and run only when judging. | SpecBench: visible validation tests check features in isolation; held-out tests compose them and are "never shown to the agent". | [SpecBench](https://arxiv.org/abs/2605.21384) |
| [ ] | (V5) Line coverage can be measured, so generated tests can be judged by what they add. | TestGen-LLM discards "Any test that does not improve coverage". | [Meta, TestGen-LLM](https://arxiv.org/abs/2402.09171) |

## Signs the verification part is missing

- The agent reports "all tests pass" and the feature does not work in the browser.
- A later session sees progress and declares the job done ([Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- Passing tests are taken as proof of a finished job ([Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler): "it is easy to see tests pass and assume
  the job is done, when this is rarely the case.").

## Notes

- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) uses one coding agent that verifies its own work and lists separate testing agents as future
  work. The separate evaluator comes from [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps).
- Use the term "grading criteria" from [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) rather than "rubric".
- [SpecBench](https://arxiv.org/abs/2605.21384) is a preprint; its main finding for this checklist is that compositional failures
  are more common than deliberate exploits.

## Sources

- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11.
- [Anthropic, Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
- [Anthropic, Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps): Prithvi Rajasekaran, "Harness design for long-running application development", Anthropic, 2026-03-24.
- [Anthropic, C compiler](https://www.anthropic.com/engineering/building-c-compiler): Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic, 2026-02-05.
- [Meta, TestGen-LLM](https://arxiv.org/abs/2402.09171): Alshahwan et al. (Meta), "Automated Unit Test Improvement using Large Language Models at Meta", FSE '24, 2024-02-14.
- [SpecBench](https://arxiv.org/abs/2605.21384): Zhao, Srikanth, Wu, Jiang (Weco AI), "SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents", preprint, 2026 (code: https://github.com/WecoAI/SpecBench).
