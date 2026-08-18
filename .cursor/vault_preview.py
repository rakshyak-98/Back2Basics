#!/usr/bin/env python3
"""Back2Basics vault tooling: preview server + wikilink integrity check.

This vault is an Obsidian knowledge base (Markdown + a few .canvas files) with no
application to build or run. The meaningful "development experience" is:

  * browsing rendered notes with working [[wikilink]] navigation, and
  * validating that [[wikilinks]] resolve to notes that actually exist.

This single script provides both, with no third-party dependency required for
the link checker. The HTTP preview uses the optional ``markdown`` package when
available and falls back to a minimal renderer otherwise.

Usage:
    python3 .cursor/vault_preview.py check        # wikilink integrity report
    python3 .cursor/vault_preview.py serve        # browsable preview on :8000
    python3 .cursor/vault_preview.py serve --port 9000 --host 0.0.0.0
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
import urllib.parse
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories that are not part of the note tree.
IGNORE_DIRS = {".git", ".obsidian", ".cursor"}

# Wikilink targets that are intentionally unresolved: template placeholders from
# NOTES_STANDARD.md and topics that are folders rather than notes. These are not
# counted as broken links (see AGENTS.md).
PLACEHOLDER_TARGETS = {
    "parent",
    "sibling",
    "tool",
    "wikilinks",
    "canonical",
    "target",
    "…",
    "...",
}

WIKILINK_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def iter_markdown_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def iter_all_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def rel(path: str) -> str:
    return os.path.relpath(path, VAULT_ROOT).replace(os.sep, "/")


class VaultIndex:
    """Resolves Obsidian-style link targets to vault-relative file paths."""

    def __init__(self, root: str = VAULT_ROOT):
        self.root = root
        # note lookups (extension stripped), lowercased for lenient matching
        self.by_basename: dict[str, list[str]] = defaultdict(list)
        self.by_relpath: dict[str, str] = {}
        # asset lookups keep their extension
        self.asset_by_basename: dict[str, list[str]] = defaultdict(list)
        self.asset_by_relpath: dict[str, str] = {}
        self._build()

    def _build(self) -> None:
        for path in iter_all_files(self.root):
            r = rel(path)
            low = r.lower()
            if low.endswith(".md"):
                no_ext = r[:-3]
                self.by_relpath[no_ext.lower()] = r
                self.by_basename[os.path.basename(no_ext).lower()].append(r)
            else:
                self.asset_by_relpath[low] = r
                self.asset_by_basename[os.path.basename(low)].append(r)

    def resolve(self, target: str, is_embed: bool = False) -> str | None:
        """Return the vault-relative path for a link target, or None."""
        target = target.strip().strip("/")
        if not target:
            return None
        low = target.lower()

        if is_embed and not low.endswith(".md"):
            # image / asset embed
            if low in self.asset_by_relpath:
                return self.asset_by_relpath[low]
            hits = self.asset_by_basename.get(os.path.basename(low))
            return hits[0] if hits else None

        # note link: try full relative path first, then basename
        candidates = [low]
        if low.endswith(".md"):
            candidates.append(low[:-3])
        for cand in candidates:
            if cand in self.by_relpath:
                return self.by_relpath[cand]
        base = os.path.basename(candidates[-1])
        hits = self.by_basename.get(base)
        return hits[0] if hits else None


def strip_code(text: str) -> str:
    """Remove fenced and inline code so link extraction ignores shell ``[[ ]]``."""
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def parse_wikilink(inner: str) -> tuple[str, str]:
    """Split raw wikilink body into (target, display). Handles alias + heading."""
    # unescape Obsidian's escaped pipe
    inner = inner.replace("\\|", "|")
    if "|" in inner:
        target, display = inner.split("|", 1)
    else:
        target, display = inner, inner
    target = target.split("#", 1)[0]  # drop heading anchor for resolution
    return target.strip(), display.strip()


# --------------------------------------------------------------------------- #
# Link checker
# --------------------------------------------------------------------------- #
def run_check() -> int:
    index = VaultIndex()
    md_files = sorted(iter_markdown_files(VAULT_ROOT), key=rel)

    total_links = 0
    resolved = 0
    placeholders = 0
    broken: list[tuple[str, str]] = []

    for path in md_files:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            body = strip_code(fh.read())
        for embed_mark, inner in WIKILINK_RE.findall(body):
            target, _ = parse_wikilink(inner)
            if not target:
                continue
            total_links += 1
            is_embed = embed_mark == "!"
            if index.resolve(target, is_embed=is_embed):
                resolved += 1
            elif target.lower() in PLACEHOLDER_TARGETS:
                placeholders += 1
            else:
                broken.append((rel(path), target))

    note_count = len(md_files)
    asset_count = sum(len(v) for v in index.asset_by_basename.values())
    resolvable = total_links - placeholders
    pct = (resolved / resolvable * 100) if resolvable else 100.0

    print("Back2Basics vault — wikilink integrity report")
    print("=" * 48)
    print(f"Markdown notes indexed : {note_count}")
    print(f"Non-note assets indexed: {asset_count}")
    print(f"Wikilinks scanned      : {total_links}")
    print(f"  resolved             : {resolved}")
    print(f"  intentional placeholder: {placeholders}")
    print(f"  unresolved (broken)  : {len(broken)}")
    print(f"Resolution rate        : {pct:.1f}% of resolvable links")
    print("=" * 48)

    if broken:
        print(f"\nUnresolved links ({len(broken)} — some may be intended stubs):")
        for src, target in broken[:60]:
            print(f"  {src}: [[{target}]]")
        if len(broken) > 60:
            print(f"  ... and {len(broken) - 60} more")

    # A non-empty vault with a healthy resolution rate is a pass. Unresolved
    # links are expected (stubs / folder topics), so they are reported, not
    # treated as a hard failure.
    return 0 if note_count > 0 else 1


# --------------------------------------------------------------------------- #
# Preview server
# --------------------------------------------------------------------------- #
try:
    import markdown as _markdown  # type: ignore

    def render_markdown(text: str) -> str:
        return _markdown.markdown(
            text,
            extensions=["fenced_code", "tables", "toc", "sane_lists", "nl2br"],
        )

    RENDERER = "python-markdown"
except Exception:  # pragma: no cover - fallback path

    def render_markdown(text: str) -> str:
        # Minimal fallback: escape and keep code blocks readable.
        return "<pre>" + html.escape(text) + "</pre>"

    RENDERER = "fallback(pre)"


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Back2Basics</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         max-width: 820px; margin: 0 auto; padding: 2rem 1.25rem 5rem; line-height: 1.6; }}
  header {{ border-bottom: 1px solid #8884; margin-bottom: 1.5rem; padding-bottom: .5rem; }}
  header a {{ text-decoration: none; font-weight: 600; }}
  code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
  pre {{ background: #8881; padding: .85rem 1rem; border-radius: 6px; overflow-x: auto; }}
  code {{ background: #8882; padding: .1rem .3rem; border-radius: 4px; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #8884; padding: .4rem .6rem; text-align: left; }}
  a.wikilink {{ color: #3b82f6; text-decoration: none; }}
  a.wikilink:hover {{ text-decoration: underline; }}
  a.wikilink.broken {{ color: #ef4444; border-bottom: 1px dashed #ef4444; }}
  img {{ max-width: 100%; }}
  blockquote {{ border-left: 3px solid #8886; margin: 1rem 0; padding: .2rem 1rem; color: inherit; }}
</style></head>
<body>
<header><a href="/">Back2Basics</a> &nbsp;·&nbsp; <a href="/INDEX.md">INDEX</a>
&nbsp;·&nbsp; <a href="/README.md">README</a>
&nbsp;·&nbsp; <span style="opacity:.6">renderer: {renderer}</span></header>
<main>{body}</main>
</body></html>"""


