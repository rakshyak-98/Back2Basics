[[Operating System]] [[Stack Frame]] [[Stack trace]] [[assembly language]]

# Stack pointer

> The stack pointer register (RSP on x86-64, SP on ARM) tracks the top of the current thread stack — decremented on call, incremented on return.

Must stay **aligned** per ABI (often 16-byte on x86-64). Corruption — buffer overflow past a local array — overwrites return address → arbitrary code or crash in [[Stack trace]].

Low-level debugging and [[assembly language]] show explicit `push`/`pop` or `sub rsp` prologues establishing a [[Stack Frame]].

## Sources

- System V AMD64 ABI — stack alignment
- Intel SDM — stack pointer semantics
