[[compiler]] [[linker]] [[Operating System/file descriptors]]

# library file

> library file — source → Object (.o) → Archive (.a) OR Shared (.so)

## Mental model

```txt
Source → Object (.o) → Archive (.a) OR Shared (.so)
                              ↓
                         Linker embeds or records dependency
                              ↓
                         Executable or higher-level .so
```

| Artifact | Link time | Run time | Size / deploy |

| **Static `.a`** | Code copied into binary | No separate lib file | Larger binary; self-contained |
| --- | --- | --- | --- |
| **Shared `.so`** | Symbol references recorded | Loader maps `.so` (SONAME) | Smaller binary; must ship compatible `.so` |

**Linux loader:** `ld.so` reads `DT_NEEDED`, searches `LD_LIBRARY_PATH`, `/etc/ld.so.cache`, `RUNPATH`/`RPATH`.

**Windows:** `.lib` import library + `.dll` runtime; **macOS:** `.dylib` + `@rpath`, `@loader_path`.

**ABI stability:** shared libs must match **ABI** (compiler, stdlib, `-fPIC`, symbol versioning) — not just API headers.

## Standard config / commands

### Inspect artifacts

```bash
# Linux: shared lib dependencies
ldd ./myapp
readelf -d libfoo.so | grep NEEDED
objdump -T libfoo.so | head          # exported symbols

# Static archive contents
ar -t libfoo.a

# macOS
otool -L ./myapp

# Windows (dumpbin on MSVC toolchain)
dumpbin /dependents myapp.exe
```

### Build patterns

```bash
# Static link (glibc caveat: some distros discourage fully static)
gcc -o myapp main.o -L./lib -lfoo -static-libgcc

# Shared link
gcc -o myapp main.o -L./lib -lfoo -Wl,-rpath,'$ORIGIN/lib'

# Position-independent code required for .so
gcc -fPIC -shared -o libfoo.so foo.c
```

### CMake (typical service native dep)

```cmake
add_library(foo SHARED foo.c)
target_include_directories(foo PUBLIC include)
install(TARGETS foo LIBRARY DESTINATION lib)
install(FILES include/foo.h DESTINATION include)
```

### pkg-config (discover flags)

```bash
pkg-config --libs --cflags libssl
# -lssl -lcrypto + include paths
```

### CI checklist

```txt
1. Pin compiler + lib version in container
2. Ship .so with SONAME or vendor in $ORIGIN/lib
3. Run ldd on binary in clean image (not dev laptop)
4. For static: audit LGPL/GPL propagation (dynamic link often required)
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `error while loading shared libraries: libfoo.so` | `ldd ./app` in prod image | Install package; set `RUNPATH`; copy `.so` next to binary |
| Wrong `.so` version loaded | `LD_DEBUG=libs ./app` | Align SONAME; remove stale paths from `LD_LIBRARY_PATH` |
| Works locally, fails CI | Dev machine has extra libs | Minimal container reproduce; explicit `-L` / vendoring |
| `undefined reference` at link | Missing `-l` or wrong order | Put `-lfoo` after objects that use it |
| `GLIBCXX_3.4.xx not found` | libstdc++ mismatch | Match build/runtime GCC; use same base image |
| Static binary huge / NSS issues | glibc static quirks | Prefer shared linking on Linux services |

## Gotchas

> [!WARNING]
> **Mixing static and shared for same lib** (e.g. OpenSSL) — symbol duplication / ODR violations → subtle crashes.

> [!WARNING]
> **Alpine (musl) vs Debian (glibc)** — binaries are not portable; build in target libc environment.

> [!WARNING]
> **LGPL libraries** — static link may trigger source disclosure obligations; legal review for `.a` embed.

> [!WARNING]
> **`LD_LIBRARY_PATH` in prod** — fragile; prefer `RUNPATH` baked at link or distro packages in standard paths.

## When NOT to use

- **Pure managed runtimes (JVM, Node, Python wheels)** — use package manager / manylinux wheels unless writing native extensions.
- **Static everything on glibc Linux servers** — operations and security updates harder; shared distro libs preferred.
- **Vendor `.so` without ABI pin** — upgrade host OS breaks application; containerize or bundle exact SONAME.

## Related

[[compiler]] · [[Operating System/file descriptors]] · [[Docker compose]] · [[docker cli]]
