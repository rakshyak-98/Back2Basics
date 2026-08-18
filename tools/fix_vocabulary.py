#!/usr/bin/env python3
"""Apply vocabulary and typo fixes across vault markdown notes."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Whole-word / phrase replacements (order matters for longer phrases first)
REPLACEMENTS: list[tuple[str, str]] = [
    ("wall defined", "well-defined"),
    ("a minux sign", "a minus sign"),
    ("liberary", "library"),
    ("can by anything", "can be anything"),
    ("physically incapable of use", "cannot use"),
    ("occured", "occurred"),
    ("seperate", "separate"),
    ("definately", "definitely"),
    ("accomodate", "accommodate"),
    ("recieve", "receive"),
    ("wierd", "weird"),
    ("untill", "until"),
    ("over-fiting", "overfitting"),
    ("under perform", "underperform"),
    ("datsets", "datasets"),
    ("ransom_state", "random_state"),
    ("there containing", "their containing"),
    ("act as they were", "behave as if they were"),
    ("make possible usage", "enable use"),
    ("also know as", "also known as"),
    ("allows to ", "allows you to "),
    ("performs tasks", "runs tasks"),
    ("continuous manner", "continuous fashion"),
    ("If you not reusing", "If you are not reusing"),
    ("enables  you", "enables you"),
    ("contianer", "container"),
    ("protacted", "protected"),
    ("InterPlanetry", "InterPlanetary"),
    ("Zookeper", "ZooKeeper"),
    ("haven't been", "has not been"),
    ("visual the system", "visualize the system"),
    ("this provide the", "this provides the"),
    ("fix you need to", "you need to"),
    ("Middle ware", "Middleware"),
    ("mange concurrent", "manage concurrent"),
    ("languages languages", "languages"),
    ("Function programming", "Functional programming"),
    ("pacakges", "packages"),
    ("formating", "formatting"),
    ("managmeen", "management"),
    ("paradigram", "paradigm"),
    ("Programing", "Programming"),
    ("Grammer", "Grammar"),
    ("Editabl", "Editable"),
    ("loggging", "logging"),
    ("pandirve", "pendrive"),
    ("hax dump", "hex dump"),
    ("custome function", "custom function"),
    ("mognodb", "mongodb"),
    ("tranning", "training"),
    ("predicated vs actual", "predicted vs actual"),
    ("connection chrun", "connection churn"),
    ("network chrun", "network churn"),
]

GENERIC_BOILERPLATE = re.compile(
    r"\n---\n\n## Standard config / commands\n\n```bash\n# version \+ config path\n# dry-run when available\n```\n\n---\n\n## Triage \(when things break\)\n\n\| Symptom \| Check \| Fix \|\n\|---------|-------|-----|\n\| Retry storm \| backoff / jitter \| Cap retries; circuit break \|\n\| Config drift \| plan/apply or lockfile \| Single source of truth \|\n\| Poison message \| DLQ \| Quarantine and alert \|\n\n---\n\n## Gotchas\n\n> \[!WARNING\]\n> Make retries safe or you will duplicate side effects\.\n\n---\n\n## When NOT to use\n\n- Avoid the tool if a simpler built-in covers the job\.\n",
    re.MULTILINE,
)

DESIGN_BOILERPLATE = re.compile(
    r"\n---\n\n## Standard config / commands\n\n```bash\n# sketch\n# actors, data stores, failure domains\n```\n\n---\n\n## Triage \(when things break\)\n\n\| Symptom \| Check \| Fix \|\n\|---------|-------|-----|\n\| Hot key / hotspot \| metrics by key \| Shard or cache \|\n\| Cascading failure \| timeouts/bulkheads \| Add limits and backoff \|\n\| Split brain \| fencing / quorum \| Use consensus or single writer \|\n\n---\n\n## Gotchas\n\n> \[!WARNING\]\n> Draw the failure mode before the happy path\.\n\n---\n\n## When NOT to use\n\n- Don.t over-design a CRUD (application|app) into Kafka\+K8s on day one\.\n",
    re.MULTILINE,
)

PLACEHOLDER_BREATH = re.compile(
    r"\*\*Say it in one breath:\*\* [^\n]+ is a design idea — I trade something off and I can name the failure mode\.\n\n\n",
    re.MULTILINE,
)


def fix_file(path: Path, typos_only: bool = False) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            changes.append(f"replaced '{old}'")

    if not typos_only:
        if GENERIC_BOILERPLATE.search(text):
            text = GENERIC_BOILERPLATE.sub("\n", text)
            changes.append("removed generic retry-storm boilerplate")

        if DESIGN_BOILERPLATE.search(text):
            text = DESIGN_BOILERPLATE.sub("\n", text)
            changes.append("removed generic design boilerplate")

        if PLACEHOLDER_BREATH.search(text):
            text = PLACEHOLDER_BREATH.sub("", text)
            changes.append("removed placeholder breath line")

        # Remove lines that contain only a lone pipe (orphans after boilerplate stripping)
        text = re.sub(r"\n\|\n", "\n", text)

    # Collapse triple+ blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    if text != original:
        path.write_text(text, encoding="utf-8")
    return changes


def main() -> None:
    typos_only = "--typos-only" in sys.argv
    md_files = sorted(ROOT.rglob("*.md"))
    touched = 0
    for path in md_files:
        if ".git" in path.parts:
            continue
        changes = fix_file(path, typos_only=typos_only)
        if changes:
            touched += 1
            rel = path.relative_to(ROOT)
            print(f"{rel}: {', '.join(changes)}")
    print(f"\nUpdated {touched} files")

if __name__ == "__main__":
    main()
