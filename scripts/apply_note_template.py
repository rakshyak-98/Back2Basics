#!/usr/bin/env python3
"""Apply strategy-aware NOTES_STANDARD templates to vault notes."""

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
        "NOTETAKING_STRATEGIES.md",
        "INDEX.md",
        "README.md",
    }
)

STRATEGY_TAG_RE = re.compile(
    r"^\s*<!--\s*note-strategy:\s*([a-z]+)\s*-->\s*$",
    re.I,
)

VALID_STRATEGIES = frozenset(
    {
        "operational",
        "reference",
        "concept",
        "comparison",
        "runbook",
        "procedure",
        "hub",
        "decision",
    }
)

# Section order, alias map, and placeholders per strategy.
STRATEGY_CONFIG: dict[str, dict[str, object]] = {
    "operational": {
        "order": [
            "Mental model",
            "Standard config / commands",
            "Triage (when things break)",
            "Gotchas",
            "When NOT to use",
            "Related",
        ],
        "aliases": {
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
        },
        "placeholders": {
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
        },
        "keyword_re": {
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
        },
        "custom_insert_after": "Standard config / commands",
    },
    "reference": {
        "order": [
            "Quick reference",
            "Common commands",
            "Options / flags",
            "Examples",
            "Related",
        ],
        "aliases": {
            "Quick reference": ["quick reference", "cheat sheet", "summary", "overview"],
            "Common commands": [
                "common commands",
                "commands",
                "usage",
                "standard config / commands",
                "standard config",
            ],
            "Options / flags": [
                "options / flags",
                "options",
                "flags",
                "parameters",
                "syntax",
            ],
            "Examples": ["examples", "example", "samples"],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Quick reference": [
                "",
                "| Task | Command |",
                "|------|---------|",
                "| … | `…` |",
            ],
            "Common commands": ["```bash", "# …", "```"],
            "Options / flags": [
                "",
                "| Flag | Effect | When to use |",
                "|------|--------|-------------|",
                "| … | … | … |",
            ],
            "Examples": ["```bash", "# …", "```"],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Common commands": re.compile(r"\b(commands?|usage|cli)\b", re.I),
            "Options / flags": re.compile(r"\b(options?|flags?|parameters?|syntax)\b", re.I),
            "Examples": re.compile(r"\b(examples?|samples?)\b", re.I),
        },
        "custom_insert_after": "Common commands",
    },
    "concept": {
        "order": [
            "Mental model",
            "Core idea",
            "Variations / implementations",
            "Trade-offs",
            "When to use / When NOT",
            "Related",
        ],
        "aliases": {
            "Mental model": ["mental model", "overview", "introduction", "concept"],
            "Core idea": ["core idea", "core concepts", "idea", "mechanism"],
            "Variations / implementations": [
                "variations / implementations",
                "variations",
                "implementations",
                "examples",
            ],
            "Trade-offs": ["trade-offs", "tradeoffs", "pros and cons", "advantages"],
            "When to use / When NOT": [
                "when to use / when not",
                "when to use",
                "when not to use",
                "when not",
            ],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Mental model": ["**Say it in one breath:** …"],
            "Core idea": ["…"],
            "Variations / implementations": ["…"],
            "Trade-offs": ["", "| Gain | Cost |", "|------|------|", "| … | … |"],
            "When to use / When NOT": ["**Use when:** …", "", "**Avoid when:** …"],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Core idea": re.compile(r"\b(core|idea|mechanism)\b", re.I),
            "Variations / implementations": re.compile(
                r"\b(variations?|implementations?|examples?)\b",
                re.I,
            ),
            "Trade-offs": re.compile(r"\b(trade-?offs?|pros?|cons?)\b", re.I),
            "When to use / When NOT": re.compile(r"\b(when\s+(to\s+)?use|when\s+not)\b", re.I),
        },
        "custom_insert_after": "Core idea",
    },
    "comparison": {
        "order": [
            "Decision context",
            "Comparison matrix",
            "Selection guide",
            "Per-option gotchas",
            "Related",
        ],
        "aliases": {
            "Decision context": ["decision context", "context", "background"],
            "Comparison matrix": [
                "comparison matrix",
                "comparison",
                "matrix",
                "versus",
                "vs",
            ],
            "Selection guide": ["selection guide", "when to choose", "recommendation"],
            "Per-option gotchas": [
                "per-option gotchas",
                "gotchas",
                "caveats",
                "warnings",
            ],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Decision context": ["…"],
            "Comparison matrix": [
                "",
                "| Criterion | Option A | Option B |",
                "|-----------|----------|----------|",
                "| … | … | … |",
            ],
            "Selection guide": ["- Choose **A** when …", "- Choose **B** when …"],
            "Per-option gotchas": ["", "> [!WARNING]", "> …"],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Comparison matrix": re.compile(r"\b(comparison|matrix|versus|vs)\b", re.I),
            "Selection guide": re.compile(r"\b(selection|choose|recommend)\b", re.I),
            "Per-option gotchas": re.compile(r"\b(gotchas?|caveats?|warnings?)\b", re.I),
        },
        "custom_insert_after": "Comparison matrix",
    },
    "runbook": {
        "order": [
            "Trigger / symptoms",
            "Preconditions",
            "Steps",
            "Verification",
            "Rollback",
            "Escalation",
            "Related",
        ],
        "aliases": {
            "Trigger / symptoms": [
                "trigger / symptoms",
                "trigger",
                "symptoms",
                "when things break",
                "triage",
            ],
            "Preconditions": ["preconditions", "prerequisites", "before you start"],
            "Steps": ["steps", "procedure", "recovery", "fix"],
            "Verification": ["verification", "validate", "confirm"],
            "Rollback": ["rollback", "undo", "revert"],
            "Escalation": ["escalation", "escalate", "when to escalate"],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Trigger / symptoms": ["…"],
            "Preconditions": ["…"],
            "Steps": ["1. …"],
            "Verification": ["```bash", "# …", "```"],
            "Rollback": ["1. …"],
            "Escalation": ["…"],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Steps": re.compile(r"\b(steps?|procedure|recovery|fix)\b", re.I),
            "Verification": re.compile(r"\b(verif(y|ication)|confirm|validate)\b", re.I),
            "Rollback": re.compile(r"\b(rollback|undo|revert)\b", re.I),
        },
        "custom_insert_after": "Steps",
    },
    "procedure": {
        "order": [
            "Prerequisites",
            "Steps",
            "Verification",
            "Troubleshooting",
            "Related",
        ],
        "aliases": {
            "Prerequisites": ["prerequisites", "preconditions", "requirements", "before you start"],
            "Steps": ["steps", "procedure", "install", "setup", "installation"],
            "Verification": ["verification", "validate", "smoke test", "confirm"],
            "Troubleshooting": [
                "troubleshooting",
                "triage",
                "debug",
                "when things break",
                "common issues",
            ],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Prerequisites": ["…"],
            "Steps": ["1. …"],
            "Verification": ["```bash", "# smoke test", "```"],
            "Troubleshooting": [
                "",
                "| Symptom | Check | Fix |",
                "|---------|-------|-----|",
                "| … | … | … |",
            ],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Steps": re.compile(r"\b(steps?|install(?:ation)?|setup)\b", re.I),
            "Troubleshooting": re.compile(
                r"\b(troubleshoot(?:ing)?|triage|debug(?:ging)?)\b",
                re.I,
            ),
        },
        "custom_insert_after": "Steps",
    },
    "hub": {
        "order": [
            "Purpose",
            "Routing table",
            "Domain links",
            "Related",
        ],
        "aliases": {
            "Purpose": ["purpose", "mental model", "overview", "introduction"],
            "Routing table": [
                "routing table",
                "symptom map",
                "index",
                "on-call / debug first",
            ],
            "Domain links": ["domain links", "subtopics", "links", "children"],
            "Related": ["related", "see also", "references", "quality examples"],
        },
        "placeholders": {
            "Purpose": ["…"],
            "Routing table": [
                "",
                "| Symptom / need | Go to |",
                "|----------------|-------|",
                "| … | [[…]] |",
            ],
            "Domain links": ["- …: [[…]]"],
            "Related": ["[[INDEX]] · [[NOTES_STANDARD]] · [[NOTETAKING_STRATEGIES]]"],
        },
        "keyword_re": {
            "Routing table": re.compile(r"\b(routing|symptom|on-?call|index)\b", re.I),
            "Domain links": re.compile(r"\b(domain|links?|subtopics?|hubs?)\b", re.I),
        },
        "custom_insert_after": "Routing table",
    },
    "decision": {
        "order": [
            "Context",
            "Decision",
            "Consequences",
            "Alternatives considered",
            "Related",
        ],
        "aliases": {
            "Context": ["context", "background", "problem"],
            "Decision": ["decision", "outcome", "resolution"],
            "Consequences": ["consequences", "impact", "trade-offs", "results"],
            "Alternatives considered": [
                "alternatives considered",
                "alternatives",
                "options rejected",
            ],
            "Related": ["related", "see also", "references", "links"],
        },
        "placeholders": {
            "Context": ["…"],
            "Decision": ["We will … because …"],
            "Consequences": ["**Positive:** …", "", "**Negative / trade-offs:** …"],
            "Alternatives considered": [
                "",
                "| Alternative | Why rejected |",
                "|-------------|--------------|",
                "| … | … |",
            ],
            "Related": ["[[…]]"],
        },
        "keyword_re": {
            "Decision": re.compile(r"\b(decision|outcome|resolution)\b", re.I),
            "Alternatives considered": re.compile(r"\b(alternatives?|options?\s+rejected)\b", re.I),
        },
        "custom_insert_after": "Decision",
    },
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


