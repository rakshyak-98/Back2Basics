[[Operating System]] [[assembly language]] [[interpreter]] [[Stack based programming language]] [[linker]] [[system call]]

# Opcode

> An opcode is the numeric operation code in a machine or bytecode instruction — the CPU or VM decoder reads it and dispatches the right micro-operation.

```txt
        Opcode ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** ISA vs bytecode

## Sources
- Intel/AMD ISA manuals — instruction encodings — deep-dive
- [Wikipedia — Opcode](https://en.wikipedia.org/wiki/Opcode) — overview

## Key Concepts
- **Machine code:** opcodes in `.text` from [[linker]] output / [[assembly language]].
- **Bytecode:** VM [[interpreter]] or JIT tables index opcodes.
- **Example:** `0x0F 0x05` → `syscall` ([[system call]] entry on x86-64).
- **Stack machines:** opcodes push/pop ([[Stack based programming language]]).

## Technical Details
- Security: unexpected opcodes in data → crash or exploit if control jumps into…

- Disassemblers map bytes → mnemonics; assemblers do the reverse.

## Mistakes to Avoid
- **Mistake:** Executing or mapping writable+executable pages casually
- **Mistake:** Assuming all “instructions” are one byte — x86 is variable-length
- **Mistake:** Confusing bytecode opcodes with host CPU opcodes when debugging …

## Pros/Cons or Trade-offs
- **Dense encodings:** compact programs; harder for humans.
- **RISC fixed sizes:** simpler decode; potentially larger code.
- **Trade-off:** CISC variable-length richness vs RISC regularity.

## Comparison
- vs mnemonic ([[assembly language]]): human form vs numeric encoding.
- vs high-level operators: language ops lower to one or many opcodes.


### Use cases
- Debuggers, JITs, emulators, and shellcode analysis.
