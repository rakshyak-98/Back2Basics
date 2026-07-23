[[PKI]] [[TLS (Transport Layer Security)]] [[fingerprint]] [[https]]

# Root certificate

> Self-signed trust anchor at the top of a certificate chain — browsers and OS trust stores decide whether your TLS cert is "valid."

---

## Mental model

**PKI chain**:

```txt
Root CA (self-signed, in trust store)
  └── Intermediate CA (signed by root)
        └── Leaf cert (your server CN/SAN)
```

**Root certificate**:
- **Self-signed** — issuer = subject
- **Long-lived** (10–25 years) — kept offline in HSM
- **Not** served by your web server in normal TLS (you send leaf + intermediates)

Trust stores: Mozilla/Apple/Microsoft/Google bundles on devices. Private roots (corp) require **manual install** on clients.

---

## Standard config / commands

### Inspect chain from server

```bash
openssl s_client -connect example.com:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer
```

### List system trust (Linux)

```bash
ls /etc/ssl/certs/ | head
trust list | grep -i example   # p11-kit
```

### Private CA root (lab only)

```bash
openssl req -x509 -newkey rsa:4096 -days 3650 -nodes \
  -keyout root.key -out root.crt -subj "/CN=Lab Root CA"
# Install root.crt on clients as trusted — never expose root.key
```

### Let's Encrypt chain (public)

```txt
Browser trusts ISRG Root X1 / DST cross-sign
You serve: cert.pem (leaf) + chain.pem (R3/E1 intermediate)
```

**Why intermediate exists:** compromise of intermediate doesn't burn root; root stays offline.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Untrusted cert in browser | Missing intermediate | Use `fullchain.pem`; fix nginx `ssl_certificate` |
| Corp laptop only fails | Private root not installed | Deploy MDM trust profile |
| Android old devices fail | Expired cross-sign | Update chain; use compatible CA |
| `certificate has expired` on root | Ancient client trust store | Client update; interim cert reissue |
| Pinning failure | Pin changed on root rotation | Update pins before CA migration |

---

## Gotchas

> [!WARNING]
> **Never put root private key on server** — only leaf + intermediate certs.

> [!WARNING]
> **Root expiration** (e.g. legacy AddTrust) breaks old clients — monitor CA announcements years ahead.

> [!WARNING]
> **Self-signed leaf ≠ private root** — dev `mkcert` is fine locally; prod needs public or managed private PKI.

> [!WARNING]
> **CT logs** — public CAs log issued certs; private roots don't — internal names still sensitive.

---

## When NOT to use

Don't create a **private root CA** unless you can **distribute trust** to all clients (MDM, mTLS fleet). Public sites use public CAs ([[certbot (letsencrypt)]]).

---

## Related

[[PKI]] [[TLS (Transport Layer Security)]] [[fingerprint]] [[DER]] [[read pem file]] [[code signing]]
