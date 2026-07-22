[[React build]] [[polyfills]] [[source map]] [[javascript engine]] [[metro bundler]]

# SWC (Speedy Web Compiler)

> **Rust-based** transpiler/minifier — Babel-compatible subset at much lower latency — powers Next.js, Vite (optional), Deno — **SWC project docs**.

---

## Mental model

```txt
TS/JSX/TSX  →  SWC parse/transform  →  ES target JS
                     ↓
              optional minify (esbuild-like speed)
```

Used for:

- **Syntax lowering** (optional chaining, JSX, TypeScript strip)
- **React Fast Refresh** transforms (Next)
- **Jest** via `@swc/jest` instead of ts-jest/babel-jest

Not a full **polyfill** layer — pair with [[polyfills]] for missing runtime APIs.

| vs Babel | SWC |
|----------|-----|
| Speed | 10–20× faster typical |
| Plugin ecosystem | Smaller; some Babel plugins missing |
| Config | `.swcrc` / bundler integration |

---

## Standard config / commands

### Vite (@vitejs/plugin-react-swc)

```bash
npm i -D @vitejs/plugin-react-swc
```

```typescript
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
});
```

### .swcrc (standalone CLI)

```json
{
  "$schema": "https://json.schemastore.org/swcrc",
  "jsc": {
    "parser": { "syntax": "typescript", "tsx": true },
    "transform": { "react": { "runtime": "automatic" } },
    "target": "es2022"
  },
  "module": { "type": "es6" },
  "minify": true
}
```

```bash
npx swc src -d dist
```

### Next.js (default)

Next uses SWC internally — custom Babel only if `.babelrc` present (disables SWC for that app).

### Jest

```javascript
module.exports = {
  transform: { "^.+\\.(t|j)sx?$": ["@swc/jest"] },
};
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Babel plugin missing | SWC unsupported syntax plugin | Keep Babel for that file or macro |
| Different output vs Babel | Edge semantic diff | Integration test; pin @swc/core version |
| JSX runtime error | Classic vs automatic | `react.runtime: "automatic"` |
| Decorators fail | Stage mismatch | Enable experimental in swc config |
| Slower than expected | Falling back to Babel | Remove `.babelrc` in Next |

---

## Gotchas

> [!WARNING]
> **Exotic Babel macros** (styled-components babel plugin, etc.) — verify SWC plugin exists before migrating.

> [!WARNING]
> **Type checking** — SWC strips types; still run `tsc --noEmit` in CI.

---

## When NOT to use

- **Heavy custom Babel plugin chain** — migration cost may exceed build time savings.
- **Non-JS languages** — SWC is JS/TS focused; use appropriate compiler (Rust, Go) for those.

---

## Related

[[React build]] · [[polyfills]] · [[source map]] · [[metro bundler]] · [[javascript engine]]
