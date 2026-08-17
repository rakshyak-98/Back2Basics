# Back2Basics
> Staff-engineer field notes — fast lookup for debug, configs, design reviews, and mental models.


Staff-engineer **field notes** — fast retrieval for debugging, standard configs, study prep, and solid mental models.

Not a framework zoo. Not man-page dumps. Notes are written for software engineers under pressure: OS, networking, databases, containers, IaC, security, and the runtimes you ship.

---

## Start here

| Need | Open |
|------|------|
| How agents (and humans) write notes | [[AGENT_NOTE_RULES]] |
| Symptom → note map | [[INDEX]] |
| Similar / duplicate note clusters | [[Similar Notes — Cluster Map]] |
| Staff-level skill model | [[staff engineer]] |
| Vault meta hub | [[general]] |

---

## What good looks like

Leaf notes pick a **shape** that matches how the topic is held in memory (omit empty sections):

1. **Clear language** — plain-English blockquote as the **center**; the writer owns comprehension.
2. **Mind Map** (default) — 4–7 primary `##` branches radiating from the center for associative topics.
3. **Cornell** — numbered **Technical Details** spine plus **Recall Cues** for sequential flows (lectures, pipelines, runbooks).
4. **Networked organization** — `[[wikilinks]]` to siblings and parents; hubs route, leaves go deep.

See [[AGENT_NOTE_RULES]] for the full agent reference.

---

## Domains

Linux · Operating System · Networking · DNS · Docker · Kubernetes · Terraform · Nginx · Database · Redis · Security · ssh · Protocol · GIT · NodeJS · Streaming · System Design · …

Use [[INDEX]] for on-call routing.

---

## Contributing to this vault

1. Read [[AGENT_NOTE_RULES]]; choose Mind Map or Cornell shape; omit empty sections.
2. Ground facts in authoritative sources (RFCs, official docs, university materials, Wikipedia + primaries); tag overview vs deep-dive.
3. Prefer expanding one empty/stub over adding a fifth synonym.
4. Merge duplicates with a redirect (`→ [[Canonical]]`).
5. Link siblings with Obsidian `[[wikilinks]]`.

---

## Why this exists

Abstractions hide the machine until production fails. These notes dig back to **process tables, sockets, WAL, route tables, cgroups, and failure modes** so you can design, debug, and review with evidence — not folklore.
