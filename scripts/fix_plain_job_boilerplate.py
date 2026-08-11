#!/usr/bin/env python3
"""Replace generic 'plain job' mental models and placeholder gotchas with one-liner text."""

from __future__ import annotations

import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP = {"AGENTS.md", "INDEX.md", "README.md", "NOTES_STANDARD.md"}

PLAIN_JOB_RE = re.compile(
    r"\*\*Say it in one breath:\*\*[^\n]*plain job, how I run it, how I know it[’']s broken\.\s*\n+",
    re.IGNORECASE,
)

GENERIC_GOTCHA_RE = re.compile(
    r"\n## Gotchas\n\n> \[!WARNING\]\n> Prefer simple words you can say in an interview\.\n",
    re.MULTILINE,
)

GENERIC_WHEN_NOT_RE = re.compile(
    r"\n## When NOT to use\n\n- Skip it when a simpler existing tool already fits\.\n",
    re.MULTILINE,
)

PLACEHOLDER_STD_RE = re.compile(
    r"\n## Standard config / commands\n\n```bash\n# reproduce with minimal input\n# compare working versus broken environment\n```\n",
    re.MULTILINE,
)

ONELINER_RE = re.compile(r"^> (.+)$", re.MULTILINE)


def oneliner(text: str) -> str | None:
    for m in ONELINER_RE.finditer(text):
        line = m.group(1).strip()
        if line.startswith("[!"):
            continue
        return line
    return None


def process(text: str) -> str:
    ol = oneliner(text)
    if ol and PLAIN_JOB_RE.search(text):
        text = PLAIN_JOB_RE.sub(f"**Say it in one breath:** {ol}\n\n", text)
    text = GENERIC_GOTCHA_RE.sub("\n", text)
    text = GENERIC_WHEN_NOT_RE.sub("\n", text)
    text = PLACEHOLDER_STD_RE.sub("\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def main() -> None:
    n = 0
    for path in sorted(VAULT.rglob("*.md")):
        if path.name in SKIP or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new = process(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    print("updated", n, "files")


if __name__ == "__main__":
    main()
