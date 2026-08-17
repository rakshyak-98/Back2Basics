[[Linux system management]] [[process]] [[gdb]] [[hax dump]]

# ELF (Executable and Linkable Format)

> Native Linux binary format — executables, shared libraries, and object files share one header/segment model.





## Interview Relevance
Expect `readelf`/`ldd`, PT_INTERP, NEEDED libs, and why `LD_LIBRARY_PATH` is a production smell.

## Sources
- [ELF man page — elf(5)](https://man7.org/linux/man-pages/man5/elf.5.html) — deep-dive
- [Wikipedia — Executable and Linkable Format](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) — overview

## Core Definition
Headers describe segments (loaded into memory) and sections (linking/debug). On `execve`, the kernel maps `PT_LOAD` segments; **ld.so** (dynamic linker) loads `NEEDED` shared libraries from RPATH/RUNPATH, `LD_LIBRARY_PATH`, and defaults.

## Key Concepts
- **ET_EXEC / PIE / ET_DYN / ET_REL:** runnables, shared objects, relocatable objects.
- **PT_INTERP:** path to the dynamic linker — wrong arch/interpreter → mysterious “No such file.”
- **SONAME / NEEDED:** runtime library identity and dependencies.
- **Symbols / strip:** production binaries often lack debug symbols.

## Technical Details
```
source.c ──compile──► .o (relocatable ELF)
           ──link──► a.out (PIE executable ELF)
           ──link -shared──► libfoo.so (shared ELF)

execve ──► kernel maps PT_LOAD segments ──► ld.so ──► main()
```

```bash
file /bin/ls
readelf -h /bin/ls
readelf -l /bin/ls
readelf -S /bin/ls
ldd /bin/ls
readelf -d /bin/ls | grep NEEDED
readelf -l /bin/ls | grep interpreter
nm -D /lib/x86_64-linux-gnu/libc.so.6 | head
objdump -T /bin/ls
ldconfig -p | grep libssl
echo '/opt/mylib/lib' | sudo tee /etc/ld.so.conf.d/mylib.conf
sudo ldconfig
gcc -g -O0 hello.c -o hello
strip hello
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No such file running binary | Arch / missing interpreter | `file`; `readelf -l \| grep interpreter` |
| error while loading shared libraries | Missing `.so` | `ldd`; install package; fix rpath |
| Wrong library version | Search order | `LD_DEBUG=libs`; fix rpath/`ldconfig` |
| Exec format error | ARM on x86 (etc.) | Matching CPU/container |
| Segfault at startup | ABI / bad rpath | `ldd`; rebuild same toolchain |

## Real-World Applications
Debug a vendor binary that fails only on Alpine (musl) vs Ubuntu (glibc), or find which `.so` an app actually loaded after an upgrade.

## Pros/Cons or Trade-offs
- **Pro:** One format for tools (`readelf`, debuggers, loaders) across the stack.
- **Con:** Dynamic linking search order is subtle; static musl/glibc mismatches are opaque.

## Comparison
- vs scripts (`#!`): kernel runs the interpreter, not an ELF of the script text.
- vs JVM bytecode: only the runtime is ELF; class files are not.

## Mistakes to Avoid
- `ldd` on untrusted binaries (it can execute code via crafted interpreters).
- Shipping `LD_LIBRARY_PATH` in production instead of fixing SONAME/rpath.
- Assuming stripped production binaries still have useful `nm` output without debuginfo.
