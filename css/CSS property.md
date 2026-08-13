[[css]]

# CSS property

> CSS property — if you change the <p> element’s display property to inline, the ::first-letter pseudo-element will not work because ::first-letter only…

---

## How it works

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


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[css]]

## Sources

- [Wikipedia — CSS property](https://en.wikipedia.org/wiki/CSS_property)
