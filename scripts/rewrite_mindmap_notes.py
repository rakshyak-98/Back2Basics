#!/usr/bin/env python3
"""Rewrite all leaf notes to Mind Map technique (center + 4-7 radiating branches)."""

from __future__ import annotations

import re
import sys
import textwrap
import urllib.parse
from pathlib import Path

# Reuse parsers from apply_note_rules
sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_note_rules import (  # noqa: E402
    SKIP,
    VAULT,
    clean_preamble,
    consolidate_sections,
    dedupe_blockquote_core_definition,
    is_redirect_stub,
    is_substantive,
    parse_sections,
    wiki_source,
)

MAX_BRANCH_CHARS = 78
MAX_CENTER_CHARS = 220

BRANCH_SHORT = {
    "Why It Matters": "Why it matters",
    "Sources": "Sources",
    "Key Concepts": "Concepts",
    "Technical Details": "Mechanism",
    "Real-World Applications": "Use cases",
    "Pros/Cons or Trade-offs": "Trade-offs",
    "Comparison": "Comparison",
    "Mistakes to Avoid": "Pitfalls",
}

MIND_MAP_PRIMARY_ORDER = [
    "Why It Matters",
    "Sources",
    "Key Concepts",
    "Technical Details",
    "Mistakes to Avoid",
    "Pros/Cons or Trade-offs",
    "Comparison",
    "Real-World Applications",
]

FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^#{1,6}\s+")


def extract_wikilinks(preamble: list[str]) -> list[str]:
    for line in preamble:
        if line.strip().startswith("[[") and "]]" in line:
            return [line.strip()]
    return []


def extract_title(preamble: list[str], path: Path) -> str:
    for line in preamble:
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def extract_blockquote(preamble: list[str]) -> str:
    for line in preamble:
        if line.startswith("> "):
            return line[2:].strip()
    return ""


def first_sentence(text: str, max_len: int = MAX_CENTER_CHARS) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= max_len:
        return text
    m = re.search(r"[.!?]\s", text[:max_len])
    if m:
        return text[: m.start() + 1].strip()
    return text[: max_len - 1].rstrip() + "…"


def compress_clause(text: str, max_len: int = MAX_BRANCH_CHARS) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= max_len:
        return text
    for sep in [" — ", " – ", "; ", ". "]:
        if sep in text:
            part = text.split(sep)[0].strip()
            if len(part) >= 12:
                return part if len(part) <= max_len else part[: max_len - 1] + "…"
    return text[: max_len - 1] + "…"


def is_structural_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if FENCE_RE.match(line):
        return True
    if HEADING_RE.match(line):
        return True
    if s.startswith("|"):
        return True
    if s.startswith(">"):
        return True
    return False


def rewrite_why_it_matters(body: list[str]) -> list[str]:
    text = "\n".join(body).strip()
    if not text:
        return body
    if re.search(r"^- \*\*", text, re.M):
        out = []
        for line in body:
            if line.strip().startswith("- "):
                out.append(compress_key_signal_line(line))
            else:
                out.append(line)
        return out
    return [f"- **Key signal:** {compress_clause(text, 120)}"]


def compress_key_signal_line(line: str) -> str:
    m = re.match(r"(- \*\*[^*]+\*\*:?\s*)(.*)", line.strip())
    if m:
        return m.group(1) + compress_clause(m.group(2))
    if line.strip().startswith("- "):
        return "- " + compress_clause(line.strip()[2:])
    return line


def recall_cue_to_concept(line: str) -> str | None:
    line = line.strip()
    m = re.match(r"- What is \*\*([^*]+)\*\*\??", line)
    if m:
        return f"- **{m.group(1).strip()}:** recall hook"
    m = re.match(r"- Why does this matter for (.+)\??", line)
    if m:
        return f"- **Key signal:** {compress_clause(m.group(1))}"
    m = re.match(r"- (.+)\??$", line)
    if m and line.startswith("- "):
        text = compress_clause(m.group(1))
        if text.lower().startswith("what mistake is"):
            return f"- **Recall:** {text}"
        return f"- **Recall:** {text}"
    return None


def rewrite_key_concepts(body: list[str]) -> list[str]:
    out: list[str] = []
    for line in body:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        if is_structural_line(line):
            out.append(line)
            continue
        if stripped.startswith("### "):
            out.append(line)
            continue
        m = re.match(r"- \*\*(.+?)\*\*\s*(.*)", stripped)
        if m:
            term = m.group(1).strip().rstrip(":")
            rest = compress_clause(m.group(2))
            out.append(f"- **{term}:** {rest}")
            continue
        if stripped.startswith("- "):
            text = stripped[2:]
            words = text.split()
            if len(words) >= 2:
                kw = " ".join(words[:2]).rstrip(",:;")
                rest = compress_clause(text)
                out.append(f"- **{kw}:** {rest}")
            else:
                out.append(f"- **Concept:** {compress_clause(text)}")
            continue
        if len(stripped) > 60 and not stripped.startswith("|"):
            out.append(f"- **Note:** {compress_clause(stripped)}")
        else:
            out.append(line)
    return out


