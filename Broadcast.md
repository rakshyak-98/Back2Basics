[[Broadcast.md]]

# Broadcast

> Broadcast — one sender to every device on the same LAN broadcast domain.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Broadcast — plain job, how I run it, how I know it’s broken.


Broadcast = One sender -> All devices in the same broadcast domain (LAN).
```txt
        Sender
           |
   -----------------
   |   |   |   |   |
  PC1 PC2 PC3 PC4 PC5
```
- Every device receives the packet, even if it doesn't need it.
Characteristics
- Sent to every host in the subnet.
- Routers do not forward broadcast packets by default.
- Increase unnecessary network traffic.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Broadcast** | Core idea of this note | “I can explain Broadcast without jargon.” |
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

[[Broadcast.md]]
