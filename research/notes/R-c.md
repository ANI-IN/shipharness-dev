# R-c OpenAI API, pricing, caching

Research date: 2026-10-16. All facts below come from official OpenAI pages (developers.openai.com, which platform.openai.com/docs now 301-redirects to), PyPI, and github.com/openai/openai-python. Third-party aggregator pages (OpenRouter and similar) were used only to confirm that the model name exists and are not cited for any fact.

## Sources

| id | title | URL | access date | summary |
|---|---|---|---|---|
| C1 | GPT-6 Luna model page | https://developers.openai.com/api/docs/models/gpt-6-luna | 2026-10-16 | `gpt-6-luna` exists. $0.10 in / $0.01 cached / $0.125 cache write / $0.50 out. 1,050,000 ctx, 922,000 max input, 128,000 max output. Efforts: none, low, medium (default), high, xhigh, max. Function calling, structured outputs, prompt caching supported. Rate limits for Build/Launch/Grow tiers. |
| C2 | Pricing (API docs) | https://developers.openai.com/api/docs/pricing | 2026-10-16 | Full Standard/Batch/Flex/Fast tables, including cache-write column, 272K short/long context split, 10% regional uplift. |
| C3 | Models overview | https://developers.openai.com/api/docs/models | 2026-10-16 | Flagships: gpt-6-astra, gpt-6.1-sol, gpt-6-luna ("Most efficient model for high-volume tasks"). |
| C4 | Prompt caching guide | https://developers.openai.com/api/docs/guides/prompt-caching | 2026-10-16 | 1,024-token minimum (GPT-5.6+). Implicit vs explicit breakpoints. `cached_tokens`, `cache_write_tokens`. Cache writes cost 1.25x input on GPT-5.6+. 30m TTL on GPT-5.6+. |
| C5 | Function calling guide | https://developers.openai.com/api/docs/guides/function-calling | 2026-10-16 | Tool shape, `function_call` / `function_call_output`, `call_id`, `parallel_tool_calls`, `tool_choice`, strict rules, reasoning items must be passed back. |
| C6 | Structured outputs guide | https://developers.openai.com/api/docs/guides/structured-outputs | 2026-10-16 | `text.format` json_schema, `client.responses.parse(text_format=...)`, `output_parsed`, supported schema subset and limits. |
| C7 | Reasoning guide | https://developers.openai.com/api/docs/guides/reasoning | 2026-10-16 | `reasoning={"effort":..., "summary":...}`, `output_tokens_details.reasoning_tokens`, stateless mode includes `encrypted_content` by default, `incomplete_details.reason`. |
| C8 | Conversation state guide | https://developers.openai.com/api/docs/guides/conversation-state | 2026-10-16 | `previous_response_id` still bills all prior input tokens. Responses stored 30 days by default. Stateless replay pattern with `store: false`. |
| C9 | Rate limits guide | https://developers.openai.com/api/docs/guides/rate-limits | 2026-10-16 | Tiers are now Free / Build / Launch / Grow. Header names. 429 retry guidance. |
| C10 | Error codes guide | https://developers.openai.com/api/docs/guides/error-codes | 2026-10-16 | 429 variants (`slow_down`, `credit_balance_exhausted`, spend limits). Python exception class names. |
| C11 | Flex processing guide | https://developers.openai.com/api/docs/guides/flex-processing | 2026-10-16 | `service_tier="flex"`, Batch-rate pricing, 429 Resource Unavailable (not charged), Responses supported. |
| C12 | Batch API guide | https://developers.openai.com/api/docs/guides/batch | 2026-10-16 | 50% discount, 24h window, `/v1/responses` supported, 50,000 requests / 200 MB per batch. |
| C13 | Responses create API reference | https://developers.openai.com/api/reference/resources/responses/methods/create | 2026-10-16 | Parameter definitions (`store` defaults to true, `include` enum, `service_tier` enum, `prompt_cache_options`, `text.format` fields) and `ResponseUsage` field names. |
| C14 | openai on PyPI | https://pypi.org/project/openai/ (and /pypi/openai/json) | 2026-10-16 | Latest 3.31.0, released 2026-10-14. Requires Python >=3.10. |
| C15 | openai-python CHANGELOG | https://raw.githubusercontent.com/openai/openai-python/main/CHANGELOG.md | 2026-10-16 | 3.0.0 (2026-08-12) breaking: HTTPX2 replaces httpx. 2.49.0 (2026-07-27) requires Python 3.10. |
| C16 | GPT-6.1 Sol model page | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 2026-10-16 | $2 / $0.10 / $2.50 write / $10. Efforts low to max (no `none`). Tool calling only via Responses. |
| C17 | GPT-6 Sol model page | https://developers.openai.com/api/docs/models/gpt-6-sol | 2026-10-16 | $2 / $0.20 / $2.50 / $10. Efforts none to max. |
| C18 | GPT-5.6 Luna model page | https://developers.openai.com/api/docs/models/gpt-5.6-luna | 2026-10-16 | $0.20 / $0.02 / $0.25 / $1.20. Efforts none to max. |
| C19 | GPT-5.4 mini model page | https://developers.openai.com/api/docs/models/gpt-5.4-mini | 2026-10-16 | $0.75 / $0.075 / $4.50, 400K ctx. Efforts none (default) to xhigh. No cache-write charge. |

