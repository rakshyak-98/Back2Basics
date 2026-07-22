[[compiler/transpiler]] [[compiler/compile time]] [[Operating System/Runtime Environment]]

# Compiler

> Translates source in a high-level language to machine code or bytecode for a target platform — portability via abstraction over CPU ISAs.

## Mental model

Source → **frontend** (parse, AST) → **optimizer** → **backend** (codegen for x86/ARM/WASM). Different hardware (x86, ARM, RISC-V) needs different instruction streams; compilers hide that. Interpreted languages still often compile to bytecode (JVM, CPython `.pyc`) — JIT bridges compile time and runtime.

```
source.c → compiler (clang) → object file → linker → executable
source.ts → tsc → JavaScript → (optional) V8 JIT
```

## Standard config / commands

### C/C++ (typical)

```bash
gcc -O2 -Wall -Wextra -c file.c -o file.o
gcc file.o -o app
clang -std=c17 -g -fsanitize=address file.c -o app_asan   # debug memory
```

### Go / Rust (single toolchain)

```bash
go build -o app ./cmd/app
rustc main.rs -O
```

### Inspect output

```bash
file app                    # ELF binary type
objdump -d app | head       # disassembly peek
ldd app                     # shared libs (dynamic link)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Undefined reference | Link stage | Add `-l` library; include `.o` |
| Works on dev, SIGILL on prod | CPU features | `-march` too new; build on oldest target |
| Optimizer bug | `-O0` vs `-O2` | Bisect flags; UB in C (sanitizers) |
| Wrong arch binary | `file bin` | Cross-compile `GOOS`/`GOARCH` or toolchain prefix |
| Huge binary | Debug symbols | `strip` or `-s`; split debug info |

## Gotchas

> [!WARNING]
> **Undefined behavior in C** — optimizer assumes rules; "works in debug" classic.
>
> **Cross-compile needs sysroot/libs** — not just compiler binary.
>
> **Reproducible builds** — timestamps and paths embed in binary unless `-trimpath`/SOURCE_DATE_EPOCH.

## When NOT to use

- Don't hand-write assembly for whole app unless extreme hot path — maintainability cost.
- Don't `-O3` blindly on latency-sensitive code without profiling — can regress.

## Related

[[compiler/compile time]] [[compiler/transpiler]] [[compiler/library file]] [[golang/go build]]
