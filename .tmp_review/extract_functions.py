#!/usr/bin/env python3
"""Extract and print Python function definitions from this repository.

This walks the repository tree, parses each Python file with ``ast``, and
prints the source for every function or method definition it finds.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".idea", ".venv", "outputs", ".tmp_review"}


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def extract_function_sources(path: Path) -> list[tuple[str, int, int, str]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    lines = source.splitlines()
    extracted: list[tuple[str, int, int, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.lineno is None or node.end_lineno is None:
            continue

        snippet = "\n".join(lines[node.lineno - 1 : node.end_lineno])
        extracted.append((node.name, node.lineno, node.end_lineno, snippet))

    return sorted(extracted, key=lambda item: (item[1], item[2], item[0]))


def main() -> int:
    first_file = True
    for path in iter_python_files(ROOT):
        functions = extract_function_sources(path)
        if not functions:
            continue

        if not first_file:
            print()
        first_file = False

        if "test" in str(path.relative_to(ROOT)) :
            continue
        print(f"## {path.relative_to(ROOT)}")
        for name, start, end, snippet in functions:
            print(f"\n### {name} [{start}:{end}]")
            print(snippet)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
