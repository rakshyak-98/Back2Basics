[[Operating System]] [[stack pointer]] [[Stack trace]] [[Thread]] [[Heap memory]]

# Stack Frame

> A stack frame is the block of memory a function call pushes — return address, saved registers, locals — nested in LIFO order on the thread stack.

Call sequence:

```txt
main frame → foo frame → bar frame
              ↑ stack pointer moves down on call, up on return
```

Each [[Thread]] has a fixed or growable stack region; overflow causes segmentation fault — not to be confused with [[Heap memory]] exhaustion.

Debuggers unwind frames to print [[Stack trace]] after crashes.

## Sources

- Bryant & O’Hallaron, *Computer Systems* — procedure call convention
- Wikipedia: [Call stack](https://en.wikipedia.org/wiki/Call_stack)
