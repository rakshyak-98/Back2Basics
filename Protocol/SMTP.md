[[E mail server]] [[TCP]] [[DNS]]

# SMTP

> One-line: push protocol for MTA-to-MTA mail relay — submission on 587/TLS, legacy 25, implicit TLS 465 — **RFC 5321**.

## Mental model

SMTP is command/response between mail agents. **Submission** (client → MSA, port 587) differs from **relay** (MTA → MTA, port 25). Delivery authenticity is enforced separately via **SPF**, **DKIM**, **DMARC** (DNS TXT) — not by SMTP itself.

```
MUA ──587/TLS──► MSA/MTA ──25──► recipient MTA ──► MDA ──► mailbox
                      │
                 SPF/DKIM/DMARC checked at recipient
```

| Command | Purpose | Typical response |
|---------|---------|------------------|
| EHLO/HELO | Identify client | 250 extensions |
| MAIL FROM | Envelope sender (bounce address) | 250 |
| RCPT TO | Envelope recipient | 250 / 550 |
| DATA | Headers + body (`.` ends) | 354 → 250 |
| QUIT | Close | 221 |

Ports: **25** (MTA relay, often blocked on residential), **587** (submission + STARTTLS), **465** (SMTPS implicit TLS, legacy but common).

## Standard config / commands

```shell
# Manual SMTP dialog (debug)
openssl s_client -connect smtp.example.com:587 -starttls smtp
# EHLO client.example.com
# MAIL FROM:<sender@example.com>
# RCPT TO:<rcip@example.com>
# DATA
# Subject: test
# .
# QUIT

# Test delivery + headers
swaks --to rcip@example.com --from sender@example.com \
  --server smtp.example.com:587 --tls

# DNS auth records
dig +short example.com TXT                    # SPF
dig +short default._domainkey.example.com TXT # DKIM selector
dig +short _dmarc.example.com TXT             # DMARC
```

### SPF / DKIM / DMARC quick reference

| Mechanism | What it proves | Record location |
|-----------|----------------|-----------------|
| **SPF** | Sending IP authorized for domain | TXT at `@` |
| **DKIM** | Message signed; private key on MTA | TXT at `selector._domainkey` |
| **DMARC** | Policy for SPF/DKIM alignment + reporting | TXT at `_dmarc` |

Example SPF: `v=spf1 include:_spf.google.com ip4:203.0.113.0/24 -all`

Example DMARC: `v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; adkim=s; aspf=s`

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mail lands in spam | `Authentication-Results` header; mail-tester.com | Fix SPF/DKIM/DMARC alignment; warm IP; reverse PTR |
| `550 5.7.1 SPF fail` | `dig TXT example.com`; sending IP | Add IP/include to SPF; avoid `-all` until complete |
| `550 5.7.1 DKIM fail` | Selector TXT; signed headers | Re-sign with correct selector; clock skew on signer |
| DMARC `fail` in aggregate report | From domain vs DKIM d= vs SPF bounce domain | Align domains (envelope From = Header From); use same domain for DKIM |
| `Connection timed out` on :25 | Cloud SG blocks outbound 25 | Request provider unblock or relay via SES/SendGrid |
| `Relay access denied` | Auth required on 587 | Enable SASL; credentials in MUA |
| `421 4.7.0 try again` | Greylisting / rate limit | Retry; fix reputation; reduce burst volume |
| Works to Gmail, not corporate | Recipient MX logs / TLS requirement | Offer TLS 1.2+; valid cert on submission |
| Bounces with `550 5.1.1` | RCPT address valid? | Fix typo; verify MX for domain |
| Queue backlog | `mailq` / `postqueue -p` | Clear deferred; fix DNS; unblock RBL listing |

### Reading `Authentication-Results` (received mail)

```
spf=pass smtp.mailfrom=example.com
dkim=pass header.d=example.com
dmarc=pass action=none header.from=example.com
```

If any `fail` → trace that mechanism first.

### RBL / reputation

```shell
# Check if your IP is listed (example)
dig +short 113.0.0.203.zen.spamhaus.org   # reverse IP octets for some RBLs
```

## Gotchas

> [!WARNING]
> **SPF `-all` before all senders listed** → all mail fails. Use `~all` during migration, then tighten.

> [!WARNING]
> **Forwarding breaks SPF** — forwarded mail fails SPF at final recipient; DKIM often survives if not rewritten.

- **Envelope vs header From** — DMARC checks alignment on visible From domain.
- **Multiple DKIM selectors** during key rotation — publish both public keys until old mail expires.
- **Port 25 blocked on AWS/GCP default** — use submission API (SES) or request removal.
- **Greylisting** causes first delivery delay 5–15 min — normal, not always fixable.

## When NOT to use

- App transactional at scale → provider API (SES, Postmark) beats self-hosted MTA ops.
- Internal alerts only → Slack/webhook may beat email deliverability fight.

## Related

[[E mail server]] · [[DNS]] · [[DNS zone]] · [[TCP]]
