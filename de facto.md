[[de facto]] [[Release cycle]] [[general]]

# de facto standard

> De facto standard — so widely used it behaves like a standard without formal ratification.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** de facto standard — plain job, how I run it, how I know it’s broken.


**De jure** = by law/spec (ISO, RFC, ECMA). **De facto** = by market habit (Git, Docker, `{json}` APIs). Interop often follows de facto before formal specs catch up (e.g. OAuth flows, S3 API shape). Risk: vendor lock-in, spec drift, sudden deprecation.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **de facto standard** | Core idea of this note | “I can explain de facto standard without jargon.” |
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

[[de facto]]] [[[Release cycle]]] [[[general]]
