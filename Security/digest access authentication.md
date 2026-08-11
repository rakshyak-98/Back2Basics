[[Security]] [[TLS (Transport Layer Security)]] [[Base64]] [[HMAC (Hash based Message Authentication Codes)]]

# digest access authentication

> Digest auth — browser proves it knows the password by sending a hash (with nonce), not the raw password — still prefer TLS + modern auth.

---

## Mental model

**Say it in one breath:** Server sends `WWW-Authenticate: Digest` with a nonce; client responds with `Authorization: Digest` containing hashes of username/realm/password/nonce/URI. Better than Basic-over-HTTP; weaker than Bearer/OIDC today.

```txt
Client                     Server
  │◄── 401 Digest realm, nonce ─┤
  │── Authorization: Digest … ─►│
  │◄── 200 ─────────────────────┤
```

| Scheme | Credential on wire |
|--------|--------------------|
| **Basic** | Base64(user:pass) — trivial to decode |
| **Digest** | Hash involving password + nonce |
| **Bearer** | Opaque/JWT token (modern APIs) |

---

## Standard config / commands

```nginx
# Example concept — many stacks discourage Digest now
location /private/ {
    auth_digest "Restricted";
    auth_digest_user_file /etc/nginx/passwd.digest;
}
```

```http
WWW-Authenticate: Digest realm="api", qop="auth", nonce="…", opaque="…"
Authorization: Digest username="u", realm="api", nonce="…", uri="/x", response="…"
```

| Knob | Why it matters |
|------|----------------|
| `nonce` + `qop` | Replay resistance (limited) |
| `realm` | Password hash is realm-scoped |
| HTTPS | Still required — Digest has known weaknesses |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Endless 401 | Stale nonce; clock; wrong realm | Fresh challenge; match realm/user file |
| Works in curl `-u`, fails Digest | Client sent Basic | Force Digest or use Bearer |
| Proxy strips `Authorization` | Ingress/auth middleware | Allow header through |
| User can’t log in after migrate | Passwd file format / realm change | Regenerate digest hashes for realm |
| Intermittent replay rejects | Nonce count (`nc`) | Sticky sessions or disable strict nc if legacy client |

---

## Gotchas

> [!WARNING]
> **Digest is not modern best practice** — phishing, downgrade, and algorithm limits remain; use OAuth/OIDC or session cookies over TLS.

> [!WARNING]
> **Basic + TLS ≠ Digest** — Basic is fine *with* TLS for simple cases; Digest’s advantage was mainly cleartext HTTP (don’t do that).

> [!WARNING]
> **Password file is hashed for a realm** — changing realm invalidates entries.

---

## When NOT to use

- **New public APIs** — Bearer JWT/OIDC or HMAC-signed requests.
- **Browser SPAs** — interactive login + CSRF-safe cookies or Authorization header.
- **High-security banking UX** — layered modern MFA, not Digest.

---

## Related

[[TLS (Transport Layer Security)]] [[HMAC (Hash based Message Authentication Codes)]] [[JWT]] [[Base64]] [[Authentication terms]]
