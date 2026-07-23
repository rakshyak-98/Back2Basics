[[HTTP module]] [[JWT authentication]] [[SOP (Same-Origin Policy)]]

# CORS (Cross Origin Request Sharing)

> One-line: browser-enforced policy — server headers permit another origin to read responses; preflight validates "non-simple" requests — **Fetch spec / W3C**.

## Mental model

CORS is **not server access control** — it stops **browser JavaScript** on `https://evil.com` from reading responses from `https://api.example.com` unless the API explicitly allows it. curl/Postman ignore CORS.

```
Browser on https://myapp.com
  │  GET https://api.example.com/data
  │  Origin: https://myapp.com
  ├──────────────────────────────► API
  │◄──────────────────────────────┤
  │  Access-Control-Allow-Origin: https://myapp.com
  │  (browser exposes response to JS)
```

**Simple requests** (GET/HEAD/POST with safelisted headers) go direct. **Preflight** `OPTIONS` runs first for custom headers, PUT/PATCH/DELETE, `Content-Type: application/json`, etc.

| Header | Role |
|--------|------|
| `Origin` | Sent by browser on cross-origin requests |
| `Access-Control-Allow-Origin` | Echo specific origin or `*` (no credentials) |
| `Access-Control-Allow-Credentials: true` | Allows cookies — **cannot** use `*` for ACAO |
| `Access-Control-Allow-Methods` | Preflight: permitted verbs |
| `Access-Control-Allow-Headers` | Preflight: permitted request headers |
| `Access-Control-Max-Age` | Cache preflight (seconds) |

Same-origin (`myapp.com` → `myapp.com/api`) → **no CORS** — preferred for monoliths and BFF patterns.

## Standard config / commands

### Express (`cors` package)

```javascript
const cors = require('cors');

const corsOptions = {
  origin: ['https://myapp.com', 'http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-Id'],
  maxAge: 86400,
};

app.use(cors(corsOptions));
app.options('*', cors(corsOptions));   // explicit preflight — some setups need this
```

### Nginx (API behind reverse proxy)

```nginx
location /api/ {
    if ($request_method = OPTIONS) {
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Credentials true always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
        add_header Access-Control-Max-Age 86400 always;
        return 204;
    }
    add_header Access-Control-Allow-Origin $http_origin always;
    add_header Access-Control-Allow-Credentials true always;
    proxy_pass http://backend;
}
```

### Preflight debug (curl simulates browser)

```shell
# Preflight
curl -i -X OPTIONS 'https://api.example.com/users' \
  -H 'Origin: https://myapp.com' \
  -H 'Access-Control-Request-Method: PUT' \
  -H 'Access-Control-Request-Headers: Authorization, Content-Type'

# Expect: 204/200 + ACAO + Allow-Methods + Allow-Headers

# Actual credentialed request
curl -i 'https://api.example.com/users' \
  -H 'Origin: https://myapp.com' \
  -H 'Cookie: session=abc' \
  --cookie 'session=abc'
```

### Browser devtools checklist

1. **Network tab** → failed request → if no response headers visible, likely **network/CORS block**.
2. Separate **`OPTIONS`** entry before POST? → preflight failure.
3. Console: `blocked by CORS policy: No 'Access-Control-Allow-Origin'` → server didn't echo origin.
4. `Credentials flag is true, but Access-Control-Allow-Origin is *` → must echo exact origin.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works in Postman, fails in browser | CORS is browser-only | Add ACAO headers; not an "API bug" |
| `No Access-Control-Allow-Origin` | Response lacks header on error paths | Add CORS middleware **before** routes; include 4xx/5xx responses (`always` in nginx) |
| Preflight 404/405 | `OPTIONS` not routed | Register `app.options('*')` or nginx OPTIONS block |
| `header X-Custom not allowed` | Missing `Allow-Headers` | Add header to `allowedHeaders` / ACAH |
| `Method PUT not allowed` | Missing `Allow-Methods` | Include verb in preflight response |
| Cookie not sent cross-origin | `SameSite`; missing `credentials` | Client: `withCredentials: true`; server: `Allow-Credentials: true` + exact ACAO |
| Intermittent after deploy | CDN strips CORS on cache hit | Vary on Origin; configure CDN CORS policy |
| Duplicate ACAO headers | nginx + app both set | Single layer owns CORS — remove duplicate |
| Redirect on preflight | 301 http→https loses CORS | Fix URL to final HTTPS; avoid redirect on OPTIONS |

## Gotchas

> [!WARNING]
> **CORS is not authentication.** Any client without a browser can call your API. Still require [[JWT authentication]] / sessions.

> [!WARNING]
> **Error responses must include CORS headers** or the browser hides the real 401/403 body from JS — looks like generic CORS failure.

- **`withCredentials: true`** forbids `Access-Control-Allow-Origin: *` — must echo requesting origin.
- **Preflight cache** (`Max-Age`) masks config fixes — hard refresh or wait cache expiry when testing.
- **Multiple origins** — dynamic `origin` callback; never reflect arbitrary `Origin` without allowlist (security hole).
- **WebSocket** has separate origin check at handshake — see [[webSocket]].

## When NOT to use

- Server-to-server calls → no CORS needed.
- Same-origin SPA + API → serve both from one host or use reverse proxy path (`/api` → backend).
- "Fix" CORS by disabling browser security — dev-only Chrome flags don't help users.

## Related

[[HTTP module]] · [[JWT authentication]] · [[single-sign-on (SSO)]] · [[webSocket]] · [[DNS rebinding]]
