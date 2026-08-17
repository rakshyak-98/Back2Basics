[[typescript]] [[tsconfig]] [[Triple-Slash Directives]] [[typescript error]] [[typescript extend types]]

# ambient modules

> `declare module` and `.d.ts` files describe JavaScript libraries TypeScript cannot see types for — they declare shapes; they do not implement runtime code.

```txt
        ambient modules ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about ambient modules to see if you can shim untyped package…

## Sources
- [TypeScript Handbook — Modules — ambient modules](https://www.typescriptlang.org/docs/handbook/modules.html) — overview
- [TypeScript Handbook — Declaration Files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html) — deep-dive
- [TypeScript Handbook — Global .d.ts / modules](https://www.typescriptlang.org/docs/handbook/declaration-files/templates/module-d-ts.html) — deep-dive

## Key Concepts
- **`declare module 'x'`:** types for an untyped package import.
- **`declare global`:** add to `Window` or other globals — keep scoped.
- **`export {}`:** force a file to be a module so augmentations apply correctly.
- **`typeRoots` / `types`:** where ambient packs load from ([[tsconfig]]).
- **Package `types` field:** official entry for shipped declarations.


- **Core:** An ambient module is a type-only declaration (`declare module 'pkg'`, package…

## Technical Details
```txt
import 'pkg' ──needs──► node_modules/pkg/*.d.ts  or  declare module 'pkg'
```

| Form | Use |
|------|-----|
| `declare module 'x'` | Untyped package |
| `declare global` | Globals / augmentation |
| `export {}` | Force file to be a module |

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
| `allowJs` + `checkJs` | Type existing JS |
| Package `types` field | Official entry |

| Symptom | Check | Fix |
|---------|-------|-----|
| Could not find declaration | Untyped package | `@types/*` or shim |
| Shim ignored | Outside `include` | Add to `include`/`typeRoots` |
| Duplicate identifier | Double globals | Narrow scope; use modules |
| Wrong shapes | Stale shim | Sync with runtime behavior |

## Mistakes to Avoid
- **Mistake:** Thinking ambient equals implementing
- **Mistake:** `declare module '*'` wildcards that silence missing packages
- **Mistake:** Overriding a package that already ships accurate types
- **Mistake:** Using ambient declarations as a substitute for runtime validation

## Pros/Cons or Trade-offs
- **Pro:** Unlocks typed imports for JS libraries without rewriting them.
- **Con:** Ambient declarations can drift from real runtime APIs.
- **Con:** Global pollution and wildcards hide missing dependencies.

## Comparison
- vs normal TypeScript exports: your own TS code should use real exports, not ambient stubs.
- vs [[Triple-Slash Directives]]: prefer `tsconfig` `types`/`include` over scattering `/// <referen…
- vs [[typescript extend types]] module augmentation: augmentation patches existing modules


### Use cases
- Legacy npm packages without types get a small `shim.d.ts`

- **Example:** `TS2307` on `import 'legacy-sdk'`
