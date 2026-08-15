[[scss]] [[css image]] [[Flash of Unstyled Content]] [[Animation]] [[tailwindcss]]

# CSS property

> A CSS property is a named style setting (`display`, `color`, `object-fit`) — some only apply in certain layout contexts, so changing one property can silently disable another feature.

## Interview Relevance

Interviewers use tricky properties (`::first-letter` with `display`, line clamping, replaced-element props) to test whether you know applicability rules, not just property names.

## Sources

- [MDN — `::first-letter`](https://developer.mozilla.org/en-US/docs/Web/CSS/::first-letter) — deep-dive
- [MDN — `-webkit-line-clamp`](https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-line-clamp) — overview
- [MDN — CSS reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference) — overview

## Core Definition

Each CSS property has a defined set of elements and display types it applies to; values cascade and inherit according to the property’s rules, and invalid combinations are ignored rather than erroring in the console.

## Key Concepts

- **Applicability:** `::first-letter` styles the first letter of a **block container** — set `display: inline` on a paragraph and the pseudo-element stops applying.
- **Limited property sets:** some pseudo-elements only accept a subset of properties (fonts, colors, floats, etc.).
- **Line clamp:** multi-line ellipsis uses a legacy `-webkit-box` flex path plus `-webkit-line-clamp`.
- **Replaced elements:** `object-fit` applies to `img`/`video` boxes — see [[css image]].
- **Cascade vs inheritance:** some properties inherit (`color`); others do not (`margin`) — knowing which avoids “why didn’t my child get this?” bugs.

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

From MDN: `::first-letter` applies to the first letter of the first line of a block container, and only when not preceded by other content such as images or inline tables.

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

## Real-World Applications

Editorial drop caps, card title clamping in dense grids, and hero image crops all depend on picking properties that apply in the actual box context.

**Example:** A magazine layout’s drop cap vanishes after a utility class sets the lede to `inline` for wrapping — restore block/flow display or wrap the letter another way.

## Pros/Cons or Trade-offs

- **Pro:** Declarative properties keep styling out of JavaScript for most UI chrome.
- **Con:** Silent non-application (wrong display type) is hard to spot without DevTools computed styles.
- **Con:** Vendor-prefixed line-clamp remains the practical multi-line truncate path in many browsers.

## Comparison

- vs [[scss]] variables/mixins: preprocessors author values; CSS properties are what the browser actually applies.
- vs [[tailwindcss]] utilities: utilities are named bundles of property declarations — the same applicability rules still apply.

## Mistakes to Avoid

- Assuming every pseudo-element works on any `display` value — check MDN “applies to.”
- Debugging inheritance when the property does not inherit — look at the element that set it.
- Clamping text with only `text-overflow: ellipsis` on a multi-line block — you also need the line-clamp box model.
