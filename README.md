# Back2Basics

Staff-engineer **field notes** — fast retrieval for debugging, standard configs, and solid mental models.

Not a framework zoo. Not man-page dumps. Notes are written for software engineers under pressure: OS, networking, databases, containers, IaC, security, and the runtimes you ship.

---

## Start here

| Need | Open |
|------|------|
| How notes are structured | [[NOTES_STANDARD]] |
| Symptom → note map | [[INDEX]] |
| Staff-level skill model | [[staff engineer]] |

---

## What good looks like

Every note should answer under ~2 minutes:

1. **What is this?** (mental model)
2. **How do I configure it correctly?** (standard config / commands)
3. **How do I debug it when it breaks?** (triage table)
4. **What bites people in production?** (gotchas)

Templates already in the vault: [[Terraform workflow]], [[gRPC]], [[Configuration]] (Nginx), [[file descriptors]], [[ss]].

---

## Domains

Linux · Operating System · Networking · DNS · Docker · Kubernetes · Terraform · Nginx · Database · Redis · Security · ssh · Protocol · GIT · NodeJS · Streaming · System Design · …

Use [[INDEX]] for on-call routing.

---

## Contributing to this vault

1. Read [[NOTES_STANDARD]] before writing.
2. Prefer expanding one empty/stub over adding a fifth synonym.
3. Merge duplicates with a redirect (`→ [[Canonical]]`).
4. Strip wiki/ChatGPT citation spam; keep book/source attributions that are real (Kleppmann, Kerrisk, Brikman, Stevens, Burns).
5. Link siblings with Obsidian `[[wikilinks]]`.

---

## Why this exists

Abstractions hide the machine until production fails. These notes dig back to **process tables, sockets, WAL, route tables, cgroups, and failure modes** so you can design and debug with evidence — not folklore.
