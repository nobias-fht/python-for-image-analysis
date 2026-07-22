#!/usr/bin/env python3
"""Strip code inside exercise blocks while preserving the markers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EXERCISE_START = "# --- Exercise"
EXERCISE_END = "# ---"


def strip_exercise_lines(lines: list[str], *, context: str = "input") -> list[str]:
    output: list[str] = []
    inside_exercise = False

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped == EXERCISE_START:
            if inside_exercise:
                raise ValueError(
                    f"Nested exercise block is not allowed in {context} at line {line_number}"
                )
            output.append(line)
            inside_exercise = True
            continue

        if stripped == EXERCISE_END:
            if not inside_exercise:
                output.append(line)
                continue
            output.append(line)
            inside_exercise = False
            continue

        if not inside_exercise:
            output.append(line)

    if inside_exercise:
        raise ValueError(f"Unclosed exercise block in {context}")

    return output


def strip_exercise_blocks(text: str) -> str:
    return "".join(strip_exercise_lines(text.splitlines(keepends=True)))


def strip_exercise_blocks_in_notebook(notebook: dict) -> dict:
    for cell_index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        context = f"cell {cell_index}"
        if isinstance(source, str):
            source_lines = source.splitlines(keepends=True)
            filtered = strip_exercise_lines(source_lines, context=context)
            cell["source"] = "".join(filtered)
        else:
            cell["source"] = strip_exercise_lines(source, context=context)
    return notebook


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+", type=Path)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write to this path instead of stdout.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file with the filtered notebook or script.",
    )
    args = parser.parse_args()

    if args.output is not None and args.in_place:
        raise ValueError("Use either --output or --in-place, not both")
    if args.output is not None and len(args.input_paths) != 1:
        raise ValueError("--output can only be used with a single input file")
    if not args.in_place and len(args.input_paths) != 1:
        raise ValueError("Multiple input files require --in-place")

    for input_path in args.input_paths:
        if input_path.suffix == ".ipynb":
            notebook = json.loads(input_path.read_text())
            filtered = json.dumps(
                strip_exercise_blocks_in_notebook(notebook),
                indent=1,
                ensure_ascii=True,
            )
            if not filtered.endswith("\n"):
                filtered += "\n"
        else:
            filtered = strip_exercise_blocks(input_path.read_text())

        if args.in_place:
            input_path.write_text(filtered)
        elif args.output is None:
            print(filtered, end="")
        else:
            args.output.write_text(filtered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
