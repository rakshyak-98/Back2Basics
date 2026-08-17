[[Operating System]] [[runtime]] [[interpreter]] [[linker]] [[OS program]] [[system call]]

# Runtime Environment

> The runtime environment is everything that executes your program after the kernel starts it — dynamic linker, libc, thread library, GC, and language builtins.

```txt
        Runtime Environmen ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Distinguishes kernel `execve` from user-space runtime (ld.so, JVM, Go runtime)

## Sources
- Levine, *Linkers and Loaders* — deep-dive
- Linux `ld.so(8)`, `ldd(1)` manual pages — deep-dive

## Key Concepts
- **After kernel handoff:** CRT/`_start`, dynamic linking, then `main` or VM bootstrap.
- **Dynamic linker:** loads `.so`, relocates ([[linker]] at load time).
- **Language runtime:** exceptions, GC, goroutine/thread schedulers.
- **Container ABI:** musl vs glibc — mismatch breaks binaries.

## Technical Details
| Piece | Role |
|-------|------|
| Dynamic linker | Loads `.so`, relocates |
| libc | [[system call]] wrappers, malloc |
| Language runtime | Exceptions, GC, goroutine scheduler |
| [[interpreter]] | Executes non-native code paths |

- For a C binary: kernel `execve` → **ld.so** maps libc → `_start` → `main`.
- For JVM: native `java` stub loads bytecode, JIT, and standard library.

- See [[runtime]] for a shorter cross-reference

## Mistakes to Avoid
- **Mistake:** Shipping a glibc-linked binary into a musl-only image
- **Mistake:** Blaming the kernel for missing `.so`
- **Mistake:** Confusing “runtime” (execution env) with “run time” (wall-clock …

## Pros/Cons or Trade-offs
- **Rich runtime:** faster development, GC, batteries included
- **Minimal runtime:** smaller images; more work falls on the application.
- **Trade-off:** static binary vs shared libc updates.

## Comparison
- vs [[OS program]]: program is the on-disk/in-memory image
- vs [[interpreter]]: interpreter is one runtime style for non-native code.


### Use cases
- Distroless/minimal images must still ship a compatible runtime
