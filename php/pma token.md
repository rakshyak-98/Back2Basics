[[php]] [[Security/CORS (Cross Origin Request Sharing)]] [[Security/IDOR]] [[cookies/cookies lifecycle]]

# PMA token (phpMyAdmin)

> CSRF token inside phpMyAdmin’s session — proves state-changing POSTs came from the logged-in UI, not a foreign site.

## Interview Relevance

Interviewers use this to check CSRF fundamentals: session-bound token, why “token mismatch” appears behind proxies, and that it is not API auth.

## Sources

- [phpMyAdmin docs — Configuration](https://docs.phpmyadmin.net/en/latest/config.html) — deep-dive
- [OWASP — Cross-Site Request Forgery](https://owasp.org/www-community/attacks/csrf) — overview

## Key Concepts

- **Session CSRF token:** stored server-side; must accompany mutating forms.
- **Mismatch causes:** expired session, multi-node file sessions, wrong public URL behind TLS terminator.
- **Not authentication:** still need strong login, network limits, and preferably VPN allowlists.
- **Admin UI only:** do not treat phpMyAdmin as your application’s data API.

## Technical Details

```ini
session.save_path = "/var/lib/php/sessions"
session.cookie_httponly = 1
session.cookie_secure = 1
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Token mismatch after idle | Session TTL | Re-login; tune `gc_maxlifetime` |
| Random logouts on scale-out | Local file sessions | Shared session store (Redis) |
| Breaks behind reverse proxy | Public URL | Set `PmaAbsoluteUri` correctly |
| HTTP OK, HTTPS fails | `cookie_secure` / HTTPS headers | Fix TLS termination flags |

## Real-World Applications

Internal DBA access via VPN with MFA; sessions on Redis when multiple FPM nodes serve PMA.

**Example:** Token mismatch after putting PMA behind a path prefix — fix absolute URI and cookie path settings.

## Pros/Cons or Trade-offs

- **Pro:** Stops basic CSRF on a powerful admin tool.
- **Con:** Does nothing against stolen sessions or exposed public PMA.

## Comparison

- vs API bearer tokens: PMA token is browser CSRF protection, not machine auth.
- vs SameSite cookies: complementary layers; do not disable CSRF checks “because SameSite.”

## Mistakes to Avoid

- Disabling CSRF checks to unblock automation.
- Exposing phpMyAdmin to the open internet with only a password.
- Embedding PMA in iframes and breaking token/cookie rules.
