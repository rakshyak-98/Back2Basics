[[compiler/compiler]] [[compiler/compile time]] [[javascript/metro bundler]]

# Transpiler

> Source-to-source translator — modern syntax down-levelled for older runtimes; runs at **build time**, not in user's browser (usually).

## Mental model

A **compiler** often targets machine code/bytecode; a **transpiler** targets another high-level language (TS→JS, ES2022→ES5). Developer runs it locally or in CI; deploy artifact is the output. Bundlers (Webpack, esbuild, Vite) chain transpile + bundle + minify.

```
author TS/JSX → Babel/SWC/tsc → deploy JS → browser/V8
```

## Standard config / commands

### Babel (classic)

```bash
npm i -D @babel/core @babel/preset-env @babel/preset-typescript
```

```json
{
  "presets": [
    ["@babel/preset-env", { "targets": ">0.5%, not dead" }],
    "@babel/preset-typescript"
  ]
}
```

### TypeScript compiler

```bash
npx tsc --target ES2020 --module ESNext --outDir dist
```

### SWC / esbuild (faster, less plugin ecosystem)

```bash
npx esbuild src/index.ts --bundle --outfile=dist/index.js --target=es2018
```

### Webpack integration

```js
module: {
  rules: [{ test: /\.tsx?$/, use: 'ts-loader' }]  // or babel-loader
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Syntax error in old browser | Build target | Lower `@babel/preset-env` targets |
| Missing polyfill | `core-js` | `useBuiltIns: 'usage'` or manual import |
| TS types ignored | Using Babel only | Add `tsc --noEmit` or `fork-ts-checker` |
| Huge bundle | Full polyfill | Target modern browsers; analyze bundle |
| Source maps wrong | `devtool` setting | `source-map` in prod selectively |

## Gotchas

> [!WARNING]
> **Ship transpiled code, not raw TS** — Node still often runs TS via ts-node in dev only.
>
> **Double transpile** — Babel + tsc both transforming = slow/conflicts.
>
> **Decorators/experimental** — stage mismatches break silently across versions.

## When NOT to use

- Don't transpile if targets are evergreen-only (internal tools) — ship native ES2022.
- Don't transpile on the server per request — always prebuild in CI.

## Related

[[compiler/compiler]] [[compiler/compile time]] [[NodeJS/node package json]] [[css/tailwindcss]]
