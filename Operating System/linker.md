[[Operating System]] [[interpreter]] [[OS program]] [[opcode]] [[Linux/management/ELF (Editabl Linkable File)]] [[Runtime Environment]]

# Linker

> The linker combines object files and libraries into one executable or shared object — resolving symbols, assigning addresses, and producing the ELF the kernel `execve` loads.





## Interview Relevance
Static vs dynamic linking, relocation/PIC, and “undefined reference” vs runtime `ld.so` failures.

## Sources
- Levine, *Linkers and Loaders* — deep-dive
- Linux `ld(1)`, ELF specification — deep-dive
- [Wikipedia — Linker (computing)](https://en.wikipedia.org/wiki/Linker_(computing)) — overview

## Key Concepts
- **Inputs:** `.o` files with unresolved refs.
- **Jobs:** merge sections, resolve symbols, apply relocations, emit ELF/shared object.
- **Dynamic link:** defer some symbols to `ld.so` at runtime ([[Runtime Environment]]).
- **Tools:** `ld`, `gold`, `lld`.

## Technical Details
```txt
main.c → cc -c → main.o ─┐
libc.so ─────────────────┼→ ld → a.out (ELF)
other.o ─────────────────┘
```

Output is an [[OS program]] / [[Linux/management/ELF (Editabl Linkable File)]]. Contrast [[interpreter]] execution of scripts without a user-code link step.

## Real-World Applications
Building binaries, diagnosing missing symbols, and shipping statically linked containers vs distroless dynamic images.

## Pros/Cons or Trade-offs
- **Static:** simple deploy; larger binaries; fewer shared updates.
- **Dynamic:** smaller/shared; load-time dependency failures.
- **Trade-off:** LTO/optimization time vs link speed.

## Comparison
- vs compiler: compiler makes objects; linker makes the final image.
- vs loader (`ld.so`): link-time vs run-time resolution.

## Mistakes to Avoid
- Confusing link errors with runtime “library not found.”
- Forgetting `-fPIC` when building shared objects.
- Mixing incompatible ABIs across objects.
