"""Build the course diagrams as .excalidraw files (one style, from code).

Usage (from this folder):
    uv run --with fonttools --with brotli python build.py REPO_ROOT [STEM ...]
    uv run --with playwright python render.py REPO_ROOT/docs/diagrams REPO_ROOT/section-*/diagrams

Each diagram is a function below. Stepped diagrams also get `<stem>-step-N` frames, each adding
one element; `<stem>` is the full diagram (the same as the last step). Render PNG and SVG with
render.py afterwards. Every label comes from a file in the repository; the source is noted
next to each diagram.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path

from diagrams_a import register as register_a
from diagrams_b import register as register_b
from diagrams_c import register as register_c
from exlib import Scene, metrics

DOCS = "docs/diagrams"
S1 = "section-1-instructions/diagrams"
S2 = "section-2-state-lifecycle/diagrams"
S3 = "section-3-scope-sandbox/diagrams"
S4 = "section-4-verification/diagrams"

REGISTRY: list[tuple[str, str, bool, Callable[[Scene], None]]] = []


def diagram(folder: str, stem: str, steps: bool = False):
    def wrap(fn: Callable[[Scene], None]) -> Callable[[Scene], None]:
        REGISTRY.append((folder, stem, steps, fn))
        return fn

    return wrap


register_a(diagram, DOCS, S1, S2, S3, S4)
register_b(diagram, DOCS, S1, S2, S3, S4)
register_c(diagram, DOCS, S1, S2, S3, S4)


def write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    root = Path(argv[0])
    only = set(argv[1:])
    for folder, stem, steps, fn in REGISTRY:
        if only and stem not in only:
            continue
        scene = Scene(stem)
        fn(scene)
        if steps:
            scene.pin_bounds()
        out = root / folder
        write(out / f"{stem}.excalidraw", scene.document())
        frames = 0
        if steps:
            for k in range(1, scene.stages + 1):
                write(out / f"{stem}-step-{k}.excalidraw", scene.document(k))
                frames += 1
        print(f"{folder}/{stem}: {len(scene.els)} elements, {frames} frames")
    if metrics().missing:
        print("MISSING GLYPHS:", "".join(sorted(metrics().missing)))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
