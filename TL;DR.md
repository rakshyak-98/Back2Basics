[[Repro]] [[general]] [[README]]

# TL;DR

> TL;DR — put outcome + key constraint first; details follow. In PRs: what changed and why. In runbooks: fix command before theory. In chat: answer the…

---

## Mental model

**Say it in one breath:** TL;DR — plain job, how I run it, how I know it’s broken.


Put **outcome + key constraint** first; details follow. In PRs: what changed and why. In runbooks: fix command before theory. In chat: answer the question in line one, then context.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **TL;DR** | Core idea of this note | “I can explain TL;DR without jargon.” |
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

[[Repro]]] [[[general]]] [[[README]]
