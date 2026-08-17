[[SMTP]] [[IMAP (Internet Message Access Protocol)]] [[DNS]] [[TLS (Transport Layer Security)]] [[E mail server]]

# mail server

> A mail server stack receives, routes, stores, and delivers email — SMTP between servers, IMAP or POP3 for clients; delivery fails when DNS (MX/SPF/DKIM/DMARC) or TLS policy mismatches receivers.





## Interview Relevance
Interviewers expect you to name submission versus relay ports, the MTA/IMAP split, and which DNS records decide inbox versus spam.

## Sources
- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321) — deep-dive
- [RFC 3501 — IMAP](https://datatracker.ietf.org/doc/html/rfc3501) — overview
- [Google — Email sender guidelines](https://support.google.com/mail/answer/81126) — overview

## Key Concepts
- **MUA → MTA → MX → mailbox:** clients submit; MTAs relay; recipient MX accepts; IMAP/POP3 serves the mailbox.
- **Submission vs relay:** 587 for authenticated users; 25 for MTA-to-MTA.
- **DNS authenticity:** MX for destination; SPF/DKIM/DMARC against spoofing; PTR for sending IP reputation.
- **Software roles:** Postfix/Exim as MTA; Dovecot as IMAP; Rspamd for filtering.

## Technical Details
```
Sender MUA (Thunderbird, Gmail UI)
        │ SMTP submission (587 + STARTTLS)
        ▼
   Outbound MTA (Postfix, Exim)
        │ SMTP (25) between MTAs
        ▼
   Recipient MX servers
        │ IMAP/POP3 (993/995)
        ▼
Receiver MUA
```

| Role | Protocol | Port (typical) |
|------|----------|----------------|
| **Submission** | [[SMTP]] + STARTTLS | 587 |
| **Relay between domains** | SMTP | 25 |
| **Mailbox access** | [[IMAP (Internet Message Access Protocol)]] | 993 (IMAPS) |
| **Legacy mailbox** | POP3 | 995 (POP3S) |

DNS requirements ([[servers/DSN records]]):

- **MX** — where mail for the domain goes
- **SPF / DKIM / DMARC** — anti-spoofing and reputation
- **PTR** — reverse DNS for sending IP

| Software | Role |
|----------|------|
| **Postfix** | MTA (send/receive) |
| **Exim** | MTA (Debian default historically) |
| **Dovecot** | IMAP/POP3 server |
| **Rspamd / SpamAssassin** | Filtering |
| **OpenDKIM / Rspamd DKIM** | Signing |

Managed alternatives: Google Workspace, Microsoft 365, Amazon SES.

```bash
dig MX example.com +short
openssl s_client -connect mail.example.com:25 -starttls smtp
swaks --to user@example.com --from test@example.com --server mail.example.com
```

## Real-World Applications
Corporate mailboxes, transactional mail from apps, and partner integrations that still require SMTP drop boxes.

**Example:** Debug “mail not arriving” with `dig MX`, then `openssl s_client -starttls smtp` to confirm the MX speaks TLS before chasing application bugs.

## Pros/Cons or Trade-offs
- **Pro:** Standard protocols everywhere — any client can talk SMTP/IMAP.
- **Con:** Cleartext paths and open relays are still footguns; require TLS and authenticated submission.
- **Con:** Deliverability is a reputation game — self-hosting outbound at scale is hard.

## Comparison
- vs [[E mail server]]: ports and components here; architecture/ops depth there.
- vs chat ([[IRC]], Slack): email is store-and-forward with strong identity/DNS coupling.

## Mistakes to Avoid
- Confusing port 25 (relay) with 587 (submission).
- Skipping PTR/SPF/DKIM and blaming the MTA software for spam folders.
- Disabling TLS on submission “for compatibility.”
- Leaving an open relay for convenience.
