[[vite config]] [[vite error]] [[transpiler]]

# Vite internals

> How Vite wires env and config into the client — `import.meta.env` replaces Webpack-style `process.env` in browser code.

```txt
        Vite internals ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask why `process.env.API_URL` is undefined in Vite apps and how …

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

- Do not expect Node’s `process.env` to exist in browser bundles unless you exp…

## Mistakes to Avoid
- **Mistake:** Prefixing secrets with `VITE_`
- **Mistake:** Mixing SSR `process.env` assumptions into client components
- **Mistake:** Assuming `.env` changes apply without restarting the dev server

## Pros/Cons or Trade-offs
- **Pro:** Fast refresh and clear client/server env boundary.
- **Con:** SSR/Node code paths still need careful split from browser code.

## Comparison
- vs Webpack: different env injection and dev serving model.
- vs [[vite config]]: internals explain the mechanism behind the knobs.


### Use cases
- Feature-flag client builds with `VITE_FEATURE_X=true` per environment

- **Example:** Migrating from Webpack `DefinePlugin`
