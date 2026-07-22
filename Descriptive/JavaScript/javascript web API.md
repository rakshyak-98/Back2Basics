[[javascript]] [[NodeJS/Event Loop]] [[Networking/webSocket]] [[Security/CORS (Cross Origin Request Sharing)]]

# JavaScript Web APIs

> Browser and runtime surfaces beyond ECMAScript — DOM, fetch, timers, storage — **MDN + integration debugging**.

## Mental model

**ECMAScript** defines the language (syntax, Promise, Map). **Web APIs** (browser) and **Node APIs** (`fs`, `http`) are host-provided, often asynchronous, and bound to the event loop.

```
Your JS
   │
   ├── ECMAScript (language)
   │
   └── Host APIs
         Browser: DOM, fetch, localStorage, WebSocket
         Node:    fs, http, setImmediate, process
```

Same name, different host: `fetch` exists in modern Node and all browsers; `setImmediate` is Node-only; `requestAnimationFrame` is browser-only.

## Standard config / commands

### Fetch (browser + Node 18+)

```javascript
const res = await fetch('https://api.example.com/users', {
  method: 'GET',
  headers: { Accept: 'application/json' },
  signal: AbortSignal.timeout(5000),
});
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const users = await res.json();
```

### Timers (browser)

```javascript
const id = setTimeout(() => {}, 1000);
clearTimeout(id);

requestAnimationFrame((ts) => {
  // runs before next repaint (~60Hz)
});
```

### Node: `setImmediate` vs `setTimeout(0)`

```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
// Order varies at top level; after I/O, immediate usually first
```

### Storage (browser)

```javascript
localStorage.setItem('theme', 'dark');   // sync, ~5MB, same origin
sessionStorage.setItem('tab', '1');      // per tab
// Prefer structured + versioned JSON; handle QuotaExceededError
```

### WebSocket

```javascript
const ws = new WebSocket('wss://example.com/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.send(JSON.stringify({ type: 'ping' }));
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CORS error on fetch | Response headers | Server `Access-Control-Allow-Origin`; see [[Security/CORS (Cross Origin Request Sharing)]] |
| `fetch failed` Node | TLS, DNS, cert | `NODE_EXTRA_CA_CERTS`; verify URL |
| Timer never fires | Tab throttled (background) | `visibilitychange`; Web Worker for critical timers |
| `localStorage` null | Private mode / SSR | Feature detect; server-side session |
| WebSocket closes 1006 | Proxy idle timeout | Heartbeat ping; reverse proxy read timeout |

## Gotchas

> [!WARNING]
> Many Web APIs return **Promises** but DOM legacy APIs use callbacks — mixing styles without `await` causes race bugs.

- **`fetch` does not reject on 404** — check `res.ok`.
- **Third-party cookie phase-out** affects storage partitioning — test Safari/Firefox.
- **Node `fetch` undici** — connection pooling differs from `axios`; tune `agent` for high throughput.

## When NOT to use

- Heavy file I/O in browser — use streams + download, not read entire blob into memory.
- Replacing REST with WebSocket for simple CRUD — HTTP caching wins.

## Related

[[javascript]] [[NodeJS/Event Loop]] [[Networking/webSocket]] [[javascript/Session Storage]]
