"""Live probe of LangSmith behaviour on the configured account (RESEARCH G-13). Uses ~6 traces,
no OpenAI calls. Prints a JSON summary; never prints a key.

Usage: uv run python scripts/probe_langsmith.py
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

import httpx
from langsmith import Client, evaluate, traceable, tracing_context

from shipharness.config import Settings


def tier_fields(data: Any) -> dict[str, Any]:
    """Fields whose name mentions tier, retention, ttl, plan, or payment (values only for those)."""
    if not isinstance(data, dict):
        return {}
    words = ("tier", "retention", "ttl", "plan", "payment", "personal", "billing")
    return {k: v for k, v in data.items() if any(w in k.lower() for w in words)}


def main() -> None:
    settings = Settings()
    assert settings.langsmith_api_key is not None, "LANGSMITH_API_KEY is missing"
    key = settings.langsmith_api_key.get_secret_value()
    base = settings.langsmith_endpoint.rstrip("/")
    http = httpx.Client(base_url=base, headers={"x-api-key": key}, timeout=30)
    client = Client(api_key=key, api_url=base)
    summary: dict[str, Any] = {"endpoint": base, "sdk": __import__("langsmith").__version__}

    # 1. Organization / plan information.
    org = http.get("/api/v1/orgs/current")
    summary["org_status"] = org.status_code
    summary["org_tier_fields"] = tier_fields(org.json()) if org.status_code == 200 else None
    info = http.get("/api/v1/orgs/current/info")
    summary["org_info_status"] = info.status_code
    summary["org_info_tier_fields"] = tier_fields(info.json()) if info.status_code == 200 else None

    # 2. Invalid key: status code and SDK exception class.
    bad = httpx.get(
        f"{base}/api/v1/sessions",
        params={"limit": 1},
        headers={"x-api-key": "lsv2_pt_" + "0" * 32 + "_" + "0" * 10},
        timeout=30,
    )
    summary["invalid_key_http_status"] = bad.status_code
    try:
        next(iter(Client(api_key="lsv2_pt_" + "0" * 43, api_url=base).list_projects(limit=1)))
        summary["invalid_key_sdk"] = "no error"
    except Exception as exc:  # noqa: BLE001
        summary["invalid_key_sdk"] = type(exc).__name__

    # 3. One traced root run with one child = how many root runs (traces)?
    project = f"shipharness-probe-{uuid.uuid4().hex[:6]}"

    @traceable(name="probe_child", run_type="tool")
    def child(x: int) -> int:
        return x + 1

    @traceable(name="probe_root", run_type="chain", project_name=project, client=client)
    def root(x: int) -> int:
        return child(x) * 2

    with tracing_context(enabled=True, project_name=project, client=client):
        root(1)
    client.flush()
    time.sleep(8)
    roots = list(client.list_runs(project_name=project, is_root=True))
    all_runs = list(client.list_runs(project_name=project))
    summary["traceable_root_runs"] = len(roots)
    summary["traceable_total_runs"] = len(all_runs)
    if roots:
        raw = http.get(f"/api/v1/runs/{roots[0].id}")
        summary["plain_trace_tier_fields"] = (
            tier_fields(raw.json()) if raw.status_code == 200 else raw.status_code
        )

    # 4. Tiny experiment: 2 examples, k=1, one evaluator returning two scores.
    dataset_name = f"shipharness-probe-{uuid.uuid4().hex[:6]}"
    dataset = client.create_dataset(dataset_name, description="temporary probe; safe to delete")
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {"inputs": {"x": 1}, "outputs": {"y": 4}, "split": ["smoke"]},
            {"inputs": {"x": 2}, "outputs": {"y": 6}, "split": ["smoke", "section-1"]},
        ],
    )

    def target(inputs: dict[str, Any]) -> dict[str, Any]:
        return {"y": (inputs["x"] + 1) * 2}

    def referee(outputs: dict[str, Any], reference_outputs: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"key": "exact", "score": int(outputs["y"] == reference_outputs["y"])},
            {"key": "diff", "score": abs(outputs["y"] - reference_outputs["y"])},
        ]

    smoke = list(client.list_examples(dataset_name=dataset_name, splits=["smoke"]))
    section = list(client.list_examples(dataset_name=dataset_name, splits=["section-1"]))
    summary["split_filter_counts"] = {"smoke": len(smoke), "section-1": len(section)}
    results = evaluate(
        target,
        data=dataset_name,
        evaluators=[referee],
        experiment_prefix="shipharness-probe",
        num_repetitions=1,
        client=client,
        max_concurrency=0,
    )
    rows = list(results)
    summary["experiment_rows"] = len(rows)
    summary["experiment_scores"] = sorted(
        {r.key for row in rows for r in row["evaluation_results"]["results"]}
    )
    summary["comparison_url_present"] = bool(getattr(results, "comparison_url", None))
    client.flush()
    time.sleep(8)
    exp_roots = list(client.list_runs(project_name=results.experiment_name, is_root=True))
    summary["experiment_root_runs"] = len(exp_roots)
    if exp_roots:
        raw = http.get(f"/api/v1/runs/{exp_roots[0].id}")
        summary["experiment_trace_tier_fields"] = (
            tier_fields(raw.json()) if raw.status_code == 200 else raw.status_code
        )
    evaluator_runs = [
        r
        for r in client.list_runs(project_name="evaluators", is_root=True, limit=50)
        if r.start_time and (time.time() - r.start_time.timestamp()) < 600
    ]
    summary["evaluator_root_runs_last_10_min"] = len(evaluator_runs)
    if evaluator_runs:
        raw = http.get(f"/api/v1/runs/{evaluator_runs[0].id}")
        summary["evaluator_trace_tier_fields"] = (
            tier_fields(raw.json()) if raw.status_code == 200 else raw.status_code
        )

    # 5. Clean up the probe dataset, the traced project, and the experiment's project.
    errors = cleanup(client, dataset.id, [project, results.experiment_name])
    if errors:
        summary["cleanup_errors"] = errors
    print(json.dumps(summary, indent=2, default=str))


def cleanup(client: Any, dataset_id: Any, projects: list[str]) -> list[str]:
    """Delete the probe dataset and every project the probe created (including the experiment
    project that evaluate() makes). Returns the names of errors, never raises."""
    errors: list[str] = []
    try:
        client.delete_dataset(dataset_id=dataset_id)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"dataset: {type(exc).__name__}")
    for name in projects:
        try:
            client.delete_project(project_name=name)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {type(exc).__name__}")
    return errors


if __name__ == "__main__":
    main()
