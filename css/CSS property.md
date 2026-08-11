[[css]]

# CSS property

> CSS property — if you change the <p> element’s display property to inline, the ::first-letter pseudo-element will not work because ::first-letter only…

---

## Mental model

**Say it in one breath:** CSS property — plain job, how I run it, how I know it’s broken.


- If you change the `<p>` element’s `display` property to `inline`, the `::first-letter` pseudo-element **will not work** because `::first-letter` only applies to block-level elements.
### Multipline ellipsis
```css
h1 {
  display: -webkit-box;
  -webkit-line-clamp: 3;      /* Limit to 3 lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **CSS property** | Core idea of this note | “I can explain CSS property without jargon.” |
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

[[css]]
