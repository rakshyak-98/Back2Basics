[[Linux system management]] [[compiler/library file]] [[process]]

# ELF (Executable and Linkable Format)

> One-line: the standard **binary object format** for executables, shared libraries, and relocatable objects on Linux — what `file`, the dynamic linker, and debuggers consume. **System V ABI / gABI**.

## Mental model

Every native Linux program is an **ELF file**: headers describe segments (loaded into memory) and sections (linking/debug). The kernel exec's the file; **ld.so** (dynamic linker) loads `NEEDED` shared libraries from `DT_RPATH`, `LD_LIBRARY_PATH`, and default paths.

```
source.c ──compile──► .o (relocatable ELF)
           ──link──► a.out (PIE executable ELF)
           ──link -shared──► libfoo.so (shared ELF)

execve ──► kernel maps PT_LOAD segments ──► ld.so ──► main()
```

| Type | `file` output | Role |
|------|---------------|------|
| ET_EXEC / PIE | executable | Run directly |
| ET_DYN | shared object | `.so` library |
| ET_REL | relocatable | `.o` before link |
| Core dump | ELF core | Post-mortem in [[gdb]] |

Key concepts: **symbols** (functions/variables), **relocations** (addresses fixed at link/load), **SONAME** (`libcurl.so.4`).

## Standard config / commands

```bash
# Identify type
file /bin/ls
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2

# Headers overview
readelf -h /bin/ls
readelf -l /bin/ls              # program headers (segments)
readelf -S /bin/ls              # sections

# Dynamic linking dependencies
ldd /bin/ls
readelf -d /bin/ls | grep NEEDED

# Symbols (stripped binaries show fewer)
nm -D /lib/x86_64-linux-gnu/libc.so.6 | head
objdump -T /bin/ls              # dynamic symbol table

# Which linker interprets this binary
readelf -l /bin/ls | grep interpreter

# Library search path (runtime)
cat /etc/ld.so.conf
ldconfig -p | grep libssl

# After installing .so in custom path
echo '/opt/mylib/lib' | sudo tee /etc/ld.so.conf.d/mylib.conf
sudo ldconfig
```

**Build / inspect workflow:**

```bash
gcc -g -O0 hello.c -o hello     # debug symbols
strip hello                     # remove symbols (smaller, harder to debug)
readelf -s hello | grep main
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `No such file or directory` running binary | Wrong architecture or missing interpreter | `file bin`; `readelf -l \| grep interpreter`; install correct arch / libc |
| `error while loading shared libraries` | Missing .so | `ldd ./app`; install package; `LD_LIBRARY_PATH` (dev only) |
| Wrong library version picked | Search order | `LD_DEBUG=libs ./app`; fix `rpath` at link; `ldconfig` |
| `Exec format error` | ARM binary on x86 | Cross-compile or run on matching CPU |
| `cannot execute binary file` | Script missing shebang vs corrupt ELF | `file`; `head -1` |
| Segfault at startup | ABI mismatch, bad rpath | `ldd`; rebuild with same toolchain/glibc |

## Gotchas

> [!WARNING]
> **`LD_LIBRARY_PATH` in production** — masks broken packaging; security risk in setuid binaries (ignored). Fix SONAME/rpath at build time.

> [!WARNING]
> **glibc vs musl** — Alpine (musl) binaries don't run on glibc distros and vice versa. `file` and ldd tell you.

> [!WARNING]
> **PIE vs non-PIE** — ASLR requires PIE; old static assumptions about fixed addresses fail.

> [!WARNING]
> **Stripped symbols** — `nm` empty on production binaries; need `-debuginfo` package or rebuild with `-g` for symbols.

## When NOT to use

- **Scripts** (#!) — kernel executes interpreter, not ELF of script itself.
- **Java/.NET/JVM bytecode** — different format; only the JVM/runtime is ELF.
- **Static analysis of app logic** → source + tests, not ELF headers alone.

## Related

[[compiler/library file]] [[process]] [[gdb]] [[Linux system management]]
