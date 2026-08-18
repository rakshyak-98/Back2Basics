#!/usr/bin/env python3
"""Repair corrupted markdown table separator rows."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BROKEN_SEP = re.compile(r"^-+\|?\s*$")


def column_count(header: str) -> int:
    return header.count("|") - 1


def make_separator(cols: int) -> str:
    return "|" + "|".join([" --- "] * cols) + "|"


def repair_tables(text: str) -> str:
    # Strip orphan broken separator lines first
    lines = [ln for ln in text.splitlines() if not BROKEN_SEP.match(ln.strip())]
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and line.count("|") >= 2:
            block = [line]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip().startswith("|") or BROKEN_SEP.match(nxt.strip()):
                    block.append(nxt)
                    i += 1
                else:
                    break
            out.extend(fix_block(block))
        else:
            out.append(line)
            i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def fix_block(block: list[str]) -> list[str]:
    if not block:
        return block
    header = block[0]
    cols = column_count(header)
    if cols < 1:
        return block

    # Drop all broken separator fragments; keep real rows
    rows = [header]
    for line in block[1:]:
        stripped = line.strip()
        if BROKEN_SEP.match(stripped):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", stripped) and "---" in stripped:
            continue  # drop old separators; we insert a fresh one below
        rows.append(line)

    if len(rows) == 1:
        return rows

    return [rows[0], make_separator(cols), *rows[1:]]


def main() -> None:
    touched = 0
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fixed = repair_tables(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            touched += 1
            print(path.relative_to(ROOT))
    print(f"\nRepaired {touched} files")


if __name__ == "__main__":
    main()
