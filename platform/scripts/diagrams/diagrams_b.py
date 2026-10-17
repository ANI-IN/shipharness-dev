"""Single diagrams: mappings, the data model, and one picture per mechanism."""

from __future__ import annotations

from exlib import AMBER, BLUE, GREY, INK, Scene, tint

AMBER_FILL = tint(AMBER, "33")
BLUE_FILL = tint(BLUE)
GREY_FILL = tint(GREY, "33")
INK_FILL = tint(INK, "10")


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Source: docs/STYLE.md (the four failures), the four concepts.md pages (the causes).
    @diagram(DOCS, "stories-causes-layers")
    def stories_causes_layers(s: Scene) -> None:
        stories = [
            "Agent copies a tenant leak\nfrom legacy code",
            "A migration is rewritten\nacross sessions",
            "Out-of-scope edits\nbreak old features",
            "Agent says done\nwhen it is not",
        ]
        causes = [
            "The rule is on disk,\nnot in its context",
            "Each new session starts\nwith no memory",
            "The file list is written down,\nbut nothing checks it",
            "It grades its own work;\nvisible tests are not the feature",
        ]
        layers = [
            "Instructions\nSection 1",
            "State and lifecycle\nSection 2",
            "Scope and sandbox\nSection 3",
            "Verification\nSection 4",
        ]
        s.text(270, 30, "Story", 28, INK, "center")
        s.text(870, 30, "Cause", 28, INK, "center")
        s.text(1440, 30, "Layer", 28, BLUE, "center")
        for i in range(4):
            y = 100 + i * 170
            a = s.box(40, y, 460, 130, stories[i])
            b = s.box(640, y, 460, 130, causes[i], fill=INK_FILL)
            c = s.box(1240, y, 400, 130, layers[i], stroke=BLUE, fill=BLUE_FILL)
            s.arrow(a, b, start="right", end="left")
            s.arrow(b, c, start="right", end="left", color=BLUE)

    # Source: platform/teamtrack/app/db/models.py (orgs, users, projects, project_members,
    # issues, audit_log, idempotency_keys); platform/teamtrack/reference/f2, f6, f7 patches
    # (comments, watchers, labels, issue_labels).
    @diagram(DOCS, "teamtrack-data-model")
    def teamtrack_data_model(s: Scene) -> None:
        orgs = s.box(630, 30, 340, 100, "orgs\nid, name, slug", fill=INK_FILL)
        s.box(40, 190, 1520, 890, dashed=True, stroke=AMBER, stroke_width=3)
        s.text(
            70,
            975,
            "Tenant boundary: every row in here carries org_id.\n"
            "Another org's row answers 404, never 403 (R1).",
            22,
            INK,
        )
        users = s.box(80, 330, 360, 120, "users\norg_id, email, role")
        projects = s.box(620, 330, 360, 120, "projects\norg_id, key, archived_at")
        labels = s.box(1160, 330, 360, 120, "labels (F7)\norg_id, name")
        members = s.box(80, 560, 360, 120, "project_members\nproject_id, user_id")
        issues = s.box(
            620,
            540,
            360,
            160,
            "issues\norg_id, project_id,\nassignee_id, created_by,\nversion",
            stroke_width=3,
        )
        issue_labels = s.box(1160, 560, 360, 120, "issue_labels (F7)\nissue_id, label_id")
        comments = s.box(330, 820, 380, 120, "comments (F2)\norg_id, issue_id, author_id")
        watchers = s.box(890, 820, 380, 120, "watchers (F6)\norg_id, issue_id, user_id")
        s.text(1540, 900, "Also scoped by org_id:\naudit_log, idempotency_keys", 20, INK, "right")
        s.arrow(orgs, users, start="bottom", end="top", via=[(260, 200)])
        s.arrow(orgs, projects, start="bottom", end="top")
        s.arrow(orgs, labels, start="bottom", end="top", via=[(1340, 200)])
        s.arrow(users, members, start="bottom", end="top")
        s.arrow(projects, members, start="left", end="right", via=[(530, 390), (530, 620)])
        s.arrow(projects, issues, start="bottom", end="top")
        s.arrow(issues, comments, start="bottom", end="top")
        s.arrow(issues, watchers, start="bottom", end="top")
        s.arrow(issues, issue_labels, start="right", end="left")
        s.arrow(labels, issue_labels, start="bottom", end="top")
        s.text(
            800,
            1110,
            "Arrow: one row has many rows. (F2), (F6), (F7): tables that the "
            "comments, watchers, and labels tickets add.",
            20,
            INK,
            "center",
        )

    # Sources: section-1-instructions/assignment/starter/original/AGENTS.md (899 lines; heading
    # lines from section-1-instructions/concepts.md); platform/teamtrack/harness/instructions/
    # AGENTS.md (94 lines, the "Where to look" rows); OpenAI quote from concepts.md.
    @diagram(S1, "manual-vs-map")
    def manual_vs_map(s: Scene) -> None:
        top, height = 90, 800
        s.text(40, 30, "Before: one 899-line AGENTS.md", 26, INK)
        s.box(40, top, 520, height, fill=INK_FILL)
        rows = [
            (1, "1  AGENTS.md: TeamTrack (read all of this ...)", INK),
            (196, "196  House rules R1 to R7 (R1 at line 204)", AMBER),
            (586, "586  The legacy /v1 API", AMBER),
            (669, "669  Team notes and history", INK),
            (787, "787  Questions we keep getting", INK),
        ]
        for line, label, color in rows:
            y = top + 12 + (line - 1) / 899 * (height - 60)
            s.text(60, y, label, 20, INK)
            if color == AMBER:
                s.line([(48, y + 28), (552, y + 28)], color=AMBER, stroke_width=3)
        s.text(300, top + height + 16, "Four retired rules are still in it.", 20, INK, "center")
        s.text(640, 30, "After: a 94-line map", 26, BLUE)
        map_h = round(height * 94 / 899)
        amap = s.box(
            640,
            top,
            300,
            map_h,
            "AGENTS.md map\nin every session's context",
            stroke=BLUE,
            fill=BLUE_FILL,
            size=20,
            pad=10,
        )
        s.text(790, top + map_h + 14, "drawn to scale:\n94 of 899 lines", 20, BLUE, "center")
        docs = [
            ".agents/skills/add-endpoint/SKILL.md\nadd or change an endpoint",
            "ARCHITECTURE.md\ntouch a router, service, or model",
            "docs/SECURITY.md\ndecide who may see or change data",
            "docs/design-docs/api-conventions.md\nshape a list, an error, a status",
            "docs/RELIABILITY.md\nwrites, idempotency, migrations",
        ]
        for i, label in enumerate(docs):
            d = s.box(1080, top + i * 150, 460, 110, label)
            s.arrow(amap, d, start="right", end="left", start_off=(i - 2) * 8)
        s.text(1310, top + 760, "On disk: opened only when\nthe task needs it", 20, INK, "center")
        s.text(
            800,
            top + height + 70,
            '"give Codex a map, not a 1,000-page instruction manual."  '
            "(OpenAI, Harness engineering)",
            20,
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
            40,
            40,
            1080,
            170,
            "Tier 1: the catalogue line, always in the context\n"
            "- add-endpoint: Add or change a TeamTrack HTTP endpoint so it follows\n"
            "  house rules R1-R7 ... (read .agents/skills/add-endpoint/SKILL.md to use it)",
            stroke=BLUE,
            fill=BLUE_FILL,
            align="left",
        )
        t2 = s.box(
            40,
            330,
            1080,
            130,
            "Tier 2: SKILL.md, 100 lines\nloaded when the agent decides to use the skill",
            stroke=BLUE,
            align="left",
        )
        t3 = s.box(
            40,
            580,
            1080,
            130,
            "Tier 3: references/tests.md, 57 lines\nopened only when a step points to it",
            stroke=BLUE,
            dashed=True,
            align="left",
        )
        s.arrow(t1, t2, "the task matches the description", start="bottom", end="top", color=BLUE)
        s.arrow(t2, t3, "a step needs it", start="bottom", end="top", color=BLUE)
        s.box(
            1200,
            300,
            400,
            190,
            "One round of test runs:\nall 3 harness arms read\ntier 2; none opened tier 3",
            stroke=AMBER,
            fill=AMBER_FILL,
        )

    # Sources: runner/loop.py base_items (developer message = core prompt + layer blocks, then
    # the user message); harness/base.py LAYER_ORDER; runner/prompts.py; instructions/router.py;
    # state/lifecycle.py; scope/layer.py; verify/layer.py.
    @diagram(S1, "context-prefix")
    def context_prefix(s: Scene) -> None:
        s.box(40, 40, 1080, 790, dashed=True)
        s.text(70, 56, "Developer message: the same text at the start of every session", 22, INK)
        blocks = [
            (
                "1  Core prompt: the tools, how to call finish\n"
                "    (both arms; the bare arm gets only this block)",
                INK,
                INK_FILL,
            ),
            ("2  Instructions: the AGENTS.md map,\n    then the skills catalogue", BLUE, BLUE_FILL),
            (
                "3  State: Getting up to speed\n    (progress.md, git log, session-handoff.md)",
                BLUE,
                BLUE_FILL,
            ),
            (
                "4  Scope: the one feature and\n    the files you may change in each phase",
                BLUE,
                BLUE_FILL,
            ),
            ("5  Verification: what the gate checks\n    when you claim done", BLUE, BLUE_FILL),
        ]
        prev = None
        for i, (label, stroke, fill) in enumerate(blocks):
            b = s.box(80, 110 + i * 142, 1000, 112, label, stroke=stroke, fill=fill, align="left")
            if prev is not None:
                s.arrow(prev, b, start="bottom", end="top", gap=4)
            prev = b
        s.box(
            40,
            880,
            1080,
            120,
            "User message: the phase and the ticket. A later session also gets:\n"
            '"A previous session worked on this ticket and was stopped."',
            align="left",
        )
        s.text(1170, 120, "Read in this order,\nfirst to last.", 22, INK)
        s.text(
            1170,
            300,
            "Each section adds\nits layer's block.\nThe full harness\nsends all five.",
            22,
            BLUE,
        )
        s.text(1170, 520, "Documents and\nskill bodies stay\non disk.", 22, INK)

    # Sources: platform/src/shipharness/harness/state/handoff.py (MachineSummary.render, the two
    # headings, merge); state/lifecycle.py (wrap-up text: what the notes hold).
    @diagram(S2, "handoff-contents")
    def handoff_contents(s: Scene) -> None:
        s.box(520, 40, 680, 900, fill=INK_FILL)
        s.text(860, 56, "session-handoff.md", 26, INK, "center")
        mach = s.box(
            550,
            110,
            620,
            440,
            "## Machine summary\n"
            "Written by the harness at the end of session N\n"
            "(phase, what ended it, turns)\n"
            "- Commits: start, end\n- Files changed in this session\n"
            "- Visible tests\n- Last commits\n- Open TODO markers\n"
            "- Migration heads\n- Harness documents read so far",
            stroke=BLUE,
            fill=tint(BLUE, "33"),
            align="left",
        )
        notes = s.box(
            550,
            600,
            620,
            300,
            "## Notes from the agent\n- What it was doing\n- What is left\n"
            "- What to watch out for\n- House rules and file locations\n"
            "  that matter for this ticket",
            align="left",
        )
        harness = s.box(
            40,
            250,
            360,
            150,
            "The harness, at the stop\nfacts read from\nthe repository",
            stroke=BLUE,
            fill=BLUE_FILL,
        )
        agent = s.box(40, 680, 360, 140, "The agent,\nin its wrap-up turns")
        s.arrow(harness, mach, "writes", start="right", end="left", color=BLUE)
        s.arrow(agent, notes, "writes", start="right", end="left")
        nxt = s.box(1340, 420, 320, 140, "The next session\nreads it first")
        s.arrow(mach, nxt, start="right", end="left", end_off=-30, color=BLUE)
        s.arrow(notes, nxt, start="right", end="left", end_off=30)
        s.text(
            860,
            960,
            "The harness rewrites only its part; the notes stay as written.",
            20,
            INK,
            "center",
        )

    # Sources: platform/teamtrack/migrations/versions/0001_initial.py; docs/evidence/s2.md
    # (0002_comments.py); harness/state/handoff.py ("house rule R7 needs exactly one");
    # concepts.md (R7).
    @diagram(S2, "alembic-heads")
    def alembic_heads(s: Scene) -> None:
        s.text(250, 30, "One head", 28, INK, "center")
        a0 = s.box(80, 100, 340, 100, "0001_initial")
        a1 = s.box(80, 320, 340, 110, "0002_comments\n(session 1)", stroke=BLUE, fill=BLUE_FILL)
        s.arrow(a0, a1, "down_revision", start="bottom", end="top")
        s.box(60, 520, 380, 110, "1 head:\nhouse rule R7 holds", stroke=INK, fill=INK_FILL)
        s.line([(560, 20), (560, 660)], dashed=True, color=GREY)
        s.text(1070, 30, "Two heads", 28, INK, "center")
        b0 = s.box(900, 100, 340, 100, "0001_initial")
        b1 = s.box(660, 320, 360, 110, "0002_comments\n(session 1)", stroke=BLUE, fill=BLUE_FILL)
        b2 = s.box(
            1120,
            320,
            360,
            110,
            "a second comments\nmigration (session 2)",
            stroke=AMBER,
            fill=AMBER_FILL,
        )
        s.arrow(b0, b1, start="bottom", end="top", start_off=-60)
        s.arrow(b0, b2, start="bottom", end="top", start_off=60)
        s.text(1070, 446, "both: down_revision = 0001_initial", 20, INK, "center")
        s.box(
            780,
            520,
            580,
            110,
            "2 heads:\nhouse rule R7 needs exactly one",
            stroke=AMBER,
            fill=AMBER_FILL,
            stroke_width=3,
        )

    # Sources: harness/scope/guard.py (HARNESS_ONLY, STATE_FILES, the reason text);
    # harness/scope/layer.py (block before a patch, revert after a command);
    # docs/evidence/s3.md (the blocked file).
    @diagram(S3, "scope-check-flow")
    def scope_check_flow(s: Scene) -> None:
        call = s.box(40, 80, 320, 120, "Tool call: apply_patch\nchanges a path")
        d1 = s.box(470, 50, 360, 180, "feature_list.json?", shape="diamond")
        b1 = s.box(
            470,
            340,
            360,
            130,
            "BLOCKED\nwritten only\nby the harness",
            stroke=AMBER,
            fill=AMBER_FILL,
        )
        d2 = s.box(960, 30, 420, 220, "In this phase's\nallowed paths?", shape="diamond")
        ok = s.box(1500, 80, 300, 120, "Allowed:\nthe patch applies", stroke=BLUE, fill=BLUE_FILL)
        b2 = s.box(
            930,
            340,
            480,
            170,
            "BLOCKED: app/services/errors.py\nis outside the allowed paths\n"
            "for the build phase (...)\nNothing is written.",
            stroke=AMBER,
            fill=AMBER_FILL,
        )
        s.arrow(call, d1, start="right", end="left")
        s.arrow(d1, b1, "yes", start="bottom", end="top")
        s.arrow(d1, d2, "no", start="right", end="left")
        s.arrow(d2, ok, "yes", start="right", end="left")
        s.arrow(d2, b2, "no", start="bottom", end="top")
        run = s.box(40, 640, 320, 120, "Tool call: run\na shell command")
        ran = s.box(520, 640, 360, 120, "The command runs\nin the sandbox")
        rev = s.box(
            1040,
            630,
            520,
            140,
            "Changes outside the allowed paths\nare restored from a snapshot:\nREVERTED",
            stroke=AMBER,
            fill=AMBER_FILL,
        )
        s.arrow(run, ran, start="right", end="left")
        s.arrow(ran, rev, "then", start="right", end="left")
        s.text(
            920,
            840,
            "progress.md, session-handoff.md, and docs/exec-plans/** count as "
            "allowed when the state layer is on.",
            20,
            INK,
            "center",
        )

    # Sources: platform/sandbox/README.md; platform/src/shipharness/sandbox/policy.py;
    # section-3-scope-sandbox/concepts.md (the flags table); .env.example (OPENAI_MODEL).
    @diagram(S3, "sandbox-boundary")
    def sandbox_boundary(s: Scene) -> None:
        s.box(40, 60, 1220, 820)
        s.text(70, 76, "Host: your machine", 24, INK)
        loop = s.box(90, 160, 330, 130, "Agent loop\n(the runner)")
        s.box(
            90,
            380,
            330,
            120,
            "API keys\nstay here, in .env",
            stroke=AMBER,
            fill=AMBER_FILL,
            stroke_width=3,
        )
        s.box(90, 590, 330, 100, "LangSmith tracing")
        s.box(640, 140, 580, 700, stroke=INK, fill=INK_FILL, stroke_width=3)
        s.text(930, 156, "Sandbox container, one per arm", 22, INK, "center")
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
                    680,
                    210 + i * 124,
                    500,
                    100,
                    label,
                    stroke=AMBER if i == 4 else INK,
                    fill=AMBER_FILL if i == 4 else None,
                )
            )
        s.arrow(loop, boxes[0], "tool commands\nonly", start="right", end="left")
        api = s.box(1400, 120, 300, 150, "Model API", shape="ellipse")
        s.arrow(
            loop,
            api,
            "the model calls go out from the host",
            start="top",
            end="top",
            start_off=100,
            via=[(355, 20), (1550, 20)],
        )
        net = s.box(1400, 700, 300, 110, "The internet", dashed=True)
        s.arrow(boxes[4], net, "blocked", start="right", end="left", color=AMBER, dashed=True)
        x, y = 1350, 755
        s.line([(x - 18, y - 18), (x + 18, y + 18)], color=AMBER, stroke_width=4)
        s.line([(x - 18, y + 18), (x + 18, y - 18)], color=AMBER, stroke_width=4)
        s.text(
            650,
            910,
            "No host environment variable is passed in; names with KEY, TOKEN, "
            "or SECRET are refused.",
            20,
            INK,
            "center",
        )

    # Sources: harness/scope/guard.py and layer.py (allowed paths, revert, harness-only files);
    # platform/teamtrack/reference/f4/task.toml (test = tests/visible/**); runner/prompts.py (the
    # 7 tools); platform/sandbox/README.md (identical containers).
    @diagram(S3, "least-privilege")
    def least_privilege(s: Scene) -> None:
        s.box(460, 40, 480, 90, "Bare arm", stroke=GREY, fill=GREY_FILL, stroke_width=3, size=24)
        s.box(
            1000, 40, 480, 90, "Harness arm", stroke=BLUE, fill=BLUE_FILL, stroke_width=3, size=24
        )
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
        y = 170
        for label, bare, harn in rows:
            s.text(420, y + 55 - 12.5 * label.count("\n") - 12.5, label, 22, INK, "right")
            s.box(460, y, 480, 110, bare, stroke=GREY)
            s.box(1000, y, 480, 110, harn, stroke=BLUE, fill=BLUE_FILL)
            y += 135
        for label, both in [
            ("Tools", "the same 7 tools for both arms"),
            ("Sandbox", "the same container: no network,\nread-only root, limits"),
        ]:
            s.text(420, y + 55 - 12.5 * both.count("\n") * 0 - 12.5, label, 22, INK, "right")
            s.box(460, y, 1020, 110, both, dashed=True)
            y += 135

    # Sources: platform/teamtrack/mutants/features/f4.jsonl (app.services.issues-m401, line 54);
    # platform/teamtrack/reference/f4/f4.patch (tests/visible/test_issue_concurrency.py).
    @diagram(S4, "mutation-testing")
    def mutation_testing(s: Scene) -> None:
        orig = s.box(
            40, 40, 620, 170, "Original code\napp/services/issues.py, line 54\nissue.version += 1"
        )
        mut = s.box(
            940,
            40,
            620,
            170,
            "Mutant: one planted fault\nissue.version += 0\nwrites no longer move the version",
            stroke=AMBER,
            fill=AMBER_FILL,
        )
        s.arrow(orig, mut, "plant one small fault", start="right", end="left")
        ta = s.box(
            40,
            360,
            740,
            190,
            "Test A\ntest_second_writer_with_the_old_version_gets_412\n"
            "On the mutant the second writer\ngets 200, not 412.",
            stroke=INK,
        )
        tb = s.box(
            820,
            360,
            740,
            190,
            "Test B\ntest_get_returns_the_version_as_etag\n"
            'On the mutant the first ETag\nis still "1".',
            stroke=INK,
        )
        s.arrow(
            mut,
            ta,
            "run on the mutant",
            start="bottom",
            end="top",
            start_off=-200,
            via=[(1050, 290), (410, 290)],
        )
        s.arrow(mut, tb, start="bottom", end="top", start_off=-60)
        ka = s.box(
            140,
            660,
            540,
            120,
            "fails on the mutant:\nthe mutant is killed",
            stroke=INK,
            fill=AMBER,
            stroke_width=3,
        )
        kb = s.box(
            920,
            660,
            540,
            120,
            "passes on the mutant:\nthe mutant survives",
            stroke=INK,
            stroke_width=3,
        )
        s.arrow(ta, ka, start="bottom", end="top")
        s.arrow(tb, kb, start="bottom", end="top")
        s.text(
            800,
            830,
            "Both tests are from the F4 reference tests. Only test A would catch a lost update.",
            20,
            INK,
            "center",
        )

    # Source: platform/teamtrack/docs/features/f4.md (ETag, If-Match, 412 precondition_failed,
    # nothing changes, the board's 409 page); reference test
    # test_second_writer_with_the_old_version_gets_412.
    @diagram(DOCS, "optimistic-concurrency")
    def optimistic_concurrency(s: Scene) -> None:
        xa, xs, xb = 220, 820, 1420
        a = s.box(xa - 160, 30, 320, 100, "Tab A\nwriter 1")
        srv = s.box(
            xs - 170, 30, 340, 100, "TeamTrack API\nissue at version 1", stroke=BLUE, fill=BLUE_FILL
        )
        b = s.box(xb - 160, 30, 320, 100, "Tab B\nwriter 2")
        for x in (xa, xs, xb):
            s.line([(x, 140), (x, 900)], dashed=True, color=GREY)
        _ = (a, srv, b)

        def msg(x1: float, x2: float, y: float, label: str, color: str = INK) -> None:
            d = 12 if x2 > x1 else -12
            s.path([(x1 + d, y), (x2 - d, y)], label, color=color)

        msg(xa, xs, 190, "GET /issues/{issue_id}")
        msg(xs, xa, 260, 'ETag: "1"')
        msg(xb, xs, 340, "GET /issues/{issue_id}")
        msg(xs, xb, 410, 'ETag: "1"')
        msg(xa, xs, 510, 'PATCH, If-Match: "1"')
        msg(xs, xa, 580, '200, ETag: "2"')
        s.box(xs - 130, 615, 260, 70, "now version 2", stroke=BLUE, fill=BLUE_FILL)
        msg(xb, xs, 740, 'PATCH, If-Match: "1"')
        msg(xs, xb, 820, "412 precondition_failed:\nnothing changes", AMBER)
        s.text(
            820,
            930,
            "Without If-Match a write works as before. "
            "On the board, the same stale save gets a 409 page.",
            20,
            INK,
            "center",
        )

    # Sources: harness/decisions.py (the four layers); the four concepts.md pages (what each
    # layer holds); platform/sandbox/README.md; section-4-verification/concepts.md (referee).
    @diagram(DOCS, "harness-one-picture")
    def harness_one_picture(s: Scene) -> None:
        ticket = s.box(40, 400, 220, 100, "Ticket", fill=INK_FILL)
        model = s.box(400, 380, 260, 140, "Model", shape="ellipse")
        s.box(860, 300, 340, 300, dashed=True)
        s.text(1030, 550, "Sandbox, both arms", 22, INK, "center")
        tools = s.box(910, 390, 240, 120, "Tools")
        done = s.box(640, 640, 280, 90, 'finish(claim="done")', stroke=AMBER, fill=AMBER_FILL)
        s.arrow(ticket, model, start="right", end="left")
        s.arrow(model, tools, start="right", end="left", start_off=-22, end_off=-22)
        s.arrow(tools, model, start="left", end="right", start_off=22, end_off=22)
        s.arrow(model, done, start="bottom", end="top")
        ins = s.box(
            160,
            40,
            560,
            170,
            "Instructions: what the agent knows\nthe AGENTS.md map in the context;\n"
            "docs/ and skills on disk",
            stroke=BLUE,
            fill=BLUE_FILL,
        )
        sc = s.box(
            880,
            40,
            560,
            170,
            "Scope: what it may change\nfeature_list.json, one feature,\nallowed paths per phase",
            stroke=BLUE,
            fill=BLUE_FILL,
        )
        st = s.box(
            40,
            800,
            560,
            170,
            "State and lifecycle: what it remembers\nprogress.md, session-handoff.md,\n"
            "exec plan, init.sh, git",
            stroke=BLUE,
            fill=BLUE_FILL,
        )
        ve = s.box(
            880,
            800,
            560,
            170,
            "Verification: what proves done\nthe verify gate on the done claim,\nfive test filters",
            stroke=BLUE,
            fill=BLUE_FILL,
        )
        ref = s.box(
            1440,
            380,
            380,
            200,
            "Referee\nafter the agents stop:\nhidden tests, referee\nmutants, R1-R7",
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
            40,
            390,
            280,
            120,
            "What went wrong?",
            stroke=AMBER,
            fill=AMBER_FILL,
            stroke_width=3,
            size=24,
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
            y = 60 + i * 230
            a = s.box(460, y, 520, 140, symptoms[i])
            b = s.box(1120, y, 480, 140, layers[i], stroke=BLUE, fill=BLUE_FILL)
            s.arrow(start, a, start="right", end="left", start_off=(i - 1.5) * 20)
            s.arrow(a, b, start="right", end="left", color=BLUE)
        s.text(
            820, 1000, "Then measure it: an A/B on your ticket, counted in runs.", 22, INK, "center"
        )
