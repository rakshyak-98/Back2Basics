[[CORS (Cross Origin Request Sharing)]] [[TLS (Transport Layer Security)]] [[JavaScript]] [[webSocket]]

# web capabilities

> Browser **capability APIs** gated by **Permissions Policy** (formerly Feature Policy) + user consent — know what works in iframe, third-party, and locked-down enterprise.

---

## Mental model

```txt
Page requests capability (camera, geolocation, clipboard, …)
        ↓
Permissions Policy: allowed for this document / iframe?
        ↓
User gesture + prompt (where required)
        ↓
Browser grants/denies → PermissionStatus / DOMException
```

**Two layers SEs confuse:**
1. **Permissions Policy** (`Permissions-Policy` header / `allow` attribute) — **who may call the API** (top-level vs embedded frame)
2. **Permission query** (`navigator.permissions.query`) — **user's choice** (granted/denied/prompt)

**Secure context required:** HTTPS (or localhost) for most sensitive APIs — won't work on mixed HTTP intranet without exception.

---

## Standard config / commands

### Common capability APIs

| API | Typical gate | Notes |
|-----|--------------|-------|
| `getUserMedia` | camera, microphone | Prompt; enterprise may block |
| `Geolocation` | geolocation | High accuracy drains battery |
| `Notification` | notifications | Also needs service worker for push |
| `Clipboard read/write` | clipboard-read/write | Read needs gesture + policy |
| `Web Bluetooth / USB / Serial` | feature-specific | Often disabled in corporate |
| `Payment Request` | payment | PSP + browser support |
| `Storage Access API` | storage-access | Third-party cookie workaround |
| `SharedArrayBuffer` | cross-origin-isolated | Requires COOP+COEP headers |

### Permissions-Policy header (deny by default pattern)

```nginx
# nginx — tighten per route
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# Allow camera only on /call route
location /call/ {
  add_header Permissions-Policy "camera=(self), microphone=(self)" always;
}
```

### iframe allow

```html
<iframe src="https://vendor.com/embed"
        allow="clipboard-write; fullscreen"
        sandbox="allow-scripts allow-same-origin">
</iframe>
```

### Query permission state (UX pre-check)

```javascript
const status = await navigator.permissions.query({ name: 'geolocation' });
status.onchange = () => console.log(status.state); // granted | denied | prompt

navigator.geolocation.getCurrentPosition(success, err);
// err.code === 1 PERMISSION_DENIED
```

### Feature detect (don't UA sniff)

```javascript
if (!('ClipboardItem' in window)) {
  showFallbackCopy();
}
```

### Cross-origin isolation (WASM threads, SAB)

```nginx
add_header Cross-Origin-Opener-Policy "same-origin" always;
add_header Cross-Origin-Embedder-Policy "require-corp" always;
# All subresources need CORP/CORS — breaks lazy third-party widgets
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `NotAllowedError` in iframe | Parent `Permissions-Policy` | Add `allow=` on iframe; relax header for origin |
| Works localhost, fails prod | Secure context | HTTPS everywhere; fix mixed content |
| `getUserMedia` NotReadableError | OS-level deny / other app | User settings; kill conflicting app |
| Clipboard read silent fail | No user gesture | Trigger on click handler |
| SharedArrayBuffer undefined | Not cross-origin isolated | COOP/COEP or drop threading |
| Enterprise "blocked" with no prompt | Group policy | Document fallback; native app bridge |
| Third-party embed broken | Sandbox + policy | Minimal sandbox flags; Storage Access API |

---

## Gotchas

> [!WARNING]
> **Safari / Firefox lag** — check caniuse before shipping capability-critical path.

> [!WARNING]
> **Prompt fatigue** — batch permission asks after user intent, not on page load.

> [!WARNING]
> **Headless automation** — fake media streams; CI won't catch policy header bugs.

> [!WARNING]
> **Revoked permissions** — listen to `permissionstatus.onchange`; don't cache "granted" forever.

---

## When NOT to use

- **File download/upload** — `<input type="file">` simpler than drag-drop File System Access API unless needed.
- **First-party auth session** — HttpOnly cookies + [[JWT authentication]] server-side; not Web Crypto keystore for sessions.
- **Background location tracking** — regulatory minefield; native app with OS permission model.

---

## Related

[[CORS (Cross Origin Request Sharing)]] · [[TLS (Transport Layer Security)]] · [[JavaScript]] · [[Etherium]] · [[Animation]]
