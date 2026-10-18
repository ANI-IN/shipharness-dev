# {{MODULE_TITLE}} - Live Demo Guide

<!-- guide: one paragraph: the PDF's file name as a link, what it walks through (every live demo of the class, one command and one screen at a time), and that each step says what to tell the class. Keep exactly one copy of the PDF in this folder, at a print-friendly size. -->

## Who it is for

<!-- guide: three bullets: instructors who run the demos live (every step has an instructor note, including what to say when a result differs from the guide's); learners who run the demos on their own copy after class; teaching assistants who rehearse a demo or help a learner whose screen looks different. -->

## What you need first

<!-- guide: the set-up copy (link ../setup/README.md), the keys in .env (never pasted into a terminal, a document, or a chat), and the readiness check that Part 0 walks through, with the line it ends on. -->

## How to follow it

1. Read [Part 0: Before you start](part0.md): it opens the terminals, checks your copy, and
   starts the results console.
2. Work through the chapters in order, one per section:
{{GUIDE_CHAPTERS}}
3. Every step reads the same way: where (which terminal or screen), what to type or press, what
   you should see, where to look, what it means, a checkpoint, what to do if it looks different,
   and an instructor note.
4. Each chapter ends with a result summary, the time and cost, and what to say in class.
5. If a live demo cannot run in class, the [appendix](appendix.md) shows how to replay a recorded
   run instead, labelled as recorded. It also has a command cheat sheet, a troubleshooting table,
   and a glossary.

## Time and cost

<!-- guide: one line on where the numbers come from: only runs that ran alone on the machine (paired runs slow each other), the range over at least two runs, and the clock basis (from launch, or from the first event), the same basis as every chapter. Then fill the table, and add the setup time and the time to follow the whole guide. -->

| Demo | Command | Time | Cost |
|---|---|---|---|
{{GUIDE_ROWS}}

## The slides

The class deck that goes with these demos is in [slides/](../slides/README.md).

## Build the PDF

<!-- guide: for maintainers: the one build command, what it needs, that it makes no model calls, and the scan of the PDF's text for keys, host paths, account links, and placeholders before it is published. -->

| Path | What it holds |
|---|---|
| `part0.md` | Part 0: Before you start |
| `chapters/` | One chapter per section's demo |
| `appendix.md` | Cheat sheet, troubleshooting, glossary, and the replay fallback |
| `images/` | Screenshots and terminal images |
| `source/` | The build sources and [the Markdown conventions](source/CONVENTIONS.md) |