Not accessible: https://openai.com/api/pricing/ returned HTTP 403 to the fetch tool. The docs pricing page (C2) was used in its place.

## Model and price table

All prices are USD per 1M tokens, Standard tier, short context (≤272K input tokens). "Cache write" is billed in place of the uncached input rate for tokens written to the cache. It is not an additional fee (C4).

| model id | input | cached input | cache write | output | context / max out | reasoning efforts | notes | source |
|---|---|---|---|---|---|---|---|---|
| `gpt-6-luna` | $0.10 | $0.01 | $0.125 | $0.50 | 1,050,000 (922K max input) / 128,000 | none, low, medium (default), high, xhigh, max | Released 2026-09-22 (per aggregators; the official page shows one snapshot `gpt-6-luna`). Knowledge cutoff 2026-05-18. On Chat Completions, function calling works only at effort `none`. On Responses, tools work at any effort. | C1, C2 |
| `gpt-6.1-sol` | $2.00 | $0.10 | $2.50 | $10.00 | 1,050,000 / 128,000 | low, medium (default), high, xhigh, max | Cache reads are 0.05x input (other GPT-5.6+ models use 0.1x). Tool calling only on Responses. | C16, C2, C4 |
| `gpt-6-sol` | $2.00 | $0.20 | $2.50 | $10.00 | 1,050,000 / 128,000 | none, low, medium (default), high, xhigh, max | Superseded by 6.1 Sol at the same input and output price but a higher cached price. | C17, C2 |
| `gpt-5.6-luna` | $0.20 | $0.02 | $0.25 | $1.20 | 1,050,000 / 128,000 | none, low, medium (default), high, xhigh, max | Previous-generation small model. Useful as a different-generation reviewer. | C18, C2 |
| `gpt-5.4-mini` | $0.75 | $0.075 | n/a (no write charge) | $4.50 | 400,000 (272K max input) / 128,000 | none (default), low, medium, high, xhigh | Uses the older caching rules (128-token rounding, `prompt_cache_retention`). | C19, C2 |
| `gpt-5-nano` | $0.05 | $0.005 | n/a | $0.40 | not fetched | not fetched | Cheapest current text model in the table. Older generation. | C2 |

Long context (>272K input) doubles the input and cache rates and multiplies output by 1.5 for the whole request on the GPT-6 / 5.6 rows (C1, C2). It does not apply at our sizes (≤ ~65K tokens per call).

## Recommendations