def strategy_config(strategy: str) -> dict[str, object]:
    return STRATEGY_CONFIG[strategy]


def canonical_for_heading(heading: str, aliases: dict[str, list[str]]) -> str | None:
    h = heading.strip().lower()
    for canon, alias_list in aliases.items():
        if h == canon.lower():
            return canon
        if h.startswith(canon.lower()):
            return canon
        for alias in alias_list:
            if h == alias or h.startswith(alias):
                return canon
    return None


def is_placeholder_content(lines: list[str]) -> bool:
    stripped = [ln.strip() for ln in lines if ln.strip()]
    if not stripped:
        return True
    placeholder_markers = {"…", "...", "[[…]]", "[[...]]", "1. …", "1. ..."}
    if all(s in placeholder_markers for s in stripped):
        return True
    if stripped == ["> [!WARNING]", "> …"] or stripped == ["> [!WARNING]", "> ..."]:
        return True
    if stripped[:3] == ["| Symptom | Check | Fix |", "|---------|-------|-----|", "| … | … | … |"]:
        return True
    if stripped[:3] == ["| Task | Command |", "|------|---------|", "| … | `…` |"]:
        return True
    if stripped[:3] == [
        "| Criterion | Option A | Option B |",
        "|-----------|----------|----------|",
        "| … | … | … |",
    ]:
        return True
    if stripped == ["```bash", "# …", "```"] or stripped == ["```bash", "# smoke test", "```"]:
        return True
    if stripped == ["**Say it in one breath:** …"]:
        return True
    if stripped == ["**Use when:** …", "**Avoid when:** …"]:
        return True
    if stripped == ["We will … because …"]:
        return True
    if stripped == ["1. …"]:
        return True
    return False


