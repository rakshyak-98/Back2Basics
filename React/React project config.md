[[React build]] [[Typescript with react]] [[NodeJS/node package json]]

# React project config

> TypeScript, Vite, path aliases, env typing — **boring correct setup** so IDE and CI agree — **Vite + TS handbook**.

---

## Mental model

Config layers:

```txt
tsconfig.json     → typecheck rules, paths, JSX
vite.config.ts    → dev server, aliases, plugins
.env.*            → build-time public vars (VITE_)
eslint/prettier    → lint in CI
```

Goal: **one import style** (`@/features/...`), strict enough TS to catch prod bugs, env vars validated once at boot.

---

## Standard config / commands

### Ambient types (`vite-env.d.ts`)

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_ENV: "development" | "staging" | "production";
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

Requires `@types/react`, `@types/node` in devDependencies.

### tsconfig (Vite React)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src", "vite-env.d.ts"]
}
```

### Vite alias (match paths)

```typescript
import path from "node:path";
export default defineConfig({
  resolve: { alias: { "@": path.resolve(__dirname, "src") } },
});
```

### Validate env at startup

```typescript
const api = import.meta.env.VITE_API_URL;
if (!api) throw new Error("VITE_API_URL missing");
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Cannot find module `@/` | tsconfig paths only | Mirror alias in vite.config |
| `import.meta.env` any | Missing vite/client ref | Add `vite-env.d.ts` |
| Types work in IDE, fail CI | `tsc` not run | `"build": "tsc -b && vite build"` |
| Node API in browser bundle | Wrong tsconfig types | `"types": []` or split tsconfig |
| Env undefined prod | Not set in CI | Inject at build; document in README |

---

## Gotchas

> [!WARNING]
> **Triple-slash refs don't replace installing `@types/*`** — both needed.

> [!WARNING]
> **Strict false** — saves time once, costs weeks in nullable bugs.

---

## When NOT to use

- **Monorepo packages** — per-package tsconfig + project references, not one giant paths map.
- **Next.js** — use `next-env.d.ts` and `NEXT_PUBLIC_*` instead of Vite env pattern.

---

## Related

[[React build]] · [[Typescript with react]] · [[source map]] · [[SWC]] · [[NodeJS/node package json]]
