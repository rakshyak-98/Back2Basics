[[TypeScript]] [[typescript]] [[tsconfig]]

# typescript error

> TypeScript errors — `TSxxxx` codes from the checker; read the *first* error, fix root cause, avoid `as any` band-aids.

---

## How it works

```txt
edit → tsc → TSxxxx + message + related spans
```

| Code family | Meaning |
|-------------|---------|
| TS2322 | Type not assignable |
| TS2345 | Arg mismatch |
| TS2339 | Property doesn’t exist |
| TS2307 | Cannot find module |
| TS7006 | Implicit `any` |

---


## Configuration and commands

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
| `strictNullChecks` | Surfaces real bugs |
| `skipLibCheck` | Fewer `.d.ts` noise |
| `exactOptionalPropertyTypes` | Stricter optionals |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| TS2307 module | Path / exports / types | Install `@types`; fix resolution |
| TS2322 null | Possibly undefined | Narrow / optional chain |
| Explosion of errors | One bad type | Fix source type |
| IDE only errors | Different TS version | Align workspace TS |
| Error in `.d.ts` | Bad lib | `skipLibCheck` or upgrade |

---


## Steps

1. …


## Verification

```bash
# …
```


## Rollback

1. …


## Gotchas

> [!WARNING]
> **`// @ts-ignore` hides bugs** — prefer `@ts-expect-error` with reason.

> [!WARNING]
> **Error cascades** — one wrong generic can spam hundreds.

> [!WARNING]
> **Build tools swallow types** — run `tsc --noEmit` in CI.

---


## When not to use

- **Silencing with `any`** — quarantine.
- **Disabling strict to green CI** — temporary only with plan.
- **Treating type errors as runtime stack traces** — different layer.

---


## Related

[[tsconfig]] [[typescript]] [[typescript types]] [[ambient modules]]

## Sources

- [Wikipedia — typescript error](https://en.wikipedia.org/wiki/typescript_error)