def split_sections(lines: list[str]) -> tuple[list[str], list[Section]]:
    intro: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    in_fence = False
    aliases: dict[str, list[str]] = STRATEGY_CONFIG["operational"]["aliases"]  # type: ignore[assignment]

    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence

        if H2_RE.match(line):
            if in_fence:
                in_fence = False
            if current is not None:
                sections.append(current)
            heading = H2_RE.match(line).group(1).strip()
            current = Section(
                heading=heading,
                canonical=canonical_for_heading(heading, aliases),
            )
            continue

        if current is None:
            intro.append(line)
        else:
            current.lines.append(line)

    if current is not None:
        sections.append(current)

    return intro, sections


def extract_strategy_tag(lines: list[str]) -> tuple[str | None, list[str]]:
    if not lines:
        return None, lines
    match = STRATEGY_TAG_RE.match(lines[0])
    if match:
        strategy = match.group(1).lower()
        if strategy in VALID_STRATEGIES:
            return strategy, lines[1:]
    return None, lines


def infer_strategy(path: Path, title: str, sections: list[Section]) -> str:
    name = path.name
    stem = path.stem.lower()
    rel_parts = path.relative_to(VAULT_ROOT).parts if path.is_relative_to(VAULT_ROOT) else path.parts

    if name in {"INDEX.md", "README.md"}:
        return "hub"
    if len(rel_parts) > 1 and stem == rel_parts[-2].lower().replace(" ", "-"):
        return "hub"

    if "design pattern" in "/".join(p.lower() for p in rel_parts):
        return "concept"

    if " vs " in title.lower() or " vs " in stem or stem.endswith(" vs"):
        return "comparison"

    if re.search(r"\b(error|troubleshoot)\b", stem, re.I):
        return "runbook"

    if re.search(r"\b(setup|installation|install|starter guide)\b", stem, re.I):
        return "procedure"

    if re.search(r"\b(cli|command|commands|keybindings)\b", stem, re.I):
        return "reference"

    if re.search(r"\b(architecture|decision|adr)\b", stem, re.I):
        return "decision"

    heading_text = " ".join(s.heading for s in sections).lower()
    if "routing table" in heading_text or "symptom / need" in heading_text:
        return "hub"
    if "alternatives considered" in heading_text:
        return "decision"
    if "comparison matrix" in heading_text:
        return "comparison"
    if "trigger / symptoms" in heading_text or "rollback" in heading_text:
        return "runbook"
    if "prerequisites" in heading_text and "troubleshooting" in heading_text:
        return "procedure"
    if "quick reference" in heading_text:
        return "reference"

    return "operational"


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


