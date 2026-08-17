[[scss]] [[css image]] [[Flash of Unstyled Content]] [[Animation]] [[tailwindcss]]

# CSS property

> A CSS property is a named style setting (`display`, `color`, `object-fit`) — some only apply in certain layout contexts, so changing one property can silently disable another feature.

```txt
        CSS property ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use tricky properties (`::first-letter` with `display`, line cla…

## Sources
- [MDN — `::first-letter`](https://developer.mozilla.org/en-US/docs/Web/CSS/::first-letter) — deep-dive
- [MDN — `-webkit-line-clamp`](https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-line-clamp) — overview
- [MDN — CSS reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference) — overview

## Key Concepts
- **Applicability:** `::first-letter` styles the first letter of a **block container**
- **Limited property sets:** some pseudo-elements only accept a subset of properties (fonts, colors, float…
- **Line clamp:** multi-line ellipsis uses a legacy `-webkit-box` flex path plus `-webkit-line-…
- **Replaced elements:** `object-fit` applies to `img`/`video` boxes — see [[css image]].
- **Cascade vs inheritance:** some properties inherit (`color`); others do not (`margin`)


- **Core:** Each CSS property has a defined set of elements and display types it applies …

## Technical Details
### `::first-letter` needs a block container

```css
/* Works — p is block by default */
p::first-letter {
  font-size: 2rem;
  font-weight: bold;
}

/* Breaks drop-cap — inline is not a block container for ::first-letter */
p.inline-lede {
  display: inline;
}
```

- From MDN: `::first-letter` applies to the first letter of the first line of a…

### Multi-line ellipsis

```css
h1 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Quick applicability checklist

| Feature | Needs | Common break |
|---------|-------|--------------|
| `::first-letter` | Block container | `display: inline` / flex item quirks |
| `object-fit` | Replaced element + sized box | Missing width/height |
| `%` height | Definite parent height | Auto-height ancestors |
| Sticky | Non-overflowing ancestor chain | `overflow: hidden` parent |

## Mistakes to Avoid
- **Mistake:** Assuming every pseudo-element works on any `display` value
- **Mistake:** Debugging inheritance when the property does not inherit
- **Mistake:** Clamping text with only `text-overflow: ellipsis` on a multi-lin…

## Pros/Cons or Trade-offs
- **Pro:** Declarative properties keep styling out of JavaScript for most UI chrome.
- **Con:** Silent non-application (wrong display type) is hard to spot without DevTools computed styles.
- **Con:** Vendor-prefixed line-clamp remains the practical multi-line truncate path in many browsers.

## Comparison
- vs [[scss]] variables/mixins: preprocessors author values
- vs [[tailwindcss]] utilities: utilities are named bundles of property declarations


### Use cases
- Editorial drop caps, card title clamping in dense grids, and hero image crops…

- **Example:** A magazine layout’s drop cap vanishes after a utility class sets…
