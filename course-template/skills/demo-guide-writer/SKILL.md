---
name: demo-guide-writer
description: Write a demo guide chapter from a real live run, in the fixed step template, with screenshots, numbered callouts, captions checked against each image, and timings as ranges. Use when a live run's captures and images are ready and a chapter must be written or refreshed.
---

# Demo guide writer

The demo guide walks an instructor or a learner through each live demo, one command and one screen
at a time. It is written only from real runs. The step template and the Markdown conventions are in
[shared-agent-brief-template.md](../../playbooks/shared-agent-brief-template.md); page style is in
[STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- A run folder has `DONE`, and its images and `images.json` exist.
- A chapter must be refreshed after new runs or a changed screen.

## Inputs

- `<RUN FOLDER>/<demo>/terminal.txt` and `meta.json` (one or more runs of the demo).
- `<IMAGE FOLDER>/<demo>/` PNGs and `images.json` (alt text, callouts, source run).
- The guide's conventions file and the chapter file you own.

## Steps

1. Start with `# Chapter N: <title>` and one problem-first paragraph: what failure this demo shows
   and what to watch for.
2. Walk the run in order with no skipped steps: start the command, how long to wait, refresh, open
   the run, each screen in order, where to scroll, each important pill or row, the terminal's last
   lines.
3. Write every step in the template: `### Step N:`, then **Where:**, **Type:** (a copy-ready bash
   block, one command per line, no prompt sign), **You should see:**, **Look at:**, **What it
   means:**, then the checkpoint, if-different (1 to 3 "cause → fix" lines) and instructor boxes.
4. **Images**: the image line, a blank line, an italic caption, then a numbered list matching the
   circles on the image. Open the image first. Describe only what is visible in it; if the crop cut
   a part off, say less or ask for a new capture, never describe the missing part.
5. **Terminal output**: a text block of at most 12 lines, or a rendered terminal image.
6. **Numbers**: every time and cost comes from `meta.json` or `terminal.txt`. With several runs,
   write the range ("3:37 to 4:45") and the date of measurement; use only runs that ran alone.
7. **Instructor notes**: what to point at and say for the expected result and for the other one
   (a fail, no claim, a reviewer reject).
8. End with `## Result summary` (a table of this run's numbers), `## Time and cost`, and `## What
   to say in class` (3 to 5 bullets).
9. Run the style checker strict and the prose lint on the chapter.

## Outputs

One chapter file, in the template, with every image captioned from the image itself and every
number traced to a run file.

## Checks

- Every command in the chapter was run in the source run, exactly as written.
- Every callout number on an image has a list item, and the reverse.
- Each caption matches its image when opened side by side.
- Times are ranges from alone runs, with the date; see
  [honesty-and-measures.md](../../playbooks/honesty-and-measures.md).
- The lessons on captions and differing results in
  [lessons-learned.md](../../playbooks/lessons-learned.md) are applied.
