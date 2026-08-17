[[mime type]] [[response header]] [[HTTP]]

# Registered Media Types (RMT)

> Registered media types are the IANA catalog of `type/subtype` labels — so HTTP, mail, and APIs agree what `application/json` means.





## Interview Relevance
Interviewers probe media types to check registry awareness (`vnd.`, `+json` suffixes, charset) and security instincts (sniffing, trusting client-supplied types on uploads).

## Sources
- [IANA Media Types Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) — deep-dive
- [RFC 6838 — Media Type Specifications and Registration](https://www.rfc-editor.org/rfc/rfc6838) — deep-dive
- [RFC 9239 — JavaScript Media Types Updates](https://www.rfc-editor.org/rfc/rfc9239) — overview
- [MDN — MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types) — overview

## Core Definition
A registered media type is an IANA-listed `type/subtype` (plus optional parameters) used in `Content-Type` / `Accept` so independent systems interoperate on format meaning. Canonical day-to-day behavior: [[mime type]].

## Key Concepts
- **Type:** top-level class — `application`, `text`, `image`, `audio`, `video`, `multipart`.
- **Subtype:** specific format — `json`, `html`, `octet-stream`, `svg+xml`.
- **Parameters:** modifiers — `charset`, `boundary` (multipart).
- **Registration trees:** standards vs vendor (`vnd.`) vs personal — inventing unregistered types hurts interoperability.
- **Structured suffix:** `+json`, `+xml` — subtype still carries base semantics (e.g. `application/vnd.api+json`).

## Technical Details
```txt
Content-Type: application/json; charset=utf-8
Accept: text/html, application/json;q=0.9
```

Wrong type → download instead of render, JSON parse errors, XSS via `text/html` mislabel.

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

```bash
curl -sI https://example.com/app.js | grep -i content-type
curl -sI -X HEAD https://api.example.com/users | grep -i content-type
```

```javascript
res.setHeader('Content-Type', 'application/json; charset=utf-8');
```

```http
Content-Type: application/json
X-Content-Type-Options: nosniff
```

**Why `charset=utf-8`:** avoids mojibake on non-ASCII JSON/text; required for proper caching in some CDNs.

| Symptom | Check | Fix |
|---------|-------|-----|
| Browser downloads file instead of showing | `application/octet-stream` | Fix `mime.types` mapping; explicit header |
| JSON.parse fails in browser | HTML error page with `text/html` | Read body; fix 502 page content-type |
| CORS preflight oddities | Custom media types trigger preflight | Use standard types; document custom |
| Android WebView blank | Missing charset | Add `; charset=utf-8` |

## Real-World Applications
Browsers, APIs, and CDNs branch on registered types for rendering, negotiation, and caching.

**Example:** Nginx serves `.js` as `application/octet-stream` because `mime.types` is incomplete — browsers download instead of executing; add the mapping or set an explicit header.

## Pros/Cons or Trade-offs
- **Pro:** Shared IANA vocabulary — clients and servers agree without bilateral docs for common types.
- **Con:** Custom/`vnd.` types need documentation and may trigger CORS preflight.
- **Con:** Legacy aliases (`text/javascript` vs `application/javascript`) still appear in the wild.

## Comparison
- vs [[mime type]]: this note is registry + registration; [[mime type]] covers handlers, sniffing, and ops symptoms.
- vs inventing `application/x-myformat`: prefer standard types or a documented `vnd.` name if you need interoperability.

## Mistakes to Avoid
- Using `text/javascript` when modern guidance prefers `application/javascript` (RFC 9239).
- Ignoring `+json` structured suffixes — `application/vnd.api+json` still has JSON semantics.
- Trusting client `Content-Type` alone on uploads — validate magic bytes; don’t execute as script.
- Inventing unregistered types without a vendor tree when others must interoperate.
