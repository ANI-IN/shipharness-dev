"""Tests for the portfolio checks (`doc_problems` in `assignment/visible_tests/a4_support.py`).

A `[[PENDING]]` marker fails the portfolio criteria for every folder, the reference solution
included, and the reference solution passes them on the files of its captured live run.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SOLUTION = TESTS.parents[1]
VISIBLE = SOLUTION.parent / "assignment" / "visible_tests"
sys.path[:0] = [str(VISIBLE)]

from a4_live import trace_link_problems  # noqa: E402
from a4_runner import run_tests  # noqa: E402
from a4_support import CASE_STUDY, EVIDENCE, LANGSMITH, PENDING, DocSpec, doc_problems  # noqa: E402

SPECS = (EVIDENCE, LANGSMITH, CASE_STUDY)
MARKER = "[[PENDING: output of the live run | source: M6 pilot | how: x]]"
# The sections whose content comes from the live run, per page.
RUN_SECTIONS = {
    EVIDENCE.file: ("Results", "Filter 6 on the kept tests"),
    LANGSMITH.file: ("Trace links", "What the comparison shows"),
    CASE_STUDY.file: (),
}
PORTFOLIO_CRITERIA = ("portfolio-evidence", "portfolio-langsmith", "portfolio-case-study")


def _copy_portfolio(root: Path) -> Path:
    shutil.copytree(SOLUTION / "portfolio", root / "portfolio")
    return root


def _markers_for_run_output(page: Path, names: tuple[str, ...]) -> None:
    """Replace the content of the sections `names` with one marker each; append one marker when
    `names` is empty. This is how the reference pages looked before the live run was captured."""
    lines = page.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    skipping = False
    for line in lines:
        if line.startswith("## "):
            skipping = line[3:].strip() in names
            out.append(line)
            if skipping:
                out += ["", MARKER, ""]
            continue
        if not skipping:
            out.append(line)
    if not names:
        out += ["", MARKER]
    page.write_text("\n".join(out) + "\n", encoding="utf-8")


@pytest.mark.parametrize("spec", SPECS, ids=lambda s: Path(s.file).stem)
def test_reference_page_passes_on_its_captured_run(spec: DocSpec) -> None:
    text = (SOLUTION / spec.file).read_text(encoding="utf-8")
    assert PENDING not in text
    assert doc_problems(SOLUTION, spec) == []


def test_reference_langsmith_page_links_a_trace_url_of_its_records() -> None:
    page = (SOLUTION / LANGSMITH.file).read_text(encoding="utf-8")
    assert trace_link_problems(SOLUTION, page) == []


@pytest.mark.parametrize("spec", SPECS, ids=lambda s: Path(s.file).stem)
def test_a_pending_marker_fails_the_page(tmp_path: Path, spec: DocSpec) -> None:
    root = _copy_portfolio(tmp_path)
    _markers_for_run_output(root / spec.file, RUN_SECTIONS[spec.file])
    problems = doc_problems(root, spec)
    assert any("[[PENDING" in p for p in problems), problems


def test_a_marker_does_not_stand_in_for_the_table_or_the_trace_link(tmp_path: Path) -> None:
    root = _copy_portfolio(tmp_path)
    for spec in (EVIDENCE, LANGSMITH):
        _markers_for_run_output(root / spec.file, RUN_SECTIONS[spec.file])
    assert any("has no Markdown table" in p for p in doc_problems(root, EVIDENCE))
    assert any("has no smith.langchain.com link" in p for p in doc_problems(root, LANGSMITH))


def test_marker_only_submission_fails_every_portfolio_and_live_criterion(tmp_path: Path) -> None:
    # The reference portfolio and live/ as they were before the live run: markers, no evidence.
    impl = _copy_portfolio(tmp_path / "impl")
    for spec in SPECS:
        _markers_for_run_output(impl / spec.file, RUN_SECTIONS[spec.file])
    (impl / "live").mkdir()
    (impl / "live" / "README.md").write_text(MARKER + "\n", encoding="utf-8")
    paths = [VISIBLE / "test_portfolio_visible.py", VISIBLE / "test_live_visible.py"]
    outcomes, output = run_tests(impl, paths, timeout_s=600)
    graded = [o for o in outcomes if o.criterion in (*PORTFOLIO_CRITERIA, "live-evidence")]
    assert len(graded) == 7, output[-2000:]
    assert not any(o.passed for o in graded), [(o.name, o.message) for o in graded if o.passed]
