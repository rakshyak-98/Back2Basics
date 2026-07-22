[[SMTP]] [[POP3 (Post Office Protocol v3)]] [[E mail server]] [[TCP]]

# IMAP (Internet Message Access Protocol)

> One-line: mailbox protocol — messages stay on server; folders, flags, UID sync; clients use 143/STARTTLS or 993/IMAPS.

## Mental model

IMAP lets MUAs **read and organize mail on the server** (unlike [[POP3 (Post Office Protocol v3)]] which typically downloads and deletes). Server holds canonical state; client syncs flags (`\Seen`, `\Deleted`), folders, and UIDs. Multiple devices see the same mailbox.

```
Client ──IMAP──► MDA (Dovecot, Cyrus, Exchange)
   │                  │
   ├── SELECT INBOX   ├── FETCH headers/body (partial)
   ├── UID SEARCH     ├── STORE flags
   └── IDLE (push)    └── APPEND sent mail
```

Modern flow: **587 [[SMTP]]** to send, **993 IMAPS** to read. Auth: LOGIN/PLAIN over TLS, OAuth2 (Gmail/365).

## Standard config / commands

### Ports & TLS

| Port | Mode |
|------|------|
| 143 | STARTTLS (upgrade to TLS) |
| 993 | Implicit TLS (IMAPS) |

### Manual session (debug)

```bash
openssl s_client -connect imap.example.com:993 -quiet
# a001 LOGIN user password
# a002 LIST "" "*"
# a003 SELECT INBOX
# a004 FETCH 1 (UID FLAGS BODY[HEADER.FIELDS (FROM SUBJECT)])
# a005 LOGOUT
```

STARTTLS on 143:

```bash
openssl s_client -connect imap.example.com:143 -starttls imap
```

### Common commands

| Command | Purpose |
|---------|---------|
| CAPABILITY | Server features |
| LOGIN / AUTHENTICATE | Auth |
| SELECT / EXAMINE | Open mailbox (rw / ro) |
| FETCH | Retrieve parts |
| UID SEARCH | Query UNSEEN, SINCE, etc. |
| STORE | Set flags |
| IDLE | Server push new mail (long-lived) |
| MOVE / COPY | RFC 6851 folder ops |

### Dovecot snippet (server)

```conf
protocols = imap
ssl = required
mail_location = maildir:~/Maildir
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failed | App password; OAuth | Enable IMAP in provider; correct token scope |
| Certificate error | Hostname mismatch | Full SAN cert; use correct server name |
| Empty INBOX on one client | Wrong folder namespace | LIST folders; prefix INBOX |
| Slow sync mobile | FETCH entire body | CONDSTORE/QRESYNC; partial FETCH |
| IDLE disconnects | NAT/firewall timeout | Client reconnect; TCP keepalive |
| Messages "duplicate" | POP3 + IMAP mixed | Pick one protocol per account |
| Login plain rejected | Secure auth required | TLS first; OAuth2 |

## Gotchas

> [!WARNING]
> **PLAIN without TLS** — credentials leak; always TLS or localhost.

> [!WARNING]
> **Deleting only local** — must `\Deleted` + EXPUNGE or MOVE to Trash on server.

> [!WARNING]
> **Provider rate limits** — bulk FETCH triggers throttling; batch UIDs.

## When NOT to use

- **Offline-first archive download only** — POP3 or one-shot migration tool simpler.
- **Transactional app notifications** — use webhooks/API, not mailbox polling.

## Related

[[POP3 (Post Office Protocol v3)]] [[SMTP]] [[E mail server]] [[Security/TLS (Transport Layer Security)]]