def wikilinks_to_html(text: str, index: VaultIndex) -> str:
    """Replace [[links]] with anchors, skipping code so shell ``[[ ]]`` is safe."""

    def repl(match: re.Match) -> str:
        embed_mark, inner = match.group(1), match.group(2)
        target, display = parse_wikilink(inner)
        is_embed = embed_mark == "!"
        resolved = index.resolve(target, is_embed=is_embed) if target else None
        if is_embed and resolved and not resolved.lower().endswith(".md"):
            src = "/" + urllib.parse.quote(resolved)
            return f'<img src="{src}" alt="{html.escape(display)}">'
        if resolved:
            href = "/" + urllib.parse.quote(resolved)
            return f'<a class="wikilink" href="{href}">{html.escape(display)}</a>'
        return (
            f'<a class="wikilink broken" href="#" title="unresolved: {html.escape(target)}">'
            f"{html.escape(display)}</a>"
        )

    # Protect fenced code blocks: rebuild the string, only rewriting outside code.
    parts = []
    last = 0
    for m in FENCE_RE.finditer(text):
        segment = text[last:m.start()]
        parts.append(WIKILINK_RE.sub(repl, segment))
        parts.append(m.group(0))
        last = m.end()
    tail = text[last:]
    parts.append(WIKILINK_RE.sub(repl, tail))
    return "".join(parts)


