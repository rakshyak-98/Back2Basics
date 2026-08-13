[[Operating System]] [[opcode]] [[Stack Frame]] [[stack pointer]] [[interpreter]]

# Stack based programming language

> Stack-based languages express programs as sequences of operations on an operand stack — no named registers in the source model; the JVM, Forth, and RPN calculators work this way.

Each [[opcode]] pushes or pops values:

```txt
push 2 → push 3 → add → stack top is 5
```

The **hardware** still uses registers under JIT/AOT compilation, but the language semantics are stack-oriented.

## OS/runtime link

Bytecode [[interpreter]] loops manipulate a virtual stack in [[Heap memory]]; native JIT maps hot traces to machine code. Deep stacks overflow with `StackOverflowError` — separate from kernel stack limits ([[Stack Frame]]).

Contrast register-machine ISAs targeted by [[assembly language]].

## Sources

- JVM specification — operand stack
- Wikipedia: [Stack machine](https://en.wikipedia.org/wiki/Stack_machine)
