[[Operating System]] [[interpreter]] [[OS program]] [[opcode]] [[Linux/management/ELF (Editabl Linkable File)]]

# Linker

> The linker combines compiled object files and libraries into one executable or shared object — resolving symbols, assigning final addresses, and producing the ELF binary the kernel execve loads.

After the compiler emits `.o` files with unresolved references, **`ld`** (or `gold`, `lld`):

1. Merges `.text`, `.data`, `.bss` sections.
2. Resolves `malloc`, `main`, etc. against libc.
3. Applies relocations for PIC/PIE.
4. Outputs ELF ([[Linux/management/ELF (Editabl Linkable File)]]) or static binary.

```txt
main.c → cc -c → main.o ─┐
libc.so ─────────────────┼→ ld → a.out (ELF)
other.o ─────────────────┘
```

Dynamic linking defers some symbols to runtime **loader** (`ld.so`) — part of the [[Runtime Environment]].

Contrast [[interpreter]] execution of scripts without a separate link step for user code.

## Sources

- Levine, *Linkers and Loaders*
- Linux `ld(1)`, ELF specification
- Wikipedia: [Linker (computing)](https://en.wikipedia.org/wiki/Linker_(computing))
