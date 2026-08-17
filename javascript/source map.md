[[React build]] [[SWC]] [[javascript engine]] [[React project configuration]] [[Security/content security policy]]

# Source map

> Source map — production ships app.js (one line, mangled names). Browser loads optional app.js.map:

```txt
        Source map ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Source map** to see if you understand what it does opera…

## Sources
- [Source Map specification](https://tc39.es/ecma426/) — deep-dive
- [Wikipedia — source map](https://en.wikipedia.org/wiki/source_map) — overview

## Key Concepts
- **Production ships:** Production ships `app.js` (one line, mangled names)
- **Works with:** Works with [[SWC]], Babel, TypeScript, Sass


- **Core:** Production ships `app.js` (one line, mangled names)

## Technical Details
- Production ships `app.js` (one line, mangled names).
- Browser loads optional `app.js.map`:

```txt
generated line/col  →  original file, line, col, symbol names
```

```txt
Error at app.js:1:48291  →  DevTools shows Checkout.tsx:42 payInvoice()
```

| Mode | Tradeoff |
|------|----------|
| `sourcemap: true` (prod) | Debuggable prod; **don't expose publicly** without auth |
| `hidden-source-map` | Sentry upload only; no browser fetch |
| `inline` | Embedded; huge bundles |
| Dev default | Fast rebuild; full maps |

- Works with [[SWC]], Babel, TypeScript, Sass

### Vite

```typescript
export default defineConfig({
  build: {
    sourcemap: true, // or 'hidden' for error trackers
  },
});
```

- Output: `dist/assets/index-abc123.js` + `index-abc123.js.map`

### Upload to Sentry (hidden maps)

```bash
npx @sentry/cli sourcemaps upload --release "$GIT_SHA" ./dist
```

- Set `build.sourcemap: 'hidden'` so maps aren't served to users.

### TypeScript

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSources": true
  }
}
```

- Bundler consumes TS maps or generates its own

### Verify in DevTools

- Settings → enable source maps → trigger error → stack links to original file.

## Mistakes to Avoid
- **Mistake:** **Public source maps leak source**
- **Mistake:** **Map mismatch after hotfix**
- **Mistake:** **Stack shows minified names:** check Map not loaded
- **Mistake:** **Wrong file/line:** check Outdated map vs bundle
- **Mistake:** **Maps 404:** check CDN omit `.map`
- **Mistake:** **Huge deploy size:** check inline maps
- **Mistake:** **CSP blocks:** check `connect-src` / map fetch

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Source map — production ships app.js (one line, mangled names). Browser loads op…).
- **Con / when not:** **Public library npm package**
- **Con / when not:** **Tiny internal scripts**

## Comparison
- vs [[React build]]: know when each applies


### Use cases
- In production APIs and tooling, **source map** shows up whenever teams ship N…
