[[compiler]] [[object code]] [[transpiler]]

# Compile time

> Work done before the program runs — parse, type-check, optimize, and generate code so the runtime starts with a finished artifact.

## Interview Relevance

Interviewers separate compile time vs runtime vs link time: where generics monomorphize, where `constexpr` runs, and why slow compiles hurt feedback loops.

## Sources

- [Wikipedia — Compile time](https://en.wikipedia.org/wiki/Compile_time) — overview
- [C++ reference — Constant expressions](https://en.cppreference.com/w/cpp/language/constant_expression) — deep-dive

## Key Concepts

- **Compile time:** translation of source → object/bytecode before execution.
- **Link time:** combine objects/libs into an executable or image (may do LTO).
- **Runtime:** actual execution on a machine/VM.
- **Metaprogramming:** templates/`constexpr`/macros shift work to compile time → faster runtime, slower builds.

## Technical Details

Typical pipeline:

```
Source → preprocess → parse/type-check → IR/optimize → codegen → object → link → binary
```

| Phase | Examples of decisions |
|-------|------------------------|
| Compile | Types, inlining, dead-code elim |
| Link | Symbol resolution, LTO across TUs |
| Runtime | I/O, heap, dynamic dispatch |

Languages differ: C/C++/Rust/Go are ahead-of-time heavy; Java/Kotlin mix compile-to-bytecode + JIT; fully dynamic languages push almost everything to runtime.

## Real-World Applications

CI time budgets: cache objects, reduce template blow-ups, enable incremental compilation so compile-time cost stays tolerable.

**Example:** A C++ header-only library doubles CI time — move implementations to `.cpp` to cut compile-time fan-out.

## Pros/Cons or Trade-offs

- **Pro:** Catching type errors before production; optimize once, run many times.
- **Con:** Long compile times slow iteration; heavy generics can explode build graphs.

## Comparison

- vs [[transpiler]]: both are pre-runtime translation; transpile usually targets another source language.
- vs interpreted startup: interpreters pay parse/cost at runtime (or cache bytecode later).

## Mistakes to Avoid

- Calling every failure “runtime” when the compiler already rejected it.
- Measuring app latency while including cold compile in the timer.
- Overusing header-only / giant unity builds without incremental strategy.
