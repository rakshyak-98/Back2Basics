[[staff engineer]] [[general]] [[INDEX]] [[NOTES_STANDARD]]

# we

> **Mission:** force-multiply engineering teams with operational field notes — retrieve fast, debug fast, configure correctly.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** we — plain job, how I run it, how I know it’s broken.


→ Primary hub: **[[staff engineer]]**
→ Vault entry: **[[INDEX]]** · **[[NOTES_STANDARD]]** · **[[README]]**

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **we** | Core idea of this note | “I can explain we without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[staff engineer]]] [[[general]]] [[[INDEX]]] [[[NOTES_STANDARD]]
