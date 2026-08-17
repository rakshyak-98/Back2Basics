[[vite config]] [[vite error]] [[transpiler]]

# Vite internals

> How Vite wires env and config into the client — `import.meta.env` replaces Webpack-style `process.env` in browser code.





## Interview Relevance
Interviewers ask why `process.env.API_URL` is undefined in Vite apps and how `define` / env prefixes prevent leaking the whole environment.

## Sources
- [Vite — Env Variables and Modes](https://vitejs.dev/guide/env-and-mode.html) — deep-dive
- [Vite — Why Vite](https://vitejs.dev/guide/why.html) — overview

## Key Concepts
- **`import.meta.env`:** typed bag of exposed env + `MODE`, `DEV`, `PROD`, `BASE_URL`.
- **Prefix filter:** default `VITE_` only — intentional safety rail.
- **Dev server:** pre-bundles deps with esbuild; serves source as native ESM.
- **Build:** Rollup bundles for production.

## Technical Details
```js
const apiUrl = import.meta.env.VITE_API_URL;
```

```js
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === "serve") {
    return { /* dev */ };
  }
  return { /* production build */ };
});
```

Do not expect Node’s `process.env` to exist in browser bundles unless you explicitly define replacements (and still avoid shipping secrets).

## Real-World Applications
Feature-flag client builds with `VITE_FEATURE_X=true` per environment; keep private API keys on the server only.

**Example:** Migrating from Webpack `DefinePlugin` — replace `process.env.X` reads with `import.meta.env.VITE_X`.

## Pros/Cons or Trade-offs
- **Pro:** Fast refresh and clear client/server env boundary.
- **Con:** SSR/Node code paths still need careful split from browser code.

## Comparison
- vs Webpack: different env injection and dev serving model.
- vs [[vite config]]: internals explain the mechanism behind the knobs.

## Mistakes to Avoid
- Prefixing secrets with `VITE_`.
- Mixing SSR `process.env` assumptions into client components.
- Assuming `.env` changes apply without restarting the dev server.
