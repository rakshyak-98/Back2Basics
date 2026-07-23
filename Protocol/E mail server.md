[[SMTP]] [[DNS]] [[TLS (Transport Layer Security)]]

# E mail server

> One-line: the MTA/MDA/MUA stack that accepts, routes, stores, and retrieves mail — debug deliverability at each hop.

## Mental model

Email crosses distinct roles. Confusing them causes misconfigured ports and wrong logs.

```
┌─────┐   submit    ┌─────┐   relay    ┌─────┐   deliver   ┌─────┐   fetch    ┌─────┐
│ MUA │ ──587──────►│ MSA │ ─────────► │ MTA │ ────────────► │ MDA │ ◄──────── │ MUA │
│     │  (Thunderbird│     │   SMTP 25  │     │  LMTP/local │     │ IMAP/POP  │     │
└─────┘   webmail)  └─────┘            └─────┘             └─────┘           └─────┘
```

| Role | Name | Job | Typical port |
|------|------|-----|--------------|
| **MUA** | Mail User Agent | Compose/read (Outlook, mutt, web UI) | — |
| **MSA** | Mail Submission Agent | Authenticated client injection | 587 STARTTLS |
| **MTA** | Mail Transfer Agent | Route/relay between domains | 25 |
| **MDA** | Mail Delivery Agent | Drop into mailbox (Maildir/mbox) | local / LMTP |
| **MX** | DNS record | Points to receiving MTA for domain | DNS |

Common stacks: **Postfix** (MTA) + **Dovecot** (MDA/IMAP) + **Rspamd/Amavis** (filter) + **OpenDKIM** (signing).

## Standard config / commands

```shell
# Postfix queue / status
sudo systemctl status postfix
mailq
postqueue -p
postsuper -d ALL deferred    # careful — deletes deferred queue

# Postfix logs
sudo tail -f /var/log/mail.log
journalctl -u postfix -f

# Test local delivery
echo "test body" | mail -s "subject" user@localhost

# Test outbound via submission
swaks --to external@gmail.com --from you@yourdomain.com \
  --server mail.yourdomain.com:587 --auth-user you@yourdomain.com --tls

# Dovecot IMAP
sudo doveadm mailbox list -u user@example.com
sudo doveadm fetch 'hdr.subject' mailbox INBOX ALL -u user@example.com

# DNS prerequisites
dig +short example.com MX
dig +short example.com TXT               # SPF
dig +short default._domainkey.example.com TXT
dig +short _dmarc.example.com TXT
dig +short -x $(curl -s ifconfig.me)     # reverse PTR for sending IP
```

### Ops checklist (new domain / server)

- [ ] **A/AAAA** for `mail.example.com` (SMTP banner host)
- [ ] **MX** points to MTA with priority
- [ ] **SPF** TXT includes all sending IPs/providers
- [ ] **DKIM** key published; MTA signs outbound
- [ ] **DMARC** policy (`p=none` → monitor, then `quarantine`/`reject`)
- [ ] **PTR/rDNS** matches SMTP EHLO hostname
- [ ] **TLS cert** valid for submission/IMAP hostnames
- [ ] **Firewall**: 25/587/993 open as needed; block 25 outbound on app servers not sending mail
- [ ] **Relay policy**: authenticated users only on 587; no open relay on 25
- [ ] **Queue monitoring** + alert on backlog depth

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mail stuck in queue | `mailq`; defer reason in log | Fix DNS/MX; clear RBL; auth to smart host |
| Users can't send | MSA auth / TLS | Verify SASL creds; cert chain on 587 |
| Users can't receive | MX DNS; MTA listening :25 | Fix MX; open SG; check `postconf inet_interfaces` |
| IMAP works, no outbound | Separate submission vs relay config | `relayhost` for smart host; SASL maps |
| All mail spam-foldered | SPF/DKIM/DMARC headers | See [[SMTP]] triage table |
| Disk full | `/var/spool/postfix`; Maildir size | Expire queue; quota; expand volume |
| Relay denied for world | `smtpd_recipient_restrictions` | `permit_mynetworks, reject_unauth_destination` |
| TLS handshake fail on Apple Mail | Cert chain / intermediate | Install full chain; use Let's Encrypt |

## Gotchas

> [!WARNING]
> **Open relay** on port 25 = immediate blacklisting. Default Postfix is safe — custom `mynetworks` too wide is the usual mistake.

- **Separate hostname for mail** (`mail.example.com`) from web — cert and PTR must align with SMTP greeting.
- **Virtual domains** need explicit maps (`virtual_mailbox_domains`) — not implicit from system users.
- **Backup MX** with lower priority still needs anti-spam — spammers target stale backup MX.
- **Log rotation** — mail.log fills disks silently on attack bursts.

## When NOT to use

- Product email at scale → managed [[SMTP]] relay (SES, SendGrid) beats running your own MTA reputation.
- Dev-only fake SMTP → Mailhog/Mailpit locally; don't point at production MX.

## Related

[[SMTP]] · [[DNS]] · [[DNS zone]] · [[TLS (Transport Layer Security)]]
