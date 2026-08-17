[[Operating System]] [[linker]] [[runtime]] [[Runtime Environment]] [[OS program]] [[opcode]] [[system call]] [[file descriptors]] [[Heap memory]]

# Interpreter

> An interpreter executes source or bytecode at runtime — trading startup simplicity and portability for lower peak speed than ahead-of-time native binaries.

```txt
        Interpreter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Compiler vs interpreter vs JIT

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

- The interpreter is itself a native executable.
- It makes [[system call]]s for scripts
- Part of the [[Runtime Environment]] / [[runtime]].

## Mistakes to Avoid
- **Mistake:** Assuming the kernel “runs Python”
- **Mistake:** Comparing interpreter microbenchmarks to fully warmed JITs unfai…
- **Mistake:** Shipping scripts without the required interpreter in the image

## Pros/Cons or Trade-offs
- **Pro:** Fast edit-run cycle; portable bytecode.
- **Con:** Lower peak throughput without JIT; larger runtime dependency.
- **Trade-off:** interpret everything vs AOT/JIT complexity.

## Comparison
- vs compiled [[OS program]]: native CPU vs software dispatch.
- vs [[linker]]: interpreters skip user-code link steps; the interpreter binary was still linked.


### Use cases
- Python/Ruby/PHP apps, JVM warmup before JIT, and embedded Forth/BASIC systems.
