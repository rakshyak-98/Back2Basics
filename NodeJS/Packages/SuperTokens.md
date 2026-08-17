[[NodeJS]] [[Security/JWT authentication]] [[Security/single-sign-on (SSO)]] [[Express middleware]] [[Security/CORS (Cross Origin Request Sharing)]] [[Security/Token rotation]]

# SuperTokens (Node SDK)

> SuperTokens (Node SDK) — superTokens splits auth into a Core service (session store, refresh rotation) and your API (SDK middleware). Sessions live in httpOnly cookies +





## Interview Relevance
Interviewers probe **SuperTokens (Node SDK)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [SuperTokens — Docs](https://supertokens.com/docs/guides) — deep-dive
- [Wikipedia — SuperTokens](https://en.wikipedia.org/wiki/SuperTokens) — overview

## Core Definition
[SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into a **Core** service (session store, refresh rotation) and your **API** (SDK middleware). Sessions live in httpOnly cookies + anti-CSRF headers — not long-lived JWTs in localStorage.

## Key Concepts
- [SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into a **Core** service (session store, refresh rotation) and your **API** (SDK middleware). Sessions li…
- Recipe modules: **EmailPassword**, **ThirdParty** (OAuth), **Passwordless**, **Session**, **UserRoles**. SDK exposes `middleware()`, `errorHandler()`, and recipe APIs for sign-u…

## Technical Details
[SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into a **Core** service (session store, refresh rotation) and your **API** (SDK middleware). Sessions live in httpOnly cookies + anti-CSRF headers — not long-lived JWTs in localStorage.

```
Browser ──login──► API (supertokens-node SDK) ──► SuperTokens Core
   │                      │
   └── session cookies ◄──┘ validate on each request via middleware
```

Recipe modules: **EmailPassword**, **ThirdParty** (OAuth), **Passwordless**, **Session**, **UserRoles**. SDK exposes `middleware()`, `errorHandler()`, and recipe APIs for sign-up/sign-in.

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

## Real-World Applications
In production APIs and tooling, **SuperTokens** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`appInfo` domains must match real URLs** — subtle mismatch breaks cookie scope and OAuth redirects; **Middleware order** — SuperTokens middleware before body parsers on auth routes per docs.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (SuperTokens (Node SDK) — superTokens splits auth into a Core service (session st…).
- **Con / when not:** **Pure SPA + opaque API tokens only** — simpler OAuth2 provider (Auth0, Cognito) may fit.
- **Con / when not:** **Machine-to-machine only** — client credentials flow, not session cookies.
- **Con / when not:** **Already deep into custom JWT** — migration cost versus incremental hardening.

## Comparison
vs [[Security/JWT authentication]]: know when each applies — do not treat them as interchangeable. vs [[Security/single-sign-on (SSO)]]: know when each applies — do not treat them as interchangeable. vs [[Express middleware]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`appInfo` domains must match real URLs** — subtle mismatch breaks cookie scope and OAuth redirects.
- **Middleware order** — SuperTokens middleware before body parsers on auth routes per docs.
- **Don't roll custom JWT refresh** — use recipe session handling; rotation is easy to get wrong.
- **Multi-region** — Core latency; consider managed SuperTokens or regional Core.
- **401 on all routes:** check Core down; wrong `connectionURI`; fix: Health check Core; verify network from API pod
- **CORS errors on `/auth`:** check `websiteDomain` mismatch; fix: Align appInfo domains; CORS before middleware
- **Refresh loop:** check Clock skew; cookie domain; fix: Sync NTP; `cookieDomain` for subdomains
- **Session exists but 403 CSRF:** check Missing anti-CSRF header; fix: Frontend SDK must send header from recipe
- **Works locally, fails prod:** check `cookieSecure` on HTTP; fix: HTTPS only in prod or correct proxy `trust proxy`
- **User deleted but session valid:** check Session revocation; fix: Call revoke session APIs; shorten access token life
