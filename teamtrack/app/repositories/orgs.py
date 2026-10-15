from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Org


def get(session: Session, org_id: int) -> Org | None:
    return session.get(Org, org_id)


def count(session: Session) -> int:
    return session.scalar(select(func.count()).select_from(Org)) or 0


def add(session: Session, name: str, slug: str) -> Org:
    org = Org(name=name, slug=slug)
    session.add(org)
    session.flush()
    return org
