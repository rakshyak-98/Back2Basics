#!/usr/bin/env python3
"""Transform template-structured notes to AGENT_NOTE_RULES layout (no fixed skeleton)."""

from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP = {
    "AGENTS.md",
    "AGENT_NOTE_RULES.md",
    "README.md",
    "INDEX.md",
}

SECTION_MAP = {
    "mental model": "How it works",
    "overview": "How it works",
    "concept": "How it works",
    "concepts": "How it works",
    "understanding": "How it works",
    "how it works": "How it works",
    "core concepts": "How it works",
    "introduction": "How it works",
    "standard config / commands": "Configuration and commands",
    "standard config": "Configuration and commands",
    "configuration": "Configuration and commands",
    "commands": "Configuration and commands",
    "setup": "Configuration and commands",
    "usage": "Configuration and commands",
    "cli": "Configuration and commands",
    "config": "Configuration and commands",
    "install": "Configuration and commands",
    "routing table": "Where to go next",
    "domain links": "Related topics in this domain",
    "triage (when things break)": "When things break",
    "triage": "When things break",
    "troubleshoot": "When things break",
    "troubleshooting": "When things break",
    "debug": "When things break",
    "debugging": "When things break",
    "when things break": "When things break",
    "gotchas": "Gotchas",
    "when not to use": "When not to use",
    "related": "Related",
    "sources": "Sources",
    "decision context": "Decision context",
    "comparison matrix": "Comparison",
    "selection guide": "How to choose",
    "per-option gotchas": "Per-option caveats",
    "trigger / symptoms": "When to use this runbook",
    "preconditions": "Before you start",
    "steps": "Steps",
    "verification": "Verification",
    "rollback": "Rollback",
    "escalation": "Escalation",
    "prerequisites": "Before you start",
    "purpose": "Purpose",
    "quality examples (optional)": "Examples",
    "context": "Context",
    "decision": "Decision",
    "consequences": "Consequences",
    "alternatives considered": "Alternatives considered",
    "quick reference": "Quick reference",
    "common commands": "Common commands",
    "options / flags": "Options and flags",
    "examples": "Examples",
    "variations / implementations": "Variations",
    "trade-offs": "Trade-offs",
    "when to use / when not": "When to use",
    "core idea": "Core idea",
    "isolation levels & anomalies": "Isolation levels and anomalies",
    "engine defaults (know before you deploy)": "Engine defaults",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FENCE_RE = re.compile(r"^\s*```")
INDEX_RE = re.compile(r"^## Index\s*$", re.I)
MENTAL_MODEL_RE = re.compile(r"^## Mental model\s*$", re.I)
PLACEHOLDER_ONLY = re.compile(r"^[\s…\.]*$|^One-line:.*source TBD")


def normalize_heading(name: str) -> str:
    return SECTION_MAP.get(name.strip().lower(), name.strip())


def parse_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """Return preamble (before first ##) and section bodies keyed by normalized heading."""
    preamble: list[str] = []
    sections: dict[str, list[str]] = {}
    current_key: str | None = None
    in_fence = False

    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            if current_key is None:
                preamble.append(line)
            else:
                sections[current_key].append(line)
            continue

        if not in_fence:
            m = HEADING_RE.match(line)
            if m and m.group(1) == "##":
                raw = m.group(2).strip()
                if raw.lower() == "index":
                    current_key = None
                    continue
                current_key = normalize_heading(raw)
                if current_key not in sections:
                    sections[current_key] = []
                continue

        if current_key is None:
            preamble.append(line)
        else:
            sections[current_key].append(line)

    return preamble, sections


def is_substantive(body: list[str]) -> bool:
    text = "\n".join(body).strip()
    if not text:
        return False
    if PLACEHOLDER_ONLY.match(text):
        return False
    if text in ("…", "...", "- …"):
        return False
    if re.fullmatch(r"[-\s…\.]+", text):
        return False
    return True


def wiki_source(title: str) -> str:
    q = title.split("#")[-1].strip()
    q = re.sub(r"\s*\([^)]*\)\s*", " ", q).strip()
    url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(q.replace(" ", "_"))
    return f"- [Wikipedia — {q}]({url})"


def transform(content: str, title: str) -> str | None:
    if not MENTAL_MODEL_RE.search(content) and "## Index" not in content:
        return None

    lines = content.splitlines()
    preamble, sections = parse_sections(lines)

    # Clean preamble — drop duplicate empty blockquote lines from old templates
    out_preamble: list[str] = []
    for line in preamble:
        if line.strip() == "---" and out_preamble and out_preamble[-1].strip() == "---":
            continue
        out_preamble.append(line)

    out: list[str] = []
    out.extend(out_preamble)

    # Preferred section order for output (only emitted if present)
    preferred = [
        "Purpose",
        "How it works",
        "Core idea",
        "Decision context",
        "Context",
        "Quick reference",
        "Configuration and commands",
        "Common commands",
        "Options and flags",
        "Examples",
        "Where to go next",
        "Related topics in this domain",
        "When things break",
        "When to use this runbook",
        "Before you start",
        "Steps",
        "Verification",
        "Rollback",
        "Escalation",
        "Isolation levels and anomalies",
        "Engine defaults",
        "Variations",
        "Trade-offs",
        "When to use",
        "Comparison",
        "How to choose",
        "Per-option caveats",
        "Decision",
        "Consequences",
        "Alternatives considered",
        "Gotchas",
        "When not to use",
    ]

    emitted: set[str] = set()
    for key in preferred:
        if key in sections and is_substantive(sections[key]):
            out.append("")
            out.append(f"## {key}")
            body = sections[key]
            # Drop "Say it in one breath" boilerplate duplicate of blockquote
            cleaned: list[str] = []
            skip_next_blank = False
            for b in body:
                if "**Say it in one breath:**" in b:
                    skip_next_blank = True
                    continue
                if skip_next_blank and not b.strip():
                    skip_next_blank = False
                    continue
                cleaned.append(b)
            out.extend(cleaned)
            emitted.add(key)

    # Any remaining sections not in preferred list
    for key, body in sections.items():
        if key in emitted or key.lower() == "related" or key.lower() == "sources":
            continue
        if is_substantive(body):
            out.append("")
            out.append(f"## {key}")
            out.extend(body)
            emitted.add(key)

    if "Related" in sections and is_substantive(sections["Related"]):
        out.append("")
        out.append("## Related")
        out.extend(sections["Related"])
    elif "Related" in sections:
        rel = "\n".join(sections["Related"]).strip()
        if rel and rel != "…":
            out.append("")
            out.append("## Related")
            out.extend(sections["Related"])

    has_sources = "Sources" in sections and is_substantive(sections["Sources"])
    if has_sources:
        out.append("")
        out.append("## Sources")
        out.extend(sections["Sources"])
    else:
        out.append("")
        out.append("## Sources")
        out.append("")
        out.append(wiki_source(title))

    result = "\n".join(out).strip() + "\n"
    return result


def main() -> None:
    changed = 0
    skipped = 0
    for path in sorted(VAULT.rglob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        if "## Mental model" not in text and "## Index" not in text:
            skipped += 1
            continue
        title = path.stem
        new = transform(text, title)
        if new and new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"transformed={changed} skipped_no_template={skipped}")


if __name__ == "__main__":
    main()
