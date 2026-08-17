[[nc]] [[nmap]] [[ss]] [[SSH]] [[Linux network commands]]

# telnet

> Cleartext TCP client — fastest manual probe for “does this port accept connections and speak text?”





## Interview Relevance
Shows you can hand-talk SMTP/HTTP for debugging, know telnet is not encrypted, and prefer [[nc]] / `openssl s_client` for most modern checks.

## Sources
- [Wikipedia — Telnet](https://en.wikipedia.org/wiki/Telnet) — overview
- [RFC 854 — Telnet Protocol Specification](https://www.rfc-editor.org/rfc/rfc854) — deep-dive

## Core Definition
`telnet host port` opens a raw TCP session and prints bytes to your terminal. It does not encrypt. It shines when you type protocol lines interactively (SMTP, HTTP/1.0, IMAP).

## Key Concepts
- **Banner grab:** see the service hello — sanity check, not a scanner.
- **Escape:** Ctrl+] then `quit` to leave stuck sessions.
- **TLS:** use `openssl s_client` (with `-starttls` when needed), not cleartext telnet.
- **vs nc:** prefer [[nc]] `-zv` for open/closed-only tests and scripting.

## Technical Details
```
telnet mail 25  → 220 banner  →  you type EHLO/STARTTLS
telnet web 80   →  GET / HTTP/1.0  →  headers back
```

| Tool | Use when |
|------|----------|
| `telnet host port` | Interactive text protocol |
| `nc -zv host port` | Open/closed only |
| `openssl s_client -connect host:465` | TLS from the start |
| `curl -v telnet://host:80` | HTTP with less typing |

```bash
telnet mail.example.com 25
# EHLO / MAIL FROM / RCPT TO / QUIT

openssl s_client -connect mail.example.com:587 -starttls smtp
openssl s_client -connect mail.example.com:465 -quiet

telnet example.com 80
# GET / HTTP/1.0
# Host: example.com
# (blank line)

nc -zv mail.example.com 25
ss -lntup
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `ss -lntp` on server | Service down; wrong port; wrong bind |
| Hangs | Firewall DROP | `nc -w 3`; fix security group / iptables |
| Connect then close | TLS-only port | `openssl s_client` on 465/993/443 |
| Garbled characters | Binary protocol | Use a real client library |

## Real-World Applications
Mail relay debugging on port 25, legacy appliance consoles, and quick HTTP header peeks when curl is unavailable.

## Pros/Cons or Trade-offs
- **Pro:** Interactive protocol debugging with zero ceremony.
- **Con:** Cleartext; often not installed; brittle for automation.

## Comparison
- vs [[nc]]: nc is better for scripting and port probes.
- vs [[SSH]]: remote administration must never use telnetd.

## Mistakes to Avoid
- Sending passwords over telnet.
- Using telnet against TLS-only ports and calling the service “broken.”
- Leaving telnetd enabled on servers.