- **OPENAI_MODEL = `gpt-6-luna`.** It is the only current model whose estimated per-run cost (see the cost section) stays under $0.20 at medium effort, and it stays under the cap even when every prompt-cache lookup misses. It supports function calling, strict schemas and prompt caching on Responses (C1). 6.1 Sol costs about $0.44 to $1.07 per run even with caching, which is over the cap.
- **OPENAI_EVAL_MODEL, default = `gpt-6-luna` at `reasoning.effort="high"`.** An estimated ~$0.003 per review (10K input, ~3.6K output) fits easily under the $0.04 cap. Drawback: the reviewer is the same model as the agent, which raises a self-preference risk. Blinding reduces that risk but does not remove it.
  - Stronger option: `gpt-6.1-sol` at effort `low`. An estimated $0.030 to $0.038 per review, but this is within the cap only if review input is ≤ ~10K tokens and `max_output_tokens` is ≤ 1,500. The worst case is 10K × $2.50 (all cache-write) + 1,500 × $10 = $0.040. A low cap like this risks `status="incomplete"` / `incomplete_details.reason="max_output_tokens"` before the JSON is emitted (C7), so the harness must handle that case.
  - Diversity option: `gpt-5.6-luna` at effort medium. About $0.006 per review, and it is a different model generation from the agent.
- **Reasoning effort candidates for the pilot: `low` and `medium`, plus `high` as a third arm if budget allows.**
  - `none` removes reasoning and is likely weak for multi-step code edits.
  - `xhigh` / `max` put per-run output cost at risk. At 3K reasoning tokens per turn, `high` already reaches ~$0.057 with cache hits and ~$0.15 with all misses.
  - Always set `reasoning.effort` explicitly. The default differs between models, for example `none` on gpt-5.4-mini and `medium` on gpt-6-luna.

## Responses API function calling

Facts (C5, C7, C8, C13):
- **Tool definition** (Responses is flat, with no nested `"function": {...}`): `{"type": "function", "name": str, "description": str, "parameters": <JSON Schema object>, "strict": bool}`. There is also an optional `defer_loading: bool`, used with tool search.
  - If `strict` is omitted on Responses, the API tries strict validation when the schema is compatible and otherwise falls back to non-strict (C5, C13). Set `strict: true` explicitly.
  - Strict requires `additionalProperties: false` on every object, and every property listed in `required`. Optional fields use a union with `"null"`.
- **Output items:** `response.output` is a list of items. A function call item has `type="function_call"`, `id` (e.g. `fc_...`), `call_id` (e.g. `call_...`), `name`, and `arguments` (a JSON-encoded string). Reasoning models also emit items with `type="reasoning"` (with `encrypted_content` in stateless mode). The docs example does not show a `status` field on function_call items, so do not rely on one.
- **Returning results:** append `{"type": "function_call_output", "call_id": <call_id>, "output": <string>}`. `output` is normally a string and can also be an array of image or file objects.
- **`parallel_tool_calls`** (bool): set it to `false` to get at most one tool call per response. The reference gives no default, and the examples show `true`.
- **`tool_choice`:**
  - `"auto"` (the model may call zero or more tools)
  - `"required"`
  - `"none"`
  - `{"type": "function", "name": "..."}`
  - an `allowed_tools` form that restricts calls to a subset of tools while the full tool list, and therefore the cache prefix, stays unchanged
- **`max_output_tokens`:** the upper bound on generated tokens, including reasoning. On overflow the response has `status="incomplete"` and `incomplete_details.reason="max_output_tokens"`, and you pay for the reasoning even if no visible output was produced (C7).
- **`reasoning`:** `{"effort": "none"|"minimal"|"low"|"medium"|"high"|"xhigh"|"max", "summary": "auto"|"concise"|"detailed"}`. Which values are accepted depends on the model (C7, C13).
- **Reasoning items:** "any reasoning items returned in model responses with tool calls must also be passed back" (C5). The reasoning guide (C7) says to pass back all reasoning, function_call and function_call_output items since the last user message. The simplest approach is to append the whole `response.output` each turn.
- **`store`:** defaults to `true` (C13), and responses are kept 30 days (C8). In stateless mode (`store=false` or ZDR), reasoning items include `encrypted_content` by default. `include=["reasoning.encrypted_content"]` is still accepted as a legacy value but is no longer required (C7).
- **`previous_response_id` vs full input:**
  - With `previous_response_id`, "all previous input tokens for responses in the chain are billed as input tokens" (C8). It saves bandwidth, not money. Caching applies the same way.
  - It requires `store=true`. `instructions` are not carried over to the next response (C13). It cannot be combined with `conversation`.
  - For a reproducible, inspectable harness, use stateless full-input replay (`store=false`, append `response.output` + tool outputs). Then the transcript we log is exactly what the model saw, nothing is retained server-side, and the prefix stays byte-stable for caching.
