#!/usr/bin/env python3
"""Merge duplicate notes and build per-cluster CLI reference files."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?]]")
BASH_BLOCK_RE = re.compile(r"```bash\n(.*?)```", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Merge:
    source: str  # relative path
    target: str  # relative path
    reason: str


# High-confidence merges: source becomes redirect stub → target canonical note.
MERGES: list[Merge] = [
    Merge("Database/mysql/mysql triggers.md", "Database/mysql/MySQL Triggers.md", "case duplicate"),
    Merge("Database/mysql partitioning.md", "Database/mysql/mysql partitioning.md", "path duplicate"),
    Merge("Linux/management/systemctl.md", "Linux/commands/systemctl.md", "path duplicate"),
    Merge("Design pattern/Creation pattern/Abstract Factor.md", "Design pattern/Creation pattern/Abstract Factory.md", "typo stub"),
    Merge("Database/mysql/mysql engine.md", "Database/mysql/MySQL Engines.md", "case duplicate"),
    Merge("NodeJS/event emitter.md", "NodeJS/EventEmitter.md", "case duplicate"),
    Merge("javascript/web worker.md", "javascript/web workers.md", "plural canonical"),
    Merge("React/React Pattern/Compound Components 1.md", "React/React Pattern/Compound Components.md", "numbered duplicate"),
    Merge("Database/mysql/mysql events 1.md", "Database/mysql/MySQL Events.md", "numbered duplicate"),
    Merge("Protocol/E mail server.md", "Protocol/mail server.md", "spacing duplicate"),
    Merge("AWS/EBS (Elastic Block Store).md", "AWS/AWS EBS(Elastic Block Store).md", "title duplicate"),
    Merge("React/Data Fetching HOC component.md", "React/React Pattern/data fetching component.md", "pattern duplicate"),
    Merge("GitHub/Github cli (2).md", "GitHub/Github cli.md", "redirect stub"),
    Merge("Operating System/MBR(Master Boot Record).md", "Operating System/MBR.md", "abbrev vs full"),
    Merge("NodeJS/node command.md", "NodeJS/NodeJS CLI.md", "fold into domain CLI"),
    Merge("NodeJS/npm command.md", "NodeJS/NodeJS CLI.md", "fold into domain CLI"),
    Merge("Security/Asymmetrical Encryption.md", "Security/Encryption.md", "unified crypto reference"),
    Merge("Security/symmetrical encryption.md", "Security/Encryption.md", "unified crypto reference"),
    Merge("React/React data management.md", "React/React State management.md", "unified state architecture"),
    Merge("LLD/Questions/Connection Pool.md", "Database/connection pooling.md", "LLD + ops in one note"),
    Merge("Operating System/non-blocking.md", "Operating System/Blocking Vs Non-Blocking.md", "combined I/O models"),
]

# CLI rename: old path -> new path (title derived from stem)
CLI_RENAMES: dict[str, str] = {
    "Docker/docker cli.md": "Docker/Docker CLI.md",
    "GIT/git command.md": "GIT/Git CLI.md",
    "golang/go cli.md": "golang/Go CLI.md",
    "helm/cli.md": "helm/Helm CLI.md",
    "Database/mysql/cli.md": "Database/mysql/MySQL CLI.md",
    "flutter/flutter cli.md": "flutter/Flutter CLI.md",
    "apache/apache command.md": "apache/Apache CLI.md",
    "GitHub/Github cli.md": "GitHub/GitHub CLI.md",
    "vim/vim commands.md": "vim/Vim CLI.md",
    "nvim/commands.md": "nvim/Neovim CLI.md",
    "NodeJS/CLI.md": "NodeJS/NodeJS CLI.md",
    "Redis/redis-cli.md": "Redis/Redis CLI.md",
    "Deployment/vercel cli.md": "Deployment/Vercel CLI.md",
    "Deployment/render cli.md": "Deployment/Render CLI.md",
    "npm/pnpm cli.md": "npm/pnpm CLI.md",
    "AWS/AWS cli commands.md": "AWS/AWS CLI.md",
    "AWS/AWS cli installation.md": "AWS/AWS CLI installation.md",
}


@dataclass
class CliCluster:
    domain: str
    output: str
    intro: str
    sections: list[tuple[str, list[str]]]  # heading, source note paths


CLI_CLUSTERS: list[CliCluster] = [
    CliCluster(
        domain="Linux",
        output="Linux/Linux CLI.md",
        intro="Consolidated Linux CLI reference — commands grouped by incident job, with deep-dive links to leaf notes.",
        sections=[
            ("Shell & daily ops", ["Linux/commands/common commands.md", "Linux/CLI.md"]),
            ("Process & resources", ["Linux/commands/Linux process commands.md", "Linux/commands/ps.md", "Linux/commands/top.md"]),
            ("Networking", ["Linux/commands/Linux network commands.md", "Linux/commands/ss.md", "Linux/commands/dig.md", "Linux/commands/ip.md"]),
            ("Services & systemd", ["Linux/commands/Services commands.md", "Linux/commands/systemctl.md", "Linux/commands/journalctl.md"]),
            ("Users & authentication", ["Linux/commands/Authentication command.md", "Linux/commands/useradd.md", "Linux/commands/passwd.md"]),
            ("Files & search", ["Linux/commands/Find command.md", "Linux/commands/grep.md", "Linux/commands/rsync.md"]),
            ("Packages (Debian/Ubuntu)", ["Linux/commands/APT policy.md"]),
        ],
    ),
    CliCluster(
        domain="Docker",
        output="Docker/Docker CLI.md",
        intro="Docker Engine CLI — build, run, inspect, network, volumes, and compose.",
        sections=[("Docker CLI", ["Docker/docker cli.md"])],
    ),
    CliCluster(
        domain="GIT",
        output="GIT/Git CLI.md",
        intro="Git CLI — recovery, bisect, merge dry-runs, and everyday workflow commands.",
        sections=[("Git CLI", ["GIT/git command.md"])],
    ),
    CliCluster(
        domain="NodeJS",
        output="NodeJS/NodeJS CLI.md",
        intro="Node.js, npm, and npx CLI — runtime flags, scripts, and debugging.",
        sections=[
            ("Node runtime", ["NodeJS/CLI.md", "NodeJS/node command.md"]),
            ("npm", ["NodeJS/npm command.md", "npm/npm.md"]),
        ],
    ),
    CliCluster(
        domain="Database/mysql",
        output="Database/mysql/MySQL CLI.md",
        intro="mysql client CLI — connect, batch SQL, and interactive meta-commands.",
        sections=[("mysql client", ["Database/mysql/cli.md"])],
    ),
    CliCluster(
        domain="AWS",
        output="AWS/AWS CLI.md",
        intro="AWS CLI v2 — identity, EC2, S3, Lambda, and operational flags.",
        sections=[
            ("Commands", ["AWS/AWS cli commands.md"]),
            ("Installation & configure", ["AWS/AWS cli installation.md"]),
        ],
    ),
    CliCluster(
        domain="Terraform",
        output="Terraform/Terraform CLI.md",
        intro="Terraform CLI workflow — init, plan, apply, state, and logging.",
        sections=[("Terraform CLI", ["Terraform/Terraform CLI.md"])],
    ),
    CliCluster(
        domain="golang",
        output="golang/Go CLI.md",
        intro="Go toolchain CLI — mod, build, test, and vet.",
        sections=[("go CLI", ["golang/go cli.md"])],
    ),
    CliCluster(
        domain="helm",
        output="helm/Helm CLI.md",
        intro="Helm CLI — repos, install, upgrade, rollback.",
        sections=[("Helm CLI", ["helm/cli.md"])],
    ),
    CliCluster(
        domain="Redis",
        output="Redis/Redis CLI.md",
        intro="redis-cli — connect, INFO, memory, slowlog, and keyspace scans.",
        sections=[("redis-cli", ["Redis/redis-cli.md"])],
    ),
    CliCluster(
        domain="flutter",
        output="flutter/Flutter CLI.md",
        intro="Flutter CLI — devices, run, build, and pub.",
        sections=[("Flutter CLI", ["flutter/flutter cli.md"])],
    ),
    CliCluster(
        domain="GitHub",
        output="GitHub/GitHub CLI.md",
        intro="GitHub CLI (gh) — auth, PRs, secrets, and API.",
        sections=[("GitHub CLI", ["GitHub/Github cli.md"])],
    ),
    CliCluster(
        domain="Kubernates",
        output="Kubernates/kubectl CLI.md",
        intro="kubectl — cluster context, workloads, and debugging.",
        sections=[("kubectl", ["Kubernates/kubectl.md"])],
    ),
    CliCluster(
        domain="apache",
        output="apache/Apache CLI.md",
        intro="Apache HTTP Server CLI — modules, sites, and configtest.",
        sections=[("Apache CLI", ["apache/apache command.md"])],
    ),
    CliCluster(
        domain="vim",
        output="vim/Vim CLI.md",
        intro="Vim command-mode reference — buffers, marks, and ex commands.",
        sections=[("Vim", ["vim/vim commands.md"])],
    ),
    CliCluster(
        domain="nvim",
        output="nvim/Neovim CLI.md",
        intro="Neovim command-mode reference.",
        sections=[("Neovim", ["nvim/commands.md"])],
    ),
    CliCluster(
        domain="Deployment",
        output="Deployment/Deployment CLI.md",
        intro="Deployment platform CLIs — Vercel and Render.",
        sections=[
            ("Vercel", ["Deployment/vercel cli.md"]),
            ("Render", ["Deployment/render cli.md"]),
        ],
    ),
    CliCluster(
        domain="npm",
        output="npm/npm CLI.md",
        intro="npm and pnpm CLI — install, scripts, and workspace commands.",
        sections=[("pnpm", ["npm/pnpm cli.md"]), ("npm", ["NodeJS/npm command.md"])],
    ),
]


def title_from_path(path: Path) -> str:
    return path.stem


def read_note(rel: str) -> str:
    return (VAULT / rel).read_text(encoding="utf-8", errors="replace")


def write_note(rel: str, content: str) -> None:
    path = VAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def extract_bash_blocks(text: str) -> list[str]:
    return [m.group(1).strip() for m in BASH_BLOCK_RE.finditer(text) if m.group(1).strip()]


def extract_subsections(text: str) -> list[tuple[str, str]]:
    """Extract ### headings and following bash blocks until next heading."""
    parts: list[tuple[str, str]] = []
    for match in re.finditer(r"^###\s+(.+)$", text, re.MULTILINE):
        heading = match.group(1).strip()
        start = match.end()
        next_h = re.search(r"^#{1,3}\s+", text[start:], re.MULTILINE)
        chunk = text[start : start + next_h.start()] if next_h else text[start:]
        blocks = extract_bash_blocks(chunk)
        if blocks:
            parts.append((heading, "\n\n".join(f"```bash\n{b}\n```" for b in blocks)))
    return parts


