# Back2Basics
> Staff-engineer field notes — fast lookup for debug, configs, and mental models.


Staff-engineer **field notes** — fast retrieval for debugging, standard configs, and solid mental models.

Not a framework zoo. Not man-page dumps. Notes are written for software engineers under pressure: OS, networking, databases, containers, IaC, security, and the runtimes you ship.

---

## Start here

| Need | Open |
|------|------|
| How agents (and humans) write notes | [[AGENT_NOTE_RULES]] |
| Symptom → note map | [[INDEX]] |
| Staff-level skill model | [[staff engineer]] |
| Vault meta hub | [[general]] |

---

## What good looks like

Notes follow **clarity, conceptual structure, and active engagement** — not fixed templates:

1. **Clear language** — accessible prose; the writer owns comprehension.
2. **Networked organization** — wikilinks and subject grouping over arbitrary section order.
3. **Engagement cues** — summaries, visual hierarchy, and questions that prompt recall and action.

See [[AGENT_NOTE_RULES]] for the full agent reference.

---

## Domains

Linux · Operating System · Networking · DNS · Docker · Kubernetes · Terraform · Nginx · Database · Redis · Security · ssh · Protocol · GIT · NodeJS · Streaming · System Design · …

Use [[INDEX]] for on-call routing.

---

## Contributing to this vault

1. Read [[AGENT_NOTE_RULES]]; structure by conceptual relationships, not predefined templates.
2. Ground facts in authoritative sources (RFCs, official docs, university materials, Wikipedia + primaries).
3. Prefer expanding one empty/stub over adding a fifth synonym.
4. Merge duplicates with a redirect (`→ [[Canonical]]`).
5. Link siblings with Obsidian `[[wikilinks]]`.

---

## Why this exists

Abstractions hide the machine until production fails. These notes dig back to **process tables, sockets, WAL, route tables, cgroups, and failure modes** so you can design and debug with evidence — not folklore.
