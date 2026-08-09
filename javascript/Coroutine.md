[[javascript]] [[promise]] [[Callback]]

# Coroutine

> Cooperative multi-step function — pause with `yield`/`await` and resume later (generators + async).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Interview map (words you can say)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A generator coroutine yields control; the caller decides when to `.next()` again. `async/await` is the mainstream coroutine style over Promises.

```txt
function* gen() { yield 1; yield 2 }
const it = gen(); it.next() → { value:1, done:false }
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **generator** | `function*` + `yield` | “Lazy sequence / pauseable fn.” |
| **async fn** | Await-based coroutine | “Most app code uses this.” |
| **cooperative** | Yields deliberately | “Not preemptive threads.” |

## Standard config / commands

```js
function* range(n) {
  for (let i = 0; i < n; i++) yield i
}

async function load() {
  const a = await fetch('/a')
  const b = await fetch('/b')
  return [a, b]
}
```

| Knob | Why it matters |
|------|----------------|
| `yield*` | Delegate to another generator |
| `for await` | Async iterables |
| Redux-saga style | Generators for side-effect DSLs |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Generator stuck | Nobody calling `.next` | Drive the iterator |
| Mixing async+gen wrongly | Complexity | Prefer async functions |
| Infinite yield loop | No break | Bound loops |
| Memory hold | Long-lived generator | Close iterators (`return`) |

---

## Gotchas

> [!WARNING]
> **Generators aren’t threads** — one JS call stack still; yield just pauses the function.

> [!WARNING]
> **Saga/middleware DSLs** — powerful but opaque; document effects.

---

## When NOT to use

- **Simple async flows** — `async/await` only.
- **Parallel CPU** — workers/processes, not coroutines.

---

## Related

[[promise]] [[Callback]] [[async utils]]
