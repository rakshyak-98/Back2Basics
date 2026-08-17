[[Operating System]] [[opcode]] [[Stack Frame]] [[stack pointer]] [[interpreter]] [[Heap memory]] [[assembly language]]

# Stack based programming language

> Stack-based languages express programs as operations on an operand stack — no named registers in the source model; the JVM, Forth, and RPN calculators work this way.

```txt
        Stack based progra ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Bytecode / VM interviews: operand stack vs register machines, and how JIT sti…

## Sources
- JVM specification — operand stack — deep-dive
- [Wikipedia — Stack machine](https://en.wikipedia.org/wiki/Stack_machine) — overview

## Key Concepts
- **Operand stack semantics:** each [[opcode]] pushes/pops values.
- **Virtual vs hardware:** language model is stack; JIT/AOT still uses CPU registers.
- **Interpreter loop:** manipulates a virtual stack often in [[Heap memory]].
- **Overflow:** deep expression stacks → `StackOverflowError`

## Technical Details
```txt
push 2 → push 3 → add → stack top is 5
```

- Contrast register-machine ISAs targeted by [[assembly language]].
- Bytecode [[interpreter]]s evaluate the stack machine

## Mistakes to Avoid
- **Mistake:** Equating JVM operand-stack overflow with Linux thread-stack over…
- **Mistake:** Assuming stack bytecode cannot be fast — JITs rewrite hot traces
- **Mistake:** Writing huge expression trees that blow interpreter stacks in re…

## Pros/Cons or Trade-offs
- **Pro:** Compact bytecode; simple compiler front-ends.
- **Con:** Naive interpreters pay stack traffic; harder for humans to read than register IR.
- **Trade-off:** stack VM simplicity vs register-based IR for optimization (LLVM-style).

## Comparison
- vs [[Stack Frame]]: call stack frames are ABI/runtime
- vs register ISAs ([[assembly language]]): named registers vs push/pop model.


### Use cases
- JVM/.NET IL, WebAssembly (stack machine ISA), Forth embedded systems, and RPN…
