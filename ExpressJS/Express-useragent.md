[[express concepts]] [[Express middleware]] [[npm]] [[expressjs]]

# Express-useragent

> `express-useragent` parses the `User-Agent` header into fields on `req.useragent` — useful for analytics and client quirks, never for security decisions.

```txt
        Express-useragent ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers check whether you treat `User-Agent` as a spoofable hint: fine f…

## Sources
- [MDN — User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) — overview
- [express-useragent on npm](https://www.npmjs.com/package/express-useragent) — overview
- [RFC 9110 — HTTP Semantics (User-Agent)](https://www.rfc-editor.org/rfc/rfc9110#name-user-agent) — deep-dive

## Key Concepts
- **Hint, not identity:** spoofing is trivial — never gate privileges on UA.
- **Mount once:** parse in global middleware; avoid re-parsing in every handler.
- **Drift:** new browsers and bots misclassify until the library updates.
- **Privacy:** UA strings are identifying — minimize production logging.


- **Core:** The middleware runs regular expressions over the `User-Agent` string and atta…

## Technical Details
```txt
User-Agent header ──middleware──► req.useragent { browser, os, isMobile, ... }
```

```js
import useragent from 'express-useragent'
app.use(useragent.express())
app.get('/', (req, res) => {
  res.json({
    browser: req.useragent.browser,
    os: req.useragent.os,
    isMobile: req.useragent.isMobile,
  })
})
```

| Concern | Practice |
|---------|----------|
| Trust boundary | Treat UA as hint, not credential |
| Performance | Mount once globally |
| Alternatives | `ua-parser-js` and similar libraries |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `req.useragent` undefined | Middleware after routes | `app.use` before handlers |
| Wrong mobile flag | New UA string | Update library; feature-detect on client |
| Missing fields | Bot or `curl` with no UA | Provide defaults |

## Mistakes to Avoid
- **Mistake:** Using User-Agent for authentication or authorization
- **Mistake:** Building responsive layout decisions only on the server from UA
- **Mistake:** Logging full UA strings indefinitely without a retention policy
- **Mistake:** Mounting the middleware after routes so `req.useragent` is alway…

## Pros/Cons or Trade-offs
- **Pro:** Cheap structured fields without writing your own regex soup.
- **Con:** Always lagging new UAs; false positives/negatives are normal.
- **Con:** Encourages server-side “device detection” that belongs in CSS/`matchMedia`.

## Comparison
- vs client feature detection: CSS and browser APIs are authoritative for layout/capability.
- vs authentication middleware: credentials and sessions prove identity; UA does not.
- vs [[Express middleware]] generally: same mount-order rules apply.


### Use cases
- Analytics dashboards, choosing a lighter payload for known mobile clients, an…

- **Example:** An A/B report groups sessions by `req.useragent.os`
