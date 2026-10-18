"""Results dot charts: one dot per run per arm, filled = passed, hollow = failed.

Every count comes from docs/evidence/s1.md to s4.md and docs/evidence/final.md. Colour is never the
only carrier: every arm is named in words ("Bare", "Harness") and every dot group ends in words
("3 of 3 passed" or "3 of 3 failed"; every group in these charts is all-pass or all-fail). The
slide carries the title, the pass rule, and the reading, so the charts have no title or footnote.
"""

from __future__ import annotations

from exlib import BLUE, GREY, Scene, metrics
from style import FONT_TITLE as T

P, F = True, False
Row = tuple[str, list[bool], list[bool]]


def _count(runs: list[bool]) -> str:
    n, k = len(runs), sum(runs)
    if k == n:
        return f"{n} of {n} passed"
    if k == 0:
        return f"{n} of {n} failed"
    raise ValueError("a mixed group: write its counts out")


def _dots(s: Scene, x: float, cy: float, runs: list[bool], color: str, dot: float, step: float):
    for i, passed in enumerate(runs):
        s.box(
            x + i * step,
            cy - dot / 2,
            dot,
            dot,
            shape="ellipse",
            stroke=color,
            fill=color if passed else None,
            stroke_width=4,
        )


def stacked_chart(s: Scene, rows: list[Row], size: float = T) -> None:
    """A card chart: per row a label, then a "Bare" line and a "Harness" line of dots."""
    m = metrics()
    dot, step, line_h, gap = 46, 62, 70, 40
    label_w = max(m.width(label, size) for label, _, _ in rows) + 50
    arm_w = m.width("Harness", size) + 40
    most = max(max(len(b), len(h)) for _, b, h in rows)
    x_arm = 60 + label_w
    x_dots = x_arm + arm_w + 30
    x_count = x_dots + most * step + 10
    y = 60
    for label, bare, harn in rows:
        block = 2 * line_h + 10
        s.text(60, y + block / 2 - m.height(label, size) / 2, label, size)
        for k, (arm, runs, role, color) in enumerate(
            (("Bare", bare, "bare", GREY), ("Harness", harn, "harness", BLUE))
        ):
            cy = y + line_h / 2 + k * (line_h + 10)
            s.box(x_arm, cy - 32, arm_w, 64, arm, role=role, size=size, pad=12)
            _dots(s, x_dots, cy, runs, color, dot, step)
            s.text(x_count, cy - m.height("x", size) / 2, _count(runs), size)
        y += block + gap


def column_chart(s: Scene, rows: list[Row], size: float = T) -> None:
    """A diagram-slide chart: one row per label, a "Bare arm" and a "Harness arm" column."""
    m = metrics()
    dot, step = 46, 62
    label_w = max(m.width(label, size) for label, _, _ in rows) + 50
    count_w = max(m.width(_count(r), size) for _, b, h in rows for r in (b, h))
    most = max(max(len(b), len(h)) for _, b, h in rows)
    group_w = most * step + 10 + count_w
    x_bare = 60 + label_w
    x_harn = x_bare + group_w + 70
    s.box(x_bare, 60, None, 64, "Bare arm", role="bare", size=size, stroke_width=3)
    s.box(x_harn, 60, None, 64, "Harness arm", role="harness", size=size, stroke_width=3)
    y = 160
    for label, bare, harn in rows:
        row_h = max(84, m.height(label, size) + 10)
        cy = y + row_h / 2
        s.text(60, cy - m.height(label, size) / 2, label, size)
        for x0, runs, color in ((x_bare, bare, GREY), (x_harn, harn, BLUE)):
            _dots(s, x0, cy, runs, color, dot, step)
            s.text(x0 + len(runs) * step + 10, cy - m.height("x", size) / 2, _count(runs), size)
        y += row_h + 22


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # docs/evidence/s1.md, "Pilot results for F1": runs 3 (medium) and 4 (low) and the
    # class-profile round, legacy-pattern ticket, 0 of 3 / 0 of 3 / 0 of 1 failing in each arm.
    @diagram(S1, "results-s1", canvas="chart")
    def results_s1(s: Scene) -> None:
        stacked_chart(
            s,
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Class settings", [P], [P]),
            ],
        )

    # docs/evidence/s2.md, "Pilot results for F2": runs 3 and 4 and the class-profile round,
    # 0 failing in each arm (run 2 is a measurement bug and is not shown).
    @diagram(S2, "results-s2", canvas="chart")
    def results_s2(s: Scene) -> None:
        stacked_chart(
            s,
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Class settings", [P], [P]),
            ],
        )

    # docs/evidence/s3.md: the S3 confirmation on Feature 4 (bare 1 out-of-scope file in each of 3
    # runs = failed, harness 0 = passed) and "Pilot results for F3": run 2 on the plain ticket
    # (0 of 3 failing each), runs 3 and 4 and the class-profile round on the middleware ticket
    # (0 of 3, 0 of 3, 0 of 1 failing each, 7 runs per arm).
    @diagram(S3, "results-s3", canvas="chart")
    def results_s3(s: Scene) -> None:
        stacked_chart(
            s,
            [
                ("Feature 4,\nversion checks", [F] * 3, [P] * 3),
                ("Feature 3,\nplain ticket", [P] * 3, [P] * 3),
                ("Feature 3,\nmiddleware temptation", [P] * 7, [P] * 7),
            ],
        )

    # docs/evidence/s4.md, "Pilot results for F4": run 2 and run 3 (medium) and the class-profile
    # round, 3 of 3 / 3 of 3 / 1 of 1 failing in each arm (69 hidden tests and 4 mutants to pass).
    @diagram(S4, "results-s4", canvas="chart")
    def results_s4(s: Scene) -> None:
        stacked_chart(
            s,
            [
                ("Medium effort,\nround 1", [F] * 3, [F] * 3),
                ("Medium effort,\nround 2", [F] * 3, [F] * 3),
                ("Class settings", [F], [F]),
            ],
        )

    # docs/evidence/final.md, "The pilot's dots for F1 to F4" (runs 3 and 4 and the class-profile
    # round: Features 1 to 3 7 of 7 passed per arm; Feature 4 run 3 and class round, 0 of 4 passed
    # per arm, as general.md's S4 row) and "The S3 confirmation" (bare 0 of 3, harness 3 of 3).
    @diagram(DOCS, "results-final", canvas="strip")
    def results_final(s: Scene) -> None:
        column_chart(
            s,
            [
                ("Section 1:\nInstructions", [P] * 7, [P] * 7),
                ("Section 2: State\nand sessions", [P] * 7, [P] * 7),
                ("Section 3,\nFeature 3", [P] * 7, [P] * 7),
                ("Section 3,\nFeature 4", [F] * 3, [P] * 3),
                ("Section 4:\nVerification", [F] * 4, [F] * 4),
            ],
        )
