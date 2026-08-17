[[tailwindcss]] [[scss]] [[Flash of Unstyled Content]] [[Animation]]

# CSS image sizing (clipped container)

> Percent-sized images inside a clipped parent need explicit width, height, and `object-fit` — otherwise browsers disagree on the containing block and the image stretches or leaks.





## Interview Relevance
Interviewers use clipped-image sizing to check whether you understand replaced elements, percentage height chains, and `object-fit` versus `background-size` for crop-and-fill UI.

## Sources
- [MDN — `object-fit`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) — deep-dive
- [MDN — Styling replaced elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Images/Replaced_element_properties) — overview
- [MDN — `object-position`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position) — overview

## Core Definition
A replaced element (`img`, `video`) has intrinsic dimensions; CSS `width`/`height` size its box, while `object-fit` / `object-position` control how the media paints inside that box without changing layout the way `background-*` does on a non-replaced box.

## Key Concepts
- **Containing block:** `%` width/height resolve against the parent — parents need a defined size for `%` height to work.
- **`object-fit: cover | contain | fill`:** scale media inside the box → `cover` crops; `contain` letterboxes; `fill` stretches.
- **Clip wrapper:** `overflow: hidden` on the parent crops; sizing belongs on the `img`, not only the wrapper.
- **Inline gap:** `img` is inline by default → baseline gap (~4px); `display: block` removes it.
- **CLS:** missing width/height attributes → layout shift when the image loads.

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

## Real-World Applications
Progress bars that reveal a photo, avatar crops in fixed squares, and hero media inside aspect-ratio cards all need `object-fit` plus a stable box.

**Example:** A funding progress widget sets wrapper width to 45% and uses `object-fit: cover; object-position: left` so the image fills the clipped region without squashing.

## Pros/Cons or Trade-offs
- **Pro:** `img` + `object-fit` keeps semantics and `alt` text while cropping cleanly.
- **Con:** Percentage height fails if any ancestor lacks a definite height.
- **Con:** Decorative fills are often simpler as `background-image`.

## Comparison
- vs `background-size: cover`: backgrounds are not replaced elements — no intrinsic `alt`, easier fill, weaker semantics.
- vs [[Flash of Unstyled Content]]: missing dimensions cause CLS; late CSS causes FOUC — related polish issues.

## Mistakes to Avoid
- Expecting `object-fit` without both width and height on the replaced element.
- Fighting `img` for pure decoration — prefer background when there is no meaningful `alt`.
- Using `object-fit: none` unless you truly want pixel-exact, unscaled cropping.
