[[NodeJS]] [[worker threads]] [[ServiceWorker]] [[Event Loop]] [[content security policy]]

# Web Workers

> Run JavaScript off the main thread so UI stays responsive during CPU-heavy work — **HTML Living Standard / WHATWG**.

## Mental model

The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]]. A **Web Worker** is a separate JS execution context with its own event loop — no DOM access, no `window`, no shared mutable state by default.

```
Main thread                    Worker thread
─────────────                  ─────────────
UI, DOM, fetch                 CPU work, parsing, crypto
     │                              ▲
     │  postMessage(data)           │
     └──────────────────────────────┘
     structured clone (copy by default)
```

Communication is **async message passing** via `postMessage` / `onmessage`. Data is copied with the structured clone algorithm (or transferred for `ArrayBuffer`). Workers die when terminated or when the creating document navigates away (unless `SharedWorker`).

Types:
- **Dedicated Worker** — one owner (`new Worker(url)`).
- **SharedWorker** — shared across same-origin tabs.
- **Service Worker** — network/cache proxy; see [[ServiceWorker]] (different lifecycle).

## Standard config / commands

### Dedicated worker

**worker.js**
```js
// No DOM — use self / globalThis
self.onmessage = (e) => {
  const result = heavyCompute(e.data);
  self.postMessage(result);
};

function heavyCompute(n) {
  // CPU-bound: parsing, compression, ML inference, etc.
  return n * n;
}
```

**main.js**
```js
const worker = new Worker(
  new URL('./worker.js', import.meta.url), // bundler-friendly (Vite/Webpack)
  { type: 'module' } // ES modules in worker (modern browsers)
);

worker.onmessage = (e) => console.log('result', e.data);
worker.onerror = (e) => console.error(e.message, e.filename, e.lineno);

worker.postMessage({ payload: 42 });

// Cleanup when done
worker.terminate();
```

### Transferable buffers (zero-copy)

```js
const buf = new ArrayBuffer(1024);
worker.postMessage({ buf }, [buf]); // buf is neutered in sender
```

### Inline worker (blob URL — dev only)

```js
const code = `self.onmessage = e => self.postMessage(e.data * 2);`;
const worker = new Worker(URL.createObjectURL(new Blob([code])));
```

### CSP requirement

Worker script must be same-origin or explicitly allowed:

```
Content-Security-Policy: worker-src 'self' https://cdn.example.com;
```

See [[content security policy]].

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Worker never starts | DevTools → Console for CSP / MIME errors | Serve `.js` as `application/javascript`; fix `worker-src` |
| `postMessage` throws or hangs | Object contains functions, DOM nodes, or circular refs | Send plain data; use transfer list for buffers |
| Worker works locally, fails in prod | Bundler inlines worker path wrong | Use `new URL('./worker.js', import.meta.url)` or bundler worker plugin |
| UI still janky | Heavy work still on main thread | Move compute to worker; batch messages; avoid huge clones |
| Memory grows unbounded | Workers not terminated; large messages cloned every frame | `terminate()` on unmount; transfer buffers; throttle posts |
| `importScripts` fails in module worker | Mixed classic vs module worker | Pick one: `{ type: 'module' }` with `import`, or classic + `importScripts` |
| SharedWorker unavailable | Safari / some mobile WebViews | Fall back to dedicated worker or main-thread chunking |

## Gotchas

> [!WARNING]
> **No DOM, no sync APIs** — `document`, `localStorage` (in dedicated workers use `WorkerGlobalScope` APIs), and blocking sync XHR are unavailable. Use `fetch` + async patterns.

> [!WARNING]
> **Structured clone cost** — posting a 10 MB object copies it. For large binary data, **transfer** `ArrayBuffer` or use [[SharedArrayBuffer]] + Atomics (requires cross-origin isolation headers).

> [!WARNING]
> **React/Vue lifecycle** — create worker once per logical job or pool workers; always `terminate()` in `useEffect` cleanup to avoid zombie threads and duplicate handlers.

> [!WARNING]
> **Error visibility** — uncaught errors in workers fire `worker.onerror`, not your app's global handler. Wire `onerror` and optionally `worker.addEventListener('messageerror', ...)`.

## When NOT to use

- **I/O-bound work** — workers don't make network/disk faster; use async `fetch` on the main thread or server-side processing.
- **Tiny computations** — message-passing overhead can exceed the savings for sub-millisecond tasks.
- **DOM updates** — workers can't touch the DOM; post results back and render on main thread.
- **Need persistent background sync** — use [[ServiceWorker]] or server push, not a dedicated worker.
- **Node.js backend** — use [[worker threads]] (shared memory, different API).

## Related

[[web worker]] [[NodeJS]] [[worker threads]] [[ServiceWorker]] [[Event Loop]] [[content security policy]] [[Descriptive/JavaScript/Concurrency]]
