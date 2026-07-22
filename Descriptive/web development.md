[[javascript]] [[css/Animation]] [[Nginx/nginx SPA deployment]] [[Rendering performance/SEO]]

# Web development

> Building for browsers — HTML parse, script loading, render path, and delivery constraints — **browser architecture + Core Web Vitals mindset**.

## Mental model

Browser pipeline for a typical page:

```
HTML bytes → parser → DOM
CSS bytes  → parser → CSSOM
        DOM + CSSOM → render tree → layout → paint → composite
JS: can block parse (sync script), defer until parse done, or async fetch
```

**Main thread** owns DOM, layout, paint, and most JS. Long tasks jank UX — see [[Rendering performance/INP]].

## Standard config / commands

### Script loading (`async` vs `defer`)

```html
<!-- Blocks parse + execute immediately when downloaded -->
<script src="legacy.js"></script>

<!-- Fetch parallel, execute after HTML parsed (order preserved) -->
<script defer src="app.js"></script>

<!-- Fetch parallel, execute ASAP when ready (order NOT preserved) -->
<script async src="analytics.js"></script>

<!-- ES modules — defer by default -->
<script type="module" src="app.js"></script>
```

| Attribute | Parse blocked? | Execute when | Order |
|-----------|----------------|--------------|-------|
| (none) | Yes | Downloaded | Sequential |
| `defer` | No | After parse | Yes |
| `async` | No | Downloaded | No |
| `type=module` | No | After parse | Yes |

### Critical rendering path hygiene

```html
<link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin>
<link rel="stylesheet" href="/app.css">  <!-- render-blocking by design -->
```

### Modern stack defaults

- **Framework:** React/Vue/Svelte — hydrate or SSR for [[Rendering performance/SEO]]
- **Bundler:** Vite/esbuild — code split routes
- **Deploy:** CDN + [[Nginx/nginx SPA deployment]] or edge (Vercel)

### Accessibility baseline

Ship [[Descriptive/WCAG (Web Content Accessibility Guidelines)]] **AA** on interactive flows from day one.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank page until JS loads | Sync script in `<head>` | `defer` or move to body end |
| FOUC / unstyled flash | CSS late | Critical CSS inline or preload |
| Hydration mismatch (SSR) | Server HTML ≠ client render | Fix random IDs/dates; `suppressHydrationWarning` last resort |
| Works in Chrome, broken Safari | API gap / date parsing | Polyfill or feature detect — [[Descriptive/JavaScript/Polyfilling]] |
| LCP slow | Hero image unoptimized | `fetchpriority="high"`, WebP/AVIF, dimensions set |

## Gotchas

> [!WARNING]
> **Third-party scripts** (ads, tags) often inject blocking sync scripts — sandbox or load after consent.

- **`document.write`** in async scripts can destroy DOM — banned in modern perf guides.
- **CSP** ([[Security/content security policy]]) breaks inline scripts unless nonce/hash.
- **Mobile Safari** ITP limits storage — don't rely on long-lived `localStorage` for auth.
- **`100vh`** includes mobile URL bar — use `dvh` where supported.

## When NOT to use

- Don't SSR every dashboard widget — SPA + client fetch is fine behind login.
- Avoid reinventing bundler/security headers — platform defaults (Vercel, Cloudflare) first.

## Related

[[javascript]] [[css/Animation]] [[Rendering performance/layout]] [[Rendering performance/SEO]] [[Descriptive/WCAG (Web Content Accessibility Guidelines)]]