def note_exists(rel: str) -> bool:
    return (VAULT / rel).exists()


def apply_merge(merge: Merge) -> bool:
    if merge.source == merge.target:
        return False
    src = VAULT / merge.source
    tgt = VAULT / merge.target
    if not src.exists():
        return False
    if not tgt.exists() and merge.target not in {c.output for c in CLI_CLUSTERS}:
        return False
    target_title = title_from_path(Path(merge.target))
    stub = f"→ [[{target_title}]]\n"
    write_note(merge.source, stub)
    return True


def replace_wikilinks(old_title: str, new_title: str) -> int:
    count = 0
    for path in VAULT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = text

        def repl(m: re.Match[str]) -> str:
            nonlocal count
            target = m.group(1)
            alias = m.group(3)
            anchor = m.group(2) or ""
            if target == old_title:
                count += 1
                if alias:
                    return f"[[{new_title}{anchor}|{alias}]]"
                return f"[[{new_title}{anchor}]]"
            return m.group(0)

        new_text = WIKILINK_RE.sub(repl, new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
    return count


def merge_systemctl_content() -> None:
    """Fold unique commands from management/systemctl into commands/systemctl before stub."""
    src = VAULT / "Linux/management/systemctl.md"
    tgt = VAULT / "Linux/commands/systemctl.md"
    if not src.exists() or not tgt.exists():
        return
    src_text = read_note("Linux/management/systemctl.md")
    extra_cmds = [
        "systemctl reload ssh",
        "systemctl reload-or-restart ssh",
        "systemctl edit ssh",
        "systemctl show ssh -p FragmentPath",
        "systemctl reset-failed",
        "systemctl list-unit-files --type=service",
        "systemctl get-default",
        "systemctl list-dependencies ssh.service",
        "systemd-analyze blame",
        "systemd-analyze critical-chain",
    ]
    tgt_text = read_note("Linux/commands/systemctl.md")
    if "systemd-analyze blame" not in tgt_text:
        insert = "\n".join(extra_cmds)
        tgt_text = tgt_text.replace(
            "journalctl -u nginx -b --no-pager | tail",
            "journalctl -u nginx -b --no-pager | tail\n" + insert,
        )
        write_note("Linux/commands/systemctl.md", tgt_text)


def build_cli_file(cluster: CliCluster) -> str:
    links: list[str] = []
    lines = [
        "[[INDEX]] [[Commands]]" if cluster.domain == "Linux" else f"[[{cluster.domain}]]",
        "",
        f"# {cluster.domain} CLI" if cluster.domain != "Linux" else "# Linux CLI",
        "",
        f"> {cluster.intro}",
        "",
        "---",
        "",
    ]
    for section, sources in cluster.sections:
        lines += [f"## {section}", ""]
        for rel in sources:
            path = VAULT / rel
            if not path.exists():
                # try renamed path
                alt = CLI_RENAMES.get(rel, rel)
                path = VAULT / alt
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            title = title_from_path(path)
            links.append(title)
            subsections = extract_subsections(text)
            if subsections:
                for sub, blocks in subsections:
                    lines += [f"### {sub}", "", f"From [[{title}]].", "", blocks, ""]
            else:
                blocks = extract_bash_blocks(text)
                if blocks:
                    lines += [f"From [[{title}]].", ""]
                    for b in blocks:
                        lines += [f"```bash\n{b}\n```", ""]
                else:
                    lines += [f"- Deep-dive: [[{title}]]", ""]
        lines.append("")
    # dedupe link line
    unique_links = []
    seen = set()
    for l in links:
        if l not in seen:
            seen.add(l)
            unique_links.append(l)
    header_links = " ".join(f"[[{t}]]" for t in unique_links[:12])
    lines[0] = header_links + " [[INDEX]]"
    return "\n".join(lines).rstrip() + "\n"


def apply_cli_renames() -> list[tuple[str, str]]:
    applied = []
    for old, new in CLI_RENAMES.items():
        old_path = VAULT / old
        new_path = VAULT / new
        if old_path.exists() and not new_path.exists():
            old_path.rename(new_path)
            applied.append((old, new))
            old_title = title_from_path(old_path)
            new_title = title_from_path(new_path)
            if old_title != new_title:
                replace_wikilinks(old_title, new_title)
            # Keep redirect stub at old path for Obsidian link resolution.
            stub_title = title_from_path(new_path)
            write_note(old, f"→ [[{stub_title}]]\n")
    return applied


def build_all_cli_files() -> list[str]:
    built = []
    for cluster in CLI_CLUSTERS:
        # resolve sources through renames
        resolved = CliCluster(
            domain=cluster.domain,
            output=cluster.output,
            intro=cluster.intro,
            sections=[
                (h, [CLI_RENAMES.get(s, s) for s in sources])
                for h, sources in cluster.sections
            ],
        )
        content = build_cli_file(resolved)
        write_note(cluster.output, content)
        built.append(cluster.output)
    return built


def title_renames_from_merges() -> list[tuple[str, str]]:
    pairs = []
    for m in MERGES:
        if m.source == m.target:
            continue
        src = Path(m.source)
        tgt = Path(m.target)
        if src.stem != tgt.stem:
            pairs.append((src.stem, tgt.stem))
    return pairs


def main() -> None:
    merge_systemctl_content()
    renames = apply_cli_renames()
    cli_files = build_all_cli_files()

    merged = 0
    for m in MERGES:
        if m.source == m.target:
            continue
        if apply_merge(m):
            merged += 1
            src_title = Path(m.source).stem
            tgt_title = Path(m.target).stem
            if src_title != tgt_title:
                replace_wikilinks(src_title, tgt_title)

    print(f"Merged {merged} duplicate notes into canonical targets")
    print(f"Renamed {len(renames)} CLI files")
    print("Built CLI files:")
    for f in cli_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
