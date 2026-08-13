[[Operating System]] [[opcode]] [[linker]] [[Stack Frame]] [[stack pointer]] [[system call]]

# Assembly language

> Assembly language is human-readable mnemonics for machine instructions — the lowest level most developers use before silicon, and the layer where syscalls, stacks, and calling conventions become visible.

Each CPU family defines an **instruction set architecture (ISA)**. Assembly maps one mnemonic (for example `mov`, `syscall`, `ret`) to one or more machine **opcodes** ([[opcode]]). An **assembler** turns `.s` files into object code; the [[linker]] combines objects into an executable [[OS program]].

## Relationship to the operating system

User programs cannot open a disk or map memory by writing to ports directly (on modern protected systems). They load arguments into registers, execute a syscall instruction, and trap into the kernel ([[system call]]). Debugging at this layer shows exactly which registers hold file descriptors and error codes.

```txt
; simplified x86-64 write(1, buf, len) — illustrative
mov    rax, 1          ; __NR_write
mov    rdi, 1          ; stdout
; rsi = buf, rdx = len
syscall
```

## Stack and procedures

Function calls push a [[Stack Frame]]: return address, saved registers, locals. The [[stack pointer]] must stay aligned; corruption here produces impossible returns — see [[Stack trace]]. Compilers generate assembly (or LLVM IR lowered to machine code); hand-written assembly remains common in boot loaders, kernels, and hot paths.

## When you still meet it

- Reading crash dumps and [[Stack trace]] output
- Boot and firmware paths ([[Boot/UEFI]], [[MBR]] first-stage loaders)
- Performance tuning where the compiler’s choices matter
- Security research on shellcode and return-oriented programming

## Sources

- Intel® 64 and IA-32 Architectures Software Developer’s Manual — instruction set reference
- AMD64 Architecture Programmer’s Manual
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective*
- Wikipedia: [Assembly language](https://en.wikipedia.org/wiki/Assembly_language)
