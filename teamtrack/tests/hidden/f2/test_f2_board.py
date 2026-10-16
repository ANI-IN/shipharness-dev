"""F2 hidden tests: the board's comments panel (spec: docs/features/f2.md, "Board")."""

from __future__ import annotations

import re

from hidden_support import auth


def login(client, email: str) -> None:  # type: ignore[no-untyped-def]
    response = client.post("/board/login", data={"email": email}, follow_redirects=False)
    assert response.status_code == 303


def comment_ids(html: str) -> list[str]:
    return re.findall(r'class="comment"[^>]*data-comment-id="(\d+)"', html) or re.findall(
        r'data-comment-id="(\d+)"[^>]*class="comment"', html
    )


def panel(html: str) -> str:
    match = re.search(r'<section[^>]*class="comments"[^>]*>(.*?)</section>', html, re.S)
    assert match, "no comments panel"
    return match.group(1)


def test_issue_page_has_a_comments_panel(client, acme) -> None:
    login(client, "member@acme.test")
    panel(client.get(f"/board/issues/{acme.issues[0]}").text)


def test_panel_lists_seeded_comments_oldest_first(client, acme) -> None:
    login(client, "member@acme.test")
    assert comment_ids(panel(client.get(f"/board/issues/{acme.issues[0]}").text)) == ["1", "2"]


def test_panel_shows_comment_text(client, acme) -> None:
    client.post(
        f"/issues/{acme.issues[1]}/comments",
        json={"body": "Seen on staging too"},
        headers=auth(acme.member),
    )
    login(client, "viewer@acme.test")
    assert "Seen on staging too" in panel(client.get(f"/board/issues/{acme.issues[1]}").text)


def test_writer_sees_the_add_form(client, acme) -> None:
    login(client, "member@acme.test")
    assert 'class="add-comment"' in client.get(f"/board/issues/{acme.issues[0]}").text


def test_viewer_sees_comments_but_no_form(client, acme) -> None:
    login(client, "viewer@acme.test")
    html = client.get(f"/board/issues/{acme.issues[0]}").text
    assert comment_ids(panel(html)) == ["1", "2"]
    assert 'class="add-comment"' not in html


def test_board_form_adds_a_comment_and_returns_to_the_issue(client, acme) -> None:
    login(client, "member@acme.test")
    response = client.post(
        f"/board/issues/{acme.issues[2]}/comments",
        data={"body": "Added on the board"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 303)
    assert response.headers["location"].endswith(f"/board/issues/{acme.issues[2]}")
    api = client.get(f"/issues/{acme.issues[2]}/comments", headers=auth(acme.member)).json()
    assert [c["body"] for c in api["items"]] == ["Added on the board"]


def test_comment_text_is_escaped(client, acme) -> None:
    client.post(
        f"/issues/{acme.issues[1]}/comments",
        json={"body": "<script>alert(1)</script>"},
        headers=auth(acme.member),
    )
    login(client, "member@acme.test")
    html = panel(client.get(f"/board/issues/{acme.issues[1]}").text)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_deleted_comment_leaves_the_panel(client, acme) -> None:
    client.delete("/comments/1", headers=auth(acme.member))
    login(client, "admin@acme.test")
    assert comment_ids(panel(client.get(f"/board/issues/{acme.issues[0]}").text)) == ["2"]
