# post-class-reading

Three short pieces that go further than class time allows. Read them after
[../concepts.md](../concepts.md). Each ends with "Why it matters for your own repo".

| Piece | Reading time | What it covers |
|---|---|---|
| [01-sandboxes-compared.md](01-sandboxes-compared.md) | about 10 min | The shipharness container policy next to A4's per-agent containers, A5's three-layer security model, and Codex's sandbox modes and approval policies (official docs; RESEARCH correction 11 on bwrap plus seccomp); why the pilot saw no denials |
| [02-scope-layer-source-tour.md](02-scope-layer-source-tour.md) | about 12 min | The scope layer's source with commentary: what the agent is told, how patches and commands are checked and reverted, the evidence behind `passes`, how the referee counts the S3 measure, and the two measurement fixes from the M6 pilot |
| [03-reading-the-s3-results.md](03-reading-the-s3-results.md) | about 8 min | What the M6 pilot found on F3, how to read a measure one arm meets by construction, the `section-3` variants, the ablation without the scope layer, and the experiment results |

Primary sources behind these pieces, in the order they matter for S3:

- A2, "Effective harnesses for long-running agents": the feature list section (`passes`, the strongly
  worded instruction, JSON over Markdown) and "work on only one feature at a time".
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- A4, "Building a C compiler with a team of parallel Claudes": the sections on running Claude in
  parallel (one Docker container per agent) and on evaluation (no internet access).
  https://www.anthropic.com/engineering/building-c-compiler
- A5, "Autonomous Coding Agent Demo" README: the security model and the generated project structure.
  https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- D21-D23, the Codex docs on agent approvals and security, sandboxing, and configuration.
  https://developers.openai.com/codex/agent-approvals-security
