[[Rendering performance]]

# composite

> composite — compositing is where the painted parts of the page are put together for displaying on screen.

---

## Mental model

**Say it in one breath:** composite — plain job, how I run it, how I know it’s broken.


Compositing is where the painted parts of the page are put together for displaying on screen.
since the part of the page were potentially drawn onto multiple layers, they need to be applied to the screen in the correct order.
- especially important for elements that overlap another.
#### factors affect page performance:
1. number of compositor layers to need to be managed.
2. the properties that you use for animations.
- Stick to transform and opacity changes for your animations.
- promote moving elements with `will-change` or `translateZ`.
- avoid overusing promotion rules; layers requires memory and management.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **composite** | Core idea of this note | “I can explain composite without jargon.” |
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

[[Rendering performance]]
