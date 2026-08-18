#!/usr/bin/env python3
"""Insert or replace the one-line > definition under the first real H1.

Skips `#` lines inside fenced code blocks (shell comments, etc.).

Usage:
  python3 tools/apply_definition.py path/to/note.md 'Definition text here'
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def _first_h1_outside_fences(lines: list[str]) -> int | None:
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Real markdown H1: "# Title" — not "##" and not "#comment" without space after #
        if re.match(r"^# [^#]", line):
            return i
    return None


def apply_definition(path: Path, definition: str) -> str:
    text = path.read_text(encoding="utf-8")
    definition = definition.strip()
    if definition.startswith(">"):
        definition = definition[1:].strip()
    blurb = f"> {definition}"

    lines = text.splitlines(keepends=True)
    h1_idx = _first_h1_outside_fences(lines)

    if h1_idx is None:
        insert_at = 0
        while insert_at < len(lines):
            s = lines[insert_at].strip()
            if s == "" or re.fullmatch(r"(\[\[.*?\]\]\s*)+", s):
                insert_at += 1
                continue
            break
        title = path.stem
        block = [f"# {title}\n", "\n", blurb + "\n", "\n"]
        lines[insert_at:insert_at] = block
        path.write_text("".join(lines), encoding="utf-8")
        return "added_h1_and_def"

    j = h1_idx + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and re.match(r"^>\s+(?!\[!)", lines[j]):
        lines[j] = blurb + "\n"
        path.write_text("".join(lines), encoding="utf-8")
        return "replaced_def"

    insert = []
    if h1_idx + 1 >= len(lines) or lines[h1_idx + 1].strip() != "":
        insert.append("\n")
    insert.append(blurb + "\n")
    insert.append("\n")
    lines[h1_idx + 1 : h1_idx + 1] = insert
    path.write_text("".join(lines), encoding="utf-8")
    return "inserted_def"


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: apply_definition.py <path.md> <definition>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[1])
    definition = sys.argv[2]
    print(apply_definition(path, definition))


if __name__ == "__main__":
    main()
