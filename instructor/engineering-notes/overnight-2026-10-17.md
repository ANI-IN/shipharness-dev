OVERNIGHT RUN — work autonomously until done or until a stop condition. I'm asleep: do NOT ask me questions or wait for approval. Where a decision is needed, apply the rules below, record the decision and your reason in VERIFICATION.md, and continue. Report everything in chat in one morning summary (format at the end).

## Hard limits (never cross)
- Money: build total ≤ $15 (MAX_BUILD_TOTAL_USD); pilot ≤ $10 and ≤ 96 arm runs; experiments within what's left of $15. Before any batch, project its cost; if it would cross a limit, skip it and note why.
- LangSmith: stay under 2,500 traces this month.
- Never: publish anything public, touch or delete ANI-IN/harness-engineering-session, rename repos, rewrite git history, change anything on Windows, delete backups, commit .env or keys, add attribution lines. Single ANI-IN identity.
- You may push to the private repo (shipharness-dev) after each phase.
- If something fails 3 times in a row for the same reason (sandbox, Docker, API), stop that track, record it, and move to the next independent task.

## Phase 0 — checks first
1. OpenAI key: confirm ~/shipharness/.env is loaded (show only the last 4 chars), make doctor, one minimal gpt-6-luna call (< $0.001), report rate limits from headers. If the key fails: do no OpenAI work tonight; do Phase 4 only.
2. No static class: list every class command (demo-1..4, final, swap, replay, console) and whether it calls OpenAI live, with evidence. Add a test that fails if demo-N or final can run with a fake/stand-in client or without a valid key (must refuse, never fall back). Replay stays fallback-only with RECORDING on every screen.

## Phase 1 — approved pre-run-3 work
1. Finish what's in progress: full suite on main, commit the VERIFICATION entries (run 2, changes 7–13, equivalence check, LangSmith), image rebuild.
2. F2 continuity bug fix (strip harness files from session patches), test-first, "bug fix, applies to both arms".
3. Equivalence check result → merge referee-speed only if every outcome matches.
4. Live console check: `make console` + `make demo-1 PURPOSE=pilot` with previews; all five screens, including the full scrollable timeline for a finished run.
5. Pre-register in DESIGN before any run-3 A/B: F1 trap variant, F3 trap variant, F2 first session at 12 turns; the turn-cost harness change (harness arm only, "harness change"); fallback = effort "low" for both arms in any section with no gap after run 3; outcome rule = a section with no gap after run 4 is reported as "no measurable difference on this task with this model", no further tuning.
6. Full run 2 report in VERIFICATION (per section: pass counts per arm, wall times, why each arm failed).

## Phase 2 — pilot run 3 (pre-authorized)
- 2 A/Bs in parallel, F1–F4, k=3, pre-registered levers, turn-cost change applied, --purpose pilot.
- Then the determinism check (same code judged 10 times → identical).
- Then the parallelism test (3, then 4 in parallel) with your reliability criteria; choose the concurrency.

## Phase 3 — decision rules (apply mechanically)
Per section, "harness ahead" = harness arm passes the pre-registered primary measure in more runs than bare (out of 3), and the difference isn't caused by harness-only timeouts.
- No gap after run 3 → run 4 for that section only: effort "low" for both arms, k=3 (within 96 runs and $10).
- After run 4, stop tuning. Classify each section: "harness ahead", "no measurable difference", or "bare ahead".
- Gate PASSES if ≥ 3 of 4 sections are "harness ahead" AND determinism passed → create harness-frozen tag (chosen concurrency and per-section effort in the frozen settings) → run M8 (batch 1 + 32-run ablation) under the tag, within budget, into "shipharness-experiments" → export → report.
- Gate does NOT pass → no freeze, no M8, stop spending. Prepare an options note for me (per-section results, cost and effect of each option).

## Phase 4 — course content (no-spend; parallel subagents with disjoint scopes; start now alongside phases 1–3)
Quality rules for every file: plain English, prose lint clean, every concept cited to a source in RESEARCH (never present course labels as source terms), every number from a source or a real run ID (otherwise write PENDING, never invent), every command shown is actually run at least once and works, all links resolve, captured output only from real runs (pilot runs 2–3 or the console check), labelled "captured on <date>, run <id>; your output will differ".

