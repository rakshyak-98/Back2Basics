[[web workers]] [[content security policy]] [[Event Loop]] [[React build]] [[source map]]

# Service Worker

> Service Worker — unlike web workers (page-spawned, die with tab), a service worker is registered per origin + scope:





## Interview Relevance
Interviewers probe **Service Worker** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [MDN — Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) — deep-dive
- [Wikipedia — ServiceWorker](https://en.wikipedia.org/wiki/ServiceWorker) — overview

## Core Definition
Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is registered per **origin + scope**:

## Key Concepts
- Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is registered per **origin + scope**:
- Short-lived: wakes on events, may terminate when idle. **No DOM access.**

## Technical Details
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

Requires **HTTPS** (localhost exempt). See [[content security policy]] for worker-source.

## Real-World Applications
In production APIs and tooling, **ServiceWorker** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Cache API ≠ HTTP cache** — you must version and delete old caches on activate; **Debugging pain** — DevTools → Application → Service Workers → "Bypass for network" during dev.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Service Worker — unlike web workers (page-spawned, die with tab), a service work…).
- **Con / when not:** **Heavy computation** — use [[web workers]]; SW is for network/cache lifecycle.
- **Con / when not:** **authentication secrets in SW** — visible; tokens belong HttpOnly cookies server-side.
- **Con / when not:** **SSR-only apps with no offline need** — skip SW complexity.

## Comparison
vs [[web workers]]: know when each applies — do not treat them as interchangeable. vs [[content security policy]]: know when each applies — do not treat them as interchangeable. vs [[Event Loop]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Cache API ≠ HTTP cache** — you must version and delete old caches on activate.
- **Debugging pain** — DevTools → Application → Service Workers → "Bypass for network" during dev.
- **SW never registers:** check Not HTTPS / wrong path; fix: Serve over TLS; scope path
- **Stale assets forever:** check cache-first on HTML; fix: network-first for navigations
- **404 after deploy:** check Old precache list; fix: Version CACHE name; cleanup activate
- **SW not updating:** check Browser cache on sw.js; fix: `Cache-Control: no-cache` on sw file
- **CSP blocks:** check `worker-src`; fix: Add self in CSP
- **Works in dev only:** check build paths; fix: Precache hashed filenames from manifest
