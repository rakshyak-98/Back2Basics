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

**Say it in one breath:** Minimal steps that **reliably** show whether a bug still exists — the human executable test for triage and QA handoff.

A good repro removes ambiguity: **preconditions**, **steps**, **expected**, **actual**. If two engineers follow it and see different results, the repro isn't stable yet. Attach environment (OS, version, feature flags, data snapshot id).

```
Given → When → Then (plus environment pin)
```


---

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

[[TL;DR]]] [[[general]]] [[[DevOps/Jenkins]]
