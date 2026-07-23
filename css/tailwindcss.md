[[css]] [[scss]] [[Nginx]] [[React]] [[Flash of Unstyled Content]]

# Tailwind CSS

> Utility-first CSS framework — compose designs from constrained class names; build step tree-shakes unused utilities for production.

## Mental model

Tailwind is **not** a component library. It generates atomic utility classes (`flex`, `pt-4`, `text-slate-600`) from a config file. At build time, it scans your source files and emits **only used** rules — keeping prod CSS small.

```
Source files ──► Tailwind scanner (content globs)
                      │
                      ▼
              Generated CSS (utilities + @layer base/components)
                      │
                      ▼
              PostCSS pipeline ──► single bundled stylesheet
```

v4 shift: CSS-first config with `@import "tailwindcss"` and `@theme` blocks (vs v3 `tailwind.config.js`).

## Standard config / commands

### Install (Vite + React example)

```bash
npm install tailwindcss @tailwindcss/vite
```

```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite';
export default { plugins: [tailwindcss()] };
```

### Entry CSS (v4)

```css
@import "tailwindcss";

/* Optional: prefix all utilities — avoids collisions with legacy CSS */
/* @import "tailwindcss" prefix(tw); */

@theme {
  --color-brand: #3b82f6;
  --font-sans: "Inter", system-ui, sans-serif;
}

/* Custom utilities in layer */
@layer components {
  .btn-primary {
    @apply rounded-lg bg-brand px-4 py-2 text-white hover:bg-brand/90;
  }
}
```

### v3-style `tailwind.config.js` (still valid in many projects)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: { colors: { brand: '#3b82f6' } } },
  plugins: [],
};
```

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Plugins (v4)

```css
@import "tailwindcss";
@plugin "@tailwindcss/forms";
@plugin "@tailwindcss/typography";
```

### Production build

```bash
npm run build   # Tailwind runs via PostCSS/Vite — verify output CSS size
# Prod CSS typically 5–15 KB gzipped with proper content paths
```

### Nginx — long-cache hashed assets

```nginx
location /assets/ {
  add_header Cache-Control "public, max-age=31536000, immutable";
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Classes have no effect | Class not in scanned `content` paths | Add glob for new folder; rebuild |
| Huge CSS in prod | CDN/play CDN Tailwind or missing purge | Use build pipeline; never `@tailwindcss/browser` in prod |
| "Unknown at rule @tailwind" in editor | IDE doesn't know Tailwind | Install Tailwind CSS IntelliSense; set `css.customData` |
| `@apply` fails on custom class | Order / layer issue | Define in `@layer components`; import order matters |
| Dark mode not working | Wrong strategy (`media` vs `class`) | Set `darkMode: 'class'` + `dark:` variants on `<html>` |
| Styles differ dev vs prod | JIT missed dynamic class string | Use full class names: `text-${color}-500` won't scan — safelist |
| v4 migration broken | Mixed v3 `@tailwind` + v4 `@import` | Pick one version's entry pattern; read upgrade guide |
| Prefix classes ignored | Forgot prefix in JSX | With `prefix(tw)`, use `tw:flex` not `flex` |

## Gotchas

> [!WARNING]
> **Dynamic class names don't purge** — `` `bg-${statusColor}-500` `` won't generate CSS unless every variant is safelisted. Use maps: `{ ok: 'bg-green-500', err: 'bg-red-500' }`.

> [!WARNING]
> **CDN Tailwind in production** — ships entire framework (~300KB+); defeats the purpose. Compile at build time only.

> [!WARNING]
> **`@apply` overuse** — recreates component CSS with harder debugging; prefer utilities in markup or `@layer components` sparingly.

> [!WARNING]
> **Specificity wars** — Tailwind utilities beat most app CSS unless you use `!important` modifier (`!flex`) or layer ordering wrong with legacy [[scss]].

## When NOT to use

- **Email templates** — poor client support for utility-class HTML; use inline styles.
- **Heavy bespoke design system with zero utility markup** — consider CSS modules or tokens-only approach.
- **No build step allowed** — Tailwind v4 still needs compilation; raw CDN is dev/prototype only.

## Related

[[css]] [[scss]] [[Flash of Unstyled Content]] [[Animation]] [[React]]
