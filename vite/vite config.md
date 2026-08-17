[[vite internal]] [[vite error]] [[transpiler]]

# Vite config

> `vite.config.*` controls dev server and build — plugins, aliases, env prefix, and mode-specific options via `defineConfig`.

```txt
        Vite config ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want `import.meta.env` + `VITE_` prefix, `command === 'serve'|'b…

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

- Environment files load automatically

## Mistakes to Avoid
- **Mistake:** Putting secrets in `VITE_` vars (they ship to the browser)
- **Mistake:** Expecting server-only `process.env` in client code
- **Mistake:** One giant config without `mode`/`command` splits when needs dive…

## Pros/Cons or Trade-offs
- **Pro:** Fast cold start; simple config surface for modern ESM apps.
- **Con:** Webpack-centric mental models (`process.env` everywhere) break until migrated.

## Comparison
- vs Webpack: different env and loader models; Vite optimizes ESM DX.
- vs [[vite internal]]: config is the knobs; internals explain env/runtime wiring.


### Use cases
- Monorepo packages share a base config

- **Example:** API URL differs per mode
