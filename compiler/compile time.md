[[compiler/compiler]] [[Operating System/runtime]] [[compiler/transpiler]]

# Compile time

> Phase before program runs — parsing, type checking, optimization, and codegen; errors here prevent broken binaries from shipping.

## Mental model

**Compile time** = while compiler/transpiler/build tool runs. **Runtime** = while program executes. Decisions at compile time are fixed (types, const generics, `#ifdef`); runtime handles user input, network, dynamic dispatch (virtual methods, `interface{}`, reflection).

| Aspect | Compile time | Runtime |
|--------|--------------|---------|
| Errors | Syntax, types, missing imports | Null deref, timeout, logic bugs |
| Cost | Paid once per build | Paid every execution |
| Knowledge | Source + declared types | Live data, env, I/O |

## Standard config / commands

### Catch errors early

```bash
# TypeScript — no emit if types fail
tsc --noEmit

# Go — compile only
go build ./...

# Rust — strict by default
cargo check          # fast typecheck
cargo clippy         # lints
```

### Compile-time configuration

```c
// C preprocessor
#ifdef DEBUG
  #define LOG(x) fprintf(stderr, x)
#else
  #define LOG(x)
#endif
```

```go
// Go build tags
//go:build integration
```

```ts
// TS — const enum inlined at compile time
const enum Dir { Up, Down }
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Build fails CI, passes locally | Toolchain version | Pin Node/Go/Rust in CI |
| Slow builds | Incremental broken | Cache artifacts; split modules |
| Type error cascade | One root error | Fix first error; rerun |
| `#ifdef` wrong branch | `-D` flags | Align Makefile/CMake defines |
| Works in IDE, fails tsc | stricter CI `tsconfig` | Align `strict` flags |

## Gotchas

> [!WARNING]
> **Template/macro errors** — line numbers lie; preprocessed output helps (`gcc -E`).
>
> **Conditional compilation drift** — prod build missing `FEATURE_X` silently.
>
> **Transpiler ≠ typecheck** — Babel alone doesn't typecheck TypeScript.

## When NOT to use

- Don't push runtime validation-only languages to "compile time" metaphors without static checker (add TypeScript/mypy).
- Don't over-use macros/templates — debug at compile time becomes nightmare.

## Related

[[compiler/compiler]] [[compiler/transpiler]] [[Operating System/Runtime Environment]]
