[[telnet]] [[ss]] [[nmap]] [[half-open connections]] [[Linux network commands]]

# nc (netcat)

> One-line: **Swiss-army TCP/UDP socket tool** — prove connectivity, banner-grab, and one-shot port checks faster than full scans. Not a replacement for proper TLS or auth testing.

## Mental model

`nc` opens a **raw socket** (client or listener). For ops, the common pattern is **connect probe**: did SYN get SYN-ACK (port open) or RST/timeout (closed/filtered)? OpenBSD netcat (`nc`) and nmap's `ncat` differ in flags — know which is installed.

```
Client: nc -zv host 443  →  SYN → SYN-ACK = open
Listener: nc -lk 8080    →  accept connections (debug/mock server)
```

| Variant | `-z` scan | `-l` listen | Notes |
|---------|-----------|-------------|-------|
| OpenBSD `nc` | yes | `-l` | Common on Debian/Ubuntu |
| GNU netcat | `-z` | `-l -p PORT` | `-p` required on listen |
| `ncat` (nmap) | `-z` | `-l` | `--ssl`, `--proxy |

## Standard config / commands

**Port reachability (daily debug):**

```bash
# Single port — verbose zero-I/O scan
nc -zv example.com 443

# Multiple ports
nc -zv example.com 22 80 443 3389

# Timeout (don't hang on firewall DROP)
nc -zv -w 3 example.com 22

# UDP (often false negative — no RST)
nc -zuv example.com 53
```

**Banner / protocol smoke test:**

```bash
# HTTP headers
printf 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n' | nc -w 3 example.com 80

# SMTP greeting
nc -w 5 mail.example.com 25
```

**Temporary listener (debug webhook):**

```bash
nc -lk 8080   # OpenBSD; GNU: nc -l -p 8080
# Ctrl+C when done — don't leave on prod hosts
```

**File transfer (emergency, no encryption):**

```bash
# Receiver
nc -l 9000 > received.bin
# Sender
nc host 9000 < file.bin
```

**Compare with [[ss]] on local box:**

```bash
ss -lntp | grep :8080    # Is anything actually listening locally?
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` | Service down or wrong port | `ss -lntp`; start unit; fix bind address |
| Hangs then timeout | Firewall DROP | Trace path; security group; `-w` |
| `nc -zv` open but app fails | TLS/HTTP layer | Use `openssl s_client`, curl — nc is TCP only |
| UDP "open" unreliable | Normal for UDP | Use `dig @host` or app-specific probe |
| Works from laptop, not server | Egress firewall | Compare `nc` from both sides |

## Gotchas

> [!WARNING]
> **`nc -l` on production** — accidental backdoor; binds 0.0.0.0 by default on some builds. Bind `127.0.0.1` only if supported.

> [!WARNING]
> **Open vs reachable** — `nc -zv` proves TCP handshake, not valid TLS cert or HTTP 200.

- **IPv6** — `-6` flag; `nc -zv [::1] 22` for local v6.
- **Script portability** — GNU vs OpenBSD flag differences break CI; prefer `timeout 3 bash -c '</dev/tcp/host/port'` for bash-only checks.
- **IDS noise** — rapid `nc` scans trigger alerts; use [[nmap]] with policy approval internally.

## When NOT to use

- **Encrypted service validation** — use `openssl s_client`, `curl -vk`, not plain nc.
- **Production load testing** — use proper tools; naive nc loops are indistinguishable from abuse.
- **Authoritative port audit** — use [[nmap]] with documented scope.

## Related

[[telnet]] [[ss]] [[nmap]] [[half-open connections]] [[Linux network commands]]
