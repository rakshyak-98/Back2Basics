[[NodeJS]] [[Express middleware]] [[TLS (Transport Layer Security)]] [[Node.js run as a non-privileged user]]

# Node.js Security — Architectural Flaws

> One-line: single-process trust boundary, huge dependency trees, and prototype pollution make Node apps fragile — design assumes hostile input and supply chain from day one.

## Mental model

Node services typically sit **directly on the internet** with:

- One language/runtime handling auth, business logic, and serialization
- **npm dependency graph** — transitive packages run with full process privileges
- **Dynamic `require()`** and eval-adjacent patterns (`vm`, template engines)
- No memory-safe guarantee — native addons and V8 alike

Attack surface clusters at: **HTTP parsers**, **JSON/body parsers**, **JWT/session**, **file uploads**, **SSRF outbound calls**, **deserialization**, **ReDoS in regex**.

```
Internet → reverse proxy (TLS terminate) → Express (trusts X-Forwarded-*) → DB/Redis/internal APIs
                    ↑ miss one layer = auth bypass or SSRF
```

---

## Standard config / commands

### Layer 0 — process & network

```bash
# Never run as root in production
useradd -r -s /bin/false nodeapp
# bind >1024 or use setcap / reverse proxy

# Keep Node patched
nvm install --lts
npm audit --production
npm audit fix --force   # review breaking changes manually
```

### Layer 1 — Express hardening

```javascript
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import hpp from 'hpp';

app.set('trust proxy', 1);              // only if behind ONE known proxy hop
app.use(helmet());
app.use(hpp());                         // HTTP parameter pollution
app.use(express.json({ limit: '10kb' })); // body bomb defense
app.use(rateLimit({ windowMs: 60_000, max: 100 }));

// Disable x-powered-by
app.disable('x-powered-by');
```

### Layer 2 — auth & secrets

```javascript
// BAD — secret in repo
const JWT_SECRET = 'dev-secret';

// GOOD — env + rotation
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error('JWT_SECRET required');

// Timing-safe compare for tokens
import { timingSafeEqual } from 'crypto';
```

Never log `req.headers.authorization` or full `req.body` in production.

### Layer 3 — SSRF & outbound fetch

```javascript
// BAD — user supplies URL
await fetch(req.query.url);

// GOOD — allowlist hosts, block metadata IPs (169.254.169.254)
const allowed = new Set(['api.stripe.com']);
const u = new URL(userUrl);
if (!allowed.has(u.hostname)) throw forbidden();
// also block private ranges in production egress
```

### Layer 4 — supply chain

```bash
npm ci                              # lockfile-only installs in CI
npx lockfile-lint --path package-lock.json
# Enable GitHub Dependabot / Snyk; pin major versions for critical deps
```

Use `.npmrc`:

```ini
ignore-scripts=true                 # block postinstall scripts (test impact first)
```

### Layer 5 — prototype pollution defense

```javascript
// Avoid deep merge from untrusted JSON
import structuredClone from 'node:structuredClone';
// or validate schema with Ajv/Zod before merge

Object.freeze(Object.prototype);    // last-resort mitigation — can break libs
```

Audit `lodash.merge`, `JSON.parse` → dynamic key assignment patterns.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth bypass via header spoof | `trust proxy` too permissive | Set exact hop count; validate at proxy |
| CPU peg, slow regex | ReDoS in user input regex | Timeout; use `safe-regex`; RE2 via `re2` |
| RCE after deploy | `npm audit`, new dependency | Remove package; pin; incident response |
| JWT accepted after "logout" | Stateless JWT until expiry | Short TTL + refresh rotation; denylist jti in Redis |
| Path traversal on upload | `path.join` with user segment | Sanitize filename; store outside web root |
| Memory spike on POST | Missing body limit | `limit` on json/urlencoded |

---

## Gotchas

> [!WARNING]
> **`eval`, `new Function`, `vm.runInNewContext`** — not a sandbox; RCE via prototype chains.

> [!WARNING]
> **Dynamic `require(userInput)`** — arbitrary code load.

> [!WARNING]
> **Error handler leaking stack** — see [[express error handler]]; hide stack in prod.

> [!WARNING]
> **Cluster doesn't isolate security** — compromised worker = same UID, same env secrets.

> [!WARNING]
> **CORS `*` with credentials** — invalid and often misconfigured; explicit origins only.

---

## When NOT to use

- **Rolling custom crypto** — use libsodium/WebCrypto wrappers; never DIY JWT "for simplicity".
- **Disabling helmet/CORS "temporarily" in prod** — becomes permanent.

---

## Related

[[express error handler]] [[Express middleware]] [[Event Loop]] [[Node.js run as a non-privileged user]] [[TLS (Transport Layer Security)]]
