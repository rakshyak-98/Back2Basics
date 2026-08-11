#!/usr/bin/env python3
"""Expand casual abbreviations in prose and remove generic template boilerplate."""

from __future__ import annotations

import re
import sys
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

BAD_MENTAL_RE = re.compile(
    r"\*\*Say it in one breath:\*\*[^\n]*infra/security tooling[^\n]*\n+",
    re.IGNORECASE,
)

GENERIC_INTERVIEW_BLOCK_RE = re.compile(
    r"\n### Interview map \(words you can say\)\n\n"
    r"\| Word \| Plain meaning \| Say in interview \|\n"
    r"\|[-| ]+\|\n"
    r"\| \*\*[^|]+\*\* \| Core idea of this note \|[^\n]+\n"
    r"(?:\| \*\*[^|]+\*\* \|[^\n]+\n)+",
    re.MULTILINE,
)

GENERIC_TRIAGE_BLOCK_RE = re.compile(
    r"\n## Triage \(when things break\)\n\n"
    r"\| Symptom \| Check \| Fix \|\n"
    r"\|[-| ]+\|\n"
    r"\| Auth fail \| clock / creds / IAM \| Sync time; fix policy \|\n"
    r"\| TLS error \| cert chain / SNI \| Fix certs and CA bundle \|\n"
    r"\| Deploy down \| rollback / health \| Roll back; check probes \|\n",
    re.MULTILINE,
)

TEMPLATE_TRIAGE_BLOCK_RE = re.compile(
    r"\n## Triage \(when things break\)\n\n"
    r"\| Symptom \| Check \| Fix \|\n"
    r"\|[-| ]+\|\n"
    r"\| Unexpected result \| inputs / versions \| Reproduce minimal case \|\n"
    r"\| Works on one machine \| env drift \| Diff config and versions \|\n"
    r"\| Silent failure \| logs / metrics \| Add checks and alerts \|\n",
    re.MULTILINE,
)

PLACEHOLDER_STD_CONFIG_RE = re.compile(
    r"\n## Standard config / commands\n\n```bash\n# status\n# check version, auth, and recent changes\n```\n",
    re.MULTILINE,
)

GENERIC_WHEN_NOT_RE = re.compile(
    r"\n## When NOT to use\n\n- Don’t build custom infra when managed services meet the SLO\.\n",
    re.MULTILINE,
)

GENERIC_GOTCHA_RE = re.compile(
    r"\n## Gotchas\n\n> \[!WARNING\]\n> Never commit long-lived secrets\.\n",
    re.MULTILINE,
)

ONELINER_RE = re.compile(r"^> (.+)$", re.MULTILINE)

# Safe phrase-level replacements (whole phrases, not single words).
PHRASE_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bworking vs broken env\b", re.I), "working versus broken environment"),
    (re.compile(r"\bworking vs broken environment\b", re.I), "working versus broken environment"),
    (re.compile(r"\benv drift\b", re.I), "environment differences between machines"),
    (re.compile(r"\bDiff config and versions\b"), "Compare configuration files and software versions"),
    (re.compile(r"\bcompare working vs broken env\b", re.I), "compare working versus broken environment"),
    (re.compile(r"# compare working vs broken env\b", re.I), "# compare working versus broken environment"),
    (re.compile(r"\bcheck version, auth, and recent changes\b", re.I),
     "check version, authentication, and recent changes"),
]

