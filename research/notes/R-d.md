# R-d LangSmith, sandbox, Marp, Vale

Research date: 2026-10-16. Method: official docs fetched as Markdown or HTML, the `langsmith` 0.14.9 wheel downloaded from PyPI and read as source, and the GitHub releases API for version numbers. No LangSmith API key was available, so nothing here was run against a live LangSmith account. Every LangSmith behaviour is marked "docs-verified; live test pending" or "source-verified; live test pending".

## Sources

| id | title | URL | access date | summary |
|---|---|---|---|---|
| D1 | LangSmith Plans and Pricing | https://www.langchain.com/pricing (same content at /pricing-langsmith) | 2026-10-16 | Developer plan: 1 seat, 5k base traces/mo, 14-day base and 180-day extended retention. Overage rates are in tooltip text. FAQ defines a trace. |
| D2 | LangSmith administration overview (usage and billing, data retention, rate limits) | https://docs.langchain.com/langsmith/administration-overview (also served as /langsmith/usage-and-billing) | 2026-10-16 | Retention tiers, auto-upgrade rules, the "Experiments: runs created at extended retention" rule, 429 limits table, usage limits. |
| D3 | Manage billing in your account | https://docs.langchain.com/langsmith/billing | 2026-10-16 | "Personal organizations are limited to 5,000 traces per month until a credit card is added." Retention settings per project. |
| D4 | Observability concepts | https://docs.langchain.com/langsmith/observability-concepts | 2026-10-16 | Trace = collection of runs for one operation. Max 25,000 runs per trace. Datasets persist indefinitely. |
| D5 | Evaluation concepts | https://docs.langchain.com/langsmith/evaluation-concepts | 2026-10-16 | Experiments, splits (an example can be in several splits), pairwise evaluation. |
| D6 | How to evaluate with repetitions | https://docs.langchain.com/langsmith/repetition | 2026-10-16 | `num_repetitions` on `evaluate`/`aevaluate`. 5 examples x 5 repetitions = 25 runs. |
| D7 | How to return multiple scores in one evaluator | https://docs.langchain.com/langsmith/multiple-scores | 2026-10-16 | Python: return a list of `{"key","score"}` dicts. Needs `langsmith>=0.2.0`. |
| D8 | How to define a summary evaluator | https://docs.langchain.com/langsmith/summary | 2026-10-16 | Summary evaluator takes `outputs: list[dict], reference_outputs: list[dict]`. |
| D9 | How to compare experiment results | https://docs.langchain.com/langsmith/compare-experiment-results | 2026-10-16 | UI comparison view under Datasets & Experiments. Red/green marks regressions and improvements. |
| D10 | How to run pairwise evaluations | https://docs.langchain.com/langsmith/evaluate-pairwise | 2026-10-16 | `evaluate_comparative` / pairwise evaluators. |
| D11 | How to create and manage datasets programmatically | https://docs.langchain.com/langsmith/manage-datasets-programmatically | 2026-10-16 | Create from list, CSV, DataFrame, or traces. Set `split` per example. |
| D12 | How to fetch performance metrics for an experiment | https://docs.langchain.com/langsmith/fetch-perf-metrics-experiment | 2026-10-16 | `read_project(..., include_stats=True)` returns latency, tokens, cost, feedback_stats. |
| D13 | Query traces using the SDK | https://docs.langchain.com/langsmith/export-traces | 2026-10-16 | `list_runs` filters and the filter query language. |
| D14 | Migrate run queries to SmithDB | https://docs.langchain.com/langsmith/smithdb-sdk-migration-query-runs | 2026-10-16 | `client.list_runs()` is replaced by async `client.runs.query()`. |
| D15 | How to read experiment results locally | https://docs.langchain.com/langsmith/read-local-experiment-results | 2026-10-16 | Iterate over `ExperimentResults`. `upload_results=False` runs locally. |
| D16 | Tracing quickstart | https://docs.langchain.com/langsmith/observability-quickstart | 2026-10-16 | Env vars `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, `LANGSMITH_ENDPOINT` (EU example). |
| D17 | Cost tracking | https://docs.langchain.com/langsmith/cost-tracking | 2026-10-16 | Cost is derived automatically from token counts and the model price table, including through the OpenAI wrapper. |
| D18 | langsmith on PyPI | https://pypi.org/project/langsmith/ | 2026-10-16 | Latest 0.14.9, uploaded 2026-10-15T13:34:41Z, requires Python >=3.10. |
| D19 | langsmith-sdk GitHub release v0.14.9 | https://github.com/langchain-ai/langsmith-sdk/releases/tag/v0.14.9 | 2026-10-16 | Published 2026-10-15. |
| D20 | langsmith 0.14.9 source (wheel) | files `langsmith/wrappers/_openai.py`, `run_helpers.py`, `client.py`, `evaluation/_runner.py`, `evaluation/evaluator.py`, `schemas.py` | 2026-10-16 | Signatures and behaviour quoted below. |
| D21 | Codex: Agent approvals & security | https://developers.openai.com/codex/agent-approvals-security (also /codex/security, /codex/sandbox) | 2026-10-16 | Sandbox modes, approval policies, network default off, OS mechanisms. |
| D22 | Codex: Sandboxing concepts | https://developers.openai.com/codex/concepts/sandboxing | 2026-10-16 | Definitions of read-only, workspace-write, danger-full-access, on-request, never. bubblewrap prerequisite. |
| D23 | Codex: Configuration reference | https://developers.openai.com/codex/config-reference | 2026-10-16 | `approval_policy` values. `untrusted` is unsupported and `on-failure` is deprecated. |
| D24 | docker container run reference | https://docs.docker.com/reference/cli/docker/container/run/ | 2026-10-16 | Flag table, `--tmpfs` and `--read-only` examples, `--security-opt no-new-privileges`. |
| D25 | Running containers | https://docs.docker.com/engine/containers/run/ | 2026-10-16 | Exit codes 125/126/127, memory/CPU options, OOM killer, capabilities. |
| D26 | Resource constraints | https://docs.docker.com/engine/containers/resource_constraints/ | 2026-10-16 | `--memory` (minimum 6m), `--memory-swap` semantics, `--cpus`. |
| D27 | None network driver | https://docs.docker.com/engine/network/drivers/none/ | 2026-10-16 | `--network none` leaves only loopback. |
| D28 | docker container stats | https://docs.docker.com/reference/cli/docker/container/stats/ | 2026-10-16 | Live resource stream. `--no-stream`, `--format "{{ json . }}"`. |
| D29 | Docker Engine API v1.51 spec | https://docs.docker.com/reference/api/engine/version/v1.51.yaml | 2026-10-16 | `State.OOMKilled` boolean field. |
| D30 | Dockerfile reference (USER) | https://docs.docker.com/reference/dockerfile/ | 2026-10-16 | `USER <user>[:<group>]`. |
| D31 | Docker Desktop WSL 2 backend and best practices | https://docs.docker.com/desktop/features/wsl/ ; https://docs.docker.com/desktop/features/wsl/best-practices/ ; https://docs.docker.com/desktop/settings-and-maintenance/settings/ | 2026-10-16 | WSL >= 2.1.5. Resource limits are set on the WSL VM. Avoid bind mounts from /mnt/c. |
| D32 | Install Docker Engine | https://docs.docker.com/engine/install/ ; https://docs.docker.com/engine/install/ubuntu/ | 2026-10-16 | Convenience script get.docker.com. |
| D33 | Podman installation | https://podman.io/docs/installation | 2026-10-16 | Installer recommended on macOS and Windows. apt/dnf on Linux. `podman machine`. |
| D34 | Podman for Windows tutorial | https://github.com/podman-container-tools/podman/blob/main/docs/tutorials/podman-for-windows.md | 2026-10-16 | MSI installer, `podman machine init` with WSL or Hyper-V provider, rootful option, Docker API listener. |
| D35 | Podman releases | https://github.com/podman-container-tools/podman/releases/tag/v6.1.4 | 2026-10-16 | Latest v6.1.4, 2026-10-12. The repo moved from containers/podman. |
| D36 | Colima README and releases | https://github.com/abiosoft/colima ; https://github.com/abiosoft/colima/releases/tag/v0.10.3 | 2026-10-16 | `brew install colima`, `colima start --cpu --memory --disk`. Latest v0.10.3, 2026-06-04. |
| D37 | Marp CLI README and release | https://github.com/marp-team/marp-cli ; https://github.com/marp-team/marp-cli/releases/tag/v4.5.1 | 2026-10-16 | v4.5.1 (2026-09-06), Node >=18, `--pptx`, experimental `--pptx-editable`, browser requirement. |
| D38 | Marpit presenter notes | https://marpit.marp.app/usage?id=presenter-notes | 2026-10-16 | HTML comments (other than directives) become presenter notes. |
| D39 | Vale installation | https://vale.sh/docs/install (docs now also at docs.vale.sh) | 2026-10-16 | brew, choco, scoop, winget, snap, apt via pkg.haus, mise pin `vale@3.24.0`. |
| D40 | Vale existence check | https://vale.sh/docs/checks/existence | 2026-10-16 | `extends: existence`, `tokens`, `ignorecase`, `message` with `%s`. |
| D41 | Vale .vale.ini | https://vale.sh/docs/vale-ini (https://docs.vale.sh/topics/.vale.ini.md) | 2026-10-16 | `StylesPath`, `MinAlertLevel`, `[*]` sections, `BasedOnStyles`. |
| D42 | Vale CLI | https://docs.vale.sh/topics/cli.md | 2026-10-16 | Exit codes 0/1/2, `--no-exit`, `--minAlertLevel`. |
| D43 | Vale styles | https://vale.sh/docs/styles | 2026-10-16 | A style is a directory under StylesPath. Rule default level is warning. "Only errors set a non-zero exit code." |
| D44 | Vale release v3.24.0 | https://github.com/vale-cli/vale/releases/tag/v3.24.0 | 2026-10-16 | Latest, 2026-10-01. The repo moved from errata-ai/vale. |

