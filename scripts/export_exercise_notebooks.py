#!/usr/bin/env python3
"""Export stripped exercise notebooks from solution notebooks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from strip_exercise_blocks import strip_exercise_blocks_in_notebook

REPO_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_ROOT / "solutions"
EXERCISES_DIR = REPO_ROOT / "exercises"


def solution_notebook_path_for(path: Path) -> Path | None:
    if path.parent != SOLUTIONS_DIR:
        return None
    if path.suffix == ".ipynb":
        return path
    if path.suffix == ".py":
        return path.with_suffix(".ipynb")
    return None


def exercise_notebook_path_for(solution_notebook_path: Path) -> Path:
    return EXERCISES_DIR / solution_notebook_path.name


def export_notebook(solution_notebook_path: Path) -> None:
    notebook = json.loads(solution_notebook_path.read_text())
    stripped = strip_exercise_blocks_in_notebook(notebook)
    output_path = exercise_notebook_path_for(solution_notebook_path)
    output_path.write_text(json.dumps(stripped, indent=1, ensure_ascii=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    notebook_paths: set[Path] = set()
    for raw_path in args:
        notebook_path = solution_notebook_path_for(Path(raw_path).resolve())
        if notebook_path is None or not notebook_path.exists():
            continue
        notebook_paths.add(notebook_path)

    for notebook_path in sorted(notebook_paths):
        export_notebook(notebook_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
