[[javascript]] [[worker]] [[throttle]] [[Optimizing performance]]

# web worker

> Background JS thread in the browser — keep heavy CPU off the UI thread; talk via `postMessage`.

```txt
        web worker ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **web worker** to check whether you can explain the mechanis…

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

## Mistakes to Avoid
- **Mistake:** **No DOM / `window`** in workers
- **Mistake:** **Vite/webpack** need correct worker URL patterns
- **Mistake:** **UI still janky:** check Work still on main
- **Mistake:** **DataCloneError:** check Non-cloneable payload
- **Mistake:** **Worker 404:** check Wrong URL / bundler
- **Mistake:** **Memory leak:** check Workers never terminated

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Background JS thread in the browser — keep heavy CPU off the UI thread; talk via…).
- **Con / when not:** **Tiny work** — message overhead can dominate.
- **Con / when not:** **Network-only waits** — async I/O already frees the UI.

## Comparison
- vs [[worker]]: know when each applies


### Use cases
- In production APIs and tooling, **web worker** shows up whenever teams ship N…
