[[mime type]] [[response header]] [[HTTP]]

# Registered Media Types (RMT)

> IANA-maintained identifiers for content formats — HTTP `Content-Type` / `Accept` values that tell clients how to parse the body.

---

## Mental model

**Media types** (MIME types) are `type/subtype` plus optional parameters:

```txt
Content-Type: application/json; charset=utf-8
Accept: text/html, application/json;q=0.9
```

Structure:
- **Type** — `application`, `text`, `image`, `audio`, `video`, `multipart`
- **Subtype** — `json`, `html`, `octet-stream`, `svg+xml`
- **Parameters** — `charset`, `boundary` (multipart)

Registered in **IANA media types registry**. Browsers, APIs, and CDNs branch on this — wrong type → download instead of render, JSON parse errors, XSS via `text/html` mislabel.

Canonical deep dive: **[[mime type]]**.

---

## Standard config / commands

### Send correct type (Nginx)

```nginx
types {
    application/json json;
    text/css css;
    application/javascript js;
}
include /etc/nginx/mime.types;
default_type application/octet-stream;
```

### curl inspect

```bash
curl -sI https://example.com/app.js | grep -i content-type
curl -sI -X HEAD https://api.example.com/users | grep -i content-type
```

### API server

```javascript
res.setHeader('Content-Type', 'application/json; charset=utf-8');
```

### Sniffing override (security)

```http
Content-Type: application/json
X-Content-Type-Options: nosniff
```

**Why `charset=utf-8`:** avoids mojibake on non-ASCII JSON/text; required for proper caching in some CDNs.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Browser downloads file instead of showing | `application/octet-stream` | Fix `mime.types` mapping; explicit header |
| JSON.parse fails in browser | HTML error page with `text/html` | Read body; fix 502 page content-type |
| CORS preflight oddities | Custom media types trigger preflight | Use standard types; document custom |
| Android WebView blank | Missing charset | Add `; charset=utf-8` |

---

## Gotchas

> [!WARNING]
> **`application/javascript` vs `text/javascript`** — use modern `application/javascript` (RFC 9239).

> [!WARNING]
> **`+json` structured suffix** — `application/vnd.api+json` still JSON semantics.

> [!WARNING]
> **Trusting client `Content-Type` alone** — validate magic bytes for uploads; don't execute as script.

---

## When NOT to use

Don't invent `application/x-myformat` without vendor tree (`vnd.`) if you need interoperability — register or document clearly.

---

## Related

[[mime type]] [[response header]] [[content security policy]] [[CORS (Cross Origin Request Sharing)]]
