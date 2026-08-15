[[compiler]] [[object code]] [[clang]] [[Linux/Memory management]]

# Library file

> Packaged object code other programs link against — static archives (`.a`) baked in at link time, or shared objects (`.so`/`.dll`) loaded at run time.

## Interview Relevance

Interviewers ask static vs shared linking, what `PIC` is for, and how `LD_LIBRARY_PATH` / rpath affect which `.so` you actually load.

## Sources

- [GNU — Introduction to Archives](https://sourceware.org/binutils/docs/binutils/ar.html) — overview
- [man ld.so](https://man7.org/linux/man-pages/man8/ld.so.8.html) — deep-dive

## Key Concepts

- **Static library (`.a`):** archive of `.o` files → linker copies needed objects into your binary.
- **Shared library (`.so` / `.dll` / `.dylib`):** one copy mapped at runtime → smaller binaries, versioned ABIs.
- **PIC / PIE:** position-independent code → required for most shared libs.
- **Symbol visibility / soname:** control exports and runtime identity of a shared lib.

## Technical Details

```
Source → Object (.o) → Archive (.a)  OR  Shared (.so)
```

```bash
gcc -c foo.c -o foo.o
ar rcs libfoo.a foo.o                 # static
gcc -fPIC -shared -o libfoo.so foo.o  # shared
gcc main.c -L. -lfoo -o app
ldd ./app                             # see .so deps (Linux)
```

| Kind | Link when | Update story |
|------|-----------|--------------|
| Static | Link time | Relink app to pick up lib fixes |
| Shared | Run time | Replace `.so` (ABI-compatible) |

## Real-World Applications

OS packages ship shared libs (`libc`, `libssl`); embedded/air-gapped tools often prefer static to reduce deployment deps.

**Example:** App works on the build machine but fails in production with `error while loading shared libraries` — fix rpath or install the `.so`.

## Pros/Cons or Trade-offs

- **Pro (shared):** one security patch updates many apps; less disk duplication.
- **Pro (static):** self-contained deploy; no `.so` search path surprises.
- **Con (shared):** ABI breaks and path hell; **con (static):** huge binaries, must relink for fixes.

## Comparison

- vs [[object code]]: libraries are organized collections of objects plus metadata.
- vs plugins: dynamically loaded modules are shared libs loaded explicitly (`dlopen`).

## Mistakes to Avoid

- Building shared libs without `-fPIC`.
- Relying on random `LD_LIBRARY_PATH` hacks in production instead of proper install + rpath.
- Mixing static and shared copies of the same dependency (ODR/ABI pain).
