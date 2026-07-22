[[css/tailwindcss]] [[css/scss]] [[css/Animation]]

# CSS image sizing (clipped container)

> When a parent clips width but `<img>` uses `width/height: 100%`, browsers disagree on which box defines 100% — fix with explicit object-fit and containment.

## Mental model

A progress bar or clipped `div` sets **used width** via `%` or flex. Child `img` with `w-full h-full` (Tailwind) or `width:100%; height:100%` resolves percentages against different containing blocks in Chrome vs Firefox if overflow/containment differs. **`object-fit`** + fixed aspect on the img decouples layout from intrinsic image dimensions.

```
Parent (overflow:hidden, width: 40%)
  └─ img (100% × 100%)  ← ambiguous containing block
Fix: img { width:100%; height:100%; object-fit: cover; display:block; }
```

## Standard config / commands

### Robust pattern

```css
.clip-wrap {
  overflow: hidden;
  width: var(--progress, 50%);
}

.clip-wrap img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;        /* or contain */
  object-position: left;    /* for progress reveal */
}
```

### Tailwind equivalent

```html
<div class="overflow-hidden" style="width: 45%">
  <img class="block h-full w-full object-cover object-left" src="…" alt="" />
</div>
```

### Background-image alternative (no img sizing bugs)

```css
.hero {
  background-image: url('…');
  background-size: cover;
  background-position: center;
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Chrome stretched, Firefox correct | DevTools computed sizes | `object-fit: cover`; `display:block` removes inline gap |
| Image overflows clip | Parent `overflow` | `overflow:hidden` on clip container not img |
| Aspect ratio collapse | No explicit height | Parent `aspect-ratio` or fixed height |
| Blurry upscale | Intrinsic vs display size | Serve correct resolution; `srcset` |
| CLS on load | No width/height attrs | `width`/`height` HTML attrs or aspect-ratio |

## Gotchas

> [!WARNING]
> **Inline img baseline gap** — `display:block` or `vertical-align:bottom` fixes 4px leak.
>
> **`object-fit` ignored** — needs explicit width **and** height on replaced element.
>
> **Percentage height chain** — parent needs defined height all the way up.

## When NOT to use

- Don't fight img in clip for decorative fills — `background-image` is simpler.
- Don't use `object-fit: none` unless you mean pixel-exact cropping.

## Related

[[css/tailwindcss]] [[css/Flash of Unstyled Content]] [[css/Animation]]
