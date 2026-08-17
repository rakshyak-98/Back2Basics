[[cookies lifecycle]] [[cookie error]] [[Security/CORS (Cross Origin Request Sharing)]]

# Cookies configuration

> `Set-Cookie` attributes control where a cookie lives, how long, and when the browser attaches it — `Domain`, `Path`, `Expires`/`Max-Age`, `Secure`, `HttpOnly`, `SameSite`.

```txt
        Cookies configurat ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Security reviews expect `HttpOnly` + `Secure` + appropriate `SameSite` for…

## Sources
- [RFC 6265bis drafts / MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie) — deep-dive
- [OWASP — Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — overview

## Key Concepts
- **`HttpOnly`:** not readable from JavaScript → mitigates XSS token theft.
- **`Secure`:** HTTPS only.
- **`SameSite`:** `Strict`/`Lax`/`None` → cross-site send policy.
- **`Domain` / `Path`:** scope of inclusion on requests.
- **Lifetime:** session cookie vs persistent (`Expires`/`Max-Age`).

## Technical Details
```http
Set-Cookie: sessionToken=abc123; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=3600
```

| Attribute | Effect |
|-----------|--------|
| `HttpOnly` | No `document.cookie` access |
| `Secure` | HTTPS only |
| `SameSite=Lax` | Sent on top-level GETs; safer default |
| `SameSite=None` | Cross-site; requires `Secure` |
| `Max-Age=0` | Delete |

## Mistakes to Avoid
- **Mistake:** Broad `Domain=.company.com` sharing sessions across all apps uni…
- **Mistake:** Missing `Secure` in production
- **Mistake:** Relying on `SameSite=Strict` then wondering OAuth return navigat…

## Pros/Cons or Trade-offs
- **Pro:** Declarative browser-enforced policy.
- **Con:** Misconfiguration fails closed (cookie missing) and is hard to see without DevTools.

## Comparison
- vs localStorage tokens: cookies can be HttpOnly; storage cannot.
- vs [[cookies lifecycle]]: configuration is attributes; lifecycle is create→send→expire.


### Use cases
- Session cookie for a first-party web app: `HttpOnly

- **Example:** Marketing site on another subdomain should not receive the sessi…
