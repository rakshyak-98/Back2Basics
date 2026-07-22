[[NodeJS]] [[Security/JWT authentication]] [[Security/single-sign-on (SSO)]] [[Express middleware]]

# SuperTokens (Node SDK)

> One-line: managed/session-based auth SDK — handles login, refresh, anti-CSRF, and session validation middleware for Express/Fastify; self-host or SaaS core.

## Mental model

[SuperTokens](https://supertokens.com/docs/nodejs) splits auth into a **Core** service (session store, refresh rotation) and your **API** (SDK middleware). Sessions live in httpOnly cookies + anti-CSRF headers — not long-lived JWTs in localStorage.

```
Browser ──login──► API (supertokens-node SDK) ──► SuperTokens Core
   │                      │
   └── session cookies ◄──┘ validate on each request via middleware
```

Recipe modules: **EmailPassword**, **ThirdParty** (OAuth), **Passwordless**, **Session**, **UserRoles**. SDK exposes `middleware()`, `errorHandler()`, and recipe APIs for sign-up/sign-in.

## Standard config / commands

### Express setup

```javascript
import supertokens from 'supertokens-node';
import Session from 'supertokens-node/recipe/session';
import EmailPassword from 'supertokens-node/recipe/emailpassword';
import { middleware, errorHandler } from 'supertokens-node/framework/express';

supertokens.init({
  framework: 'express',
  supertokens: {
    connectionURI: process.env.SUPERTOKENS_CONNECTION_URI,
    apiKey: process.env.SUPERTOKENS_API_KEY,
  },
  appInfo: {
    appName: 'MyApp',
    apiDomain: 'https://api.example.com',
    websiteDomain: 'https://app.example.com',
    apiBasePath: '/auth',
    websiteBasePath: '/auth',
  },
  recipeList: [
    EmailPassword.init(),
    Session.init({
      cookieSecure: process.env.NODE_ENV === 'production',
      cookieSameSite: 'lax',
    }),
  ],
});

app.use(middleware());
app.use(errorHandler());
```

### Protect route

```javascript
import { verifySession } from 'supertokens-node/recipe/session/framework/express';

app.get('/api/me', verifySession(), async (req, res) => {
  const session = req.session;
  const userId = session.getUserId();
  res.json({ userId });
});
```

### Optional session (public + personalized)

```javascript
app.get('/feed', verifySession({ sessionRequired: false }), handler);
```

### Docker Core (self-host)

```yaml
# supertokens-core on 3567; point connectionURI to it
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 401 on all routes | Core down; wrong `connectionURI` | Health check Core; verify network from API pod |
| CORS errors on `/auth` | `websiteDomain` mismatch | Align appInfo domains; CORS before middleware |
| Refresh loop | Clock skew; cookie domain | Sync NTP; `cookieDomain` for subdomains |
| Session exists but 403 CSRF | Missing anti-CSRF header | Frontend SDK must send header from recipe |
| Works locally, fails prod | `cookieSecure` on HTTP | HTTPS only in prod or correct proxy `trust proxy` |
| User deleted but session valid | Session revocation | Call revoke session APIs; shorten access token life |

## Gotchas

> [!WARNING]
> **`appInfo` domains must match real URLs** — subtle mismatch breaks cookie scope and OAuth redirects.

> [!WARNING]
> **Middleware order** — SuperTokens middleware before body parsers on auth routes per docs.

> [!WARNING]
> **Don't roll custom JWT refresh** — use recipe session handling; rotation is easy to get wrong.

> [!WARNING]
> **Multi-region** — Core latency; consider managed SuperTokens or regional Core.

## When NOT to use

- **Pure SPA + opaque API tokens only** — simpler OAuth2 provider (Auth0, Cognito) may fit.
- **Machine-to-machine only** — client credentials flow, not session cookies.
- **Already deep into custom JWT** — migration cost vs incremental hardening.

## Related

[[Security/JWT authentication]] [[Security/single-sign-on (SSO)]] [[Security/CORS (Cross Origin Request Sharing)]] [[Express middleware]] [[Security/Token rotation]]
