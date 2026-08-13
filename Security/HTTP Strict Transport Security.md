<!-- note-strategy: operational -->
[[Security]] [[TLS (Transport Layer Security)]] [[https]] [[response header]]

# HTTP Strict Transport Security

> HSTS — browser remembers “this host is HTTPS-only,” so it never sends cleartext HTTP (and blocks cert bypass for preload).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** First HTTPS response can send `Strict-Transport-Security`; for `max-age` seconds the browser upgrades `http://` to `https://` automatically and refuses to ignore invalid certs (when policy applies).

```txt
User types http://example.com
  → if HSTS known: rewrite to https:// (no cleartext request)
  → if not: HTTP may still happen once (sslstrip window) unless preload
```

| Directive | Meaning |
|-----------|---------|
| `max-age` | How long to remember (seconds) |
| `includeSubDomains` | Apply to all subdomains |
| `preload` | Eligible for browser preload list |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Site “stuck” on bad cert | HSTS cached | Fix cert; clear HSTS in browser (dev); wait max-age |
| HTTP still used first visit | No prior HSTS / no preload | Keep redirect + HSTS; consider preload carefully |
| Subdomain HTTP broken | `includeSubDomains` | Issue certs for subs or drop directive |
| Header missing on errors | nginx `add_header` without `always` | Add `always` |
| Mixed content after HSTS | HTTP asset URLs | Upgrade URLs / CSP upgrade-insecure-requests |

---

## Gotchas

> [!WARNING]
> **Don’t HSTS-preload before HTTPS is perfect** — bad cert + preload = outage for users.

> [!WARNING]
> **First visit still vulnerable** — until HSTS is cached or preloaded.

> [!WARNING]
> **`max-age=0`** — clears policy; use when deliberately rolling back.

---

## When NOT to use

- **HTTP-only internal tools** — HSTS will fight you.
- **Hosts with intentional HTTP APIs on same domain** — split hosts or avoid `includeSubDomains`.
- **Ephemeral review apps with unstable HTTPS** — skip long max-age/preload.

---

## Related

[[https]] [[TLS (Transport Layer Security)]] [[response header]] [[content security policy]] [[certbot (letsencrypt)]]
