[[Operating System]] [[assembly language]] [[interpreter]] [[Stack based programming language]]

# Opcode

> An opcode is the numeric operation code in a machine or bytecode instruction — the CPU or VM decoder reads it and dispatches the right micro-operation.

In **machine code**, opcodes sit in executable `.text` sections ([[linker]] output). In **bytecode VMs**, opcodes index an interpreter loop ([[interpreter]]) or JIT tables.

Example (conceptual x86): `0x0F 0x05` → `syscall` for [[system call]] entry.

## Stack machines

Some ISAs and bytecodes ([[Stack based programming language]]) use opcodes that push/pop an operand stack instead of naming registers — JVM, Forth, some embedded VMs.

Security: unexpected opcodes in data → crash or exploit if execution jumps into data.

## Sources

- Intel/AMD ISA manuals — instruction encodings
- Wikipedia: [Opcode](https://en.wikipedia.org/wiki/Opcode)