- **`include` enum** (C13): `file_search_call.results`, `web_search_call.results`, `web_search_call.action.sources`, `message.input_image.image_url`, `computer_call_output.output.image_url`, `code_interpreter_call.outputs`, `reasoning.encrypted_content`, `message.output_text.logprobs`.
- **Other request fields:**
  - `truncation`: `auto` or `disabled`, default `disabled`, which returns a 400 if the input exceeds the context window.
  - `safety_identifier` (replaces `user`).
  - `service_tier`: `auto`, `default`, `flex`, `scale`, `priority`, `fast`, `ultrafast`.

Minimal example (written for this report, not copied from the docs):

```python
import json
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY

TOOLS = [{
    "type": "function",
    "name": "read_file",
    "description": "Read a UTF-8 text file from the task repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Repo-relative path"},
            "max_lines": {"type": ["integer", "null"]},
        },
        "required": ["path", "max_lines"],
        "additionalProperties": False,
    },
    "strict": True,
}]  # keep tool list order and text byte-identical across turns and runs (cache prefix)

def run_tool(name: str, args: dict) -> str:
    ...  # dispatch to list_dir/read_file/search/apply_patch/run/run_visible_tests; truncate to ~2k tokens

items = [
    {"role": "developer", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
    {"role": "user", "content": TASK_TEXT},
]
for turn in range(25):
    resp = client.responses.create(
        model="gpt-6-luna",
        input=items,
        tools=TOOLS,
        tool_choice="auto",
        parallel_tool_calls=False,
        reasoning={"effort": "low"},
        max_output_tokens=8000,
        store=False,                 # stateless; reasoning items come back with encrypted_content
        prompt_cache_key="harness-v1",
    )
    tracker.add(resp.model, resp.usage)          # CostTracker
    if resp.status == "incomplete":
        break                                     # resp.incomplete_details.reason
    items += resp.output                          # includes reasoning + function_call items
    calls = [it for it in resp.output if it.type == "function_call"]
    if not calls:
        final_text = resp.output_text
        break
    for call in calls:
        result = run_tool(call.name, json.loads(call.arguments))
        items.append({"type": "function_call_output", "call_id": call.call_id, "output": result})
```

## Structured outputs

- **Raw request shape (Responses, C6, C13):**
  ```python
  text={"format": {"type": "json_schema", "name": "review", "description": "...", "schema": {...}, "strict": True}}
  ```
  - `name`: letters, digits, `_` or `-`, up to 64 characters (required).
  - `schema` (required).
  - `strict` (bool or null).
  - `description` (optional).
  - JSON mode is `{"type": "json_object"}`. It guarantees valid JSON but not schema adherence, and the docs recommend json_schema instead.
- **SDK helper:** `client.responses.parse(model=..., input=..., text_format=PydanticModel)`, then read `response.output_parsed` (C6). `type_to_response_format_param` became a public export in openai 3.25.0 (C15).
- **Schema restrictions with strict (C6):**
  - The root must be an object and must not be `anyOf`.
  - Every property must be in `required`. For an optional field, use `"type": [..., "null"]`.
  - `additionalProperties: false` on every object.
  - Supported types: string, number, boolean, integer, object, array, enum, anyOf.
  - String keywords: `pattern`, and `format` with the values date-time, time, date, duration, email, hostname, ipv4, ipv6, uuid.
  - Number keywords: `multipleOf`, `maximum`, `exclusiveMaximum`, `minimum`, `exclusiveMinimum`.
  - Array keywords: `minItems`, `maxItems`.
  - `$defs` / `$ref` and recursion (`"$ref": "#"`) are supported.
  - Not supported: `allOf`, `not`, `dependentRequired`, `dependentSchemas`, `if` / `then` / `else`.
  - Limits: 5,000 properties in total; 10 nesting levels; 120,000 characters across property, definition, enum and const names; 1,000 enum values in total (a single string enum with more than 250 values must total ≤15,000 characters).
  - Keys are emitted in schema order. Put `findings` before `verdict` if you want the model to reason before it commits to a verdict.
