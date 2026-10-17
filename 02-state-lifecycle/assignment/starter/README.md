# starter

Your starting point for assignment A2 (task and grading criteria: [`../README.md`](../README.md)).

`a2_state/` is a state layer that runs without errors: the initializer step writes init.sh,
progress.md, session-handoff.md, and the exec plan, and every session gets the Getting up to speed
routine. Nothing is written at a session stop, so the self-check fails until you fill in the TODOs:

| File | TODOs |
|---|---|
| `a2_state/ledger.py` | 1a `parse_steps`, 1b `derive_ledger`, 1c `render_ledger` |
| `a2_state/layer.py` | 1-5 `on_session_end`, 6 `on_session_start`, 7 `on_phase_end` |
| `a2_state/progress_log.py` | 4 `normalise_progress` |

Work here, or copy the folder and pass the copy with `A2_IMPL=<folder>`:

```
make check-assignment-2                 # visible scenarios (test stand-in agent), PASS/FAIL per criterion
```

The scenarios run the test stand-in agent (`../a2_scenario/literal_agent.py`), a deterministic
program, not a model. When your layer is final, run the required live step once (`../README.md`,
"Required live step"); it writes `live/` next to `a2_state/`. Submit the folder with both. The
instructor's grader adds hidden scenarios and checks `live/`; the score is out of 100.
