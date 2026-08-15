[[NodeJS]] [[worker threads]] [[ServiceWorker]] [[Event Loop]] [[content security policy]] [[web worker]] [[Descriptive/JavaScript/Concurrency]]

# Web Workers

> Web Workers — the browser's main thread owns the DOM, layout, paint, and the Event Loop. A Web Worker is a separate JS execution context with

## Interview Relevance

Interviewers probe **Web Workers** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [MDN — Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) — deep-dive
- [Wikipedia — web workers](https://en.wikipedia.org/wiki/web_workers) — overview

## Core Definition

The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]]. A **Web Worker** is a separate JS execution context with its own event loop — no DOM access, no `window`, no shared mutable state by default.

## Key Concepts

- The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]]. A **Web Worker** is a separate JS execution context with its own event loop — no DOM access, no `w…
- Communication is **async message passing** via `postMessage` / `onmessage`. Data is copied with the structured clone algorithm (or transferred for `ArrayBuffer`). Workers die wh…
- Types: - **Dedicated Worker** — one owner (`new Worker(url)`). - **SharedWorker** — shared across same-origin tabs. - **Service Worker** — network/cache proxy; see [[ServiceWork…

## Technical Details

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

## Real-World Applications

In production APIs and tooling, **web workers** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **No DOM, no sync APIs** — `document`, `localStorage` (in dedicated workers use `WorkerGlobalScope` APIs), and blocking sync XHR are unavailable. Use `fetch` + async patterns; **Structured clone cost** — posting a 10 MB object copies it. For large binary data, **transfer** `ArrayBuffer` or use [[SharedArrayBuffer]] + Atomics (requires cross-origin isolation headers).

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Web Workers — the browser's main thread owns the DOM, layout, paint, and the Eve…).
- **Con / when not:** **I/O-bound work** — workers don't make network/disk faster; use async `fetch` on the main thread or server-side processing.
- **Con / when not:** **Tiny computations** — message-passing overhead can exceed the savings for sub-millisecond tasks.
- **Con / when not:** **DOM updates** — workers can't touch the DOM; post results back and render on main thread.
- **Con / when not:** **Need persistent background sync** — use [[ServiceWorker]] or server push, not a dedicated worker.
- **Con / when not:** **Node.js backend** — use [[worker threads]] (shared memory, different API).

## Comparison

vs [[worker threads]]: know when each applies — do not treat them as interchangeable. vs [[ServiceWorker]]: Web Worker = CPU off main thread; Service Worker = network/cache proxy with its own lifecycle. vs [[Event Loop]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **No DOM, no sync APIs** — `document`, `localStorage` (in dedicated workers use `WorkerGlobalScope` APIs), and blocking sync XHR are unavailable. Use `fetch` + async patterns.
- **Structured clone cost** — posting a 10 MB object copies it. For large binary data, **transfer** `ArrayBuffer` or use [[SharedArrayBuffer]] + Atomics (requires cross-origin isolation headers).
- **React/Vue lifecycle** — create worker once per logical job or pool workers; always `terminate()` in `useEffect` cleanup to avoid zombie threads and duplicate handlers.
- **Error visibility** — uncaught errors in workers fire `worker.onerror`, not your app's global handler. Wire `onerror` and optionally `worker.addEventListener('messageerror', ...)`.
- **Worker never starts:** check DevTools → Console for CSP / MIME errors; fix: Serve `.js` as `application/javascript`; fix `worker-src`
- **`postMessage` throws or hangs:** check Object contains functions, DOM nodes, or circular refs; fix: Send plain data; use transfer list for buffers
- **Worker works locally, fails in prod:** check Bundler inlines worker path wrong; fix: Use `new URL('./worker.js', import.meta.url)` or bundler worker plugin
- **UI still janky:** check Heavy work still on main thread; fix: Move compute to worker; batch messages; avoid huge clones
- **Memory grows unbounded:** check Workers not terminated; large messages cloned every frame; fix: `terminate()` on unmount; transfer buffers; throttle posts
- **`importScripts` fails in module worker:** check Mixed classic vs module worker; fix: Pick one: `{ type: 'module' }` with `import`, or classic + `importScripts`
