"""Hidden seeded violations on a TeamTrack copy (revealed in the Thursday review).

Each seed is a list of changes for `a4_support.make_build`. Routers added here import the database
models directly for brevity; that breaks R6, which is not what these builds test.
"""

from __future__ import annotations

from a4_support import NewFile, Patch, include_router

_HEADER = '''\
"""Seeded router for the A4 grader."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import Id, current_actor, get_db, require_writer
from app.api.pagination import Page, to_page
from app.api.schemas import IssueOut
from app.db.models import Issue
from app.services.context import Actor
from app.services.errors import NotFound

router = APIRouter(tags=["a4-seed"])
'''


def _router(module: str, body: str) -> list[Patch | NewFile]:
    return [NewFile(f"api/{module}.py", _HEADER + body), include_router(module)]


def recent(live_only: bool) -> list[Patch | NewFile]:
    """A new list endpoint; it ignores deleted_at unless `live_only`."""
    where = ", Issue.deleted_at.is_(None)" if live_only else ""
    return _router(
        "a4_recent",
        f"""

@router.get("/projects/{{project_id}}/recent-issues", response_model=Page[IssueOut])
def recent_issues(
    project_id: Id, actor: Actor = Depends(current_actor), db: Session = Depends(get_db)
) -> Page[IssueOut]:
    stmt = (
        select(Issue)
        .where(Issue.org_id == actor.org_id, Issue.project_id == project_id{where})
        .order_by(Issue.id)
        .limit(50)
    )
    return to_page(list(db.scalars(stmt)), None, IssueOut.model_validate)
""",
    )


H_RECENT = recent(live_only=False)
H_RECENT_OK = recent(live_only=True)

# A board-style response: deleted issues hide two levels down, inside a dict of lists.
H_NESTED_LIST = _router(
    "a4_columns",
    """

@router.get("/projects/{project_id}/columns")
def columns(
    project_id: Id, actor: Actor = Depends(current_actor), db: Session = Depends(get_db)
) -> dict[str, object]:
    rows = list(
        db.scalars(
            select(Issue).where(Issue.org_id == actor.org_id, Issue.project_id == project_id)
        )
    )
    shown = [IssueOut.model_validate(i).model_dump(mode="json") for i in rows]
    return {
        "columns": {
            status: [i for i in shown if i["status"] == status]
            for status in ("open", "in_progress", "done")
        }
    }
""",
)

# Only the transition service skips the live-issue lookup: a write-only violation.
H_TRANSITION = [
    Patch(
        "services/issues.py",
        "def transition(session: Session, actor: Actor, issue_id: int, status: str) -> Issue:\n"
        "    issue = get(session, actor, issue_id)\n",
        "def transition(session: Session, actor: Actor, issue_id: int, status: str) -> Issue:\n"
        "    issue = session.get(Issue, issue_id)\n"
        "    if issue is None or issue.org_id != actor.org_id:\n"
        '        raise NotFound("issue not found")\n',
    )
]

# A path parameter named `{id}` right after an `issues` segment.
H_ID_PARAM = _router(
    "a4_history",
    """

@router.get("/issues/{id}/history")
def issue_history(
    id: Id, actor: Actor = Depends(current_actor), db: Session = Depends(get_db)
) -> dict[str, object]:
    issue = db.get(Issue, id)
    if issue is None or issue.org_id != actor.org_id:
        raise NotFound("issue not found")
    return {"issue": IssueOut.model_validate(issue).model_dump(mode="json"), "events": []}
""",
)

# The issue parameter comes after another resource's parameter.
H_NESTED_PATH = _router(
    "a4_peek",
    """

@router.get("/projects/{project_id}/issues/{issue_id}/peek")
def peek(
    project_id: Id,
    issue_id: Id,
    actor: Actor = Depends(current_actor),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    issue = db.get(Issue, issue_id)
    if issue is None or issue.org_id != actor.org_id or issue.project_id != project_id:
        raise NotFound("issue not found")
    return {"id": issue.id, "title": issue.title}
""",
)


def watches(live_only: bool) -> list[Patch | NewFile]:
    """A write that names an issue in its body; it accepts a deleted one unless `live_only`."""
    deleted = " or issue.deleted_at is not None" if live_only else ""
    return _router(
        "a4_watches",
        f"""

class WatchIn(BaseModel):
    issue_id: int


@router.post("/projects/{{project_id}}/watches", status_code=201)
def watch(
    project_id: Id,
    body: WatchIn,
    actor: Actor = Depends(require_writer),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    issue = db.get(Issue, body.issue_id)
    if issue is None or issue.org_id != actor.org_id or issue.project_id != project_id{deleted}:
        raise NotFound("issue not found")
    return {{"issue_id": issue.id, "watching": True}}
""",
    )


H_BODY = watches(live_only=False)
H_BODY_OK = watches(live_only=True)

# Shares numeric ids with the deleted issues (project 1, issue count) but holds no issue.
H_DECOY = _router(
    "a4_digest",
    """

@router.get("/projects/{project_id}/digest")
def digest(
    project_id: Id, actor: Actor = Depends(current_actor), db: Session = Depends(get_db)
) -> dict[str, object]:
    live = list(
        db.scalars(
            select(Issue.id).where(
                Issue.org_id == actor.org_id,
                Issue.project_id == project_id,
                Issue.deleted_at.is_(None),
            )
        )
    )
    return {"id": project_id, "project_id": project_id, "live_issues": len(live)}
""",
)
