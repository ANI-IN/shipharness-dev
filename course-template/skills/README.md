# Skills for building and running a course

Agent Skills (one folder per skill, each with a `SKILL.md`: frontmatter `name` and `description`,
then the instructions) that cover a course build from the first folder to the public release. Copy
them into an agent's skills folder, or point an agent at one by path. They apply the rules of
[STRUCTURE-AND-TASTE.md](../STRUCTURE-AND-TASTE.md) and the team process in
[../playbooks/](../playbooks/README.md).

| Skill | Use it to |
|---|---|
| [new-course](new-course/SKILL.md) | Start a course from the kit: generate, fill the names, first checks |
| [section-author](section-author/SKILL.md) | Write one section: pages, demo, assignment, reading, session notes |
| [live-demo-runner](live-demo-runner/SKILL.md) | Run the live demos for capture and timing, within budget |
| [demo-guide-writer](demo-guide-writer/SKILL.md) | Write a demo guide chapter from a live run, in the step template |
| [screenshot-capture](screenshot-capture/SKILL.md) | Capture screenshots, terminal renders and callouts, redacted and legible |
| [fresh-reviewer](fresh-reviewer/SKILL.md) | Follow a guide or page on a clean copy as a learner, then as an instructor |
| [evidence-and-results](evidence-and-results/SKILL.md) | Record runs and measures; re-judge and disclose by the rules |
| [release-and-publish](release-and-publish/SKILL.md) | Build the single-commit public release and publish it safely |
| [ui-layout-check](ui-layout-check/SKILL.md) | Prove a web screen holds at any width, pixel ratio and zoom |
| [slide-review](slide-review/SKILL.md) | Turn a deck's text and notes into a change list against the repository |
| [style-and-naming](style-and-naming/SKILL.md) | Apply the naming and wording rules and run the checkers |

## The order in a build

new-course, then section-author for one golden section, fresh-reviewer on it, then section-author
for the rest in parallel. live-demo-runner pilots each demo as soon as it exists; screenshot-capture
and demo-guide-writer follow each run; evidence-and-results records every run. ui-layout-check runs
whenever a screen changes. style-and-naming runs before every commit. slide-review runs on the
owner's deck once the repository is settled; release-and-publish runs at the publish stop point.
