[[Operating System]] [[Stack Frame]] [[Stack trace]] [[assembly language]]

# Stack pointer

> The stack pointer register (RSP on x86-64, SP on ARM) tracks the top of the current thread stack — decremented on call/push, incremented on return/pop.





## Interview Relevance
ABI alignment (often 16-byte), how overflows smash return addresses, and reading SP in [[assembly language]] / crash dumps.

## Sources
- System V AMD64 ABI — stack alignment — deep-dive
- Intel SDM — stack pointer semantics — deep-dive

## Key Concepts
- **Top of stack:** SP points at current extent of the stack.
- **Call/return:** hardware/ABI adjust SP around [[Stack Frame]]s.
- **Alignment:** ABI-required alignment or calls break.
- **Corruption:** buffer overflow past locals → bad return → bad [[Stack trace]].

## Technical Details
Low-level debugging shows `push`/`pop` or `sub rsp` prologues. Each thread has its own SP. Red zones (x86-64 SysV) allow limited scratch below SP without adjusting it — easy to mishandle in hand asm.

## Real-World Applications
Exploit mitigations (canaries, NX), compiler frame setup, and `gdb` inspection of `$rsp`.

## Pros/Cons or Trade-offs
- **Pro:** Extremely cheap stack allocation.
- **Con:** Fixed/limited growth; overflow is catastrophic.
- **Trade-off:** larger thread stacks vs memory use.

## Comparison
- vs frame pointer: FP anchors a frame; SP is the live top.
- vs heap pointers: SP is register-managed LIFO, not `malloc`.

## Mistakes to Avoid
- Misaligned SP before a call (SSE/AVX ABI faults).
- Writing below SP without respecting red-zone rules.
- Huge stack allocations in deep recursion.