- **Refusals:** a message content item with `type == "refusal"` may appear instead of schema output, so check for it before using `output_parsed`. The first request with a new schema has extra latency (C6).
- **Caching interaction:** `text.format` is part of the cached prefix (C4). Keep the reviewer schema byte-stable.

Reviewer sketch:
```python
from typing import Literal
from pydantic import BaseModel

class Finding(BaseModel):
    file: str
    line: int | None
    severity: Literal["blocker", "major", "minor"]
    comment: str

class Review(BaseModel):
    findings: list[Finding]
    score: int            # 0-10, range enforced in rubric text or via minimum/maximum
    verdict: Literal["accept", "reject"]

resp = client.responses.parse(
    model=EVAL_MODEL, input=review_items, text_format=Review,
    reasoning={"effort": "high"}, max_output_tokens=6000, store=False,
)
review = resp.output_parsed   # None if refusal/incomplete: check resp.status and content types
```

## Prompt caching and usage fields

Behaviour for GPT-5.6 and later models, which includes gpt-6-luna, gpt-6-sol, gpt-6.1-sol and gpt-5.6-luna (C4, C13):
- **On by default.** The minimum cacheable prompt is 1,024 tokens. OpenAI's hidden system content does not count toward it.
- **Prefix rule:** "Cache reuse requires the entire rendered prefix to match." Tool definitions, `text.format`, reasoning effort and verbosity all change the prefix.
  - Append new items and never rewrite earlier turns. Summarisation, compaction or truncation resets reuse.
  - Changing `reasoning.effort` between arms means the arms do not share cache entries.
- **Breakpoints:**
  - Implicit mode (default): OpenAI places a breakpoint at the end of the latest eligible message. Eligible messages are user messages, the last tool response in a consecutive group, and the last developer message in the initial group.
  - Explicit mode: `prompt_cache_options={"mode": "explicit"}` plus `"prompt_cache_breakpoint": {"mode": "explicit"}` on an `input_text` content block. With no breakpoints in explicit mode there is no caching and no cache-write charge.
  - Top-level `instructions` cannot hold a breakpoint. Put stable instructions in a developer message.
  - There are up to 4 cache-write slots per request, and the implicit breakpoint uses one of them.
  - Lookups check the first 2 and the latest 50 explicit breakpoints.
- **Retention:** `prompt_cache_options.ttl` supports only `"30m"` (the default). A prefix stays eligible for 30 minutes after its most recent write or reuse.
  - `prompt_cache_retention` (`in_memory` / `24h`) is deprecated and applies to older models: in_memory lasts ~5–10 min idle, up to 1 h; 24h lasts typically ~30 min, up to 24 h.
- **`prompt_cache_key`:** on GPT-5.6+ it is optional and used for separate cache accounting, with routing handled automatically. On older models it influences routing; the guidance there is ≤ ~15 RPM per key.
- **Price:**
  - Cache read: 0.1x the input rate on most GPT-5.6+ models ($0.01 for luna) and 0.05x on gpt-6.1-sol.
  - Cache write: 1.25x the input rate ($0.125 for luna).
  - Older models have no write charge.
  - Cached tokens still count toward TPM.
  - Caches are per organization and do not cross regional processing boundaries.
- **Reporting precision:** GPT-5.6+ reports the exact eligible boundary. Older models round down to a multiple of 128.

**Usage object (`ResponseUsage`, C13), exact names:**
- `usage.input_tokens` (total input, including cached and written)
- `usage.input_tokens_details.cached_tokens` (read from cache)
- `usage.input_tokens_details.cache_write_tokens` (written to cache)
- `usage.output_tokens` (includes reasoning)
- `usage.output_tokens_details.reasoning_tokens`
- `usage.total_tokens`

The openai 3.6.0 changelog also mentions `compute_units` added to usage (C15). It was not seen in the reference excerpt.

CostTracker formula, per OpenAI's own example in C4:

