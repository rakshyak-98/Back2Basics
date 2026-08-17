[[Javascript]] [[JavaScript/Call stack]] [[promise]] [[event listener]]

# Asynchronous

> Async JS schedules work for later — callbacks, promises, async/await on the event loop, not OS threads by default.

```txt
        Asynchronous ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Async interviews cover promises/async-await, microtasks, and error propagatio…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
call stack empty → microtasks → next macrotask (timers, I/O)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Event loop** | Schedules turns | “One turn at a time.” |
| **Microtask** | Promise jobs | “Run before next render/timer.” |
| **async/await** | Promise syntax | “Awaitable thenables.” |
| **Concurrency vs parallelism** | Interleave vs multi-core | “Workers for CPU parallel.” |

## Technical Details
```js
async function load() {
  const res = await fetch('/api')
  return res.json()
}
load().catch(console.error)
```

| Knob | Why it matters |
|------|----------------|
| Error handling | Rejected promises |
| Cancellation | AbortController |
| Queue choice | micro vs macro ordering |

## Mistakes to Avoid
> [!WARNING]
> **await in a loop** — serializes; use `Promise.all` when safe.

> [!WARNING]
> **Floating promises** — fire-and-forget without catch hides failures.

| Symptom | Check | Fix |
|---------|-------|-----|
| UnhandledRejection | missing catch | catch / tryawait |
| Race UI | unordered awaits | sequence or lock |
| Starvation | long sync | chunk work |
| Zalgo | sync sometimes callback | Always async or always sync |

## Pros/Cons or Trade-offs
- **Pure CPU crunch on main thread** — worker.
- **Truly parallel shared-memory needs** — careful Atomics / WASM / native.
