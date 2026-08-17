[[Operating System]] [[runtime]] [[interpreter]] [[linker]] [[OS program]] [[system call]]

# Runtime Environment

> The runtime environment is everything that executes your program after the kernel starts it — dynamic linker, libc, thread library, GC, and language builtins.





## Interview Relevance
Distinguishes kernel `execve` from user-space runtime (ld.so, JVM, Go runtime) — and explains “works on my machine” ABI / glibc vs musl failures.

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

For a C binary: kernel `execve` → **ld.so** maps libc → `_start` → `main`. For JVM: native `java` stub loads bytecode, JIT, and standard library.

See [[runtime]] for a shorter cross-reference; [[OS program]] for the image the kernel loads.

## Real-World Applications
Distroless/minimal images must still ship a compatible runtime. Language version managers switch runtimes without changing the kernel.

## Pros/Cons or Trade-offs
- **Rich runtime:** faster development, GC, batteries included — larger attack surface and memory.
- **Minimal runtime:** smaller images; more work falls on the application.
- **Trade-off:** static binary vs shared libc updates.

## Comparison
- vs [[OS program]]: program is the on-disk/in-memory image; runtime is the supporting execution machinery.
- vs [[interpreter]]: interpreter is one runtime style for non-native code.

## Mistakes to Avoid
- Shipping a glibc-linked binary into a musl-only image.
- Blaming the kernel for missing `.so` — that is the dynamic linker/runtime.
- Confusing “runtime” (execution env) with “run time” (wall-clock duration) in design docs.
