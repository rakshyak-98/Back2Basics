[[React build]] [[polyfills]] [[source map]] [[javascript engine]] [[metro bundler]]

# SWC (Speedy Web Compiler)

> SWC (Speedy Web Compiler) — TS/JSX/TSX → SWC parse/transform → ES target JS

```txt
        SWC (Speedy Web Co ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **SWC (Speedy Web Compiler)** to see if you understand wha…

## Sources
- [SWC — Getting started](https://swc.rs/docs/getting-started) — deep-dive
- [Wikipedia — SWC](https://en.wikipedia.org/wiki/SWC) — overview

## Key Concepts
- **Used for:** Used for:
- **Syntax lowering:** (optional chaining, JSX, TypeScript strip) - **React Fast Refresh** transform…
- **Not a:** Not a full **polyfill** layer

## Technical Details
```txt
TS/JSX/TSX  →  SWC parse/transform  →  ES target JS
                     ↓
              optional minify (esbuild-like speed)
```

- **Syntax lowering:** (optional chaining, JSX, TypeScript strip)
- **React Fast Refresh:** transforms (Next)
- **Jest:** via `@swc/jest` instead of ts-jest/babel-jest

- Not a full **polyfill** layer

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

- Next uses SWC internally

### Jest

```javascript
module.exports = {
  transform: { "^.+\\.(t|j)sx?$": ["@swc/jest"] },
};
```

## Mistakes to Avoid
- **Mistake:** **Exotic Babel macros** (styled-components babel plugin, etc.)

> [!WARNING]
> **Type checking** — SWC strips types; still run `tsc --noEmit` in CI.
- **Mistake:** **Babel plugin missing:** check SWC unsupported syntax plugin
- **Mistake:** **Different output vs Babel:** check Edge semantic diff
- **Mistake:** **JSX runtime error:** check Classic vs automatic
- **Mistake:** **Decorators fail:** check Stage mismatch
- **Mistake:** **Slower than expected:** check Falling back to Babel

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (SWC (Speedy Web Compiler) — TS/JSX/TSX → SWC parse/transform → ES target JS).
- **Con / when not:** **Heavy custom Babel plugin chain**
- **Con / when not:** **Non-JS languages**

## Comparison
- vs [[React build]]: know when each applies


### Use cases
- In production APIs and tooling, **SWC** shows up whenever teams ship Node/JS …
