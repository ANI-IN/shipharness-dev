"""The five step-by-step diagrams: each `s.stage = N` starts the element that frame N adds.

Coordinates are canvas units of a "wide" canvas (1920x1080); style comes from style.py. Labels
are 5 words at most; the slide notes carry the explanation.
"""

from __future__ import annotations

from exlib import BLUE, GREY, INK, Scene
from style import STROKE_WIDTH_BOLD as BOLD


def register(diagram, DOCS, S1, S2, S3, S4):  # noqa: N803
    # Sources: platform/src/shipharness/runner/prompts.py (the tools, finish(claim=...)),
    # runner/loop.py (one turn = one model call; a done claim ends the phase in the bare arm).
    @diagram(DOCS, "agent-loop", steps=True)
    def agent_loop(s: Scene) -> None:
        s.stage = 1
        ticket = s.box(60, 380, 260, 140, "Ticket", role="neutral")
        model = s.box(500, 330, 440, 240, "Model\npicks next step", shape="ellipse")
        s.arrow(ticket, model, "context", start="right", end="left")
        s.stage = 2
        tools = s.box(1240, 330, 560, 240, "Tools\nread, search, patch, run", role="plain")
        s.arrow(model, tools, "tool call", start="right", end="left", start_off=-50, end_off=-50)
        s.stage = 3
        s.arrow(tools, model, "result", start="left", end="right", start_off=50, end_off=50)
        s.text(1090, 600, "one turn, one model call", 28, INK, "center")
        s.stage = 4
        repo = s.box(1240, 790, 560, 150, "Repository\nthe agent's workspace", role="plain")
        s.arrow(tools, repo, "reads, changes files", start="bottom", end="top", both=True)
        s.stage = 5
        done = s.box(
            440, 790, 560, 150, "Phase ends on\nits word", role="accent", stroke_width=BOLD
        )
        s.arrow(model, done, 'finish(claim="done")', start="bottom", end="top")

    # Sources: harness/decisions.py (layers: instructions, state, scope, verify);
    # docs/STYLE.md (layer names); platform/sandbox/README.md (both arms, identical).
    @diagram(DOCS, "harness-around-loop", steps=True)
    def harness_around_loop(s: Scene) -> None:
        s.stage = 1
        model = s.box(560, 420, 280, 160, "Model", shape="ellipse")
        tools = s.box(1030, 420, 260, 160, "Tools", role="plain")
        s.arrow(model, tools, "tool call", start="right", end="left", start_off=-35, end_off=-35)
        s.arrow(tools, model, "result", start="left", end="right", start_off=35, end_off=35)
        done = s.box(530, 820, 340, 110, 'finish(claim="done")', role="accent")
        s.arrow(model, done, start="bottom", end="top")
        s.stage = 2
        ins = s.box(60, 70, 460, 200, "Instructions\nwhat it knows", role="harness")
        s.arrow(ins, model, "in the context", start="bottom", end="left", end_off=-40, color=BLUE)
        s.stage = 3
        st = s.box(60, 780, 460, 200, "State\nwhat it remembers", role="harness")
        s.arrow(st, model, "at session start", start="top", end="left", end_off=40, color=BLUE)
        s.stage = 4
        sc = s.box(1400, 70, 460, 200, "Scope\nwhat it may change", role="harness")
        s.arrow(sc, tools, "checks each call", start="bottom", end="right", color=BLUE)
        s.stage = 5
        ve = s.box(1400, 780, 460, 200, "Verification\nwhat proves done", role="harness")
        s.arrow(ve, done, "checks the claim", start="left", end="right", color=BLUE)
        s.stage = 6
        s.box(980, 320, 360, 400, dashed=True)
        s.text(1160, 336, "Sandbox", 28, INK, "center")
        s.text(1160, 630, "same for both arms", 28, INK, "center")

    # Sources: section-2-state-lifecycle/concepts.md; harness/state/lifecycle.py (wrap-up text,
    # getting up to speed, the harness commit); harness/state/handoff.py (the two parts);
    # runner/prompts.py ("This session is ending soon."); docs/evidence/s2.md (12-turn session 1).
    @diagram(S2, "session-lifecycle", steps=True)
    def session_lifecycle(s: Scene) -> None:
        s.stage = 1
        s1 = s.box(60, 140, 440, 240, "Session 1:\nget going, work", role="plain")
        s.stage = 2
        stop = s.box(640, 140, 420, 240, "Stopped at\n12 turns", role="accent", stroke_width=BOLD)
        s.arrow(s1, stop, start="right", end="left")
        s.text(280, 440, "warned: notes,\nthen commit", 28, INK, "center")
        s.stage = 3
        ho = s.box(
            1320,
            100,
            540,
            320,
            "session-handoff.md\nharness summary,\nagent notes",
            role="harness",
        )
        s.arrow(stop, ho, "harness writes\nand commits", start="right", end="left", color=BLUE)
        s.text(1250, 560, "also progress.md,\nplan, git log", 28, INK, "right")
        s.stage = 4
        s2 = s.box(1320, 700, 540, 240, "Session 2:\nreads handoff first", role="plain")
        s.arrow(ho, s2, "read first", start="bottom", end="top", color=BLUE)

    # Sources: section-4-verification/concepts.md (the flow and the five filters);
    # harness/verify/gate.py and verify/layer.py (gate items, "first three failures").
    @diagram(S4, "verification-pipeline", steps=True)
    def verification_pipeline(s: Scene) -> None:
        s.stage = 1
        agent = s.box(
            60,
            210,
            440,
            200,
            'Build phase:\nfinish(claim="done")',
            role="accent",
            stroke_width=BOLD,
        )
        s.stage = 2
        gate = s.box(680, 180, 520, 260, "Verify gate:\ntests, rules, state", role="harness")
        s.arrow(agent, gate, start="right", end="left")
        s.arrow(
            gate,
            agent,
            "refused: first 3 failures",
            start="top",
            end="top",
            via=[(940, 90), (280, 90)],
            color=BLUE,
        )
        s.stage = 3
        test = s.box(1420, 210, 440, 200, "Test phase\nwrites tests", role="harness")
        s.arrow(gate, test, "passed", start="right", end="left")
        s.stage = 4
        filt = s.box(1360, 640, 500, 300, "Five test filters", role="harness")
        s.arrow(test, filt, "proposed tests", start="bottom", end="top")
        s.stage = 5
        ref = s.box(680, 640, 460, 300, "Referee: hidden tests,\nreferee mutants", role="plain")
        s.arrow(filt, ref, "kept tests", start="left", end="right")
        s.stage = 6
        verdict = s.box(
            60,
            700,
            420,
            180,
            "Primary verdict\nPASS or FAIL",
            role="accent",
            stroke=INK,
            stroke_width=BOLD,
        )
        s.arrow(ref, verdict, start="left", end="right")

    # Sources: docs/STYLE.md (A/B, bare arm, harness arm, referee); platform/sandbox/README.md
    # (identical containers); .env.example (OPENAI_MODEL, MAX_RUN_COST_USD).
    @diagram(DOCS, "ab-referee", steps=True)
    def ab_referee(s: Scene) -> None:
        s.stage = 1
        ticket = s.box(710, 60, 500, 110, "One ticket", role="neutral")
        s.stage = 2
        bare = s.box(100, 290, 520, 210, "Bare arm\nno harness", role="bare", stroke_width=BOLD)
        s.arrow(ticket, bare, start="left", end="top", via=[(360, 115)], color=GREY)
        s.stage = 3
        harn = s.box(
            1300, 290, 520, 210, "Harness arm\nharness on", role="harness", stroke_width=BOLD
        )
        s.arrow(ticket, harn, start="right", end="top", via=[(1560, 115)], color=BLUE)
        s.stage = 4
        s.box(720, 280, 480, 230, "Same model, tools,\nsandbox, caps", dashed=True)
        s.stage = 5
        ref = s.box(640, 620, 640, 180, "One referee\nscores both arms", role="plain")
        s.arrow(bare, ref, "shipped diff", start="bottom", end="left", via=[(360, 710)], color=GREY)
        s.arrow(
            harn, ref, "shipped diff", start="bottom", end="right", via=[(1560, 710)], color=BLUE
        )
        s.stage = 6
        vb = s.box(430, 900, 360, 110, "Bare: one dot", role="bare")
        vh = s.box(1130, 900, 360, 110, "Harness: one dot", role="harness")
        s.arrow(ref, vb, start="bottom", end="top", start_off=-100, color=GREY)
        s.arrow(ref, vh, start="bottom", end="top", start_off=100, color=BLUE)
