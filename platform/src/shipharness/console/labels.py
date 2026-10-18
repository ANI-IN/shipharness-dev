"""How the console and the terminal name referee checks, test filters, and primary measures.

People read "<Kind> N: <name>" (`shipharness.datasets.names`): "House rule 1: Tenant isolation",
"Filter 3: Adds coverage or catches a mutant". Event payloads, scores, and exports keep the machine
ids (`r1_tenant`, `R1`, `r1_new_violations`, filter numbers); only the words shown change.
"""

from __future__ import annotations

import re

from shipharness.datasets.names import (
    FILTER_NAMES,
    RULE_NAMES,
    filter_label,
    rule_label,
    rule_short,
)

# Primary-measure fields as people read them.
MEASURE_LABELS = {
    "r1_new_violations": f"{rule_label('R1')}, new violations",
    "continuity_failure": "continuity failure",
    "out_of_scope_files": "out-of-scope files",
    "test_phase_source_edits": "test-phase source edits",
    "hidden_passed": "hidden tests passed",
    "mutants_killed": "mutants killed",
}


# A rule check's name ("r1_tenant", `shipharness.checks.builtin.RULE_LABELS`) or its rule label.
_RULE_CHECK = re.compile(r"[Rr]([0-9])(_[a-z_]+)?")


def _rule(name: str) -> str | None:
    """The house rule a check name ("r1_tenant") or rule label ("R1") stands for, else None."""
    match = _RULE_CHECK.fullmatch(name)
    code = f"R{match.group(1)}" if match else ""
    return code if code in RULE_NAMES else None


def check_label(name: str) -> str:
    """'House rule 1: Tenant isolation' for r1_tenant or R1; any other check name unchanged."""
    code = _rule(name)
    return rule_label(code) if code else name


def check_short(name: str) -> str:
    """'House rule 1' for r1_tenant or R1 (where space is tight); any other name unchanged."""
    code = _rule(name)
    return rule_short(code) if code else name


def filter_name(number: int) -> str:
    """'Filter 3: Adds coverage or catches a mutant'; 'Filter 9' for a number without a name."""
    return filter_label(number) if number in FILTER_NAMES else f"Filter {number}"


def measure_label(name: str) -> str:
    """'House rule 1: Tenant isolation, new violations' for r1_new_violations; others as is."""
    return MEASURE_LABELS.get(name, name)
