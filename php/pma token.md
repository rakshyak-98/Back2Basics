[[Security/CORS (Cross Origin Request Sharing)]] [[php]] [[Database/mysql/MySQL Events]]

# PMA token (phpMyAdmin)

> CSRF token in phpMyAdmin sessions — validates that form POSTs came from your logged-in UI, not a malicious site.

## Mental model

On login, phpMyAdmin stores `$_SESSION['PMA_token']` (name may vary by version). Every mutating form includes this token. Server compares submitted token to session; mismatch → rejected. Token rotates on login/session regenerate. It's **session CSRF protection**, not API auth.

## Standard config / commands

### Where it lives

- PHP session file or Redis/memcached session handler
- Browser cookie: `phpMyAdmin` session id

### Typical failure in logs

```
Token mismatch
```

### Fix session issues

```ini
; php.ini — consistent session path across FPM workers
session.save_path = "/var/lib/php/sessions"
session.cookie_httponly = 1
session.cookie_secure = 1    ; HTTPS only
```

```nginx
# Sticky not required if sessions on shared storage (Redis)
fastcgi_param HTTPS on;       ; if behind TLS terminator
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Token mismatch" after idle | Session expired | Re-login; increase `session.gc_maxlifetime` |
| Works on HTTP, fails on HTTPS | `cookie_secure` | Enable HTTPS end-to-end or fix proxy headers |
| Random logouts | Multiple FPM nodes, file sessions | Centralize sessions (Redis) |
| CSRF after reverse proxy | `PmaAbsoluteUri` in config | Set correct URL in `config.inc.php` |
| iframe/embed breaks token | `AllowThirdPartyFraming` | Don't embed PMA; open in top window |

## Gotchas

> [!WARNING]
> **Exposing phpMyAdmin to public internet** — token doesn't stop brute force; use VPN/IP allowlist + 2FA.
>
> **Session fixation** — ensure PMA regenerates session id on login (default in modern versions).

## When NOT to use

- Don't disable CSRF checks to "fix" integration — fix session/URL config instead.
- Don't use phpMyAdmin as your app's database API — it's an admin UI only.

## Related

[[Security/CORS (Cross Origin Request Sharing)]] [[Security/IDOR]] [[php]] [[Database/mysql/mysql ssl connection]]
