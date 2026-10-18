---
name: new-course
description: Start a new course module from the course kit. Generates the course-first skeleton with new_module.py, fills the names and config, records the up-front decisions, and runs the first checks. Use when a new course or module begins, before any page is written.
---

# New course

Creates the empty, checkable shape of a module so every later page has a fixed place, template and
check. The layout and page templates are in [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md);
the generator is described in the kit's [README](../../README.md).

## When to use

- A new module or course starts and the repository does not exist yet.
- The layout, naming or section list must be fixed before agents start writing.

Do not use it on a repository that already has pages; the generator refuses an existing folder.

## Inputs

- `<COURSE>`: the module title, and `<N>`: the module number.
- The section names, in class order (`<SECTION 1>` ... `<SECTION K>`).
- `<PROJECT>`: the project the course works on (used in "How <PROJECT> does it").
- The demo files folder name (default `files`).
- The owner's approval of the project and the sections (stop point ⏸ 1 in section 4.2 of the
  structure guide).

## Steps

1. Get the owner's approval of the project, the section list, and one failure story per section.
   Stop here until it is given.
2. Generate the skeleton from the kit's repository root:

   ```bash
   uv run python course-template/scripts/new_module.py --name "<COURSE>" --module <N> \
     --sections "<SECTION 1>" "<SECTION 2>" --project "<PROJECT>" --out ../<folder>
   ```

3. Open `platform/config/course.toml` in the new folder and fill the named kinds ("<Kind> N:
   <name>"), the codes, the id patterns, and the sources. These names are used everywhere; see
   [style-and-naming](../style-and-naming/SKILL.md).
4. Write the up-front decisions (layout, naming, solutions policy, demo format, slide process) in
   the private engineering notes, with the table in section 4.1 of the structure guide. Do not reopen
   them without the owner.
5. Initialise the repository and run the first checks:

   ```bash
   cd ../<folder> && git init && make setup
   make check-style          # 0 errors on the empty skeleton
   make check-style-strict   # fails until every guide comment is replaced
   ```

6. Commit the skeleton with the owner's identity only.
7. Write the governing brief for the first phase from
   [brief-template.md](../../playbooks/brief-template.md), and the shared agent brief from
   [shared-agent-brief-template.md](../../playbooks/shared-agent-brief-template.md).
8. Pick one section as the golden sample and start [section-author](../section-author/SKILL.md) on
   it alone.

## Outputs

- A new repository with the course-first folders, one `section-N-<slug>/` per section, every page
  holding its template headings and guide comments, and CI, Makefile and checkers in place.
- `platform/config/course.toml` with the real names.
- The decisions record and the first governing and shared briefs.

## Checks

- `make check-style` reports 0 errors; `make test` passes on the skeleton.
- The top level matches the layout table in section 1.1 of the structure guide.
- Every section name in `course.toml` matches the folder slugs.
- No guide comment is deleted before its part is written.
- Lessons to plan for now: [lessons-learned.md](../../playbooks/lessons-learned.md).
