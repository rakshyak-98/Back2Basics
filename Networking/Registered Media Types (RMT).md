[[mime type]] [[response header]] [[HTTP]]

# Registered Media Types (RMT)

> Registered media types are the IANA catalog of `type/subtype` labels — so HTTP, mail, and APIs agree what `application/json` means.

```txt
        Registered Media T ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe media types to check registry awareness (`vnd.`, `+json` s…

## Sources
- [IANA Media Types Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) — deep-dive
- [RFC 6838 — Media Type Specifications and Registration](https://www.rfc-editor.org/rfc/rfc6838) — deep-dive
- [RFC 9239 — JavaScript Media Types Updates](https://www.rfc-editor.org/rfc/rfc9239) — overview
- [MDN — MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types) — overview

## Key Concepts
- **Type:** top-level class
- **Subtype:** specific format — `json`, `html`, `octet-stream`, `svg+xml`.
- **Parameters:** modifiers — `charset`, `boundary` (multipart).
- **Registration trees:** standards vs vendor (`vnd.`) vs personal
- **Structured suffix:** `+json`, `+xml`


- **Core:** A registered media type is an IANA-listed `type/subtype` (plus optional param…

## Technical Details
```txt
Content-Type: application/json; charset=utf-8
Accept: text/html, application/json;q=0.9
```

- Wrong type → download instead of render, JSON parse errors, XSS via `text/htm…

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

- **Why `charset=utf-8`:** avoids mojibake on non-ASCII JSON/text

| Symptom | Check | Fix |
|---------|-------|-----|
| Browser downloads file instead of showing | `application/octet-stream` | Fix `mime.types` mapping; explicit header |
| JSON.parse fails in browser | HTML error page with `text/html` | Read body; fix 502 page content-type |
| CORS preflight oddities | Custom media types trigger preflight | Use standard types; document custom |
| Android WebView blank | Missing charset | Add `; charset=utf-8` |

## Mistakes to Avoid
- **Mistake:** Using `text/javascript` when modern guidance prefers `applicatio…
- **Mistake:** Ignoring `+json` structured suffixes
- **Mistake:** Trusting client `Content-Type` alone on uploads
- **Mistake:** Inventing unregistered types without a vendor tree when others m…

## Pros/Cons or Trade-offs
- **Pro:** Shared IANA vocabulary — clients and servers agree without bilateral docs for common types.
- **Con:** Custom/`vnd.` types need documentation and may trigger CORS preflight.
- **Con:** Legacy aliases (`text/javascript` vs `application/javascript`) still appear in the wild.

## Comparison
- vs [[mime type]]: this note is registry + registration
- vs inventing `application/x-myformat`: prefer standard types or a documented `vnd.` name if you n…


### Use cases
- Browsers, APIs, and CDNs branch on registered types for rendering, negotiatio…

- **Example:** Nginx serves `.js` as `application/octet-stream` because `mime.t…