# Word replacements only on prose lines (not tables, headings, code).
WORD_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\be\.g\.\b"), "for example"),
    (re.compile(r"\bi\.e\.\b"), "that is"),
    (re.compile(r"\baka\b", re.I), "also known as"),
    (re.compile(r"\bapprox\b", re.I), "approximately"),
    (re.compile(r"\bthru\b", re.I), "through"),
    (re.compile(r"\bw/o\b"), "without"),
    (re.compile(r"\bw/\b"), "with"),
    (re.compile(r"\bcreds\b", re.I), "credentials"),
    (re.compile(r"\bprivileges needed\b", re.I), "privileges needed"),  # anchor
    (re.compile(r"\bpriv\b", re.I), "privileges"),
    (re.compile(r"\bcwd\b", re.I), "current working directory"),
    (re.compile(r"\bFD leak\b"), "file descriptor leak"),
    (re.compile(r"\bFD\b"), "file descriptor"),
    (re.compile(r"\bauth fail\b", re.I), "authentication failure"),
    (re.compile(r"\bauth\b", re.I), "authentication"),
    (re.compile(r"\bprod\b", re.I), "production"),
    (re.compile(r"\bdev\b", re.I), "development"),
    (re.compile(r"\brepo\b", re.I), "repository"),
    (re.compile(r"\bconfig\b", re.I), "configuration"),
    (re.compile(r"\bapp\b", re.I), "application"),
    (re.compile(r"\benv\b", re.I), "environment"),
    (re.compile(r"\bvs\b"), "versus"),
    (re.compile(r"\badmin\b", re.I), "administrator"),
    (re.compile(r"\bops\b", re.I), "operations"),
    (re.compile(r"\bmgmt\b", re.I), "management"),
    (re.compile(r"\butil\b", re.I), "utility"),
    (re.compile(r"\bparams\b", re.I), "parameters"),
    (re.compile(r"\bparam\b", re.I), "parameter"),
    (re.compile(r"\bargs\b", re.I), "arguments"),
    (re.compile(r"\bfunc\b", re.I), "function"),
    (re.compile(r"\bvars\b", re.I), "variables"),
    (re.compile(r"\bvar\b", re.I), "variable"),
    (re.compile(r"\btemp\b", re.I), "temporary"),
    (re.compile(r"\bproc\b", re.I), "process"),
    (re.compile(r"\bsrc\b", re.I), "source"),
    (re.compile(r"\bdst\b", re.I), "destination"),
    (re.compile(r"\breq\b", re.I), "request"),
    (re.compile(r"\bres\b", re.I), "response"),
    (re.compile(r"\berr\b", re.I), "error"),
    (re.compile(r"\bmsg\b", re.I), "message"),
    (re.compile(r"\bval\b", re.I), "value"),
    (re.compile(r"\bobj\b", re.I), "object"),
    (re.compile(r"\barr\b", re.I), "array"),
    (re.compile(r"\bstr\b", re.I), "string"),
    (re.compile(r"\bnum\b", re.I), "number"),
    (re.compile(r"\bspec\b", re.I), "specification"),
    (re.compile(r"\bimpl\b", re.I), "implementation"),
    (re.compile(r"\bext\b", re.I), "external"),
    (re.compile(r"\binfo\b", re.I), "information"),
    (re.compile(r"\bdoc\b", re.I), "document"),
    (re.compile(r"\bref\b", re.I), "reference"),
    (re.compile(r"\binit\b", re.I), "initialize"),
    (re.compile(r"\bexec\b", re.I), "execute"),
]

RESTORE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"git configuration"), "git config"),
    (re.compile(r"next\.configuration"), "next.config"),
    (re.compile(r"tsconfiguration"), "tsconfig"),
    (re.compile(r"~/.ssh/configuration"), "~/.ssh/config"),
    (re.compile(r"/\.ssh/configuration\b"), "/.ssh/config"),
    (re.compile(r"var\.environment"), "var.environment"),
    (re.compile(r"pm\.environment"), "pm.environment"),
    (re.compile(r"import\.meta\.environment"), "import.meta.env"),
    (re.compile(r"process\.environment"), "process.env"),
    (re.compile(r"\.environment`"), ".env`"),
    (re.compile(r"\.environment\b"), ".env"),
    (re.compile(r"\benvironmentIRONMENT\b"), "environment"),
    (re.compile(r"applicationlication"), "application"),
    (re.compile(r"configfiguration"), "configuration"),
    (re.compile(r"authenticationhentication"), "authentication"),
    (re.compile(r"productionduction"), "production"),
    (re.compile(r"developmentvelopment"), "development"),
    (re.compile(r"repositorypository"), "repository"),
    (re.compile(r"\| versus \|"), "| vs |"),
    (re.compile(r"versus rebase"), "vs rebase"),
    (re.compile(r"versus static"), "vs static"),
    (re.compile(r"HLS versus\. DASH"), "HLS vs. DASH"),
    (re.compile(r"Standard configuration / commands"), "Standard config / commands"),
    (re.compile(r"\benvironment variables\b", re.I), "environment variables"),
    (re.compile(r"build\.environment"), "build.environment"),
    (re.compile(r"\[\"development\", \"stage\", \"production\"\]"),
     '["dev", "stage", "prod"]'),
    (re.compile(r"contains\(\[\"development\", \"stage\", \"production\"\]"),
     'contains(["dev", "stage", "prod"]'),
]


