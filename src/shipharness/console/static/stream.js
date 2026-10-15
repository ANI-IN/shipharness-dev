// Minimal live stream of run events using the browser's EventSource API.
// The full five-screen console is built on the same /events/<run> stream.
(function () {
  "use strict";
  let source = null;

  function show(run) {
    const list = document.getElementById("events");
    const status = document.getElementById("status");
    list.textContent = "";
    if (source) source.close();
    source = new EventSource("/events/" + encodeURIComponent(run));
    status.textContent = "(connecting to " + run + ")";
    source.onopen = function () { status.textContent = "(live: " + run + ")"; };
    source.onerror = function () { status.textContent = "(reconnecting to " + run + ")"; };
    source.onmessage = append;
    [
      "run_start", "sandbox_start", "sandbox_usage", "sandbox_denied", "turn", "tool_call",
      "tool_result", "harness_decision", "blocked", "session_stop", "session_resume",
      "test_proposed", "test_filter_result", "check_progress", "check_result", "mutant_result",
      "reviewer_output", "gate_result", "claim", "verdict", "cost", "screenshot", "trace_link",
      "run_end",
    ].forEach(function (type) { source.addEventListener(type, append); });
  }

  function append(message) {
    const event = JSON.parse(message.data);
    const item = document.createElement("li");
    const arm = event.arm ? "[" + event.arm + "] " : "";
    const badge = event.recorded ? "RECORDING " : "";
    item.textContent = badge + "#" + event.seq + " " + arm + event.type;
    document.getElementById("events").prepend(item);
  }

  document.addEventListener("click", function (e) {
    const run = e.target && e.target.getAttribute && e.target.getAttribute("data-run");
    if (run) show(run);
  });
})();