Per submodule (01-instructions, 02-state-lifecycle, 03-scope-sandbox, 04-verification):
1. concepts.md — problem seen live → cause (cited) → the harness piece → how shipharness implements it → what the A/B measures. Two Mermaid diagrams minimum. Readable in 15 minutes.
2. demo/README.md — purpose; the class timing (poll → make demo-N → concepts and walkthrough → demo block); exact commands; screen sequence (which console screen when); code anchors to open; poll question; what to watch (specific events, BLOCKED lines, gate pills, board marks); what the harness arm did differently from bare and why (the "solution" to the problem shown); captured output and screenshots from real runs; experiment or pilot dots with run IDs; time and cost; troubleshooting; replay fallback.
3. assignment/ — README with every required section (objective, problem, background, what to build, concepts tested, prerequisites, input/output, requirements, constraints, steps, structure, setup, run, test, expected behaviour, examples, rubric with point weights totalling 100, common mistakes, cost and trace budget); starter/ with clear TODOs; `make check-assignment-N`; the required live step.
4. solution/ — complete working solution, SOLUTION_NOTES.md (approach, design choices, alternatives, trade-offs, known limits), captured self-check and grader output, one real captured live run. (Solutions stay private per the release plan.)
5. post-class-reading/ — 2–4 cited reading notes going deeper than class time, each with a reading time and "why it matters for your own repo".
6. session-notes.md — what was shown, key ideas with sources, what the A/B showed (experiment dots, not only the live run), common questions with answers, what to try next.

Repo-level:
- README.md (detailed): problem → solution storyline; what learners get; architecture diagram; prerequisites and accounts (OpenAI Build tier, LangSmith free, no card); quick start; per-OS setup links; every make command; how the demos work and the class timing; the five console screens; assignments overview; costs and caps; using shipharness and the four skills on your own repo; troubleshooting; references.
- docs/setup-macos.md, setup-windows.md (WSL2 + Docker Engine in Ubuntu, repo in the WSL filesystem), setup-linux.md — exact commands; state plainly which were tested live (Linux/WSL2) and which follow official docs only (macOS).
- docs/instructor-guide.md — stage by stage (T-1 day, T-30 min, opening, S1–S4 including the final launched during S4, final block, after class, Thursday review), each with command, what to check, pass criteria, expected time and cost, if-it-fails.
- docs/troubleshooting.md, docs/after-class.md, docs/architecture.md, REFERENCES.md.
- final-project/README.md — full end-to-end walkthrough.
- Skills READMEs: how to install and use each of the four skills in Claude Code, Codex, and Cursor (both .claude/skills and .agents/skills).
- Merge m7-a1..a4 after their checks pass.
- Release tooling (dry run only): retarget to ANI-IN/harness-engineering-session with the agreed public layout and allow-list, frozen-content check, rebuilt checkpoint tags, no solution/ or assignment grader tests, pilot exports excluded, no links from public files to private ones.

After Phase 4: run a content audit subagent (one that wrote none of it): checks every rule above file by file and lists gaps; fix them in one pass.

## Morning summary (chat only)
1. Phase 0 results (key, rate limits, no-static guard).
2. What finished per phase.
3. Run 2, run 3 (and run 4 if any) per section: pass counts per arm, times, classification.
4. Gate result and why; freeze yes/no; M8 done/not with results.
5. Content: per file — done / PENDING items (why) / audit findings fixed.
6. Every decision you made under these rules, one line each.
7. Problems, stopped tracks, anything needing me.
8. Budget: build $ spent/left, pilot runs used, traces used.
9. What you propose next.

Confirm the class has no static demos:
1. List every command used in the 4-hour class (demo-1..4, final, swap, replay, console) and state for each whether it calls OpenAI live, with evidence from the run logs or ledger.
2. Add a test that fails if any class command (demo-N, final) can run with a fake or stand-in model client, or without a valid OPENAI_API_KEY (it must refuse, not fall back).
3. Replay must remain fallback-only and always show RECORDING.
