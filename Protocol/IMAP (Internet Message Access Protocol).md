[[SMTP]] [[E mail server]] [[mail server]] [[TCP]] [[TLS (Transport Layer Security)]]

# IMAP (Internet Message Access Protocol)

> IMAP lets mail clients synchronize folders and flags with a server-side mailbox over TCP — messages stay on the server so multiple devices share the same state (unlike typical POP3).





## Interview Relevance
Interviewers contrast IMAP with POP3 and SMTP: who stores mail, which port is preferred, and what `\Seen` / IDLE mean for multi-device sync.

## Sources
- [RFC 3501 — IMAP4rev1](https://datatracker.ietf.org/doc/html/rfc3501) — deep-dive
- [RFC 2177 — IMAP IDLE](https://datatracker.ietf.org/doc/html/rfc2177) — overview
- [RFC 8314 — Use of TLS for Email](https://datatracker.ietf.org/doc/html/rfc8314) — overview

## Key Concepts
- **Server-side mailbox:** folders, UIDs, flags (`\Seen`, `\Answered`), partial MIME fetch.
- **Multi-device sync:** flag and folder changes propagate to every client.
- **IDLE:** server push of new mail; mobile often polls instead for battery.
- **Pair with SMTP:** 587 sends; 993 reads — often same credentials via SASL or OAuth2.

## Technical Details
```
Client                    Server
  LOGIN user pass
  SELECT INBOX
  FETCH 1 (FLAGS BODY[HEADER.FIELDS (FROM SUBJECT)])
  STORE 1 +FLAGS (\Seen)
  IDLE                    (push new mail notification)
```

| Port | Mode |
|------|------|
| **143** | Cleartext + optional STARTTLS |
| **993** | Implicit TLS (IMAPS) — prefer this |

| IMAP | POP3 |
|------|------|
| Server-side folders | Usually download-and-delete |
| Multi-device sync | Single-device oriented |
| Higher server storage | Offloads to client |

```bash
openssl s_client -connect imap.example.com:993
# a001 LOGIN user pass
# a002 LIST "" "*"
```

## Real-World Applications
Desktop + phone mail clients against Dovecot, Exchange, or Workspace IMAP endpoints.

**Example:** Marking a message read on the phone sets `\Seen`; the desktop client refreshes and shows it read without re-downloading the body.

## Pros/Cons or Trade-offs
- **Pro:** Correct model for multi-device users and shared server search.
- **Con:** Higher server storage and I/O than POP3.
- **Con:** Long IDLE connections and mobile battery trade-offs.

## Comparison
- vs POP3: IMAP keeps state on the server; POP3 is download-oriented.
- vs [[SMTP]]: SMTP moves mail between MTAs; IMAP accesses the stored mailbox.

## Mistakes to Avoid
- Preferring port 143 without STARTTLS in production.
- Expecting POP3-style “delete after download” semantics from IMAP.
- Forgetting that `\Seen` is shared state — “unread counts” surprise users across devices.
