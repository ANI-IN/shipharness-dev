"""platform/scripts/fix_evidence_links.py: each evidence link names the file with its anchor."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
_spec = importlib.util.spec_from_file_location(
    "fix_evidence_links", REPO / "platform" / "scripts" / "fix_evidence_links.py"
)
assert _spec and _spec.loader
fel = importlib.util.module_from_spec(_spec)
sys.modules["fix_evidence_links"] = fel
_spec.loader.exec_module(fel)


def _put(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _tree(root: Path) -> None:
    _put(root, "docs/evidence.md", "# Evidence\n\n## How to use this page\n")
    _put(root, "docs/evidence/s1.md", '# S1\n\n<a id="src-openai"></a>\n\n## Run `ab-1` (F1)\n')
    _put(root, "docs/evidence/general.md", "# General\n\n## Gate\n\n## Gate\n")
    _put(root, "docs/evidence/s4.md", '<a id="dup"></a>\n')
    _put(root, "docs/evidence/final.md", '<a id="dup"></a>\n')


def test_github_heading_slugs() -> None:
    assert fel.slug("Run `ab-1` (F1)") == "run-ab-1-f1"
    assert fel.slug("S3 confirmation: result") == "s3-confirmation-result"
    assert fel.slug("[Link](x.md) and *more*") == "link-and-more"
    text = "# A\n\n```\n# not a heading\n```\n\n## Gate\n\n## Gate\n"
    assert fel.anchors_in(text) == {"a", "gate", "gate-1"}


def test_links_are_rewritten_to_the_file_that_holds_the_anchor(tmp_path: Path) -> None:
    _tree(tmp_path)
    page = _put(
        tmp_path,
        "01-x/README.md",
        "[a](../docs/evidence.md#src-openai) [b](../docs/evidence/general.md#run-ab-1-f1)\n"
        "[c](../docs/evidence.md#how-to-use-this-page) [d](../docs/evidence/general.md#gate-1)\n",
    )
    s3 = _put(tmp_path, "docs/evidence/s3.md", "[e](#src-openai) [f](s1.md#src-openai)\n")
    report = fel.fix(tmp_path)
    assert page.read_text(encoding="utf-8") == (
        "[a](../docs/evidence/s1.md#src-openai) [b](../docs/evidence/s1.md#run-ab-1-f1)\n"
        "[c](../docs/evidence.md#how-to-use-this-page) [d](../docs/evidence/general.md#gate-1)\n"
    )
    assert s3.read_text(encoding="utf-8") == "[e](s1.md#src-openai) [f](s1.md#src-openai)\n"
    assert sorted(report.changed) == ["01-x/README.md", "docs/evidence/s3.md"]
    assert report.missing == [] and report.ambiguous == []
    assert fel.fix(tmp_path).changed == []  # re-runnable: nothing left to do


def test_missing_and_duplicate_anchors_are_reported_and_left(tmp_path: Path) -> None:
    _tree(tmp_path)
    text = "[a](docs/evidence.md#nowhere) [b](docs/evidence.md#dup) [c](docs/evidence/s4.md#dup)\n"
    page = _put(tmp_path, "README.md", text)
    report = fel.fix(tmp_path)
    assert page.read_text(encoding="utf-8") == text
    assert report.missing == [("README.md", "docs/evidence.md#nowhere")]
    assert report.ambiguous == [("README.md", "docs/evidence.md#dup")]
    assert report.duplicates == {"dup": ["docs/evidence/final.md", "docs/evidence/s4.md"]}


def test_a_section_page_prefers_its_own_part_file(tmp_path: Path) -> None:
    _tree(tmp_path)
    _put(tmp_path, "docs/evidence/s3.md", '<a id="shared"></a>\n')
    _put(tmp_path, "docs/evidence/general.md", '<a id="shared"></a>\n')
    s3 = _put(tmp_path, "03-x/README.md", "[a](../docs/evidence.md#shared)\n")
    root = _put(tmp_path, "setup/README.md", "[a](../docs/evidence.md#shared)\n")
    final = _put(tmp_path, "final-project/README.md", "[a](../docs/evidence.md#dup)\n")
    report = fel.fix(tmp_path)
    assert s3.read_text(encoding="utf-8") == "[a](../docs/evidence/s3.md#shared)\n"
    assert root.read_text(encoding="utf-8") == "[a](../docs/evidence/general.md#shared)\n"
    assert final.read_text(encoding="utf-8") == "[a](../docs/evidence/final.md#dup)\n"
    assert report.ambiguous == []
    assert "shared" in report.duplicates


def test_page_structure_headings_shared_by_every_file_are_not_duplicates(tmp_path: Path) -> None:
    _tree(tmp_path)
    for rel in fel.evidence_files(tmp_path):
        _put(tmp_path, rel, (tmp_path / rel).read_text(encoding="utf-8") + "\n## Results\n")
    assert "results" not in fel.fix(tmp_path).duplicates


def test_do_not_edit_paths_are_skipped(tmp_path: Path) -> None:
    _tree(tmp_path)
    text = "[a](../../../../docs/evidence.md#src-openai)\n"
    live = _put(tmp_path, "01-x/assignment/solution/live/README.md", text)
    fel.fix(tmp_path)
    assert live.read_text(encoding="utf-8") == text
