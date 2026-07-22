[[React build]] [[SWC]] [[javascript engine]] [[React project config]] [[Security/content security policy]]

# Source map

> Maps **bundled/minified code** back to original TS/JS sources for stack traces and debugging — **Source Map v3 spec**.

---

## Mental model

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

---

## Standard config / commands

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

Bundler consumes TS maps or generates its own — avoid double-confusion; usually let Vite own prod maps.

### Verify in DevTools

Settings → enable source maps → trigger error → stack links to original file.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stack shows minified names | Map not loaded | `sourceMappingURL` comment; deploy `.map` |
| Wrong file/line | Outdated map vs bundle | Rebuild; maps CI artifact tied to release |
| Maps 404 | CDN omit `.map` | Upload maps to Sentry; block public `.map` |
| Huge deploy size | inline maps | External `.map` files |
| CSP blocks | `connect-src` / map fetch | Allow error tracker domain only |

---

## Gotchas

> [!WARNING]
> **Public source maps leak source** — business logic visible; use hidden maps + private symbol server.

> [!WARNING]
> **Map mismatch after hotfix** — always tag maps with release version (git SHA).

---

## When NOT to use

- **Public library npm package** — ship types + docs, not full source maps to consumers.
- **Tiny internal scripts** — readable unminified code may suffice.

---

## Related

[[SWC]] · [[React build]] · [[React project config]] · [[javascript engine]] · [[Security/content security policy]]
