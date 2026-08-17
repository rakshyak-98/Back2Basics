[[Operating System]] [[Stack Frame]] [[stack pointer]] [[process]] [[gdb]]

# Stack trace

> A stack trace lists the chain of function calls at a moment — the first map when a program crashes, deadlocks, or logs an exception.

```txt
        Stack trace ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Debugging reviews: read a trace top-to-bottom, know you need symbols, and …

## Sources
- Kerrisk, *The Linux Programming Interface* — core dumps — deep-dive
- Linux `backtrace(3)`, `gdb(1)` manual pages — deep-dive
- [Wikipedia — Stack trace](https://en.wikipedia.org/wiki/Stack_trace) — overview

## Key Concepts
- **Unwind:** walk [[Stack Frame]]s via frame pointers or `.eh_frame` unwind tables.
- **Symbols:** `-g` or debuginfo packages resolve addresses to names/lines.
- **Tools:** `gdb bt`, language dumps, `pstack`, profilers.
- **Kernel oops:** kernel stack, not the user [[process]] stack.

## Technical Details
```txt
#0  crash() at bug.c:12
#1  handle() at srv.c:88
#2  main() at srv.c:40
```

- Generated at exceptions, signals, or attached debuggers.
- Missing symbols produce only hex addresses.

## Mistakes to Avoid
- **Mistake:** Reading only the top frame and ignoring the real root cause lowe…
- **Mistake:** Shipping fully stripped binaries with no debuginfo mapping
- **Mistake:** Mixing kernel oops lines into a user-space analysis without noti…

## Pros/Cons or Trade-offs
- **Pro:** Immediate narrative of “how we got here”.
- **Con:** Optimized/inlined code can omit or confuse frames.
- **Trade-off:** keeping debug symbols (disk/security) vs faster postmortems.

## Comparison
- vs [[Stack Frame]]: frame is one call’s data; trace is the chain.
- vs core dump: dump is full memory; trace is the derived call list.


### Use cases
- Production crash reporting (Sentry, Breakpad), SRE on-call paste from `gdb`, …