def merge_sections(
    sections: list[Section],
    aliases: dict[str, list[str]],
) -> tuple[dict[str, Section], list[Section]]:
    canonical: dict[str, Section] = {}
    custom: list[Section] = []

    for sec in sections:
        if sec.heading == "Index":
            continue
        key = sec.canonical or canonical_for_heading(sec.heading, aliases)
        sec.canonical = key
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


def heading_matches_keywords(heading: str, canon: str, keyword_re: dict[str, re.Pattern[str]]) -> bool:
    pattern = keyword_re.get(canon)
    return bool(pattern and pattern.search(heading))


def should_skip_placeholder(
    canon: str,
    custom: list[Section],
    canonical: dict[str, Section],
    keyword_re: dict[str, re.Pattern[str]],
) -> bool:
    if canon in canonical and section_has_content(canonical[canon]):
        return True
    return any(heading_matches_keywords(s.heading, canon, keyword_re) for s in custom)


def first_canonical_slot(order: list[str], insert_after: str) -> int:
    try:
        idx = order.index(insert_after)
        return idx + 1
    except ValueError:
        return len(order) - 1


def rebuild_note(path: Path, lines: list[str]) -> list[str]:
    default_title = path.stem
    strategy_tag, body_lines = extract_strategy_tag(lines)
    intro, sections = split_sections(body_lines)

    # Re-parse sections with inferred strategy aliases when tag was absent.
    wikilinks, intro_body = extract_wikilinks(intro)
    title, oneliner, orphan = extract_title_and_oneliner(intro_body, default_title)
    strategy = strategy_tag or infer_strategy(path, title, sections)
    cfg = strategy_config(strategy)
    order: list[str] = cfg["order"]  # type: ignore[assignment]
    aliases: dict[str, list[str]] = cfg["aliases"]  # type: ignore[assignment]
    placeholders: dict[str, list[str]] = cfg["placeholders"]  # type: ignore[assignment]
    keyword_re: dict[str, re.Pattern[str]] = cfg["keyword_re"]  # type: ignore[assignment]
    custom_insert_after: str = cfg["custom_insert_after"]  # type: ignore[assignment]

    # Re-canonicalize section headings with the chosen strategy.
    for sec in sections:
        sec.canonical = canonical_for_heading(sec.heading, aliases)

    canonical, custom = merge_sections(sections, aliases)

    first_section = order[0] if order else "Mental model"
    if orphan:
        target = canonical.get(first_section)
        orphan_block = orphan + ([""] if orphan else [])
        if target:
            if section_has_content(target):
                target.lines = orphan_block + [""] + target.lines
            else:
                target.lines = orphan_block + target.lines
        else:
            canonical[first_section] = Section(
                heading=first_section,
                lines=orphan_block,
                canonical=first_section,
            )

    for canon in order:
        if canon in canonical:
            if not section_has_content(canonical[canon]):
                canonical[canon].lines = list(placeholders[canon])
            continue
        if should_skip_placeholder(canon, custom, canonical, keyword_re):
            continue
        canonical[canon] = Section(
            heading=canon,
            lines=list(placeholders[canon]),
            canonical=canon,
        )

    if not wikilinks:
        parent = infer_parent_wikilink(path)
        if parent:
            wikilinks = [parent]

    ordered_headings: list[str] = []
    body: list[str] = []

    body.append(f"<!-- note-strategy: {strategy} -->")

    if wikilinks:
        body.extend(wikilinks)
        body.append("")

    body.append(f"# {title}")
    body.append("")
    body.append(f"> {oneliner or default_oneliner(title)}")
    body.append("")
    body.append("---")
    body.append("")

    content_sections: list[Section] = []
    insert_idx = first_canonical_slot(order, custom_insert_after)
    for i, canon in enumerate(order):
        if canon in canonical:
            content_sections.append(canonical[canon])
        if i == insert_idx:
            content_sections.extend(custom)

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
