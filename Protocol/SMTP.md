[[E mail server]] [[mail server]] [[TCP]] [[DNS]] [[TLS (Transport Layer Security)]]

# SMTP

> Simple Mail Transfer Protocol moves email between Mail Transfer Agents with text commands over TCP — 587 + STARTTLS for client submission; 25 for server-to-server relay.

```txt
        SMTP ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe envelope versus headers, submission versus relay ports, an…

## Sources
- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321) — deep-dive
- [RFC 5322 — Internet Message Format](https://datatracker.ietf.org/doc/html/rfc5322) — overview
- [RFC 6409 — Message Submission](https://datatracker.ietf.org/doc/html/rfc6409) — overview

## Key Concepts
- **Text command session:** EHLO, MAIL FROM, RCPT TO, DATA, QUIT.
- **Envelope vs headers:** envelope routes and bounces
- **Ports:** 25 relay, 587 authenticated submission, 465 legacy implicit TLS.
- **DNS:** MX for delivery; SPF checks envelope sender; DKIM signs headers.

## Technical Details
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

| Port | Use |
|------|-----|
| **25** | MTA-to-MTA delivery |
| **587** | Message submission (authenticated users) |
| **465** | Legacy SMTPS (implicit TLS); still seen in the wild |

- Prefer **587 + STARTTLS** or **MTA-STS** policies for modern deployments.

- Extensions: **SIZE**, **PIPELINING**, **SMTPUTF8** ([RFC 6531](https://datatr…

```bash
dig MX example.com +short
openssl s_client -connect mx.example.com:25 -starttls smtp
```

## Mistakes to Avoid
- **Mistake:** Using port 25 for end-user submission
- **Mistake:** Trusting the `From:` header as proof of sender identity
- **Mistake:** Skipping STARTTLS on submission “because the LAN is trusted.”

## Pros/Cons or Trade-offs
- **Pro:** Universal interoperability — every domain speaks SMTP.
- **Con:** Open relays and spoofable headers without SPF/DKIM/DMARC.
- **Con:** Residential networks often block outbound 25 — clients must use submission.

## Comparison
- vs [[IMAP (Internet Message Access Protocol)]]: SMTP sends/relays; IMAP reads stored mail.
- vs HTTP APIs (SendGrid/SES): still often SMTP under the hood or a proprietary REST façade over th…


### Use cases
- Application transactional mail, corporate outbound MTAs, and inbound MX accep…

- **Example:** A web app submits via authenticated 587 to Postfix
