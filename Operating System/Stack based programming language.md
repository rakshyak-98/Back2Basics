[[interpreter]] [[opcode]] [[Heap memory]]

# Stack-based programming language

> Evaluation model where operands and results live on a stack — programs are often postfix (Reverse Polish) with no named registers in source form.

---

## Mental model

**Stack machines** push/pop values instead of assigning to registers in source syntax:

```txt
Infix:     (3 + 4) * 5
Postfix:   3 4 + 5 *     → stack: [3] [3,4] [7] [7,5] [35]

Execution:
  PUSH 3    stack: 3
  PUSH 4    stack: 3 4
  ADD       stack: 7
  PUSH 5    stack: 7 5
  MUL       stack: 35
```

Languages / VMs:
- **Forth**, **PostScript**, **Factor**
- **JVM bytecode** (operand stack + locals)
- **WebAssembly** (value stack)
- **DC**, some calculator DSLs

Contrast **register machines** (most native ISAs, Lua VM) — compilers map stack code to registers anyway.

---

## Standard config / commands

### Forth example (gforth)

```forth
\ RPN: square then add one
: sq1 ( n -- n^2+1 ) dup * 1 + ;

5 sq1 .   \ prints 26
```

### JVM stack intuition (javap)

```bash
javac Hello.java
javap -c Hello.class | less
# iload_0, iadd, istore — stack operations
```

### WebAssembly stack (wat)

```wat
(module
  (func (export "add") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add))
```

**Why stack IR:** compact encoding, easy verification (stack depth analysis), simple interpreters — good for portable bytecode.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stack underflow in VM | Compiler bug or corrupt bytecode | Verify with VM validator (JVM VerifyError) |
| Deep recursion stack overflow | Language maps calls to stack | Trampoline; explicit stack machine in heap |
| Slow vs native | Stack dispatch overhead | JIT (JVM C2, WASM engines) |
| Confusing postfix bugs | Wrong order of ops | Draw stack diagram; use named words/functions |

---

## Gotchas

> [!WARNING]
> **Postfix errors are silent** — `3 4 -` vs `4 3 -` swap operands with no syntax cue.

> [!WARNING]
> **JVM has both operand stack and local slots** — "stack language" at bytecode, not at Java source level.

> [!WARNING]
> **Stack depth limits** — WASM and embedded VMs cap depth; deep expressions fail validation.

---

## When NOT to use

Greenfield app logic in Forth-style RPN hurts readability for teams — use stack IR **under** a conventional language (JVM, WASM), not as your primary source syntax unless domain fits (DSL calculators, PostScript).

---

## Related

[[interpreter]] [[opcode]] [[Stack Frame]] [[Heap memory]] [[runtime]]
