#!/usr/bin/env python3
"""Generate Mermaid mindmap diagrams from vault topic structure."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".git", "scripts", "tools", "diagram", "Canvas", ".obsidian"}

SUPER_GROUPS = {
    "OS and Linux": ["Linux", "Operating System"],
    "Networking and DNS": ["Networking", "DNS", "Protocol"],
    "Containers and Orchestration": ["Docker", "Kubernates", "helm"],
    "Cloud and IaC": ["AWS", "Terraform", "Deployment", "Netlify"],
    "Data Stores": ["Database", "MongoDB", "Redis", "Prisma"],
    "Security and Access": ["Security", "ssh", "cookies"],
    "Web Frontend": [
        "React",
        "javascript",
        "css",
        "NextJS",
        "TypeScript",
        "vite",
        "Rendering performance",
    ],
    "Backend Runtimes": [
        "NodeJS",
        "ExpressJS",
        "npm",
        "php",
        "Python",
        "golang",
        "kotlin",
        "dart",
        "flutter",
        "android",
    ],
    "Messaging and Streaming": ["Messaging", "Streaming"],
    "System Design and Architecture": ["System Design", "Architectures", "Design pattern"],
    "DevOps and Delivery": ["DevOps", "GIT", "GitHub", "Nginx", "apache", "pm2"],
    "Data Structures and Algorithms": ["Data structure", "compiler"],
    "Machine Learning and AI": ["ML", "MCP"],
    "Editors and Terminals": ["vim", "nvim", "zed", "tmux"],
    "Reference and Descriptive": ["Descriptive"],
    "Features and Projects": [
        "Feature implementation",
        "LLD",
        "Projects",
        "Payments",
        "Firebase",
    ],
    "Miscellaneous": ["Errors", "Proxy", "RTQ", "Programming paradigram"],
}

META_SKIP = {
    "README",
    "INDEX",
    "NOTES_STANDARD",
    "AGENTS",
    "WORKLOG",
    "TL;DR",
    "Useful prompt for learning with AI chat",
}


def sanitize_node(text: str) -> str:
    """Flatten labels so Mermaid mindmap parsers accept them."""
    text = text.strip()
    text = re.sub(r"\(([^)]*)\)", r" \1", text)
    for char in '/:;#"|[]{}':
        text = text.replace(char, " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or "untitled"


def insert_tree(tree: dict, parts: tuple[str, ...], leaf: str) -> None:
    node = tree
    for part in parts:
        node = node.setdefault(part, {})
    node.setdefault("__leaves__", []).append(leaf)


def tree_to_mindmap_lines(tree: dict, indent: int = 2) -> list[str]:
    lines: list[str] = []
    leaves = tree.pop("__leaves__", [])
    for key in sorted(k for k in tree if k != "__leaves__"):
        lines.append(" " * indent + sanitize_node(key))
        lines.extend(tree_to_mindmap_lines(tree[key], indent + 2))
    for leaf in sorted(leaves):
        lines.append(" " * indent + sanitize_node(leaf))
    return lines


def collect_topics(root: Path) -> tuple[dict[str, list[Path]], list[str]]:
    by_folder: dict[str, list[Path]] = defaultdict(list)
    root_topics: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS or part.startswith(".") for part in path.parts):
            continue
        if path.stem in META_SKIP:
            continue
        if len(path.parts) == 1:
            root_topics.append(path.stem)
        else:
            by_folder[path.parts[0]].append(path)
    return by_folder, root_topics


def build_folder_tree(files: list[Path]) -> dict:
    tree: dict = {}
    for path in files:
        rel_parts = path.parts[1:]
        stem = path.stem
        if len(rel_parts) == 1:
            insert_tree(tree, (), stem)
        else:
            insert_tree(tree, rel_parts[:-1], stem)
    return tree


def write_diagram(path: Path, title: str, subtitle: str, root: str, tree: dict) -> None:
    lines = ["mindmap", f"  root(({sanitize_node(root)}))"]
    lines.extend(tree_to_mindmap_lines(tree, indent=4))
    content = f"""# {title} — Topic Mind Map

> {subtitle}

```mermaid
{chr(10).join(lines)}
```
"""
    path.write_text(content, encoding="utf-8")


def write_readme(out: Path) -> None:
    rows = []
    for group, folders in SUPER_GROUPS.items():
        fname = group.replace(" ", "-").replace("/", "-") + ".md"
        rows.append(f"| [[{fname.replace('.md', '')}]] | {', '.join(folders)} |")
    rows.append("| [[Vault-Root]] | Root-level standalone notes |")
    rows.append("| [[Vault-Overview]] | All groups at a glance |")

    readme = """# Diagrams — Topic Mind Maps

Mermaid `mindmap` diagrams for memorizing vault topics. Each file groups **related topics**; nodes are **topic names only** (no descriptions).

## Files

| Mind map | Vault folders |
|----------|---------------|
"""
    readme += "\n".join(rows)
    readme += """

## How to use

1. Open a group mind map in Obsidian (enable **Mermaid**).
2. Read outward from the center — root → folder → subfolder → topic.
3. Jump to the note via `[[wikilink]]` from folder hubs or search.

Regenerate: run `python3 scripts/generate_mindmaps.py` after adding notes.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    root = Path(".")
    by_folder, root_topics = collect_topics(root)
    out = root / "diagram"
    out.mkdir(exist_ok=True)

    for group, folders in SUPER_GROUPS.items():
        group_tree: dict = {}
        present = [folder for folder in folders if folder in by_folder]
        for folder in present:
            group_tree[folder] = build_folder_tree(by_folder[folder])
        subtitle = (
            f"Minimal topic names for memorization. Vault folders: {', '.join(present)}."
        )
        fname = group.replace(" ", "-").replace("/", "-") + ".md"
        write_diagram(out / fname, group, subtitle, group, group_tree)

    root_tree = {"Topics": {"__leaves__": root_topics}}
    write_diagram(
        out / "Vault-Root.md",
        "Vault Root",
        "Standalone notes at vault root (excluding navigation/meta files).",
        "Vault Root",
        root_tree,
    )

    overview: dict = {}
    for group, folders in SUPER_GROUPS.items():
        overview[group] = {"__leaves__": [f for f in folders if f in by_folder]}
    overview["Vault Root"] = {"__leaves__": ["standalone notes"]}
    write_diagram(
        out / "Vault-Overview.md",
        "Vault Overview",
        "Top-level topic groups in this vault — use as the entry mind map.",
        "Back2Basics",
        overview,
    )

    write_readme(out)
    print(f"Wrote {len(list(out.glob('*.md')))} files to {out}/")


if __name__ == "__main__":
    main()
