[[JavaScript]]

# Call stack

> Call stack — function gets added to call stack when they are invoked.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Structure]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- function gets added to call stack when they are invoked.
- call stack is part of JavaScript engine.
- function returns a value, it gets popped off the stack.
The main reason for having call stack is:
- keep track active sub-routine should return control when it finished executing.
-  Active sub-routine is one that has called, but is yet to complete execution.
> [!INFO] Adding a block's of sub-routine's entry to the call stack is sometimes called *winding*, and removing entries *unwinding*.
The actual details of the the stack in a programming language depend upon the compiler, operating system and the available *instruction set*.

## Standard config / commands

…

## Structure

Call stack is compose of [[stack frame]] also called activation records or activation frames.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
