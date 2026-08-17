[[Security]] [[TLS (Transport Layer Security)]] [[Base64]] [[HMAC (Hash based Message Authentication Codes)]] [[JWT]] [[Authentication terms]]

# digest access authentication

> Digest auth — browser proves it knows the password by sending a hash (with nonce), not the raw password — still prefer TLS + modern auth.

```txt
        digest access auth ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Legacy auth: Digest avoids sending the raw password but is obsolete for new a…

## Sources
- [RFC 7616 — HTTP Digest Access Authentication](https://www.rfc-editor.org/rfc/rfc7616) — deep-dive
- [MDN — HTTP authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) — overview

## Key Concepts
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


- **Core:** HTTP Digest authentication proves password knowledge with a hash involving a …

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Endless 401 | Stale nonce; clock; wrong realm | Fresh challenge; match realm/user file |
| Works in curl `-u`, fails Digest | Client sent Basic | Force Digest or use Bearer |
| Proxy strips `Authorization` | Ingress/auth middleware | Allow header through |
| User can’t log in after migrate | Passwd file format / realm change | Regenerate digest hashes for realm |
| Intermittent replay rejects | Nonce count (`nc`) | Sticky sessions or disable strict nc if legacy client |

## Mistakes to Avoid
- **Mistake:** Digest is not modern best practice
- **Mistake:** Basic + TLS ≠ Digest
- **Mistake:** Password file is hashed for a realm

## Pros/Cons or Trade-offs
- **Pro:** Better than cleartext Basic on ancient clients when TLS is missing (legacy only).
- **Con:** New public APIs — Bearer JWT/OIDC or HMAC-signed requests.
- **Con:** Browser SPAs — interactive login + CSRF-safe cookies or Authorization header.
- **Con:** High-security banking UX — layered modern MFA, not Digest.

## Comparison
- vs Basic auth: Digest avoids cleartext password but is still legacy.
- vs [[JWT]] / session cookies over [[TLS (Transport Layer Security)]]: prefer modern schemes for n…


### Use cases
- Legacy device UIs and old proxies may still speak Digest
