[[compile time]] [[object code]] [[library file]] [[clang]] [[transpiler]]

# Compiler

> Program that translates source in one language into machine code, bytecode, or another lower form a machine or VM can run.

## Interview Relevance

Interviewers want the pipeline (lex → parse → IR → optimize → codegen), front end vs back end, and how errors surface at each stage.

## Sources

- [Aho et al. — Compilers: Principles, Techniques, and Tools](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) — deep-dive
- [Wikipedia — Compiler](https://en.wikipedia.org/wiki/Compiler) — overview

## Key Concepts

- **Front end:** lex, parse, semantic analysis → syntax/type errors here.
- **IR (intermediate representation):** portable program shape for optimizations.
- **Back end / codegen:** IR → machine code or bytecode for a target.
- **Optimizer:** rewrite IR for speed/size without changing observable behavior (within the language model).
- **Driver:** orchestrates compile + assemble + link steps (`clang`, `gcc`).

## Technical Details

```
Source → tokens → AST → IR → optimize → asm/object → linker → executable
```

| Artifact | Meaning |
|----------|---------|
| `.o` / `.obj` | [[object code]] — not yet a full program |
| `.a` / `.so` / `.dll` | [[library file]] — reusable object collections |
| bytecode | VM-targeted form (JVM, .NET, etc.) |

Single-pass vs multi-pass: modern compilers are multi-pass over IR for better optimization.

## Real-World Applications

Every shipped native binary and most mobile/desktop apps pass through a compiler (or JIT that contains one).

**Example:** Turning on `-O2` fixes a tight loop in production CPU — confirm correctness tests still pass after optimization.

## Pros/Cons or Trade-offs

- **Pro:** Static checking and optimization before users run the code.
- **Con:** Build complexity and long compile times; optimizer bugs are rare but severe.

## Comparison

- vs [[transpiler]]: compiler usually targets machine/VM; transpiler targets another high-level language.
- vs interpreter: interpreter executes without producing a standalone native binary (may still bytecode-compile).

## Mistakes to Avoid

- Treating “the compiler” as one box — know which stage failed (parse vs link).
- Shipping `-O0` debug builds as performance truth.
- Ignoring warnings that later become runtime UB in C/C++.