## LangSmith facts

| item | verified value | exact quote (30 words or fewer) | source | status |
|---|---|---|---|---|
| Developer seats | 1 seat, $0 | "Maximum of 1 seat (free)" | D1 | docs-verified |
| Monthly base trace allowance | 5,000 base traces per month | "5k base traces / mo included" ... "Pay as you go thereafter" | D1 | docs-verified |
| Base retention | 14 days | "Base traces have a shorter retention period of 14 days." | D1, D2 | docs-verified |
| Extended retention | 180 days (the older 400-day figure no longer applies to new traces) | "Starting September 14, 2026, the maximum long-lived trace retention period for SaaS customers is changing to 180 days." | D2, D3 | docs-verified |
| Overage price, base | 0.005 LSU per base trace (1 LSU = $1, so $5.00 per 1,000) | tooltip: "0.005 LSU/base trace" ; FAQ: "1 LSU = $1" | D1 (pricing table tooltip) | docs-verified; check again before publishing (the rate appears only in tooltip text) |
| Extended upgrade price | 0.0025 LSU per upgraded trace ($2.50 per 1,000) on top of the base charge | tooltip: "0.0025 LSU/extended trace upgrade" | D1 | docs-verified; check again before publishing |
| No card on file: monthly cap | Hard cap of 5,000 traces per month. Calls past it get HTTP 429, and the cap resets at the start of the UTC month | "Personal organizations are limited to 5,000 traces per month until a credit card is added." ; "This is thrown by our application and applies only to the Developer Plan Tier when there is no payment method on file." | D3, D2 | docs-verified; live test pending (confirm whether the SDK logs a warning or fails silently) |
| What happens to traces past a limit | Rejected with 429, not stored. For project and user limits: "new traces are dropped and are not ingested again until the limit resets." | "LangSmith will respond with HTTP Status Code 429 indicating that rate or usage limits have been exceeded" | D2 | docs-verified; live test pending |
| Hourly events limit (no card) | 50,000 events per hour (250,000 with a card). An event is the creation or update of a run | "Developer (no payment on file) / 50,000 events / 1 hour" | D2 | docs-verified |
| Hourly ingest size (no card) | 500 MB per hour (2.5 GB with a card) | "Developer (no payment on file) / 500MB / 1 hour" | D2 | docs-verified |
| Per-minute API limits (all plans) | POST/PATCH /runs 5000/min; POST /feedbacks 5000/min; GET /runs/:id 30/min; DELETE /sessions 30/min; all other endpoints 2000/min, per key | "The LangSmith SDK ... batching up to 100 runs from a single session ID into a single API call." | D2 | docs-verified |
| Trace definition | Root run plus all its child runs = 1 trace (shared trace ID) | "A trace is a collection of runs for a single operation." ; "Runs are bound to a trace by a unique trace ID." | D4 | docs-verified |
| Max runs per trace | 25,000 | "Each trace is limited to a maximum of 25,000 runs." | D4 | docs-verified |
| Evaluator runs count as traces | Yes. In `evaluate()`, each evaluator call on each target run is traced as its own root trace in a project named `evaluators`. Summary evaluators are traced the same way. Turn this off with `disable_evaluator_tracing=True` | pricing FAQ: "A trace represents a single execution of your application—whether it's an agent, evaluator, or playground session." ; SDK: "Whether to skip tracing evaluator invocations to the `evaluators` project" | D1, D20 (`_runner.py` lines ~199-205, ~1708-1745) | docs- and source-verified; live test pending (count traces per experiment) |
| Experiment runs retention | Experiment (target) runs are created at extended retention (180 days) by default | "Experiments: Runs are created at extended retention by default." | D2 | docs-verified; live test pending (does the free 5k cap also cover these? are they billed as upgrades?) |
| SDK feedback default | `Client.create_feedback(..., extend_trace_retention=True)` is the default. `evaluate()` logs feedback through this path without overriding it | SDK docstring: "If false, create the feedback without extending the trace's retention tier." ; docs: "explicitly passes `extend_trace_retention=true`" | D20 (`client.py` line 8347), D2 | source-verified; live test pending |
| UI feedback | Does not upgrade | "The LangSmith UI sends feedback and notes without extending retention." | D2 | docs-verified |
| Annotation queue adds | Manual adds do not upgrade by default | "Manually adding runs or threads to an annotation queue does not upgrade retention by default." | D2 | docs-verified |
| Online evaluators / automation rules | Upgrade by default (opt-out available) | "Retention extension is enabled by default for new online evaluators and automation rules." | D2 | docs-verified |
| Datasets | Not an upgrade trigger. Dataset data is kept indefinitely | "Datasets have an indefinite data retention period." | D2, D4 | docs-verified |
| After retention ends | Trace gone from UI and API. Inputs and outputs deleted within a day | "traces are no longer accessible in the tracing project UI or via the API." | D2 | docs-verified |
| Extended-limit side effect | If an extended-trace usage limit is reached: rule matching, adding feedback, and annotation-queue adds stop working | "you can no longer: 1. match run rules 2. add feedback to traces 3. add runs to annotation queues" | D2 | docs-verified; whether a no-card Developer org has an extended limit is unknown (see Open gaps) |
| SDK version | `langsmith` 0.14.9, released 2026-10-15, Python >=3.10 | n/a | D18, D19 | verified |
| `wrap_openai` + Responses API | Supported since 0.3.16. It wraps `client.responses.create` (streaming too) and `client.responses.parse`. It converts the response's `usage` into `usage_metadata` (token counts) | "Support for Responses API added." (Behavior changed in `langsmith` 0.3.16) | D20 (`wrappers/_openai.py` lines ~446-572, 586-603) | source-verified; live test pending |
| Cost for wrapped OpenAI calls | Computed automatically from token counts and the workspace model price table | "LangSmith automatically records LLM token usage and costs for major providers" ; Automatically: "Using LangSmith wrappers for OpenAI or Anthropic" | D17 | docs-verified; live test pending (confirm the Responses model name is in the price table) |
| `run_type` values | `"tool", "chain", "llm", "retriever", "embedding", "prompt", "parser"`; default `"chain"` | `RUN_TYPE_T = Literal["tool", "chain", "llm", "retriever", "embedding", "prompt", "parser"]` | D20 (`client.py` line 666) | source-verified |
| Env vars | `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (default project created if unset), `LANGSMITH_ENDPOINT` (needed outside US; EU `https://eu.api.smith.langchain.com`, no trailing slash) | "Do not add a trailing slash to the URL, as this can cause authentication errors." | D16 | docs-verified |
| Run URL | `RunTree.get_url()` (cached). `Client.get_run_url(run=...)` is deprecated; use `Client.runs.get_url`. `ExperimentResults.url` and `.comparison_url` exist | "Use :meth:`langsmith.Client.runs.get_url` instead. ... Will be removed after Jan 31, 2027." | D20 | source-verified; live test pending |
| `list_runs` deprecation | Deprecated in favour of async `client.runs.query()`; removal after 2027-01-31. Still the method shown in the docs examples (D13) | "`client.runs.query()` is now async. Call it with `await`." | D14, D20 | docs- and source-verified |
| `get_experiment_results` | Deprecated; replacement `Client.datasets.experiment_runs.query` | "Will be removed after Jan 31, 2027." | D20 (`client.py` line ~11363) | source-verified |
| Dataset size limits (free plan) | Not documented in the pages read | n/a | D2, D11 | gap |

