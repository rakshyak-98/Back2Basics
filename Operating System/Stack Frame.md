[[Operating System]] [[stack pointer]] [[Stack trace]] [[Thread]] [[Heap memory]]

# Stack Frame

> A stack frame is the memory a function call pushes — return address, saved registers, locals — nested LIFO on the thread stack.

## Interview Relevance

Debugging and ABI interviews: explain call/return, frame pointers vs unwind tables, and why stack overflow differs from heap OOM.

## Sources

- Bryant & O’Hallaron, *Computer Systems* — procedure call convention — deep-dive
- [Wikipedia — Call stack](https://en.wikipedia.org/wiki/Call_stack) — overview

## Key Concepts

- **LIFO nesting:** caller frame below callee frame.
- **Contents:** return address, spilled registers, locals, spilled args (ABI-dependent).
- **Per thread:** each [[Thread]] has its own stack region.
- **Unwind:** debuggers walk frames for a [[Stack trace]].

## Technical Details

```txt
main frame → foo frame → bar frame
              ↑ stack pointer moves down on call, up on return
```

Overflow causes segmentation fault / stack overflow — not the same as [[Heap memory]] exhaustion. The [[stack pointer]] register tracks the current top.

## Real-World Applications

Crash dumps, profilers (`perf`), and language runtimes that allocate large locals or deep recursion budgets.

## Pros/Cons or Trade-offs

- **Pro:** Extremely cheap allocation/deallocation of locals.
- **Con:** Fixed or limited growth; deep recursion fails hard.
- **Trade-off:** large thread stacks (memory) vs smaller stacks (overflow risk).

## Comparison

- vs [[Heap memory]]: heap is explicit lifetime; stack is automatic with call lifetime.
- vs [[Stack trace]]: the trace is the *list* of frames at a moment.

## Mistakes to Avoid

- Huge VLAs / large arrays on the stack in hot server threads.
- Confusing stack overflow with heap OOM in postmortems.
- Stripping frame pointers and unwind info then expecting perfect traces.
