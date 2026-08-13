[[SMTP]] · [[E mail server]] · [[mail server]] · [[TCP]] · [[TLS (Transport Layer Security)]]

# IMAP (Internet Message Access Protocol)

> IMAP lets mail clients synchronize folders and flags with a server-side mailbox over TCP — unlike POP3, messages stay on the server and multiple devices see the same state.

---

## Model

[IMAP4rev1 (RFC 3501)](https://datatracker.ietf.org/doc/html/rfc3501) maintains **mailbox hierarchy** (folders), **UIDs**, **flags** (`\Seen`, `\Answered`), and **partial fetch** of MIME parts.

```
Client                    Server
  LOGIN user pass
  SELECT INBOX
  FETCH 1 (FLAGS BODY[HEADER.FIELDS (FROM SUBJECT)])
  STORE 1 +FLAGS (\Seen)
  IDLE                    (push new mail notification)
```

## Ports

| Port | Mode |
|------|------|
| **143** | Cleartext + optional STARTTLS |
| **993** | Implicit TLS (IMAPS) — prefer this |

## vs POP3

| IMAP | POP3 |
|------|------|
| Server-side folders | Usually download-and-delete |
| Multi-device sync | Single-device oriented |
| Higher server storage | Offloads to client |

## IDLE extension

`IDLE` ([RFC 2177](https://datatracker.ietf.org/doc/html/rfc2177)) holds connection open for server push — mobile clients often use periodic polling instead to save battery.

## Common with [[SMTP]]

- **SMTP** (587) sends mail
- **IMAP** (993) reads mail
- Same credentials via Dovecot SASL or OAuth2 (modern providers)

## Debugging

```bash
openssl s_client -connect imap.example.com:993
# a001 LOGIN user pass
# a002 LIST "" "*"
```

## Recall

- Why does IMAP suit mobile plus desktop better than POP3?
- What does the `\Seen` flag change for other clients?

## Sources

- [RFC 3501 — IMAP4rev1](https://datatracker.ietf.org/doc/html/rfc3501)
- [RFC 8314 — Use of TLS for Email](https://datatracker.ietf.org/doc/html/rfc8314)
