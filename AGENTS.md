# AGENTS.md

## Cursor Cloud specific instructions

This repository (`Back2Basics`) is a **documentation/knowledge-base vault**, not a
runnable software product. It is an [Obsidian](https://obsidian.md) vault of
staff-engineer field notes: ~1000+ Markdown (`.md`) files plus a handful of
Obsidian `.canvas` files, organized into topic folders (Linux, Networking,
Docker, Kubernetes, Database, Security, React, NodeJS, etc.).

Non-obvious things worth knowing:

- **There is no build/run/test/lint toolchain.** No `package.json`, `Makefile`,
  `Dockerfile`, lockfiles, or CI config exist. `golang/Makefile.md` is a *note
  about* Makefiles, not a real build file. The update script is intentionally a
  no-op (`true`) — there are no dependencies to install.
- **`.gitignore` only ignores `.obsidian`** (the Obsidian app config). The vault
  itself is the deliverable.
- **The "product" is the notes and their cross-links.** Notes reference each
  other with Obsidian `[[wikilinks]]` (and `[[target|alias]]`). The intended
  viewer is the Obsidian desktop app; any Markdown editor also works.
- **Navigation entry points:** `README.md` (overview), `INDEX.md` (symptom→note
  routing map), `NOTES_STANDARD.md` (note template/quality bar).
- **Validating the vault:** the meaningful integrity check is whether
  `[[wikilinks]]` resolve to existing notes. A quick way to preview rendered
  notes with working wikilink navigation in a browser is to serve the vault with
  a small on-the-fly Markdown→HTML renderer (e.g. Python `markdown` +
  `http.server`) that rewrites `[[name]]` to links against a basename index.
  Note: a portion of wikilinks are intentionally unresolved (template
  placeholders like `[[Parent]]`, `[[Sibling]]`, `[[Tool]]`, `[[wikilinks]]`,
  and topics that are folders rather than notes), so 100% resolution is not
  expected.
