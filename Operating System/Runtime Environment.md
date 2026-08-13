[[Operating System]] [[runtime]] [[interpreter]] [[linker]] [[OS program]]

# Runtime Environment

> The runtime environment is everything that executes your program after the kernel starts it — dynamic linker, libc, thread library, GC, and language builtins.

For a C binary: kernel `execve` → **ld.so** maps libc and resolves symbols → `_start` → `main`. For JVM: native `java` stub loads bytecode, JIT, and standard library.

## Components

| Piece | Role |
|-------|------|
| Dynamic linker | Loads `.so`, relocates ([[linker]] at load time) |
| libc | [[system call]] wrappers, malloc |
| Language runtime | Exceptions, GC, goroutine scheduler |
| [[interpreter]] | Executes non-native code paths |

Container images ship a minimal runtime (musl vs glibc) — ABI mismatch breaks binaries.

See [[runtime]] for shorter cross-reference.

## Sources

- Levine, *Linkers and Loaders*
- Linux `ld.so(8)`, `ldd(1)` manual pages
