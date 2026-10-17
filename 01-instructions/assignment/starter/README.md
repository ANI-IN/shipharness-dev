# starter

Your work folder for assignment A1. The task, the specification, and the grading criteria are in
[../README.md](../README.md).

| Path | What it is | What you do |
|---|---|---|
| `original/AGENTS.md` | the TeamTrack variant's 899-line instruction file, 70 tagged rules | read it; never edit it (the grader pins its hash) |
| `instructions/AGENTS.md` | a stub with `TODO(A1-1)` and `TODO(A1-2)` | replace it with the map; add `ARCHITECTURE.md`, `docs/`, and one skill |
| `checker/check_docs.py` | the checker's interface, with `TODO(A1-3)` and `TODO(A1-4)` stubs | implement it |
| `checker/test_check_docs.py` | visible tests (12 fail on the stubs) | do not edit; add your own test file next to it |
| `ab-report.md` | the A/B report template, with `TODO` fields | fill it after the A/B run |
| `live/` (not there yet) | the live evidence of your A/B: command output, experiment exports, score records, harness run logs | create it with `live_evidence.py` after the A/B run (README, task 6) and commit it |

Start with:

```bash
uv run python 01-instructions/assignment/check.py
uv run python -m pytest -q -p no:cacheprovider 01-instructions/assignment/starter/checker
```

Both run without keys or Docker. The first prints one FAIL line per requirement still open; the
second shows which parts of the checker are missing.
