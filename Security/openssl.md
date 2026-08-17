[[Security]] [[TLS (Transport Layer Security)]] [[read pem file]] [[PKI]] [[DER]] [[Root certificate]] [[certbot (letsencrypt)]]

# openssl

> The Swiss-army CLI for keys, CSRs, certs, and TLS debugging on the box.

```txt
        openssl ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Hands-on PKI: generate keys/CSRs, inspect certs, and debug TLS handshakes wit…

## Sources
- [OpenSSL documentation](https://www.openssl.org/docs/) — deep-dive
- [man openssl](https://www.openssl.org/docs/manmaster/man1/openssl.html) — overview

## Key Concepts
```txt
private key ──► CSR ──► CA signs ──► leaf.crt
                 │
                 └── self-sign (lab only) ──► cert.pem
```


- **Core:** OpenSSL is the standard CLI/library for keys, CSRs, certificates, and TLS deb…

## Technical Details
```bash
# Self-signed lab cert (no passphrase on key)
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 365 -nodes -subj "/CN=localhost"

# Nginx-style local HTTPS
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/certs/shop.localhost.key \
  -out /etc/nginx/certs/shop.localhost.crt \
  -subj "/CN=shop.localhost"
# Common Name / SAN must match the hostname you type in the browser

# Key + CSR + self-sign
openssl genpkey -algorithm RSA -out privatekey.pem -aes256
openssl req -key privatekey.pem -new -out request.csr
openssl x509 -req -days 365 -in request.csr -signkey privatekey.pem -out certificate.crt

# Inspect
openssl req -in request.csr -text -noout
openssl x509 -in certificate.crt -text -noout
openssl x509 -in certificate.crt -noout -subject -issuer -fingerprint -dates
openssl verify -CAfile ca_bundle.crt certificate.crt

# Live TLS
openssl s_client -connect example.com:443 -servername example.com </dev/null | openssl x509 -noout -dates -subject
```

| Flag | Why it matters |
|------|----------------|
| `-nodes` | No passphrase on private key (needed for unattended nginx) |
| `-subj "/CN=…"` | Non-interactive; still prefer SANs for modern clients |
| `-servername` | SNI — right cert on multi-vhost hosts |

### Generate random string

```bash
openssl rand -hex 32
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to load Private Key` | Passphrase; PEM vs DER; wrong file | `-nodes` or supply pass; convert format |
| Browser name mismatch | CN/SAN vs URL | Reissue with correct CN/SAN |
| `verify error:num=20` | Missing intermediate / wrong CAfile | Pass full chain; fix `-CAfile` |
| `s_client` shows wrong cert | SNI missing | Add `-servername` |
| Permission denied reading key | File mode / user | `chmod 600`; run service as owner |
| Typo `private.key` vs `privatekey.pem` | Path in docs vs disk | Align filenames in scripts |

## Mistakes to Avoid
- **Mistake:** Self-signed ≠ trusted
- **Mistake:** `-aes256` on keys
- **Mistake:** CN alone is fragile

## Pros/Cons or Trade-offs
- **Pro:** Universal CLI for PKI and TLS debugging on servers and CI.
- **Con:** Public production certs — use [[certbot (letsencrypt)]] / ACME, not hand-rolled OpenSSL + email CSR unless required.
- **Con:** application-level crypto APIs — prefer language libs (crypto, NaCl); don’t shell out to openssl in hot paths.
- **Con:** Password hashing — use Argon2/bcrypt/yescrypt, not ad-hoc OpenSSL digests.

## Comparison
- vs [[certbot (letsencrypt)]]: OpenSSL is the toolkit; Certbot automates ACME issuance.
- vs GUI cert managers: CLI is scriptable for CI and break-glass debugging.


### Use cases
- Generate CSRs, inspect `fullchain.pem`, and `s_client`-debug handshake failur…
