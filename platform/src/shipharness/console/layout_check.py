"""Layout checks for the console in a real browser (Playwright), shared by the browser tests and
`platform/scripts/check_console_layout.py` (recorded runs at the three class screen sizes).

For one screen: nothing scrolls sideways (document scrollWidth <= window width), no element clips
its content (overflow hidden with content taller or wider than the box), except the lists built to
scroll (`data-scroll`), every panel lies inside the window horizontally, and the page scrolls to its
bottom; no pill wraps onto a second line, and no word of 8 or more letters or digits breaks across
lines (names break only after _ . / or -).
"""

from __future__ import annotations

from typing import Any

SIZES: tuple[tuple[int, int], ...] = ((1366, 768), (1440, 900), (1920, 1080))

MEASURE_JS = """(key) => {
  const w = window.innerWidth;
  const screen = document.querySelector('#screen-' + key);
  const visible = [...screen.querySelectorAll('*')].filter(e => e.offsetParent !== null);
  const clipped = visible.filter(e => {
    if (e.closest('[data-scroll]')) return false;
    const cs = getComputedStyle(e);
    const hidesY = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
    const hidesX = cs.overflowX === 'hidden' || cs.overflowX === 'clip';
    return (hidesY && e.scrollHeight > e.clientHeight + 2) ||
           (hidesX && e.scrollWidth > e.clientWidth + 2);
  }).map(e => e.tagName.toLowerCase() + '.' + (e.className || '') + ' ' +
         (e.textContent || '').trim().slice(0, 40));
  const outside = [...screen.querySelectorAll('.panel')].filter(p => p.offsetParent !== null)
    .filter(p => { const r = p.getBoundingClientRect(); return r.left < -1 || r.right > w + 1; })
    .map(p => (p.querySelector('h2') || p).textContent.trim().slice(0, 30));
  const panels = [...screen.querySelectorAll('.panel')].filter(p => p.offsetParent !== null);
  const bottom = Math.max(0, ...panels.map(p => p.getBoundingClientRect().bottom + window.scrollY));
  window.scrollTo(0, document.documentElement.scrollHeight);
  const reached = window.scrollY + window.innerHeight >= bottom - 2;
  window.scrollTo(0, 0);
  const cw = document.documentElement.clientWidth;
  const wide = [...document.querySelectorAll('body *')].filter(e => e.offsetParent !== null)
    .filter(e => e.getBoundingClientRect().right > cw + 1 || e.scrollWidth > e.clientWidth + 1)
    .slice(0, 6).map(e => e.tagName.toLowerCase() + '.' + (e.className || '') + ' ' +
         Math.round(e.getBoundingClientRect().right) + '>' + cw +
         ' sw' + e.scrollWidth + '/' + e.clientWidth);
  // A pill on more than one line, or a word of 8+ letters or digits broken across lines.
  const wrappedPills = [...screen.querySelectorAll('.status')].filter(e => e.offsetParent !== null)
    .filter(e => {
      const cs = getComputedStyle(e);
      const line = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.35;
      return e.getBoundingClientRect().height > line * 1.6;
    }).map(e => e.textContent.trim().slice(0, 40));
  const brokenWords = [];
  const walker = document.createTreeWalker(screen, NodeFilter.SHOW_TEXT);
  while (walker.nextNode() && brokenWords.length < 5) {
    const node = walker.currentNode;
    if (!node.parentElement || node.parentElement.offsetParent === null) continue;
    if (node.parentElement.closest('[data-scroll]')) continue;
    for (const m of node.textContent.matchAll(/[A-Za-z0-9]{8,}/g)) {
      const range = document.createRange();
      range.setStart(node, m.index); range.setEnd(node, m.index + m[0].length);
      const tops = new Set([...range.getClientRects()].map(r => Math.round(r.top)));
      if (tops.size > 1) { brokenWords.push(m[0]); break; }
    }
  }
  return {scrollWidth: document.documentElement.scrollWidth, width: w, clipped, outside, wide,
          wrappedPills, brokenWords,
          panels: panels.length, reachedBottom: reached};
}"""


def screen_problems(page: Any, key: str) -> list[str]:
    """Every layout problem of screen `key` on the open console page (empty when it is fine)."""
    page.keyboard.press(key)
    m = page.evaluate(MEASURE_JS, key)
    problems: list[str] = []
    if m["panels"] < 1:
        problems.append("no panel shown")
    if m["scrollWidth"] > m["width"]:
        problems.append(f"scrolls sideways: {m['scrollWidth']} > {m['width']} ({m['wide']})")
    problems += [f"clipped: {c}" for c in m["clipped"]]
    problems += [f"panel outside the window: {o}" for o in m["outside"]]
    problems += [f"pill on more than one line: {p}" for p in m["wrappedPills"]]
    problems += [f"word broken across lines: {w}" for w in m["brokenWords"]]
    if not m["reachedBottom"]:
        problems.append("the page does not scroll to its last panel")
    return problems
