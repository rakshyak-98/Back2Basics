[[SMTP]] [[DNS]] [[TLS (Transport Layer Security)]] [[mail server]] [[IMAP (Internet Message Access Protocol)]]

# E mail server

> An email server accepts SMTP, stores mailboxes, and serves messages to clients — treat it as a distributed system bounded by DNS authentication and reputation, not just open ports.

```txt
        E mail server ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers separate “run Postfix” from running a deliverable mail system: M…

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

- **Note:** Same host can run all layers (small install) or split (SES for outbound, Dove…

## Technical Details
```
Internet :25  → Postfix (mydestination, virtual mailboxes)
Clients :587  → Postfix submission (SASL auth) → Dovecot LMTP delivery
Clients :993  → Dovecot IMAP (Maildir ~/mail)
```

- Without aligned **SPF**, **DKIM**, and **DMARC**, major providers throttle or…
- See [[servers/DSN records]].

- Operational metrics to watch:

- Queue depth (`mailq`)
- Bounce rate and FBL complaints
- TLS version on inbound/outbound connections
- Greylist / RBL hits

## Mistakes to Avoid
- **Mistake:** Treating open ports as “mail works” without SPF/DKIM/DMARC align…
- **Mistake:** Running an open relay — authenticate submission users
- **Mistake:** Ignoring queue depth and bounce rates until the IP is blocklisted
- **Mistake:** Strict DMARC with DKIM pass but SPF fail

## Pros/Cons or Trade-offs
- **Pro:** Full control over retention, routing, and compliance.
- **Con:** Reputation and DNS misconfiguration hurt deliverability more than software choice.
- **Con:** Operating all layers is expensive — many teams outsource outbound (SES) or the whole stack (Workspace/365).

## Comparison
- vs [[mail server]]: this note emphasizes architecture and operations
- Protocol detail: [[SMTP]] and [[IMAP (Internet Message Access Protocol)]].


### Use cases
- Self-hosted company mail, hybrid setups (local IMAP + cloud outbound), and on…

- **Example:** Residential ISP blocks outbound port 25
