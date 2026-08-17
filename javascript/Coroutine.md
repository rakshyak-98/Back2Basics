[[javascript]] [[promise]] [[Callback]] [[async utils]]

# Coroutine

> Cooperative multi-step function — pause with `yield`/`await` and resume later (generators + async).





## Interview Relevance
Interviewers use **Coroutine** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **generator**, **async fn**, **cooperative**.

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

## Real-World Applications
In production APIs and tooling, **Coroutine** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Generators aren’t threads** — one JS call stack still; yield just pauses the function; **Saga/middleware DSLs** — powerful but opaque; document effects.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Cooperative multi-step function — pause with `yield`/`await` and resume later (g…).
- **Con / when not:** **Simple async flows** — `async/await` only.
- **Con / when not:** **Parallel CPU** — workers/processes, not coroutines.

## Comparison
vs [[promise]]: know when each applies — do not treat them as interchangeable. vs [[Callback]]: know when each applies — do not treat them as interchangeable. vs [[async utils]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Generators aren’t threads** — one JS call stack still; yield just pauses the function.
- **Saga/middleware DSLs** — powerful but opaque; document effects.
- **Generator stuck:** check Nobody calling `.next`; fix: Drive the iterator
- **Mixing async+gen wrongly:** check Complexity; fix: Prefer async functions
- **Infinite yield loop:** check No break; fix: Bound loops
- **Memory hold:** check Long-lived generator; fix: Close iterators (`return`)
