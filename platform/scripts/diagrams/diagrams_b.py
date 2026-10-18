"""Single diagrams: mappings, the data model, and one picture per mechanism.

Coordinates are canvas units of a "wide" canvas (1920x1080); style comes from style.py. Labels
are 5 words at most; the slide notes carry the explanation.
"""

from __future__ import annotations

from exlib import AMBER, BLUE, GREY, INK, RED, Scene
from style import FONT_BODY as B
from style import FONT_SMALL
from style import FONT_TITLE as T
from style import STROKE_WIDTH_BOLD as BOLD


def note(s: Scene, x: float, y: float, text: str, align: str = "center") -> None:
    """The one small footnote line a diagram may carry."""
    s.text(x, y, text, FONT_SMALL, INK, align, role="footnote")


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Source: docs/STYLE.md (the four failures), the four concepts.md pages (the causes).
    @diagram(DOCS, "stories-causes-layers")
    def stories_causes_layers(s: Scene) -> None:
        stories = [
            "Copies a legacy\ntenant leak",
            "Migration rewritten\nacross sessions",
            "Out-of-scope edits\nbreak features",
            "Says done\nwhen not done",
        ]
        causes = [
            "Rule on disk,\nnot context",
            "New session,\nno memory",
            "File list,\nnothing checks it",
            "Grades its\nown work",
        ]
        layers = [
            "Section 1:\nInstructions",
            "Section 2: State\nand sessions",
            "Section 3: Scope\nand sandbox",
            "Section 4:\nVerification",
        ]
        s.text(320, 60, "Story", T, INK, "center")
        s.text(980, 60, "Cause", T, INK, "center")
        s.text(1590, 60, "Layer", T, INK, "center")
        for i in range(4):
            y = 140 + i * 225
            a = s.box(60, y, 520, 185, stories[i], role="plain")
            b = s.box(700, y, 560, 185, causes[i], role="neutral")
            c = s.box(1380, y, 420, 185, layers[i], role="harness")
            s.arrow(a, b, start="right", end="left")
            s.arrow(b, c, start="right", end="left", color=BLUE)

    # Source: platform/teamtrack/app/db/models.py (orgs, users, projects, project_members,
    # issues, audit_log, idempotency_keys); platform/teamtrack/reference/f2, f6, f7 patches
    # (comments, watchers, labels, issue_labels).
    @diagram(DOCS, "teamtrack-data-model")
    def teamtrack_data_model(s: Scene) -> None:
        orgs = s.box(760, 40, 400, 110, "orgs\nid, name, slug", role="neutral")
        s.box(60, 190, 1800, 780, dashed=True, stroke=AMBER, stroke_width=BOLD)
        users = s.box(120, 250, 460, 130, "users\norg_id, email, role", role="plain")
        projects = s.box(730, 250, 460, 130, "projects\norg_id, key, archived_at", role="plain")
        labels = s.box(1340, 250, 460, 130, "labels\norg_id, name", role="plain")
        members = s.box(120, 480, 460, 130, "project_members\nproject_id, user_id", role="plain")
        issues = s.box(
            730,
            460,
            460,
            170,
            "issues: org_id,\nproject_id, assignee_id,\nversion",
            role="plain",
            stroke_width=BOLD,
        )
        issue_labels = s.box(1340, 480, 460, 130, "issue_labels\nissue_id, label_id", role="plain")
        comments = s.box(300, 710, 560, 130, "comments\norg_id, issue_id, author_id", role="plain")
        watchers = s.box(1060, 710, 560, 130, "watchers\norg_id, issue_id, user_id", role="plain")
        s.text(100, 880, "every row carries org_id", B, INK)
        s.text(960, 880, "other org: 404, never 403", B, INK, "center")
        s.text(1820, 880, "audit_log, idempotency_keys: org_id", B, INK, "right")
        s.arrow(orgs, users, start="bottom", end="top", via=[(350, 200)])
        s.arrow(orgs, projects, start="bottom", end="top")
        s.arrow(orgs, labels, start="bottom", end="top", via=[(1570, 200)])
        s.arrow(users, members, start="bottom", end="top")
        s.arrow(projects, members, start="left", end="right", via=[(655, 315), (655, 545)])
        s.arrow(projects, issues, start="bottom", end="top")
        s.arrow(issues, comments, start="bottom", end="top", start_off=-80)
        s.arrow(issues, watchers, start="bottom", end="top", start_off=80)
        s.arrow(issues, issue_labels, start="right", end="left")
        s.arrow(labels, issue_labels, start="bottom", end="top")
        note(s, 960, 985, "arrow: one row has many rows")

    # Sources: section-1-instructions/assignment/starter/original/AGENTS.md (899 lines; heading
    # lines from section-1-instructions/concepts.md); platform/teamtrack/harness/instructions/
    # AGENTS.md (94 lines, the "Where to look" rows); OpenAI quote from concepts.md.
    @diagram(S1, "manual-vs-map")
    def manual_vs_map(s: Scene) -> None:
        top, height = 120, 780
        s.text(60, 60, "Before: 899-line AGENTS.md", B, INK)
        s.box(60, top, 660, height, role="neutral")
        rows = [
            (1, "1  read all of this", INK),
            (196, "196  house rules", AMBER),
            (204, "204  House rule 1", AMBER),
            (586, "586  legacy /v1 API", AMBER),
            (669, "669  team notes, history", INK),
            (787, "787  questions we get", INK),
        ]
        last = -100.0
        for line, label, color in rows:
            y = max(top + 14 + (line - 1) / 899 * (height - 90), last + 44)
            last = y
            s.text(80, y, label, B, INK)
            if color == AMBER:
                s.line([(70, y + 38), (710, y + 38)], color=AMBER, stroke_width=4)
        s.text(390, top + height + 16, "four retired rules inside", B, INK, "center")
        s.text(800, 60, "After: 94-line map", B, INK)
        map_h = round(height * 94 / 899)
        amap = s.box(800, top, 380, map_h, "AGENTS.md map", role="harness", stroke_width=BOLD)
        s.text(990, top + map_h + 16, "always in context,\nto scale", B, INK, "center")
        docs = [
            ".agents/skills/add-endpoint/SKILL.md\nadd or change endpoints",
            "ARCHITECTURE.md\nrouter, service, model",
            "docs/SECURITY.md\nwho may see data",
            "docs/design-docs/api-conventions.md\nlists, errors, statuses",
            "docs/RELIABILITY.md\nwrites, idempotency, migrations",
        ]
        for i, label in enumerate(docs):
            d = s.box(1260, top + i * 150, 600, 120, label, role="plain")
            s.arrow(amap, d, start="right", end="left", start_off=(i - 2) * 6)
        s.text(1560, top + 760, "on disk, opened when needed", B, INK, "center")
        note(s, 960, top + height + 80, 'OpenAI: "a map, not a manual"')

    # Sources: platform/src/shipharness/runner/skills_loader.py (catalogue line format);
    # platform/teamtrack/harness/instructions/.agents/skills/add-endpoint/ (SKILL.md 100 lines,
    # references/tests.md 57 lines); concepts.md tier table; docs/evidence/s1.md (what each arm
    # read).
    @diagram(S1, "skills-three-tiers")
    def skills_three_tiers(s: Scene) -> None:
        t1 = s.box(60, 80, 1240, 170, "Tier 1: always in context", role="harness")
        s.text(1340, 150, "one catalogue line", B, INK)
        t2 = s.box(60, 440, 1240, 170, "Tier 2: SKILL.md, 100 lines", role="plain", stroke=BLUE)
        s.text(1340, 510, "loaded on use", B, INK)
        t3 = s.box(
            60,
            800,
            1240,
            170,
            "Tier 3: tests.md, 57 lines",
            role="plain",
            stroke=BLUE,
            dashed=True,
        )
        s.text(1340, 870, "opened when pointed to", B, INK)
        s.arrow(t1, t2, "task matches description", start="bottom", end="top", color=BLUE)
        s.arrow(t2, t3, "a step needs it", start="bottom", end="top", color=BLUE)
        s.box(1340, 575, 520, 100, "All 3 arms read it", role="accent")
        s.box(1340, 935, 520, 100, "None opened it", role="accent")

    # Sources: runner/loop.py base_items (developer message = core prompt + layer blocks, then
    # the user message); harness/base.py LAYER_ORDER; runner/prompts.py; instructions/router.py;
    # state/lifecycle.py; scope/layer.py; verify/layer.py.
    @diagram(S1, "context-prefix")
    def context_prefix(s: Scene) -> None:
        s.box(60, 60, 1300, 800, dashed=True)
        s.text(90, 76, "Developer message, every session", B, INK)
        blocks = [
            ("1  Core prompt, both arms", "neutral"),
            ("2  Instructions: map, skills", "harness"),
            ("3  State: up to speed", "harness"),
            ("4  Scope: allowed paths", "harness"),
            ("5  Verification: the gate", "harness"),
        ]
        prev = None
        for i, (label, role) in enumerate(blocks):
            b = s.box(100, 136 + i * 142, 1220, 112, label, role=role, align="left")
            if prev is not None:
                s.arrow(prev, b, start="bottom", end="top", gap=4)
            prev = b
        s.box(60, 900, 1300, 120, "User message: phase, ticket", role="plain", align="left")
        s.text(1420, 150, "read first to last", B, INK)
        s.text(1420, 420, "one block per layer", B, INK)
        s.text(1420, 690, "docs stay on disk", B, INK)
        s.text(1420, 940, "bare arm: block 1", B, INK)

    # Sources: platform/src/shipharness/harness/state/handoff.py (MachineSummary.render, the two
    # headings, merge); state/lifecycle.py (wrap-up text: what the notes hold).
    @diagram(S2, "handoff-contents")
    def handoff_contents(s: Scene) -> None:
        s.box(560, 50, 800, 930, role="neutral")
        s.text(960, 66, "session-handoff.md", T, INK, "center")
        mach = s.box(590, 140, 740, 400, "Machine summary\ncommits, files, tests", role="harness")
        notes = s.box(590, 580, 740, 360, "Agent notes\ndoing, left, risks", role="plain")
        harness = s.box(60, 250, 380, 180, "Harness,\nat the stop", role="harness")
        agent = s.box(60, 680, 380, 160, "Agent, in\nwrap-up turns", role="plain")
        s.arrow(harness, mach, "writes", start="right", end="left", color=BLUE)
        s.arrow(agent, notes, "writes", start="right", end="left")
        nxt = s.box(1500, 440, 360, 160, "Next session\nreads it first", role="plain")
        s.arrow(mach, nxt, start="right", end="left", end_off=-30, color=BLUE)
        s.arrow(notes, nxt, start="right", end="left", end_off=30)
        note(s, 960, 1000, "the harness rewrites only its part")

    # Sources: platform/teamtrack/migrations/versions/0001_initial.py; docs/evidence/s2.md
    # (0002_comments.py); harness/state/handoff.py ("needs exactly one" head);
    # concepts.md (House rule 7: Migrations).
    @diagram(S2, "alembic-heads")
    def alembic_heads(s: Scene) -> None:
        s.text(310, 60, "One head", T, INK, "center")
        a0 = s.box(110, 150, 400, 120, "0001_initial", role="plain")
        a1 = s.box(110, 460, 400, 130, "0002_comments\n(session 1)", role="harness")
        s.arrow(a0, a1, "down_revision", start="bottom", end="top")
        s.box(80, 760, 460, 160, "House rule 7: Migrations\nholds", role="neutral")
        s.line([(660, 40), (660, 960)], dashed=True, color=GREY)
        s.text(1310, 60, "Two heads", T, INK, "center")
        b0 = s.box(1110, 150, 400, 120, "0001_initial", role="plain")
        b1 = s.box(760, 460, 440, 130, "0002_comments\n(session 1)", role="harness")
        b2 = s.box(1420, 460, 440, 130, "second comments migration\n(session 2)", role="accent")
        s.arrow(b0, b1, start="bottom", end="top", start_off=-80)
        s.arrow(b0, b2, start="bottom", end="top", start_off=80)
        s.text(1310, 630, "both: down_revision = 0001_initial", B, INK, "center")
        s.box(
            990,
            760,
            640,
            160,
            "House rule 7: Migrations\nfails",
            role="fail",
            stroke_width=BOLD,
        )

    # Sources: harness/scope/guard.py (HARNESS_ONLY, STATE_FILES, the reason text);
    # harness/scope/layer.py (block before a patch, revert after a command);
    # docs/evidence/s3.md (the blocked file).
    @diagram(S3, "scope-check-flow")
    def scope_check_flow(s: Scene) -> None:
        call = s.box(60, 95, 360, 130, "Tool call:\napply_patch", role="plain")
        d1 = s.box(500, 60, 580, 200, "feature_list.json?", shape="diamond")
        b1 = s.box(1200, 95, 660, 130, "BLOCKED:\nharness-only file", role="fail")
        d2 = s.box(530, 346, 520, 230, "In allowed\npaths?", shape="diamond")
        ok = s.box(1200, 395, 660, 130, "Allowed:\npatch applies", role="harness")
        b2 = s.box(420, 660, 740, 160, "BLOCKED: errors.py\noutside build paths", role="fail")
        s.arrow(call, d1, start="right", end="left")
        s.arrow(d1, b1, "yes", start="right", end="left")
        s.arrow(d1, d2, "no", start="bottom", end="top")
        s.arrow(d2, ok, "yes", start="right", end="left")
        s.arrow(d2, b2, "no", start="bottom", end="top")
        s.text(1300, 700, "state files count\nas allowed", B, INK)
        run = s.box(60, 890, 360, 120, "Tool call: run", role="plain")
        ran = s.box(520, 890, 400, 120, "Runs in\nthe sandbox", role="plain")
        rev = s.box(1080, 880, 780, 140, "Outside changes:\nREVERTED", role="fail")
        s.arrow(run, ran, start="right", end="left")
        s.arrow(ran, rev, "then", start="right", end="left")

    # Sources: platform/sandbox/README.md; platform/src/shipharness/sandbox/policy.py;
    # section-3-scope-sandbox/concepts.md (the flags table); .env.example (OPENAI_MODEL).
    @diagram(S3, "sandbox-boundary")
    def sandbox_boundary(s: Scene) -> None:
        s.box(60, 100, 1360, 860, role="plain")
        s.text(90, 116, "Host: your machine", B, INK)
        loop = s.box(100, 200, 340, 140, "Agent loop\n(the runner)", role="plain")
        s.box(100, 430, 340, 140, "API keys:\nhere, in .env", role="accent", stroke_width=BOLD)
        s.box(100, 660, 340, 110, "LangSmith tracing", role="plain")
        s.box(700, 170, 640, 760, role="neutral", stroke_width=BOLD)
        s.text(1020, 186, "Sandbox: one per arm", B, INK, "center")
        items = [
            "/work: writable",
            "root read-only, /tmp writable",
            "user 1000, no capabilities",
            "1024 MB, 256 processes",
            "network: none",
        ]
        boxes = []
        for i, label in enumerate(items):
            boxes.append(
                s.box(740, 250 + i * 134, 560, 110, label, role="fail" if i == 4 else "plain")
            )
        s.arrow(loop, boxes[0], "tool commands\nonly", start="right", end="left")
        api = s.box(1520, 130, 340, 180, "Model API", shape="ellipse", role="plain")
        s.arrow(
            loop,
            api,
            "model calls leave the host",
            start="top",
            end="top",
            start_off=110,
            via=[(380, 62), (1690, 62)],
        )
        net = s.box(1520, 790, 340, 120, "The internet", dashed=True)
        s.arrow(boxes[4], net, "blocked", start="right", end="left", color=RED, dashed=True)
        note(s, 960, 975, "no KEY, TOKEN, SECRET variables")

    # Sources: harness/scope/guard.py and layer.py (allowed paths, revert, harness-only files);
    # platform/teamtrack/reference/f4/task.toml (test = tests/visible/**); runner/prompts.py (the
    # 7 tools); platform/sandbox/README.md (identical containers).
    @diagram(S3, "least-privilege")
    def least_privilege(s: Scene) -> None:
        s.box(440, 60, 680, 100, "Bare arm", role="bare", stroke_width=BOLD)
        s.box(1180, 60, 680, 100, "Harness arm", role="harness", stroke_width=BOLD)
        rows = [
            ("Files it may change", "any workspace file", "allowed paths only"),
            ("Test phase", "any file, source too", "tests/visible/** only"),
            ("Command changes outside", "kept", "reverted"),
            ("feature_list.json passes", "no feature list", "harness writes it"),
        ]
        y = 190
        for label, bare, harn in rows:
            s.text(400, y + 60 - 17.5, label, B, INK, "right")
            s.box(440, y, 680, 120, bare, role="plain", stroke=GREY)
            s.box(1180, y, 680, 120, harn, role="harness")
            y += 140
        for label, both in [("Tools", "same 7 tools"), ("Sandbox", "same container, no network")]:
            s.text(400, y + 60 - 17.5, label, B, INK, "right")
            s.box(440, y, 1420, 120, both, dashed=True)
            y += 140

    # Sources: platform/teamtrack/mutants/features/f4.jsonl (app.services.issues-m401, line 54);
    # platform/teamtrack/reference/f4/f4.patch (tests/visible/test_issue_concurrency.py).
    @diagram(S4, "mutation-testing")
    def mutation_testing(s: Scene) -> None:
        orig = s.box(60, 60, 700, 190, "Original code\nissue.version += 1", role="plain")
        mut = s.box(1160, 60, 700, 190, "Mutant\nissue.version += 0", role="accent")
        s.arrow(orig, mut, "plant one fault", start="right", end="left")
        ta = s.box(
            60,
            400,
            880,
            220,
            "Test A\ntest_second_writer_with_the_old_version_gets_412",
            role="plain",
        )
        tb = s.box(980, 400, 880, 220, "Test B\ntest_get_returns_the_version_as_etag", role="plain")
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
        ka = s.box(180, 720, 640, 150, "fails:\nmutant killed", role="harness", stroke_width=BOLD)
        kb = s.box(1100, 720, 640, 150, "passes:\nmutant survives", role="fail", stroke_width=BOLD)
        s.arrow(ta, ka, start="bottom", end="top")
        s.arrow(tb, kb, start="bottom", end="top")
        note(s, 960, 930, "app/services/issues.py, line 54")

    # Source: platform/teamtrack/docs/features/f4.md (ETag, If-Match, 412 precondition_failed,
    # nothing changes, the board's 409 page); reference test
    # test_second_writer_with_the_old_version_gets_412.
    @diagram(DOCS, "optimistic-concurrency")
    def optimistic_concurrency(s: Scene) -> None:
        xa, xs, xb = 300, 960, 1620
        s.box(xa - 180, 60, 360, 110, "Tab A\nwriter 1", role="plain")
        s.box(xs - 200, 60, 400, 110, "TeamTrack API\nversion 1", role="harness")
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
        msg(xs, xb, 880, "412 precondition_failed:\nnothing changes", RED)
        note(s, 960, 980, "without If-Match, writes work as before")

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
        ins = s.box(140, 40, 560, 180, "Instructions:\nwhat it knows", role="harness")
        sc = s.box(800, 40, 560, 180, "Scope:\nwhat it may change", role="harness")
        st = s.box(60, 830, 620, 180, "State:\nwhat it remembers", role="harness")
        ve = s.box(800, 830, 620, 180, "Verification:\nwhat proves done", role="harness")
        ref = s.box(1440, 360, 420, 220, "Referee: hidden tests,\nmutants", role="plain")
        s.arrow(ins, model, start="bottom", end="top", color=BLUE)
        s.arrow(sc, tools, start="bottom", end="top", color=BLUE)
        s.arrow(st, model, start="top", end="bottom", end_off=-60, color=BLUE)
        s.arrow(ve, done, start="top", end="right", color=BLUE)
        s.arrow(tools, ref, "shipped diff", start="right", end="left")

    # Sources: docs/STYLE.md (the four failures); the four section concepts.md pages.
    @diagram(DOCS, "which-layer-when")
    def which_layer_when(s: Scene) -> None:
        start = s.box(60, 410, 300, 130, "What went\nwrong?", role="accent", stroke_width=BOLD)
        symptoms = [
            "Broke a written rule",
            "New session redid work",
            "Changed files outside ticket",
            "Said done, not done",
        ]
        layers = [
            "Instructions:\na map",
            "State:\nfiles and git",
            "Scope:\nenforced paths",
            "Verification:\ncheck with code",
        ]
        for i in range(4):
            y = 50 + i * 230
            a = s.box(480, y, 600, 150, symptoms[i], role="plain")
            b = s.box(1260, y, 600, 150, layers[i], role="harness")
            s.arrow(start, a, start="right", end="left", start_off=(i - 1.5) * 24)
            s.arrow(a, b, start="right", end="left", color=BLUE)
        note(s, 960, 985, "then measure it with an A/B")
