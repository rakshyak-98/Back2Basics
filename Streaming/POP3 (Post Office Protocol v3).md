[[SMTP]] [[mail server]] [[TLS (Transport Layer Security)]] [[DNS]]

# POP3 (Post Office Protocol v3)

> Simple mail retrieval — download-and-delete mental model; brief ops note and when **IMAP** wins — **RFC 1939**.

```txt
        POP3 (Post Office  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers ask about POP3 to see if you understand the pipeline role, failu…

## Sources
- [Wikipedia — POP3](https://en.wikipedia.org/wiki/POP3) — overview

## Key Concepts
- **Note:** **POP3** lets an MUA fetch mail from an MDA mailbox over TCP (110 plain, 995 …

| Command phase | Commands |
|---------------|----------|
| **Auth** | `USER`/`PASS` or `AUTH PLAIN`/`CRAM-MD5` |
| **Transaction** | `LIST`, `UIDL`, `RETR n`, `DELE n` |
| **Update** | Deletes committed on `QUIT` |

- **Note:** **versus IMAP:** POP3 is **offline-first, single-client**

## Technical Details
```txt
MUA ── TCP 995 ──► MDA (Dovecot/Courier)
       USER/PASS or AUTH
       LIST / RETR / DELE
       QUIT
```

### Test POP3 (swaks alternative — openssl)

```shell
openssl s_client -connect mail.example.com:995 -quiet
# After connect:
USER alice@example.com
PASS secret
LIST
RETR 1
QUIT
```

### Dovecot POP3

```shell
sudo doveadm auth test user@example.com
sudo doveadm mailbox status -u user@example.com ALL
grep -E 'pop3|protocols' /etc/dovecot/dovecot.conf
# protocols = imap pop3 lmtp
sudo systemctl status dovecot
```

### When POP3 is acceptable

```txt
✓ Legacy device / embedded scanner forwarding
✓ Single workstation, local mail archive (Thunderbird + leave on server OFF)
✓ Download agent piping to custom processor then delete

✗ Phone + laptop + webmail — use IMAP
✗ Shared mailbox team visibility
✗ Folder hierarchy / Sent sync across devices
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fails | `doveadm auth test`; SASL logs | Password scheme; app password; MFA not on POP |
| Mail "disappears" | Client deletes on fetch | Enable leave-on-server; switch IMAP |
| SSL errors | Cert hostname; chain | Renew [[certbot (letsencrypt)]]; full chain on 995 |
| Connection refused | `ss -tlnp \| grep 995` | Enable pop3 in Dovecot; firewall |
| Duplicate UID confusion | POP3 UIDL not stable across reinstall | Client re-downloads all — expected once |
| Large mailbox timeout | RETR entire 500MB message | IMAP partial fetch; server-side limits |

```shell
journalctl -u dovecot -f
sudo tail -f /var/log/mail.log
```

- **Mistake:** **Delete on QUIT**
- **Mistake:** **Plain POP3 port 110**
- **Mistake:** **Google/Outlook consumer**
- **Mistake:** **No server-side search**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **New product email client** — ship IMAP + OAuth2.
- **Con / skip when:** **Team shared inbox** — IMAP namespaces or web UI.
- **Con / skip when:** **Mobile-first** — IMAP IDLE push approximations win.

## Real-World Applications
- **Scenario:** Used wherever POP3 sits in an ingest → package → CDN → player path
