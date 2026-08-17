[[cookies lifecycle]] [[cookies configuration]] [[Security/CORS (Cross Origin Request Sharing)]]

# Cookie errors (cross-origin)

> Browser refuses to store or send cookies across sites when `Secure`/`SameSite`/domain attributes disagree with how the frontend and API are hosted.





## Interview Relevance
Interviewers love cross-site cookie debugging: `SameSite=None; Secure`, HTTPS requirements, and SPA-on-localhost calling `api.example.com`.

## Sources
- [MDN — SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite) — deep-dive
- [Chrome — Cookies default SameSite](https://www.chromium.org/updates/same-site/) — overview

## Key Concepts
- **Hosted on different sites:** frontend and API may be cross-site → `SameSite=None` needs `Secure`.
- **Dev vs prod:** `localhost` vs real HTTPS domains behave differently.
- **Third-party blocking:** browsers increasingly restrict cross-site cookies.
- **CORS ≠ cookie magically works:** you still need `credentials` mode + correct `Access-Control-Allow-Credentials` and a non-`*` origin.

## Technical Details
```txt
Browser stores cookie for api.example.com
SPA on app.example.com → cross-site request → SameSite rules apply
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Set-Cookie ignored | Secure/SameSite/domain | Align attributes with HTTPS topology |
| Cookie not sent | Site context | `SameSite=None; Secure` or same-site deploy |
| CORS error with credentials | ACAO `*` | Echo specific origin; allow credentials |

## Real-World Applications
SPA + API on sibling subdomains: prefer same-site parent domain cookie strategy or first-party BFF proxy to avoid third-party cookie pain.

**Example:** Local Vite app → production API cookies rejected — use a local proxy or HTTPS tunnel matching attributes.

## Pros/Cons or Trade-offs
- **Pro:** Cookie auth is browser-native for first-party apps.
- **Con:** Cross-site setups are fragile under modern browser rules.

## Comparison
- vs bearer tokens in memory: fewer cookie attribute issues; more XSS token theft risk if stored wrong.
- vs [[cookies configuration]]: errors note is triage; configuration note is attribute meanings.

## Mistakes to Avoid
- `SameSite=None` without `Secure`.
- `Access-Control-Allow-Origin: *` with credentialed requests.
- Setting `Domain=.example.com` incorrectly for localhost.
