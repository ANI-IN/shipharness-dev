"""Hidden A2 scenarios (kept out of the starter): other stop points, a four-step feature with two
chained migrations, and agents that write notes, rewrite progress.md, or tick a step early."""

from __future__ import annotations

from a2_scenario.feature import Feature, FileSlot, Step
from a2_scenario.scenarios import COMMENTS, Scenario

LABELS_MIGRATION = '''"""Labels table."""

import sqlalchemy as sa
from alembic import op

revision = "{rev}"
down_revision = "{down}"


def upgrade() -> None:
    op.create_table(
        "labels",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("labels")
'''

LABELS_MODELS = '''"""Labels table definition."""

import sqlalchemy as sa

from app.db import metadata

labels = sa.Table(
    "labels",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False, unique=True),
)
'''

LINKS_MIGRATION = '''"""Issue labels table."""

import sqlalchemy as sa
from alembic import op

revision = "{rev}"
down_revision = "{down}"


def upgrade() -> None:
    op.create_table(
        "issue_labels",
        sa.Column("issue_id", sa.Integer, sa.ForeignKey("issues.id"), primary_key=True),
        sa.Column("label_id", sa.Integer, sa.ForeignKey("labels.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("issue_labels")
'''

LINKS_MODELS = '''"""Issue labels table definition."""

import sqlalchemy as sa

from app.db import metadata
from app.labels.models import labels

issue_labels = sa.Table(
    "issue_labels",
    metadata,
    sa.Column("issue_id", sa.Integer, sa.ForeignKey("issues.id"), primary_key=True),
    sa.Column("label_id", sa.Integer, sa.ForeignKey(labels.c.id), primary_key=True),
)
'''

LABELS_SERVICE = '''"""Create labels and put them on issues."""

import sqlalchemy as sa

from app.labels.links import issue_labels
from app.labels.models import labels


def create_label(conn, name: str) -> int:
    text = name.strip()
    if not 1 <= len(text) <= 50:
        raise ValueError("name must be 1 to 50 characters")
    return int(conn.execute(labels.insert().values(name=text)).inserted_primary_key[0])


def add_label(conn, issue_id: int, label_id: int) -> None:
    conn.execute(issue_labels.insert().values(issue_id=issue_id, label_id=label_id))


def labels_for_issue(conn, issue_id: int) -> list[str]:
    query = sa.select(labels.c.name).join(issue_labels, issue_labels.c.label_id == labels.c.id)
    query = query.where(issue_labels.c.issue_id == issue_id).order_by(labels.c.name)
    return [row.name for row in conn.execute(query)]
'''

LABELS_TESTS = '''"""Tests for the label service."""

import pytest
import sqlalchemy as sa

from app.db import issues, metadata
from app.labels.service import add_label, create_label, labels_for_issue


@pytest.fixture
def conn():
    engine = sa.create_engine("sqlite://")
    metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(issues.insert().values(id=1, title="first"))
        yield connection


def test_labels_on_an_issue_are_sorted_by_name(conn):
    add_label(conn, 1, create_label(conn, "ui"))
    add_label(conn, 1, create_label(conn, "bug"))
    assert labels_for_issue(conn, 1) == ["bug", "ui"]


def test_a_blank_name_is_rejected(conn):
    with pytest.raises(ValueError):
        create_label(conn, " ")
'''

LABELS = Feature(
    id="labels",
    title="Labels on issues",
    summary="Teams want to tag issues. Add labels, a link table, a label service, and tests.",
    rev_code="l",
    base_rev="0001",
    steps=(
        Step(
            "S1",
            "Labels table",
            "one migration that creates the labels table, and app/labels/models.py",
            (
                FileSlot("migration", "migrations/versions/{rev}_labels.py", LABELS_MIGRATION),
                FileSlot("models", "app/labels/models.py", LABELS_MODELS),
            ),
        ),
        Step(
            "S2",
            "Issue labels table",
            "one migration that creates the issue_labels table on top of the labels "
            "migration, and app/labels/links.py",
            (
                FileSlot("migration", "migrations/versions/{rev}_issue_labels.py", LINKS_MIGRATION),
                FileSlot("links", "app/labels/links.py", LINKS_MODELS),
            ),
        ),
        Step(
            "S3",
            "Label service",
            "app/labels/service.py",
            (FileSlot("service", "app/labels/service.py", LABELS_SERVICE),),
        ),
        Step(
            "S4",
            "Label tests",
            "tests/visible/test_labels.py",
            (FileSlot("tests", "tests/visible/test_labels.py", LABELS_TESTS),),
        ),
    ),
)

HIDDEN: tuple[Scenario, ...] = (
    Scenario(
        name="H1-uneven-stops",
        description="stops after one of two files, after a commit plus one file, and mid-step",
        feature=COMMENTS,
        budgets=(4, 7, 5, 9),
    ),
    Scenario(
        name="H2-four-steps",
        description="a four-step feature with two chained migrations",
        feature=LABELS,
        budgets=(7, 5, 6, 6),
    ),
    Scenario(
        name="H3-notes-and-rewrite",
        description="the agent writes a handoff note, then rewrites progress.md",
        feature=LABELS,
        budgets=(7, 7, 6, 6),
        behaviours={1: "note", 2: "clobber"},
    ),
    Scenario(
        name="H4-early-tick",
        description="the agent ticks the next step in the exec plan before doing it",
        feature=COMMENTS,
        budgets=(7, 6, 7, 5),
        behaviours={1: "tick"},
    ),
)
