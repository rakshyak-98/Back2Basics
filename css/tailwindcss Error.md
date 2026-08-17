[[tailwindcss]] [[scss]] [[Flash of Unstyled Content]]

# tailwindcss Error

> Tailwind CSS v4 errors like “Cannot apply unknown utility class” usually mean `@apply` ran in an isolated stylesheet without `@reference` — not that the utility was deleted.





## Interview Relevance
Interviewers use this failure to see if you understand Tailwind v4’s CSS-first model: utilities are not globally visible to CSS modules / Vue / Svelte `<style>` blocks unless you `@reference` the theme entry.

## Sources
- [Tailwind CSS Docs — Functions and directives (`@reference`)](https://tailwindcss.com/docs/functions-and-directives#reference-directive) — deep-dive
- [Tailwind CSS Docs — Upgrade guide (`@apply` with Vue/Svelte/CSS modules)](https://tailwindcss.com/docs/upgrade-guide#using-apply-with-vue-svelte-or-css-modules) — overview
- [GitHub — tailwindcss#15778 (unknown utility / `@apply`)](https://github.com/tailwindlabs/tailwindcss/issues/15778) — overview

## Core Definition
In v4, stylesheets bundled separately from the main Tailwind entry do not automatically see theme tokens or utilities; `@reference` imports that context for `@apply` / `@variant` without duplicating CSS output.

## Key Concepts
- **Symptom:** `[plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class w-3` (or any utility) while asking about `@reference`.
- **Cause:** `@apply` in a CSS module, component `<style>`, or secondary sheet without theme context.
- **Fix:** `@reference "../app.css";` (your Tailwind entry) or `@reference "tailwindcss";` for defaults only.
- **Paths:** `@reference` paths are relative to the file that contains the directive.
- **Prefer less `@apply`:** utilities in markup avoid this class of build errors.

## Technical Details
Main entry (once):

```css
/* app.css */
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
}
```

Isolated stylesheet / CSS module:

```css
@reference "../app.css";
/* or: @reference "tailwindcss"; for default theme only */

.card-title {
  @apply text-lg font-bold text-brand;
}
```

Vue / Svelte style block:

```html
<style>
  @reference "../../app.css";
  h1 {
    @apply text-2xl font-bold;
  }
</style>
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Unknown utility on valid class | File is a CSS module / SFC style | Add `@reference` to Tailwind entry |
| Custom token unknown | Theme only in main file | `@reference` that file, not bare `"tailwindcss"` |
| Huge duplicated CSS | Used `@import` of main sheet | Use `@reference`, not a second full import |
| Class works in HTML, fails in `@apply` | Isolation of stylesheet | Same — wire `@reference` |

## Real-World Applications
Design-system CSS modules and Vue SFCs that wrap utilities with `@apply` for component classes hit this immediately after a v3 → v4 upgrade.

**Example:** Migrating `Button.module.css` that `@apply`s `px-4 py-2` fails until `@reference "../../styles/app.css";` is added at the top.

## Pros/Cons or Trade-offs
- **Pro:** `@reference` keeps component styles able to `@apply` without shipping Tailwind twice.
- **Con:** Deep relative paths to the entry file are brittle — aliases or less `@apply` help.
- **Con:** Overusing `@apply` recreates a custom CSS layer that is harder to debug than utilities in markup.

## Comparison
- vs [[tailwindcss]] setup: the framework note covers scanning and themes; this note is the isolated-`@apply` failure mode.
- vs unknown class at runtime (no styles): that is usually a content-path / scanner miss, not `@reference`.

## Mistakes to Avoid
- Re-`@import`ing the full Tailwind entry into every module — duplicates CSS.
- Assuming v3 global `@apply` behavior still holds in v4 CSS modules.
- Treating “unknown utility” as “Tailwind is broken” before checking isolation and `@reference`.
