[[ExpressJS]] [[express concepts]] [[npm]] [[Express middleware]]

# Express-useragent

> `express-useragent` middleware parses the `User-Agent` header into structured fields on `req.useragent` — useful for analytics and client quirks, not for security decisions because clients can spoof the header.

---

## What it does

```txt
User-Agent header ──middleware──► req.useragent { browser, os, isMobile, ... }
```

The library applies regular expressions against the header string. New browsers and bots may parse incorrectly until the library is updated.

---

## Usage

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
| Performance | Parsing is cheap; avoid re-parsing in every handler if mounted once |
| Alternatives | `ua-parser-js` and similar libraries |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `req.useragent` undefined | Middleware after routes | `app.use` before route handlers |
| Wrong mobile flag | New UA string | Update library; feature-detect on client |
| Missing fields | Bot or `curl` with no UA | Handle defaults |

---

## Do not use User-Agent for

- **Authentication or authorization** — trivial to spoof.
- **Responsive layout** — use CSS and `matchMedia` on the client.

Privacy: User-Agent is identifying; minimize logging in production.

---

## Related

[[express concepts]] · [[Express middleware]] · [[npm]]
