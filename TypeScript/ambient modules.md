<!-- note-strategy: operational -->
[[TypeScript]] [[typescript]] [[Triple-Slash Directives]]

# ambient modules

> Ambient modules — `declare module` / `.d.ts` that describe JS libraries TypeScript can’t see types for.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Ambient decls invent types for existing JS. Global (`declare var`) versus module (`declare module 'pkg'`). Prefer DefinitelyTyped or the package’s own types when available.

```txt
import 'pkg' ──needs──► node_modules/pkg/*.d.ts  or  declare module 'pkg'
```

| Form | Use |
|------|-----|
| `declare module 'x'` | Untyped package |
| `declare global` | Globals / augmentation |
| `export {}` | Force file to be a module |

---

## Standard config / commands

```ts
// types/shim.d.ts
declare module 'untyped-lib' {
  export function doThing(x: string): number
}

declare global {
  interface Window {
    APP_CONFIG: { api: string }
  }
}
export {}
```

| Knob | Why it matters |
|------|----------------|
| `typeRoots` | Where ambient packs live |
| `allowJs` + checkJs | Type existing JS |
| Package `types` field | Official entry |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Could not find declaration | Untyped pkg | `@types/*` or shim |
| Shim ignored | Outside include | Add to `include`/`typeRoots` |
| Duplicate identifier | Double globals | Narrow scope; modules |
| Wrong shapes | Stale shim | Sync with runtime |

---

## Gotchas

> [!WARNING]
> **Ambient ≠ implementing** — runtime still must provide the value.

> [!WARNING]
> **Wildcard `declare module '*'`** — hides missing deps.

> [!WARNING]
> **Global pollution** — prefer module forms.

---

## When NOT to use

- **Package already ships types** — don’t override casually.
- **Your own TS code** — normal exports.
- **Runtime validation** — still need Zod/etc.

---

## Related

[[Triple-Slash Directives]] [[tsconfig]] [[typescript error]]
