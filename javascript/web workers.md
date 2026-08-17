[[NodeJS]] [[worker threads]] [[ServiceWorker]] [[Event Loop]] [[content security policy]] [[Descriptive/JavaScript/Concurrency]]

# Web Workers

> A Web Worker runs JavaScript in a background thread separate from the browser's main thread — enabling CPU-heavy work without blocking DOM updates, layout, or user input.

---

## Why It Matters

The browser main thread owns the DOM, layout, paint, and the JavaScript event loop. A long-running computation (parsing a large CSV, image processing, cryptography, ML inference) on the main thread freezes the UI — scroll stutters, clicks queue, and the tab shows "page unresponsive." Web Workers move that work to a parallel thread with its own event loop, communicating back via asynchronous `postMessage`.

---

## Sources

- [MDN — Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) — Complete API reference for Dedicated, Shared, and Service Workers with browser compatibility.
- [MDN — Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) — Step-by-step tutorial with `postMessage`, transferable objects, and error handling.
- [HTML Standard — Workers](https://html.spec.whatwg.org/multipage/workers.html) — Normative specification for worker lifecycle, origin model, and structured clone algorithm.
- [MDN — Content Security Policy worker-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src) — CSP directive required to allow worker scripts from specific origins.

---

## Key Concepts

```txt
Main thread                    Worker thread
─────────────                  ─────────────
UI, DOM, fetch                 CPU work, parsing, crypto
     │                              ▲
     │  postMessage(data)           │
     └──────────────────────────────┘
     structured clone (copy) or Transferable (zero-copy)
```

| Worker type | Scope | Use case |
|-------------|-------|----------|
| **Dedicated Worker** | One owner document | `new Worker(url)` — general background compute |
| **SharedWorker** | Same-origin tabs | Rare — shared connection to server |
| **Service Worker** | Origin-wide | Offline cache, push notifications — see [[ServiceWorker]] |

| Constraint | Detail |
|------------|--------|
| **No DOM** | Workers cannot access `document`, `window`, or most Web APIs tied to UI. |
| **Message passing only** | All communication is async via `postMessage` / `onmessage`. |
| **Structured clone** | Data is copied by default — large objects are expensive to send. |
| **Transferable** | `ArrayBuffer` can be transferred (neutered in sender) for zero-copy. |
| **Lifecycle** | Worker dies on `terminate()` or when the creating document navigates away. |

---

## Technical Details

### Dedicated worker

**worker.js** (no DOM — use `self`):

```javascript
self.onmessage = (e) => {
  const result = heavyCompute(e.data);
  self.postMessage(result);
};

function heavyCompute(n) {
  // CPU-bound: parsing, compression, ML inference
  let sum = 0;
  for (let i = 0; i < n; i++) sum += Math.sqrt(i);
  return sum;
}
```

**main.js**:

```javascript
const worker = new Worker(
  new URL('./worker.js', import.meta.url), // bundler-friendly (Vite/Webpack)
  { type: 'module' }                        // ES modules in worker
);

worker.onmessage = (e) => console.log('result', e.data);
worker.onerror = (e) => console.error(e.message, e.filename, e.lineno);
worker.postMessage(10_000_000);

worker.terminate(); // cleanup when done
```

### Transferable buffers (zero-copy)

```javascript
const buf = new ArrayBuffer(1024 * 1024);
worker.postMessage({ buf }, [buf]); // buf is neutered in sender — zero copy
```

### Inline worker (development only)

```javascript
const code = `self.onmessage = e => self.postMessage(e.data * 2);`;
const worker = new Worker(URL.createObjectURL(new Blob([code])));
```

### CSP requirement

```
Content-Security-Policy: worker-src 'self' https://cdn.example.com;
```

Worker script must be same-origin or explicitly allowed. See [[content security policy]].

### Failure signals

| Symptom | Cause | Fix |
|---------|-------|-----|
| Worker never starts | CSP blocks script | Add `worker-src` directive |
| `postMessage` throws | Object contains functions or DOM nodes | Send plain data only |
| Works locally, fails in prod | Bundler path wrong | Use `new URL('./worker.js', import.meta.url)` |
| UI still janky | Heavy work still on main thread | Profile — verify worker is actually used |
| Memory grows | Workers not terminated | Call `terminate()` when done |

---

## Mistakes to Avoid

- Passing DOM nodes or functions through `postMessage` — structured clone rejects them.
- Sending large objects without Transferable — copies are expensive.
- Keeping workers alive indefinitely — memory leak on SPA navigations.
- Using workers for I/O-bound work — `fetch` on main thread is already async; workers help CPU-bound.
- Confusing Dedicated Workers with Service Workers — different lifecycle and APIs.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Keeps UI responsive during CPU work | No DOM access — message-passing overhead |
| True parallel execution on multi-core | Startup cost per worker |
| Sandboxed from main thread globals | Harder to debug than main-thread code |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[worker threads]] (Node.js) | Node worker_threads — server-side; shares no browser APIs |
| [[ServiceWorker]] | Persistent network proxy — different lifecycle and purpose |
| `requestIdleCallback` | Runs on main thread during idle — not parallel |
| WebAssembly in worker | Even faster for compute-heavy numeric work |

---

## Use cases

- Parsing a 50 MB CSV upload without freezing the upload progress UI.
- Image thumbnail generation in a photo editor.
- Client-side PDF rendering or cryptography in a zero-knowledge app.
- Offloading regex-heavy log parsing in a browser-based log viewer.
