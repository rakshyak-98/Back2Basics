[[css]] [[Animation]]

# scss

> SCSS in 2026: still valuable for **design tokens, mixins, and partials** — but lean on native CSS where it caught up — **Sass team + modern CSS spec**.

---

## Mental model

SCSS = CSS + variables, nesting, mixins, functions, `@use` modules. Build step compiles to plain CSS.

```txt
2026 stack options:
  Vite/Webpack + sass-embedded (dart-sass)
  PostCSS for autoprefixer + nesting polyfill (optional)
  CSS @layer + @property for some former SCSS jobs
```

**Migration reality:** greenfield may ship CSS modules + Tailwind; legacy codebases still run large SCSS — know both maintenance and sunset patterns.

**Module system (`@use` / `@forward`)** replaced `@import` (deprecated) — one namespace per file, no duplicate global pollution.

---

## Standard config / commands

### File layout (design system)

```scss
// tokens/_colors.scss
$color-primary: #2563eb;
$color-danger: #dc2626;

// tokens/_spacing.scss
$space-unit: 0.25rem;
@function space($n) { @return $n * $space-unit; }

// _mixins.scss
@mixin focus-ring {
  outline: 2px solid $color-primary;
  outline-offset: 2px;
}

// components/_button.scss
@use '../tokens/colors' as c;
@use '../mixins' as m;

.btn-primary {
  background: c.$color-primary;
  &:focus-visible { @include m.focus-ring; }
}
```

### `@use` vs old `@import`

```scss
// ✅ Modern
@use 'tokens/colors' as *;   // or namespaced: colors.$primary
@forward 'tokens/colors';    // re-export from index

// ❌ Deprecated — duplicate CSS, global scope leaks
// @import 'tokens/colors';
```

### Mixins worth keeping (no native equivalent)

```scss
@mixin truncate($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

@mixin respond-to($breakpoint) {
  @if $breakpoint == md {
    @media (min-width: 768px) { @content; }
  }
}
```

### Prefer native CSS now

```css
/* Custom properties — runtime themable, no build for toggle */
:root {
  --color-primary: #2563eb;
  --space-4: 1rem;
}

/* Nesting (widely supported 2024+) */
.card {
  padding: var(--space-4);
  & .title { font-weight: 600; }
}

/* @layer for cascade control */
@layer reset, components, utilities;
```

### Build (Vite example)

```bash
npm i -D sass-embedded
# vite.config: css.preprocessorOptions.scss.additionalData optional for global @use
```

```json
"scripts": {
  "build:css": "sass src/styles:dist/css --style=compressed --no-source-map"
}
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate CSS in bundle | Leftover `@import` | Migrate to `@use`; single entry `@forward` barrel |
| Undefined variable | Namespace | `@use 'tokens/colors' as c;` → `c.$primary` |
| Deprecation warnings CI fail | dart-sass 1.80+ | Replace `@import`, `/` division → `math.div()` |
| Huge CSS output | `@extend` chains | Prefer mixins or utility classes |
| Dark mode tokens wrong | Compile-time `$vars` only | Move theme to CSS custom properties |
| Slow builds | `@use` graph + source maps | `--quiet-deps`; limit `additionalData` glob |

---

## Gotchas

> [!WARNING]
> **`@extend` across files** — unpredictable selector bloat and ordering bugs; prefer mixins or utility classes.

> [!WARNING]
> **Sass variables can't change at runtime** — theme switching needs CSS variables, not `$primary-dark`.

> [!WARNING]
> **`!default` override order** — depends on `@use` load order; document token override chain.

> [!WARNING]
> **Tailwind + SCSS duplication** — pick source of truth for spacing/color; don't define both.

---

## When NOT to use

- **New micro-frontends with Tailwind/CSS-in-JS** — SCSS adds build complexity without team buy-in.
- **Runtime theming / user accent colors** — CSS custom properties only.
- **One-off static landing** — plain CSS or utility framework faster than token architecture.

---

## Related

[[Animation]] · [[css]] · [[JavaScript]]
