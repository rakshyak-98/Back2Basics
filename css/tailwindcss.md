[[scss]] [[Flash of Unstyled Content]] [[Animation]] [[css image]] [[React]] [[Nginx]]

# Tailwind CSS

> Tailwind CSS is a utility-first framework — you compose designs from constrained class names, and the build step emits only the utilities your source files use.

```txt
        Tailwind CSS ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about Tailwind to probe purge/content scanning, why dynamic …

## Sources
- [Tailwind CSS Docs](https://tailwindcss.com/docs) — overview
- [Tailwind CSS Docs — Functions and directives](https://tailwindcss.com/docs/functions-and-directives) — deep-dive
- [Wikipedia — Tailwind CSS](https://en.wikipedia.org/wiki/Tailwind_CSS) — overview

## Key Concepts
- **Not a component library:** you build UI from utilities (or thin `@layer` components)
- **Content scanning:** only class names found in scanned files are emitted → dynamic string concaten…
- **v4 CSS-first:** `@import "tailwindcss"` and `@theme` in CSS (versus v3 `tailwind.config.js` +…
- **`@apply`:** pulls utilities into custom classes
- **Plugins:** forms, typography, etc. extend the theme via `@plugin` (v4) or `plugins` (v3).


- **Core:** Tailwind generates atomic utility classes (`flex`, `pt-4`, `text-slate-600`) …

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

## Mistakes to Avoid
- **Mistake:** Shipping the Tailwind CDN / browser build to production
- **Mistake:** Building class names with string concatenation
- **Mistake:** Overusing `@apply` until you reinvent a bespoke CSS framework on…

## Pros/Cons or Trade-offs
- **Pro:** Fast UI iteration and small production CSS when scanning works.
- **Con:** Markup can get verbose; teams need naming conventions for repeated patterns.
- **Con:** Poor fit for email HTML or environments with no build step.

## Comparison
- vs [[scss]]: SCSS is a preprocessor with variables/mixins
- vs CSS modules: modules scope local class names; Tailwind shares a global utility vocabulary.


### Use cases
- Product UIs and design systems use Tailwind for speed and consistency

- **Example:** A [[React]] dashboard maps status to full class names (`bg-green…
