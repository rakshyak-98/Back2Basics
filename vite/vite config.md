[[vite internal]] [[vite error]] [[transpiler]]

# Vite config

> `vite.config.*` controls dev server and build — plugins, aliases, env prefix, and mode-specific options via `defineConfig`.

## Interview Relevance

Interviewers want `import.meta.env` + `VITE_` prefix, `command === 'serve'|'build'` branching, and why Vite is esbuild/Rollup-shaped rather than Webpack-shaped.

## Sources

- [Vite — Configuring Vite](https://vitejs.dev/config/) — deep-dive
- [Vite — Env variables](https://vitejs.dev/guide/env-and-mode.html) — overview

## Key Concepts

- **Dev vs build:** native ESM + esbuild transform in dev; Rollup build for production.
- **Env exposure:** only `VITE_`-prefixed vars reach the client via `import.meta.env`.
- **Config as function:** `defineConfig(({ command, mode }) => …)` for conditional setups.
- **Custom file:** `vite --config my-config.js`.

## Technical Details

```bash
vite --config my-config.js
```

```js
export default defineConfig(({ command, mode }) => {
  if (command === "serve") {
    return { server: { port: 5173 } };
  }
  return { build: { sourcemap: true } };
});
```

Environment files load automatically; application code reads `import.meta.env.VITE_*`, not raw `process.env`, in the browser bundle.

## Real-World Applications

Monorepo packages share a base config; apps override aliases and proxy rules for local APIs.

**Example:** API URL differs per mode — `VITE_API_URL` in `.env.development` / `.env.production`.

## Pros/Cons or Trade-offs

- **Pro:** Fast cold start; simple config surface for modern ESM apps.
- **Con:** Webpack-centric mental models (`process.env` everywhere) break until migrated.

## Comparison

- vs Webpack: different env and loader models; Vite optimizes ESM DX.
- vs [[vite internal]]: config is the knobs; internals explain env/runtime wiring.

## Mistakes to Avoid

- Putting secrets in `VITE_` vars (they ship to the browser).
- Expecting server-only `process.env` in client code.
- One giant config without `mode`/`command` splits when needs diverge.
