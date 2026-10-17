"""The five step-by-step diagrams: each `s.stage = N` starts the element that frame N adds."""

from __future__ import annotations

from exlib import AMBER, BLUE, GREY, INK, Scene, tint


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Sources: platform/src/shipharness/runner/prompts.py (the tools, finish(claim=...)),
    # runner/loop.py (one turn = one model call; a done claim ends the phase in the bare arm).
    @diagram(DOCS, "agent-loop", steps=True)
    def agent_loop(s: Scene) -> None:
        s.stage = 1
        ticket = s.box(40, 290, 220, 110, "Ticket", fill=tint(INK, "10"))
        model = s.box(
            440, 260, 280, 170, "Model\nreads the context,\npicks the next step", shape="ellipse"
        )
        s.arrow(ticket, model, "context", start="right", end="left")
        s.stage = 2
        tools = s.box(
            960,
            260,
            400,
            170,
            "Tools\nlist_dir, read_file, search,\napply_patch, run,\nrun_visible_tests, finish",
        )
        s.arrow(model, tools, "tool call", start="right", end="left", start_off=-40, end_off=-40)
        s.stage = 3
        s.arrow(tools, model, "result", start="left", end="right", start_off=40, end_off=40)
        s.text(840, 450, "one turn = one model call; repeat", 20, INK, "center")
        s.stage = 4
        repo = s.box(960, 560, 400, 110, "Repository\nthe agent's workspace")
        s.arrow(tools, repo, "reads and changes files", start="bottom", end="top", both=True)
        s.stage = 5
        done = s.box(
            380,
            560,
            400,
            130,
            "The phase ends\non the agent's own word",
            stroke=AMBER,
            fill=tint(AMBER, "33"),
            stroke_width=3,
        )
        s.arrow(
            model,
            done,
            'finish(claim="done")',
            start="bottom",
            end="top",
            color=INK,
            label_color=INK,
        )

    # Sources: harness/decisions.py (layers: instructions, state, scope, verify);
    # docs/STYLE.md (layer names); platform/sandbox/README.md (both arms, identical).
    @diagram(DOCS, "harness-around-loop", steps=True)
    def harness_around_loop(s: Scene) -> None:
        s.stage = 1
        model = s.box(560, 330, 230, 120, "Model", shape="ellipse")
        tools = s.box(960, 330, 230, 120, "Tools")
        s.arrow(model, tools, "tool call", start="right", end="left", start_off=-25, end_off=-25)
        s.arrow(tools, model, "result", start="left", end="right", start_off=25, end_off=25)
        done = s.box(
            560, 600, 230, 90, 'finish(claim="done")', stroke=AMBER, fill=tint(AMBER, "33")
        )
        s.arrow(model, done, start="bottom", end="top")
        s.stage = 2
        ins = s.box(
            60,
            90,
            400,
            140,
            "Instructions\nwhat the agent knows:\nmap, docs, skills",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(ins, model, "in the context", start="bottom", end="left", end_off=-30, color=BLUE)
        s.stage = 3
        st = s.box(
            60,
            560,
            400,
            140,
            "State and lifecycle\nwhat it remembers:\nprogress, handoff, git",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(st, model, "at session start", start="top", end="left", end_off=30, color=BLUE)
        s.stage = 4
        sc = s.box(
            1290,
            90,
            400,
            140,
            "Scope\nwhat it may change:\nallowed paths per phase",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(sc, tools, "checks each call", start="bottom", end="right", color=BLUE)
        s.stage = 5
        ve = s.box(
            1290,
            560,
            400,
            140,
            "Verification\nwhat proves done:\ngate, test filters",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(ve, done, "checks the claim", start="left", end="right", color=BLUE)
        s.stage = 6
        s.box(920, 250, 310, 250, dashed=True, stroke=INK)
        s.text(1075, 262, "Sandbox", 22, INK, "center")
        s.text(1075, 520, "the same container\nfor both arms", 20, INK, "center")

    # Sources: section-2-state-lifecycle/concepts.md; harness/state/lifecycle.py (wrap-up text,
    # getting up to speed, the harness commit); harness/state/handoff.py (the two parts);
    # runner/prompts.py ("This session is ending soon."); docs/evidence/s2.md (12-turn session 1).
    @diagram(S2, "session-lifecycle", steps=True)
    def session_lifecycle(s: Scene) -> None:
        s.stage = 1
        s1 = s.box(40, 200, 360, 200, "Session 1\nempty context\nget up to speed,\nwork, commit")
        s.stage = 2
        stop = s.box(
            520,
            220,
            300,
            160,
            "Turn budget reached\n(12 turns)\nthe runner stops\nthe session",
            stroke=AMBER,
            fill=tint(AMBER, "33"),
            stroke_width=3,
        )
        s.arrow(s1, stop, start="right", end="left")
        s.text(
            220,
            430,
            'Near the end: "This session\nis ending soon." The agent\nwrites notes and commits.',
            20,
            INK,
            "center",
        )
        s.stage = 3
        ho = s.box(
            1010,
            160,
            400,
            280,
            "session-handoff.md\n\nMachine summary\n(the harness, at the stop)\n\n"
            "Notes from the agent\n(its wrap-up turns)",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(stop, ho, "harness writes\nand commits", start="right", end="left", color=BLUE)
        s.text(1210, 460, "also progress.md, the exec plan,\nand the git log", 20, INK, "center")
        s.stage = 4
        s2 = s.box(
            1560, 200, 360, 200, "Session 2\nempty context\nreads the handoff,\nthen continues"
        )
        s.arrow(ho, s2, "read first", start="right", end="left", color=BLUE)

    # Sources: section-4-verification/concepts.md (the flow and the five filters);
    # harness/verify/gate.py and verify/layer.py (gate items, "first three failures").
    @diagram(S4, "verification-pipeline", steps=True)
    def verification_pipeline(s: Scene) -> None:
        s.stage = 1
        agent = s.box(
            40,
            170,
            360,
            150,
            'Agent, build phase\nsays done:\nfinish(claim="done")',
            stroke=AMBER,
            fill=tint(AMBER, "33"),
            stroke_width=3,
        )
        s.stage = 2
        gate = s.box(
            540,
            150,
            420,
            190,
            "Verify gate\nin the arm's container:\nvisible tests, existing tests,\n"
            "R1-R7, board, clean state",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(agent, gate, start="right", end="left")
        s.arrow(
            gate,
            agent,
            "refused: first 3 failures,\nthe phase continues",
            start="top",
            end="top",
            via=[(750, 60), (220, 60)],
            color=BLUE,
        )
        s.stage = 3
        test = s.box(
            1240,
            170,
            360,
            150,
            "Agent, test phase\nwrites tests\nfor the feature",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(gate, test, "passed", start="right", end="left")
        s.stage = 4
        filt = s.box(
            1180,
            470,
            480,
            210,
            "Five test filters\n1 collects  2 passes 5 runs\n"
            "3 adds coverage or kills a mutant\n4 real assertions\n"
            "5 no source file changed",
            stroke=BLUE,
            fill=tint(BLUE),
        )
        s.arrow(test, filt, "proposed tests", start="bottom", end="top")
        s.stage = 5
        ref = s.box(
            540,
            480,
            420,
            190,
            "Referee\nits own container,\nafter the agent stops:\nhidden tests, referee mutants",
        )
        s.arrow(filt, ref, "kept tests", start="left", end="right")
        s.stage = 6
        verdict = s.box(
            40,
            505,
            360,
            140,
            "Primary verdict\nPASS or FAIL",
            stroke=INK,
            fill=tint(AMBER, "33"),
            stroke_width=3,
        )
        s.arrow(ref, verdict, start="left", end="right")

    # Sources: docs/STYLE.md (A/B, bare arm, harness arm, referee); platform/sandbox/README.md
    # (identical containers); .env.example (OPENAI_MODEL, MAX_RUN_COST_USD).
    @diagram(DOCS, "ab-referee", steps=True)
    def ab_referee(s: Scene) -> None:
        s.stage = 1
        ticket = s.box(610, 40, 380, 100, "One ticket", fill=tint(INK, "10"))
        s.stage = 2
        bare = s.box(
            120,
            260,
            460,
            170,
            "Bare arm\nticket + repository,\nno harness",
            stroke=GREY,
            fill=tint(GREY, "33"),
            stroke_width=3,
        )
        s.arrow(ticket, bare, start="left", end="top", via=[(350, 90)], color=GREY)
        s.stage = 3
        harn = s.box(
            1020,
            260,
            460,
            170,
            "Harness arm\nthe same run,\nharness turned on",
            stroke=BLUE,
            fill=tint(BLUE),
            stroke_width=3,
        )
        s.arrow(ticket, harn, start="right", end="top", via=[(1250, 90)], color=BLUE)
        s.stage = 4
        s.box(620, 240, 360, 210, "The same for both:\nmodel, tools,\nsandbox, caps", dashed=True)
        s.stage = 5
        ref = s.box(
            560, 560, 480, 150, "One referee\nscores both arms the same way\nafter the agents stop"
        )
        s.arrow(bare, ref, "shipped diff", start="bottom", end="left", via=[(350, 635)], color=GREY)
        s.arrow(
            harn, ref, "shipped diff", start="bottom", end="right", via=[(1250, 635)], color=BLUE
        )
        s.stage = 6
        vb = s.box(400, 800, 300, 90, "Bare: one dot", stroke=GREY, fill=tint(GREY, "33"))
        vh = s.box(900, 800, 300, 90, "Harness: one dot", stroke=BLUE, fill=tint(BLUE))
        s.arrow(ref, vb, start="bottom", end="top", start_off=-80, color=GREY)
        s.arrow(ref, vh, start="bottom", end="top", start_off=80, color=BLUE)
