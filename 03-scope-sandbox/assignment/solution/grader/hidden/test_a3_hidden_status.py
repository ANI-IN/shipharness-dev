"""Hidden tests: evidence-gated status updates.

test_status_sets_*: passes becomes true. test_status_keeps_*: the document is unchanged.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

import pytest

from shipharness.sandbox import ExecResult, FakeSandbox, SandboxDenial

NOW = datetime(2026, 10, 16, 12, 0, tzinfo=UTC)
HEAD = "5eed" + "1" * 36
DOC: dict[str, Any] = {
    "$schema": "./feature_list.schema.json",
    "features": [
        {
            "id": "F2",
            "category": "api",
            "description": "Done earlier",
            "steps": [],
            "passes": True,
            "evidence": {"gate_id": "gate-1", "commit": "a" * 40, "visible": "3/3"},
            "testedAt": "2026-10-15T09:00:00Z",
        },
        {
            "id": "F3",
            "category": "api",
            "description": "Idempotency keys on create-issue",
            "steps": ["POST twice with one key returns the same issue"],
            "passes": False,
            "evidence": None,
            "testedAt": None,
        },
    ],
}
ITEMS = [
    {"name": "visible tests", "status": "pass", "detail": "passed 12/12"},
    {"name": "existing tests", "status": "pass", "detail": "40/40 keep passing"},
    {"name": "R1", "status": "pass", "detail": ""},
    {"name": "R2", "status": "skipped", "detail": "not applicable"},
    {"name": "R4", "status": "pass", "detail": ""},
    {"name": "board", "status": "pass", "detail": ""},
]
GATE = {"gate_id": "gate-9", "passed": True, "feedback": "", "items": ITEMS}
DONE = {"phase": "build", "claim": "done", "summary": "F3 done"}


def end(**overrides: Any):  # type: ignore[no-untyped-def]
    from a3scope.status import SessionEnd

    values: dict[str, Any] = {
        "phase": "build",
        "last_claim": DONE,
        "verify_layer": True,
        "gate": GATE,
        "head_commit": HEAD,
    }
    values.update(overrides)
    return SessionEnd(**values)


def run(session_end, sandbox=None, now=lambda: NOW):  # type: ignore[no-untyped-def]
    from a3scope.status import update_status

    box = sandbox or FakeSandbox()
    doc = copy.deepcopy(DOC)
    decision = update_status(doc, "F3", session_end, box, now)
    assert doc == DOC, "the input document was changed"
    return decision, box


def scripted_box(output: str, exit_code: int = 0, **extra: Any) -> FakeSandbox:
    return FakeSandbox(
        default=ExecResult(exit_code=exit_code, output=output, duration_ms=3, **extra)
    )


def assert_unchanged(decision, box=None, ran: bool | None = None) -> None:  # type: ignore[no-untyped-def]
    assert decision.kind in ("note", "none")
    assert decision.document == DOC
    assert decision.evidence is None
    if ran is False:
        assert box.commands == []


# -- sets ------------------------------------------------------------------------------------------


def test_status_sets_with_skipped_items_and_only_passing_rule_checks() -> None:
    decision, box = run(end())
    assert decision.kind == "status_set"
    assert decision.evidence == {
        "gate_id": "gate-9",
        "commit": HEAD,
        "visible": "12/12",
        "existing": "40/40",
        "checks": ["R1", "R4"],
    }
    assert box.commands == []


def test_status_sets_only_the_named_feature() -> None:
    decision, _ = run(end())
    f2, f3 = decision.document["features"]
    assert f2 == DOC["features"][0]
    assert f3["passes"] is True and f3["testedAt"] == "2026-10-16T12:00:00Z"
    assert {k: v for k, v in f3.items() if k not in ("passes", "evidence", "testedAt")} == {
        k: v for k, v in DOC["features"][1].items() if k not in ("passes", "evidence", "testedAt")
    }
    assert decision.document["$schema"] == DOC["$schema"]


def test_status_sets_testedat_in_utc_from_another_timezone() -> None:
    ist = timezone(timedelta(hours=5, minutes=30))
    decision, _ = run(end(), now=lambda: datetime(2026, 10, 16, 17, 30, 15, tzinfo=ist))
    assert decision.document["features"][1]["testedAt"] == "2026-10-16T12:00:15Z"


def test_status_sets_without_an_existing_tests_item() -> None:
    gate = {**GATE, "items": [ITEMS[0], ITEMS[2]]}
    decision, _ = run(end(gate=gate))
    assert decision.kind == "status_set"
    assert decision.evidence["existing"] == "not run"


def test_status_sets_from_visible_tests_with_skips_and_warnings() -> None:
    from a3scope.status import VISIBLE_TESTS_COMMAND

    box = scripted_box("....s.x\n12 passed, 1 skipped, 1 xfailed, 2 warnings in 1.10s\n")
    decision, box = run(end(verify_layer=False, gate=None), box)
    assert decision.kind == "status_set"
    assert decision.evidence["visible"] == "12/12"
    assert box.commands == [VISIBLE_TESTS_COMMAND]


def test_status_sets_from_a_decorated_summary_line() -> None:
    box = scripted_box("============ 7 passed in 0.52s ============\n")
    decision, _ = run(end(verify_layer=False, gate=GATE | {"passed": False}), box)
    assert decision.kind == "status_set"  # verify layer off: the gate is not the evidence
    assert decision.evidence["gate_id"] == "visible-tests"


def test_status_sets_passes_the_timeout_to_the_sandbox() -> None:
    from a3scope.status import update_status

    seen: list[int] = []

    class Box(FakeSandbox):
        def exec(self, command: str, timeout_s: int) -> ExecResult:
            seen.append(timeout_s)
            return ExecResult(exit_code=0, output="3 passed in 0.1s\n", duration_ms=1)

    decision = update_status(
        copy.deepcopy(DOC), "F3", end(verify_layer=False, gate=None), Box(), lambda: NOW, 77
    )
    assert decision.kind == "status_set" and seen == [77]


# -- keeps -----------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "claim",
    [
        None,
        {"phase": "build", "claim": "not_done", "summary": ""},
        {"phase": "test", "claim": "done", "summary": ""},
        {"phase": "build", "claim": "none", "summary": ""},
        "done",
    ],
    ids=["no-claim", "not-done", "claim-from-test-phase", "claim-none", "claim-not-a-dict"],
)
def test_status_keeps_without_a_done_claim_for_build(claim: Any) -> None:
    decision, box = run(end(last_claim=claim, verify_layer=False, gate=None))
    assert decision.kind == "none"
    assert_unchanged(decision, box, ran=False)


def test_status_keeps_in_the_test_phase_even_with_a_test_done_claim() -> None:
    decision, box = run(end(phase="test", last_claim={**DONE, "phase": "test"}, verify_layer=False))
    assert decision.kind == "none"
    assert_unchanged(decision, box, ran=False)


def test_status_keeps_once_already_set() -> None:
    decision, box = run(end(passes_already_set=True, verify_layer=False))
    assert_unchanged(decision, box, ran=False)


@pytest.mark.parametrize(
    "gate",
    [
        None,
        {**GATE, "passed": "true"},
        {**GATE, "passed": 1},
        {k: v for k, v in GATE.items() if k != "passed"},
        {**GATE, "items": [i for i in ITEMS if i["name"] != "visible tests"]},
        {**GATE, "items": [{**ITEMS[0], "status": "fail"}, *ITEMS[1:]]},
        {**GATE, "items": [{**ITEMS[0], "detail": "passed 11/12"}, *ITEMS[1:]]},
        {**GATE, "items": [{**ITEMS[0], "detail": "passed 0/0"}, *ITEMS[1:]]},
        {**GATE, "items": [{**ITEMS[0], "detail": "all good"}, *ITEMS[1:]]},
        {**GATE, "items": [*ITEMS, {"name": "R6", "status": "fail", "detail": "layering"}]},
        {**GATE, "items": [*ITEMS, {"name": "clean state", "status": "pending", "detail": ""}]},
        {**GATE, "items": [ITEMS[0], {**ITEMS[1], "status": "fail"}]},
        "passed",
    ],
    ids=[
        "no-gate",
        "passed-is-a-string",
        "passed-is-1",
        "passed-missing",
        "no-visible-item",
        "visible-item-failed",
        "visible-11-of-12",
        "visible-0-of-0",
        "visible-no-ratio",
        "rule-check-failed",
        "item-pending",
        "existing-tests-failed",
        "gate-not-a-dict",
    ],
)
def test_status_keeps_when_gate_evidence_is_missing_or_inconsistent(gate: Any) -> None:
    decision, box = run(end(gate=gate))
    assert decision.kind == "note"
    assert "F3" in decision.message
    assert_unchanged(decision, box, ran=False)  # verify on: nothing is re-run


@pytest.mark.parametrize(
    ("output", "exit_code", "extra"),
    [
        ("1 failed, 3 passed in 0.40s\n", 1, {}),
        ("4 passed, 1 error in 0.50s\n", 1, {}),
        ("no tests ran in 0.01s\n", 5, {}),
        ("collected 0 items\n\nno tests ran in 0.01s\n", 0, {}),
        ("2 failed, 3 passed in 0.40s\n", 0, {}),
        ("OK\n", 0, {}),
        ("", 0, {}),
        ("test output: 5 passed in 0.1s\n...F\n1 failed, 4 passed in 1.00s\n", 0, {}),
        ("3 passed in 0.10s\n", 0, {"timed_out": True}),
        ("3 passed in 0.10s\n", 124, {}),
        (
            "DENIED by sandbox: no network\n",
            126,
            {"denied": SandboxDenial(reason_code="network", detail="no network")},
        ),
        ("FAILED tests/visible/test_x.py::test_3_passed - assert 0\n1 failed in 0.2s\n", 1, {}),
    ],
    ids=[
        "one-failed",
        "one-error",
        "no-tests-exit-5",
        "no-tests-exit-0",
        "failures-but-exit-0",
        "no-summary",
        "empty-output",
        "last-summary-wins",
        "timed-out",
        "timeout-exit-code",
        "denied",
        "passed-in-a-test-name",
    ],
)
def test_status_keeps_when_visible_tests_do_not_prove_it(
    output: str, exit_code: int, extra: dict[str, Any]
) -> None:
    decision, box = run(
        end(verify_layer=False, gate=GATE), scripted_box(output, exit_code, **extra)
    )
    assert decision.kind == "note"
    assert len(box.commands) == 1
    assert_unchanged(decision)


def test_status_keeps_for_an_unknown_feature() -> None:
    from a3scope.status import update_status

    doc = copy.deepcopy(DOC)
    decision = update_status(doc, "F9", end(), FakeSandbox(), lambda: NOW)
    assert decision.kind == "note" and decision.document == DOC and decision.evidence is None
