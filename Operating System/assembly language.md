[[Operating System]] [[opcode]] [[linker]] [[Stack Frame]] [[stack pointer]] [[system call]] [[OS program]] [[Stack trace]] [[Boot/UEFI]] [[MBR]]

# Assembly language

> Assembly language is human-readable mnemonics for machine instructions — the lowest level most developers use before silicon, where syscalls, stacks, and calling conventions become visible.

## Interview Relevance

Shows you can read a syscall sequence, explain calling convention / stack frames, and connect crashes to bad returns — not just high-level pseudocode.

## Sources

- Intel® 64 and IA-32 Architectures Software Developer’s Manual — deep-dive
- AMD64 Architecture Programmer’s Manual — deep-dive
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective* — deep-dive
- [Wikipedia — Assembly language](https://en.wikipedia.org/wiki/Assembly_language) — overview

## Key Concepts

- **ISA + mnemonics:** `mov`, `syscall`, `ret` map to [[opcode]]s.
- **Assembler → objects → [[linker]] → [[OS program]].**
- **Syscall trap:** registers + `syscall` enter the kernel ([[system call]]).
- **Procedures:** push [[Stack Frame]]; [[stack pointer]] alignment matters.

## Technical Details

```txt
; simplified x86-64 write(1, buf, len) — illustrative
mov    rax, 1          ; __NR_write
mov    rdi, 1          ; stdout
; rsi = buf, rdx = len
syscall
```

Compilers emit assembly (or IR lowered to machine code). Hand-written assembly remains in boot loaders, kernels, and hot paths.

You still meet it when reading [[Stack trace]] / crash dumps, firmware paths ([[Boot/UEFI]], [[MBR]]), performance tuning, and security research (ROP/shellcode).

## Real-World Applications

Kernel entry stubs, crypto/math hot loops, boot stage-1 loaders, and teaching OS/ABI courses.

## Pros/Cons or Trade-offs

- **Pro:** Full control; visible costs of each instruction.
- **Con:** Non-portable, easy to get ABI and safety wrong.
- **Trade-off:** intrinsics/compiler asm vs full hand-written modules.

## Comparison

- vs [[opcode]]: opcode is the encoded bytes; assembly is the mnemonic form.
- vs high-level languages: HLLs hide calling convention and register allocation.

## Mistakes to Avoid

- Ignoring ABI (red zone, alignment, caller/callee-saved) and corrupting the stack.
- Assuming user space can talk to devices by port I/O on modern protected OS builds.
- Optimizing assembly before proving the algorithm and data layout are right.
