[[cookies configuration]] [[cookie error]] [[Feature implementation/Manage cart with session id]]

# Cookies lifecycle

> Create via `Set-Cookie`, store in the browser jar, send on matching requests, then expire or delete — session cookies die with the browser session; persistent ones use timers.





## Interview Relevance
Interviewers ask when cookies are sent, difference between session vs persistent, and how logout deletes server session *and* clears the cookie.

## Sources
- [MDN — Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) — overview
- [RFC 6265](https://datatracker.ietf.org/doc/html/rfc6265) — deep-dive

## Key Concepts
- **Set:** server response `Set-Cookie` (or JS for non-HttpOnly).
- **Store:** browser cookie jar scoped by scheme/host/path rules.
- **Send:** request `Cookie` header when scope + SameSite allow.
- **End:** expire by time, delete with past `Expires`/`Max-Age=0`, or session end.

## Technical Details
```txt
Set-Cookie → browser store → matching request includes Cookie → expire/delete
```

| Kind | Lifetime |
|------|----------|
| Session | Until browser session ends (roughly) |
| Persistent | Until `Expires` / `Max-Age` |

Logout pattern: invalidate server-side session id; set cookie `Max-Age=0`.

## Real-World Applications
Guest cart session cookie lasts seven days; login rotates session id and may promote to a longer authenticated cookie.

**Example:** User “logs out” but API still accepts the old id — you cleared the cookie only on one subdomain path.

## Pros/Cons or Trade-offs
- **Pro:** Automatic attach on requests reduces client glue.
- **Con:** Lifecycle bugs show up as intermittent auth (especially across subdomains).

## Comparison
- vs bearer header auth: explicit per call; no automatic jar lifecycle.
- vs [[cookies configuration]]: lifecycle is the time dimension; configuration is the attribute dimension.

## Mistakes to Avoid
- Deleting cookies only in DevTools while debugging server sessions that still exist.
- Assuming all browsers end “session” cookies at the same time (restore policies differ).
- Setting a new session cookie without invalidating the old server session.
