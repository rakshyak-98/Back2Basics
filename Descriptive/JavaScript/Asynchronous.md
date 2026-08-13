<!-- note-strategy: operational -->
[[Javascript]] [[JavaScript/Call stack]] [[promise]]

# Asynchronous

> Async JS schedules work for later — callbacks, promises, async/await on the event loop, not OS threads by default.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Start I/O, return to the loop; when ready, a microtask/task runs a fresh stack. `await` pauses the async function, not the whole runtime.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| UnhandledRejection | missing catch | catch / tryawait |
| Race UI | unordered awaits | sequence or lock |
| Starvation | long sync | chunk work |
| Zalgo | sync sometimes callback | Always async or always sync |

---

## Gotchas

> [!WARNING]
> **await in a loop** — serializes; use `Promise.all` when safe.

> [!WARNING]
> **Floating promises** — fire-and-forget without catch hides failures.

---

## When NOT to use

- **Pure CPU crunch on main thread** — worker.
- **Truly parallel shared-memory needs** — careful Atomics / WASM / native.

## Related

[[promise]] [[JavaScript/Call stack]] [[event listener]]
