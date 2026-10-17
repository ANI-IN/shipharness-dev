# skill

Put your own skill here: exactly one folder with a `SKILL.md`, copied from
`use-in-your-repo/skills/skill-template` and renamed (see `use-in-your-repo/skills/skill-template/README.md`).

```bash
cp -r use-in-your-repo/skills/skill-template 04-verification/assignment/starter/skill/<your-skill>
uv run shipharness skills validate 04-verification/assignment/starter/skill
```

The grader checks that the folder validates, that `name` is no longer `skill-template`, that no
template placeholder such as `<Skill title>` is left, and that "When to use" and "Steps" have
content.
