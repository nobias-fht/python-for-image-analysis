#!/usr/bin/env python3
"""Convert notebook-style Python lesson scripts to Jupyter notebooks.

The course scripts use VSCode/Jupytext-style cell markers:

- ``# %% [markdown]`` starts a markdown cell.
- ``# %%`` starts a code cell.

By default this converts all ``modules/**/*.py`` lesson scripts into
``notebooks/**/*.ipynb`` while preserving the module directory structure.
No third-party package is required.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

CellKind = Literal["code", "markdown"]


@dataclass
class ParsedCell:
    kind: CellKind
    lines: list[str] = field(default_factory=list)


def is_cell_marker(line: str) -> bool:
    return line.startswith("# %%")


def marker_kind(line: str) -> CellKind:
    marker = line.strip().lower()
    if marker.startswith("# %% [markdown]"):
        return "markdown"
    return "code"


def markdown_source(lines: list[str]) -> list[str]:
    """Remove Python comment prefixes from a markdown cell."""
    source: list[str] = []
    for line in lines:
        if line.startswith("# "):
            source.append(line[2:])
        elif line.startswith("#"):
            source.append(line[1:])
        else:
            source.append(line)
    return source


def parse_percent_script(path: Path) -> list[ParsedCell]:
    cells: list[ParsedCell] = []
    current: ParsedCell | None = None

    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if is_cell_marker(line):
            if current is not None:
                cells.append(current)
            current = ParsedCell(kind=marker_kind(line))
            continue

        if current is None:
            current = ParsedCell(kind="code")
        current.lines.append(line)

    if current is not None:
        cells.append(current)

    return [cell for cell in cells if cell.lines or cell.kind == "markdown"]


def notebook_cell(cell: ParsedCell) -> dict:
    if cell.kind == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": markdown_source(cell.lines),
        }

    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell.lines,
    }


def notebook_document(cells: list[ParsedCell]) -> dict:
    return {
        "cells": [notebook_cell(cell) for cell in cells],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def convert_script(source_path: Path, source_root: Path, output_root: Path, overwrite: bool) -> Path:
    relative = source_path.relative_to(source_root).with_suffix(".ipynb")
    output_path = output_root / relative

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} already exists; pass --overwrite to replace it")

    cells = parse_percent_script(source_path)
    notebook = notebook_document(cells)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return output_path


def find_scripts(source_root: Path) -> list[Path]:
    return sorted(path for path in source_root.rglob("*.py") if path.is_file() and "__pycache__" not in path.parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert notebook-style Python lesson scripts to .ipynb notebooks."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("modules"),
        help="Directory containing .py scripts to convert. Default: modules",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("notebooks"),
        help="Directory where notebooks are written. Default: notebooks",
    )
    parser.add_argument(
        "--overwrite",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Replace existing notebooks. Default: true",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    source_root = args.source.resolve()
    output_root = args.output.resolve()

    if not source_root.exists():
        raise SystemExit(f"Source directory does not exist: {source_root}")

    scripts = find_scripts(source_root)
    if not scripts:
        raise SystemExit(f"No Python scripts found in {source_root}")

    for source_path in scripts:
        output_path = convert_script(
            source_path=source_path,
            source_root=source_root,
            output_root=output_root,
            overwrite=args.overwrite,
        )
        print(f"{source_path.relative_to(source_root)} -> {output_path.relative_to(output_root)}")

    print(f"Converted {len(scripts)} script(s) to {output_root}")


if __name__ == "__main__":
    main()
