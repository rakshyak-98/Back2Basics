[[SMTP]] [[DNS]] [[TLS (Transport Layer Security)]] [[mail server]] [[IMAP (Internet Message Access Protocol)]]

# E mail server

> An email server accepts SMTP, stores mailboxes, and serves messages to clients — treat it as a distributed system bounded by DNS authentication and reputation, not just open ports.

## Interview Relevance

Interviewers separate “run Postfix” from running a deliverable mail system: MX edge, queue, storage, IMAP access, and SPF/DKIM/DMARC alignment.

## Sources

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321) — deep-dive
- [Postfix documentation](http://www.postfix.org/documentation.html) — deep-dive
- [Dovecot documentation](https://doc.dovecot.org/) — overview

## Key Concepts

- **Edge / MX:** receive inbound SMTP; greylisting; SPF/DKIM/DMARC checks.
- **Routing:** alias expansion, transport maps, relay rules.
- **Storage:** Maildir or mbox per user; quotas; backups.
- **Access:** IMAP for sync; optional POP3; CalDAV/CardDAV adjacent.
- **Outbound:** queue, retry schedule, DKIM signing.

Same host can run all layers (small install) or split (SES for outbound, Dovecot for storage).

## Technical Details

```
Internet :25  → Postfix (mydestination, virtual mailboxes)
Clients :587  → Postfix submission (SASL auth) → Dovecot LMTP delivery
Clients :993  → Dovecot IMAP (Maildir ~/mail)
```

Without aligned **SPF**, **DKIM**, and **DMARC**, major providers throttle or reject mail. See [[servers/DSN records]].

Operational metrics to watch:

- Queue depth (`mailq`)
- Bounce rate and FBL complaints
- TLS version on inbound/outbound connections
- Greylist / RBL hits

## Real-World Applications

Self-hosted company mail, hybrid setups (local IMAP + cloud outbound), and on-call triage when mail queues grow.

**Example:** Residential ISP blocks outbound port 25 — submission must use authenticated 587 on a proper MTA, not direct MX delivery from a laptop.

## Pros/Cons or Trade-offs

- **Pro:** Full control over retention, routing, and compliance.
- **Con:** Reputation and DNS misconfiguration hurt deliverability more than software choice.
- **Con:** Operating all layers is expensive — many teams outsource outbound (SES) or the whole stack (Workspace/365).

## Comparison

- vs [[mail server]]: this note emphasizes architecture and operations; [[mail server]] covers protocol ports and component names.
- Protocol detail: [[SMTP]] and [[IMAP (Internet Message Access Protocol)]].

## Mistakes to Avoid

- Treating open ports as “mail works” without SPF/DKIM/DMARC alignment.
- Running an open relay — authenticate submission users.
- Ignoring queue depth and bounce rates until the IP is blocklisted.
- Strict DMARC with DKIM pass but SPF fail — understand alignment rules before enforcing `p=reject`.
