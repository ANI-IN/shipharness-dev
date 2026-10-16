"""Marks long validations as `slow`, so the default run (`uv run pytest`, `make test`) stays fast.

pyproject addopts deselects `slow`; `make test-all` (`-m "not live and not docker"`) runs them.
Each entry is a node id or node id prefix relative to the repository root. Keep the list explicit:
add a test here only when it is a long validation (roughly > 10 s on its own), and say why.

Already marked `slow` in their own files (not repeated here):
- tests/unit/datasets/test_features_controls.py: the referee on each control's reference, hidden
  tests on the start checkpoint, and referee mutants killed by the reference tests (C1-C8).
- tests/unit/datasets/test_testgen_libs.py: every mutant against the pinned boltons and WTForms
  suites (skipped when .shipharness/libs is absent).
"""

from __future__ import annotations

import pytest

SLOW_TESTS: tuple[str, ...] = (
    # Mutant kill check: the TeamTrack visible suite against every filter and referee mutant.
    "tests/unit/filters/test_teamtrack_mutants.py::test_visible_suite_kills_every_mutant",
    # Full TeamTrack check run: the regression check runs the whole visible suite on the base.
    "tests/unit/checks/test_pytest_checks.py::test_regression_base_keeps_every_visible_test_passing",
    # Full TeamTrack check run: these three share a module fixture that runs the checks runner
    # with R1-R7 and the board on the TeamTrack base.
    "tests/unit/checks/test_runner.py::test_teamtrack_base_has_no_new_violations_except_the_legacy_r1_leak",
    "tests/unit/checks/test_runner.py::test_progress_lines_on_stderr_are_json",
    "tests/unit/checks/test_runner.py::test_baseline_marks_the_legacy_leak_and_exits_zero",
)


def _is_slow(nodeid: str) -> bool:
    return any(nodeid == p or nodeid.startswith((f"{p}[", f"{p}::")) for p in SLOW_TESTS)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Add the `slow` marker before pytest's own -m deselection sees the items."""
    for item in items:
        if _is_slow(item.nodeid):
            item.add_marker(pytest.mark.slow)
