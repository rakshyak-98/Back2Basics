[[tsconfig]] [[typescript types]] [[typescript error]] [[typescript extend types]] [[Descriptive/Javascript]]

# typescript

> TypeScript is JavaScript plus a static type layer erased at compile time — it catches interface mistakes before runtime, not instead of runtime checks.





## Interview Relevance
Interviewers ask TypeScript to see if you understand erasure (types disappear at runtime), when to use `unknown` vs `any`, and why boundary validation (Zod, etc.) still matters beside the type checker.

## Sources
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — deep-dive
- [TypeScript — Why TypeScript](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html) — overview
- [Wikipedia — TypeScript](https://en.wikipedia.org/wiki/TypeScript) — overview

## Core Definition
TypeScript extends JavaScript with optional static types. The compiler (`tsc`) typechecks `.ts` sources and emits plain JavaScript; type annotations are erased and never enforce behavior at runtime by themselves.

## Key Concepts
- **Static contracts:** types describe shapes of values → catch mismatches at compile time.
- **Erasure:** emitted JS has no types → validate untrusted input at boundaries.
- **`tsconfig`:** controls strictness, modules, emit ([[tsconfig]]).
- **Declaration files (`.d.ts`):** types for JavaScript libraries ([[ambient modules]]).
- **Structural typing:** compatibility by shape, not by nominal class name.

## Technical Details
```txt
.ts ──typecheck──► errors?
    ──emit──► .js (types erased)
```

| Piece | Job |
|-------|-----|
| Types | Static contracts |
| `tsconfig` | Strictness / module mode |
| Declaration `.d.ts` | Types for JS libs |

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
|------|----------------|
| `strict` | Real safety |
| `moduleResolution` | Match Node or bundler |
| `noEmit` | Typecheck-only in CI |

| Symptom | Check | Fix |
|---------|-------|-----|
| Works in JS, fails `tsc` | Implicit any / null | Fix types; enable strict gradually |
| Runtime still blows | Types lie / `as` casts | Validate at boundaries |
| Slow typecheck | Huge `any` graphs | Project references; simpler types |
| Dual package hazard | CJS/ESM mix | Fix `module` / `exports` |

## Real-World Applications
Application codebases typecheck in CI with `tsc --noEmit` while Vite emits bundles; libraries ship `.d.ts` beside JS for consumers.

**Example:** An API handler types `body` as `User` but attackers send missing fields — add Zod (or similar) at the boundary; TypeScript alone will not reject the payload at runtime.

## Pros/Cons or Trade-offs
- **Pro:** Catches interface and null mistakes early; better editor navigation.
- **Con:** Types can lie via `as` casts and unsound escape hatches.
- **Con:** Not a substitute for runtime validation of external data.

## Comparison
- vs plain JavaScript: TypeScript adds a compile-time checker; runtime is still JS.
- vs [[typescript types]] / [[typescript extend types]]: this note is the language overview; those cover the type system tools.
- vs [[class-transformer]]: class-transformer hydrates runtime instances; TypeScript types alone do not.

## Mistakes to Avoid
- Reaching for `any` to ship — prefer `unknown` and narrow.
- Trusting assertion `as T` as proof — it is unchecked.
- Using numeric `enum` when a string union fits the JSON API better.
- Teaching TypeScript before basic JavaScript values and async.
- Expecting the type system to validate HTTP/JSON without a schema parser.
