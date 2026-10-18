# Shared agent brief template

When several agents work on one phase at once, the lead writes one shared brief that every agent
reads first. Their own prompts then say only which part is theirs
([agent-prompt-templates.md](agent-prompt-templates.md)). The shared brief fixes everything two
agents could otherwise decide differently: the environment, the folders, who writes where, and the
conventions of the output. Write it before the first agent starts; changing a convention later
means every agent redoes work.

Copy the block below and fill every `<...>`.

```markdown
# <PHASE> shared brief: <DELIVERABLE>

Every agent reads this first. Your own prompt says which part is yours. Report to the lead, who
merges, runs the full checks and pushes. Never push. Never merge into main.

## Course and repositories
- Course: "<COURSE>". Tool: <TOOL>. What learners see: <screens, keys, URLs>.
- Dev repository: <PATH>, branch main at <SHA>. Public release: <URL> at <SHA>, tag <TAG>.
- Recorded runs to start from: <run folder>, one line per demo with its run id.

## Running commands
- <How to run a command on this machine, e.g. write a .sh file in YOUR scratch folder
  <SCRATCH>/<role>/ and run it with <COMMAND>; start each script with <PATH SETUP>.>
- Long jobs run in the background and write a log; poll the log, never sleep in the foreground.
- If the machine hangs: <restart command>, then check status and fsck, resume, tell the lead.

## Hard rules
- SECRETS: never open <SECRETS FILE>. No key, host path or personal detail in any image, render,
  PDF page or committed file. Redact host paths to ~/... in terminal renders.
- MODEL CALLS: only the live runner, only through the course's commands.
- HEAVY JOBS: at most <N>; the live runner owns them. Others: targeted tests only.
- COMMITS (where your role commits): <identity flags>. No co-author or "generated with" lines.
- HONESTY: never change recorded results, measures or settings; never pick or drop runs.
- STYLE: <STYLE GUIDE PATH>; <checker> --strict and <prose lint> pass on every Markdown file.

## Folder contract
- <RUN FOLDER>/<demo>/: terminal.txt (host paths redacted), meta.json, DONE when finished.
- <RUN FOLDER>/STATUS.md: running log and cumulative cost.
- <IMAGE FOLDER>/<demo>/: PNGs plus images.json.

## Write scopes
| Role | Writes | Commits |
|---|---|---|
| Live runner | <RUN FOLDER> only | no |
| Screenshot tooling | <IMAGE FOLDER>, <tooling worktree> | yes, its branch |
| Writer N | <chapter N file> only | no |
| Repo updater | <its worktree> | yes, its branch |

## Conventions fixed up front
<File names, heading forms, box markers, image and caption form, terminal excerpt length, how run
ids may appear: everything the build script or the checker relies on.>

## Step template
<The exact step template below, copied in.>
```

## Environment

State the operating system, where the repository lives, the user, the tools on the path, and the
recorded runs agents may start from. Give commit shas and tags, so an agent can tell a stale copy.

## Running commands

Give the one way to run a command that works on this machine, with the exact command line and
the traps (for example, shell variables that a wrapper expands too early). Say how to run long
jobs in the background and what to do when the machine hangs.

## Hard rules

Repeat the governing brief's hard rules ([brief-template.md](brief-template.md)) in the form each
agent needs: which role makes model calls, who owns the heavy-job slots, which identity commits.

## Folder contract

Name every shared folder, its files and their fields. A `meta.json` per live run holds: demo,
command, run id, start and end, `ran: "alone" | "paired with <demo>"`, wall time, the verdict
times as printed, the outcome per arm, the cost, and notes. A `DONE` file tells other agents the
folder is complete. An `images.json` holds, per image: file, screen, moment, alt text, callouts
(`n`, `x`, `y`, `text`), source run id, and whether it is recorded or live.

## Write scopes

A table of role, folders it may write, and whether it commits. No two roles write the same file.
Agents that share a worktree write files only; one named agent commits at the end, at the lead's
request.

## Conventions fixed up front

Fix the Markdown conventions the build script and the checker rely on: the chapter heading form,
the step heading form, the field labels in order, the box markers, the image line followed by a
blank line and an italic caption, numbered callout lists that match the circles on the image,
terminal excerpts of at most 12 lines (longer output becomes a rendered image), and the chapter
end sections. Writers can start the same hour; the designer implements the conventions.

## Step template

Every guide step, exactly:

```text
### Step N: <short action>
**Where:** <Terminal 1 / Terminal 2 / browser + screen key>
**Type:** <a fenced bash block: copy-ready, one command per line, no prompt sign>, or "Click ..." / "Press 3"
**You should see:** <expected output, or a screenshot with numbered callouts>
**Look at:** <the exact panel, line, pill or column>
**What it means:** <plain words, for an engineer>
> [!CHECKPOINT] <how you know it worked>
> [!IFDIFFERENT] <1 to 3 likely causes, each "cause → fix">
> [!INSTRUCTOR] <what to point at and say, including how to explain a fail>
> [!WARNING] <optional>
```

No skipped steps: starting each command, how long to wait, refreshing, opening the run, each
screen in order, where to scroll, each important pill or row, and the terminal's final lines.
Each chapter ends with `## Result summary` (a table of this run's numbers), `## Time and cost`,
and `## What to say in class` (3 to 5 bullets). The skill that writes chapters is
[demo-guide-writer](../skills/demo-guide-writer/SKILL.md).
