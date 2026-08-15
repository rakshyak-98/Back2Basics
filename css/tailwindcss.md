[[scss]] [[Flash of Unstyled Content]] [[Animation]] [[css image]] [[React]] [[Nginx]]

# Tailwind CSS

> Tailwind CSS is a utility-first framework — you compose designs from constrained class names, and the build step emits only the utilities your source files use.

## Interview Relevance

Interviewers ask about Tailwind to probe purge/content scanning, why dynamic class strings fail, v3 versus v4 configuration, and when utilities beat (or lose to) CSS modules / [[scss]].

## Sources

- [Tailwind CSS Docs](https://tailwindcss.com/docs) — overview
- [Tailwind CSS Docs — Functions and directives](https://tailwindcss.com/docs/functions-and-directives) — deep-dive
- [Wikipedia — Tailwind CSS](https://en.wikipedia.org/wiki/Tailwind_CSS) — overview

## Core Definition

Tailwind generates atomic utility classes (`flex`, `pt-4`, `text-slate-600`) from a theme; a scanner (content globs or v4 automatic detection) keeps production CSS small by omitting unused rules.

## Key Concepts

- **Not a component library:** you build UI from utilities (or thin `@layer` components) — no opinionated Button package required.
- **Content scanning:** only class names found in scanned files are emitted → dynamic string concatenation breaks generation.
- **v4 CSS-first:** `@import "tailwindcss"` and `@theme` in CSS (versus v3 `tailwind.config.js` + `@tailwind` layers).
- **`@apply`:** pulls utilities into custom classes — useful sparingly; needs `@reference` in isolated sheets (see [[tailwindcss Error]]).
- **Plugins:** forms, typography, etc. extend the theme via `@plugin` (v4) or `plugins` (v3).

## Technical Details

```txt
Source files ──► Tailwind scanner
                      │
                      ▼
              Generated utilities + @layer CSS
                      │
                      ▼
              Bundler / PostCSS ──► stylesheet
```

### Install (Vite + React)

```bash
npm install tailwindcss @tailwindcss/vite
```

```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite'
export default { plugins: [tailwindcss()] }
```

### Entry CSS (v4)

```css
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --font-sans: "Inter", system-ui, sans-serif;
}

@layer components {
  .btn-primary {
    @apply rounded-lg bg-brand px-4 py-2 text-white hover:bg-brand/90;
  }
}
```

### v3-style configuration (many existing apps)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: { colors: { brand: '#3b82f6' } } },
  plugins: [],
}
```

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

```bash
npm run build   # verify output CSS size — often ~5–15 KB gzipped when scanned well
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Classes do nothing | Content paths / scanner | Include the folder; rebuild |
| Huge CSS in production | CDN / browser build | Compile at build time only |
| `@apply` unknown utility | Isolated stylesheet | [[tailwindcss Error]] — add `@reference` |
| Dark mode broken | `media` vs `class` strategy | Set class strategy + `dark:` on `<html>` |
| Dev ≠ production styles | Dynamic class strings | Use complete class names or safelist |
| Prefix ignored | Prefixed install | Use `tw:flex` (etc.) consistently |

## Real-World Applications

Product UIs and design systems use Tailwind for speed and consistency; hashed CSS assets get long-cache headers on [[Nginx]] or a CDN.

**Example:** A [[React]] dashboard maps status to full class names (`bg-green-500`) instead of `` `bg-${color}-500` `` so the scanner emits the rules.

## Pros/Cons or Trade-offs

- **Pro:** Fast UI iteration and small production CSS when scanning works.
- **Con:** Markup can get verbose; teams need naming conventions for repeated patterns.
- **Con:** Poor fit for email HTML or environments with no build step.

## Comparison

- vs [[scss]]: SCSS is a preprocessor with variables/mixins; Tailwind is a constrained utility system with a scanner.
- vs CSS modules: modules scope local class names; Tailwind shares a global utility vocabulary.

## Mistakes to Avoid

- Shipping the Tailwind CDN / browser build to production — defeats tree-shaking and invites [[Flash of Unstyled Content]].
- Building class names with string concatenation — the scanner will miss them.
- Overusing `@apply` until you reinvent a bespoke CSS framework on top of Tailwind.
