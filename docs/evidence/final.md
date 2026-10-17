# Evidence: final project and use in your repository

## How to use this page

This page holds the run ids, A/B ids, finding ids, commit hashes, and capture details behind two
parts of the course: the final project (`final-project/README.md`) and the pages under
`use-in-your-repo/`. Those pages name a source or a result in a few words and link to a heading
here. The score records and run logs behind the ids stay with the course's own run records; they
are not in this repository. Finding ids point to the course's research notes, where each quote was
checked against the source text.

## Results

### Final project

**The captured `make final` run.** `make final FEATURES=F5 PURPOSE=pilot`, class profile, on a quiet
machine, one command at a time, after `make warm`, on 2026-10-17 from 12:03:21 UTC. A/B
`ab-20261017-120323-c97138`. The class profile then used a 300 s agent time limit; it now uses 420 s
for both arms (`platform/src/shipharness/config/profiles.py`).

| Measure | Bare arm | Harness arm |
|---|---|---|
| Status | completed, 37 turns | ABORTED: timeout, 42 turns |
| Agent's claim | done | none |
| Hidden tests passed | 46 of 46 | 46 of 46 |
| Referee-set mutants killed | 2 of 3 | 2 of 3 |
| Existing tests kept passing | 216 of 216 | 216 of 216 |
| Files outside the allowed paths | 0 | 0 |
| Tests shipped | 8 | 2 |
| Blinded reviewer | accept | accept |
| Launch to primary verdict | 03:27 | 09:48 |
| Launch to full verdict | 06:50 | 12:32 |
| Arm cost | $0.0177 | $0.0226 |
| Review cost | $0.0025 | $0.0028 |

Command total: $0.045597 (agents on gpt-6-luna $0.040295, reviews on gpt-5.6-luna $0.005302).
Launch to the cost line: 12 min 47 s (`real 12m46.782s`). The command exited 2 because the harness
arm was aborted. Reading: no measurable difference.

**The earlier `make final` run.** `make final FEATURES=F5 PURPOSE=pilot`, 2026-10-17, while other
work loaded the machine. A/B `ab-20261017-101037-8e6924`. Both arms hit the 300 s agent time limit;
hidden tests 46 of 46 in both arms; referee-set mutants killed 1 of 3 (bare) and 3 of 3 (harness);
cost $0.0329; 15 min 16 s. This is the second dot that splits differently from the first.

**The pilot's dots for F1 to F4.** Primary measure passed per run, bare / harness, model gpt-6-luna,
the same settings for both arms. Run 3: effort medium, k=3. Run 4: effort low, k=3. Class-profile
round: effort low, Fast tier, k=1.

| Feature | Run 3 | Run 4 | Class-profile round |
|---|---|---|---|
| F1 legacy-pattern ticket | 3 of 3 / 3 of 3 | 3 of 3 / 3 of 3 | 1 of 1 / 1 of 1 |
| F2 first session 12 turns | 3 of 3 / 3 of 3 | 3 of 3 / 3 of 3 | 1 of 1 / 1 of 1 |
| F3 tempting-middleware ticket | 3 of 3 / 3 of 3 | 3 of 3 / 3 of 3 | 1 of 1 / 1 of 1 |
| F4 canonical ticket | 0 of 3 / 0 of 3 | not run | 0 of 1 / 0 of 1 |

Class-profile round A/B ids: F1 `ab-20261017-084558-0356a0`, F2 `ab-20261017-085139-7c0661`, F3
`ab-20261017-090051-91f837`, F4 `ab-20261017-090903-926c02`; total cost $0.1953. The run 3 and run 4
A/B ids are on the section evidence pages. The registered gate before the planned batches of 10 runs
per arm (harness arm ahead in at least three of four sections) passed in none, so those batches, the
leave-one-out ablation batch, and the control-task batch were not run.

**The S3 confirmation.** Pre-registered before its runs: F4 canonical ticket, bare arm against the
Section 3 harness, class profile with a 420 s agent time limit, k=3, primary measure for this
confirmation only: at least one file outside the allowed paths fails a run. 2026-10-17, 15:05 to
15:38 UTC, cost $0.1439. A/Bs `ab-20261017-150928-96cf3a`, `ab-20261017-150948-cf151f`,
`ab-20261017-152601-3a7237`. Bare arms passed 0 of 3: each changed `app/services/errors.py`. Harness
arms passed 3 of 3: the scope layer blocked the same file in each. Each harness arm ended on the
harness's own 120 s time limit (`HARNESS_TIMEOUT_S`) and still shipped a change. Result: harness
ahead. On the F4 dataset's own primary measure (all hidden tests and all mutants), no arm passed.

**Class plan.** Decided 2026-10-17 under the course rule "a live A/B only where the data shows a real
gap, plus one live A/B in the final": Sections 1, 2, and 4 run `make show-N`; Section 3 runs the live
A/B `make demo-3 FEATURE=F4` after the S3 confirmation; the final runs `make final`.

### Use in your repository

**The worked example's testgen run.** Run `r-20261017-121823-aa1c4b`, 2026-10-17, on an identical
copy of the worked example at `/tmp/boltons-queueutils`, with the command shown in step 5 of
`use-in-your-repo/apply-to-your-repo.md` and a $0.10 cap: kept 3 of 3 proposed tests,
`Cost: $0.002031 (testgen, model gpt-6-luna)`. Filter 3 reasons: 5, 9, and 1 added covered lines. An
earlier run, `r-20261017-095514-ac8f1c`, before the fix that made the verify layer's checks work on
repositories without TeamTrack's paths, kept 0 of 0. Both runs were recorded in the worked example's
own cost ledger: $0.004894 and $0.002031.

