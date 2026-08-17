[[DNS]] [[dns record]] [[Protocol/SMTP]] [[E mail server]] [[DNS zone]]

# DSN records

> Email deliverability depends on DNS records beyond MX — SPF, DKIM, and DMARC TXT records tell receiving servers which hosts may send mail for your domain and what to do when authentication fails.

```txt
        DSN records ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Mail and platform interviews ask MX preference, single-SPF-record rule, DKIM …

## Sources
- [RFC 7208 — SPF](https://datatracker.ietf.org/doc/html/rfc7208) — deep-dive
- [RFC 6376 — DKIM](https://datatracker.ietf.org/doc/html/rfc6376) — deep-dive
- [RFC 7489 — DMARC](https://datatracker.ietf.org/doc/html/rfc7489) — deep-dive

## Key Concepts
- **MX:** where to deliver mail — lower preference number = higher priority.
- **SPF:** which IPs/includes may send for the domain (one SPF TXT).
- **DKIM:** cryptographic signature verified via selector TXT public key.
- **DMARC:** policy + reporting when SPF/DKIM alignment fails


- **Core:** Filename `DSN` in the vault is a historical typo for **DNS** mail records (no…

## Technical Details
| Record | Purpose |
|--------|---------|
| **MX** | Mail exchanger host + priority |
| **SPF (TXT)** | Authorized sending IPv4/IPv6/includes |
| **DKIM (TXT)** | Public key for signed message headers/body |
| **DMARC (TXT)** | Policy for SPF/DKIM alignment failures |
| **PTR** | Reverse DNS for sending IP (ISP/provider sets) |

```
example.com.  3600  IN  MX  10 mail.example.com.
mail.example.com.  A  203.0.113.20
```

- Lower preference value = higher priority.

- **SPF:** ([RFC 7208](https://datatracker.ietf.org/doc/html/rfc7208)):

```
example.com.  TXT  "v=spf1 ip4:203.0.113.0/24 include:_spf.google.com ~all"
```

| Mechanism | Meaning |
|-----------|---------|
| `ip4:` / `ip6:` | Allowed sender networks |
| `include:` | Delegate to another domain's SPF |
| `~all` | Softfail unauthorized |
| `-all` | Hardfail unauthorized |

- **One SPF TXT per domain:** — merge includes into a single record.

```
selector1._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=MIIB..."
```

- Mail server signs with private key; receivers verify with `p=` public key.
- Rotate selectors (`selector2`) before key expiry.

- **DMARC:** ([RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489)):

```
_dmarc.example.com.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; adkim=s; aspf=s"
```

| Tag | Effect |
|-----|--------|
| `p=none` | Monitor only |
| `p=quarantine` | Spam-folder failures |
| `p=reject` | Reject failures |
| `rua` | Aggregate report mailbox |

- Start with `p=none`, analyze reports, tighten policy.

```bash
dig +short MX example.com
dig +short TXT example.com
dig +short TXT _dmarc.example.com
dig +short TXT default._domainkey.example.com
```

## Mistakes to Avoid
- **Mistake:** Publishing multiple SPF TXT records instead of one merged string
- **Mistake:** Orange-cloud / proxying MX targets that must reach the real mail…
- **Mistake:** Enabling `p=reject` without reading `rua` aggregate reports first

## Pros/Cons or Trade-offs
- **Pro:** Strong authentication reduces spoofing and improves inbox placement.
- **Con:** SPF DNS lookup limits (`include:` chains) can break evaluation.
- **Con:** Jumping to `p=reject` before inventorying all legitimate senders drops real mail.

## Comparison
- vs generic [[dns record]]: these are the mail-auth subset operators touch weekly.
- vs Delivery Status Notification (SMTP DSN): bounce messages are not the same as these DNS TXT/MX …


### Use cases
- Google Workspace / Microsoft 365 / SendGrid onboarding

- **Example:** Add ESP `include:` to SPF, publish DKIM for `selector1`, set DMA…
