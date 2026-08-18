[[javascript]] [[worker]] [[throttle]]

# web worker

> Background JS thread in the browser — keep heavy CPU off the UI thread; talk via `postMessage`.

## Mental model

**Say it in one breath:** Main thread owns DOM; Worker owns compute. Structured-clone messages (or transfer ArrayBuffers). No direct DOM access from the worker.

```txt
main ──postMessage──► Worker
     ◄──onmessage────
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Dedicated worker** | One script page owns | “Classic CPU offload.” |
| --- | --- | --- |
| **SharedWorker** | Multi-tab | “Less common; different API.” |
| **transfer** | Move buffer ownership | “Zero-copy large data.” |

## Standard config / commands

```js
const w = new Worker(new URL('./heavy.js', import.meta.url), { type: 'module' })
w.postMessage({ op: 'fib', n: 42 })
w.onmessage = (e) => console.log(e.data)
w.onerror = console.error
```

| Knob | Why it matters |

| Module workers | `import` inside worker |
| --- | --- |
| Transfer list | `[buffer]` second arg |
| Terminate | `w.terminate()` on unmount |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| UI still janky | Work still on main | Move loop into worker |
| DataCloneError | Non-cloneable payload | Transfer buffers; plain data |
| Worker 404 | Wrong URL / bundler | Use `new URL(..., import.meta.url)` |
| Memory leak | Workers never terminated | Terminate on page leave |

## Gotchas

> [!WARNING]
> **No DOM / `window`** in workers — pass results back to main to render.

> [!WARNING]
> **Vite/webpack** need correct worker URL patterns — don’t string-path casually.

## When NOT to use

- **Tiny work** — message overhead can dominate.
- **Network-only waits** — async I/O already frees the UI.

## Related

[[throttle]] [[worker]] [[Optimizing performance]]