## LangSmith SDK usage notes

All code below is our own illustration based on the 0.14.9 signatures. None of it has been run against a live account.

### Tracing

```python
# env: LANGSMITH_TRACING=true, LANGSMITH_API_KEY=..., LANGSMITH_PROJECT=harness-dev
from langsmith import traceable, Client
from langsmith.run_helpers import get_current_run_tree
from langsmith.wrappers import wrap_openai
import openai

oai = wrap_openai(openai.OpenAI())          # responses.create is traced as an llm run with usage_metadata

@traceable(run_type="tool", name="sandbox_exec")
def run_in_container(cmd: str) -> dict:
    ...                                       # nested automatically under the caller's run

@traceable(run_type="chain", name="agent_run", tags=["section-1"], metadata={"variant": "baseline"})
def agent_run(task: str) -> dict:
    resp = oai.responses.create(model="<model>", input=task)
    out = run_in_container("pytest -q")
    rt = get_current_run_tree()
    return {"answer": resp.output_text, "trace_url": rt.get_url() if rt else None}

# Per-call overrides without redecorating:
agent_run("fix bug", langsmith_extra={"project_name": "harness-eval", "metadata": {"seed": 1}, "tags": ["smoke"]})
Client().flush()   # before process exit in short CLI runs
```

- `traceable(run_type="chain", *, name, metadata, tags, client, reduce_fn, project_name, process_inputs, process_outputs, enabled, ...)`. `langsmith_extra` keys: `name, reference_example_id, run_extra, parent, project_name, metadata, tags, ...`.
- Nesting: calling one `@traceable` function inside another makes a child run of the same trace, so one trace per agent run.
- `trace` is also available as a context manager (`langsmith.run_helpers.trace`). `tracing_context(enabled=..., project_name=...)` overrides settings for a block of code.

