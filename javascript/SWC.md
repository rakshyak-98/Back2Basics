[[React build]] [[polyfills]] [[source map]] [[javascript engine]] [[metro bundler]]

# SWC (Speedy Web Compiler)

> SWC (Speedy Web Compiler) — TS/JSX/TSX → SWC parse/transform → ES target JS

## Interview Relevance

Interviewers probe **SWC (Speedy Web Compiler)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [SWC — Getting started](https://swc.rs/docs/getting-started) — deep-dive
- [Wikipedia — SWC](https://en.wikipedia.org/wiki/SWC) — overview

## Key Concepts

- Used for:
- **Syntax lowering** (optional chaining, JSX, TypeScript strip) - **React Fast Refresh** transforms (Next) - **Jest** via `@swc/jest` instead of ts-jest/babel-jest
- Not a full **polyfill** layer — pair with [[polyfills]] for missing runtime APIs.

## Technical Details

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

Next uses SWC internally — custom Babel only if `.babelrc` present (disables SWC for that application).

### Jest

```javascript
module.exports = {
  transform: { "^.+\\.(t|j)sx?$": ["@swc/jest"] },
};
```

## Real-World Applications

In production APIs and tooling, **SWC** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Exotic Babel macros** (styled-components babel plugin, etc.) — verify SWC plugin exists before migrating.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (SWC (Speedy Web Compiler) — TS/JSX/TSX → SWC parse/transform → ES target JS).
- **Con / when not:** **Heavy custom Babel plugin chain** — migration cost may exceed build time savings.
- **Con / when not:** **Non-JS languages** — SWC is JS/TS focused; use appropriate compiler (Rust, Go) for those.

## Comparison

vs [[React build]]: know when each applies — do not treat them as interchangeable. vs [[polyfills]]: know when each applies — do not treat them as interchangeable. vs [[source map]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Exotic Babel macros** (styled-components babel plugin, etc.) — verify SWC plugin exists before migrating.

> [!WARNING]
> **Type checking** — SWC strips types; still run `tsc --noEmit` in CI.
- **Babel plugin missing:** check SWC unsupported syntax plugin; fix: Keep Babel for that file or macro
- **Different output vs Babel:** check Edge semantic diff; fix: Integration test; pin @swc/core version
- **JSX runtime error:** check Classic vs automatic; fix: `react.runtime: "automatic"`
- **Decorators fail:** check Stage mismatch; fix: Enable experimental in swc config
- **Slower than expected:** check Falling back to Babel; fix: Remove `.babelrc` in Next
