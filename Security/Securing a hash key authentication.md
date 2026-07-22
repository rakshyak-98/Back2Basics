[[HMAC (Hash based Message Authentication Codes)]] [[Token rotation]] [[KMS]] [[https]]

# Securing a hash key authentication

> Operational playbook for shared MAC/API secrets — generate strong material, store safely, rotate, and detect compromise.

---

## Mental model

**Hash-key authentication** = server and client share a secret used to compute [[HMAC (Hash based Message Authentication Codes)]] or compare API key hashes:

```txt
Client:  Authorization: HMAC-SHA256 signature over canonical request
Server:  recompute with stored secret → timing-safe equal?
```

Threat model:
- **Leak** via git, logs, env dump, support ticket
- **Offline brute force** if secret weak or fast hash (MD5)
- **Replay** if no timestamp/nonce in signed payload

Security = **key hygiene** + **transport** + **verification discipline**.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail after deploy | Wrong secret version in pod | Sync secret mount; rollout restart |
| Intermittent 401 | Load balancer dual secrets | Sticky validation or complete rotation |
| Secret in logs | Debug logging request headers | Redact `Authorization`; structured logging filters |
| Suspected leak | Unusual IPs; spike in usage | Rotate immediately; invalidate old key |
| Timing attacks | Non-constant compare | `crypto.timingSafeEqual` |

---

## Gotchas

> [!WARNING]
> **Logging full request** includes `Authorization` — common leak vector.

> [!WARNING]
> **MD5/SHA1 for password storage** — use argon2/bcrypt/yescrypt — see [[yashcrypt]].

> [!WARNING]
> **Same secret all environments** — prod key in staging = breach multiplier.

> [!WARNING]
> **Query string signing** — URLs logged everywhere; prefer headers or POST body.

---

## When NOT to use

Shared MAC keys **don't scale** to untrusted third-party integrators — use OAuth/mTLS or asymmetric webhook signatures per consumer.

---

## Related

[[HMAC (Hash based Message Authentication Codes)]] [[Token rotation]] [[KMS]] [[https]] [[Authentication terms]]
