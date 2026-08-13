[[css]]

# CSS property

> CSS property — if you change the <p> element’s display property to inline, the ::first-letter pseudo-element will not work because ::first-letter only…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** CSS property — if you change the <p> element’s display property to inline, the ::first-letter pseudo-element will not work because ::first-letter only…

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

[[css]]
