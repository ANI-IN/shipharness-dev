"""Hidden tests for R8: seeded violations the visible tests miss, false positives, baselines."""

from __future__ import annotations

from pathlib import Path

import pytest
from a4_support import (
    CHECK_NAME,
    LEGACY,
    V_GET,
    V_GET_ENDPOINTS,
    counted_keys,
    load_impl,
    make_build,
    new_keys,
    run_r8,
)
from hidden_seeds import (
    H_BODY,
    H_BODY_OK,
    H_DECOY,
    H_ID_PARAM,
    H_NESTED_LIST,
    H_NESTED_PATH,
    H_RECENT,
    H_RECENT_OK,
    H_TRANSITION,
)

RECENT = ("GET /projects/{project_id}/recent-issues", "deleted_list")


@pytest.mark.criterion("R8-hidden")
def test_new_list_endpoint_is_discovered_from_the_schema(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_RECENT))
    assert RECENT in counted_keys(result)


@pytest.mark.criterion("R8-hidden")
def test_deleted_issue_nested_inside_a_list_response(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_NESTED_LIST))
    assert ("GET /projects/{project_id}/columns", "deleted_list") in counted_keys(result)


@pytest.mark.criterion("R8-hidden")
def test_write_endpoint_that_resolves_a_deleted_issue(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_TRANSITION))
    assert counted_keys(result) == {("POST /issues/{issue_id}/transition", "deleted_path"), LEGACY}


@pytest.mark.criterion("R8-hidden")
def test_id_parameter_after_an_issues_segment(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_ID_PARAM))
    assert ("GET /issues/{id}/history", "deleted_path") in counted_keys(result)


@pytest.mark.criterion("R8-hidden")
def test_issue_parameter_after_another_resource_parameter(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_NESTED_PATH))
    endpoint = "GET /projects/{project_id}/issues/{issue_id}/peek"
    assert (endpoint, "deleted_path") in counted_keys(result)


@pytest.mark.criterion("R8-hidden")
def test_deleted_issue_named_in_a_request_body(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_BODY))
    assert ("POST /projects/{project_id}/watches", "deleted_body") in counted_keys(result)


@pytest.mark.criterion("R8-no-false-positives")
def test_correct_new_endpoints_are_not_reported(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, [*H_RECENT_OK, *H_BODY_OK]))
    assert counted_keys(result) == {LEGACY}


@pytest.mark.criterion("R8-no-false-positives")
def test_shared_numeric_ids_are_not_evidence(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path, H_DECOY))
    assert counted_keys(result) == {LEGACY}


@pytest.mark.criterion("R8-baseline")
def test_findings_are_stable_across_runs(tmp_path: Path) -> None:
    def keys(result: object) -> set[tuple[str, str | None, str, str]]:
        return {(f.rule, f.endpoint, f.severity, f.detail_key) for f in result.findings}  # type: ignore[attr-defined]

    first = run_r8(make_build(tmp_path / "one", H_TRANSITION))
    second = run_r8(make_build(tmp_path / "two", H_TRANSITION))
    assert keys(first) == keys(second)


@pytest.mark.criterion("R8-baseline")
def test_baseline_with_several_new_findings(tmp_path: Path) -> None:
    from shipharness.checks import mark_baseline

    baseline = run_r8(make_build(tmp_path / "checkpoint"))
    current = run_r8(make_build(tmp_path / "arm", [V_GET, *H_RECENT]))
    marked = mark_baseline(current, baseline)
    expected = {(e, "deleted_path") for e in V_GET_ENDPOINTS} | {RECENT}
    assert new_keys(marked) == expected
    assert marked.new_violations == len(expected)
    assert marked.baseline_violations == 1
    legacy = [f for f in marked.findings if (f.endpoint, f.detail_key) == LEGACY]
    assert legacy and all(f.baseline for f in legacy)


@pytest.mark.criterion("R8-baseline")
def test_exempt_endpoint_is_reported_as_info(tmp_path: Path) -> None:
    result = run_r8(make_build(tmp_path), exemptions={"R8": [LEGACY[0]]})
    assert result.passed
    assert result.new_violations == 0
    legacy = [f for f in result.findings if f.endpoint == LEGACY[0]]
    assert legacy and all(f.severity == "info" for f in legacy)


@pytest.mark.criterion("R8-interface")
def test_shipharness_runner_runs_the_check_with_a_baseline(tmp_path: Path) -> None:
    load_impl()
    from shipharness.checks.runner import run_checks

    build = make_build(tmp_path)
    common = {"checkpoint": "m1-base", "feature_id": "A4", "seed": 0, "params": {}}
    first, crashed = run_checks(build, [CHECK_NAME], **common)  # type: ignore[arg-type]
    assert not crashed and not first[0].passed
    second, crashed = run_checks(
        build,
        [CHECK_NAME],
        baseline={CHECK_NAME: first[0]},
        **common,  # type: ignore[arg-type]
    )
    assert not crashed and second[0].passed and second[0].baseline_violations == 1


@pytest.mark.criterion("R8-interface")
def test_progress_is_reported(tmp_path: Path) -> None:
    load_impl()
    from shipharness.checks import CheckContext, get_check

    seen: list[tuple[int, int]] = []
    ctx = CheckContext(checkpoint="m1-base", feature_id="A4")
    ctx.progress = lambda done, total, _label: seen.append((done, total))
    result = get_check(CHECK_NAME).run(make_build(tmp_path), ctx)
    assert seen and seen[-1][0] == seen[-1][1] == result.total_probes
