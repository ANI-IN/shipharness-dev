"""Single diagrams: mappings, the data model, and one picture per mechanism.

Coordinates are canvas units of a "wide" canvas (1920x1080); style comes from style.py.
"""

from __future__ import annotations

from exlib import AMBER, BLUE, GREY, INK, Scene
from style import FONT_BODY as B
from style import FONT_SMALL
from style import FONT_TITLE as T
from style import STROKE_WIDTH_BOLD as BOLD


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Source: docs/STYLE.md (the four failures), the four concepts.md pages (the causes).
    @diagram(DOCS, "stories-causes-layers")
    def stories_causes_layers(s: Scene) -> None:
        stories = [
            "Agent copies a tenant\nleak from legacy code",
            "A migration is rewritten\nacross sessions",
            "Out-of-scope edits\nbreak old features",
            "Agent says done\nwhen it is not",
        ]
        causes = [
            "The rule is on disk,\nnot in its context",
            "Each new session starts\nwith no memory",
            "The file list is written\ndown, but nothing checks it",
            "It grades its own work;\nvisible tests are not\nthe feature",
        ]
        layers = [
            "Instructions\nSection 1",
            "State and lifecycle\nSection 2",
            "Scope and sandbox\nSection 3",
            "Verification\nSection 4",
        ]
        s.text(320, 60, "Story", T, INK, "center")
        s.text(980, 60, "Cause", T, INK, "center")
        s.text(1590, 60, "Layer", T, INK, "center")
        for i in range(4):
            y = 140 + i * 215
            a = s.box(60, y, 520, 180, stories[i], role="plain")
            b = s.box(700, y, 560, 180, causes[i], role="neutral")
            c = s.box(1380, y, 420, 180, layers[i], role="harness")
            s.arrow(a, b, start="right", end="left")
            s.arrow(b, c, start="right", end="left", color=BLUE)

    # Source: platform/teamtrack/app/db/models.py (orgs, users, projects, project_members,
    # issues, audit_log, idempotency_keys); platform/teamtrack/reference/f2, f6, f7 patches
    # (comments, watchers, labels, issue_labels).
    @diagram(DOCS, "teamtrack-data-model")
    def teamtrack_data_model(s: Scene) -> None:
        orgs = s.box(760, 40, 400, 110, "orgs\nid, name, slug", role="neutral")
        s.box(60, 190, 1800, 760, dashed=True, stroke=AMBER, stroke_width=BOLD)
        users = s.box(120, 250, 460, 120, "users\norg_id, email, role", role="plain")
        projects = s.box(730, 250, 460, 120, "projects\norg_id, key, archived_at", role="plain")
        labels = s.box(1340, 250, 460, 120, "labels (F7)\norg_id, name", role="plain")
        members = s.box(120, 470, 460, 120, "project_members\nproject_id, user_id", role="plain")
        issues = s.box(
            730,
            440,
            460,
            180,
            "issues\norg_id, project_id,\nassignee_id, created_by,\nversion",
            role="plain",
            stroke_width=BOLD,
        )
        issue_labels = s.box(
            1340, 470, 460, 120, "issue_labels (F7)\nissue_id, label_id", role="plain"
        )
        comments = s.box(
            300, 690, 560, 120, "comments (F2)\norg_id, issue_id, author_id", role="plain"
        )
        watchers = s.box(
            1060, 690, 560, 120, "watchers (F6)\norg_id, issue_id, user_id", role="plain"
        )
        s.text(
            100,
            835,
            "Tenant boundary: every row in here carries org_id.\n"
            "Another org's row answers 404, never 403\n(R1 tenant isolation).",
            B,
            INK,
        )
        s.text(1820, 865, "Also scoped by org_id:\naudit_log, idempotency_keys", B, INK, "right")
        s.arrow(orgs, users, start="bottom", end="top", via=[(350, 200)])
        s.arrow(orgs, projects, start="bottom", end="top")
        s.arrow(orgs, labels, start="bottom", end="top", via=[(1570, 200)])
        s.arrow(users, members, start="bottom", end="top")
        s.arrow(projects, members, start="left", end="right", via=[(655, 310), (655, 530)])
        s.arrow(projects, issues, start="bottom", end="top")
        s.arrow(issues, comments, start="bottom", end="top", start_off=-80)
        s.arrow(issues, watchers, start="bottom", end="top", start_off=80)
        s.arrow(issues, issue_labels, start="right", end="left")
        s.arrow(labels, issue_labels, start="bottom", end="top")
        s.text(
            960,
            975,
            "Arrow: one row has many rows. Tables marked (F2), (F6), (F7)\n"
            "come from the comments, watchers, and labels tickets.",
            B,
            INK,
            "center",
        )

    # Sources: section-1-instructions/assignment/starter/original/AGENTS.md (899 lines; heading
    # lines from section-1-instructions/concepts.md); platform/teamtrack/harness/instructions/
    # AGENTS.md (94 lines, the "Where to look" rows); OpenAI quote from concepts.md.
    @diagram(S1, "manual-vs-map")
    def manual_vs_map(s: Scene) -> None:
        top, height = 120, 760
        s.text(60, 60, "Before: one 899-line AGENTS.md", B, INK)
        s.box(60, top, 660, height, role="neutral")
        rows = [
            (1, "1  AGENTS.md: TeamTrack (read all ...)", INK),
            (196, "196  House rules R1 to R7\n       (tenant rule at line 204)", AMBER),
            (586, "586  The legacy /v1 API", AMBER),
            (669, "669  Team notes and history", INK),
            (787, "787  Questions we keep getting", INK),
        ]
        for line, label, color in rows:
            y = top + 14 + (line - 1) / 899 * (height - 90)
            s.text(80, y, label, B, INK)
            if color == AMBER:
                hy = y + 37 * (label.count("\n") + 1)
                s.line([(70, hy), (710, hy)], color=AMBER, stroke_width=4)
        s.text(390, top + height + 16, "Four retired rules are still in it.", B, INK, "center")
        s.text(800, 60, "After: a 94-line map", B, INK)
        map_h = round(height * 94 / 899)
        amap = s.box(800, top, 380, map_h, "AGENTS.md map", role="harness", stroke_width=BOLD)
        s.text(
            990,
            top + map_h + 16,
            "in every session's\ncontext; drawn to\nscale: 94 of 899 lines",
            B,
            INK,
            "center",
        )
        docs = [
            ".agents/skills/add-endpoint/SKILL.md\nadd or change an endpoint",
            "ARCHITECTURE.md\ntouch a router, service, or model",
            "docs/SECURITY.md\ndecide who may see or change data",
            "docs/design-docs/api-conventions.md\nshape a list, an error, a status",
            "docs/RELIABILITY.md\nwrites, idempotency, migrations",
        ]
        for i, label in enumerate(docs):
            d = s.box(1260, top + i * 146, 600, 116, label, role="plain")
            s.arrow(amap, d, start="right", end="left", start_off=(i - 2) * 6)
        s.text(1560, top + 736, "On disk: opened only when\nthe task needs it", B, INK, "center")
        s.text(
            960,
            top + height + 80,
            '"give Codex a map, not a 1,000-page instruction manual."\n'
            "(OpenAI, Harness engineering)",
            B,
            INK,
            "center",
        )

    # Sources: platform/src/shipharness/runner/skills_loader.py (catalogue line format);
    # platform/teamtrack/harness/instructions/.agents/skills/add-endpoint/ (SKILL.md 100 lines,
    # references/tests.md 57 lines); concepts.md tier table; docs/evidence/s1.md (what each arm
    # read).
    @diagram(S1, "skills-three-tiers")
    def skills_three_tiers(s: Scene) -> None:
        t1 = s.box(
            60,
            60,
            1300,
            230,
            "Tier 1: the catalogue line, always in the context\n"
            "- add-endpoint: Add or change a TeamTrack HTTP\n"
            "  endpoint so it follows house rules R1-R7 ...\n"
            "  (read .agents/skills/add-endpoint/SKILL.md to use it)",
            role="harness",
            align="left",
        )
        t2 = s.box(
            60,
            420,
            1300,
            140,
            "Tier 2: SKILL.md, 100 lines\nloaded when the agent decides to use the skill",
            role="plain",
            stroke=BLUE,
            align="left",
        )
        t3 = s.box(
            60,
            740,
            1300,
            140,
            "Tier 3: references/tests.md, 57 lines\nopened only when a step points to it",
            role="plain",
            stroke=BLUE,
            dashed=True,
            align="left",
        )
        s.arrow(t1, t2, "the task matches the description", start="bottom", end="top", color=BLUE)
        s.arrow(t2, t3, "a step needs it", start="bottom", end="top", color=BLUE)
        s.box(
            1440,
            390,
            420,
            200,
            "One round of test runs:\nall 3 harness arms read\ntier 2; none opened tier 3",
            role="accent",
        )

    # Sources: runner/loop.py base_items (developer message = core prompt + layer blocks, then
    # the user message); harness/base.py LAYER_ORDER; runner/prompts.py; instructions/router.py;
    # state/lifecycle.py; scope/layer.py; verify/layer.py.
    @diagram(S1, "context-prefix")
    def context_prefix(s: Scene) -> None:
        s.box(60, 60, 1300, 800, dashed=True)
        s.text(90, 76, "Developer message: the same text at the start of every session", B, INK)
        blocks = [
            (
                "1  Core prompt: the tools, how to call finish\n"
                "    (both arms; the bare arm gets only this block)",
                "neutral",
            ),
            ("2  Instructions: the AGENTS.md map,\n    then the skills catalogue", "harness"),
            (
                "3  State: Getting up to speed\n    (progress.md, git log, session-handoff.md)",
                "harness",
            ),
            (
                "4  Scope: the one feature and\n    the files you may change in each phase",
                "harness",
            ),
            ("5  Verification: what the gate checks\n    when you claim done", "harness"),
        ]
        prev = None
        for i, (label, role) in enumerate(blocks):
            b = s.box(100, 136 + i * 142, 1220, 112, label, role=role, align="left")
            if prev is not None:
                s.arrow(prev, b, start="bottom", end="top", gap=4)
            prev = b
        s.box(
            60,
            900,
            1300,
            120,
            "User message: the phase and the ticket. A later session also gets:\n"
            '"A previous session worked on this ticket and was stopped."',
            role="plain",
            align="left",
        )
        s.text(1420, 120, "Read in this order,\nfirst to last.", B, INK)
        s.text(
            1420,
            330,
            "Each section adds\nits layer's block.\nThe full harness\nsends all five.",
            B,
            INK,
        )
        s.text(1420, 600, "Documents and\nskill bodies stay\non disk.", B, INK)

    # Sources: platform/src/shipharness/harness/state/handoff.py (MachineSummary.render, the two
    # headings, merge); state/lifecycle.py (wrap-up text: what the notes hold).
    @diagram(S2, "handoff-contents")
    def handoff_contents(s: Scene) -> None:
        s.box(560, 50, 800, 930, role="neutral")
        s.text(960, 66, "session-handoff.md", T, INK, "center")
        mach = s.box(
            590,
            130,
            740,
            480,
            "## Machine summary\n"
            "Written by the harness at the end\n"
            "of session N (phase, what ended it, turns)\n"
            "- Commits: start, end\n- Files changed in this session\n"
            "- Visible tests\n- Last commits\n- Open TODO markers\n"
            "- Migration heads\n- Harness documents read so far",
            role="harness",
            align="left",
        )
        notes = s.box(
            590,
            640,
            740,
            310,
            "## Notes from the agent\n- What it was doing\n- What is left\n"
            "- What to watch out for\n- House rules and file locations\n"
            "  that matter for this ticket",
            role="plain",
            align="left",
        )
        harness = s.box(
            60,
            270,
            380,
            190,
            "The harness, at the stop\nfacts read from\nthe repository",
            role="harness",
        )
        agent = s.box(60, 720, 380, 150, "The agent, in\nits wrap-up turns", role="plain")
        s.arrow(harness, mach, "writes", start="right", end="left", color=BLUE)
        s.arrow(agent, notes, "writes", start="right", end="left")
        nxt = s.box(1500, 450, 360, 160, "The next session\nreads it first", role="plain")
        s.arrow(mach, nxt, start="right", end="left", end_off=-30, color=BLUE)
        s.arrow(notes, nxt, start="right", end="left", end_off=30)
        s.text(
            960,
            995,
            "The harness rewrites only its part; the notes stay as written.",
            B,
            INK,
            "center",
        )

    # Sources: platform/teamtrack/migrations/versions/0001_initial.py; docs/evidence/s2.md
    # (0002_comments.py); harness/state/handoff.py ("house rule R7 needs exactly one");
    # concepts.md (R7).
    @diagram(S2, "alembic-heads")
    def alembic_heads(s: Scene) -> None:
        s.text(310, 60, "One head", T, INK, "center")
        a0 = s.box(110, 140, 400, 110, "0001_initial", role="plain")
        a1 = s.box(110, 420, 400, 120, "0002_comments\n(session 1)", role="harness")
        s.arrow(a0, a1, "down_revision", start="bottom", end="top")
        s.box(80, 680, 460, 140, "1 head: house rule\nR7 migrations holds", role="neutral")
        s.line([(660, 40), (660, 860)], dashed=True, color=GREY)
        s.text(1310, 60, "Two heads", T, INK, "center")
        b0 = s.box(1110, 140, 400, 110, "0001_initial", role="plain")
        b1 = s.box(760, 420, 440, 120, "0002_comments\n(session 1)", role="harness")
        b2 = s.box(1420, 420, 440, 120, "a second comments\nmigration (session 2)", role="accent")
        s.arrow(b0, b1, start="bottom", end="top", start_off=-80)
        s.arrow(b0, b2, start="bottom", end="top", start_off=80)
        s.text(1310, 570, "both: down_revision = 0001_initial", B, INK, "center")
        s.box(
            990,
            680,
            640,
            140,
            "2 heads: house rule\nR7 migrations needs one",
            role="fail",
            stroke_width=BOLD,
        )

    # Sources: harness/scope/guard.py (HARNESS_ONLY, STATE_FILES, the reason text);
    # harness/scope/layer.py (block before a patch, revert after a command);
    # docs/evidence/s3.md (the blocked file).
    @diagram(S3, "scope-check-flow")
    def scope_check_flow(s: Scene) -> None:
        call = s.box(60, 95, 360, 130, "Tool call: apply_patch\nchanges a path", role="plain")
        d1 = s.box(500, 60, 580, 200, "feature_list.json?", shape="diamond")
        b1 = s.box(1200, 95, 660, 130, "BLOCKED\nwritten only by the harness", role="fail")
        d2 = s.box(530, 346, 520, 230, "In this phase's\nallowed paths?", shape="diamond")
        ok = s.box(1200, 395, 660, 120, "Allowed: the patch applies", role="harness")
        b2 = s.box(
            420,
            660,
            740,
            180,
            "BLOCKED: app/services/errors.py\nis outside the allowed paths\n"
            "for the build phase (...)\nNothing is written.",
            role="fail",
        )
        s.arrow(call, d1, start="right", end="left")
        s.arrow(d1, b1, "yes", start="right", end="left")
        s.arrow(d1, d2, "no", start="bottom", end="top")
        s.arrow(d2, ok, "yes", start="right", end="left")
        s.arrow(d2, b2, "no", start="bottom", end="top")
        s.text(
            1240,
            650,
            "progress.md, session-handoff.md,\nand docs/exec-plans/** count as\n"
            "allowed when the state layer is on.",
            B,
            INK,
        )
        run = s.box(60, 890, 360, 120, "Tool call: run\na shell command", role="plain")
        ran = s.box(520, 890, 400, 120, "The command runs\nin the sandbox", role="plain")
        rev = s.box(
            1080,
            870,
            780,
            160,
            "Changes outside the allowed paths\nare restored from a snapshot:\nREVERTED",
            role="fail",
        )
        s.arrow(run, ran, start="right", end="left")
        s.arrow(ran, rev, "then", start="right", end="left")

    # Sources: platform/sandbox/README.md; platform/src/shipharness/sandbox/policy.py;
    # section-3-scope-sandbox/concepts.md (the flags table); .env.example (OPENAI_MODEL).
    @diagram(S3, "sandbox-boundary")
    def sandbox_boundary(s: Scene) -> None:
        s.box(60, 100, 1360, 860, role="plain")
        s.text(90, 116, "Host: your machine", B, INK)
        loop = s.box(100, 200, 340, 140, "Agent loop\n(the runner)", role="plain")
        s.box(
            100,
            430,
            340,
            140,
            "API keys\nstay here, in .env",
            role="accent",
            stroke_width=BOLD,
        )
        s.box(100, 660, 340, 110, "LangSmith tracing", role="plain")
        s.box(700, 170, 640, 760, role="neutral", stroke_width=BOLD)
        s.text(1020, 186, "Sandbox container, one per arm", B, INK, "center")
        items = [
            "/work: the arm's workspace\n(writable)",
            "/tmp writable;\nthe root is read-only",
            "user 1000:1000,\nall capabilities dropped",
            "limits: CPUs, 1024 MB,\n256 processes, time",
            "network: none\n(loopback only)",
        ]
        boxes = []
        for i, label in enumerate(items):
            boxes.append(
                s.box(
                    740,
                    250 + i * 134,
                    560,
                    110,
                    label,
                    role="fail" if i == 4 else "plain",
                )
            )
        s.arrow(loop, boxes[0], "tool commands\nonly", start="right", end="left")
        api = s.box(1520, 130, 340, 180, "Model API", shape="ellipse", role="plain")
        s.arrow(
            loop,
            api,
            "the model calls go out from the host",
            start="top",
            end="top",
            start_off=110,
            via=[(380, 40), (1690, 40)],
        )
        net = s.box(1520, 790, 340, 120, "The internet", dashed=True)
        s.arrow(boxes[4], net, "blocked", start="right", end="left", color="#E46962", dashed=True)
        s.text(
            960,
            990,
            "No host environment variable is passed in; names with KEY, TOKEN, "
            "or SECRET are refused.",
            B,
            INK,
            "center",
        )

    # Sources: harness/scope/guard.py and layer.py (allowed paths, revert, harness-only files);
    # platform/teamtrack/reference/f4/task.toml (test = tests/visible/**); runner/prompts.py (the
    # 7 tools); platform/sandbox/README.md (identical containers).
    @diagram(S3, "least-privilege")
    def least_privilege(s: Scene) -> None:
        s.box(440, 60, 680, 90, "Bare arm", role="bare", stroke_width=BOLD)
        s.box(1180, 60, 680, 90, "Harness arm", role="harness", stroke_width=BOLD)
        rows = [
            ("Files it may change", "any file in its workspace", "only the phase's allowed paths"),
            ("In the test phase", "any file, source included", "tests only (tests/visible/**)"),
            ("A command's changes\noutside the list", "kept", "reverted"),
            (
                "feature_list.json\nand its passes field",
                "no feature list",
                "only the harness writes it",
            ),
        ]
        y = 180
        for label, bare, harn in rows:
            lines = label.count("\n") + 1
            s.text(400, y + 55 - 17.5 * lines, label, B, INK, "right")
            s.box(440, y, 680, 110, bare, role="plain", stroke=GREY)
            s.box(1180, y, 680, 110, harn, role="harness")
            y += 130
        for label, both in [
            ("Tools", "the same 7 tools for both arms"),
            ("Sandbox", "the same container: no network,\nread-only root, limits"),
        ]:
            s.text(400, y + 55 - 17.5, label, B, INK, "right")
            s.box(440, y, 1420, 110, both, dashed=True)
            y += 130

    # Sources: platform/teamtrack/mutants/features/f4.jsonl (app.services.issues-m401, line 54);
    # platform/teamtrack/reference/f4/f4.patch (tests/visible/test_issue_concurrency.py).
    @diagram(S4, "mutation-testing")
    def mutation_testing(s: Scene) -> None:
        orig = s.box(
            60,
            60,
            700,
            190,
            "Original code\napp/services/issues.py, line 54\nissue.version += 1",
            role="plain",
        )
        mut = s.box(
            1160,
            60,
            700,
            190,
            "Mutant: one planted fault\nissue.version += 0\nwrites no longer move the version",
            role="accent",
        )
        s.arrow(orig, mut, "plant one small fault", start="right", end="left")
        ta = s.box(
            60,
            400,
            880,
            220,
            "Test A\ntest_second_writer_with_the_old_version_gets_412\n"
            "On the mutant the second writer\ngets 200, not 412.",
            role="plain",
        )
        tb = s.box(
            980,
            400,
            880,
            220,
            "Test B\ntest_get_returns_the_version_as_etag\n"
            'On the mutant the first ETag\nis still "1".',
            role="plain",
        )
        s.arrow(
            mut,
            ta,
            "run on the mutant",
            start="bottom",
            end="top",
            start_off=-200,
            via=[(1310, 325), (500, 325)],
        )
        s.arrow(mut, tb, start="bottom", end="top", start_off=-90)
        ka = s.box(
            180,
            720,
            640,
            130,
            "fails on the mutant:\nthe mutant is killed",
            role="harness",
            stroke_width=BOLD,
        )
        kb = s.box(
            1100,
            720,
            640,
            130,
            "passes on the mutant:\nthe mutant survives",
            role="fail",
            stroke_width=BOLD,
        )
        s.arrow(ta, ka, start="bottom", end="top")
        s.arrow(tb, kb, start="bottom", end="top")
        s.text(
            960,
            900,
            "Both tests are from the reference tests for version checks (F4).\n"
            "Only test A would catch a lost update.",
            B,
            INK,
            "center",
        )

    # Source: platform/teamtrack/docs/features/f4.md (ETag, If-Match, 412 precondition_failed,
    # nothing changes, the board's 409 page); reference test
    # test_second_writer_with_the_old_version_gets_412.
    @diagram(DOCS, "optimistic-concurrency")
    def optimistic_concurrency(s: Scene) -> None:
        xa, xs, xb = 300, 960, 1620
        s.box(xa - 180, 60, 360, 110, "Tab A\nwriter 1", role="plain")
        s.box(xs - 200, 60, 400, 110, "TeamTrack API\nissue at version 1", role="harness")
        s.box(xb - 180, 60, 360, 110, "Tab B\nwriter 2", role="plain")
        for x in (xa, xs, xb):
            s.line([(x, 180), (x, 950)], dashed=True, color=GREY)

        def msg(x1: float, x2: float, y: float, label: str, color: str = INK) -> None:
            d = 12 if x2 > x1 else -12
            s.path([(x1 + d, y), (x2 - d, y)], label, color=color)

        msg(xa, xs, 235, "GET /issues/{issue_id}")
        msg(xs, xa, 305, 'ETag: "1"')
        msg(xb, xs, 385, "GET /issues/{issue_id}")
        msg(xs, xb, 455, 'ETag: "1"')
        msg(xa, xs, 550, 'PATCH, If-Match: "1"')
        msg(xs, xa, 620, '200, ETag: "2"')
        s.box(xs - 150, 655, 300, 70, "now version 2", role="harness")
        msg(xb, xs, 790, 'PATCH, If-Match: "1"')
        msg(xs, xb, 880, "412 precondition_failed:\nnothing changes", "#E46962")
        s.text(
            960,
            965,
            "Without If-Match a write works as before.\n"
            "On the board, the same stale save gets a 409 page.",
            B,
            INK,
            "center",
        )

    # Sources: harness/decisions.py (the four layers); the four concepts.md pages (what each
    # layer holds); platform/sandbox/README.md; section-4-verification/concepts.md (referee).
    @diagram(DOCS, "harness-one-picture")
    def harness_one_picture(s: Scene) -> None:
        ticket = s.box(60, 415, 220, 100, "Ticket", role="neutral")
        model = s.box(380, 390, 280, 150, "Model", shape="ellipse", role="plain")
        s.box(800, 300, 420, 340, dashed=True)
        s.text(1010, 580, "Sandbox, both arms", B, INK, "center")
        tools = s.box(870, 380, 280, 130, "Tools", role="plain")
        done = s.box(560, 680, 340, 90, 'finish(claim="done")', role="accent")
        s.arrow(ticket, model, start="right", end="left")
        s.arrow(model, tools, start="right", end="left", start_off=-22, end_off=-22)
        s.arrow(tools, model, start="left", end="right", start_off=22, end_off=22)
        s.arrow(model, done, start="bottom", end="top", start_off=60, end_off=-60)
        ins = s.box(
            140,
            40,
            560,
            180,
            "Instructions: what the agent knows\nthe AGENTS.md map in the context;\n"
            "docs/ and skills on disk",
            role="harness",
        )
        sc = s.box(
            800,
            40,
            560,
            180,
            "Scope: what it may change\nfeature_list.json, one feature,\nallowed paths per phase",
            role="harness",
        )
        st = s.box(
            60,
            830,
            620,
            180,
            "State and lifecycle: what it remembers\nprogress.md, session-handoff.md,\n"
            "exec plan, init.sh, git",
            role="harness",
        )
        ve = s.box(
            800,
            830,
            620,
            180,
            "Verification: what proves done\nthe verify gate on the done claim,\nfive test filters",
            role="harness",
        )
        ref = s.box(
            1440,
            360,
            420,
            220,
            "Referee\nafter the agents stop:\nhidden tests, referee\nmutants, house rules",
            role="plain",
        )
        s.arrow(ins, model, start="bottom", end="top", color=BLUE)
        s.arrow(sc, tools, start="bottom", end="top", color=BLUE)
        s.arrow(st, model, start="top", end="bottom", end_off=-60, color=BLUE)
        s.arrow(ve, done, start="top", end="right", color=BLUE)
        s.arrow(tools, ref, "shipped diff", start="right", end="left")

    # Sources: docs/STYLE.md (the four failures); the four section concepts.md pages.
    @diagram(DOCS, "which-layer-when")
    def which_layer_when(s: Scene) -> None:
        start = s.box(
            60,
            410,
            300,
            130,
            "What went\nwrong?",
            role="accent",
            stroke_width=BOLD,
        )
        symptoms = [
            "It broke a rule that is\nwritten down somewhere",
            "A new session redid or\nundid earlier work",
            "It changed files outside the\nticket, or reached too far",
            "It said done, and\nthe work was not done",
        ]
        layers = [
            "Instructions\nput a map in its context",
            "State and lifecycle\nhand off through files and git",
            "Scope and sandbox\nenforce the allowed paths",
            "Verification\ncheck the claim with code",
        ]
        for i in range(4):
            y = 50 + i * 230
            a = s.box(480, y, 600, 150, symptoms[i], role="plain")
            b = s.box(1260, y, 600, 150, layers[i], role="harness")
            s.arrow(start, a, start="right", end="left", start_off=(i - 1.5) * 24)
            s.arrow(a, b, start="right", end="left", color=BLUE)
        s.text(
            960, 975, "Then measure it: an A/B on your ticket, counted in runs.", B, INK, "center"
        )
        _ = FONT_SMALL
