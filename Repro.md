[[TL;DR]] [[general]] [[DevOps/Jenkins]]

# Repro (reproduction case)

> Minimal steps that **reliably** show whether a bug still exists — the human executable test for triage and QA handoff.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Repro — plain job, how I run it, how I know it’s broken.


A good repro removes ambiguity: **preconditions**, **steps**, **expected**, **actual**. If two engineers follow it and see different results, the repro isn't stable yet. Attach environment (OS, version, feature flags, data snapshot id).

```
Given → When → Then (plus environment pin)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Repro** | Core idea of this note | “I can explain Repro without jargon.” |
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

[[TL;DR]]] [[[general]]] [[[DevOps/Jenkins]]
