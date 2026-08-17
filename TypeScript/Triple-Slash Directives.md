[[ambient modules]] [[tsconfig]] [[typescript]] [[typescript error]]

# Triple-Slash Directives

> `/// <reference … />` comments pull declaration files or `@types` packages into compilation — legacy wiring; prefer `import` and `tsconfig` `types`/`include`.

```txt
        Triple-Slash Direc ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers may mention triple-slash directives to see if you know they are …

## Sources
- [TypeScript Handbook — Triple-Slash Directives](https://www.typescriptlang.org/docs/handbook/triple-slash-directives.html) — deep-dive
- [TypeScript Handbook — tsconfig types](https://www.typescriptlang.org/tsconfig#types) — overview

## Key Concepts
- **`reference path`:** include another `.d.ts` or TS file by relative path.
- **`reference types`:** load a package from `@types` / `node_modules` (for example `node`, `vite/clie…
- **Order matters:** earlier references are processed first.
- **Prefer `tsconfig`:** `compilerOptions.types` and `include` usually replace ad-hoc refs.
- **Types only:** directives do not create runtime imports.


- **Core:** Triple-slash directives are single-line comments of the form `/// <reference …

## Technical Details
```ts
/// <reference types="node" />
/// <reference path="./shim.d.ts" />
```

| Directive | Job |
|-----------|-----|
| `path` | Include another file |
| `types` | Package like `@types/node` |
| `lib` | (rare) built-in lib components |

```ts
/// <reference types="vite/client" />

// prefer in tsconfig instead:
// "compilerOptions": { "types": ["vite/client"] }
```

| Knob | Why it matters |
|------|----------------|
| Order | Earliest refs process first |
| `types` vs `path` | Package vs relative file |
| `tsconfig` `types` | Often replaces scattered refs |

| Symptom | Check | Fix |
|---------|-------|-----|
| Types missing in Vite | Client types not loaded | Add `vite/client` via ref or `types` |
| Duplicate globals | Multiple refs | Deduplicate via `tsconfig` `types` |
| Path not found | Wrong relative path | Fix path; use `include` |

## Mistakes to Avoid
- **Mistake:** Sprinkling directives through application source when `tsconfig`…
- **Mistake:** Fighting generated emit that inserts references without understa…
- **Mistake:** Assuming a reference creates a runtime dependency
- **Mistake:** Using `path` refs instead of fixing `include` for project files

## Pros/Cons or Trade-offs
- **Pro:** Explicit, file-local way to pull declarations in older or generated code.
- **Con:** Scattering refs in application TS obscures the real dependency graph.
- **Con:** `reference types` can load an entire package and pollute globals.

## Comparison
- vs ES `import`: imports are the modern module graph; triple-slash is declaration wiring.
- vs [[tsconfig]] `types`/`include`: central configuration beats per-file refs for apps.
- vs [[ambient modules]]: ambient modules declare shapes


### Use cases
- Generated declaration emit may insert references

- **Example:** Globals appear twice because both a triple-slash and `compilerOp…
