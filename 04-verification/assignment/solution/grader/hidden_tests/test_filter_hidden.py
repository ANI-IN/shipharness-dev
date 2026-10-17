"""Hidden candidate tests for filter 6 (no duplicate test)."""

from __future__ import annotations

from pathlib import Path

import pytest
from a4_support import candidates, dedup_filter, filter_context

BASE = """\
def test_total(client):
    first = client.get("/a").json()["n"]
    second = client.get("/b").json()["n"]
    assert first < second
"""


def _verdict(tmp_path: Path, existing: str, candidate: str) -> object:
    old = candidates(tmp_path, {"tests/test_old.py": existing})
    (cand,) = candidates(tmp_path, {"tests/test_cand.py": candidate})
    return dedup_filter(old).evaluate(cand, filter_context(tmp_path))


@pytest.mark.criterion("F6-hidden")
def test_consistently_renamed_locals_are_a_duplicate(tmp_path: Path) -> None:
    cand = BASE.replace("first", "low").replace("second", "high").replace("test_total", "test_x")
    result = _verdict(tmp_path, BASE, cand)
    assert result.passed is False  # type: ignore[attr-defined]
    assert "tests/test_old.py::test_total" in result.reason  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_swapped_locals_are_not_a_duplicate(tmp_path: Path) -> None:
    cand = """\
def test_swapped(client):
    second = client.get("/a").json()["n"]
    first = client.get("/b").json()["n"]
    assert first < second
"""
    assert _verdict(tmp_path, BASE, cand).passed is True  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_a_different_fixture_is_not_a_duplicate(tmp_path: Path) -> None:
    cand = BASE.replace("client", "admin_client").replace("test_total", "test_admin")
    assert _verdict(tmp_path, BASE, cand).passed is True  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_a_different_global_helper_is_not_a_duplicate(tmp_path: Path) -> None:
    existing = "def test_a(client):\n    assert is_live(client.get('/x'))\n"
    cand = "def test_b(client):\n    assert is_archived(client.get('/x'))\n"
    assert _verdict(tmp_path, existing, cand).passed is True  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_a_different_attribute_is_not_a_duplicate(tmp_path: Path) -> None:
    existing = "def test_a(client):\n    r = client.get('/x')\n    assert r.status_code\n"
    cand = "def test_b(client):\n    r = client.get('/x')\n    assert r.headers\n"
    assert _verdict(tmp_path, existing, cand).passed is True  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_parametrize_data_matters(tmp_path: Path) -> None:
    existing = """\
import pytest

@pytest.mark.parametrize("n", [1, 2])
def test_n(n):
    assert n > 0
"""
    same = existing.replace("test_n", "test_m")
    other = existing.replace("[1, 2]", "[3, 4]").replace("test_n", "test_k")
    assert _verdict(tmp_path / "same", existing, same).passed is False  # type: ignore[attr-defined]
    assert _verdict(tmp_path / "other", existing, other).passed is True  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_a_later_copy_of_an_earlier_kept_candidate_is_discarded(tmp_path: Path) -> None:
    cands = candidates(
        tmp_path,
        {"tests/test_cand.py": BASE + "\n\n" + BASE.replace("test_total", "test_total_again")},
    )
    flt = dedup_filter([])
    ctx = filter_context(tmp_path)
    first, second = (flt.evaluate(c, ctx) for c in cands)
    assert first.passed is True
    assert second.passed is False
    assert "tests/test_cand.py::test_total" in second.reason


@pytest.mark.criterion("F6-hidden")
def test_an_existing_test_is_not_its_own_duplicate(tmp_path: Path) -> None:
    old = candidates(tmp_path, {"tests/test_old.py": BASE})
    result = dedup_filter(old).evaluate(old[0], filter_context(tmp_path))
    assert result.passed is True


@pytest.mark.criterion("F6-hidden")
def test_methods_in_test_classes(tmp_path: Path) -> None:
    existing = "class TestA:\n    def test_one(self, client):\n        assert client.get('/a')\n"
    cand = "class TestB:\n    def test_two(self, client):\n        assert client.get('/a')\n"
    result = _verdict(tmp_path, existing, cand)
    assert result.passed is False  # type: ignore[attr-defined]
    assert "tests/test_old.py::TestA::test_one" in result.reason  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_async_duplicates(tmp_path: Path) -> None:
    existing = "async def test_a(client):\n    value = await client.get('/a')\n    assert value\n"
    cand = "async def test_b(client):\n    got = await client.get('/a')\n    assert got\n"
    assert _verdict(tmp_path, existing, cand).passed is False  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_loop_with_and_except_names_are_locals(tmp_path: Path) -> None:
    existing = """\
def test_a(tmp_path):
    for item in range(3):
        with open(tmp_path / str(item), "w") as handle:
            handle.write("x")
    try:
        int("x")
    except ValueError as error:
        assert str(error)
"""
    cand = (
        existing.replace("item", "i")
        .replace("handle", "fh")
        .replace("error", "exc")
        .replace("test_a", "test_b")
    )
    assert _verdict(tmp_path, existing, cand).passed is False  # type: ignore[attr-defined]


@pytest.mark.criterion("F6-hidden")
def test_a_file_that_does_not_parse_is_discarded_with_a_reason(tmp_path: Path) -> None:
    (cand,) = candidates(tmp_path, {"tests/test_broken.py": "def test_x(:\n    pass\n"})
    result = dedup_filter([]).evaluate(cand, filter_context(tmp_path))
    assert result.passed is False
    assert result.filter == 6
    assert result.reason
