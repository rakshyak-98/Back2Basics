#!/usr/bin/env bash
# Idempotent setup for the Back2Basics Obsidian vault.
#
# This repository is a Markdown knowledge base with no application to compile.
# The only dependency is the pure-Python `markdown` package, used by the
# preview server (.cursor/vault_preview.py) to render notes as HTML. The
# wikilink integrity checker needs no third-party packages at all.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[install] python: $(python3 --version)"

# Install the optional renderer dependency into the user site. Pure Python, so
# no venv or system packages are required; re-runs are no-ops once satisfied.
if python3 -c 'import markdown' 2>/dev/null; then
  echo "[install] markdown already present: $(python3 -c 'import markdown; print(markdown.__version__)')"
else
  echo "[install] installing markdown"
  python3 -m pip install --user --break-system-packages markdown
fi

echo "[install] markdown version: $(python3 -c 'import markdown; print(markdown.__version__)')"

# Smoke-test the vault: report wikilink integrity. Non-fatal by design because
# a portion of wikilinks are intentionally unresolved (template placeholders
# and folder topics), so this is informational rather than a hard gate.
echo "[install] running wikilink integrity check"
python3 .cursor/vault_preview.py check | sed -n '1,10p' || true

echo "[install] done"
