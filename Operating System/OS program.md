[[Operating System]] [[linker]] [[interpreter]] [[system call]] [[Runtime Environment]] [[process]] [[runtime]] [[Linux/management/ELF (Editabl Linkable File)]]

# OS program

> An OS program is an executable image the kernel loads into a [[process]] — ELF binary, shebang script, or shared object run by the loader.





## Interview Relevance
Walk `execve` → ELF map → `_start` → `main`, and distinguish kernel load from the user-space [[runtime]] / dynamic linker.

## Sources
- Bryant & O’Hallaron, *Computer Systems* — deep-dive
- Linux `execve(2)`, ELF specification — deep-dive
- [Wikipedia — Executable](https://en.wikipedia.org/wiki/Executable) — overview

## Key Concepts
- **Image formats:** ELF on Linux ([[Linux/management/ELF (Editabl Linkable File)]]), PE on Windows.
- **Scripts:** shebang delegates to an [[interpreter]] binary.
- **Kernel handoff:** maps segments, sets stack/heap, jumps to entry.
- **After handoff:** [[runtime]] / [[Runtime Environment]] (libc, threads, dynamic linking).

## Technical Details
```txt
User invokes path → execve() → kernel reads ELF headers
→ maps segments → sets up stack/heap → start (e.g. _start → main)
→ program runs via [[system call]] until exit
```

The [[linker]] resolves symbols at build and/or load time; the kernel does not run your `main` directly without CRT startup.

## Real-World Applications
Containers `ENTRYPOINT` binaries, `#!` ops scripts, and dynamically linked services that fail at startup on missing `.so` files — all are “OS programs” under `execve`.

## Pros/Cons or Trade-offs
- **Static linking:** simpler deploy; larger binaries, fewer shared CVE updates.
- **Dynamic linking:** smaller disk/RAM sharing; load-time dependency failures.
- **Interpreted:** fast to change; needs interpreter presence and has startup cost.

## Comparison
- vs [[process]]: program is the image; process is the running instance.
- vs [[Runtime Environment]]: runtime is libraries/VM after the kernel starts the image.

## Mistakes to Avoid
- Confusing compile-time [[linker]] errors with runtime loader (`ld.so`) failures.
- Assuming the kernel interprets Python/JS — it executes the interpreter binary named in the shebang.
- Forgetting that `execve` replaces the process image; PIDs can stay the same.
