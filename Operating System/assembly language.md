[[opcode]] [[linker]] [[system call]] [[interpreter]]

# Assembly language

> Human-readable mnemonics for machine instructions — one step above binary, one step below high-level languages; ISA-specific.

---

## Mental model

**Assembly** maps 1:1 (or close) to **opcodes** the CPU decodes. The assembler (`as`) produces object files; the **linker** resolves symbols.

```txt
C source  ──compiler──►  asm  ──assembler──►  .o  ──linker──►  executable
                              ▲
                              └── inline asm, hand-tuned hot paths
```

Each **ISA** (x86-64, ARM64, RISC-V) has its own syntax (AT&T vs Intel for x86). Registers, calling conventions, and stack layout are part of the language contract ([[Stack Frame]]).

Use assembly when you need:
- Boot / bring-up / kernels
- SIMD intrinsics wrappers
- Exploit mitigations review (ROP gadgets)
- Last-mile optimization (rare — profile first)

---

## Standard config / commands

### Write and build minimal asm (x86-64 Linux)

```assembly
# hello.S (AT&T syntax)
.global _start
_start:
    mov $1, %rax      # sys_write
    mov $1, %rdi      # stdout
    lea msg(%rip), %rsi
    mov $13, %rdx
    syscall
    mov $60, %rax     # sys_exit
    xor %rdi, %rdi
    syscall
msg: .ascii "Hello, asm\n"
```

```bash
as -64 hello.S -o hello.o
ld hello.o -o hello
./hello
```

### Inspect compiler output

```bash
gcc -S -O2 -fno-omit-frame-pointer app.c -o app.s
objdump -d -M intel ./a.out | less
```

### Debug at asm level

```bash
gdb ./a.out
(gdb) disassemble main
(gdb) si              # step one instruction
```

**Why `-fno-omit-frame-pointer`:** preserves [[Stack Frame]] chain for profilers.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `SIGILL` illegal instruction | CPU features (AVX-512 on old CPU) | `-march=x86-64-v2` baseline; runtime CPU dispatch |
| Wrong results after inline asm | Clobber list wrong, memory order | Use compiler intrinsics instead; read ABI docs |
| Link errors `undefined reference` | Missing `.global`; C name mangling | `extern "C"`; correct symbol visibility |
| ROP / security audit findings | Gadgets in executable segments | `-Wl,-z,relro,-z,now`; CET where available |

---

## Gotchas

> [!WARNING]
> **Assembly is not portable** — ARM64 code won't assemble on x86.

> [!WARNING]
> **Calling convention mismatches** between C and asm corrupt stack — follow System V AMD64 ABI (Linux) or platform docs.

> [!WARNING]
> **Micro-architecture matters** — instruction latency/throughput tables change per CPU generation; "fast" asm from 2010 may lose to `-O3` today.

---

## When NOT to use

Default to C/Rust/Go with intrinsics. Hand-written asm increases maintenance cost and blocks compiler optimizations across function boundaries.

---

## Related

[[opcode]] [[linker]] [[Stack Frame]] [[system call]] [[Single Instruction, Multiple Data (SIMD)]]
