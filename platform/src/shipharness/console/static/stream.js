// shipharness console client. Keys 1-5 switch screens, F cycles full screen for one arm
// (both -> bare -> harness -> both), H or Esc goes back to the run list. Screens arrive as server-rendered, escaped HTML over
// server-sent events (browser EventSource API). No build step, no CDN.
(function () {
  "use strict";
  var body = document.body;
  var run = body.getAttribute("data-run");
  if (!run) return;
  var FULL = ["", "bare", "harness"];

  function show(key) {
    if (!/^[1-5]$/.test(key)) return;
    body.setAttribute("data-screen", key);
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#" + key);
    }
  }

  function cycleFull() {
    var index = FULL.indexOf(body.getAttribute("data-full") || "");
    var next = FULL[(index + 1) % FULL.length];
    body.setAttribute("data-full", next);
    var label = document.getElementById("full-label");
    if (label) label.textContent = next || "both";
  }

  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    if (e.key >= "1" && e.key <= "5") {
      show(e.key);
      e.preventDefault();
    } else if (e.key === "f" || e.key === "F") {
      cycleFull();
      e.preventDefault();
    } else if (e.key === "h" || e.key === "H" || e.key === "Escape") {
      e.preventDefault();
      window.location.href = "/";
    }
  });

  document.addEventListener("click", function (e) {
    var tab = e.target && e.target.closest ? e.target.closest(".tab") : null;
    if (tab) show(tab.getAttribute("data-key"));
  });

  show((window.location.hash || "#1").slice(1));

  var conn = document.getElementById("conn");
  function status(text) { if (conn) conn.textContent = text; }

  var finished = body.getAttribute("data-finished") === "true";
  var source = new EventSource("/screens/" + encodeURIComponent(run));
  source.onopen = function () { status(finished ? "finished" : "live"); };
  source.onerror = function () { status(finished ? "finished" : "reconnecting"); };
  source.addEventListener("screens", function (message) {
    var update = JSON.parse(message.data);
    Object.keys(update.screens).forEach(function (key) {
      var section = document.getElementById("screen-" + key);
      // Server-rendered with autoescape: agent text is already escaped.
      if (section) section.innerHTML = update.screens[key];
    });
    body.setAttribute("data-recorded", update.recorded ? "true" : "false");
    body.setAttribute("data-seq", String(update.seq));
    // A complete run says "finished", not a live event counter.
    finished = update.finished === true;
    body.setAttribute("data-finished", finished ? "true" : "false");
    status(finished ? "finished" : "live · event " + update.seq);
  });
})();
