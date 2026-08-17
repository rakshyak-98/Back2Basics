#!/usr/bin/env python3
"""Find clusters of similar and related notes in the vault."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP = {"AGENTS.md", "README.md", "INDEX.md", "WORKLOG.md"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REDIRECT_RE = re.compile(r"^\s*→\s*\[\[([^\]|]+)")

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "with", "vs",
    "using", "use", "how", "what", "when", "why", "from", "by", "at", "is", "are",
}

# Generic tokens that should not drive similarity clustering on their own.
GENERIC_TOKENS = STOPWORDS | {
    "command", "commands", "error", "errors", "config", "configuration",
    "configurations", "management", "server", "servers", "cli", "setup",
    "install", "installation", "guide", "overview", "basics", "essential",
    "essentials", "notes", "note", "concepts", "concept", "workflow",
    "deployment", "build", "module", "modules", "pattern", "patterns",
    "authentication", "auth", "security", "network", "networking", "linux",
    "node", "react", "mysql", "postgres", "mongodb", "docker", "kubernetes",
    "aws", "git", "npm", "php", "python", "golang", "go", "express", "nextjs",
    "vite", "vim", "nvim", "zed", "apache", "nginx", "redis", "terraform",
    "kafka", "streaming", "database", "data", "api", "service", "services",
    "application", "app", "system", "type", "types", "based", "time",
    "file", "files", "key", "keys", "user", "users", "state", "layer",
}


def normalize_title(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def title_tokens(name: str, *, include_generic: bool = False) -> set[str]:
    tokens = {t for t in normalize_title(name).split() if len(t) > 1}
    if include_generic:
        return tokens - STOPWORDS
    return {t for t in tokens if t not in GENERIC_TOKENS}


def similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    ratio = SequenceMatcher(None, na, nb).ratio()
    ta, tb = title_tokens(a), title_tokens(b)
    if not ta or not tb:
        return ratio if ratio >= 0.9 else 0.0
    shared = ta & tb
    jaccard = len(shared) / len(ta | tb)
    # Require at least one meaningful shared token for jaccard to count.
    if not shared:
        return ratio if ratio >= 0.92 else 0.0
    return max(ratio, jaccard)


def pair_similarity(a: str, b: str) -> tuple[float, str]:
    """Return score and reason for a candidate duplicate pair."""
    na, nb = normalize_title(a), normalize_title(b)
    if na == nb:
        return 1.0, "exact"
    ratio = SequenceMatcher(None, na, nb).ratio()
    ta, tb = title_tokens(a), title_tokens(b)
    shared = ta & tb
    if ratio >= 0.88:
        return ratio, "string"
    if shared and len(shared) >= 2:
        score = len(shared) / max(len(ta), len(tb))
        if score >= 0.5:
            return score, "tokens"
    if shared and len(shared) == 1 and ratio >= 0.75:
        return ratio, "token+string"
    return 0.0, ""


@dataclass
class Note:
    path: Path
    title: str
    folder: str
    links_out: set[str] = field(default_factory=set)
    is_redirect: bool = False
    redirect_to: str | None = None
    word_count: int = 0


def basename_index(paths: list[Path]) -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = defaultdict(list)
    for p in paths:
        idx[p.stem.lower()].append(p)
    return idx


def parse_note(path: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem
    folder = str(path.parent.relative_to(VAULT)) if path.parent != VAULT else "(root)"
    links = {m.group(1).strip() for m in WIKILINK_RE.finditer(text)}
    redirect = None
    is_redirect = False
    for line in text.splitlines()[:20]:
        m = REDIRECT_RE.match(line)
        if m:
            redirect = m.group(1).strip()
            is_redirect = True
            break
    words = len(re.findall(r"\w+", text))
    return Note(path, title, folder, links, is_redirect, redirect, words)


def build_notes() -> tuple[list[Note], dict[str, list[Path]]]:
    paths = sorted(
        p for p in VAULT.rglob("*.md")
        if p.name not in SKIP and ".git" not in p.parts
    )
    notes = [parse_note(p) for p in paths]
    return notes, basename_index(paths)


def folder_clusters(notes: list[Note]) -> dict[str, list[str]]:
    clusters: dict[str, list[str]] = defaultdict(list)
    for n in notes:
        clusters[n.folder].append(n.title)
    return dict(sorted(clusters.items(), key=lambda kv: (-len(kv[1]), kv[0])))


def title_similarity_clusters(notes: list[Note], threshold: float = 0.85) -> list[list[str]]:
    titles = [n.title for n in notes if not n.is_redirect]
    parent: dict[str, str] = {t: t for t in titles}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, a in enumerate(titles):
        for b in titles[i + 1 :]:
            score, _ = pair_similarity(a, b)
            if score >= threshold:
                union(a, b)

    groups: dict[str, list[str]] = defaultdict(list)
    for t in titles:
        groups[find(t)].append(t)
    return sorted([sorted(g) for g in groups.values() if len(g) > 1], key=len, reverse=True)


def likely_duplicate_pairs(notes: list[Note], min_score: float = 0.72) -> list[dict]:
    titles = [n.title for n in notes if not n.is_redirect]
    path_by_title = {n.title: str(n.path.relative_to(VAULT)) for n in notes}
    pairs: list[dict] = []
    for i, a in enumerate(titles):
        for b in titles[i + 1 :]:
            score, reason = pair_similarity(a, b)
            if score >= min_score:
                pairs.append({
                    "a": a,
                    "b": b,
                    "score": round(score, 3),
                    "reason": reason,
                    "path_a": path_by_title.get(a, ""),
                    "path_b": path_by_title.get(b, ""),
                })
    return sorted(pairs, key=lambda p: -p["score"])


def shared_prefix_clusters(notes: list[Note], min_size: int = 3) -> list[tuple[str, list[str]]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for n in notes:
        first = normalize_title(n.title).split()[0] if normalize_title(n.title) else ""
        if first and len(first) >= 3:
            buckets[first].append(n.title)
    return sorted(
        [(k, sorted(v)) for k, v in buckets.items() if len(v) >= min_size],
        key=lambda kv: (-len(kv[1]), kv[0]),
    )


def link_neighborhood_clusters(notes: list[Note], min_shared: int = 4) -> list[list[str]]:
    """Cluster notes that share many outbound wikilinks."""
    link_sets = {n.title: n.links_out for n in notes if not n.is_redirect}
    titles = list(link_sets)
    parent = {t: t for t in titles}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, a in enumerate(titles):
        la = link_sets[a]
        if len(la) < 2:
            continue
        for b in titles[i + 1 :]:
            lb = link_sets[b]
            shared = len(la & lb)
            if shared >= min_shared:
                union(a, b)

    groups: dict[str, list[str]] = defaultdict(list)
    for t in titles:
        groups[find(t)].append(t)
    return sorted([sorted(g) for g in groups.values() if len(g) > 2], key=len, reverse=True)


def mutual_link_clusters(notes: list[Note], min_degree: int = 3) -> list[list[str]]:
    """Undirected graph: edge if A links B or B links A."""
    titles = {n.title for n in notes}
    adj: dict[str, set[str]] = defaultdict(set)
    for n in notes:
        for target in n.links_out:
            if target in titles:
                adj[n.title].add(target)
                adj[target].add(n.title)

    visited: set[str] = set()
    clusters: list[list[str]] = []
    for start in sorted(adj, key=lambda t: -len(adj[t])):
        if start in visited:
            continue
        stack = [start]
        comp: list[str] = []
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            comp.append(node)
            for nb in adj[node]:
                if nb not in visited:
                    stack.append(nb)
        if len(comp) >= min_degree:
            clusters.append(sorted(comp, key=lambda t: -len(adj[t])))
    return sorted(clusters, key=len, reverse=True)


def duplicate_basename_clusters(basename_idx: dict[str, list[Path]]) -> list[dict]:
    out = []
    for stem, paths in sorted(basename_idx.items()):
        if len(paths) > 1:
            out.append({
                "basename": stem,
                "paths": [str(p.relative_to(VAULT)) for p in paths],
            })
    return out


def hub_notes(notes: list[Note], top_n: int = 30) -> list[tuple[str, int]]:
    incoming: Counter[str] = Counter()
    titles = {n.title for n in notes}
    for n in notes:
        for target in n.links_out:
            if target in titles:
                incoming[target] += 1
    return incoming.most_common(top_n)


def topic_keyword_clusters(notes: list[Note]) -> dict[str, list[str]]:
    keywords = [
        "docker", "kubernetes", "kubernates", "kubectl", "pod", "ingress", "helm",
        "terraform", "nginx", "redis", "mysql", "postgres", "mongo", "jwt", "tls",
        "ssh", "dns", "tcp", "udp", "grpc", "http", "websocket", "git", "linux",
        "nginx", "react", "nextjs", "node", "express", "vim", "nvim", "aws",
        "security", "auth", "cert", "oauth", "kafka", "rabbit", "mqtt", "pm2",
        "vite", "typescript", "python", "golang", "php", "firebase", "fcm",
        "design pattern", "proxy", "cors", "cilium", "ebpf", "cgroup", "oom",
    ]
    clusters: dict[str, list[str]] = {}
    for kw in keywords:
        matched = sorted(
            n.title for n in notes
            if kw in normalize_title(n.title) or kw in normalize_title(n.folder)
        )
        if len(matched) >= 2:
            clusters[kw] = matched
    return clusters


def render_markdown(
    folder_clusters: dict[str, list[str]],
    title_clusters: list[list[str]],
    duplicate_pairs: list[dict],
    prefix_clusters: list[tuple[str, list[str]]],
    link_clusters: list[list[str]],
    graph_clusters: list[list[str]],
    basename_dups: list[dict],
    hubs: list[tuple[str, int]],
    topic_clusters: dict[str, list[str]],
) -> str:
    major_domains = [
        (folder, titles) for folder, titles in folder_clusters.items()
        if folder != "(root)" and len(titles) >= 10
    ]
    major_domains.sort(key=lambda kv: -len(kv[1]))

    lines = [
        "[[INDEX]] [[general]] [[README]]",
        "",
        "# Similar Notes — Cluster Map",
        "",
        "> Clusters of related notes across the vault — folder groups, naming families, link hubs, and likely duplicates.",
        "",
        "---",
        "",
        "## Executive summary",
        "",
        f"- **{sum(len(t) for f, t in folder_clusters.items() if f != '(root)')}** notes organized into **{len(major_domains)}** major folder domains (10+ notes each).",
        f"- **{len(topic_clusters)}** cross-folder topic keyword families (docker, mysql, react, etc.).",
        f"- **{len(title_clusters)}** high-confidence title-similarity groups and **{len(duplicate_pairs)}** likely duplicate pairs to review.",
        f"- **{len(basename_dups)}** basename collisions across different paths.",
        "",
        "### Major domain clusters",
        "",
        "| Domain folder | Notes | Sample topics |",
        "|---------------|-------|---------------|",
    ]
    for folder, titles in major_domains[:20]:
        sample = ", ".join(f"[[{t}]]" for t in titles[:3])
        lines.append(f"| `{folder}` | {len(titles)} | {sample} |")

    lines += [
        "",
        "---",
        "",
        "## How to read this map",
        "",
        "- **Folder clusters** — notes already co-located by directory.",
        "- **Likely duplicate pairs** — highest-confidence merge candidates.",
        "- **Title similarity groups** — near-duplicate or synonym clusters.",
        "- **Shared-prefix clusters** — naming families (e.g. all `docker …` notes).",
        "- **Topic keyword clusters** — cross-folder notes sharing a domain keyword.",
        "- **Hub notes** — heavily linked notes that anchor a cluster.",
        "",
        "---",
        "",
        "## Hub notes (most inbound links)",
        "",
        "| Note | Inbound links |",
        "|------|---------------|",
    ]
    for title, count in hubs:
        lines.append(f"| [[{title}]] | {count} |")

    lines += ["", "---", "", "## Folder clusters (top-level domains)", ""]
    for folder, titles in folder_clusters.items():
        if folder == "(root)" or len(titles) < 2:
            continue
        lines.append(f"### {folder} ({len(titles)} notes)")
        lines.append("")
        for t in titles[:25]:
            lines.append(f"- [[{t}]]")
        if len(titles) > 25:
            lines.append(f"- … and {len(titles) - 25} more")
        lines.append("")

    lines += ["", "---", "", "## Likely duplicate pairs (review first)", ""]
    if duplicate_pairs:
        lines += ["| Score | Note A | Note B | Reason |", "|-------|--------|--------|--------|"]
        for p in duplicate_pairs[:60]:
            lines.append(
                f"| {p['score']} | [[{p['a']}]] | [[{p['b']}]] | {p['reason']} |"
            )
        lines.append("")

    lines += ["---", "", "## Title similarity groups (possible duplicates)", ""]
    for i, group in enumerate(title_clusters[:40], 1):
        lines.append(f"### Cluster {i} ({len(group)} notes)")
        for t in group:
            lines.append(f"- [[{t}]]")
        lines.append("")

    lines += ["---", "", "## Shared-prefix naming families", ""]
    for prefix, titles in prefix_clusters[:35]:
        lines.append(f"### `{prefix}*` ({len(titles)} notes)")
        for t in titles[:15]:
            lines.append(f"- [[{t}]]")
        if len(titles) > 15:
            lines.append(f"- … and {len(titles) - 15} more")
        lines.append("")

    lines += ["---", "", "## Topic keyword clusters (cross-folder)", ""]
    for kw, titles in sorted(topic_clusters.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"### {kw} ({len(titles)} notes)")
        for t in titles[:20]:
            lines.append(f"- [[{t}]]")
        if len(titles) > 20:
            lines.append(f"- … and {len(titles) - 20} more")
        lines.append("")

    lines += ["---", "", "## Link neighborhood clusters", ""]
    for i, group in enumerate(link_clusters[:25], 1):
        lines.append(f"### Neighborhood {i} ({len(group)} notes)")
        for t in group:
            lines.append(f"- [[{t}]]")
        lines.append("")

    lines += ["---", "", "## Mutual-link graph components", ""]
    for i, group in enumerate(graph_clusters[:20], 1):
        lines.append(f"### Component {i} ({len(group)} notes)")
        for t in group[:20]:
            lines.append(f"- [[{t}]]")
        if len(group) > 20:
            lines.append(f"- … and {len(group) - 20} more")
        lines.append("")

    if basename_dups:
        lines += ["---", "", "## Same basename in different paths", ""]
        for item in basename_dups[:30]:
            lines.append(f"### `{item['basename']}`")
            for p in item["paths"]:
                lines.append(f"- `{p}`")
            lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    notes, basename_idx = build_notes()
    folders = folder_clusters(notes)
    title_clusters = title_similarity_clusters(notes)
    duplicate_pairs = likely_duplicate_pairs(notes)
    prefix_clusters = shared_prefix_clusters(notes)
    link_clusters = link_neighborhood_clusters(notes)
    graph_clusters = mutual_link_clusters(notes)
    basename_dups = duplicate_basename_clusters(basename_idx)
    hubs = hub_notes(notes)
    topic_clusters = topic_keyword_clusters(notes)

    out_md = VAULT / "Similar Notes — Cluster Map.md"
    out_json = VAULT / "scripts" / "cluster_report.json"
    md = render_markdown(
        folders, title_clusters, duplicate_pairs, prefix_clusters, link_clusters,
        graph_clusters, basename_dups, hubs, topic_clusters,
    )
    out_md.write_text(md, encoding="utf-8")

    report = {
        "note_count": len(notes),
        "folder_cluster_count": len([f for f, t in folders.items() if len(t) >= 2 and f != "(root)"]),
        "title_similarity_cluster_count": len(title_clusters),
        "likely_duplicate_pair_count": len(duplicate_pairs),
        "prefix_cluster_count": len(prefix_clusters),
        "topic_cluster_count": len(topic_clusters),
        "basename_duplicate_count": len(basename_dups),
        "hubs": hubs,
        "title_similarity_clusters": title_clusters,
        "likely_duplicate_pairs": duplicate_pairs[:100],
        "topic_clusters": topic_clusters,
    }
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Analyzed {len(notes)} notes")
    print(f"Folder clusters: {report['folder_cluster_count']}")
    print(f"Title similarity clusters: {report['title_similarity_cluster_count']}")
    print(f"Likely duplicate pairs: {report['likely_duplicate_pair_count']}")
    print(f"Topic keyword clusters: {report['topic_cluster_count']}")
    print(f"Same-basename duplicates: {report['basename_duplicate_count']}")
    print(f"Wrote {out_md.relative_to(VAULT)}")
    print(f"Wrote {out_json.relative_to(VAULT)}")


if __name__ == "__main__":
    main()