```
uncached = input_tokens - cached_tokens - cache_write_tokens
cost = (uncached*P_in + cached_tokens*P_cached + cache_write_tokens*P_write + output_tokens*P_out) / 1e6
```

The prices file therefore needs a `cache_write` column, and short/long context columns if inputs could exceed 272K. Read `cache_write_tokens` defensively (`getattr(..., 0) or 0`) in case an older SDK lacks the field.

## SDK version

- **Version:** `openai` 3.31.0, released 2026-10-14 on PyPI (C14). Requires Python >=3.10 (C14).
- **Breaking and relevant changes in the last 6 months (C15):**
  - 3.0.0 (2026-08-12) is the only release marked BREAKING: HTTPX2 is now the default HTTP client and `httpx` is no longer installed automatically. Custom `http_client` / transport code must move to HTTPX2 equivalents. A temporary legacy-httpx escape hatch exists.
  - 2.49.0 (2026-07-27) requires Python 3.10.
  - 2.34.0 (2026-05-04) fixed the `prompt_cache_retention` enum value from `in-memory` to `in_memory`.
  - 2.39.0 added `additional_tools` items in Responses.
  - 3.9.0 added prompt-cache diagnostics, and 3.15.0 added prompt-cache prewarming plus managed Responses WebSocket sessions.
  - 3.16.2 fixed a memory leak in `parse_response`.
  - Retry changes: 3.19.0 retries only replayable request content, and 3.20.0 retries unmapped TLS transport errors.
- **Pinning:** pin `openai>=3.31,<4` and keep the HTTP client at the SDK default.

## Rate limits and errors

- **Tiers (C9):** the old "Tier 1–5" naming is replaced by Free / Build / Launch / Grow, and upgrades are automatic.
  - Free: $100/month usage limit, for users in allowed geographies.
  - Build: qualifies at $5 total credit purchases; $500/month limit.
  - Launch: qualifies at $100; $5,000/month.
  - Grow: qualifies at $500; $200,000/month.
  - No waiting period is stated.
- **Scope:** limits are set at the organization and project level and vary by model. Some models share limits.
- **Per-model limits:**

| model | Build RPM / TPM | Launch RPM / TPM | Grow RPM / TPM | source |
|---|---|---|---|---|
| gpt-6-luna | 5,000 / 2,000,000 | 10,000 / 10,000,000 | 30,000 / 180,000,000 | C1 |
| gpt-6.1-sol | 5,000 / 1,000,000 | 10,000 / 4,000,000 | 15,000 / 40,000,000 | C16 |

  The gpt-6-luna page lists no Free tier row (C1).
- **How TPM is counted:** "Your rate limit is calculated as the maximum of `max_tokens` and the estimated number of tokens" (C9). The guide wording refers to `max_tokens`, which corresponds to `max_output_tokens` on Responses. Cached tokens count toward TPM (C4).
- **Implication for 2 arms + 4 workers (6 concurrent loops) at Build:**
  - Average input per call is ~35.6K tokens in the run model below, ~40K with an output allowance.
  - At ~10 calls/min per loop, that is ~60 calls/min × 40K ≈ 2.4M TPM, which is above Build's 2M TPM.
  - Either buy up to Launch ($100 total purchases → 10M TPM), throttle to ≤ ~4 concurrent loops, or keep `max_output_tokens` modest. RPM is not the binding limit.
- **Headers:**
  - `x-ratelimit-limit-requests`, `x-ratelimit-limit-tokens`
  - `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`
  - `x-ratelimit-reset-requests`, `x-ratelimit-reset-tokens`
  - project variants `x-ratelimit-*-project-tokens`
  - `Retry-After` (seconds)
- **Errors (C9, C10):**
  - **429 variants:**
    - Request or token rate limit reached.
    - `slow_down` (type `rate_limit_error`): traffic ramped too fast. Follow `Retry-After`, back off, then ramp up gradually.
    - Billing variants with `error.code` `credit_balance_exhausted`, `organization_spend_limit_exceeded`, `project_spend_limit_exceeded` or `organization_usage_limit_exceeded`. `error.type` may be `insufficient_quota`. Do not retry these.
  - **503:** `server_is_overloaded`.
  - **Python exceptions:** `RateLimitError` (429), `InternalServerError` (5xx), `APIConnectionError`, `APITimeoutError`, `AuthenticationError`, `BadRequestError`, `ConflictError`, `NotFoundError`, `PermissionDeniedError`, `UnprocessableEntityError`.
  - **Retry guidance:** use exponential backoff with jitter and cap both attempts and total time. Failed requests still count toward per-minute limits. In the harness, distinguish billing 429s by `error.code` and abort the session rather than retrying.

