#!/usr/bin/env python3
"""Remove note-strategy HTML comments from vault notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

SKIP_FILES = frozenset(
    {
        "AGENTS.md",
        "NOTES_STANDARD.md",
        "NOTETAKING_STRATEGIES.md",
        "INDEX.md",
        "README.md",
    }
)

STRATEGY_TAG_RE = re.compile(r"^\s*<!--\s*note-strategy:\s*[a-z]+\s*-->\s*\n?", re.I)


def strip_tags(text: str) -> tuple[str, bool]:
    if not STRATEGY_TAG_RE.match(text):
        return text, False
    return STRATEGY_TAG_RE.sub("", text, count=1), True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    changed = 0
    unchanged = 0

    for path in sorted(VAULT_ROOT.rglob("*.md")):
        if path.name.startswith("."):
            continue
        rel = path.relative_to(VAULT_ROOT)
        if rel.parts and rel.parts[0] in {"scripts", ".git"}:
            continue
        if path.name in SKIP_FILES:
            continue

        original = path.read_text(encoding="utf-8")
        if original.startswith("\ufeff"):
            original = original[1:]
        updated, did_change = strip_tags(original)
        if not did_change:
            unchanged += 1
            continue
        changed += 1
        if not dry_run:
            path.write_text(updated, encoding="utf-8", newline="\n")

    print(f"changed: {changed}")
    print(f"unchanged: {unchanged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
