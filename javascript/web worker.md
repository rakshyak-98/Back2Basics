[[javascript]] [[worker]] [[throttle]] [[Optimizing performance]]

# web worker

> Background JS thread in the browser — keep heavy CPU off the UI thread; talk via `postMessage`.

## Interview Relevance

Interviewers use **web worker** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Dedicated worker**, **SharedWorker**, **transfer**.

## Sources

- [MDN — Using web workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) — deep-dive
- [Wikipedia — web worker](https://en.wikipedia.org/wiki/web_worker) — overview

## Key Concepts

- **Dedicated worker:** One script page owns — Classic CPU offload.
- **SharedWorker:** Multi-tab — Less common; different API.
- **transfer:** Move buffer ownership — Zero-copy large data.

## Technical Details

```txt
main ──postMessage──► Worker
     ◄──onmessage────
```

```js
const w = new Worker(new URL('./heavy.js', import.meta.url), { type: 'module' })
w.postMessage({ op: 'fib', n: 42 })
w.onmessage = (e) => console.log(e.data)
w.onerror = console.error
```

| Knob | Why it matters |
|------|----------------|
| Module workers | `import` inside worker |
| Transfer list | `[buffer]` second arg |
| Terminate | `w.terminate()` on unmount |

## Real-World Applications

In production APIs and tooling, **web worker** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **No DOM / `window`** in workers — pass results back to main to render; **Vite/webpack** need correct worker URL patterns — don’t string-path casually.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Background JS thread in the browser — keep heavy CPU off the UI thread; talk via…).
- **Con / when not:** **Tiny work** — message overhead can dominate.
- **Con / when not:** **Network-only waits** — async I/O already frees the UI.

## Comparison

vs [[worker]]: know when each applies — do not treat them as interchangeable. vs [[throttle]]: know when each applies — do not treat them as interchangeable. vs [[Optimizing performance]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **No DOM / `window`** in workers — pass results back to main to render.
- **Vite/webpack** need correct worker URL patterns — don’t string-path casually.
- **UI still janky:** check Work still on main; fix: Move loop into worker
- **DataCloneError:** check Non-cloneable payload; fix: Transfer buffers; plain data
- **Worker 404:** check Wrong URL / bundler; fix: Use `new URL(..., import.meta.url)`
- **Memory leak:** check Workers never terminated; fix: Terminate on page leave
