"""The five step-by-step diagrams: each `s.stage = N` starts the element that frame N adds.

Coordinates are canvas units of the canvas named in each @diagram ("wide" 1920x1080 or
"strip" 1920x720); style comes from style.py. Labels
are 5 words at most; the slide notes carry the explanation.
"""

from __future__ import annotations

from exlib import BLUE, GREY, INK, RED, Scene
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
    # Strip canvas: the loop in the middle, one layer in each corner; the box sub-labels say what
    # each layer touches, so the layer arrows carry no labels.
    @diagram(DOCS, "harness-around-loop", steps=True, canvas="strip")
    def harness_around_loop(s: Scene) -> None:
        s.stage = 1
        model = s.box(510, 240, 290, 170, "Model", shape="ellipse")
        tools = s.box(1170, 250, 190, 150, "Tools", role="plain")
        s.arrow(model, tools, "tool call", start="right", end="left", start_off=-35, end_off=-35)
        s.arrow(tools, model, "result", start="left", end="right", start_off=35, end_off=35)
        done = s.box(475, 520, 360, 110, 'finish(claim="done")', role="accent")
        s.arrow(model, done, start="bottom", end="top")
        s.stage = 2
        ins = s.box(60, 60, 400, 170, "Instructions\nwhat it knows", role="harness")
        s.arrow(ins, model, start="bottom", end="left", end_off=-30, via=[(260, 295)], color=BLUE)
        s.stage = 3
        st = s.box(60, 490, 400, 170, "State\nwhat it remembers", role="harness")
        s.arrow(st, model, start="top", end="left", end_off=30, via=[(260, 355)], color=BLUE)
        s.stage = 4
        sc = s.box(1460, 60, 400, 170, "Scope\nwhat it may change", role="harness")
        s.arrow(sc, tools, start="bottom", end="right", via=[(1660, 325)], color=BLUE)
        s.stage = 5
        ve = s.box(1460, 490, 400, 170, "Verification\nwhat proves done", role="harness")
        s.arrow(ve, done, start="left", end="right", start_off=0, color=BLUE)
        s.stage = 6
        s.box(1100, 150, 330, 340, dashed=True)
        s.text(1265, 164, "Sandbox", 28, INK, "center")
        s.text(1265, 432, "same for both arms", 28, INK, "center")

    # Sources: section-2-state-lifecycle/concepts.md; harness/state/lifecycle.py (wrap-up text,
    # getting up to speed, the harness commit); harness/state/handoff.py (the two parts);
    # runner/prompts.py ("This session is ending soon."); docs/evidence/s2.md (12-turn session 1).
    # Strip canvas: session 1 and the stop on the left, the handoff and session 2 stacked right.
    @diagram(S2, "session-lifecycle", steps=True, canvas="strip")
    def session_lifecycle(s: Scene) -> None:
        s.stage = 1
        s1 = s.box(60, 130, 400, 200, "Session 1:\nget going, work", role="plain")
        s.stage = 2
        stop = s.box(560, 130, 340, 200, "Stopped at\n12 turns", role="accent", stroke_width=BOLD)
        s.arrow(s1, stop, start="right", end="left")
        s.text(260, 390, "warned: notes,\nthen commit", 28, INK, "center")
        s.stage = 3
        ho = s.box(
            1260,
            130,
            600,
            200,
            "session-handoff.md:\nharness facts, agent notes",
            role="harness",
        )
        s.arrow(stop, ho, "harness writes,\ncommits", start="right", end="left", color=BLUE)
        s.text(1180, 520, "also progress.md,\nplan, git log", 28, INK, "right")
        s.stage = 4
        s2 = s.box(1260, 480, 600, 180, "Session 2:\nreads handoff first", role="plain")
        s.arrow(ho, s2, "read first", start="bottom", end="top", color=BLUE)

    # Sources: section-4-verification/concepts.md (the flow, the five filters, the referee);
    # harness/verify/gate.py and verify/layer.py (gate items, "first three failures");
    # platform/src/shipharness/filters/filters.py (Filter 1 to Filter 5 run; there is no sixth).
    # Strip canvas, three bands, one per slide: frame 1 the build phase grading itself (slide 60),
    # frame 2 the test phase and its filters (slide 61), frame 3 the verify gate between the claim
    # and the test phase, then the referee and the verdict (slide 63). The test phase has no
    # incoming arrow until frame 3 adds the gate, so no frame shows a path that later changes.
    @diagram(S4, "verification-pipeline", steps=True, canvas="strip")
    def verification_pipeline(s: Scene) -> None:
        s.stage = 1
        build = s.box(60, 60, 840, 130, "Build phase:\ncode, visible tests", role="plain")
        claim = s.box(1360, 60, 500, 130, 'finish(claim="done")', role="accent", stroke_width=BOLD)
        s.arrow(build, claim, "own tests pass", start="right", end="left")
        s.stage = 2
        test = s.box(700, 330, 460, 130, "Test phase:\nproposes tests", role="harness")
        filt = s.box(60, 330, 500, 130, "Five test filters", role="harness")
        s.arrow(test, filt, start="left", end="right")
        s.stage = 3
        gate = s.box(1360, 330, 500, 130, "Verify gate:\ntests, rules, state", role="harness")
        s.arrow(claim, gate, start="bottom", end="top", start_off=80, end_off=80)
        s.arrow(
            gate,
            build,
            "refused: first 3 failures",
            start="top",
            end="bottom",
            start_off=-170,
            end_off=220,
            via=[(1440, 260), (700, 260)],
            color=RED,
        )
        s.arrow(gate, test, "passed", start="left", end="right")
        ref = s.box(60, 560, 500, 130, "Referee: hidden tests,\nreferee mutants", role="plain")
        s.arrow(filt, ref, "kept tests", start="bottom", end="top")
        verdict = s.box(
            700,
            560,
            460,
            130,
            "Primary verdict\nPASS or FAIL",
            role="accent",
            stroke=INK,
            stroke_width=BOLD,
        )
        s.arrow(ref, verdict, start="right", end="left")

    # Sources: docs/STYLE.md (A/B, bare arm, harness arm, referee); platform/sandbox/README.md
    # (identical containers); .env.example (OPENAI_MODEL, MAX_RUN_COST_USD).
    # Strip canvas: read left to right, ticket -> two arms -> one referee -> one dot per arm.
    @diagram(DOCS, "ab-referee", steps=True, canvas="strip")
    def ab_referee(s: Scene) -> None:
        s.stage = 1
        ticket = s.box(60, 300, 280, 120, "One ticket", role="neutral")
        s.stage = 2
        bare = s.box(480, 70, 440, 170, "Bare arm\nno harness", role="bare", stroke_width=BOLD)
        s.arrow(ticket, bare, start="top", end="left", via=[(200, 155)], color=GREY)
        s.stage = 3
        harn = s.box(
            480, 480, 440, 170, "Harness arm\nharness on", role="harness", stroke_width=BOLD
        )
        s.arrow(ticket, harn, start="bottom", end="left", via=[(200, 565)], color=BLUE)
        s.stage = 4
        s.box(480, 280, 440, 160, "Same model, tools,\nsandbox, caps", dashed=True)
        s.stage = 5
        ref = s.box(1060, 280, 380, 160, "One referee\nscores both arms", role="plain")
        s.arrow(
            bare,
            ref,
            "shipped diff",
            start="right",
            end="top",
            via=[(1000, 155), (1250, 155)],
            color=GREY,
        )
        s.arrow(
            harn,
            ref,
            "shipped diff",
            start="right",
            end="bottom",
            via=[(1000, 565), (1250, 565)],
            color=BLUE,
        )
        s.stage = 6
        vb = s.box(1580, 200, 280, 100, "Bare: one dot", role="bare")
        vh = s.box(1580, 420, 280, 100, "Harness: one dot", role="harness")
        s.arrow(ref, vb, start="right", end="left", start_off=-40, color=GREY)
        s.arrow(ref, vh, start="right", end="left", start_off=40, color=BLUE)
