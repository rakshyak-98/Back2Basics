[[typescript]] [[typescript types]] [[typescript error]] [[ambient modules]] [[Triple-Slash Directives]]

# tsconfig

> `tsconfig.json` tells the TypeScript compiler which files to include, how strict to check, how modules resolve, and whether to emit JavaScript.

```txt
        tsconfig ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about `tsconfig` to see if you enable `strict`, understand `…

## Sources
- [TypeScript Handbook — tsconfig.json](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html) — deep-dive
- [TypeScript — Compiler Options](https://www.typescriptlang.org/tsconfig) — deep-dive
- [TypeScript Handbook — Modules](https://www.typescriptlang.org/docs/handbook/modules.html) — overview

## Key Concepts
- **Safety flags:** `strict`, `noUncheckedIndexedAccess` → catch null and index bugs early.
- **Module settings:** `module`, `moduleResolution`, `verbatimModuleSyntax` → must match Node or bun…
- **Emit vs check-only:** `noEmit` / `declaration` / `outDir` → CI often typechecks without emitting.
- **Path aliases:** `paths` + `baseUrl` → IDE/tsc only; runtime needs real resolution.
- **Incremental:** `incremental` + `tsBuildInfoFile` → faster rebuilds when cached in CI.


- **Core:** A `tsconfig.json` is the project file for `tsc`: `include`/`exclude` define r…

## Technical Details
```txt
include/exclude → parse → typecheck → emit?
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["node"],
    "tsBuildInfoFile": ".cache/tsbuildinfo"
  },
  "include": ["src"]
}
```

```bash
npx tsc -p tsconfig.json --noEmit
npx tsc -b  # project references
```

| Area | Knobs |
|------|-------|
| Safety | `strict`, `noUncheckedIndexedAccess` |
| Modules | `module`, `moduleResolution`, `verbatimModuleSyntax` |
| Output | `outDir`, `declaration`, `noEmit` |
| DX | `paths`, `baseUrl`, `incremental` |

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t find `@types` | `types`/`typeRoots` too narrow | Remove empty `types: []` or add names |
| Path alias fails at runtime | Only TypeScript knows `paths` | Mirror in bundler or use package exports |
| IDE ≠ CLI errors | Wrong configuration root | Point the editor at the right `tsconfig` |
| Slow CI | No incremental cache | Cache `tsbuildinfo` |
| Emit into the repository | Accidental emit | `noEmit` or clean `outDir` |

## Mistakes to Avoid
- **Mistake:** Treating `paths` as Node resolution
- **Mistake:** Loosening `strict` to silence errors instead of fixing types
- **Mistake:** Mixing app and test `tsconfig` casually until IDE and CLI disagr…
- **Mistake:** Emitting build artifacts into source trees without a clean `outD…

## Pros/Cons or Trade-offs
- **Pro:** One file encodes safety and module policy for the whole project.
- **Con:** `skipLibCheck` speeds CI but can hide broken `.d.ts` issues.
- **Con:** Multiple configs (app / Node / test) confuse editors if the wrong root is used.

## Comparison
- vs command-line flags alone: `tsconfig` is shareable project truth
- vs [[ambient modules]] / [[Triple-Slash Directives]]: prefer `types`/`include` in `tsconfig` over…
- vs bundler configuration: bundler owns runtime emit; `tsc --noEmit` owns type safety in CI.


### Use cases
- Apps use `noEmit: true` with Vite/webpack owning emit

- **Example:** Imports work in the IDE via `paths` but crash in Node
