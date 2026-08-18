[[Operating System]] [[Stack Frame]] [[Stack trace]] [[assembly language]] [[opcode]]

# stack pointer

> The stack pointer (SP) is the CPU register that holds the address of the current stack top — push lowers it, pop raises it on typical ABIs.

## Mental model

**Say it in one breath:** Calls and locals move SP; the old return address and saved registers live in the [[Stack Frame]] SP just carved out.

```txt
high address
  … previous frame …
  return address
  saved regs / locals     ← SP points near here (ABI-dependent)
low address  (stack grows downward on x86/ARM)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **SP / ESP / RSP** | Stack pointer register (x86) | “RSP tracks the top of the stack.” |
| --- | --- | --- |
| **FP / RBP / frame pointer** | Stable base for this frame | “Locals are RBP−offset; helps unwinding.” |
| **Push / pop** | Store/load and adjust SP | “Push decrements SP then writes (x86).” |
| **PC / IP / RIP** | Next instruction address | “Not the stack — that’s the instruction pointer.” |
| **LR (ARM)** | Link register — return address | “BL stores return in LR; may spill to stack.” |
| **Red zone** | Scratch below SP (SysV AMD64) | “Leaf functions may use 128B without adjusting SP.” |

### Related registers (keep short)

| Register | Job in one line |

| **SP** | Top of stack |
| --- | --- |
| **FP** | Base of current frame (optional) |
| **PC/IP** | Next instruction to execute |
| **LR** | Return address (ARM calling convention) |

### How the story goes (4 steps)

1. **Call** — push return address (or use LR); adjust SP for locals.
2. **Run** — address locals via SP/FP offsets.
3. **Return** — tear down frame; jump to saved return address.
4. **Overflow** — SP walks into guard page → segfault / stack overflow.

## Standard config / commands

```bash
# Disassemble prologue — watch SP adjustments
objdump -d ./a.out | less
gdb ./a.out
(gdb) break main
(gdb) run
(gdb) info registers rsp rbp rip
(gdb) x/16gx $rsp
```

```asm
; x86-64 SysV sketch
push %rbp
mov  %rsp, %rbp
sub  $0x20, %rsp      ; allocate locals
; …
leave                 ; mov %rbp,%rsp ; pop %rbp
ret
```

| Knob | Why it matters |

| `-fomit-frame-pointer` | Smaller code; harder `bt` / profiling |
| --- | --- |
| Stack size (`ulimit -s`, pthread attr) | Overflow vs deep recursion |
| Guard pages | Catch overflow as SIGSEGV |
| ABI (SysV vs Windows) | Red zone, arg regs differ — see [[SYSV (System V)]] |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| SIGSEGV near stack addresses | `bt`; huge recursion | Reduce depth; heap-allocate big arrays |
| Corrupt locals / return | Buffer overflow on stack | Bounds checks; canaries (`-fstack-protector`) |
| Bad `bt` in profiler | Omitted frame pointers | Build with frame pointers for debug |
| Crash only with optimization | Wrong asm / clobbered SP | Fix inline asm constraints |
| Thread-only crash | Small pthread stack | `pthread_attr_setstacksize` |

## Gotchas

> [!WARNING]
> **Stack grows down on mainstream ISAs** — “increasing SP” means popping, not allocating.

> [!WARNING]
> **Huge VLAs / `alloca`** can blow the stack silently until the guard page.

> [!WARNING]
> **SP must stay aligned** (16-byte on SysV AMD64 before calls) — misaligned SP → mysterious SSE faults.

> [!WARNING]
> **PC ≠ SP.** Confusing instruction pointer with stack pointer fails interviews and debugging.

## When NOT to use

- **Large or long-lived data** — put it on the [[Heap memory|heap]]; stack frames vanish on return.
- **Sharing across threads** — each thread has its own stack; don’t pass pointers to another thread’s locals.
- **Persisting across `setjmp` carefully** — understand what survives; prefer clearer control flow.

## Related

[[Stack Frame]] [[Stack trace]] [[Heap memory]] [[assembly language]] [[opcode]] [[SYSV (System V)]] [[Stack based programming language]]
