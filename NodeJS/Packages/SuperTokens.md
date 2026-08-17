[[NodeJS]] [[Security/JWT authentication]] [[Security/single-sign-on (SSO)]] [[Express middleware]] [[Security/CORS (Cross Origin Request Sharing)]] [[Security/Token rotation]]

# SuperTokens (Node SDK)

> SuperTokens (Node SDK) — superTokens splits auth into a Core service (session store, refresh rotation) and your API (SDK middleware). Sessions live in httpOnly cookies +

```txt
        SuperTokens (Node  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **SuperTokens (Node SDK)** to see if you understand what i…

## Sources
- [SuperTokens — Docs](https://supertokens.com/docs/guides) — deep-dive
- [Wikipedia — SuperTokens](https://en.wikipedia.org/wiki/SuperTokens) — overview

## Key Concepts
- **[SuperTokens](https://supertokens.com/docs/nodejs) splits:** [SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into…
- **Recipe modules:** Recipe modules: **EmailPassword**, **ThirdParty** (OAuth), **Passwordless**, …


- **Core:** [SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into…

## Technical Details
- [SuperTokens](https://supertokens.com/docs/nodejs) splits authentication into…
- Sessions live in httpOnly cookies + anti-CSRF headers

```
Browser ──login──► API (supertokens-node SDK) ──► SuperTokens Core
   │                      │
   └── session cookies ◄──┘ validate on each request via middleware
```

- Recipe modules: **EmailPassword**, **ThirdParty** (OAuth), **Passwordless**, …
- SDK exposes `middleware()`, `errorHandler()`, and recipe APIs for sign-up/sig…

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

## Mistakes to Avoid
- **Mistake:** **`appInfo` domains must match real URLs**
- **Mistake:** **Middleware order**
- **Mistake:** **Don't roll custom JWT refresh**
- **Mistake:** **Multi-region**
- **Mistake:** **401 on all routes:** check Core down
- **Mistake:** **CORS errors on `/auth`:** check `websiteDomain` mismatch
- **Mistake:** **Refresh loop:** check Clock skew
- **Mistake:** **Session exists but 403 CSRF:** check Missing anti-CSRF header
- **Mistake:** **Works locally, fails prod:** check `cookieSecure` on HTTP
- **Mistake:** **User deleted but session valid:** check Session revocation

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (SuperTokens (Node SDK) — superTokens splits auth into a Core service (session st…).
- **Con / when not:** **Pure SPA + opaque API tokens only**
- **Con / when not:** **Machine-to-machine only**
- **Con / when not:** **Already deep into custom JWT**

## Comparison
- vs [[Security/JWT authentication]]: know when each applies


### Use cases
- In production APIs and tooling, **SuperTokens** shows up whenever teams ship …
