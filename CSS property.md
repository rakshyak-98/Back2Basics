- If you change the `<p>` element’s `display` property to `inline`, the `::first-letter` pseudo-element **will not work** because `::first-letter` only applies to block-level elements.

### Multipline ellipsis
```css
h1 {
  display: -webkit-box;
  -webkit-line-clamp: 3;      /* Limit to 3 lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

```

## at-rules
- they are not style selectors, but directives that control how CSS is parsed and applied.
```css
@import "file.css"; /* bring external css */
@media (max-width: 768px) {}; /* apply rules under conditions */
@font-face {}; /* define custom fonts */
@keyframe fade {}; /* define animations */
@supports; /* feature queries (if browser supports property) */
@layer; /* define cascade layers (CSS Cascade Level 5) */
@page; /* page box settings for print */
```

> [!NOTE]
> `@import` must appear before all other rules in a CSS file, if placed after normal rules, it's ignored.
> Browser sees `@import` -> sends an extra HTTP request to fetch the stylesheet

> [!INFO]
> `@import "tailwindcss"` -> tailwindcss registers itself as a PostCSS plugin. The `tailwindcss` package in `node_modules` exposes an entry point. When PostCSS parses `@import "tailwindcss"` the PostCSS import plugin + tailwindcss plugin intercept the directive.
