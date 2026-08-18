[[TypeScript]] [[tsconfig]] [[javascript]]

# typescript

> TypeScript — JavaScript plus a type layer erased at compile time; catches interface mistakes before runtime.

## Mental model

**Say it in one breath:** You annotate shapes; `tsc` (or bundler) typechecks and emits JS. Types don’t exist at runtime unless you add schemas (Zod) or emit decorators metadata.

```txt
.ts ──typecheck──► errors?
    ──emit──► .js (types erased)
```

| Piece | Job |
| --- | --- |
| Types | Static contracts |
| `tsconfig` | Strictness / module mode |
| Declaration `.d.ts` | Types for JS libs |

## Standard config / commands

```bash
npm i -D typescript
npx tsc --init
npx tsc -p tsconfig.json --noEmit
```

```ts
type User = { id: string; email: string }
function greet(u: User) {
  return u.email
}
```

| Knob | Why it matters |

| `strict` | Real safety |
| --- | --- |
| `moduleResolution bundler` | Modern apps |
| `noEmit` | Typecheck-only in CI |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Works in JS, fails `tsc` | Implicit any / null | Fix types; enable strict gradually |
| Runtime still blows | Types lie / `as` casts | Validate at boundaries |
| Slow typecheck | Huge `any` graphs | Project references; simpler types |
| Dual package hazard | CJS/ESM mix | Fix `module`/`exports` |

## Gotchas

> [!WARNING]
> **`any` disables the point** — prefer `unknown` + narrow.

> [!WARNING]
> **Assertion `as T` is unchecked** — trust ≠ proof.

> [!WARNING]
> **Enum pitfalls** — prefer string unions for most APIs.

## When NOT to use

- **10-line script** — plain JS fine.
- **Runtime validation needs** — add Zod/io-ts; TS alone isn’t enough.
- **Teaching JS basics** — learn values first.

## Related

[[tsconfig]] [[typescript types]] [[typescript error]] [[javascript]]
