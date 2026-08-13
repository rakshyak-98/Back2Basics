[[Javascript]] [[JavaScript/Asynchronous]] [[JavaScript/execution context]]

# Call stack

> The call stack tracks nested function frames — push on call, pop on return; overflow when recursion is too deep.

---

## How it works

```txt
main → a → b → c   then pop c,b,a
async: stack clears → task/microtask → new stack
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Frame** | One function activation | “Locals + return addr.” |
| **Stack overflow** | Too deep recursion | “Convert to loop / trampoline.” |
| **Stack trace** | Frames for errors | “Source maps help.” |
| **Event loop** | Schedules next stack | “Promises ≠ new threads.” |

---


## Configuration and commands

```js
function a() { b() }
function b() { throw new Error('x') }
try { a() } catch (e) { console.log(e.stack) }
```

| Knob | Why it matters |
|------|----------------|
| Async boundaries | New stacks; lost sync context |
| `Error.stack` | Debugging |
| Tail calls | Not reliably optimized in JS |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Maximum call stack | unbounded recursion | Iterate; increase? no — redesign |
| Useless async stack | lost context | async hooks / better logs |
| Silent hang | busy sync loop | Yield to event loop |

---


## Gotchas

> [!WARNING]
> **“Async = other thread”** — still one JS stack at a time on the main thread.

> [!WARNING]
> **Heavy sync work** — blocks rendering/input even with empty microtask queue.

---


## When not to use

- **CPU-bound parallelism** — workers.
- **Deep recursion algorithms** — prefer explicit stacks/loops in JS.


## Related

[[JavaScript/Asynchronous]] [[JavaScript/execution context]] [[Stack trace]]

## Sources

- [Wikipedia — Call stack](https://en.wikipedia.org/wiki/Call_stack)
