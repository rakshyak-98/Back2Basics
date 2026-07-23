# Notes Standard — Staff Engineer Field Notes

> Algorithm used by top 1% operators: **retrieve fast, debug fast, configure correctly**.
> Source bar: production incident muscle memory + books (Brikman, Stevens, Kerrisk, Kleppmann, Burns) + battle stories from staff/principal eng knowledge transfer — **not** man-page dumps.

---

## Why this format

| Goal | How the note delivers it |
|------|--------------------------|
| Fast retrieval | Front-load mental model + decision table; Obsidian wikilinks |
| Debugging | Symptom → check → fix playbook |
| Standard configs | Copy-pasteable, annotated, production-safe defaults |
| Solid understanding | “Why it exists” + failure modes + when **not** to use |
| Experience signal | Gotchas that only show up after years of on-call |

---

## Note-taking algorithm (apply every rewrite)

1. **Name the concept in one line** — what it *is* for an engineer under pressure.
2. **Mental model (2–5 sentences)** — how the system thinks; draw a tiny ASCII/table if useful.
3. **Standard config / commands** — the boring, correct path. Annotate *why* each knob.
4. **Triage / when things break** — symptom → diagnostic command → likely cause → fix.
5. **Gotchas** — silent failures, daemon overwrites, race conditions, “works in lab / dies in prod”.
6. **When NOT to use** — force-multiplier skill; prevents golden-hammer mistakes.
7. **Related** — `[[wikilinks]]` to siblings (OS ↔ Linux ↔ Network ↔ DB).
8. **Delete fluff** — no Wikipedia history, no ChatGPT citation spam, no empty headings.

---

## Canonical template

```markdown
[[Parent]] [[Sibling]] [[Tool]]

# Topic

> One-line: what / why — **Book or source** if relevant.

## Mental model

…

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
```

---

## Quality bar (pass/fail)

**Pass** if a mid-level SE can:
- configure the thing correctly without leaving the note
- debug the top 3 production failures from the triage table
- explain the mental model in a design review

**Fail** if the note is only: empty, 1-line definition, command list with no interpretation, or AI wiki paste.

---

## Vault priorities (rewrite order)

1. **P0** — empty staff-critical: fd, fsync, WAL, eBPF, epoll, compose, Cilium, …
2. **P1** — thin high-leverage: Redis, ACID, ss, kubectl, certbot, …
3. **P2** — decent → experience-grade: Nginx playbooks, OOM+cgroups, BGP debug
4. **P3** — leave strong notes (Terraform/, gRPC, Nginx Configuration) as templates

---

## Retrieval map

→ [[INDEX]] for domain → note routing.
→ Prefer one sharp note over five stubs. Merge duplicates (e.g. MBR ×2) instead of filling both empties.
