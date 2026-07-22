[[CORS (Cross Origin Request Sharing)]] [[cookies configuration]] [[cross-site scripting]] [[XSRF (cross-site request forgery)]]

# Cookie errors (cross-origin dev & prod)

> **Browser blocked the cookie** — almost always SameSite/Secure/domain mismatch, missing CORS credentials, or third-party cookie phaseout — not "cookies broken."

## Mental model

Cookies are set by `Set-Cookie` on a **response** and sent on **matching requests** per domain/path/SameSite/Secure rules. Cross-origin SPA (frontend `localhost:3000`, API `localhost:4000`) is **not** same-site; production subdomain splits (`app.example.com` vs `api.example.com`) are **same-site** but still **cross-origin** for CORS.

```
Browser stores cookie for api.example.com
       │
       └── sent only if: URL match + SameSite rules + Secure + credentials mode
```

Frontend must opt in (`credentials: 'include'`); backend must echo specific `Access-Control-Allow-Origin` (not `*`) with `Allow-Credentials: true`.

## Standard config / commands

### Cross-origin dev (different ports)

**Backend** (Express example):
```javascript
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true,
}));
app.use(session({
  cookie: {
    secure: false,      // true only on HTTPS
    sameSite: 'lax',    // or 'none' + secure for cross-site POST from other domains
    httpOnly: true,
  },
}));
```

**Frontend**:
```javascript
fetch('http://localhost:4000/api/me', { credentials: 'include' });
axios.defaults.withCredentials = true;
```

### Subdomain prod (`app.` + `api.`)

```javascript
// Set-Cookie from api.example.com
Set-Cookie: session=...; Domain=.example.com; Path=/; Secure; HttpOnly; SameSite=Lax
```

- `Domain=.example.com` — shared across subdomains ([[cookies configuration]]).
- `Secure: true` required for `SameSite=None`.

### SameSite=None (embedded or true cross-site)

Required when frontend on `other.com` calls your API — **and** `Secure: true` (HTTPS).

| Scenario | SameSite | Secure |
|----------|----------|--------|
| Same origin | Lax (default OK) | HTTPS in prod |
| Cross-subdomain API | Lax often enough for top-level nav | Yes |
| Cross-site iframe/embed | None | Yes (mandatory) |
| Localhost HTTP dev | Lax; None may fail without Secure | Browser-dependent |

### Checklist when cookie "not sent"

1. DevTools → Application → Cookies — is it stored?
2. Network tab — request includes `Cookie` header?
3. Response had `Set-Cookie`? Any `SameSite`/`Domain`/`Path` reject?
4. Fetch used `credentials: 'include'`?
5. CORS: exact origin + `Access-Control-Allow-Credentials: true`?

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Login OK, next request 401 | Cookie not stored (Secure on HTTP) | HTTPS or disable Secure locally |
| Works in Chrome, not Safari | ITP; third-party cookie blocked | First-party cookie on shared parent domain |
| POST login loses cookie | SameSite=Lax blocks cross-site POST | SameSite=None + Secure or same-origin proxy |
| Cookie set but not on API calls | Wrong Domain (host-only vs `.parent`) | Set `Domain=.example.com` |
| CORS error + no cookie | `Allow-Origin: *` with credentials | Explicit origin whitelist |
| After OAuth redirect, session gone | SameSite strict on redirect chain | Lax or None on OAuth callback path |
| `document.cookie` can't read | HttpOnly (correct for session) | Use API `/me`, not JS read |

## Gotchas

> [!WARNING]
> **Frontend and backend on two different registrable domains** — `SameSite=None; Secure` + third-party cookie deprecation in Chrome may still block; prefer **same-site proxy** (nginx `/api` → backend).

> [!WARNING]
> **`SameSite=Strict` on auth cookie** — user following link from email won't send cookie on first GET ([[cookies configuration]]).

> [!WARNING]
> **Proxy strips Set-Cookie** — nginx `proxy_cookie_path/domain` misconfig drops attributes.

> [!WARNING]
> **Max-Age vs browser session** — missing both = session cookie; tab close logs user out.

## When NOT to use

- **Cookie for API tokens in mobile native apps** — use Authorization header + secure storage.
- **Large payloads in cookies** — 4KB limit; use session server-side id only.

## Related

[[cookies configuration]] · [[CORS (Cross Origin Request Sharing)]] · [[JWT authentication]] · [[cross-site scripting]] · [[XSRF (cross-site request forgery)]]
