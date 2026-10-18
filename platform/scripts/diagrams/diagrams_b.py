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
    @diagram(DOCS, "stories-causes-layers", canvas="strip")
    def stories_causes_layers(s: Scene) -> None:
        stories = [
            "Copies a legacy tenant leak",
            "Migration rewritten across sessions",
            "Out-of-scope edits break features",
            "Says done when not",
        ]
        causes = [
            "Rule not in context",
            "New session, no memory",
            "Nothing checks file list",
            "Grades its own work",
        ]
        layers = [
            "Section 1: Instructions",
            "Section 2: State and sessions",
            "Section 3: Scope and sandbox",
            "Section 4: Verification",
        ]
        s.text(290, 60, "Story", T, INK, "center")
        s.text(860, 60, "Cause", T, INK, "center")
        s.text(1540, 60, "Layer", T, INK, "center")
        for i in range(4):
            y = 140 + i * 135
            mid = y + 50
            s.text(290, mid - 17.5, stories[i], B, INK, "center")
            s.text(860, mid - 17.5, causes[i], B, INK, "center")
            s.path([(560, mid), (650, mid)])
            s.box(1220, y, 640, 100, layers[i], role="harness")
            s.path([(1070, mid), (1200, mid)], color=BLUE)

    # Source: platform/teamtrack/app/db/models.py (the seven tables; project_members has no
    # org_id of its own, it joins a project and a user).
    @diagram(DOCS, "teamtrack-data-model", canvas="strip")
    def teamtrack_data_model(s: Scene) -> None:
        orgs = s.box(60, 100, 300, 130, "orgs\nid, name, slug", role="neutral")
        s.text(210, 290, "dashed: org_id\non every row", B, INK, "center")
        zone = s.box(440, 60, 1420, 420, dashed=True, stroke=AMBER, stroke_width=BOLD)
        users = s.box(480, 100, 420, 130, "users\norg_id, email, role", role="plain")
        projects = s.box(940, 100, 420, 130, "projects\norg_id, key", role="plain")
        s.box(1400, 100, 420, 130, "issues\norg_id, version", role="plain", stroke_width=BOLD)
        s.box(1060, 300, 360, 130, "audit_log\norg_id, actor_id", role="plain")
        s.box(1460, 300, 360, 130, "idempotency_keys\norg_id, key", role="plain")
        members = s.box(480, 530, 420, 130, "project_members\nproject_id, user_id", role="plain")
        s.arrow(orgs, zone, start="right", end="left", end_off=-105)
        s.arrow(users, members, start="bottom", end="top")
        s.arrow(projects, members, start="bottom", end="right", start_off=-160, via=[(990, 595)])

    # Sources: section-1-instructions/assignment/starter/original/AGENTS.md (899 lines; heading
    # lines from section-1-instructions/concepts.md); platform/teamtrack/harness/instructions/
    # AGENTS.md (94 lines, the "Where to look" rows).
    @diagram(S1, "manual-vs-map", canvas="strip")
    def manual_vs_map(s: Scene) -> None:
        top, height = 60, 600
        s.box(60, top, 560, height, role="neutral")
        s.text(340, top + 16, "Before: 899 lines", T, INK, "center")
        rows = [
            (1, "1  read all of this", INK),
            (204, "204  House rule 1", AMBER),
            (586, "586  legacy /v1 API", AMBER),
            (787, "787  questions we get", INK),
        ]
        for line, label, color in rows:
            y = top + 90 + (line - 1) / 899 * (height - 150)
            s.text(90, y, label, B, INK)
            if color == AMBER:
                s.line([(80, y + 40), (600, y + 40)], color=AMBER, stroke_width=4)
        map_h = round(height * 94 / 899)
        s.text(950, 200, "After: 94-line map", T, INK, "center")
        amap = s.box(760, 275, 380, map_h, "AGENTS.md map", role="harness", stroke_width=BOLD)
        s.text(950, 275 + map_h + 20, "always in context,\nto scale", B, INK, "center")
        docs = [
            "add-endpoint skill\nendpoint changes",
            "ARCHITECTURE.md\nrouter, service, model",
            "docs/SECURITY.md\nwho may see data",
        ]
        for i, label in enumerate(docs):
            d = s.box(1300, top + 20 + i * 165, 560, 130, label, role="plain")
            s.arrow(amap, d, start="right", end="left", start_off=(i - 1) * 10)
        s.text(1580, top + 520, "on disk, opened when needed", B, INK, "center")

    # Sources: platform/src/shipharness/runner/skills_loader.py (catalogue line format);
    # platform/teamtrack/harness/instructions/.agents/skills/add-endpoint/ (SKILL.md 100 lines,
    # references/tests.md 57 lines); concepts.md tier table; docs/evidence/s1.md (what each arm
    # read).
    @diagram(S1, "skills-three-tiers", canvas="strip")
    def skills_three_tiers(s: Scene) -> None:
        bottom = 480
        s.box(600, 60, 1260, 600, dashed=True)
        s.text(630, 76, "On disk", T, INK)
        t1 = s.box(60, bottom - 130, 420, 130, "Tier 1: add-endpoint\ndescription", role="harness")
        s.text(270, bottom - 200, "always in context", B, INK, "center")
        t2 = s.box(700, bottom - 230, 480, 230, "Tier 2: SKILL.md,\n100 lines", role="plain")
        t3 = s.box(
            1340, bottom - 330, 480, 330, "Tier 3: tests.md,\n57 lines", role="plain", dashed=True
        )
        s.arrow(t1, t2, start="right", end="left", end_off=50, color=BLUE)
        s.arrow(t2, t3, start="right", end="left", start_off=50, end_off=100, color=BLUE)
        s.text(930, bottom + 30, "loaded when picked", B, INK, "center")
        s.text(930, bottom + 80, "all 3 arms read it", B, INK, "center")
        s.text(1570, bottom + 30, "when a step needs it", B, INK, "center")
        s.text(1570, bottom + 80, "none opened it", B, INK, "center")

    # Sources: harness/instructions/router.py build_prefix (usage sentence, the map with two
    # walkthrough lines stripped, the skills catalogue); runner/loop.py base_items (core prompt
    # first, in the developer message); runner/skills_loader.py (catalogue = tier 1 only).
    @diagram(S1, "context-prefix", canvas="strip")
    def context_prefix(s: Scene) -> None:
        s.box(60, 60, 1000, 600, dashed=True)
        s.text(90, 76, "First message, every session", B, INK)
        blocks = [
            ("Core prompt: both arms", "neutral"),
            ("Usage sentence", "harness"),
            ("AGENTS.md map, 92 lines", "harness"),
            ("Skills catalogue: tier 1", "harness"),
        ]
        stack = []
        for i, (label, role) in enumerate(blocks):
            stack.append(s.box(100, 130 + i * 112, 920, 92, label, role=role, align="left"))
        s.text(560, 590, "blocks 2-4: harness arm only", B, INK, "center")
        s.text(1600, 200, "On disk, not sent", T, INK, "center")
        docs = s.box(1340, 300, 520, 120, "Docs the map names", role="plain")
        bodies = s.box(1340, 460, 520, 120, "SKILL.md bodies", role="plain")
        s.arrow(stack[2], docs, "read_file", start="right", end="left", start_off=-40)
        s.arrow(stack[3], bodies, "read_file", start="right", end="left", start_off=8)

    # Sources: platform/src/shipharness/harness/state/handoff.py (MachineSummary.render: commits,
    # files changed, tests, migration heads; the two headings; merge keeps the agent's part);
    # state/lifecycle.py (wrap-up text: what the notes hold).
    @diagram(S2, "handoff-contents", canvas="strip")
    def handoff_contents(s: Scene) -> None:
        s.box(560, 60, 840, 540, role="neutral")
        s.text(980, 76, "session-handoff.md", T, INK, "center")
        mach = s.box(590, 140, 780, 200, role="harness")
        s.text(980, 185, "Machine summary, from git", B, INK, "center")
        s.text(980, 255, "commits, files, tests, heads", B, INK, "center")
        notes = s.box(590, 370, 780, 200, role="plain")
        s.text(980, 415, "Notes from the agent", B, INK, "center")
        s.text(980, 485, "doing, left, watch out", B, INK, "center")
        harness = s.box(60, 170, 340, 140, "Harness,\nat each stop", role="harness")
        agent = s.box(60, 400, 340, 140, "Agent, in\nwrap-up turns", role="plain")
        s.arrow(harness, mach, "writes", start="right", end="left", color=BLUE)
        s.arrow(agent, notes, "writes", start="right", end="left")
        nxt = s.box(1540, 285, 320, 140, "Next session\nreads it first", role="plain")
        s.arrow(mach, nxt, start="right", end="left", end_off=-30, color=BLUE)
        s.arrow(notes, nxt, start="right", end="left", end_off=30)

    # Sources: section-2-state-lifecycle/demo/harness/init.sh (alembic heads, upgrade head, a
    # basic test); docs/evidence/s2.md (session 2's first calls; 0002_comments.py);
    # harness/state/handoff.py ("exactly one" head); concepts.md (House rule 7: Migrations).
    @diagram(S2, "alembic-heads", canvas="strip")
    def alembic_heads(s: Scene) -> None:
        s.text(250, 230, "Session 2, first call", B, INK, "center")
        read = s.box(60, 290, 380, 140, "git log;\ncat progress.md", role="neutral")
        s.text(760, 230, "then bash init.sh", B, INK, "center")
        init = s.box(570, 290, 380, 140, "alembic heads,\nupgrade, test", role="plain")
        one = s.box(1100, 90, 360, 140, "One head:\n0001, then 0002", role="harness")
        ok = s.box(1560, 90, 300, 140, "init.sh passes,\nthen code", role="harness")
        two = s.box(1100, 490, 360, 140, "Two heads:\ntwo 0002 migrations", role="accent")
        bad = s.box(
            1520, 490, 340, 140, "House rule 7:\nMigrations fails", role="fail", stroke_width=BOLD
        )
        s.arrow(read, init, start="right", end="left")
        s.arrow(init, one, start="right", end="left")
        s.arrow(init, two, start="right", end="left")
        s.arrow(one, ok, start="right", end="left")
        s.arrow(two, bad, start="right", end="left")

    # Sources: harness/scope/guard.py (reason(path): the phase's allowed paths);
    # harness/scope/layer.py (before_tool blocks a patch before anything is written; after_tool
    # restores stray files from a byte snapshot after a command).
    @diagram(S3, "scope-check-flow", canvas="strip")
    def scope_check_flow(s: Scene) -> None:
        call = s.box(60, 280, 320, 140, "Agent tool call", role="plain")
        check = s.box(470, 200, 560, 300, "Path allowed\nin this phase?", shape="diamond")
        ok = s.box(1240, 70, 620, 130, "Workspace:\nchange kept", role="harness")
        blocked = s.box(1240, 285, 620, 130, "Patch: BLOCKED,\nnothing written", role="fail")
        reverted = s.box(1240, 505, 620, 130, "Command: REVERTED\nfrom snapshot", role="fail")
        s.arrow(call, check, start="right", end="left")
        s.arrow(check, ok, "yes", start="top", end="left", via=[(750, 135), (990, 135)])
        s.arrow(check, blocked, "no", start="right", end="left")
        s.arrow(check, reverted, "no", start="bottom", end="left", via=[(750, 570), (990, 570)])

    # Sources: platform/sandbox/README.md; platform/src/shipharness/sandbox/policy.py;
    # section-3-scope-sandbox/concepts.md (the flags table: --network none, read-only root,
    # /work and /tmp writable); .env.example (the keys stay on the host).
    @diagram(S3, "sandbox-boundary", canvas="strip")
    def sandbox_boundary(s: Scene) -> None:
        s.box(60, 60, 1360, 600, role="plain")
        s.text(90, 76, "Host: your machine", B, INK)
        loop = s.box(100, 190, 380, 130, "Agent loop\nand harness", role="plain")
        s.box(100, 420, 380, 150, "API keys:\nhere, in .env", role="accent", stroke_width=BOLD)
        s.box(760, 130, 620, 500, role="neutral", stroke_width=BOLD)
        s.text(1070, 146, "Sandbox: one per arm", B, INK, "center")
        work = s.box(800, 200, 540, 110, "/work, /tmp: writable", role="plain")
        s.box(800, 340, 540, 110, "root: read-only", role="plain")
        net = s.box(800, 480, 540, 110, "network: none", role="fail")
        s.arrow(loop, work, "tool commands", start="right", end="left")
        web = s.box(1600, 475, 260, 120, "The internet", dashed=True)
        s.arrow(net, web, "blocked", start="right", end="left", color=RED, dashed=True)

    # Sources: harness/scope/guard.py and layer.py (allowed paths per phase; the "blocked"
    # event, harness arm only); platform/src/shipharness/sandbox/policy.py and events/models.py
    # (the "sandbox_denied" event, both arms); platform/sandbox/README.md (identical containers).
    @diagram(S3, "least-privilege", canvas="strip")
    def least_privilege(s: Scene) -> None:
        s.box(60, 60, 1800, 600, role="neutral")
        s.text(100, 320, "Container limits:\nboth arms", B, INK)
        s.box(1260, 85, 570, 90, "sandbox_denied: possible at all?", role="fail")
        s.box(480, 200, 1350, 430, role="harness")
        s.text(520, 380, "Phase's allowed paths:\nharness arm", B, INK)
        s.box(1320, 225, 480, 90, "blocked: in scope now?", role="fail")
        s.box(920, 340, 880, 260, "The one feature", role="plain", stroke_width=BOLD)

    # Sources: platform/teamtrack/mutants/features/f4.jsonl (app.services.issues-m401:
    # app/services/issues.py line 54, set "referee"; the "filter" set feeds Filter 3);
    # section-4-verification/concepts.md (the two sets share no mutation).
    @diagram(S4, "mutation-testing", canvas="strip")
    def mutation_testing(s: Scene) -> None:
        orig = s.box(60, 90, 440, 160, "Original\nissue.version += 1", role="plain")
        mut = s.box(780, 90, 440, 160, "Mutant\nissue.version += 0", role="accent")
        s.arrow(orig, mut, "plant one fault", start="right", end="left")
        caught = s.box(
            1420,
            60,
            440,
            130,
            "Shipped test fails:\nmutant caught",
            role="harness",
            stroke_width=BOLD,
        )
        survived = s.box(
            1420,
            210,
            440,
            130,
            "Shipped test passes:\nmutant survived",
            role="fail",
            stroke_width=BOLD,
        )
        s.arrow(mut, caught, start="right", end="left", start_off=-35)
        s.arrow(mut, survived, start="right", end="left", start_off=35)
        s.box(60, 470, 640, 150, "Filter set:\nfeeds Filter 3", role="neutral")
        s.text(960, 510, "no shared\nmutation", B, INK, "center")
        s.box(1220, 470, 640, 150, "Referee set:\nscores the run", role="neutral")

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
    # layer holds); platform/sandbox/README.md (tool commands run in the sandbox, both arms);
    # section-4-verification/concepts.md (the referee scores the shipped diff).
    @diagram(DOCS, "harness-one-picture", canvas="strip")
    def harness_one_picture(s: Scene) -> None:
        ins = s.box(60, 80, 420, 160, "Instructions:\nwhat it knows", role="harness")
        st = s.box(60, 480, 420, 160, "State:\nwhat it remembers", role="harness")
        model = s.box(570, 280, 300, 160, "Model", shape="ellipse", role="plain")
        sc = s.box(940, 60, 460, 130, "Scope:\nwhat it may change", role="harness")
        # One box for the tools and the sandbox (dashed = the sandbox): 7 boxes in all.
        tools = s.box(980, 250, 380, 220, "Tools in sandbox:\nboth arms", dashed=True, role="plain")
        ve = s.box(940, 530, 460, 130, "Verification:\nwhat proves done", role="harness")
        ref = s.box(1540, 280, 320, 160, "Referee: hidden\ntests, mutants", role="plain")
        s.arrow(model, tools, start="right", end="left", start_off=-20, end_off=-20)
        s.arrow(tools, model, start="left", end="right", start_off=20, end_off=20)
        s.arrow(ins, model, start="right", end="left", end_off=-30, color=BLUE)
        s.arrow(st, model, start="right", end="left", end_off=30, color=BLUE)
        s.arrow(sc, tools, start="bottom", end="top", color=BLUE)
        s.arrow(model, ve, "claims done", start="bottom", end="left", via=[(720, 595), (800, 595)])
        s.arrow(tools, ref, "diff", start="right", end="left")

    # Sources: docs/STYLE.md (the four failures); the four section concepts.md pages; slides
    # (slide 70 notes: scope is the only measured gap, on Feature 4).
    @diagram(DOCS, "which-layer-when", canvas="strip")
    def which_layer_when(s: Scene) -> None:
        symptoms = [
            "Broke a written rule",
            "New session redid work",
            "Edits outside the ticket",
            "Said done, not done",
        ]
        layers = [
            "Instructions: a map",
            "State: files and git",
            "Scope: enforced paths",
            "Verification: check with code",
        ]
        # The failures are plain text, the layers boxes: 4 layer boxes and the gap tag, 5 boxes.
        for i in range(4):
            y = 60 + i * 155
            cy = y + 135 / 2
            s.text(620, cy - B * 0.65, symptoms[i], B, INK, "right")
            b = s.box(780, y, 600, 135, layers[i], role="harness")
            s.path([(645, cy), (768, cy)], color=BLUE)
            if i == 2:
                gap = s.box(1460, y + 20, 400, 95, "Measured gap: Feature 4", role="accent")
                s.arrow(b, gap, start="right", end="left", color=AMBER, dashed=True)
