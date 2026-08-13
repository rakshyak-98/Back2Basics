[[cookies]]

# cookies lifecycle

> cookies lifecycle — session — deleted when tab/session ends

---

## How it works

**Cookies types**
- Session -> deleted when tab/session ends
- Persistent -> stored until expiration
- Host-only -> not shared with subdomains
**Storage rules**
- Stored per domain + path scope
- Public suffix protection (cannot set `.com` etc)
- Attributes control visibility/security
`Path` -> Which routes auto-send this cookie
`Domain` -> Which subdomains can access it
`Max-Age/Expires` -> Defines **persistence**
`HttpOnly` -> JavaScript **cannot** read it
`Secure` -> Only over **HTTPS**
`SameSite` -> Controls cross-site sending
`Priority` -> Browser eviction order
**Automatic sending in requests**
- Browser checks domain + path + security flag
- If matched -> adds to `Cookie:` request header
`SameSite=Lax/strict` -> blocks many cross-site sends (CSRF defence).
`HttpOnly` -> protects from [[XSS cookie]]
**Phases**: `Client Request → Server Response (Set-Cookie) → Client Stores → Subsequent Requests → Server Reads → Expiry / Manual Deletion`


---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[cookies]]

## Sources

- [Wikipedia — cookies lifecycle](https://en.wikipedia.org/wiki/cookies_lifecycle)
