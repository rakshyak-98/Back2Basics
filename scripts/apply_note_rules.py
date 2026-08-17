#!/usr/bin/env python3
"""Apply Mind Map / Cornell shapes from AGENT_NOTE_RULES to vault notes."""

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
    "WORKLOG.md",
}

STANDARD_SECTIONS = {
    "Why It Matters",
    "Sources",
    "Core Definition",
    "Key Concepts",
    "Recall Cues",
    "Technical Details",
    "Real-World Applications",
    "Pros/Cons or Trade-offs",
    "Comparison",
    "Mistakes to Avoid",
    "Summary",
    "Related",
}

MIND_MAP_ORDER = [
    "Why It Matters",
    "Sources",
    "Core Definition",
    "Key Concepts",
    "Technical Details",
    "Real-World Applications",
    "Pros/Cons or Trade-offs",
    "Comparison",
    "Mistakes to Avoid",
    "Summary",
]

CORNELL_ORDER = [
    "Why It Matters",
    "Sources",
    "Core Definition",
    "Recall Cues",
    "Technical Details",
    "Mistakes to Avoid",
    "Comparison",
    "Real-World Applications",
    "Pros/Cons or Trade-offs",
    "Summary",
]

# Non-standard headings → merge target (section name)
MERGE_TO_KEY_CONCEPTS = {
    "how it works",
    "core idea",
    "mental model",
    "purpose",
    "firmware setup concepts",
    "design pass (lightweight)",
    "smells",
    "questions before adding a part",
    "dependency inversion in practice",
    "smells and which principle speaks to them",
    "schema evolution rules",
    "abstraction versus implementation",
    "common failure patterns in design reviews",
    "related design principles in this vault",
}

MERGE_TO_TECHNICAL = {
    "configuration and commands",
    "common commands",
    "options and flags",
    "examples",
    "quick reference",
    "steps",
    "before you start",
    "verification",
    "rollback",
    "escalation",
    "when to use this runbook",
    "preconditions",
    "prerequisites",
    "reference flow",
    "kubernetes edge topology (example)",
    "ingest contract",
    "edge proxy and health",
    "metadata model (broadcast)",
    "typical workflow",
    "operational failures",
    "login flow (local credentials)",
    "common patterns",
    "json web token cautions",
    "threat model highlights",
    "application programming interface sketch",
    "balance calculation",
    "debt simplification",
    "a practical design loop",
    "scaling path (typical order)",
    "measurement",
    "knobs that move throughput",
    "asynchronous job pattern",
    "connection and protocol tuning",
    "practical pitfalls",
    "client patterns",
    "scaling fan-out",
    "kiss at boundaries",
    "when simplicity becomes negligence",
    "recovery checklist",
    "post order",
}

MERGE_TO_MISTAKES = {
    "when things break",
    "triage",
    "troubleshooting",
    "gotchas",
    "symptom → direction",
    "operational failures",
}

MERGE_TO_TRADE_OFFS = {
    "when not to use",
    "when not to over-optimize",
    "when csm still matters",
    "tension with [[dry]] and [[solid]]",
}

MERGE_TO_COMPARISON = {
    "relationship to [[solid]]",
    "relationship to [[grasp]] and [[system design]]",
    "relationship to [[solid]]",
    "comparison matrix",
    "how to choose",
    "selection guide",
}

MERGE_TO_APPLICATIONS = {
    "where to go next",
    "related topics in this domain",
    "variations / implementations",
}

DROP_SECTIONS = {"related", "index"}

CORNELL_SECTION_NAMES = {
    "steps",
    "before you start",
    "verification",
    "rollback",
    "escalation",
    "when to use this runbook",
    "preconditions",
    "prerequisites",
}

CORNELL_PATH_RE = re.compile(
    r"workflow|runbook|setup|install|deploy|procedure|checklist|traversal",
    re.I,
)

