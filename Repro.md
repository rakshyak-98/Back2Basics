[[TL;DR]] [[general]] [[DevOps/Jenkins]]

# Repro (reproduction case)

> Minimal steps that **reliably** show whether a bug still exists — the human executable test for triage and QA handoff.

---

## How it works

A good repro removes ambiguity: **preconditions**, **steps**, **expected**, **actual**. If two engineers follow it and see different results, the repro isn't stable yet. Attach environment (OS, version, feature flags, data snapshot id).

```
Given → When → Then (plus environment pin)
```


---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[TL;DR]]] [[[general]]] [[[DevOps/Jenkins]]

## Sources

- [Wikipedia — Repro](https://en.wikipedia.org/wiki/Repro)
