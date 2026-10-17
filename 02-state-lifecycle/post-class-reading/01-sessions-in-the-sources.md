# How the sources carry work across sessions

Reading time: about 9 minutes.

Class time covers A2's initializer agent and A3's context reset. This piece puts five sources next to
each other, so you can see which parts they agree on and which parts are one team's choice. Quotes
are copied verbatim from the sources, cited by source id and finding id (see
[REFERENCES.md](../../../REFERENCES.md)); all sources were accessed on 2026-10-16.

## A2: two prompts, one harness

A2 (Anthropic, "Effective harnesses for long-running agents") is the base design for this section.
Its answer to "each new session begins with no memory of what came before." (F-a-08) has two parts:
"an initializer agent that sets up the environment on the first run, and a coding agent that is
tasked with making incremental progress in every session" (F-a-49). The initializer writes "an init.sh
script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git
commit that shows what files were added." (F-a-50). After that, "Every subsequent session asks the
model to make incremental progress, then leave structured updates." (F-a-51).

The section headed "Getting up to speed" lists the coding agent's first steps:

1. "Run pwd to see the directory you’re working in. You’ll only be able to edit files in this
   directory." (F-a-58)
2. "Read the git logs and progress files to get up to speed on what was recently worked on." (F-a-59)
3. "Read the features list file and choose the highest-priority feature that’s not yet done to work
   on." (F-a-60)
4. Run `init.sh` and "a basic end-to-end test before implementing a new feature." (F-a-61)

Step 4 exists because a broken start gets worse: "If the agent had instead started implementing a new
feature, it would likely make the problem worse." (F-a-62). A2's failure table closes the loop at the
other end: "End the session by writing a git commit and progress update." (F-a-63).

Two details that are easy to miss. First, the "two agents" are the same system with a different first
message: "We refer to these as separate agents in this context only because they have different
initial user prompts." (F-a-52). Second, A2 tried compaction and found it lacking: "However,
compaction isn’t sufficient." (F-a-54).

## A5: the same pattern as runnable code

A5 is the README of Anthropic's autonomous-coding quickstart, the reference implementation of A2.
Only the README was read; its prompts and templates were not opened (the course's clean-room rule).
In our own words: session 1 runs the initializer agent, later sessions run the coding agent, each
session gets a fresh context window, and the README lists `init.sh` and `claude-progress.txt` in the
generated project. Its one-line summary of state: "Progress is persisted via `feature_list.json` and
git commits" (F-a-74).

## A3: resets, compaction, and files as the channel

A3 (Anthropic, "Harness design for long-running application development") is where the term "context
reset" comes from: "Context resets—clearing the context window entirely and starting a fresh agent,
combined with a structured handoff that carries the previous agent's state and the next steps"
(F-a-65). A3 weighs it against compaction: "While compaction preserves continuity, it doesn't give the
agent a clean slate, which means context anxiety can still persist." (F-a-66).

A3's agents also talk to each other through files, not shared context: "Communication was handled via
files: one agent would write a file, another agent would read it and respond either within that file
or with a new file" (F-a-70).

A3 is also the source that dates the technique. Resets cost "orchestration complexity, token overhead,
and latency" (F-a-68), and a later model made them unnecessary in that harness: "Opus 4.5 largely
removed that behavior on its own, so I was able to drop context resets from this harness entirely."
(F-a-69). Read this as a measured choice for one model, not a rule.

## A4: notes for agents who arrive cold

A4 (Anthropic, "Building a C compiler with a team of parallel Claudes") ran many agents in parallel
containers, each starting cold: "each agent is dropped into a fresh container with no context and will
spend significant time orienting itself, especially on large projects." (F-a-10). The author's answer
was written notes: "I included instructions to maintain extensive READMEs and progress files that
should be updated frequently with the current status." (F-a-72). The agents added one of their own:
"When stuck on a bug, Claude will often maintain a running doc of failed approaches and remaining
tasks." (F-a-73).

## A6: the vendor guidance (supplementary)

A6 is a living Claude docs page that A2 links. Its text has changed since A2 cited it, so treat it
as supplementary and read it with its access date (2026-10-16). It gives the same split between a
first window and later ones: "Use the first context window to set up a framework (write tests,
create setup scripts), then use future context windows to iterate on a todo-list." (F-a-75). It also
notes that "Claude's latest models are extremely effective at discovering state from the local
filesystem." (F-a-76), and recommends structured formats for state: "When tracking structured
information (like test results or task status), use JSON or other structured formats" (F-a-77).

## Side by side

| Question | A2 | A3 | A4 | A5 (README) | A6 |
|---|---|---|---|---|---|
| How does a session learn what happened? | progress file + git log (F-a-53, F-a-59) | structured handoff (F-a-65) | READMEs, progress files (F-a-72) | feature list + git commits (F-a-74) | filesystem, JSON for structured state (F-a-76, F-a-77) |
| Who sets up the first files? | initializer agent (F-a-49) | a planner expands the prompt into a spec (F-a-153) | the author's harness and tests (F-a-136) | initializer agent (A5 README, in our own words above) | first context window (F-a-75) |
| Fresh context or compaction? | compaction "isn’t sufficient" (F-a-54) | resets for one model, dropped for a later one (F-a-69) | fresh container per agent (F-a-10) | fresh context per session (A5 README, F-a-74) | a fresh window is an option to consider (F-a-76) |

## What the course takes, and what it changes

- File names: A2's `claude-progress.txt` is `progress.md` in the course, and the template says so.
- The initializer is deterministic harness code, not a model session, because for one ticket the
  files are fixed (course design, building on F-a-52).
- The handoff has a part the harness writes itself (files changed, tests, commits, TODO markers,
  migration heads), so it exists even if the agent writes nothing (course design).
- The stop is produced by a session turn budget, the same for both arms. That mechanism is the
  course's, not a source term; the reset it produces is A3's (F-a-65).

## Why it matters for your own repo

The table above is a menu, not one design. Two points from it decide most of what you build:

- **Whether you need a reset at all depends on the model.** A3 dropped resets once the model stopped
  needing them (F-a-69). In pilot run 2 the bare arm, with no state files, found session 1's
  uncommitted migration with `git status` and carried on (run `r-20261016-181736-a05ddb`,
  [concepts.md](../concepts.md) §1), which is what A6 describes for Claude models (F-a-76). Measure
  your own agent across a stop before you add machinery.
- **Git is part of the state.** A2 and A5 both keep it next to their files (F-a-53, F-a-74).
  If your agent's sessions end before the work is done, make sure what it did reaches the working
  tree and, at the end of a session, a commit, so the next session and your measurements can see it.

Then pick the smallest set of files that answers "what happened, and what is next" for your
tickets, and give each one an owner (agent or harness).
