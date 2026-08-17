[[Animation]] [[tailwindcss]] [[Flash of Unstyled Content]] [[CSS property]] [[Javascript]]

# scss

> SCSS (Sassy CSS) extends CSS with variables, nesting, mixins, and `@use` modules — a build step compiles it to plain CSS the browser understands.

```txt
        scss ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about SCSS to see if you know `@use` versus deprecated `@imp…

## Sources
- [Sass Docs — `@use`](https://sass-lang.com/documentation/at-rules/use/) — deep-dive
- [Sass Docs — Breaking change: `@import`](https://sass-lang.com/documentation/breaking-changes/import/) — overview
- [MDN — Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) — overview

## Key Concepts
- **Compile step:** `.scss` → `.css` via Vite/`sass-embedded` or the Sass CLI
- **`@use` / `@forward`:** modern module system with namespaces → replaces global `@import` pollution.
- **Mixins / functions:** reusable chunks and calculations → keep what native CSS still lacks.
- **Sass `$variables` vs CSS `var()`:** Sass values are build-time; custom properties are runtime-themeable.
- **Migration pressure:** native nesting, `@layer`, and `@property` cover many former SCSS jobs in gree…


- **Core:** SCSS is a stylesheet language compiled by Dart Sass (or compatible tools) int…

## Technical Details
```txt
2026 stack options:
  Vite/Webpack + sass-embedded (dart-sass)
  PostCSS for autoprefixer (optional)
  Native CSS nesting / @layer for some former SCSS jobs
```

### File layout

```scss
// tokens/_colors.scss
$color-primary: #2563eb;

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
  &:focus-visible {
    @include m.focus-ring;
  }
}
```

### `@use` vs deprecated `@import`

```scss
// Modern
@use 'tokens/colors' as *;
@forward 'tokens/colors';

// Deprecated — duplicate CSS, global scope leaks
// @import 'tokens/colors';
```

### Mixins still useful

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
```

### Prefer native CSS for runtime themes

```css
:root {
  --color-primary: #2563eb;
  --space-4: 1rem;
}

.card {
  padding: var(--space-4);
  & .title {
    font-weight: 600;
  }
}
```

```bash
npm i -D sass-embedded
# or: sass src/styles:dist/css --style=compressed --no-source-map
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate CSS in bundle | Leftover `@import` | Migrate to `@use` / `@forward` |
| Undefined variable | Namespace | `c.$primary` after `@use … as c` |
| Deprecation warnings fail CI | dart-sass 1.80+ | Replace `@import`; use `math.div()` |
| Huge output | `@extend` chains | Prefer mixins or utilities |
| Dark mode wrong | Compile-time `$vars` only | Move theme to CSS custom properties |

## Mistakes to Avoid
- **Mistake:** Keeping `@import` in new code — migrate to `@use` / `@forward`
- **Mistake:** Using `@extend` across files until selector graphs become unread…
- **Mistake:** Defining the same spacing/color tokens in both SCSS and Tailwind…

## Pros/Cons or Trade-offs
- **Pro:** Strong authoring structure (modules, mixins) for large shared stylesheets.
- **Con:** Extra build dependency and mental model beside native CSS.
- **Con:** Sass variables cannot switch at runtime for user themes — need `var(--*)`.

## Comparison
- vs [[tailwindcss]]: Tailwind constrains design via utilities
- vs plain CSS: native nesting and custom properties close the gap


### Use cases
- Large design systems still organize tokens and component sheets in SCSS

- **Example:** A component library `@forward`s tokens from `index.scss` so apps…
