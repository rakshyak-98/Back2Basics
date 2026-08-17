[[nc]] [[nmap]] [[ss]] [[SSH]] [[Linux network commands]]

# telnet

> Cleartext TCP client — fastest manual probe for “does this port accept connections and speak text?”

```txt
        telnet ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you can hand-talk SMTP/HTTP for debugging, know telnet is not encrypted…

## Sources
- [Wikipedia — Telnet](https://en.wikipedia.org/wiki/Telnet) — overview
- [RFC 854 — Telnet Protocol Specification](https://www.rfc-editor.org/rfc/rfc854) — deep-dive

## Key Concepts
- **Banner grab:** see the service hello — sanity check, not a scanner.
- **Escape:** Ctrl+] then `quit` to leave stuck sessions.
- **TLS:** use `openssl s_client` (with `-starttls` when needed), not cleartext telnet.
- **vs nc:** prefer [[nc]] `-zv` for open/closed-only tests and scripting.


- **Core:** `telnet host port` opens a raw TCP session and prints bytes to your terminal

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

## Mistakes to Avoid
- **Mistake:** Sending passwords over telnet
- **Mistake:** Using telnet against TLS-only ports and calling the service “bro…
- **Mistake:** Leaving telnetd enabled on servers

## Pros/Cons or Trade-offs
- **Pro:** Interactive protocol debugging with zero ceremony.
- **Con:** Cleartext; often not installed; brittle for automation.

## Comparison
- vs [[nc]]: nc is better for scripting and port probes.
- vs [[SSH]]: remote administration must never use telnetd.


### Use cases
- Mail relay debugging on port 25, legacy appliance consoles, and quick HTTP he…