## Batch/flex

- **Batch (C12):**
  - Discount and window: 50% off with a 24h completion window.
  - Endpoints: `/v1/responses` and `/v1/chat/completions`.
  - Input format: JSONL lines of `{custom_id, method, url, body}`, one model per file.
  - Limits: ≤50,000 requests and ≤200 MB per batch. Batch limits are separate from the per-model limits; gpt-6-luna's Build batch queue limit is 20M tokens (C1).
  - Price for gpt-6-luna: $0.05 / $0.005 cached / $0.0625 write / $0.25 out (C2).
  - Each line is an independent request with no chaining, so a multi-turn tool-calling agent cannot run inside one batch.
  - Usable for one-shot jobs such as re-running the blinded reviewer over saved transcripts.
- **Flex (C11):**
  - Request it with `service_tier="flex"` on Responses or Chat Completions. Tokens are billed at Batch rates (the same 50%), and gpt-6-luna is listed in the Flex table (C2). Prompt caching discounts still apply.
  - Downsides: slower, and it can return `429 Resource Unavailable`, which is not charged. Timeouts are more likely; the SDK default is 10 min and the guide's examples use 15 min.
  - It is synchronous, so it can drive a multi-turn agent loop. It is suitable for pre-class experiments where latency does not matter, with the halved prices.
  - Fallback on 429: retry with backoff, or drop to `service_tier="auto"`.
  - The flex guide does not mention function calling explicitly. Function tools are a Responses feature and should work, but this is unverified.
  - Not recommended during live class: the latency is unpredictable.

## Cost sanity check

Assumptions (gpt-6-luna, Standard tier):
- 25 turns. Stable prefix P = 8,000 tokens (developer prompt + task + tool schemas).
- Each turn adds the model's 300 visible output tokens (the function call) plus one tool output of ≤2,000 tokens to the history: d = 2,300 tokens per turn.
- Reasoning tokens R per turn: 500 (low), 1,000 (medium), 3,000 (high). Reasoning items replayed as input are ignored here; see Open gaps.

Input tokens:
- Input at turn t (t = 1..25): I_t = 8,000 + (t−1) × 2,300.
- I_1 = 8,000. I_25 = 8,000 + 24 × 2,300 = 63,200.
- Σ I_t = 25 × 8,000 + 2,300 × (0+1+…+24) = 200,000 + 2,300 × 300 = 890,000 input tokens.

Output tokens: 25 × (300 + R) = 20,000 (R=500), 32,500 (R=1,000), or 82,500 (R=3,000).

Caching model (implicit, ideal hits): each turn reads the previous turn's whole input from the cache and writes the new 2,300-token tail.
- Written = I_25 = 63,200 (every token is written exactly once).
- Cached reads = 890,000 − 63,200 = 826,800.

Costs at medium (R = 1,000), from $0.10 / $0.01 / $0.125 / $0.50:
- **No caching:** input 890,000 × 0.10/1e6 = $0.0890; output 32,500 × 0.50/1e6 = $0.0163; **total $0.105.**
- **Caching, ideal hits:** cached 826,800 × 0.01/1e6 = $0.0083; writes 63,200 × 0.125/1e6 = $0.0079; output $0.0163; **total $0.032.**
- **Caching on, every lookup misses** (all input billed as writes): 890,000 × 0.125/1e6 = $0.111, plus $0.016 output = **$0.128.** This is the worst case and is still under $0.20.

| effort (R/turn) | no caching | caching, ideal hits | caching, all misses |
|---|---|---|---|
| low (500) | $0.099 | $0.026 | $0.121 |
| medium (1,000) | $0.105 | $0.032 | $0.128 |
| high (3,000) | $0.130 | $0.057 | $0.153 |

