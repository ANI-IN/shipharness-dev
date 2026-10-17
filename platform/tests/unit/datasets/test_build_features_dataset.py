"""scripts/build_features_dataset.py: deterministic 60-line build from manifests and ticket sources.

The F1-F7 manifests are fixtures (B-features writes the real ones in parallel); the controls and the
ticket sources are the real files.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tomllib
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from shipharness.datasets.features_checks import check_features_file, check_features_line
from shipharness.datasets.schema import FeatureTask

from .features_fixtures import CONTROLS, FEATURES, REPO, make_repo

SCRIPT = REPO / "scripts" / "build_features_dataset.py"
TICKETS = REPO / "datasets" / "sources" / "tickets.toml"
KEY_PHRASES = {
    "F1": ["GET /issues", "q"],
    "F2": ["/issues/{issue_id}/comments", "/comments/{comment_id}"],
    "F3": ["Idempotency-Key", "idempotency_conflict"],
    "F4": ["If-Match", "/issues/{issue_id}/history"],
    "F5": ["bulk-close", "issue_ids"],
    "F6": ["/watchers/me", "/me/watching"],
    "F7": ["/labels", "label_exists"],
}


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_features_dataset", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=120,
    )


@pytest.fixture(scope="module")
def repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return make_repo(tmp_path_factory.mktemp("course"))


@pytest.fixture(scope="module")
def lines(repo: Path) -> list[dict[str, Any]]:
    return load_script().build_lines(repo)


def by_group(lines: list[dict[str, Any]], group: str) -> list[dict[str, Any]]:
    return [line for line in lines if line["metadata"]["group"] == group]


# -- the whole file -----------------------------------------------------------------------------


def test_builds_sixty_valid_lines_that_pass_both_checks(
    repo: Path, lines: list[dict[str, Any]]
) -> None:
    assert len(lines) == 60
    for line in lines:
        FeatureTask.model_validate(line)
    assert check_features_file(lines) == []
    problems = [p for line in lines for p in check_features_line(line, repo)]
    assert problems == []


def test_output_is_deterministic_jsonl(repo: Path, tmp_path: Path) -> None:
    first, second = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    for out in (first, second):
        result = run_script("--repo", str(repo), "--out", str(out))
        assert result.returncode == 0, result.stdout + result.stderr
    data = first.read_bytes()
    assert data == second.read_bytes()
    assert b"\r" not in data and data.endswith(b"\n")
    assert len(data.decode("utf-8").splitlines()) == 60


def test_check_mode_compares_with_the_written_file(repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "features.jsonl"
    assert run_script("--repo", str(repo), "--out", str(out)).returncode == 0
    assert run_script("--repo", str(repo), "--out", str(out), "--check").returncode == 0
    out.write_text(out.read_text(encoding="utf-8").replace("F1", "F9", 1), encoding="utf-8")
    result = run_script("--repo", str(repo), "--out", str(out), "--check")
    assert result.returncode == 1 and "differs" in result.stdout + result.stderr


def test_groups_come_in_the_registered_order(lines: list[dict[str, Any]]) -> None:
    order = [line["metadata"]["group"] for line in lines]
    blocks = [g for n, g in enumerate(order) if n == 0 or order[n - 1] != g]
    expected = ["canonical", "reworded", "alt_checkpoint", "session_stop", "trap", "control"]
    assert blocks == expected
    assert Counter(order) == {
        "canonical": 7,
        "reworded": 21,
        "alt_checkpoint": 8,
        "session_stop": 9,
        "trap": 7,
        "control": 8,
    }


def test_example_ids_and_variants(lines: list[dict[str, Any]]) -> None:
    ids = [line["metadata"]["example_id"] for line in lines]
    assert len(set(ids)) == 60
    assert "F1-canonical" in ids and "F1-reworded-terse" in ids and "F2-stop-3" in ids
    assert "F4-alt-b" in ids and "F7-trap" in ids and "C8-canonical" in ids
    for line in lines:
        assert line["metadata"]["control"] is line["inputs"]["feature_id"].startswith("C")


# -- groups -------------------------------------------------------------------------------------


def test_canonical_lines_copy_the_manifest(repo: Path, lines: list[dict[str, Any]]) -> None:
    for line in by_group(lines, "canonical"):
        task = line["inputs"]["feature_id"].lower()
        data = tomllib.loads((repo / "teamtrack" / "reference" / task / "task.toml").read_text())
        assert line["inputs"]["ticket_text"] == data["canonical_ticket"]
        assert line["inputs"]["checkpoint"] == data["start_checkpoint"]
        assert line["inputs"]["session_budget"] == data["session_budget"]
        assert line["outputs"]["mutant_set"] == data["mutant_set"]
        assert line["outputs"]["primary_measure"] == data["primary_measure"]
        assert line["outputs"]["allowed_paths"] == data["allowed_paths"]
        assert line["inputs"]["variant"] == "canonical"


def test_reworded_lines_cover_three_styles_per_feature(lines: list[dict[str, Any]]) -> None:
    reworded = by_group(lines, "reworded")
    styles = Counter((line["inputs"]["feature_id"], line["metadata"]["style"]) for line in reworded)
    assert set(styles) == {(f, s) for f in FEATURES for s in ("terse", "pm", "bug")}
    texts = [line["inputs"]["ticket_text"] for line in reworded]
    assert len(set(texts)) == 21


def test_trap_lines_name_their_trap(lines: list[dict[str, Any]]) -> None:
    traps = by_group(lines, "trap")
    assert sorted(line["inputs"]["feature_id"] for line in traps) == list(FEATURES)
    for line in traps:
        assert line["metadata"]["trap"] in {"legacy-pattern", "tempting-middleware"}
        assert line["metadata"]["trap_detail"]
        assert line["inputs"]["variant"] == f"trap-{line['metadata']['trap']}"
    kinds = Counter(line["metadata"]["trap"] for line in traps)
    assert kinds["legacy-pattern"] >= 1 and kinds["tempting-middleware"] >= 1


def test_session_stop_lines_split_the_manifest_budget(lines: list[dict[str, Any]]) -> None:
    stops = by_group(lines, "session_stop")
    canonical = {
        line["inputs"]["feature_id"]: line["inputs"]["session_budget"]
        for line in by_group(lines, "canonical")
    }
    assert Counter(line["inputs"]["feature_id"] for line in stops) == {"F2": 3, "F6": 3, "F7": 3}
    for feature in ("F2", "F6", "F7"):
        budgets = [
            line["inputs"]["session_budget"]
            for line in stops
            if line["inputs"]["feature_id"] == feature
        ]
        assert all(len(b) == 2 and min(b) >= 1 for b in budgets)
        assert {sum(b) for b in budgets} == {sum(canonical[feature])}
        firsts = [b[0] for b in budgets]
        assert firsts == sorted(firsts) and len(set(firsts)) == 3


def test_alt_checkpoint_lines_use_that_checkpoints_hidden_tests(
    lines: list[dict[str, Any]],
) -> None:
    alts = by_group(lines, "alt_checkpoint")
    pairs = {(line["inputs"]["feature_id"], line["inputs"]["checkpoint"]) for line in alts}
    assert pairs == {(f, cp) for f in ("F1", "F2", "F3", "F4") for cp in ("m1-alt-a", "m1-alt-b")}
    for line in alts:
        assert line["outputs"]["hidden_test_ids"]
        assert line["metadata"]["base_checkpoint"] != line["inputs"]["checkpoint"]


def test_control_lines_come_from_the_control_manifests(lines: list[dict[str, Any]]) -> None:
    controls = by_group(lines, "control")
    assert [line["inputs"]["feature_id"] for line in controls] == list(CONTROLS)
    for line in controls:
        assert line["inputs"]["checkpoint"] == "m1-s1-start"
        assert line["outputs"]["primary_measure"] == ""
        assert line["metadata"]["control"] is True


# -- splits -------------------------------------------------------------------------------------


def split_members(lines: list[dict[str, Any]], name: str) -> list[str]:
    return [line["metadata"]["example_id"] for line in lines if name in line["split"]]


def test_smoke_split(lines: list[dict[str, Any]]) -> None:
    assert split_members(lines, "smoke") == [
        "F1-canonical",
        "F2-canonical",
        "F3-canonical",
        "F4-canonical",
        "C5-canonical",
        "C6-canonical",
    ]


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_section_splits(lines: list[dict[str, Any]], n: int) -> None:
    f = f"F{n}"
    assert split_members(lines, f"section-{n}") == [
        f"{f}-canonical",
        f"{f}-reworded-terse",
        f"{f}-reworded-pm",
        f"{f}-reworded-bug",
        f"{f}-alt-a",
        f"{f}-alt-b",
        f"{f}-trap",
        f"C{n}-canonical",
    ]


def test_every_line_has_a_split_and_splits_are_sorted(lines: list[dict[str, Any]]) -> None:
    for line in lines:
        assert line["split"] == sorted(line["split"]) and line["split"]
    rest = [line for line in lines if line["split"] == ["extended"]]
    assert len(rest) == 60 - 6 - 32 + 4  # F1-F4 canonical are in a section and in smoke


# -- failures -----------------------------------------------------------------------------------


def test_missing_feature_manifest_names_the_file(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "course", features=("F1", "F2", "F4", "F5", "F6", "F7"))
    result = run_script("--repo", str(repo), "--out", str(tmp_path / "x.jsonl"))
    assert result.returncode == 2
    assert "teamtrack/reference/f3/task.toml" in result.stderr
    assert not (tmp_path / "x.jsonl").exists()


def test_missing_hidden_entry_for_an_alternate_checkpoint_is_named(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "course")
    path = repo / "teamtrack" / "reference" / "f2" / "task.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line for line in text.splitlines() if not line.startswith('"m1-alt-b"')) + "\n",
        encoding="utf-8",
    )
    module = load_script()
    with pytest.raises(module.DatasetSourceError, match=r"F2.*m1-alt-b"):
        module.build_lines(repo)


def test_failed_checks_stop_the_write(repo: Path, tmp_path: Path) -> None:
    broken = make_repo(tmp_path / "course")
    (broken / "teamtrack" / "reference" / "checkpoints.toml").write_text(
        '[checkpoints."m1-s1-start"]\ntasks = []\n', encoding="utf-8"
    )
    out = tmp_path / "x.jsonl"
    result = run_script("--repo", str(broken), "--out", str(out))
    assert result.returncode == 1
    assert "m1-s2-start" in result.stdout + result.stderr
    assert not out.exists()


# -- ticket sources -----------------------------------------------------------------------------


def ticket_texts() -> list[tuple[str, str, str]]:
    data = tomllib.loads(TICKETS.read_text(encoding="utf-8"))
    found = []
    for group in ("reworded", "trap"):
        for entry in data[group]:
            found.append((group, entry["feature"], entry["text"]))
    return found


def test_ticket_sources_have_the_registered_counts() -> None:
    data = tomllib.loads(TICKETS.read_text(encoding="utf-8"))
    assert len(data["reworded"]) == 21
    assert len(data["trap"]) == 7
    assert len(data["session_stop"]) == 9
    assert len(data["alt_checkpoint"]) == 8


@pytest.mark.parametrize(
    ("group", "feature", "text"), ticket_texts(), ids=lambda v: v if len(v) < 12 else "text"
)
def test_ticket_text_points_to_the_spec_and_names_the_feature(
    group: str, feature: str, text: str
) -> None:
    assert f"docs/features/{feature.lower()}.md" in text
    for phrase in KEY_PHRASES[feature]:
        assert phrase in text, (group, feature, phrase)


def test_ticket_texts_pass_the_prose_lint() -> None:
    spec = importlib.util.spec_from_file_location("lint_prose", REPO / "scripts" / "lint_prose.py")
    assert spec and spec.loader
    lint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint)
    problems = {
        f"{group} {feature}": lint.lint_text(text)
        for group, feature, text in ticket_texts()
        if lint.lint_text(text)
    }
    assert problems == {}


def test_trap_texts_mention_the_temptation() -> None:
    data = tomllib.loads(TICKETS.read_text(encoding="utf-8"))
    for entry in data["trap"]:
        if entry["trap"] == "tempting-middleware":
            assert "app/api/middleware.py" in entry["text"]
        else:
            assert "legacy" in entry["text"].lower()


def test_written_file_is_json_per_line(repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "features.jsonl"
    assert run_script("--repo", str(repo), "--out", str(out)).returncode == 0
    parsed = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert [p["metadata"]["example_id"] for p in parsed][:2] == ["F1-canonical", "F2-canonical"]