### evaluate / aevaluate

```text
evaluate(target, /, data=None, evaluators=None, summary_evaluators=None, metadata=None,
         experiment_prefix=None, description=None, max_concurrency=0, num_repetitions=1,
         client=None, blocking=True, experiment=None, upload_results=True,
         disable_evaluator_tracing=False, error_handling="log", **kwargs) -> ExperimentResults
aevaluate(... same ..., evaluators may be async) -> AsyncExperimentResults
evaluate_comparative((exp_a, exp_b), /, evaluators, experiment_prefix=None, description=None,
         max_concurrency=5, client=None, metadata=None, load_nested=False,
         randomize_order=False) -> ComparativeExperimentResults
```

- `max_concurrency`: "If `None` then no limit is set. If `0` then no concurrency." (D20)
- `num_repetitions`: "Each item in the dataset will be run and evaluated this many times." It is confirmed in the source and in D6. The UI shows the average per feedback key and the standard deviation across repetitions.
- `upload_results=False` runs tracing in `"local"` mode (`tracing_context(enabled="local")`), so nothing is uploaded. Useful for offline dry runs that use no trace allowance.
- `disable_evaluator_tracing=True` keeps feedback but does not create evaluator traces. This roughly halves the trace count when there is one evaluator.
- `evaluate((exp_a, exp_b), evaluators=[...])` routes to comparative mode. `num_repetitions`, `summary_evaluators`, `data`, `experiment`, and `disable_evaluator_tracing` are rejected in that mode.
- Evaluator arguments are matched by name: `run, example, inputs, outputs, reference_outputs, attachments`. Summary evaluators take `runs, examples, inputs, outputs, reference_outputs` as lists.
- Evaluator return shapes accepted (`_format_evaluator_result`): bool/int/float becomes `{"score": x}`; str becomes `{"value": s}`; dict is a single result (`{"key","score"|"value","comment",...}`); list of dicts becomes `{"results": [...]}`; or `EvaluationResults` = `{"results": [EvaluationResult, ...]}`.

