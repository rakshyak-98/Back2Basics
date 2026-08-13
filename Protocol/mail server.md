[[SMTP]] · [[IMAP (Internet Message Access Protocol)]] · [[DNS]] · [[TLS (Transport Layer Security)]] · [[E mail server]]

# mail server

> A mail server stack receives, routes, stores, and delivers email using SMTP between servers and often IMAP or POP3 for clients — delivery fails when DNS (MX/SPF/DKIM/DMARC) or TLS policy does not match what receivers expect.

---

## Components

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

## DNS requirements

See [[servers/DSN records]]:

- **MX** — where mail for the domain goes
- **SPF / DKIM / DMARC** — anti-spoofing and reputation
- **PTR** — reverse DNS for sending IP

## Popular software

| Software | Role |
|----------|------|
| **Postfix** | MTA (send/receive) |
| **Exim** | MTA (Debian default historically) |
| **Dovecot** | IMAP/POP3 server |
| **Rspamd / SpamAssassin** | Filtering |
| **OpenDKIM / Rspamd DKIM** | Signing |

Managed: Google Workspace, Microsoft 365, Amazon SES.

## Security baseline

- Require **TLS** for submission and prefer **DANE** / **MTA-STS** where supported
- Disable open relay — authenticate submission users
- Rate limit outbound mail; monitor bounce rates

## Debugging

```bash
dig MX example.com +short
openssl s_client -connect mail.example.com:25 -starttls smtp
swaks --to user@example.com --from test@example.com --server mail.example.com
```

## Recall

- What is the difference between port 25 and 587?
- Which DNS records affect whether your mail lands in spam?

## Sources

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321)
- [RFC 3501 — IMAP](https://datatracker.ietf.org/doc/html/rfc3501)
- [Google — Email sender guidelines](https://support.google.com/mail/answer/81126)
