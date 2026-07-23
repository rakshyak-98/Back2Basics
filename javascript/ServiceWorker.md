[[web workers]] [[content security policy]] [[Event Loop]] [[React build]]

# Service Worker

> **Browser-owned background thread** for fetch interception, offline cache, push — separate lifecycle from page JS — **Service Worker spec / MDN**.

---

## Mental model

Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is registered per **origin + scope**:

```txt
Page registers /sw.js
  → install (precache)
  → activate (cleanup old caches)
  → fetch event (network proxy)
  → optional push / sync
```

Short-lived: wakes on events, may terminate when idle. **No DOM access.**

| Capability | API |
|------------|-----|
| Offline shell | Cache API + fetch handler |
| Update strategy | cache-first / network-first |
| Push notifications | `push` + `notificationclick` |
| Background sync | `sync` event (limited support) |

```txt
Client page  ──fetch──►  Service Worker  ──► network / cache
                              ↑
                         controls scope path
```

---

## Standard config / commands

### Register (main thread)

```javascript
if ("serviceWorker" in navigator) {
  window.addEventListener("load", async () => {
    const reg = await navigator.serviceWorker.register("/sw.js", { scope: "/" });
    console.log("scope", reg.scope);
  });
}
```

### Minimal sw.js

```javascript
const CACHE = "app-v1";
const ASSETS = ["/", "/index.html", "/app.js", "/app.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
```

### Update flow

New SW waits in **waiting** until tabs close — call `skipWaiting()` + `clients.claim()` carefully; prompt user to refresh.

Requires **HTTPS** (localhost exempt). See [[content security policy]] for worker-src.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| SW never registers | Not HTTPS / wrong path | Serve over TLS; scope path |
| Stale assets forever | cache-first on HTML | network-first for navigations |
| 404 after deploy | Old precache list | Version CACHE name; cleanup activate |
| SW not updating | Browser cache on sw.js | `Cache-Control: no-cache` on sw file |
| CSP blocks | `worker-src` | Add self in CSP |
| Works in dev only | build paths | Precache hashed filenames from manifest |

---

## Gotchas

> [!WARNING]
> **Cache API ≠ HTTP cache** — you must version and delete old caches on activate.

> [!WARNING]
> **Debugging pain** — DevTools → Application → Service Workers → "Bypass for network" during dev.

---

## When NOT to use

- **Heavy computation** — use [[web workers]]; SW is for network/cache lifecycle.
- **Auth secrets in SW** — visible; tokens belong HttpOnly cookies server-side.
- **SSR-only apps with no offline need** — skip SW complexity.

---

## Related

[[web workers]] · [[content security policy]] · [[Event Loop]] · [[React build]] · [[source map]]
