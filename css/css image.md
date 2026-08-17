[[tailwindcss]] [[scss]] [[Flash of Unstyled Content]] [[Animation]]

# CSS image sizing (clipped container)

> Percent-sized images inside a clipped parent need explicit width, height, and `object-fit` — otherwise browsers disagree on the containing block and the image stretches or leaks.

```txt
        CSS image sizing ( ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use clipped-image sizing to check whether you understand replace…

## Sources
- [MDN — `object-fit`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) — deep-dive
- [MDN — Styling replaced elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Images/Replaced_element_properties) — overview
- [MDN — `object-position`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position) — overview

## Key Concepts
- **Containing block:** `%` width/height resolve against the parent
- **`object-fit: cover | contain | fill`:** scale media inside the box → `cover` crops
- **Clip wrapper:** `overflow: hidden` on the parent crops
- **Inline gap:** `img` is inline by default → baseline gap (~4px); `display: block` removes it.
- **CLS:** missing width/height attributes → layout shift when the image loads.


- **Core:** A replaced element (`img`, `video`) has intrinsic dimensions

## Technical Details
```txt
Parent (overflow:hidden, width: 40%)
  └─ img (100% × 100%)  ← needs object-fit + defined box
Fix: img { width:100%; height:100%; object-fit: cover; display:block; }
```

### Robust pattern

```css
.clip-wrap {
  overflow: hidden;
  width: var(--progress, 50%);
  aspect-ratio: 16 / 9; /* or an explicit height */
}

.clip-wrap img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: left; /* progress-style reveal */
}
```

### Tailwind equivalent

```html
<div class="overflow-hidden aspect-video" style="width: 45%">
  <img
    class="block h-full w-full object-cover object-left"
    src="…"
    alt=""
    width="640"
    height="360"
  />
</div>
```

### Background alternative

```css
.hero {
  background-image: url('…');
  background-size: cover;
  background-position: center;
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Chrome stretched, Firefox OK | Computed sizes | `object-fit: cover`; `display: block` |
| Image overflows clip | Parent `overflow` | `overflow: hidden` on wrapper |
| Aspect ratio collapse | No height chain | Parent `aspect-ratio` or fixed height |
| Blurry upscale | Intrinsic vs display size | Correct resolution; `srcset` |
| CLS on load | Missing dimensions | HTML `width`/`height` or `aspect-ratio` |

## Mistakes to Avoid
- **Mistake:** Expecting `object-fit` without both width and height on the repl…
- **Mistake:** Fighting `img` for pure decoration
- **Mistake:** Using `object-fit: none` unless you truly want pixel-exact, unsc…

## Pros/Cons or Trade-offs
- **Pro:** `img` + `object-fit` keeps semantics and `alt` text while cropping cleanly.
- **Con:** Percentage height fails if any ancestor lacks a definite height.
- **Con:** Decorative fills are often simpler as `background-image`.

## Comparison
- vs `background-size: cover`: backgrounds are not replaced elements
- vs [[Flash of Unstyled Content]]: missing dimensions cause CLS; late CSS causes FOUC


### Use cases
- Progress bars that reveal a photo, avatar crops in fixed squares, and hero me…

- **Example:** A funding progress widget sets wrapper width to 45% and uses `ob…
