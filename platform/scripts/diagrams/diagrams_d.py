"""Round-2 diagrams for Sections 1 and 2: failure story, Socratic build-up, the idea diagram,
the captured-run timeline, and the cheat sheet."""

from __future__ import annotations

from exlib import Scene
from layouts import cheat_sheet, socratic, story_strip, timeline, title
from style import FONT_SMALL


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Source: slides/module1-slides.md, "Failure story: The search that showed another org"
    # (illustrative; list_all_legacy is real code in platform/teamtrack/app/repositories/issues.py).
    @diagram(S1, "failure-story-s1")
    def failure_story_s1(s: Scene) -> None:
        story_strip(
            s,
            "The search that showed another org",
            [
                (
                    None,
                    [
                        "Ticket: org-wide\nissue search",
                        "Agent finds\nlist_all_legacy",
                        "Copies it: short,\npaginates",
                    ],
                ),
                (
                    None,
                    [
                        "One-org tests pass",
                        "Review approves:\nlooks familiar",
                        "Acme sees\nGlobex issues",
                    ],
                ),
            ],
            note="The copied query has no org_id filter.",
        )

    # Source: slides "Instructions: Why not paste every rule?" (builds 1-3); the 899-line file is
    # section-1-instructions/assignment/starter/original/AGENTS.md.
    @diagram(S1, "socratic-s1", steps=True)
    def socratic_s1(s: Scene) -> None:
        socratic(
            s,
            "Paste every rule\ninto the prompt?",
            "No: not the main mechanism",
            [
                "Crowds out task and code\n(899 lines, every task)",
                "Too much guidance is none\n(tenant rule at line 204)",
                "Goes stale, nothing checks\n(four retired rules inside)",
            ],
            "What can we use instead?",
            3,
        )

    # Sources: slides "4) Mechanical checks keep the map true"; docs/evidence/s1.md (the
    # reference checker's OK line); section-1-instructions/assignment (check_docs.py).
    @diagram(S1, "checker-flow")
    def checker_flow(s: Scene) -> None:
        title(s, "Mechanical checks keep the map true")
        docs = s.box(60, 430, 360, 170, "AGENTS.md map,\ndocs, skills", role="neutral")
        c1 = s.box(
            560,
            170,
            560,
            170,
            "check_docs.py\nlinks, rule coverage,\nno retired rules",
            role="harness",
        )
        c2 = s.box(560, 430, 560, 170, "skills validate\nskill frontmatter", role="harness")
        c3 = s.box(560, 690, 560, 170, "test_parity.py\nrules still in handbook", role="harness")
        d = s.box(1210, 400, 280, 230, "All\npass?", shape="diamond")
        ok = s.box(
            1560,
            170,
            300,
            200,
            "OK: 13 files,\n147 links,\n66 rules",
            role="harness",
            stroke_width=3,
        )
        bad = s.box(1560, 690, 300, 170, "ERROR:\nbroken link", role="fail", stroke_width=3)
        for c in (c1, c2, c3):
            s.arrow(docs, c, start="right", end="left")
            s.arrow(c, d, start="right", end="left")
        s.arrow(d, ok, "yes", start="top", end="left", via=[(1350, 270)])
        s.arrow(d, bad, "no", start="bottom", end="left", via=[(1350, 775)])
        s.arrow(
            bad,
            docs,
            "fix in the same PR",
            start="bottom",
            end="bottom",
            via=[(1710, 960), (240, 960)],
        )
        s.text(
            240, 330, "you write check_docs.py\nin Assignment 1", FONT_SMALL, "#212121", "center"
        )

    # Sources: docs/evidence/s1.md (the show-1 capture, run ab-20261017-112101-c5d839);
    # section-1-instructions/demo/expected/terminal.txt (real 10m14s).
    @diagram(S1, "timeline-s1")
    def timeline_s1(s: Scene) -> None:
        timeline(
            s,
            "One run, minute by minute (harness arm)",
            [
                (
                    None,
                    "harness",
                    [
                        (60, "map and skill read,\nfirst patches", "plain"),
                        (180, "test phase runs\nits own test", "plain"),
                        (233, "run ends,\n35 turns", "plain"),
                        (251, "primary verdict\nPASS", "harness"),
                        (600, "full verdict: hidden\n52/52, mutants 2/4", "plain"),
                        (614, "command\nfinished", "plain"),
                    ],
                )
            ],
            614,
            "10:14",
            "captured 2026-10-17; agent limit then 300 s",
        )

    @diagram(S1, "cheat-sheet-s1")
    def cheat_sheet_s1(s: Scene) -> None:
        cheat_sheet(
            s,
            "The instructions layer in four moves",
            [
                ("A map", "a short file\nthat points\nto the docs", "map", "harness"),
                ("Disclosure", "skill names first,\nbodies later", "stack", "harness"),
                ("The prefix", "fixed, read-only,\nat session start", "lock", "harness"),
                ("Checks", "links and rule\ncoverage,\nchecked by code", "check", "harness"),
            ],
            note="It informs. It never blocks.",
        )

    # Source: slides "Problem statement: The second session redoes the first" (illustrative).
    @diagram(S2, "failure-story-s2")
    def failure_story_s2(s: Scene) -> None:
        story_strip(
            s,
            "The second session redoes the first",
            [
                (
                    "Session 1 stops at its turn limit",
                    [
                        "Migration for\nthe comments table",
                        "Half an endpoint,\nnever committed",
                        "No note for\nthe next session",
                    ],
                ),
                (
                    "Session 2 starts with an empty context",
                    [
                        "A second migration\nfrom the old head",
                        "Two Alembic heads\nblock the deploy",
                        "The team\npays twice",
                    ],
                ),
            ],
        )

    # Source: slides "Fresh session: Why redo work already on disk?" (builds 1-3).
    @diagram(S2, "socratic-s2", steps=True)
    def socratic_s2(s: Scene) -> None:
        socratic(
            s,
            "Carry the old context over?",
            "Not on its own",
            [
                "Compaction keeps a\nsqueezed copy",
                "The repo holds it,\nbut nobody reads it",
            ],
            "What can we use instead?",
            3,
        )

    # Sources: slides "3) The exec plan and the progress ledger"; section-2-state-lifecycle/
    # demo/walkthrough.md (harness/state/layer.py, lifecycle.py); demo/harness/progress.md.
    @diagram(S2, "exec-plan-ledger")
    def exec_plan_ledger(s: Scene) -> None:
        title(s, "The exec plan and the progress ledger")
        init = s.box(60, 470, 380, 170, "Initializer step\n(harness code)", role="harness")
        plan = s.box(
            680,
            160,
            480,
            190,
            "Exec plan\ndocs/exec-plans/\nactive/F2.md",
            role="plain",
            stroke_width=3,
        )
        prog = s.box(
            680,
            760,
            520,
            190,
            "progress.md\ndone, in progress,\nnext",
            role="plain",
            stroke_width=3,
        )
        agent = s.box(740, 470, 400, 170, "The agent\nworks, then wraps up", role="neutral")
        done = s.box(
            1440, 160, 420, 190, "Feature passes:\nplan moves to\ncompleted/", role="harness"
        )
        nxt = s.box(1440, 470, 420, 170, "Next session\nreads both first", role="plain")
        stop = s.box(1440, 780, 420, 150, "Session stop\n(harness)", role="harness")
        s.arrow(init, plan, "template", start="top", end="left", via=[(250, 255)])
        s.arrow(init, prog, "template", start="bottom", end="left", via=[(250, 855)])
        s.arrow(agent, plan, "decisions", start="top", end="bottom")
        s.arrow(agent, prog, "wrap-up edits", start="bottom", end="top")
        s.arrow(plan, done, "harness moves it", start="right", end="left")
        s.arrow(plan, nxt, start="right", end="left", start_off=60, end_off=-40)
        s.arrow(prog, nxt, "read first", start="right", end="left", start_off=-60, end_off=40)
        s.arrow(stop, prog, "appends", start="left", end="right", end_off=50)

    # Sources: docs/evidence/s2.md (the show-2 capture, run ab-20261017-113213-fe89a3);
    # section-2-state-lifecycle/demo/expected/terminal.txt (real 10m7s).
    @diagram(S2, "timeline-s2")
    def timeline_s2(s: Scene) -> None:
        timeline(
            s,
            "One run, two sessions (harness arm)",
            [
                (
                    None,
                    "harness",
                    [
                        (0, "initializer writes\nfour files", "plain"),
                        (83, "session 1 stops,\nhandoff committed", "harness"),
                        (396, "run ends: time\nlimit, 43 turns", "plain"),
                        (406, "primary verdict\nPASS", "harness"),
                        (592, "full verdict: hidden\n56/56, mutants 0/4", "plain"),
                        (607, "command\nfinished", "plain"),
                    ],
                )
            ],
            607,
            "10:07",
            "captured 2026-10-17; agent limit then 300 s; sessions of 12 and 31 turns",
            bars=[(0, 83, "session 1"), (83, 396, "session 2")],
        )

    @diagram(S2, "cheat-sheet-s2")
    def cheat_sheet_s2(s: Scene) -> None:
        cheat_sheet(
            s,
            "Four state pieces across a stop",
            [
                ("init.sh", "setup plus\na basic test", "terminal", "harness"),
                ("progress.md", "done and next,\nper session", "list", "harness"),
                ("Exec plan", "plan, decisions,\nrestart bar", "document", "harness"),
                ("Handoff", "harness facts,\nagent notes", "twoband", "harness"),
            ],
            tags=["by the harness", "by both", "by the agent", "two owners"],
        )
