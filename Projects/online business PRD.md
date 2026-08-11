[[Projects]]

# Product Requirements Document (PRD)

> Product Requirements Document — know what it does, how to configure it, and how it fails in production.

---

## Mental model

**Say it in one breath:** Product Requirements Document — plain job, how I run it, how I know it’s broken.


Absolutely. Here’s a comprehensive PRD for CityDress AI, structured to cover strategy, product, and execution details you can hand to engineers, designers, and stakeholders.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Product Requirements Document** | Core idea of this note | “I can explain Product Requirements Document without jargon.” |
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

[[Projects]]
