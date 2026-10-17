"""Results dot charts: one dot per run per arm, filled = passed, hollow = failed.

Every count comes from docs/evidence/s1.md to s4.md and docs/evidence/final.md. The pass rule
and the reading of each chart are in the slide notes; the chart carries the title, one footnote
line with the pass rule, and the dots.
"""

from __future__ import annotations

from exlib import BLUE, GREY, INK, Scene
from style import FONT_BODY as B
from style import FONT_SMALL
from style import FONT_TITLE as T

P, F = True, False
DOT, STEP = 40, 54


def dot_chart(
    s: Scene,
    heading: str,
    rows: list[tuple[str, list[bool], list[bool]]],
    rule: str,
) -> None:
    most = max(max(len(b), len(h)) for _, b, h in rows)
    label_w = 470
    group_w = most * STEP + 160
    x_bare = 60 + label_w + 30
    x_harn = x_bare + group_w + 40
    s.text(60, 50, heading, T, INK, role="title")
    top = 150
    s.box(x_bare, top, 250, 64, "Bare arm", role="bare", stroke_width=3)
    s.box(x_harn, top, 250, 64, "Harness arm", role="harness", stroke_width=3)
    y = top + 100
    for label, bare, harn in rows:
        lines = label.count("\n") + 1
        row_h = max(90, lines * 35 + 30)
        s.text(60, y + row_h / 2 - lines * 17.5, label, B, INK)
        for x0, runs, color in ((x_bare, bare, GREY), (x_harn, harn, BLUE)):
            cy = y + row_h / 2 - DOT / 2
            for i, passed in enumerate(runs):
                s.box(
                    x0 + i * STEP,
                    cy,
                    DOT,
                    DOT,
                    shape="ellipse",
                    stroke=color,
                    fill=color if passed else None,
                    stroke_width=3,
                )
            s.text(
                x0 + len(runs) * STEP + 12,
                y + row_h / 2 - 17.5,
                f"{sum(runs)} of {len(runs)}",
                B,
                INK,
            )
        y += row_h + 16
    y += 20
    s.box(60, y + 2, 32, 32, shape="ellipse", stroke=INK, fill=INK)
    s.text(104, y, "passed", B, INK)
    s.box(240, y + 2, 32, 32, shape="ellipse", stroke=INK, stroke_width=3)
    s.text(284, y, "failed", B, INK)
    s.text(60, y + 70, rule, FONT_SMALL, INK, role="footnote")


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # docs/evidence/s1.md, "Pilot results for F1": runs 3 and 4, class-profile round.
    @diagram(S1, "results-s1")
    def results_s1(s: Scene) -> None:
        dot_chart(
            s,
            "Section 1: legacy pattern",
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Class settings", [P], [P]),
            ],
            "pass: no new tenant isolation leak",
        )

    # docs/evidence/s2.md, "Pilot results for F2": runs 3 and 4, class-profile round (run 2 is a
    # measurement bug and is not shown).
    @diagram(S2, "results-s2")
    def results_s2(s: Scene) -> None:
        dot_chart(
            s,
            "Section 2: comments",
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Class settings", [P], [P]),
            ],
            "pass: no continuity failure across sessions",
        )

    # docs/evidence/s3.md: the S3 confirmation (F4) and "Pilot results for F3".
    @diagram(S3, "results-s3")
    def results_s3(s: Scene) -> None:
        dot_chart(
            s,
            "Section 3: files outside allowed paths",
            [
                ("Version checks", [F] * 3, [P] * 3),
                ("Idempotency keys", [P] * 3, [P] * 3),
                ("Idempotency, middleware temptation", [P] * 7, [P] * 7),
            ],
            "pass: nothing shipped outside allowed paths",
        )

    # docs/evidence/s4.md, "Pilot results for F4": runs 2 and 3, class-profile round.
    @diagram(S4, "results-s4")
    def results_s4(s: Scene) -> None:
        dot_chart(
            s,
            "Section 4: version checks",
            [
                ("Medium effort, round 1", [F] * 3, [F] * 3),
                ("Medium effort, round 2", [F] * 3, [F] * 3),
                ("Class settings", [F], [F]),
            ],
            "pass: 69 hidden tests, 4 mutants caught",
        )

    # docs/evidence/final.md, "The pilot's dots for F1 to F4" and "The S3 confirmation".
    @diagram(DOCS, "results-final")
    def results_final(s: Scene) -> None:
        dot_chart(
            s,
            "All sections, each on its measure",
            [
                ("Section 1: legacy", [P] * 7, [P] * 7),
                ("Section 2: comments", [P] * 7, [P] * 7),
                ("Section 3: middleware", [P] * 7, [P] * 7),
                ("Section 3: scope", [F] * 3, [P] * 3),
                ("Section 4: hidden tests", [F] * 4, [F] * 4),
            ],
            "one dot per run, each arm",
        )
