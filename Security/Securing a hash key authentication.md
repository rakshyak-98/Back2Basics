[[HMAC (Hash based Message Authentication Codes)]] [[Token rotation]] [[KMS]] [[https]] [[Authentication terms]]

# Securing a hash key authentication

> Shared-secret HMAC authentication done safely — vault the key, rotate it, verify tags in constant time, always over TLS.





## Interview Relevance
API design: shared-secret HMAC auth — key storage, rotation, timing-safe compare, and transport over TLS.

## Sources
- [OWASP — REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) — overview
- [RFC 2104 — HMAC](https://www.rfc-editor.org/rfc/rfc2104) — deep-dive

## Core Definition
Hash-key authentication means client and server share a secret used to compute an HMAC (or similar) tag; securing it is key custody, rotation, and constant-time verification.

## Key Concepts
**Hash-key authentication** = server and client share a secret used to compute [[HMAC (Hash based Message Authentication Codes)]] or compare API key hashes:

```txt
Client:  Authorization: HMAC-SHA256 signature over canonical request
Server:  recompute with stored secret → timing-safe equal?
```

Threat model:
- **Leak** via git, logs, environment dump, support ticket
- **Offline brute force** if secret weak or fast hash (MD5)
- **Replay** if no timestamp/nonce in signed payload

Security = **key hygiene** + **transport** + **verification discipline**.

## Technical Details
### Generate strong secrets

```bash
openssl rand -hex 32          # 256-bit hex secret
openssl rand -base64 32       # URL-safe with encoding care
```

### Store in KMS / vault (not plaintext env in repo)

```bash
# AWS example
aws secretsmanager create-secret --name prod/api/hmac-key --secret-string "$(openssl rand -hex 32)"
```

```yaml
# K8s — reference secret, don't inline
env:
  - name: HMAC_KEY
    valueFrom:
      secretKeyRef:
        name: api-hmac
        key: primary
```

### Verify HMAC (Node)

```javascript
import crypto from 'crypto';
function verify(body, sig, secret) {
  const expected = crypto.createHmac('sha256', secret).update(body).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(sig, 'hex'), Buffer.from(expected, 'hex'));
}
```

### Rotation with dual-key window

```txt
Day 0: accept primary + secondary; issue new creds with secondary
Day 7: revoke primary; secondary → primary
```

See [[Token rotation]].

### Require HTTPS

```nginx
# Reject plaintext API
if ($scheme != "https") { return 301 https://$host$request_uri; }
```

**Why KMS:** audit trail, IAM access, automatic rotation hooks — not grep-able in `.env` backups.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail after deploy | Wrong secret version in pod | Sync secret mount; rollout restart |
| Intermittent 401 | Load balancer dual secrets | Sticky validation or complete rotation |
| Secret in logs | Debug logging request headers | Redact `Authorization`; structured logging filters |
| Suspected leak | Unusual IPs; spike in usage | Rotate immediately; invalidate old key |
| Timing attacks | Non-constant compare | `crypto.timingSafeEqual` |

## Real-World Applications
Partner webhooks and machine APIs authenticate with rotated HMAC secrets stored in a vault or KMS.

## Pros/Cons or Trade-offs
- **Pro:** Simple machine auth when mutual TLS or OAuth is overkill — if keys are vaulted.
- **Con:** Shared MAC keys **don't scale** to untrusted third-party integrators — use OAuth/mTLS or asymmetric webhook signatures per consumer.

## Comparison
- vs [[HMAC (Hash based Message Authentication Codes)]]: HMAC is the primitive; this note is operational key hygiene.
- vs [[KMS]]: prefer KMS/vault over long-lived plaintext secrets on disk.

## Mistakes to Avoid
- Logging full request — includes `Authorization` — common leak vector.
- MD5/SHA1 for password storage — use argon2/bcrypt/yescrypt — see [[yashcrypt]].
- Same secret all environments — prod key in staging = breach multiplier.
- Query string signing — URLs logged everywhere; prefer headers or POST body.
