[[Operating System]] [[linker]] [[interpreter]] [[system call]] [[Runtime Environment]] [[process]] [[runtime]] [[Linux/management/ELF (Editabl Linkable File)]]

# OS program

> An OS program is an executable image the kernel loads into a [[process]] — ELF binary, shebang script, or shared object run by the loader.

```txt
        OS program ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Walk `execve` → ELF map → `_start` → `main`, and distinguish kernel load from…

## Sources
- Bryant & O’Hallaron, *Computer Systems* — deep-dive
- Linux `execve(2)`, ELF specification — deep-dive
- [Wikipedia — Executable](https://en.wikipedia.org/wiki/Executable) — overview

## Key Concepts
- **Image formats:** ELF on Linux ([[Linux/management/ELF (Editabl Linkable File)]]), PE on Window…
- **Scripts:** shebang delegates to an [[interpreter]] binary.
- **Kernel handoff:** maps segments, sets stack/heap, jumps to entry.
- **After handoff:** [[runtime]] / [[Runtime Environment]] (libc, threads, dynamic linking).

## Technical Details
```txt
User invokes path → execve() → kernel reads ELF headers
→ maps segments → sets up stack/heap → start (e.g. _start → main)
→ program runs via [[system call]] until exit
```

- The [[linker]] resolves symbols at build and/or load time

## Mistakes to Avoid
- **Mistake:** Confusing compile-time [[linker]] errors with runtime loader (`l…
- **Mistake:** Assuming the kernel interprets Python/JS
- **Mistake:** Forgetting that `execve` replaces the process image

## Pros/Cons or Trade-offs
- **Static linking:** simpler deploy; larger binaries, fewer shared CVE updates.
- **Dynamic linking:** smaller disk/RAM sharing; load-time dependency failures.
- **Interpreted:** fast to change

## Comparison
- vs [[process]]: program is the image; process is the running instance.
- vs [[Runtime Environment]]: runtime is libraries/VM after the kernel starts the image.


### Use cases
- Containers `ENTRYPOINT` binaries, `#!` ops scripts, and dynamically linked se…
