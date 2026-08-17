[[NodeJS]] [[Express middleware]] [[TLS (Transport Layer Security)]] [[Node.js run as a non-privileged user]] [[express error handler]] [[Event Loop]]

# Node.js Security — Architectural Flaws

> single-process trust boundary, huge dependency trees, and prototype pollution make Node apps fragile — design assumes hostile input and supply chain from day one.

```txt
        Node.js Security — ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js Security

## Sources
- [Node.js — Security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices) — deep-dive
- [OWASP — Node.js Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html) — overview
- [Wikipedia — Node.js security flaws in architecture](https://en.wikipedia.org/wiki/Node.js_security_flaws_in_architecture) — overview

## Key Concepts
- **Node services:** Node services typically sit **directly on the internet** with:
- **One language/runtime:** One language/runtime handling authentication, business logic, and serializati…
- **Attack surface:** Attack surface clusters at: **HTTP parsers**, **JSON/body parsers**, **JWT/se…


- **Core:** Node services typically sit **directly on the internet** with:

## Technical Details
- Node services typically sit **directly on the internet** with:

- One language/runtime handling authentication, business logic, and serializati…
- **npm dependency graph:** — transitive packages run with full process privileges
- **Dynamic `require()`:** and eval-adjacent patterns (`vm`, template engines)
- No memory-safe guarantee — native addons and V8 alike

- Attack surface clusters at: **HTTP parsers**, **JSON/body parsers**, **JWT/se…

```
Internet → reverse proxy (TLS terminate) → Express (trusts X-Forwarded-*) → DB/Redis/internal APIs
                    ↑ miss one layer = auth bypass or SSRF
```

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

- Never log `req.headers.authorization` or full `req.body` in production.

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

- Use `.npmrc`:

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

- Audit `lodash.merge`, `JSON.parse` → dynamic key assignment patterns.

### Decision

- We will … because …

### Consequences

- **Positive:** …

- **Negative / trade-offs:** …

### Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

## Mistakes to Avoid
- **Mistake:** **`eval`, `new Function`, `vm.runInNewContext`**
- **Mistake:** **Dynamic `require(userInput)`** — arbitrary code load
- **Mistake:** **Error handler leaking stack**
- **Mistake:** **Cluster doesn't isolate security**
- **Mistake:** **CORS `*` with credentials**
- **Mistake:** **Auth bypass via header spoof:** check `trust proxy` too permis…
- **Mistake:** **CPU peg, slow regex:** check ReDoS in user input regex
- **Mistake:** **RCE after deploy:** check `npm audit`, new dependency
- **Mistake:** **JWT accepted after "logout":** check Stateless JWT until expiry
- **Mistake:** **Path traversal on upload:** check `path.join` with user segment
- **Mistake:** **Memory spike on POST:** check Missing body limit

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (single-process trust boundary, huge dependency trees, and prototype pollution ma…).
- **Con / when not:** **Rolling custom crypto**
- **Con / when not:** **Disabling helmet/CORS "temporarily" in production**

## Comparison
- vs [[Express middleware]]: know when each applies


### Use cases
- In production APIs and tooling, **Node.js security flaws in architecture** sh…
