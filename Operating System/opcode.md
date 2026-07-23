[[assembly language]] [[system call]] [[Single Instruction, Multiple Data (SIMD)]]

# Opcode

> The operation field of a machine or protocol instruction — tells the executor *what* to do with the operands that follow.

---

## Mental model

An **opcode** (operation code) is the discriminant in an instruction word. Everything else in the instruction (registers, immediates, addressing mode) is **operand encoding**.

```txt
CPU instruction (conceptual)
┌────────┬─────────────────────────┐
│ opcode │ operands (reg, imm, mem)  │
└────────┴─────────────────────────┘
         ▼
    decode → execute unit (ALU, load/store, branch)
```

Two common contexts engineers hit:

| Context | Opcode means | Example |
|---------|--------------|---------|
| **Machine / assembly** | CPU ALU or control operation | `ADD`, `MOV`, `JMP`, `SYSCALL` |
| **Wire protocol / VM bytecode** | Message or instruction type | RPC `0x01=LOGIN`, JVM `iconst_1`, Redis op prefix |

Variable-length ISAs (x86) interleave opcode bytes with prefixes; fixed-width (ARM, RISC-V) pack opcode into fixed bit fields. **Illegal opcode** → `#UD` fault on x86, undefined instruction on ARM.

---

## Standard config / commands

### Disassemble and inspect opcodes

```bash
# x86-64 binary
objdump -d ./a.out | less
llvm-objdump -d ./a.out

# Live process (requires perf rights)
perf record -e instructions:u -p PID -- sleep 3
perf annotate --stdio
```

```bash
# strace: see syscall opcodes (software trap), not CPU opcodes
strace -e trace=read,write,openat -p PID
```

### Assembly examples (mnemonic = human-readable opcode)

```assembly
MOV  RAX, 1      ; opcode MOV — load immediate
ADD  RAX, RBX    ; opcode ADD
SYSCALL          ; opcode SYSCALL — enter kernel
```

**Protocol example:** a custom binary frame might use `uint8 opcode` as first byte; parsers `switch(opcode)` before reading payload length.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `#UD` / illegal instruction crash | CPU feature mismatch (AVX on old host) | Build for baseline CPU; gate SIMD at runtime |
| Wrong results after compiler upgrade | New instruction selection | Compare `objdump`; pin `-march` |
| Protocol parse errors at byte 0 | Opcode enum drift between versions | Version header; reject unknown opcodes |
| JIT sandbox escape | Writable+executable pages | W^X, separate RX mapping for JIT code |

---

## Gotchas

> [!WARNING]
> **Opcode ≠ syscall number.** `SYSCALL` is one CPU opcode; the *kernel service* is selected via register (e.g., `RAX` on x86-64).

> [!WARNING]
> **Self-modifying code and JIT** generate opcodes at runtime — debuggers may desync from memory.

> [!WARNING]
> **SIMD opcodes** (`VEX`, `EVEX` prefixes on x86) change instruction length — disassembly must start at correct boundaries.

---

## When NOT to use

Application developers rarely choose opcodes directly — compilers and VMs do. Hand-write assembly only for hot paths, intrinsics, or bring-up where profiling proves the need.

---

## Related

[[assembly language]] [[system call]] [[Single Instruction, Multiple Data (SIMD)]] [[interpreter]] [[linker]]
