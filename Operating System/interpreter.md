[[Operating System]] [[linker]] [[runtime]] [[Runtime Environment]] [[OS program]] [[opcode]] [[system call]] [[file descriptors]] [[Heap memory]]

# Interpreter

> An interpreter executes source or bytecode at runtime — trading startup simplicity and portability for lower peak speed than ahead-of-time native binaries.

## Interview Relevance

Compiler vs interpreter vs JIT; shebang → `execve` of interpreter binary; same OS rules for fds/heap underneath.

## Sources

- Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools* — deep-dive
- [Wikipedia — Interpreter (computing)](https://en.wikipedia.org/wiki/Interpreter_(computing)) — overview

## Key Concepts

- **Pure interpretation:** fetch/decode/execute loop.
- **Bytecode VM:** software decode of [[opcode]]s (CPython, JVM without JIT).
- **JIT hybrid:** hot paths → machine code; cold paths stay interpreted.
- **Shebang:** `#!/usr/bin/env python3` selects the interpreter [[OS program]].

## Technical Details

```txt
Source → interpreter ──► run immediately

Source → compiler → object → [[linker]] → native binary → CPU
Source → compiler → bytecode → VM interpreter / JIT
```

The interpreter is itself a native executable. It makes [[system call]]s for scripts — same [[file descriptors]] and [[Heap memory]] rules. Part of the [[Runtime Environment]] / [[runtime]].

## Real-World Applications

Python/Ruby/PHP apps, JVM warmup before JIT, and embedded Forth/BASIC systems.

## Pros/Cons or Trade-offs

- **Pro:** Fast edit-run cycle; portable bytecode.
- **Con:** Lower peak throughput without JIT; larger runtime dependency.
- **Trade-off:** interpret everything vs AOT/JIT complexity.

## Comparison

- vs compiled [[OS program]]: native CPU vs software dispatch.
- vs [[linker]]: interpreters skip user-code link steps; the interpreter binary was still linked.

## Mistakes to Avoid

- Assuming the kernel “runs Python” — it runs the interpreter binary.
- Comparing interpreter microbenchmarks to fully warmed JITs unfairly.
- Shipping scripts without the required interpreter in the image.
