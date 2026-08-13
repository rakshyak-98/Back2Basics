[[E mail server]] · [[mail server]] · [[TCP]] · [[DNS]] · [[TLS (Transport Layer Security)]]

# SMTP

> Simple Mail Transfer Protocol moves email between Mail Transfer Agents using text commands over TCP — port 587 with STARTTLS is the standard client submission path; port 25 remains server-to-server relay.

---

## Session flow

```
Client                          Server
  EHLO client.example
  <---------------------------  250-server.example
  STARTTLS
  <---------------------------  220 Ready
  [TLS handshake]
  EHLO client.example
  MAIL FROM:<sender@example.com>
  RCPT TO:<recipient@example.org>
  DATA
  ...message headers + body...
  .
  QUIT
```

Defined in [RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321); message format in [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322).

## Ports

| Port | Use |
|------|-----|
| **25** | MTA-to-MTA delivery |
| **587** | Message submission (authenticated users) |
| **465** | Legacy SMTPS (implicit TLS); still seen in the wild |

Prefer **587 + STARTTLS** or **MTA-STS** policies for modern deployments.

## Envelope vs header

- **Envelope** — `MAIL FROM` / `RCPT TO` (routing, bounces)
- **Headers** — `From:`, `To:` (what users see; can differ — phishing)

Receivers validate **SPF** against envelope sender domain, **DKIM** on signed headers.

## DNS dependencies

- **MX** — where to deliver `@domain`
- **SPF, DKIM, DMARC** — [[servers/DSN records]]

```bash
dig MX example.com +short
openssl s_client -connect mx.example.com:25 -starttls smtp
```

## Extensions

- **SIZE** — max message bytes
- **PIPELINING** — batch commands
- **SMTPUTF8** — internationalized addresses ([RFC 6531](https://datatracker.ietf.org/doc/html/rfc6531))

## Recall

- What is the difference between MAIL FROM and the From header?
- When should clients use port 587 instead of 25?

## Sources

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321)
- [RFC 6409 — Message Submission](https://datatracker.ietf.org/doc/html/rfc6409)