Same workload on the other models (medium, ideal caching / no caching):

| model | ideal caching | no caching | within $0.20 cap |
|---|---|---|---|
| gpt-5.6-luna | $0.071 | $0.217 | only with caching |
| gpt-5.4-mini | $0.256 | $0.814 | no |
| gpt-6.1-sol | $0.566 | $2.105 | no |

Review cost (10K input, of which 3K is a stable rubric and schema; 600 visible output tokens):
- gpt-6-luna, high (~3K reasoning): ≈ $0.001 + 3,600 × 0.5/1e6 = **~$0.003.**
- gpt-6.1-sol, low (~1K reasoning): 7K × $2 = $0.014, plus 3K at $0.10 (hit, $0.0003) or $2.50 (write, $0.0075), plus 1,600 × $10 = $0.016. **Total ≈ $0.030 to $0.038.**
- gpt-5.6-luna, medium (~2K reasoning): **~$0.006.**

Session check: 2 arms × 8 tasks = 16 runs × $0.06 (luna, mixed hits) + 16 reviews × $0.04 (worst-case Sol reviewer) ≈ $0.96 + $0.64 = $1.60. That is ≤ $2.50, which leaves room for retries.

## Open gaps

1. Whether replayed reasoning items (encrypted_content) from earlier turns are billed as input tokens on later turns, and how many of them the model keeps. This is not quantified in the docs read. Upper bound: R × 300 = 300K extra tokens per run at medium. If mostly cache-read at $0.01, that adds ~$0.003, and the cache writes for them add up to ~$0.003 to $0.04 more. Measure in the pilot from `usage.input_tokens`.
2. Real cache hit rates for implicit mode under 6 concurrent loops are untested. Cost ranges from $0.032 (all hits) to $0.128 (all misses) at medium. Log `cached_tokens` / `cache_write_tokens` per turn.
3. Which `openai` SDK version first exposed `input_tokens_details.cache_write_tokens` as a typed field was not found in the changelog excerpt. Read it defensively.
4. Whether a Free-tier org can call gpt-6-luna: the model page lists only Build, Launch and Grow (C1).
5. The flex guide does not explicitly confirm function calling support.
6. The gpt-6-luna release date (2026-09-22) and the "fast/cost-efficient" positioning come from aggregator pages. The official page shows no dated snapshot. The SDK 3.17.0–3.19.0 releases on 2026-09-22 are consistent with that date.
7. openai.com/api/pricing could not be fetched (403). All prices come from developers.openai.com/api/docs/pricing and the model pages, which agree with each other.
8. Typical reasoning-token counts per turn for gpt-6-luna at each effort are not published. The R values above are assumptions.

## Corrections to the brief

- **Model and price:** `gpt-6-luna` exists, and the reported price $0.10 / $0.01 / $0.50 is correct. The brief omits the **cache-write price of $0.125/1M (1.25x input)**, which applies to GPT-5.6+ models. CostTracker must price `cache_write_tokens` separately, or it will under-count.
- **Tier naming:** "Tier 1" no longer exists. The new paid entry tier is **Build** ($5 purchases): 5,000 RPM / 2,000,000 TPM for gpt-6-luna.
- **Caching parameters:** for GPT-5.6+ models, `prompt_cache_retention` (in_memory/24h) is deprecated. Use `prompt_cache_options` (`mode`: implicit/explicit, `ttl`: `"30m"` only). The 128-token increment rule applies only to older models, and the minimum is 1,024 tokens.
- **Encrypted reasoning:** with `store=false`, `include=["reasoning.encrypted_content"]` is no longer required. Encrypted reasoning is returned by default in stateless mode.
- **`previous_response_id` cost:** it does not reduce billed input tokens (C8). It needs `store=true` and does not carry `instructions` forward.
- **Default flagship:** the docs' default is `gpt-6-astra` ($10/$50), which is unsuitable under these caps. Do not copy model ids from doc examples (C6 uses `gpt-6-astra`).
- **SDK major version:** the SDK is at major version 3 (3.31.0). Code written against 1.x/2.x HTTPX customisation needs migration to HTTPX2.
