[[web workers]] [[content security policy]] [[Event Loop]] [[React build]] [[source map]]

# Service Worker

> Service Worker — unlike web workers (page-spawned, die with tab), a service worker is registered per origin + scope:

```txt
        Service Worker ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Service Worker** to see if you understand what it does o…

## Sources
- [MDN — Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) — deep-dive
- [Wikipedia — ServiceWorker](https://en.wikipedia.org/wiki/ServiceWorker) — overview

## Key Concepts
- **Unlike [[web:** Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is …
- **Short-lived: wakes:** Short-lived: wakes on events, may terminate when idle. **No DOM access.**


- **Core:** Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is …

## Technical Details
- Unlike [[web workers]] (page-spawned, die with tab), a **service worker** is …

```txt
Page registers /sw.js
  → install (precache)
  → activate (cleanup old caches)
  → fetch event (network proxy)
  → optional push / sync
```

- Short-lived: wakes on events, may terminate when idle.
- **No DOM access.:** 

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

- New SW waits in **waiting** until tabs close

- Requires **HTTPS** (localhost exempt).
- See [[content security policy]] for worker-source.

## Mistakes to Avoid
- **Mistake:** **Cache API ≠ HTTP cache**
- **Debugging pain** — DevTools::** → Application → Service Workers → "Bypass for network" during dev
- **Mistake:** **SW never registers:** check Not HTTPS / wrong path
- **Mistake:** **Stale assets forever:** check cache-first on HTML
- **Mistake:** **404 after deploy:** check Old precache list
- **Mistake:** **SW not updating:** check Browser cache on sw.js
- **Mistake:** **CSP blocks:** check `worker-src`; fix: Add self in CSP
- **Mistake:** **Works in dev only:** check build paths

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Service Worker — unlike web workers (page-spawned, die with tab), a service work…).
- **Con / when not:** **Heavy computation**
- **Con / when not:** **authentication secrets in SW**
- **Con / when not:** **SSR-only apps with no offline need**

## Comparison
- vs [[web workers]]: know when each applies


### Use cases
- In production APIs and tooling, **ServiceWorker** shows up whenever teams shi…
