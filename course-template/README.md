# Course template

The structure and taste of this program's modules, and a generator for a new module's empty
skeleton. This folder is for course authors; the release build does not ship it.

| File | What it is |
|---|---|
| [STRUCTURE-AND-TASTE.md](STRUCTURE-AND-TASTE.md) | The layout, page templates, what the owner liked and rejected, and the build process |
| [STRUCTURE-AND-TASTE-CHECKLIST.md](STRUCTURE-AND-TASTE-CHECKLIST.md) | The checklist a reviewer uses to confirm a module matches |
| `scripts/new_module.py` | Generates an empty module skeleton |
| `skeleton/` | The files the generator renders |
| `tests/` | Tests that generate a skeleton into a temporary folder and run its checks |

## Generate a module

From the repository root:

```bash
uv run python course-template/scripts/new_module.py \
  --name "Loop Engineering for Coding Agents" --module 2 \
  --sections "Triggers" "Loops" "Hill climbing" "Reliability" --out ../module2
```

It refuses to write into a folder that already exists. Options: `--project` sets the name used in
the concepts heading "How <project> does it" (default "the project"); `--demo-files` sets the
folder in each `demo/` that holds the demo's real files (default `files`).

The skeleton holds:

- the course-first folders, with one `section-N-<slug>/` per section;
- every page with its template headings and an HTML comment starting `guide:` under each heading
  that says what goes there (hidden on GitHub, never shipped text);
- `docs/STYLE.md`, the generalised style guide;
- `platform/scripts/check_style.py` and `lint_prose.py`, configured by
  `platform/config/course.toml` (module title, section names, named kinds, codes, id patterns,
  sources);
- `.github/workflows/ci.yml` (lint, prose lint, style check, tests), a `Makefile` with `setup`,
  `check-style`, `check-style-strict`, `test`, `demo-N`, and `check-assignment-N`, and
  `.env.example`.

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

## Test the generator

```bash
uv run pytest -q course-template/tests
```
