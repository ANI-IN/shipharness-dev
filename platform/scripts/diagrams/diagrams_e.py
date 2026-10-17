"""Round-2 diagrams for Sections 3 and 4 and the opening: failure stories, Socratic build-ups,
the feature-list lifecycle, timelines, cheat sheets, house rules, glossary, module summary."""

from __future__ import annotations

from exlib import Scene
from layouts import CENTRE, cheat_sheet, socratic, story_strip, timeline, title
from style import FONT_BODY, FONT_SMALL, FONT_TITLE, INK


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Source: slides "Problem statement: A tidy diff in a shared file" (illustrative); every bare
    # arm on version checks changed app/services/errors.py (docs/evidence/s3.md).
    @diagram(S3, "failure-story-s3")
    def failure_story_s3(s: Scene) -> None:
        story_strip(
            s,
            "A tidy diff in a shared file",
            [
                (
                    None,
                    [
                        "The ticket lists\nfiles to change",
                        "The handbook points\nto errors.py",
                        "The agent edits\nthe shared module",
                    ],
                ),
                (
                    None,
                    [
                        "Ticket tests pass,\ndiff approved",
                        "Another team changes\nthe error mapping",
                        "Wrong status,\nnobody links it",
                    ],
                ),
            ],
            note="In the pilot, every bare arm changed app/services/errors.py.",
        )

    # Source: slides "Scope: Is the ticket's file list enough?" (builds 1-2); docs/evidence/s3.md.
    @diagram(S3, "socratic-s3", steps=True)
    def socratic_s3(s: Scene) -> None:
        socratic(
            s,
            "Is the ticket's\nfile list enough?",
            "No: text is only a request",
            [
                "Nothing checks\nthe list",
                '"Less likely" is\nnot "never"',
                "The bare arm left it\nin 3 of 3 runs",
            ],
            "What can we use instead?",
            2,
        )

    # Sources: platform/src/shipharness/harness/scope/features.py, status.py, guard.py
    # (HARNESS_ONLY), layer.py; docs/evidence/s3.md (passes set at 4:30 in the captured run).
    @diagram(S3, "feature-list-lifecycle")
    def feature_list_lifecycle(s: Scene) -> None:
        title(s, "One feature at a time: feature_list.json")
        b1 = s.box(60, 150, 520, 160, "The harness writes it\npasses: false", role="harness")
        b2 = s.box(700, 150, 520, 160, "The agent reads it;\na patch is BLOCKED", role="plain")
        b3 = s.box(
            1340,
            150,
            520,
            160,
            'The agent says done\nfinish(claim="done")',
            role="accent",
            stroke_width=3,
        )
        d = s.box(1420, 440, 360, 240, "Evidence\nholds?", shape="diamond")
        b6 = s.box(
            740,
            485,
            520,
            150,
            "The harness sets\npasses: true, commits",
            role="harness",
            stroke_width=3,
        )
        b7 = s.box(60, 485, 480, 150, "Set once,\nnever again", role="harness")
        bad = s.box(1400, 820, 400, 150, "passes stays false,\nthe reason noted", role="fail")
        s.arrow(b1, b2, start="right", end="left")
        s.arrow(b2, b3, start="right", end="left")
        s.arrow(b3, d, start="bottom", end="top")
        s.text(1580, 345, "Section 3: visible tests\nSection 4: the gate", FONT_SMALL, INK, "right")
        s.arrow(d, b6, "yes", start="left", end="right")
        s.arrow(b6, b7, start="left", end="right")
        s.arrow(d, bad, "no", start="bottom", end="top")
        s.text(
            60,
            800,
            "Captured run, 2026-10-17:\nthe harness set passes at 4:30.",
            FONT_BODY,
            INK,
        )

    # Sources: docs/evidence/s3.md (the captured demo-3 A/B, run 3, alone); terminal.txt.
    @diagram(S3, "timeline-s3")
    def timeline_s3(s: Scene) -> None:
        timeline(
            s,
            "Same pull, two arms (console clock)",
            [
                (
                    "Bare arm",
                    "bare",
                    [
                        (23, "patches\nerrors.py", "fail"),
                        (222, "bare ends,\n43 turns", "plain"),
                        (315, "primary\nverdict", "plain"),
                        (486, "full\nverdict", "plain"),
                    ],
                ),
                (
                    "Harness arm",
                    "harness",
                    [
                        (76, "errors.py patch\nblocked", "harness"),
                        (270, "sets passes:\nvisible tests", "harness"),
                        (442, "ABORTED: timeout,\n39 turns", "plain"),
                        (530, "primary\nverdict", "plain"),
                        (678, "full\nverdict", "plain"),
                    ],
                ),
            ],
            690,
            "11:30",
            "captured 2026-10-17 (run 3, alone); agent limit 420 s",
        )

    @diagram(S3, "cheat-sheet-s3")
    def cheat_sheet_s3(s: Scene) -> None:
        cheat_sheet(
            s,
            "Four boundaries for one feature",
            [
                ("Feature list", "one feature;\nthe harness\nsets passes", "checklist", "harness"),
                ("Allowed paths", "patch blocked,\ncommand reverted", "fence", "harness"),
                ("Sandbox", "no network,\nkeys on the host", "globe", "harness"),
                ("Least privilege", "non-root,\ncapabilities\ndropped", "lock", "harness"),
            ],
            tags=["harness arm only", "harness arm only", "both arms", "both arms"],
        )

    # Source: slides "The problem: Done, but two edits still collide" (illustrative).
    @diagram(S4, "failure-story-s4")
    def failure_story_s4(s: Scene) -> None:
        story_strip(
            s,
            "Done, but two edits still collide",
            [
                (
                    None,
                    [
                        "Adds the If-Match\ncheck",
                        "Writes one\nhappy-path test",
                        "Runs the suite:\nall green",
                    ],
                ),
                (
                    None,
                    [
                        'Reports "done,\nsuite passes"',
                        "Review sees\ngreen CI",
                        "Two editors still\noverwrite",
                    ],
                ),
            ],
            note="If-Match is optional, and no test sends a stale one.",
        )

    # Source: slides "Verification: The suite is green. Is F4 done?" (builds 1-2);
    # docs/evidence/s4.md (68 of 69 hidden tests; test_invalid_body_with_a_stale_version_is_412).
    @diagram(S4, "socratic-s4", steps=True)
    def socratic_s4(s: Scene) -> None:
        socratic(
            s,
            "The suite is green.\nAre version checks (F4) done?",
            "No: 68 of 69 hidden tests",
            [
                "The visible suite\nmissed a case",
                "Stale If-Match plus\nan invalid body",
                "The agent graded\nits own work",
            ],
            "Who should decide done?",
            2,
        )

    # Sources: docs/evidence/s4.md (the captured show-4 run); section-4-verification/demo/
    # expected/terminal.txt (real 11m5.912s). Times from launch.
    @diagram(S4, "timeline-s4")
    def timeline_s4(s: Scene) -> None:
        timeline(
            s,
            "Eleven minutes of show-4 (harness arm)",
            [
                (
                    None,
                    "harness",
                    [
                        (55, "scope blocks\nerrors.py", "harness"),
                        (138, 'finish "done",\ngate pending', "plain"),
                        (204, "gate passes,\n190 tests", "harness"),
                        (351, "test filters: 4\nproposed, 1 kept", "plain"),
                        (514, "ABORTED: timeout,\n43 turns", "plain"),
                        (559, "primary verdict\nFAIL", "fail"),
                        (655, "hidden 68/69,\nmutants 0/4", "plain"),
                        (666, "command\nfinished", "plain"),
                    ],
                )
            ],
            666,
            "11:06",
            "captured 2026-10-17; harness arm only; agent limit then 300 s",
        )

    @diagram(S4, "cheat-sheet-s4")
    def cheat_sheet_s4(s: Scene) -> None:
        cheat_sheet(
            s,
            "Four checks the agent does not own",
            [
                ("Verify gate", "at done: tests,\nrules, clean state", "gate", "harness"),
                ("Test filters", "keep tests that\nprove something", "funnel", "harness"),
                ("Hidden tests", "run after\nthe agent stops", "vault", "harness"),
                ("Referee mutants", "would the tests\nnotice a fault?", "bug", "harness"),
            ],
            tags=["feedback to the agent", "feedback to the agent", "held out", "held out"],
        )

    # Source: platform/teamtrack/docs/HANDBOOK.md, "House rules" R1 to R7.
    @diagram(DOCS, "house-rules")
    def house_rules(s: Scene) -> None:
        title(s, "TeamTrack house rules R1 to R7")
        rules = [
            ("R1 tenant isolation", "another org's issue:\n404, never 403"),
            ("R2 roles", "a viewer's write:\n403 forbidden"),
            ("R3 API conventions", "keyset cursor lists,\none error envelope"),
            ("R4 idempotent creates", "same Idempotency-Key:\none record"),
            ("R5 audit log", "every write adds\none audit row"),
            ("R6 layering", "app/api never\nimports app/db"),
            ("R7 migrations", "exactly one\nAlembic head"),
        ]
        w, gap = 420, 40
        for i, (name, example) in enumerate(rules):
            row, col = divmod(i, 4)
            n = 4 if row == 0 else 3
            x0 = CENTRE - (n * w + (n - 1) * gap) / 2
            x = x0 + col * (w + gap)
            y = 170 + row * 420
            s.box(x, y, w, 340, role="plain", stroke="#3896D2", stroke_width=3)
            s.text(x + w / 2, y + 40, name, FONT_BODY, INK, "center")
            s.line([(x + 30, y + 110), (x + w - 30, y + 110)], color="#3896D2")
            s.text(x + w / 2, y + 160, example, FONT_BODY, INK, "center")

    # Sources: section-1/3/4 concepts.md glossaries; docs/STYLE.md; instructor/run-sheet.md.
    @diagram(DOCS, "glossary-terms")
    def glossary_terms(s: Scene) -> None:
        title(s, "Eight words we use all session")
        terms = [
            ("Arm", "one run: bare\nor harness"),
            ("Referee", "scores runs after\nthe agents stop"),
            ("Primary measure", "one result,\nchosen first"),
            ("Hidden tests", "tests the agent\nnever sees"),
            ("Mutant", "code with one\nplanted fault"),
            ("Allowed paths", "files it may\nchange in a phase"),
            ("Gate", "checks the\ndone claim"),
            ("Harness in action", "one harness arm,\nnot an A/B"),
        ]
        w, gap = 420, 40
        for i, (term, line) in enumerate(terms):
            row, col = divmod(i, 4)
            x = 60 + col * (w + gap)
            y = 160 + row * 420
            s.box(x, y, w, 360, role="plain", stroke="#3896D2", stroke_width=3)
            s.text(x + w / 2, y + 40, term, FONT_TITLE, INK, "center")
            s.line([(x + 30, y + 115), (x + w - 30, y + 115)], color="#3896D2")
            s.text(x + w / 2, y + 160, line, FONT_BODY, INK, "center")

    # Sources: the four concepts.md pages; docs/evidence/final.md (the registered result).
    @diagram(DOCS, "module-summary")
    def module_summary(s: Scene) -> None:
        title(s, "Module 1 in one picture")
        layers = [
            ("Instructions", "a map,\nnot a manual"),
            ("State", "a handoff\nsurvives a stop"),
            ("Scope", "code checks\nallowed paths"),
            ("Verification", "the agent never\ngrades itself"),
        ]
        w, gap = 405, 60
        for i, (name, line) in enumerate(layers):
            x = 60 + i * (w + gap)
            s.box(x, 160, w, 360, role="harness", stroke_width=3)
            s.text(x + 28, 180, str(i + 1), FONT_TITLE, INK)
            s.text(x + w / 2, 250, name, FONT_TITLE, INK, "center")
            s.text(x + w / 2, 360, line, FONT_BODY, INK, "center")
        s.box(
            60,
            620,
            870,
            300,
            "Measured: one gap\nscope, version checks (F4)\nharness 3 of 3, bare 0 of 3",
            role="accent",
            stroke_width=3,
        )
        s.box(
            990,
            620,
            870,
            300,
            "Everywhere else:\nno measurable difference",
            role="neutral",
        )
