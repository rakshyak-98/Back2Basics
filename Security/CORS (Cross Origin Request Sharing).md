[[HTTP module]] [[JWT authentication]] [[SOP (Same-Origin Policy)]] [[single-sign-on (SSO)]] [[webSocket]] [[DNS rebinding]]

# CORS (Cross Origin Request Sharing)

> Browser rule: JS on evil.com cannot read api.example.com responses unless that API opts in with CORS headers — curl ignores it.

```txt
        CORS (Cross Origin ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic frontend/backend interview: CORS is browser-enforced, not server ACL

## Sources
- [MDN — CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) — overview
- [Fetch Living Standard — CORS protocol](https://fetch.spec.whatwg.org/#http-cors-protocol) — deep-dive

## Key Concepts
- **Core:** CORS is a browser mechanism that allows (or blocks) reading cross-origin resp…

## Technical Details
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

### Failure signals

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

## Mistakes to Avoid
- **Mistake:** CORS is not authentication
- **Mistake:** Error responses must include CORS headers
- **Mistake:** **`withCredentials: true`** forbids `Access-Control-Allow-Origin…
- **Mistake:** **Preflight cache** (`Max-Age`) masks configuration fixes
- **Mistake:** **Multiple origins**
- **Mistake:** **WebSocket** has separate origin check at handshake

## Pros/Cons or Trade-offs
- **Pro:** Lets a deliberate cross-origin SPA/API split work in browsers.
- **Con:** Server-to-server calls → no CORS needed.
- **Con:** Same-origin SPA + API → serve both from one host or use reverse proxy path (`/api` → backend).
- **Con:** "Fix" CORS by disabling browser security — development-only Chrome flags don't help users.

## Comparison
- vs [[SOP (Same-Origin Policy)]]: SOP is the default deny
- vs server ACLs: curl ignores CORS — still authenticate and authorize.


### Use cases
- SPA on `app.example.com` calling `api.example.com` needs explicit ACAO (and c…
