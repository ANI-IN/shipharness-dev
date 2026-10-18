---
name: screenshot-capture
description: Capture high-resolution screenshots of a course's web console, render terminal output as images, and draw numbered callouts, with redaction and legibility rules and an images.json record. Use when a guide, page or slide needs images from a recorded or live run.
---

# Screenshot capture

Images in the course are evidence: each shows a real run, legibly, with nothing private in it. The
image record and folders are fixed in
[shared-agent-brief-template.md](../../playbooks/shared-agent-brief-template.md); diagram style
(a different thing) is in section 2.3 of [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- A run folder has `DONE` and its chapter or page needs images.
- A screen changed and its images must be re-captured.

## Inputs

- The run (its run id and folder), and the screens and moments to show.
- A browser automation tool (for example Playwright) and a local console serving recorded runs.
- `<IMAGE FOLDER>/<demo>/` to write to.

## Steps

1. **Serve recorded runs locally.** No model calls; the console reads stored runs.
2. **HD capture.** Viewport 1920 by 1080 CSS px at device pixel ratio 2, browser zoom 100%, no
   browser chrome (headless page screenshots). Crop to the region the step talks about; keep the
   screen's title in the crop so the reader knows where they are.
3. **Terminal renders.** Render `terminal.txt` to a PNG with a monospaced font at a size that reads
   at full page width (at least 14 px at the printed width), the real colours, and the last lines the
   step needs. Long output: crop with a visible "lines cut" marker.
4. **Callouts.** Numbered circles placed by element position (from the page's layout, not guessed
   coordinates), each with a short text; at most 5 per image; never on top of the thing they point at.
5. **Redaction.** Before saving: no secrets file content, key, token, host path (redact to `~/...`),
   user name, email, machine name, or browser bookmarks. Blur or crop; never fake the content.
6. **Record** each image in `images.json`: file, screen, moment, alt text, callouts (`n`, `x`, `y`,
   `text`), source run id, recorded or live.
7. **Open every image.** Check legibility at the size it will be printed, that each callout sits on
   its target, and that nothing important is cut off at an edge.

## Outputs

PNGs and `images.json` per demo; the capture, render and callout tooling with tests, on its own
branch.

## Checks

- A search of every PNG's source text (terminal renders) and of `images.json` finds no host path,
  key pattern or personal detail.
- Every image has alt text that says what it shows, not "screenshot".
- Every callout's number and text match the caption list the writer will use.
- Images of web screens were also checked at display scaling; see
  [ui-layout-check](../ui-layout-check/SKILL.md) and
  [lessons-learned.md](../../playbooks/lessons-learned.md).
