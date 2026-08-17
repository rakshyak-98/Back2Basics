[[CORS (Cross Origin Request Sharing)]] [[JWT authentication]] [[single-sign-on (SSO)]] [[webSocket]] [[IDOR]]

# Session Storage

> Session Storage — sessionStorage is a Storage object tied to a top-level browsing context (tab/window). Data survives page reloads and SPA navigations within the same tab

```txt
        Session Storage ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Session Storage** to check whether you can explain the mec…

## Sources
- [MDN — sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) — deep-dive
- [Wikipedia — Session Storage](https://en.wikipedia.org/wiki/Session_Storage) — overview

## Key Concepts
- **sessionStorage:** Tab — No
- **localStorage:** Until cleared — No
- **Cookie:** Configurable — Yes (auto)
- **Memory (React state):** Page — No


- **Core:** `sessionStorage` is a **`Storage` object** tied to a **top-level browsing con…

## Technical Details
- `sessionStorage` is a **`Storage` object** tied to a **top-level browsing con…
- Data survives **page reloads and SPA navigations** within the same tab, but d…
- It is **origin-scoped** (`scheme + host + port`) like `localStorage`.

```txt
Tab A (origin app.example.com)
  sessionStorage.setItem('draft', ...)
  reload / router push → still there
  close tab → gone

Tab B (same origin) → separate sessionStorage (not shared)
```

| Store | Lifetime | Sent to server | Size (~) | XSS impact |
|-------|----------|----------------|----------|------------|
| **sessionStorage** | Tab | No | ~5MB | Full read if XSS |
| **localStorage** | Until cleared | No | ~5MB | Full read if XSS |
| **Cookie** | Configurable | Yes (auto) | ~4KB | HttpOnly mitigates JS read |

- **Not a session mechanism for authentication:** 
- authentication sessions use **HttpOnly Secure cookies** or **Bearer tokens** …

### Basic API

```javascript
sessionStorage.setItem('cartId', 'abc-123');
const cartId = sessionStorage.getItem('cartId');
sessionStorage.removeItem('cartId');
sessionStorage.clear(); // nuclear — all keys in this tab

// Always string values
sessionStorage.setItem('user', JSON.stringify({ id: 1 }));
const user = JSON.parse(sessionStorage.getItem('user') ?? 'null');
```

### Safe patterns

```javascript
// Namespaced keys — avoid collisions in micro-frontends
const KEY = 'checkout:v1:draft';
sessionStorage.setItem(KEY, JSON.stringify(draft));

// Guard SSR / private mode
function getSession(key) {
  try {
    return sessionStorage.getItem(key);
  } catch {
    return null; // Safari private, quota exceeded, disabled
  }
}
```

### When to choose sessionStorage

```txt
✓ Multi-step form draft (don't pollute localStorage forever)
✓ Wizard state, filters for single research session
✓ Post-login redirect URL (short-lived, tab-local)
✓ Staging UI flags that must not leak across tabs

✗ Auth tokens (use HttpOnly cookie)
✗ Cross-tab sync (use localStorage + storage event, or BroadcastChannel)
✗ Server-side rendering reads (no window on server)
```

### Cross-tab communication (if needed)

```javascript
// sessionStorage does NOT fire storage events in other tabs for same origin
// use localStorage + window.addEventListener('storage', ...) or BroadcastChannel
const bc = new BroadcastChannel('app');
bc.postMessage({ type: 'logout' });
```

## Mistakes to Avoid
- **Mistake:** **XSS = full storage read**
- **Mistake:** **Third-party scripts**
- **Mistake:** **Subdomain scope**
- **Mistake:** **Iframe embedding**
- **Mistake:** **Safari ITP / private mode**
- **Mistake:** **Data lost on refresh:** check Expected if new tab/window
- **Mistake:** **Data not shared between tabs:** check By design
- **Mistake:** **`QuotaExceededError`:** check Large JSON blobs
- **Mistake:** **Works in dev, null in prod:** check SSR accessing `sessionStor…
- **Mistake:** **Stale state after deploy:** check Old keys without version
- **Mistake:** **Security audit flag:** check PII in sessionStorage

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Session Storage — sessionStorage is a Storage object tied to a top-level browsin…).
- **Con / when not:** **Authentication/session IDs**
- **Con / when not:** **Preferences that should persist**
- **Con / when not:** **Large datasets** — IndexedDB or server fetch.

## Comparison
- vs [[CORS (Cross Origin Request Sharing)]]: know when each applies


### Use cases
- In production APIs and tooling, **Session Storage** shows up whenever teams s…
