"""The course's score records measured before class ship with the course (`docs/evidence/scores/`):
screen 4 always shows them. They carry no key, no host path, and no LangSmith link (those name the
course's workspace), and the release build keeps them."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from shipharness.ab.score import REFEREE_VERSION, ScoreRecord
from shipharness.layout import find_repo_root
from shipharness.log_setup import KEY_PATTERNS

REPO = find_repo_root(Path(__file__))
SCORES = REPO / "docs" / "evidence" / "scores"
SECTIONS = REPO / "docs" / "evidence" / "score-sections.json"

_spec = importlib.util.spec_from_file_location(
    "make_release_for_records", REPO / "platform" / "scripts" / "make_release.py"
)
assert _spec and _spec.loader
mr = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = mr
_spec.loader.exec_module(mr)

WINDOWS_ABS = re.compile(r"(?<![A-Za-z])[A-Za-z]:(?:\\\\|\\|/)[^\s\"']")
POSIX_ABS = re.compile(r"(?<![\w.:/-])/(?:home|Users|tmp|var|private|root|mnt|opt|etc|srv)/")


def _files() -> list[Path]:
    return sorted(SCORES.glob("*.json"))


def test_the_records_are_current_score_records_of_real_runs() -> None:
    files = _files()
    assert len(files) >= 50
    for path in files:
        record = ScoreRecord.model_validate_json(path.read_text(encoding="utf-8"))
        assert path.stem == record.run_id
        assert record.referee_version == REFEREE_VERSION
        assert not record.constructed  # scripted examples are never counted


def test_the_records_carry_no_key_no_host_path_and_no_trace_link() -> None:
    for path in [*_files(), SECTIONS]:
        text = path.read_text(encoding="utf-8")
        for pattern in KEY_PATTERNS:
            assert not re.search(pattern, text), (path.name, pattern)
        assert not WINDOWS_ABS.search(text) and not POSIX_ABS.search(text), path.name
        assert "smith.langchain.com" not in text and "langchain" not in text.lower(), path.name


def test_every_record_names_its_section_or_none() -> None:
    sections = json.loads(SECTIONS.read_text(encoding="utf-8"))
    for path in _files():
        ab_id = json.loads(path.read_text(encoding="utf-8"))["ab_id"]
        assert ab_id in sections, path.name
        assert sections[ab_id] in (None, "demo-1", "demo-2", "demo-3", "demo-4", "final")


def test_the_release_ships_the_records_and_the_leak_check_passes() -> None:
    paths = [p.relative_to(REPO).as_posix() for p in [*_files(), SECTIONS]]
    for path in paths:
        assert mr.classify(path) is None, path
    assert mr.leaks(paths) == []
    assert set(paths) <= set(mr.select(paths).included)
