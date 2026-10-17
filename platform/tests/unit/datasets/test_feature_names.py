"""Readable feature names: one alias per dataset feature, accepted by every command in place of
the code (case-insensitive) and normalised to the code; the dataset and exports keep the code."""

from __future__ import annotations

import json

import pytest

from shipharness.ab.commands import FEATURES_FILE
from shipharness.datasets.names import (
    FEATURE_ALIASES,
    UnknownFeature,
    feature_code,
    feature_label,
    valid_feature_names,
)

EXPECTED = {
    "F1": "org-search",
    "F2": "comments",
    "F3": "idempotent-create",
    "F4": "version-checks",
    "F5": "bulk-close",
    "F6": "watchers",
    "F7": "labels",
}


def _dataset_features() -> set[str]:
    ids = set()
    for line in FEATURES_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["inputs"]["feature_id"])
    return ids


def test_every_dataset_feature_has_exactly_one_alias() -> None:
    # Control tasks (C1-C8) are not course features: they keep their code and have no alias.
    features = {code for code in _dataset_features() if code.startswith("F")}
    assert features == set(FEATURE_ALIASES)
    aliases = list(FEATURE_ALIASES.values())
    assert len(aliases) == len(set(aliases))  # one feature per alias
    assert FEATURE_ALIASES == EXPECTED


@pytest.mark.parametrize(("name", "code"), [*((a, c) for c, a in EXPECTED.items())])
def test_an_alias_normalises_to_its_code(name: str, code: str) -> None:
    assert feature_code(name) == code
    assert feature_code(name.upper()) == code
    assert feature_code(f" {name.title()} ") == code


def test_codes_still_work_in_any_case() -> None:
    assert feature_code("F4") == "F4"
    assert feature_code("f4") == "F4"
    assert feature_code("C3") == "C3"  # control tasks keep their code


def test_an_unknown_name_lists_the_valid_names_and_codes() -> None:
    with pytest.raises(UnknownFeature) as caught:
        feature_code("versions")
    message = str(caught.value)
    assert "'versions'" in message
    for code, alias in EXPECTED.items():
        assert f"{alias} ({code})" in message
    assert valid_feature_names() in message


def test_the_label_puts_the_plain_name_next_to_the_code() -> None:
    assert feature_label("F4") == "F4 version checks"
    assert feature_label("F1") == "F1 org search"
    assert feature_label("C2") == "C2"  # no plain name: the code alone
    assert feature_label("F-07") == "F-07"