def paragraph_to_bullets(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    bullets = []
    for s in sentences:
        s = s.strip()
        if len(s) < 10:
            continue
        bullets.append(f"- {compress_clause(s)}")
    return bullets


def rewrite_technical_details(body: list[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    para_buf: list[str] = []

    def flush_para() -> None:
        nonlocal para_buf
        if not para_buf:
            return
        text = " ".join(para_buf).strip()
        para_buf = []
        if text:
            out.extend(paragraph_to_bullets(text))
            out.append("")

    for line in body:
        if FENCE_RE.match(line):
            flush_para()
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        stripped = line.strip()
        if re.match(r"^\d+\.\s", stripped):
            flush_para()
            out.append(line)
            continue
        if is_structural_line(line) and stripped:
            flush_para()
            out.append(line)
            continue
        if line.strip().startswith("- "):
            flush_para()
            stripped_b = line.strip()
            m = re.match(r"- \*\*(.+?)\*\*\s*(.*)", stripped_b)
            if m:
                term = m.group(1).strip().rstrip(":")
                rest = compress_clause(m.group(2))
                out.append(f"- **{term}:** {rest}")
            else:
                out.append("- " + compress_clause(stripped_b[2:]))
            continue
        if line.strip():
            para_buf.append(line.strip())
        else:
            flush_para()
            if out and out[-1] != "":
                out.append("")

    flush_para()
    # trim trailing blanks
    while out and not out[-1].strip():
        out.pop()
    return out


def rewrite_tradeoffs(body: list[str]) -> list[str]:
    out: list[str] = []
    for line in body:
        if not line.strip():
            out.append(line)
            continue
        if line.strip().startswith(("- **Pro:**", "- **Con:**", "- **Trade-off:**")):
            m = re.match(r"(- \*\*(?:Pro|Con|Trade-off)\*\*:?\s*)(.*)", line.strip())
            if m:
                out.append(m.group(1) + compress_clause(m.group(2)))
            else:
                out.append(line)
        elif line.strip().startswith("- "):
            out.append("- " + compress_clause(line.strip()[2:]))
        else:
            out.append(line)
    return out


def rewrite_mistakes(body: list[str]) -> list[str]:
    out: list[str] = []
    for line in body:
        if line.strip().startswith("- "):
            text = line.strip()[2:].rstrip(".")
            if text.startswith("**Mistake:**"):
                out.append(f"- {compress_clause(text)}")
            elif " → " in text:
                wrong, fix = text.split(" → ", 1)
                wrong = wrong.strip().strip("*").strip()
                out.append(
                    f"- **{compress_clause(wrong, 40)}:** → {compress_clause(fix)}"
                )
            else:
                out.append(f"- **Mistake:** {compress_clause(text)}")
        else:
            out.append(line)
    return out


def rewrite_comparison(body: list[str]) -> list[str]:
    out: list[str] = []
    for line in body:
        stripped = line.strip()
        if stripped.startswith("### "):
            out.append(line)
            continue
        if stripped.startswith("- vs "):
            out.append(compress_clause(stripped, 100))
        elif stripped.startswith("- "):
            out.append(compress_clause(stripped, 100))
        elif stripped and not stripped.startswith("|"):
            out.append(f"- {compress_clause(stripped)}")
        else:
            out.append(line)
    return out


def rewrite_applications(body: list[str]) -> list[str]:
    text = "\n".join(body).strip()
    if not text:
        return body
    if text.count("\n") == 0 and not text.startswith("-"):
        return [f"- **Scenario:** {compress_clause(text)}"]
    return rewrite_key_concepts(body)


def merge_into_key_concepts(sections: dict[str, list[str]]) -> list[str]:
    kc: list[str] = []
    if "Key Concepts" in sections:
        kc.extend(sections["Key Concepts"])
    if "Core Definition" in sections:
        cd = "\n".join(sections["Core Definition"]).strip()
        if cd:
            kc.append("")
            kc.append(f"- **Core:** {compress_clause(cd)}")
    # Mind Map shape: Recall Cues (Cornell) are not a primary branch — drop them.
    return kc


def merge_comparison_and_apps(sections: dict[str, list[str]]) -> list[str]:
    out: list[str] = []
    if "Comparison" in sections:
        out.extend(sections["Comparison"])
    if "Real-World Applications" in sections:
        if out:
            out.append("")
        out.append("### Use cases")
        out.extend(sections["Real-World Applications"])
    return out


def build_primary_sections(
    sections: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Consolidate to Mind Map primary branches (max 7)."""
    merged_kc = merge_into_key_concepts(sections)
    if merged_kc:
        sections["Key Concepts"] = rewrite_key_concepts(merged_kc)
    sections.pop("Core Definition", None)
    sections.pop("Recall Cues", None)

    if "Technical Details" in sections:
        sections["Technical Details"] = rewrite_technical_details(
            sections["Technical Details"]
        )

    if "Why It Matters" in sections:
        sections["Why It Matters"] = rewrite_why_it_matters(
            sections["Why It Matters"]
        )

    if "Pros/Cons or Trade-offs" in sections:
        sections["Pros/Cons or Trade-offs"] = rewrite_tradeoffs(
            sections["Pros/Cons or Trade-offs"]
        )

    if "Mistakes to Avoid" in sections:
        sections["Mistakes to Avoid"] = rewrite_mistakes(
            sections["Mistakes to Avoid"]
        )

    has_comp = "Comparison" in sections and is_substantive(sections["Comparison"])
    has_apps = (
        "Real-World Applications" in sections
        and is_substantive(sections["Real-World Applications"])
    )

    if has_comp and has_apps:
        combined = merge_comparison_and_apps(sections)
        sections["Comparison"] = rewrite_comparison(combined)
        sections.pop("Real-World Applications", None)
    elif has_apps:
        sections["Real-World Applications"] = rewrite_applications(
            sections["Real-World Applications"]
        )
    elif has_comp:
        sections["Comparison"] = rewrite_comparison(sections["Comparison"])

    sections.pop("Summary", None)
    sections.pop("Related", None)

    # Collect primaries in order, cap at 7
    primaries: dict[str, list[str]] = {}
    overflow: list[str] = []

    for key in MIND_MAP_PRIMARY_ORDER:
        if key not in sections or not is_substantive(sections[key]):
            continue
        if len(primaries) < 7:
            primaries[key] = sections[key]
        else:
            overflow.extend([f"### {key}", *sections[key], ""])

    if overflow and "Technical Details" in primaries:
        primaries["Technical Details"].extend(["", *overflow])
    elif overflow:
        primaries["Technical Details"] = overflow

    return primaries


def ascii_mind_map(title: str, branch_keys: list[str]) -> str:
    labels = [BRANCH_SHORT.get(k, k[:12]) for k in branch_keys]
    if not labels:
        return ""
    center = title[:18]
    if len(labels) == 1:
        return f"```txt\n{center} ── {labels[0]}\n```"
    lines = ["```txt"]
    lines.append(f"        {center} ──┬── {labels[0]}")
    for lbl in labels[1:-1]:
        lines.append(f"               ├── {lbl}")
    lines.append(f"               └── {labels[-1]}")
    lines.append("```")
    return "\n".join(lines)


def rebuild_preamble(
    wikilinks: list[str],
    title: str,
    blockquote: str,
    branch_keys: list[str],
) -> list[str]:
    out: list[str] = []
    if wikilinks:
        out.extend(wikilinks)
        out.append("")
    out.append(f"# {title}")
    out.append("")
    center = first_sentence(blockquote) if blockquote else f"{title} — central topic."
    out.append(f"> {center}")
    out.append("")
    diagram = ascii_mind_map(title, branch_keys)
    if diagram:
        out.append(diagram)
    return out


def already_mindmap_shaped(content: str) -> bool:
    return (
        "┬──" in content
        and "## Why It Matters" in content
        and "## Recall Cues" not in content
    )


def transform_mindmap(content: str, path: Path) -> str | None:
    if is_redirect_stub(content):
        return None
    if already_mindmap_shaped(content):
        return None

    lines = content.splitlines()
    preamble, sections = parse_sections(lines)

    if not sections and len(content.strip()) < 120:
        return None

    sections = consolidate_sections(sections)
    dedupe_blockquote_core_definition(preamble, sections)

    wikilinks = extract_wikilinks(preamble)
    title = extract_title(preamble, path)
    blockquote = extract_blockquote(preamble)

    if "Sources" not in sections or not is_substantive(sections.get("Sources", [])):
        sections["Sources"] = ["", wiki_source(title)]

    primaries = build_primary_sections(sections)

    if not primaries:
        return None

    branch_keys = list(primaries.keys())

    out: list[str] = []
    out.extend(rebuild_preamble(wikilinks, title, blockquote, branch_keys))
    for key in MIND_MAP_PRIMARY_ORDER:
        if key not in primaries:
            continue
        out.append("")
        out.append(f"## {key}")
        body = primaries[key]
        while body and not body[0].strip():
            body = body[1:]
        while body and not body[-1].strip():
            body = body[:-1]
        out.extend(body)

    result = "\n".join(out).strip() + "\n"
    old = content.strip() + "\n"
    if result == old:
        return None
    # Skip if only whitespace differs
    if re.sub(r"\s+", " ", result) == re.sub(r"\s+", " ", old):
        return None
    return result


def main() -> None:
    changed = 0
    skipped_redirect = 0
    skipped_stub = 0
    unchanged = 0

    for path in sorted(VAULT.rglob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        if is_redirect_stub(text):
            skipped_redirect += 1
            continue
        new = transform_mindmap(text, path)
        if new is None:
            if len(text.strip()) < 120:
                skipped_stub += 1
            else:
                unchanged += 1
            continue
        path.write_text(new, encoding="utf-8")
        changed += 1

    print(
        f"changed={changed} unchanged={unchanged} "
        f"skipped_redirect={skipped_redirect} skipped_stub={skipped_stub}"
    )


if __name__ == "__main__":
    main()
