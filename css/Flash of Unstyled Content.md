[[css]] [[scss]] [[Animation]] [[Nginx]] [[React]]

# Flash of Unstyled Content (FOUC)

> Brief display of unstyled or wrong-theme HTML before CSS loads — users see a layout jump; Lighthouse flags CLS; trust drops on first paint.

## Mental model

The browser parses HTML incrementally. If CSS arrives **after** first paint, content renders with **user-agent defaults** (or wrong theme), then **reflows** when rules apply.

```
Timeline (bad):
HTML parsed ──► first paint (ugly) ──► CSS arrives ──► restyle + reflow (FOUC)

Timeline (good):
CSS discovered early ──► block render until CSSOM ──► first paint (styled)
```

Common triggers:
- Render-blocking CSS loaded late (`@import`, bottom `<link>`, async CSS).
- **CSS-in-JS** hydration mismatch (SSR sends HTML, client injects styles late).
- **Dark/light theme** applied via JS after reading `localStorage`.
- Web fonts swapping (`font-display: swap`) causing text reflow (FOUT — related).

## Standard config / commands

### HTML — load critical CSS first

```html
<head>
  <!-- Preconnect to CSS CDN -->
  <link rel="preconnect" href="https://cdn.example.com" crossorigin>

  <!-- Render-blocking but correct: styles before body content -->
  <link rel="stylesheet" href="/assets/main.css">

  <!-- Avoid @import in CSS for critical path — serializes downloads -->
</head>
```

### Inline critical CSS (above-the-fold)

```html
<head>
  <style>
    /* Minimal layout shell: header height, font-size, background */
    body { margin: 0; font-family: system-ui, sans-serif; }
    .hero { min-height: 40vh; }
  </style>
  <link rel="preload" href="/assets/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/assets/main.css"></noscript>
</head>
```

### Theme without flash (SSR or blocking script)

```html
<!-- Inline in <head> BEFORE body — reads preference before paint -->
<script>
  (function () {
    const theme = localStorage.getItem('theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
  })();
</script>
```

```css
:root[data-theme="light"] { --bg: #fff; --fg: #111; }
:root[data-theme="dark"]  { --bg: #111; --fg: #eee; }
body { background: var(--bg); color: var(--fg); }
```

### React / CSS-in-JS (styled-components, Emotion)

```js
// SSR: collect styles on server, inject in <head> before body
// Client: use consistent class names (no hydration mismatch)
```

### Font loading

```css
@font-face {
  font-family: 'Brand';
  src: url('/fonts/brand.woff2') format('woff2');
  font-display: optional; /* or swap with size-adjust fallback */
}
```

### Nginx — cache + HTTP/2 push (legacy) / early hints

```nginx
location /assets/ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}
# Ensure CSS gets correct Content-Type: text/css
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| White page → styled jump | CSS `<link>` at bottom of body | Move stylesheets to `<head>`; inline critical CSS |
| Dark mode flash (light then dark) | Theme JS at end of body | Inline theme script in `<head>`; use `color-scheme` CSS |
| FOUC only on slow 3G | Waterfall: CSS after JS | Preload CSS; reduce JS blocking; split bundles |
| FOUC after deploy only | CDN cache miss / hashed filename mismatch | Verify cache headers; atomic deploys |
| React hydration warning + flash | SSR/client class mismatch | Fix SSR style collection; consistent builds |
| Text jumps when font loads | `font-display: swap` without metrics | Use `size-adjust`, fallback stack, or `optional` |
| FOUC with Tailwind CDN | Full utility CSS loads async | Build CSS at compile time; don't rely on CDN in prod |

## Gotchas

> [!WARNING]
> **`@import` inside CSS** — forces serial fetch; each import blocks the next. Prefer `<link>` tags or bundler imports.

> [!WARNING]
> **`media="print" onload` trick** — non-blocking CSS still causes FOUC for screen; only use for non-critical styles with inline critical CSS covering layout.

> [!WARNING]
> **JS that mutates layout on DOMContentLoaded** — adding classes, showing hidden nav, injecting stylesheets — all cause CLS. Match initial HTML to final state where possible.

> [!WARNING]
> **SPA client-only render** — empty `#root` until JS runs is FOUC-by-design; use SSR/SSG or skeleton in HTML.

## When NOT to use

- **Hiding body with `visibility:hidden` until load** — hurts LCP and accessibility; fix CSS delivery instead.
- **Blocking all JS for style** — overkill; inline tiny theme/critical CSS, async the rest.
- **Aggressive `font-display: block`** — eliminates FOUT but can hide text for seconds on slow networks.

## Related

[[css]] [[scss]] [[Animation]] [[tailwindcss]] [[Nginx]] [[React]]
