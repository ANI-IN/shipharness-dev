"""Round-2 diagrams for Sections 3 and 4 and the opening: failure stories, Socratic build-ups,
the feature-list lifecycle, timelines, cheat sheets, house rules, glossary, module summary."""

from __future__ import annotations

from exlib import Scene
from layouts import CENTRE, cheat_sheet, socratic, story_strip, timeline, title
from style import FONT_BODY, FONT_TITLE, INK

from shipharness.datasets.names import RULE_NAMES


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
                        "The ticket lists\nfiles",
                        "The handbook points\nto errors.py",
                        "Agent edits the\nshared module",
                    ],
                ),
                (
                    None,
                    [
                        "Ticket tests pass,\ndiff approved",
                        "Another team changes\nthe mapping",
                        "Wrong status,\nnobody links it",
                    ],
                ),
            ],
            note="pilot: every bare arm changed errors.py",
        )

    # Source: slides "Scope: Is the ticket's file list enough?" (builds 1-2); docs/evidence/s3.md.
    @diagram(S3, "socratic-s3", steps=True)
    def socratic_s3(s: Scene) -> None:
        socratic(
            s,
            "Is the file\nlist enough?",
            "No: text is a request",
            [
                "Nothing checks\nthe list",
                '"Less likely" is\nnot "never"',
                "Bare arm left\nit: 3/3",
            ],
            "What can we use instead?",
            2,
        )

    # Sources: platform/src/shipharness/harness/scope/features.py, status.py (passes, evidence,
    # testedAt; evidence from the visible tests or the gate), guard.py (HARNESS_ONLY), layer.py;
    # docs/evidence/s3.md (passes set at 4:30 in the captured run).
    @diagram(S3, "feature-list-lifecycle", canvas="strip")
    def feature_list_lifecycle(s: Scene) -> None:
        w, gap, y = 390, 80, 100
        xs = [60 + i * (w + gap) for i in range(4)]
        b1 = s.box(xs[0], y, w, 170, "Harness writes\npasses: false", role="harness")
        b2 = s.box(xs[1], y, w, 170, "Agent reads;\npatch BLOCKED", role="plain")
        b3 = s.box(
            xs[2], y, w, 170, 'Agent says done\nfinish(claim="done")', role="accent", stroke_width=3
        )
        test = s.box(xs[3], y, w, 170, "Harness checks:\nvisible tests, gate", role="harness")
        ok = s.box(
            xs[3], 450, w, 170, "passes: true,\nevidence, testedAt", role="harness", stroke_width=3
        )
        bad = s.box(xs[2], 450, w, 170, "passes\nstays false", role="fail")
        s.arrow(b1, b2, start="right", end="left")
        s.arrow(b2, b3, start="right", end="left")
        s.arrow(b3, test, start="right", end="left")
        s.arrow(test, ok, "pass", start="bottom", end="top")
        s.arrow(test, bad, "fail", start="bottom", end="top", start_off=-150, end_off=120)
        s.text(xs[0], 510, "Captured run: set at 4:30", FONT_BODY, INK)

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
                        (270, "sets passes", "harness"),
                        (442, "timeout,\n39 turns", "plain"),
                        (530, "primary\nverdict", "plain"),
                        (678, "full\nverdict", "plain"),
                    ],
                ),
            ],
            690,
            "11:30",
            "captured 2026-10-17, run 3; limit 420 s",
        )

    @diagram(S3, "cheat-sheet-s3")
    def cheat_sheet_s3(s: Scene) -> None:
        cheat_sheet(
            s,
            "Four boundaries for one feature",
            [
                ("Feature list", "one feature;\nharness sets passes", "checklist", "harness"),
                ("Allowed paths", "patch blocked,\ncommand reverted", "fence", "harness"),
                ("Sandbox", "no network,\nkeys on host", "globe", "harness"),
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
                        "Adds the\nIf-Match check",
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
            note="If-Match is optional; no test sends one",
        )

    # Source: slides "Verification: The suite is green. Is it done?" (builds 1-2);
    # docs/evidence/s4.md (68 of 69 hidden tests; test_invalid_body_with_a_stale_version_is_412).
    @diagram(S4, "socratic-s4", steps=True)
    def socratic_s4(s: Scene) -> None:
        socratic(
            s,
            "Green suite:\nis it done?",
            "No: 68/69 hidden tests",
            [
                "Visible suite\nmissed a case",
                "Stale If-Match\nplus bad body",
                "The agent\ngraded itself",
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
                        (351, "filters\nkeep 1/4", "plain"),
                        (514, "timeout,\n43 turns", "plain"),
                        (559, "primary verdict\nFAIL", "fail"),
                        (655, "hidden 68/69,\nmutants 0/4", "plain"),
                        (666, "command\nfinished", "plain"),
                    ],
                )
            ],
            666,
            "11:06",
            "captured 2026-10-17; harness only; limit 300 s",
        )

    @diagram(S4, "cheat-sheet-s4")
    def cheat_sheet_s4(s: Scene) -> None:
        cheat_sheet(
            s,
            "Four checks the agent does not own",
            [
                ("Verify gate", "at done:\ntests, rules", "gate", "harness"),
                ("Test filters", "keep tests that\nprove something", "funnel", "harness"),
                ("Hidden tests", "run after\nthe agent stops", "vault", "harness"),
                ("Referee mutants", "would tests\nnotice faults?", "bug", "harness"),
            ],
            tags=["feedback to the agent", "feedback to the agent", "held out", "held out"],
        )

    # Source: platform/teamtrack/docs/HANDBOOK.md, "House rules", House rules 1 to 7.
    @diagram(DOCS, "house-rules")
    def house_rules(s: Scene) -> None:
        title(s, "TeamTrack's seven house rules")
        examples = [
            "other org:\n404, not 403",
            "a viewer's write:\n403 forbidden",
            "cursor lists,\nerror envelope",
            "same Idempotency-Key:\none record",
            "one audit row\nper write",
            "app/api never\nimports app/db",
            "exactly one\nAlembic head",
        ]
        w, gap = 420, 40
        for i, example in enumerate(examples):
            row, col = divmod(i, 4)
            n = 4 if row == 0 else 3
            x0 = CENTRE - (n * w + (n - 1) * gap) / 2
            x = x0 + col * (w + gap)
            y = 170 + row * 420
            name = f"House rule {i + 1}:\n{RULE_NAMES[f'R{i + 1}']}"
            s.box(x, y, w, 340, role="plain", stroke="#3896D2", stroke_width=3)
            s.text(x + w / 2, y + 26, name, FONT_BODY, INK, "center")
            s.line([(x + 30, y + 122), (x + w - 30, y + 122)], color="#3896D2")
            s.text(x + w / 2, y + 168, example, FONT_BODY, INK, "center")

    # Sources: section-1/3/4 concepts.md glossaries; docs/STYLE.md; instructor/run-sheet.md.
    @diagram(DOCS, "glossary-terms")
    def glossary_terms(s: Scene) -> None:
        title(s, "Eight words we use all session")
        terms = [
            ("Arm", "one run: bare\nor harness"),
            ("Referee", "scores runs after\nagents stop"),
            ("Primary measure", "one result,\nchosen first"),
            ("Hidden tests", "tests the agent\nnever sees"),
            ("Mutant", "code with one\nplanted fault"),
            ("Allowed paths", "files changeable\nper phase"),
            ("Gate", "checks the\ndone claim"),
            ("Harness in action", "one harness arm,\nno A/B"),
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

    # Sources: the four concepts.md pages; docs/evidence/final.md (the registered result);
    # slides "Module 1 Summary" speaker notes (takeaways 1-5).
    @diagram(DOCS, "module-summary", canvas="strip")
    def module_summary(s: Scene) -> None:
        layers = [
            ("Instructions", "a map,\nnot a manual", "no measurable\ndifference", "harness"),
            ("State", "a handoff\nsurvives a stop", "no measurable\ndifference", "harness"),
            ("Scope", "code checks\nallowed paths", "harness 3/3,\nbare 0/3", "accent"),
            ("Verification", "the agent never\ngrades itself", "no measurable\ndifference", "harness"),
        ]
        w, gap, y, h = 405, 60, 60, 340
        boxes = []
        for i, (name, line, result, role) in enumerate(layers):
            x = 60 + i * (w + gap)
            boxes.append(s.box(x, y, w, h, role=role, stroke_width=3))
            s.text(x + 28, y + 22, str(i + 1), FONT_TITLE, INK)
            s.text(x + w / 2, y + 22, name, FONT_TITLE, INK, "center")
            s.text(x + w / 2, y + 95, line, FONT_BODY, INK, "center")
            s.line([(x + 30, y + 200), (x + w - 30, y + 200)])
            s.text(x + w / 2, y + 230, result, FONT_BODY, INK, "center")
        last = s.box(
            60, 500, 1800, 110, "5: measure before you keep", role="plain", stroke_width=3, size=FONT_TITLE
        )
        for b in boxes:
            s.arrow(b, last, start="bottom", end="top", end_off=b["x"] + w / 2 - 960)
