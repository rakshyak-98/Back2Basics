#!/usr/bin/env python3
"""Add or update per-note ## Index sections per NOTES_STANDARD."""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
HEADING_RE = re.compile(r"^## (.+)$")
FENCE_RE = re.compile(r"^```")


def parse_headings(lines: list[str]) -> list[str]:
    """Return ## headings outside fenced code blocks, excluding Index."""
    headings: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m and m.group(1).strip() != "Index":
            headings.append(m.group(1).strip())
    return headings


def build_index_block(headings: list[str]) -> list[str]:
    if not headings:
        return []
    block = ["## Index", ""]
    block.extend(f"- [[#{h}]]" for h in headings)
    block.append("")
    return block


def find_index_span(lines: list[str]) -> tuple[int, int] | None:
    """Return [start, end) line indices of existing Index section body (incl. heading)."""
    in_fence = False
    start: int | None = None
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.strip() == "## Index":
            start = i
            continue
        if start is not None and HEADING_RE.match(line):
            return start, i
    if start is not None:
        return start, len(lines)
    return None


def first_content_heading_line(lines: list[str]) -> int | None:
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m and m.group(1).strip() != "Index":
            return i
    return None


def trim_trailing_blank_lines(lines: list[str]) -> list[str]:
    out = list(lines)
    while out and out[-1] == "":
        out.pop()
    return out


def process_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text[1:]

    had_trailing_newline = text.endswith("\n")
    lines = text.splitlines()
    headings = parse_headings(lines)

    if not headings:
        return "skip_no_headings"

    index_block = build_index_block(headings)
    span = find_index_span(lines)

    if span:
        start, end = span
        new_lines = lines[:start] + index_block + lines[end:]
        action = "updated"
    else:
        insert_at = first_content_heading_line(lines)
        if insert_at is None:
            return "skip_no_insert"
        intro = trim_trailing_blank_lines(lines[:insert_at])
        rest = lines[insert_at:]
        new_lines = intro + [""] + index_block + rest
        action = "added"

    new_text = "\n".join(new_lines)
    if had_trailing_newline or not new_text.endswith("\n"):
        new_text += "\n"

    if new_text == text if text.endswith("\n") else text + "\n":
        # normalize comparison
        old_norm = text if text.endswith("\n") else text + "\n"
        if new_text == old_norm:
            return "unchanged"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return action


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    stats: dict[str, int] = {}
    errors: list[str] = []

    for path in sorted(VAULT_ROOT.rglob("*.md")):
        if path.name.startswith("."):
            continue
        rel = path.relative_to(VAULT_ROOT)
        if rel.parts and rel.parts[0] in {"scripts", ".git"}:
            continue
        try:
            result = process_file(path, dry_run=dry_run)
            stats[result] = stats.get(result, 0) + 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel}: {exc}")

    print("Results:")
    for key in sorted(stats):
        print(f"  {key}: {stats[key]}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for err in errors[:20]:
            print(f"  {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
