---
name: ui-layout-check
description: Prove a course web screen (console, dashboard) holds at any size - fluid layout rules, an automated width, pixel-ratio and zoom sweep in a real browser, cache-busted assets, then a person reviewing the screenshots. Use when a screen's layout or styles change, or before class.
---

# UI layout check

Learners and instructors open the course's screens on laptops at 125% or 150% display scaling, on
projectors, and on small windows. A layout tested only at 1920 by 1080 breaks there. The lesson is in
[lessons-learned.md](../../playbooks/lessons-learned.md); image rules are in
[screenshot-capture](../screenshot-capture/SKILL.md). Accessibility (never colour alone) follows
[STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md).

## When to use

- Any change to a screen's templates, styles or scripts.
- Before class, on the class machine's real display settings.

## Inputs

- The screen served locally from recorded data (no model calls).
- A real-browser automation tool (for example Playwright).
- The list of screens and states to check (each tab, an empty list, a long run).

## Steps

1. **Fluid layout rules.** No fixed widths for the page; grids and flex wrap; long words and ids
   wrap or carry a full-text title; tables and long lists scroll inside their own box; pills stay on
   one line; text never smaller than about 12 CSS px.
2. **Cache-busting.** Version static asset URLs by content hash and send `Cache-Control: no-cache`;
   add a test asserting both, so a fixed layout reaches every browser.
3. **Automated sweep** in a real browser: widths 320 to 2560 CSS px in steps of 40, heights 600 and
   1000, pixel ratios 1.25, 1.5 and 2 at a few widths. On each screen assert: nothing scrolls
   sideways, no element wider than its box (except boxes built to scroll), nothing past the right
   edge, no clipped text, no ellipsis without a title, the page scrolls to its bottom, navigation back
   works.
4. **Named viewports** for screenshots: 1920 by 1080 at 125% and 150% scaling (1536 and 1280 CSS
   px), a small laptop (1366 by 768), browser zoom 150% and 175%, a phone width.
5. **Human review.** Save the named-viewport screenshots and look at every one. The automated
   checks miss overlaps, awkward wraps and unreadable contrast.
6. Fix failures test-first: add the failing viewport to the sweep, then fix the styles.
7. On the class machine, open the screen at its real scaling and zoom, and reload with a hard
   refresh.

## Outputs

- A green sweep, the screenshot set, and a short note of what a person checked.
- Tests for the layout rules and the cache headers.

## Checks

- The sweep reports 0 problems across all widths, heights and pixel ratios.
- A person has opened every named-viewport screenshot.
- The class machine shows the current styles at its own scaling (hard refresh done).
- Results reported as in [status-and-report-formats.md](../../playbooks/status-and-report-formats.md).
