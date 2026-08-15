# Back2Basics
> Staff-engineer field notes — fast lookup for debug, configs, interviews, and mental models.


Staff-engineer **field notes** — fast retrieval for debugging, standard configs, interview prep, and solid mental models.

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

Leaf notes follow a fixed **interview-prep** section order (omit empties):

1. **Clear language** — plain-English blockquote; the writer owns comprehension.
2. **Predictable sections** — Interview Relevance → Sources → Core Definition → Key Concepts → Technical Details → Applications → Trade-offs → Comparison → Mistakes to Avoid.
3. **Networked organization** — `[[wikilinks]]` to siblings and parents; hubs route, leaves go deep.

See [[AGENT_NOTE_RULES]] for the full agent reference.

---

## Domains

Linux · Operating System · Networking · DNS · Docker · Kubernetes · Terraform · Nginx · Database · Redis · Security · ssh · Protocol · GIT · NodeJS · Streaming · System Design · …

Use [[INDEX]] for on-call routing.

---

## Contributing to this vault

1. Read [[AGENT_NOTE_RULES]]; use the interview-prep leaf skeleton; omit empty sections.
2. Ground facts in authoritative sources (RFCs, official docs, university materials, Wikipedia + primaries); tag overview vs deep-dive.
3. Prefer expanding one empty/stub over adding a fifth synonym.
4. Merge duplicates with a redirect (`→ [[Canonical]]`).
5. Link siblings with Obsidian `[[wikilinks]]`.

---

## Why this exists

Abstractions hide the machine until production fails. These notes dig back to **process tables, sockets, WAL, route tables, cgroups, and failure modes** so you can design, debug, and interview with evidence — not folklore.
