[[DNS]] · [[dns record]] · [[Protocol/SMTP]] · [[E mail server]]

# DSN records

> Email deliverability depends on DNS records beyond MX — SPF, DKIM, and DMARC TXT records tell receiving servers which hosts may send mail for your domain and what to do when authentication fails.

---

## Record set overview

| Record | Purpose |
|--------|---------|
| **MX** | Mail exchanger host + priority |
| **SPF (TXT)** | Authorized sending IPv4/IPv6/includes |
| **DKIM (TXT)** | Public key for signed message headers/body |
| **DMARC (TXT)** | Policy for SPF/DKIM alignment failures |
| **PTR** | Reverse DNS for sending IP (ISP/provider sets) |

Filename `DSN` in the vault is a historical typo for **DNS** mail records.

## MX example

```
example.com.  3600  IN  MX  10 mail.example.com.
mail.example.com.  A  203.0.113.20
```

Lower preference value = higher priority.

## SPF ([RFC 7208](https://datatracker.ietf.org/doc/html/rfc7208))

```
example.com.  TXT  "v=spf1 ip4:203.0.113.0/24 include:_spf.google.com ~all"
```

| Mechanism | Meaning |
|-----------|---------|
| `ip4:` / `ip6:` | Allowed sender networks |
| `include:` | Delegate to another domain's SPF |
| `~all` | Softfail unauthorized |
| `-all` | Hardfail unauthorized |

**One SPF TXT per domain** — merge includes into a single record.

## DKIM

```
selector1._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=MIIB..."
```

Mail server signs with private key; receivers verify with `p=` public key. Rotate selectors (`selector2`) before key expiry.

## DMARC ([RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489))

```
_dmarc.example.com.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; adkim=s; aspf=s"
```

| Tag | Effect |
|-----|--------|
| `p=none` | Monitor only |
| `p=quarantine` | Spam-folder failures |
| `p=reject` | Reject failures |
| `rua` | Aggregate report mailbox |

Start with `p=none`, analyze reports, tighten policy.

## Verify

```bash
dig +short MX example.com
dig +short TXT example.com
dig +short TXT _dmarc.example.com
dig +short TXT default._domainkey.example.com
```

## Recall

- What is the difference between SPF softfail (`~all`) and hardfail (`-all`)?
- Why do DKIM selectors simplify key rotation?

## Sources

- [RFC 7208 — SPF](https://datatracker.ietf.org/doc/html/rfc7208)
- [RFC 6376 — DKIM](https://datatracker.ietf.org/doc/html/rfc6376)
- [RFC 7489 — DMARC](https://datatracker.ietf.org/doc/html/rfc7489)
