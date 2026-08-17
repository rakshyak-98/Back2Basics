[[ambient modules]] [[tsconfig]] [[typescript]] [[typescript error]]

# Triple-Slash Directives

> `/// <reference … />` comments pull declaration files or `@types` packages into compilation — legacy wiring; prefer `import` and `tsconfig` `types`/`include`.





## Interview Relevance
Interviewers may mention triple-slash directives to see if you know they are a dependency mechanism for `.d.ts` files, and that modern apps should not sprinkle them when `tsconfig` already controls types.

## Sources
- [TypeScript Handbook — Triple-Slash Directives](https://www.typescriptlang.org/docs/handbook/triple-slash-directives.html) — deep-dive
- [TypeScript Handbook — tsconfig types](https://www.typescriptlang.org/tsconfig#types) — overview

## Core Definition
Triple-slash directives are single-line comments of the form `/// <reference … />` that instruct the compiler to include another file (`path`) or a type package (`types`) as part of the compilation context.

## Key Concepts
- **`reference path`:** include another `.d.ts` or TS file by relative path.
- **`reference types`:** load a package from `@types` / `node_modules` (for example `node`, `vite/client`).
- **Order matters:** earlier references are processed first.
- **Prefer `tsconfig`:** `compilerOptions.types` and `include` usually replace ad-hoc refs.
- **Types only:** directives do not create runtime imports.

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

## Real-World Applications
Generated declaration emit may insert references; Vite templates sometimes keep `/// <reference types="vite/client" />` at the top of `vite-env.d.ts`.

**Example:** Globals appear twice because both a triple-slash and `compilerOptions.types` load `@types/node` — pick one path.

## Pros/Cons or Trade-offs
- **Pro:** Explicit, file-local way to pull declarations in older or generated code.
- **Con:** Scattering refs in application TS obscures the real dependency graph.
- **Con:** `reference types` can load an entire package and pollute globals.

## Comparison
- vs ES `import`: imports are the modern module graph; triple-slash is declaration wiring.
- vs [[tsconfig]] `types`/`include`: central configuration beats per-file refs for apps.
- vs [[ambient modules]]: ambient modules declare shapes; triple-slash decides which declaration files participate.

## Mistakes to Avoid
- Sprinkling directives through application source when `tsconfig` already lists types.
- Fighting generated emit that inserts references without understanding why.
- Assuming a reference creates a runtime dependency — it is types only.
- Using `path` refs instead of fixing `include` for project files.
