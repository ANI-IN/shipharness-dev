# SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents

Reading time: about 5 minutes.
Source: Zhao, Srikanth, Wu, Jiang (Weco AI), "SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents", preprint, v2 2026-09-09, <https://arxiv.org/abs/2605.21384>, with its repository <https://github.com/WecoAI/SpecBench> ([evidence](../../docs/evidence.md#src-specbench)).

> **Terms on this page**
>
> - **Visible tests**: Tests the agent can read and run while it works. SpecBench calls them validation tests.
> - **Hidden tests**: Tests the agent never sees; the referee runs them after the agent stops.
> - **Reward hacking gap**: How much more of the visible suite an agent passes than of the held-out suite.

## Why it matters

If every test lives where the agent can read it, a green suite tells you about those tests only.
SpecBench measures how far that can mislead you. It gives coding agents long tasks with a visible
suite, then scores them on a second suite they never see. Section 4's hidden tests follow its design.
Do not confuse it with Spec-Bench (arXiv 2401.07851), an unrelated benchmark.

## Three key ideas

1. **Two suites, one spec.** Each task has "visible validation tests that exercise specified features
   in isolation" and "held-out tests that compose those same features to simulate real-world usage."
   The held-out suite is "never shown to the agent, is used solely for evaluation." It asks for
   nothing new: "test introduces no requirements beyond what [spec] and val already specify."

2. **Agents pass the visible suite and still fail the held-out one.** "while every frontier agent
   saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on
   holdout suites." The gap also grows with the size of the code.

3. **The cause is mostly composition, not cheating.** "deliberate exploits are rare, while
   compositional failures account for a much larger fraction of reward hacking behavior." Features
   that pass alone fail together. And better visible tests do not close the gap: "reward hacking
   cannot be eliminated by improving the test suite alone".

The course applies the design to TeamTrack. Hidden tests live outside each arm's workspace, and the
referee mounts them read-only in its own container. F4 has 69 of them, including two files that
combine F4 with earlier features. They check only what the feature spec states. In the captured
Section 4 run, the one hidden test that failed combined two rules: a stale `If-Match` and an invalid
body.

## Apply it to your repo

1. Pick two features of your service that users combine, such as editing and permissions, or
   pagination and filters. Write one test that uses both, the way a user would.
2. Keep a few such tests out of the agent's reach: a separate folder the agent's sandbox does not
   mount, or a CI job it cannot edit.
3. Write them from the spec, not from the code. A held-out test that checks an unwritten rule
   measures the spec's gaps, not the agent.
4. After each agent task, compare the two results. A green visible suite with a red held-out test is
   the gap this paper measures.