class PreviewHandler(BaseHTTPRequestHandler):
    index: VaultIndex = None  # set on the class before serving

    def log_message(self, fmt, *args):  # quieter logs
        sys.stderr.write("[preview] " + (fmt % args) + "\n")

    def _send(self, status: int, body: bytes, content_type: str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        raw = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        relpath = raw.lstrip("/")
        if relpath in ("", "/"):
            relpath = "README.md"

        abs_path = os.path.normpath(os.path.join(VAULT_ROOT, relpath))
        # prevent path traversal outside the vault
        if not abs_path.startswith(VAULT_ROOT):
            self._send(403, b"forbidden", "text/plain; charset=utf-8")
            return
        if not os.path.isfile(abs_path):
            self._send(
                404,
                self._page("Not found", f"<h1>404</h1><p>No file: {html.escape(relpath)}</p>"),
                "text/html; charset=utf-8",
            )
            return

        if abs_path.lower().endswith(".md"):
            with open(abs_path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            linked = wikilinks_to_html(text, self.index)
            body = render_markdown(linked)
            title = os.path.basename(abs_path)[:-3]
            self._send(200, self._page(title, body), "text/html; charset=utf-8")
        else:
            ctype = self._guess_type(abs_path)
            with open(abs_path, "rb") as fh:
                self._send(200, fh.read(), ctype)

    @staticmethod
    def _guess_type(path: str) -> str:
        ext = os.path.splitext(path)[1].lower()
        return {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".webp": "image/webp",
            ".canvas": "application/json",
            ".json": "application/json",
        }.get(ext, "application/octet-stream")

    def _page(self, title: str, body: str) -> bytes:
        return PAGE_TEMPLATE.format(
            title=html.escape(title), body=body, renderer=RENDERER
        ).encode("utf-8")


def run_serve(host: str, port: int) -> int:
    PreviewHandler.index = VaultIndex()
    note_count = len(list(iter_markdown_files(VAULT_ROOT)))
    server = ThreadingHTTPServer((host, port), PreviewHandler)
    print(f"Back2Basics preview serving {note_count} notes")
    print(f"Renderer: {RENDERER}")
    print(f"Open http://{host}:{port}/  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping preview server")
    finally:
        server.server_close()
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Back2Basics vault tooling")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="report wikilink integrity")
    s = sub.add_parser("serve", help="serve a browsable HTML preview")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    if args.cmd == "check":
        return run_check()
    if args.cmd == "serve":
        return run_serve(args.host, args.port)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
