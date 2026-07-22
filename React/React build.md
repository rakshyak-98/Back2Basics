[[React project config]] [[Optimizing performance]] [[source map]] [[SWC]] [[Deployment/vercel deployment]]

# React build

> Turn TS/JSX into optimized static assets — dev server vs production bundle, env injection, source maps — **Vite / CRA / Next docs**.

---

## Mental model

```txt
Source (TSX, CSS) → bundler (Vite/webpack/esbuild) → chunks + hashed filenames → CDN
Dev:  ESM + HMR (fast refresh)
Prod: minify, tree-shake, code-split, asset hash
```

| Tool | Typical stack |
|------|---------------|
| **Vite** | esbuild pre-bundle + Rollup prod ([[SWC]] optional) |
| **Next.js** | Webpack/Turbopack + RSC pipeline |
| **CRA (legacy)** | webpack — migrate to Vite |

Build output must match **runtime env**: `import.meta.env.VITE_*` baked at build time, not read dynamically from shell at runtime (unless SSR injects).

---

## Standard config / commands

### Vite production build

```bash
npm run build          # → dist/
npm run preview        # local static serve of prod build
```

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    sourcemap: true,           // prod debug — see [[source map]]
    rollupOptions: {
      output: { manualChunks: { vendor: ["react", "react-dom"] } },
    },
  },
});
```

### Analyze bundle

```bash
npx vite-bundle-visualizer
# or webpack-bundle-analyzer for Next/webpack
```

### Environment variables (Vite)

```bash
# .env.production
VITE_API_URL=https://api.example.com
```

```typescript
const url = import.meta.env.VITE_API_URL; // string; validate at startup
```

### Next.js

```bash
next build && next start
# ANALYZE=true next build  (with @next/bundle-analyzer)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `undefined` API URL in prod | Env not prefixed `VITE_` | Rename; rebuild |
| White screen prod only | Thrown error minified away | Enable sourcemap; Sentry |
| Huge main chunk | No route split | `React.lazy` + dynamic import |
| Stale assets after deploy | CDN cache | Hash filenames (default Vite) |
| Works dev, fails build | TS errors stricter | `tsc -b` in CI |
| CORS on static host | API separate origin | Proxy in dev; CDN rules prod |

---

## Gotchas

> [!WARNING]
> **Secrets in `VITE_*`** — embedded in client bundle; never API keys server-only.

> [!WARNING]
> **Dev ≠ prod** — test `npm run build && preview` before release.

---

## When NOT to use

- **SSR/RSC app** — don't treat as pure SPA build; use framework pipeline (Next).
- **Library package** — publish ESM/CJS via tsup/rollup, not SPA `index.html` build.

---

## Related

[[React project config]] · [[source map]] · [[SWC]] · [[Deployment/vercel deployment]] · [[Optimizing performance]]
