[[Protocol]] [[E mail server]] [[SMTP]] [[IMAP (Internet Message Access Protocol)]] [[DNS]]

# mail server

> Mail server — the box (or service) that accepts, routes, stores, and lets clients fetch email — SMTP out, IMAP/POP in.

---

## Mental model

**Say it in one breath:** “Mail server” is a role bundle: submission/relay ([[SMTP]]), mailbox store, and retrieval ([[IMAP (Internet Message Access Protocol)]] / POP3) — often split across MSA/MTA/MDA. See [[E mail server]] for the role diagram.

```txt
MUA ──587 SMTP──► MSA/MTA ──25──► far MTA ──► MDA ◄──993 IMAP── MUA
                     │
              SPF/DKIM/DMARC in [[DNS]]
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **SMTP** | Send / relay | “Clients submit on 587; servers talk 25.” |
| **IMAP** | Read mail on server | “Multi-device needs IMAP, not POP.” |
| **POP3** | Download (often delete) | “Single device, leave-or-delete semantics.” |
| **MX** | DNS “who receives mail” | “No MX → others don’t know where to deliver.” |
| **MSA vs MTA** | Submission vs server-to-server | “Don’t expose open relay on 25.” |

| Protocol | Job | Typical secure port | Keeps mail on server? |
|----------|-----|---------------------|------------------------|
| **SMTP** | Send / relay | 587 STARTTLS, 465 | No (transfer only) |
| **IMAP** | Fetch + sync | 993 | Yes |
| **POP3** | Fetch | 995 | Usually no |

---

## Standard config / commands

```bash
# DNS prerequisites
dig +short MX example.com
dig +short TXT example.com   # SPF
dig +short TXT default._domainkey.example.com  # DKIM

# Submission smoke test
openssl s_client -connect mail.example.com:587 -starttls smtp

# IMAP smoke test
openssl s_client -connect mail.example.com:993
```

application configuration knobs (any language): host, port, TLS mode, username/password or OAuth2 — **separate** SMTP (send) from IMAP (read).

| Knob | Why it matters |
|------|----------------|
| 587 vs 25 | Clients use submission; 25 is often blocked on residential ISPs |
| Auth + TLS | Open/unencrypted submission = spam cannon |
| Reverse DNS / PTR | Many receivers reject mail without matching PTR |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can receive, can’t send | 587/auth/TLS | Fix submission creds; try 465 |
| Sent mail lands in spam | SPF/DKIM/DMARC + PTR | Align DNS; sign DKIM; fix HELO/PTR |
| “Relay access denied” | Not authenticated on 25/587 | Authenticate; don’t use open relay |
| IMAP sync stuck | Quota / IDLE / cert | Raise quota; fix cert SAN; check logs |
| MX points wrong host | `dig MX` | Fix MX to current MDA/MTA hostname |
| Timeout from home ISP | Port 25 blocked | Use provider MSA on 587 |

---

## Gotchas

> [!WARNING]
> **Running your own mail is reputation ops** — IP warm-up, blocklists, and feedback loops matter more than Postfix syntax.

> [!WARNING]
> **SMTP auth on the wrong port** — submission (587) ≠ MX inbound (25). Mixing them causes mysterious 550s.

> [!WARNING]
> **“Mail server” in SaaS** — SES/SendGrid/Workspace are still SMTP/IMAP endpoints; DNS auth records still required.

---

## When NOT to use

- **Transactional application mail only** — use a provider API (SES, Postmark); skip running Postfix.
- **Chat / realtime** — not email; use WebSocket or [[WebRTC]].
- **Guaranteed instant delivery UX** — email is store-and-forward with greylisting delays.

---

## Related

[[E mail server]] [[SMTP]] [[IMAP (Internet Message Access Protocol)]] [[DNS]] [[DSN records]] [[TLS (Transport Layer Security)]]
