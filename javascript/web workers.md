[[NodeJS]] [[worker threads]] [[ServiceWorker]] [[Event Loop]] [[content security policy]] [[web worker]] [[Descriptive/JavaScript/Concurrency]]

# Web Workers

> Web Workers — the browser's main thread owns the DOM, layout, paint, and the Event Loop. A Web Worker is a separate JS execution context with

```txt
        Web Workers ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Web Workers** to see if you understand what it does oper…

## Sources
- [MDN — Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) — deep-dive
- [Wikipedia — web workers](https://en.wikipedia.org/wiki/web_workers) — overview

## Key Concepts
- **The browser's:** The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]]…
- **Communication is:** Communication is **async message passing** via `postMessage` / `onmessage`
- **Types: -:** Types: - **Dedicated Worker**


- **Core:** The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]]…

## Technical Details
- The browser's main thread owns the DOM, layout, paint, and the [[Event Loop]].
- A **Web Worker** is a separate JS execution context with its own event loop

```
Main thread                    Worker thread
─────────────                  ─────────────
UI, DOM, fetch                 CPU work, parsing, crypto
     │                              ▲
     │  postMessage(data)           │
     └──────────────────────────────┘
     structured clone (copy by default)
```

- Communication is **async message passing** via `postMessage` / `onmessage`.
- Data is copied with the structured clone algorithm (or transferred for `Array…
- Workers die when terminated or when the creating document navigates away (unl…

- **Dedicated Worker:** — one owner (`new Worker(url)`).
- **SharedWorker:** — shared across same-origin tabs.
- **Service Worker:** — network/cache proxy; see [[ServiceWorker]] (different lifecycle).

### Dedicated worker

- **worker.js:** 

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

- **main.js:** 

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

- Worker script must be same-origin or explicitly allowed:

```
Content-Security-Policy: worker-src 'self' https://cdn.example.com;
```

- See [[content security policy]].

## Mistakes to Avoid
- **Mistake:** **No DOM, no sync APIs**
- **Mistake:** **Structured clone cost**
- **Mistake:** **React/Vue lifecycle**
- **Mistake:** **Error visibility**
- **Worker never starts:** check DevTools::** → Console for CSP / MIME errors
- **Mistake:** **`postMessage` throws or hangs:** check Object contains functio…
- **Mistake:** **Worker works locally, fails in prod:** check Bundler inlines w…
- **Mistake:** **UI still janky:** check Heavy work still on main thread
- **Mistake:** **Memory grows unbounded:** check Workers not terminated
- **Mistake:** **`importScripts` fails in module worker:** check Mixed classic …

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Web Workers — the browser's main thread owns the DOM, layout, paint, and the Eve…).
- **Con / when not:** **I/O-bound work**
- **Con / when not:** **Tiny computations**
- **Con / when not:** **DOM updates**
- **Con / when not:** **Need persistent background sync**
- **Con / when not:** **Node.js backend**

## Comparison
- vs [[worker threads]]: know when each applies


### Use cases
- In production APIs and tooling, **web workers** shows up whenever teams ship …
