[[React build]] [[SWC]] [[javascript engine]] [[React project configuration]] [[Security/content security policy]]

# Source map

> Source map — production ships app.js (one line, mangled names). Browser loads optional app.js.map:





## Interview Relevance
Interviewers probe **Source map** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Source Map specification](https://tc39.es/ecma426/) — deep-dive
- [Wikipedia — source map](https://en.wikipedia.org/wiki/source_map) — overview

## Core Definition
Production ships `app.js` (one line, mangled names). Browser loads optional `app.js.map`:

## Key Concepts
- Production ships `app.js` (one line, mangled names). Browser loads optional `app.js.map`:
- Works with [[SWC]], Babel, TypeScript, Sass — anything that emits `//# sourceMappingURL=`.

## Technical Details
Production ships `app.js` (one line, mangled names). Browser loads optional `app.js.map`:

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

Works with [[SWC]], Babel, TypeScript, Sass — anything that emits `//# sourceMappingURL=`.

### Vite

```typescript
export default defineConfig({
  build: {
    sourcemap: true, // or 'hidden' for error trackers
  },
});
```

Output: `dist/assets/index-abc123.js` + `index-abc123.js.map`

### Upload to Sentry (hidden maps)

```bash
npx @sentry/cli sourcemaps upload --release "$GIT_SHA" ./dist
```

Set `build.sourcemap: 'hidden'` so maps aren't served to users.

### TypeScript

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSources": true
  }
}
```

Bundler consumes TS maps or generates its own — avoid double-confusion; usually let Vite own production maps.

### Verify in DevTools

Settings → enable source maps → trigger error → stack links to original file.

## Real-World Applications
In production APIs and tooling, **source map** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Public source maps leak source** — business logic visible; use hidden maps + private symbol server; **Map mismatch after hotfix** — always tag maps with release version (git SHA).

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Source map — production ships app.js (one line, mangled names). Browser loads op…).
- **Con / when not:** **Public library npm package** — ship types + docs, not full source maps to consumers.
- **Con / when not:** **Tiny internal scripts** — readable unminified code may suffice.

## Comparison
vs [[React build]]: know when each applies — do not treat them as interchangeable. vs [[SWC]]: know when each applies — do not treat them as interchangeable. vs [[javascript engine]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Public source maps leak source** — business logic visible; use hidden maps + private symbol server.
- **Map mismatch after hotfix** — always tag maps with release version (git SHA).
- **Stack shows minified names:** check Map not loaded; fix: `sourceMappingURL` comment; deploy `.map`
- **Wrong file/line:** check Outdated map vs bundle; fix: Rebuild; maps CI artifact tied to release
- **Maps 404:** check CDN omit `.map`; fix: Upload maps to Sentry; block public `.map`
- **Huge deploy size:** check inline maps; fix: External `.map` files
- **CSP blocks:** check `connect-src` / map fetch; fix: Allow error tracker domain only
