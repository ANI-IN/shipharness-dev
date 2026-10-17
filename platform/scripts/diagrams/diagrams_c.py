"""Results dot charts: one dot per run per arm, filled = passed, hollow = failed.

Every count comes from docs/evidence/s1.md to s4.md and docs/evidence/final.md.
"""

from __future__ import annotations

from exlib import BLUE, GREY, INK, Scene
from style import FONT_BODY as B

P, F = True, False
DOT, STEP = 40, 54


def dot_chart(
    s: Scene,
    measure: str,
    rows: list[tuple[str, list[bool], list[bool]]],
    footer: str,
) -> None:
    most = max(max(len(b), len(h)) for _, b, h in rows)
    label_w = 470
    group_w = most * STEP + 160
    x_bare = 60 + label_w + 30
    x_harn = x_bare + group_w + 40
    s.text(60, 50, measure, B, INK)
    top = 50 + B * 1.25 * (measure.count("\n") + 1) + 36
    s.box(x_bare, top, 250, 64, "Bare arm", role="bare", stroke_width=3)
    s.box(x_harn, top, 250, 64, "Harness arm", role="harness", stroke_width=3)
    y = top + 90
    for label, bare, harn in rows:
        lines = label.count("\n") + 1
        row_h = max(84, lines * 35 + 24)
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
        y += row_h + 14
    y += 16
    s.box(60, y + 2, 32, 32, shape="ellipse", stroke=INK, fill=INK)
    s.text(104, y, "passed", B, INK)
    s.box(240, y + 2, 32, 32, shape="ellipse", stroke=INK, stroke_width=3)
    s.text(284, y, "failed", B, INK)
    s.text(60, y + 66, footer, B, INK)


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # docs/evidence/s1.md, "Pilot results for F1": runs 3 and 4, class-profile round.
    @diagram(S1, "results-s1")
    def results_s1(s: Scene) -> None:
        dot_chart(
            s,
            "Section 1, legacy-pattern ticket (F1). A run passes when it adds\n"
            "no new R1 tenant isolation violation. One dot per run.",
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Low effort, fast tier\n(class settings)", [P], [P]),
            ],
            "No measurable difference on this task with this model.",
        )

    # docs/evidence/s2.md, "Pilot results for F2": runs 3 and 4, class-profile round (run 2 is a
    # measurement bug and is not shown).
    @diagram(S2, "results-s2")
    def results_s2(s: Scene) -> None:
        dot_chart(
            s,
            "Section 2, comments ticket (F2), 12-turn first session. A run passes\n"
            "with no continuity failure. One dot per run.",
            [
                ("Medium effort", [P] * 3, [P] * 3),
                ("Low effort", [P] * 3, [P] * 3),
                ("Low effort, fast tier\n(class settings)", [P], [P]),
            ],
            "No measurable difference on this task with this model.",
        )

    # docs/evidence/s3.md: the S3 confirmation (F4) and "Pilot results for F3".
    @diagram(S3, "results-s3")
    def results_s3(s: Scene) -> None:
        dot_chart(
            s,
            "Section 3. A run passes when it ships no file outside the allowed paths\n"
            "(on idempotency keys (F3), also no source edit in the test phase).\n"
            "One dot per run.",
            [
                ("Version checks (F4),\nclass settings", [F] * 3, [P] * 3),
                ("Idempotency keys (F3),\nplain ticket", [P] * 3, [P] * 3),
                ("Idempotency keys (F3),\nnearby middleware\ntemptation", [P] * 7, [P] * 7),
            ],
            "Version checks (F4): the bare arm left the allowed paths in 3 of 3 runs,\n"
            "the harness arm in 0 of 3. Idempotency keys (F3): no measurable difference.",
        )

    # docs/evidence/s4.md, "Pilot results for F4": runs 2 and 3, class-profile round.
    @diagram(S4, "results-s4")
    def results_s4(s: Scene) -> None:
        dot_chart(
            s,
            "Section 4, version checks ticket (F4). A run passes with all 69 hidden\n"
            "tests passed and all 4 referee mutants caught. One dot per run.",
            [
                ("Medium effort,\nfirst round", [F] * 3, [F] * 3),
                ("Medium effort,\nsecond round", [F] * 3, [F] * 3),
                ("Low effort, fast tier\n(class settings)", [F], [F]),
            ],
            "Both arms failed every run: no measurable difference.",
        )

    # docs/evidence/final.md, "The pilot's dots for F1 to F4" and "The S3 confirmation".
    @diagram(DOCS, "results-final")
    def results_final(s: Scene) -> None:
        dot_chart(
            s,
            "All sections, each on its own primary measure. One dot per run:\n"
            "medium effort, low effort (not run on version checks), and class settings.",
            [
                ("Section 1, legacy\npattern (F1)", [P] * 7, [P] * 7),
                ("Section 2,\ncomments (F2)", [P] * 7, [P] * 7),
                ("Section 3, tempting\nmiddleware (F3)", [P] * 7, [P] * 7),
                ("Section 3, version checks\n(F4): allowed paths", [F] * 3, [P] * 3),
                ("Section 4, version checks\n(F4): hidden tests, mutants", [F] * 4, [F] * 4),
            ],
            "The harness arm was ahead on one measure: files outside the allowed paths\n"
            "on version checks (F4), 3 of 3 runs passed against 0 of 3.\n"
            "Elsewhere, no measurable difference.",
        )