```python
def rubric(outputs: dict, reference_outputs: dict) -> list[dict]:
    return [
        {"key": "tests_pass", "score": int(outputs["tests_passed"])},
        {"key": "diff_lines", "score": outputs["diff_lines"]},
        {"key": "verdict", "value": "ok" if outputs["tests_passed"] else "fail"},
    ]

def pass_rate(outputs: list[dict], reference_outputs: list[dict]) -> dict:
    return {"key": "pass_rate", "score": sum(o["tests_passed"] for o in outputs) / len(outputs)}

res = evaluate(agent_target, data=client.list_examples(dataset_name="harness-tasks", splits=["smoke"]),
               evaluators=[rubric], summary_evaluators=[pass_rate],
               experiment_prefix="baseline", metadata={"model": "<model>", "sandbox": "docker"},
               num_repetitions=3, max_concurrency=2)
print(res.experiment_name, res.url, res.comparison_url)
rows = [ {"example_id": str(r["example"].id), "outputs": r["run"].outputs,
          "scores": {e.key: e.score for e in r["evaluation_results"]["results"]}} for r in res ]
```

- Comparison: the UI comparison view (D9) is opened by selecting experiments on the dataset's Experiments tab and clicking Compare. `ExperimentResults.comparison_url` gives a link. For pairwise LLM-judge scoring use `evaluate_comparative` (D10).

### Datasets

```python
c = Client()
ds = c.create_dataset("harness-tasks", description="...", metadata={"course": "harness"})
c.create_examples(dataset_id=ds.id, examples=[
    {"inputs": {"task": "..."}, "outputs": {"expected": "..."}, "metadata": {"id": "t01"}, "split": ["smoke", "section-1"]},
])
smoke = list(c.list_examples(dataset_name="harness-tasks", splits=["smoke"]))
```

- `ExampleCreate` fields include `inputs, outputs, metadata, split: str | list[str]`. An example can be in more than one split (D5). There is no JSONL uploader: read the JSONL in Python and pass a list to `create_examples` (`max_concurrency` 1 to 3). `upload_csv` and DataFrame paths also exist (D11).
- Reference outputs are the example `outputs` and reach evaluators as `reference_outputs`.

### Export (so reports outlive retention)

- Best approach: write rows from the `ExperimentResults` iterator to local JSON at run time (above). This does not depend on retention.
- Aggregate stats: `c.read_project(project_name=res.experiment_name, include_stats=True)` returns `run_count, latency_p50/p99, total_tokens, prompt_tokens, completion_tokens, total_cost, feedback_stats{key:{n,avg,...}}` (D12). Experiments and tracing projects are both "sessions".
- Runs: `c.list_runs(project_name=..., is_root=True, select=[...])` works but is deprecated. New code should use `await c.runs.query(...)` (D14).
- Feedback: `c.list_feedback(run_ids=[...])`.