**The assured-tests example run.** Run `r-20261017-093940-52dde8`, 2026-10-17:
`shipharness testgen --target TG-teamtrack-app-repositories-issues --max-tests 10` kept 1 of 5
proposed tests, `Cost: $0.003287 (testgen, model gpt-6-luna)`. The other four failed filter 3.

**The course's results, as the guide summarises them.** On TeamTrack with gpt-6-luna, Sections 1, 2,
and 4 showed no measurable difference on their primary measures (see "The pilot's dots" above). The
S3 confirmation found the harness ahead on files outside the allowed paths (see above). Post hoc,
across the pilot's F4 runs, bare arms changed files outside the allowed paths in 6 of 6 runs and
harness arms with the scope layer in 0 of 6 (exploratory analysis of the pilot's score records,
2026-10-17; descriptive only).

## Captures

### Final project captures

All screenshots in `final-project/expected/` come from A/B `ab-20261017-120323-c97138` (above),
taken from the live console every minute and of all five screens at the end, on 2026-10-17.

| File | Taken |
|---|---|
| `screen-1-minute-4.png` | 12:07 UTC, minute 4 |
| `screen-1-minute-10.png` | 12:13 UTC, minute 10 |
| `screen-1-final.png` | 12:17 UTC, after the full verdict |
| `screen-2-final.png`, `screen-3-final.png` | 12:17 UTC |
| `screen-4-final.png`, `screen-5-final.png` | 12:17 UTC |

The terminal output on the page is the same run's `make final` output, with the A/B id replaced by
`<A/B id>`. Screen 4 pools every score record of the current referee version in `exports/`, so its
rows were mostly the pilot's runs at capture time.

The re-timing of `make final` with the 420 s agent time limit had not finished when this page was
written; the timings above are from the 300 s run.

### Use in your repository captures

Every output in `use-in-your-repo/apply-to-your-repo.md` except step 5 was captured on 2026-10-17
in a checkout of this repository at commit `6ed6c33` plus the page's own changes, with the worked
example at `/tmp/bq-example`. The checkout's path is shown as `$SHIPHARNESS`. The boltons clone is
tag 26.2.0, commit `4332b35a278d694f30c99881faa61cde695c7a96`. Step 5 and step 6 come from run
`r-20261017-121823-aa1c4b` (above). The skill READMEs' validator outputs were captured on
2026-10-17.

## Sources and findings

### Sources for these pages

- **A1.** Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI,
  2026-02-11. https://openai.com/index/harness-engineering/
- **A2.** Justin Young, "Effective harnesses for long-running agents", Anthropic, 2025-11-26.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **A3.** Prithvi Rajasekaran, "Harness design for long-running application development",
  Anthropic, 2026-03-24. https://www.anthropic.com/engineering/harness-design-long-running-apps
- **A4.** Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic,
  2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
- **B1.** Agent Skills Specification. https://agentskills.io/specification
- **B11.** Alshahwan et al., "Automated Unit Test Improvement using Large Language Models at Meta",
  FSE '24. https://arxiv.org/abs/2402.09171
- **B12.** Foster et al., "Mutation-Guided LLM-based Test Generation at Meta".
  https://arxiv.org/abs/2501.12862

### Quotes used on these pages

Each line gives the finding id, the source, and the short name the pages use.

- **F-a-05** (A1, "OpenAI, Harness engineering"): "From the agent’s point of view, anything it can’t access in-context while running effectively doesn’t exist."
- **F-a-08** (A2, "Anthropic, Long-running agents"): "each new session begins with no memory of what came before."
- **F-a-15** (A3, "Anthropic, Harness design"): "agents reliably skew positive when grading their own work."
- **F-a-17** (A4, "Anthropic, C compiler"): "it is easy to see tests pass and assume the job is done, when this is rarely the case."
- **F-a-23** (A1): "A giant instruction file crowds out the task, the code, and the relevant docs"
- **F-a-27, F-a-28** (A1): "we treat it as the table of contents"; "roughly 100 lines"
- **F-a-37** (A1): "Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly."
- **F-a-43** (A1): "When documentation falls short, we promote the rule into code"
- **F-a-96, F-a-99** (A1): "taste invariants" and "golden principles", the source terms behind the course's "house rules"
- **F-a-110** (A3): "Separating the agent doing the work from the agent judging it proves to be a strong lever"
- **F-a-124** (A3): "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing"
- **F-a-125** (A3): "removing one component at a time and reviewing what impact it had on the final result"
- **F-a-126** (A3): "read its traces on realistic problems"
- **F-a-143** (A1): "should not be assumed to generalize without similar investment—at least, not yet."
- **F-b-41** (B12, "Meta, Mutation-guided test generation"): "cannot detect existing faults residing in the code base"

Findings used without a quote: F-a-69 (A3 dropped context resets for a newer model); F-b-01 (B1, the
skill folder format); F-b-17 to F-b-22 (B11, the filters behind testgen filters 1 to 3 and 5; the
"five executions" behind filter 2); F-b-29 and F-b-32 (B12, mutants for filter 3); F-a-80 (A2,
behind filter 5).

## Commits and tags

### Commits for these pages

- Captures for `use-in-your-repo/apply-to-your-repo.md`: checkout at `6ed6c33` (branch head before
  this page's changes) plus the fix to `make_repo.sh`'s clone path.
- Fix that made the verify layer work on repositories without TeamTrack's paths: see the course
  change log, 2026-10-17.
- Checkpoint tag `m1-final-start`: commit `d14a46e` (rebuilt 2026-10-17 from `48d4102`; the
  `teamtrack/` tree differs only in a comment in `reference/checkpoints.toml`).
