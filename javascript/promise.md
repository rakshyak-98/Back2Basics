[[javascript]] [[Callback]] [[async utils]] [[Coroutine]]

# promise

> Object for a future value — pending then fulfilled or rejected; `async/await` is syntax over the same machinery.

## Interview Relevance

Interviewers use **promise** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **thenable**, **microtask**, **all / allSettled / race**.

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

## Real-World Applications

In production APIs and tooling, **promise** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Executor runs sync** — `new Promise((res) => { throw })` rejects; sync throw inside async fn rejects the returned promise; **`.then` without return** — next then gets `undefined`.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Object for a future value — pending then fulfilled or rejected; `async/await` is…).
- **Con / when not:** **Sync pure computation** — just return the value.
- **Con / when not:** **Event streams** — Observables/EventTarget may fit better.

## Comparison

vs [[Callback]]: Promises chain and surface rejection; raw callbacks need explicit error-first discipline. vs [[async utils]]: know when each applies — do not treat them as interchangeable. vs [[Coroutine]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Executor runs sync** — `new Promise((res) => { throw })` rejects; sync throw inside async fn rejects the returned promise.
- **`.then` without return** — next then gets `undefined`.
- **Unhandled rejection:** check Missing catch/await; fix: Always handle
- **Swallow then continue wrong:** check Empty catch; fix: Rethrow or return Result
- **Race wrong winner:** check Used `race` for timeout poorly; fix: AbortSignal pattern
- **Floating promise:** check fire-and-forget; fix: void + catch or await