### Key validation (`make doctor`)

- Cheapest authenticated call: `GET {endpoint}/api/v1/sessions?limit=1` with header `x-api-key`. The SDK itself uses `GET /sessions` with `limit=1` to learn the tenant ID. In Python: `next(iter(Client().list_projects(limit=1)), None)`. Catch `langsmith.utils.LangSmithAuthError` (401/403), `LangSmithRateLimitError` (429), and `LangSmithConnectionError`. `Client.info` (`GET /info`) does not prove the key is valid: it logs a warning on failure instead of raising. Status: source-verified; live test pending (confirm 401 vs 403 and the 429 body when the monthly cap is hit).

## Retention decision input

- On the free plan, scores do not change the retention or cost of experiment traces, because experiment runs are already created at extended retention by default (D2). So the question that matters is not "do scores upgrade traces" but "are experiment traces extended, and how does a no-card Developer org handle extended traces". The docs do not answer the second part.
- For ordinary tracing projects (agent runs outside `evaluate()`): `create_feedback` from the SDK upgrades the whole trace to extended by default (`extend_trace_retention=True`). Passing `extend_trace_retention=False` keeps the trace at base. UI feedback and manual annotation-queue adds do not upgrade. Online evaluators and automation rules upgrade unless you opt out.
- Datasets keep data indefinitely and are not an upgrade trigger.
- Recommendation:
  1. Store each score in the run's own outputs or metadata, and also in a local JSON report written at run time. Use LangSmith feedback only as a view on top of that.
  2. Pass `extend_trace_retention=False` in any direct `create_feedback` call on non-experiment traces.
  3. Use `disable_evaluator_tracing=True` by default to halve trace usage. Turn it off only in the lesson that shows evaluator traces.
  4. Budget traces per experiment as examples x repetitions x (1 + number of evaluators, unless evaluator tracing is disabled) + summary evaluators. Keep the course total well under 5,000 per learner per month.
  5. Use `upload_results=False` for dry runs.
  6. Live-test on a fresh no-card Developer account: run a 5-example experiment, then check Settings > Usage for base vs extended counts, and confirm no 429 or charge prompt appears.

## Sandbox facts

### Codex (official OpenAI docs, D21-D23)

- Sandbox modes (`sandbox_mode` / `--sandbox`): `read-only | workspace-write | danger-full-access`.
  - read-only: "The agent can inspect files, but it can't edit files or run commands without approval."
  - workspace-write: "The agent can read files, edit within the workspace, and run routine local commands inside that boundary. This is the default low-friction mode for local work."
  - danger-full-access: "The agent runs without sandbox restrictions. This removes the filesystem and network boundaries".
