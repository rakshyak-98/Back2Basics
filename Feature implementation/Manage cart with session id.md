[[cookies/cookies lifecycle]] [[marketplace app]] [[Security/IDOR]]

# Manage cart with session id

> Guest carts bind to a server-side session identifier — persist line items until login merges into a user cart or the session expires.





## Interview Relevance
Interviewers want cookie/session fixation awareness, merge-on-login rules, and concurrency when two tabs mutate the same cart.

## Sources
- [OWASP — Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — deep-dive
- [MDN — HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) — overview

## Key Concepts
- **Anonymous session id:** opaque token in a cookie → server stores cart rows keyed by it.
- **Merge on login:** combine guest + user carts with deterministic conflict rules.
- **TTL:** expire idle carts; do not keep forever.
- **Authorization:** never accept client-supplied “session id” in raw body without cookie binding checks.

## Technical Details
```txt
Browser cookie sid → API → cart_items(session_id)
Login → merge(session cart, user cart) → new authenticated cart
```

| Issue | Approach |
|-------|----------|
| Session fixation | Rotate id on login |
| Tab races | Row version / transactional updates |
| IDOR | Server derives sid from cookie, not user input |

## Real-World Applications
Ecommerce guest checkout: shop before account creation; merge when the user signs in.

**Example:** User adds items as guest on phone, logs in — duplicate SKUs merge quantities rather than duplicating lines.

## Pros/Cons or Trade-offs
- **Pro:** Low-friction shopping without forced signup.
- **Con:** Cookie/privacy constraints and multi-device continuity limits.

## Comparison
- vs purely client localStorage carts: server carts survive browser clears less often but need session infra.
- vs user-only carts: simpler security, worse conversion.

## Mistakes to Avoid
- Trusting `sessionId` from JSON body over the signed cookie.
- Losing the guest cart on login (no merge).
- Letting carts become an unbounded growth table without TTL jobs.
