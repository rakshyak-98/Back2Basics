[[typescript]] [[tsconfig]] [[typescript types]] [[ambient modules]]

# typescript error

> `TSxxxx` diagnostics from the type checker — read the first error, fix the root type, and avoid `as any` or blanket `@ts-ignore` band-aids.





## Interview Relevance
Interviewers watch how you debug TypeScript errors: narrow unions, install missing types, align TypeScript versions, and keep `tsc --noEmit` in CI so the bundler cannot hide type failures.

## Sources
- [TypeScript Handbook — Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) — deep-dive
- [TypeScript — Error codes (playground / messages)](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) — overview
- [TypeScript Compiler Options](https://www.typescriptlang.org/tsconfig) — overview

## Core Definition
A TypeScript error is a static diagnostic (`TSxxxx`) produced when values, arguments, or imports do not match declared types. Fixing the earliest error often collapses cascades from one bad generic or missing module.

## Key Concepts
- **Assignability (`TS2322`):** value not assignable to target type.
- **Argument mismatch (`TS2345`):** call site types disagree with parameters.
- **Missing property (`TS2339`):** property does not exist on the type.
- **Cannot find module (`TS2307`):** resolution or missing `@types` / declarations.
- **Implicit `any` (`TS7006`):** under `noImplicitAny` / `strict`.
- **Narrowing over asserting:** guards and control flow beat `as` casts.

## Technical Details
```txt
edit → tsc → TSxxxx + message + related spans
```

| Code family | Meaning |
|-------------|---------|
| TS2322 | Type not assignable |
| TS2345 | Argument mismatch |
| TS2339 | Property does not exist |
| TS2307 | Cannot find module |
| TS7006 | Implicit `any` |

```bash
npx tsc --noEmit --pretty false | head
npx tsc --pretty --traceResolution  # module issues
```

```ts
// narrow instead of assert
function len(x: string | null) {
  if (x == null) return 0
  return x.length
}
```

| Knob | Why it matters |
|------|----------------|
| `strictNullChecks` | Surfaces real null bugs |
| `skipLibCheck` | Fewer noisy `.d.ts` errors |
| `exactOptionalPropertyTypes` | Stricter optionals |

| Symptom | Check | Fix |
|---------|-------|-----|
| TS2307 module | Path / exports / types | Install `@types`; fix resolution |
| TS2322 null | Possibly undefined | Narrow / optional chain |
| Explosion of errors | One bad type | Fix the source type first |
| IDE-only errors | Different TypeScript version | Align workspace TypeScript |
| Error in `.d.ts` | Bad lib | `skipLibCheck` or upgrade package |

## Real-World Applications
CI runs `tsc --noEmit` so Vite/webpack green builds cannot ship broken types; developers fix the first `TS2322` instead of silencing hundreds of follow-ons.

**Example:** `TS2307` after adding a package — install matching `@types/*` or add an [[ambient modules]] shim, do not cast the import to `any`.

## Pros/Cons or Trade-offs
- **Pro:** Failures at compile time beat production type confusion.
- **Con:** Cascades from one bad generic can look like hundreds of unrelated errors.
- **Con:** `skipLibCheck` trades noise for occasional missed declaration bugs.

## Comparison
- vs runtime exceptions: type errors are static; they do not replace input validation at boundaries.
- vs ESLint: lint catches style/patterns; `tsc` enforces the type system.
- vs `@ts-ignore` / `any`: both silence the checker — prefer `@ts-expect-error` with a reason or proper narrowing.

## Mistakes to Avoid
- Using `// @ts-ignore` without a plan — prefer `@ts-expect-error` and fix soon.
- Disabling `strict` to green CI permanently.
- Treating type errors like stack traces — different layer; start from the first diagnostic.
- Letting the bundler be the only “build” — always keep `tsc --noEmit` in CI.