- Approval policies (`approval_policy` / `--ask-for-approval`, `-a`): `on-request | never | { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. "untrusted is unsupported, and on-failure is deprecated; use on-request for interactive runs or never for non-interactive runs." A project-level `trust_level = "untrusted"` entry is still supported. Approval reviewer: `approvals_reviewer = "user"` (default) or `"auto_review"`.
- Network default: "By default, the agent runs with network access turned off." To enable it in workspace-write: `[sandbox_workspace_write] network_access = true`. Optional `features.network_proxy` domain allow/deny rules.
- Presets: Auto = `--sandbox workspace-write --ask-for-approval on-request` (the default for version-controlled folders; read-only for other folders). CI read-only = `--sandbox read-only --ask-for-approval never`. `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`): "No sandbox; no approvals (not recommended)". Non-interactive: `codex exec --sandbox workspace-write`.
- Protected paths in workspace-write: `.git` (including a gitdir pointer target), `.agents`, `.codex`, `.aws` under writable roots stay read-only. Writable roots include the current directory and temp dirs such as /tmp.
- OS mechanisms: "macOS uses Seatbelt policies and runs commands using sandbox-exec with a profile ( -p )". "Linux uses bwrap plus seccomp by default." "Windows supports MXC , with elevated and unelevated as legacy fallbacks. In ... WSL2 , Codex uses the Linux sandbox implementation." WSL1 is unsupported from 0.115. On Linux/WSL2, install bubblewrap first (`sudo apt install bubblewrap` / `sudo dnf install bubblewrap`). Test commands: `codex sandbox macos|linux|windows [COMMAND]...` (aliases `codex sandbox seatbelt`, `codex sandbox landlock`).

### Docker flags (D24-D31)

| purpose | syntax | quote / note | source |
|---|---|---|---|
| no network | `--network none` | "Within the container, only the loopback device is created." | D27 |
| memory | `-m 512m` / `--memory=512m` | "Minimum is 6M." Set `--memory-swap` equal to `--memory` to deny swap: "the container doesn't have access to swap". If unset, swap up to the same amount again is allowed | D25, D26 |
| CPU | `--cpus=1.5` | "Number of CPUs. Number is a fractional number. 0.000 means no limit." | D25, D26 |
| process count | `--pids-limit 256` | "Tune container pids limit (set -1 for unlimited)" | D24 |
| read-only root + scratch | `--read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m` | example: `docker run -d --tmpfs /run:rw,noexec,nosuid,size=65536k my_image`; `--read-only` "Mount the container's root filesystem as read only" | D24 |
| non-root | `--user 1000:1000` or Dockerfile `USER <user>[:<group>]` | "Username or UID (format: <name\|uid>[:<group\|gid>])" | D24, D30 |
| drop capabilities | `--cap-drop ALL` (also `--cap-drop=ALL`) | `--cap-add`/`--cap-drop` accept names with or without `CAP_`; `ALL` is accepted (docs show `--cap-add=ALL`) | D25 |
| no privilege escalation | `--security-opt no-new-privileges` (or `no-new-privileges=true`) | "Disable container processes from gaining new privileges" | D24 |
| auto-remove, init | `--rm`, `--init` | `--init` "forwards signals and reaps processes" | D24 |
| live usage | `docker stats <name>`; one sample: `docker stats --no-stream --format "{{ json . }}" <name>` | "Display a live stream of container(s) resource usage statistics" | D28 |
| OOM signal | `docker inspect --format '{{.State.OOMKilled}} {{.State.ExitCode}}' <id>` | API: OOMKilled = "Whether a process within this container has been killed because it ran out of memory since the container was last started." Exit 137 = 128+SIGKILL(9): this is the POSIX shell convention, not stated on the Docker pages read. Docker documents only 125/126/127 as Docker-specific | D29, D25 |

Example combined command (ours):
`docker run --rm --network none --memory 1g --memory-swap 1g --cpus 1 --pids-limit 256 --read-only --tmpfs /tmp:rw,nosuid,size=256m --user 1000:1000 --cap-drop ALL --security-opt no-new-privileges -v "$PWD/work:/work" -w /work harness-sandbox:latest bash -lc "pytest -q"`

Docker Desktop on Windows (WSL2):
- Needs WSL 2.1.5 or later.
- "In WSL 2 mode, configure memory, CPU, and swap limits on the WSL 2 utility VM" (that is, `.wslconfig`). Per-container `--memory`/`--cpus` still apply inside that VM.
- Keep bind-mounted code in the Linux filesystem: "avoid `docker run -v /mnt/c/users:/users`".
- Uninstall any Docker Engine installed inside a WSL distro before installing Desktop.
- In PowerShell, quote `--format` templates and use `${PWD}` instead of `$PWD` in paths (our note).

### Alternatives

- Docker Engine on Linux or inside WSL2 (no Desktop): convenience script `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh` (D32; the docs suggest `--dry-run` first and the apt repository for production). Rootless mode is documented at /engine/security/rootless/.
- Podman v6.1.4 (2026-10-12). The repo is now podman-container-tools/podman.
  - Linux: `sudo apt-get -y install podman` (Ubuntu 20.10+, Debian 11+) or `sudo dnf -y install podman` (Fedora; add `podman-machine` if you need `podman machine`).
  - macOS: the installer from podman.io is recommended ("It's not recommended to install via Homebrew"), then `podman machine init && podman machine start`.
  - Windows: MSI installer, then `podman machine init` (provider `--provider wsl` or `--provider hyperv`) and `podman machine start`. Rootless by default; `podman machine set --rootful` switches.
  - Docker compatibility: "Docker-compatible CLI interface" and "Podman on Mac and Windows also listens for Docker API clients". The Windows tutorial says Docker API clients default to its address with no DOCKER_HOST change.
  - Rootless `--memory`/`--cpus`/`--pids-limit` depend on cgroup v2 delegation (our note; live test pending).
- Colima v0.10.3 (macOS and Linux): `brew install colima` (also MacPorts, Nix, mise), plus a Docker client (`brew install docker`). Start with `colima start --cpu 2 --memory 4 --disk 20`. Default VM: 2 CPU, 2 GiB, 100 GiB. Runtimes: docker (default), containerd, incus.

## Marp and Vale

### Marp CLI (D37, D38)

- Version 4.5.1 (GitHub release 2026-09-06; npm `latest` 4.5.1). npm `engines`: `node >=18`. The README says "Node.js v18 and later is required".
- Run without installing: `npx @marp-team/marp-cli@latest deck.md --pdf` / `--pptx` / `-o deck.html`. Standalone binaries and a container image (marpteam/marp-cli) are also available.
- Browser: "You have to install any one of Google Chrome, Microsoft Edge, or Mozilla Firefox to convert slide deck into PDF, PPTX, and image(s)." Choose with `--browser chrome|edge|firefox` (default `auto`) or `--browser-path`.
- `--pptx`: slides are pre-rendered images, so content is not editable. Presenter notes are carried into the PPTX ("includes rendered Marp slide pages and the support of Marpit presenter notes").
- `--pptx-editable` is marked "[EXPERIMENTAL]". It needs the browser plus LibreOffice Impress, may fail with complex themes, and "presenter notes are not supported". Not recommended for the course.
- Speaker notes: any HTML comment that is not a directive, for example `<!-- say this aloud -->`. `--notes` exports notes to .txt. `--pdf-notes` adds PDF note annotations.
- Local images in PDF/PPTX conversion need `--allow-local-files` ("conversion that is using the browser cannot use local files by default").

### Vale (D39-D44)

- Version v3.24.0 (2026-10-01). The repo is now vale-cli/vale and the docs are at docs.vale.sh (vale.sh/docs URLs still work).
- Install:
  - macOS: `brew install vale`
  - Windows: `choco install vale`, `scoop install vale`, or `winget install -e --id errata-ai.Vale`
  - Linux: `sudo snap install vale`, Arch `sudo pacman -S vale`, Debian/Ubuntu via the pkg.haus APT archive then `sudo apt install vale`
  - Project pin: `mise use vale@3.24.0`, `npm install --save-dev @vvago/vale`, or `pip install vale`. The PyPI `vale` package is a third-party wrapper (daniperez/vale-python-package) at 3.22.0.0, behind the current release, so prefer a version-pinned binary.
- Minimal `.vale.ini`:

```ini
StylesPath = styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Course
```

- Custom style: directory `styles/Course/`, one rule per YAML file, addressed as `Course.<FileName>`. Banned-word rule `styles/Course/Banned.yml`:

```yaml
extends: existence
message: "Avoid '%s'."
level: error          # default is warning; "Only errors set a non-zero exit code."
ignorecase: true
tokens:
  - seamless
  - leverage
  - cutting-edge
