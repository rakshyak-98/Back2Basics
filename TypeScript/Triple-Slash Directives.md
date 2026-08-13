[[TypeScript]] [[ambient modules]] [[tsconfig]]

# Triple-Slash Directives

> Triple-slash — `/// <reference … />` comments that pull in `.d.ts` or set a module path (legacy; prefer `import` / `tsconfig` includes).

---

## How it works

```ts
/// <reference types="node" />
/// <reference path="./shim.d.ts" />
```

| Directive | Job |
|-----------|-----|
| `path` | Include another file |
| `types` | Package like `@types/node` |
| `lib` | (rare) lib components |

---


## Configuration and commands

```ts
/// <reference types="vite/client" />

// prefer in tsconfig instead:
// "compilerOptions": { "types": ["vite/client"] }
```

| Knob | Why it matters |
|------|----------------|
| Order | Earliest refs process first |
| `types` vs `path` | Package vs relative file |
| `tsconfig` `types` | Often replaces refs |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Types missing in Vite | Client ref | Add vite/client ref or types |
| Duplicate globals | Multiple refs | Deduge via tsconfig types |
| Path not found | Wrong relative | Fix path; use include |

---


## Gotchas

> [!WARNING]
> **Don’t sprinkle in app TS** — use imports/`tsconfig`.

> [!WARNING]
> **`reference types` loads whole package** — can pollute globals.

> [!WARNING]
> **Generated emit may insert them** — don’t fight blindly.

---


## When not to use

- **Modern application code** — ES imports.
- **Controlling `@types` set** — `compilerOptions.types`.
- **Runtime dependency** — it’s types only.

---


## Related

[[ambient modules]] [[tsconfig]] [[typescript]]

## Sources

- [Wikipedia — Triple-Slash Directives](https://en.wikipedia.org/wiki/Triple-Slash_Directives)
