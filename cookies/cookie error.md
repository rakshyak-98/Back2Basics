[[cookies lifecycle]] [[cookies configuration]] [[Security/CORS (Cross Origin Request Sharing)]]

# Cookie errors (cross-origin)

> Browser refuses to store or send cookies across sites when `Secure`/`SameSite`/domain attributes disagree with how the frontend and API are hosted.

```txt
        Cookie errors (cro ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers love cross-site cookie debugging: `SameSite=None

## Sources
- [MDN — SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite) — deep-dive
- [Chrome — Cookies default SameSite](https://www.chromium.org/updates/same-site/) — overview

## Key Concepts
- **Hosted on different sites:** frontend and API may be cross-site → `SameSite=None` needs `Secure`.
- **Dev vs prod:** `localhost` vs real HTTPS domains behave differently.
- **Third-party blocking:** browsers increasingly restrict cross-site cookies.
- **CORS ≠ cookie magically works:** you still need `credentials` mode + correct `Access-Control-Allow-Credentials…

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

## Mistakes to Avoid
- **Mistake:** `SameSite=None` without `Secure`
- **Mistake:** `Access-Control-Allow-Origin: *` with credentialed requests
- **Mistake:** Setting `Domain=.example.com` incorrectly for localhost

## Pros/Cons or Trade-offs
- **Pro:** Cookie auth is browser-native for first-party apps.
- **Con:** Cross-site setups are fragile under modern browser rules.

## Comparison
- vs bearer tokens in memory: fewer cookie attribute issues
- vs [[cookies configuration]]: errors note is triage; configuration note is attribute meanings.


### Use cases
- SPA + API on sibling subdomains: prefer same-site parent domain cookie strate…

- **Example:** Local Vite app → production API cookies rejected
