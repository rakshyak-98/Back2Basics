[[Operating System]] [[interpreter]] [[OS program]] [[opcode]]

# Linker

> The linker merges object files and libraries into one executable or shared library — it resolves symbols to real addresses.

## Mental model

**Say it in one breath:** Compiler emits `.o` with holes (undefined symbols); linker fills holes, applies relocations, writes ELF/PE/Mach-O.

```txt
a.o + b.o + libc.so ──ld──► app
   undefined printf ──► resolved to libc
   reloc sites ──► patched addresses
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Linker** | Combines objects | “Resolves symbols and layouts sections.” |
| --- | --- | --- |
| **Symbol** | Named address | “`main`, `printf` are symbols.” |
| **Relocation** | Fixup patch | “Where to write the final address.” |
| **Static link** | Copy lib into binary | “Bigger binary; fewer runtime deps.” |
| **Dynamic link** | Resolve at load | “Shared libc; needs matching `.so`.” |
| **Loader** | Maps binary to memory | “Runtime cousin of the linker.” |

### How the story goes

1. **Compile** — sources → objects with symbol tables.
2. **Link** — merge sections; resolve; emit executable/DSO.
3. **Load** — dynamic loader binds remaining symbols (`LD_LIBRARY_PATH`, rpath).
4. **Run** — jump to entry point.

## Standard config / commands

```bash
gcc -c a.c b.c
gcc -o app a.o b.o -lm          # link
gcc -shared -fPIC -o libx.so x.o
ldd ./app                       # dynamic deps
nm -C app | head                # symbols
readelf -d app | grep NEEDED
```

| Knob | Why it matters |

| `-Wl,-rpath,…` | Where to find `.so` at runtime |
| --- | --- |
| `--as-needed` | Drop unused DT_NEEDED |
| LTO (`-flto`) | Optimize across TUs at link |
| Version scripts | Export surface for `.so` |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `undefined reference` | Missing `.o`/lib order | Add lib; fix link order (`-l` after objs) |
| `cannot open shared object` | `ldd` / rpath | Install lib; set rpath/`LD_LIBRARY_PATH` |
| Wrong symbol version | `GLIBC_x.y` | Build on older glibc or ship compat |
| Huge binary | Static everything | Prefer dynamic; strip carefully |
| Duplicate symbol | Two defs of same global | `static` / namespaces / weak |
| Plugin won’t load | Missing exports / ABI | Export map; match compilers |

## Gotchas

> [!WARNING]
> **Link order matters with classic UNIX ld** — put libraries *after* the objects that need them.

> [!WARNING]
> **`LD_LIBRARY_PATH` in prod** — convenient footgun; prefer rpath/packages.

> [!WARNING]
> **Static glibc** — painful (NSS, DNS); often avoid.

> [!WARNING]
> **LTO + mismatched tools** — thin LTO needs matching plugin/bitcode toolchain.

## When NOT to use

- **Scripting / bytecode ship** — interpreter loads modules; no native link step.
- **Single translation unit toys** — compiler driver still links crt; you just don’t notice.
- **Kernel modules** — special `modpost` link rules, not userspace `ld` habits.

## Related

[[interpreter]] [[opcode]] [[assembly language]] [[OS program]] [[runtime]] [[Heap memory]]