```

- Exit codes: `0` = no error-level alerts (warnings and suggestions do not count); `1` = at least one `error` (`--no-exit` forces 0); `2` = Vale could not run (missing config, bad rule, bad path). `--minAlertLevel=error` overrides the config.

## Open gaps

1. Whether experiment runs (extended by default) count against the 5,000/month no-card cap the same way base traces do, and whether extended upgrades are blocked, allowed free, or produce 429 on a no-card Developer org. Live test pending.
2. Whether the `evaluators` project traces are base or extended (likely the project default, which is base). Live test pending.
3. Whether experiment retention can be set to base per experiment or project to avoid extended. The docs say only "by default".
4. Whether experiment feedback and `read_project(include_stats=True)` aggregates stay readable after the underlying runs expire. Assume they do not, and export at run time.
5. Dataset, example, and payload size limits on the free plan: not found in the official pages read.
6. Exact HTTP status and body when an invalid key is used (401 vs 403), and SDK behaviour (warning vs exception) when background tracing gets 429. Live test pending.
7. Whether the LangSmith price table includes the specific OpenAI model used with the Responses API (needed for cost display).
8. Overage rates come from pricing-page tooltip text. Re-check before publishing slide numbers.
9. Rootless Podman resource-flag support on each learner OS: live test pending.

## Corrections to the brief

- Extended retention is 180 days for new traces since 2026-09-14, not 400 days.
- On Linux, Codex uses bubblewrap (`bwrap`) plus seccomp by default, not Landlock. `landlock` survives only as a CLI alias. Windows uses MXC (with elevated/unelevated fallbacks). WSL2 uses the Linux sandbox and WSL1 is unsupported.
- The Codex approval policy names have changed: `untrusted` is retired (it can stop Codex from starting) and `on-failure` is deprecated. Valid values are `on-request`, `never`, or `granular`.
- Feedback scores are not the main retention question: `evaluate()` experiment runs are created at extended retention by default, whatever feedback is attached.
- Evaluator calls inside `evaluate()` are separate traces (project `evaluators`), one per evaluator per run, unless `disable_evaluator_tracing=True`.
- `Client.list_runs`, `get_run_url`, `read_run`, and `get_experiment_results` are deprecated in langsmith 0.14.x (removal after 2027-01-31). Replacements: `client.runs.query()` (async), `client.runs.get_url`, `client.runs.retrieve`, `client.datasets.experiment_runs.query`.
- LangSmith pricing is now stated in LSUs (1 LSU = $1), not dollars per 1k traces.
- There is no JSONL upload helper. Build `examples` lists from JSONL in Python.
- Repositories moved: Podman to podman-container-tools/podman, Vale to vale-cli/vale (docs at docs.vale.sh).
- Docker documents exit code 137 nowhere on the pages read. Use `State.OOMKilled` as the authoritative OOM signal and treat 137 as the SIGKILL convention.
