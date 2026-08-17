[[tsconfig]] [[typescript types]] [[typescript error]] [[typescript extend types]] [[Descriptive/Javascript]]

# typescript

> TypeScript is JavaScript plus a static type layer erased at compile time — it catches interface mistakes before runtime, not instead of runtime checks.

```txt
        typescript ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask TypeScript to see if you understand erasure (types disappear…

## Sources
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — deep-dive
- [TypeScript — Why TypeScript](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html) — overview
- [Wikipedia — TypeScript](https://en.wikipedia.org/wiki/TypeScript) — overview

## Key Concepts
- **Static contracts:** types describe shapes of values → catch mismatches at compile time.
- **Erasure:** emitted JS has no types → validate untrusted input at boundaries.
- **`tsconfig`:** controls strictness, modules, emit ([[tsconfig]]).
- **Declaration files (`.d.ts`):** types for JavaScript libraries ([[ambient modules]]).
- **Structural typing:** compatibility by shape, not by nominal class name.


- **Core:** TypeScript extends JavaScript with optional static types. The compiler (`tsc`…

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

## Mistakes to Avoid
- **Mistake:** Reaching for `any` to ship — prefer `unknown` and narrow
- **Mistake:** Trusting assertion `as T` as proof — it is unchecked
- **Mistake:** Using numeric `enum` when a string union fits the JSON API better
- **Mistake:** Teaching TypeScript before basic JavaScript values and async
- **Mistake:** Expecting the type system to validate HTTP/JSON without a schema…

## Pros/Cons or Trade-offs
- **Pro:** Catches interface and null mistakes early; better editor navigation.
- **Con:** Types can lie via `as` casts and unsound escape hatches.
- **Con:** Not a substitute for runtime validation of external data.

## Comparison
- vs plain JavaScript: TypeScript adds a compile-time checker; runtime is still JS.
- vs [[typescript types]] / [[typescript extend types]]: this note is the language overview
- vs [[class-transformer]]: class-transformer hydrates runtime instances


### Use cases
- Application codebases typecheck in CI with `tsc --noEmit` while Vite emits bu…

- **Example:** An API handler types `body` as `User` but attackers send missing…
