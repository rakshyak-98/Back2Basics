[[SMTP]] · [[DNS]] · [[TLS (Transport Layer Security)]] · [[mail server]] · [[E mail server]]

# E mail server

> An email server is the infrastructure that accepts SMTP, stores mailboxes, and serves messages to clients — treat it as a distributed system bounded by DNS authentication records and reputation, not just open ports.

---

## Logical layers

| Layer | Responsibility |
|-------|----------------|
| **Edge / MX** | Receive inbound SMTP, greylisting, SPF/DKIM/DMARC checks |
| **Routing** | Alias expansion, transport maps, relay rules |
| **Storage** | Maildir or mbox per user; quotas; backups |
| **Access** | IMAP for sync, optional POP3, CalDAV/CardDAV adjacent |
| **Outbound** | Queue, retry schedule, DKIM signing |

Same host can run all layers (small install) or split (SES for outbound, Dovecot for storage).

## Minimal Postfix + Dovecot pattern

```
Internet :25  → Postfix (mydestination, virtual mailboxes)
Clients :587  → Postfix submission (SASL auth) → Dovecot LMTP delivery
Clients :993  → Dovecot IMAP (Maildir ~/mail)
```

## Authentication records ([[DNS]])

Without aligned **SPF**, **DKIM**, and **DMARC**, major providers throttle or reject mail. See [[servers/DSN records]].

## Operational metrics

- Queue depth (`mailq`)
- Bounce rate and FBL complaints
- TLS version on inbound/outbound connections
- Greylist / RBL hits

## vs [[mail server]]

This note emphasizes **architecture and operations**; [[mail server]] covers protocol ports and component names. Cross-link [[SMTP]] and [[IMAP (Internet Message Access Protocol)]] for protocol detail.

## Recall

- Why is port 25 often blocked on residential ISP networks?
- What happens if DKIM passes but SPF fails under strict DMARC?

## Sources

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321)
- [Postfix documentation](http://www.postfix.org/documentation.html)
- [Dovecot documentation](https://doc.dovecot.org/)
