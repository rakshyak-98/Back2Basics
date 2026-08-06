#!/usr/bin/env python3
"""Apply NOTES_STANDARD canonical template structure to vault notes."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

SKIP_FILES = frozenset(
    {
        "AGENTS.md",
        "NOTES_STANDARD.md",
        "INDEX.md",
        "README.md",
    }
)

CANONICAL_ORDER = [
    "Mental model",
    "Standard config / commands",
    "Triage (when things break)",
    "Gotchas",
    "When NOT to use",
    "Related",
]

CANONICAL_ALIASES: dict[str, list[str]] = {
    "Mental model": [
        "mental model",
        "overview",
        "concept",
        "concepts",
        "understanding",
        "how it works",
        "core concepts",
        "introduction",
    ],
    "Standard config / commands": [
        "standard config",
        "configuration",
        "commands",
        "setup",
        "usage",
        "cli",
        "config",
        "install",
        "standard configuration",
    ],
    "Triage (when things break)": [
        "triage",
        "troubleshoot",
        "troubleshooting",
        "debug",
        "debugging",
        "when things break",
        "common issues",
        "errors",
        "failure",
    ],
    "Gotchas": ["gotchas", "pitfalls", "caveats", "warnings", "gotcha"],
    "When NOT to use": [
        "when not to use",
        "when not",
        "anti-pattern",
        "anti-patterns",
        "limitations",
    ],
    "Related": ["related", "see also", "references", "further reading", "links"],
}

PLACEHOLDERS: dict[str, list[str]] = {
    "Mental model": ["…"],
    "Standard config / commands": ["…"],
    "Triage (when things break)": [
        "",
        "| Symptom | Check | Fix |",
        "|---------|-------|-----|",
        "| … | … | … |",
    ],
    "Gotchas": ["", "> [!WARNING]", "> …"],
    "When NOT to use": ["…"],
    "Related": ["[[…]]"],
}

H1_RE = re.compile(r"^# (.+)$")
H2_RE = re.compile(r"^## (.+)$")
FENCE_RE = re.compile(r"^\s*```")
WIKILINK_LINE_RE = re.compile(r"^(\[\[[^\]]+\]\]\s*)+$")


@dataclass
class Section:
    heading: str
    lines: list[str] = field(default_factory=list)
    canonical: str | None = None


def canonical_for_heading(heading: str) -> str | None:
    h = heading.strip().lower()
    for canon, aliases in CANONICAL_ALIASES.items():
        if h == canon.lower():
            return canon
        if h.startswith(canon.lower()):
            return canon
        for alias in aliases:
            if h == alias or h.startswith(alias):
                return canon
    return None


def is_placeholder_content(lines: list[str]) -> bool:
    stripped = [ln.strip() for ln in lines if ln.strip()]
    if not stripped:
        return True
    placeholder_markers = {"…", "...", "[[…]]", "[[...]]"}
    if all(s in placeholder_markers for s in stripped):
        return True
    if stripped == ["> [!WARNING]", "> …"] or stripped == ["> [!WARNING]", "> ..."]:
        return True
    if stripped[:3] == ["| Symptom | Check | Fix |", "|---------|-------|-----|", "| … | … | … |"]:
        return True
    return False


def split_sections(lines: list[str]) -> tuple[list[str], list[Section]]:
    """Return intro lines (before first ##) and parsed sections."""
    intro: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    in_fence = False

    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence

        if H2_RE.match(line):
            if in_fence:
                # Unclosed fence before a real section — treat as broken markdown.
                in_fence = False
            if current is not None:
                sections.append(current)
            heading = H2_RE.match(line).group(1).strip()
            current = Section(
                heading=heading,
                canonical=canonical_for_heading(heading),
            )
            continue

        if current is None:
            intro.append(line)
        else:
            current.lines.append(line)

    if current is not None:
        sections.append(current)

    return intro, sections


def extract_wikilinks(intro: list[str]) -> tuple[list[str], list[str]]:
    wikilinks: list[str] = []
    rest: list[str] = []
    for line in intro:
        if WIKILINK_LINE_RE.match(line.strip()):
            wikilinks.append(line.strip())
        else:
            rest.append(line)
    return wikilinks, rest


def extract_title_and_oneliner(intro: list[str], default_title: str) -> tuple[str, str, list[str]]:
    title = default_title
    oneliner = ""
    orphan: list[str] = []
    i = 0
    while i < len(intro):
        line = intro[i]
        m = H1_RE.match(line)
        if m:
            title = m.group(1).strip()
            i += 1
            continue
        if line.startswith("> ") and not oneliner:
            # Obsidian callouts are content, not the one-line summary.
            if line[2:].startswith("[!"):
                orphan.append(line)
                i += 1
                while i < len(intro) and intro[i].startswith("> "):
                    orphan.append(intro[i])
                    i += 1
                continue
            oneliner_parts = [line[2:]]
            i += 1
            while i < len(intro) and intro[i].startswith("> "):
                oneliner_parts.append(intro[i][2:])
                i += 1
            oneliner = " ".join(oneliner_parts).strip()
            continue
        if line.strip() in {"", "---"}:
            i += 1
            continue
        orphan.append(line)
        i += 1
    return title, oneliner, orphan


def infer_parent_wikilink(path: Path) -> str | None:
    try:
        rel = path.relative_to(VAULT_ROOT)
    except ValueError:
        rel = path
    if len(rel.parts) > 1:
        parent = rel.parent.name
        if parent not in {".", "scripts"}:
            return f"[[{parent}]]"
    return None


def default_oneliner(title: str) -> str:
    return f"One-line: what / why for **{title}** — source TBD."


def build_index(headings: list[str]) -> list[str]:
    block = ["## Index", ""]
    block.extend(f"- [[#{h}]]" for h in headings)
    block.append("")
    return block


def merge_sections(sections: list[Section]) -> tuple[dict[str, Section], list[Section]]:
    """Map canonical sections; return canonical dict + custom sections in order."""
    canonical: dict[str, Section] = {}
    custom: list[Section] = []

    for sec in sections:
        if sec.heading == "Index":
            continue
        key = sec.canonical
        if key:
            if key in canonical:
                canonical[key].lines.extend(["", f"### {sec.heading}", ""])
                canonical[key].lines.extend(sec.lines)
            else:
                canonical[key] = Section(
                    heading=sec.heading if sec.heading != key else key,
                    lines=list(sec.lines),
                    canonical=key,
                )
                if sec.heading.lower().startswith(key.lower()):
                    canonical[key].heading = sec.heading
        else:
            custom.append(sec)

    return canonical, custom


def section_has_content(sec: Section | None) -> bool:
    return sec is not None and not is_placeholder_content(sec.lines)


KEYWORD_RE: dict[str, re.Pattern[str]] = {
    "Standard config / commands": re.compile(
        r"\b(commands?|configuration|configuring|setup|cli|install|usage|init)\b",
        re.I,
    ),
    "Triage (when things break)": re.compile(
        r"\b(triage|debug(?:ging)?|troubleshoot(?:ing)?|errors?|failures?|issues?)\b",
        re.I,
    ),
    "Gotchas": re.compile(r"\b(gotchas?|pitfalls?|caveats?|warnings?)\b", re.I),
    "When NOT to use": re.compile(r"\b(when\s+not|limitations?)\b", re.I),
}


def heading_matches_keywords(heading: str, canon: str) -> bool:
    pattern = KEYWORD_RE.get(canon)
    return bool(pattern and pattern.search(heading))


def should_skip_placeholder(canon: str, custom: list[Section], canonical: dict[str, Section]) -> bool:
    if canon in canonical and section_has_content(canonical[canon]):
        return True
    return any(heading_matches_keywords(s.heading, canon) for s in custom)


def rebuild_note(path: Path, lines: list[str]) -> list[str]:
    default_title = path.stem
    intro, sections = split_sections(lines)
    wikilinks, intro_body = extract_wikilinks(intro)
    title, oneliner, orphan = extract_title_and_oneliner(intro_body, default_title)

    canonical, custom = merge_sections(sections)

    if orphan:
        mental = canonical.get("Mental model")
        orphan_block = orphan + ([""] if orphan else [])
        if mental:
            if section_has_content(mental):
                mental.lines = orphan_block + [""] + mental.lines
            else:
                mental.lines = orphan_block + mental.lines
        else:
            canonical["Mental model"] = Section(
                heading="Mental model",
                lines=orphan_block,
                canonical="Mental model",
            )

    for canon in CANONICAL_ORDER:
        if canon in canonical:
            if not section_has_content(canonical[canon]):
                canonical[canon].lines = list(PLACEHOLDERS[canon])
            continue
        if should_skip_placeholder(canon, custom, canonical):
            continue
        canonical[canon] = Section(
            heading=canon,
            lines=list(PLACEHOLDERS[canon]),
            canonical=canon,
        )

    if not wikilinks:
        parent = infer_parent_wikilink(path)
        if parent:
            wikilinks = [parent]

    ordered_headings: list[str] = []
    body: list[str] = []

    if wikilinks:
        body.extend(wikilinks)
        body.append("")

    body.append(f"# {title}")
    body.append("")
    body.append(f"> {oneliner or default_oneliner(title)}")
    body.append("")
    body.append("---")
    body.append("")

    # Index after intro; content order: mental, standard, custom, triage, gotchas, when not, related
    content_sections: list[Section] = []
    for canon in CANONICAL_ORDER[:2]:
        if canon in canonical:
            content_sections.append(canonical[canon])
    content_sections.extend(custom)
    for canon in CANONICAL_ORDER[2:]:
        if canon in canonical:
            content_sections.append(canonical[canon])

    for sec in content_sections:
        ordered_headings.append(sec.heading)

    body.extend(build_index(ordered_headings))

    for sec in content_sections:
        body.append(f"## {sec.heading}")
        body.append("")
        trimmed = list(sec.lines)
        while trimmed and trimmed[0] == "":
            trimmed.pop(0)
        while trimmed and trimmed[-1] == "":
            trimmed.pop()
        if trimmed:
            body.extend(trimmed)
            body.append("")

    while body and body[-1] == "":
        body.pop()

    return body


def normalize_lines(lines: list[str]) -> list[str]:
    return [ln.rstrip() for ln in lines]


def process_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines()
    new_lines = rebuild_note(path, lines)
    old_norm = normalize_lines(lines)
    new_norm = normalize_lines(new_lines)

    if old_norm == new_norm:
        return "unchanged"

    new_text = "\n".join(new_norm) + "\n"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return "updated"


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
        if path.name in SKIP_FILES:
            stats["skipped_meta"] = stats.get("skipped_meta", 0) + 1
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
        for err in errors[:30]:
            print(f"  {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
