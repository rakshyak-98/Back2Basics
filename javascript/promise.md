[[javascript]] [[Callback]] [[async utils]]

# promise

> Object for a future value — pending then fulfilled or rejected; `async/await` is syntax over the same machinery.

---

## How it works

```txt
pending → fulfilled(value) | rejected(reason)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **thenable** | Has `.then` | “Awaited like a Promise.” |
| **microtask** | then/await queue | “Runs before next macrotask (timers).” |
| **all / allSettled / race** | Combine promises | “all = fail-fast; settled = gather.” |


## Configuration and commands

```js
const p = fetch('/api').then((r) => r.json())
const data = await p

await Promise.all([a(), b()])
await Promise.allSettled([a(), b()])
```

| Knob | Why it matters |
|------|----------------|
| `finally` | Cleanup either way |
| `Promise.resolve/reject` | Wrap values |
| Avoid `new Promise` for already-async | Don’t wrap `fetch` needlessly |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Unhandled rejection | Missing catch/await | Always handle |
| Swallow then continue wrong | Empty catch | Rethrow or return Result |
| Race wrong winner | Used `race` for timeout poorly | AbortSignal pattern |
| Floating promise | fire-and-forget | void + catch or await |

---


## Gotchas

> [!WARNING]
> **Executor runs sync** — `new Promise((res) => { throw })` rejects; sync throw inside async fn rejects the returned promise.

> [!WARNING]
> **`.then` without return** — next then gets `undefined`.

---


## When not to use

- **Sync pure computation** — just return the value.
- **Event streams** — Observables/EventTarget may fit better.

---


## Related

[[Callback]] [[async utils]] [[Coroutine]]

## Sources

- [Wikipedia — promise](https://en.wikipedia.org/wiki/promise)
