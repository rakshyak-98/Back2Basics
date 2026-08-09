[[WORKLOG.md]]

# Work Log — DRM Streaming Demo

> Work Log — DRM Streaming Demo — project: Browser DRM playback demo (streaming origin + Widevine + license server)

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Work Log — DRM Streaming Demo — plain job, how I run it, how I know it’s broken.


**Project:** Browser DRM playback demo (streaming origin + Widevine + license server)
**Period:** June 2026

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Work Log — DRM Streaming Demo** | Core idea of this note | “I can explain Work Log — DRM Streaming Demo without jargon.” |
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

[[WORKLOG.md]]
