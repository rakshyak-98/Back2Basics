[[Javascript]] [[JavaScript/Asynchronous]] [[JavaScript/execution context]] [[Stack trace]]

# Call stack

> The call stack tracks nested function frames — push on call, pop on return; overflow when recursion is too deep.

## Interview Relevance

Call stack questions check frames, stack overflow, and relation to the event loop/queue.

## Sources

- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [Call stack — Wikipedia](https://en.wikipedia.org/wiki/Call_stack) — overview

## Key Concepts

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

## Technical Details

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

## Pros/Cons or Trade-offs

- **CPU-bound parallelism** — workers.
- **Deep recursion algorithms** — prefer explicit stacks/loops in JS.

## Mistakes to Avoid

> [!WARNING]
> **“Async = other thread”** — still one JS stack at a time on the main thread.

> [!WARNING]
> **Heavy sync work** — blocks rendering/input even with empty microtask queue.

| Symptom | Check | Fix |
|---------|-------|-----|
| Maximum call stack | unbounded recursion | Iterate; increase? no — redesign |
| Useless async stack | lost context | async hooks / better logs |
| Silent hang | busy sync loop | Yield to event loop |

