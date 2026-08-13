[[Operating System]] [[linker]] [[runtime]] [[Runtime Environment]] [[OS program]]

# Interpreter

> An interpreter executes source or bytecode instructions directly at runtime — trading startup simplicity and portability for lower peak speed compared with ahead-of-time compiled [[OS program]] binaries.

**Pure interpretation** fetches each instruction in a loop. **Bytecode VMs** (CPython, JVM without JIT, Ruby) decode opcodes ([[opcode]]) in software. **JIT** hybrids compile hot paths to machine code while retaining interpreter fallback.

## Versus compilation pipeline

```txt
Source → interpreter ──► run immediately

Source → compiler → object → [[linker]] → native binary → CPU
Source → compiler → bytecode → VM interpreter / JIT
```

## OS involvement

The interpreter itself is a native executable loaded by the loader ([[Boot/UEFI]] chain → kernel → execve). It makes [[system call]]s on behalf of scripts — same [[file descriptors]] and [[Heap memory]] rules.

Shebang `#!/usr/bin/env python3` selects the interpreter binary via `execve`.

## Sources

- Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools*
- Wikipedia: [Interpreter (computing)](https://en.wikipedia.org/wiki/Interpreter_(computing))
