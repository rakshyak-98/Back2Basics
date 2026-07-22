[[nc]] [[nmap]] [[ss]] [[SMTP]] [[Linux network commands]]

# telnet

> One-line: **cleartext TCP client** — still the fastest manual probe for "does this port accept connections and speak text?" Mail debugging and legacy gear; never for secrets on untrusted networks.

## Mental model

`telnet host port` opens a **raw TCP session** and prints bytes to your terminal. It does not encrypt. For production checks, prefer [[nc]] `-zv` for port-only tests and `openssl s_client` for TLS. telnet shines when you need to **type protocol lines** (SMTP, HTTP/1.0, IMAP) interactively.

```
telnet mail 25  → 220 banner  →  you type EHLO/STARTTLS
telnet web 80   →  GET / HTTP/1.0  →  headers back
```

| Tool | Use when |
|------|----------|
| `telnet host port` | Interactive text protocol |
| `nc -zv host port` | Open/closed only |
| `openssl s_client -connect host:465` | TLS from the start (SMTPS, HTTPS debug) |
| `curl -v telnet://host:80` | HTTP with less typing |

## Standard config / commands

**Mail server smoke test (port 25, cleartext):**

```bash
telnet mail.example.com 25
# After connect:
EHLO test.example.com
MAIL FROM:<test@example.com>
RCPT TO:<you@example.com>
QUIT
```

**STARTTLS on port 587 (telnet then upgrade — awkward):**

```bash
# Easier: openssl for TLS
openssl s_client -connect mail.example.com:587 -starttls smtp
# Or SMTPS:
openssl s_client -connect mail.example.com:465 -quiet
```

**HTTP quick probe:**

```bash
telnet example.com 80
GET / HTTP/1.0
Host: example.com

# blank line — read response headers
```

**Port open (non-interactive — prefer nc):**

```bash
nc -zv mail.example.com 25
timeout 3 bash -c 'cat < /dev/null > /dev/tcp/mail.example.com/25' && echo open
```

**Local listen audit (what's bound):**

```bash
ss -lntup
sudo nmap -p 25,587,465 localhost
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` | `ss -lntp` on server | Service down; wrong port; not listening on interface |
| Hangs | Firewall DROP | [[nc]] with `-w 3`; fix SG/iptables path |
| Connect then close | TLS-only port | Use `openssl s_client` on 465/993/443 |
| Garbled characters | Binary protocol | Don't use telnet; use client library |
| EHLO rejected | Relay policy | Auth required; use authenticated submission |
| Works telnet, fails app | App TLS/cert config | Not a network issue — check app logs |

## Gotchas

> [!WARNING]
> **Credentials over telnet** — passwords visible on wire. SSH, TLS, or VPN only for auth.

> [!WARNING]
> **Modern distros omit telnet client** — `apt install telnet` or use `nc`/`openssl`.

- **Escape character** — Ctrl+] then `quit` to exit telnet session (not Ctrl+C alone in all states).
- **IPv6** — `telnet -6 host port` if available; or `nc -6`.

## When NOT to use

- **Remote admin** — use [[SSH]]; telnetd on servers should be absent/disabled.
- **Encrypted service validation** — openssl/curl, not cleartext telnet.
- **Automated monitoring** — use health checks; telnet scripts are brittle.

## Related

[[nc]] [[nmap]] [[ss]] [[SMTP]] [[Linux network commands]] [[SSH]]
