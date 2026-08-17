[[CORS (Cross Origin Request Sharing)]] [[JWT authentication]] [[single-sign-on (SSO)]] [[webSocket]] [[IDOR]]

# Session Storage

> Session Storage — sessionStorage is a Storage object tied to a top-level browsing context (tab/window). Data survives page reloads and SPA navigations within the same tab





## Interview Relevance
Interviewers use **Session Storage** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **sessionStorage**, **localStorage**, **Cookie**, **Memory (React state)**.

## Sources
- [MDN — sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) — deep-dive
- [Wikipedia — Session Storage](https://en.wikipedia.org/wiki/Session_Storage) — overview

## Core Definition
`sessionStorage` is a **`Storage` object** tied to a **top-level browsing context** (tab/window). Data survives **page reloads and SPA navigations** within the same tab, but dies when the tab closes. It is **origin-scoped** (`scheme + host + port`) like `localStorage`.

## Key Concepts
- **sessionStorage:** Tab — No
- **localStorage:** Until cleared — No
- **Cookie:** Configurable — Yes (auto)
- **Memory (React state):** Page — No

## Technical Details
`sessionStorage` is a **`Storage` object** tied to a **top-level browsing context** (tab/window). Data survives **page reloads and SPA navigations** within the same tab, but dies when the tab closes. It is **origin-scoped** (`scheme + host + port`) like `localStorage`.

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

**Not a session mechanism for authentication** — the server doesn't see sessionStorage. authentication sessions use **HttpOnly Secure cookies** or **Bearer tokens** with explicit tradeoffs ([[JWT authentication]]).

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

## Real-World Applications
In production APIs and tooling, **Session Storage** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **XSS = full storage read** — anything in sessionStorage/localStorage is stealable. Never store refresh tokens accessible to JS if avoidable; **Third-party scripts** — analytics tag XSS exfiltrates storage; CSP + script hygiene.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Session Storage — sessionStorage is a Storage object tied to a top-level browsin…).
- **Con / when not:** **Authentication/session IDs** — HttpOnly cookies + SameSite.
- **Con / when not:** **Preferences that should persist** — theme, locale → `localStorage` or account settings API.
- **Con / when not:** **Large datasets** — IndexedDB or server fetch.

## Comparison
vs [[CORS (Cross Origin Request Sharing)]]: know when each applies — do not treat them as interchangeable. vs [[JWT authentication]]: know when each applies — do not treat them as interchangeable. vs [[single-sign-on (SSO)]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **XSS = full storage read** — anything in sessionStorage/localStorage is stealable. Never store refresh tokens accessible to JS if avoidable.
- **Third-party scripts** — analytics tag XSS exfiltrates storage; CSP + script hygiene.
- **Subdomain scope** — `app.example.com` ≠ `www.example.com`; storage not shared.
- **Iframe embedding** — third-party iframe has its own origin storage; don't rely on parent sessionStorage.
- **Safari ITP / private mode** — `setItem` throws; always try/catch.
- **Data lost on refresh:** check Expected if new tab/window; fix: Use `localStorage` or server persistence
- **Data not shared between tabs:** check By design; fix: `localStorage` or URL state
- **`QuotaExceededError`:** check Large JSON blobs; fix: Compress; server-side session store
- **Works in dev, null in prod:** check SSR accessing `sessionStorage`; fix: `typeof window !== 'undefined'` guard
- **Stale state after deploy:** check Old keys without version; fix: Namespace with version suffix `v2:`
- **Security audit flag:** check PII in sessionStorage; fix: Move sensitive data server-side