CORNELL_PATH_EXCLUDE = {
    "system design",
    "system design fundemental",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FENCE_RE = re.compile(r"^\s*```")
PLACEHOLDER_ONLY = re.compile(r"^[\s…\.]*$|^One-line:.*source TBD")
REDIRECT_RE = re.compile(r"^→\s*\[\[")
WIKILINK_TOP_RE = re.compile(r"^\[\[.+?\]\]")

CORNELL_FLOW_SECTIONS = {
    "reference flow",
    "typical workflow",
    "login flow (local credentials)",
    "a practical design loop",
    "scaling path (typical order)",
}


def merge_target(heading: str) -> str | None:
    """Return standard section name to merge into, or None to drop."""
    key = heading.strip().lower()
    if key in DROP_SECTIONS:
        return None
    if key in MERGE_TO_KEY_CONCEPTS:
        return "Key Concepts"
    if key in MERGE_TO_TECHNICAL:
        return "Technical Details"
    if key in MERGE_TO_MISTAKES:
        return "Mistakes to Avoid"
    if key in MERGE_TO_TRADE_OFFS:
        return "Pros/Cons or Trade-offs"
    if key in MERGE_TO_COMPARISON:
        return "Comparison"
    if key in MERGE_TO_APPLICATIONS:
        return "Real-World Applications"
    # relationship to * patterns
    if key.startswith("relationship to"):
        return "Comparison"
    if "flow" in key or "workflow" in key or "checklist" in key:
        return "Technical Details"
    if "pattern" in key or "measurement" in key or "topology" in key:
        return "Technical Details"
    return "Technical Details"


def parse_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    preamble: list[str] = []
    sections: dict[str, list[str]] = {}
    current_key: str | None = None
    in_fence = False

    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            target = preamble if current_key is None else sections[current_key]
            target.append(line)
            continue

        if not in_fence:
            m = HEADING_RE.match(line)
            if m and m.group(1) == "##":
                raw = m.group(2).strip()
                if raw.lower() == "index":
                    current_key = None
                    continue
                current_key = raw
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
    if text.startswith("→ See") or "canonical note" in text.lower():
        return False
    return True


def is_redirect_stub(text: str) -> bool:
    stripped = text.strip()
    if REDIRECT_RE.match(stripped):
        return True
    if "→ See **[[" in text or "redirect alias" in text.lower():
        return True
    if re.search(r"^>\s+.*→\s*See\s+\[\[", text, re.M):
        return True
    return False


def numbered_spine_count(td_body: list[str]) -> int:
    """Count top-level numbered steps in Technical Details (before first ###)."""
    count = 0
    for line in td_body:
        if line.startswith("###"):
            break
        if re.match(r"^\d+\.\s", line):
            count += 1
    return count


def is_cornell(path: Path, sections: dict[str, list[str]]) -> bool:
    stem_lower = path.stem.lower()
    if stem_lower in CORNELL_PATH_EXCLUDE:
        return False
    names = {k.lower() for k in sections}
    if names & CORNELL_SECTION_NAMES:
        return True
    if CORNELL_PATH_RE.search(path.stem):
        return True
    if names & CORNELL_FLOW_SECTIONS:
        return True
    td = sections.get("Technical Details", [])
    if numbered_spine_count(td) >= 3:
        return True
    for key in sections:
        kl = key.lower()
        if kl in CORNELL_FLOW_SECTIONS:
            return True
        if kl.endswith(" workflow") or kl.startswith("login flow"):
            return True
    return False


def wiki_source(title: str) -> str:
    q = title.split("#")[-1].strip()
    q = re.sub(r"\s*\([^)]*\)\s*", " ", q).strip()
    url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(q.replace(" ", "_"))
    return f"- [Wikipedia — {q}]({url}) — overview"


def merge_body_into(
    target_body: list[str],
    source_heading: str,
    source_body: list[str],
    as_subsection: bool,
) -> list[str]:
    if not is_substantive(source_body):
        return target_body
    out = list(target_body)
    if as_subsection:
        if out and out[-1].strip():
            out.append("")
        out.append(f"### {source_heading}")
    out.extend(source_body)
    return out


def consolidate_sections(sections: dict[str, list[str]]) -> dict[str, list[str]]:
    """Merge non-standard ## sections into standard Mind Map / Cornell branches."""
    consolidated: dict[str, list[str]] = {}
    for key, body in sections.items():
        if key in STANDARD_SECTIONS:
            if key in consolidated:
                consolidated[key] = merge_body_into(
                    consolidated[key], key, body, as_subsection=False
                )
            else:
                consolidated[key] = list(body)
        else:
            target = merge_target(key)
            if target is None:
                continue
            as_sub = target in ("Technical Details", "Key Concepts", "Mistakes to Avoid")
            if target not in consolidated:
                consolidated[target] = []
            consolidated[target] = merge_body_into(
                consolidated[target], key, body, as_subsection=as_sub
            )
    return consolidated


def generate_recall_cues(sections: dict[str, list[str]]) -> list[str]:
    cues: list[str] = []
    seen: set[str] = set()

    ir_text = "\n".join(sections.get("Why It Matters", [])).strip()
    if ir_text and not ir_text.startswith("What reviewers probe about"):
        if re.match(r"^(Pick|Name|Defend|Walk|Clarify|Explain|Describe|Compare)", ir_text):
            cue = f"- {ir_text.rstrip('.')}?"
            if cue not in seen:
                cues.append(cue)
                seen.add(cue)
        else:
            cleaned = re.sub(
                r"^Reviewers?\s+(probe|ask|want|expect|test)\s+",
                "",
                ir_text,
                flags=re.I,
            )
            parts = re.split(r"[;](?=\s+[A-Z])|\.\s+(?=[A-Z])", cleaned)
            for part in parts:
                part = part.strip().rstrip(".")
                if len(part) < 12:
                    continue
                cue = f"- Why does this matter for {part}?"
                if cue not in seen:
                    cues.append(cue)
                    seen.add(cue)

    kc = sections.get("Key Concepts", [])
    for line in kc:
        m = re.match(r"- \*\*([^*:]+)\*\*", line.strip())
        if m:
            term = m.group(1).strip()
            cue = f"- What is **{term}**?"
            if cue not in seen:
                cues.append(cue)
                seen.add(cue)

    td = sections.get("Technical Details", [])
    for line in td:
        m = re.match(r"^\d+\.\s+\*\*([^*]+)\*\*", line.strip())
        if m:
            step = m.group(1).strip()
            cue = f"- What happens in the **{step}** step?"
            if cue not in seen:
                cues.append(cue)
                seen.add(cue)
        m2 = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if m2 and not m:
            step = m2.group(1).strip()
            if len(step) < 60:
                cue = f"- What is step {line.strip().split('.')[0]}: {step.rstrip('.')}?"
                if cue not in seen:
                    cues.append(cue)
                    seen.add(cue)

    mistakes = sections.get("Mistakes to Avoid", [])
    for line in mistakes:
        line = line.strip()
        if line.startswith("- ") and len(line) > 4:
            mistake = line[2:].strip().rstrip(".")
            cue = f"- What mistake is **{mistake}**?"
            if cue not in seen and len(cues) < 8:
                cues.append(cue)
                seen.add(cue)

    return cues[:8]


def ensure_title_blockquote(preamble: list[str], path: Path) -> list[str]:
    has_h1 = any(line.startswith("# ") for line in preamble)
    has_bq = any(line.startswith("> ") for line in preamble)
    out = list(preamble)
    if not has_h1:
        out.insert(0, f"# {path.stem}")
        out.insert(1, "")
    if not has_bq:
        idx = 1
        while idx < len(out) and not out[idx].startswith("# "):
            idx += 1
        if idx < len(out):
            out.insert(idx + 1, "")
            out.insert(idx + 2, f"> {path.stem} — see Technical Details below.")
    return out


def ensure_why_it_matters(title: str, sections: dict[str, list[str]]) -> None:
    if "Why It Matters" in sections and is_substantive(sections["Why It Matters"]):
        ir_text = "\n".join(sections["Why It Matters"]).strip()
        if not ir_text.startswith("What reviewers probe about"):
            return
    sections["Why It Matters"] = [
        f"Definitions, trade-offs, and failure modes for {title}.",
    ]


def ensure_sources(title: str, sections: dict[str, list[str]]) -> None:
    if "Sources" in sections and is_substantive(sections["Sources"]):
        return
    sections["Sources"] = ["", wiki_source(title)]


def dedupe_blockquote_core_definition(preamble: list[str], sections: dict[str, list[str]]) -> None:
    """Remove Core Definition that duplicates the blockquote anchor."""
    bq = ""
    for line in preamble:
        if line.startswith("> "):
            bq = line[2:].strip()
            break
    if not bq or "Core Definition" not in sections:
        return
    cd = "\n".join(sections["Core Definition"]).strip()
    if cd == bq or cd.replace("**", "") == bq.replace("**", ""):
        del sections["Core Definition"]


def clean_preamble(preamble: list[str]) -> list[str]:
    out: list[str] = []
    for line in preamble:
        if line.strip() == "---" and out and out[-1].strip() == "---":
            continue
        out.append(line)
    # trim trailing --- before sections
    while out and out[-1].strip() == "---":
        out.pop()
    return out


def emit_sections(order: list[str], sections: dict[str, list[str]]) -> list[str]:
    out: list[str] = []
    emitted: set[str] = set()
    for key in order:
        if key in sections and is_substantive(sections[key]):
            out.append("")
            out.append(f"## {key}")
            body = sections[key]
            # trim leading/trailing blank lines in body
            while body and not body[0].strip():
                body = body[1:]
            while body and not body[-1].strip():
                body = body[:-1]
            out.extend(body)
            emitted.add(key)
    return out


def transform(content: str, path: Path) -> str | None:
    if is_redirect_stub(content):
        return None

    lines = content.splitlines()
    preamble, sections = parse_sections(lines)

    if not sections and len(content.strip()) < 200:
        return None  # stub — handle manually

    consolidated = consolidate_sections(sections)
    ensure_why_it_matters(path.stem, consolidated)
    ensure_sources(path.stem, consolidated)
    dedupe_blockquote_core_definition(preamble, consolidated)

    cornell = is_cornell(path, consolidated)
    order = CORNELL_ORDER if cornell else MIND_MAP_ORDER

    if cornell:
        cues = generate_recall_cues(consolidated)
        if cues:
            consolidated["Recall Cues"] = cues
    else:
        consolidated.pop("Recall Cues", None)

    preamble = ensure_title_blockquote(preamble, path)

    out: list[str] = []
    out.extend(clean_preamble(preamble))
    out.extend(emit_sections(order, consolidated))

    result = "\n".join(out).strip() + "\n"
    if result == content.strip() + "\n":
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
        new = transform(text, path)
        if new is None:
            if len(text.strip()) < 200 and "## Why It Matters" not in text:
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
