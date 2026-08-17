[[PKI]] [[TLS (Transport Layer Security)]] [[fingerprint]] [[https]] [[DER]] [[read pem file]] [[code signing]]

# Root certificate

> Self-signed trust anchor at the top of a certificate chain — browsers and OS trust stores decide whether your TLS cert is "valid."

```txt
        Root certificate ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Trust anchors: what a root is, why private CAs need distribution, and risks o…

## Sources
- [RFC 5280 — X.509](https://www.rfc-editor.org/rfc/rfc5280) — deep-dive
- [Mozilla CA Certificate Policy](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/) — overview

## Key Concepts
**PKI chain**:

```txt
Root CA (self-signed, in trust store)
  └── Intermediate CA (signed by root)
        └── Leaf cert (your server CN/SAN)
```

**Root certificate**:
- **Self-signed:** — issuer = subject
- **Long-lived:** (10–25 years) — kept offline in HSM
- **Not:** served by your web server in normal TLS (you send leaf + intermediates)

- **Note:** Trust stores: Mozilla/Apple/Microsoft/Google bundles on devices


- **Core:** A root certificate is a self-signed trust anchor at the top of a chain

## Technical Details
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

- **Why intermediate exists:** compromise of intermediate doesn't burn root

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Untrusted cert in browser | Missing intermediate | Use `fullchain.pem`; fix nginx `ssl_certificate` |
| Corp laptop only fails | Private root not installed | Deploy MDM trust profile |
| Android old devices fail | Expired cross-sign | Update chain; use compatible CA |
| `certificate has expired` on root | Ancient client trust store | Client update; interim cert reissue |
| Pinning failure | Pin changed on root rotation | Update pins before CA migration |

## Mistakes to Avoid
- **Mistake:** Never put root private key on server
- **Mistake:** Root expiration
- **Mistake:** Self-signed leaf ≠ private root
- **Mistake:** CT logs — public CAs log issued certs

## Pros/Cons or Trade-offs
- **Pro:** Single trust anchor can vouch for an entire private CA hierarchy.
- **Con:** Don't create a **private root CA** unless you can **distribute trust** to all clients (MDM, mTLS fleet). Public sites use public CAs ([[certbot (letsencrypt)]]).

## Comparison
- vs leaf/intermediate certs: root is the trust anchor; leaves end the chain.
- vs [[fingerprint]]: operators may pin a root fingerprint when distributing a private CA.


### Use cases
- Enterprise MITM appliances and private CAs require distributing a corporate r…
