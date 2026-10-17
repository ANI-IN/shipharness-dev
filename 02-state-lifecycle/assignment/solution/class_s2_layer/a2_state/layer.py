"""The class's S2 state layer under the name the grader loads, to grade it as a baseline:

    uv run python submodules/02-state-lifecycle/solution/grader/grade.py \
        --impl submodules/02-state-lifecycle/solution/class_s2_layer
"""

from shipharness.harness.state.layer import StateLayer as ResumableStateLayer

__all__ = ["ResumableStateLayer"]
