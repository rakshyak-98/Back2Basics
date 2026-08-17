[[SMTP]] [[IMAP (Internet Message Access Protocol)]] [[DNS]] [[TLS (Transport Layer Security)]] [[servers/DSN records]]

# mail server

> A mail server stack receives, routes, stores, and delivers email — SMTP moves messages between servers, IMAP or POP3 gives clients mailbox access, and DNS records (MX, SPF, DKIM, DMARC) determine whether receivers accept your mail.

---

## Why It Matters

Email looks simple from the user side but involves multiple protocols, ports, and DNS records that must align. Confusing port 25 (MTA relay) with 587 (authenticated submission), missing PTR records, or broken DKIM signing are the top causes of "mail not arriving" tickets. Self-hosting outbound mail at scale is a reputation game — most teams use transactional providers (SES, SendGrid) for outbound and self-host only when compliance demands it.

---

## Sources

- [RFC 5321 — Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321) — Normative SMTP specification for message relay, bounce handling, and envelope vs header addresses.
- [RFC 3501 — Internet Message Access Protocol](https://datatracker.ietf.org/doc/html/rfc3501) — IMAP4rev1 protocol for mailbox access, folder sync, and server-side search.
- [Google — Email sender guidelines](https://support.google.com/mail/answer/81126) — Practical requirements for deliverability to Gmail: SPF, DKIM, DMARC, and reverse DNS.
- [RFC 7208 — SPF](https://datatracker.ietf.org/doc/html/rfc7208) — Sender Policy Framework DNS record format for authorizing sending IPs.
- [RFC 6376 — DKIM](https://datatracker.ietf.org/doc/html/rfc6376) — DomainKeys Identified Mail — cryptographic signing of message headers and body.

---

## Key Concepts

```txt
Sender MUA (Thunderbird, app)
        │ SMTP submission (587 + STARTTLS + auth)
        ▼
   Outbound MTA (Postfix, Exim)
        │ SMTP (25) between MTAs
        ▼
   Recipient MX servers (DNS MX lookup)
        │ Delivery to mailbox
        ▼
Receiver MUA (IMAP 993 or POP3 995)
```

| Role | Protocol | Port | Purpose |
|------|----------|------|---------|
| **Submission** | SMTP + STARTTLS | 587 | Authenticated users send outbound mail |
| **MTA relay** | SMTP | 25 | Server-to-server delivery between domains |
| **Mailbox access** | IMAP | 993 (IMAPS) | Sync folders, server-side search |
| **Legacy mailbox** | POP3 | 995 (POP3S) | Download-and-delete model |

### DNS requirements

| Record | Purpose |
|--------|---------|
| **MX** | Points to the mail server hostname for the domain |
| **SPF** | Lists authorized sending IP addresses/subnets |
| **DKIM** | Public key for verifying signed message headers |
| **DMARC** | Policy for what receivers do when SPF/DKIM fail |
| **PTR** | Reverse DNS for sending IP — receivers check this |

### Common software stack

| Software | Role |
|----------|------|
| **Postfix** | MTA — send, receive, relay |
| **Exim** | MTA — Debian default historically |
| **Dovecot** | IMAP/POP3 mailbox server |
| **Rspamd / SpamAssassin** | Spam filtering |
| **OpenDKIM / Rspamd DKIM** | Outbound message signing |

---

## Technical Details

### Verify DNS setup

```bash
dig MX example.com +short
dig TXT example.com +short          # SPF record
dig TXT default._domainkey.example.com +short  # DKIM
dig TXT _dmarc.example.com +short     # DMARC policy
dig -x 203.0.113.10 +short           # PTR for sending IP
```

### Test SMTP connectivity

```bash
openssl s_client -connect mail.example.com:587 -starttls smtp
openssl s_client -connect mail.example.com:25 -starttls smtp
swaks --to user@example.com --from test@example.com --server mail.example.com:587 --tls
```

### Postfix submission config (conceptual)

```
# /etc/postfix/main.cf
smtpd_tls_cert_file = /etc/ssl/certs/mail.pem
smtpd_tls_key_file  = /etc/ssl/private/mail.key
smtpd_sasl_auth_enable = yes
submission inet n - n - - smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Mail to Gmail lands in spam | SPF/DKIM/DMARC alignment | Fix DNS; warm up IP reputation |
| Connection refused on 587 | Firewall; Postfix listening | `ss -lntp \| grep 587` |
| Relay denied | Not authenticated | Require SASL on submission |
| Bounce "550 relay not permitted" | Open relay misconfiguration | Restrict `mynetworks` and require auth |

---

## Mistakes to Avoid

- Using port 25 for client submission — use 587 with authentication.
- Skipping PTR/SPF/DKIM and blaming the MTA software for spam folder delivery.
- Leaving an open relay — anyone on the internet can send through your server.
- Disabling TLS on submission "for compatibility" — credentials travel in cleartext.
- Self-hosting high-volume outbound without IP warming and reputation monitoring.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Standard protocols — any client works | Deliverability is a reputation game |
| Full control over data residency | Self-hosted outbound at scale is hard |
| Rich ecosystem (Postfix, Dovecot) | DNS misconfiguration causes silent delivery failure |

---

## Comparison

| vs | Distinction |
|----|-------------|
| Transactional email (SES, SendGrid) | Managed reputation and APIs — preferred for app outbound |
| Chat (Slack, IRC) | Real-time; email is store-and-forward with DNS identity |
| [[SMTP]] | Protocol detail — this note is the full server stack |

---

## Use cases

- Corporate mailboxes with Dovecot IMAP and Postfix MTA.
- App transactional mail via Amazon SES with DKIM signing in Route 53.
- Debug "mail not arriving": `dig MX` → `openssl s_client` → check SPF/DKIM alignment.
