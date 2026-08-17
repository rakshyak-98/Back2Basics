[[Security]] [[TLS (Transport Layer Security)]] [[https]] [[response header]] [[content security policy]] [[certbot (letsencrypt)]]

# HTTP Strict Transport Security

> HSTS — browser remembers “this host is HTTPS-only,” so it never sends cleartext HTTP (and blocks cert bypass for preload).

```txt
        HTTP Strict Transp ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Hardening interviews: HSTS removes the cleartext HTTP window

## Sources
- [RFC 6797 — HSTS](https://www.rfc-editor.org/rfc/rfc6797) — deep-dive
- [MDN — Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) — overview

## Key Concepts
```txt
User types http://example.com
  → if HSTS known: rewrite to https:// (no cleartext request)
- **Note:** → if not: HTTP may still happen once (sslstrip window) unless preload
```

| Directive | Meaning |
|-----------|---------|
| `max-age` | How long to remember (seconds) |
| `includeSubDomains` | Apply to all subdomains |
| `preload` | Eligible for browser preload list |


- **Core:** HSTS tells browsers to speak only HTTPS to a host for a period, reducing SSL-…

## Technical Details
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
# Only after HTTPS is solid. Start with short max-age in canaries.
```

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

| Knob | Why it matters |
|------|----------------|
| Short `max-age` first | Recover from mis-issue without year-long lock |
| `includeSubDomains` | Needs HTTPS on **all** subs you care about |
| `preload` | Submit to hstspreload.org — hard to undo |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Site “stuck” on bad cert | HSTS cached | Fix cert; clear HSTS in browser (dev); wait max-age |
| HTTP still used first visit | No prior HSTS / no preload | Keep redirect + HSTS; consider preload carefully |
| Subdomain HTTP broken | `includeSubDomains` | Issue certs for subs or drop directive |
| Header missing on errors | nginx `add_header` without `always` | Add `always` |
| Mixed content after HSTS | HTTP asset URLs | Upgrade URLs / CSP upgrade-insecure-requests |

## Mistakes to Avoid
- **Mistake:** Don’t HSTS-preload before HTTPS is perfect
- **Mistake:** First visit still vulnerable — until HSTS is cached or preloaded
- **Mistake:** `max-age=0` — clears policy; use when deliberately rolling back

## Pros/Cons or Trade-offs
- **Pro:** Removes the cleartext HTTP window after the browser learns the policy.
- **Con:** HTTP-only internal tools — HSTS will fight you.
- **Con:** Hosts with intentional HTTP APIs on same domain — split hosts or avoid `includeSubDomains`.
- **Con:** Ephemeral review apps with unstable HTTPS — skip long max-age/preload.

## Comparison
- vs HTTPS redirect alone: redirect still allows a first cleartext request
- vs certificate pinning: HSTS is host-policy in the browser


### Use cases
- After HTTPS is reliable, send HSTS (optionally preload) so browsers stop clea…
