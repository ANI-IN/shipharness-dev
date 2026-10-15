"""R3 conventions: every list returns {items, next_cursor}; cursor pagination is stable."""

from __future__ import annotations

import pytest

from conftest import auth, error_code


def list_paths(o):  # type: ignore[no-untyped-def]
    return [
        "/users",
        "/projects",
        f"/projects/{o.projects[0]}/members",
        f"/projects/{o.projects[0]}/issues",
        "/audit",
    ]


@pytest.mark.parametrize("index", range(5))
def test_list_envelope(client, acme, index: int) -> None:
    response = client.get(list_paths(acme)[index], headers=auth(acme.admin))
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"items", "next_cursor"}
    assert isinstance(body["items"], list)


def test_cursor_pagination_walks_every_issue_once(client, acme) -> None:
    path = f"/projects/{acme.projects[0]}/issues"
    seen: list[int] = []
    cursor = None
    for _ in range(20):
        query = "?limit=3" + (f"&cursor={cursor}" if cursor else "")
        body = client.get(path + query, headers=auth(acme.admin)).json()
        seen.extend(item["id"] for item in body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break
    assert seen == sorted(seen)
    assert len(seen) == len(set(seen)) == 10


def test_next_cursor_is_null_on_last_page(client, acme) -> None:
    body = client.get("/projects?limit=100", headers=auth(acme.admin)).json()
    assert body["next_cursor"] is None


def test_invalid_cursor_is_400_envelope(client, acme) -> None:
    response = client.get("/projects?cursor=not-a-cursor", headers=auth(acme.admin))
    assert response.status_code == 400
    assert error_code(response) == "invalid_cursor"


@pytest.mark.parametrize("limit", [0, 101, -1])
def test_out_of_range_limit_is_validation_error(client, acme, limit: int) -> None:
    response = client.get(f"/projects?limit={limit}", headers=auth(acme.admin))
    assert response.status_code == 422
    assert error_code(response) == "validation_error"


def test_unknown_route_uses_error_envelope(client, acme) -> None:
    response = client.get("/nope", headers=auth(acme.admin))
    assert response.status_code == 404
    assert error_code(response) == "not_found"


def test_bad_body_uses_validation_envelope(client, acme) -> None:
    response = client.post("/projects", json={"name": 5}, headers=auth(acme.admin))
    assert response.status_code == 422
    assert error_code(response) == "validation_error"
