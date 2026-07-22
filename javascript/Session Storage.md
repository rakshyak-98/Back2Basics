[[CORS (Cross Origin Request Sharing)]] [[JWT authentication]] [[single-sign-on (SSO)]] [[webSocket]]

# Session Storage

> Browser `sessionStorage` API — tab-scoped key/value store; security and storage choice vs `localStorage` and cookies — **WHATWG HTML / OWASP**.

---

## Mental model

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
| **Memory (React state)** | Page | No | RAM | Lost on refresh |

**Not a session mechanism for auth** — the server doesn't see sessionStorage. Auth sessions use **HttpOnly Secure cookies** or **Bearer tokens** with explicit tradeoffs ([[JWT authentication]]).

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Data lost on refresh | Expected if new tab/window | Use `localStorage` or server persistence |
| Data not shared between tabs | By design | `localStorage` or URL state |
| `QuotaExceededError` | Large JSON blobs | Compress; server-side session store |
| Works in dev, null in prod | SSR accessing `sessionStorage` | `typeof window !== 'undefined'` guard |
| Stale state after deploy | Old keys without version | Namespace with version suffix `v2:` |
| Security audit flag | PII in sessionStorage | Move sensitive data server-side |

---

## Gotchas

> [!WARNING]
> **XSS = full storage read** — anything in sessionStorage/localStorage is stealable. Never store refresh tokens accessible to JS if avoidable.

> [!WARNING]
> **Third-party scripts** — analytics tag XSS exfiltrates storage; CSP + script hygiene.

> [!WARNING]
> **Subdomain scope** — `app.example.com` ≠ `www.example.com`; storage not shared.

> [!WARNING]
> **Iframe embedding** — third-party iframe has its own origin storage; don't rely on parent sessionStorage.

> [!WARNING]
> **Safari ITP / private mode** — `setItem` throws; always try/catch.

---

## When NOT to use

- **Authentication/session IDs** — HttpOnly cookies + SameSite.
- **Preferences that should persist** — theme, locale → `localStorage` or account settings API.
- **Large datasets** — IndexedDB or server fetch.

---

## Related

[[CORS (Cross Origin Request Sharing)]] [[JWT authentication]] [[single-sign-on (SSO)]] [[webSocket]] [[IDOR]]
