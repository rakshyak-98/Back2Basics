[[javascript]] [[Callback]] [[async utils]] [[Coroutine]]

# promise

> Object for a future value — pending then fulfilled or rejected; `async/await` is syntax over the same machinery.

```txt
        promise ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **promise** to check whether you can explain the mechanism i…

## Sources
- [MDN — Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) — deep-dive
- [ECMA-262 — Promise Objects](https://tc39.es/ecma262/#sec-promise-objects) — overview
- [Wikipedia — promise](https://en.wikipedia.org/wiki/promise) — overview

## Key Concepts
- **thenable:** Has `.then` — Awaited like a Promise.
- **microtask:** then/await queue — Runs before next macrotask (timers).
- **all / allSettled / race:** Combine promises — all = fail-fast; settled = gather.

## Technical Details
```txt
pending → fulfilled(value) | rejected(reason)
```

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

## Mistakes to Avoid
- **Mistake:** **Executor runs sync**
- **Mistake:** **`.then` without return** — next then gets `undefined`
- **Mistake:** **Unhandled rejection:** check Missing catch/await
- **Mistake:** **Swallow then continue wrong:** check Empty catch
- **Mistake:** **Race wrong winner:** check Used `race` for timeout poorly
- **Mistake:** **Floating promise:** check fire-and-forget

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Object for a future value — pending then fulfilled or rejected; `async/await` is…).
- **Con / when not:** **Sync pure computation** — just return the value.
- **Con / when not:** **Event streams**

## Comparison
- vs [[Callback]]: Promises chain and surface rejection; raw callbacks need exp…


### Use cases
- In production APIs and tooling, **promise** shows up whenever teams ship Node…
