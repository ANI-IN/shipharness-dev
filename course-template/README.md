# Course template

A complete kit for building a hands-on technical course module: one with live demos, a results
console, assignments with graders, a step-by-step demo guide, and a public release built from a
private development repository. This folder is for course authors; the release build does not ship
it.

## Create a new course in 7 steps

1. **Read the rules.** Read [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md) once, end to end.
2. **Write the shared brief.** Copy the brief template from [playbooks/](playbooks/) and fix the
   environment, the rules, the folder contract, and the conventions before any agent starts.
3. **Generate the skeleton**, with the kit installed, from the repository root:

   ```bash
   uv run python course-template/scripts/new_module.py \
     --name "Your Module Name" --module 2 \
     --sections "First section" "Second section" "Third section" --out ../module2 --with-kit
   ```

4. **Fix the decisions in files.** Fill `platform/config/measures.toml` (each section's headline
   measure and time bar) and check `course.toml` and `release.toml`, before the first run.
5. **Build a golden sample.** Write one section completely with the [skills/](skills/), pilot its
   demo live, and have it reviewed; then build the other sections in parallel.
6. **Make the slides and the guide.** Draft the outline from [slides/](slides/), build the Live
   Demo Guide with the tools from [tools/](tools/), and have a fresh reviewer follow it live.
7. **Review and release.** Walk [STRUCTURE-AND-TASTE-CHECKLIST.md](STRUCTURE-AND-TASTE-CHECKLIST.md),
   run the strict checks, the secret scan, and the release build, and verify from a fresh clone.

## What is in the kit

| Path | What it is |
|---|---|
| [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md) | The layout, page templates, taste, console, results, guide, release, and process rules |
| [STRUCTURE-AND-TASTE-CHECKLIST.md](STRUCTURE-AND-TASTE-CHECKLIST.md) | The checklist a reviewer uses to confirm a module matches |
| [scripts/](scripts/) | `new_module.py`, which generates a module skeleton and installs the kit parts |
| [skeleton/](skeleton/) | The files the generator renders: pages, guide, checker, prose lint, config, CI |
| [skills/](skills/) | Agent Skills for building a course |
| [playbooks/](playbooks/) | The shared brief, prompt templates for agent teams, and report formats |
| [slides/](slides/) | The slide template, the outline template, speaker-note rules, the slide review |
| [tools/](tools/) | The guide PDF builder, screenshot and callout tools, the layout sweep, the release build, the secret scan |
| [tests/](tests/) | Tests for the generator and the kit |

## Generate a module

`new_module.py` refuses to write into a folder that already exists. Options:

- `--project` sets the name used in the concepts heading "How <project> does it" (default "the
  project").
- `--demo-files` sets the folder in each `demo/` that holds the demo's real files (default
  `files`).
- `--with-kit` installs this kit's parts; `--kit` followed by a folder installs another kit's.
  Each part that exists is copied: `slides/` into `slides/`, `tools/guide/` into
  `guide/source/`, the other tools into `platform/scripts/kit/`, `skills/` into `.claude/skills/`.
  A missing part is skipped, a kit's own tests are left behind, and a skeleton file is never
  replaced.

The skeleton holds:

- the course-first folders, with one `section-N-<slug>/` per section;
- every page with its template headings and an HTML comment starting `guide:` under each heading
  that says what goes there (hidden on GitHub, never shipped text);
- `guide/`: the Live Demo Guide's README, Part 0, one chapter per section in the step template,
  the appendix, and `source/CONVENTIONS.md`;
- `docs/STYLE.md`, the generalised style guide;
- `platform/scripts/check_style.py` and `lint_prose.py`, configured by
  `platform/config/course.toml`;
- `platform/config/measures.toml` (pre-registered measures), `release.toml` (the release
  allow-list), and `platform/before-class/` (the before-class records);
- a `.gitignore` with the tool's output folders, and tests that check it and the release list;
- `.github/workflows/ci.yml`, a `Makefile` with `setup`, `check-style`, `check-style-strict`,
  `test`, `demo-N`, and `check-assignment-N`, and `.env.example`.

## Then

```bash
cd ../module2
git init
make setup
make check-style          # 0 errors on the empty skeleton
make check-style-strict   # fails until every guide comment is replaced by real content
```

Write each page by its guide comments and [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md), delete
each comment when its part is written, and review the module against the checklist.

## Test the kit

```bash
uv run pytest -q course-template/tests
```
