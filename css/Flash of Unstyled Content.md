[[scss]] [[Animation]] [[tailwindcss]] [[React]] [[Nginx]]

# Flash of Unstyled Content (FOUC)

> Flash of Unstyled Content is the brief moment unstyled or wrong-theme HTML appears before CSS loads — users see a jump; layout shift metrics suffer.

```txt
        Flash of Unstyled  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about FOUC to see if you understand the critical CSS path, t…

## Sources
- [Wikipedia — Flash of unstyled content](https://en.wikipedia.org/wiki/Flash_of_unstyled_content) — overview
- [web.dev — Optimize CSS delivery](https://web.dev/articles/defer-non-critical-css) — deep-dive
- [MDN — `font-display`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) — overview

## Key Concepts
- **Render-blocking CSS:** `<link rel="stylesheet">` in `<head>` delays first paint until styles apply →…
- **Late CSS:** `@import`, bottom-of-body links, async stylesheets → classic FOUC triggers.
- **Theme flash:** reading `localStorage` after first paint → light then dark (or reverse).
- **CSS-in-JS SSR:** server HTML without matching injected styles → flash or hydration mismatch wi…
- **FOUT:** font swap after fallback metrics → text reflow


- **Core:** The browser paints as HTML arrives; if the CSSOM is incomplete or theme class…

## Technical Details
```txt
Bad:  HTML parsed → first paint (ugly) → CSS arrives → restyle + reflow
Good: CSS discovered early → block until CSSOM → first paint styled
```

### Load critical CSS first

```html
<head>
  <link rel="preconnect" href="https://cdn.example.com" crossorigin>
  <link rel="stylesheet" href="/assets/main.css">
  <!-- Avoid @import in critical CSS — serializes downloads -->
</head>
```

### Inline critical CSS + deferred full sheet

```html
<head>
  <style>
    body { margin: 0; font-family: system-ui, sans-serif; }
    .hero { min-height: 40vh; }
  </style>
  <link rel="preload" href="/assets/main.css" as="style"
        onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/assets/main.css"></noscript>
</head>
```

### Theme before paint

```html
<script>
  (function () {
    const theme =
      localStorage.getItem('theme') ||
      (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    document.documentElement.setAttribute('data-theme', theme)
  })()
</script>
```

```css
:root[data-theme='light'] { --bg: #fff; --fg: #111; }
:root[data-theme='dark']  { --bg: #111; --fg: #eee; }
body { background: var(--bg); color: var(--fg); }
```

### Fonts

```css
@font-face {
  font-family: 'Brand';
  src: url('/fonts/brand.woff2') format('woff2');
  font-display: optional; /* or swap with size-adjusted fallback */
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| White page → styled jump | CSS link at end of body | Move stylesheets to `<head>`; inline critical CSS |
| Dark mode flash | Theme script late | Inline theme script in `<head>` |
| FOUC on slow networks | Waterfall: CSS after JS | Preload CSS; reduce blocking JS |
| Flash after deploy | CDN miss / wrong hash | Atomic deploys; correct cache headers |
| React flash + warnings | SSR style collection | Match server/client classes; see [[hydration]] |
| Tailwind CDN flash | Full utility CSS async | Build CSS at compile time — see [[tailwindcss]] |

## Mistakes to Avoid
- **Mistake:** Using `@import` inside critical CSS — forces serial fetches
- **Mistake:** Relying on Tailwind (or other) CDN builds in production
- **Mistake:** Animating or class-toggling layout on `DOMContentLoaded` that sh…

## Pros/Cons or Trade-offs
- **Pro:** Early CSS and theme scripts make first paint match the final design.
- **Con:** Fully blocking large CSS delays LCP on slow networks — split critical vs deferred.
- **Con:** Hiding `body` until `load` hurts LCP and accessibility; fix delivery instead.

## Comparison
- vs [[Animation]] jank: FOUC is a first-paint styling gap; animation jank is ongoing frame cost.
- vs FOUT: fonts swapping after paint; FOUC is missing stylesheets or theme rules.


### Use cases
- Marketing sites inline critical layout CSS

- **Example:** A Next.js app with theme toggle runs a blocking `<head>` script …
