[[javascript]] [[promise]] [[Callback]] [[async utils]]

# Coroutine

> Cooperative multi-step function — pause with `yield`/`await` and resume later (generators + async).

```txt
        Coroutine ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Coroutine** to check whether you can explain the mechanism…

## Sources
- [Wikipedia — Coroutine](https://en.wikipedia.org/wiki/Coroutine) — overview

## Key Concepts
- **generator:** `function*` + `yield` — Lazy sequence / pauseable fn.
- **async fn:** Await-based coroutine — Most app code uses this.
- **cooperative:** Yields deliberately — Not preemptive threads.

## Technical Details
```txt
function* gen() { yield 1; yield 2 }
const it = gen(); it.next() → { value:1, done:false }
```

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

## Mistakes to Avoid
- **Mistake:** **Generators aren’t threads**
- **Mistake:** **Saga/middleware DSLs** — powerful but opaque; document effects
- **Mistake:** **Generator stuck:** check Nobody calling `.next`
- **Mistake:** **Mixing async+gen wrongly:** check Complexity
- **Mistake:** **Infinite yield loop:** check No break; fix: Bound loops
- **Mistake:** **Memory hold:** check Long-lived generator

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Cooperative multi-step function — pause with `yield`/`await` and resume later (g…).
- **Con / when not:** **Simple async flows** — `async/await` only.
- **Con / when not:** **Parallel CPU** — workers/processes, not coroutines.

## Comparison
- vs [[promise]]: know when each applies


### Use cases
- In production APIs and tooling, **Coroutine** shows up whenever teams ship No…
