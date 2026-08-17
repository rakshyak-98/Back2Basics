[[typescript]] [[tsconfig]] [[Triple-Slash Directives]] [[typescript error]] [[typescript extend types]]

# ambient modules

> `declare module` and `.d.ts` files describe JavaScript libraries TypeScript cannot see types for — they declare shapes; they do not implement runtime code.





## Interview Relevance
Interviewers ask about ambient modules to see if you can shim untyped packages, augment globals safely, and avoid wildcard `declare module '*'` that hides missing dependencies.

## Sources
- [TypeScript Handbook — Modules — ambient modules](https://www.typescriptlang.org/docs/handbook/modules.html) — overview
- [TypeScript Handbook — Declaration Files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html) — deep-dive
- [TypeScript Handbook — Global .d.ts / modules](https://www.typescriptlang.org/docs/handbook/declaration-files/templates/module-d-ts.html) — deep-dive

## Core Definition
An ambient module is a type-only declaration (`declare module 'pkg'`, package `.d.ts`, or `declare global`) that tells the checker the shape of a value that already exists at runtime from JavaScript or the environment.

## Key Concepts
- **`declare module 'x'`:** types for an untyped package import.
- **`declare global`:** add to `Window` or other globals — keep scoped.
- **`export {}`:** force a file to be a module so augmentations apply correctly.
- **`typeRoots` / `types`:** where ambient packs load from ([[tsconfig]]).
- **Package `types` field:** official entry for shipped declarations.

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

## Real-World Applications
Legacy npm packages without types get a small `shim.d.ts`; browser apps augment `Window` for injected configuration.

**Example:** `TS2307` on `import 'legacy-sdk'` — add `@types/legacy-sdk` or a local `declare module 'legacy-sdk'`, and keep the shim inside `include`.

## Pros/Cons or Trade-offs
- **Pro:** Unlocks typed imports for JS libraries without rewriting them.
- **Con:** Ambient declarations can drift from real runtime APIs.
- **Con:** Global pollution and wildcards hide missing dependencies.

## Comparison
- vs normal TypeScript exports: your own TS code should use real exports, not ambient stubs.
- vs [[Triple-Slash Directives]]: prefer `tsconfig` `types`/`include` over scattering `/// <reference />`.
- vs [[typescript extend types]] module augmentation: augmentation patches existing modules; ambient modules introduce types for modules that had none.

## Mistakes to Avoid
- Thinking ambient equals implementing — runtime must still provide the value.
- `declare module '*'` wildcards that silence missing packages.
- Overriding a package that already ships accurate types.
- Using ambient declarations as a substitute for runtime validation.