def should_skip_line(line: str, in_fence: bool) -> bool:
    if in_fence:
        return True
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("|"):
        return True
    if stripped.startswith("```"):
        return True
    if stripped.startswith("#"):
        return True
    if stripped.startswith(">"):
        return True
    if re.match(r"^[-*]\s+`", stripped):
        return True
    return False


def expand_prose_line(line: str) -> str:
    for pattern, repl in PHRASE_REPLACEMENTS:
        line = pattern.sub(repl, line)
    if should_skip_line(line, False):
        return line
    # Expand inside inline code segments only outside backticks
    parts: list[str] = []
    i = 0
    while i < len(line):
        if line[i] == "`":
            j = line.find("`", i + 1)
            if j == -1:
                parts.append(line[i:])
                break
            parts.append(line[i : j + 1])
            i = j + 1
            continue
        j = line.find("`", i)
        chunk = line[i:] if j == -1 else line[i:j]
        i = len(line) if j == -1 else j
        for pattern, repl in WORD_REPLACEMENTS:
            chunk = pattern.sub(repl, chunk)
        parts.append(chunk)
    result = "".join(parts)
    for pattern, repl in RESTORE_PATTERNS:
        result = pattern.sub(repl, result)
    return result


def expand_abbreviations(text: str) -> str:
    in_fence = False
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(expand_prose_line(line))
    return "".join(out)


def extract_oneliner(text: str) -> str | None:
    for m in ONELINER_RE.finditer(text):
        line = m.group(1).strip()
        if line.startswith("[!"):
            continue
        return line
    return None


def fix_bad_mental_model(text: str) -> str:
    if "infra/security tooling" not in text:
        return text
    oneliner = extract_oneliner(text)
    if not oneliner:
        return BAD_MENTAL_RE.sub("", text)
    replacement = f"**Say it in one breath:** {oneliner}\n\n"
    return BAD_MENTAL_RE.sub(replacement, text)


def remove_orphan_separators(text: str) -> str:
    """Collapse runs of --- with only blank lines between them."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            j = i + 1
            while j < len(lines) and lines[j].strip() in {"", "---"}:
                j += 1
            # Keep one --- only if next line is a real section heading
            if j < len(lines) and lines[j].startswith("## "):
                out.append("---")
                out.append("")
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def cleanup_double_blanks(text: str) -> str:
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def process_text(text: str) -> tuple[str, bool]:
    original = text
    text = fix_bad_mental_model(text)
    text = GENERIC_INTERVIEW_BLOCK_RE.sub("\n", text)
    text = GENERIC_TRIAGE_BLOCK_RE.sub("\n", text)
    text = TEMPLATE_TRIAGE_BLOCK_RE.sub("\n", text)
    text = PLACEHOLDER_STD_CONFIG_RE.sub("\n", text)
    text = GENERIC_WHEN_NOT_RE.sub("\n", text)
    text = GENERIC_GOTCHA_RE.sub("\n", text)
    text = remove_orphan_separators(text)
    text = expand_abbreviations(text)
    text = cleanup_double_blanks(text)
    return text, text != original


def process_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text[1:]
    new_text, changed = process_text(text)
    if not changed:
        return "unchanged"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return "updated"


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    stats: dict[str, int] = {}
    for path in sorted(VAULT_ROOT.rglob("*.md")):
        if path.name.startswith("."):
            continue
        rel = path.relative_to(VAULT_ROOT)
        if rel.parts and rel.parts[0] in {".git", "scripts", "tools"}:
            continue
        if path.name in SKIP_FILES:
            stats["skipped"] = stats.get("skipped", 0) + 1
            continue
        result = process_file(path, dry_run=dry_run)
        stats[result] = stats.get(result, 0) + 1
    print("Results:", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
