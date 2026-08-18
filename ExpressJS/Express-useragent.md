[[ExpressJS]] [[express concepts]] [[npm]]

# Express-useragent

> `express-useragent` — middleware that parses `User-Agent` into a structured object on `req` (browser/OS/device flags).

## Mental model

**Say it in one breath:** Read UA string → regex/parse → attach fields. Useful for analytics/quirks; easy to get wrong (spoofing, new browsers).

```txt
User-Agent header ──middleware──► req.useragent
```

## Standard config / commands

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

| Knob | Why it matters |

| Trust boundary | Clients lie |
| --- | --- |
| Caching parse | Hot paths |
| Alternatives | `ua-parser-js` etc. |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Undefined fields | Middleware order | `app.use` before routes |
| Wrong mobile flag | New UA | Update lib; feature-detect client |
| Missing header | Bot/curl | Defaults |

## Gotchas

> [!WARNING]
> **Never authorize by UA** — trivial spoof.

> [!WARNING]
> **Privacy** — UA is identifying-ish; minimize logging.

## When NOT to use

- **AuthN/AuthZ** — real credentials.
- **Responsive UI** — CSS/`matchMedia`.
- **Security decisions** — no.

## Related

[[express concepts]] [[Express middleware]] [[npm]]
