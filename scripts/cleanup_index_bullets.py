#!/usr/bin/env python3
"""Remove leftover template Index bullet blocks from notes."""

import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP = {"AGENTS.md", "README.md", "INDEX.md"}

BLOCK_RE = re.compile(
    r"\n---\n+(?:- \[\[#.*?\]\]\n)+\n*",
    re.MULTILINE,
)


def main() -> None:
    n = 0
    for path in VAULT.rglob("*.md"):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        new = BLOCK_RE.sub("\n---\n\n", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    print(f"cleaned={n}")


if __name__ == "__main__":
    main()
